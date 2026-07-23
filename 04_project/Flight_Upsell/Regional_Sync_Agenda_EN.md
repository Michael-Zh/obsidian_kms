---
title: "Flight Upsell Regional Sync 20260724 v2"
source: "https://trip.sg.larkenterprise.com/docx/VY68djwUlox1fxxxBXjlAsQigqf"
synced: 2026-07-23
---

# H1 highlights & H2 plan

## Strategic direction and hypothesis

- The H1 core question was, **do we have the fares to sell (supply coverage) or not.** With the help of regional teams, our brand fare audit shows **supply is not bad** (still room to improve) and **not the major issue**.
- Another hypothesis was that **we have fares but we don't sell because they are a) filtered out by fare selection algorithm** and/or **b) ranked in low positions and hence lack of exposure**. Based on that, FBU rolled out the **value-based fare selection algorithm** and is testing **personalized ranking based on purchase probability**.
- Lastly, based on recent SG/UK user research results, users are less motivated to upgrade because they believe **buying the cheapest fare + add-ons is cheaper than buying fares bundling these services** on Trip, which leads to H2's focus on strengthening **the expression of value proposition**.

## H2 Upsell-specific Objectives by priorities

**🎯 High Priority O1 (display and ranking - frontend/AGG):** Enable users to "grasp the value at a glance and make the upsell decision with peace of mind" on the middle page

**🎯 Medium-High Priority O2 (fare selection - AGG):** Shift from "listing everything" to "active scenario-based fare selection matching correspondent upsell motivation"

**🎯 Medium-priority O3 (data foundation - backend):** Complete the brand fare infrastructure development + Airline perspective upsell measurement, and enable the automated feedback loop of "coverage measurement → diagnosis → optimization"

**🎯 [Pending] Medium Priority O4 (Price Competitiveness/RM):** Price Competitiveness — Moving from definition and evaluation to pilot verification, exploring scalable price levers

---

# ABT & Product Highlights

We are highlighting a few H1 new features/H2 ongoing works, especially the ones aligned with H2 objectives: **stronger and clearer value proposition**

## Change/Refund Policy Display

### Issue 1: (almost) Identical attributes but priced differently

- Two fares have the same baggage allowance and flexibility policy, only 1 air mile and 4 trip coins difference, which is **not enough to justify the +9% price premium** to upgrade to the 2nd fare
- Root cause: the underlying **refundable tax** is different

**[Rolled out feature] Display Full Flexibility Cost**

- Roll out to 100% **APP** traffic on Jul 3
- Decision based on **no significant negative impact** on CR and Middle Page to Fill-in Page CTR, and Business/First Class fare selection algorithm ABT depends on this feature

---

### Issue 2: 24h free cancellation overwrites long-term policy

- On the middle page, a "free cancellation within 24 hours" label is shown on fares that are actually non-refundable after that window — overriding the long-term refund policy. This misleads customers and hinders the motivation to upgrade to a higher fare.
- **Quantification**: Affects ~11% of orders globally (Y class, 1-meta YTD), across major FSCs, such as EY, UA, DL, AA, BA, AC, etc.
- FBU confirmed this is a poor customer experience and the fix is expected in the H2 roadmap.

#### Appendix: 24h free cancellation technical details

There are two distinct backend policies involved:

- **24h free cancellation** (2C): customers can cancel free within 24 hours of booking
- **Void policy** (2B): allows agents to correct a booking error free within 24 hours

The two are mutually exclusive. The share varies significantly across airlines — void policies are more prevalent overall; 24h free cancellation is less common (EY / AA / DL, etc. are exceptions).

Trip displayed the void policy (when available) as a consumer USP **in the US, BR, and KR markets**, while the 24h free cancellation policy (when available) is displayed **across all markets**. In both cases, the middle page shows the same "free cancellation within 24 hours" label, **overriding the long-term refund policy**.

---

## Quick Filter (baggage filter)

- Roll out to 100% **APP** traffic on Jul 2
- Decision based on Version E (filter always visible) **upsell uplift 1.07%**

### Current ABTs

(see Feishu doc for live spreadsheet)

### Upcoming ABTs

(see Feishu doc for live spreadsheet)

Note for airline compliance: FBU will conduct ABT to evaluate the business impact of these compliance requests. Ultimately, BD will decide if they will roll it out based on the impact (e.g. revenue/profit or CR drops drastically.)

---

# A BIG THANK YOU

**Success stories**

- **Peam** (TH) shared the baggage filtering idea and similar design now rolled out with a successful ABT result recently.
- **Cristina** (EU) helped identify missing high tier fares among BA. Now BA is expected to ABT the effect of retaining these fares.
- **Saja** (MENA) shared the idea of adding rationale to explain the new personalized ranking, now included in the H2 roadmap.
- All participating regions help us with the brand fare audit.

**Where we need your support**

- We will do better to bring the front-end features for feedback in the **mock-up stage**. Please speak up with your **feedback**!
- Share your **ideas** and **inspiration** from competitors (especially the ones aligned with H2 objectives)
- We'll also do better to **circle back** the response from FBU for your requests
