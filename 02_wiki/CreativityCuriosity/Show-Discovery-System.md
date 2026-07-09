---
name: Show Discovery System
pillar: CreativityCuriosity
type: practice
status: active
created: 2026-06-12
updated: 2026-06-12
description: Automated scraper for discovering dance/performance shows in Amsterdam and Netherlands — keywords + venues tracked on wearepublic.nl
tags:
  - CreativityCuriosity
  - LifeManagement
---

# [[Show-Discovery-System]]

## Purpose

Automated discovery of dance and performance shows in the Netherlands. Solves the problem of manually checking multiple theater websites and missing relevant performances.

## How It Works

- Python scraper targeting [wearepublic.nl](https://www.wearepublic.nl) (Dutch performing arts aggregator)
- Tracks: keywords (NDT, Introdans, Scapino, Club Guy, Carré) + 11 specific venues (ITA, Amare, Bellevue, Frascati, Korzo, Schuur, Stadsschouwburg Haarlem, etc.)
- Outputs to CSV with title, date, artists, venue, disciplines, URL
- Deduplicates against already-seen shows
- Supports blockout days (exclude dates when unavailable)
- Results emailed via SMTP on schedule via GitHub Actions
(ref: [[Show_scraper]])

## Venues Tracked

Amsterdam: ITA, Amare, Bellevue, Frascati, Korzo
Other NL: Schuur (Haarlem), Stadsschouwburg Haarlem, Carré, Theater ins Blau
Den Haag: Korzo (also here)

## Technical Notes

- Uses ScraperAPI for JavaScript-rendered pages (optional)
- Dutch date parsing (vandaag/morgen + month abbreviations) → ISO 8601
- Concurrent scraping with ThreadPoolExecutor
- CSV persistence: adds new shows, tracks update dates

## Connections

Related Pages: [[Dance-Creation]], [[Aesthetic-Intelligence]], [[Travel-Interests]]
Related Projects: [[Show_scraper]]
