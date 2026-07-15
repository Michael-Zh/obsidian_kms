# Void / 24h Free Cancel Display Override — Analysis Brief
_Last updated: 2026-06-16_

---

## Problem Statement

A significant portion of EY (and likely AA, UA, DL) tickets display a "24-hour free cancellation" or "void" label on the middle selection page. This label **overrides the ticket's true refund policy**, meaning:

- A ticket that is genuinely `non-refundable` (Change Only or Not Flexible) shows "free cancellation within 24 hours"
- The user has no visibility into what happens **after** the 24-hour window
- The user might be misled by the 24h policy and and bought a non-refundable fare
- This eliminates the primary upgrade motivation (refundability) for users who would otherwise consider a higher-tier branded fare

**Two business impacts:**
1. **Customer trust risk:** Users believe they can cancel freely, but the ticket is non-refundable — leading to complaints and disputes
2. **Upsell opportunity loss:** Users have no signal to upgrade to Flexible fares because all tiers show the same label

---

## Key Questions Being Investigated

1. How many tickets have void / 24h free cancel policy? ✅ Answered
2. Under what conditions does the system display this override? ❌ Not yet answered (requires FBU product logic)
3. Of affected orders, how many users were misled about their actual refund policy? ✅ Answered for EY
4. What is the upsell rate impact? ⚠️ Partially answered — causal link needs cleaner method

---

## Data Source

**Primary table:** `trip-ibu-adhoc.ibu_adhoc_temp.MZ_202606_quantification_v4`

This is a pre-aggregated table built from the following source tables (Oliver Tang's SQL):

| Source Table | Content |
|---|---|
| `flt_predb.v_fltorderdb_o_orders` | Master order table |
| `flt_predb.v_fltorderdb_fltintlorderpolicy` | Order-level policy (ownerairline, agency) |
| `flt_predb.v_fltorderdb_o_orderdetail` | Order detail (source, subchannel) |
| `flt_predb.v_fltorderdb_o_flightextdetail` | Flight ext detail — contains `policytokenno` (bridge to penalty tables) |
| `ods_fltairtickets_mysql_fltintlpenaltydb.o_customer_cancellation` | Free cancellation policy (service_fee_type) |
| `ods_fltairtickets_mysql_fltintlpenaltydb.o_other_detail` | Void / 24h policy — contains `ticketOperationType` |
| `ods_fltairtickets_mysql_fltbasedatadb.BD_ChannelConfigInfo` | Channel config (market, channel, subchannel mapping) |

**`ticketOperationType` values (from Oliver Tang):**
- `1` = VOID
- `2` = 24-hour free cancellation
- `3` = 48-hour free cancellation
- `4` = 2-hour free refund (China domestic airlines)
- `null` = Does not support any of the above

**Key metrics in the aggregated table:**

| Column | Formula | Meaning |
|---|---|---|
| `primary_ord_count` | count distinct primaryorderid_fill | Total orders |
| `upsell_base_primary_ord_count` | orders with `is_lowest_price IS NOT NULL` | Orders with upsell signal |
| `upsell_primary_ord_count` | orders with `is_lowest_price = 0` | Orders that upsold |
| `free_cancel_24h_ord_count` | `ticketoperationtype = '2'` AND `service_fee_type IN (1024, 16)` | 24h free cancel orders (requires both conditions) |
| `void_ord_count` | `ticketoperationtype = '1'` AND `service_fee_type IN (1024, 16)` | Void orders (requires both conditions) |
| `overwritten_ord_count` | (`ticketoperationtype = '2'`) OR (`= '1'` AND `market IN ('US','BR','KR')`), AND `service_fee_type IN (1024, 16)` | Orders where display is overwritten — 24h globally + void in US/BR/KR markets |
| `cancel_policy_class` | from `e_customer_cancellation`: `is_allowed` + `all_un_use_show_up_amount` | Benefit fingerprint: `3.free_cancel` / `2.paid_cancel` / `1.no_cancel` / NULL (no token) |
| `change_policy_class` | from `c_customer_change`: outbound `is_allowed` + `out_all_un_use_show_up_strict_amount` | Benefit fingerprint: `3.free_change` / `2.paid_change` / `1.no_change` / NULL (no token) |
| `baggage_final` | resolved from `has_checkin_baggage` + `has_carryon_baggage` | Final baggage: `1.fare_only_final` / `2.fare_carry_on_only_final` / `3.fare_check_in_only_final` / `4.fare_both_bag_final` |
| `rp_bundle_ord_count` | `rp_bundle = 1` | Orders with RP (Cancellation Guarantee) bundle from middle page |
| `all_flexibility_bundle_ord_count` | `all_flexibility_bundle = 1` | Orders with full flexibility bundle (change + cancel) from middle page |

> **v4 note:** `free_cancel_or_void_ord_count` has been removed. Use `void_ord_count + free_cancel_24h_ord_count` for the combined count, or `overwritten_ord_count` for the display-adjusted override count (which carves out void orders where the US/BR/KR DOT rule legitimately triggers the display). Both require `service_fee_type IN (1024, 16)` as a co-condition — tickets without this flag are excluded even if `ticketoperationtype` is set.

**Upsell rate formula:** `upsell_primary_ord_count / upsell_base_primary_ord_count`

**Policy share formula:** `(void_ord_count + free_cancel_24h_ord_count) / primary_ord_count`

---

## EY Findings (2026 Jan–May, All Locales)

### Overall scale

| Metric | Value |
|---|---|
| Total orders (all locales) | 110,782 |
| Policy share (has void/24h) | 88% |
| Overall upsell rate | 79% |
| Top 20 locales coverage | 93% of total |

### Policy group vs upsell rate

| Group | Orders | Upsell base | Upsell rate |
|---|---|---|---|
| all_have_policy | 150,746 | 143,993 | 81.4% |
| mixed | 15,921 | 15,482 | 78.2% |
| no_policy | 13,937 | 12,802 | 56.1% |

> ⚠️ The `no_policy` group's lower upsell rate (56.1%) is **not** evidence that void/24h improves upsell. It reflects selection bias — tickets without any void/24h policy are structurally different products (codeshare, incomplete GDS connection, incomplete brand fare ladder). This is an apples-to-oranges comparison.

### Core finding: potential misleading display at scale

Among orders with potential misleading void/24h policy displayed:

| Actual refund policy | Orders | % of total |
|---|---|---|
| 2. Change Only (can change, cannot refund) | 122,102 | 73.3% |
| 1. Not Flexible (cannot change or refund) | 22,343 | 13.4% |
| **Subtotal: misled users** | **144,445** | **86.7%** |
| 4. Flexible (truly refundable) | 22,168 | 13.3% |

**Up to 86.7% of users bought a ticket that is non-refundable after the 24-hour window may see "free cancellation within 24h" displayed.**

Only 13.3% of orders had a label consistent with their actual ticket policy.

---

## Full-Airline Risk Exposure Ranking (2026 Jan–May, all airlines ≥500 orders)

> Ranked by `misled_exposed` = orders where `free_cancel_or_void_ord_count > 0` AND `flexible IN ('2.Change Only','1.Not Flexible')`

\* **Upper limit of Misled Exposed**: orders include void/24h AND either Change Only or Not Flexible
\* **Non-refundable % of Void/24h Orders**: among orders include void/24h, share of orders either Change Only or Not Flexible

| Rank | Airline            | Type | Total Orders | Orders incl. Void/24h | Void/24h % | **Non-refundable among Void/24h Orders** | Non-refundable % of Void/24h Orders* | Upsell Rate |
| ---- | ------------------ | ---- | ------------ | --------------------- | ---------- | ---------------------------------------- | ------------------------------------ | ----------- |
| 1    | EY Etihad          | FSC  | 180,604      | 161,597               | 89.5%      | **139,651**                              | 86.4%                                | 79.2%       |
| 2    | TG Thai Airways    | FSC  | 354,911      | 283,838               | 80.0%      | **138,176**                              | 48.7%                                | 26.3%       |
| 3    | MU China Eastern   | FSC  | 456,195      | 296,344               | 65.0%      | **103,247**                              | 34.8%                                | 22.8%       |
| 4    | TK Turkish         | FSC  | 217,804      | 164,757               | 75.6%      | **92,981**                               | 56.4%                                | 39.2%       |
| 5    | CA Air China       | FSC  | 239,663      | 147,405               | 61.5%      | **74,409**                               | 50.5%                                | 23.9%       |
| 6    | PR Philippine      | FSC  | 354,443      | 239,286               | 67.5%      | **74,331**                               | 31.1%                                | 22.9%       |
| 7    | WS WestJet         | LCC  | 73,124       | 71,480                | 97.8%      | **68,861**                               | 96.3%                                | 36.6%       |
| 8    | MH Malaysia        | FSC  | 348,412      | 207,789               | 59.6%      | **50,614**                               | 24.4%                                | 41.3%       |
| 9    | UA United          | FSC  | 58,589       | 51,525                | 87.9%      | **46,511**                               | 90.3%                                | 38.1%       |
| 10   | BA British Airways | FSC  | 58,668       | 49,389                | 84.2%      | **45,609**                               | 92.3%                                | 43.1%       |
| 11   | UX Air Europa      | FSC  | 71,528       | 47,586                | 66.5%      | **45,251**                               | 95.1%                                | 24.3%       |
| 12   | SQ Singapore       | FSC  | 193,511      | 104,152               | 53.8%      | **43,394**                               | 41.7%                                | 31.3%       |
| 13   | AC Air Canada      | FSC  | 53,241       | 49,622                | 93.2%      | **42,955**                               | 86.6%                                | 44.8%       |
| 14   | TO Transavia       | LCC  | 122,071      | 85,985                | 70.4%      | **39,844**                               | 46.3%                                | 26.2%       |
| 15   | LH Lufthansa       | FSC  | 44,093       | 41,170                | 93.4%      | **38,178**                               | 92.7%                                | 38.9%       |
| 16   | IB Iberia          | FSC  | 50,024       | 40,424                | 80.8%      | **35,534**                               | 87.9%                                | 31.2%       |
| 17   | DL Delta           | FSC  | 42,679       | 35,552                | 83.3%      | **32,970**                               | 92.7%                                | 32.2%       |
| 18   | AZ ITA Airways     | FSC  | 41,393       | 34,900                | 84.3%      | **32,692**                               | 93.7%                                | 38.5%       |
| 19   | NH ANA             | FSC  | 79,653       | 45,647                | 57.3%      | **31,894**                               | 69.9%                                | 22.9%       |
| 20   | SK SAS             | FSC  | 47,834       | 32,623                | 68.2%      | **30,283**                               | 92.8%                                | 53.7%       |

**Total upper limit of misled_exposed across top 40 airlines: >1,700,000 orders (estimated)**

### Priority Tiers

**P0 — Fix first (high absolute volume + high misled% + healthy upsell rate):**
- EY: 139K misled, 86.4%, upsell 79% — **highest repair ROI.** Repair ROI = misled volume × probability of upselling after fix × fare delta. EY leads on the first two: largest misled pool (139K) AND highest upsell rate (79%), meaning EY's users are already the most willing to pay for Flexible tickets — so restoring the refund signal has the highest expected conversion lift. Counter-intuitive point: the high upsell rate does NOT mean there's no room left — it was achieved *despite* the label being wrong (users were upgrading for baggage and other reasons). Fixing the label adds a refundability signal on top, so the rate should only go higher.
- WS: 69K misled, **96.3%**, upsell 37% — near-total override
- UA: 47K misled, 90.3%, upsell 38%
- BA: 46K misled, **92.3%**, upsell 43%
- AC: 43K misled, 86.6%, upsell 45%

**P1 — Second wave (large volume but lower misled% or lower upsell rate):**
- TG: 138K misled but only 48.7% misled rate — many legitimate void/24h; needs separate treatment
- TK: 93K misled, 56.4%
- LH: 38K misled, **92.7%**, upsell 39%
- SK: 30K misled, **92.8%**, upsell **54%** — highest upsell rate in tier

**Structural anomalies:**
- KE (Korean Air): void/24h 83.7% coverage but misled rate only **12.9%** — mostly genuine Flexible tickets; low actual risk
- TG: large absolute misled volume but structurally different (many real Flexible tickets mixed in)

---

## EY: Upsell Rate Variance by Airport Pair × Region

**Hypothesis:** If void/24h display override varies by region/channel, then the same route should show meaningfully different upsell rates across markets — with the higher-upsell region being the one where the override does NOT fire (so users can see the real refund policy and upgrade accordingly).

### Method
Filtered for airport_pairs with ≥2 regions, each ≥50 orders, and upsell rate spread ≥15pp between regions.

### Key Findings — Routes with Largest Upsell Rate Spread

| Airport Pair | Region | Orders | Void/24h% | Upsell Rate | Spread |
|---|---|---|---|---|---|
| KUL→RUH | id | 121 | 37.2% | 40.0% | **44.9pp** |
| KUL→RUH | sa | 94 | 76.6% | 84.9% | |
| KUL→RUH | my | 88 | 81.8% | 77.6% | |
| CMB→AUH | ae | 132 | 84.1% | 88.0% | **37.0pp** |
| CMB→AUH | hk | 68 | 98.5% | **100.0%** | |
| CMB→AUH | ru | 59 | 83.1% | 63.0% | |
| JED→BKK | sa | 197 | 83.2% | 60.6% | **35.0pp** |
| JED→BKK | th | 94 | 91.5% | **95.6%** | |
| IST→BKK | th | 210 | 92.9% | **95.7%** | **34.3pp** |
| IST→BKK | tr | 177 | 93.8% | 61.4% | |
| ICN→LHR | kr | 201 | 93.5% | 63.6% | **31.1pp** |
| ICN→LHR | gb | 81 | 95.1% | **94.7%** | |
| BCN→BKK | es | 248 | 99.2% | 56.4% | **30.0pp** |
| BCN→BKK | fr | 59 | 93.2% | **86.4%** | |
| JED→CGK | id | 3,703 | 95.6% | **96.3%** | **28.9pp** |
| JED→CGK | sa | 272 | 91.2% | 69.2% | |
| CDG→BKK | fr | 800 | 98.8% | 74.4% | **23.5pp** |
| CDG→BKK | th | 50 | 98.0% | **97.9%** | |

### Analytical Observation

⚠️ **The hypothesis is NOT straightforwardly confirmed by this data.**

The pattern that emerges is more nuanced:
- On most routes, void/24h coverage is uniformly high across regions (both the high-upsell and low-upsell regions have 80–99% void/24h exposure)
- This means the upsell rate spread is **not explained by differential void/24h coverage** — both regions see the same label
- The spread more likely reflects **structural demand differences** by market: e.g. Indonesian buyers on JED→CGK (96.3% upsell) vs Saudi buyers on the same route (69.2%) — likely because Indonesian buyers are migrant workers with strong bag+refund preferences, whereas Saudi buyers may have different purchasing patterns

**The one exception worth noting:** KUL→RUH / `id` region has void/24h coverage of only 37.2% (vs 77–82% for `sa`/`my` regions) and correspondingly lower upsell rate (40% vs 78–85%). This is the closest pattern to the original hypothesis — lower display coverage correlating with lower upsell — but this is a single data point.

**Implication for the void/24h fix thesis:** The upsell suppression effect of void/24h display may be real but hard to isolate from region-level demand differences using this data alone. The causal claim needs a cleaner method (e.g. before/after comparison if display logic changes, or a controlled experiment).

### Open Question: What Drives the Display Override?

Three hypotheses remain open — none can be ruled out with current data. **Parked — to be confirmed with Product Owner / FBU.**

1. **Booking channel** — different GDS/direct connections may pass void/24h policy data differently, causing the display logic to fire inconsistently across channels (e.g. TF-WS showed near-100% override rate vs 1A-WS at ~60–77% for UA)
2. **Agency** — certain agencies may have specific contractual or technical configurations that trigger or suppress the display override; `source + subchannel` in `edw_ord_flt_order` is a candidate dimension but could not be cross-referenced with void/24h data in the current aggregated table
3. **Locale / region** — local regulatory requirements may mandate displaying void/24h cancellation rights regardless of the underlying ticket policy (e.g. EU consumer protection rules, US DOT 24h cancellation rule); this would explain why some markets systematically show the label

Until the display trigger logic is obtained from FBU, the **246K** (EY+AA+UA+DL) and **>1.7M** (all airlines) figures remain **upper-bound estimates** of risk exposure, not confirmed counts of misled users.

---

## Airlines Flagged for Further Investigation

- **EY** — fully analyzed; see sections above
- **AA, UA, DL** — analyzed; findings consistent with EY (83–93% misled rate)
- **WS, BA, AC, LH, SK** — P0/P1 priority; same query pattern applicable
- **Priority next:** Run flexible breakdown (Q1) for WS, BA, LH to confirm misled structure

---

## SQL Queries

### Q1: Flexible breakdown for orders with void/24h policy (run for any airline)
```sql
SELECT
  flexible,
  SUM(primary_ord_count) AS orders,
  ROUND(SUM(primary_ord_count)*100.0 / SUM(SUM(primary_ord_count)) OVER(), 1) AS pct_of_total
FROM `trip-ibu-adhoc.ibu_adhoc_temp.MZ_202606_quantification_v4`
WHERE order_year = 2026
  AND order_month BETWEEN 1 AND 5
  AND marketing_airline = 'EY'   -- swap airline here
  AND (void_ord_count + free_cancel_24h_ord_count) > 0
GROUP BY 1
ORDER BY 2 DESC
```

### Q2: Policy group vs upsell rate (by airline)
```sql
SELECT
  CASE 
    WHEN (void_ord_count + free_cancel_24h_ord_count) > 0 
      AND (void_ord_count + free_cancel_24h_ord_count) = primary_ord_count 
    THEN 'all_have_policy'
    WHEN (void_ord_count + free_cancel_24h_ord_count) = 0 
    THEN 'no_policy'
    ELSE 'mixed'
  END AS policy_group,
  SUM(primary_ord_count) AS total_orders,
  SUM(upsell_base_primary_ord_count) AS upsell_base,
  SUM(upsell_primary_ord_count) AS upsell_orders,
  ROUND(SUM(upsell_primary_ord_count) * 100.0 
    / NULLIF(SUM(upsell_base_primary_ord_count), 0), 1) AS upsell_rate_pct
FROM `trip-ibu-adhoc.ibu_adhoc_temp.MZ_202606_quantification_v4`
WHERE order_year = 2026
  AND order_month BETWEEN 1 AND 5
  AND marketing_airline = 'EY'   -- swap airline here
GROUP BY 1
ORDER BY 1
```

### Q3: Airline-level overview (void/24h coverage + upsell rate)
```sql
SELECT
  marketing_airline, marketing_airline_name, LCCorFSc,
  SUM(primary_ord_count) AS total_orders,
  SUM(void_ord_count + free_cancel_24h_ord_count) AS void_or_24h_orders,
  ROUND(SUM(void_ord_count + free_cancel_24h_ord_count)*100.0 / NULLIF(SUM(primary_ord_count),0), 1) AS void_24h_pct,
  SUM(upsell_base_primary_ord_count) AS upsell_base,
  ROUND(SUM(upsell_primary_ord_count)*100.0 / NULLIF(SUM(upsell_base_primary_ord_count),0), 1) AS upsell_rate_pct
FROM `trip-ibu-adhoc.ibu_adhoc_temp.MZ_202606_quantification_v4`
WHERE order_year = 2026
  AND order_month BETWEEN 1 AND 5
GROUP BY 1,2,3
HAVING SUM(primary_ord_count) > 500
ORDER BY void_24h_pct DESC
LIMIT 30
```

### Q4: Order share by baggage × flexibility (FSC, 1-Meta, 40 audit airlines, 2026 Jan–May)

This is the main table used in the session — matches the screenshot shared 2026-06-22. Filters applied:
- FSC only, Economy cabin (Y), 1-Meta, isBatch1 = 'Y', order_year = 2026
- baggage_incl_bundle_group IN ('2.fare+carry on', '4.Fare+carry on+checkin')
- flexible IN ('1.Not Flexible', '2.Change Only', '4.Flexible')

```sql
SELECT 
  marketing_airline,
  baggage_incl_bundle_group,
  flexible,
  SUM(primary_ord_count) as ord_count
FROM `trip-ibu-adhoc.ibu_adhoc_temp.MZ_202606_quantification_v4`
WHERE marketing_airline IN ('UA','AA','EY','AC')   -- swap or remove for all airlines
  AND LCCorFSc = 'FSC'
  AND isMeta = '1-Meta'
  AND isBatch1 = 'Y'
  AND cabin_IATAcode = 'Y'
  AND order_year = 2026
  AND flexible IN ('1.Not Flexible','2.Change Only','4.Flexible')
  AND baggage_incl_bundle_group IN ('2.fare+carry on','4.Fare+carry on+checkin')
GROUP BY 1,2,3
ORDER BY marketing_airline, baggage_incl_bundle_group, flexible
```

**Verified totals (2026 Jan–May, same filters):**

| Airline | Total Orders | Void % | 24hr % | Void Orders | 24hr Orders |
|---------|-------------|--------|--------|-------------|-------------|
| EY | 109,541 | 27% | 62% | 29,047 | 67,774 |
| UA | 50,780 | 29% | 59% | 14,684 | 29,806 |
| AC | 30,477 | 36% | 58% | 10,848 | 17,758 |
| AA | 28,938 | 75% | 17% | 21,668 | 4,821 |

Note: Void% and 24hr% here use the bag-filtered denominator. Screenshot uses unfiltered total as denominator — small numerical difference, directionally identical.

---

### Q5: Void/24hr share per airline (Jay's query) — `JN_202606_void_24`

Source: `trip-ibu-adhoc.ibu_adhoc_temp.JN_202606_void_24`

Built from `edw_ord_flt_order` joined to `o_flightextdetail` → `o_other_detail` for `ticketoperationtype`, and `o_customer_cancellation` for `service_fee_type`. Covers Jan 2026 onwards. Includes channel/market dimension via `BD_ChannelConfigInfo`.

Key field: `ticketoperationtype_meaning` — values: void / 24 hour free cancel / 48 hour free cancel / 2 hour free cancel / standard (no free cancel policy)

Use this table for market-split analysis (purchase market via `x.market` field) — critical for UA/AA void vs. 24hr separation by US/BR/KR vs. rest of world.

```sql
-- Market split for UA and AA: void vs 24hr share by purchase market
SELECT
  ownerairline,
  market,
  ticketoperationtype_meaning,
  SUM(ord_count) as orders
FROM `trip-ibu-adhoc.ibu_adhoc_temp.JN_202606_void_24`
WHERE ownerairline IN ('UA','AA')
GROUP BY 1,2,3
ORDER BY ownerairline, market, orders DESC
```

---

## BQ Access Notes

- **Project:** `trip-ibu-adhoc`
- **Dataset:** `ibu_adhoc_temp`
- **Table:** `MZ_202606_quantification_v4`
- **Account:** `michael.zhang@trip.com`
- **Active gcloud config:** `company` (located at `~/.config/gcloud/configurations/config_company`)
- **Known issue:** Claude Code sandbox blocks HTTPS CONNECT tunnels through corporate proxy (`localhost:58601`) to `googleapis.com` — BQ queries must be run from a regular terminal or a new Claude Code session without sandbox network restrictions

---

## Pending Next Steps

- [ ] Run Q1 (flexible breakdown) for AA, UA, DL — replicate EY finding
- [ ] Run Q3 (airline overview) to identify other high-impact airlines beyond the 4 flagged
- [ ] Quantify revenue leakage: identify average fare delta between Non-Flexible and Flexible for EY, multiply by estimated conversion lift
- [ ] Get display logic from FBU: under what conditions does the void/24h label trigger? (This is the fix scope question)
- [ ] Draft leadership narrative: frame as customer trust issue + upsell opportunity, not just upsell metric

---

## Fare Family Design Analysis: Why Suppression Depth Varies by Airline

_Added 2026-06-23 — based on fare family screenshots and BQ data cross-analysis for EY, UA, AC_

### Why Fare Family Design Matters

The global 4% FSC figure establishes scale — but does not tell you which airlines to fix first or how large the per-airline opportunity is. The missing variable is **suppression depth**: how many non-refundable tiers sit below the first genuine refund right, and what is the price gradient across those steps.

Three factors determine suppression depth per airline:

1. **Number of non-refundable tiers before first refundability** — more tiers = larger addressable upgrade pool
2. **What drives each upgrade step** — if the step is purely a refundability signal, 24hr eliminates it entirely; if the step also bundles bags or seat upgrades, 24hr only partially suppresses it
3. **Route type split** — domestic vs. international fare structures often differ within the same airline; the correct suppression count depends on which segment dominates volume

### Framework: Upgrade Step Anatomy

Each upgrade step can be classified by its benefit composition:

| Step type | Bag delta | Seat delta | Refund delta | 24hr suppression effect |
|---|---|---|---|---|
| Pure refundability | None | None | Yes | **Full** — 24hr eliminates the entire motivation |
| Refund + bag | Added | None | Yes | **Partial** — bag incentive remains; refund signal suppressed |
| Refund + seat | None | Added | Yes | **Partial** — seat incentive remains; refund signal suppressed |
| Bag only | Added | None | None | **None** — refundability not a factor at this step |

The highest-ROI targets are airlines where the step immediately above the most-purchased tier is a **pure refundability** step. 24hr display fully eliminates the upgrade motivation at that step.

---

### EY (Etihad Airways)

#### Fare Family Structure (all international — no domestic on Trip.com)

| Tier | Checked bag | Change | Refund | Seat selection | Miles | Step type above |
|---|---|---|---|---|---|---|
| Basic | None | ✗ | ✗ | Fee | 15% | Bag + refund (partial suppression) |
| Value | 25kg | Fee | ✗ | Fee | 35% | **Pure refundability** |
| Comfort | 30kg | Fee | Fee applies | Free standard | 75% | Bag + full refund |
| Deluxe | 40kg | Free | Free | Free preferred | 125% | — |

> **Note:** Current fares carry a temporary first-change-free overlay across all tiers (Middle East disruption waiver). Refundability rights are unaffected. Table reflects permanent underlying structure.

#### Upgrade Drivers

| Step | Bag delta | Seat delta | Refund delta | Step type |
|---|---|---|---|---|
| Basic → Value | +25kg | None | None | Bag only |
| Value → Comfort | +5kg | Free standard seat | Fee applies | **Partial — but refund is the primary new signal** |
| Comfort → Deluxe | +10kg | Free preferred seat | Free (upgrade from fee) | Bag + seat + full refund |

The critical step is **Value → Comfort**: the bag increment (+5kg) is marginal relative to the price jump; the dominant new value is the introduction of refundability. 24hr eliminates this signal for Value-tier buyers.

#### Price Gradient

| Route example | Basic | Value premium | Comfort premium | Deluxe premium |
|---|---|---|---|---|
| Long-haul (JED-CGK) | SAR 1,438 | +SAR 76 (+5.3%) | +SAR 193 (+13.4%) | +SAR 647 (+45.0%) |
| Short-haul (AUH-BOM) | AED 635 | +AED 60 (+9.4%) | +AED 190 (+29.9%) | +AED 690 (+108.7%) |

The Comfort premium is accessible — especially on long-haul (+13.4%). Customers who genuinely want refundability are not being priced out; they are being given false assurance by the 24hr label.

#### BQ Mapping

| EY tier | BQ `flexible` | Non-refundable? |
|---|---|---|
| Basic | 2. Change Only | Yes |
| Value | 2. Change Only | Yes |
| Comfort | 4. Flexible | No |
| Deluxe | 4. Flexible | No — indistinguishable from Comfort |

#### Volume & Suppression Summary

| Metric | Value |
|---|---|
| Total orders (Jan–May 2026) | 109,541 |
| Non-refundable share (Basic + Value) | 86.7% |
| Orders with 24hr flag | 88% |
| Upsell rate | 79% |
| Suppressed tiers | 2 (Basic, Value) |
| First refundability at | Comfort (tier 3 of 4) |
| Pure refundability step | Value → Comfort |

**Why EY is the lead case:** Simplest structure, largest misled volume (139K upper bound), highest upsell rate (79%) — users are already the most willing to pay. Fixing the label adds a refundability signal on top of an already-high conversion base. Counter-intuitive point: the high upsell rate does not mean there is no room — users were upgrading for baggage. Restoring the refund signal adds a second motivation.

---

### UA (United Airlines)

#### Fare Family Structure

UA operates a 4-cabin × 3-sub-tier matrix. Our analysis covers economy cabin only (`cabin_IATAcode = 'Y'`).

**4 cabin tiers:**
- United Economy — main cabin economy
- Economy Plus — extra legroom, **still economy cabin** (not a separate cabin class)
- United Premium Plus — true premium economy
- United Polaris — business class (no international first class)

**3 sub-tiers within each tier:**

| Sub-tier | Change | Refund |
|---|---|---|
| Basic | ✗ | ✗ |
| Standard | Free | ✗ |
| Flexible | Free | Free |

> **Data note:** `cabin_IATAcode = 'Y'` captures all economy-cabin orders including Economy Plus. Economy Plus buyers are indistinguishable from flat economy buyers in BQ — upsell rates are conflated across these two groups.

#### Upgrade Drivers by Route Type

**Domestic (EWR-LAX example):**

| Step | Bag delta | Seat delta | Refund delta | Step type |
|---|---|---|---|---|
| Basic → Standard | Carry-on added | None | None | Bag + changeability |
| Standard → Flexible | None | None | Full refund | **Pure refundability** |

**International (HKG-BKK, LAX-HKG examples):**

| Step | Bag delta | Seat delta | Refund delta | Step type |
|---|---|---|---|---|
| Basic → Standard | +1 checked bag | None | None | Bag + changeability |
| Standard → Flexible | None | None | Full refund | **Pure refundability** |

In both route types, baggage incentive is fully exhausted at the Basic→Standard step. Standard→Flexible is a pure refundability signal with nothing else bundled — 24hr fully suppresses it.

#### Price Gradient (Domestic EWR-LAX)

| Sub-tier | Price | Premium |
|---|---|---|
| Basic | $249 | — |
| Standard | $304 | +$55 (+22.1%) |
| Flexible | $354 | +$50 (+16.4% over Standard) |

The Flexible premium over Standard ($50) is modest — customers are not being priced out of refundability.

#### BQ Mapping

| UA sub-tier | BQ `flexible` | Non-refundable? |
|---|---|---|
| Basic | 1. Not Flexible | Yes |
| Standard | 2. Change Only | Yes |
| Flexible | 4. Flexible | No |

#### Volume Split

| Segment | Orders | Share | Display policy | Suppression type |
|---|---|---|---|---|
| International | ~41,700 | 75% | 24hr (global) | Pure refundability — unconfounded |
| Domestic | ~13,800 | 25% | Void (US purchase market) | Pure refundability — one step has confounder (carry-on) |

#### Volume & Suppression Summary

| Metric | Value |
|---|---|
| Total orders (Jan–May 2026) | 50,780 |
| Non-refundable share | 90.3% |
| Upsell rate | 38.1% |
| Suppressed tiers | 1 (Standard) |
| First refundability at | Flexible sub-tier |
| Pure refundability step | Standard → Flexible |

**Why UA is a validation case, not the lead:** More complex fare architecture, Economy Plus conflation in BQ, domestic/international split requires two arguments, and only one suppression point vs. two for EY. The mechanism is the same; the narrative is harder.

---

### AC (Air Canada)

#### Fare Family Structure

5 economy tiers with a **critical structural difference between international and domestic/US routes**.

**International routes:**

| Tier | Change | Refund | Same-day change | Step type above |
|---|---|---|---|---|
| Basic | ✗ | ✗ | ✗ | Change only |
| Standard | Fee | ✗ | CA$100–120 | **Pure refundability** |
| Flex | Fee | **Fee applies** | CA$100–120 | Seat + refund upgrade |
| Comfort | Fare diff | Refundable | Included | Incremental |
| Latitude | Fare diff | Refundable | Included | — |

**Domestic (within Canada) and To/From US routes:**

| Tier | Change | Refund | Same-day change | Step type above |
|---|---|---|---|---|
| Basic | ✗ | ✗ | ✗ | Change only |
| Standard | Fee | ✗ | CA$100–120 | Change + bag |
| Flex | Fee | **No refund** | CA$100–120 | **Pure refundability** |
| Comfort | Fare diff | Refundable | Included | Incremental |
| Latitude | Fare diff | Refundable | Included | — |

On domestic and US routes, **Flex is non-refundable** — the non-refundable zone extends one tier deeper than international. First genuine refundability only appears at Comfort.

#### BQ Mapping by Route Type

| AC tier | International `flexible` | Domestic/US `flexible` |
|---|---|---|
| Basic | 1. Not Flexible | 1. Not Flexible |
| Standard | 2. Change Only | 2. Change Only |
| Flex | **4. Flexible** | **2. Change Only** |
| Comfort | 4. Flexible | 4. Flexible |
| Latitude | 4. Flexible | 4. Flexible |

> **Data note:** Flex, Comfort, and Latitude all collapse to `4. Flexible` on international routes. On domestic/US routes, only Comfort and Latitude are Flexible. In neither case can we distinguish which of the 2–3 collapsed tiers the customer chose.

#### Volume Split (Revised — US Carved Out)

| Segment | Orders | Share | Non-refundable tiers | First refundability | Pure refundability step |
|---|---|---|---|---|---|
| True international | 18,947 | 46% | 2 (Basic, Standard) | Flex (tier 3) | Standard → Flex |
| US origin/destination | 14,144 | 34% | 3 (Basic, Standard, Flex) | Comfort (tier 4) | Flex → Comfort |
| CA Domestic | 8,415 | 20% | 3 (Basic, Standard, Flex) | Comfort (tier 4) | Flex → Comfort |

**54% of AC orders (domestic + US) follow the deeper suppression structure** — three non-refundable tiers before first genuine refundability. This is the highest suppression depth of the three airlines analyzed.

#### Volume & Suppression Summary

| Metric | Value |
|---|---|
| Total orders (Jan–May 2026) | 30,477 |
| Non-refundable share | 86.6% |
| Upsell rate | 44.8% |
| Suppressed tiers — international | 2 |
| Suppressed tiers — domestic/US | 3 |
| First refundability — international | Flex (tier 3 of 5) |
| First refundability — domestic/US | Comfort (tier 4 of 5) |

---

### Three-Airline Comparison

| Dimension | EY | UA | AC |
|---|---|---|---|
| Economy tiers | 4 flat | 4 cabin × 3 sub-tier | 5 |
| Route split needed | No | Yes (D/I) | Yes (intl / domestic+US) |
| Suppressed tiers — primary segment | 2 | 1 | 2–3 |
| First refundability at | Comfort (tier 3) | Flexible sub-tier | Flex (intl) / Comfort (domestic+US) |
| Pure refundability step | Value → Comfort | Standard → Flexible | Standard→Flex (intl) / Flex→Comfort (domestic+US) |
| Price to first refundability | +13.4% long-haul | +16.4% over Standard | Not yet quantified |
| BQ visibility | Clean | Moderate (Economy Plus conflated) | Limited (3 Flexible tiers collapsed) |
| Non-refundable % | 86.7% | 90.3% | 86.6% |
| Upsell rate | 79% | 38.1% | 44.8% |
| Narrative role | **Lead case** | Validation | Structural complexity illustration |

### Cross-Airline Takeaways

1. **The suppression mechanism is consistent.** Across all three airlines and all route types, 24hr display fires at tiers where long-term refundability is the sole or primary upgrade driver. The label removes exactly the signal that would motivate the next upgrade step.

2. **Suppression depth is the ROI filter.** Airlines with more non-refundable tiers below first refundability have larger addressable upgrade pools. The pure refundability step is where fix impact is highest — no competing upgrade motivation to absorb the loss.

3. **Route type is a required dimension.** Domestic and international fare structures differ materially within the same airline (UA, AC). Using blended totals without route-type split understates suppression depth for domestic/US-heavy segments (AC: 54% of orders in deeper suppression structure).

4. **BQ visibility limits measurement.** Multiple tiers collapsing to the same `flexible` value means we cannot observe which tier customers land at after a fix. The correct A/B test metric is **Flexible-tier share** or **average revenue per economy order** — not headline upsell rate. Standard upsell% will not capture tier-to-tier movements within the non-refundable or refundable zones.
