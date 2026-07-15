---
name: "Project Template System"
description: "Complete guide to creating and managing projects in your KMS"
---

# Project Template System

Finalized template structure for managing projects in your KMS.

---

## Folder Structure

```
/04_project/[ProjectName]/
├── _[ProjectName]_overview.md      ← Main project file (status, roadmap, decisions)
├── _[ProjectName]_trial_log.md     ← Constantly updated experiments log
└── _[ProjectName]_*.md             ← Additional files (appendices, research, etc.)
```

**Example:**
```
/04_project/Analytics_Strategist_Skill/
├── _Analytics_Strategist_Skill_overview.md
├── _Analytics_Strategist_Skill_trial_log.md
└── _Analytics_Strategist_Skill_research.md
```

---

## File 1: Project Overview (`_[ProjectName]_overview.md`)

**Purpose:** Single source of truth for project status, progress, decisions, roadmap.

**Sections (9 total):**
1. **YAML Frontmatter** — Metadata (name, status, pillar, current_focus, dates, priority, tags)
2. **Overview** — What is this project? Why does it matter? How does it connect to broader vision?
3. **Context & Background** — What led to this? Trigger, assumptions, constraints, prior work
4. **Objectives & Goals** — How will you measure success? What are the main goals?
5. **Roadmap** — Flexible: "Modules & Roadmap" (product) OR "Research Questions/Topics" (research)
6. **Next Steps** — What can you start doing and prioritize now?
7. **Open Decisions/Questions** — Decisions pending, blockers, constraints
8. **Accomplishments** — What's already done? Track progress here
9. **Connections** — Parent pillar, related quests, coaching sessions, projects

**Context & Background Section (NEW):**

Purpose: Capture the origin story and foundational context of the project. Helps you remember WHY you started this and identify blind spots/assumptions early.

**What to include:**
- **Trigger:** What sparked this project? Was it a coaching insight, a daily note theme, a sudden idea, or solving a specific problem?
- **Key Assumptions:** What are you assuming is true about this project? (e.g., "I assume autonomy matters more than commitment" or "I assume minimal gym work is enough")
- **Constraints:** Any time/resource/dependency constraints? (e.g., "Must complete by June", "Limited to €500 budget", "Depends on partner agreement")
- **Prior Work:** What's already been done related to this? What can you build on? Previous projects, research, drafts?

**Why it matters:**
- When you revisit a project 3 months later, you need context to understand why you started
- Documenting assumptions early lets you test them (becomes trial log entries)
- Constraints help prioritize and sequence work

**Example entries:**
```
**Trigger:** Coaching session revealed I might need ENM framework for cohabitation
**Key Assumptions:** 
  - Partner cares about monogamy but values authenticity more
  - ENM SLA can be structured to reduce his anxiety
**Constraints:** 
  - Need decision by Q2 2026 (kids timeline)
  - Requires partner buy-in (not unilateral)
**Prior Work:** 
  - 3 years of partnership data
  - Initial mismatch audit completed
```

---

**Roadmap Section (Flexible Naming & Content):**

The Roadmap section adapts based on project type:

**For Product/System Projects:**
- Section name: "Modules & Roadmap"
- Include: Architecture/modules + high-level roadmap based on current priority and feasibility
- Content: Describes the structure of what you're building + phased approach

**For Research-Driven Projects:**
- Section name: "Research Questions/Topics"
- Include: Questions/topics ranked by priority and dependencies
- Content: What are you investigating? Why does each question matter? What depends on what?

**When to update:**
- After each coaching session that touches this project
- After completing a phase or significant milestone
- When you make a major decision or pivot
- Weekly (or as needed for active projects)
- Update Accomplishments regularly to track progress
- Update Next Steps as priorities shift based on roadmap progress
- Update Open Decisions as blockers emerge or decisions become clear

**Note:** Learnings are documented in the Trial Log (where experiments happen), not here. This keeps the overview focused on strategy, actions, and blockers. Trial log is where you document discoveries, what's working/not working, and decisions made from experiments.

---

## File 2: Trial Log (`_[ProjectName]_trial_log.md`)

**Purpose:** Constantly updated record of experiments, results, learnings, and decisions. This is where all discoveries live.

**Header Elements:**
- **Project name, dates, status**
- **Purpose Statement:** One-line summary of why you're running these experiments. What are you trying to learn or prove? (Example: "Testing whether iterative approaches beat big upfront planning")

**Structure:**
- **Header:** Project name, dates, status, purpose statement
- **Trial Log Table:** | Date | Experiment | Result | Learning | Decision |
- **Notes & Context:** Why these experiments? Key insights? Next to try?
- **Decisions, Blockers & Pivots:** 
  - Decisions made (with rationale and impact on overview sections)
  - Blockers encountered (description, impact, resolution)
  - Pivots taken (what changed and why)
  - Next experiments to try
- **Reflection Entries (Optional):** Anytime reflections that feed into daily notes for coaching

**When to update:**
- After each experiment/trial (even small ones)
- After each phase completion
- Anytime you have a learning or insight
- When decisions are made (document the decision and rationale here, linked to the experiment)
- When you update trial log with decisions, also update the corresponding sections in the overview (Next Steps, Open Decisions, or Accomplishments)

**Trial Log Entry Format:**
| Date | Experiment | Result | Learning | Decision (if any) |
|---|---|---|---|---|
| YYYY-MM-DD | What did you test/try? | What happened? | What did you learn? | If a decision was made, note it here with rationale |

**Learning format:**
- Short, actionable phrase
- Captures the insight or pattern
- Not verbose; concise
- If it reveals a challenge or blocker, note it so you can surface it in "Open Decisions"

---

## File 3+: Supporting Files (Optional)

**Examples:**
- `_ProjectName_research.md` — Research, notes, references
- `_ProjectName_context.md` — Stakeholders, dependencies, background
- `_ProjectName_resources.md` — Links, tools, templates used

---

## Project Lifecycle

### Birth (In Dev)
**Status:** `in dev`
**Triggered by:**
- Coaching insight: "This could be a project"
- Wiki theme: "Let's systematize this"
- Manual creation: "I want to explore this"

**At creation:**
- Set primary pillar (one only)
- Link to relevant quests
- Note coaching session that inspired it (if applicable)
- Write Overview explaining the why
- Start trial log if experiments will happen immediately

### Active (In Progress)
**Status:** `active`
**What happens:**
- Trial log gets updated regularly with experiments and learnings
- Discoveries and insights documented in trial log
- Decisions, blockers, and pivots tracked in merged "Decisions, Blockers & Pivots" section
- Learnings flow into daily notes (anytime reflection)
- Coaching sessions reference this project
- Overview sections updated based on trial log decisions (Next Steps, Open Decisions, Accomplishments)
- Blockers escalated if needed

### Completion Tracking
**When project completes:**
1. Mark status: `completed` or `one day` (depending on outcome)
2. Final trial log entries capture what succeeded/failed and key learnings
3. Update Accomplishments section in overview with summary
4. Extract key learnings from trial log:
   - Option A: Write POS signals (batch processed monthly)
   - Option B: Write reflection in daily note (continuous)
5. Archive project (keep for reference, close to active)

---

## Integration with Wiki + Coaching + Learnings

### Wiki Processing
When wiki processes a daily note:
1. Links related quests to this project (bidirectional)
2. Updates project status in page's "Connections" section
3. Can suggest new projects from insights

### Coaching Sessions
When coaching generates a session:
1. Reference active projects (e.g., "Project X aligns with this insight")
2. Suggest new projects (e.g., "This could become Project Y")
3. Ask about completed projects (e.g., "What did Project Z teach you?")

### Learnings Flow
**Option A (Batch via POS signals):**
- User extracts learnings from completed project
- Creates POS signals from key insights
- Signals batch-processed monthly via pos_update skill
- Updates _POS.md + _POS_changelog.md

**Option B (Continuous via daily notes):**
- Anytime during project (not just at completion), user writes reflection in daily note
- Reflection mentions project, learnings, insights
- Daily note gets processed by wiki + coaching
- Learnings naturally surface in future coaching sessions
- No separate "project completion" processing needed

**Combined flow:**
- Continuous reflections (daily note) surface insights in real-time
- Batch signals (monthly) capture patterns for _POS updates
- Best of both: ongoing guidance + systematic refinement

---

## Template Files (To Use)

**Project Overview Template:**
- File: `Project_Overview_Template.md`
- Copy this when creating a new project overview

**Trial Log Template:**
- File: `Project_Trial_Log_Template.md`
- Copy this when creating a new project trial log

---

## Key Rules for Projects

1. **One primary pillar per project — Connections to other pillars via tags and page links
2. **Bidirectional linking** — Projects link to quests; quests link back to projects
3. **Trial log is living** — Update frequently (even small experiments count)
4. **Purpose statement is clear** — "Why are we running these experiments?" should be answerable from the purpose statement
5. **Learnings are continuous** — Don't wait until completion; reflect anytime
6. **Status always current** — Update "Current Focus" weekly to reflect where you are
7. **Decisions documented** — Major choices get written with rationale in trial log, with clear impact on overview sections
8. **Blockers and pivots tracked** — All project changes (blockers, pivots, decisions) live in one merged section for easy reference
9. **Connections maintained** — Review connections quarterly to stay aligned

---

## When to Create a Project

**Create a project when:**
- You're running multiple experiments on a topic
- You want to track "Constructive Failures" (trials + learnings)
- A coaching insight suggests testing something
- A wiki theme could benefit from systematic exploration
- You want accountability for a focused effort (4-12 weeks)

**Don't create a project when:**
- It's a one-off task (use daily note or page instead)
- It's a permanent system (belongs in page/wiki)
- You're just researching (use captured items + daily notes)

---

## Examples

### Example 1: Analytics Strategist Skill Project

```yaml
name: "Analytics Strategist Skill Development"
status: "active"
pillar: "Career"
current_focus: "Week 3: Testing small-team approach vs. large-dataset approach"
priority: "P2"
```

**Overview:** Testing whether small, iterative experiments are better than big upfront planning for developing analytics strategy skill.

**Trial log:** Recording 2 experiments/week; discovered that hybrid approach works best.

**Learnings:** Iterative beats perfectionism; small tests reveal surprises that big plans miss.

**Connections:** 
- Quest: [[Career Strategy Development]]
- Coaching: [[coaching_session_20260503]] inspired this

### Example 2: Relationship Authenticity Project

```yaml
name: "Partnership Authenticity"
status: "one day"
pillar: "Relationships"
current_focus: "Completed: Explored vulnerability + autonomy in partnership"
priority: "P3"
```

**Status:** Completed (one_day = exploring but putting aside for now)

**What we learned:** Solo reflection complete (documented in trial log). Waiting for partner availability to have deeper conversations (planned Q3).

**Next phase:** Scheduled for Q3 coaching sessions.

---

## FAQ

**Q: Can a project link to multiple quests?**
A: Yes. One primary pillar, but multiple quests within that pillar can reference it.

**Q: Should I write daily in the trial log?**
A: Only after experiments. If you're not experimenting that day, no entry needed.

**Q: Where do learnings and discoveries go?**
A: All in the trial log (not the overview). The overview stays focused on strategy, actions, and blockers. Learnings in the trial log feed into daily notes and eventually into _POS signals.

**Q: Can I pause a project mid-way?**
A: Yes. Change status to `one day` (on hold) and update current_focus to explain why.

**Q: What if I fail?**
A: Mark status `completed` or `one day`, document what didn't work, extract learnings. Failures are valuable signals.

**Q: How do I connect project learnings to _POS updates?**
A: Create POS signals from key learnings (batch monthly), OR write reflections in daily notes (continuous). Or both.
