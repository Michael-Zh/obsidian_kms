---
name: "air-china-fare-analysis"
description: "Batch process Air China fare HTML files from /CA folder, extract flight data, calculate coverage rates ranked by price, and display results as a table with insights."
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

### Step 3: Calculate coverage rates with price-based ranking

After parsing, calculate fare coverage rates. **Rank fares by their actual average price**, not by name.

### Step 4: Save outputs

Save two CSV files to the project folder:
- `CA_flights.csv` - Raw extracted flight data
- `CA_coverage.csv` - Coverage rate analysis

### Step 5: Display results in conversation

**IMPORTANT:** After processing, you MUST display the coverage rate as a **markdown table** in the conversation. Format it exactly like this:

```
| Fare | OW 1pax | OW 2pax | RT Out 1pax | RT Out 2pax | RT In 1pax | RT In 2pax |
|------|---------|---------|-------------|-------------|------------|------------|
| [Cheapest Fare] | X% | X% | X% | X% | X% | X% |
| [Mid Fare] | X% | X% | X% | X% | X% | X% |
| [Most Expensive] | X% | X% | X% | X% | X% | X% |
```

Where:
- Rows are ordered by price (cheapest fare at top, most expensive at bottom)
- Columns show: OW (one-way) by pax count, then RT outbound by pax, then RT inbound by pax
- Values are coverage percentages (e.g., "20.0%", "100.0%", "0.0%")

### Step 6: Provide insights

After the table, provide brief insights:

1. **Availability Pattern**: Which fares have limited vs full availability
2. **Price-Availability Trade-off**: Cheaper fares typically have lower coverage
3. **OW vs RT**: How coverage differs between trip types
4. **Direction Differences**: Any asymmetry between outbound and inbound
5. **Recommendations**: When to book which fare based on availability

## Example Output Format

After running the analysis, your response should look like:

---

**Coverage Rate Analysis Complete**

Processed X files, extracted Y flight records.

| Fare | OW 1pax | OW 2pax | RT KUL→PEK 1pax | RT KUL→PEK 2pax | RT PEK→KUL 1pax | RT PEK→KUL 2pax |
|------|---------|---------|-----------------|-----------------|-----------------|-----------------|
| Economy Standard | 20.0% | 20.0% | 9.1% | 0.0% | 10.0% | 20.0% |
| Economy Flex | 100.0% | 100.0% | 63.6% | 20.0% | 60.0% | 60.0% |
| Economy Selected | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |

**Key Insights:**
- Economy Standard (cheapest) has very limited availability (~10-20%), mainly on direct flights
- Economy Flex has good availability for OW but drops significantly for RT with 2 passengers
- Economy Selected is always available across all flight options
- For RT bookings with 2 passengers, Economy Standard may not be available at all on outbound

Files saved:
- `CA_flights.csv` - Raw flight data
- `CA_coverage.csv` - Coverage analysis

---

## Python Code Reference

Use the `parse_html.py` and `coverage_analysis.py` scripts in the project folder if available, or implement the parsing logic as documented in the previous version of this skill.

