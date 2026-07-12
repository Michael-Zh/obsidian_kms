# Project Context: Flight Upsell
_Last updated: 2026-06-22_

## What This Project Is

An end-to-end strategy initiative to increase international flight ancillary revenue at Trip.com by optimizing conversion from cheapest fare to higher-tier branded fares on the middle selection page. Phase 1 (coordination engine) is formally delivered and praised by leadership. Phase 2 (Insights Engine) is the active workstream — IBU independently generating granular, data-driven opportunity sizing at airline/route/segment level. The void/24h display override is currently the lead candidate for a needle-mover finding.

**Primary Pillar:** Career  
**Status:** Active — Phase 2 analytical work ongoing  
**Current Focus:** H1 review submission (void/24h number pending) + H2 analytical insights phase  
**Priority:** P1  
**Updated:** 2026-07-11

---

## Objectives

1. **Operational Efficiency:** Streamline issue identification (IBU), provide sufficient technical context for investigation, and ensure FBU updates IBU in plain, concise language.
2. **KPI Alignment:** Establish a unified metric and monitoring system shared between FBU and IBU.
3. **Data-Driven Strategy:** Generate actionable insights to steer business direction and prioritize high-ROI development areas.

---

## Current State & Recent Progress

**Phase 1 (Foundation) — Delivered:**
- Cross-functional coordination engine, global brand fare audit across 40+ airlines, Ghost Fare detection prototype
- Global upsell rate ~34–35% vs. 38% target; bulk optimization ceiling confirmed (+1–2% QoQ)
- Leadership gave explicit positive feedback on the presentation

**Phase 2 (Insights Engine) — BQ/GCP now live:**

**Void/24h Display Override — Lead Finding (Sessions 1–3, 2026-06-16/17) | FBU aligned 2026-06-25:**
- **Core problem:** Backend void/24h policy flag triggers a "free cancellation" label even when the ticket is non-refundable. The correct label (refundability signal) would motivate upgrades to Flexible fares — both misleading users and suppressing upsell.
- **EY anchor finding:** 88% of EY orders have void/24h flag; 86.7% are actually non-refundable → ~144K users potentially misled (Jan–May 2026)
- **Replication complete:** UA (47K, 90.3% misled), DL (33K, 92.7%), AA (26K, 83.3%) — 246K upper bound across 4 carriers
- **Full-airline ranking built:** Top 40 airlines → >1.7M orders upper bound. P0: EY/WS/UA/BA/AC; P1: TG/TK/LH/SK
- **Important caveat:** 1.7M is an upper bound — whether frontend actually shows the label depends on FBU display trigger logic (not yet obtained). Need this to convert to confirmed exposure.
- **Upsell paradox:** EY achieved 79% upsell rate *despite* wrong label (users upgrade for baggage). Fixing the label adds refundability signal on top → rate can only increase.
- **Oliver Tang re-run pending:** `MZ_202606_quantification_cc` void/24h data invalid (snapshot filter issue with `DATE(d) = yesterday`) — needs clean re-run before revenue quantification
- **FBU cross-BU alignment (Session 6, 2026-06-25):** FBU confirmed as UX issue; entered H2 roadmap. Two directions: display both vs. redirect to detail page (hotel precedent via Doris). No aligned solution yet. J/Michael to own ABT metrics spec.

**Diagnostic Framework — Formalized (upsell_diagnostic_framework.md):**
- Five-layer funnel: Data Foundation → Supply → Fare Selection → Ranking → Display
- Two types of needle movers: Type 1 (Volume Capture Gap, e.g. EU supply fix) vs. Type 2 (Revenue Quality Gap, e.g. void/24h) — void/24h is Type 2
- Void/24h = Display layer; global/uniform fix; owned by Global Strategy team

**H1 Strategist Narrative — Draft in progress (H1_strategist_narrative.md, updated 2026-06-21):**
- Core reframe from coaching_20260620: the diagnostic framework is Michael's structural contribution — J's manual check happened *within* the framework
- Key missing piece: the number (rough quantification of 24h/void gap, order of magnitude)
- Draft verbal narrative ready — needs [$X revenue leakage] placeholder filled

**TK Coverage Scraper:**
- v1 (CDP mode): Operational, has historical data for select routes
- v2 (Chromium → CDP fallback): Path B started; calendar selector failing (cookie banner + form load issues) — fix in progress

**Stakeholder dynamics — active pattern:**
- J's standard for strategist output: (1) needle-mover scale (quantify, don't just identify), (2) independent judgment (arrive with hypothesis, not raw data)
- BLUF before J updates: state hypothesis first, then offer data
- Cross-BU escalation pattern: open with mandate + shared OKR, escalate early from junior contacts, close with one scoped question

**Open decisions / blockers:**
- FBU display trigger logic not obtained — defines conversion from 1.7M upper bound to confirmed count; this is the key missing input
- Oliver Tang re-run needed (`MZ_202606_quantification_cc` fix) before revenue leakage can be calculated
- Revenue leakage placeholder still empty: fare delta (Non-Flexible → Flexible) × conversion lift for EY
- H1 narrative needs [$X] filled before review

---

## Next Steps (session backlog)

- [ ] **Oliver Tang re-run:** Fix `MZ_202606_quantification_cc` (snapshot filter `DATE(d) = yesterday` invalid) — get clean void/24h data as input for revenue quantification
- [ ] **Revenue leakage quantification:** Estimate fare delta (Non-Flexible → Flexible) × conversion lift for EY; fill [$X revenue leakage] placeholder — this unlocks H1 narrative
- [ ] **FBU display logic:** Get from FBU PM — under what conditions does void/24h label trigger? (channel vs. agency vs. locale) — converts 1.7M upper bound to confirmed exposure
- [ ] **H1 review narrative:** Finalize `H1_strategist_narrative.md` once [$X] is filled; practice verbal delivery
- [ ] **Top-Down Sizing:** Fill revenue leakage placeholder for at least one airline group (e.g., EU LCCs: Ryanair vs. WizzAir benchmark)
- [ ] **Natural Demand Ceiling:** Identify Golden Routes with 100% coverage; calculate bag/refund attachment rates as baseline
- [ ] **Ghost Query rate:** Establish as primary diagnostic metric with actual numbers from BQ
- [ ] **TK scraper v2:** Fix Path B (Chromium) — cookie banner auto-dismiss + form visibility validation
- [ ] **Apply J's stakeholder framing:** BLUF pattern in next J update; document what changes vs. previous approach
- [ ] **Expand airline scope:** Beyond 4 flagged airlines — use Q3 in `void_policy_display_analysis.md` to run airline-level overview for remaining P1/P2 tiers
- [ ] **Upgrade step framework — P0/P1 airlines:** Apply upgrade step anatomy to WS, BA, LH, SK — classify suppression depth and pure refundability steps per airline
- [ ] **RouteType BQ split:** Run for EY and AC to confirm domestic/international volume figures used in Session 4 case studies
- [ ] **A/B test metrics spec:** Define Flexible-tier share + revenue per economy order as primary metrics (not headline upsell%) — must be designed before any test runs
- [ ] **Track FBU void/24h execution:** Monitor solution direction (display both vs. redirect); intervene on ABT metrics spec before FBU design is finalized — do not wait until after design
- [ ] **service_fee_type exploration:** Run distribution of `service_fee_type` from `e_customer_cancellation` against the refreshed table — does it classify cancellation penalty severity (full forfeiture vs. partial fee)? Could sharpen "misleading label" narrative
- [ ] **Void/24h by market cut:** Re-run misled rate split by `market` (CN / HK / SG / EN-INT) — potential indirect evidence of locale-specific FBU display trigger logic

---

## Related Wiki Pages

- **[[Strategist-Requirements]]** — `/02_wiki/Career/Strategist-Requirements.md` — Skills for strategist role at Trip.com
  - Strategist = "driver of movement": diagnoses root problems, aligns matrix stakeholders, translates to roadmap with KPIs
  - Influence gap: "making people around you better" is the distinguishing mark — beyond technical excellence
  - Flight Upsell presentation win + Claude prototype are concrete delivery evidence for H1 review

- **[[Career-Confidence-and-Delivery]]** — `/02_wiki/Career/Career-Confidence-and-Delivery.md` — Confidence vs. anxiety patterns in delivery
  - H1 review explicitly named as calibration moment: what does manager actually see vs. what you fear they see?
  - Anxiety trigger: unclear OKR contribution → over-scoping, delayed delivery. Primary fix: scope clearly (what's in / out)
  - Identity shift in progress: "juggling everything" → "real value through data + strategy + cross-cultural lens"

- **[[OKR-Contribution]]** — `/02_wiki/Career/OKR-Contribution.md` — OKR alignment and career path options
  - Key message to surface with HR BP: "creating clarity is itself a contribution" — needs explicit articulation in formal review language
  - Direction shifting: analysis execution → decision influence (in the room where decisions are made)
  - Two paths: New Market Development (J's trajectory) vs. Regional Strategist (higher autonomy, direct influence)

---

## File Map

| File | When to read |
|------|-------------|
| `Flight Upsell Project Strategic Review - May 2026.md` | Full Phase 1 retrospective, roadmap, workstream status |
| `H2 priority.md` | H2 strategic direction + detailed methodology for all three pillars |
| `upsell_diagnostic_framework.md` | Five-layer funnel, two types of needle movers, KPI comparability principles |
| `void_policy_display_analysis.md` | Full technical brief on void/24h — EY findings, replication queries, risk ranking, SQL |
| `upsell_data_analysis_strategy.md` | Three-phase data analysis playbook; BQ/GCP scope appended 2026-06-12 |
| `H1_strategist_narrative.md` | H1 review draft narrative — verbal script, reframe, what's still needed |
| `Strategic Framework - Brand Fare Coverage Optimization.md` | Triage & Trigger methodology: Archetypes, Golden Routes, Ghost Query filter |
| `Strategic Portfolio - Global Flight Fare Upsell Optimization.md` | Elevator pitches, OKR bullets, strategic lessons, leadership communication scripts |
| `upsell_leadership_review_draft_refined.md` | Leadership review narrative (most recent full version) |
| `Flight_Upsell_Trial_Log.md` | Session log — Sessions 1–5 complete (2026-06-16/17, 2026-06-22/23, 2026-06-24/25); append at end of each session |
| `audit/TK/` | TK scraper v1 (operational) + v2 (in dev); audit workflow documentation |

---

## Working Agreement

You are acting as a **thought partner and analyst** for this project. Your role is to:

- Help design and pressure-test analytical frameworks for opportunity sizing (Phase 2 focus)
- Connect new data findings to the Smart Whitelisting / Top-Down Sizing / Natural Demand Ceiling pillars
- Help translate technical FBU outputs into plain-language IBU strategy and leadership communication
- Challenge assumptions — especially around whether a finding is a pricing issue, coverage issue, or ranking issue
- Reference [[Strategic Framework - Brand Fare Coverage Optimization]] and [[H2 priority]] when discussing methodology
- Use `[[simple_link]]` format for all internal references
- **Start each session by reviewing Next Steps** — triage, discuss, or action before moving on

**Key context to keep front-of-mind:**
- The void/24h display override is the current lead candidate for a needle-mover finding — 1.7M upper bound, but needs FBU display trigger logic to confirm actual exposure
- Revenue leakage quantification (fare delta × conversion lift) is the single most important number missing — unlocks both the business case and the H1 narrative
- The diagnostic framework (five-layer funnel) is Michael's structural contribution — frame it this way in stakeholder conversations and H1 review
- J's standard: arrive with hypothesis + scale estimate, not raw data. BLUF before every J update.
- BQ/GCP is connected — SQL generation and pattern detection are available; new session without sandbox network restriction may be needed for direct queries
- This project feeds directly into H1 performance review narrative; frame all contributions with impact language

**At the end of each conversation:**
1. Summarize any insights, decisions, or new information worth preserving
2. Propose a single log entry for `Flight_Upsell_Trial_Log.md` covering all discussions — formatted and ready to paste, including date, decisions, and food for thought
3. Propose any updates to `## Next Steps` above (items to add, check off, or remove)
4. Wait for approval before writing anything
5. If a wiki page should be updated, note which one and what the addition would be

**Prompt occasionally** during longer sessions: "Good stopping point — want to wrap up and capture what we've covered so far?"

**Do not** rewrite existing content — only propose additions.

**Sync rule:** 每次会话结束更新此 CLAUDE.md 时，同步更新 `_in_case_you_are_bored.md` 里 [[Flight_Upsell]] 行的 Current Focus + Updated 字段。
