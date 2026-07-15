---
name: "coach-session"
description: "Run an ad-hoc coaching session without wiki processing — either an open check-in or focused on a specific question or challenge."
---

# Ad-Hoc Coaching Session Skill

Generate a priority-aware coaching session on demand — no inbox, no wiki updates, no preparation required. Use for open check-ins or when you want to think through a specific question or challenge.

---

## Two Modes

**Open check-in** — No topic needed. Claude loads recent context and surfaces what seems most alive or unresolved right now.

**Topic-focused** — You provide a specific question or challenge (e.g., "I want to think through my manager conversation" or "help me decide between Movement Lab and content creation"). Claude loads relevant wiki page context and coaches around that specific thread.

Both modes can be combined: "Open check-in, but I also want to dig into X."

---

## What This Skill Loads

1. `/00_system/_priority.md` — Current P1/P2/P3 priorities
2. `/00_system/_POS.md` — Personal Operating System (constraints, patterns, patches)
3. Most recent `coaching_YYYYMMDD.md` from `/01_raw/coaching/` — for continuity and progress tracking
4. **Project headers + changelog:** Read the YAML header of each active project in `/04_project/`. If any project's `updated` date is more recent than the last coaching session, read its `## Next Steps`, recent `Trial_Log` entries, and any strategy/discussion notes in the project folder — surface relevant changes in coaching. The goal is to catch project-level decisions and discussions that haven't yet propagated into coaching context.
5. **Wiki relevance pass (on by default):** Search `/02_wiki/` for pages relevant to current priorities that haven't surfaced in recent coaching sessions — surface as "you already know this" prompts. Skip with explicit `/coach-session no-relevance`.
6. **If topic provided:** Search `/02_wiki/` for 1–2 most relevant pages and extract key insights

Do NOT process the inbox. Do NOT update any wiki pages. This skill is read-only except for its output.

---

## Coaching Session Structure

### For Open Check-In

```
## Coaching Check-In — [Date]

### What's Live Right Now
[Based on priorities + recent coaching session + project updates: what's unresolved, in motion, or asking for attention — 3–5 items max, 1–2 sentences each]

### Progress Since Last Session
[Only what moved — resolved items ✅, new items that emerged. Don't re-list unchanged open items.]

### What Deserves Focus Today
[1–2 things that feel most alive or most stuck; lean on POS patterns to frame — keep tight]

### Experiment Suggestions
[2–3 concrete, small experiments; one sentence each]

### Patterns Worth Naming (if any)
[Only if a cross-cutting POS pattern emerged — 2–4 compact bullets. One concrete move per pattern. No sub-sections.]
```

### For Topic-Focused Session

```
## Coaching Session — [Topic] — [Date]

[Each question/topic: 1–2 paragraphs, no internal sub-headers. Core answer + one concrete move inline.]

---

## Open Items (delta)
✅ [resolved item] — one line why
→ [new or changed item] — one line what
[Carry-forwards not mentioned = still live; don't re-list them]

---

## Patterns Worth Naming (if any)
[Only if a cross-cutting POS pattern emerged — 2–4 compact bullets. One concrete move per pattern. No sub-sections.]
```

**Format rules:**
- Each response section: max 2 paragraphs, no bold sub-headers within the section
- Open items: delta only — what resolved and what's new/changed; not a full re-list
- Patterns Worth Naming: only if something genuinely cross-cutting emerged; skip the section if not
- Never repeat the same content across sections — if it's in the response body, it doesn't appear again in Open Items or Patterns

---

## Closing Every Session

At the end of every session, regardless of mode:

### POS Signals

If any pattern emerged that could update `_POS.md`, flag it in the standard signal format for the next `/pos-update` run:

```markdown
## Signal: [Name]

- **Type:** Patch Evidence / Contradiction / New Pattern / Obsolete
- **_POS Section:** [Section number]
- **Evidence:** [Brief description]
- **Source:** [[coaching_YYYYMMDD]] or [[relevant_wiki_page]] — must be a specific link
- **Date:** YYYY-MM-DD
```

**Source field is mandatory and must be specific.** Use `[[coaching_YYYYMMDD]]` as the primary source. If the signal was triggered by a specific wiki page discussed in the session, include that too (e.g., `[[coaching_YYYYMMDD]], [[Identity-Based-Life-Philosophy]]`).

Do NOT write signals to the signal file directly — present them to the user as proposals. The user confirms before anything is saved.

### Project Sync

If any coaching conclusion directly changes the strategy, framing, or next steps of a specific project, propose a project update — same pattern as POS signals: present to user, write only after confirmation.

```markdown
## Project Update Proposal: [ProjectName]

- **File:** `04_project/[ProjectName]/[ProjectName].md`
- **Section:** [## Next Steps / ## Open Decisions / Overview]
- **Proposed change:** [What to add, update, or close off]
- **Reason:** [What in this coaching session prompted it]
```

Do NOT write to project files directly — propose only. The user confirms before anything is saved.

---

## Output File

Save the session as:
`/01_raw/coaching/coaching_YYYYMMDD.md`

All coaching sessions use this single naming convention — no `_session` or `_discussion` suffix.

---

## Instructions for Running

1. **Access KMS** — vault at `/Users/michael_zhang/Library/Mobile Documents/iCloud~md~obsidian/Documents/KMS`
2. **Load context** — Read `_priority.md`, `_POS.md`, and the most recent `coaching_YYYYMMDD.md` from `/01_raw/coaching/`
3. **Project scan** — Read YAML header of each active project in `/04_project/`; for any project updated since last coaching session, read `## Next Steps`, recent Trial_Log entries, and any strategy/discussion notes in the project folder. Catch project-level decisions that haven't yet propagated into coaching context.
4. **Wiki relevance pass (on by default)** — Search `/02_wiki/` for pages relevant to current priorities not recently surfaced; prepare 3–5 "you already know this" prompts. Skip if user passes `no-relevance` flag.
5. **If topic given** — Search or directly load 1–2 relevant wiki pages
6. **Determine mode** — open check-in, topic-focused, or both
7. **Generate session** using the appropriate structure above
8. **Close with** — any POS signals to propose, and any Project Sync proposals if coaching conclusions affect a specific project's strategy or next steps
9. **Save output** to `/01_raw/coaching/coaching_YYYYMMDD.md`
10. **Confirm** — tell the user what was saved, what signal proposals are pending their approval, and what project updates are proposed

---

## Key Rules

- Read-only except for the output coaching discussion file and confirmed project/POS updates
- Never update wiki pages, indexes, or `_POS.md` directly
- Never write to `_inbox/` — coaching insights are no longer kept; insights either land in the coaching output itself or as POS signals
- **POS signal Source field must be a specific `[[link]]`** — never generic or blank
- **Project Sync proposals require user confirmation** — never write to project files directly
- Use `[[simple_link]]` format for all internal references
- Keep coaching grounded in `_POS.md` patterns and current priorities — avoid generic life coaching
- Wiki relevance pass is on by default for open check-ins; suppress with `no-relevance` flag
- Project scan is always on; read full project content (not just headers) for any project updated since last coaching session

