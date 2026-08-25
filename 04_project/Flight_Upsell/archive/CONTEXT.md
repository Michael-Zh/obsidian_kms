# Data Context — Flight Upsell

## 1. Core Table Catalog

| Table | Purpose | Partition | Join Key |
|-------|---------|-----------|----------|
| `trip-ibu-bi-dw-etl.ibu_bi_dw_cdw.edw_ord_flt_order` | Order-level fact table. One row per sub-order. | `orderdate_d` (DATE) | `orderid` ↔ segment table; `primaryorderid_fill` (self-join) |
| `trip-ibu-bi-dw-etl.ibu_bi_dw_cdw.edw_prd_flt_factfltsegment_eng` | Segment-level fact table. One row per flight segment within a sub-order. | `d` (DATE, daily snapshot — use `DATE(d) = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)`) | `orderid` ↔ order table |

---

## 2. Key Concepts: Primary Order vs Sub-Order

### Primary Order (`primaryorderid_fill`)

- **User-facing** concept: a single booking action from the customer.
- `primaryorderid_fill` = the normalized ID used for counting distinct bookings.
- **Filling rule**: if the order was never split, `primaryorderid_fill = orderid`; if split post-booking, `primaryorderid_fill` takes the original `primaryorderid`.

### Sub-Order (`orderid`)

- **Fulfillment** concept: the actual ticket/tickets issued.
- A single primary order can be **split into multiple sub-orders** for several reasons:
  1. **Round-trip split**: outbound and return legs issued as separate orders
  2. **Multi-passenger split**: each passenger gets their own order
  3. **Adult-child split**: adult and child tickets issued separately (different fare rules)
- `subordercount` = number of sub-orders under this primary order.

### `is_primaryorder` flag

- `1` = this row is the primary order (if not split, it's both the primary and a sub-order; if split, it's the anchor row)
- `0` = this row is a non-primary sub-order (was split off from the primary)
- **Important**: `is_primaryorder = 1` does NOT mean "outbound leg". It's an administrative flag, not a directional one.

### Split scenario examples

**Scenario A: Simple RT, not split** (`subordercount = 1`)
```
primaryorderid_fill = 100
  orderid = 100, is_primaryorder = 1, airline = AK, flightway = D
  └── Segment: sequence=1 AK JHB→KUL (outbound)
  └── Segment: sequence=2 AK KUL→JHB (return)
```
Both legs in the same order. No `is_primaryorder = 0` rows exist.

**Scenario B: RT split into two sub-orders** (`subordercount = 2`)
```
primaryorderid_fill = 200
  orderid = 200, is_primaryorder = 1, airline = AK  ← outbound
  orderid = 201, is_primaryorder = 0, airline = MH  ← return (different airline!)
```
`is_primaryorder = 1` corresponds to the outbound; `is_primaryorder = 0` rows are the return leg(s).

**Scenario C: Multi-pax split** (`subordercount = quantity * 2`)
```
primaryorderid_fill = 300, ord_persons = 2, RT
  orderid = 300, is_primaryorder = 1, airline = AK   ← pax1 outbound
  orderid = 301, is_primaryorder = 0, airline = AK   ← pax1 return
  orderid = 302, is_primaryorder = 0, airline = AK   ← pax2 outbound
  orderid = 303, is_primaryorder = 0, airline = AK   ← pax2 return
```
Sub-orders for multiple pax are all `is_primaryorder = 0` except the anchor.

**Scenario D: OW with connecting segments** (`primorderflightway = S`, `subordercount = 2`)
```
primaryorderid_fill = 400
  orderid = 400, is_primaryorder = 1, airline = AK  ← KUL→BKK
  orderid = 401, is_primaryorder = 0, airline = TG  ← BKK→NRT (connecting)
```
OW multi-leg can have different airlines on different segments.

---

## 3. Key Field Reference — `edw_ord_flt_order`

### Order Identity

| Field | Type | Description |
|-------|------|-------------|
| `primaryorderid_fill` | INT | **Primary order ID** (normalized). Use for counting distinct bookings. |
| `orderid` | INT | **Sub-order ID**. Fulfillment-level ticket ID. |
| `primaryorderid` | INT | Original primary order ID (raw, not filled). |
| `is_primaryorder` | INT | 1 = primary order anchor; 0 = split sub-order. |
| `subordercount` | INT | Number of sub-orders under this primary order. 1 = no split; 2+ = split exists. |

### Itinerary Attributes

| Field | Type | Description |
|-------|------|-------------|
| `primorderflightway` | STRING | **Primary-order-level itinerary type.** S = one-way, D = round-trip, M = multi-leg. Use this for RT/OW classification. |
| `flightway` | STRING | Sub-order-level itinerary type. Same values. Less reliable for primary-order analysis. |
| `flightclass` | STRING | Flight class: I = International, D = Domestic. |
| `primorderflightclass` | STRING | Primary-order-level flight class. Same values. |
| `classes` | STRING | Cabin class combo across all segments, e.g. 'Y', 'Y-Y', 'Y-Y-Y'. Y = all economy; C = business. |
| `sequencecount` | INT | Number of flight segments in this sub-order. |
| `ord_quantity` | INT | Total segment volume: passengers × segments. |
| `ord_persons` | INT | Number of passengers in this sub-order. |

### Product/Routing

| Field | Type | Description |
|-------|------|-------------|
| `subprdtype_pos_primorder` | STRING | **Primary-order-level POS type.** FDM = Domestic, FOB = Outbound Intl, FOS = Outbound Intl Short-haul, FIB = Inbound Intl, FCN = Connecting. **Use for POS filtering at primary order level.** |
| `region` | STRING | Market region (lowercase): th, my, ph, hk, sg, cn, etc. |
| `airline` | STRING | **Airline of the first segment of this sub-order** (IATA 2-letter code). |
| `dportcode` | STRING | Departure airport (IATA 3-letter, first leg). |
| `aportcode` | STRING | Arrival airport (IATA 3-letter, first leg). |
| `dcitycode` | STRING | Departure city code. |
| `acitycode` | STRING | Arrival city code. |

### Financial

| Field | Type | Description |
|-------|------|-------------|
| `price` | FLOAT | Ticket price excluding tax (actual received). |
| `tax` | FLOAT | Tax. |
| `cost` | FLOAT | Bottom price excluding tax. |
| `saleprice` | FLOAT | Airline selling price. |

### Dimensions (join keys)

| Field | Joins to | Purpose |
|-------|----------|---------|
| `airline` | `dim_prd_flt_airline.airline` | Airline name, LCC/FSC flag, home country |
| `dcityid` + `dcitycode` | `dim_prd_pub_city.cityid + citycode` | Departure city details, country code |
| `flightagency` | `dim_prd_flt_flightagencyattribute.flightagencyid` | Agency attributes |

### Date

| Field | Type | Description |
|-------|------|-------------|
| `orderdate_d` | DATE | **Order date (date partition key).** Use for filtering. |
| `orderdate` | STRING | Order date (raw timestamp). |

---

## 4. Key Field Reference — `edw_prd_flt_factfltsegment_eng`

### Segment Identity

| Field | Type | Description |
|-------|------|-------------|
| `orderid` | INT | Sub-order ID. Join key to order table. |
| `sequence` | INT | **Segment sequence within the order.** 1 = first segment (outbound), 2 = second (return for RT). |
| `airline` | STRING | **Operating airline of this segment** (IATA 2-letter). |
| `isshared` | STRING | Whether this is a code-share flight. |
| `carrierflightno` | STRING | Carrier flight number (code-share scenario). |

### Cabin & Brand

| Field | Type | Description |
|-------|------|-------------|
| `classname` | STRING | Cabin class name (Chinese): 经济舱 / 公务舱 / 超级经济舱. |
| `class` | STRING | Cabin class code: Y / C / W. |
| `subclass` | STRING | Booking subclass (fare bucket). |
| `ctrip_brandtier` | STRING | Brand tier at airline/route level. |
| `show_brand_name` | STRING | Customer-facing brand name. |
| `ori_brand_name` | STRING | Raw brand name from underlying engine. |
| `atpco_brand_name` | STRING | ATPCO brand name from branded fare service. |
| `airline_brandtier` | STRING | Brand tier (manually curated, only ~50 airlines). |
| `brand_attributes` | REPEATED STRING | Entitlements for the branded fare. |

### Route

| Field | Type | Description |
|-------|------|-------------|
| `dport` | STRING | Departure airport (IATA 3-letter). |
| `aport` | STRING | Arrival airport (IATA 3-letter). |
| `dcity` / `dcityname` | INT / STRING | Departure city. |
| `acity` / `acityname` | INT / STRING | Arrival city. |
| `tpm` | INT | Mileage. |

### Refund/Change

| Field | Type | Description |
|-------|------|-------------|
| `nonref` | STRING | Refundable flag: T = not refundable, H = refundable. |
| `nonrer` | STRING | Changeable flag (rebook). |
| `nonend` | STRING | Endorsable flag. |
| `reftxt` | STRING | Refund policy (JSON). |
| `rebooktxt` | STRING | Change policy (JSON). |

### Baggage

| Field | Type | Description |
|-------|------|-------------|
| `checkin_bagweight` | INT | Checked baggage weight. -1 = unknown/varies. |
| `checkin_bagnumber` | INT | Number of checked bags. 0 = none; -1+weight>0 = unlimited; -2 = suspect data. |
| `is_free_checkinbag` | STRING | Free checked bag: 是/否/以航司客规为准. |
| `carryon_bagweight` | INT | Carry-on weight. |
| `carryon_bagnumber` | INT | Number of carry-on items. |
| `is_free_carryonbag` | STRING | Free carry-on: 是/否. |
| `baggagevalue` | STRING | Full baggage policy (JSON). |

### Partition

| Field | Type | Description |
|-------|------|-------------|
| `d` | DATE | **Snapshot date.** Always filter with `DATE(d) = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)` for latest. This is a daily full snapshot — historical data may not be available for old dates. |

---

## 5. Common Query Patterns

### Filter to primary orders only
```sql
WHERE is_primaryorder = 1
```

### Count distinct bookings
```sql
COUNT(DISTINCT primaryorderid_fill)
```

### Filter to RT only
```sql
WHERE primorderflightway = 'D'   -- primary-order level
```

### Filter to domestic FDM only
```sql
WHERE subprdtype_pos_primorder = 'FDM'
```

### Filter to Y class only
```sql
WHERE classes LIKE 'Y%'   -- all segments economy
-- Or via segment table:
AND classname IN ('经济舱', '超级经济舱')
```

### Join order table to segment table
```sql
LEFT JOIN `edw_prd_flt_factfltsegment_eng` s
  ON a.orderid = s.orderid
  AND DATE(s.d) = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
  AND s.sequence = 1   -- first segment only (outbound)
```

### Get all segments (not just outbound)
```sql
JOIN `edw_prd_flt_factfltsegment_eng` s
  ON a.orderid = s.orderid
  AND DATE(s.d) = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
-- No s.sequence filter → get all segments
```

### Determine mixed-carrier status within a primary order
The segment table's `airline` field is segment-level and is the most accurate source of which airline operates each leg. For primary-order analysis:

1. Join order table (primary orders) → all sub-orders (via `primaryorderid_fill`) → segment table (via `orderid`).
2. Collect `DISTINCT s.airline` across all segments in all sub-orders of the same primary order.
3. Compare against the AirAsia group set: `('AK','FD','XJ','D7','Z2','QZ','KT')`.

### AirAsia airline codes
```
AK  = AirAsia (Malaysia)
FD  = Thai AirAsia
XJ  = Thai AirAsia X
D7  = AirAsia X (Malaysia)
Z2  = AirAsia Zest / Philippines AirAsia
QZ  = Indonesia AirAsia
KT  = Cambodia AirAsia
```

### POS type codes
```
FDM = Domestic
FOB = Outbound International
FOS = Outbound International Short-haul
FIB = Inbound International
FCN = Connecting
```

---

## 6. Known Pitfalls

1. **`flightway` vs `primorderflightway`**: Always use `primorderflightway` for primary-order-level analysis. `flightway` is sub-order-level and can differ from the primary's actual itinerary type (e.g., a sub-order split from a round-trip may show `flightway = 'S'`).

2. **Segment table partition**: `d` is a daily snapshot. Historical dates may not be available — the table only holds the most recent snapshot state. Always use `DATE(d) = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)`.

3. **`airline` in order table is first-segment only**: The `airline` field on `edw_ord_flt_order` describes the first segment of that sub-order. For multi-leg or mixed-carrier scenarios, use the segment table's `airline` per `sequence`.
   - **Verified (2026-08-06):** For `sequence=1`, `order.airline` and `segment.airline` are 100% identical (tested on 14,246 FDM RT primary orders over 5 days). For `sequence ≥ 2`, rare mismatches exist (<0.3%, mostly PH code-shares like 5J/T6/DG). Conclusion: using `order.airline` for outbound classification is safe, but segment-level is always the correct source of truth.

4. **`is_primaryorder = 0` ≠ return leg**: When `subordercount = 1` (no split), the single order contains both outbound and return segments — there are no `is_primaryorder = 0` rows. When `subordercount ≥ 2`, the `is_primaryorder = 0` rows are the non-anchor sub-orders (could be return legs, additional passengers, or connecting segments).

5. **`ord_persons` can inflate subordercount**: Multi-pax bookings can produce many sub-orders (e.g., 2 pax × RT split = 4 sub-orders). Segment-level counting without `DISTINCT` on `primaryorderid_fill` can double-count.

6. **Region field is lowercase**: `'th'`, `'my'`, `'ph'` — not `'TH'`, `'MY'`, `'PH'`.

---

## 7. Metrics & KPI Definitions

### Primary KPI: Upsell Rate

| Item | Detail |
|------|--------|
| **Formula** | Non-lowest-price primary orders / All primary orders with lowest-price flag |
| **Target** | 33% → 38% (2026) |
| **BQ fields** | `is_lowest_price` (from `dw_fltdb_edw_deal_ord_intl_is_middle_page_lowest_price_di`) |
| **Scope** | Y/W class, 1-meta, all markets |
| **Guardrails** | CR (conversion rate), user dwell time, GMV — must not be negatively impacted |
| **Known weakness** | Denominator includes "passive upsell" (lowest tier sold out or route has no low-tier option), inflating the rate |

### Coverage Rate

| Dimension | Definition |
|-----------|-----------|
| **Supply-level coverage** | Source fare is a Brand Fare → counted as covered, regardless of whether used as a gambling fare or self-bundle. Reflects raw supply capability. |
| **Display-level coverage (excl. gambling)** | Only fares surfaced as genuine Brand Fares in the display path. Gap vs supply-level = gambling fare consumption of supply. |
| **Interpretability caveat** | Denominator unknown — cannot distinguish "we failed to source it" from "airline never offered it." Most interpretable on strict-compliance airlines (AF/KL, AA/DL/LH home markets). |

### Five-Layer Funnel Metrics

| Layer | Core Question | Diagnostic Signal |
|-------|-------------|-------------------|
| 1. Data Foundation | Does fare family design create upsell motivation? | Coverage Rate, fare family structure |
| 2. Supply | Did we receive this fare from the source? | Coverage Rate at supply output |
| 3. Fare Selection | Was the fare correctly included in the candidate set? | **Filter Drop** = Coverage Rate drop between Supply and Selection |
| 4. Ranking | Was the fare in a position users see? | Average rank position of non-purchased upsell fares |
| 5. Display | Does frontend label reflect true ticket attributes? | Attribute accuracy validation (e.g., void/24h vs real refund policy) |

### Filter Drop

Calculated as: `Supply Coverage % − Selection Coverage %` per airline per tier per route. A sudden drop indicates the fare selection algorithm is filtering out fares that should be shown. Common pattern: lowest price tier drop <10pp, highest tier drop 50–80pp.

### Key Dimensions for All Metrics

| Dimension | BQ Source | Example Values |
|-----------|-----------|---------------|
| `region` | `edw_ord_flt_order` | th, my, ph, hk, sg, cn |
| `primorderflightway` | Same table | S (one-way), D (round-trip), M (multi-leg) |
| `subprdtype_pos_primorder` | Same table | FDM (domestic), FOB (outbound intl), FIB (inbound intl) |
| `classes` | Same table | Y, Y-Y (all economy); C, Y-C (mixed cabin) |
| `airline` | Same table (first-segment only) | AK, FD, TG, MH, 5J, etc. |
| `seg_airline` | `edw_prd_flt_factfltsegment_eng` | Per-segment operating airline |
| `is_lowest_price` | `dw_..._is_middle_page_lowest_price_di` | TRUE / FALSE |
| `brand_name` / `atpco_brand_name` | Segment table | Brand fare tier label |
| `cabin_IATAcode` | Derived from `classname` | Y, W, C |

### Two Types of Needle Mover

| Type | Description | Example | Data Requirement |
|------|------------|---------|-----------------|
| Type 1 — Volume Capture Gap | Supply-side coverage gap | EU airline missing baggage-inclusive fare | External benchmark (airline.com) |
| Type 2 — Revenue Quality Gap | Display-side signal error suppressing upsell intent | void/24h label overriding true refund policy | Internal BQ data only; globally uniform fix |
