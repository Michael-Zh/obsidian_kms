-- MZ_202606_quantification_v2 — Master merged table (MZ + JN)
-- Merged changes vs. MZ previous version:
--   - Date range expanded to 2025-08-01 to CURRENT_DATE() (rolling)
--   - flightclass = 'I' filter added (international orders only, from JN)
--   - datachange_createtime cutoff set to 2025-07-01
--   - e_customer_cancellation CTE added (from JN) → service_fee_type in output
--   - x_BD_ChannelConfigInfo CTE added (from JN) → market + channelenname in output
--   - ownerairline + ownerairline_name added (from JN)
--   - source + subchannel added to segment_table for market join
--   - xbag renamed to xprod; rp_bundle + all_flexibility_bundle added
--   - flexible subquery: SELECT DISTINCT → GROUP BY + MAX() (prevents fan-out double-counting)
--   - effective_flexible_rp: ticket policy + RP bundle (cancel right only)
--   - effective_flexible_all: ticket policy + all flexibility bundle (change + cancel)
--   - rp_bundle_ord_count + all_flexibility_bundle_ord_count added to final SELECT
--
-- v2 changes (benefit fingerprint):
--   - e_customer_cancellation CTE: added is_allowed_all_un_use_show_up + carrier_amount
--     → enables cancel_policy_class (free / paid / not allowed, airline fee only)
--   - c_customer_change CTE added (new): outbound change flag + carrier_strict_amount
--     → enables change_policy_class (free / paid / not allowed, airline fee only)
--   - cancel_policy_class + change_policy_class added to segment_table and final SELECT
--   - Purpose: decompose the flexible tier into benefit fingerprints (baggage × cancel × change)
--     to infer Brand Fare tier without relying on ATPCO brand name mapping
--
-- is_primaryorder design note:
--   MZ filters is_primaryorder = 1 early (in segment_table WHERE), so policy lookup
--   runs only against the primary sub-order's orderid. JN filters late (final SELECT),
--   allowing policy to be picked up from any sub-order (return/connecting legs).
--   This table uses the MZ approach: cleaner counting, avoids self-join inflation.
--   Implication: if a return leg has a different void/24hr policy than the outbound,
--   this table will not capture it. Acceptable trade-off for counting accuracy.

CREATE OR REPLACE TABLE `trip-ibu-adhoc.ibu_adhoc_temp.MZ_202606_quantification_v4`

AS

WITH

brand_en_name AS (

SELECT DISTINCT

carrier,

IF(applicablecabin = 'S', 'W', applicablecabin) AS applicablecabin,

TRIM(REPLACE(LOWER(brandname), ' ', '')) AS atpco_brand_name,

TRIM(REPLACE(LOWER(enname), ' ', '')) AS brand_name,

MAX(CAST(airlinebrandtier AS INT64)) AS airline_brandtier

FROM

`trip-ibu-bi-dw-etl.ibu_bi_dw_source.ods_fltairtickets_mysql_fltresourcedb_tb_brandname_unified`

WHERE

DATE(d) >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)

AND actived = '1'

AND enname IS NOT NULL

AND applicablecabin = 'Y'

GROUP BY ALL

),

xprod AS (

-- Aggregated at primaryorderid_fill level so products purchased on either

-- leg of a round-trip are captured under the same primary order.

SELECT

o.primaryorderid_fill,

MAX(

IF(

x.productname = '手提行李'

AND x.booktype = 1

AND x.businesstype_detail = 4,

1,

0)) AS carryon_bundle,

MAX(

IF(

x.productname = '行李额'

AND x.booktype = 1

AND x.businesstype_detail = 4,

1,

0)) AS checkbag_bundle,

MAX(

IF(

(x.productname LIKE '%退%' OR x.productname LIKE '%改%')

AND x.bookpagename = '中间页',

1,

0)) AS all_flexibility_bundle,

MAX(

IF(

x.packagename = 'Cancellation Guarantee - Bundled with Fare'

AND x.bookpagename = '中间页',

1,

0)) AS rp_bundle

FROM

`trip-ibu-adhoc.ibu_adhoc_temp.dw_fltdb_edw_deal_ord_factxproductorderdetail_all`

x

JOIN `trip-ibu-bi-dw-etl.ibu_bi_dw_cdw.edw_ord_flt_order` o

ON x.orderid = o.orderid

WHERE

DATE(x.orderdate) BETWEEN "2025-08-01" AND CURRENT_DATE()

AND x.sequence = 1

GROUP BY 1

),

lowest_price_ranked AS (

SELECT

CAST(primary_orderid AS BIGINT) AS primary_orderid,

is_lowest_price,

ROW_NUMBER() OVER (PARTITION BY primary_orderid ORDER BY d DESC) AS rn

FROM

`trip-ibu-bi-dw-etl.ibu_bi_dw_source.dw_fltdb_edw_deal_ord_intl_is_middle_page_lowest_price_di`

WHERE

CAST(d AS DATE) BETWEEN "2025-08-01" AND CURRENT_DATE()

AND is_trip = 'T'

AND is_rebook_new_order = 0

AND subchnl < 7900000

AND is_lowest_price IS NOT NULL

),

lowest_price AS (

SELECT primary_orderid, is_lowest_price

FROM lowest_price_ranked

WHERE rn = 1

),

f_textdetail AS (

SELECT DISTINCT

a.orderid,

a.sequence,

a.policytokenno

FROM

`trip-ibu-bi-dw-etl.ibu_bi_dw_source.ods_fltairtickets_fltorderdb_o_flightextdetail`

a

JOIN

(

SELECT DISTINCT orderid

FROM `trip-ibu-bi-dw-etl.ibu_bi_dw_cdw.edw_ord_flt_order`

WHERE

orderdate_d BETWEEN "2025-08-01" AND CURRENT_DATE()

AND is_primaryorder = 1

) b

ON a.orderid = b.orderid

WHERE

DATE(a.d) = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)

AND a.sequence = 1

),

g_other AS (

SELECT DISTINCT

a.token,

a.ticketoperationtype

FROM

`trip-ibu-bi-dw-etl.ibu_bi_dw_source.ods_fltairtickets_mysql_fltintlpenaltydb_o_other_detail`

a

JOIN

(

SELECT DISTINCT orderid

FROM `trip-ibu-bi-dw-etl.ibu_bi_dw_cdw.edw_ord_flt_order`

WHERE

orderdate_d BETWEEN "2025-08-01" AND CURRENT_DATE()

AND is_primaryorder = 1

) b

ON a.orderid = b.orderid

WHERE

a.isactivated = 1

AND DATE(a.d) = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)

),

e_customer_cancellation AS (

-- cancel_policy_class source: is_allowed + carrier_amount (airline fee only, excl. Trip/consolidator)

-- condition_start_minute = -1: current active window (sentinel value)

-- is_allowed values: H = allowed, T = not allowed (not Y/N)

SELECT DISTINCT

e.token,

e.service_fee_type,

e.is_allowed_all_un_use_show_up,

e.all_un_use_show_up_amount

FROM

`trip-ibu-bi-dw-etl.ibu_bi_dw_source.ods_fltairtickets_mysql_fltintlpenaltydb_o_customer_cancellation`

e

JOIN

(

SELECT DISTINCT orderid

FROM `trip-ibu-bi-dw-etl.ibu_bi_dw_cdw.edw_ord_flt_order`

WHERE

orderdate_d BETWEEN "2025-08-01" AND CURRENT_DATE()

AND is_primaryorder = 1

) b

ON e.orderid = b.orderid

WHERE

DATE(e.d) = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)

AND e.isactivated = 1

AND e.condition_start_minute = -1

),

c_customer_change AS (

-- change_policy_class source: outbound is_allowed + carrier_strict_amount (airline fee only)

-- no_show_strict_condition_start_minute = -1: current active window (sentinel value, mirrors cancel)

-- is_allowed values: H = allowed, T = not allowed (not Y/N)

SELECT DISTINCT

c.token,

c.is_allowed_out_all_un_use_show_up_strict,

c.out_all_un_use_show_up_strict_amount

FROM

`trip-ibu-bi-dw-etl.ibu_bi_dw_source.ods_fltairtickets_mysql_fltintlpenaltydb_o_customer_change`

c

JOIN

(

SELECT DISTINCT orderid

FROM `trip-ibu-bi-dw-etl.ibu_bi_dw_cdw.edw_ord_flt_order`

WHERE

orderdate_d BETWEEN "2025-08-01" AND CURRENT_DATE()

AND is_primaryorder = 1

) b

ON c.orderid = b.orderid

WHERE

DATE(c.d) = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)

AND c.isactivated = 1

AND c.no_show_strict_condition_start_minute = -1

),

x_BD_ChannelConfigInfo AS (

-- From JN: maps source + subchannel to market and channel name

SELECT DISTINCT

UPPER(x.channel) AS channel,

x.subchannel,

x.market,

x.channelenname

FROM

`trip-ibu-bi-dw-etl.ibu_bi_dw_source.dim_fltdb_dim_bd_channelconfiginfo` x

WHERE x.isactivated = 1

),

segment_table AS (

SELECT DISTINCT

a.region,

EXTRACT(YEAR FROM a.orderdate_d) AS order_year,

EXTRACT(MONTH FROM a.orderdate_d) AS order_month,

a.orderid,

a.primaryorderid_fill,

a.is_primaryorder,

CASE WHEN a.refername = 'Meta' THEN 'Meta' ELSE '1-Meta' END AS isMeta,

a.primorderflightway,

-- Marketing airline (with codeshare remapping)

CASE

WHEN a.airline = 'HV' THEN 'TO'

WHEN a.airline IN ('W4', 'W6', 'W9') THEN 'W6'

ELSE a.airline

END AS order_marketing_airline,

CASE

WHEN dimf1.airlinename_eng = 'TRANSAVIA FRANCE' THEN 'TRANSAVIA'

WHEN a.airline IN ('W4', 'W6', 'W9') THEN 'WIZZ AIR'

ELSE dimf1.airlinename_eng

END AS marketing_airlinename_eng,

dimf1.countrycode AS airline_homecountry,

CASE WHEN dimf1.isbudget = 1 THEN 'LCC' ELSE 'FSC' END AS LCCorFSc,

-- Owner/ticketing airline (from JN)

a.ownerairline AS order_ticketing_airline,

dimf2.airlinename_eng AS order_ticketing_airline_name,

-- Source + subchannel (needed for market join)

UPPER(a.source) AS source,

a.subchannel,

-- OD

a.dportcode,

a.dcityid,

a.dcitycode,

a.dcountryename,

dct.country_code AS Dcountry_code,

a.aportcode,

a.acityid,

a.acitycode,

a.acountryename,

act.country_code AS Acountry_Code,

CONCAT(a.dportcode, '-', a.aportcode) AS airport_pair,

CONCAT(a.dcitycode, '-', a.acitycode) AS city_pair,

CONCAT(dct.country_code, '-', act.country_code) AS country_pair,

a.subprdtype_pos_primorder,

a.primorder_haultype,

IF(

dct.country_code IS NULL

OR act.country_code IS NULL

OR dimf1.countrycode IS NULL,

'N',

IF(

dct.country_code = dimf1.countrycode

AND act.country_code = dimf1.countrycode,

'D',

'I')) AS RouteType,

-- Supplier info

CASE

WHEN d.flightagencyaffiliation IN ('境内供应商')

THEN 'Chinese_Supplier'

WHEN d.flightagencyaffiliation IN ('境内自营') THEN 'CNBSP'

WHEN d.flightagencyaffiliation IN ('境外自营')

THEN 'Oversea_IATA_non_gamble'

WHEN

d.flightagencyaffiliation IN ('境外供应商')

AND a.flightagencyname IN (

'北京乐途二部(国际平台)',

'北京逸趣飞六部(国际平台)')

THEN 'Oversea_IATA_gamble'

WHEN

d.flightagencyaffiliation IN ('境外供应商')

AND a.flightagencyname NOT IN (

'北京乐途二部(国际平台)',

'北京逸趣飞六部(国际平台)')

THEN 'Oversea_Supplier'

ELSE 'error'

END AS suppliertype_toB,

a.bookingchannel,

a.origin_agcycode,

a.origin_intlagenttype,

-- Baggage: fare base only

CASE

WHEN a.is_free_checkinbagen = 'Y' AND a.is_free_carryonbagen = 'Y'

THEN '4.Fare+carry on+checkin'

WHEN a.is_free_checkinbagen = 'Y' AND a.is_free_carryonbagen != 'Y'

THEN '3.fare+check in'

WHEN a.is_free_checkinbagen != 'Y' AND a.is_free_carryonbagen = 'Y'

THEN '2.fare+carry on'

WHEN a.is_free_checkinbagen != 'Y' AND a.is_free_carryonbagen != 'Y'

THEN '1.fare only'

ELSE 'other'

END AS baggage_allowance_group,

-- Baggage: fare base + bundle

CASE

WHEN

a.is_free_checkinbagen IS NULL

AND a.is_free_carryonbagen IS NULL

AND x.checkbag_bundle IS NULL

AND x.carryon_bundle IS NULL

THEN 'other'

WHEN

(a.is_free_checkinbagen = 'Y' OR x.checkbag_bundle = 1)

AND (a.is_free_carryonbagen = 'Y' OR x.carryon_bundle = 1)

THEN '4.Fare+carry on+checkin'

WHEN (a.is_free_checkinbagen = 'Y' OR x.checkbag_bundle = 1)

THEN '3.fare+check in'

WHEN (a.is_free_carryonbagen = 'Y' OR x.carryon_bundle = 1)

THEN '2.fare+carry on'

ELSE '1.fare only'

END AS baggage_incl_bundle_group,

-- Baggage: final resolved field

CASE

WHEN a.has_checkin_baggage != 'Y' AND a.has_carryon_baggage != 'Y'

THEN '1.fare_only_final'

WHEN a.has_checkin_baggage != 'Y' AND a.has_carryon_baggage = 'Y'

THEN '2.fare_carry_on_only_final'

WHEN a.has_checkin_baggage = 'Y' AND a.has_carryon_baggage != 'Y'

THEN '3.fare_check_in_only_final'

WHEN a.has_checkin_baggage = 'Y' AND a.has_carryon_baggage = 'Y'

THEN '4.fare_both_bag_final'

END AS baggage_final,

-- Flexibility: ticket policy (GROUP BY + MAX to guarantee one row per orderid)

flexible.flexible,

-- Cabin

CASE

WHEN b.classname = '头等舱' THEN 'F'

WHEN b.classname = '超级经济舱' THEN 'S'

WHEN b.classname = '公务舱' THEN 'C'

WHEN b.classname = '经济舱' THEN 'Y'

ELSE NULL

END AS cabin_IATAcode,

b.atpco_brand_name,

lp.is_lowest_price,

g.ticketoperationtype,

e.service_fee_type,

-- Benefit fingerprint: cancel policy class (airline fee only)

-- H = allowed, T = not allowed; COALESCE handles NULL carrier_amount as 0

CASE

WHEN

e.is_allowed_all_un_use_show_up = 'H'

AND COALESCE(e.all_un_use_show_up_amount, 0) = 0

THEN '3.free_cancel'

WHEN e.is_allowed_all_un_use_show_up = 'H' AND e.all_un_use_show_up_amount > 0

THEN '2.paid_cancel'

WHEN e.is_allowed_all_un_use_show_up = 'T' THEN '1.no_cancel'

ELSE NULL -- no penalty record (token absent)

END AS cancel_policy_class,

-- Benefit fingerprint: change policy class (outbound only, airline fee only)

CASE

WHEN

c.is_allowed_out_all_un_use_show_up_strict = 'H'

AND COALESCE(c.out_all_un_use_show_up_strict_amount, 0) = 0

THEN '3.free_change'

WHEN

c.is_allowed_out_all_un_use_show_up_strict = 'H'

AND c.out_all_un_use_show_up_strict_amount > 0

THEN '2.paid_change'

WHEN c.is_allowed_out_all_un_use_show_up_strict = 'T' THEN '1.no_change'

ELSE NULL -- no change record (token absent)

END AS change_policy_class,

-- Bundle fields (from xprod, already aggregated at primaryorderid_fill level)

x.rp_bundle,

x.all_flexibility_bundle,

-- Effective flexibility: RP bundle adds cancel right only

-- 1.Not Flexible + rp_bundle → 3.Cancel Only

-- 2.Change Only + rp_bundle → 4.Flexible

-- others unchanged

CASE

WHEN x.rp_bundle = 1 AND flexible.flexible = '1.Not Flexible'

THEN '3.Cancel Only'

WHEN

x.rp_bundle = 1

AND flexible.flexible IN (

'2.Change Only', '3.Cancel Only', '4.Flexible')

THEN '4.Flexible'

ELSE flexible.flexible

END AS effective_flexible_rp,

-- Effective flexibility: all_flexibility_bundle adds both change + cancel rights

-- any ticket + all_flexibility_bundle → 4.Flexible

CASE

WHEN x.all_flexibility_bundle = 1 THEN '4.Flexible'

ELSE flexible.flexible

END AS effective_flexible_all

FROM `trip-ibu-bi-dw-etl.ibu_bi_dw_cdw.edw_ord_flt_order` a

LEFT JOIN

`trip-ibu-bi-dw-etl.ibu_bi_dw_cdw.edw_prd_flt_factfltsegment_eng` b

ON

a.orderid = b.orderid

AND DATE(b.d) = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)

AND b.sequence = 1

LEFT JOIN `trip-ibu-bi-dw-etl.ibu_bi_dw_dim.dim_prd_flt_airline` dimf1

ON a.airline = dimf1.airline

LEFT JOIN `trip-ibu-bi-dw-etl.ibu_bi_dw_dim.dim_prd_flt_airline` dimf2

ON a.ownerairline = dimf2.airline

LEFT JOIN

`trip-ibu-bi-dw-etl.ibu_bi_dw_dim.dim_prd_flt_flightagencyattribute` d

ON a.flightagency = d.flightagencyid

LEFT JOIN `trip-ibu-bi-dw-etl.ibu_bi_dw_dim.dim_prd_pub_city` dct

ON a.dcityid = dct.cityid AND a.dcitycode = dct.citycode

LEFT JOIN `trip-ibu-bi-dw-etl.ibu_bi_dw_dim.dim_prd_pub_city` act

ON a.acityid = act.cityid AND a.acitycode = act.citycode

-- Flexibility: GROUP BY + MAX per orderid prevents fan-out double-counting

LEFT JOIN

(

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

WHERE orderdate_d BETWEEN "2025-08-01" AND CURRENT_DATE()

GROUP BY orderid

) flexible

ON a.orderid = flexible.orderid

LEFT JOIN lowest_price lp

ON a.primaryorderid_fill = lp.primary_orderid

LEFT JOIN xprod x

ON a.primaryorderid_fill = x.primaryorderid_fill

LEFT JOIN f_textdetail ft

ON a.orderid = ft.orderid

LEFT JOIN g_other g

ON ft.policytokenno = g.token

LEFT JOIN e_customer_cancellation e

ON ft.policytokenno = e.token

LEFT JOIN c_customer_change c

ON ft.policytokenno = c.token

WHERE

a.orderdate_d BETWEEN "2025-08-01" AND CURRENT_DATE()

AND a.is_primaryorder = 1

AND a.flightclass = 'I'

AND b.classname IN ('经济舱', '超级经济舱')

AND a.subprdtype_pos_primorder NOT IN ('FCN')

)

SELECT

region,

order_year,

order_month,

CONCAT(order_year, '_', LPAD(CAST(order_month AS STRING), 2, '0'))

AS year_month,

-- Market (from BD_ChannelConfigInfo via source + subchannel)

chan.market,

chan.channelenname,

dportcode,

dcitycode,

Dcountry_code,

aportcode,

acitycode,

Acountry_Code,

airport_pair,

city_pair,

country_pair,

subprdtype_pos_primorder,

primorder_haultype,

RouteType,

isMeta,

suppliertype_toB,

bookingchannel,

origin_agcycode,

origin_intlagenttype,

-- Marketing airline

order_marketing_airline AS marketing_airline,

marketing_airlinename_eng AS marketing_airline_name,

-- Owner/ticketing airline (from JN)

order_ticketing_airline,

order_ticketing_airline_name,

CASE

WHEN

order_marketing_airline IN (

'AA', 'AC', 'AF', 'AS', 'AZ', 'BA', 'BR', 'CA', 'CI', 'CX', 'CZ', 'DL',

'EK', 'EY', 'FD', 'FR', 'GA', 'HX', 'IB', 'JL', 'KE', 'KL', 'LH', 'LX',

'MH', 'MU', 'NH', 'OS', 'OZ', 'PR', 'QF', 'QR', 'SQ', 'TG', 'TK', 'TO',

'UA', 'VB', 'VF', 'VN', 'VS', 'VY', 'W4', 'W6', 'W9')

THEN 'Y'

ELSE 'N'

END AS isBatch1,

LCCorFSc,

airline_homecountry,

cabin_IATAcode,

CASE

WHEN a.cabin_IATAcode = 'Y' THEN 'Economy Class'

WHEN a.cabin_IATAcode = 'S' THEN 'Premium Economy Class'

WHEN a.cabin_IATAcode = 'C' THEN 'Business Class'

WHEN a.cabin_IATAcode = 'F' THEN 'First Class'

ELSE NULL

END AS cabin_IATAcode_en_name,

airline_brandtier,

brand_name,

baggage_allowance_group,

baggage_incl_bundle_group,

baggage_final,

-- Flexibility dimensions

flexible,

effective_flexible_rp,

effective_flexible_all,

-- Void/24hr policy label (from JN)

CASE

WHEN ticketoperationtype = '1' THEN 'void'

WHEN ticketoperationtype = '2' THEN '24 hour free cancel'

WHEN ticketoperationtype = '3' THEN '48 hour free cancel'

WHEN ticketoperationtype = '4' THEN '2 hour free cancel'

WHEN ticketoperationtype IS NULL THEN 'standard (no free cancel policy)'

ELSE ticketoperationtype

END AS ticketoperationtype_meaning,

service_fee_type,

-- Benefit fingerprint dimensions (airline fee only, excl. Trip/consolidator)

cancel_policy_class,

change_policy_class,

-- Order counts

COUNT(DISTINCT a.primaryorderid_fill) AS primary_ord_count,

COUNT(

DISTINCT

CASE WHEN is_lowest_price IS NOT NULL THEN a.primaryorderid_fill END)

AS upsell_base_primary_ord_count,

COUNT(DISTINCT CASE WHEN is_lowest_price = 0 THEN a.primaryorderid_fill END)

AS upsell_primary_ord_count,

-- Void / 24hr ticket policy counts (requires both ticketoperationtype AND service_fee_type IN (1024,16))

COUNT(

DISTINCT

CASE

WHEN ticketoperationtype = '2' AND service_fee_type IN (1024, 16)

THEN a.primaryorderid_fill

END) AS free_cancel_24h_ord_count,

COUNT(

DISTINCT

CASE

WHEN ticketoperationtype = '1' AND service_fee_type IN (1024, 16)

THEN a.primaryorderid_fill

END) AS void_ord_count,

COUNT(

DISTINCT

CASE

WHEN

(

ticketoperationtype = '2'

OR (

ticketoperationtype = '1' AND chan.market IN ('US', 'BR', 'KR')))

AND service_fee_type IN (1024, 16)

THEN a.primaryorderid_fill

END) AS overwritten_ord_count,

-- Flexibility bundle counts

COUNT(DISTINCT CASE WHEN rp_bundle = 1 THEN a.primaryorderid_fill END)

AS rp_bundle_ord_count,

COUNT(

DISTINCT

CASE WHEN all_flexibility_bundle = 1 THEN a.primaryorderid_fill END)

AS all_flexibility_bundle_ord_count

FROM segment_table a

LEFT JOIN brand_en_name b

ON

a.order_marketing_airline = b.carrier

AND a.cabin_IATAcode = b.applicablecabin

AND TRIM(REPLACE(LOWER(a.atpco_brand_name), ' ', '')) = b.atpco_brand_name

LEFT JOIN x_BD_ChannelConfigInfo chan

ON

a.source = chan.channel

AND CAST(a.subchannel AS STRING) = CAST(chan.subchannel AS STRING)

GROUP BY ALL