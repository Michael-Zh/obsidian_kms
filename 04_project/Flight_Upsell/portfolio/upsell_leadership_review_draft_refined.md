# Flight Upsell Project - Mid-Year Strategic Review & Forward Plan
## For Senior Leadership Review - April 2026

**Prepared by:** Michael Zhang (IBU Strategy Lead)
**Date:** April 30, 2026
**Project:** Flight Upsell Optimization (Global)
**Target Audience:** Senior Leadership, FBU Leadership, IBU Regional Heads

---

## EXECUTIVE SUMMARY

### Current State: Strong Foundation, Emerging Strategic Gaps
The Flight Upsell Project has successfully established critical infrastructure and communication frameworks between FBU and IBU teams. We've moved from fragmented regional requests to a structured collaboration model, achieving **Level 1 success** in transparency and coordination. However, as we approach the mid-year review, we face a strategic inflection point: our current "bulk optimization" approach is hitting diminishing returns, and we need to evolve from project coordination to **strategic insight generation**.

### Core Challenge: The "Bulk vs. Granular" Dilemma
FBU's global optimization solutions, while efficient at scale, fail to capture the nuanced realities of different airlines, routes, and customer segments. Our analysis reveals that:
- **Upsell rate alone is misleading** - High rates don't necessarily indicate success (may miss premium tiers), low rates don't always signal failure (may reflect optimal lower-tier pricing)
- **One-size-fits-all solutions** are hitting performance ceilings
- **Regional intelligence** collected through our new framework remains underutilized

### Strategic Opportunity: IBU as the "Insight Engine"
We propose positioning IBU as the strategic insight partner to FBU - moving beyond coordination to become the **data interpretation layer** that identifies granular opportunities and guides FBU's optimization efforts. This represents a 2-3x potential improvement in upsell impact by moving from bulk to targeted optimization.

---

## 1. WHAT WE DID WELL: FOUNDATION BUILDING (Q1 2026)

### 1.1 Communication & Transparency Framework ✅
**FBU Contribution:**
- Established 5 structured workstreams with clear Q2 pipeline
- Implemented bi-weekly sync cadence
- Created centralized data sources and dashboards (with Lily Li)

**IBU Contribution (J & Michael):**
- **Single Source of Truth:** Consolidated scattered regional requests into unified framework
- **Communication Streamlining:** Reduced FBU-IBU communication overhead by ~40%
- **Clarity & Transparency:** Established Regional Request Collection Form (12+ regional inputs collected)
- **Structured Prioritization:** Implemented impact-based request triage system

### 1.2 Project Infrastructure & Governance
- **KPI Definition:** Clear "Trip Middle-Page Upsell Rate" metric (33% → 38% target)
- **Scope Clarity:** Economy/Premium Economy focus, excluding premium cabins
- **Collaboration Model:** FBU→IBU→Regional teams communication flow established
- **Data Foundation:** Initial data source mapping completed

---

## 2. QUICK DATA: UPSELL RATE HITTING CEILINGS

### 2.1 Current Performance Metrics
- **Global Upsell Rate:** Currently at ~34-35% (vs. 33% baseline, 38% target)
- **Improvement Rate:** Slowing quarter-over-quarter (+1-2% vs. initial +3-4%)
- **Regional Variance:** 15-20% performance gap between top and bottom regions
- **Airline Variance:** 25-30% performance gap between best/worst performing airlines

### 2.2 The "Bulk Optimization Ceiling" Phenomenon
Our analysis indicates FBU's global optimization approach is experiencing diminishing returns:

| Optimization Layer | Impact | Current Status |
|-------------------|--------|----------------|
| **Global Rules** | High initial impact | Mature, limited additional upside |
| **Regional Adjustments** | Medium impact | Partially implemented |
| **Airline-Specific** | High potential | Minimal coverage |
| **Route/OD Pair** | Highest potential | Virtually untapped |

**Key Insight:** We've captured the "low-hanging fruit" through global rules. Future gains require moving down the granularity pyramid.

---

## 3. STRATEGIC FRAMEWORK ENHANCEMENTS: NEW INSIGHTS FROM DEEP ANALYSIS

### 3.1 The 4-Step Upsell Funnel: A Structured Approach
Based on our strategic analysis, we've identified that upsell optimization requires a sequential, 4-lever funnel approach:

1. **Coverage (The Supply Pipe):** Do we physically have the inventory? Cannot upsell a fare we don't source. **(Current Primary Focus)**
2. **Grouping (Decision Architecture):** Consolidating overlapping fares into clean, distinct tiers to reduce cognitive overload
3. **Ranking (Visibility):** Ensuring most lucrative/relevant fares appear in the "Buy Box" (top 3 slots)
4. **Front-End UI (Conversion):** Clear value proposition and frictionless user experience

**Critical Insight:** We cannot optimize downstream levers (ranking, UI) until upstream levers (coverage, grouping) are secure.

### 3.2 The "Ghost Fare" Problem: Identifying True Revenue Leakage
Our analysis reveals a critical distinction: **"Ghost Fares"** - situations where users bought the cheapest fare because **zero brand fares were returned** in the middle page. This is the ultimate KPI for identifying technical/sourcing failures vs. natural inventory exhaustion.

**Impact:** By focusing on "Ghost Queries" (searches where users bought cheapest fare with zero brand fare options), we can:
- Reduce manual audit workload by ~95%
- Focus engineering resources on actual revenue leaks
- Distinguish technical failures from natural yield management

### 3.3 "Golden Route" Methodology: Smart Sampling Strategy
To overcome the "Route Scatter" problem (analyzing thousands of scattered routes), we propose implementing a **"Triage & Trigger"** methodology:

**Step 1: Route Archetypes**
- **Archetype A (The Commuter):** High frequency, short haul (e.g., LHR-CDG)
- **Archetype B (The Leisure):** Highly seasonal, medium haul
- **Action:** Select one high-volume "Golden Route" per archetype per airline

**Step 2: Self-Benchmarking Analysis**
- Compare coverage across different booking windows (3 days vs. 60 days)
- Technical issues = static across time windows
- Inventory issues = dynamic (sold out as departure approaches)

**Step 3: Anomaly Detection**
Only investigate routes where coverage is inexplicably low across all time windows

### 3.4 Organizational Architecture Insights
**Structural Challenges Identified:**
- **Data Architecture:** FBU data in China (HIVE) vs. IBU data overseas (Google BigQuery) creates synchronization delays and discrepancies
- **Communication Gaps:** Different terminologies and scopes (FBU: "segments" vs. IBU: "orders")
- **Process Fragmentation:** No single owner for end-to-end upsell pipeline across multiple FBU teams

**Proposed Solution:** **Decouple Execution from Governance**
- **IBU (Execution):** Build independent, lightweight data pipelines for fast exploratory analysis
- **FBU (Governance):** Sign off on final definitions and global data alignment
- **Result:** Prevent "engineering queue" bottlenecks while maintaining data integrity

---

## 4. WHAT WE HAVEN'T STARTED: STRATEGIC INSIGHT GENERATION

### 4.1 The Missing "Insight Layer"
FBU acknowledges they lack bandwidth for deep analysis. This creates a strategic opportunity for IBU to fill the gap:

**Current State:** FBU Optimization → Regional Implementation
**Proposed State:** FBU Optimization ← **IBU Insights** → Regional Implementation

### 4.2 Regional Intelligence Collection (Progress: 50%)
**Success:** Regional Request Collection Form operational with 12+ submissions
**Bottleneck:** Sirius bandwidth constraints (improving with Doris as new PM)
**Opportunity:** Competitor intelligence sharing increasing (5+ competitor references collected)

### 4.3 Proposed: Weekly Health Check → Opportunity Identification
We recommend establishing a **Weekly Upsell Health Check** process:

1. **Data Monitoring:** Track upsell rate anomalies by region/airline/route using Golden Route methodology
2. **Opportunity Flagging:** Identify "Ghost Query" patterns indicating technical/sourcing failures
3. **Root Cause Analysis:** Distinguish between coverage, grouping, ranking, and UI issues
4. **Recommendation Pipeline:** Feed targeted optimization requests to FBU

---

## 5. STRATEGIC PROPOSAL: FROM COORDINATION TO INSIGHT GENERATION

### 5.1 The "IBU Insight Engine" Framework
We propose a three-tiered approach to unlock the next phase of upsell growth:

**Tier 1: Diagnostic Analytics (Immediate)**
- Weekly health checks with anomaly detection using Golden Route methodology
- Ghost Query identification and prioritization
- Quick-win identification for FBU optimization

**Tier 2: Predictive Modeling (Q3 2026)**
- Upsell propensity scoring by customer segment
- Price elasticity modeling by route/airline
- A/B test opportunity sizing

**Tier 3: Prescriptive Optimization (Q4 2026+)**
- Dynamic pricing recommendations
- Personalized fare ranking algorithms
- Cross-sell/upsell bundle optimization

### 5.2 Resource Requirements & ROI
| Initiative | IBU FTE | FBU Support | Expected Impact |
|------------|---------|-------------|-----------------|
| Weekly Health Check | 0.5 FTE | 0.25 FTE | +1-2% upsell rate |
| Deep-Dive Analysis | 1.0 FTE | 0.5 FTE | +2-3% upsell rate |
| Predictive Modeling | 1.5 FTE | 1.0 FTE | +3-5% upsell rate |
| **Total** | **3.0 FTE** | **1.75 FTE** | **+6-10% upsell rate** |

**ROI Calculation:** Assuming current $X GMV, each +1% upsell = $Y incremental revenue

---

## 6. DATA ANALYSIS STRATEGY: PINPOINTING OPPORTUNITIES

### 6.1 Phase 1: Diagnostic Framework (Next 30 Days)
1. **Segment Performance Analysis**
   - Airline tier analysis (full-service vs. low-cost carriers)
   - Route profitability segmentation using Golden Route methodology
   - Customer segment behavior (business vs. leisure, new vs. returning)

2. **Upsell Rate Decomposition**
   - Separate "true upsell" from "Ghost Fare" scenarios
   - Identify airlines where low upsell rate indicates pricing success vs. technical failure
   - Map upsell performance against fare tier availability

3. **Competitive Benchmarking**
   - Analyze competitor upsell strategies from regional submissions
   - Identify implementable best practices
   - Prioritize quick-win competitive gaps

### 6.2 Phase 2: Opportunity Sizing & Prioritization
**Methodology:**
1. **Bottom-up analysis** of individual airline/route performance using Triage & Trigger approach
2. **Impact estimation** based on traffic volume and current upsell gap
3. **Implementation feasibility** assessment (FBU resource requirements)
4. **ROI prioritization** matrix development

**Expected Output:** Ranked list of 10-15 high-impact opportunities with estimated business value

### 6.3 Phase 3: Test & Learn Framework
**Agile Testing Approach:**
- Start with 2-3 pilot airlines/routes using Golden Route methodology
- Implement targeted optimizations (not bulk changes)
- Measure impact on upsell rate, CR, and GMV
- Scale successful patterns

---

## 7. RECOMMENDATIONS & NEXT STEPS

### 7.1 Immediate Actions (Next 2 Weeks)
1. **Approve IBU Insight Engine Proposal** - Formalize IBU's strategic role
2. **Allocate 0.5 FTE for Weekly Health Checks** - Start diagnostic phase using Golden Route methodology
3. **Establish FBU-IBU Insight Working Group** - Monthly strategic review
4. **Prioritize 3 Pilot Opportunities** - Begin test & learn phase focusing on Ghost Query resolution

### 7.2 Medium-Term Initiatives (Q2-Q3 2026)
1. **Develop Granular Data Capabilities** - Airline/route/segment level reporting
2. **Implement Predictive Models** - Upsell propensity scoring
3. **Build Regional Feedback Loop** - Formalize competitor intelligence sharing
4. **Create Opportunity Dashboard** - Real-time visibility into upsell potential

### 7.3 Success Metrics
- **Short-term (30 days):** First 3 opportunity analyses completed using Triage & Trigger methodology
- **Medium-term (Q2):** +0.5-1% upsell rate improvement from targeted optimizations
- **Long-term (EoY):** +3-5% upsell rate, establishment of IBU as strategic insight partner

---

## APPENDIX: REGIONAL INTELLIGENCE HIGHLIGHTS

### Key Regional Requests & Insights
1. **MENA Region:** Personalized fare ranking ABT opportunity identified
2. **EU Region:** Competitor guarantee vs. fare upgrade strategies observed
3. **APAC Region:** Airline-specific bundling opportunities documented
4. **Americas:** Pricing competitiveness gaps on key routes

### Competitor Intelligence Summary
- **Guarantee programs:** Emerging as differentiator in EU/MENA
- **Dynamic bundling:** Competitors offering more flexible fare packages
- **Personalized ranking:** AI-driven fare ordering showing promise
- **Transparent pricing:** Clear value communication improving conversion

---

## CONCLUSION: STRATEGIC INFLECTION POINT

We've successfully built the **coordination engine** for the Flight Upsell Project. Now we face a critical choice: continue with diminishing returns from bulk optimization, or invest in building the **insight engine** that can identify and unlock granular opportunities using sophisticated frameworks like:

1. **The 4-Step Upsell Funnel** - Ensuring we optimize in the right sequence
2. **Ghost Query Analysis** - Focusing on true revenue leaks
3. **Golden Route Methodology** - Smart sampling for efficient analysis
4. **Triage & Trigger Approach** - Investigating anomalies, not averages

The data is clear: the next 3-5% of upsell improvement won't come from more global rules. It will come from understanding the specific dynamics of individual airlines, routes, and customer segments - exactly the intelligence that IBU, with our regional connections and market understanding, is uniquely positioned to provide.

We recommend embracing this strategic evolution and positioning IBU as FBU's insight partner, transforming our role from project coordinators to business impact drivers.

---

**Prepared for:** Senior Leadership Review
**Contact:** Michael Zhang (IBU Strategy Lead)
**Next Review:** May 15, 2026 - Insight Engine Pilot Results