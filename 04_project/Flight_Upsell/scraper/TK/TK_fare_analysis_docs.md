# Airline.com Brand Fare Coverage Checker

## Purpose

When trip.com shows a low coverage rate for a particular brand fare on a given route, the root cause can be one of two things: either the airline does not offer that fare product at all (expected, nothing to fix), or the airline does offer it but trip.com is missing the supply (a gap that needs to be investigated). Distinguishing between these two cases requires checking the airline's own website directly.

This tool automates that check. It samples airline.com across a defined set of routes, dates, and search parameters, extracts the brand fares available on each flight, and calculates a coverage rate that can be compared directly against trip.com's internal supply data. Any fare where airline.com coverage is significantly higher than trip.com coverage is flagged as a potential supply gap.

---

## Workflow

The process has three steps:

**Step 1 — Identify candidates.** Use trip.com's internal supply coverage report to narrow down which routes and airlines have potentially low brand fare coverage. These become the input for the airline.com check.

**Step 2 — Sample airline.com.** The tool automatically searches airline.com for each candidate route using a standardised set of parameters (see Sampling Rules below). For each search it records every flight returned and all brand fares available on that flight, along with the displayed price. Screenshots of each result are saved for manual review.

**Step 3 — Compare and flag.** The parser aggregates the sampled data and calculates coverage rates per brand fare per route. These are compared against the internal figures. Fares where the gap exceeds a meaningful threshold are flagged for follow-up.

---

## Sampling Rules

Searches are generated automatically based on the following rules, so that the sample is consistent and reproducible across runs.

**Routes** are loaded from a `routes.csv` file with columns `airline, departure, arrival`. Any number of airlines and routes can be included; each airline's scraper filters to its own rows.

**Dates** are derived from the date the tool is run: the nearest upcoming Monday at +2 months, the nearest upcoming Wednesday at +3 months, and the nearest upcoming Saturday at +4 months. This gives three departure dates spread across a near-to-mid future horizon, covering a weekday and a weekend across different seasons.

**Search types** follow fixed rules:
- One-way (OW): 2 passengers, all three dates
- Round-trip (RT): 1 passenger, all three dates as departure, return 6 days later (Mon→Sun, Wed→Tue, Sat→Fri)

This yields 6 searches per route (3 dates × 2 trip types), or 24 searches for a typical batch of 4 routes, which takes approximately 45–60 minutes to complete per airline.

---

## Output

Each run produces the following in the airline's output folder:

**Per-search CSVs** — one file per search, containing one row per brand fare per flight with price, flight number, times, and origin/destination.

**Combined flights CSV** — all searches merged into a single file, ready for analysis in Excel or Python.

**Coverage rate table** — printed to the console and saved as a CSV. Shows, for each route and brand fare, what percentage of sampled flights offered that fare. Example:

```
Route: IST-AYT

| Fare      | OW 2pax | RT 1pax |
|-----------|--------:|--------:|
| EcoFly    |  100.0% |  100.0% |
| ExtraFly  |  100.0% |   95.0% |
| PrimeFly  |   93.0% |   90.0% |
| Business  |  100.0% |  100.0% |
```

**Screenshots** — one screenshot per flight per cabin, saved to a `screenshots/` subfolder, for manual spot-checking of what the airline's website actually showed.

---

## Multi-Airline Design

The tool is designed to scale across airlines. The scraper for each airline handles the website-specific interaction (booking form, calendar, fare extraction). All scrapers write to the same standard CSV schema, so the coverage calculation and comparison logic is shared and does not need to be rewritten per airline.

The core output schema covers: checking date, departure date, trip type, passenger count, origin, destination, flight number, departure and arrival times, fare name, price, and currency. Airlines that display additional fare attributes (carry-on allowance, checked bag policy, change and refund conditions, or unique perks) can add these as extension columns without breaking the shared analysis.

Routes are managed centrally in `routes.csv`. To add a new airline, add rows with the new airline code and its routes — no changes to the analysis logic are needed.

---

## Technical Reference

This section covers implementation details for anyone maintaining or extending the tool.

### Architecture

Each airline has a dedicated scraper script (`fetch_fares_{airline}_playwright.py`) that connects to a locally running Chrome session via the Chrome DevTools Protocol (CDP). The scraper fills the airline's booking form, waits for results, expands fare tier panels, and writes CSV output. The shared parser script (`parse_{airline}_html.py`) reads the CSVs and runs the coverage calculation.

### Chrome Setup

The scraper connects to an existing Chrome window rather than launching its own browser. This avoids bot detection, allows manual CAPTCHA solving, and preserves session cookies across runs.

```bash
# macOS — launch once before running a batch
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir="/tmp/chrome-debug-session"
```

This can run alongside a regular Chrome session (different user-data-dir = separate process). The debug Chrome window can be minimised; the scraper controls it in the background. Cookie state persists to disk, so subsequent runs on the same machine do not need to re-authenticate or re-accept consent banners.

If a session expires mid-batch, the script detects that the booking form is not visible and prints recovery instructions, waiting for manual intervention before resuming.

### Reliability Features

- **Retry logic** — each search is retried up to 3 times (with a 5-second pause) before being written to `failed_searches.log`. Failed searches can be re-run individually without repeating the whole batch.
- **CAPTCHA handling** — if a CAPTCHA is detected, the script pauses and waits up to 5 minutes for manual solving before resuming.
- **Session recovery** — booking form visibility is checked at the start of each search; if missing, the script prints step-by-step guidance and waits for confirmation before continuing.

### Scaling Considerations

- **Per-airline scraper effort.** Each new airline requires a bespoke scraper for its booking form UI. The analysis layer is reused as-is.
- **Anti-bot variability.** Airlines vary significantly in their bot detection aggressiveness. The real-browser CDP approach mitigates most risk but is not a guarantee on all sites.
- **Runtime.** Searches run sequentially to reduce detection risk. Expect roughly 10–12 minutes per route per airline for a full OW + RT sample. A batch of 4 routes takes approximately 45–60 minutes.
- **UI fragility.** Scrapers depend on CSS selectors and page structure. Airline website updates may require selector maintenance. Each airline's repository includes a diagnostic script for quickly identifying what changed.

### Standard Fare CSV Schema

| Column | Description |
|---|---|
| `checking_date` | Date the data was collected (YYYY-MM-DD) |
| `departing_date` | Scheduled departure date |
| `trip_type` | `OW` or `RT` |
| `pax_count` | Number of passengers searched |
| `departing_airport` | Origin IATA code |
| `arriving_airport` | Destination IATA code |
| `flight` | Flight number |
| `departing_time` | Scheduled departure time |
| `arrival_time` | Scheduled arrival time |
| `fare_name` | Brand fare name as shown on airline.com |
| `price_after_promo` | Displayed fare price |
| `currency` | Currency code |

Additional airline-specific columns (baggage, change policy, etc.) may follow these core columns.
