---
name: "wiki-coach-kms-cli"
description: "Process raw inputs to update wiki AND generate priority-aware coaching in parallel"
---

# Wiki-Coach KMS Skill

Two parallel processes from one input:
- **Wiki Process:** Check lint queue → Extract themes → Update pages/indexes → Log changes → Collect signals
- **Coaching Process:** Filter through priorities → Generate coaching session → Collect signals
- **Project Ideas:** Project-specific ideas → `[ProjectName].md ## Next Steps`; exploratory/new ideas → `_in_case_you_are_bored.md`
- **Articles:** Scan YAML-only first; only load full file if `annotation:` property is present

---

## The 8 Pillars (use the name in [] for pillar folder name and pillar tags)

- **Relationships** — Social health and core connections [Relationships]
- **Mind & Mental Health** — Internal world, reflection, and therapy [MindMentalHealth]
- **Career** — Professional output and skill development [Career]
- **Physical Health** — Sleep, fitness, diet [PhysicalHealth]
- **Life Management** — Systems and meta-work (including KMS itself) [LifeManagement]
- **Finance** — Wealth management and resource allocation [Finance]
- **Creativity & Curiosity** — Exploration and hobbies [CreativityCuriosity]
- **Admin & Home** — Physical environment and bureaucracy [AdminHome]
- **Travel** — Travel ideas and planning [Travel]

---

## Input Folders

**Primary inbox:** `/01_raw/` — contains `_daily_note/` (daily notes), `_journal/` (written reflections, non-daily), and loose files
**Articles:** `/01_raw/文章/` and `/01_raw/YT/` — YAML scanned for `annotation:` property; full file only loaded if annotated
**Watchlist inbox:** `/01_raw/_watchlist_inbox.md` — staged entries from Apple Shortcut, sorted into `_watchlist.md` each run
**Read-only:** Files never modified after processing.

---

## Article Annotation Format

Articles are edited directly in Obsidian. Add `annotation:` to the YAML frontmatter:

```yaml
---
source: 小红书
url: https://...
saved: "2026-05-21 09:56:45"
id: uuid-string
author: AuthorName
annotation: |
  What struck you: [your answer]
  Why now: [your answer]
  Action/contradiction: [your answer]
---
```

Or for full article synthesis:
```yaml
annotation: full article
```

Articles without `annotation:` are skipped entirely — no logging, no pending status.

---

## Page Types

Each wiki page has a `type` field in YAML. Generate content appropriate to the type:

| Type | What it captures | How to synthesize |
|------|-----------------|-------------------|
| **concept** | Abstract framework, philosophy, pattern (e.g., `Identity-Based-Life-Philosophy`) | Emphasize connections to other ideas, tensions, evolution of thinking over time |
| **practice** | Active protocol, routine, habit (e.g., `Sleep-Optimization-Routine`) | Emphasize what's working, evidence, current protocol, experiment results |
| **topic** | Domain being explored, not yet settled (e.g., `Portfolio-Career-Design`) | Track what you know, what you're learning, open questions, next steps |
| **synthesis** | Generated analysis or comparison filed back into wiki (e.g., `Iyengar vs Gyrokinesis`) | Preserve the analysis structure; update with new evidence as it arrives |
| **entity** | Person, book, or named artifact (e.g., `James_Clear`, `Atomic_Habits`) | Index of what you learned from it, with links to relevant topic/concept pages; structured as key takeaways + internal links |

---

## CLI Reference

> For the full obsidian CLI command reference, syntax, and flags — invoke the `/obsidian-cli` skill. The patterns below are KMS-specific usage only.

Use the **obsidian CLI** for targeted reads, writes, and property edits. Use **kms_search.py** for bulk metadata. Never load file content speculatively.

```bash
KMS="/Users/michael_zhang/Library/Mobile Documents/iCloud~md~obsidian/Documents/KMS"

# --- obsidian CLI: reads ---

# Read a page (YAML + body):
obsidian vault=KMS read file="Page_Name"

# YAML properties only for a page:
obsidian vault=KMS properties file="Page_Name" format=json

# Read a single YAML property:
obsidian vault=KMS property:read name=type file="Page_Name"

# All wikilinks in a page:
obsidian vault=KMS links file="Page_Name" format=json

# All pages that link to a page (backlinks):
obsidian vault=KMS backlinks file="Page_Name" format=json

# --- obsidian CLI: writes (replaces read+edit+write cycles) ---

# Set a single YAML property (add missing fields, fix type, update date):
obsidian vault=KMS property:set name=type value=topic file="Page_Name"
obsidian vault=KMS property:set name=updated value="2026-06-06" file="Page_Name"

# Append to a file (logs, signal files, processed_log, project Next Steps):
obsidian vault=KMS append path="02_wiki/_log.md" content="[new entry]"

# Prepend to a file (reverse-chronological logs):
obsidian vault=KMS prepend path="02_wiki/_log.md" content="[new entry]"

# Create a new page:
obsidian vault=KMS create path="02_wiki/Career/New-Page.md" content="[full content]"

# --- kms_search.py: bulk metadata (no file content loaded) ---

# Find pages matching a keyword:
python3 "$KMS/00_system/kms_search.py" search "theme_keyword" --pillar PILLAR --limit 5

# List all pages with metadata:
python3 "$KMS/00_system/kms_search.py" list [--pillar PILLAR] --json

# Get YAML-only for one page:
python3 "$KMS/00_system/kms_search.py" meta PAGE_NAME

# List all active projects:
python3 "$KMS/00_system/kms_search.py" projects
```

---

## Wiki Processing (12 Steps)

### 1. Load New Input Files + Check Lint Queue
Check `_processed_log.md`. Load only unprocessed `.md` files from `01_raw/_daily_note/` and `01_raw/_journal/`.

**Quick highlights (elevated priority):**
Check `01_raw/_journal/` for any `quick_highlights_*.md` files not yet in `_processed_log.md`. Files are named `quick_highlights_[ProjectName]_YYYYMMDD.md` (or `quick_highlights_general_YYYYMMDD.md`). Load these first — they are pre-filtered, high-relevance entries already connected to source files and projects. Each highlight entry contains:
- `source: [[FILENAME]]` — the originating article/clip; do not re-read the source unless needed for synthesis depth
- `connected_pages:` — already mapped; use as merge targets
- The YAML `project:` field identifies which project's context to use for synthesis
- Implications + actions — treat as the annotation equivalent; no re-extraction needed

**Article scanning (YAML only — no full file reads yet):**
Scan `01_raw/文章/` and `01_raw/YT/` recursively. For each `.md` file, read the annotation property only:

**Coaching files (wiki synthesis — new):**
Scan `01_raw/coaching/` for any `coaching_YYYYMMDD.md` files not yet in `_processed_log.md`. These contain past discussions, decisions, and reflections that should be synthesized into the wiki — treat them as high-value input equivalent to annotated articles. The full file is always loaded (no annotation gate). Process decisions and insights into relevant wiki pages; route project-level conclusions to `[ProjectName].md ## Next Steps` or `_in_case_you_are_bored.md` as appropriate.
```bash
obsidian vault=KMS property:read name=annotation file="FILENAME"
```
- If `annotation:` is **absent or null/empty** → skip entirely, do nothing
- If `annotation:` has a **non-empty value** → add to processing list; full file will be loaded in Step 2 if needed
- Check `_processed_log.md` to exclude already-processed articles (match by filename)

Note: The `annotation:` property is now always included in the YAML template by default (may be null). Use `property:read` rather than checking for property existence — null/empty = skip, any real value = process.

**Lint queue check:** If `/02_wiki/lint/_lint_queue.md` exists and has unchecked items (`- [ ]`), load it. Process lint queue items alongside normal ingest. After processing, check off completed items (`- [x]`).

**Watchlist inbox sort:** Check if `/01_raw/_watchlist_inbox.md` exists and has content. If so:
- Read each line (format: `date | category | name | note | url | type | status`)
- Read `_watchlist.md`, insert each entry as a new table row under the matching `## Category` section, then write the file back
- After all entries are sorted, clear `_watchlist_inbox.md` (overwrite with empty string)
- If `_watchlist_inbox.md` doesn't exist or is empty, skip silently

- **Missing type fields** → `obsidian vault=KMS property:set name=type value=SUGGESTED file="Page_Name"`
- **Orphan pages** → Add link from suggested index or related page (read+edit index file)
- **Index gaps** → Add page to pillar index (read+edit index file)
- **Broken links** → Remove or fix the broken `[[link]]` (read+edit source page)
- **Stale pages** → `obsidian vault=KMS property:set name=status value=archived file="Page_Name"` or update `updated:` date
- **Missing project links** → Add `Related Projects:` entry to page (read+edit page body)
- **Missing YAML fields** → `obsidian vault=KMS property:set name=FIELD value=VALUE file="Page_Name"`
- **Contradictions** → Flag for human review in the coaching session (do not auto-resolve)
- **iOS capture gaps** → Leave for user; note in coaching session

### 2. Extract Themes & Handle Annotated Articles

**For regular input files:** Identify key themes/insights. Map each to ONE primary pillar. Note cross-pillar connections.

**For annotated articles** (only those flagged in Step 1):
- Load the full article file: `obsidian vault=KMS read file="FILENAME"`
- Read the `annotation:` value
- **If annotation is `full article`:** Use the full article body as synthesis source; map to pillar(s)
- **Otherwise:** Use only the annotation text as synthesis source — the annotation IS the input

### 2b. Generate summary: for New Articles Without One

For every article file loaded in Step 2 (文章 or YT), check whether `summary:` already exists:
```bash
obsidian vault=KMS property:read name=summary file="FILENAME"
```
If absent or null, generate and write it:
- **If annotation is `full article`:** summarize from the full body (1-3 sentences: main ideas, arguments, frameworks)
- **Otherwise:** derive from title + `description:` YAML field — 1-3 sentences, factual, content-focused
- Write in English regardless of article language
- Write it using:
```bash
obsidian vault=KMS property:set name=summary value="YOUR SUMMARY" file="FILENAME"
```

The `summary:` captures what the content argued. The `annotation:` captures why it matters to you. Both coexist.

### 3. Find Existing Pages (kms_search)
For each theme, discover relevant pages via kms_search before loading any content:
```bash
python3 "$KMS/00_system/kms_search.py" search "theme_keyword" --pillar PILLAR --limit 5
```
Returns: file path + pillar + type + description — no file content loaded yet.
- Load only the 2–3 matched page files via `obsidian vault=KMS read file="Page_Name"`
- Prevents token bloat

### 4. Merge Intelligently
- **Exact/Near Match** → Update existing page
- **Partial Overlap** → Merge into existing page
- **Pillar Mismatch** → Consider moving to appropriate pillar
- **No Match** → Create new page

### 5. Generate Updates
Create/update pages with:
- YAML: name, pillar (PRIMARY ONLY), type, status, created, updated, description, tags
- Markdown: ## Insights, ## Connections
- Tags: primary pillar + related pillars (for cross-pillar connections)
- **Each page has ONE primary pillar**, but can have tags linking to related pillars
- **Mark new content:** Prefix any new sections/paragraphs added to existing pages with `(new)` so user can see changes at a glance

**Source references MUST be wikilinks — no plain text refs:**
Every `(ref: ...)` in page content must use `[[wikilink]]` format, not plain text. If the source filename is long or contains special characters, use the display alias syntax:
```
(ref: [[Long Filename With Special Chars|Short Display Name]])
```
This applies to section headers too:
```
## Section Title (ref: [[Source File|Short Name]])
```
Never write: `(ref: 文章标题, date)` — always write: `(ref: [[文章标题]])`

**For YAML-only fixes** (type, updated date, missing fields), prefer:
```bash
obsidian vault=KMS property:set name=FIELD value=VALUE file="Page_Name"
```
This avoids a full read+edit cycle.

### 6. Update Pillar Indexes
For each affected pillar, refresh `/02_wiki/[Pillar]/_[PillarName]_Index.md`:
- Update "Active Pages" list
- **List projects per page:** `- [[Page_Name]] — [summary] (projects: [[Project_X]], [[Project_Y]])`

### 7. Log Changes (Prepend to _log.md)
Use obsidian CLI to prepend — avoids loading the full log file:
```bash
obsidian vault=KMS prepend path="02_wiki/_log.md" content="[entry]"
```
- Group by Pillar: `| Action | Page | Project |`
- Include **Cross-Pillar Connections** section (how themes bridge pillars)
- If lint queue items were processed, include a "Lint Fixes" section
- **If input touches an active project, include a Project Updates section:**

```markdown
## Project Updates

| Project | Update | Source |
|---------|--------|--------|
| [[Project_X]] | [What changed — new next step added / decision made / insight logged] | [[input_filename]] |
```

### 8. Track in Processed Log
Append one row per processed file using obsidian CLI (avoids loading the full log):
```bash
obsidian vault=KMS append path="02_wiki/_processed_log.md" content="| YYYY-MM-DD | [[filename]] |"
```

### 9. Route Project Ideas
For any project ideas or action items identified in the input:

**Decision rule:**
- **Clearly tied to an existing active project** → Append to `## Next Steps` in `/04_project/[ProjectName]/[ProjectName].md`
- **Exploratory, new project, or no clear home** → Write to `/04_project/_in_case_you_are_bored.md` under appropriate pillar

**When appending to `[ProjectName].md ## Next Steps`:**
- Use obsidian append:
  ```bash
  obsidian vault=KMS append path="04_project/[ProjectName]/[ProjectName].md" content="- [ ] [Idea] — [brief context] (from: [[input_filename]])"
  ```
- Preserve existing items; append only

**In coaching session:** Reference project backlog additions and new items in `_in_case_you_are_bored.md`.

### 9b. Dance Notes Routing

Triggered when a daily note contains dance/movement content. Detection signals: ballet terms (tendu, plié, arabesque, port de bras, relevé, etc.), CT/countertechnique, gaga, improv, hiphop, yoga pose names, physio corrections, class notes.

**All dance content routes to `04_project/Dance_Note/` — never to the wiki.**

#### Target files

| Content type | Target file |
|---|---|
| CT / universal movement principle | `CT_Toolbox.md` |
| Ballet corrections and exercises | `Ballet_Notes.md` |
| Gaga / improv class notes | `Gaga_Improv_Notes.md` |
| Hiphop cues | `Hiphop_Notes.md` |
| Yoga corrections | `Yoga_Notes.md` |
| Running technique / training | `Running_Notes.md` |
| Physio / structural imbalances | `Physio_Notes.md` |
| Artistic reflection, philosophy, performance log | `Dance_Creation.md` |

#### CT Toolbox taxonomy

Use this to classify any cue that is a universal movement principle (not genre-specific):

- **A — Perspective**: direction and point of view, especially through joints. e.g. *X and Y moving away from each other; wide back; the ankle is lower than you think*
- **B — Space**: expanding into space, inside and outside of the volume. e.g. *your pelvis is 3D like a spaceship; bones are not flat; think the cube of space is bigger than you see*
- **C — Body**: anatomical facts that reframe what you know. e.g. *your X body part is not your Y body part; hip joint is lower than you think; lower back spans from rib to hip joint*
- **D — Energy**: physics in relation to gravity; managing tension. e.g. *use your falling energy; fat feet; reduce unnecessary tension around the ankle, eyes, brain*
- **E — Awareness**: mindset and attention. e.g. *fuck it if not working; you don't have to "do" the seeing; keep it simple; seeing without judging*
- **F — CT Principles**: structural rules of the method. e.g. *sustain it and release it; distinguish release and relax; think from the joint not the muscle*

A cue may belong to multiple categories — place in the primary one, note secondary as `[Primary, Secondary]`.

#### Pipeline

**1. Classify** — for each line of dance content:
- Is it a CT/universal principle? → assign CT category (A–F)
- Is it genre-specific? → assign target file
- Can it be both? → place in CT with a cross-reference note for the style file

**2. Infer** — use surrounding context (lines before/after, class style, section heading) to interpret incomplete or cryptic notes. Rewrite for clarity. If the inference feels like a stretch, flag it.

**3. Flag** — collect lines that are too ambiguous to place confidently, appear cut off, or require your input to interpret. Do NOT flag every line — only genuine blockers.

**4. Write** — append classified cues to the correct section in the target file:
```bash
obsidian vault=KMS append path="04_project/Dance_Note/CT_Toolbox.md" content="[cue under correct ## section]"
obsidian vault=KMS append path="04_project/Dance_Note/Ballet_Notes.md" content="[cue under correct ## section]"
# etc.
```
Cross-references between CT and style notes use `[[File#^block-id]]` syntax where a block ID already exists.

#### Output: Dance Flags section

After writing, if any flags exist, output them as a **separate section** at the end of the run (not inline in coaching):

```markdown
## Dance Flags — Lines Needing Your Input

1. **"[original line]"** — [what's unclear]. Inferred as: [your best guess]. Confirm or correct?
2. ...
```

If no flags, omit the section entirely.

---

### 10. Link Projects to Updated Pages
For any pages that were updated/created:
```bash
obsidian vault=KMS backlinks file="Page_Name" format=json
python3 "$KMS/00_system/kms_search.py" projects
```
Add `Related Projects:` to page Connections section. Ensure reciprocal link in project file.

### 11. Extract and Catalog Captured Items
Identify titles/links from regular input files:
- URLs, movie/book titles, workshops, shows, museum visits, recipes, etc.
- Append to `_watchlist.md`:
  ```bash
  obsidian vault=KMS append path="01_raw/_watchlist.md" content="[new rows]"
  ```

**Note:** Annotated articles are NOT logged to `_watchlist.md` — they are processed, not pending.

### 12. Append Signals
Append POS signals using obsidian CLI:
```bash
obsidian vault=KMS append path="00_system/POS_signal/POS_signal_YYYYMMDD.md" content="[signal entry]"
```

---

## Coaching Processing (Parallel)

### Load Context
```bash
obsidian vault=KMS read file="_priority"
obsidian vault=KMS read file="_POS"
python3 "$KMS/00_system/kms_search.py" projects
```
- **Most recent coaching session for progress comparison** — load the most recent `coaching_YYYYMMDD.md` from `01_raw/coaching/` (the one just written this run if applicable, otherwise the previous one). This is the single unified file — no separate session/discussion files.
- **Project deep-read for updated projects** — For any project whose `updated` date is more recent than the last coaching session, read the full project file (not just YAML header): `## Next Steps`, Trial Log recent entries, and any strategy/discussion notes in the project folder. Surface any project-level decisions or discussions that haven't yet appeared in coaching context.

### Process

1. Read same input file(s)
2. Establish Priority Frame: short-term focus vs. annual priorities
3. Identify insights relevant to priorities
4. Check: Do recommended actions align with _POS?
5. **Compare with previous session:** Track changes and developments
6. **Reference active projects:** Mention projects that align with insights
7. Surface lint contradictions in coaching session for human decision
8. Generate coaching session:
   - **Priority Frame**
   - **Progress Update** (compare with previous session)
   - **Active Projects**
   - **By Priority Area** (only areas the input touches)
   - **High-Impact Insights**
   - **On the Horizon**
   - **Open Items / To Be Concluded**
   - **Experiment Checklist**
   - **Watchlist: Ready to Process** — any `_watchlist.md` entries where `type=process` and `status=done`; prompt: "You finished X — ready to annotate for the wiki?"
   - **Lint Queue: Contradictions** (if any)

---

## Signal Collection (Both Processes)

```markdown
## Signal: [Name]

- **Type:** Patch Evidence / Contradiction / New Pattern / Obsolete
- **_POS Section:** [Section number]
- **Evidence:** [Brief description]
- **Source:** [[specific_page_name]] or [[coaching_YYYYMMDD]] — must be a specific link
- **Date:** YYYY-MM-DD
```

**Always create a new file per run** named `POS_signal_YYYYMMDD.md` (today's date). Do not append to an existing signal file from a previous run — each session's signals should be cleanly separated by date.

```bash
obsidian vault=KMS create path="00_system/POS_signal/POS_signal_YYYYMMDD.md" content="[all signals for this run]"
```

If multiple runs happen on the same date, append to the existing file for that date:
```bash
obsidian vault=KMS append path="00_system/POS_signal/POS_signal_YYYYMMDD.md" content="[signal block]"
```

---

## Output Templates

### Page File
```markdown
---
name: "Page_Name"
pillar: "Career"
type: "topic"
status: "active"
created: "2026-05-01"
updated: "2026-05-01"
description: "One-line summary"
tags: [Career, MindMentalHealth]
---

# [[Page_Name]]

## Insights

- (new) **[Theme]**: [Summary] (ref: [[Source]])

## Connections

Related Pages: [[Page_B]]
Related Projects: [[Project_X]] — [one-line desc]
```

### Change Log Entry (`/02_wiki/_log.md`, prepend)
```markdown
**[2026-05-03] Career**

| Action | Page | Project |
|--------|------|---------|
| Created | [[New-Page]] | [[Project_X]] |
| Updated | [[Existing-Page]] | |

## Cross-Pillar Connections
* Theme → Pillar A, Pillar B (explanation)

## Project Updates
| Project | Update | Source |
|---------|--------|--------|
| [[Project_X]] | Added next step: [description] | [[input_filename]] |

## Lint Fixes (if applicable)
| Fix | Page | Issue Resolved |
|-----|------|----------------|
| Added type | [[Page_Name]] | Missing type field |
```

---

## Execution Checklist

- [ ] Load only unprocessed files (check `_processed_log.md`)
- [ ] **Scan article YAMLs only** — `obsidian properties` for each article in `01_raw/文章/` and `01_raw/YT/`; load full file only if `annotation:` present
- [ ] **Process unprocessed coaching files** — scan `01_raw/coaching/` for `coaching_YYYYMMDD.md` not yet in `_processed_log.md`; load full file; synthesize decisions and reflections into wiki pages
- [ ] **Generate summary: for new articles** — check summary: property; write if absent (full body if `annotation: full article`, else title + description)
- [ ] **Check `/02_wiki/lint/_lint_queue.md` — process unchecked items, check them off**
- [ ] Assign ONE primary pillar per theme
- [ ] Use `kms_search.py search` to find existing pages (don't load all files)
- [ ] Choose appropriate `type` for each page
- [ ] **Mark new page content with `(new)` prefix**
- [ ] Update indexes with projects per page
- [ ] **Prepend to `_log.md`** using `obsidian prepend` (avoids reading full log)
- [ ] **Route project-specific ideas → `[ProjectName].md ## Next Steps`** via `obsidian append`
- [ ] **Route exploratory ideas → `_in_case_you_are_bored.md`**
- [ ] **Dance content in daily notes → classify (CT A–F or style file) → infer → append to `Dance_Note/` files → output Dance Flags section if any ambiguous lines**
- [ ] **For annotated articles: use annotation as synthesis input; `full article` loads body**
- [ ] **Append signals** via `obsidian append` — Source field must be a specific `[[link]]`
- [ ] **Sort `_watchlist_inbox.md`** — insert entries into correct category sections in `_watchlist.md`; clear inbox after
- [ ] **Flag `process` + `done` watchlist items** in coaching: "You finished X — ready to annotate?"
- [ ] **Generate coaching session WITH Progress Update section**
- [ ] **Surface lint contradictions in coaching (do not auto-resolve)**
- [ ] **Use simple link format ONLY:** `[[name]]`
- [ ] **Append one row per processed file to `_processed_log.md`** via `obsidian append`
- [ ] **Use `obsidian property:set`** for YAML-only fixes (type, dates, missing fields)
- [ ] **Coaching output saved to `01_raw/coaching/coaching_YYYYMMDD.md`**

---

## File Structure

```
/KMS
  /00_system
    /_POS.md
    /_priority.md
    /kms_search.py
    /POS_signal/

  /01_raw (read-only)
    /_daily_note/         ← Daily notes
    /_journal/            ← Written reflections, quick_highlights_*.md
    /_ebooks/
    /文章/                 ← Articles (flat, no date subfolders); add annotation: property to YAML to trigger processing
    /YT/                  ← YouTube clips; same annotation + summary workflow as 文章/
    /coaching/            ← All coaching sessions (coaching_YYYYMMDD.md); processed into wiki like any other input
    /_watchlist.md                ← Watchlist (movies, books, recipes, workshops, ideas, Instagram)
    /_watchlist_inbox.md          ← Staged entries from Apple Shortcut; cleared after each sort

  /02_wiki
    /_log.md
    /_processed_log.md  ← Simple table: date | [[file]]
    /lint/
      /_lint_queue.md
      /wiki_lint_YYYYMMDD.md
    /[Pillar]/
      /_[Pillar]_Index.md
      /[Page_Name].md

  /03_priming
    /priming_YYYYMMDD.html

  /04_project
    /_in_case_you_are_bored.md
    /[ProjectName]/
      /[ProjectName].md
      /[ProjectName]_Trial_Log.md
      /CLAUDE.md
```

---

## Key Rules

1. **Each page has ONE primary pillar** — cross-pillar via tags
2. **Link format is ALWAYS simple:** `[[name]]` — no paths
3. **Mark new page content with `(new)`** for easy scanning
4. **Assign `type` to every page** — concept / practice / topic / synthesis
5. **Project-specific ideas → `[ProjectName].md ## Next Steps`; exploratory ideas → `_in_case_you_are_bored.md`**
6. **Compare with previous coaching session** — include Progress Update section
7. **Use `kms_search.py`** for bulk metadata discovery — never load files speculatively
8. **Use obsidian CLI** for targeted reads, property writes, and appends — avoids read+edit+write cycles
9. **Merge intelligently** — don't overwrite user edits
10. **Process `/02_wiki/lint/_lint_queue.md` every run** — check off completed items
11. **POS signal Source field must be a specific `[[link]]`** — never generic or blank
12. **Log project updates** — include Project Updates table in `_log.md` when input touches a project
13. **Article scanning is YAML-only** — scan both `文章/` and `YT/`; load full article body ONLY if `annotation:` is present
19. **Watchlist inbox is always cleared after sort** — entries in `_watchlist_inbox.md` are transient; once sorted into `_watchlist.md` they are removed from inbox
20. **`process` + `done` watchlist items surface in coaching** — prompt user to annotate so wiki-coach can synthesize on next run
14. **For regular annotations:** use annotation text as the synthesis input — do NOT read the article body
15. **All `(ref: ...)` citations are wikilinks** — never plain text. Use `[[Filename]]` or `[[Filename|Display Name]]` for long/special-character filenames. Applies to inline refs and section headers alike.
16. **Unannotated articles are silently skipped** — no logging, no pending status
17. **Processed log is a simple table** — date | `[[file]]`; append via `obsidian append`
18. **Quick highlights are pre-filtered — trust the mapping.** `quick_highlights_*.md` entries already have `source:`, `connected_projects:`, and `connected_pages:` filled in by `/quick-read`. Use these as merge targets directly; don't re-search or re-extract. The source `[[link]]` must be preserved in any wiki page update generated from a highlight.
21. **Coaching files are always fully loaded** — no annotation gate; `coaching_YYYYMMDD.md` files in `01_raw/coaching/` are treated as high-value synthesis input. Decisions, reflections, and project conclusions flow into wiki pages. Save new coaching output to `01_raw/coaching/coaching_YYYYMMDD.md`.
