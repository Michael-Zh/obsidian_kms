---
name: "project-review"
description: "Lightweight project review — load all active projects and ideas, identify what feels alive, and get a suggested priority ordering. Run monthly or when priorities feel stale."
---

---
name: "project-review"
description: "Lightweight project review — load all active projects and ideas, identify what feels alive, and get a suggested priority ordering. Run monthly or when priorities feel stale."
---

# Project Review Skill

A lightweight project review to answer: **what's alive right now, and where should my energy go?**

This isn't a formal audit. It's a quick reset when you feel scattered across too many things, when you've had a burst of new energy in a specific area, or when a wiki run has surfaced new information that might shift priorities.

**Trigger this when:**
- You've just run `/wiki-coach-kms-cli` and want to reflect on which projects it touched
- You feel like you're not sure what to focus on
- Something new happened (conversation, idea, event) that might change priorities
- Roughly monthly — whenever the current priority list feels stale

---

## What This Skill Does

### Step 1: Load the Current Picture

Read:
- `/00_system/_priority.md` — your current top 3
- `/04_project/_in_case_you_are_bored.md` — all ideas and pending items
- All active project YAML headers (no full file load) — run via bash:

```bash
# $KMS = /Users/michael_zhang/Library/Mobile Documents/iCloud~md~obsidian/Documents/KMS
# In VM bash: /sessions/<session>/mnt/KMS
python3 "$KMS/00_system/kms_search.py" projects
```

Returns: name, pillar, priority, status, current_focus, updated — no full file content.  
Only read a project's full `.md` file if the current_focus or status needs more context.

- **Most recent coaching session** — scan `01_raw/coaching/` for the most recent `coaching_YYYYMMDD.md`. For each active project, note any coaching mentions: what was said, what was deferred, what was flagged as stuck. Surface this in the snapshot as a "Last coaching mention" column so project state and coaching state are visible together.

### Step 2: Present a Snapshot

Show the current state of all active projects in a single view:

```
## Active Projects

| Project | Status | Focus | Priority | Last Updated |
|---------|--------|-------|----------|--------------|
| [[AI_assistant]] | active | Phase 2.1 | P1 | 2026-05-09 |
| [[Training_program]] | active | Recomposition | P2 | 2026-05-06 |
| ...

## Ideas Ready to Become Projects (from _in_case_you_are_bored)
[Items that have accumulated enough context to formalize]

## On Hold
[Projects with status "one day"]
```

### Step 3: Ask What Feels Alive

Prompt:
> "Which of these feel most alive or urgent right now? Which haven't moved in a while and might be worth pausing? Are there any new ideas from `_in_case_you_are_bored` that feel ready to become a project?"

The user names what's drawing energy. They don't need to justify it — inspiration is the signal.

### Step 4: Suggest Priority Ordering

Based on what the user shares, propose:
- Which 2–3 to actively work on now (P1/P2)
- Which to put on hold without guilt (one day)
- Which ideas from `_in_case_you_are_bored` are ready to formalize (suggest running `/Project-Initiation`)
- Which need a `/project-context` CLAUDE.md refresh before the next session

Priority criteria to weigh (in order):
1. **Energy signal** — What the user said feels alive
2. **Time-sensitivity** — Any hard deadlines or windows closing?
3. **Dependencies** — Does anything block something else?
4. **Strategic fit** — Does it connect to current priorities in `_priority.md`?

### Step 5: Optional Updates

If the priority ordering changes:
- Update `/00_system/_priority.md` with the new top 3
- Update project YAML headers (`priority: P1/P2/P3` and `status: active/one day`) for any shifts

---

## The Underlying Pattern

Your working style is a mix of **"waiting for invitation"** (ideas that arrive, inspire, and pull you in) and **active pursuit** (deliberate research and experimentation). Both are legitimate — this review honors that by not forcing artificial urgency on dormant projects.

The right signal to activate a project isn't always a calendar — it's when new information, an insight from a coaching session, or a burst of energy arrives. This review just makes that pattern visible and intentional rather than accidental.

---

## Recommended Cadence

- **After every wiki run:** Glance at `_in_case_you_are_bored.md` to see if anything new has surfaced
- **Monthly (or when priorities feel stale):** Run a full project review
- **After a significant life event or decision:** Run a review to see what it shifts

---

## KMS paths

- KMS vault: `/Users/michael_zhang/Library/Mobile Documents/iCloud~md~obsidian/Documents/KMS`
- Projects: `/04_project/[ProjectName]/[ProjectName].md`
- Project landscape: `/04_project/_in_case_you_are_bored.md`
- Priorities: `/00_system/_priority.md`
- kms_search CLI: `/00_system/kms_search.py`

