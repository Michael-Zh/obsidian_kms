---
name: Show Scraper
pillar: CreativityCuriosity
status: active
created: 2026-06-12
updated: 2026-06-12
description: Automated show discovery — wearepublic.nl scraper (Phase 1 complete); Phase 2 multi-source expansion
---

# Show Scraper

## Goal

Never miss a relevant dance/performance show in the Netherlands.

## Phase 1 — wearepublic.nl (Complete)

Python scraper tracking keywords (NDT, Introdans, Scapino, Club Guy, Carré) + 11 venues. Results to CSV, email delivery via GitHub Actions. See: `we-are-public-scraper-main/`

## Phase 2 — Multi-Source Expansion (Next)

Collect shows from additional internet sources beyond wearepublic.nl.

## Next Steps

- [ ] Identify additional sources for show discovery (venue direct sites, other aggregators, social channels)
- [ ] Design Phase 2 scraper architecture — unified output format across sources
- [ ] Evaluate deduplication logic when same show appears in multiple sources

## Key Files

- `we-are-public-scraper-main/main.py` — Phase 1 scraper

## Connections

Related Pages: [[Show-Discovery-System]], [[Dance-Creation]]
