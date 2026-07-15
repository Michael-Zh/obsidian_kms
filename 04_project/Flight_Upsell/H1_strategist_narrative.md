---
created: 2026-06-21
updated: 2026-06-21
status: draft — to be revised after quantification complete
purpose: H1 review strategist narrative; update as 24h/void quantification lands
---

# H1 Strategist Narrative — Flight Upsell

_Draft. Revisit when: (1) 24h/void quantification complete, (2) before H1 review conversation with J._

---

## The Strategic Contribution in One Sentence

I designed the diagnostic framework that turned a vague "coverage is low" observation into a structured, quantifiable opportunity hunt — and identified the 24h free cancellation / void display gap as the priority candidate for needle-mover validation.

---

## What I Actually Did (Strategist Frame)

### 1. I structured the problem before we could measure it

The starting condition was: brand fare coverage rates are low on certain routes. That's a symptom, not a diagnosis. The work was building the analytical logic that could tell the difference between "airline doesn't offer it" (expected, nothing to fix) and "platform fails to retrieve or display it" (a gap worth fixing).

The framework I developed operates in three layers:
- **Attributes combination delta** — where exactly does coverage drop? Identifying the specific attribute combinations that under-perform narrows the search space from thousands of routes to a tractable set of candidates.
- **Fare Family feasibility vs. attractiveness** — separating "can we fix this?" from "is it worth fixing?" before committing manual verification effort. This is the prioritization gate.
- **Observed Rate + funnel decomposition** — distinguishing pre-comparison coverage loss (supplier retrieval failure) from post-comparison loss (ranking/display filtering). Each has a different fix.

This structure is what made targeted manual checking possible. Without it, we'd be doing random sampling on a problem that's inherently fragmented (C1: Route Scatter, C2: Yield Management Variable — see `upsell_diagnostic_framework.md`).

### 2. The 24h / void finding came from running the framework

J's manual check of the 24h free cancellation and void display case happened within the framework — the framework is what surfaced it as a priority candidate to check. That's the direction of causality worth naming at review time.

The finding: there's a potential gap between what airlines display (24h free cancel as a standalone policy) and what Trip.com shows (void policy as a substitute). If Trip.com is not surfacing the correct fare type in the right context, this is a platform-side retrieval/display issue — not an airline supply issue. That makes it actionable.

### 3. I'm developing the independent judgment J is looking for

J's standard is clear: don't hand him data and ask him to judge it — arrive with a hypothesis, evidence for its size, and a validation path. The framework is the beginning of that operating mode. What's still developing: the quantification muscle (how big is this opportunity in absolute terms?) and the communication habit (open with the hypothesis, not the methodology).

---

## What's Still In Progress

- **Quantification of 24h/void gap** — in progress with J. Target: a number that can be named in the review. Even a rough estimate (order of magnitude) is better than "we're still working on it."
- **Attributes combination delta analysis** — framework is built; full output pending BQ/GCP session.
- **Formal presentation** — the three-layer framework has been discussed in J catchups but not formally presented or circulated. Before the review, consider whether there's a natural moment to send a summary to J or the broader team.

---

## Two Questions to Resolve Before H1 Review

1. **What's the number?** The 24h/void opportunity — what's the estimated revenue or coverage impact? Rough order of magnitude is enough for the narrative. Without a number, the needle-mover claim can't land.

2. **Where is your name?** Has the diagnostic framework been put in writing anywhere that J or stakeholders have seen? If not, the review itself is the moment to name it explicitly: "the analytical approach I designed for this."

---

## Narrative Version for Verbal Use (H1 Review)

> "My H1 contribution on upsell was building the analytical framework that made this problem tractable. Brand fare coverage is hard to diagnose because the causes are structurally different — supply gaps, retrieval failures, and display errors all look similar in aggregate data. I designed a three-layer approach that separates them: attributes delta to locate the anomaly, feasibility vs. attractiveness to prioritize, and funnel decomposition to find the specific break point.
>
> That framework is what surfaced the 24h free cancellation / void case as a priority candidate. We're currently quantifying the size of that gap — early indication is [X]. If confirmed, it's a needle-mover candidate at global scale.
>
> What I'm building toward is the full strategist loop: hypothesis → evidence → size estimate → validation plan. I'm not there consistently yet, but I know what the standard is and I'm closing the gap."

_(Fill in [X] before the review.)_
