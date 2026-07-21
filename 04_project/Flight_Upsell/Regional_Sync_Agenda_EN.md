---
title: "Regional Sync Agenda — Upsell Q3"
created: 2026-07-20
updated: 2026-07-21
purpose: Global PGM & market sync — project update and regional collaboration
---

# ABT & product update

**Fully rolled out:**
- **Quick Filter (baggage filter)** — Jul 2, App 100% rollout
    - Special thanks to Peam for the original idea and for helping us push this through with FBU — a great example of successful collaboration
- **Full Change/Refund Cost Display** — Jul 3, App 100% rollout; displays total change/refund cost (service fee + airline penalty + agency fee)

### Current Active ABTs

| ABT                                                                       | Launch Date | Details                                                                                   |
| ------------------------------------------------------------------------- | ----------- | ----------------------------------------------------------------------------------------- |
| C/F Fare Comparison Algorithm                                             | Jul 7       | Consistent with Y/W logic, extended to C/F cabin                                          |
| Personalized Ranking                                                      | Jul 9       | Fares ranked by purchase probability; currently at 16% traffic, expected to expand to 30% |
| Web Middle Page Vertical Redesign Phase 1                                 | Jul 11      | Vertical slide-out layout                                                                 |
| Compact Itinerary V2                                                      | Jul 22      | Allows customers who want to review flight details to do so; those who don't can skip it  |
| Upcoming Airline Compliance Implementation BA/VN, implemented LH/CX/LA/NZ | Varied      | https://trip.larkenterprise.com/wiki/G7XJw55KZiUTtKk5jL7cZE2inNf                          |

### Where we need your support
- Share your **ideas** and **inspiration** from competitors (via the request form or chat)
- **Airline / market-specific nuance:** flag issues if things don't work well with your region

---

# Audit update: 24h free cancellation display

## 1. Issue discovered during front-end audit

*(screenshot)*

**The problem:** The "free cancellation within 24 hours" label overrides the long-term refund policy, leading customers to believe they have cancellation protection — or making it difficult to distinguish between different fare tiers — and affecting the motivation to upgrade to a higher fare.

## 2. Understood root cause and quantified impact

There are two distinct backend policies involved:
- **24h free cancellation** (2C): customer can cancel free within 24 hours of booking
- **Void policy** (2B): allows agents to correct a booking error free within 24 hours

The two are mutually exclusive. The share varies significantly across airlines — void policies are more prevalent overall; 24h free cancellation is less common (EY / AA / DL, etc. are exceptions).

Trip displayed the void policy (when available) as a consumer USP **in the US, BR, and KR markets**, while the 24h free cancellation policy (when available) is displayed **across all markets**. In both cases, the middle page shows the same "free cancellation within 24 hours" label, **overriding the long-term refund policy**.

Through historical order analysis, this affects approximately **11% of orders globally** (Y class, 1-meta YTD):
- Found across major FSCs including EY, UA, DL, AA, BA, AC, and effectively affect all airlines and especially US/BR/KR markets

## 3. Data-driven FBU alignment; fix entering H2 roadmap

**FBU confirmed this is a poor experience for customers**. The fix will be discussed and taken into FBU's H2 roadmap. IBU will continue to follow up in H2 on both the ABT design and the resolution rollout.

We'll continue to drive upsell as strategy team — proactively identifying systemic blind spots, quantifying business impact, and driving high-impact issues through to resolution.