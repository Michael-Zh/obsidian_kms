# Upsell Diagnostic Framework
_Created: 2026-06-16 | Status: Working draft — revisit as project evolves_

---

## Overview

This document captures the diagnostic framework developed through Sessions 1–3 of the Upsell Project analytical work. It is intended as a living reference — not a final deliverable — to be revisited as new data and findings emerge.

**Core framing:** The framework is a hypothesis generator, not a diagnostic conclusion. Its purpose is to narrow the search space and surface priority candidates for experimental validation. Perfection is not the goal; directional accuracy is.

---

## Part 1: Team & Project Positioning

**Team mandate:** Global Strategy team, parallel to Country Market teams. Focus on identifying system-level opportunities with needle mover potential (triple-digit growth unlock). Opportunities that require market-by-market customization are better handed to local teams.

**Decision standard:** Does this opportunity have sufficient scale and global coverage to justify the team's attention? If not, move on.

**Upsell Project status:** Active needle mover candidate. Triggered by an EU success story; the goal is to determine whether similar or larger global opportunities exist in the same domain.

---

## Part 2: The Five-Layer Diagnostic Funnel

```
Data Foundation → Supply → Fare Selection → Ranking → Display
```

### Layer 1: Data Foundation
**Core question:** Does the airline's Fare Family design create sufficient upsell motivation? What is the realistic fare supply on this route?

**Key concept — Fare Family design types:**
- **Stepped jump design:** Lowest tier has carry-on only + non-refundable; next tier jumps directly to checked bag + full flexibility. Large functional leap, strong upsell motivation if price delta is small.
- **Gradual design:** Fine-grained tiers with incremental benefit additions. Each step has different conversion logic; must be analyzed tier-by-tier.
- **LCC Bare Fare model:** Base fare has zero inclusions; add-ons purchased separately. Competes or coexists with Branded Fares; upsell mechanism fundamentally different.

**Why this matters:** Fare Family design is a precondition to the funnel, not a layer within it. If the design itself lacks upsell motivation, fixing any downstream layer yields limited ROI — you'd be better presenting an unattractive product.

**Diagnostic signal:** Coverage Rate (with caveats — see Weakness 1 below)

---

### Layer 2: Supply
**Core question:** Did we receive this Fare from the source?

**Two failure modes:**
- External supply absence: Airline didn't make this Fare available (allocation constraint, seasonal, route-specific)
- Internal configuration error: We have the connection but the Fare wasn't surfaced correctly (e.g., EU success story — Fare existed but was not placed into the selection candidate pool)

**Diagnostic signal:** Coverage Rate at the Supply layer output

---

### Layer 3: Fare Selection
**Core question:** Was an available Fare correctly included in the candidate set shown to the user?

**Diagnostic signal:** Coverage Rate drop between Supply layer and Fare Selection output. A sudden drop here indicates the algorithm is filtering out Fares that should be shown.

---

### Layer 4: Ranking
**Core question:** Was the Fare placed in a position where users are likely to see it?

**Why this layer matters:** ~80% of users only view the top 3 Fares. A Fare ranked 12th has 100% Coverage Rate but near-zero visibility. Coverage Rate cannot detect Ranking problems.

**Diagnostic signal:** Average rank position of upsell Fares — specifically, where non-purchased upsell Fares appear (to distinguish "ranked too low to be seen" from "was seen but not chosen").

**Current data limitation:** Frontend impression data and backend Fare identity linkage is not yet fully confirmed. Ranking diagnostics are partially actionable only.

---

### Layer 5: Display
**Core question:** Does the frontend label accurately reflect the ticket's true attributes?

**Key issue identified:** Void/24h display override — backend `ticketOperationType IN (1,2)` coexists with non-refundable tickets (Change Only / Not Flexible), causing users to see a "24-hour free cancellation" label on a ticket that is actually non-refundable after that window. This suppresses the refundability signal that would motivate Flexible fare upgrades.

**Scale:** 1.7M+ orders upper bound across 40+ airlines (2026 Jan–May). Confirmed replication across EY, UA, DL, AA.

---

## Part 3: Three Structural Weaknesses of the Framework

### Weakness 1: Coverage Rate — unknown denominator

**Problem:** Coverage Rate denominator includes flights where the airline never offered that Fare. Low Coverage Rate conflates:
- **Type A:** We failed to source it → fixable
- **Type B:** Airline doesn't offer it on this route → not our problem

The two cases are indistinguishable from Coverage Rate alone.

**Partial workaround (Coverage Scraper):** Sample + crawl airline website to establish external ground truth:
- Low coverage + airline website also low → Type B, not actionable
- Low coverage + airline website significantly higher → Type A, actionable gap
- Low coverage + airline website similar → Likely temporary configuration, deprioritize

**Limitation:** Scraper is manually triggered sampling, not automated detection. Solves "how to confirm a suspicion" but not "how to find all problems systematically."

---

### Weakness 2: Supply connection configuration is a black box

**Problem:** Having an official connection (GDS / NDC) does not guarantee correct configuration. Airlines change Fare Structure without notification; internal mapping may not be updated. Coverage Rate can appear normal while the actual Fare content is wrong.

**Additional constraint:** Trip.com's supply sources are not uniformly GDS or direct NDC. Not all airlines have official connections, broadening the configuration black box.

---

### Weakness 3: Upsell Rate denominator contamination

**Problem:** `Upsell Rate = is_lowest_price=0 orders / is_lowest_price IS NOT NULL orders`. Denominator includes "passive upsell" cases:
- Lowest-tier already sold out at time of booking
- Route genuinely has no low-tier option

These inflate Upsell Rate without reflecting true conversion capability.

**Practical stance:** Known limitation; still the most operationally trackable proxy in the current system. Accept it, but keep the boundary in mind.

---

## Part 4: KPI Comparability — What Is and Isn't Apple-to-Apple

**Core conclusion:** Upsell Rate absolute values are not comparable across cells.

| Comparison dimension | Comparable? | Reason |
|---|---|---|
| Cross-airline absolute values | No | Fare Family structure differs |
| Same airline, cross-route | No | Business vs seasonal demand structure differs |
| Same airline, same route, cross-market | No | Passenger demand profile differs (e.g., JED→CGK: Indonesian migrant workers vs Saudi local buyers — 27pp spread with same high void/24h coverage) |
| Same airline, same route, same market, over time | Most reliable | Control for structural variables; but adjust for seasonality |

**Practical implication:** The safest comparison is each cell versus itself over time. Cross-cell comparisons require explicit justification that structural differences are controlled.

**Pragmatic stance:** 100% precision is impossible. Framework output = directional priority hypothesis. Best guess → experiment → correct.

---

## Part 5: Priority Ordering Principle

**Current principle:** Higher in the funnel = higher priority. Without "the product," there's nothing to sell.

**Corrected principle (Session 3):**
> Higher in the funnel = higher priority — **only if the upper-layer problem is confirmed and quantified.** If the upper-layer problem is unconfirmed, lower-layer fixes (e.g., Display) should not be blocked.

**Two-step execution:**
1. **Diagnosis step:** Confirm whether a problem actually exists at each layer (don't assume)
2. **Prioritization step:** Among confirmed problems, order by funnel layer

**EY as counter-example:** EY had no confirmed Data Foundation or Supply gap, yet had a significant Display problem (void/24h). Strict "upper layer first" would have perpetually deferred the Display fix — the one that actually has ROI.

---

## Part 6: Two Candidate Needle Mover Types

| | Type 1: Volume Capture Gap | Type 2: Revenue Quality Gap |
|---|---|---|
| Reference case | EU Success Story | Void/24h Display Override |
| Problem type | Orders we should have captured but didn't | Orders captured but upsell suppressed |
| Detection signal | Internal volume vs external market trend divergence | Non-refundable ticket with free cancel label |
| Root cause layer | Supply (internal configuration error) | Display (label logic error) |
| Global coverage | Limited by external benchmark data availability | Fully internal, globally uniform |
| Requires airline-by-airline deep dive | Yes | No — same logic applies across all airlines |
| Fix mechanism | Case-by-case, varied root causes | Single display logic fix covers all airlines |
| Current quantification | No systematic global figure | 1.7M+ orders upper bound (40+ airlines) |
| Best execution level | Country Market teams (day-to-day) | Global Strategy team |

---

## Part 7: The EU Success Story — Methodology

**What happened:** Manager identified stagnation in EU country growth → compared against Skyscanner external data → found internal volume/market trend divergence on specific airline × route → manual investigation revealed missing round-trip fare add-on → root cause: Fare existed but was excluded from Fare Selection candidate pool → fix → volume recovered to market trend.

**Methodology core:**
> External market data as ground truth → identify internal volume vs market trend gap → trace funnel root cause

**Replicability constraints:**
- Skyscanner data only available in high-penetration markets (primarily Europe)
- IATA data has delay and coarse granularity; directional only
- Other markets lack equivalent external benchmark; rely on internal self-comparison or manual discovery

**Implication:** Type 1 opportunity detection is not uniformly replicable globally. More suited to market teams doing local deep dives than to Global Strategy systematic scanning.

---

## Part 8: Coverage Rate — Refined Interpretation

### Gambling fare & self-bundle: two-layer calculation

Coverage Rate can be calculated at two levels using the gambling flag in the database:

- **Supply-level coverage (incl. gambling):** Source fare is a Brand Fare → counted as covered, regardless of whether it ends up being used as a gambling fare or self-bundle. This reflects raw supply capability.
- **Display-level coverage (excl. gambling):** Only fares that are surfaced as genuine Brand Fares in the display path. The gap between these two numbers = gambling fare consumption of supply.

**Self-bundle note:** Baggage bundles are already included in the data. Flexibility bundles (converting non-refundable → refundable) are not yet included — Oliver Tang is integrating this. Until then, Flexibility Bundle and Void/24h display paths are assumed to be mutually exclusive (different display triggers), so the 1.7M Void/24h upper bound is not polluted by Flexibility Bundle cases.

### Commercial compliance and coverage interpretability

| Airline type | Market | Self-bundle allowed | Coverage Rate interpretability |
|---|---|---|---|
| AF/KL (strict everywhere) | All markets | No | Highest — low coverage = confirmed supply gap, no workaround |
| AA/DL/LH (home market strict) | US/DE home markets | No | High — same as above |
| AA/DL/LH | Non-home markets | Yes | Lower — self-bundle can mask true supply gap |
| Other airlines | All markets | Flexible | Varies |

**Implication:** AF/KL and AA/DL/LH home markets are the cleanest audit targets — Coverage Rate is most interpretable and low coverage has no self-bundle buffer, making gaps directly actionable.

---

## Part 9: Audit Workflow (Operational Reference)

Five-step process for a single airline audit. Steps 1–2 are data-driven; Step 3 requires manual spot-checking.

| Step | Name | What happens |
|---|---|---|
| 0 | Preparation | Download artnova data, build pivot tables, confirm debugging tool access |
| 1 | Brand Mapping Verification | Research airline.com (domestic + international ODs); identify fare attributes (baggage, change/cancel); cross-check with Trip coverage data for name/tier/count accuracy |
| 2 | Coverage Analysis | Build pivot by country/airport pair × tier × brand name; flag ODs with <80% coverage; prioritize near-0% or single-digit cases |
| 3 | Manual Validation | For flagged ODs: search airline.com + Trip app, compare attributes using debugging tool; classify as Type A (fixable supply gap) or Type B (airline restriction) |
| 4 | Knowledge Transfer | Document findings with screenshots; equip regional teams with data literacy + debugging tool access |

**Scraper role in this workflow:** Automates Step 3 by sampling airline.com at scale and calculating coverage rates per route and fare tier. Narrows manual effort from "all low-coverage ODs" to "ODs where airline.com coverage significantly exceeds Trip coverage."

**Current scraper status (as of 2026-06-17):**
- TK v1 (CDP mode): operational, historical data for IST→NAV/AYT/ASR/VAN
- TK v2 (Path B → A fallback): in development, OW + RT logic added, cookie banner fix in progress
- File location: `Flight Upsell/audit/TK/`
- Planned expansion: Japan, North America (US/CA), Mexico/South America

**Localization strategy:** Phase 1 = English (`en-int`) version only. Phase 2 = local language/currency for specific airlines where home market pricing is known to differ. Phase 2 is triggered by finding suspicious discrepancies, not done upfront.

---

## Part 10: Open Questions (as of 2026-06-17)

1. **Void/24h confirmed impact:** 1.7M is an upper bound. To convert to a leadership-grade number, need FBU display trigger logic: under what exact conditions does the label fire? This converts upper bound to confirmed exposure.

2. **Oliver Tang re-run:** `MZ_202606_quantification_cc` void/24h data is invalid (all zeros) due to snapshot filter issue (`DATE(d) = yesterday`). Needs re-run at original timestamp to restore source/subchannel dimension analysis.

3. **Fare Family design mapping:** No systematic mapping of 40+ airlines' Fare Family designs exists yet. This is the precondition to funnel diagnostics — without it, low upsell rate interpretation is ambiguous (product design ceiling vs execution gap).

4. **Ranking layer data:** Frontend impression data and backend Fare identity linkage not yet 100% confirmed. Ranking diagnostics partially actionable only; full operationalization pending.

5. **Display trigger hypotheses (parked):** Three open hypotheses for why void/24h label fires on some orders but not others — (1) booking channel GDS connection layer, (2) agency contractual/technical configuration, (3) locale/region regulatory requirements (EU consumer protection, US DOT 24h rule). None excludable without FBU Product Owner confirmation.
