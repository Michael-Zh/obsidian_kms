-- =============================================================================
-- Order-Level Master Table — build SQL (v3, rebuild 2026-09-02)
-- =============================================================================
-- Purpose : One row per primary order (`primaryorderid_fill`) with all dimensions
--           pre-joined + cleaned — single source of truth for global upsell analysis.
--           Monthly/weekly reports aggregate from this table.
--
-- v2 changes (2026-09-01 rebuild):
--   1. PAX BACKFILL — d_snapshot raised 08-31 → 09-02. Fact `persons` lags ~2 days:
--      the 08-31 snapshot carried only 363 persons for 08-31 orders vs 229,262 in
--      the 09-02 snapshot (last ~2 days of pax were near-empty). Weekly monitor
--      should run Tuesday to stay ahead of this lag.
--   2. ECONOMY COERCION FIX — `so.classname = '经济舱'` moved from WHERE into the
--      seg_out LEFT JOIN (no longer silently drops non-economy / missing-segment
--      orders). New flags: `is_segment_missing` (no outbound segment row),
--      `is_non_economy` (segment present but non-economy cabin), `cabin_raw`
--      (raw outbound classname). Downstream economy scope = `is_non_economy = 0
--      AND is_segment_missing = 0`.
--   3. IS_MIXED_CABIN — `COUNT(DISTINCT classname) > 1` across all segments (flags
--      orders whose measures mix economy + premium cabin classes).
--
-- v3 changes (2026-09-02 rebuild):
--   1. BAGGAGE FLAG FIX — `is_free_checkinbag`/`is_free_carryonbag` now read from
--      the ORDER table EN fields `is_free_checkinbagen`/`is_free_carryonbagen`
--      ('Y'/'N'); the segment table stores Chinese 是/否/以航司客规为准 (was
--      breaking `baggage_combo`).
--   2. BAGGAGE TAXONOMY SPLIT — post-booking (booktype=2) split into
--      `*_postbooking_predep` (orderdate < takeofftime) vs
--      `*_postbooking_departed` (orderdate >= takeofftime).
--   3. XPROD SCOPE FIX — filter by ORDER date `o.orderdate_d` (was add-on date
--      `x.orderdate`, which missed late pre-departure add-ons).
--   4. CANONICAL CHECKED-BAG ATTACH RATES — `checkbag_mid_attach` (fare + mid-page
--      bundle) and `checkbag_final_attach` (all sources) as the default baggage
--      metrics going forward.
--
-- Design  : learnings/master-table-schema.md (grain, dims, joins, decisions)
--           learnings/upsell-metric-definitions.md (metric口径)
--
-- Base    : edw_ord_flt_order (official reporting table) → full coverage; NULL tags kept.
--
-- Key rules:
--   • segment leg: `segmentno` = leg (1=outbound, 2=return); `sequence` = within-leg order.
--     Outbound = segmentno=1 & sequence=1; return = segmentno=2 & sequence=1.
--   • is_lowest_price: join primaryorderid_fill = primary_orderid (NOT orderid).
--   • order-level dims are invariant across sub-orders → take is_primaryorder=1.
--   • measures aggregate over ALL sub-orders (SUM amount/ord_quantity); primary_pax
--     comes from fact table `persons` (NOT MAX/SUM ord_persons — both are wrong).
--   • RT duration: fact table `duration_rt`. VFR: keep NULL (untagged) visible.
--
-- Parameters: d_start / d_end (orderdate window), d_snapshot (fact table `d`,
--   must be >= d_end + 2d for complete `persons`). xbag source is
--   `dw_fltdb_edw_deal_ord_factxproductorderdetail_all_ibu` (verified).
-- Runtime  : ~2-5 min (2-year, 70M rows). Owner : Michael (MZ)
-- =============================================================================

DECLARE d_snapshot DATE DEFAULT DATE '2026-09-02';  -- MUST be >= d_end + 2d: fact `persons` lags ~2d (08-31 snapshot had 363 persons for 08-31 vs 229,262 in 09-02 snapshot)
DECLARE d_start    DATE DEFAULT DATE '2024-09-01';
DECLARE d_end      DATE DEFAULT DATE '2026-08-31';

CREATE OR REPLACE TABLE `trip-ibu-adhoc.ibu_adhoc_temp.order_level_master_v3`
AS
WITH
  -- =========================================================================
  -- Brand fare mapping (atpco → normalized brand_name + tier)
  -- =========================================================================
  brand_en_name AS (
    SELECT DISTINCT
      carrier,
      IF(applicablecabin = 'S', 'W', applicablecabin) AS applicablecabin,
      TRIM(REPLACE(LOWER(brandname), ' ', ''))         AS atpco_brand_name,
      TRIM(REPLACE(LOWER(enname), ' ', ''))            AS brand_name,
      MAX(CAST(airlinebrandtier AS INT64))             AS airline_brandtier
    FROM `trip-ibu-bi-dw-etl.ibu_bi_dw_source.ods_fltairtickets_mysql_fltresourcedb_tb_brandname_unified`
    WHERE DATE(d) >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
      AND actived = '1' AND enname IS NOT NULL AND applicablecabin = 'Y'
    GROUP BY ALL
  ),

  -- =========================================================================
  -- x-product (baggage + flexibility) — ONE table, keyed by primary order
  -- =========================================================================
  xprod AS (
    SELECT
      o.primaryorderid_fill,
      -- baggage (手提行李 / 行李额)
      MAX(IF(x.productname = '手提行李' AND x.booktype = 1 AND x.businesstype_detail = 4, 1, 0)) AS carryon_bundle,
      MAX(IF(x.productname = '手提行李' AND x.booktype = 1 AND x.businesstype_detail != 4, 1, 0)) AS carryon_xpage,
      MAX(IF(x.productname = '手提行李' AND x.booktype = 2 AND x.orderdate <  x.takeofftime, 1, 0)) AS carryon_postbooking_predep,
      MAX(IF(x.productname = '手提行李' AND x.booktype = 2 AND x.orderdate >= x.takeofftime, 1, 0)) AS carryon_postbooking_departed,
      MAX(IF(x.productname = '行李额' AND x.booktype = 1 AND x.businesstype_detail = 4, 1, 0))   AS checkbag_bundle,
      MAX(IF(x.productname = '行李额' AND x.booktype = 1 AND x.businesstype_detail != 4, 1, 0))   AS checkbag_xpage,
      MAX(IF(x.productname = '行李额' AND x.booktype = 2 AND x.orderdate <  x.takeofftime, 1, 0)) AS checkbag_postbooking_predep,
      MAX(IF(x.productname = '行李额' AND x.booktype = 2 AND x.orderdate >= x.takeofftime, 1, 0)) AS checkbag_postbooking_departed,
      -- flexibility (Cancellation Guarantee / 退改)
      MAX(IF(x.packagename = 'Cancellation Guarantee - Bundled with Fare'
             AND x.bookpagename = '中间页', 1, 0)) AS rp_bundle,
      MAX(IF((x.productname LIKE '%退%' OR x.productname LIKE '%改%')
             AND x.bookpagename = '中间页', 1, 0))  AS all_flexibility_bundle
    FROM `trip-ibu-bi-dw-etl.ibu_bi_dw_source.dw_fltdb_edw_deal_ord_factxproductorderdetail_all_ibu` x
    JOIN `trip-ibu-bi-dw-etl.ibu_bi_dw_cdw.edw_ord_flt_order` o ON x.orderid = o.orderid
    WHERE o.orderdate_d BETWEEN d_start AND d_end
      AND x.sequence = 1
    GROUP BY 1
  ),

  -- =========================================================================
  -- is_lowest_price (upsell flag), deduped to primary order
  -- =========================================================================
  lowest_price AS (
    SELECT primary_orderid, is_lowest_price FROM (
      SELECT
        CAST(primary_orderid AS BIGINT) AS primary_orderid,
        is_lowest_price,
        ROW_NUMBER() OVER (PARTITION BY primary_orderid ORDER BY d DESC) AS rn
      FROM `trip-ibu-bi-dw-etl.ibu_bi_dw_source.dw_fltdb_edw_deal_ord_intl_is_middle_page_lowest_price_di`
      WHERE CAST(d AS DATE) BETWEEN d_start AND d_end
        AND is_trip = 'T' AND is_rebook_new_order = 0 AND subchnl < 7900000
        AND is_lowest_price IS NOT NULL
    ) WHERE rn = 1
  ),

  -- =========================================================================
  -- RT trip duration (fact primary-order table; d = snapshot date)
  -- =========================================================================
  rt AS (
    SELECT
      primaryorderid, orderdate, flightway, persons,
      SAFE_DIVIDE(CAST(duration_rt AS FLOAT64), 1440) AS trip_days,
      pri_takeofftime, back_takeofftime
    FROM `trip-ibu-bi-dw-etl.ibu_bi_dw_source.flt_bidb_v_edw_factfltprimaryorder_eng`
    WHERE d = d_snapshot AND flightclass = 'I' AND CAST(orderdate AS DATE) BETWEEN d_start AND d_end
  ),

  -- =========================================================================
  -- VFR tag (sub-order × passenger → dedup to primary order; keep NULL)
  -- =========================================================================
  vfr AS (
    SELECT primaryorderid_fill AS primaryorderid, MAX(is_vfr_tag) AS is_vfr_tag
    FROM `trip-ibu-bi-dw-etl.ibu_bi_dw_cdw.adm_vfr_tag_order_final`
    WHERE d BETWEEN d_start AND d_end
    GROUP BY primaryorderid_fill
  ),

  -- =========================================================================
  -- User attributes (order index / new-or-old / first-order year)
  -- =========================================================================
  user_label AS (
    SELECT
      orderid,
      CASE WHEN uid_flt_order_index = 1 THEN '1st order'
           WHEN uid_flt_order_index = 2 THEN '2nd order'
           WHEN uid_flt_order_index = 3 THEN '3rd order'
           ELSE '4th order and above' END AS orderindex,
      CASE WHEN uid_flt_order_index = 1 THEN '1st order' ELSE 'repeat_order' END AS NewOrOld,
      CASE
        WHEN FORMAT_DATE('%Y', uid_flt_firstorder_orderdate) = '2026' THEN 'newin2026'
        WHEN FORMAT_DATE('%Y', uid_flt_firstorder_orderdate) = '2025' THEN 'newin2025'
        WHEN FORMAT_DATE('%Y', uid_flt_firstorder_orderdate) = '2024' THEN 'newin2024'
        WHEN FORMAT_DATE('%Y', uid_flt_firstorder_orderdate) = '2023' THEN 'newin2023'
        WHEN FORMAT_DATE('%Y', uid_flt_firstorder_orderdate) = '2022' THEN 'newin2022'
        WHEN FORMAT_DATE('%Y', uid_flt_firstorder_orderdate) = '2021' THEN 'newin2021'
        WHEN FORMAT_DATE('%Y', uid_flt_firstorder_orderdate) = '2020' THEN 'newin2020'
        ELSE 'before 2020' END AS neworoldYear
    FROM `trip-ibu-bi-dw-etl.ibu_bi_dw_cdw.fact_audience_ibu_flight_order_user_label`
  ),

  -- =========================================================================
  -- All segments mapped to primary order (for concat_airline + outbound/return)
  -- =========================================================================
  seg AS (
    SELECT
      o.primaryorderid_fill,
      o.is_primaryorder,
      s.segmentno, s.sequence, s.airline,
      s.atpco_brand_name, s.ori_brand_name, s.show_brand_name, s.airline_brandtier,
      s.checkin_bagweight, s.checkin_bagnumber, s.is_free_checkinbag, s.is_free_carryonbag,
      s.classname, s.dport, s.aport, s.dcity, s.acity,
      s.brand_attributes, s.interests_attribute, s.nonref, s.nonrer
    FROM `trip-ibu-bi-dw-etl.ibu_bi_dw_cdw.edw_prd_flt_factfltsegment_eng` s
    JOIN `trip-ibu-bi-dw-etl.ibu_bi_dw_cdw.edw_ord_flt_order` o ON s.orderid = o.orderid
    WHERE DATE(s.d) = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
      AND o.orderdate_d BETWEEN d_start AND d_end
  ),
  -- Outbound/return attributed to the PRIMARY sub-order only (is_primaryorder=1).
  -- Multi-sub-order orders restart segmentno at 1 per sub-order → fan-out otherwise.
  seg_out AS (SELECT * FROM seg WHERE is_primaryorder = 1 AND segmentno = 1 AND sequence = 1),
  seg_ret AS (SELECT * FROM seg WHERE is_primaryorder = 1 AND segmentno = 2 AND sequence = 1),
  concat_airline AS (
    SELECT primaryorderid_fill,
           STRING_AGG(airline, '||' ORDER BY segmentno, sequence) AS concat_airline,
           COUNT(DISTINCT airline)   AS distinct_airline_count,
           COUNT(DISTINCT classname) AS distinct_classname_count
    FROM seg GROUP BY primaryorderid_fill
  ),

  -- =========================================================================
  -- Flexibility fare-embedded (nonref 退 / nonrebook 改, from order_view)
  -- =========================================================================
  flexible AS (
    SELECT
      orderid,
      MAX(
        CASE
          WHEN nonref = 'H' AND nonrebook = 'H' THEN '4.Flexible'
          WHEN nonref = 'T' AND nonrebook = 'T' THEN '1.Not Flexible'
          WHEN nonref = 'T' AND nonrebook = 'H' THEN '2.Change Only'
          WHEN nonref = 'H' AND nonrebook = 'T' THEN '3.Cancel Only'
          ELSE '5.Other'
        END) AS flexible
    FROM `trip-ibu-bi-dw-etl.ibu_bi_dw_cdw.edw_ord_flt_order_view`
    WHERE orderdate_d BETWEEN d_start AND d_end
    GROUP BY orderid
  ),

  -- =========================================================================
  -- Measures aggregated over ALL sub-orders
  -- =========================================================================
  measures AS (
    SELECT
      primaryorderid_fill,
      SUM(ord_quantity) AS primary_ord_quantity,
      -- primary_pax_sum removed: ord_persons is per (sub-order × passengertype);
      --   MAX undercounts children/infants, SUM double-counts leg splits. Use rt.persons.
      SUM(amount)        AS primary_amount,
      SUM(tot_price)     AS primary_actual_paid_price
    FROM `trip-ibu-bi-dw-etl.ibu_bi_dw_cdw.edw_ord_flt_order`
    WHERE orderdate_d BETWEEN d_start AND d_end
      AND flightclass = 'I'
      AND subprdtype_pos_primorder NOT IN ('FCN')
      AND orderstatus IN ('S','T','R')
      AND manualset = 'F'
      AND uid NOT IN ('HuaMeiYiDa','M351274275','M2555541076','M117699353','_U2662303168')
      AND NOT (SOURCE = 'Affiliate' AND subchannel IN ('778105','108352','777122'))
    GROUP BY primaryorderid_fill
  ),

  -- =========================================================================
  -- Base: one row per primary order (is_primaryorder=1) + all dims
  -- =========================================================================
  base AS (
    SELECT
      a.primaryorderid_fill,
      a.orderid,  -- primary sub-order's orderid (for user_label join)
      a.orderdate_d,
      EXTRACT(YEAR FROM a.orderdate_d)  AS order_year,
      EXTRACT(MONTH FROM a.orderdate_d) AS order_month,
      a.primorderflightway,

      a.region,
      a.channeltype,
      a.primorder_haultype,
      a.bookingchannel,
      a.origin_intlagenttype,
      a.origin_agcycode,
      CASE WHEN a.refername = 'Meta' THEN 'Meta' ELSE '1-Meta' END AS isMeta,

      -- supplier type (flightagencyaffiliation)
      CASE
        WHEN d.flightagencyaffiliation IN ('境内供应商') THEN 'Chinese_Supplier'
        WHEN d.flightagencyaffiliation IN ('境内自营')   THEN 'CNBSP'
        WHEN d.flightagencyaffiliation IN ('境外自营')   THEN 'Oversea_IATA_non_gamble'
        WHEN d.flightagencyaffiliation IN ('境外供应商')
             AND a.flightagencyname IN ('北京乐途二部(国际平台)', '北京逸趣飞六部(国际平台)')
          THEN 'Oversea_IATA_gamble'
        WHEN d.flightagencyaffiliation IN ('境外供应商')
             AND a.flightagencyname NOT IN ('北京乐途二部(国际平台)', '北京逸趣飞六部(国际平台)')
          THEN 'Oversea_Supplier'
        ELSE 'error'
      END AS suppliertype_toB,

      -- gambling type (producttype)
      CASE
        WHEN a.producttype IN ('CSDPrivate','CSD','PlatformsPrivate','RTKSeat','BSeat')
          THEN 'gambling products from CN consolidator'
        WHEN a.producttype IN ('OverseasPrivate','OverseasLow')
          THEN 'gambling product from project mask'
        WHEN a.producttype IN ('CSDPrivateDown','PLATFORMSPRIVATEDOWN','RTSEATDOWN','CSDDown')
          THEN 'delayed-CN consolidator'
        WHEN a.producttype IN ('OverseasDown') THEN 'delayed-project mask'
        ELSE 'non-gambling'
      END AS gamblingYN,

      -- marketing airline (outbound; HV→TO only)
      CASE WHEN so.airline = 'HV' THEN 'TO' ELSE so.airline END AS marketing_airline,
      CASE WHEN dimf1.isbudget = 1 THEN 'LCC' ELSE 'FSC' END AS LCCorFSC,
      CASE WHEN LOWER(dimf1.countrycode) = a.region THEN 'home-carrier' ELSE 'non-home-carrier' END AS Ishomecarrierornot,

      -- brand (raw + mapped)
      so.atpco_brand_name, so.ori_brand_name, so.show_brand_name, so.airline_brandtier,
      bn.brand_name,

      -- fare-embedded baggage (checked only); EN flags from order table (segment table stores Chinese 是/否/以航司客规为准)
      so.checkin_bagweight, so.checkin_bagnumber,
      a.is_free_checkinbagen AS is_free_checkinbag,
      a.is_free_carryonbagen AS is_free_carryonbag,

      -- economy-coercion flags (2026-09-01 rebuild): keep non-economy / missing-segment
      -- orders instead of silently dropping them (coverage visibility, decision #7)
      CASE WHEN so_raw.primaryorderid_fill IS NULL THEN 1 ELSE 0 END AS is_segment_missing,
      CASE WHEN so_raw.primaryorderid_fill IS NOT NULL AND so.primaryorderid_fill IS NULL THEN 1 ELSE 0 END AS is_non_economy,
      so_raw.classname AS cabin_raw,

      -- cabin / OD / seat
      so.classname, so.dport, so.aport, so.dcity, so.acity,
      a.dcountryename, a.acountryename,
      so.brand_attributes, so.interests_attribute,

      -- flexibility fare-embedded (from order_view)
      f.flexible AS flexible,

      -- return first flight brand
      sr.atpco_brand_name AS return_brand

    FROM `trip-ibu-bi-dw-etl.ibu_bi_dw_cdw.edw_ord_flt_order` a
    LEFT JOIN seg_out so ON a.primaryorderid_fill = so.primaryorderid_fill AND so.classname = '经济舱'
    LEFT JOIN seg_out so_raw ON a.primaryorderid_fill = so_raw.primaryorderid_fill  -- raw (any cabin) for coverage flags
    LEFT JOIN seg_ret sr ON a.primaryorderid_fill = sr.primaryorderid_fill
    LEFT JOIN `trip-ibu-bi-dw-etl.ibu_bi_dw_dim.dim_prd_flt_airline` dimf1 ON so.airline = dimf1.airline
    LEFT JOIN `trip-ibu-bi-dw-etl.ibu_bi_dw_dim.dim_prd_flt_flightagencyattribute` d ON a.flightagency = d.flightagencyid
    LEFT JOIN brand_en_name bn
      ON so.airline = bn.carrier
     AND TRIM(REPLACE(LOWER(so.atpco_brand_name), ' ', '')) = bn.atpco_brand_name
    LEFT JOIN flexible f ON a.orderid = f.orderid

    WHERE
      a.orderdate_d BETWEEN d_start AND d_end
      AND a.flightclass = 'I'
      AND a.is_primaryorder = 1                       -- one row per primary order
      AND a.subprdtype_pos_primorder NOT IN ('FCN')
      AND a.orderstatus IN ('S','T','R')
      AND a.manualset = 'F'
      AND a.uid NOT IN ('HuaMeiYiDa','M351274275','M2555541076','M117699353','_U2662303168')
      AND NOT (a.SOURCE = 'Affiliate' AND a.subchannel IN ('778105','108352','777122'))
  ),

  -- =========================================================================
  -- Derived: is_mixed_airline (needs concat_airline before trip_type)
  -- =========================================================================
  derived AS (
    SELECT b.*,
      CASE
        WHEN ca.concat_airline IS NULL THEN NULL
        WHEN ca.distinct_airline_count > 1 THEN 1 ELSE 0
      END AS is_mixed_airline,
      CASE WHEN ca.distinct_classname_count > 1 THEN 1 ELSE 0 END AS is_mixed_cabin,
      ca.concat_airline,
      lp.is_lowest_price,
      xp.carryon_bundle, xp.carryon_xpage, xp.carryon_postbooking_predep, xp.carryon_postbooking_departed,
      xp.checkbag_bundle, xp.checkbag_xpage, xp.checkbag_postbooking_predep, xp.checkbag_postbooking_departed,
      xp.rp_bundle, xp.all_flexibility_bundle,
      u.orderindex, u.NewOrOld, u.neworoldYear,
      rt.trip_days, rt.pri_takeofftime, rt.back_takeofftime,
      vfr.is_vfr_tag,
      m.primary_ord_quantity, rt.persons AS primary_pax_sum, m.primary_amount, m.primary_actual_paid_price
    FROM base b
    LEFT JOIN concat_airline ca ON b.primaryorderid_fill = ca.primaryorderid_fill
    LEFT JOIN lowest_price lp   ON b.primaryorderid_fill = lp.primary_orderid
    LEFT JOIN xprod xp          ON b.primaryorderid_fill = xp.primaryorderid_fill
    LEFT JOIN user_label u      ON b.orderid = u.orderid
    LEFT JOIN rt                ON b.primaryorderid_fill = rt.primaryorderid
    LEFT JOIN vfr               ON b.primaryorderid_fill = vfr.primaryorderid
    LEFT JOIN measures m        ON b.primaryorderid_fill = m.primaryorderid_fill
  )

-- ===========================================================================
-- Final output
-- ===========================================================================
SELECT
  primaryorderid_fill,
  orderdate_d, order_year, order_month,
  CONCAT(CAST(order_year AS STRING), '_', LPAD(CAST(order_month AS STRING), 2, '0')) AS year_month,
  primorderflightway AS trip_way,

  region, channeltype AS channel, primorder_haultype AS haul,
  bookingchannel, origin_intlagenttype, origin_agcycode, isMeta,
  suppliertype_toB, gamblingYN,
  marketing_airline, LCCorFSC, Ishomecarrierornot,

  atpco_brand_name, ori_brand_name, show_brand_name, airline_brandtier, brand_name,
  checkin_bagweight, checkin_bagnumber, is_free_checkinbag, is_free_carryonbag,
  classname AS cabin, cabin_raw, is_segment_missing, is_non_economy,
  dport, aport, dcity, acity, dcountryename, acountryename,
  brand_attributes, interests_attribute,
  flexible, return_brand,

  carryon_bundle, carryon_xpage, carryon_postbooking_predep, carryon_postbooking_departed,
  checkbag_bundle, checkbag_xpage, checkbag_postbooking_predep, checkbag_postbooking_departed,
  rp_bundle, all_flexibility_bundle,

  is_lowest_price,           -- keep NULL (untagged) visible
  orderindex, NewOrOld, neworoldYear,
  trip_days AS rt_trip_days, pri_takeofftime, back_takeofftime,
  is_vfr_tag,                -- keep NULL (untagged) visible
  concat_airline,

  is_mixed_airline, is_mixed_cabin,
  CASE
    WHEN primorderflightway = 'S' AND is_mixed_airline = 0 THEN 'OW-single'
    WHEN primorderflightway = 'S' AND is_mixed_airline = 1 THEN 'OW-mixed'
    WHEN primorderflightway = 'D' AND is_mixed_airline = 0 THEN 'RT-pure'
    WHEN primorderflightway = 'D' AND is_mixed_airline = 1 THEN 'RT-mixed'
    WHEN primorderflightway = 'M' THEN 'Multi-city'
    ELSE NULL
  END AS trip_type,

  DATE_DIFF(DATE(pri_takeofftime), DATE(orderdate_d), DAY) AS advance_day,

  -- baggage combo (none / carryon_only / checkbag_only / both)
  CASE
    WHEN (is_free_carryonbag = 'Y' OR carryon_bundle = 1 OR carryon_xpage = 1 OR carryon_postbooking_predep = 1 OR carryon_postbooking_departed = 1)
     AND (is_free_checkinbag = 'Y' OR checkbag_bundle = 1 OR checkbag_xpage = 1 OR checkbag_postbooking_predep = 1 OR checkbag_postbooking_departed = 1)
      THEN 'bag+carryon'
    WHEN (is_free_checkinbag = 'Y' OR checkbag_bundle = 1 OR checkbag_xpage = 1 OR checkbag_postbooking_predep = 1 OR checkbag_postbooking_departed = 1)
      THEN 'checkbag_only'
    WHEN (is_free_carryonbag = 'Y' OR carryon_bundle = 1 OR carryon_xpage = 1 OR carryon_postbooking_predep = 1 OR carryon_postbooking_departed = 1)
      THEN 'carryon_only'
    ELSE 'no_bag'
  END AS baggage_combo,

  -- Two canonical checked-bag attachment rates (2026-09-02):
  --   checkbag_mid_attach   = fare-embedded + middle-page bundle  (does the middle page capture the need?)
  --   checkbag_final_attach = ALL sources incl. fill-in + post-booking pre/post departure (final)
  CASE WHEN is_free_checkinbag = 'Y' OR checkbag_bundle = 1 THEN 1 ELSE 0 END AS checkbag_mid_attach,
  CASE WHEN is_free_checkinbag = 'Y' OR checkbag_bundle = 1 OR checkbag_xpage = 1
             OR checkbag_postbooking_predep = 1 OR checkbag_postbooking_departed = 1
       THEN 1 ELSE 0 END AS checkbag_final_attach,

  -- flexibility fare-embedded + bundle
  flexible AS flexibility_fare,
  CASE
    WHEN all_flexibility_bundle = 1 THEN '4.Flexible'
    ELSE flexible
  END AS flexibility_fare_bundle,

  primary_ord_quantity, primary_pax_sum, primary_amount, primary_actual_paid_price

FROM derived
