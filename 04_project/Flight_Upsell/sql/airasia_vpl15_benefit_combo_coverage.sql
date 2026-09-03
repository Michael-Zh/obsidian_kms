-- =============================================================================
-- Benefit-Combo Coverage — Non-Brand Fallback Cross-Check (VPL15 / VP20 supply)
-- =============================================================================
-- Purpose : Measure supply-side coverage of airline products that carry NO
--           stable brand mapping, using ACTUAL fare benefit fields (checked
--           baggage weight + refund/change policy + seat selection) instead of
--           brand name.
--           This is the brand-agnostic fallback for supply coverage: it stays
--           consistent even when the airline rebrands the same product (see
--           brand-name caveat below).
--
-- Deliverables (per date partition, engine = SPARK3):
--   Query 1  VPL15 ("value pack lite 15kg") and VP20 ("value pack") brand-name
--            coverage — pre (appeared) vs post (output='true').
--   Query 2  Full benefit-combo matrix: bag_bucket x flex_combo, pre vs post.
--   Query 3  Brand-agnostic 15kg / 20kg checked-bag coverage (the stable
--            cross-check, comparable across dates despite the rebrand).
--   Query 4  Upsell headroom: among VPL15 searches, % that also surface a
--            20kg+ checked-bag fare (the VP20 upsell target).
--
-- Tables  : dwflt.edw_rsc_engine_paimon_agg_intl_compare_result_log_di (paimon)
-- Engine  : SPARK3 ONLY. (HIVE cannot read paimon; STARROCKS_HIVE times out.)
-- Parameters: <D> — partition date (STRING 'YYYY-MM-DD').
-- Runtime : ~1-3 min per query on one day (~500M rows for sch_type 14 alone).
-- Owner   : Michael (MZ)
-- =============================================================================
--
-- VERIFIED SCHEMA (DESCRIBE, 2026-09-02) — actual column names on the paimon
-- table DIFFER from the task brief's camelCase. Use the names below:
--   requesttype        -> sch_type                 (STRING; 14=middle reverse
--                                                   search, 24=..., 9=preload)
--   brandname          -> brand_name               (STRING; multi-seg joined ';'/'|')
--   checkedbaggagedetail -> checked_baggage_detail (STRING; see parsing below)
--   handbaggagedetail  -> hand_baggage_detail      (carry-on)
--   carryonbaggagedetail-> carryon_baggage_detail  (carry-on)
--   refundfeatures     -> rfd_feature (agg) / rfd_feature_split (per-ticket)
--   changefeatures     -> chg_feature (agg) / chg_feature_split (per-ticket)
--   brandtier          -> brand_tier               (STRING; also ccom_brand_tier)
--   output             -> output                   (STRING 'true'/'false')
--   traceid / parent_traceid / vc / d             (all STRING; d is partition)
--
-- FILTERS:
--   sch_type IN ('14','24')  — keep; '9' = preload, EXCLUDE.
--
-- CHECKED-BAG WEIGHT PARSING (VERIFIED):
--   checked_baggage_detail = "<bag-part>;<dim-part>"
--     bag-part  = segments joined by '|', each "<seg>,<pieces>,<weight_kg>,<?>"
--     weight_kg = the 3rd comma field (index 2) of each segment entry.
--   Examples:
--     "1,-1,15,15;1,319&..."                     -> 15kg  (VPL15, 1 segment)
--     "1,-1,20,20|2,-1,20,20;1,..|2,.."          -> 20kg  (Value Pack, 2 segment)
--     weight 0 or -1  = no checked bag.
--   MAX weight is taken across segments (documented approximation: complex
--   multi-airline interline rows bundle multiple fare options, so MAX reads as
--   "best checked-bag weight offered in that row").
--
-- FLEXIBILITY (rfd_feature / chg_feature):
--   refundable  = rfd_feature LIKE '%refund%'  AND NOT LIKE '%nonrefund%'
--   changeable  = chg_feature LIKE '%change%'  AND NOT LIKE '%nonchange%'
--   'NAN' = unknown -> treated as NOT flexible (e.g. some AK rows).
--
-- SEAT SELECTION (VERIFIED 2026-09-02):
--   There is NO standalone seat column and ext_columns_map has no seat key.
--   Seat selection is encoded inside price_json (NOT a dedicated column):
--     price_json -> ticketPackageProductList[*] -> serviceRefs[*] ->
--                   brandFareRefs[*] -> brandService -> serviceDetails[{key,value}]
--   Seat selection = a serviceDetails element {"key":"Seat","value":"Standard"}.
--     - "Value Pack" / "Value Pack Lite 15kg"  -> has Seat (seat selection bundled)
--     - "Regular Fare with Luggage 15/20"      -> NO Seat (baggage only)
--   Detector: instr(price_json, '"key":"Seat"') > 0  (exact string, no spaces).
--   Related: same JSON has ancillariesInfo {hasBaggageService, unFreeBaggage,
--   checkInServiceStatus}.  xprd_bundle_detail is masked as "****" (unusable).
--
-- DATA CAVEATS:
--   1) PARTITIONS: NOT just two. Actual range is daily 2026-05-07 .. 2026-09-01
--      (118 partitions). There is NO 2026-01-19 partition (brief was stale).
--   2) PARALLEL PRODUCTS (corrected interpretation, NOT a rebrand):
--      "Regular Fare with Luggage 15/20" = checked baggage ONLY, NO seat.
--      "Value Pack Lite 15kg" / "Value Pack" = NEW fares running IN PARALLEL
--      that add seat selection (and a meal) on top of baggage. Both families
--      coexist on 2026-08-12. Bag-weight alone merges them -> use the seat
--      dimension (Query 5/6) to tell them apart.
--   3) bag-weight coverage (Query 3) is BROADER than the VPL15/VP20 product:
--      15kg/20kg are common weights across many airlines, so the fallback
--      captures non-AirAsia fares too — use Query 1 for product-specific,
--      Query 3 for the stable cross-check.
--   4) SEAT DETECTION COST: instr(price_json, '"key":"Seat"') scans a ~50KB
--      JSON, so only run it on the rows you need (Query 6 gates it behind
--      kg IN (15,20); Query 5 restricts to AirAsia vc). Full-table seat scans
--      time out the adhoc engine.
-- =============================================================================

-- =============================================================================
-- QUERY 1 — VPL15 / VP20 brand-name coverage (pre vs post)
-- =============================================================================
WITH base AS (
  SELECT traceid, output, brand_name
  FROM dwflt.edw_rsc_engine_paimon_agg_intl_compare_result_log_di
  WHERE d = '<D>'                -- e.g. '2026-08-12'
    AND sch_type IN ('14','24')  -- exclude '9' (preload)
),
enriched AS (
  SELECT
    traceid,
    output,
    -- VPL15 = substring, case-insensitive
    CASE WHEN lower(brand_name) LIKE '%value pack lite 15kg%' THEN 1 ELSE 0 END AS is_vpl15,
    -- VP20 = exact element 'value pack' after splitting on ';' / '|'
    CASE WHEN array_contains(
             transform(split(lower(coalesce(brand_name,'')), '[;|]'), x -> trim(x)),
             'value pack'
           ) THEN 1 ELSE 0 END AS is_vp20
  FROM base
)
SELECT
  COUNT(DISTINCT traceid) AS total_traces,
  COUNT(DISTINCT CASE WHEN is_vpl15 = 1 THEN traceid END) AS vpl15_pre,
  COUNT(DISTINCT CASE WHEN is_vpl15 = 1 AND output = 'true' THEN traceid END) AS vpl15_post,
  COUNT(DISTINCT CASE WHEN is_vp20  = 1 THEN traceid END) AS vp20_pre,
  COUNT(DISTINCT CASE WHEN is_vp20  = 1 AND output = 'true' THEN traceid END) AS vp20_post
FROM enriched;

-- =============================================================================
-- QUERY 2 — Benefit-combo matrix: bag_bucket x flex_combo (pre vs post)
-- =============================================================================
WITH base AS (
  SELECT traceid, output, checked_baggage_detail, rfd_feature, chg_feature
  FROM dwflt.edw_rsc_engine_paimon_agg_intl_compare_result_log_di
  WHERE d = '<D>'
    AND sch_type IN ('14','24')
),
enriched AS (
  SELECT
    traceid,
    output,
    -- max checked-bag weight across segments (kg); <=0 = no checked bag
    COALESCE(
      aggregate(split(split(checked_baggage_detail,';')[0], '\\|'), -1,
        (acc, x) -> greatest(acc, COALESCE(cast(split(x, ',')[2] AS INT), -1))),
      -1
    ) AS max_checked_kg,
    CASE WHEN lower(coalesce(rfd_feature,'')) LIKE '%refund%'
           AND lower(coalesce(rfd_feature,'')) NOT LIKE '%nonrefund%'
         THEN 1 ELSE 0 END AS is_refundable,
    CASE WHEN lower(coalesce(chg_feature,'')) LIKE '%change%'
           AND lower(coalesce(chg_feature,'')) NOT LIKE '%nonchange%'
         THEN 1 ELSE 0 END AS is_changeable
  FROM base
),
classified AS (
  SELECT
    traceid, output,
    CASE
      WHEN max_checked_kg <= 0  THEN 'no_checked'
      WHEN max_checked_kg <= 15 THEN 'le15kg'
      WHEN max_checked_kg <= 20 THEN '16_20kg'
      WHEN max_checked_kg <= 23 THEN '21_23kg'
      WHEN max_checked_kg <= 30 THEN '24_30kg'
      ELSE 'gt30kg'
    END AS bag_bucket,
    CASE
      WHEN is_refundable = 1 AND is_changeable = 1 THEN 'Flexible'
      WHEN is_refundable = 1 AND is_changeable = 0 THEN 'Cancel_Only'
      WHEN is_refundable = 0 AND is_changeable = 1 THEN 'Change_Only'
      ELSE 'Not_Flexible'
    END AS flex_combo
  FROM enriched
)
SELECT
  bag_bucket,
  flex_combo,
  COUNT(DISTINCT traceid) AS pre_searches,
  COUNT(DISTINCT CASE WHEN output = 'true' THEN traceid END) AS post_searches
FROM classified
GROUP BY bag_bucket, flex_combo
ORDER BY bag_bucket, flex_combo;

-- =============================================================================
-- QUERY 3 — Brand-agnostic 15kg / 20kg checked-bag coverage (stable cross-check)
--           Comparable across dates even though the brand name changed.
-- =============================================================================
WITH base AS (
  SELECT traceid, output, checked_baggage_detail
  FROM dwflt.edw_rsc_engine_paimon_agg_intl_compare_result_log_di
  WHERE d = '<D>'
    AND sch_type IN ('14','24')
),
enriched AS (
  SELECT
    traceid,
    output,
    COALESCE(
      aggregate(split(split(checked_baggage_detail,';')[0], '\\|'), -1,
        (acc, x) -> greatest(acc, COALESCE(cast(split(x, ',')[2] AS INT), -1))),
      -1
    ) AS max_checked_kg
  FROM base
)
SELECT
  COUNT(DISTINCT traceid) AS total_traces,
  COUNT(DISTINCT CASE WHEN max_checked_kg = 15 THEN traceid END) AS kg15_pre,
  COUNT(DISTINCT CASE WHEN max_checked_kg = 15 AND output = 'true' THEN traceid END) AS kg15_post,
  COUNT(DISTINCT CASE WHEN max_checked_kg = 20 THEN traceid END) AS kg20_pre,
  COUNT(DISTINCT CASE WHEN max_checked_kg = 20 AND output = 'true' THEN traceid END) AS kg20_post
FROM enriched;

-- =============================================================================
-- QUERY 4 — Upsell headroom: among VPL15 searches, % also surfacing a 20kg+ fare
-- =============================================================================
WITH base AS (
  SELECT traceid, output, brand_name, checked_baggage_detail
  FROM dwflt.edw_rsc_engine_paimon_agg_intl_compare_result_log_di
  WHERE d = '<D>'
    AND sch_type IN ('14','24')
),
enriched AS (
  SELECT
    traceid,
    output,
    COALESCE(
      aggregate(split(split(checked_baggage_detail,';')[0], '\\|'), -1,
        (acc, x) -> greatest(acc, COALESCE(cast(split(x, ',')[2] AS INT), -1))),
      -1
    ) AS max_checked_kg,
    CASE WHEN lower(brand_name) LIKE '%value pack lite 15kg%' THEN 1 ELSE 0 END AS is_vpl15
  FROM base
),
vpl15_searches AS (
  SELECT DISTINCT traceid FROM enriched WHERE is_vpl15 = 1
)
SELECT
  (SELECT COUNT(*) FROM vpl15_searches) AS vpl15_searches,
  COUNT(DISTINCT CASE WHEN e.max_checked_kg >= 20 THEN e.traceid END) AS with_20kg_plus,
  COUNT(DISTINCT CASE WHEN e.max_checked_kg = 20 THEN e.traceid END) AS with_20kg,
  COUNT(DISTINCT CASE WHEN e.max_checked_kg BETWEEN 21 AND 23 THEN e.traceid END) AS with_21_23kg,
  COUNT(DISTINCT CASE WHEN e.max_checked_kg BETWEEN 24 AND 30 THEN e.traceid END) AS with_24_30kg,
  COUNT(DISTINCT CASE WHEN e.max_checked_kg > 30 THEN e.traceid END) AS with_gt30kg
FROM enriched e
JOIN vpl15_searches v ON e.traceid = v.traceid
WHERE e.is_vpl15 = 0;

-- =============================================================================
-- QUERY 5 — Seat x bag_bucket x flex cross-tab (AirAsia validating carriers)
--           The seat dimension is what separates the two parallel AirAsia
--           products (Value Pack = seat+bag; Regular Fare = bag only), so the
--           cross-tab is scoped to AirAsia vc to keep the JSON scan fast.
-- =============================================================================
WITH base AS (
  SELECT traceid, output, checked_baggage_detail, rfd_feature, chg_feature, price_json
  FROM dwflt.edw_rsc_engine_paimon_agg_intl_compare_result_log_di
  WHERE d = '<D>'
    AND sch_type IN ('14','24')
    AND vc RLIKE '^(AK|FD|QZ|Z2|D7|XJ|KT)(\\|(AK|FD|QZ|Z2|D7|XJ|KT))*$'
),
enriched AS (
  SELECT
    traceid,
    output,
    CASE WHEN instr(price_json, '"key":"Seat"') > 0 THEN 'has_seat' ELSE 'no_seat' END AS seat,
    COALESCE(
      aggregate(split(split(checked_baggage_detail,';')[0], '\\|'), -1,
        (acc, x) -> greatest(acc, COALESCE(cast(split(x, ',')[2] AS INT), -1))),
      -1
    ) AS max_checked_kg,
    CASE WHEN lower(coalesce(rfd_feature,'')) LIKE '%refund%'
           AND lower(coalesce(rfd_feature,'')) NOT LIKE '%nonrefund%'
         THEN 1 ELSE 0 END AS is_refundable,
    CASE WHEN lower(coalesce(chg_feature,'')) LIKE '%change%'
           AND lower(coalesce(chg_feature,'')) NOT LIKE '%nonchange%'
         THEN 1 ELSE 0 END AS is_changeable
  FROM base
),
classified AS (
  SELECT
    traceid, output, seat,
    CASE
      WHEN max_checked_kg <= 0  THEN 'no_checked'
      WHEN max_checked_kg <= 15 THEN 'le15kg'
      WHEN max_checked_kg <= 20 THEN '16_20kg'
      WHEN max_checked_kg <= 23 THEN '21_23kg'
      WHEN max_checked_kg <= 30 THEN '24_30kg'
      ELSE 'gt30kg'
    END AS bag_bucket,
    CASE
      WHEN is_refundable = 1 AND is_changeable = 1 THEN 'Flexible'
      WHEN is_refundable = 1 AND is_changeable = 0 THEN 'Cancel_Only'
      WHEN is_refundable = 0 AND is_changeable = 1 THEN 'Change_Only'
      ELSE 'Not_Flexible'
    END AS flex_combo
  FROM enriched
)
SELECT
  seat,
  bag_bucket,
  flex_combo,
  COUNT(DISTINCT traceid) AS pre_searches,
  COUNT(DISTINCT CASE WHEN output = 'true' THEN traceid END) AS post_searches
FROM classified
GROUP BY seat, bag_bucket, flex_combo
ORDER BY seat, bag_bucket, flex_combo;

-- =============================================================================
-- QUERY 6 — Seat x bag-weight headline (benefit fields, FULL table)
--           Distinguishes the two parallel products at the benefit level:
--             seat+15kg  = VPL15-type    vs  no_seat+15kg = Regular Fare 15
--             seat+20kg  = VP20-type     vs  no_seat+20kg = Regular Fare 20
--           NOTE: the instr() seat scan is gated behind kg IN (15,20) so it
--           only runs on the relevant rows (avoids the full-table timeout).
-- =============================================================================
WITH base AS (
  SELECT traceid, output, checked_baggage_detail, price_json
  FROM dwflt.edw_rsc_engine_paimon_agg_intl_compare_result_log_di
  WHERE d = '<D>'
    AND sch_type IN ('14','24')
),
enriched AS (
  SELECT
    traceid,
    output,
    price_json,
    COALESCE(
      aggregate(split(split(checked_baggage_detail,';')[0], '\\|'), -1,
        (acc, x) -> greatest(acc, COALESCE(cast(split(x, ',')[2] AS INT), -1))),
      -1
    ) AS max_checked_kg
  FROM base
),
flagged AS (
  SELECT
    traceid,
    output,
    max_checked_kg,
    CASE WHEN max_checked_kg IN (15, 20)
              AND instr(price_json, '"key":"Seat"') > 0
         THEN 1 ELSE 0 END AS has_seat
  FROM enriched
)
SELECT
  COUNT(DISTINCT traceid) AS total_traces,
  COUNT(DISTINCT CASE WHEN has_seat = 1 AND max_checked_kg = 15 THEN traceid END) AS seat15_pre,
  COUNT(DISTINCT CASE WHEN has_seat = 1 AND max_checked_kg = 15 AND output = 'true' THEN traceid END) AS seat15_post,
  COUNT(DISTINCT CASE WHEN has_seat = 0 AND max_checked_kg = 15 THEN traceid END) AS noseat15_pre,
  COUNT(DISTINCT CASE WHEN has_seat = 0 AND max_checked_kg = 15 AND output = 'true' THEN traceid END) AS noseat15_post,
  COUNT(DISTINCT CASE WHEN has_seat = 1 AND max_checked_kg = 20 THEN traceid END) AS seat20_pre,
  COUNT(DISTINCT CASE WHEN has_seat = 1 AND max_checked_kg = 20 AND output = 'true' THEN traceid END) AS seat20_post,
  COUNT(DISTINCT CASE WHEN has_seat = 0 AND max_checked_kg = 20 THEN traceid END) AS noseat20_pre,
  COUNT(DISTINCT CASE WHEN has_seat = 0 AND max_checked_kg = 20 AND output = 'true' THEN traceid END) AS noseat20_post
FROM flagged;

-- =============================================================================
-- QUERY 7 — Four-product coverage (brand name + seat), product-specific headline
--           value pack lite 15kg / value pack = seat+bag (new parallel fares)
--           regular fare with luggage 15/20     = bag only (legacy fares)
-- =============================================================================
WITH base AS (
  SELECT traceid, output, brand_name
  FROM dwflt.edw_rsc_engine_paimon_agg_intl_compare_result_log_di
  WHERE d = '<D>'
    AND sch_type IN ('14','24')
),
enriched AS (
  SELECT
    traceid,
    output,
    CASE
      WHEN lower(brand_name) LIKE '%value pack lite 15kg%'            THEN 'vpl15_seat_15kg'
      WHEN lower(brand_name) LIKE '%regular fare with luggage 15%'    THEN 'rfl15_noseat_15kg'
      WHEN array_contains(transform(split(lower(coalesce(brand_name,'')),'[;|]'), x -> trim(x)), 'value pack')
                                                                      THEN 'vp20_seat_20kg'
      WHEN lower(brand_name) LIKE '%regular fare with luggage 20%'    THEN 'rfl20_noseat_20kg'
      ELSE 'other'
    END AS product
  FROM base
)
SELECT
  product,
  COUNT(DISTINCT traceid) AS pre_searches,
  COUNT(DISTINCT CASE WHEN output = 'true' THEN traceid END) AS post_searches
FROM enriched
GROUP BY product
ORDER BY product;
