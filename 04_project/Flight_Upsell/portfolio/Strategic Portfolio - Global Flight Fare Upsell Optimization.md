## 1. The Elevator Pitch (For Senior Leadership)

_Context: Use this when a VP or Senior Director asks, "What are you working on?" Focus on the business impact, not the mechanics._

**The Pitch:** "I'm leading the International Flight Upsell strategy. Historically, we've struggled to grow ancillary revenue because we treated 'upsell' as a purely UI problem. My analysis revealed it's actually a supply-chain problem—we were losing margin because of 'Ghost Fares' where we simply weren't sourcing the higher-tier airline brands correctly on the backend.

I’ve restructured our approach into a 4-step funnel: _Coverage, Grouping, Ranking, and Display_. Right now, I'm spearheading an audit of 40 global airlines using a new 'Golden Route' anomaly detection framework. By fixing the upstream coverage pipes first, we are unblocking downstream UI conversions, which is projected to lift our global upsell rate by [X]% in Q[Y].

We are identifying massive revenue leaks. To do this faster, I actually restructured how the International team works with the FBU data engineers—we've bypassed the old dependency queues by prototyping the data ourselves, which is letting us move 10x faster."

note: what's in Schubert / Serena / Nikki's mind?
## 2. Background: The Complexity of the OTA Flight Upsell

_Context: For future replication and onboarding._

Upselling flight fares in a multi-source OTA environment is fundamentally different from a direct airline dot-com. The complexity stems from:

- **Supplier Fragmentation:** We aggregate from direct airline APIs, GDS, and consolidators. Each has different technical constraints, brand naming conventions, and ATPCO matching limitations.
    
- **The "Constructed Fare" Dilemma:** As an OTA, we have the unique advantage of bundling custom fare options (e.g., combining a naked fare with a 3rd-party bag). However, this creates an immense "decision load" for the user. We must balance offering superior variety against overwhelming the customer, while building trust for non-official OTA bundles.
    
- **Dynamic Yield Management:** Fare families change without notice, and availability fluctuates wildly based on route and days to departure, making benchmarking highly volatile.
    

## 3. The Solution Framework: The Upsell Funnel

_Context: Demonstrates structured product thinking for CV and performance reviews._

To systematically address these challenges, I defined a sequential, 4-lever optimization funnel (plus 2 governance levers). We cannot optimize a downstream lever until the upstream lever is secure.

1. **Coverage (The Supply Pipe):** Do we physically have the inventory? We cannot upsell a fare we don't source. (Current Primary Focus).
    
2. **Grouping (Decision Architecture):** Are we overwhelming the user? We must consolidate overlapping fares from different sources into clean, distinct "tiers" (e.g., Light, Standard, Flex) to reduce cognitive overload.
    
3. **Ranking (Visibility):** Are the most lucrative/relevant fares in the "Buy Box"? Since 80% of users only view the top 3 slots, we must prevent irrelevant combinations or extreme prices from displacing highly convertible fares.
    
4. **Front-End UI (Conversion):** Is the value proposition clear? Resolving UI friction (unclear inclusions, missing brand names, difficult comparisons).
    
5. _Governance Levers (Deprioritized for Phase 1):_ Airline Compliance (Workstream 5) and Internal Pricing/Markup Logic (Workstream 6).

## 4. My OKR Contributions & Impact

_Context: Direct input for performance reviews and resume bullets. Fill in the [X] placeholders with hard data._

**Objective:** Increase total ancillary revenue and Upsell Rate (conversion from cheapest fare to non-cheapest fare) for direct international traffic.

**Key Results & Leadership Actions:**

- **Architected the "Coverage First" Strategy:** Shifted cross-functional focus from UI tweaking to root-cause supply analysis. Designed a "Triage & Trigger" methodology (Archetypes & Golden Routes) to distinguish between natural inventory exhaustion (Sold Out) and true technical/sourcing bugs, saving engineering teams estimated [X] hours of wasted debugging.
    
- **Led the Global Brand Fare Audit (40 Airlines):** Directed regional teams to map and audit Brand Fares across 40 top-tier global airlines. Created the auditing framework and training materials, aligning disparate regional teams into a single data-gathering standard.
    
- **Data Pipeline Prototyping:** Ideated and prototyped the initial coverage dataset requirements with the Flight Business Unit (FBU) and Data Engineering, enabling the business to query "Ghost Fares" (where users bought cheap fares because up-tier options were structurally missing).
    
- **Business Impact:** Identified [X] critical routing gaps, leading to a [X]% improvement in brand fare coverage on target routes, directly contributing to a [X]% lift in Upsell Conversion for [Specific Airline/Region].

- **Redefined Cross-Functional Ways of Working:** Overcame historical data-dependency bottlenecks between the International and Flight Business (FBU) departments. Established a new agile collaboration model by leveraging local IBU data capabilities for rapid prototyping (~1 hour query times), while aligning with FBU strictly for final metric governance. This reduced cross-departmental friction and accelerated time-to-insight.

## 5. Strategic Lessons & Future Replication

_Context: Proves you are a "thinker" who can build scalable playbooks._

- **Lesson 1: Don't Boil the Ocean (Data constraints):** Trying to analyze coverage across all global routes is mathematically impossible due to route scatter and seasonality. Future audits must use "Route Archetypes" (Commuter vs. Leisure) and monitor only the highest-volume "Golden Route" per archetype as a proxy for total airline health.sd
    
- **Lesson 2: The "Ghost Query" is the Ultimate KPI:** General coverage rates are misleading. The only metric that matters is identifying searches where a user bought the cheapest fare _and_ zero brand fares were returned. This isolates technical failure from pricing rejection.
    
- **Lesson 3: Decouple Execution from Governance:** The biggest barrier to speed is not technical; it is organizational dependency. To drive efficiency in a matrixed org, we must separate _execution_ from _governance_. IBU should build independent, lightweight data pipelines for fast exploratory analysis (Execution), but rely on FBU to sign off on the final definitions (Governance). This prevents "engineering queue" bottlenecks while maintaining global data alignment.

---

1. **Quantify the Leakage (The "Why"):** Calculate or estimate the revenue lost due to the mapping errors you found in the 40-airline audit. (e.g., "Identified a 15% coverage gap in premium fares across top 40 airlines").
    
2. **Define the Architectural Fix (The "How"):** Frame your data prototyping not as just "making a dataset," but as "engineering a cross-database translation layer between HIVE and BigQuery to bypass data silos."
    
3. **Draft the Bullet Points (The "Result"):**
    
    - _CV Bullet 1 (Strategic Leadership):_ "Led global fare upsell strategy, aligning technical execution (FBU) with international market strategy (IBU) to optimize premium fare visibility, identifying $X in potential revenue leakage across 40 tier-1 airlines."
        
    - _CV Bullet 2 (Data & Operations):_ "Prototyped cross-functional data pipelines bypassing legacy HIVE/BigQuery silos, and implemented AI-driven communication frameworks that reduced cross-departmental issue resolution time by X%."
---

_Standard approach:_ You tell leadership that you are improving communication between FBU and IBU to make the middle page look better and sell better fares. (This is too operational).

_Option C (The Executive Frame):_ Focus on the **structural advantage** and the **hidden money**. Executives don't care about the meetings; they care about the moat.

**The Elevator Pitch (Memorize the structure, adapt the numbers):**

> *"Trip.com is leaving significant margin on the table because our infrastructure historically treats premium airline fares as technical anomalies rather than core products. Currently, IBU and FBU are speaking different languages—literally and in the data architecture.
> 
> I am building the translation layer between our market strategy and our technical infrastructure. We just completed an audit of 40 global airlines and found [Insert Key Data Point, e.g., 'we were failing to map 20% of high-margin branded fares']. By fixing the supply coverage and ranking algorithms, I'm not just cleaning up the UI; I'm aligning our technical stack with user willingness-to-pay. This will allow us to construct OTA-specific fare bundles that bypass airline limitations and directly increase our upsell rate without sacrificing base conversion."*

---
## The Elevator Pitch (The 3-Sentence Strategy)

_Standard approach:_ You tell leadership what you are doing (monologue). _Strategic approach:_ You don't try to make them remember you; you make them want to _talk_ to you. Leaders are constantly told things; they are rarely asked high-level, thought-provoking questions.

**The Framework:**

1. **Ownership + Team Credit:** State what you did, but shift the spotlight to the team to show collaborative leadership.
    
2. **The Strategic Trade-Off Ask:** Ask a question regarding a high-level business trade-off (e.g., Margin vs. Conversion). Do _not_ ask operational questions.
    
3. **The Actionable Close:** Validate their response and immediately tie it to a next step.
    

**The Script (Adapt based on context):**

> **Sentence 1 (The Hook):** > _"I led the premium fare audit across our top 40 global airlines, and the FBU/IBU team together mapped out exactly where we are leaking high-margin revenue on the middle page."_
> 
> **Sentence 2 (The Ask):** > _"We are presenting the technical fix roadmap next week. Given current company priorities, do you think we should push FBU to aggressively prioritize upsell visibility to maximize AOV, or take a more conservative UI approach to fiercely protect base conversion rates?"_
> 
> _(Pause. Let the VP answer. They will likely give you a nuanced view on how the company is currently balancing growth vs. margin)._
> 
> **Sentence 3 (The Close):** > _"That makes complete sense and is super helpful. I'll take that exact perspective back to the team so we can adjust our ranking algorithms to reflect that balance in the next sprint."_

Painpoints:
FBU works on bulk optimization, but we think the opportunity lies in different pockets. It's easier to do small experiments and run small tests then think about how to scale it.