-- ============================================================
-- FSC High-Tier Fare Filtering Analysis
-- Purpose: Identify Batch 1 FSC airlines that benefit most from
--          unlocking filtered tier 3/4 fares via new capability
-- Created: 2026-06-25 | Updated: 2026-06-25
-- ============================================================
--
-- Three screening criteria:
--   C1: filter_pp (pre_coverage - post_coverage) > 15pp — May 2026 only (algo fully rolled out)
--   C2: flexibility_share under FSC benchmark — threshold TBD after Sheets review
--   C3: actual_display_pollution < 20%
--       = void_rate × us_br_kr_share   (void shown only in US/BR/KR)
--       + free_cancel_24h_rate         (24h shown in ALL markets)
--
-- Run order: Q4 first (export to Sheets, verify C3 logic), then Q1–Q3.
-- ============================================================


-- ============================================================
-- Q4: Raw void/24h counts by airline × market
-- Purpose: Export to Google Sheets → build pivot table →
--          verify actual_display_pollution formula before running Q3
-- Source:  MZ_202606_quantification_v2
-- Scope:   Batch 1 FSC, Economy, Jan–May 2026
-- ============================================================

SELECT
  marketing_airline,
  marketing_airline_name,
  market,
  SUM(primary_ord_count)             AS total_orders,
  SUM(void_ord_count)                AS void_orders,
  SUM(free_cancel_24h_ord_count)     AS free_cancel_24h_orders,
  SUM(free_cancel_or_void_ord_count) AS void_or_24h_orders
FROM `trip-ibu-adhoc.ibu_adhoc_temp.MZ_202606_quantification_v2`
WHERE
  isBatch1 = 'Y'
  AND LCCorFSc = 'FSC'
  AND cabin_IATAcode = 'Y'
GROUP BY 1, 2, 3
ORDER BY marketing_airline, market
;


-- ============================================================
-- Q1: Airline profile — flexibility share + void/24h breakdown
-- Source: MZ_202606_quantification_v2
-- Scope:  Batch 1 FSC, Economy class, Jan–May 2026
-- ============================================================

SELECT
  marketing_airline,
  marketing_airline_name,

  SUM(primary_ord_count) AS total_orders,

  -- Flexibility share: both bags in fare OR full flexibility (incl. bundles)
  ROUND(SAFE_DIVIDE(
    SUM(CASE WHEN baggage_final = '4.fare_both_bag_final'
               OR effective_flexible_all = '4.Flexible'
             THEN primary_ord_count ELSE 0 END),
    SUM(primary_ord_count)
  ), 3) AS flexibility_share,

  -- Breakdown: both bags share
  ROUND(SAFE_DIVIDE(
    SUM(CASE WHEN baggage_final = '4.fare_both_bag_final' THEN primary_ord_count ELSE 0 END),
    SUM(primary_ord_count)
  ), 3) AS both_bags_share,

  -- Breakdown: carry-on only share (separate discussion needed)
  ROUND(SAFE_DIVIDE(
    SUM(CASE WHEN baggage_final = '2.fare_carry_on_only_final' THEN primary_ord_count ELSE 0 END),
    SUM(primary_ord_count)
  ), 3) AS carryon_only_share,

  -- Breakdown: bare fare (no bags, no flex)
  ROUND(SAFE_DIVIDE(
    SUM(CASE WHEN baggage_final = '1.fare_only_final' THEN primary_ord_count ELSE 0 END),
    SUM(primary_ord_count)
  ), 3) AS bare_fare_share,

  -- Breakdown: full flexibility share (incl. bundles)
  ROUND(SAFE_DIVIDE(
    SUM(CASE WHEN effective_flexible_all = '4.Flexible' THEN primary_ord_count ELSE 0 END),
    SUM(primary_ord_count)
  ), 3) AS full_flex_share,

  -- C3 inputs: void rate, 24h rate, US/BR/KR market share
  ROUND(SAFE_DIVIDE(SUM(void_ord_count),           SUM(primary_ord_count)), 3) AS void_rate,
  ROUND(SAFE_DIVIDE(SUM(free_cancel_24h_ord_count), SUM(primary_ord_count)), 3) AS free_cancel_24h_rate,
  ROUND(SAFE_DIVIDE(
    SUM(CASE WHEN market IN ('US','BR','KR') THEN primary_ord_count ELSE 0 END),
    SUM(primary_ord_count)
  ), 3) AS us_br_kr_share,

  -- C3: actual display pollution
  --   void shown only in US/BR/KR; 24h shown in all markets
  ROUND(
    SAFE_DIVIDE(SUM(void_ord_count), SUM(primary_ord_count))
      * SAFE_DIVIDE(SUM(CASE WHEN market IN ('US','BR','KR') THEN primary_ord_count ELSE 0 END), SUM(primary_ord_count))
    + SAFE_DIVIDE(SUM(free_cancel_24h_ord_count), SUM(primary_ord_count))
  , 3) AS actual_display_pollution

FROM `trip-ibu-adhoc.ibu_adhoc_temp.MZ_202606_quantification_v2`
WHERE
  isBatch1 = 'Y'
  AND LCCorFSc = 'FSC'
  AND cabin_IATAcode = 'Y'
GROUP BY 1, 2
ORDER BY flexibility_share ASC
;


-- ============================================================
-- Q2: Coverage gap — brand-level filter_pp by airline
-- Source: MZ_coverage_check_for_claude
-- Scope:  Batch 1 FSC, tier >= 3000, Economy, MAY 2026 ONLY
--         (algo fully rolled out end of April; May data is clean)
-- C1 threshold: filter_pp > 15pp
-- ============================================================

WITH brand_agg AS (
  SELECT
    vc                 AS airline,
    airlinename_eng,
    airline_brandtier,
    brand_name,
    SUM(total_cnt)            AS total_cnt,
    SUM(has_brand_cnt)        AS pre_cnt,
    SUM(output_total_cnt)     AS post_total_cnt,
    SUM(output_has_brand_cnt) AS post_cnt,
    SAFE_DIVIDE(SUM(has_brand_cnt),        SUM(total_cnt))        AS pre_rate,
    SAFE_DIVIDE(SUM(output_has_brand_cnt), SUM(output_total_cnt)) AS post_rate
  FROM `trip-ibu-adhoc.ibu_adhoc_temp.MZ_coverage_check_for_claude`
  WHERE
    vc IN (
      'AA','AC','AF','AS','AZ','BA','BR','CA','CI','CX','CZ','DL',
      'EK','EY','FD','FR','GA','HX','IB','JL','KE','KL','LH','LX',
      'MH','MU','NH','OS','OZ','PR','QF','QR','SQ','TG','TK','TO',
      'UA','VB','VF','VN','VS','VY','W4','W6','W9'
    )
    AND airline_brandtier >= 3000
    AND class = 'Y'
    AND d >= '2026-05-01'          -- May only: algo fully rolled out
  GROUP BY 1, 2, 3, 4
  HAVING SUM(has_brand_cnt) > 500  -- exclude negligible volume
)
SELECT
  airline,
  airlinename_eng,
  airline_brandtier,
  brand_name,
  total_cnt,
  pre_cnt,
  post_total_cnt,
  post_cnt,
  ROUND(pre_rate,             3) AS pre_coverage_rate,
  ROUND(post_rate,            3) AS post_coverage_rate,
  ROUND(pre_rate - post_rate, 3) AS filter_pp          -- C1 metric: pp drop
FROM brand_agg
WHERE ROUND(pre_rate - post_rate, 3) > 0.15            -- C1 threshold: > 15pp
ORDER BY filter_pp DESC, airline, airline_brandtier
;


-- ============================================================
-- Q3: Combined screening — join Q1 + Q2, apply all 3 criteria
-- ============================================================
--
-- C1: max filter_pp across tier>=3000 brands > 15pp  (May 2026)
-- C2: flexibility_share < [threshold TBD after Sheets review]
-- C3: actual_display_pollution < 20%
--
-- Note: C2 threshold set to 0.80 as a wide initial pass;
--       adjust after confirming benchmark from Sheets pivot.

WITH
  airline_profile AS (
    SELECT
      marketing_airline,
      marketing_airline_name,
      SUM(primary_ord_count) AS total_orders,
      ROUND(SAFE_DIVIDE(
        SUM(CASE WHEN baggage_final = '4.fare_both_bag_final'
                   OR effective_flexible_all = '4.Flexible'
                 THEN primary_ord_count ELSE 0 END),
        SUM(primary_ord_count)
      ), 3) AS flexibility_share,
      ROUND(SAFE_DIVIDE(
        SUM(CASE WHEN baggage_final = '2.fare_carry_on_only_final' THEN primary_ord_count ELSE 0 END),
        SUM(primary_ord_count)
      ), 3) AS carryon_only_share,
      -- C3: actual display pollution
      ROUND(
        SAFE_DIVIDE(SUM(void_ord_count), SUM(primary_ord_count))
          * SAFE_DIVIDE(SUM(CASE WHEN market IN ('US','BR','KR') THEN primary_ord_count ELSE 0 END), SUM(primary_ord_count))
        + SAFE_DIVIDE(SUM(free_cancel_24h_ord_count), SUM(primary_ord_count))
      , 3) AS actual_display_pollution
    FROM `trip-ibu-adhoc.ibu_adhoc_temp.MZ_202606_quantification_v2`
    WHERE isBatch1 = 'Y' AND LCCorFSc = 'FSC' AND cabin_IATAcode = 'Y'
    GROUP BY 1, 2
  ),

  brand_filter AS (
    SELECT
      vc AS airline,
      airline_brandtier,
      brand_name,
      ROUND(
        SAFE_DIVIDE(SUM(has_brand_cnt), SUM(total_cnt))
        - SAFE_DIVIDE(SUM(output_has_brand_cnt), SUM(output_total_cnt))
      , 3) AS filter_pp
    FROM `trip-ibu-adhoc.ibu_adhoc_temp.MZ_coverage_check_for_claude`
    WHERE
      vc IN (
        'AA','AC','AF','AS','AZ','BA','BR','CA','CI','CX','CZ','DL',
        'EK','EY','FD','FR','GA','HX','IB','JL','KE','KL','LH','LX',
        'MH','MU','NH','OS','OZ','PR','QF','QR','SQ','TG','TK','TO',
        'UA','VB','VF','VN','VS','VY','W4','W6','W9'
      )
      AND airline_brandtier >= 3000
      AND class = 'Y'
      AND d >= '2026-05-01'
    GROUP BY 1, 2, 3
    HAVING SUM(has_brand_cnt) > 500
  ),

  coverage_gap_airline AS (
    SELECT
      airline,
      MAX(airline_brandtier) AS max_tier_available,
      MAX(filter_pp)         AS max_filter_pp
    FROM brand_filter
    GROUP BY 1
  )

SELECT
  p.marketing_airline,
  p.marketing_airline_name,
  p.total_orders,
  p.flexibility_share,
  p.carryon_only_share,
  p.actual_display_pollution,
  c.max_filter_pp,
  c.max_tier_available,

  -- Criteria flags
  IF(c.max_filter_pp > 0.15,              'Y', 'N') AS C1_filter_gt15pp,
  IF(p.flexibility_share < 0.80,          'Y', 'N') AS C2_flex_below_threshold,  -- threshold TBD
  IF(p.actual_display_pollution < 0.20,   'Y', 'N') AS C3_clean,

  IF(
    c.max_filter_pp > 0.15
    AND p.flexibility_share < 0.80
    AND p.actual_display_pollution < 0.20,
    'PRIORITY', ''
  ) AS priority_flag,

  IF(p.carryon_only_share > 0.20, 'CARRYON_DISCUSS', '') AS carryon_flag

FROM airline_profile p
LEFT JOIN coverage_gap_airline c ON p.marketing_airline = c.airline
ORDER BY priority_flag DESC, p.flexibility_share ASC
;
