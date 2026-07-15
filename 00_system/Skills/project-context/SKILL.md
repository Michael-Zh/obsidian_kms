---
name: "project-context"
description: "Generate or refresh a CLAUDE.md context file for a project, pulling from the project folder and related wiki pages. Use before starting a focused project session in Claude Projects."
---

# Project Context Skill

Generate or refresh a `CLAUDE.md` context file for a specific project. That file becomes the persistent context when you open the project folder in Claude's Projects feature — so every conversation starts with full awareness of the project's objectives, current state, related wiki pages, and working agreements.

**Use this skill when:**
- Starting a focused working session on a project
- The project has evolved significantly and the context needs refreshing
- Kicking off a new project for the first time (after `/Project-Initiation`)

**The result:** A `CLAUDE.md` inside `/04_project/[ProjectName]/` that Claude reads automatically whenever you open that folder as a Project.

---

## What the Skill Reads

For the named project, load the following (summaries only — read depth on demand):

1. **`[ProjectName].md`** — Full read (objectives, roadmap, current focus, open decisions, **`## Next Steps`** — this is the project backlog, load in full)
2. **Trial / check-in log** — Look for `[ProjectName]_Trial_Log.md`, `[ProjectName]_Weekly_CheckIn_Log.md`, or any similar log file in the project folder. Load last 5–10 entries if it exists; note explicitly in Current State if it doesn't exist yet (and name the file that should be used).
3. **Related wiki pages** — Found via the overview's `Connections` section; load each page and extract 2–3 key insights
4. **`_in_case_you_are_bored.md`** — Scan for any pending items referencing this project
5. **Most recent coaching session** — Scan for any mentions of this project

---

## What the Skill Generates

A `CLAUDE.md` file saved to `/04_project/[ProjectName]/CLAUDE.md` with this structure:

```markdown
# Project Context: [ProjectName]
_Last updated: YYYY-MM-DD_

## What This Project Is

[2–3 sentence compressed summary: what it is, why it matters, what phase it's in]

**Primary Pillar:** [Pillar]
**Status:** [active / in dev / one day]
**Current Focus:** [current_focus from YAML]
**Priority:** [P1 / P2 / P3]

## Objectives

[Paste the 3 core goals from the overview verbatim — these are the north star]

## Current State & Recent Progress

[Summary of last 3–5 log entries: what was tested, what was learned, any decisions made]

**Open decisions / blockers:**
[List from overview's Open Decisions section]

## Pending Next Steps

[Full contents of ## Next Steps from [ProjectName].md — these are the backlog items to discuss this session]

## Related Wiki Pages

[For each related page: one line summary + the 2–3 most relevant insights]

- **[[Page_Name]]** — [one-line description]
  - [Key insight 1]
  - [Key insight 2]

## Other Pending Items (from _in_case_you_are_bored)

[Any items referencing this project from _in_case_you_are_bored.md — concrete actions, open decisions not yet in Next Steps]

## File Map

Read these files when you need depth:

| File | When to read |
|------|--------------|
| `[ProjectName].md` | Full context, roadmap, all decisions, current Next Steps |
| `[LogFileName].md` | Session log — entries added at the end of each conversation |
| `[Page_Name]` — `/02_wiki/[Pillar]/Page_Name.md` | Deep context for [topic] |

## Working Agreement

You are acting as a **thought partner and analyst** for this project. Your role is to:

- Help think through problems, hypotheses, and next experiments
- Connect new information to existing wiki pages, decisions, and patterns
- Challenge assumptions when appropriate — especially around complexity vs. simplicity trade-offs
- Reference `[LogFileName].md` when discussing past learnings
- Use `[[simple_link]]` format for all internal references
- **Start each session by reviewing Pending Next Steps** — triage, discuss, or action them before moving on

**At the end of each conversation:**
1. Summarize any insights, decisions, or new information worth preserving
2. When wrapping up, propose a single log entry for `[LogFileName].md` covering all discussions and decisions from the session — formatted and ready to paste, including date, decisions made, and food for thought for future reference
3. Propose any updates to `## Next Steps` in `[ProjectName].md` (items to add, check off, or remove)
4. **If the conversation changed the project strategy, framing, or open decisions** — propose the specific update to the Overview or Open Decisions section in `[ProjectName].md`
5. Wait for approval before writing anything
6. If a wiki page should be updated, note which one and what the addition would be

**Prompt occasionally** during longer sessions: "Good stopping point — want to wrap up and capture what we've covered so far?"

**Do not** rewrite existing content — only propose additions.
```

---

## Instructions for Running This Skill

When invoked with a project name:

1. **Access KMS** — vault at `/Users/michael_zhang/Library/Mobile Documents/iCloud~md~obsidian/Documents/KMS`

2. **Confirm project folder exists** — look in `[KMS]/04_project/[ProjectName]/`. Get the project's YAML metadata without loading the full file:
   ```bash
   # $KMS = /Users/michael_zhang/Library/Mobile Documents/iCloud~md~obsidian/Documents/KMS
   # In VM bash: /sessions/<session>/mnt/KMS
   python3 "$KMS/00_system/kms_search.py" meta ProjectName
   ```

3. **Read overview and trial log** — full read of `[ProjectName].md`, paying special attention to `## Next Steps` (this is the session's starting agenda). Also extract the Connections section for step 4:
   ```bash
   python3 "$KMS/00_system/kms_search.py" section ProjectName "Connections"
   ```
   Then scan the project folder for any log file (`_Trial_Log.md`, `_Weekly_CheckIn_Log.md`, etc.) and note its exact filename — this is what gets referenced throughout the generated CLAUDE.md.

4. **Follow page links** from the `Connections` section → for each linked wiki page, first get metadata to confirm it exists, then load for insights:
   ```bash
   python3 "$KMS/00_system/kms_search.py" meta PAGE_NAME   # confirm page + get pillar
   ```
   Then load the full page file for 2–3 key insights per page. If a linked page doesn't exist yet, note it as a forward-looking reference rather than listing it as active — point to the closest existing wiki page instead.

5. **Scan `_in_case_you_are_bored.md`** — Read the file directly (single structured document). Look for any items referencing this project that aren't already in `## Next Steps`.

6. **Scan most recent coaching session** — List `[KMS]/01_raw/coaching/` and read the most recent `coaching_YYYYMMDD.md` for any mentions of the project.

7. **Generate `CLAUDE.md`** using the template above — compress, don't copy verbatim; paste `## Next Steps` in full. Use the actual log filename found in step 3 everywhere `[LogFileName]` appears.

8. **Save to** `[KMS]/04_project/[ProjectName]/CLAUDE.md`

9. **Confirm** to the user: "CLAUDE.md created for [ProjectName]. Open that folder as a Project in Claude to start your session."

---

## Refreshing an Existing CLAUDE.md

When the project has progressed, re-run this skill to update:
- Current state & recent progress (new log entries)
- Updated open decisions
- Refreshed Next Steps (new items added by wiki-coach since last refresh)
- Any newly linked wiki pages

The skill **overwrites** the existing CLAUDE.md with the refreshed version. Previous conversation history in the Project is unaffected.

---

## Notes

- Keep CLAUDE.md lean: summaries + file paths, not full content. Exception: `## Next Steps` is always pasted in full — it's the session agenda.
- The "Working Agreement" section is the most important part — it defines how Claude should behave in every conversation in this project context.
- Insight saving is always propose → approve. Claude never writes to project files without explicit confirmation.
- **Log entry on wrap-up:** The Working Agreement instructs Claude to propose a single log entry when wrapping up — covering the full conversation, not piecemeal after each exchange. Claude should prompt the user periodically during long sessions ("Good stopping point — want to wrap up?") to create a natural moment for this. If no log file exists yet, note that in Current State, name the file that should be created, and include it in the File Map.
- If a Connections page doesn't exist yet, list it as a forward-looking note rather than an active reference — point to the closest existing wiki page instead.
- If `## Next Steps` is empty, note that explicitly — it means either no backlog has accumulated yet, or items need to be sourced from `_in_case_you_are_bored.md`.

