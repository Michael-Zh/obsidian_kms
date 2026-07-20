# Project Context: Life_Management_System (LMS)
_Last updated: 2026-07-21_

## What This Project Is

The **meta-system hub** — the overarching operating system that integrates all of Michael's knowledge management, training and physical management, daily priming, and coaching into one cohesive whole. Two layers: (1) 概念层 — how the system works (8 pillars, wiki-coach, POS, priority system); (2) 执行层 — the technical implementation (custom App + Claude Code + iOS Shortcuts). Modules 1–3 are complete and live. The system now orchestrates multiple integrated sub-systems: Training Coach App, Training Program, Meal Prep Routine, Priming, and Coaching.

**Primary Pillar:** LifeManagement
**Status:** Active — meta-system hub
**Current Focus:** Ongoing: maintain + evolve. LMS itself no longer has a separate build roadmap — it evolves through the sub-systems it orchestrates.
**Priority:** P1

---

## Objectives

- **Goal 1: Capture & Preserve** — Durable, immutable record of sources (`01_raw`)
- **Goal 2: Automated wiki synthesis** — 8 pillars with active pages, linked projects, bidirectional connections
- **Goal 3: Executive Action** — Convert knowledge into trials, coaching sessions, Apple Reminders
- **Goal 4: Social Loop** — Document the "Trial and Error" process for sharing

---

## Current State & Recent Progress

**Phase 2.10 complete (2026-06-16) — Daily workflow automation:**
- AutoSleep → `sleep_log.md`: iOS Personal Automation at noon, silent append per day
- `/priming` morning skill: Typeless transcript → POS + priorities + sleep + both calendars → (A) warm daily note block, (B) HTML card in `03_priming/`
- `calendar_scheduler_v3.py --today` flag: returns JSON of today's events across both calendars
- Laptop wake automation: `pmset` wake 07:00 weekdays + `caffeinate -i` launchd agent

**External validation (coaching_session_20260617):**
- "KMS architecture is ahead of the curve — use it, don't keep refining it." Key signal: the build phase is done; the system needs to be used and tested in practice, not further elaborated.

**All capture gaps closed (2026-06-07):**
- Mobile web + WeChat/XHS → bijitongbu; Desktop → Web Clipper; YouTube → playlist → desktop clip
- `_watchlist.md`: 8 categories, `type:ref` vs `type:process`; Apple Shortcut → `_watchlist_inbox.md` staging

**Open decisions / blockers:**
- [ ] Module 4 design: how do `_watchlist` `type:process` + `status:done` entries flow into wiki? Own entity page vs. feed existing topic page?
- [ ] Shows & museums as a first-class capture type in `_watchlist.md`

---

## Pending Next Steps

- [ ] **Design Module 4 entity processing** — `_watchlist.md` `type:process` + `status:done` → annotation → wiki synthesis. Key question: own wiki page per entity, or feed existing topic page?
- [ ] **Shows & museums capture type** — add to `_watchlist.md` categories and define processing path
- [ ] **Mobile quick-read route** — Gemini project per domain + `/export-gemini-context` skill + "Send to Obsidian" Shortcut; defer until desktop `/quick-read` is validated in practice
- [ ] **Update module flow chart** — reflects Phases 2.5–2.8 completions
- [ ] **YAML metadata enrichment** — when processing `_watchlist` entries, enrich with pillar, linked_page

---

## Other Pending Items (from _in_case_you_are_bored)

- **Naval's Almanack as KMS skill** — Convert Naval Ravikant's decision-making prompts into a reusable Claude skill. Trigger: July 2026, low priority, quiet slot. (ref: [[coaching_20260530]])
- **Xiaohongshu Content Series** — Share KMS journey + movement/body tips; defer until KMS MVP validated. Related: [[Content-Creator-and-Entrepreneurship-Ideas]]

---

## Architecture: The Three-Layer Design

**Layer 1 — Raw Input** (`/01_raw/`)
Immutable. Subfolders: `_daily_note/` (daily notes), `_journal/` (reflections + quick highlights), `文章/` (articles), `YT/` (YouTube clips), `coaching/` (all coaching sessions — also fed into wiki synthesis).

**Layer 2 — Wiki** (`/02_wiki/`)
Timeless synthesis. "What do I know about X?" AI-generated. 5 page types: concept / practice / topic / synthesis / entity.

**Layer 3 — Morning Priming** (`/03_priming/`)
HTML card output from the `/priming` skill. Dated, self-contained.

**The bridge:** `_in_case_you_are_bored.md` — durable project landscape (active + backlog + ideas).

**Key architectural insight:** Annotation IS the routing logic. Add `annotation:` to a file's YAML → it gets processed. Coaching files are always processed (no annotation gate). No database, no explicit routing rules.

---

## Capture Matrix

| Source | Mobile | Desktop |
|--------|--------|---------|
| WeChat / XHS | ✅ bijitongbu | n/a |
| Web pages | ✅ bijitongbu | ✅ Web Clipper |
| YouTube | 🔄 playlist → desktop | ✅ Web Clipper |
| Instagram | URL only → `_watchlist` | rarely needed |
| Watchlist items | ✅ Apple Shortcut → `_watchlist_inbox.md` | manual edit |

---

## Related Wiki Pages

- **[[KMS-System-Design]]** — System architecture and long-term vision
  - Design philosophy for all three layers; canonical source for "why annotation-first"
  - Long-term vision includes Module 4 entity processing scope

- **[[Daily-Note-Workflow]]** — Daily capture and brain dump protocol
  - How raw daily notes flow into `01_raw/_daily_note/` and get picked up by wiki-coach
  - Relevant when debugging priming output or daily note capture

- **[[Wiki-Organization]]** — Pillar and page structure
  - 8 pillars, 5 page types (concept/practice/topic/synthesis/entity)
  - Authoritative reference for Module 4: where entity pages live in the hierarchy

---

## File Map

| File | When to read |
|------|--------------|
| `Life_Management_System.md` | Full roadmap, all module statuses, all decisions, accomplishments |
| `Life_Management_System_Trial_Log.md` | Experiment history; decisions 1–3; past blockers |
| `02_wiki/LifeManagement/KMS-Development.md` | Development history; note-taking friction requirements |
| `02_wiki/LifeManagement/Information-Overload.md` | Problem definition; ideal pipeline; capture friction points |
| `01_raw/_watchlist.md` | Current watchlist; check for `process+done` items ready for annotation |
| `01_raw/coaching/coaching_YYYYMMDD.md` | Past coaching sessions — all unified here now |
| `04_project/_in_case_you_are_bored.md` | Full active project landscape and backlog |

---

## Working Agreement

You are acting as a **thought partner and analyst** for the KMS / Life_Management_System project. Your role is to:

- Help think through Module 4 entity processing design — this is the active frontier
- Connect new information to existing wiki pages, decisions, and patterns
- Challenge assumptions — especially complexity vs. simplicity trade-offs (the architecture rewards elegant simplicity)
- Reference `Life_Management_System_Trial_Log.md` when discussing past experiments or decisions
- Use `[[simple_link]]` format for all internal references
- **Start each session by reviewing Pending Next Steps** — triage, discuss, or action them before moving on

**Orienting signal:** The external validation from coaching (2026-06-17) is clear — use the system, don't keep building it. Push toward Module 4 design decisions rather than further architecture elaboration.

**At the end of each conversation:**
1. Summarize any insights, decisions, or new information worth preserving
2. Propose a single log entry for `Life_Management_System_Trial_Log.md` — formatted, ready to paste, covering full session
3. Propose any updates to `## Next Steps` in `Life_Management_System.md`
4. If the conversation changed strategy, framing, or open decisions — propose the specific update to `Life_Management_System.md`
5. Wait for approval before writing anything
6. If a wiki page should be updated, note which one and what the addition would be

**Prompt occasionally** during longer sessions: "Good stopping point — want to wrap up and capture what we've covered so far?"

**Do not** rewrite existing content — only propose additions.

**Session-start reconcile rule:** 每次 CC session 加载 project-context 时，如果 `project-context` skill 在顶部显示 `## ⚠️ Pending App Changes`，必须先 review delta（backlog 完成情况 + coaching sessions 的 decisions），和用户确认是否写入 Obsidian project doc，完成 reconcile 后再进入正式讨论。

**Output rules:** Always reply in Chinese (中文).

**Sync rule:** 每次会话结束更新此 CLAUDE.md 时，同步更新 `_in_case_you_are_bored.md` 里 [[Life_Management_System]] 行的 Current Focus + Updated 字段。
