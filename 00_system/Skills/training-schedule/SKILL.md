---
name: "training-schedule"
description: "Plan Michael's weekly training schedule, read calendar conflicts, and allow interactive adjustments before writing to Google Calendar"
---

# Training Schedule — Interactive Weekly Planner

Plan Michael's next training week by reading Google Calendar conflicts, generating an optimal schedule based on Scheduling Rules, and allowing adjustments before writing.

## How to Use This Skill

**Start the weekly planning session:**
```
/training-schedule
```

This will:
1. Read your main calendar (shows, dinners, etc.) for unmovable events
2. Read your current training calendar
3. Generate the optimal week using your Scheduling Rules
4. Show you the proposed plan with any conflicts highlighted
5. Wait for your adjustments

**Make adjustments by telling me what you'd like to change:**
- "Swap Thursday Iyengar for Reformer at noon (KC Move)"
- "Skip Friday Mysore, I need rest"
- "Move Tuesday Contemporary to 18:45 instead of 20:15"
- "Add HJS Ballet on Friday at 09:30"
- "Delete Monday gym (too tired)"

I'll update the plan dynamically and show you the modified schedule.

**Approve and write the final plan:**
- "Write it" / "Looks good" / "Confirm"
- The training calendar will be cleared for that week and repopulated with your finalized schedule

## Base Schedule Template

This is what gets generated if there are no conflicts:

- **Sunday 15:00–16:30** — Gym: Back/Leg/Arm
- **Monday 19:00–20:15** — ADC Ballet
- **Monday 21:00–22:15** — Gym: Chest/Shoulder
- **Tuesday 20:15–21:30** — ADC Contemporary (or Salsa 19:00 + Hiphop 20:30)
- **Wednesday 19:00–20:15** — ADC Jazz
- **Thursday 18:30–19:45** — Iyengar Yoga (Light recovery day)
- **Friday 07:00–08:30** — Mysore Ashtanga (optional, check energy)
- **Saturday** — Rest

## Supported Adjustments

### Swap/Replace Classes
- **Syntax:** "Swap [Day] [Class] for [New Class] at [Time] ([Location])"
- **Example:** "Swap Thursday Iyengar for Reformer at noon (KC Move)"
- **What happens:** Removes the original class, adds the new one with specified time/location

### Delete/Skip Classes
- **Syntax:** "Delete [Day] [Class]" or "Skip [Day] [Class]"
- **Example:** "Skip Friday Mysore" or "Delete Monday gym"
- **What happens:** Removes the class from the week

### Modify Time
- **Syntax:** "Move [Day] [Class] to [Time]"
- **Example:** "Move Tuesday Contemporary to 18:45"
- **What happens:** Changes the start/end time of a class

### Add Classes
- **Syntax:** "Add [Class] on [Day] at [Time] ([Location])"
- **Example:** "Add HJS Ballet on Friday at 09:30 (HJS)" or "Add Reformer Tuesday at 13:00 (KC Move)"
- **What happens:** Inserts new class into the schedule

### Force Schedule Despite Conflicts
- **Syntax:** "Force [Day] [Class] even with conflicts" or "[Day] [Class] anyway"
- **Example:** "Add dinner Monday anyway" (schedule over a conflict)
- **What happens:** Schedules the class even if there's an unmovable event that day (you decide to override)

## File Locations (read these first, before searching)

| What | Path |
|------|------|
| **Scheduler script** | `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/KMS/04_project/Training_program/training-calendar-scheduler/calendar_scheduler_v3.py` |
| **OAuth credentials** | Same folder: `google_oauth_credentials.json` |
| **Project CLAUDE.md** | `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/KMS/04_project/Training_program/CLAUDE.md` |
| **Scheduling Rules** | `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/KMS/04_project/Training_program/Training_program_Scheduling_Rules.md` |
| **Class Pool** | `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/KMS/04_project/Training_program/Training_program_Class_Pool.md` |
| **Weekly Schedule log** | `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/KMS/04_project/Training_program/Training_program_Weekly_Schedule.md` |
| **Prior session memory** | `~/.claude/projects/-Users-michael-zhang-training-calendar-scheduler/memory/` |

**Run the scheduler:**
```bash
cd "~/Library/Mobile Documents/iCloud~md~obsidian/Documents/KMS/04_project/Training_program/training-calendar-scheduler"
source .venv/bin/activate                   # activate Python venv first
python3 calendar_scheduler_v3.py --json    # fetch conflicts + proposed plan as JSON
python3 calendar_scheduler_v3.py           # human-readable preview
python3 calendar_scheduler_v3.py --push    # write to Google Calendar (use after approval)
```

**Key config baked into the script:**
- Main calendar: `boping.m.zhang@gmail.com`
- Training calendar ID: `ea1cec57657387a2fef264ce336796fd22b6b6696591106f58742db91335ef0c@group.calendar.google.com`
- Timezone: `Europe/Amsterdam`
- OAuth token cached at `.google_token.pickle` in the same folder

**Google auth note:** Michael uses the **"Personal" Google profile**. On first OAuth browser prompt, switch to the Personal profile if the wrong one opens. The token caches after that.

## Notes

- Changes are shown in real-time as you request them
- Preview the full updated schedule before confirming
- The training calendar is cleared and repopulated completely each week (clean slate)
- All times are in your local timezone (Europe/Amsterdam)
- Your OAuth token is cached — no re-authentication needed
- Unmovable events from your main calendar are always highlighted

## Example Workflow

```
/training-schedule

[System shows week plan with conflicts]

✅ Thursday has no conflicts
⚠️ Wednesday: Dinner with friends at 19:30

You: "Swap Wednesday Jazz for Iyengar at 18:30, and add Hiphop Friday at 20:30"

[Updated plan shown]

You: "Write it"

[Calendar updated successfully]
```

