---
name: Life_Management_System
project_id: pj0001
status: active
pillar: LifeManagement
current_focus: "Meta-system hub — 概念层（KMS 知识架构 + wiki-coach + POS + priority） + 执行层（自定义 App + Claude Code）| 集成的子系统：Training Coach App、Training Program、Meal Prep、Priming、Coaching"
created: 2026-05-03
updated: 2026-07-21
target_completion: ongoing
priority: P1
tags:
  - LifeManagement
---
## 0. Overview

Life Management System (LMS) is the **meta-system hub** — the overarching operating system that integrates all of Michael's knowledge management, training and physical management, daily priming, and coaching into one cohesive whole.

**Two-layer architecture:**

1. **概念层（Concept Layer）** — How the system works: 8-pillar knowledge architecture, wiki-coach synthesis, Personal Operating System (POS), priority system, coaching generation
2. **执行层（Execution Layer）** — The technical implementation: a custom-built App (via Vibe Coding) paired with Claude Code, plus iOS Shortcuts and automation

**Integrated sub-systems:**

| Sub-system | Role | Project Folder |
|------------|------|----------------|
| **Training Coach App** | 日常训练/生活管理/priming 的统一执行载体 | [[Training_Coach]] |
| **Training Program** | 训练执行 + 数据追踪 + 周计划 | [[Training_program]] |
| **Meal Prep Routine** | 饮食哲学 + routine 设计（未来并入 App）| [[Meal_prep_routine]] |
| **Priming** | 早晨启动流程（Typeless → daily note block + HTML card）| Part of this project |
| **Coaching** | 所有 coaching sessions 作为系统输入 + action 输出 | `01_raw/coaching/` |
| **KMS 知识管理** | 8 pillars, wiki synthesis, article ingestion, watchlist | This project |

The key insight (2026-07-21 re-org): these are not separate concerns — they are a single integrated system. The Training Coach App is the execution interface; Claude Code + Obsidian is the cognitive engine; the coaching sessions are the feedback loop.

---

## 0.1 Design Philosophy — Three-Layer Architecture

The KMS is built on three distinct layers with clearly separated purposes. Understanding this prevents content from landing in the wrong place.

**Layer 1 — Raw Input** (`/04_project/_inbox/`)
The unprocessed stream. Source-agnostic: brain dumps, web clips, transcripts, ebooks, coaching responses you wrote later, digests of interesting conversations, your own answers to open coaching questions. The rule: **if it hasn't been synthesized yet, it belongs here.** Raw inputs are immutable — never edited after capture.

**Layer 2 — Wiki** (`/02_wiki/`)
The synthesis layer. Answers the question: *"what do I know about X?"* Timeless, pillar-organized, AI-generated from whatever came through the inbox. You should almost never write directly into the wiki — that's the wiki-coach skill's job. If you feel the urge to add something directly to a page, that's a signal it should go to `_inbox/` first and be processed properly.

Each wiki page has a `type` that determines how the LLM synthesizes it:

| Type | What it captures | Example |
|------|-----------------|---------|
| **concept** | Abstract framework, philosophy, identity pattern | `Identity-Based-Life-Philosophy`, `Work-Performance-Anxiety` |
| **practice** | Active protocol, routine, habit with experiment results | `Sleep-Optimization-Routine`, `Fitness-Routine` |
| **topic** | Domain being explored — open questions, evolving understanding | `Portfolio-Career-Design`, `KMS-Development` |
| **synthesis** | Generated analysis or comparison filed back into wiki | A comparison you asked the LLM, now preserved as a page |
| **entity** | Person, book, or named artifact — index of learnings + internal links | `James_Clear`, `Atomic_Habits` |

**Layer 3 — Coaching Outputs** (`/03_output/`)
The temporal action layer. Answers: *"what should I do now, given my current priorities?"* Dated, contextual, tied to a moment. The closest thing to a diary/journal in the system. These are not synthesized into the wiki — they stay as-is, and become source material for the inbox if you write responses to them later.

**The bridge — `_in_case_you_are_bored.md`**
The durable *action* layer (what projects exist, what's worth pursuing). Sits between coaching (ephemeral guidance) and wiki (durable knowledge). Updated after each coaching run.

**The feedback loop:**
Coaching generates questions → you answer them later → answers go to `_inbox/` as `coaching_insight_YYYYMMDD.md` → next wiki-coach run synthesizes your answers into wiki pages → those pages inform richer future coaching.

---

## 0.2 Article Ingestion — Annotation-First Design

Articles and long-form content (WeChat 公众号, XHS posts) follow a special path that preserves personalization.

**Why annotation-first?** Without personal relevance framing, raw articles synthesize into impersonal digests — accurate summaries of what the *author* thought, not what *you* think. Annotating directly in the article YAML keeps the workflow minimal and the output personal.

**The workflow:**

1. **Capture** → bijitongbu saves full article to `01_raw/_inbox/文章/` (flat, no date subfolders; automatic, one tap)
2. **Annotate in Obsidian** → open the article, add `annotation:` property to YAML frontmatter:
   - Regular: answer the 3 questions (what struck you / why now / action or contradiction)
   - Full synthesis: set `annotation: full article`
   - No annotation: leave as-is — article is skipped until annotated
3. **Process** → run `/wiki-coach-kms-cli`
   - Scans YAML-only for all articles in `01_raw/_inbox/文章/` (token-efficient via `kms_search.py meta`)
   - Loads article body ONLY if `annotation: full article`
   - For regular annotations: annotation text IS the synthesis input — body never read
   - Unannotated articles silently skipped — checked again next run
4. **Archive** → raw articles stay in `01_raw/` permanently as immutable source

**`_processed_log.md`** tracks all processed inputs (daily notes + articles) as a plain table: date | `[[file]]`.

---

## 1. Objectives & Goals

- **Goal 1: Capture & Preserve** — Create a durable, immutable record of sources (`01_raw`)
- **Goal 2:** **Automated wiki synthesis** and 8 pillars organized with active pages, linked projects, and bidirectional connections
- **Goal 3:** **Executive Action** — Convert knowledge into tangible trials, coaching sessions, and Apple Reminders
- **Goal 4: Social Loop** — Document the "Trial and Error" process for social sharing

---

## 2. Roadmap

### 1. Modules & Roadmap
![[Pasted image 20260505003309.png]]

**Current Module Status:**

| #       | Module Name                 | Status            | Purpose                                                                                              | Priority      |
| ------- | --------------------------- | ----------------- | ---------------------------------------------------------------------------------------------------- | ------------- |
| **1a**  | Apple Shortcuts capture     | ✅ Complete       | Unified shortcut built: URL share → `_watchlist_inbox.md`; text/manual → name field; category picker; hardcoded `ref`; appends 7-column format | —             |
| **1b**  | Article annotation workflow | ✅ Complete       | bijitongbu + annotation-first design + wiki-coach; personalized synthesis of saved articles + YT     | —             |
| **2**   | Input sorting system        | ✅ Complete       | `_watchlist.md` restructured by category; `_watchlist_inbox.md` staging; wiki-coach sort step; no database needed — annotation IS the routing logic | —             |
| **3**   | Web content extraction      | ✅ Complete       | Solved at capture layer: bijitongbu (WeChat/XHS/web mobile), Web Clipper (desktop + mobile Safari), YT playlist → desktop clip. MCP server not needed. | —             |
| **4**   | Entity processing           | 🔵 Next           | Process `_watchlist.md` entries with `type: process` + `status: done` → annotation → wiki synthesis | P1            |
| **5**   | Obsidian Daily Note inbox   | ✅ Complete       | Brain dump capture; input consolidated to `/04_project/_inbox/`                                      | —             |
| **6.1** | Wiki generation & synthesis | ✅ Complete       | wiki-coach-kms-cli skill live; YT folder added; summary generation; watchlist inbox sort step        | —             |
| **6.2** | Coaching generation         | ✅ Complete       | Progress Update section; project-context skill; watchlist `process+done` flagging in coaching        | —             |
| **6.3** | Instant implication layer   | ✅ Complete       | `/quick-read` skill: load source + named project(s) + wiki → implications + actions → `quick_highlights_[Project]_YYYYMMDD.md`; wiki-coach picks up on next run | —             |


**High-Level Roadmap (Based on Current Priority & Feasibility):**

- **Phase 1 (✅ Complete):** Capture infrastructure + wiki-coach-kms-cli skill live
- **Phase 2.1 (✅ Complete - 2026-06-07):** Input routing resolved — annotation IS the routing logic; no database schema needed; folder structure sufficient
- **Phase 2.2 (✅ Complete - 2026-05-16):** Project template integration — all project files standardized, links cleaned, `_in_case_you_are_bored.md` unified, two new skills shipped (`project-context`, `project-review`)
- **Phase 2.3 (✅ Partial - 2026-05-16):** Ad-hoc coaching — `project-context` skill generates CLAUDE.md per project; `project-review` handles monthly priority re-ordering; standalone conversational trigger still open
- **Phase 2.4 (✅ Complete - 2026-05-16):** Input consolidation — decided and implemented (`_inbox/` single folder approach)
- **Phase 2.5 (✅ Complete - 2026-06-07):** Watchlist system — `_watchlist.md` restructured by category; `_watchlist_inbox.md` staging flow; Apple Shortcut built (unified URL+text); wiki-coach sort step added
- **Phase 2.6 (✅ Complete - 2026-05-31):** Article annotation workflow — bijitongbu + annotation-first design; personalized synthesis
- **Phase 2.7 (✅ Complete - 2026-06-07):** Web capture gaps closed — bijitongbu handles mobile web + WeChat/XHS; Web Clipper on mobile Safari; YT via playlist → desktop. MCP server not needed.
- **Phase 2.8 (✅ Complete - 2026-06-07):** Summary layer — `summary:` property backfilled on all 文章 + YT files; wiki-coach generates summary on new files automatically
- **Phase 2.9 (✅ Complete - 2026-06-07):** Instant implication layer — `/quick-read` skill; inbox restructured (`_daily_note/`, `_journal/`); articles flat in `文章/`
- **Phase 2.10 (✅ Complete - 2026-06-16):** Daily workflow automation — AutoSleep → sleep_log.md (iOS Shortcut, noon daily, append block format); `/priming` morning skill (Typeless transcript → daily note block + HTML card, warm tone, calendar-integrated); `calendar_scheduler_v3.py --today` flag (both training + main calendar); laptop wake at 07:00 weekdays (pmset + caffeinate launchd agent)
- **Phase 3 (🔵 Next):** Module 4 — Entity processing: books, people, concepts from `_watchlist.md` `type:process` entries

### 2. Directory Structure

```
/KMS
  /00_system                      <-- System Instructions (LLM Logic)
    /_POS.md                      <-- Personal Operating System
    /_priority.md                 <-- Current priorities & sequencing
    /POS_signal/                  <-- Signal files (daily-rotating)
    
  /01_raw                         <-- Immutable Sources (Archive)
    /_daily_note/                 <-- Daily notes
    /_journal/                    <-- Written reflections, quick highlights
    /_ebooks/                     <-- eBook extracts (full files only)
    /文章/                          <-- Full articles (flat, no date subfolders); bijitongbu saves here
    /YT/                          <-- YouTube clips (Obsidian Web Clipper)
    /coaching/                    <-- All coaching sessions (coaching_YYYYMMDD.md); fed into wiki synthesis
    _watchlist.md                 <-- Watchlist by category (films, books, people, recipes, workouts...)
    _watchlist_inbox.md           <-- Staging file: Apple Shortcut appends here; wiki-coach sorts into _watchlist.md
    
  /02_wiki                        <-- Persistent Knowledge Artifacts
    /_log.md                      <-- Chronological change record (prepend)
    /_processed_log.md            <-- Input files processed tracker
    /lint/                        <-- Lint outputs
      /_lint_queue.md             <-- Issues for next wiki-coach run
      /wiki_lint_YYYYMMDD.md      <-- Health reports from each lint run
    /[Pillar]/
      /_[Pillar]_Index.md
      /[Page].md
      
  /03_priming                     <-- Morning priming HTML cards
    /priming_YYYYMMDD.html
    
  /04_project                     <-- Projects (Action-Oriented, Time-Bound)
    /_in_case_you_are_bored.md    <-- Full project landscape (active + backlog + ideas)
    /[ProjectName]/
      /[ProjectName].md           <-- Project overview (links as [[ProjectName]])
      /[ProjectName]_Trial_Log.md <-- Trial log
      /CLAUDE.md                  <-- Project context for Claude Projects (generated by /project-context)
```

**Hierarchy Mapping:**

|**Level**|**Mapping**|**Role**|**Location**|**Status**|
|---|---|---|---|---|
|**Pillar**|Root|Permanent Life Area|`/02_wiki/[Pillar]/`|✅ Live|
|**Page**|1 Pillar : N Pages|Typed knowledge artifact (concept / practice / topic / synthesis)|`/02_wiki/[Pillar]/[Page].md`|✅ Live|
|**Project**|1 Page : N Projects|Action-Oriented Trial|`/04_project/[Project_Name]/`|✅ Live|
|**Index**|Single Source|Master Map|`/02_wiki/[Pillar]/_Index.md`|✅ Live|
|**Log**|Audit Trail|Chronological Record|`/02_wiki/_log.md`|✅ Live|

---

### 4. The 8 Pillars (Life Organization)

- **Relationships** — Social health and core connections
- **Mind & Mental Health** — Internal world, reflection, therapy
- **Career** — Professional output and skill development
- **Physical Health** — Sleep, fitness, diet
- **Life Management** — Systems and meta-work (including KMS itself)
- **Finance** — Wealth management and resource allocation
- **Creativity & Curiosity** — Exploration and hobbies
- **Admin & Home** — Physical environment and bureaucracy
- **Travel** — Travel ideas and planning

---

### 5. Proposed Full Workflow (Input → Wiki + Coaching → Output)

```
INPUT (daily note, web clip, transcript, etc.)
  │
  ├─→ Wiki Process
  │   ├─ Extract themes → Assign to pillars
  │   ├─ Find related pages (Obsidian CLI search)
  │   ├─ Merge intelligently with existing content
  │   ├─ Update `/02_wiki` pages + indexes
  │   ├─ Prepend to `_log.md` (with Cross-Pillar Connections)
  │   └─ Append signals to `/00_system/POS_signal/`
  │
  └─→ Coaching Process (PARALLEL)
      ├─ Load same input + current priorities
      ├─ Load _POS.md constraints
      ├─ Filter insights through priorities
      ├─ Generate actionable coaching session
      ├─ Output to `/03_output/coaching_session_YYYYMMDD.md`
      └─ Append signals to `/00_system/POS_signal/`

RESULT: Both wiki updates (neutral) + coaching guidance (priority-filtered) from one input
```

---

## Next Steps

What can you start doing and prioritize now?

**Immediate priorities (This week):**
- [ ] **Design Module 4 entity processing** — define how `_watchlist.md` entries with `type: process` + `status: done` flow into wiki synthesis. Key question: does a book/person get its own wiki page, or does it feed into an existing topic page?

**Near-term (Next 2-3 weeks):**
- [ ] **Shows & museums as a capture type** — Add cultural events (shows, museum visits, exhibitions) as a first-class type in `_watchlist.md`. Define how they get processed and linked to wiki pages.
- [ ] **Update module flow chart** — reflects Phases 2.5–2.8 completions
- [ ] **YAML metadata enrichment** — When wiki-coach processes a `_watchlist.md` `process` entry, enrich source with structured metadata: type, pillar, capture_date, processing_status, linked_page
- [ ] **Mobile quick-read route** — once desktop `/quick-read` is validated in practice, design mobile flow (Gemini project per domain + `/export-gemini-context` skill + "Send to Obsidian" Shortcut)

**Decision gates:**
- [x] **Input Consolidation (2.4)** — Resolved 2026-05-16: `_inbox/` single folder
- [x] **Module 2 database schema** — Resolved 2026-06-07: no database needed; annotation IS the routing logic
- [x] **Module 3 MCP server** — Resolved 2026-06-07: not needed; capture solved at tool layer (bijitongbu + Web Clipper)
- [x] **Instant implication layer** — Resolved 2026-06-07: desktop `/quick-read` skill; mobile route deferred

---

## Open Decisions

Decisions to be made, blockers to resolve.

### Decisions Pending

- 

### Decisions Resolved

- 

### Blockers

- 
---

## Accomplishments

What's already been completed or achieved in this project.

- **Phase 1 Complete (✅):** Capture infrastructure + wiki processing live
  - ✅ Obsidian vault directory structure initialized
  - ✅ Daily note capture in `/01_raw/_daily_note/` working
  - ✅ Apple Shortcuts capturing raw URLs + text to `/01_raw/`

- **wiki-coach-kms-cli Skill (✅ LIVE):** 8-step wiki processing + parallel coaching generation
  - ✅ Extract themes → assign to pillar
  - ✅ Find related pages using `obsidian search`
  - ✅ Merge intelligently (exact/partial/no match decision tree)
  - ✅ Generate page updates with proper formatting and cross-pillar tags
  - ✅ Update pillar indexes (preserve manual edits, list projects per page)
  - ✅ Log changes (prepend to `_log.md` with cross-pillar connections)
  - ✅ Parallel: Generate coaching sessions with priority filtering
  - ✅ Signal collection (both processes append to daily-rotating signal files)

- **POS Update Process (✅ COMPLETE):** Signal-based, on-demand batch processing
  - ✅ Signals accumulate continuously
  - ✅ File rotation (new calendar day = new signal file)
  - ✅ Batch processing via `pos_update` skill
  - ✅ Full audit trail in `_POS_changelog.md`

- **Priority System (✅ COMPLETE):** Three-level structure (P1, P2, P3)
  - ✅ Current state: P1 (Physical Base), P2 (Resource Moat), P3 (Relationship Gate)
  - ✅ Each includes: outcomes, KPIs, initiatives, timeline, dependencies

- **Project Template (✅ COMPLETE):** Finalized 2026-05-03
  - ✅ Project Overview structure (8 sections with flexible Roadmap for product vs. research projects)
  - ✅ Trial Log structure (5 sections with merged Decisions/Blockers/Pivots)
  - ✅ Integration mapping to wiki + coaching workflows

- **Phase 2.2 + Skill Updates (✅ COMPLETE - 2026-05-16):** Full project template integration + KMS system cleanup
  - ✅ All project overview files renamed to `[ProjectName].md` (8 projects including Flight Upsell)
  - ✅ All path-based Obsidian links fixed → simple `[[name]]` format across wiki, coaching sessions, and POS signals
  - ✅ `_in_case_you_are_bored.md` merged with `_projects_index.md` — unified project landscape (Active Projects table + Backlog + Ideas by pillar)
  - ✅ Input folder consolidated to `/04_project/_inbox/` (merged `_daily_note` + `_dump`)
  - ✅ `wiki-coach-kms-cli` skill updated: 5 improvements (consolidated inbox, `(new)` prefix for page updates, Progress Update section comparing to previous session, project ideas routed to `_in_case_you_are_bored.md`, simple links only)
  - ✅ `project-context` skill created: generates/refreshes `CLAUDE.md` per project for use in Claude Projects
  - ✅ `project-review` skill created: lightweight monthly priority re-ordering based on what feels alive

- **Article Annotation Workflow (✅ COMPLETE - 2026-05-31):** Personalized article ingestion with annotation-first design
  - ✅ bijitongbu plugin integration for WeChat 公众号 & XHS + general web pages (mobile)
  - ✅ Unified YAML format across all bijitongbu sources
  - ✅ Annotation-first: `annotation:` property drives synthesis; body never loaded unless `annotation: full article`
  - ✅ Token-efficient: YAML-only scan; body loaded only when needed
  - ✅ `_processed_log.md` simplified to plain table

- **Capture Gap Closure (✅ COMPLETE - 2026-06-07):** All input sources now covered without MCP server
  - ✅ Mobile web pages → bijitongbu
  - ✅ Desktop web + YouTube → Obsidian Web Clipper
  - ✅ Mobile YouTube → save to playlist → clip on desktop
  - ✅ Instagram → URL only in `_watchlist.md` (login-protected; ref type)
  - ✅ Decision: MCP server not needed; capture solved elegantly at tool layer

- **Instant Implication Layer (✅ COMPLETE - 2026-06-07):** `/quick-read` skill for on-demand source analysis
  - ✅ Accepts multiple sources and optional named project(s) in one call
  - ✅ Named project → load full project overview only (not whole folder)
  - ✅ Generic route → scan all active project headers + Next Steps
  - ✅ Loads 2–3 relevant wiki pages per source themes
  - ✅ Saves to project-scoped highlight files: `quick_highlights_[ProjectName]_YYYYMMDD.md`
  - ✅ Multiple queries same day → append as timestamped blocks in same file
  - ✅ One source → multiple projects → split implications across each project's file
  - ✅ wiki-coach updated: picks up `quick_highlights_*.md` first, trusts pre-mapped connections
  - ✅ Inbox restructured: `_daily_note/` and `_journal/` subfolders; articles flat in `文章/`

- **Skill System Consolidation (✅ COMPLETE - 2026-06-07):** Skills aligned with current architecture
  - ✅ `coach-session` skill: wiki relevance surfacing (on by default); project scan (reads active project headers, loads Next Steps + Trial_Log for recently updated projects); coaching insights removed — insights stay in output or escalate to POS signal; compact output format (delta-only Open Items, "Patterns Worth Naming" replacing "High-Impact Insights"); stale naming references fixed
  - ✅ `wiki-lint` skill: `entity` added as 5th page type; Check 10 (page density — flag >800 words or 5+ `(new)` prefixes); Check 11 (entity gaps — people/books referenced 3+ times without their own entity page)
  - ✅ `wiki-coach-kms-cli` skill: `entity` added as 5th page type with synthesis guidance
  - ✅ `coaching_discussion` naming convention unified across all skills and output files
  - ✅ Coaching consolidation: `coaching_insight` + `_adhoc` files merged into `coaching_discussion_YYYYMMDD.md`; 6 old files deleted; 13 internal links updated

- **Watchlist System (✅ COMPLETE - 2026-06-07):** Structured personal collection replacing iOS_capture.md
  - ✅ `_watchlist.md` restructured into 8 category sections (Film/TV, Book, Show & Performance, Person, Place, Recipe, Workout & Exercise, Tech & Tools)
  - ✅ 7-column format: Name | Note | URL | Type | Status | Date
  - ✅ `type: ref` (keep as link) vs `type: process` (annotate → wiki synthesis)
  - ✅ `_watchlist_inbox.md` staging file: Apple Shortcut appends; wiki-coach sorts each run
  - ✅ Apple Shortcut designed: unified URL (share sheet) + text (manual) flow; category picker; hardcoded `ref`
  - ✅ wiki-coach updated: sort step + `process+done` flagging in coaching session
  - ✅ `summary:` property backfilled on all 59 文章 + YT files; auto-generated for new files

- **Daily Workflow Automation (✅ COMPLETE - 2026-06-16):** Zero-friction daily data capture + morning briefing
  - ✅ AutoSleep → `sleep_log.md` automation: iOS Personal Automation at noon daily, appends block (Time Asleep dict + Readiness dict + Note field), silent/no interaction required
  - ✅ `/priming` morning skill: Typeless transcript → processes against POS + priorities + sleep + both calendars + coaching files → (A) warm daily note block with main goal/top 3/schedule/energy/POS nudge, (B) self-contained dark-mode HTML card in `03_output/priming/`
  - ✅ `calendar_scheduler_v3.py --today` flag: returns JSON with both training + main calendar events for today; reuses existing `fetch_events()` method
  - ✅ Laptop wake automation: `pmset repeat wakeorpoweron MTWRF 07:00:00` + `caffeinate -i` launchd agent (com.michael.caffeinate) — Mac wakes and stays awake for WeChat → Claude Code morning workflow

---

## Connections

**Parent Pillar:** [[LifeManagement]] (cross-pillar tags: [[Career]], [[CreativityCuriosity]])

**Related Pages:**
- [[KMS-System-Design]] — System architecture and long-term vision
- [[Daily-Note-Workflow]] — Daily capture and brain dump
- [[Wiki-Organization]] — Pillar and page structure

**Related Coaching Sessions:**
- [[coaching_20260503]] — KMS architecture review
- [[coaching_20260516]] — Phase 2.2 completion: skill updates, project standardization, link cleanup

**Related Projects:**
