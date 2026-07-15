# Background

When Trip.com shows a low brand fare coverage rate for a given route, the root cause can be one of two things: either the airline does not offer that fare product at all (expected, nothing to fix), or the airline does offer it but Trip.com is failing to retrieve it (a gap that needs to be investigated). Distinguishing between these two cases requires checking the airline's own website directly.

There are also two distinct layers where coverage can be lost:

- **比价前覆盖率 (Pre-comparison / resource-side coverage)** — whether Trip.com successfully retrieved the branded fare from the supplier at all, measured as `has_brand_cnt / total_cnt`. A low rate here means the supply retrieval itself is failing.
- **比价后覆盖率 (Post-comparison / selection coverage)** — whether the retrieved fare survived the comparison/ranking algorithm and was actually shown on the selection page, measured as `output_has_brand_cnt / output_total_cnt`. A material drop between the two rates (> 5pp) indicates the comparison step is filtering out fares that were successfully retrieved.

Airline website verification addresses the pre-comparison layer: it confirms whether the fare exists on the airline's side, allowing us to determine whether the issue is "airline doesn't offer it" or "platform failed to retrieve it."

# Tool Description

**This tool automates the airline website check**. It samples airline.com across a defined set of routes, dates, and search parameters, extracts the brand fares available on each flight, and calculates a coverage rate that can be compared directly against Trip.com's internal supply data. Any fare where airline.com shows significantly higher coverage than Trip.com's pre-comparison rate is flagged as a platform retrieval gap ("航司有，平台缺").

---

## Workflow

The process has four steps:

**Step 0 — Fare Family Research (desk research).** Before running BQ analysis or scraping, establish the airline's Fare Family design via desk research. Key areas to cover:
- **Baggage policy** — how many checked bags per tier, carry-on rules
- **Change/rebook policy** — fee-based vs. free, which tiers allow changes
- **Refund policy** — non-refundable / fee-based / free per tier
- **Fare gradient** — how many tiers exist and how they differ in flexibility

This matters because Trip.com's internal mapping may be missing tiers. For example, ANA (NH) currently maps only Value, Flex, and Full Flex — missing the **Standard** tier that exists on the airline's website. Desk research surfaces these gaps before data collection, so the scraper and BQ analysis can be interpreted correctly.

**Step 1 — Identify candidates.** Use Trip.com's internal supply coverage data (BigQuery) to identify routes where pre-comparison or post-comparison coverage is anomalous. Routes where pre-comparison coverage is below 80% become candidates for airline website verification. Routes where post-comparison coverage drops more than 5pp below pre-comparison coverage are flagged as comparison filter anomalies (no airline website check needed for these — the issue is in the platform's comparison algorithm, not the supplier).

Each BQ run automatically saves a raw data snapshot to `audit/{AIRLINE}/bq_snapshot_YYYYMMDD.csv` (see BQ Data Pipeline section). This avoids re-querying BQ for historical comparisons.

**Step 2 — Sample airline.com.** The tool automatically searches airline.com for each candidate route using a standardised set of parameters (see Sampling Rules below). For each search it records every flight returned and all brand fares available on that flight, along with the displayed price. Screenshots of each result are saved for reference.

Even when theoretical coverage rates are not problematic, it is useful to run a spot-check scrape on 1–2 high-volume routes per fare family type. This confirms that the mapped fare tiers are actually being surfaced correctly end-to-end.

**Step 3 — Compare and flag.** The parser aggregates the sampled data and calculates coverage rates per brand fare per route. These are compared against the internal pre-comparison figures:
- Airline website ≈ 100%, Trip.com pre-comparison < 80% → **航司有，平台缺** (platform retrieval gap; escalate to tech/commercial team)
- Airline website also low → fare is not offered by the airline on this route (expected; no action)

---

## Sampling Rules

Searches are generated automatically based on the following rules, so that the sample is consistent and reproducible across runs.

**Routes** are loaded from a per-airline `routes.csv` file located at `audit/{AIRLINE}/routes.csv` (e.g., `audit/TK/routes.csv`, `audit/JL/routes.csv`). Each airline manages its own route list independently, which allows scrapers for different airlines to run in parallel without file conflicts. The `--update-routes` flag on `bq_coverage_check.py` writes flagged ODs to the correct per-airline file automatically.

**Dates** default to 7 consecutive days starting approximately +45 days from the run date. This can be overridden via CLI flag.

**Search type** defaults to round-trip (RT), 1 passenger, for all dates. This yields 7 searches per route. A typical batch of 4 routes = 28 searches.

**Concurrency:** The scraper supports up to 3 concurrent browser workers (`--workers 1/2/3`, default 3). Routes are distributed round-robin across workers; each worker controls its own Chromium browser instance. Actual runtime:
- 3 domestic routes (21 searches): ~5–8 min with 3 workers
- 4 international routes (28 searches): ~11–12 min with 3 workers

*The original sequential design (3 dates × OW+RT = 6 searches per route, ~45–60 min for 4 routes) has been superseded by the concurrent 7-day RT-only design above.*

---

## Output

Each run produces the following in the airline's output folder (`~/Documents/Audit/{AIRLINE}/`):

**Per-search CSVs** — one file per search (`{AIRLINE}_{YYYYMMDD}_{pax}pax_{triptype}_{route}_fares.csv`), containing one row per brand fare per flight.

**Combined flights CSV** — `TK_flights.csv` — all searches merged, ready for analysis.

**Coverage rate CSV** — `TK_coverage.csv` — coverage rate per route × fare × direction.

**HTML report** — `TK_coverage_report.html` — single-page bilingual report (中文 / English toggle) with four sections:
1. 比价前覆盖率 · 国内线 — historical BQ data + airline website verification table + screenshots
2. 比价前覆盖率 · 国际线 — historical BQ data + proxy route verification (if run)
3. 比价后覆盖率 · 国内线 — supply% → selection% table with per-fare drop
4. 比价后覆盖率 · 国际线 — summary only if no issues

Sections with no issues are summarised in one line. The report is self-contained (screenshots embedded as base64) and opens directly in any browser.

**Screenshots** — `screenshots/YYYYMMDD_{flight_id}_economy.png` — one screenshot per flight per cabin. The `flight_id` matches the `flight` column in the fare CSVs (e.g., `TK1865_TK8219`).

---

## Report Generation

After the parser runs, the HTML report is built programmatically from:
- BQ data (pre-comparison coverage, filter drop, volume thresholds)
- `TK_coverage.csv` (airline website verification rates)
- Screenshots (embedded as base64)

**Language toggle:** CSS classes `.zh` / `.en` (block elements) and `.zh-i` / `.en-i` (inline spans). A JavaScript `setLang()` function toggles `body.lang-en` to switch between languages. Both versions are in the same HTML file — no separate files needed.

**Key terminology in reports:**

| Chinese | English | Definition |
|---|---|---|
| 比价前覆盖率 / 资源侧覆盖率 | Pre-comparison coverage / resource-side coverage | `has_brand_cnt / total_cnt` |
| 比价后覆盖率 | Post-comparison coverage / selection coverage | `output_has_brand_cnt / output_total_cnt` |
| 中间页计数 | Trace ID Count | Each Trace ID = one unique selection page |
| 航司有，平台缺 | Airline has it; platform does not retrieve it | Root cause classification for supply gaps |

---

## Multi-Airline Design

The tool is designed to scale across airlines. The scraper for each airline handles the website-specific interaction (booking form, calendar, fare extraction). All scrapers write to the same standard CSV schema, so the coverage calculation and report generation logic is shared and does not need to be rewritten per airline.

Routes are managed centrally in `routes.csv`. To add a new airline, add rows with the new airline code and its routes — no changes to the analysis logic are needed.

---

## Technical Reference

This section covers implementation details for anyone maintaining or extending the tool.

### Architecture

Each airline has a dedicated scraper (`fetch_fares_{airline}_v2.py`) that launches Playwright's own Chromium browser in headful mode (Path B, default). A CDP fallback (`--cdp`, Path A) connects to a user-launched Chrome session instead — used when the airline's bot detection blocks Path B.

The scraper fills the airline's booking form, waits for fare results, expands fare tier panels, and writes CSV output. The shared parser (`parse_{airline}_html.py`) reads the CSVs and computes coverage rates.

### Browser Modes

**Path B (default):** Playwright launches its own Chromium headfully with stealth arguments (`--disable-blink-features=AutomationControlled`, etc.). No manual setup required. Works for most airlines.

**Path A (CDP fallback):** Connects to a user-launched Chrome via Chrome DevTools Protocol. Use when Path B is blocked.

```bash
# macOS — launch once before running a batch
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir="/tmp/chrome-debug-session"
```

Then run the scraper with `--cdp`. The debug Chrome window can be minimised. Cookie state persists to disk across runs.

### Concurrency

Workers are implemented with `asyncio.gather()`. Each worker runs `run_worker()`, which manages its own browser context from start to finish. Routes are distributed round-robin across workers at startup (`route_batches[i % n_workers]`). Workers share no state. The script automatically caps workers to the number of routes (no point in more workers than routes).

### Reliability Features

- **Retry logic** — each search is retried up to 3 times (5-second pause) before being written to `failed_searches.log`
- **CAPTCHA handling** — if detected, script pauses up to 5 minutes for manual solving
- **Session recovery** — booking form visibility checked at start of each search; script waits for manual intervention if missing

### Scaling Considerations

- **Per-airline scraper effort** — each new airline requires a bespoke scraper for its booking form UI; analysis layer is reused
- **Anti-bot variability** — airlines vary in bot detection aggressiveness; Path B (stealth Chromium) handles most cases; Path A (real user Chrome) as fallback
- **UI fragility** — scrapers depend on CSS selectors; airline website updates may require selector maintenance

### BQ Data Pipeline

**Table:** `trip-ibu-adhoc.ibu_adhoc_temp.MZ_coverage_check_for_claude`

The BQ script (`bq_coverage_check.py`) checks table freshness (refreshes if >30 days old) and produces two flagging outputs:

**【资源缺口】 Resource gap** (`supply_coverage < 80%`, above P75 volume or coverage = 0%):
- These routes are written to `audit/{AIRLINE}/routes.csv` and scraped
- Top-50 country pairs; P75 volume threshold filters noise from low-volume ODs
- OD limits: top-5 country pairs → 20 ODs each; others → 10 ODs

**【比价过滤】 Comparison filter** (`filter_drop > 5pp`, `supply_coverage ≥ 80%`, above P75):
- These routes are reported in the analysis output but are NOT scraped (issue is in Trip's algorithm, not the airline)
- Shown in report Part 2 with supply% → selection% and drop per fare

**Raw snapshot:** Every `bq_coverage_check.py` run automatically saves a raw data snapshot to `audit/{AIRLINE}/bq_snapshot_YYYYMMDD.csv`. This file contains all coverage metrics (supply_pct, selection_pct, filter_drop_pp) per airport_pair × brand_name, and is kept as a permanent record. Use `--no-snapshot` to skip if needed.

### Standard Fare CSV Schema

| Column | Description |
|---|---|
| `checking_date` | Date the data was collected (YYYY-MM-DD) |
| `departing_date` | Scheduled departure date |
| `trip_type` | OW or RT |
| `pax_count` | Number of passengers searched |
| `departing_airport` | Origin IATA code |
| `arriving_airport` | Destination IATA code |
| `flight` | Flight number(s), e.g. `TK1865_TK8219` for a connecting itinerary |
| `departing_time` | Scheduled departure time |
| `arrival_time` | Scheduled arrival time |
| `fare_name` | Brand fare name as shown on airline.com |
| `price_after_promo` | Displayed fare price |
| `currency` | Currency code |

Additional airline-specific columns (baggage allowance, change policy, etc.) may follow these core columns.