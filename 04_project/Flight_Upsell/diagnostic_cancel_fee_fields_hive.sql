-- Diagnostic: carrier_amount vs consolidator_amount vs tax_carrier fields
-- Based on Oliver's SQL structure
-- Airlines: EY, BA, NH | Scope: 2026 YTD
-- Purpose: confirm which field carries the actual airline penalty fee

SELECT
  p.ownerairline,
  CASE
    WHEN COALESCE(e.carrier_amount, 0) > 0
      THEN 'carrier_gt0'
    WHEN COALESCE(e.carrier_amount, 0) = 0
     AND COALESCE(e.consolidator_amount, 0) > 0
      THEN 'consolidator_only_gt0'
    WHEN COALESCE(e.carrier_amount, 0) = 0
     AND COALESCE(e.consolidator_amount, 0) = 0
     AND COALESCE(e.all_un_use_tax_carrier_amount, 0) > 0
      THEN 'tax_carrier_only_gt0'
    WHEN COALESCE(e.carrier_amount, 0) = 0
     AND COALESCE(e.consolidator_amount, 0) = 0
     AND COALESCE(e.all_un_use_tax_carrier_amount, 0) = 0
     AND COALESCE(e.no_show_tax_carrier_amount, 0) > 0
      THEN 'no_show_tax_only_gt0'
    ELSE 'all_zero_or_null'
  END                                                              AS fee_bucket,
  e.is_allowed_all_un_use_show_up                                  AS cancel_flag,
  COUNT(*)                                                         AS row_count,
  ROUND(AVG(COALESCE(e.carrier_amount, 0)), 2)                    AS avg_carrier,
  ROUND(AVG(COALESCE(e.consolidator_amount, 0)), 2)               AS avg_consolidator,
  ROUND(AVG(COALESCE(e.all_un_use_tax_carrier_amount, 0)), 2)     AS avg_tax_carrier,
  ROUND(AVG(COALESCE(e.no_show_tax_carrier_amount, 0)), 2)        AS avg_no_show_tax

FROM flt_predb.v_fltorderdb_o_orders AS o
JOIN flt_predb.v_fltorderdb_fltintlorderpolicy AS p
  ON p.orderid = o.orderid
JOIN flt_predb.v_fltorderdb_o_orderdetail AS d
  ON d.orderid = o.orderid
JOIN flt_predb.v_fltorderdb_o_flightextdetail f
  ON f.orderid = o.orderid AND f.sequence = 1
LEFT JOIN ods_fltairtickets_mysql_fltintlpenaltydb.o_customer_cancellation e
  ON e.isactivated = 1
  AND f.policytokenno = e.token
  AND e.condition_start_minute = -1
  AND e.d = substr(cast(date_add(current_timestamp, INTERVAL -1 day) AS VARCHAR), 1, 10)

WHERE o.OrderStatus NOT IN ('C')
  AND o.FlightClass = 'I'
  AND o.orderdate >= '2026-01-01'
  AND p.ownerairline IN ('EY', 'BA', 'NH')

GROUP BY 1, 2, 3
ORDER BY p.ownerairline, row_count DESC
;
