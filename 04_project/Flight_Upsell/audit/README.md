# Air China Fare Scraper - Sept 16, 2026 Only

This script scrapes Air China fares for ICN→TAO on **September 16, 2026** only, for both 1 and 2 passengers.

## Install

```bash
pip3 install selenium pandas webdriver-manager
```

## Run

```bash
python3 air_china_fare_scraper.py
```

## Output

Creates `air_china_fares_ICN_TAO_20260916.csv` with columns:

| Column | Example |
|--------|---------|
| checking_date | 2026-05-07 |
| departing_date | 2026-09-16 |
| arrival_date | 2026-09-16 |
| pax_count | 1 or 2 |
| departing_airport | ICN |
| arriving_airport | TAO |
| class | Economy |
| flight | CA8888 |
| departing_time | 12:15 |
| arrival_time | 13:05 |
| fare_name | Economy Flex / Economy Latitude |
| baggage | (to be extracted) |
| change | (to be extracted) |
| refund | (to be extracted) |
| phoenix_miles | (to be extracted) |
| price_before_promo | 1185.00 |
| price_after_promo | 1185.00 |

## What it does

1. Searches Sept 16 for 1 passenger
2. Extracts all flights and fare options
3. Searches Sept 16 for 2 passengers
4. Saves all data to CSV

Takes about 5-10 minutes. Chrome will stay open while running.

## Next Steps

Once this works, we can:
- Extract detailed baggage/change/refund policies by clicking into fare cards
- Add Oct 15 and Nov 15 searches
- Parse promo code scenarios
