---
name: "project-initiation"
description: "Interactive step-by-step guide to create a new project using the project template. Auto-creates folder structure and files."
---

# New Project Initiation Skill

Launch a new project with guided step-by-step prompts. The skill creates the folder structure, generates YAML frontmatter, and populates template sections based on your input.

---

## How to Invoke This Skill

### Trigger 1: Standalone Project Creation
```
/new-project
"I want to start a new project on autonomy in relationships"
```

### Trigger 2: During Ongoing Conversation
```
"Make this into a project: [topic from our conversation]"
or
"Turn what we've been discussing into a project"
```

The skill will:
1. Extract context from our conversation (topic, trigger, pillar, related quests)
2. Pre-fill relevant template sections
3. Guide you through remaining sections

---

## What the Skill Does

### Step-by-Step Workflow

**Step 1: Project Basics (Contextual)**
- If starting standalone: "What's your project name and pillar?"
- If from conversation: "I'm suggesting [Project Name] in [Pillar] based on our chat. Correct?"
- Extract and confirm: Project name, Pillar, Cross-pillar tags

**Step 2: Load & Display Pillar Index (NEW)**
- Query: Load the pillar's `_[Pillar]_Index.md` file
- Display: Active quests in this pillar with their summaries
- Ask: "Which of these quests relate to your project? Any you want to link?"
- Show example: "[[Quest_A]] — Description. Related Projects: [[ProjectX]]"
- Suggest: Based on project context, recommend which quests might be relevant
- Collect: User selects related quests to link (can be 0-3+ quests)

**Step 3: Context & Background (Pre-filled from conversation if available)**
- Present discovered context: "You mentioned X triggered this. Shall I use that as the Trigger?"
- Collect remaining: Assumptions, Constraints, Prior Work
- Offer to draft or refine each section

**Step 4: Objectives & Goals**
- "What are 3 core goals for this project?"
- Offer examples based on project type
- Format as Goal 1 / Goal 2 / Goal 3

**Step 5: Roadmap Type Selection**
- "Is this product/system work (Modules & Roadmap) or research-driven (Research Questions/Topics)?"
- Based on choice, guide through appropriate section

**Step 6: Next Steps (Optional)**
- "Any immediate actions for this week?"
- If empty: "I can mark this as planning phase. That okay?"

**Step 7: Initial Metadata**
- Confirm Priority (P1/P2/P3)
- Set Target Completion Date (reasonable estimate)
- Confirm related quests already selected in Step 2

**Step 8: Create Project Structure**
- Generate YAML frontmatter
- Create `/04_project/[ProjectName]/` folder with:
  - `[ProjectName]_overview.md` (pre-filled with your inputs + linked quests)
  - `[ProjectName]_trial_log.md` (template ready; Purpose Statement included)
  - Optional: `[ProjectName]_context.md` (if you want to preserve detailed background)

---

## Context Extraction from Ongoing Conversation

When you use this skill mid-conversation, it automatically captures:

### ✅ What Gets Extracted
1. **Project Name/Topic** — From the subject we're discussing
2. **Trigger** — Why this is relevant now (recent coaching insight, daily note theme, problem identified)
3. **Pillar** — Which life area this belongs to (inferred from context)
4. **Related Pages/Projects** — Any quests or projects you've mentioned
5. **Objectives/Goals** — Goals you've expressed related to this

### 🔄 How It Works
- Skill summarizes detected context
- You confirm/refine each element
- Pre-fills the overview template with confirmed context
- Guides you through remaining template sections

### Example Conversation Extraction
```
You: "I'm realizing I need to optimize my skincare routine before the China trip"

Skill detects:
✅ Project name: "China Travel Skincare Prep" or "Anti-Aging Skincare Optimization"
✅ Trigger: "2-month China trip coming up; need pollution defense + anti-aging"
✅ Pillar: AdminHome (or PhysicalHealth cross-tag)
✅ Related: Travel quest mentioned; skincare routine mentioned
✅ Goals: "Pollution defense for China" + "Maintain anti-aging progress"

Skill asks: "Is this accurate? Any changes?"
```

---

## Template Sections Guided Step-by-Step

### Section 1: Overview
**Skill prompt:** "In 2-3 sentences, what's this project about and why does it matter?"
- Pre-fills if extracted from conversation
- You refine or expand

### Section 2: Context & Background
**Skill prompt:** "What triggered this project? What assumptions are you making?"
- Trigger: [Pre-filled if from conversation]
- Key Assumptions: [You provide]
- Constraints: [You provide or "None"]
- Prior Work: [You provide or "Starting fresh"]

### Section 3: Objectives & Goals
**Skill prompt:** "What are your 3 core goals? How will you measure success?"
- Goal 1: [You provide]
- Goal 2: [You provide]
- Goal 3: [You provide]

### Section 4: Roadmap (Conditional)
**Skill prompt:** "Is this product/system work or research-driven?"
- **If Product/System:** Guide through "Modules & Roadmap"
  - Module 1: [You describe]
  - Module 2: [You describe]
  - Phase 1: [You describe]
  
- **If Research-Driven:** Guide through "Research Questions/Topics"
  - Q1 (P1): [You ask]
  - Q2 (P2): [You ask]
  - Q3 (P3): [You ask]

### Section 5: Next Steps
**Skill prompt:** "What can you do this week? Any immediate actions?"
- [Optional; can leave empty for "planning phase"]

### Section 6: Trial Log (Auto-Generated)
**Skill prompt:** "For your trial log, what's the Purpose Statement? Why are you running this project?"
- Purpose: [You define]
- [Rest of trial log template auto-generated]

---

## Output: Folder Structure Created

After completing all steps, the skill creates:

```
/04_project/[ProjectName]/
├── _[ProjectName]_overview.md
│   ├── YAML frontmatter (all fields populated)
│   ├── Overview
│   ├── Context & Background
│   ├── Objectives & Goals
│   ├── Roadmap (Modules or Research Questions)
│   ├── Next Steps
│   ├── Open Decisions/Questions
│   ├── Accomplishments (empty, ready to populate)
│   └── Connections
│
├── _[ProjectName]_trial_log.md
│   ├── Header (Start Date, Status, Purpose Statement)
│   ├── Trial Log Format (table template)
│   ├── Notes & Context
│   ├── Decisions, Blockers & Pivots
│   └── Reflection Entries
│
└── _[ProjectName]_*.md (optional)
    └── Additional files if needed (research notes, context, etc.)
```

---

## Examples

### Example 1: Standalone Project Creation

```
User: "/new-project"

Skill: "Let's create a new project! What's the project name and which pillar?"
User: "Project Name: Analytics Strategist Skill, Pillar: Career"

Skill: "Great! Is this about learning analytics strategy? Tell me more."
User: "Testing whether iterative experiments beat big upfront planning for developing analytics skills"

Skill: "I see. What triggered this? Was it a coaching insight?"
User: "Yes, session with coach about learning faster through small tests"

Skill: "Got it. Next: Key assumptions. What are you assuming about this approach?"
User: "That small reversible experiments are more valuable than big plans"

... [continues through all sections] ...

Skill: "Creating project folder and files now..."
✅ Created: /04_project/Analytics_Strategist_Skill/
  - _Analytics_Strategist_Skill_overview.md (pre-filled)
  - _Analytics_Strategist_Skill_trial_log.md (ready)
```

### Example 2: Project from Ongoing Conversation

```
[Earlier in conversation about relationship dynamics...]

User: "I think I should structure this into a formal project so I track it properly"

Skill detects:
✅ Project Name: "Strategic Relationship Audit & Cohabitation Roadmap"
✅ Trigger: "Cohabitation planning; need to address mismatch inventory"
✅ Pillar: Relationships (MindMentalHealth cross-tag)
✅ Related: Partnership quest, cohabitation discussions
✅ Goals: ENM SLA, Kids decision, Move-in with transparency

Skill: "I detected this project from our conversation. Confirm?"
- Project: Strategic Relationship Audit & Cohabitation Roadmap ✓
- Pillar: Relationships ✓
- Trigger: Cohabitation planning; address mismatches ✓

User: "Yes, but add 'Q2 deadline' to constraints"

Skill: "Added. Now: What's the Purpose Statement for your trial log?"
User: "Testing whether ENM framework can resolve cohabitation mismatches"

... [continues] ...

✅ Created: /04_project/Strategic_Relationship_Audit/
  - _Strategic_Relationship_Audit_overview.md (pre-filled from context)
  - _Strategic_Relationship_Audit_trial_log.md (Purpose: "Testing ENM framework...")
```

---

## Tips for Using This Skill

### For Quick Projects
- Provide minimal responses; skill adapts to project complexity
- Can leave "Next Steps" and "Open Decisions" empty initially
- Focus on name, pillar, goals, roadmap

### For Complex Projects
- Spend time on "Context & Background" — it surfaces blind spots
- Be specific with assumptions (these become trial log hypotheses)
- Define multiple goals if needed (no strict limit)

### For Research-Driven Projects
- Spend extra time on Research Questions/Topics step
- Think about dependencies between questions
- Rank by priority (P1/P2/P3)

### For Conversation-Based Projects
- Skill will ask: "Should I create a project from this?"
- Confirm the extracted context before proceeding
- Refine/add missing elements in guided steps

---

## Skill Assumptions

1. **Project names use underscore format**: `Analytics_Strategist_Skill` (for folder names)
2. **Pillar must be one of:** LifeManagement, Career, PhysicalHealth, Relationships, Finance, CreativityCuriosity, AdminHome, MindMentalHealth, Travel
3. **Priority defaults to P2** (can be adjusted: P1/P2/P3)
4. **Status defaults to "active"** (can be adjusted: active/in dev/completed/one day)
5. **Created date = today**, Updated date auto-filled
6. **Target completion** should be realistic (2-4 weeks for execution, 2-3 months for research/strategy)

---

## When to Use This Skill

✅ **Use when:**
- Starting a new project from scratch
- Want to systematize an ongoing exploration
- Had a coaching insight that could become a project
- Need to convert a daily note theme into a project
- During conversations about work/goals/exploration

❌ **Don't use when:**
- Just brainstorming (use daily notes instead)
- It's a one-off task (belongs in quest, not project)
- It's already a permanent system (belongs in wiki/quest)

---

## What Happens After Project Creation

Once your project is created:
1. **Go to the project folder** and open `_[ProjectName]_overview.md`
2. **Review and refine** template sections as needed
3. **Set Priority** if it's P1 or P3 (default is P2)
4. **Add to Projects Index** — Skill will prompt you to add row to `_projects_index.md`
5. **Start trial log** when you run your first experiment
6. **Link to quests** — Update "Related Pages" if applicable

---

## Ready to Create a Project?

Invoke the skill and follow the step-by-step prompts:

**`/project-initiation`**

Or mention it mid-conversation:

**"Turn this into a project"**

The skill will guide you through the rest!
