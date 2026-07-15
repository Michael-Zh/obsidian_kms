-- Coverage check table for Claude scraper workflow
-- Run this to (re)create the table; takes ~1–2 min.
-- Claude checks table freshness before each scraper run and re-runs if >30 days old.

CREATE OR REPLACE TABLE trip-ibu-adhoc.ibu_adhoc_temp.MZ_coverage_check_for_claude
AS
WITH
  brand_en_name AS (
    SELECT DISTINCT
      carrier,
      IF(applicablecabin = 'S', 'W', applicablecabin) AS applicablecabin,
      enname,
      MAX(CAST(airlinebrandtier AS INT64)) AS airline_brandtier,
    FROM
      `trip-ibu-bi-dw-etl.ibu_bi_dw_source.ods_fltairtickets_mysql_fltresourcedb_tb_brandname_unified`
    WHERE
      DATE(d) >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
      AND actived = '1'
      AND enname IS NOT NULL
      AND applicablecabin = 'Y'
    GROUP BY ALL
  ),
  od_haultype AS (
    SELECT DISTINCT primary_dairport, primary_aairport, haultype
    FROM
      `trip-ibu-bi-dw-etl.ibu_bi_dw_source.dw_fltdb_adm_fltinsight_competiortrip_od_compare`
    WHERE d = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
  )
SELECT
  a.d,
  a.vc,
  dimf1.airlinename_eng,
  a.class,
  CASE
    WHEN a.class IN ('Y') THEN 'Economy Class'
    WHEN a.class IN ('S') THEN 'Premium Economy Class'
    WHEN a.class IN ('C') THEN 'Business Class'
    WHEN a.class IN ('F') THEN 'First Class'
    ELSE NULL
    END
    AS class_en_name,
  b.airline_brandtier,
  a.brand_name,
  a.airport_pair,
  a.city_pair,
  a.country_pair,
  h.haultype,
  CASE
    WHEN a.city_pair IS NULL THEN 'country level'
    ELSE 'airport/city level'
    END
    AS data_level,
  SUM(a.total_cnt) AS total_cnt,
  SUM(a.has_brand_cnt) AS has_brand_cnt,
  SUM(a.output_total_cnt) AS output_total_cnt,
  SUM(a.output_has_brand_cnt) AS output_has_brand_cnt
FROM
  `trip-ibu-bi-dw-etl.ibu_bi_dw_source.dw_fltdb_adm_rsc_engine_airline_route_brand_cover_v2_di`
    a
LEFT JOIN brand_en_name b
  ON
    a.vc = b.carrier
    AND a.class = b.applicablecabin
    AND TRIM(a.brand_name) = TRIM(b.enname)
LEFT JOIN `trip-ibu-bi-dw-etl.ibu_bi_dw_dim.dim_prd_flt_airline` dimf1
  ON a.vc = dimf1.airline
LEFT JOIN od_haultype h
  ON
    SPLIT(a.airport_pair, '-')[SAFE_OFFSET(0)] = h.primary_dairport
    AND SPLIT(a.airport_pair, '-')[SAFE_OFFSET(1)] = h.primary_aairport
WHERE
  a.d >= "2026-01-01"
  AND a.class = 'Y'
  AND LENGTH(TRIM(a.country_pair)) > 0
  AND LENGTH(TRIM(a.airport_pair)) > 0
GROUP BY ALL
