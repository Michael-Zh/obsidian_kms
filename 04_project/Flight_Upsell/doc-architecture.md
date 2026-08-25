---
name: doc-architecture
description: Information types and three-source sync model for the Flight Upsell project
metadata:
  type: reference
  created: 2026-08-24
  project: Flight_Upsell
---

# Flight Upsell — Doc Architecture & Sync Model

> Designed 2026-08-24. Describes how project information is classified and how the three sources (Feishu, Trip_Repo, KMS) work together.

---

## Information Types

| Type | Description | Change rate |
|---|---|---|
| **A — Project management** | WS status, tasks, meeting notes, decisions, OKR | High — changes frequently |
| **B — Data context** | BQ/HIVE table catalog, field definitions, access tools | Low — stable reference |
| **C — Analysis reports** | Diagnosis findings, data results, charts | Per analysis cycle |
| **D — SQL queries** | Reusable queries | Per analysis cycle |
| **E — Domain knowledge** | Definitions, methodology, cleanup rules, gotchas | Low — accumulates over time |
| **F — Project background** | Goals, framework, what's been done, what's ruled out | Low — core context |
| **G — Personal / career** | H1/H2 self-eval, strategic portfolio | KMS-only |

---

## Three-Source Ownership

| Source | Owns | Maintained by |
|---|---|---|
| **Feishu Hub** (`SMRpdUHgxo9U2hxOJ4ElyTMHg5f`) | A — project management (primary) | openclaw (auto) + manual |
| **Trip_Repo** (`github: Trip_Repo`) | B, C, D, E, F (primary) | Claude + Michael |
| **KMS** (`04_project/Flight_Upsell/`) | Mirror of B/C/D/E/F + G (KMS-only) | Overwrite from repo |

**Key principle**: Trip_Repo is the source of truth for all technical content. KMS is a personal mirror — overwrite, don't merge.

---

## Repo Structure

```
Trip_Repo/
  CLAUDE.md                    — AI context: data rules, SQL index, session start protocol
  learnings/
    project-context.md         — F: goals, framework, completed analyses, pitfalls, exploration directions
    data-sources.md            — B: BQ/HIVE table catalog (from Feishu "All about Data" wiki)
    *.md                       — E: domain knowledge (definitions, cleanup rules, gotchas)
  analysis/
    *.md + *.html              — C: analysis reports and charts
  sql/
    *.sql                      — D: reusable queries
```

---

## Workflow

### Session Start → `/upsell-update`

1. Fetch Feishu Hub + "All about Data" wiki
2. Full-text compare against `learnings/data-sources.md` and CLAUDE.md SQL table
3. Show diff → apply on confirm
4. Feishu Hub project status stays in session context — no need to write back to repo
5. CLAUDE.md is configured to auto-trigger this at every session start

### During Session

- Claude reads `learnings/project-context.md` as background layer
- All analysis output goes to `analysis/`, `sql/`, or `learnings/`
- Feishu Hub status available in context without re-fetching

### Session End → `/upsell-update end`

1. Identify new/modified files in `analysis/`, `learnings/`, `sql/`
2. Push to KMS: overwrite corresponding files in `04_project/Flight_Upsell/analysis/`, `learnings/`, `sql/`
3. Push to Feishu: add summary to relevant WS section + update data wiki if needed
4. `git commit` repo changes

---

## Sync Rules

| Trigger | Action |
|---|---|
| New analysis completed (`analysis/`) | Add summary to Feishu Hub relevant WS section |
| Feishu Hub has new meeting/decision | If it affects data rules → update `learnings/` or CLAUDE.md |
| New SQL added (`sql/`) | Update CLAUDE.md SQL Available table |
| Feishu data wiki updated | Sync to `learnings/data-sources.md` |
| Session ends with new output | `/upsell-update end` → KMS overwrite + Feishu push |

---

## What KMS Does NOT Store

- Live project status (tasks, WS status) — that's Feishu Hub
- Operational data (raw query results, temp tables)
- Anything already authoritative in Trip_Repo — KMS is a mirror, not a parallel source
