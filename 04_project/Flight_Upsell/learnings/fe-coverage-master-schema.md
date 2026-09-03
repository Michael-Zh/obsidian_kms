# FE & Coverage Master — Schema & Cleanup

> Design spec for the supply + exposure layers that pair with the order master
> (conversion). Together they form the **supply → exposure → conversion** chain
> used in airline deep-dives. Companion: [master-table-schema.md](master-table-schema.md)
> (order), [fare-card-cleanup-rules.md](fare-card-cleanup-rules.md) (Rules 1/2/3).

## The three-layer chain

| Layer | Artifact | Grain | Key |
|---|---|---|---|
| Supply | `coverage_brand_master_v1` (materialized) | one row per (d, airline, brand fare, route) | `d`, `vc` |
| Exposure | `fe_exposure_template.sql` (canonical SQL, NOT materialized) | one row per fare-card exposure (after Rules 1/2/3) | `(d, vid, sid, pvid)` |
| Conversion | `order_level_master_v3` (materialized) | one row per primary order | `primaryorderid_fill` |

FE is kept as a template (not materialized): card-event grain ≈ 12M rows/day (~4.4B/yr),
too expensive to materialize; BQ materialized views can't express Rule 2 (ROW_NUMBER)
or Rule 3 (self-join). Coverage is materialized because it is already pre-aggregated
(~700K rows/day) and the `idx_dim` cleanup is error-prone enough to bake in once.

---

## Coverage master (`coverage_brand_master_v1`)

- **Build**: [sql/coverage_brand_master.sql](../sql/coverage_brand_master.sql)
- **Source**: `ibu_bi_dw_source.dw_fltdb_adm_rsc_engine_airline_route_brand_cover_v2_di`
- **Grain**: one row = one brand fare on one route on one day (source grain — this is a
  clean + enrich + preserve, NOT a re-aggregation).
- **Scope**: 2026-03-22 → 2026-08-31 (~5.5 months; source has earlier partitions but no
  city_pair + economy data before 03-22). 42M rows, 59 airlines, LCC 10% / FSC 90%.

### Cleanup baked in (do NOT re-derive)

1. **`idx_dim = 'city_pair'`** — the source slices the SAME searches across 5 `idx_dim`
   values (city_pair / country_pair / engine_type / rsv_type / rsv_type+engine_type).
   Summing across slices double-counts the denominator → meaningless weighted average.
   city_pair (airport_pair + city_pair both non-null) is the route-level slice.
   ⚠️ `idx_dim='city_pair'` is only populated on NEWER partitions (≈2026-03-22+). For older
   data, use the equivalent explicit filter `airport_pair IS NOT NULL AND city_pair IS NOT
   NULL` instead of the `idx_dim` value.
2. **`class = 'Y'`** — ⚠️ this is **cabin class** (Y=economy, C=business, W=premium economy,
   F=first), NOT a "brand-fare class" flag. It scopes coverage to economy, matching the
   order master's economy default. (The old H1 SQL's "brand fare class" comment is wrong.)
3. **`brand_name` non-empty** — mapped brand fares only.

### Coverage metric (per airline × brand fare × route)

- `has_brand_cnt / total_cnt` = pre-selection (supply) coverage
- `output_has_brand_cnt / output_total_cnt` = post-selection (display) coverage
- filter rate = `(has_brand - output_has_brand) / has_brand`
- See [sql/coverage_brand.sql](../sql/coverage_brand.sql) for the aligned analysis query.

---

## FE exposure template (`fe_exposure_template.sql`)

- **File**: [sql/fe_exposure_template.sql](../sql/fe_exposure_template.sql)
- **Source**: `edw_usr_ubt_ibu_pageview` (denominator) + `edw_prd_flt_frontendtrace` (cards)
  + `edw_prd_flt_odpageview` (airline-scoped denominator).
- **Join key**: `(d, vid, sid, pvid)` — NOT uid. `sid`/`pvid` cast to STRING (type mismatch).

### Cleanup (Rules 1/2/3, see [fare-card-cleanup-rules.md](fare-card-cleanup-rules.md))

1. UBT middle page = denominator: `p_pageid='10650038753'`, `ua_channeltype='app'`,
   `iscrawler=0`, `context.vid IS NOT NULL`, `duration > 2 OR NULL`. FE trace inflates
   pvid ~55% — never a raw denominator.
2. FE trace latest exposure per `(d,vid,sid,pvid,index,segmentno)` ORDER BY `starttime DESC`.
3. Exclude gappy pvs: `HAVING COUNT(DISTINCT index) = MAX(index) + 1`.

### Airline scoping (two denominators)

Airline X's middle page = `odpageview` outbound `flightno='X'` UNION FE-trace
`concat_airline LIKE '%X%'` (any-leg). Report **two denominators** — they answer
different questions:

1. **Visit-level — "entered the middle page"** (theoretical): all UBT middle-page pvs,
   card or no card. Use this to diagnose *why* a visit produced no card (load latency,
   tracking gap, etc.). FE-unmatched pvs (UBT present, no FE card) belong here.
2. **Card-visible — "saw a fare card"** (actionable): only pvs that actually surfaced
   ≥1 fare card (FE card matched). This is the population our fare-card changes can
   influence, so card-level numerators and attachment rates use this denominator.

---

## Compare table — benefit-combo coverage (HIVE, NOT BQ)

For products with **no brand mapping** (VPL15/VP20, unbranded fares), coverage is measured
by **actual fare benefits** (baggage + refund/change), not brand name.

- **Source (HIVE, SPARK3 only)**: `dwflt.edw_rsc_engine_paimon_agg_intl_compare_result_log_di`
  (paimon — HIVE engine can't read it; use SPARK3 via bigdata-adhoc-mcp).
- **BQ mirror** `ibu_bi_dw_source.dw_fltlogdata_flight_intl_agg_analysis_compareresult_log_etl`
  is **incomplete** (missing `is_low_price`, `prim_order_id`, `atpco_brand_name`) and will
  **NOT be backfilled** — read HIVE for anything needing those fields.
- **Partitions**: only 2026-01-19 and 2026-08-12 populated (2 days; before/after comparison
  possible, no full trend).
- **Grain**: `traceid` = one search (one search → ~33 fare rows). `parent_traceid` = traceid.
  `requesttype` `'14'`/`'24'` kept, `'9'` = preload (exclude). `output='true'` = returned/won.

### Benefit field parsing (verified 2026-09-02)

| Benefit | Field | Format → extract |
|---|---|---|
| Checked bag | `checkedbaggagedetail` | `1,<pieces>,<weight>,<?>;1,<dim>` → weight = **3rd comma-field of the segment before `;`**. `-1`/`0` = none. e.g. `1,1,20,-1;1,158CM` → 20kg |
| Carry-on | `handbaggagedetail` / `carryonbaggagedetail` | weight > 0 = present (7kg / 3kg standard) |
| Refund | `refundfeatures` | `OrgCanRefund,...` vs `OrgNonRefund` |
| Change | `changefeatures` | `OrgCanChange,...` vs `OrgNonChange` |
| Seat | `price_json` (no dedicated column) | `instr(price_json, '"key":"Seat"') > 0` → has_seat. "Value Pack"/"Value Pack Lite 15kg" = seat bundled; "Regular Fare with Luggage 15/20" = no seat. |
| Brand tier | `brandtier` | ⚠️ mixed/unreliable — see note below |

⚠️ `brandtier` is NOT a clean "Basic=1, Value=2" ordinal. Distinct values mix a single-digit
internal tier (1–14, 20), a mapped tier in thousands (1000/1250/2000/3000/4000), multi-segment
joins (`1;1`, `2|2`, `EMPTYTICKET|1`), negatives (`-24`), and ~66M empty/NULL (the largest
bucket). Treat as unreliable for the benefit-combo fallback — omit unless a specific
normalization is confirmed.

### Benefit-combo coverage metric

Classify each fare by `bag_bucket` (no_checked / ≤15 / ≤20 / ≤23 / ≤30 / 30+) ×
`flex_combo` (Not_Flexible / Change_Only / Cancel_Only / Flexible), then:

- pre coverage = `COUNT(DISTINCT IF(has_benefit, traceid)) / COUNT(DISTINCT traceid)`
- post coverage = same but restricted to `output='true'`

This measures "does the airline offer a fare with checked bag ≥20kg + flexibility on this
route?" regardless of brand naming — the non-brand fallback cross-check.
