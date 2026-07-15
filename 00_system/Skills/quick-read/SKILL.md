---
name: "quick-read"
description: "Instantly surface implications and actions from a specific source (clipped article, YT, or any file) against your current priorities, projects, and wiki."
---

# Quick-Read Skill

Given one or more sources already in the KMS vault, load full context and return: what each source means for you *right now*, which projects it touches, which wiki pages it connects to, and 1–2 concrete actions. Output is saved as highlight entries in project-specific files in `_journal/` for wiki-coach to pick up.

**Invoke as:** `/quick-read [source(s)] [project(s) — optional]`

Examples:
- `/quick-read 如何利用一个周末掌握 Claude Code` — generic route, no project specified
- `/quick-read dancer-nutrition-video Training_program` — project specified, load that project in full
- `/quick-read article1 article2 Training_program Flight_Upsell` — multiple sources, multiple projects

---

## What This Skill Loads

**Sources (always):**
- All named source files in full — `obsidian vault=KMS read file="FILENAME"` for each

**Context:**
- `/00_system/_priority.md` — short-term focus order
- `/00_system/_POS.md` — skim for active patterns relevant to source themes

**Projects:**
- **If project(s) named:** load each named project's overview file in full — `obsidian vault=KMS read file="ProjectName"`. No other files in the project folder needed.
- **If no project named:** run `kms_search.py projects` → read YAML header + `## Next Steps` of each active project; identify which are relevant

**Wiki pages:**
- Run `kms_search.py search "THEME" --limit 5` for 2–3 themes per source → load 2–3 most relevant pages in full

---

## Processing Steps

### 1. Read all sources in parallel
For each named source file:
```bash
obsidian vault=KMS read file="FILENAME"
```
Extract per source: main argument, key claims, frameworks, data points.

### 2. Load project context
**If projects named:** read each named project overview file in full.  
**If not:** run `kms_search.py projects` → read YAML + `## Next Steps` of each active project.

### 3. Find relevant wiki pages
```bash
python3 "$KMS/00_system/kms_search.py" search "THEME" --limit 5
```
Run searches based on source themes. Load 2–3 most relevant pages.

### 4. Generate implications
For each source × project/wiki combination:
- Does this **validate, contradict, or extend** what you know/are doing?
- Is there a **concrete next step** this unlocks or accelerates?
- Is there a **trade-off or risk** relevant to your situation?

Frame relative to current priority order — higher-priority connections first.

### 5. Save highlights (project-scoped files)

Highlights are saved to **project-specific files**, not one flat file. This way multiple queries in a day stay organised and wiki-coach can easily attribute them.

**File naming:** `_journal/quick_highlights_[ProjectName]_YYYYMMDD.md`  
**If no clear project:** `_journal/quick_highlights_general_YYYYMMDD.md`

**Append behaviour:**
- If the file already exists (earlier query today for the same project): append a new `## [Source Title] — [HH:MM]` block
- If the file doesn't exist: create it with the project header

**File format:**
```markdown
---
project: [[ProjectName]]
date: YYYY-MM-DD
---

# Quick Highlights — [ProjectName] — YYYY-MM-DD

## [Source Title] — [HH:MM]

source: [[FILENAME]]
connected_pages: [[WikiPage1]], [[WikiPage2]]

**Implications:**
- [specific implication — name the claim, not just the theme]

**Actions:**
- [ ] [concrete action]
- [ ] [optional second]

---

## [Another Source Title] — [HH:MM]

source: [[FILENAME2]]
...
```

**If a query touches multiple projects:** write one entry per project file, with only the implications relevant to that project in each.

---

## Output Format (in conversation)

For each source:

```
## Quick Read: [Source Title]

**Relevance to you:** [1–2 sentences on why this matters given your priorities]

**Project connections:**
- [[ProjectName]] — [specific implication, e.g. "validates July nutrition variable, protein timing claim"]
- [[ProjectB]] — [specific implication]

**Wiki connections:**
- [[WikiPage1]] — [extends / contradicts / fills gap / validates]

**Actions:**
- [ ] [concrete, owned action]
- [ ] [optional second]

*Saved → `_journal/quick_highlights_ProjectName_YYYYMMDD.md`*
```

If multiple sources were read, output them in sequence, then a brief "Common thread:" note if they share implications.

---

## Key Rules

- Always link source by `[[filename]]` — never plain text
- Project connections must be specific: name the claim, not just "relevant to fitness"
- Wiki connections must say *how* — extends / contradicts / fills gap / validates
- Max 2 actions per source; concrete enough to do without further planning
- **Project-specific highlight files** — one file per project per day; append within the day
- **Multiple sources, one project:** all appear as separate `## [Title] — [HH:MM]` blocks in the same file
- **One source, multiple projects:** split implications across each project's file
- If a source has no meaningful connection to current priorities or projects, say so — don't manufacture relevance
- Always save the highlight regardless — it creates the audit trail

---

## KMS Paths

```
KMS="/Users/michael_zhang/Library/Mobile Documents/iCloud~md~obsidian/Documents/KMS"

Articles:   $KMS/01_raw/文章/
YT clips:   $KMS/01_raw/YT/
Projects:   $KMS/04_project/[ProjectName]/[ProjectName].md
Wiki:       $KMS/02_wiki/
Priorities: $KMS/00_system/_priority.md
POS:        $KMS/00_system/_POS.md
Highlights: $KMS/01_raw/_journal/quick_highlights_[ProjectName]_YYYYMMDD.md
```
