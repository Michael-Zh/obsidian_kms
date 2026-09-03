-- =============================================================================
-- Global Upsell Rate — Master-Derived Monitoring Query Suite
-- =============================================================================
-- Purpose  : Monthly / weekly global upsell monitoring, derived from the
--            order-level master table (single source of truth). Supersedes
--            `global_upsell_monitoring.sql` (which read the raw
--            `is_middle_page_lowest_price_di` table directly).
--
--            Sections:
--              1. Weekly trend — 1-Meta vs Meta, FSC vs LCC rate
--              2. Weekly volume — total / upsell / lowest / untagged (1-Meta)
--              3. Monthly KPI — global / FSC / LCC rate + MoM + tag rate
--              4. Monthly by trip type × FSC/LCC (share + Jun/Jul/Aug rates)
--              5. Monthly by channel × FSC/LCC
--              6. Monthly by haul × FSC/LCC
--              7. Airline movers (Jun vs Aug, top volume)
--              8. Top routes by 3-month volume (monthly rates)
--
-- Scope    : economy only (is_non_economy = 0 AND is_segment_missing = 0),
--            1-Meta (isMeta = '1-Meta'), tagged (is_lowest_price IS NOT NULL)
--            for all rate metrics. Volume keeps untagged visible.
--
-- Tables   : trip-ibu-adhoc.ibu_adhoc_temp.order_level_master_v3
-- Parameters: d_weekly_start / d_weekly_end (weekly trend window)
--            d_month_start / d_month_end (Jun/Jul/Aug window)
-- Runtime  : each section ~2-5s (master is a pre-joined materialized table)
-- Owner    : Michael (MZ)
-- =============================================================================

-- ─────────────────────────────────────────────────────────────────────────────
-- SHARED SCOPE (apply in every section)
--   isMeta = '1-Meta'                       -- 1-Meta definition (refername != Meta)
--   is_non_economy = 0 AND is_segment_missing = 0   -- economy only
--   is_lowest_price IS NOT NULL             -- tagged (rate metrics only)
--   is_lowest_price = 0  -> upsell (chose non-cheapest)
--   is_lowest_price = 1  -> lowest-price
-- ─────────────────────────────────────────────────────────────────────────────


-- =============================================================================
-- SECTION 1: Weekly trend — 1-Meta vs Meta, FSC vs LCC upsell rate
-- =============================================================================

DECLARE d_weekly_start DATE DEFAULT DATE '2026-03-02';
DECLARE d_weekly_end   DATE DEFAULT DATE '2026-08-31';

SELECT
  DATE_TRUNC(orderdate_d, WEEK(MONDAY))                                   AS week_start,
  isMeta                                                                  AS meta_scope,
  LCCorFSC                                                                AS airline_type,
  COUNT(*)                                                                AS total_orders,
  COUNTIF(is_lowest_price = 0)                                           AS upsell_orders,
  ROUND(SAFE_DIVIDE(COUNTIF(is_lowest_price = 0), COUNT(*)) * 100, 1)   AS upsell_rate_pct
FROM `trip-ibu-adhoc.ibu_adhoc_temp.order_level_master_v3`
WHERE orderdate_d BETWEEN d_weekly_start AND d_weekly_end
  AND is_non_economy = 0 AND is_segment_missing = 0
  AND is_lowest_price IS NOT NULL
GROUP BY week_start, meta_scope, airline_type
ORDER BY week_start, meta_scope, airline_type;


-- =============================================================================
-- SECTION 2: Weekly volume — total / upsell / lowest / untagged (1-Meta)
-- =============================================================================

DECLARE d_weekly_start DATE DEFAULT DATE '2026-03-02';
DECLARE d_weekly_end   DATE DEFAULT DATE '2026-08-31';

SELECT
  DATE_TRUNC(orderdate_d, WEEK(MONDAY))                                   AS week_start,
  COUNT(*)                                                                AS total_orders,
  COUNTIF(is_lowest_price = 0)                                           AS upsell_orders,
  COUNTIF(is_lowest_price = 1)                                           AS lowest_price_orders,
  COUNTIF(is_lowest_price IS NULL)                                       AS untagged_orders,
  ROUND(SAFE_DIVIDE(COUNTIF(is_lowest_price = 0),
                    COUNTIF(is_lowest_price IS NOT NULL)) * 100, 1)      AS rate_tagged_pct
FROM `trip-ibu-adhoc.ibu_adhoc_temp.order_level_master_v3`
WHERE orderdate_d BETWEEN d_weekly_start AND d_weekly_end
  AND isMeta = '1-Meta'
  AND is_non_economy = 0 AND is_segment_missing = 0
GROUP BY week_start
ORDER BY week_start;


-- =============================================================================
-- SECTION 3: Monthly KPI — global / FSC / LCC rate + MoM + tag rate
-- =============================================================================

DECLARE d_month_start DATE DEFAULT DATE '2026-06-01';
DECLARE d_month_end   DATE DEFAULT DATE '2026-08-31';

WITH tagged AS (
  SELECT
    year_month,
    LCCorFSC,
    is_lowest_price
  FROM `trip-ibu-adhoc.ibu_adhoc_temp.order_level_master_v3`
  WHERE orderdate_d BETWEEN d_month_start AND d_month_end
    AND isMeta = '1-Meta'
    AND is_non_economy = 0 AND is_segment_missing = 0
    AND is_lowest_price IS NOT NULL
),
rate AS (
  SELECT
    year_month,
    COUNT(*)                                              AS tagged_total,
    COUNTIF(is_lowest_price = 0)                          AS upsell,
    ROUND(SAFE_DIVIDE(COUNTIF(is_lowest_price = 0), COUNT(*)) * 100, 1) AS rate_pct
  FROM tagged
  GROUP BY year_month
),
fsc_lcc AS (
  SELECT
    year_month,
    LCCorFSC,
    ROUND(SAFE_DIVIDE(COUNTIF(is_lowest_price = 0), COUNT(*)) * 100, 1) AS rate_pct
  FROM tagged
  GROUP BY year_month, LCCorFSC
),
tag AS (
  SELECT
    year_month,
    COUNTIF(is_lowest_price IS NOT NULL) AS tagged_cnt,
    COUNT(*)                             AS total_cnt,
    ROUND(SAFE_DIVIDE(COUNTIF(is_lowest_price IS NOT NULL), COUNT(*)) * 100, 1) AS tag_rate_pct
  FROM `trip-ibu-adhoc.ibu_adhoc_temp.order_level_master_v3`
  WHERE orderdate_d BETWEEN d_month_start AND d_month_end
    AND isMeta = '1-Meta'
    AND is_non_economy = 0 AND is_segment_missing = 0
  GROUP BY year_month
)
SELECT r.year_month, r.tagged_total, r.upsell, r.rate_pct,
       f.fsc_pct, f.lcc_pct, t.tag_rate_pct
FROM rate r
LEFT JOIN (SELECT year_month,
                  MAX(IF(LCCorFSC = 'FSC', rate_pct, NULL)) AS fsc_pct,
                  MAX(IF(LCCorFSC = 'LCC', rate_pct, NULL)) AS lcc_pct
           FROM fsc_lcc GROUP BY year_month) f
  ON r.year_month = f.year_month
LEFT JOIN tag t ON r.year_month = t.year_month
ORDER BY r.year_month;


-- =============================================================================
-- SECTION 4: Monthly by trip type × FSC/LCC (share + Jun/Jul/Aug rates)
-- =============================================================================

DECLARE d_month_start DATE DEFAULT DATE '2026-06-01';
DECLARE d_month_end   DATE DEFAULT DATE '2026-08-31';

WITH scoped AS (
  SELECT
    year_month,
    CASE
      WHEN trip_type IN ('OW-single','OW-mixed') THEN 'OW'
      WHEN trip_type = 'RT-pure'                 THEN 'Pure RT'
      WHEN trip_type = 'RT-mixed'                THEN 'Mixed RT'
      ELSE 'Other'
    END                                          AS trip_group,
    LCCorFSC,
    is_lowest_price
  FROM `trip-ibu-adhoc.ibu_adhoc_temp.order_level_master_v3`
  WHERE orderdate_d BETWEEN d_month_start AND d_month_end
    AND isMeta = '1-Meta'
    AND is_non_economy = 0 AND is_segment_missing = 0
    AND is_lowest_price IS NOT NULL
    AND trip_type IN ('OW-single','OW-mixed','RT-pure','RT-mixed')
)
SELECT
  trip_group,
  LCCorFSC,
  year_month,
  COUNT(*)                                              AS orders,
  ROUND(SAFE_DIVIDE(COUNTIF(is_lowest_price = 0), COUNT(*)) * 100, 1) AS rate_pct
FROM scoped
GROUP BY trip_group, LCCorFSC, year_month
ORDER BY trip_group, LCCorFSC, year_month;


-- =============================================================================
-- SECTION 5: Monthly by channel × FSC/LCC
-- =============================================================================

DECLARE d_month_start DATE DEFAULT DATE '2026-06-01';
DECLARE d_month_end   DATE DEFAULT DATE '2026-08-31';

SELECT
  channel,
  LCCorFSC,
  year_month,
  COUNT(*)                                              AS orders,
  ROUND(SAFE_DIVIDE(COUNTIF(is_lowest_price = 0), COUNT(*)) * 100, 1) AS rate_pct
FROM `trip-ibu-adhoc.ibu_adhoc_temp.order_level_master_v3`
WHERE orderdate_d BETWEEN d_month_start AND d_month_end
  AND isMeta = '1-Meta'
  AND is_non_economy = 0 AND is_segment_missing = 0
  AND is_lowest_price IS NOT NULL
  AND channel IN ('app','online','h5')
GROUP BY channel, LCCorFSC, year_month
ORDER BY channel, LCCorFSC, year_month;


-- =============================================================================
-- SECTION 6: Monthly by haul × FSC/LCC
-- =============================================================================

DECLARE d_month_start DATE DEFAULT DATE '2026-06-01';
DECLARE d_month_end   DATE DEFAULT DATE '2026-08-31';

SELECT
  haul,
  LCCorFSC,
  year_month,
  COUNT(*)                                              AS orders,
  ROUND(SAFE_DIVIDE(COUNTIF(is_lowest_price = 0), COUNT(*)) * 100, 1) AS rate_pct
FROM `trip-ibu-adhoc.ibu_adhoc_temp.order_level_master_v3`
WHERE orderdate_d BETWEEN d_month_start AND d_month_end
  AND isMeta = '1-Meta'
  AND is_non_economy = 0 AND is_segment_missing = 0
  AND is_lowest_price IS NOT NULL
GROUP BY haul, LCCorFSC, year_month
ORDER BY haul, LCCorFSC, year_month;


-- =============================================================================
-- SECTION 7: Airline movers — Jun vs Aug rate + 3-month volume (top by volume)
-- =============================================================================

DECLARE d_month_start DATE DEFAULT DATE '2026-06-01';
DECLARE d_month_end   DATE DEFAULT DATE '2026-08-31';

WITH scoped AS (
  SELECT
    marketing_airline,
    LCCorFSC,
    order_month,
    is_lowest_price
  FROM `trip-ibu-adhoc.ibu_adhoc_temp.order_level_master_v3`
  WHERE orderdate_d BETWEEN d_month_start AND d_month_end
    AND isMeta = '1-Meta'
    AND is_non_economy = 0 AND is_segment_missing = 0
    AND is_lowest_price IS NOT NULL
    AND marketing_airline IS NOT NULL
),
vol AS (
  SELECT marketing_airline, LCCorFSC, COUNT(*) AS total_3mo
  FROM scoped GROUP BY marketing_airline, LCCorFSC
),
by_month AS (
  SELECT marketing_airline, LCCorFSC, order_month,
         COUNT(*) AS orders,
         ROUND(SAFE_DIVIDE(COUNTIF(is_lowest_price = 0), COUNT(*)) * 100, 1) AS rate_pct
  FROM scoped
  GROUP BY marketing_airline, LCCorFSC, order_month
)
SELECT
  b.marketing_airline, b.LCCorFSC, v.total_3mo,
  MAX(IF(b.order_month = 6, b.rate_pct, NULL)) AS jun_pct,
  MAX(IF(b.order_month = 8, b.rate_pct, NULL)) AS aug_pct
FROM by_month b
JOIN vol v ON b.marketing_airline = v.marketing_airline AND b.LCCorFSC = v.LCCorFSC
WHERE v.total_3mo >= 5000
GROUP BY b.marketing_airline, b.LCCorFSC, v.total_3mo
ORDER BY v.total_3mo DESC
LIMIT 30;


-- =============================================================================
-- SECTION 8: Top routes by 3-month volume (monthly rates)
-- =============================================================================

DECLARE d_month_start DATE DEFAULT DATE '2026-06-01';
DECLARE d_month_end   DATE DEFAULT DATE '2026-08-31';

WITH scoped AS (
  SELECT
    CONCAT(dport, '-', aport) AS od,
    order_month,
    is_lowest_price
  FROM `trip-ibu-adhoc.ibu_adhoc_temp.order_level_master_v3`
  WHERE orderdate_d BETWEEN d_month_start AND d_month_end
    AND isMeta = '1-Meta'
    AND is_non_economy = 0 AND is_segment_missing = 0
    AND is_lowest_price IS NOT NULL
    AND dport IS NOT NULL AND aport IS NOT NULL
),
top AS (
  SELECT od, COUNT(*) AS total_3mo,
         ROW_NUMBER() OVER (ORDER BY COUNT(*) DESC) AS rk
  FROM scoped GROUP BY od
),
by_month AS (
  SELECT od, order_month, COUNT(*) AS orders,
         ROUND(SAFE_DIVIDE(COUNTIF(is_lowest_price = 0), COUNT(*)) * 100, 1) AS rate_pct
  FROM scoped GROUP BY od, order_month
)
SELECT
  b.od, t.total_3mo, t.rk,
  MAX(IF(b.order_month = 6, b.rate_pct, NULL)) AS jun_pct,
  MAX(IF(b.order_month = 7, b.rate_pct, NULL)) AS jul_pct,
  MAX(IF(b.order_month = 8, b.rate_pct, NULL)) AS aug_pct
FROM by_month b
JOIN top t ON b.od = t.od
WHERE t.rk <= 25
GROUP BY b.od, t.total_3mo, t.rk
ORDER BY t.rk;
