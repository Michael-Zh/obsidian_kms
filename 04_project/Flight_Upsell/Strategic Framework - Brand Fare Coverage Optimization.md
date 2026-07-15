## 1. Executive Summary & Objective

**Business Objective:** Increase Total Upsell Revenue (and consequent Order/Segment growth) within Direct, Economy-class traffic by optimizing the conversion rate from the "Cheapest Fare" to "Higher-Tier Brand Fares" on the multi-source middle page.

**Phase 1 Objective (The Coverage Audit):** Determine the root cause of "Missing Brand Fares." When a user searches for a flight and the middle page fails to display an up-tier Brand Fare option, we must accurately attribute the failure to one of three categories:

1. **Inventory/Supplier Driven:** The fare is genuinely Sold Out (OOS) or not filed for that specific date/route.
    
2. **Sourcing/Commercial Driven:** The OTA does not have the commercial agreement or connection to source that specific fare family.
    
3. **Technical/Configuration Driven:** The OTA _should_ have the fare, but mapping errors, caching issues, or API timeouts are preventing display.
    

## 2. The Core Challenges (Diagnosis)

The traditional "Top-Down" analysis approach fails in this environment due to the following structural complexities:

- **C1. The "Route Scatter" Problem:** Fare families vary by City Pair, and booking volume is heavily fragmented. Taking a simple "Top 100 Routes" list yields scattered, unrepresentative data that makes drawing systemic conclusions nearly impossible.
    
- **C2. The Yield Management Variable (Intermittency):** Airline inventory is highly dynamic. A fare missing on a specific flight/date is often a standard revenue management tactic (sold out), not a technical failure. Distinguishing "OOS" from "Tech Bug" via aggregate data is highly prone to false positives.
    
- **C3. The "Relative Low" Dilemma:** There is no universal benchmark for "Good" coverage. 40% coverage on a peak holiday route might be excellent, while 40% on a low-season Tuesday indicates a severe technical break.
    
- **C4. The Anti-Scraping Constraint:** Because automated benchmarking against airline websites (the "source of truth") is blocked, validation must be entirely manual. This creates a severe bottleneck and mandates a microscopic, highly-targeted sampling strategy.
    

## 3. Strategic Recommendations (The Linear Sequence)

To solve the "Manual Bottleneck" and "Route Scatter," we must abandon random sampling. We will implement a **"Triage & Trigger"** methodology. We only investigate anomalies, never averages.

### Step 1: Abandon "Routes" – Use "Archetypes"

Instead of looking at thousands of scattered routes, categorize routes into 3-4 structural archetypes per airline based on internal OTA data.

- _Archetype A (The Commuter):_ High frequency, short haul (e.g., LHR-CDG). Expected behavior: Consistent fare families, rarely sold out weeks in advance.
    
- _Archetype B (The Leisure):_ Highly seasonal, medium haul. Expected behavior: Wild swings in availability based on holidays.
    
- _Action:_ Select only **one high-volume representative route** for each archetype per airline. This becomes your "Golden Route." You only monitor the Golden Routes.
    

### Step 2: Define "Low Coverage" via Self-Benchmarking

Do not compare coverage against an arbitrary number (e.g., "Is 50% bad?"). Compare the route against itself across different booking windows (Days to Departure - DTD).

- _The Logic:_ Technical issues are static; Inventory issues are dynamic.
    
- _The Test:_ Look at the Golden Route for flights departing in 3 days vs. flights departing in 60 days.
    
    - _Result A:_ If 3-day coverage is 10% and 60-day coverage is 90%, **this is normal Yield Management (Sold Out)**. Do not manual check.
        
    - _Result B:_ If 3-day coverage is 10% and 60-day coverage is 15%, **this is a Sourcing/Tech failure**. Proceed to manual check.
        

### Step 3: The "Ghost Query" Filter (Minimizing the Sample)

Before deploying human capital for manual checks, isolate the exact searches that represent actual revenue loss.

- Filter internal data for searches where the user ultimately bought the _Cheapest Fare_ on a Golden Route.
    
- Isolate the traces where _zero_ Brand Fares were returned in the middle page.
    
- This specific list of trace IDs forms the absolute boundary of your manual testing pool.
    

### Step 4: The "Manual Check" Protocol (Execution)

Because manual checks are expensive, they must be highly structured. When an anomaly triggers a manual check (e.g., 60-day coverage is inexplicably low), the human tester executes this exact sequence:

1. **The Control Search:** Search the exact Date/Flight/Origin/Destination on the OTA. Confirm the Brand Fare is missing.
    
2. **The Source Search:** Search the exact Date/Flight/Origin/Destination on the Airline's official website.
    
3. **The Verdict Classification:**
    
    - _Airline site shows Sold Out / Unavailable:_ Log as **Valid OOS** (Close case).
        
    - _Airline site shows Fare available:_ Log as **Tech/Sourcing Defect**.
        
4. **The Escalation:** Only Tech/Sourcing defects are passed to the FBU/Engineering teams, accompanied by the exact Trace ID and a timestamped screenshot of the airline website.
    

**Summary of Approach:** By moving from "Global Route Mapping" to "Archetype Anomaly Detection," we reduce the manual validation workload by ~95%, ensuring that every manual check performed is highly likely to uncover a fixable technical or commercial gap rather than natural inventory exhaustion.