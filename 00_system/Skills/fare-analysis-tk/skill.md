---
name: "fare-analysis-tk"
description: "Run the Turkish Airlines fare scraper, parse output CSVs, calculate coverage rates, and display results in the current conversation."
---

# Turkish Airlines Fare Analysis Skill

When invoked, run the full TK coverage audit pipeline — BQ coverage check → route selection → scraper → parser → display results.

## File Locations

| Purpose | Path |
|---|---|
| Scraper + parser scripts | `…/audit/TK/fetch_fares_tk_v2.py`, `parse_tk_html.py` |
| BQ scripts | `…/audit/bq/bq_coverage_check.py`, `create_coverage_table.sql` |
| Routes config | `…/audit/routes.csv` |
| Output (raw CSVs, screenshots, coverage results) | `~/Documents/Audit/TK/` |

Base path for all scripts: `/Users/michael_zhang/Library/Mobile Documents/iCloud~md~obsidian/Documents/KMS/04_project/Flight Upsell/audit/`

All scripts use absolute paths internally — no `cd` required.

## BQ Coverage Table

**Table:** `trip-ibu-adhoc.ibu_adhoc_temp.MZ_coverage_check_for_claude`

**Key fields:**
- `total_cnt` — query denominator at Supply layer (all flight queries)
- `has_brand_cnt` — queries where this specific brand fare was present in supply
- `output_total_cnt` — queries where any fare was returned after Fare Selection
- `output_has_brand_cnt` — queries where this specific fare survived Fare Selection

**Derived metrics:**
- `supply_coverage = has_brand_cnt / total_cnt` — what % of supply queries had this fare
- `selection_coverage = output_has_brand_cnt / output_total_cnt` — same after Fare Selection
- `selection_drop = supply_coverage − selection_coverage` — how much Fare Selection filters out

**Flag thresholds:**
- `supply_coverage < 80%` → core alert (potential Type A supply gap)
- `selection_drop > 5pp` → bonus flag (Fare Selection filtering anomaly)

## Modes

| Mode | Argument | What it does |
|---|---|---|
| **Auto** | _(none)_ | BQ check → auto-select flagged routes → full scrape → parse → display |
| **Test** | `--test` | BQ check + IST→AYT scrape only (2 searches). Fast validation. |
| **Parse only** | `--parse-only` | Skip BQ check + scraper. Re-analyze existing `~/Documents/Audit/TK/*_fares.csv`. |
| **BQ only** | `--bq-only` | Run BQ check and show flagged routes, without scraping. |

If the user just says `/fare-analysis-tk` with no argument, use **Auto** mode.

---

## Execution Steps

### Step 1: BQ coverage check (skip for `--parse-only`)

```bash
python3 ".../audit/bq/bq_coverage_check.py" TK
```

This script:
1. Checks the last `d` value in `MZ_coverage_check_for_claude`
2. If table is missing or last updated >30 days ago → runs `CREATE OR REPLACE TABLE` (takes ~1–2 min, show a progress message to the user)
3. Queries flagged airport-pairs for TK: `supply_coverage < 80%` OR `selection_drop > 5pp`
4. Prints a `__FLAGGED_ROUTES_JSON__` block with the list

**Report to the user** before scraping:
- How many routes are flagged and why (supply gap vs selection drop)
- Whether the table was refreshed or reused

For `--test` mode: still run the BQ check, but scrape IST→AYT only regardless of flags.

### Step 2: Update routes.csv

```bash
python3 ".../audit/bq/bq_coverage_check.py" TK --update-routes
```

This adds any flagged ODs not already in `routes.csv`. Existing manual routes are preserved.

**Before writing**, show the user which routes will be added and ask for confirmation if >5 new routes are being added (to avoid accidental large runs).

### Step 3: Run the scraper (skip for `--parse-only` and `--bq-only`)

```bash
python3 ".../audit/TK/fetch_fares_tk_v2.py" [--test]
```

- The browser window opens visibly (headful). This is expected.
- Report search count upfront: "Running N searches (X routes × 3 dates × OW+RT)…"
- Typical runtime: ~3–5 min for a full run, ~30s per route.

**If scraper fails:**
- Bot-detection / CAPTCHA → advise `--cdp` flag (Path A, uses user's own Chrome)
- Airport/calendar error → show raw error, pause for user

### Step 4: Run the parser

```bash
python3 ".../audit/TK/parse_tk_html.py"
```

Reads all `~/Documents/Audit/TK/*_fares.csv` and writes:
- `~/Documents/Audit/TK/TK_flights.csv`
- `~/Documents/Audit/TK/TK_coverage.csv`

### Step 5: Display results

Read `~/Documents/Audit/TK/TK_coverage.csv` and render as markdown tables — **do not paste raw script output**. Build tables from the CSV.

**Table format:** One table per route pair. Columns built dynamically from `trip_type` × `direction` × `pax_count`. Rows ordered cheapest → most expensive (use `fare_rank`). Include average price in fare name cell.

```
### Route: AYT-IST

| Fare (avg TRY) | OW IST 2pax | RT IST→AYT 1pax | RT AYT→IST 1pax |
|---|---|---|---|
| EcoFly (4,431) | 100.0% | 100.0% | 100.0% |
| ExtraFly (5,155) | 100.0% | 100.0% | 100.0% |
| PrimeFly (5,434) | 100.0% | 100.0% | 100.0% |
| Business (11,909) | 100.0% | 100.0% | 100.0% |
```

Use `—` for combinations with no data.

**For each flagged route** (from Step 1), cross-reference the scraper result against the BQ flag reason:
- If BQ said supply < 80% AND scraper shows airline website also < 80% → Type B (airline restriction), note this
- If BQ said supply < 80% AND scraper shows airline website at 100% → Type A (Trip sourcing gap), highlight this
- If BQ flagged selection_drop AND scraper confirms fare exists on airline side → Fare Selection filter anomaly

### Step 6: Insights

1. **Tier structure** — fare tiers present and their price spread
2. **BQ-flagged routes** — cross-reference scraper findings with BQ flag reasons (Type A vs B)
3. **Coverage gaps** — any scraper result < 100%; distinguish supply vs selection layer
4. **OW vs RT** — any tiers that only appear in one trip type
5. **Data quality** — searches succeeded/failed, dates scraped, sample size caveat

### Step 7: Offer next steps

- Re-run without BQ refresh: `/fare-analysis-tk --parse-only`
- BQ check only (no scrape): `/fare-analysis-tk --bq-only`
- Expand to other airlines: suggest next candidate based on BQ flag volume

---

## TK Fare Tier Reference

| Tier | Class | Includes |
|---|---|---|
| EcoFly | Economy | Carry-on only, non-refundable, no changes |
| ExtraFly | Economy | 1× checked bag, fee-based changes |
| PrimeFly | Economy | 1× checked bag, free changes, partially refundable |
| Business | Business | Full flexibility, lounge access |

TK also has **Saver** fares (below EcoFly) on some routes — note if they appear.

---

## Technical Notes

- **Path B default** (own Chromium, headful) — no manual Chrome setup needed
- **Path A fallback** (`--cdp`) — user must launch Chrome with `--remote-debugging-port=9222`
- **Airport input** — TK uses autocomplete (`[role="option"]`), not a modal; script types IATA code
- **Calendar** — TK auto-opens calendar after destination selection; script detects this
- **OW 2pax + RT 1pax** — both scraped intentionally; some fares only appear in RT context
- **BQ auth** — uses `bq` CLI with active `michael.zhang@trip.com` gcloud account
- **Table staleness** — `MZ_coverage_check_for_claude` is refreshed if last `d` > 30 days ago
