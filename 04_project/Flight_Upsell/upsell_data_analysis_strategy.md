# Flight Upsell Project: Data Analysis Strategy for Opportunity Discovery
## Moving Beyond Bulk Optimization to Granular Insights

**Prepared for:** Michael Zhang (IBU Strategy Lead)
**Date:** April 30, 2026
**Objective:** Develop actionable framework to identify and prioritize upsell opportunities at airline/route/segment level

---

## EXECUTIVE SUMMARY: THE GRANULARITY IMPERATIVE

### The Core Problem
FBU's "bulk optimization" approach has delivered initial gains but is now hitting performance ceilings. The fundamental issue: **aggregate upsell rates mask enormous variation** at granular levels. An airline with 20% upsell rate might have routes performing at 5% and 40% - but bulk optimization treats them the same.

### The Strategic Solution
We need to move from **"one-size-fits-all"** to **"segment-of-one"** optimization. This requires a three-phase data analysis approach that identifies where the true opportunities lie and provides FBU with targeted optimization requests.

### Expected Business Impact
- **Short-term (30 days):** Identify 5-10 high-potential opportunities with +1-2% aggregate upsell impact
- **Medium-term (Q2):** Establish systematic opportunity discovery process
- **Long-term (H2 2026):** +3-5% overall upsell rate through targeted optimizations

---

## PHASE 1: DIAGNOSTIC FRAMEWORK (WEEKS 1-4)

### 1.1 Data Source Inventory & Quality Assessment

**Primary Data Sources:**
1. **Transaction Data:** Order-level details (airline, route, fare type, customer segment)
2. **Fare Availability Data:** What fares were actually available at time of search
3. **Pricing Data:** Competitor pricing and our fare ladder positioning
4. **Customer Behavior Data:** Browsing patterns, search history, booking window
5. **Regional Intelligence:** From Request Collection Form (12+ submissions)

**Quality Assessment Checklist:**
- [ ] Data completeness by region/airline
- [ ] Historical consistency (6+ months)
- [ ] Granularity level (route/OD pair availability)
- [ ] Timeliness (data latency < 24 hours)

### 1.2 Upsell Rate Decomposition Analysis

**Critical Insight:** Not all upsell rate variations are equal. We need to distinguish:

| Scenario | Upsell Rate | True Business Implication |
|----------|-------------|---------------------------|
| **Optimal Pricing** | Low (20-25%) | Airline offers perfect lower-tier fare, hard to upsell - **SUCCESS** |
| **Missing Premium Fares** | Low (20-25%) | Higher-tier fares unavailable - **OPPORTUNITY** |
| **Aggressive Upselling** | High (40-45%) | Effective conversion of willing customers - **SUCCESS** |
| **Poor Lower-tier Pricing** | High (40-45%) | Customers forced to upgrade - **PROBLEM** |

**Analysis Methodology:**
1. **Benchmark Creation:** Establish airline-specific "expected" upsell rates based on fare tier distribution
2. **Gap Analysis:** Identify airlines performing above/below expectations
3. **Root Cause Investigation:** Pricing vs. coverage vs. display issues

### 1.3 Segment Performance Heat Mapping

**Three-Dimensional Analysis Framework:**

**Dimension 1: Airline Segmentation**
- Full-service carriers vs. low-cost carriers
- Alliance groupings (Star Alliance, SkyTeam, oneworld)
- Regional dominance (home market advantage)

**Dimension 2: Route Characteristics**
- Distance bands (short-haul < 3h, medium 3-6h, long-haul > 6h)
- Competition intensity (monopoly, oligopoly, competitive)
- Business/leisure mix (based on day-of-week patterns)

**Dimension 3: Customer Segments**
- New vs. returning customers
- Business vs. leisure (inferred from booking patterns)
- Price sensitivity (based on historical purchase behavior)

**Expected Output:** 3D matrix identifying "sweet spots" and "dead zones" in upsell performance

---

## PHASE 2: OPPORTUNITY IDENTIFICATION & PRIORITIZATION (WEEKS 5-8)

### 2.1 Bottom-Up Opportunity Sizing

**Step 1: Micro-Segment Analysis**
- Analyze performance at airline × route × customer segment level
- Identify top 20% and bottom 20% performers
- Calculate "upsell gap" = expected performance - actual performance

**Step 2: Business Impact Estimation**
```
Opportunity Value = Traffic Volume × Upsell Gap × Average Fare Difference × Conversion Rate
```

**Step 3: Implementation Feasibility Assessment**
- FBU resource requirements
- Technical complexity
- Testing timeline
- Regulatory/contractual constraints

### 2.2 Prioritization Matrix Development

**Scoring Framework (1-10 scale):**

| Criteria | Weight | Description |
|----------|--------|-------------|
| **Business Impact** | 40% | Estimated GMV improvement |
| **Implementation Effort** | 25% | FBU development complexity |
| **Speed to Impact** | 20% | Time to test and scale |
| **Strategic Alignment** | 15% | Fits with broader upsell strategy |

**Expected Output:** Ranked list of 15-20 opportunities with clear ROI calculations

### 2.3 Quick-Win Identification

**Characteristics of Quick Wins:**
- High impact (>$X GMV potential)
- Low implementation effort (<2 FBU weeks)
- Uses existing optimization capabilities
- No major technical/contractual barriers

**Target:** Identify 3-5 quick wins for immediate FBU action

---

## PHASE 3: TEST & LEARN FRAMEWORK (WEEKS 9-12)

### 3.1 Agile Testing Methodology

**Pilot Selection Criteria:**
1. **Representative:** Covers different airline types, routes, customer segments
2. **Measurable:** Clear baseline and target metrics
3. **Containable:** Limited scope to minimize risk
4. **Scalable:** Successful patterns can be expanded

**Recommended Pilot Structure:**
- **Pilot 1:** Airline-specific fare ranking optimization
- **Pilot 2:** Route-specific bundling strategy
- **Pilot 3:** Customer segment personalization

### 3.2 Measurement Framework

**Primary Metrics:**
- **Upsell Rate:** Segment-level change
- **Conversion Rate:** Impact on overall booking conversion
- **GMV per Booking:** Average order value change
- **Customer Satisfaction:** Post-booking survey scores

**Control Group Design:**
- Statistical significance targets (95% confidence)
- Minimum sample sizes per variant
- Run duration based on traffic volume

### 3.3 Learning & Scaling Process

**Weekly Review Cadence:**
1. **Performance Monitoring:** Check test metrics vs. targets
2. **Anomaly Detection:** Identify unexpected outcomes
3. **Root Cause Analysis:** Understand why tests succeed/fail
4. **Scale Decisions:** Continue, modify, or stop tests

**Knowledge Capture:**
- Document successful patterns
- Create optimization playbooks
- Update opportunity prioritization based on learnings

---

## DATA INFRASTRUCTURE REQUIREMENTS

### 4.1 Current Gaps & Solutions

**Gap 1: Granular Data Accessibility**
- **Current:** Aggregate reporting only
- **Solution:** Build airline/route/segment level data cubes
- **Timeline:** 4-6 weeks

**Gap 2: Real-time Monitoring**
- **Current:** Weekly/Monthly reporting
- **Solution:** Daily performance dashboards
- **Timeline:** 2-3 weeks

**Gap 3: Competitive Intelligence Integration**
- **Current:** Manual collection in Regional Request Form
- **Solution:** Structured competitor tracking database
- **Timeline:** 3-4 weeks

### 4.2 Tooling & Technology Stack

**Recommended Stack:**
1. **Data Warehouse:** Existing Trip infrastructure + new granular tables
2. **BI Tool:** Tableau/Looker for visualization
3. **Analysis Environment:** Python/R for statistical modeling
4. **Collaboration:** Feishu Docs/Base for sharing insights

**Resource Requirements:**
- **Data Engineering:** 0.5 FTE for 8 weeks
- **Analytics:** 1.0 FTE ongoing
- **FBU Partnership:** 0.25 FTE for requirements alignment

---

## ORGANIZATIONAL MODEL & GOVERNANCE

### 5.1 IBU Insight Team Structure

**Proposed Roles:**
1. **Insight Lead (Michael):** Strategy, prioritization, stakeholder management
2. **Data Analyst:** Daily analysis, opportunity identification
3. **Regional Liaison:** Intelligence gathering, feedback collection
4. **FBU Partner:** Technical feasibility, implementation planning

### 5.2 Weekly Operating Rhythm

**Monday: Health Check**
- Review previous week's performance
- Flag anomalies for investigation
- Update opportunity pipeline

**Wednesday: Deep Dive**
- Analyze 1-2 priority opportunities
- Develop recommendations
- Prepare FBU requests

**Friday: Progress Review**
- Track FBU implementation status
- Update regional teams
- Plan following week's focus

### 5.3 Decision Rights & Escalation

| Decision Type | Owner | Escalation Path |
|---------------|-------|-----------------|
| **Opportunity Prioritization** | IBU Insight Lead | FBU-IBU Leadership |
| **Test Design** | Joint (IBU/FBU) | Technical Governance |
| **Scale Decisions** | FBU with IBU input | Product Leadership |
| **Resource Allocation** | Senior Leadership | Budget Review |

---

## RISK ASSESSMENT & MITIGATION

### 6.1 Key Risks

**Risk 1: Data Quality Issues**
- **Impact:** Misleading opportunity identification
- **Mitigation:** Phase 1 data quality assessment, conservative estimates

**Risk 2: FBU Bandwidth Constraints**
- **Impact:** Slow implementation of identified opportunities
- **Mitigation:** Clear prioritization, quick-win focus, executive sponsorship

**Risk 3: Analysis Paralysis**
- **Impact:** Too much analysis, not enough action
- **Mitigation:** Time-boxed phases, minimum viable analysis approach

**Risk 4: Regional Adoption**
- **Impact:** Insights not translated to local action
- **Mitigation:** Regular regional updates, clear value communication

### 6.2 Success Metrics & Milestones

**30-Day Milestones:**
- [ ] Complete Phase 1 diagnostic analysis
- [ ] Identify first 3 quick-win opportunities
- [ ] Establish weekly health check process
- [ ] Secure FBU partnership agreement

**90-Day Milestones:**
- [ ] Complete 2-3 pilot tests
- [ ] Demonstrate +0.5-1% upsell improvement
- [ ] Formalize IBU Insight Team
- [ ] Scale successful patterns to 5+ airlines

**180-Day Milestones:**
- [ ] Achieve +2-3% aggregate upsell improvement
- [ ] Establish systematic opportunity discovery engine
- [ ] Transition to predictive modeling capability
- [ ] Document and share best practices globally

---

## IMMEDIATE NEXT STEPS (WEEK 1)

### 7.1 Week 1 Action Plan

**Day 1-2: Foundation Setup**
1. Secure access to granular transaction data
2. Map existing data sources and quality
3. Set up analysis environment

**Day 3-4: Initial Analysis**
1. Calculate airline-level upsell rates (6-month trend)
2. Identify top 5 and bottom 5 performers
3. Conduct preliminary root cause analysis

**Day 5: Stakeholder Alignment**
1. Present initial findings to FBU partners
2. Agree on first quick-win opportunity
3. Establish weekly sync cadence

### 7.2 Resource Mobilization

**Immediate Needs:**
1. **Data Access:** Granular transaction data (airline/route/segment level)
2. **Analytics Tool:** Access to BI tools for visualization
3. **FBU Partnership:** Designated FBU counterpart for collaboration
4. **Executive Sponsorship:** Clear mandate for insight generation role

### 7.3 Communication Plan

**Internal (IBU):**
- Daily standup with insight team
- Weekly update to regional heads
- Bi-weekly progress report to J

**External (FBU):**
- Weekly working session with FBU partners
- Bi-weekly leadership sync
- Monthly opportunity review with FBU leadership

---

## CONCLUSION: FROM DATA TO DOLLARS

The Flight Upsell Project stands at a critical juncture. We've built the coordination engine; now we must build the insight engine. The data analysis strategy outlined here provides a clear, phased approach to moving from bulk optimization to granular opportunity discovery.

The potential is significant: our analysis suggests that targeted, airline/route/segment-specific optimizations could deliver 2-3x the impact of continued bulk approaches. But realizing this potential requires investing in analytical capabilities and embracing a new model of FBU-IBU collaboration.

We recommend immediate approval to begin Phase 1, with the goal of identifying our first quick-win opportunities within 30 days and demonstrating measurable impact within 90 days.

---

**Prepared by:** Strategy Analysis Team
**For:** Michael Zhang, IBU Strategy Lead
**Next Review:** May 7, 2026 - Phase 1 Completion


---

## BQ/GCP Integration — 2026-06-12

Claude Code now connected to Google Cloud database + BQ CLI. Scope for dedicated session:
- Specific analysis approach for H1 deliverable
- Maximizing AI assistance for data analysis (SQL generation, pattern detection, hypothesis testing)
- Strategic opportunity detection via BQ queries
- Document drafting support for H1 review output

Session trigger: proactive user prompt (check-back target: mid-July).
