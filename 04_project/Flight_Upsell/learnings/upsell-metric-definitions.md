# Upsell Metric Definitions (canonical)

> Canonical source of truth for the global upsell monitor + deep-dive analysis.
> Every metric口径, filter, join key, and dimension value used in a report must
> trace back to a definition in this file. If a number cannot be derived from a
> definition here, it must be added here first (and reviewed) before it is used.

## 1. North-star metric

**Upsell rate** = share of eligible primary orders that chose a non-cheapest fare.

```
upsell_rate = SAFE_DIVIDE(
  COUNT(DISTINCT CASE WHEN is_lowest_price = 0 THEN primaryorderid_fill END),
  COUNT(DISTINCT CASE WHEN is_lowest_price IS NOT NULL THEN primaryorderid_fill END)
)
```

- `is_lowest_price = 0` → upsell (non-cheapest fare chosen)
- `is_lowest_price = 1` → cheapest (no upsell)
- `is_lowest_price IS NULL` → untagged — **excluded from both numerator and denominator**

Untagged orders (~9.5%) have no reliable cheapest-fare signal; including them in the
denominator would bias the rate downward.

## 2. Eligibility scope (base filters)

Every order-level analysis starts from this scope unless explicitly stated otherwise:

- `flightclass = 'I'` (international)
- Cabin: economy only by default — `b.classname = '经济舱'` (premium economy only when explicitly stated)
- `subprdtype_pos_primorder NOT IN ('FCN')` (exclude FCN)
- `iscrawler = 0`
- All timestamps in Shanghai time (UTC+8)

## 3. Canonical join keys

| Join | Key | Note |
|------|-----|------|
| order ↔ is_lowest_price | `a.primaryorderid_fill = lp.primary_orderid` (CAST BIGINT) | ~90.5% coverage. `orderid` on primary rows (`is_primaryorder=1`) is equivalent. ⚠️ Never join raw `primaryorderid` (NULL on ~76% of primary rows → ~22%) |
| order ↔ segment | `a.orderid = b.orderid` + `b.sequence = 1` | outbound segment; latest snapshot `DATE(b.d) = DATE_SUB(CURRENT_DATE(), 1)` |
| UBT ↔ FE trace | `(d, vid, sid, pvid)` | NOT `uid` |
| order ↔ LCC/FSC | `a.airline = dim.airline` | `dim.isbudget = 1` = LCC |

## 4. Dimension enum values

| Dimension | Field | Values |
|-----------|-------|--------|
| Trip way | `primorderflightway` | `'S'` = OW (single-way), `'D'` = RT (round-trip) |
| LCC/FSC | `dim_prd_flt_airline.isbudget` | `1` = LCC, else FSC |
| Cabin | segment `classname` | 经济舱 = Y, 超级经济舱 = S, 公务舱 = C, 头等舱 = F |
| Channel | order `channeltype` | app / online / h5 |
| Upsell flag | `is_lowest_price` | `0` = upsell, `1` = cheapest, `NULL` = untagged |

## 5. Baggage attach rates (canonical, v3 2026-09-02)

Two default checked-bag attachment rates, pre-computed on the order master. Both are
order-level 0/1 flags; `baggage_combo` (no_bag / carryon_only / checkbag_only / bag+carryon)
remains the categorical grouping.

| Metric | Definition | Meaning |
|---|---|---|
| `checkbag_mid_attach` | `is_free_checkinbag = 'Y' OR checkbag_bundle = 1` | fare-embedded + middle-page bundle — "does the middle page capture the checked-bag need?" |
| `checkbag_final_attach` | `checkbag_mid_attach OR checkbag_xpage = 1 OR checkbag_postbooking_predep = 1 OR checkbag_postbooking_departed = 1` | all sources incl. fill-in + post-booking pre/post departure (final attach) |

Field semantics (v3):
- `is_free_checkinbag` / `is_free_carryonbag` = order-table EN flags `is_free_checkinbagen` /
  `is_free_carryonbagen` ('Y'/'N'). The segment table stores Chinese 是/否/以航司客规为准.
- `checkbag_bundle` / `checkbag_xpage` = x-product `productname='行李额'`, `booktype=1`,
  `businesstype_detail` 4 (= bundle) vs ≠4 (= fill-in/other).
- `checkbag_postbooking_predep` / `_departed` = `productname='行李额'`, `booktype=2`, split by
  `orderdate < takeofftime` (predep) vs `>=` (departed).

## 6. Cleanup rules (middle-page / UBT denominator only)

Apply in order before computing any UBT or FE-trace denominator:

1. **Rule 1** — UBT middle page, `ua_channeltype = 'app'` + `duration > 2 OR NULL`
2. **Rule 2** — latest exposure per `(d, vid, sid, pvid, index)` by `starttime DESC`
3. **Rule 3** — exclude gappy pvs (`COUNT(DISTINCT index) = MAX(index) + 1`)

Channel note: `ua_channeltype` (device on this visit) is the UBT channel field — distinct from
the order table's `channeltype` (app / online / h5). FE trace is app-only, so the UBT
denominator is scoped to app (`ua_channeltype = 'app'`) to match. The order-level north-star
metric has no UBT step and uses order `channeltype` as a dimension instead.

## 7. Known coverage caveats

- `is_lowest_price` untagged ≈ 9.5% of primary orders (excluded from rate).
- **`is_lowest_price` untagged is channel-skewed (Meta × h5)** — Meta-referred h5 (mobile-web)
  orders are untagged at ~64% (vs ~13% for 1-Meta h5, ~2–5% for app/online). These orders have
  a row in the is_lowest table (subchnl < 7900000) but `is_lowest_price IS NULL` — the Meta→h5
  flow appears to bypass the middle-page fare comparison that produces the tag. ~8% of all orders
  are affected; split Meta × channel when analyzing Meta. See `sql/meta_tag_rate_diagnosis.sql`.
- Brand name for brand-fare analysis: default to the **brand fare mapping CTE**
  (`tb_brandname_unified` → normalized `brand_name` + `airline_brandtier`, keyed on carrier +
  cabin + `atpco_brand_name`). For airlines/brands not mapped there, fall back to the two raw
  fields `atpco_brand_name` (ATPCO-standardized, preferred) and `ori_brand_name` (original/raw) —
  compare both, use the cleaner (non-NULL). **When aggregating, combine both sources** (mapped
  `brand_name` + raw atpco/ori for the unmapped tail). `atpco_brand_name` is only populated from
  ~2025-08, so earlier orders rely on `ori_brand_name`.
- FE trace inflates pvid counts ~55% — never use as a raw denominator.
- UBT `duration` = seconds (pageview); event `context.duration` = milliseconds.
- Segment table `d` = data refresh time, not retention window; historical orders are queryable
  via the latest snapshot.

## 8. Cross-validation anchors

- Reconcile analysis totals vs official reporting SQL by comparing **ratios/distributions**,
  not absolutes (the two use intentionally different scopes/filters).
- Expected: analysis tagged orders ≈ 90.5% of official (9.5% untagged).
- Official uses `orderbrand IN ('trip')`; analysis uses `is_trip='T' AND is_rebook_new_order=0
  AND subchnl < 7900000`.

## 9. Locked decisions (2026-09-01)

1. **Cabin default = economy only** (`b.classname = '经济舱'`). Premium economy included only
   when explicitly stated. (Note: `ref_master_order_quantification.sql` v4 currently uses
   economy + premium economy — reconcile to economy-only when the master table is rebuilt.)
2. **Master table grain = pre-aggregated.** New dimensions (RT trip duration, VFR) must be
   pre-designed into the aggregate at build time, or shipped as documented side-tables keyed
   by `primaryorderid_fill` — never inline in ad-hoc analysis.
