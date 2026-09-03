---
name: "Plant_rearrangement"
project_id: "pj0014"
status: "active"
pillar: "AdminHome"
parent_project: "Studio_makeover"
current_focus: "Phase 2: 介壳虫检查 + Alocasia 抢救（工作日晚间 10 分钟）；换盆/修剪/分区需周末半天（9/19–20）"
created: "2026-06-01"
updated: "2026-09-03"
priority: "P2"
execution_state: main
tags: [AdminHome]
---

# Plant Rearrangement — Indoor Garden Overhaul

> **Sub-project of [[Studio_makeover]]**

## Overview

Rescue and reorganize the indoor plant collection. Two plant groups, three phases ordered by urgency: stabilize tropicals → rescue succulents → relocate and establish routine.

---

## Context & Background

- **Trigger:** Yellowing Monstera leaves and general plant neglect during travel/training focus
- **Key Assumptions:** Root issues are primary cause (dense soil, root-bound); succulents can wait
- **Constraints:** Limited windows with good light; travel schedule interrupts care
- **Prior Work:** Master Indoor Gardening Playbook written; Sprint execution plan active

---

## Objectives & Goals

- **Goal 1:** Stabilize struggling tropicals (Monstera, Ficus, Alocasia)
- **Goal 2:** Repot succulents with proper soil; eliminate mealybugs
- **Goal 3:** Establish sustainable watering/maintenance routine compatible with travel schedule

---

## Execution Plan

### Phase 1: Tropical Triage & Root Audit ✅ (Mostly Done)

- [x] **Monstera Root Check & Repot** — Massaged out old suffocating dirt; repotted into Universal Chunky Mix
- [x] **Prune Dead Weight** — Cut entirely yellow bottom leaf, dead black leaf stem, trimmed crispy variegated edges
- [x] **Ficus Root Rescue** — Root ball loosened; repotted into Universal Chunky Mix
- [ ] **Alocasia Rescue (URGENT)** — Unpot, massage away old soil, check/snip black/mushy roots, repot in Chunky Mix; do NOT plant too deep (corm top must sit at or just above soil line)

### Phase 2: Succulent Rescue & Pest Control (Current)

- [ ] **Snake Plant Repotting** — Desert Dwellers Mix (2–3 parts cactus soil + 1 part perlite); wait until roots fully dry before watering
- [ ] **Succulent Mealybug Check (URGENT)** — Move any plant with white cotton fuzz 2m away; Q-tip test with 70% alcohol (rust/brown = mealybugs); dab all bugs with alcohol

### Phase 3: Relocation & Reset (Next Week)

- [ ] **Succulent Chop** — Behead leggy/stretched rosettes, callous 3 days, plant in dry soil
- [ ] **Light Zone Placement** — Move all plants to designated zones (see Strategy below)

---

## Plant Groups & Diagnosed Issues

### Group A: Tropicals (Monstera, Ficus 'Tineke', Alocasia)

| Issue | Symptom | Fix |
|---|---|---|
| Overwatering / root suffocation | Yellow leaves, brown patches with yellow halos, soil fungus | Chunky Mix + wet-to-dry watering cycles |
| No climbing support | Monstera tilting, top-heavy | Bamboo stake / moss pole |
| Browning variegation | White patches turn brown/crispy | Stable watering + bright indirect light (no direct afternoon sun) |

### Group B: Desert Dwellers (Succulents & Snake Plants)

| Issue | Symptom | Fix |
|---|---|---|
| Mealybugs | White cotton fuzz in crevices | Alcohol Strike (Q-tip dab) |
| Etiolation | Stretching/legginess | Succulent Chop + more direct sunlight |

---

## Long-Term Strategy

### Light Zoning

- **Zone 1 — Direct Sun** (South/West window): All succulents & snake plants
- **Zone 2 — Bright Indirect** (East window or pulled back from South/West): Monstera & Ficus; keep variegated Monstera out of direct afternoon sun

### Watering System

- **Tropicals (Top-2-Inches Rule):** Water when top 2–3 inches are completely dry; always empty cache pot 30 min after watering
- **Succulents (Soak & Dry):** Wait until 100% bone dry all the way down; drench, drain, then ignore for weeks

### Preventative Maintenance

- Monthly lukewarm leaf showers for tropicals (dust + pest deterrent)
- 15-second weekly check: inspect leaf undersides and stem joints every time you water

---

## Soil Mix Recipes

**Universal Chunky Mix (Tropicals — 2:1:1)**
- 2 parts standard potting soil
- 1 part bark chips
- 1 part perlite

**Desert Dwellers Mix (Succulents & Snake Plants — 2–3:1)**
- 2–3 parts cactus soil
- 1 part perlite
- No bark chunks

**Repotting Steps:**
1. Wash nursery pot with hot soapy water
2. Add 1–2 inch base layer of mix (don't pack)
3. Place stake/moss pole first (bottom of pot)
4. Position plant — angle root ball to correct tilt; root flare at/just below soil surface; never bury main stem
5. Backfill sides with mix
6. Tap outside of pot gently to settle (don't press)
7. Tie main stem (not leaf stems) to stake; water thoroughly until it runs from drainage holes

---

## Decisions

- Repotting sequence: Tropicals first (most urgent), succulents second
- Stake placement: insert before backfilling to avoid root damage
- **2026-09-03:** 文件夹从 `04_project/Plant_rearrangement/` 移入 `04_project/Studio_makeover/Plant_rearrangement/` — 它本来就是 [[Studio_Makeover]] 的 sub-project，结构上跟 [[Meal_prep_routine]] 在 Training 之下一致。wikilink 不受影响（Obsidian 按文件名解析），`kms_search.py` 与 `sync-context.py` 都按 `project_id` 递归探测，也不受影响。
- **2026-09-03:** 本项目不写 `## Strategic Direction` — task 由 app backlog 承载。此前 app 的 re-sync cascade 会把「不在 Strategic Direction 里」的 backlog 项静默标 done，对没有该 section 的项目（本项目）尤其致命；已在 app Session 54 修复（改为只有 KMS 来源的行才可被 KMS 自动解决）。

---

## Connections

**Parent Pillar:** [[AdminHome]]

**Related References:**
- [[The Master Indoor Gardening Playbook]] — Comprehensive strategy document
