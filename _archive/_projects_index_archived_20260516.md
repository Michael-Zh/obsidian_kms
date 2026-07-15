---
updated: "2026-05-04"
description: "Lightweight index of all projects for efficient querying and wiki integration"
---

# Projects Index

Complete inventory of all active, on-hold, and completed projects. Use this index for efficient project discovery without loading individual project folders.

---

## Active Projects

| Project Name | Status | Pillar | Current Focus | Priority | Last Updated | Related Pages |
|---|---|---|---|---|---|---|
| [[AI_assistant]] | active | LifeManagement | Phase 2.1-2.2: Module 2 database design + Project template integration | P1 | 2026-05-04 | [[KMS-System-Design]], [[Daily-Note-Workflow]], [[Wiki-Organization]] |
| [[Road to 2040 Investment Blueprint]] | active | Finance | Q2 2026: Bucket 1 automation setup + Bucket 2 growth kickoff | P1 | 2026-05-04 | [[Retirement Planning]], [[Surrogacy Planning]], [[Dutch Tax Optimization]] |
| [[Strategic Relationship Audit & Cohabitation Roadmap]] | active | Relationships | Phase 1: Internal audit + disclosure meeting planning | P2 | 2026-05-04 | [[Partnership Authenticity]], [[Autonomy vs Commitment]], [[Future Planning]] |
| [[Hybrid Athlete OS: Danseur Noble Master Ecosystem]] | active | PhysicalHealth | Body recomposition: 86-87kg, 43kg+ muscle, <10% BFM | P2 | 2026-05-04 | [[Movement & Dance]], [[Nutrition Mastery]], [[Body Composition]] |
| [[Anti-Aging Skincare Optimization: Home + Travel]] | active | AdminHome | Spring 2026: Shopping strategy + China travel routine prep | P3 | 2026-05-04 | [[Anti-Aging Strategy]], [[Travel Preparation]] |

---

## On Hold / Paused Projects

| Project Name | Status | Pillar | Reason on Hold | Last Updated |
|---|---|---|---|---|
| (None currently) | — | — | — | — |

---

## Completed Projects

| Project Name | Status | Pillar | Completion Date | Key Learnings |
|---|---|---|---|---|
| (None yet logged) | — | — | — | — |

---

## Project Template Reference

**Each project uses the standardized 8-section template:**
1. YAML Frontmatter (name, status, pillar, current_focus, dates, priority, tags)
2. Overview
3. **Objectives & Goals**
4. **Roadmap** (flexible: "Modules & Roadmap" for product projects OR "Research Questions/Topics" for research projects)
5. Next Steps
6. **Open Decisions/Questions**
7. Accomplishments
8. Connections

**Each project has a companion Trial Log (5 sections):**
1. Header (with Purpose Statement)
2. Trial Log Format table (Date | Experiment | Result | Learning | Decision)
3. Notes & Context
4. **Decisions, Blockers & Pivots** (merged)
5. Reflection Entries

---

## How to Use This Index

### For Wiki Processing
When wiki-coach-kms-cli processes a daily note:
1. Query this index for related active projects by **Pillar** or **Related Pages**
2. Load only relevant project overview files (not all projects)
3. Add "Related Projects" section to page file
4. Keep bidirectional link maintained (quest ← → project)

### For Coaching Sessions
When generating coaching output:
1. Load this index (active projects only)
2. Filter by **Priority** (P1 projects relevant to current priorities)
3. Reference aligned projects in coaching output
4. Suggest new projects if insights warrant (check index first to avoid duplicates)

### For Project Queries
To find projects:
- **By Pillar:** Search by pillar name (e.g., "Finance" → Investment Blueprint, potentially others)
- **By Status:** Filter by active/on-hold/completed
- **By Priority:** Find P1 (top focus) vs. P3 (background) projects
- **By Quest:** Look at "Related Pages" column to see project-quest connections

---

## Maintenance Notes

**Update this index when:**
- [ ] New project created (add row to Active Projects)
- [ ] Project status changes (active → on-hold / completed)
- [ ] Project relationships change (add/remove quests)
- [ ] Weekly/monthly: Update "Last Updated" and "Current Focus" for active projects

**How to update:**
- Manually edit this file directly (lightweight)
- Or use Obsidian CLI `append` command to add rows
- Keep format consistent (use markdown table format)

---

## Index Statistics

- **Total Active Projects:** 5
- **By Pillar:**
  - LifeManagement: 1 (KMS)
  - Finance: 1 (Investment Blueprint)
  - Relationships: 1 (Strategic Relationship Audit)
  - PhysicalHealth: 1 (Training)
  - AdminHome: 1 (Skincare)
  - Career: 0
  - CreativityCuriosity: 0
  - Travel: 0
  - MindMentalHealth: 0 (cross-tagged in Relationships project)

- **By Priority:**
  - P1: 2 (KMS, Investment)
  - P2: 2 (Relationships, Training)
  - P3: 1 (Skincare)

- **By Project Type:**
  - Product/System: 1 (KMS)
  - Research-Driven: 1 (Relationships)
  - Strategic: 1 (Investment)
  - Execution/Skill: 2 (Training, Skincare)

---

## Quick Links to Project Files

- KMS: `/04_project_backup/AI_assistant/AI_assistant_overview.md` (alias: KMS project)
- Investment Blueprint: `/04_project_backup/Road_to_2040_Investment_Blueprint/Road_to_2040_Investment_Blueprint_overview.md`
- Strategic Relationship Audit: `/04_project_backup/Strategic_relationship_audit/Strategic_relationship_audit_overview.md`
- Training Program: `/04_project_backup/Training_program/Training_program_overview.md`
- Skincare Routine: `/04_project_backup/Skincare_Routine/Skincare_Routine_overview.md`

---

**Last updated:** 2026-05-04  
**Maintained by:** Michael Zhang  
**Next scheduled update:** Weekly (active projects only)
