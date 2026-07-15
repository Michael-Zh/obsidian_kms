-- ============================================================
-- SECTION B: RECONCILE RESULT TABLE VS OFFICIAL REPORTING
-- ============================================================

-- B1. Sum of primary_ord_count from your result table
-- This is what you'd get if you summed the grouped output.
-- If rows are double-counted (same primary order in 2 buckets),
-- this will be HIGHER than the true distinct count.
SELECT
  SUM(primary_ord_count)            AS sum_of_grouped_counts,
  SUM(upsell_base_primary_ord_count) AS sum_of_upsell_base,
  SUM(upsell_primary_ord_count)     AS sum_of_upsell
FROM `trip-ibu-adhoc.ibu_adhoc_temp.MZ_202606_quantification`
;

-- B2. True distinct count directly from the raw order table
-- This is the ground truth. Compare against B1.
SELECT
  COUNT(DISTINCT primaryorderid_fill) AS true_distinct_primary_orders
FROM `trip-ibu-bi-dw-etl.ibu_bi_dw_cdw.edw_ord_flt_order`
WHERE orderdate_d BETWEEN "2026-05-01" AND "2026-05-31"
;

-- B3. Identify which primary orders are counted more than once
-- Must run at the segment_table level (before GROUP BY),
-- since primaryorderid_fill is not in the final result table.
WITH segment_table AS (
  SELECT DISTINCT
    a.primaryorderid_fill,
    a.dportcode,
    a.aportcode,
    CASE WHEN a.airline = 'HV' THEN 'TO' WHEN a.airline IN ('W4','W6','W9') THEN 'W6' ELSE a.airline END AS order_marketing_airline,
    CASE WHEN b.classname = '头等舱' THEN 'F' WHEN b.classname = '超级经济舱' THEN 'S' WHEN b.classname = '公务舱' THEN 'C' WHEN b.classname = '经济舱' THEN 'Y' ELSE NULL END AS cabin_IATAcode
  FROM `trip-ibu-bi-dw-etl.ibu_bi_dw_cdw.edw_ord_flt_order` a
  LEFT JOIN `trip-ibu-bi-dw-etl.ibu_bi_dw_cdw.edw_prd_flt_factfltsegment_eng` b
    ON a.orderid = b.orderid
    AND DATE(b.d) = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
    AND b.sequence = 1
  WHERE a.orderdate_d BETWEEN "2025-01-01" AND "2026-05-31"
    AND b.orderid IS NOT NULL
)
SELECT
  primaryorderid_fill,
  COUNT(*) AS appears_in_n_buckets,
  COUNT(DISTINCT dportcode)               AS distinct_dport,
  COUNT(DISTINCT aportcode)               AS distinct_aport,
  COUNT(DISTINCT order_marketing_airline) AS distinct_airline,
  COUNT(DISTINCT cabin_IATAcode)          AS distinct_cabin
FROM segment_table
GROUP BY primaryorderid_fill
HAVING COUNT(*) > 1
ORDER BY appears_in_n_buckets DESC
LIMIT 100
;

-- B4. Summary of double-counting magnitude (also at segment_table level)
WITH segment_table AS (
  SELECT DISTINCT
    a.primaryorderid_fill,
    a.dportcode,
    a.aportcode
  FROM `trip-ibu-bi-dw-etl.ibu_bi_dw_cdw.edw_ord_flt_order` a
  LEFT JOIN `trip-ibu-bi-dw-etl.ibu_bi_dw_cdw.edw_prd_flt_factfltsegment_eng` b
    ON a.orderid = b.orderid
    AND DATE(b.d) = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
    AND b.sequence = 1
  WHERE a.orderdate_d BETWEEN "2025-01-01" AND "2026-05-31"
    AND b.orderid IS NOT NULL
),
bucket_counts AS (
  SELECT primaryorderid_fill, COUNT(*) AS appears_in_n_buckets
  FROM segment_table
  GROUP BY primaryorderid_fill
)
SELECT
  COUNT(*)                                  AS double_counted_primary_orders,
  SUM(appears_in_n_buckets) - COUNT(*)      AS extra_count_inflation,
  SUM(appears_in_n_buckets)                 AS total_counted,
  COUNT(DISTINCT primaryorderid_fill)       AS true_distinct_orders
FROM bucket_counts
WHERE appears_in_n_buckets > 1
;

-- ▶ If B1 > B2: double-counting confirmed. Run B3 to see which
--   dimension column causes the split (e.g. dportcode varies
--   between outbound and return sub-orders of the same primary order).
-- ▶ Fix: move segment-level dimensions (OD pair, cabin, airline)
--   to a sub-order-level report, OR pick one canonical sub-order
--   per primary order before grouping (e.g. sequence = 1 only,
--   or is_primaryorder = 1).


-- ============================================================
-- DIAGNOSTIC QUERIES: Finding the discrepancy in primary_ord_count
-- Run in order. The first query whose count differs from Correct Code
-- is the step where the bug was introduced.
--
-- BASELINE (from Correct Code): use May 2026 date range throughout.
-- ============================================================


-- ─────────────────────────────────────────────────────────────
-- STEP 1: orderdate vs orderdate_d
-- Current Code uses `a.orderdate BETWEEN ...` in segment_table WHERE,
-- Correct Code uses `a.orderdate_d BETWEEN ...`.
-- These fields may differ in type/value, causing row set mismatch.
-- ─────────────────────────────────────────────────────────────

-- 1a. Count using orderdate (Current Code's field)
SELECT
  'orderdate' AS filter_field,
  COUNT(DISTINCT primaryorderid_fill) AS primary_ord_count
FROM `trip-ibu-bi-dw-etl.ibu_bi_dw_cdw.edw_ord_flt_order`
WHERE orderdate BETWEEN "2026-05-01" AND "2026-05-31"
;

-- 1b. Count using orderdate_d (Correct Code's field)
SELECT
  'orderdate_d' AS filter_field,
  COUNT(DISTINCT primaryorderid_fill) AS primary_ord_count
FROM `trip-ibu-bi-dw-etl.ibu_bi_dw_cdw.edw_ord_flt_order`
WHERE orderdate_d BETWEEN "2026-05-01" AND "2026-05-31"
;

-- ▶ If counts differ: root cause is the orderdate vs orderdate_d field.


-- ─────────────────────────────────────────────────────────────
-- STEP 2: Missing `b.orderid IS NOT NULL` filter
-- Correct Code has: `AND b.orderid IS NOT NULL` after the LEFT JOIN
-- to edw_prd_flt_factfltsegment_eng. Current Code does not.
-- Without this, orders with no matching segment row are included.
-- ─────────────────────────────────────────────────────────────

-- 2a. WITHOUT the segment filter (Current Code behaviour)
SELECT
  'no_segment_filter' AS variant,
  COUNT(DISTINCT a.primaryorderid_fill) AS primary_ord_count
FROM `trip-ibu-bi-dw-etl.ibu_bi_dw_cdw.edw_ord_flt_order` a
LEFT JOIN `trip-ibu-bi-dw-etl.ibu_bi_dw_cdw.edw_prd_flt_factfltsegment_eng` b
  ON a.orderid = b.orderid
  AND DATE(b.d) = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
  AND b.sequence = 1
WHERE a.orderdate_d BETWEEN "2026-05-01" AND "2026-05-31"
;

-- 2b. WITH the segment filter (Correct Code behaviour)
SELECT
  'with_segment_filter' AS variant,
  COUNT(DISTINCT a.primaryorderid_fill) AS primary_ord_count
FROM `trip-ibu-bi-dw-etl.ibu_bi_dw_cdw.edw_ord_flt_order` a
LEFT JOIN `trip-ibu-bi-dw-etl.ibu_bi_dw_cdw.edw_prd_flt_factfltsegment_eng` b
  ON a.orderid = b.orderid
  AND DATE(b.d) = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
  AND b.sequence = 1
WHERE a.orderdate_d BETWEEN "2026-05-01" AND "2026-05-31"
  AND b.orderid IS NOT NULL
;

-- ▶ If counts differ: orders without a matching segment row are inflating
--   the count in Current Code.


-- ─────────────────────────────────────────────────────────────
-- STEP 3: The `flexible` subquery fan-out
-- Current Code joins a flexible subquery that queries edw_ord_flt_order_view
-- on orderdate (not orderdate_d) with SELECT DISTINCT orderid, flexible.
-- If one orderid maps to multiple flexible values (e.g. split tickets or
-- amended orders), the LEFT JOIN produces extra rows, which then cause
-- one primaryorderid_fill to appear in multiple GROUP BY buckets,
-- inflating the summed count.
-- ─────────────────────────────────────────────────────────────

-- 3a. Check: are there orderids with more than one flexible value?
SELECT
  COUNT(*) AS multi_flexible_orderids
FROM (
  SELECT orderid, COUNT(DISTINCT flexible) AS flex_count
  FROM (
    SELECT DISTINCT
      orderid,
      CASE
        WHEN nonref = 'H' AND nonrebook = 'H' THEN '4.Flexible'
        WHEN nonref = 'T' AND nonrebook = 'T' THEN '1.Not Flexible'
        WHEN nonref = 'T' AND nonrebook = 'H' THEN '2.Only change is allowed'
        WHEN nonref = 'H' AND nonrebook = 'T' THEN '3.Only cancel is allowed'
        ELSE '5.other'
      END AS flexible
    FROM `trip-ibu-bi-dw-etl.ibu_bi_dw_cdw.edw_ord_flt_order_view`
    WHERE orderdate BETWEEN "2026-05-01" AND "2026-05-31"
  )
  GROUP BY orderid
)
WHERE flex_count > 1
;

-- ▶ If count > 0: the flexible join is fanning out rows.
--   Fix: take only one flexible value per orderid, e.g. with a MAX() or QUALIFY.

-- 3b. (Bonus) How many extra rows does the fan-out create?
SELECT
  COUNT(*) AS total_rows,
  COUNT(DISTINCT orderid) AS distinct_orderids,
  COUNT(*) - COUNT(DISTINCT orderid) AS extra_rows_from_fanout
FROM (
  SELECT DISTINCT
    orderid,
    CASE
      WHEN nonref = 'H' AND nonrebook = 'H' THEN '4.Flexible'
      WHEN nonref = 'T' AND nonrebook = 'T' THEN '1.Not Flexible'
      WHEN nonref = 'T' AND nonrebook = 'H' THEN '2.Only change is allowed'
      WHEN nonref = 'H' AND nonrebook = 'T' THEN '3.Only cancel is allowed'
      ELSE '5.other'
    END AS flexible
  FROM `trip-ibu-bi-dw-etl.ibu_bi_dw_cdw.edw_ord_flt_order_view`
  WHERE orderdate BETWEEN "2026-05-01" AND "2026-05-31"
)
;


-- ─────────────────────────────────────────────────────────────
-- STEP 4: brand_en_name JOIN fan-out
-- Current Code joins brand_en_name at the final SELECT on
-- (carrier, applicablecabin, atpco_brand_name). If that combination
-- is non-unique in the source table even after GROUP BY ALL,
-- it would fan out rows and inflate the count.
-- ─────────────────────────────────────────────────────────────

-- 4a. Check uniqueness of the brand join key
SELECT
  COUNT(*) AS total_rows,
  COUNT(DISTINCT CONCAT(carrier, '|', applicablecabin, '|', atpco_brand_name)) AS unique_keys,
  COUNT(*) - COUNT(DISTINCT CONCAT(carrier, '|', applicablecabin, '|', atpco_brand_name)) AS duplicate_key_rows
FROM (
  SELECT DISTINCT
    carrier,
    IF(applicablecabin = 'S', 'W', applicablecabin) AS applicablecabin,
    TRIM(REPLACE(LOWER(brandname), ' ', '')) AS atpco_brand_name,
    TRIM(REPLACE(LOWER(enname), ' ', '')) AS brand_name,
    MAX(CAST(airlinebrandtier AS INT64)) AS airline_brandtier,
  FROM `trip-ibu-bi-dw-etl.ibu_bi_dw_source.ods_fltairtickets_mysql_fltresourcedb_tb_brandname_unified`
  WHERE
    DATE(d) >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
    AND actived = '1'
    AND enname IS NOT NULL
    AND applicablecabin = 'Y'
  GROUP BY ALL
)
;

-- ▶ If duplicate_key_rows > 0: the brand join is fanning out rows.
--   Fix: add QUALIFY ROW_NUMBER() OVER (PARTITION BY carrier, applicablecabin, atpco_brand_name ORDER BY airline_brandtier DESC) = 1
--   inside the brand_en_name CTE.


-- ─────────────────────────────────────────────────────────────
-- STEP 5: Confirm which factor accounts for the FULL gap
-- After identifying suspects above, run this to measure the combined
-- effect: start from the Correct Code baseline and add Current Code
-- differences one at a time.
-- ─────────────────────────────────────────────────────────────

-- 5a. Baseline (matches Correct Code logic — should match your known good number)
WITH
  lowest_price_ranked AS (
    SELECT
      CAST(primary_orderid AS BIGINT) AS primary_orderid,
      is_lowest_price,
      ROW_NUMBER() OVER (PARTITION BY primary_orderid ORDER BY d DESC) AS rn
    FROM `trip-ibu-bi-dw-etl.ibu_bi_dw_source.dw_fltdb_edw_deal_ord_intl_is_middle_page_lowest_price_di`
    WHERE
      CAST(d AS DATE) BETWEEN "2026-05-01" AND "2026-05-31"
      AND is_trip = 'T'
      AND is_rebook_new_order = 0
      AND subchnl < 7900000
      AND is_lowest_price IS NOT NULL
  ),
  lowest_price AS (
    SELECT primary_orderid, is_lowest_price FROM lowest_price_ranked WHERE rn = 1
  ),
  segment_table AS (
    SELECT DISTINCT
      a.primaryorderid_fill, a.primorder_haultype, lp.is_lowest_price
    FROM `trip-ibu-bi-dw-etl.ibu_bi_dw_cdw.edw_ord_flt_order` a
    LEFT JOIN `trip-ibu-bi-dw-etl.ibu_bi_dw_cdw.edw_prd_flt_factfltsegment_eng` b
      ON a.orderid = b.orderid
      AND DATE(b.d) = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
      AND b.sequence = 1
    LEFT JOIN lowest_price lp ON a.primaryorderid_fill = lp.primary_orderid
    WHERE
      a.orderdate_d BETWEEN "2026-05-01" AND "2026-05-31"
      AND b.orderid IS NOT NULL   -- ← key filter
  )
SELECT
  'baseline_correct_code' AS variant,
  COUNT(DISTINCT primaryorderid_fill) AS primary_ord_count
FROM segment_table
;

-- 5b. Remove the segment filter → shows the effect of Step 2 alone
WITH
  segment_table AS (
    SELECT DISTINCT a.primaryorderid_fill
    FROM `trip-ibu-bi-dw-etl.ibu_bi_dw_cdw.edw_ord_flt_order` a
    LEFT JOIN `trip-ibu-bi-dw-etl.ibu_bi_dw_cdw.edw_prd_flt_factfltsegment_eng` b
      ON a.orderid = b.orderid
      AND DATE(b.d) = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
      AND b.sequence = 1
    WHERE a.orderdate_d BETWEEN "2026-05-01" AND "2026-05-31"
    -- b.orderid IS NOT NULL deliberately removed
  )
SELECT
  'no_segment_filter' AS variant,
  COUNT(DISTINCT primaryorderid_fill) AS primary_ord_count
FROM segment_table
;
