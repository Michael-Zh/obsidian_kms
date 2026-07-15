---
name: "pos-update"
description: "Batch process _POS signals, group similar patterns, and update your Personal Operating System based on evidence"
---

# _POS Update Skill

Process accumulated _POS signals on-demand. This skill groups similar signal patterns, presents them with context, and helps you decide which warrant updates to your Personal Operating System.

---

## How to Use This Skill

**Trigger:** Manual, on-demand (no fixed schedule)

**When to run it:**
- After 2-4 weeks of signal accumulation
- After completing a major priority
- When you feel your self-model has shifted
- Before quarterly priority review
- Whenever you want to consolidate learnings

**Example prompt:**
- "Process my recent _POS signals"
- "What patterns have emerged in my signals since 2026-05-01?"
- "Help me batch-process _POS updates"

---

## What This Skill Does

### Step 1: Load Your Signal Files

I'll scan `/00_system/POS_signal/` and load all signal files created since your last processing.

**What I'm looking for:**
- All `.md` files in the POS_signal folder
- Extract: Type | _POS Section | Evidence | Source Links | Context | Date

**You provide (if needed):**
- Optional: "Process signals from [date] to [date]" (if you want a specific range)

### Step 2: Group Similar Signals

I'll cluster signals by pattern/category and identify:
- How many times this pattern appeared
- Where in your _POS it connects
- Confidence level (1 signal = low, 3+ signals = high)
- Related source links

**Example grouping:**
```
GROUP: "Satisficing Patch Working" (3 signals)
├─ From: coaching_session_2026-05-03
├─ From: daily_note_2026-05-05
├─ From: daily_note_2026-05-12
└─ Confidence: High (repeated across 1 week)

Pattern: You've set boundaries as "good enough" (sleep baseline, investment allocation, apartment design) 
instead of pursuing perfection. Analysis paralysis has decreased.

_POS Connection: Section 1.3 (Decision Paralysis Patch)
```

### Step 3: Present Groups with Context

For each group, I'll show:
- **Pattern Summary:** What emerged
- **Relevant _POS Section:** What would be updated
- **Source Evidence:** Links to all signals with brief context
- **Your Decision Prompt:** Three options

### Step 4: You Decide

For each signal group, you choose:

**Option A: "Yes, Update _POS"**
- I update the relevant section in `/00_system/_POS.md`
- I log the change to `/00_system/_POS_changelog.md` with:
  - Date of processing
  - What changed
  - Evidence (signal sources)
  - Your decision

**Option B: "No, Don't Update"**
- Signal remains in files (audit trail preserved)
- Logged as "Reviewed but not updated"
- Can revisit in future processing

**Option C: "Ask Me Later / Need More Data"**
- Signal group flagged for next processing run
- Not applied yet, but marked for reconsideration

### Step 5: Generate Output

I'll provide:

1. **Processing Summary Report:**
   - Groups reviewed
   - Decisions made
   - Changes applied
   - Flagged for later

2. **Updated _POS.md** (if you approved updates)
   - Relevant sections updated with new evidence

3. **Updated _POS_changelog.md**
   - Full audit trail of all decisions
   - Timestamp + evidence + rationale

---

## What I Need From You

**Minimal:** Just say "Process my _POS signals" and I'll handle the rest.

**With detail:** Specify:
- Date range (e.g., "signals from May 1-15")
- Focus area (e.g., "focus on Career signals only")
- Processing mode (e.g., "group by _POS section" vs. "group by priority")

**During the process:** 
- I'll present each group and ask for your decision
- You respond with: "Yes" / "No" / "Later" + optional notes
- I update files accordingly

---

## Special: Processing Project Completions

When projects are marked as `completed` or `one day`:

1. **Extract Learnings:** Review project's `_[ProjectName]_trial_log.md` and `_overview.md`
   - Identify key insights, patterns, surprises
   - Note what worked vs. what didn't

2. **Create POS Signals:** Convert learnings → POS signals
   - Example: "Project X succeeded because we applied satisficing approach from _POS section 1.3"
   - Example: "Project Y failed because we ignored constraint from _POS section 2.1"
   - Append as signals to active signal file

3. **Document Reflection:** Optionally write reflection in daily note
   - User can reflect anytime during project (not just at completion)
   - Coaching reads daily note → surfaces learnings in future sessions
   - Becomes part of natural input flow

---

## Signal Processing Workflow

### What Signals Look Like

Each signal file contains entries like:

```markdown
## Signal: "Satisficing working faster than expected"

- **Type:** Patch Evidence
- **_POS Section:** 1.3 (Decision Paralysis)
- **Source:** [[coaching_session_2026-05-03]], [[daily_note_2026-05-03]]
- **Evidence:** You set 7hrs sleep baseline as "good enough" without perfect optimization
- **Related Context:** [[Daily-Habits-and-Sleep-Optimization]]
- **Date Collected:** 2026-05-03
```

### File Structure You Already Have

```
/00_system/
  /_POS.md                           ← Your current operating system
  /_POS_changelog.md                 ← History of all updates
  /POS_signal/
    /POS_signal_20260101.md          ← Signals from Jan 1 - Apr 2
    /POS_signal_20260403.md          ← Signals from Apr 3 onwards
    /POS_signal_20260510.md          ← Latest signals
```

---

## How I Group Signals

I'll identify signal clusters across dimensions:

**By _POS Section:**
- All signals that reference Section 1.3 (Decision Paralysis) grouped together
- All signals that reference Section 2.3 (Relationship Protocol) grouped together
- Etc.

**By Pattern Type:**
- "Patch Evidence" (your solution is working)
- "Contradiction" (you're behaving differently than documented)
- "New Pattern" (something emerging that isn't yet in _POS)
- "Obsolete" (documented pattern no longer applies)

**By Confidence:**
- 3+ signals = High confidence
- 2 signals = Medium confidence
- 1 signal = Low confidence (might need more data)

**By Recency:**
- Recent signals prioritized (what's happening now matters more)

---

## Example Processing Session

**You:** "Process my _POS signals"

**I:** *Loading signal files from /POS_signal/...*

---

**GROUP 1: "Satisficing Working" (3 signals, HIGH confidence)**

Pattern: You've set boundaries as "good enough" (7hr sleep, 80/20 investment, "good enough" apartment design) without analysis paralysis. Shows your satisficing patch is working across domains.

_POS Connection: Section 1.3 (Decision Paralysis) → Patch: "Satisficing"

Source Evidence:
- [[coaching_session_2026-05-03]] — You set 7hr sleep as minimal baseline
- [[daily_note_2026-05-05]] — You approved apartment design without perfect optimization
- [[daily_note_2026-05-12]] — You accepted 80/20 investment allocation

**Your decision: Update _POS? [Yes / No / Later]**
→ You: "Yes"
→ I update Section 1.3 with new evidence

---

**GROUP 2: "New Pattern: Autonomy vs. Commitment" (2 signals, MEDIUM confidence)**

Pattern: You're designing for flexibility and exit mechanisms (apartment redesign-able in 6 months, strategic role has learning phase, relationship has explicit decision point). This aligns with your _POS "Variable Self" but is becoming more deliberate.

_POS Connection: Section 1.5 (The "Think-Want" Confusion) or could be separate new section

Source Evidence:
- [[coaching_session_2026-05-03]] — You emphasized "flexibility" in apartment design
- [[Financial_discussion]] — You mentioned exit clauses in investment planning

**Your decision: Update _POS? [Yes / No / Later]**
→ You: "Ask me later, I need more data"
→ I flag for next processing run; signals stay in file

---

**GROUP 3: "ENM Exploration Emerging" (1 signal, LOW confidence)**

Pattern: New threads about sexual autonomy and ENM appearing in daily notes, but only 1 signal so far.

_POS Connection: Section 2.3 (Relationship Protocol) as a sub-point

Source Evidence:
- [[daily_note_2026-05-10]] — You mentioned exploring ENM as potential need

**Your decision: Update _POS? [Yes / No / Later]**
→ You: "No, too early. I'm still exploring."
→ I leave as-is; signals stay for next run

---

**Processing Complete**

**Summary:**
- ✅ GROUP 1: Applied update to Section 1.3
- ⏳ GROUP 2: Flagged for next run
- 📋 GROUP 3: Reviewed but not updated

**Output Generated:**
- `/00_system/_POS.md` updated (Section 1.3)
- `/00_system/_POS_changelog.md` updated (full audit trail)

---

## Tips for Getting the Most From This Skill

1. **Run periodically, not obsessively** — 2-4 week batches are ideal; don't process after every daily note
2. **Trust medium/high confidence groups** — If 2-3 signals point to same pattern, it's real
3. **Take time with low-confidence signals** — 1 signal might be noise; wait for confirmation
4. **Use "Later" liberally** — No pressure to decide immediately
5. **Read your _POS_changelog.md** — See your evolution over time

---

## Integration Notes

**This skill works alongside:**
- **wiki-coach-kms skill:** Generates signals continuously
- **_POS.md:** The document being updated
- **_POS_changelog.md:** The audit trail

**This skill does NOT:**
- Modify your priorities (that's separate)
- Change coaching recommendations (those reference current _POS automatically)
- Manage signal files (wikik-coach-kms appends; you don't need to organize)

---

## Ready?

Just tell me:
- "Process my _POS signals" (I'll load all new signals since last processing)
- "Process signals from May 1-15" (specific date range)
- Or any specific question about your signals

I'll handle the rest: load, group, present, decide, update.
