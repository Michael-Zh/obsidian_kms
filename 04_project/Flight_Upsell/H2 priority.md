## Executive Summary - The Strategic Inflection Point

The document opens with a clear thesis: we've successfully built the coordination engine but now face diminishing returns from bulk optimization. The next phase requires building an insight engine to unlock granular opportunities.

## What We Did Well - Foundation Building (Q1 2026)

- FBU Contributions: 5 structured workstreams, bi-weekly syncs, centralized data sources
    
- IBU Contributions (J&M): Single source of truth, 40% communication overhead reduction, 12+ regional requests consolidated
    
- Project Infrastructure: Clear KPI definitions (33%→38% target), structured collaboration model
    

## Quick Data - Upsell Rate Hitting Ceilings

- Current global rate: ~34-35% (vs. 38% target)
    
- Improvement rate slowing: +1-2% QoQ vs. initial +3-4%
    
- Critical insight: Bulk optimization is experiencing diminishing returns - we've captured the low-hanging fruit
    

## Strategic Gap - Missing Insight Generation

- FBU acknowledges bandwidth limitations for deep analysis
    
- Regional intelligence (12+ submissions) remains underutilized
    
- Opportunity: IBU can fill the insight gap, moving from coordinator to strategic partner

## 2. Data Analysis Strategy for Opportunity Discovery ✅

Document: upsell_data_analysis_strategy.md (included in artifacts)

This strategy directly addresses your challenge: _"how can I estimate how much potential business impact we can get, just by looking at the high level data"_

## Three-Phase Approach:

## Phase 1: Diagnostic Framework (Weeks 1-4)

- Upsell Rate Decomposition: Distinguish between "optimal pricing" (good low rate) vs. "missing premium fares" (bad low rate)
    
- Segment Performance Heat Mapping: 3D analysis (airline × route × customer segment)
    
- Data Quality Assessment: Ensure granular data availability
    

## Phase 2: Opportunity Identification (Weeks 5-8)

- Bottom-Up Analysis: Micro-segment performance at airline/route/customer level
    
- Business Impact Formula:
    
    Opportunity Value = Traffic Volume × Upsell Gap × Average Fare Difference × Conversion Rate
    
- Prioritization Matrix: Business impact (40%), implementation effort (25%), speed to impact (20%), strategic alignment (15%)
    

## Phase 3: Test & Learn Framework (Weeks 9-12)

- Agile Testing: 3 pilot programs covering different optimization types
    
- Measurement Framework: Statistical significance targets, control group design
    
- Weekly Review Cadence: Performance monitoring → anomaly detection → root cause analysis → scale decisions
    

## Key Methodologies to Address Your Challenges:

1. "Bulk vs. Granular" Dilemma:
    
    - Move from aggregate reporting to airline/route/segment level analysis
        
    - Identify where bulk optimization is masking significant variation
        
    
2. Upsell Rate Misinterpretation:
    
    - Establish airline-specific "expected" upsell rates based on fare tier distribution
        
    - Separate true upsell success from pricing/coverage issues
        
    
3. Business Impact Estimation:
    
    - Bottom-up calculation at granular level
        
    - Conservative estimates with clear confidence intervals
        
    - ROI prioritization based on implementation feasibility
        
    

## Immediate Next Steps (Week 1):

1. Secure granular data access (airline/route/segment level)
    
2. Calculate airline-level upsell rates with 6-month trends
    
3. Identify top/bottom 5 performers for root cause analysis
    
4. Present initial findings to FBU partners for quick-win alignment

---
# Insight work brainstorming
Pillar 1: "Smart Whitelisting" (Solving the FBU "Bulk" Problem)

The Strategy: Accept that FBU will only build generic, global solutions (e.g., a generic "Upsell Pop-up" or a "Highlight Badge").

• The PM approach: Tests it globally. It fails. The PM scraps it.

• The Strategist approach: Knows it failed globally because it was shown to the wrong people. You analyze the failed test to find the sub-segments where it worked.

• The Action: You introduce the concept of "Smart Whitelisting." Tell FBU: "Build the generic feature, but put a toggle on it. IBU will give you the exact list of Airlines/Archetypes to turn it ON for, and we will keep it OFF for the rest." * Example: The pop-up harms conversion for Leisure routes (they get scared of the price and leave), but it works for Business routes. You tell FBU to run their generic solution only on the "Archetype A (Commuter)" routes we defined earlier.

Pillar 3: "Top-Down Sizing" (Estimating Impact without Deep Dives)

The Strategy: You do not need to look at individual routes to estimate impact. You just need a benchmark.

• The Formula: Take a specific airline segment (e.g., Top 5 EU LCCs). Calculate their current average Upsell %. Now, look at the best performing EU LCC in that group.

• The Math: (Target Best-in-Class Upsell % - Current Avg Upsell %) * Total Annual Orders * Average Upsell Margin ($) = Total Opportunity Size.

• The Action: You say, "If we can bring Ryanair and EasyJet up to the same baseline upsell rate as WizzAir, the mathematical opportunity is $X Million per year. We don't need to check every route; we just need to close the systemic gap."

---
#### Step 1: Deconstruct the "Brand" into "Primitives"

Customers do not wake up wanting an "Economy Flex" ticket. They want to check a bag, or they want the safety of a refund.

- **Action:** Stop looking at the "Brand Fare" name. Break the fares down into their Primitive Attributes: `Bag`, `Seat`, `Refundability`.
    

#### Step 2: Find the "Natural Demand Ceiling" (What they want)

To know what people _want_, you must look at a pristine environment where Supply and UI are both perfect.

- **Action:** Take your **Golden Routes** (from the Archetypes we built earlier) where you know Coverage is exactly 100%.
    
- **The Calculation:** On these perfect routes, what percentage of people buy a Bag? What percentage buy Refundability?
    
- **The Baseline:** Let's say on Leisure Golden Routes, **45%** of people buy a bag when it is offered perfectly. _This 45% is your Natural Demand Ceiling._ That is what the market "wants."
    

#### Step 3: The "Price Elasticity" Check (The Right Price)

Now we find out what they are willing to pay for what they want.

- **Action:** Filter that 45% bucket by the _Price Delta_ (the cost difference between the Base fare and the Bag fare).
    
- **The Logic:** You will see a breaking point. For example, when the Bag costs +$30, the attachment rate is 45%. When the Bag costs +$60, it drops to 15%.
    
- **The Insight:** You now have mathematical proof of the "Right Price." You know they _want_ it, but they only _value_ it at <$50.
    

#### Step 4: The "Supply Gap" Audit (Do we offer it?)

Now you take the "Want" (45%) and apply it to the rest of the messy, real-world routes.

- **Action:** Pick a random, underperforming Leisure route (e.g., LON to ALC). Look at its Bag attachment rate.
    
- **The Diagnosis:**
    
    - If the rate is **5%**, you compare it to your 45% ceiling. You are missing 40% of the demand.
        
    - _Why?_ Check the Price Delta. Is it +$60? (Pricing problem). Check the Ghost Query. Did the bag option even load? (Coverage problem).
        

### The Pitch to Leadership

When you explain this, you merge the Supply and the UI seamlessly:

> *"We don't need to guess what customers want. By analyzing our 'Golden Routes' where our supply connection is perfect, we’ve established the **Natural Demand Ceiling**—for example, we know mathematically that 45% of leisure travelers _want_ a checked bag if the upsell is under $40.
> 
> If a route is underperforming that 45% benchmark, we only have to ask two questions: 1) Did we fail to source the bag (Coverage)? or 2) Did we price it above their elasticity threshold? My strategy isolates those two variables so we stop treating every low-converting route as a mystery."*