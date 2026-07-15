---
name: "fare-analysis-ca"
description: "Batch process Air China fare HTML files from /CA folder, extract flight data, calculate coverage rates ranked by price, and provide insights."
---

# Air China Fare Analysis Skill

You are an Air China fare data analyst. When invoked, process HTML/TXT files from the project's `/CA` folder to extract flight data and calculate fare coverage rates.

## Prerequisites

The project folder must contain a `/CA` subfolder with Air China search result HTML files saved as `.txt` files.

## Fare Ranking

**Important:** Fares should be ranked dynamically by their actual average price (cheapest to most expensive), NOT by hardcoded fare names. Calculate the average price for each fare type from the data and sort accordingly.

## Execution Steps

### Step 1: Locate the CA folder

Find the `/CA` folder in the current project directory. If not found, ask the user to provide the path or create the folder structure.

### Step 2: Run the fare parser

Execute the parsing script to extract flight data from all `.txt` files in the CA folder. The parser should:

- Extract metadata from HTML content (not filenames): date, passenger count, trip type (OW/RT), route
- Extract flight details: flight numbers, times, airlines
- Extract fare details: fare name, baggage, change/refund policies, prices, phoenix miles
- For RT flights: correctly identify outbound vs inbound by detecting when flight indices restart
- Swap airports for inbound flights (departing_airport shows actual departure city)

Use this Python code for parsing:

```python
"""Air China Fare Parser - Extract flight data from HTML files"""

from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import re
from pathlib import Path

def extract_info_from_html(html_content):
    """Extract date, pax count, trip type, and airports from HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    departing_date = pax_count = trip_type = from_airport = to_airport = None
    
    # Extract trip type from cart-header-details
    cart_header = soup.find(class_='cart-header-details')
    if cart_header:
        header_text = cart_header.get_text().lower()
        if 'round trip' in header_text:
            trip_type = "RT"
        elif 'one way' in header_text:
            trip_type = "OW"
    
    # Fallback to page title
    if not trip_type:
        title = soup.find('title')
        if title:
            title_text = title.get_text()
            if 'Round' in title_text:
                trip_type = "RT"
            elif 'One Way' in title_text:
                trip_type = "OW"
    
    # Extract route from cart-header-details
    if cart_header:
        header_text = cart_header.get_text()
        route_match = re.search(r'\(([A-Z]{3})\)\s*to\s*[^(]*\(([A-Z]{3})\)', header_text)
        if route_match:
            from_airport = route_match.group(1)
            to_airport = route_match.group(2)
    
    # Extract passenger count
    pax_match = re.search(r'(\d+)\s*Passenger', html_content, re.IGNORECASE)
    if pax_match:
        pax_count = int(pax_match.group(1))
    
    # Extract date
    month_names = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
                   'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
    
    date_match = re.search(r'(\d{1,2})\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)', html_content)
    if date_match:
        day = date_match.group(1).zfill(2)
        month = month_names.get(date_match.group(2), '01')
        departing_date = f"2026-{month}-{day}"
    
    return departing_date, pax_count, trip_type, from_airport, to_airport
```

### Step 3: Calculate coverage rates with price-based ranking, split by route

After parsing, calculate fare coverage rates. **Two rules apply:**

1. **Rank fares by their actual average price** (cheapest to most expensive), not by name.
2. **Split coverage by route** — calculate a separate table for each origin-destination route pair (e.g. HKG-BCN and HKG-TFU are separate). Do NOT mix flights from different routes into the same coverage calculation.

**How to determine the route pair:**
- Normalise each record's route to an unordered pair so that both directions map to the same group: `route_pair = '-'.join(sorted([departing_airport, arriving_airport]))` (e.g. both HKG→TFU and TFU→HKG become `HKG-TFU`).
- Group all OW and RT records for the same route pair together under one table.

```python
def calculate_coverage_by_route(df):
    """Calculate coverage rate split by route pair, trip_type, direction, pax_count, and fare."""

    # Fare ranking uses the full dataset so prices are comparable across routes
    fare_avg_price = df.groupby('fare_name')['price_after_promo'].mean()
    fares_sorted = list(fare_avg_price.sort_values().index)
    fare_ranking = {f: i for i, f in enumerate(fares_sorted)}

    # Assign route pair (normalised, order-independent)
    df = df.copy()
    df['route_pair'] = df.apply(
        lambda r: '-'.join(sorted([r['departing_airport'], r['arriving_airport']])), axis=1
    )

    results = []
    for route_pair, route_df in df.groupby('route_pair'):
        # OW legs for this route
        ow_df = route_df[route_df['trip_type'] == 'OW']
        for pax, group in ow_df.groupby('pax_count'):
            group = group.copy()
            group['fk'] = group['departing_date'].astype(str) + '_' + group['flight']
            total = group['fk'].nunique()
            for fare in fares_sorted:
                n = group[group['fare_name'] == fare]['fk'].nunique()
                results.append({
                    'route_pair': route_pair, 'trip_type': 'OW', 'direction': 'N/A',
                    'pax_count': pax, 'fare_name': fare,
                    'flights_with_fare': n, 'total_flights': total,
                    'coverage_rate': round(n / total * 100, 1) if total > 0 else 0,
                    'avg_price': fare_avg_price[fare], 'fare_rank': fare_ranking[fare]
                })

        # RT legs for this route
        rt_df = route_df[route_df['trip_type'] == 'RT']
        for (pax, dep), group in rt_df.groupby(['pax_count', 'departing_airport']):
            arr = group['arriving_airport'].iloc[0]
            direction = dep + '->' + arr
            group = group.copy()
            group['fk'] = group['departing_date'].astype(str) + '_' + group['flight']
            total = group['fk'].nunique()
            for fare in fares_sorted:
                n = group[group['fare_name'] == fare]['fk'].nunique()
                results.append({
                    'route_pair': route_pair, 'trip_type': 'RT', 'direction': direction,
                    'pax_count': pax, 'fare_name': fare,
                    'flights_with_fare': n, 'total_flights': total,
                    'coverage_rate': round(n / total * 100, 1) if total > 0 else 0,
                    'avg_price': fare_avg_price[fare], 'fare_rank': fare_ranking[fare]
                })

    cdf = pd.DataFrame(results)
    cdf = cdf.sort_values(['route_pair', 'trip_type', 'direction', 'pax_count', 'fare_rank'])
    return cdf, fares_sorted, fare_avg_price
```

### Step 4: Save outputs

Save two CSV files to the project folder:
- `CA_flights.csv` - Raw extracted flight data
- `CA_coverage.csv` - Coverage rate analysis (includes `route_pair` column)

### Step 5: Display results in conversation

**IMPORTANT:** After processing, display **one markdown table per route pair**. Each table should have a heading with the route name. Columns are built dynamically from whatever OW pax counts and RT directions exist for that route. Rows are ordered by price (cheapest first). Include the average price in the fare name cell.

Use `—` for any combination that has no data (no search was done for that pax count / direction on that route).

### Step 6: Provide insights

After the tables, provide brief per-route insights:

1. **Availability Pattern**: Which fares have limited vs full availability per route
2. **Price-Availability Trade-off**: Cheaper fares typically have lower coverage
3. **OW vs RT**: How coverage differs between trip types per route
4. **Direction Differences**: Any asymmetry between outbound and inbound
5. **Recommendations**: When to book which fare based on availability and route

## Example Output Format

---

**Coverage Rate Analysis Complete**

Processed X files, extracted Y fare records.

### Route: HKG-BCN

| Fare (avg HKD) | OW 1pax | RT HKG→BCN 2pax | RT BCN→HKG 2pax |
|----------------|---------|-----------------|-----------------|
| Economy Standard (3,730) | 0.0% | 0.0% | 0.0% |
| Economy Flex (3,752) | 0.0% | 0.0% | 0.0% |
| Economy Selected (4,796) | 100.0% | 100.0% | 100.0% |
| Economy Latitude (5,058) | 0.0% | 0.0% | 0.0% |

### Route: HKG-TFU

| Fare (avg HKD) | OW 2pax | RT HKG→TFU 1pax | RT HKG→TFU 2pax | RT TFU→HKG 1pax | RT TFU→HKG 2pax |
|----------------|---------|-----------------|-----------------|-----------------|-----------------|
| Economy Standard (3,730) | 60.0% | 90.0% | 52.9% | 88.9% | 88.9% |
| Economy Flex (3,752) | 60.0% | 100.0% | 58.8% | 100.0% | 100.0% |
| Economy Selected (4,796) | 70.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| Economy Latitude (5,058) | 100.0% | 100.0% | 58.8% | 100.0% | 100.0% |

**Key Insights — HKG-BCN:** Economy Selected is the only available fare; all cheaper tiers show 0% coverage on this long-haul route.

**Key Insights — HKG-TFU:** Strong availability across all tiers, especially for 1pax. Economy Standard/Flex are good value choices.

Files saved:
- `CA_flights.csv` - Raw flight data
- `CA_coverage.csv` - Coverage analysis (with route_pair column)

---

## Python Code Reference

Use the `parse_html.py` and `coverage_analysis.py` scripts in the project folder if available, or implement the parsing logic as documented in this skill.

