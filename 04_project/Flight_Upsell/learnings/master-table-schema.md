# Master Table — Schema & Dimension Handling (order-level)

> Design spec for the order-level master table — the single source of truth for global
> upsell analysis. Review this before writing the build SQL.
> Companion: [upsell-metric-definitions.md](upsell-metric-definitions.md) (metric口径).

## Grain & key

- **Base table**: `edw_ord_flt_order` (primary-order grain via `primaryorderid_fill`). RT-duration +
  time fields come from `flt_bidb_v_edw_factfltprimaryorder_eng` (joined, not the base).
- **One row per primary order** = `primaryorderid_fill` (NOT segment `orderid`).
- `segmentno` = leg number (1=outbound, 2=return, 3+=multi-city); `sequence` = within-leg flight
  order (resets per leg; 1 = first flight). Outbound first segment = `segmentno=1 AND sequence=1`;
  return first segment = `segmentno=2 AND sequence=1`. (Verified 2026-09-01: segmentno=2 rows start
  at sequence=1.) ⚠️ `sequence=1` without a `segmentno` filter hits BOTH legs.
  ⚠️ **`segmentno` restarts per SUB-order** (each sub-order's first leg = segmentno=1), so a
  multi-sub-order primary order fans out when joining segments on `orderid` — every sub-order
  contributes its own `segmentno=1`. Outbound/return attribution MUST filter `is_primaryorder = 1`
  (the primary sub-order). Verified 2026-09-01: without this, 26.6% of orders duplicate (grain break)
  and outbound dimensions are internally inconsistent across the duplicate rows.
- Trip way = `primorderflightway` (`S` = OW, `D` = RT, `M` = multi-city).
- Partition by order month (`orderdate_d`); cluster by marketing airline + region.

## Base filters (eligibility)

- `flightclass = 'I'`
- Order-level dims are primary-order-level (invariant across sub-orders) → take one row per
  `primaryorderid_fill`; dims are identical whether you filter `is_primaryorder = 1` or dedupe.
- Segment-level dims (airline / brand / baggage / cabin) must cover ALL segments of the primary
  order — join the segment table on `primaryorderid_fill` (via `orderid`), not just the primary
  sub-order's `sequence = 1`.
- `subprdtype_pos_primorder NOT IN ('FCN')`
- Economy only (default scope): `so.classname = '经济舱'` on the `seg_out` LEFT JOIN (v2, 2026-09-01)
  — non-economy orders are KEPT (not silently dropped) and flagged `is_non_economy = 1`; missing
  outbound segments flagged `is_segment_missing = 1`. Downstream economy scope =
  `is_non_economy = 0 AND is_segment_missing = 0`.
- Crawler filter: `iscrawler = 0` applies to UBT / FE-trace denominators only — the order table
  (`edw_ord_flt_order`) has NO `iscrawler` column, so the order master has no crawler filter.
- Shanghai time (UTC+8)
- FBU default filters:
  - `uid NOT IN ('HuaMeiYiDa','M351274275','M2555541076','M117699353','_U2662303168')` (test/internal)
  - `orderstatus IN ('S','T','R')` (valid statuses)
  - `manualset = 'F'` (not manually set)
  - `NOT (SOURCE = 'Affiliate' AND subchannel IN ('778105','108352','777122'))`

## Dimension handling

### A. Order-level dimensions (1 value per primary order; direct from `edw_ord_flt_order`)

| Dimension | Field(s) | Values |
|---|---|---|
| Trip way | `primorderflightway` | `S` = OW, `D` = RT |
| Region | `region` | site region |
| Market / channel name | channel config (`x_BD_ChannelConfigInfo`) | market, channelenname |
| Channel | `channeltype` | app / online / h5 |
| Haul | `primorder_haultype` | short / medium / long |
| Supplier type | (a) `suppliertype_toB` via `flightagencyaffiliation` (CASE below) · (b) sourcing type via `origin_intlagenttype` × `bookingchannel` (see below) | suppliertype_toB: Chinese_Supplier / CNBSP / Oversea_IATA_non_gamble / Oversea_IATA_gamble / Oversea_Supplier · sourcing: TFLCCNDC / CNSupplier / OverseasSupplier / OverseasIATA / CNBSP |
| Gambling type | `producttype` → `gamblingYN` (CASE below) | gambling (CN consolidator / project mask / delayed) vs non-gambling |
| Booking channel / sourcing | `bookingchannel`, `origin_intlagenttype`, `origin_agcycode` | GDS / NDC / … |
| Order month | `orderdate_d` | yyyy-mm (partition key) |
| `isMeta` (flag, not filter) | `refername = 'Meta'` → Meta, else 1-Meta (order table) | 1-Meta / Meta — keep BOTH (Meta retained, not dropped). `subchnl < 7900000` is a SEPARATE scope filter (already in the lp join) — NOT part of isMeta |
| Upsell flag | `is_lowest_price` (join `primaryorderid_fill` = `primary_orderid`, dedupe latest `d`) | 0 / 1 / NULL |

#### Supplier & gambling classification (exact CASE)

```sql
-- suppliertype_toB
CASE
  WHEN d.flightagencyaffiliation IN ('境内供应商') THEN 'Chinese_Supplier'
  WHEN d.flightagencyaffiliation IN ('境内自营') THEN 'CNBSP'
  WHEN d.flightagencyaffiliation IN ('境外自营') THEN 'Oversea_IATA_non_gamble'
  WHEN d.flightagencyaffiliation IN ('境外供应商')
       AND a.flightagencyname IN ('北京乐途二部(国际平台)', '北京逸趣飞六部(国际平台)')
    THEN 'Oversea_IATA_gamble'
  WHEN d.flightagencyaffiliation IN ('境外供应商')
       AND a.flightagencyname NOT IN ('北京乐途二部(国际平台)', '北京逸趣飞六部(国际平台)')
    THEN 'Oversea_Supplier'
  ELSE 'error'
END AS suppliertype_toB

-- gamblingYN
CASE
  WHEN a.producttype IN ('CSDPrivate','CSD','PlatformsPrivate','RTKSeat','BSeat')
    THEN 'gambling products from CN consolidator'
  WHEN a.producttype IN ('OverseasPrivate','OverseasLow')
    THEN 'gambling product from project mask'
  WHEN a.producttype IN ('CSDPrivateDown','PLATFORMSPRIVATEDOWN','RTSEATDOWN','CSDDown')
    THEN 'delayed-CN consolidator'
  WHEN a.producttype IN ('OverseasDown') THEN 'delayed-project mask'
  ELSE 'non-gambling'
END AS gamblingYN
```

#### Sourcing type (`origin_intlagenttype` × `bookingchannel`)

`origin_intlagenttype` is also a supplier-type signal (采购来源 — which Trip connection the supply came from):

| origin_intlagenttype | bookingchannel | Meaning |
|---|---|---|
| TFLCCNDC | TF-WS | Trip NDC direct connect (LCC + now FSC) |
| CNSupplier | CSD-WS | CN consolidator (screen-scrape) |
| OverseasSupplier | GDS-WS / OZD-WS | overseas supplier (GDS) |
| OverseasIATA | 1A-WS / 1B-WS / 1G-WS | overseas IATA (Amadeus / Abacus / Galileo) |
| CNBSP | — | CN BSP direct |

#### User attributes

Join `fact_audience_ibu_flight_order_user_label` (alias `user`) on `a.orderid = user.orderid`.

| Dimension | Field | Values |
|---|---|---|
| `orderindex` | `user.uid_flt_order_index` | 1st / 2nd / 3rd / 4th+ order |
| `NewOrOld` | `user.uid_flt_order_index` | 1st order / repeat_order |
| `neworoldYear` | `user.uid_flt_firstorder_orderdate` | newin2020 … newin2026 / before 2020 |

#### Primary-order measures (window over `primaryorderid_fill`)

| Measure | Formula | Note |
|---|---|---|
| `primary_ord_quantity` | `SUM(ord_quantity) OVER (PARTITION BY primaryorderid_fill)` | `ord_quantity` = pax × segments (passenger-segment volume), additive |
| `primary_pax_sum` | fact table `persons` (join `flt_bidb_v_edw_factfltprimaryorder_eng`) | `persons` = adult+child+infant (authoritative, 99.96% coverage). NOT MAX/SUM `ord_persons`: `ord_persons` is per (sub-order × passengertype) — MAX undercounts children/infants (−5.1%), SUM double-counts leg splits (+37.7%) |
| `primary_amount` | `SUM(amount) OVER (…)` | RMB, base fare+taxes+fuel, EXCLUDES ancillary/insurance |
| `primary_actual_paid_price` | `SUM(tot_price) OVER (…)` | total paid incl. ancillary/service fees/insurance |

#### `Ishomecarrierornot`

```sql
CASE WHEN LOWER(dim_prd_flt_airline.countrycode) = a.region THEN 'home-carrier'
     ELSE 'non-home-carrier' END
```
— airline home country vs order market region (segment-level: marketing airline).

### B. Segment-level dimensions — resolved to primary order

**Rule: attribute to the OUTBOUND leg (`segmentno = 1`, `sequence = 1` = first outbound flight)** — fare selection is anchored on the
outbound search. For RT, also carry return-leg columns so mixed-airline and RT duration are
covered without a rebuild. Deeper per-leg detail is NOT pre-joined — join the segment table on
demand when a specific deep-dive needs it.

| Dimension | Source | Handling |
|---|---|---|
| Marketing airline | segment `airline` | outbound + codeshare remap (HV→TO only; W4/W6/W9 kept separate) |
| LCC/FSC | `dim_prd_flt_airline.isbudget` | outbound marketing airline's `isbudget` (return-leg type NOT recorded) |
| Brand | `atpco_brand_name` + `ori_brand_name` (+ `show_brand_name`) + `airline_brandtier` | outbound; store RAW columns + mapped `brand_name`; fallback (mapped→atpco→ori→unbranded) at ANALYSIS time, not baked in |
| Seat | segment `brand_attributes` (REPEATED, seat attr IDs) / `interests_attribute` (JSON) | outbound; seat entitlement (FSC tier distinction) |
| Baggage | multi-level (see below) | fare / +MP bundle / +fill-in / full (departed / anytime) |
| Cabin | segment `classname` | outbound (economy-only filter) |
| OD | `dport`/`aport` (airport) + `dcity`/`acity` (city) + country (`dcountryename`/`acountryename` or `dim_prd_pub_city` → country_code) | outbound; also concat `airport_pair`/`city_pair`/`country_pair` |
| `concat_airline` | all segments' `airline` (sequence order, remapped) | full itinerary airline string — enables any-leg analysis (e.g. "any order touching AirAsia" = `concat_airline LIKE '%FD%'`) + multi-airline detection |

**Return-leg columns** (NULL for OW):

| Column | Source | Purpose |
|---|---|---|
| `return_depart_date` | fact table `back_takeofftime` | return departure (first return leg); NOT segment `sequence=2` |
| `return_airline` | `concat_airline` return portion | first airline of the return |
| `return_brand` | segment table `segmentno = 2 AND sequence = 1` | return first flight's brand — `segmentno` = leg, `sequence` = within-leg |

#### Baggage & flexibility (split dims → final combo)

**Baggage** — carry-on and checked are **separate** dimensions (a customer can add either or both).

Fare-embedded attributes (outbound; checked baggage only — weight + pieces distinguish FSC fare
tiers; carry-on is fixed/standard, not tracked):
- `checkin_bagweight` — checked bag weight (kg; 0 / −1 = none)
- `checkin_bagnumber` — checked bag pieces (order table; 0=none, >0=count, −1=unlimited)
- `is_free_checkinbag` — free checked-bag flag = order `is_free_checkinbagen` (EN 'Y'/'N')
- `is_free_carryonbag` — free carry-on flag = order `is_free_carryonbagen` (EN 'Y'/'N')
  ⚠️ v3 reads these from the ORDER table EN fields — the segment table stores Chinese
  是/否/以航司客规为准 and was breaking `baggage_combo`.

Raw x-product flags from `dw_fltdb_edw_deal_ord_factxproductorderdetail_all_ibu` (join on
`orderid`, `sequence=1`, `productname IN ('行李额','手提行李')`). `booktype`: 1 = with ticket,
2 = post-booking add-on. `businesstype_detail`: 4 = middle page bundle, ≠4 = fill-in/other.
Post-booking is split by departure: `_predep` (`orderdate < takeofftime`) vs `_departed`
(`orderdate >= takeofftime`).

| Flag | productname | booktype | businesstype_detail |
|---|---|---|---|
| `carryon_bundle` / `carryon_xpage` | 手提行李 | 1 / 1 | 4 / ≠4 |
| `carryon_postbooking_predep` / `carryon_postbooking_departed` | 手提行李 | 2 / 2 | — |
| `checkbag_bundle` / `checkbag_xpage` | 行李额 | 1 / 1 | 4 / ≠4 |
| `checkbag_postbooking_predep` / `checkbag_postbooking_departed` | 行李额 | 2 / 2 | — |

Per-type inclusive level (compute **independently** for carry-on and checked):
- `carryon_level` = fare (`is_free_carryonbag`) → +`carryon_bundle` → +`carryon_xpage` → +`carryon_postbooking_predep` → +`carryon_postbooking_departed`
- `checkbag_level` = fare (`is_free_checkinbag`) → +`checkbag_bundle` → +`checkbag_xpage` → +`checkbag_postbooking_predep` → +`checkbag_postbooking_departed`

**Canonical checked-bag attach rates (v3, 2026-09-02)** — the default baggage metrics:
- `checkbag_mid_attach` = `is_free_checkinbag = 'Y' OR checkbag_bundle = 1` — fare-embedded + middle-page bundle ("does the middle page capture the checked-bag need?")
- `checkbag_final_attach` = `checkbag_mid_attach OR checkbag_xpage = 1 OR checkbag_postbooking_predep = 1 OR checkbag_postbooking_departed = 1` — all sources (final attach)

Final combo (the grouping):
- `baggage_combo` = no_bag / carryon_only / checkbag_only / bag+carryon

**Flexibility** — cancel (退) and change (改) are **separate** dimensions.

- fare-embedded: `nonref` (cancel) + `nonrebook` (change) from `edw_ord_flt_order_view`
- MP bundle: `rp_bundle` (cancel guarantee) + `all_flexibility_bundle` (退/改)
- Final combo: `flexibility_combo` = Not_Flexible / Change_Only / Cancel_Only / Flexible

### C. Derived dimensions

| Dimension | Formula | Notes |
|---|---|---|
| `is_mixed_airline` | `concat_airline` spans >1 distinct airline (after remap) | applies to OW AND RT — a one-way itinerary can also be multi-airline |
| `is_mixed_cabin` | `COUNT(DISTINCT classname) > 1` across ALL segments (all sub-orders) | flags orders whose measures mix economy + premium (公务舱/超级经济舱/头等舱) — v2 |
| `is_segment_missing` | `so_raw` (raw seg_out) is NULL | no outbound segment row in segment table (coverage gap) — v2 |
| `is_non_economy` | `so_raw` present AND `so` (economy join) NULL | outbound cabin is 公务舱/超级经济舱/头等舱 — v2 |
| `cabin_raw` | `so_raw.classname` | raw outbound classname (economy orders = `经济舱`; else real non-economy value) — v2 |
| Trip type | `OW-single` / `OW-mixed` / `RT-pure` / `RT-mixed` | `primorderflightway` × `is_mixed_airline` |
| RT trip duration (BL-3) | `duration_rt` (minutes) ÷ 1440 = destination-stay days, from `flt_bidb_v_edw_factfltprimaryorder_eng` | NULL for OW; bucket later |
| VFR (BL-4) | `is_vfr_tag` (0/1/NULL) from `adm_vfr_tag_order_final`, dedup `MAX` per `primaryorderid_fill` | NULL = untagged (~29%, no VFR row) — keep visible, do NOT IFNULL(0), like `is_lowest_price` |
| Advance window | `orderdate_d − outbound_depart_date` (days) | bucket later |

## Locked decisions (2026-09-01)

1. **Any-leg airline analysis** = via `concat_airline` (full itinerary string); single-airline
   attribution = outbound marketing airline. A `mixed_airline` flag marks itineraries spanning
   >1 airline (OW or RT).
2. **Cross-type RT (LCC outbound × FSC return)** = attribute to **outbound leg's type** (no
   separate "mixed-type" category); return-leg type is not recorded.
3. **Cabin** = economy only (premium economy only when explicitly requested).
4. **Grain** = order-level (`primaryorderid_fill`), with pre-aggregated monthly/weekly views
   derived from it.
5. **Base table** = `edw_ord_flt_order` (the official reporting table → guarantees coverage of
   all officially-reported orders). Fact table joined only for RT-duration/time fields.
6. **Trip way** = `primorderflightway` (`S`/`D`/`M`); multi-city (M) in scope.
7. **Coverage visibility** = retain NULL/untagged tags (`is_lowest_price` NULL, VFR no-tag) as
   distinct states — do not silently coerce or drop — so coverage gaps are detectable.
8. **Economy coercion (v2, 2026-09-01)** = economy filter is a JOIN-side scope, NOT a hard WHERE
   drop. Non-economy (公务舱/超级经济舱/头等舱 ≈2.4% of orders) and missing-segment orders are
   kept and flagged (`is_non_economy` / `is_segment_missing`) instead of silently vanishing.
9. **Pax snapshot lag (v2, 2026-09-01)** = fact `persons` settles ~2 days after the order date
   (08-31 snapshot had 363 persons for 08-31 vs 229,262 in the 09-02 snapshot). `d_snapshot` MUST
   be ≥ `d_end` + 2 days. Weekly monitor runs **Tuesday** to stay ahead of this lag.

## RT duration & VFR source tables

- **`flt_bidb_v_edw_factfltprimaryorder_eng`** — primary-order fact table; `d` = snapshot date
  (keep latest snapshot only, ~5 days retained), `orderdate` = real order date. Has `flightway`
  (S=OW / D=RT / M=multi-city), time fields (`pri_takeofftime` / `dest_arrivaltime` /
  `back_takeofftime` / `max_arrivaltime`), `duration_rt` (minutes = destination stay),
  `persons` (total pax = adult+child+infant, authoritative), `advanceday` (⚠️ name says days
  but value is minutes). Join key `primaryorderid`.
  ⚠️ **`persons` lags ~2 days**: the snapshot for date X only settles X's orders ~2 days later.
  Set `d_snapshot ≥ d_end + 2d` in the build (v2 uses 09-02 for d_end 08-31).
- **`adm_vfr_tag_order_final`** — VFR tag; `d` = order date (daily, ~3 weeks retained). Dedup
  `MAX(is_vfr_tag)` per `primaryorderid_fill`; join `primaryorderid = primaryorderid_fill`
  (~71% coverage; the other ~29% = NULL → keep visible, do NOT IFNULL 0).

## TBD (slots — not built yet)

- **24-hour order tag** (void / 24h free-cancel affected orders) — leave a slot, do not add yet.
- **Fare price / price-gap** (segment `price` / `saleprice` / `currency`) — skipped for now; add later for value-step analysis.
