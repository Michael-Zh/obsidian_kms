---
name: "priming"
description: "Morning context briefing — process a Typeless voice transcript into a structured, warm day brief with top tasks, schedule, energy baseline, and a POS nudge. Outputs to daily note + HTML card file."
---

# Priming Skill

Morning ritual skill. Takes a Typeless voice transcript as input, cross-references it against all existing context, and outputs a warm, energising day briefing in two formats: a daily note block and a phone-optimised HTML card file.

Run via WeChat → Claude Code, or directly in Claude Code with the transcript pasted as input.

---

## KMS Paths

```
Vault: /Users/michael_zhang/Library/Mobile Documents/iCloud~md~obsidian/Documents/KMS

Context files:
  00_system/_POS.md
  00_system/_priority.md
  04_project/Training_program/sleep_log.md
  01_raw/coaching/coaching_YYYYMMDD.md    ← all coaching sessions (unified)

Calendar script:
  04_project/Training_program/training-calendar-scheduler/calendar_scheduler_v3.py

Output targets:
  01_raw/_daily_note/YYYY-MM-DD.md           ← append priming block
  03_priming/priming_YYYYMMDD.html           ← create HTML card file
```

---

## Working Context

- **Working hours:** Monday–Friday, 09:00–17:30 (full-time job)
- **Work tasks** are scheduled within this window unless specified otherwise
- **Personal/life tasks** scheduled outside working hours
- Today is a workday if Mon–Fri; adjust tone and task suggestions accordingly

---

## Step 1 — Load Context

Load in this order:

1. **`_POS.md`** — communication style, active bugs, operating patterns
2. **`_priority.md`** — current priorities and short-term focus (read the Short-Term Focus section closely)
3. **`sleep_log.md`** — read the most recent entry only (last AutoSleep block at the top of file)
4. **Calendar — today's events:**
   ```bash
   python3 "[vault]/04_project/Training_program/training-calendar-scheduler/calendar_scheduler_v3.py" --today
   ```
   Returns JSON with `training_events` and `main_events` for today.
5. **Most recent coaching session** — find the latest `coaching_YYYYMMDD.md` in `01_raw/coaching/` by date → read the Open Items and Experiment Checklist sections only
6. (Step 6 removed — session and discussion are now unified in a single `coaching_YYYYMMDD.md` file)

---

## Step 2 — Process the Transcript

Extract from the user's Typeless transcript:

- **Tasks mentioned** — anything they want to do, need to do, or are thinking about doing
- **Intentions** — how they want to feel or approach the day
- **Concerns or blockers** — things weighing on their mind
- **Energy signals** — how they feel, any physical notes

Then cross-reference:

1. **Priority alignment** — do the tasks align with current P1/P2 focus? Flag anything that looks like distraction or low-priority busywork
2. **Schedule constraint** — check training_events: if there's a class/gym session, note reduced afternoon energy. Check main_events for fixed commitments blocking time
3. **Open items** — is anything from the transcript a follow-up on a coaching open item? Note it
4. **POS lens** — apply relevant patches:
   - More than 3 tasks → apply 90% Solution: narrow to top 3
   - Certainty Trap signals (gathering info instead of starting, waiting for the right moment) → reference `[[Daily-Procrastination-Protocol]]`
   - Work task involving J or presentation → remind: write hypothesis first
   - Emotional weight detected → acknowledge before pivoting to tasks

Set the **main goal**: the single most important outcome for the day, phrased as an action.

---

## Step 3 — Generate Output

### A. Daily Note Block

Append to `01_raw/_daily_note/YYYY-MM-DD.md`:

```markdown
## 🌅 Morning Priming — YYYY-MM-DD

**今天的主线：** [main goal — one sentence, warm and concrete]

**Top 3:**
1. [task] ✦ [brief why — connect to priority or schedule]
2. [task]
3. [task]

**今天的节奏：** [today's schedule from calendar — class at X / gym / rest day / work meetings]

**能量基础：** Readiness [X]% — [one warm sentence on what this means for today]

**小提醒：** [one POS-aware nudge — warm, not preachy. E.g. "H1 review coming up — 写下你的假设，先发制人 💪"]

[[03_priming/priming_YYYYMMDD.html|📱 Open priming card]]

---
```

### B. HTML Card File

Save to `03_priming/priming_YYYYMMDD.html`.

After saving the HTML, also render a PNG to `/tmp/priming_YYYYMMDD.png` for WeChat delivery:
```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu \
  --screenshot="/tmp/priming_YYYYMMDD.png" \
  --window-size=520,1100 \
  --force-device-scale-factor=2 \
  --hide-scrollbars \
  "file:///[vault]/03_priming/priming_YYYYMMDD.html" 2>/dev/null
```
Then output the PNG path `/tmp/priming_YYYYMMDD.png` so the WeChat bridge auto-pushes it.

Self-contained HTML — no external dependencies, works offline, phone screen optimised (max-width 480px).

**Card structure:**
- **Header**: dark blue background, yellow title "Daily Priming" + date + one-line subtitle (main goal)
- **Card 1 — Main Goal**: large bold text in dark blue
- **Card 2 — Top 3 Tasks**: numbered list with dark blue number badges on yellow background
- **Card 3 — Today's Rhythm**: schedule rows with yellow time chips + energy note
- **Card 4 — Nudge**: dark blue box with yellow accent text

**Design spec:**
- Page background: `#e8e8c8` (warm off-white)
- Primary blue: `#1a2a6c`
- Accent yellow: `#f5c518`
- Header: blue background, yellow title, muted blue subtitle
- Hazard stripe dividers between sections: alternating yellow/blue diagonal stripes, 10px height
- Cards: white background, 2px blue border, no border-radius except last card (0 0 16px 16px)
- Task number badges: yellow text on blue background, 32×32px rounded square
- Time chips in rhythm card: yellow background, blue text
- Nudge box: blue background, light text, yellow highlights
- Font: system-ui / -apple-system stack, 16px, line-height 1.6
- Width: 480px max, 16px padding

---

## Tone Rules

- **Warm and energising** — this is the first thing they read in the morning. Make it feel like a thoughtful friend who knows them well, not a productivity robot
- **Encouraging** — acknowledge their energy and intentions before organising them
- **Still concise** — no padding or filler. Every sentence earns its place
- **BLUF for tasks** — main goal first, but with warmth not coldness
- **Chinese/English mixed is natural** — match the language register of the transcript. If they spoke Chinese, respond in Chinese with natural English terms where appropriate
- **Pattern-naming with care** — if flagging a Certainty Trap or over-planning, do it with humour and empathy, not diagnosis ("看起来今天的你有点野心勃勃 — 我们先选3个吧 😄")
- Total output readable in under 2 minutes

---

## Key Rules

1. Never skip the calendar fetch — schedule context is essential for realistic task suggestions
2. Read the most recent `coaching_YYYYMMDD.md` from `01_raw/coaching/` — read the full file for the most recent one to get Open Items and tone context
3. Top 3 tasks maximum — if transcript has more, pick the 3 most aligned with current priorities
4. HTML file must be fully self-contained (no external CSS/JS/fonts)
5. The daily note link must use Obsidian wikilink format: `[[03_priming/priming_YYYYMMDD.html|📱 Open priming card]]`
6. Working hours are 09:00–17:30 Mon–Fri — don't schedule work tasks outside this window unless the user explicitly mentioned them
7. If sleep_log.md has no entry yet today, use the most recent available entry and note it's from the day before
