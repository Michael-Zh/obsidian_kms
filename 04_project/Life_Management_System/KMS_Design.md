# KMS Design — Pipeline Architecture & Info Flow

> Detailed design extracted from Life_Management_System.md on 2026-08-09 during LMS restructuring.

## Three-Layer Architecture

The KMS is built on three distinct layers with clearly separated purposes.

### Layer 1 — Raw Input (`01_raw/`)
The unprocessed stream. Source-agnostic: brain dumps, web clips, transcripts, ebooks, coaching responses from later reflection, digests of interesting conversations, answers to open coaching questions.

Rule: **if it hasn't been synthesized yet, it belongs here.** Raw inputs are immutable — never edited after capture.

### Layer 2 — Wiki (`02_wiki/`)
The synthesis layer. Answers the question: *"what do I know about X?"* Timeless, pillar-organized, AI-generated from whatever came through the inbox. Should almost never be written directly into — that's the wiki-coach skill's job. If you feel the urge to add something directly to a page, that's a signal it should go to `_inbox/` first.

Each wiki page has a `type`:

| Type | What it captures | Example |
|------|-----------------|---------|
| **concept** | Abstract framework, philosophy, identity pattern | `Identity-Based-Life-Philosophy` |
| **practice** | Active protocol, routine, habit with experiment results | `Sleep-Optimization-Routine` |
| **topic** | Domain being explored — open questions, evolving understanding | `Portfolio-Career-Design` |
| **synthesis** | Generated analysis or comparison filed back into wiki | LLM comparison, preserved as a page |
| **entity** | Person, book, or named artifact | `James_Clear`, `Atomic_Habits` |

### Layer 3 — Coaching Outputs
The temporal action layer. Answers: *"what should I do now, given my current priorities?"* Dated, contextual, tied to a moment. These are not synthesized into the wiki — they stay as-is, and become source material for the inbox if you write responses later.

### The Bridge — `project_overview.md`
The durable action layer (what projects exist, what's worth pursuing). Sits between coaching (ephemeral guidance) and wiki (durable knowledge). Updated after each coaching run.

### The Feedback Loop
Coaching generates questions → you answer them later → answers go to `01_raw/` as `coaching_insight_YYYYMMDD.md` → next wiki-coach run synthesizes your answers into wiki pages → those pages inform richer future coaching.

---

## Article Ingestion — Annotation-First Design

Articles and long-form content follow a special path that preserves personalization.

**Why annotation-first?** Without personal relevance framing, raw articles synthesize into impersonal digests. Annotating directly in the article YAML keeps the workflow minimal and the output personal.

**The workflow:**
1. **Capture** → bijitongbu saves full article to `01_raw/文章/` (flat, no date subfolders; automatic, one tap)
2. **Annotate in Obsidian** → open the article, add `annotation:` property:
   - Regular: answer 3 questions (what struck you / why now / action or contradiction)
   - Full synthesis: set `annotation: full article`
   - No annotation: article skipped until annotated
3. **Process** → run `/wiki-coach-kms-cli`
   - Scans YAML-only for all articles (token-efficient via `kms_search.py meta`)
   - Loads article body ONLY if `annotation: full article`
   - For regular annotations: annotation text IS the synthesis input
   - Unannotated articles silently skipped
4. **Archive** → raw articles stay in `01_raw/` permanently

---

## Directory Structure

```
/KMS
  /00_system                      <-- System Instructions (LLM Logic)
    /_POS.md                      <-- Personal Operating System
    /_priority.md                 <-- Current priorities & sequencing
    /POS_signal/                  <-- Signal files (daily-rotating)
    
  /01_raw                         <-- Immutable Sources (Archive)
    /_daily_note/                 <-- Daily notes
    /_journal/                    <-- Written reflections, quick highlights
    /_ebooks/                     <-- eBook extracts
    /文章/                          <-- Full articles (flat, no date subfolders)
    /YT/                          <-- YouTube clips (Obsidian Web Clipper)
    /coaching/                    <-- All coaching sessions
    _watchlist.md                 <-- Watchlist by category
    _watchlist_inbox.md           <-- Staging file (Apple Shortcut appends here)
    
  /02_wiki                        <-- Persistent Knowledge Artifacts
    /_log.md                      <-- Chronological change record (prepend)
    /_processed_log.md            <-- Input files processed tracker
    /lint/
      /_lint_queue.md
      /wiki_lint_YYYYMMDD.md
    /[Pillar]/
      /_[Pillar]_Index.md
      /[Page].md
      
  /03_priming                     <-- Morning priming HTML cards
    /priming_YYYYMMDD.html
    
  /04_project                     <-- Projects (Action-Oriented)
    /project_overview.md
    /[ProjectName]/
      /[ProjectName].md
      /CLAUDE.md
```

---

## 8 Pillars

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

## Input → Wiki → Coaching Workflow

```
INPUT (daily note, web clip, transcript, etc.)
  │
  ├─→ Wiki Process
  │   ├─ Extract themes → Assign to pillars
  │   ├─ Find related pages (Obsidian CLI search)
  │   ├─ Merge intelligently with existing content
  │   ├─ Update /02_wiki pages + indexes
  │   ├─ Prepend to _log.md
  │   └─ Append signals to /00_system/POS_signal/
  │
  └─→ Coaching Process (PARALLEL)
      ├─ Load same input + current priorities
      ├─ Load _POS.md constraints
      ├─ Filter insights through priorities
      ├─ Generate actionable coaching session
      └─ Append signals to /00_system/POS_signal/

RESULT: Both wiki updates (neutral) + coaching guidance (priority-filtered)
from one input
```

---

## Roadmap Status

| Module | Status | Purpose |
|--------|--------|---------|
| 1a — Apple Shortcuts capture | ✅ Complete | URL share → _watchlist_inbox.md |
| 1b — Article annotation | ✅ Complete | bijitongbu + annotation-first |
| 2 — Input sorting | ✅ Complete | _watchlist.md by category |
| 3 — Web content extraction | ✅ Complete | bijitongbu + Web Clipper |
| 4 — Entity processing | 🔵 Next | type:process → annotation → wiki |
| 5 — Daily Note inbox | ✅ Complete | Brain dump capture |
| 6.1 — Wiki generation | ✅ Complete | wiki-coach-kms-cli skill |
| 6.2 — Coaching generation | ✅ Complete | Progress Update + project-context |
| 6.3 — Instant implication | ✅ Complete | /quick-read skill |

**Phase History:**
- Phase 1: Capture infrastructure ✅
- Phase 2.1–2.10: Input routing, project templates, watchlist, annotation, web capture, summaries, quick-read, daily automation ✅
- Phase 3 (Next): Module 4 — Entity processing from watchlist
