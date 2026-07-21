# Scraper — Airline.com Brand Fare Coverage Checker

## Purpose

When trip.com shows low coverage for a brand fare on a route, check the airline's own website to distinguish:
- Airline doesn't offer that fare → expected, nothing to fix
- Airline offers it but trip.com is missing supply → gap to investigate

## Directory

| Dir | Airline | Status |
|-----|---------|--------|
| `TK/` | Turkish Airlines | ✅ v1 working (CDP), v2 in dev |
| `NH/` | ANA (All Nippon Airways) | 🟡 v1 CDP — search flow works, fare extraction WIP |
| `JL/` | JAL | ⚪ placeholder |

## Shared Architecture

All scrapers follow the same pattern from `TK/TK_fare_analysis_docs.md`:
- **Launch:** CDP connect to user's Chrome (`--remote-debugging-port=9222`)
- **Routes:** `routes.csv` per airline
- **Dates:** +1mo and +3mo from nearest Monday
- **Output:** standard CSV schema (checking_date, departing_date, trip_type, pax, O/D, flight, times, fare_name, price, currency)
- **Coverage:** shared `parse_*.py` aggregates per-route × tier coverage

## NH Scraper Notes

- **CDP only** — ANA detects automated Chromium. Start Chrome manually:
  ```
  /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
    --remote-debugging-port=9222 --user-data-dir="/tmp/chrome-nh-session"
  ```
- **Must click One Way tab FIRST**, then fill airport/date/pax
- Search flow: airport modal (click field → type IATA → select from list) → keyboard date input → Search
- Results page has 7-day date tabs; click each "From USD..." tab to expand flight details
- Each flight shows 4 Economy tiers (Value/Standard/Flex/Full Flex) plus Premium Economy tiers
- Fare extraction: parse `innerText`, match NH flight blocks, extract USD prices in tier order
- No retry needed on anti-bot page — reuse existing Chrome session with browsing history

## TK Scraper Notes

- v1 CDP working, v2 Playwright has calendar bug
- See `TK/TK_fare_analysis_docs.md` for full workflow and sampling rules
