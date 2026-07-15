---
name: "wiki-lint"
description: "Periodic health check of the KMS wiki — find contradictions, orphan pages, stale content, missing types, broken links, and write a lint queue for wiki-coach to process."
---

# Wiki Lint Skill

Periodic health check of the KMS wiki. Run this monthly (or when the wiki feels stale) to surface issues, then hand off a lint queue for wiki-coach to fix on the next run.

**Output:** Health report + structured `_lint_queue.md` file listing issues for wiki-coach to resolve.

---

## KMS Paths

```
/KMS
  /00_system/_POS.md, _priority.md
  /00_system/kms_search.py         ← CLI for bulk metadata discovery
  /01_raw/_watchlist.md
  /02_wiki/lint/_lint_queue.md       ← lint queue (read/write)
  /02_wiki/lint/wiki_lint_YYYYMMDD.md ← health reports
  /02_wiki/[Pillar]/_[Pillar]_Index.md, [Page_Name].md
  /04_project/_in_case_you_are_bored.md
  /04_project/[ProjectName]/[ProjectName].md
```

**Vault path:** `/Users/michael_zhang/Library/Mobile Documents/iCloud~md~obsidian/Documents/KMS`

---

## The 8 Pillars

| Folder Name | Display Name |
|-------------|--------------|
| Relationships | Relationships |
| MindMentalHealth | Mind & Mental Health |
| Career | Career |
| PhysicalHealth | Physical Health |
| LifeManagement | Life Management |
| Finance | Finance |
| CreativityCuriosity | Creativity & Curiosity |
| AdminHome | Admin & Home |
| Travel | Travel |

---

## Page Types

Each wiki page should have a `type` field in its YAML frontmatter:

| Type | What it captures |
|------|-----------------|
| **concept** | Abstract framework, philosophy, pattern |
| **practice** | Active protocol, routine, habit |
| **topic** | Domain being explored, not yet settled |
| **synthesis** | Generated analysis or comparison filed back into wiki |
| **entity** | Person, book, or named artifact — index of what you learned from it, with links to relevant topic pages |

---

## CLI Reference

> For the full obsidian CLI command reference, syntax, and flags — invoke the `/obsidian-cli` skill. The patterns below are KMS-specific usage only.

Use the **obsidian CLI** for targeted lookups and the **kms_search.py** for bulk metadata. Never load file content until needed.

```bash
KMS="/Users/michael_zhang/Library/Mobile Documents/iCloud~md~obsidian/Documents/KMS"

# --- obsidian CLI (preferred for per-file and structural queries) ---

# All orphan pages in vault (no inbound links) — replaces backlinks loop:
obsidian vault=KMS orphans

# All unresolved (broken) wikilinks — replaces per-page links+verify loop:
obsidian vault=KMS unresolved format=json

# Backlinks to a specific page:
obsidian vault=KMS backlinks file="Page_Name" format=json

# All wikilinks in a page:
obsidian vault=KMS links file="Page_Name" format=json

# Read a page (YAML + body):
obsidian vault=KMS read file="Page_Name"

# YAML properties only for a page:
obsidian vault=KMS properties file="Page_Name" format=json

# --- kms_search.py (preferred for bulk metadata across all wiki pages) ---

# List all pages with metadata — no file content (Checks 1, 2, 3, 5, 8):
python3 "$KMS/00_system/kms_search.py" list --json

# List pages in a specific pillar:
python3 "$KMS/00_system/kms_search.py" list --pillar Career --json

# Get YAML-only for a specific page:
python3 "$KMS/00_system/kms_search.py" meta PAGE_NAME

# List all active projects with YAML headers (Check 6: missing project links):
python3 "$KMS/00_system/kms_search.py" projects
```

---

## 9 Lint Checks

### Check 1: Missing `type` field
Run `kms_search.py list --json` → filter for pages where `type == ""`. Suggest type based on page name.
- **Action:** Add to lint queue with suggested type

### Check 2: Orphan pages
Run `obsidian vault=KMS orphans` → filter results to `02_wiki/` files only (exclude system/output/project files).
- **Action:** Add to lint queue — either link them or flag for deletion
- **Why obsidian CLI:** Returns all orphans in one call; no per-page backlink loop needed.

### Check 3: Index coverage
Run `kms_search.py list --pillar PILLAR --json` for each pillar → compare against entries in `_[Pillar]_Index.md`.
- **Action:** Add missing pages to lint queue for index update

### Check 4: Broken links
Run `obsidian vault=KMS unresolved format=json` → review each unresolved link and its source file.
- **Action:** Add to lint queue with the source file and broken target
- **Why obsidian CLI:** Returns all broken links across the vault in one call; no per-page loop needed.

### Check 5: Stale pages
Run `kms_search.py list --json` → filter for pages where `updated` is 90+ days ago and `status == "active"`.
- **Action:** Flag in lint queue for review — confirm still relevant or archive

### Check 6: Missing project links
Run `kms_search.py projects` → for each project, run `obsidian vault=KMS backlinks file=PROJECT_NAME format=json` to check if any wiki pages reference it.
- **Action:** Add to lint queue — link from appropriate pillar page

### Check 7: Contradictions (best-effort)
Read pairs of related pages (same pillar, connected by links) and check for conflicting claims about the same topic.
- **Action:** Flag specific contradictions in lint queue for human review + resolution

### Check 8: Missing YAML fields
From `kms_search.py list --json` output, check each entry for: `name`, `pillar`, `type`, `status`, `created`, `updated`, `description`. Then read files with missing fields to confirm.
- **Action:** List missing fields per page in lint queue

### Check 9: Watchlist capture gaps
Run `obsidian vault=KMS read file="_watchlist"` → scan for rows with missing `Note/context` or `Type = Unknown`.
- **Action:** Flag in lint queue for enrichment on next wiki-coach run

### Check 10: Page density
Run `kms_search.py list --json` → for each page, read and check word count and count of `(new)` prefixes. Flag pages >800 words or with 5+ `(new)` prefixes as candidates for splitting or sub-page creation.
- **Action:** Add to lint queue with word count and suggestion (split / archive old sections / promote to synthesis)

### Check 11: Entity gaps
Scan all wiki pages for people and books referenced 3+ times across pages. Check if each referenced entity has its own entity-type wiki page.
- **Action:** Add to lint queue each person/book referenced ≥3 times without a dedicated entity page — propose page name and pillar

---

## Execution Order

1. Run `kms_search.py list --json` → cache all page metadata (used for Checks 1, 3, 5, 8, 10)
2. Run `kms_search.py projects` → cache all project metadata (used for Check 6)
3. Run `obsidian vault=KMS orphans` → filter to `02_wiki/` pages (Check 2)
4. Run `obsidian vault=KMS unresolved format=json` → all broken links at once (Check 4)
5. Run Checks 1, 3, 5, 8 from cached metadata (structural — fast, no extra reads)
6. Run Check 6: for each project not found in any page's links output, run `obsidian vault=KMS backlinks` to confirm
7. Run Checks 7, 9: requires reading page pairs and `_watchlist.md` (content — slower)
8. Run Check 10: read pages flagged as large by metadata; count words and `(new)` prefixes
9. Run Check 11: grep all wiki pages for person/book references; cross-check against existing entity pages
10. Write `_lint_queue.md`
11. Write health report to `/02_wiki/lint/wiki_lint_YYYYMMDD.md`

---

## Lint Queue Format

Write to `/02_wiki/lint/_lint_queue.md` — **overwrite** on each lint run (not append). This is the to-do list for the next wiki-coach run.

```markdown
# Lint Queue
_Generated: YYYY-MM-DD_
_Clear this file after wiki-coach processes all items._

## Missing Type Fields
- [ ] `[[Page_Name]]` (pillar: Career) — suggested type: `topic`
- [ ] `[[Another_Page]]` (pillar: Finance) — suggested type: `practice`

## Orphan Pages
- [ ] `[[Page_Name]]` — no inbound links; consider linking from `[[Pillar_Index]]`

## Index Gaps
- [ ] Add `[[Page_Name]]` to `LifeManagement` index

## Broken Links
- [ ] `[[Source_Page]]` references `[[Missing_Page]]` — page does not exist

## Stale Pages (90+ days, status: active)
- [ ] `[[Old_Page]]` — last updated 2025-11-01; confirm still relevant

## Missing Project Links
- [ ] Project `[[Project_X]]` not referenced in any wiki page — link from `[[Relevant_Page]]`

## Contradictions
- [ ] `[[Page_A]]` vs `[[Page_B]]` — conflicting claims about [topic]; human review needed

## Missing YAML Fields
- [ ] `[[Page_Name]]` — missing: `type`, `description`

## Watchlist Capture Gaps
- [ ] Row 42: Type=Unknown, no context — enrich during next ingest

## Page Density
- [ ] `[[Dense_Page]]` — 1200 words, 6 `(new)` prefixes — candidate for splitting or archiving old sections

## Entity Gaps
- [ ] "James Clear" referenced 5 times — no entity page; suggested: `[[James_Clear]]` in CreativityCuriosity
```

---

## Health Report Format

Write to `/02_wiki/lint/wiki_lint_YYYYMMDD.md`:

```markdown
---
date: "YYYY-MM-DD"
type: "wiki_lint"
---

# Wiki Lint Report — YYYY-MM-DD

## Summary

| Check | Issues Found | Severity |
|-------|-------------|----------|
| Missing type fields | N | Medium |
| Orphan pages | N | Low |
| Index gaps | N | Medium |
| Broken links | N | High |
| Stale pages | N | Low |
| Missing project links | N | Medium |
| Contradictions | N | High |
| Missing YAML fields | N | Medium |
| Watchlist capture gaps | N | Low |
| Page density | N | Medium |
| Entity gaps | N | Medium |

**Total issues:** N
**Lint queue written:** `[[_lint_queue]]`

## Highlights

[2-3 most important findings that need attention]

## By Pillar

### Career
[Issues found in Career pillar]

### LifeManagement
[Issues found in LifeManagement pillar]

[... repeat for each affected pillar ...]

## Recommended Next Actions

1. Run `/wiki-coach-kms-cli` — it will pick up `_lint_queue.md` automatically
2. [Any issues requiring human decision before wiki-coach can fix them]
3. [Contradictions requiring your judgment]
```

---

## Key Rules

1. **Never modify wiki files** — lint is read-only; all fixes go to `_lint_queue.md`
2. **Overwrite `_lint_queue.md`** each run (don't append to stale issues)
3. **Flag but don't decide** contradictions — write them to queue for human review
4. **Use obsidian CLI** for orphans and broken links (single call beats per-page loops)
5. **Use `kms_search.py`** for bulk metadata across all wiki pages
6. **Simple links only:** `[[name]]` format in all output files
