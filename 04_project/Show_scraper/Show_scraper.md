---
name: Show Scraper
pillar: CreativityCuriosity
status: active
created: 2026-06-12
updated: 2026-07-24
description: Automated show discovery — wearepublic.nl scraper (Phase 1 complete); Phase 2 multi-source expansion
priority: P3
---

# Show Scraper

## Goal

Never miss a relevant dance/performance show in the Netherlands.

## Phase 1 — wearepublic.nl (Complete)

Python scraper tracking keywords (NDT, Introdans, Scapino, Club Guy, Carré) + 11 venues. Results to CSV, email delivery via GitHub Actions. See: `we-are-public-scraper-main/`

## Phase 2 — Multi-Source Expansion (Next)

Collect shows from additional internet sources beyond wearepublic.nl.

## Strategic Direction

- 识别额外来源 — 场地官网、其他聚合器、社交媒体渠道
- Phase 2 架构设计 — 多源统一输出格式
- 去重逻辑评估 — 同一演出在多源重复出现时的处理方案

---

## Decisions

<!-- Populate after coaching sessions -->

---

## Archived: Detailed Next Steps

*Previous next steps preserved for alignment verification.*

- [ ] ~~Identify additional sources~~ → 识别额外来源
- [ ] ~~Design Phase 2 scraper architecture~~ → Phase 2 架构设计
- [ ] ~~Evaluate deduplication logic~~ → 去重逻辑评估
## Key Files

- `we-are-public-scraper-main/main.py` — Phase 1 scraper

## Connections

Related Pages: [[Show-Discovery-System]], [[Dance-Creation]]
