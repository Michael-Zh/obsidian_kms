**Last updated:** 2026-05-03

---

## Part 1: Core Vision & Architecture

### 0. Core Mission & Goals

Transform raw content into "Constructive Failures" (Trials) using an LLM as the primary maintenance agent.

**Goal 1: Capture & Preserve** — Create a durable, immutable record of sources (`01_raw`)

**Goal 2: Hierarchical Synthesis** — Organize knowledge into a strict tree structure: **Pillar > Quest / Project**

**Goal 3: Executive Action** — Convert knowledge into tangible trials, coaching sessions, and Apple Reminders

**Goal 4: Social Loop** — Document the "Trial and Error" process for social sharing

---

### 1. Module Architecture & Current Status

|#|Module Name|Status|Purpose|
|---|---|---|---|
|**1**|Apple Shortcuts to capture URL & entities|🟡 In Progress|Capture raw URLs + text (book/movie names); working on context extraction|
|**2**|Sorting system for next-step tools|🔵 Planned|Route content to appropriate processor|
|**3**|Desktop tools to process clip URL contents|🔵 Planned|Web clipper + transcription layer + context extraction|
|**4**|Entity sorting and processing|🔵 Planned|Process persons, books, concepts|
|**5**|Obsidian Daily Note as generic inbox|✅ Complete|Brain dump capture (daily notes)|
|**6.1**|Brain Dump sorting & Wiki generation|✅ Complete|**wiki-coach-kms-cli skill (LIVE)**|
|**6.2**|Coaching action suggestions|✅ Mostly Complete|Integrated to wiki workflow; needs dedicated coach skill|

**Legend:** ✅ Complete | 🟡 In Progress | 🔵 Planned | 🔴 Blocked

---

### 2. Directory Structure (The "Codebase")

```
/KMS
  /00_system                      <-- System Instructions (LLM Logic)
    /_POS.md                      <-- Personal Operating System
    /_priority.md                 <-- Current priorities & sequencing
    /POS_signal/                  <-- Signal files (daily-rotating)
    
  /01_raw                         <-- Immutable Sources (Archive)
    /_daily_note/                 <-- Daily notes from Obsidian
    /_web_clips/                  <-- Web clipped articles & links
    /_transcripts/                <-- Video/audio transcripts
    /_ebooks/                     <-- eBook extracts
    
  /02_wiki                        <-- Persistent Knowledge Artifacts
    /_log.md                      <-- Chronological change record (prepend)
    /_processed_log.md            <-- Input files processed tracker
    /[Pillar]/
      /_[Pillar]_Index.md
      /Quest_*.md
      
  /03_output                      <-- Coaching Sessions
    /coaching_session_YYYYMMDD.md
    
  /04_project                     <-- Projects (Action-Oriented, Time-Bound)
    /_priority.md                 <-- Current priorities & sequencing
    /Project_A/
      /project.md
      /tasks.md
```

**Hierarchy Mapping:**

|**Level**|**Mapping**|**Role**|**Location**|**Status**|
|---|---|---|---|---|
|**Pillar**|Root|Permanent Life Area|`/02_wiki/[Pillar]/`|✅ Live|
|**Quest**|1 Pillar : N Quests|Thematic Deep Dive|`/02_wiki/[Pillar]/[Quest].md`|✅ Live|
|**Project**|1 Quest : N Projects|Action-Oriented Trial|`/04_project/[Project_Name]/`|🔵 Planned|
|**Index**|Single Source|Master Map|`/02_wiki/[Pillar]/_Index.md`|✅ Live|
|**Log**|Audit Trail|Chronological Record|`/02_wiki/_log.md`|✅ Live|

---

### 3. The 8 Pillars (Life Organization)

- **Relationships** — Social health and core connections
- **Mind & Mental Health** — Internal world, reflection, therapy
- **Career** — Professional output and skill development
- **Physical Health** — Sleep, fitness, diet
- **Life Management** — Systems and meta-work (including KMS itself)
- **Finance** — Wealth management and resource allocation
- **Creativity & Curiosity** — Exploration and hobbies
- **Admin & Home** — Physical environment and bureaucracy
- **Travel** — Travel ideas and planning

---

### 4. Proposed Full Workflow (Input → Wiki + Coaching → Output)

```
INPUT (daily note, web clip, transcript, etc.)
  │
  ├─→ Wiki Process
  │   ├─ Extract themes → Assign to pillars
  │   ├─ Find related quests (Obsidian CLI search)
  │   ├─ Merge intelligently with existing content
  │   ├─ Update `/02_wiki` quests + indexes
  │   ├─ Prepend to `_log.md` (with Cross-Pillar Connections)
  │   └─ Append signals to `/00_system/POS_signal/`
  │
  └─→ Coaching Process (PARALLEL)
      ├─ Load same input + current priorities
      ├─ Load _POS.md constraints
      ├─ Filter insights through priorities
      ├─ Generate actionable coaching session
      ├─ Output to `/03_output/coaching_session_YYYYMMDD.md`
      └─ Append signals to `/00_system/POS_signal/`

RESULT: Both wiki updates (neutral) + coaching guidance (priority-filtered) from one input
```

---

### 5. What's Built (✅ Phase 1 Complete)

#### Phase A Setup: Capture Infrastructure (✅ COMPLETE)

1. ✅ Obsidian vault directory structure initialized
2. ✅ Daily note capture in `/01_raw/_daily_note/`
3. ✅ Apple Shortcuts capturing raw URLs + text to `/01_raw/` (working on context extraction)

#### Phase B MVP Workflow (✅ COMPLETE, Historical Record)

Manual workflow for initial testing:

- Pack input as markdown
- Upload to Gemini app
- Generate Obsidian CLI commands
- Manually run commands in terminal
- Replaced by Claude desktop integrated workflow

#### The Integrated wiki-coach-kms-cli Skill (✅ LIVE)

**Location:** `/Users/michael_zhang/Documents/Claude/wiki-coach-kms-cli-v4.md`

**Wiki Process (8-Step Workflow):**

1. Load new input files (check `_processed_log.md`)
2. Extract themes and assign to Pillar
3. Find relevant existing quests using `obsidian search`
4. Merge intelligently (Exact/Partial/No Match decision tree)
5. Generate updates with proper formatting and tagging
6. Update Pillar Indexes (preserve manual edits, list projects per quest)
7. Log changes by prepending to `_log.md` (Pillar-grouped tables + Cross-Pillar Connections)
8. Track in `_processed_log.md`

**Coaching Process (Parallel):**

1. Load same input + current `_priority.md`
2. Load `_POS.md` constraints
3. Identify insights relevant to current priorities
4. Generate coaching session:
    - Quick Summary (what emerged, why it matters)
    - By Priority Area (only if input touches priority)
    - High-Impact Insights (mentioned inline)
    - On the Horizon (exploratory items)
    - Open Items / To Be Concluded
5. Output to `/03_output/coaching_session_YYYYMMDD.md`

**Signal Collection (Both Processes):**

- ✅ Wiki identifies patterns → appends to `/00_system/POS_signal/POS_signal_YYYYMMDD.md`
- ✅ Coaching identifies contradictions/patches → appends to same file
- ✅ Signal file rotates daily (new calendar day = new signal file)
- ✅ All signals include Obsidian internal links

**Key Technical Decisions:**

- Input folder is read-only (processing state tracked separately in `_processed_log.md`)
- Obsidian CLI for discovery (token efficiency)
- Prepend log entries (reverse-chronological)
- Cross-pillar tagging (e.g., `#AdminHome`, `#CreativityCuriosity`)
- Coaching outputs to separate `/03_output/` folder (keeps logs clean)

#### The POS Update Process (✅ COMPLETE)

**Model A+: Signal-Based, On-Demand Batch Processing**

1. **Signal Collection (Continuous)**
    
    - During wiki processing: Patterns identified → appended to signal file
    - During coaching processing: Contradictions/patches identified → appended to signal file
    - Signals accumulate in active file: `/00_system/POS_signal/POS_signal_YYYYMMDD.md`
    - File rotates daily (new calendar day = new signal file)
2. **File Rotation (Automatic)**
    
    - When first signal appears on new calendar day → Create new file
    - Example: Jan 1-Apr 2 signals in `POS_signal_20260101.md`, then `POS_signal_20260403.md` starts
3. **Batch Processing (On-Demand)**
    
    - User decides when to process (no fixed schedule)
    - pos_update skill loads accumulated signals
    - Groups similar signals (e.g., all "satisficing patches" together)
    - Presents groups with context, user decides: "Update _POS? Yes/No/Later"
    - Applies updates to `_POS.md` + logs changes to `_POS_changelog.md`

#### The Priority System (✅ COMPLETE)

**Location:** `/04_project/_priority.md`

**Three Levels:**

1. **Top 3 (Current Focus)** — Primary allocation of attention (P1, P2, P3)
2. **Secondary Focus** — Active monitoring, not top priority
3. **Background** — Interesting but not urgent

**Each Priority Includes:**

- Clear outcome/theme (e.g., "Physical Base", "Resource Moat", "Relationship Gate")
- Success metrics and KPIs
- Key initiatives within that priority
- Timeline and review cadence
- Cross-priority dependencies and sequencing notes

**Current State (as of 2026-05-03):**

- P1: Physical Base (Q2-Q3 focus, swimming/deload/mobility)
- P2: Resource Moat (moved from P3, Q2 investment planning, strategist role)
- P3: Relationship Gate (moved from P2, Q2 solo reflection, H2 conversations, timeline to Q3/Q4)

---

## Part 2: Open Decisions & Roadmap Forward

### Decision 1: Coaching Layer Architecture (Core Architecture Decision)

**Current State:**

- ✅ Coaching schema fully integrated into wiki-coach-kms-cli skill
- ✅ Real-time coaching generated alongside wiki updates
- ✅ Parallel execution on same input
- ✅ Priority-aware filtering working
- ✅ _POS constraints respected

**What's Missing:**

- 🔴 **Dedicated Ad-Hoc Coaching Skill** — Standalone skill to continue coaching conversations
    - Not tied to new inputs
    - Automatically considers current priority, _POS
    - Can take conversation(s) as input to provide continuity
    - Use cases: Mid-week priority check-ins, deeper exploration of open items from prior sessions, coaching on specific challenges

**Next Step:** Build standalone `coach-session` skill (separate from wiki-coach-kms-cli):

- Input: Previous coaching session(s) + current focus question/challenge
- Context: Load `_priority.md` + `_POS.md` + recent `_log.md`
- Output: Continued coaching conversation (not tied to wiki update)
- Can be triggered ad-hoc without running wiki processing

---

### Decision 2: Input Consolidation & Workflow for Non-Daily-Note Sources

**Current State:**

- ✅ Daily notes → Process directly into wiki (clean, pre-digested input)
- 🟡 URLs/text from Apple Shortcuts → Captured to `/01_raw/` (raw URLs + names, no context yet)
- 🔴 Web clips, videos, ebooks, transcripts → No workflow yet

**The Problem:** Raw URLs and text lack the context needed for meaningful wiki processing. We need a strategy to extract and enrich content before wiki processing.

**Options to Explore:**

#### Option A: Two-Tier Processing (Context Extraction)

1. **Tier 1 (Capture)**: Apple Shortcuts saves raw URL + name/text to `/01_raw/` subfolders
2. **Tier 2 (Context Extraction)**: LLM fetches URL/extracts content → Generate structured note with key insights, themes, connections
    - Web article → Extract core claims, evidence, implications, relevant to your pillars
    - Video/transcript → Summarize key points, moments, learnings
    - eBook → Extract relevant chapters, quotes, frameworks
    - Result stored to `/01_raw/_digested/` or directly to input folder

**Pros:**

- Keeps raw URLs immutable and lightweight
- Allows async processing (capture now, digest later)
- Different extraction strategies per media type
- Digested artifacts ready for wiki processing

**Cons:**

- Extra step and additional LLM calls
- More complex workflow

#### Option B: Direct Processing (Simpler, Real-Time)

- Store URLs directly in `/01_raw/`
- During wiki processing, LLM fetches and processes the URL inline
- No separate digestion step

**Pros:**

- Simpler workflow
- One-pass processing

**Cons:**

- Slower, more expensive per run
- Real-time web fetching may fail
- Raw artifacts not preserved separately

#### Option C: Hybrid (Manual Flagging)

- Store URLs in `/01_raw/`
- Manual flag: "This needs context extraction"
- Run context extraction only on flagged items
- Digested output goes to input folder → wiki processes as normal

**Pros:**

- Flexible (you decide what's worth extracting)
- No forced digestion of everything
- Keeps wiki processing simple

**Cons:**

- Manual overhead to flag items
- Inconsistent processing

---

### Decision 3: Project Template & Flow Integration (New Workstream)

**Current State:**

- 🔵 Project structure exists in `/04_project/` but undefined
- 🔵 Projects not integrated into wiki flow
- 🔵 Coaching insights not connected to projects/trials
- 🔵 No tracking of "Constructive Failures" (trials + learnings)

**The Need:** Convert coaching insights into actionable experiments. Track what you tried, what you learned, and which quests/pillars it connects to.

**What to Design:**

1. **Project Template** (YAML + Markdown structure)
    
    - Fields: name, status, linked quest, timeline, success metrics, trials, learnings
    - Tracks: Which priority area? Which coaching session inspired it? What did we learn?
2. **Integration Points**
    
    - Wiki: Quests reference projects; project updates appear in quest timeline
    - Coaching: Sessions suggest new projects or reference active ones
    - Logging: Projects inherit pillar tagging from parent quest
    - Tracking: Can query "active projects this quarter" or "projects that failed and why"
3. **Data Model**
    
    - Does each project get its own folder in `/04_project/`?
    - Or should projects live within pillar folders alongside quests?
    - How should we track: Project → Coaching Session → Wiki Quest → Pillar → Learnings?

**Next Step:** Clarify project location/structure, then design wiki-coach integration points.

**Estimated:** 2-3 weeks (parallel with Module 2)

## Part 3: Implementation Priority & Sequencing

### Build Sequence (Revised — Priorities Reordered)

|Phase|Component|Status|Priority|Timeline|Blocking Notes|
|---|---|---|---|---|---|
|**2.1**|Module 2 + Database Design|🔴 Next|🔴 URGENT|1-2 weeks|Unblocked; enables Module 3 planning|
|**2.2**|Project Template & Flow Integration|🔴 New|🔴 URGENT|2-3 weeks|Parallel with Module 2; integrates into wiki|
|**2.3**|Ad-hoc Coach Skill|🔴 Next|🟡 High|1-2 weeks|Unblocked; doesn't depend on other modules|
|**2.4**|Input Consolidation Decision|🔵 Blocked|🟡 High|Decision only|Choose A/B/C → unblocks Module 3|
|**2.5**|Module 3 (Context Extraction)|🔵 Blocked|🟡 High|2-3 weeks (after 2.4)|Depends on Module 2 + decision|
|**2.6**|Module 1 Enhance|🔵 Blocked|🟡 High|1 week (after 2.5)|Improve capture, integrate with Module 3|
|**3**|Module 4 (Entity Sorting)|🔵 Planned|🟢 Medium|2-3 weeks|After all Phase 2 modules|
|**3**|Ad-hoc Skills (Weekly, Monthly)|🔵 Planned|🟢 Medium|2-4 weeks|After Phase 2 stabilizes|

---

### Next Steps (🔴 BLOCKED until decisions made)

#### 🔴 URGENT: Module 2 + Database Design

**What to build:**

1. **Module 2 (Routing/Sorting System)**
    
    - Route daily notes → `/01_raw/_daily_note/`
    - Route web clips → `/01_raw/_web_clips/`
    - Route transcripts → `/01_raw/_transcripts/`
    - Route ebooks → `/01_raw/_ebooks/`
2. **Database Table Structure** (for Module 3 pipeline)
    
    - Design schema to store: URLs, book/author/movie names, metadata
    - Support: URL source, content type, capture date, capture context
    - Support: Processing status (raw → digested → in wiki)
    - Support: Linking to resulting wiki pages once processed
    - Consider: SQLite (simple, local) vs. structured JSON files (simpler integration)

**Purpose:**

- Organize captured content by type
- Create audit trail for routing
- Enable Module 3 to query what needs processing
- Track content through digestion pipeline

**Success Criteria:**

- ✅ Daily notes, web clips, transcripts, ebooks have dedicated routing
- ✅ Database can store metadata from Module 1 captures (URL, name, type, date)
- ✅ Can query "what needs digesting" for Module 3
- ✅ Can track "has this been processed into wiki yet?"

**Estimated:** 1-2 weeks

---

#### 🔴 URGENT: Project Template & Flow Integration (Parallel Workstream)

**What to build:**

1. **Define Project Template Structure**
    
    - Project YAML frontmatter (name, status, linked quest, timeline, success metrics)
    - Project markdown structure (Overview, Trials/Experiments, Learnings, Status)
    - Example project files with best practices
2. **Integrate Projects into Wiki Flow**
    
    - Quests can now reference projects (1 Quest : N Projects)
    - Wiki-coach-kms-cli: When updating quests, also check/update linked projects
    - Coaching sessions can reference active projects and suggest new trials
    - Projects inherit cross-pillar tags from parent quest
3. **Project-to-Coaching Connection**
    
    - Coaching sessions identify: "This aligns with Project X, consider trial Y"
    - Projects track: "Started from coaching session dated YYYYMMDD"
    - Trials emerge from coaching → get logged as projects → tracked for learnings

**Purpose:**

- Convert coaching insights → actionable projects (trials)
- Track "Constructive Failures" as experiments with learnings
- Link back: Project → Coaching session → Wiki quest → Pillar
- Enable weekly/monthly review of "what did we try, what did we learn"

**Success Criteria:**

- ✅ Project template defined and documented
- ✅ Pillar indexes now show "Active Projects" alongside quests
- ✅ Coaching sessions can suggest/reference projects
- ✅ Wiki processing can detect and link to relevant projects
- ✅ Can query "what projects are active this quarter"

**Estimated:** 2-3 weeks (parallel with Module 2)

**Blocking:** Clarify: Should projects live in `/04_project/[Project_Name]/` or scattered across pillar folders?

---

#### 🟡 HIGH: Ad-hoc Coach Skill

**What to build:**

- Standalone skill to continue coaching conversations
- Input: Previous coaching session(s) + current question/challenge
- Context: Load `_priority.md` + `_POS.md` + recent `_log.md`
- Output: Continued coaching conversation (not tied to wiki update)
- Triggered ad-hoc, no dependency on wiki processing

**Purpose:**

- Enable mid-week priority check-ins
- Deeper exploration of open items from prior sessions
- Coaching on specific challenges without new inputs

**Success Criteria:**

- ✅ Can run anytime without wiki processing
- ✅ Respects current priorities and POS constraints
- ✅ Can reference previous coaching sessions
- ✅ Produces 1.5-3 page conversational output

**Estimated:** 1-2 weeks (unblocked, can start anytime)

---

#### 🔵 BLOCKED: Input Consolidation Decision

**What to decide:** Choose one of three models for handling captured URLs/content:

**Option A: Two-Tier Processing (Context Extraction)**

1. Tier 1: Apple Shortcuts captures raw URL + name/text
2. Tier 2: LLM fetches & extracts → Creates digested note with themes/insights/connections
3. Result: Digested artifact ready for wiki processing

**Option B: Direct Processing**

- Store URLs → During wiki processing, fetch & process inline → No separate digestion

**Option C: Hybrid (Manual Flagging)**

- Store URLs → Manual flag "needs digestion" → Only flagged items get extracted → Rest go to input folder

**Unblocks:** Module 3 design and implementation

---

#### 🔵 BLOCKED: Module 3 (Context Extraction)

**What to build:** (after input consolidation decided)

1. **Web Article Extraction**
    
    - Fetch URL → Extract core claims, evidence, implications
    - Map to your pillars (which life areas are relevant?)
    - Create structured markdown with source, key insights, connections
2. **Video/Transcript Extraction**
    
    - Summarize key points, moments, learnings
    - Identify: Speakers, topics, actionable insights
    - Create structured markdown ready for wiki
3. **eBook/Article Extraction**
    
    - Extract relevant chapters, quotes, frameworks
    - Summarize key themes and how they connect to your work
    - Create structured markdown

**Output:** Digested artifacts stored to `/01_raw/_digested/` or directly to input folder

**Depends on:** Module 2 database design (to query what needs processing)

---

#### 🔵 BLOCKED: Enhance Module 1 + Build Module 2 Sorting

**What to build:** (after Module 3 designed)

1. **Improve Module 1 (Apple Shortcuts)**
    
    - Capture not just URL + name, but context (why am I saving this? which pillar?)
    - Integrate with Module 3 workflow (trigger digestion)
    - Add quick tagging/categorization
2. **Complete Module 2 (Routing)**
    
    - Route digested artifacts appropriately
    - Maintain audit trail through processing

---

### Next Steps (Immediate Actions)

**This week:**

1. Define Module 2 routing structure (folders, metadata)
2. Design database schema for storing captured metadata
3. Define Project template structure
4. Clarify: Where should projects live? (single folder vs. pillar-based?)

**Next week:**

1. Start building Module 2 + database
2. Start designing Project-Wiki integration
3. (Optional) Begin ad-hoc coaching skill

**Success Criteria for Phase 2.1-2.2:**

- ✅ Module 2 routing working (daily notes, clips, transcripts, ebooks separated)
- ✅ Database stores metadata from captures
- ✅ Project template documented and examples created
- ✅ Wiki-coach-kms-cli can reference active projects
- ✅ Coaching sessions can suggest new projects/trials
- ✅ Can track: "This project came from coaching session X on quest Y"

---

## Appendix: Model Choices & Cost Optimization

For reference, here's the cost landscape for running wiki + coaching synthesis at scale (100K-token input, 6–8K token output per run):

|Model|Cost per Run|Best For|Trade-off|
|---|---|---|---|
|**DeepSeek V3.2**|~$0.01–0.03|Cheap batch processing|Reasoning quality lower than Opus/GPT-4o|
|**Claude Haiku**|~$0.15–0.35|Fast, cheap, good enough|Best for quick wiki updates|
|**Qwen 2.5 72B**|~$0.05|Solid mid-tier|Limited availability|
|**Claude Sonnet**|~$0.42|Strong all-rounder|Mid-tier cost|
|**Claude Opus**|~$0.70|Highest quality|Expensive for daily runs|
|**GPT-4o**|~$0.33|Strong reasoning|Comparable to Sonnet|
|**Gemini 3.1 Pro**|~$0.30|Fast reasoning|Good for complex synthesis|

**Recommendation:**

- **Daily wiki updates:** Use Haiku or DeepSeek (cheap, sufficient)
- **Weekly coaching synthesis:** Use Sonnet or GPT-4o (better reasoning)
- **Monthly audit:** Use Opus (highest quality for deep analysis)
- **Ad-hoc coaching:** Use Sonnet (conversational, real-time)