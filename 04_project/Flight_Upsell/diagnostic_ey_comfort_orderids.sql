-- EY Comfort / Deluxe brand orders — June 2026, primary orders only
-- Purpose: get sample orderids for cancel fee field investigation

SELECT DISTINCT
  o.orderid,
  o.brandname,
  o.orderbrand,
  o.orderdate_d
FROM `trip-ibu-bi-dw-etl.ibu_bi_dw_cdw.edw_ord_flt_order` o
WHERE o.orderdate_d BETWEEN '2026-06-01' AND '2026-06-30'
  AND o.is_primaryorder = 1
  AND o.airline = 'EY'
  AND (
    LOWER(o.brandname) LIKE '%comfort%'
    OR LOWER(o.brandname) LIKE '%deluxe%'
  )
ORDER BY o.orderdate_d DESC
;
