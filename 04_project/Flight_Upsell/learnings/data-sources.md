# Data Sources Reference — Flight Upsell

> Migrated from Feishu "All about Data" wiki (PDEKwPY4RiNJFMkUz5ZcWuElnSc), last synced 2026-08-23.
> **Convention:** ⚠️ Unverified = not yet used by Michael. BQ project = `trip-ibu-bi-dw-etl` unless noted.

---

## 1. Data Access

### Access Tools

| Tool | Details |
|---|---|
| **Adhoc: ROUTER** | Permission search: https://iam.basebiz.ctripcorp.com/user/myPermission |
| **Flight order details** | http://flight.order.offline.ctripcorp.com/order/page/detail?language=en-US&orderId=...&type=FLIGHT&offset=480 |
| **HIVE permission guide** | https://trip.larkenterprise.com/wiki/LTkKwg3DriynT4kLBVcc90Xdnye |
| **FBU Dashboard** | https://fltinsight.flight.ctripcorp.com/#/flight/internationalKPI/IKPIDetail |
| **IBU BI wiki** | https://trip.larkenterprise.com/wiki/IjlEw5WNWiV1KPkpXN2clWernwe |
| **SPG metadata search** | https://metadata.ops.sgp.tripws.com/#/metadata |
| **BQ user guide** | https://trip.larkenterprise.com/wiki/IX6Iwwqh6ifu6vkvacncGviwnPg |
| **Data sync process** | https://trip.larkenterprise.com/wiki/A1cJwVNe2ihxS7kjLcJcYFg6nHf |
| **HIVE→BQ one-click sync** | https://trip.larkenterprise.com/wiki/IyK9wRtPRiSqagkLo0Hc9tTqnYe |
| **FBU HIVE skills repo** | https://git.dev.sh.ctripcorp.com/fltbianalysis/trip_ds_skills |

### MCP Tools

| Tool | Link |
|---|---|
| Hive Data Query MCP | https://aicoding.portal.ctripcorp.com/mcp-server/detail?id=6a4b9c9ec2f362212ef012f4&from=market |
| Live Tracking mPaaS | https://mpaas.ctripcorp.com/cdataV2/search?appId=37&env=prod&metric=ibu_flt_app_middle_fare_card_exposure |
| UBT trace detail | https://ubtdata.bdai.ctripcorp.com/web/center/dataCenter/trace/detail?keyName=ibu_flt_app_middle_fare_card_exposure |

---

## 2. Order Data

| Table (BQ) | Table (HIVE) | Description |
|---|---|---|
| `ibu_bi_dw_cdw.edw_ord_flt_order` | — | All flight orders. Primary analysis table. |
| `ibu_bi_dw_cdw.edw_prd_flt_factfltsegment_eng` | — | Segment-level brand fare / benefit info. Fields: free bag, brand name, code share, seat rights. **Partitioned by `d` (daily snapshot, 3-day retention)** — use `d = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)`. |
| `ibu_bi_dw_cdw.edw_ord_ibu_order` | — | All IBU orders (all product lines) |
| `ibu_bi_dw_cdw.edw_fin_ibu_financeorder` | — | Financial order data |
| `ibu_bi_dw_source.flt_bidb_v_edw_factfltprimaryorder_eng` | — | Larger order table; includes `back_takeofftime` |
| `ibu_bi_dw_source.flt_bidb_olap_fltrefund_eng` | — | Refund request time |
| `ibu_bi_dw_source.flt_bidb_dw_factfltpassenger_eng` | `flt_bidb.dw_factfltpassenger_eng` | Passenger data (contains unmasked pax name!) |
| `ibu_bi_dw_cdw.adm_vfr_tag_order_final` | — | VFR tag (family name origin, not just passport nationality) |
| `ibu_bi_dw_source.dw_fltdb_edw_flt_overseasteam_orderdetail` | `dw_fltdb.v_flt_overseasteam_orderdetail` | Brand fare audit list per carrier; carrier+PJ to agency code |

---

## 3. Brand Fare / Upsell

### Brand Fare Mapping & Coverage

| Table (BQ) | Table (HIVE) | Description |
|---|---|---|
| `ibu_bi_dw_source.ods_fltairtickets_mysql_fltresourcedb_tb_brandname_unified` | `ods_fltairtickets_mysql_fltresourcedb.tb_brandname_unified` | Brand fare mapping (~50 airlines). Join with `flt_bidb.dw_factfltsegment`. Dashboard: https://smartweb.flight.ctripcorp.com/main/intlfareanalysis/brandnameunified |
| `ibu_bi_dw_source.dw_fltdb_adm_rsc_engine_airline_route_brand_detail_di` | `dw_fltdb.adm_rsc_engine_airline_route_brand_detail_di` | **Compare-result coverage (primary for supply-side)**. Adds haul type, gambling/lowest-price tag. |

Coverage types (per Vivi/Miao):
- Coverage **before** fare selection — the ceiling
- Coverage **after** fare selection — what actually shows on the middle page (AGG filters duplicates, sometimes useful content)

Brand fare coverage dashboard: https://artnova.ops.sgp.tripws.com/#/configuration/dashboard/c6cdad1d-3da6-4ec3-b6db-d4e46a851fd1

AGG comparison raw table (HIVE): `dw_fltlogdata.flight_intl_agg_analysis_compareresult_log_etl`

### Lowest Fare Tracking & Upsell Rate

| Table (BQ) | Table (HIVE) | Description |
|---|---|---|
| `ibu_bi_dw_source.dw_fltdb_edw_deal_ord_intl_is_middle_page_lowest_price_di` | `dw_fltdb.edw_deal_ord_intl_is_middle_page_lowest_price_di` | **Primary upsell rate table.** One row per primary order. `is_lowest_price` = back-end tag post price comparison. Removes flight+hotel and rebooking orders. ~13% null = no middle-page trace. |

Dashboard: https://artnova.ops.sgp.tripws.com/#/dashboard/c30870d7-6511-429d-820a-acd9928b30cc

### Brand Fare Price Comparison

| Table (BQ) | Table (HIVE) | Description |
|---|---|---|
| `ibu_bi_dw_source.dw_fltdb_edw_mkt_crw_baggage_brandname_price_compare_log_di` | `edw_mkt_crw_baggage_brandname_price_compare_log_di` | Brand fare price comparison log |
| `ibu_bi_dw_source.dw_fltdb_edw_mkt_crw_baggage_price_compare_log_hi` | `dw_fltdb.edw_mkt_crw_baggage_price_compare_log_hi` | Base for brand fare price competitiveness + coverage dashboard. Related sheet: https://trip.larkenterprise.com/sheets/PaDzs0B5Ghs4qvtXy2Bca6jFnrf |

### Refund / Rebook

| Table (BQ) | Table (HIVE) | Description |
|---|---|---|
| `ibu_bi_dw_source.flt_bidb_edw_deal_ref_rbk_intl_info` | — | Refund/rebook data |

### Reference Docs

- Brand Fare Info Explain (field definitions): https://trip.larkenterprise.com/docx/J2yVdgkR3oxchyxTswwl3fiKgad
- Brand name & attribute coverage: https://trip.larkenterprise.com/wiki/YNu2wJ9JXi0rMkkwGPVcKDFfnne
- Trip Upsell Analytics Framework: https://trip.larkenterprise.com/wiki/AnxmwInO1iYkc1kWbzicOrt4njc

---

## 4. Frontend Trace

| Table (BQ) | Table (HIVE) | Description |
|---|---|---|
| `ibu_bi_dw_source.dw_fltdb_edw_log_trc_trip_flt_fare_exposure_click_order_trace` | — | Raw FE trace (fare exposure, click, order). Session IDs conf: http://conf.ctripcorp.com/pages/viewpage.action?pageId=786308542 |
| `ibu_bi_dw_cdw.edw_prd_flt_frontendtrace` | — | **Summarized FE trace.** Used for exposure/click/order funnel. Filter `ua_channeltype = 'app'`. Reference: [fare-card-tracking-entities.md](fare-card-tracking-entities.md), [fare-card-cleanup-rules.md](fare-card-cleanup-rules.md) |
| `ibu_bi_dw_cdw.edw_usr_ubt_ibu_pageview` | — | **UBT page view.** Middle-page denominator. Join key: `(d, cid, sid, pvid)`. Seat fields: `segment_rights_info_list`, `seats_right_info`, `segmentfarerightsinfos`. Reference: [middle-page-definition.md](middle-page-definition.md) |
| `ibu_bi_dw_source.ods_fltairtickets_mysql_fltresourcedb_tb_brandname_unified` | — | Front-end brand name unified mapping |

Debugging tools:
- UBT trace detail: https://ubtdata.bdai.ctripcorp.com/web/center/dataCenter/trace/detail?keyName=ibu_flt_app_middle_fare_card_exposure
- Cloud phone (visual inspection): https://ubtdata.bdai.ctripcorp.com/web/tracking/vet/cloudPhone?appType=Trip&platform=Android

---

## 5. Baggage

| Table (BQ) | Table (HIVE) | Description |
|---|---|---|
| `ibu_bi_dw_source.dwflt_sharedb_edw_factxproductorderdetail_ibu` | — | X-product: self-bundle and pre/post booking x-bag attachment. `businesstype` values — 1: XAPI Regular; 2: Agg Gift-Reduction; 3: Agg Regular; 4: Agg Strong Binding; 5: XAPI Dependent; 9: Direct |
| ⚠️ `ibu_bi_dw_source.dwflt_sharedb_edw_deal_fin_xproductorderdetail_ibu` | — | IBU ancillary. `producttype` 8=Checked, 1015=Carry-on. Main Echo/Harry table. `booktype` 1=pre, 2=post |
| ⚠️ `ibu_bi_dw_source.dw_fltdb_dw_xproduct_o_baggages` | — | X-product baggage type, weight, piece |
| `ibu_bi_dw_source.dw_fltdb_edw_deal_ord_factxproductorderdetail_all_ibu` | `dw_fltdb.edw_deal_ord_factxproductorderdetail_all` (base) · `_all_ibu` = IBU view (wraps base; errors on CDH5.7) | **Master v3 x-product source** (baggage + guarantee). `packagename` = bundle, `productname` = component, `producttype`: 36=退票 · 30=改签 · 1049=退另订 · 123=回电 · 121=短信 · 1013=中转多票. `bookpagename`: 中间页/填写页. `businesstype_detail`: 4=bundle ≠4=xpage. |
| ⚠️ — | `dw_fltdb.v_edw_ibuxdimension_fltinsight` | Ancillary — FBU (official FBU ancillary table) |
| ⚠️ — | `ods_fltairtickets_fltorderdb.o_xproductorderdetail` | Raw x-product order detail; `producttype=8` + `businesstype=4` = baggage attach from fare family |
| ⚠️ `ibu_bi_dw_source.flt_bidb_dw_factfltsegment_eng` | `flt_bidb.dw_factfltsegment` | Contains refund/change policy fields + free baggage allowance indicator |

Dashboards: [self bundle](https://artnova.ops.ctripcorp.com/#/dashboard/72729045) | [carry-on coverage](https://artnova.ops.ctripcorp.com/#/dashboard/4ef1aad0) | [checked bag](https://artnova.ops.ctripcorp.com/#/dashboard/9dcff8d5)

---

## 7. Dimensions & Reference

| Table (BQ) | Table (HIVE) | Description |
|---|---|---|
| `ibu_bi_dw_dim.dim_prd_pub_region` | — | Region dimension |
| `ibu_bi_dw_dim.dim_prd_flt_airline` | `dim_fltdb.dimairline` | Airline code → name |
| `ibu_bi_dw_dim.dim_prd_pub_country` | — | Country code |
| `ibu_bi_dw_dim.dim_prd_pub_continent` | — | Continent |
| `ibu_bi_dw_dim.dim_usr_ubt_allpageid` | — | Page ID → page name |
| ⚠️ `ibu_bi_dw_dim.dim_prd_flt_lcc` | — | LCC airlines only |
| ⚠️ `ibu_bi_dw_dim.dim_prd_pub_airport` | `dim_fltdb.dimairport` | Airport code |
| ⚠️ `ibu_bi_dw_dim.dim_fin_ibu_exchangerate_perday` | — | Exchange rate |
| ⚠️ `ibu_bi_dw_source.dim_fltdb_dimtpm` | `dim_fltdb.dimtpm` | Haul type by TPM (FBU definition) |

---

## 8. Other Flight Data (selected)

| Table (BQ) | Table (HIVE) | Description |
|---|---|---|
| `ibu_bi_dw_cdw.tbl_v_cdm_mkt_ibu_traffic_flight_city_daily_190916` | — | Summarized UV, seg, CTR |
| ⚠️ `ibu_bi_dw_cdw.cdm_prd_flt_fltsearch` | — | Flight search data |
| `ibu_bi_dw_source.ods_fltairtickets_mysql_fltbaseflightinfodb_oag_schedule_analyser` | — | OAG schedule (ASK calculation) |
| ⚠️ `ibu_bi_dw_source.dw_fltdb_iata_od` | `dw_fltdb.iata_od` | IATA DDS OD-level pax stats (2-month lag). Fields: `quantity_iata` (market), `quantity_ibu` (Trip share incl. meta), `quantity_ibu_direct` (1-meta only) |
| ⚠️ `ibu_bi_dw_cdw.edw_fin_flt_reve_ful` | `dw_engdb.cdm_fin_flt_reve_ful` | FBU finance |
