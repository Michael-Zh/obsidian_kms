---
name: Life_Management_System
project_id: pj0001
status: active
type: meta-system
pillar: LifeManagement
current_focus: "5-module architecture map — does not produce backlog items. Detailed KMS design at KMS_Design.md."
created: 2026-05-03
updated: 2026-08-09
target_completion: ongoing
priority: P1
tags:
  - LifeManagement
---

# Life Management System (LMS)

LMS is the **architecture map** for Michael's personal operating system. It defines the boundaries and relationships between five modules. It does NOT produce backlog items — each module has its own project folder for execution.

---

## Five Modules

| Module | Description | Project Folder |
|--------|-------------|----------------|
| 1. KMS (知识管理) | Daily notes → wiki synthesis pipeline, skill definitions, templates, info flow design | `KMS_Design.md` (this folder) |
| 2. Overall Life Coaching (全面生活教练) | Cross-project pattern recognition, POS updates, life direction coaching | `01_raw/coaching/` |
| 3. Training Program (训练计划) | Training philosophy, weekly rules, class pools, recovery strategies | `Training/` |
| 4. Project Coaching (独立项目跟进) | Each project has its own CLAUDE.md — a protocol, not a folder | Per project |
| 5. Daily Operations (日常执行层) | Priming, backlog prioritization, scheduling. Meal prep is independent (5d) | Danseur Noble Hub App |

---

## Data Flow

```
01_raw (input) → wiki-coach skill → 02_wiki (synthesis)
                                  → coaching sessions (guidance)
                                  → POS signals (pattern detection)

KMS Obsidian (strategy) → GitHub Action sync-context → Supabase (execution data)
                                                       → Danseur Noble Hub App (daily interface)

App coaching decisions → Push to Obsidian → KMS project docs
```

---

## Skills Index

System-level skills and which module they serve:

| Skill | Serves Module(s) | Purpose |
|-------|-----------------|---------|
| wiki-coach-kms-cli | KMS + Coaching | Raw input → wiki synthesis + coaching output |
| priming | Daily Ops | Typeless transcript → daily brief + Top 3 |
| training-coach-context | Training | Load training context from Supabase |
| training-schedule | Training + Daily Ops | Weekly training schedule planning |
| project-context | Project Coaching | Load single-project CLAUDE.md context |
| project-review | Project Coaching | Cross-project priority review |
| coach-session | Coaching | Ad-hoc coaching without wiki processing |
| schedule-week | Training + Daily Ops | Weekly scheduling with calendar integration |
| quick-read | KMS | Instant implications from a specific source |
| wiki-lint | KMS | Periodic wiki health check |
| pos-update | Coaching | Batch process POS signals, update operating system |
| consolidate-memory | KMS | Memory file maintenance |

---

## Architecture Decisions

- **2026-08-09:** LMS restructured — extracted KMS design details to `KMS_Design.md`. App documentation moved to `Danseur_Noble_Hub/`. Training concept layer consolidated under `Training/`.
- **2026-07-21:** Two-layer architecture confirmed — KMS = Strategy Layer, App = Execution Layer.
- **2026-07-24:** CC Backlog Sync implemented — coaching sessions push action items directly to App DB.

---

## Related

- [[Danseur_Noble_Hub]] — App execution layer
- [[Training_Program]] — Training philosophy + rules
- [[Meal_prep_routine]] — Nutrition system design
