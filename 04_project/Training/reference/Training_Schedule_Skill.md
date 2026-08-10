Run the weekly training scheduler, review planned vs actual, discuss adjustments, and push to Google Calendar.

Working directory: `~/training-calendar-scheduler`
KMS base: `/Users/michael_zhang/Library/Mobile Documents/iCloud~md~obsidian/Documents/KMS/04_project/Training_program`

---

## Step 1 — Load source-of-truth files (bash, minimal reads)

```bash
KMS="/Users/michael_zhang/Library/Mobile Documents/iCloud~md~obsidian/Documents/KMS/04_project/Training_program"

# Get last 2 weekly schedule entries (line offset, not full file)
grep -n "^## Week:" "$KMS/Training_program_Weekly_Schedule.md" | tail -2
```

Use the returned line numbers to Read only the last 2 entries from `Training_program_Weekly_Schedule.md`.

Read in full (small files, needed entirely):
- `Training_program_Class_Pool.md`
- `Training_program_Scheduling_Rules.md`

Do NOT read the full Weekly Schedule file. Do NOT read training_running_log.md here — that's for monthly review only.

---

## Step 2 — Pull actual calendar events for last week

```bash
cd ~/training-calendar-scheduler
python3 calendar_scheduler_v3.py --review
```

This fetches last week's actual training calendar events. Cross-reference with the previous `## Week:` entry to build planned vs actual:

- Sessions in the plan but not in calendar → likely skipped; ask why if pattern is recurring
- Sessions in calendar but not in plan → ad-hoc addition; note it
- Flag recurring drops (same session missing 2+ weeks in a row)
- Flag any rule violations (e.g. High session on Thursday, no gym 2+ weeks running)

Summarise in 3–5 bullets. Fill in the "Actual vs Planned" placeholder in the previous week's log entry now (before planning the new week).

---

## Step 3 — Plan the new week

```bash
python3 calendar_scheduler_v3.py
```

Output is the base schedule. Cross-check against rules before presenting:
- Max 4 High sessions/week; Thursday = Light only (Iyengar default)
- Choreo cycle (Rule 9) — Jazz/Contemporary required (W2/W4) or optional (W1/W3)?
- Deload due? (Rule 6 — default every 5 weeks; hard limits 3–6)
- Mysore placement (Rule 3) — Friday primary; Thursday last resort only
- Ballet teacher priority (Rule 8) — Mon ADC ⭐⭐⭐; Thu/Fri ADC ⭐ backup
- Double session target (Rule 1) — at least one double per week

---

## Step 4 — Discuss and adjust

Present the patterns summary and proposed plan together. Ask for any adjustments:
- Swap/skip a session
- Apply deload mode
- Override due to social plan, travel, low energy, teacher absence
- Choreo cycle shift (teacher sick, etc.)

Keep it conversational. Don't re-read files during this step.

---

## Step 5 — Push and log

Once approved:

```bash
python3 calendar_scheduler_v3.py --push
```

This clears the training calendar for the week and writes the approved events.

Then append a new entry to `Training_program_Weekly_Schedule.md`:

```bash
cat >> "$KMS/Training_program_Weekly_Schedule.md" << 'ENTRY'

---

## Week: YYYY-MM-DD

**Planned (Mon DD – Sun DD):**
- Sunday HH:MM–HH:MM — [session]
- Monday HH:MM–HH:MM — [session]
- ...

**Adjustments from base schedule:** [any swaps/skips and reasons]

**Choreo cycle:** Jazz W[N] ([required/optional]), Contemporary W[N] ([required/optional])

**Actual vs Planned:** _To be reviewed on next planning session._
ENTRY
```

---

## Step 6 — Update previous week's Actual vs Planned

Edit the most recent entry that still says `_To be reviewed on next planning session._` and replace with:

```
**Actual vs Planned:**
- ✓ [sessions that matched]
- Skipped: [session] — [reason if known]
- Added: [session] — [ad-hoc]
- Observation: [one line if pattern emerging]
```

Use the `--review` output from Step 2. Do this as a targeted Edit, not a full file rewrite.

---

## Technical reference

- **Hard conflicts** (block scheduling): shows, office hours, company events, social events
- **Soft conflicts** (suggest moving): Dinner, Lunch, Breakfast, Sauna, Bath, Shower
- **Naming tip**: "Social: X", "Show: Y" in calendar events improves conflict detection
- **Token efficiency**: never read the full Weekly Schedule file; always use grep line offset → targeted Read

## Files
- `calendar_scheduler_v3.py` — main script (`--review`, `--push`, `--json` flags)
- `Training_program_Weekly_Schedule.md` — weekly planning log (append only; awk/grep for reads)
- `.google_token.pickle` — OAuth token (auto-refreshes; browser re-auth only if revoked)
- `Training_program_Class_Pool.md` — class intensity + priority source of truth
- `Training_program_Scheduling_Rules.md` — 9 scheduling rules
