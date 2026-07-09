---
name: KMS Development & Journey
pillar: LifeManagement
status: active
type: topic
created: 2026-05-03
updated: 2026-07-04
description: Personal Knowledge Management System development and documentation
tags:
  - LifeManagement
  - CreativityCuriosity
---

# [[KMS-Development]]

## Background

- Tried various tools before: n8n, Make, Feishu, Tana, Notion—all without systematic approach
- Had bad experiences with each; need better understanding of why (ref: [[2026-04-12]])
- Inspired by [[llm-wiki]] concept and great content creators' frameworks

## Development Approach

- Refined personal requirements first (ref: [[2026-04-12]])
- Split into modules with clear MVP + future versions (ref: [[2026-04-12]])
- Get MVP running with existing resources (Gemini Pro) (ref: [[2026-04-12]])
- Continuous iteration (ref: [[2026-04-12]])

## Documentation

- Planning Xiaohongshu (Little Red Book) content series about KMS journey (ref: [[2026-04-12]])
- Share learnings from tool experiments with audience

## Note-Taking Friction Points

Real pain points surfaced as requirements for KMS (ref: [[2026-05-06]]):

- **Lost serendipity**: Random books, authors, movies, YT videos — forgotten because no capture habit with context
- **Deferred relevance**: Even when captured, no time to read/watch immediately, and no clear record of *why* it was relevant
- **Missing personal relevance layer**: Need summary + highlight of sections relevant to *me* — not just information, but actionable steps to try something new (e.g., new workout, note-taking method, good habit)
- **Gemini canvas retention**: Discussion insights in AI canvas not easy to retain
- **Thought isolation**: New thoughts lack connection to existing ones — is it truly new, or building on prior ideas? What to do with it? No way to review by current priority
- **Friction in capture**: Apple Notes used most for capture; voice recording rarely used. Copying links from video/social posts into notes is annoying
- **Priority review gap**: After documenting thoughts, no way to surface them based on what matters *now*

**Ideal KMS behavior**: Know when a thought is new vs. building on existing; suggest implications and actions based on current interests and priorities; recommend relevant sections of saved content based on current focus.

## Tool Research: Obsidian Workflow Solutions

Articles saved 2026-05-20/21 — addressing the friction points above (ref: 文章/2026-05-20, 文章/2026-05-21):

**Capture friction solutions:**
- **Obsidian Web Clipper** (official plugin): One-click save of web content + YouTube transcripts as Markdown. Can add AI "interpreter" for auto-summarize in Chinese using Why/How/What structure. Addresses the "link copy-paste annoyance" and "missing personal relevance layer" friction points. Enhanced Chinese version supports Bilibili and Feishu: `github.com/nextcaicai/obsidian-clipper-cn`
- **Obsidian + WeChat bot** (chatgpt_on_wechat): Automatically saves WeChat articles and messages to Obsidian by acting as a second WeChat account. Addresses link capture friction from social/mobile context. Selenium-based scraping of article content.

**AI integration:**
- **Claudian plugin** (`github.com/YishenTu/claudian`): Embeds Claude Code as an AI agent directly inside Obsidian vault. Supports inline edit, multi-tab chat, Plan Mode, MCP servers, @mention files, slash commands. Data fully local. Vault becomes the agent's working directory for file read/write, search, command execution. — Directly relevant to the [[Life_Management_System]] KMS project.

**Workflow/organisation:**
- **Image Converter plugin**: Auto-renames images and converts format on paste; stores in `images/` subfolder per note. Addresses messy image management.
- **draw.io + Obsidian (Diagrams plugin)**: Allows architecture/diagram creation via natural language inside Obsidian (via opencode). Relevant for KMS architecture visualisation.
- **Symbol/notation consistency guide**: Article on Chinese/English punctuation conventions for Obsidian notes.

**Emergent 4th priority (ref: [[coaching_discussion_20260518]])**: KMS/AI system integration — connecting siloed systems via AI assistant — has the highest momentum currently and is functioning as a cross-priority engine for all three main priorities.

## Coaching Session Format Feedback

- (new) **Clarity on what coaching session should and shouldn't do (2026-05-28)**: Coaching session output should remind what is *new* and what is *important*. The actual backlog — list of projects, things to do, learn, read — should live in `_in_case_you_are_bored.md` or other archive/append logs, not clutter the coaching session itself. Coaching = signal, not the full list. May need to revisit format to sharpen this distinction (ref: [[2026-05-28]])
- (new) **The "put it away and surface when relevant" principle**: Not everything needs to be top-of-mind. The KMS should support deferring items gracefully — they'll surface when the time is right or when explicitly searched. The coaching session is not the right place for comprehensive review; it's for current relevance + new signal (ref: [[2026-05-28]])

## New Tool Ideas (2026-05-28)

- (new) **Daily notes as training log input**: Use daily note as primary log for training energy and notes, eliminating need for a separate log. Add a specific section to the daily note template for training tracking (ref: [[2026-05-25]])
- (new) **Apple Shortcut for sleep + workout data**: Input sleep data and calendar-based actual workout data via Apple Shortcut to reduce manual logging friction (ref: [[2026-05-25]])

## Connections

Related Pages: [[Information-Overload]], [[Project-Ideas]], [[Public-Knowledge-Sharing]], [[Sleep-Optimization-Routine]], [[Life_Management_System]]


## Claude Code Ecosystem (2026-05-29–06-06 batch)

Multiple articles converging on Claude Code as the primary AI development environment:

- (new) **Claude Code session memory via Obsidian (ref: [[让 Claude Code 不再失忆：基于 Obsidian 的会话管理机制实现|让 Claude Code 不再失忆]])**: Pattern to retain conversation context across sessions by logging to Obsidian vault. Directly relevant to the AI assistant project — addresses the "context loss between sessions" friction point.
- (new) **Obsidian CLI stability with AI (ref: [[终于知道怎么让AI稳定使用obsidian-cli了！]])**: Techniques to stabilize obsidian-cli when used from AI agents. Now validated in this very workflow.
- (new) **Remote Claude Code access via 扣子3.0 (ref: [[扣子3.0，让我不再担心网络ip，遥控家里的 Claude Code 干活|扣子3.0]])**: Method to control Claude Code running at home from anywhere via network tunneling. Relevant when travel + coding overlap.
- (new) **AI can directly operate Obsidian via Local REST API (ref: [[装了这个插件，你的Obsidian终于能被AI直接「操作」了｜Local REST API完全指南|Local REST API完全指南]])**: Plugin that exposes Obsidian to AI control over HTTP. Alternative to obsidian-cli — worth comparing when building Module 2.
- (new) **Three-layer AI work system (ref: [[三层AI工作系统：Obsidian、Agent与飞书的知识管理闭环|三层AI工作系统]])**: Obsidian (capture/store) → Agent (process/synthesize) → Feishu (collaborate/output). Useful architecture schema for KMS module design.
- (new) **Claude Code 101 tutorials**: Multiple tutorials ([[从零玩转Claude Code：真实案例带你深度上手|从零玩转Claude Code]], [[如何利用一个周末掌握 Claude Code]]) and [[16个Claude高效技巧，让你的工作效率飞升！|16个Claude高效技巧]] saved. Quality reference for onboarding or revisiting fundamentals.
- (new) **draw.io in Obsidian (ref: [[Obsidian+opencode+draw.io：让架构图绘制融入笔记工作流！|Obsidian+opencode+draw.io]])**: Architecture diagrams via natural language inside vault. Useful for visualizing KMS module design.
- (new) **AI agent browser control comparison (ref: [[AI Agent 浏览器控制工具横评（2026）|AI Agent 浏览器控制工具横评2026]])**: Market comparison of tools for AI-controlled browsing. Relevant when Module 2 (web content extraction) is designed.
- (new) **Bright Data crawler agent (ref: [[GitHub上这个新式爬虫智能体真的好用|GitHub crawler agent]])**: Web scraping agent — option for article ingestion in Module 2 backlog.
- (new) **AI prompt tips for personalized output (ref: [[别再给AI贴标签：两个技巧让AI输出高质量、个性化内容|别再给AI贴标签]])**: Two techniques to avoid generic AI output: no labels, specific context anchoring. Applicable when designing coaching prompts.

## Karpathy LLM Wiki Ecosystem (2026-05-29 batch)

- (new) **LLM wiki explained (ref: [[Karpathy LLM wiki到底是什么？一个视频讲清楚|Karpathy LLM wiki到底是什么]])**: Orientation video — confirms the framework used as KMS inspiration is now widely discussed.
- (new) **Karpathy open-sourced Agent + Obsidian wiki (ref: [[Karpathy 开源了 Agent + Obsidian 个人知识库， 超级有启发。|Karpathy 开源了]])**: The actual repo is now public. Worth reviewing architecture decisions directly from source.
- (new) **Karpathy wiki desktop app (ref: [[Karpathy 的知识库构想被人做成桌面应用了，而且做得相当扎实，已在 Github 上斩获 5.8k+ Star！|知识库构想被人做成桌面应用了, 5.8k stars]])**: Third-party desktop implementation. Another reference point for Module architecture.
- (new) **How to build Obsidian wiki from scratch (ref: [[如何从零搭建Obsidian知识库：Karpathy框架+手把手实操|如何从零搭建Obsidian知识库]])**: Tutorial using Karpathy framework + hands-on walkthrough. Reference for anyone onboarding to the system.

## Tool References (low-priority backlog)

- (new) **Tolaria**: New note-taking app combining Obsidian + Notion advantages, local + open source. Worth monitoring — not switching now.
- (new) **Gemini CLI + Obsidian**: Alternative AI+Obsidian integration path. Reference only.
- (new) **Obsidian Web Clipper maximization (ref: [[如何把Obsidian Web Clipper价值最大化？]])**: Tips for getting more from Web Clipper — in AI assistant backlog.
- (new) **13 Obsidian clipping templates (ref: [[死磕Obsidian剪藏！分享13个Obsidian剪藏模板～|死磕Obsidian剪藏]])**: Template library for Web Clipper — in AI assistant backlog.
- (new) **Obsidian directory structure guide (ref: [[纠结Obsidian目录结构？我梳理了一份指南|纠结Obsidian目录结构]])**: Survey of organizational approaches — worth cross-checking current KMS structure once.

## AI Frontier Notes

- (new) **Anthropic calling for global pause on AI development (ref: [[AI自进化过快，Anthropic呼吁全球中止研发|AI自进化过快]], 2026-06-05)**: Self-governance signal from within the AI industry. Worth tracking for implications on AI tool stability and trust.
- (new) **ChatGPT + Codex merged (ref: [[今天，ChatGPT与Codex官宣合体！10亿人喜提「超级Agent」|今天ChatGPT与Codex官宣合体]], 2026-06-04)**: OpenAI competitive move. Confirms Claude Code vs Codex competitive landscape is shifting fast.

## 超体 Course Context (ref: [[AI_learning]])

Enrollment survey submitted June 2026. Key self-assessment extracted:

**(new) Current AI penetration**: 10–30% of daily tasks; primarily SQL/data analysis, KMS system, virtual-self coaching

**(new) AI management philosophy**: AI as a tool — not fully reliable, requires human validation, context quality determines output quality; leverage for efficiency, blind spot discovery, decision-speed improvement; guard against laziness and dependence

**(new) Primary pain points for resolution via course**:
- Tool FOMO: too many models/tools, selection paralysis
- ROI calibration: when is AI worth the token cost vs. traditional methods?
- Vibe coding ceiling: how to evaluate whether AI output meets requirements when uncertain
- Mobile/desktop integration gap
- Build-vs-buy decision framework (custom tool vs. off-shelf for repeating vs. one-off needs)

**(new) Desired work application**: After KMS, priority is maximizing AI use in commercial data and business analysis — the domain where the gap between AI capability and actual usage is highest

**(new) Core system insight from survey**: KMS solves the "none of this is connected" problem — M1 (POS) → M2 (KMS) → M3 (life coach) → M4 (project mgmt) → M5 (schedule), each generating insights that feed back upstream. The positive feedback loop is the value.


## New Tool References (June 2026 batch)

- (new) **Anthropic Prompt Engineering 101 (ref: [[Anthropic 提示词工程101：从零构建优质提示词]])** — AI Learning backlog. Key question flagged: what can I start using today? Add to 超体 course prep reading.
- (new) **Obsidian 10 best AI Skills (ref: [[Obsidian 10大AI Skill ，第1名安装量37万]])** — Check which of the top-installed are worth trying to upgrade Obsidian+AI game.
- (new) **Codex + Obsidian second brain schema (ref: [[Codex + Obsidian ，建立第二大脑]])** — Alternative architecture reference; review before next LMS module design decision.
- (new) **Obsidian vault template collection, 48 vaults (ref: [[Obsidian vault 模板库合集：48 个 GitHub 上的宝藏 vault，下载即用]])** — Cross-check current KMS structure once; look for gaps or structural improvements.
- (new) **LM Studio phone→PC local LLM control (ref: [[LM Studio史诗级更新：你的手机，从此能指挥电脑里的大模型了]])** — Addresses mobile/desktop integration gap. Check when mobile integration is next priority.
- (new) **WeChat → Claude Code Skill update (ref: [[在你微信里用爽 Claude Code，我的开源 Skill 又更新了。]])** — WeChat bridge; useful for mobile-to-vault capture.
- (new) **AI clipper → Codex integration (ref: [[我的 AI 剪藏小狗，终于把资料叼进 Codex]])** — Alternative clipping architecture idea; reference when revisiting M2 input pipeline.
- (new) **Claude Code 5 investment SKILLs (ref: [[Claude Code 5大投资必装SKILL]])** — Finance-specific Claude Code skills; relevant when BQ/GCP session starts.
- (new) **Token resource roundup June 2026 (ref: [[6月最新汇总：国内外Token羊毛大合集（建议收藏）！]])** — Reference for when token costs become a constraint; revisit if needed.


## PKM Paradigm Validation: Karpathy + Plugin Hygiene (June 2026)

- (new) **Karpathy LLM Wiki paradigm validated externally (ref: [[Obsidian+workbuddy：轻松复刻AI大神Karpathy的个人本地知识库|Obsidian+workbuddy]], 2026-06-06)**: Core framing: AI as knowledge *compiler* rather than *retriever* — Raw→Wiki→Outputs with CLAUDE.md as instruction layer. This is precisely the architecture already running here. Multiple independent sources (WorkBuddy article, Karpathy's open-source release, community builders) confirm the design is directionally correct. WorkBuddy is the Chinese-user-friendly desktop alternative; Claude Code + obsidian-cli is more programmable with no walled-garden limits.
- (new) **Actions URI pattern confirmed for iOS integration (ref: [[8 Obsidian Plugins That I Can't Live Without]], 2026-06-06)**: Mike Schmitz's #1 essential plugin is Actions URI — the iOS Shortcuts bridge that writes to Obsidian periodic notes. This is architecturally identical to the Action Button shortcut built into this KMS. Confirms the integration pattern is mature and battle-tested.
- (new) **Plugin hygiene principle (ref: [[8 Obsidian Plugins That I Can't Live Without]], 2026-06-06)**: Lean vault over feature-rich vault. Choose plugins that fit defined PKM workflows, not as feature collection. Two plugins with KMS application to watch: *Keep the Rhythm* (writing heat map, builds consistency habit) and *QuickAdd* (keyboard-driven macro automation, append to daily note from anywhere).
## AI as Power User Tool — Reflections (June 2026)

- (new) **AI's three core strengths**: (1) Customization — any idea can be realized as a fully bespoke solution, deeply liberating for someone specific and opinionated; (2) Information processing efficiency — finds logic across vast data, offers multiple implementation options; (3) Sounding board — when no idea exists, AI coaches through questions into a structured output that originates from you. (ref: [[2026-06-21]])
- (new) **Control + Customization appeal**: Jeroen named it directly — attraction to AI is partly attraction to mastery and control. Highly personalized outcomes = liberation for a specific, opinionated person. (ref: [[2026-06-27]])
- (new) **Vibe Coding learning curve reality**: Despite "everyone can be a programmer" narrative, the learning curve remains steep. Requires fluency with professional terminology; AI guidance needs to be very detailed. Still significantly easier than pure self-study. (ref: [[2026-06-27]])
- (new) **Three future user tiers**: (1) Power Users — know exactly what they want, build their own tools; (2) Regular consumers — use pre-built apps, minimal configuration; (3) Professionals — PM + developer + analyst working together at higher level to build apps that anticipate general user needs. (ref: [[2026-06-27]])
- (new) **App as packaged automation**: A well-designed app = specific input → specific output with packaged workflow in between. Like wrapping a prompt into a skill. The skill (self-awareness, clarifying requirements, validating AI output) is not yet universally democratized. (ref: [[2026-06-27]])
- (new) **Future app model**: AI-mediated feature marketplace — an app offers 1000 features, user AI trims to 300 relevant ones, evolves with use. Like enterprise SAP/Oracle tailoring, scaled to individual. (ref: [[2026-06-27]])
- (new) **Professional judgment requirement**: For generic (multi-user) apps, complexity is exponential — must design for many different use cases with fallbacks. This remains a specialized skill that AI augments but does not replace. (ref: [[2026-06-27]])


## Stanford AI System Architecture — Builder's Map (ref: [[一部影片看完 Stanford AI 系統課程，從 LLM 到 Agentic Workflow|Stanford AI Systems]])

(new) **The Vertical Axis principle**: You can't train a better base model — that's OpenAI/Anthropic's job. Your leverage is the *vertical axis*: augmenting existing LLMs with engineering layers on top. Every KMS module is a vertical-axis project.

(new) **LLM augmentation stack** (low to high):
1. **Prompt Engineering** — the universal baseline; Prompt Chaining is the most powerful sub-skill: split one complex prompt into sequential steps where each output feeds the next. Gives you *observability* — you can debug which step failed. (This is exactly how wiki-coach-kms-cli works.)
2. **Fine-Tuning** — avoid unless absolutely necessary: requires massive quality-labeled data, overfits to narrow domain, new base model versions obsolete your fine-tune in weeks.
3. **RAG** — the right answer when fine-tuning is impractical: embed documents into vector DB, retrieve semantically similar chunks at query time. Solves: stale knowledge, hallucination, domain gaps.
4. **Agentic Workflow** — LLM with tools (web search, code execution, function calls) + planning loop. The KMS skill system is this tier.
5. **Multi-Agent** — multiple specialized agents with defined roles, one orchestrator. Future architecture direction for KMS when modules need to run concurrently.

(new) **Centaur vs Cyborg — the framework for choosing AI usage mode**:
- **Centaur** (半人馬, batch-delegation): Write one long prompt, hand off, do other things. Right for: repetitive, process-clear tasks. KMS wiki-coach is Centaur mode.
- **Cyborg** (生化人, high-frequency): Sentence-by-sentence back-and-forth collaboration. Right for: judgment, creativity, iterative correction tasks.
- No hierarchy — consciously switch based on task nature. Most work uses both in different phases.

(new) **Jagged Frontier** (鋸齒邊界): AI doesn't uniformly excel across all tasks. Some tasks — AI dramatically boosts performance. Other tasks — AI makes output *worse* than no AI. The BCG experiment (Boston Consulting Group, 2024) with management consultants found: "Falling asleep at the wheel" — when you don't know a task falls in AI's weak zone, over-trusting AI and shipping the output without review produces results worse than no AI. Knowing your own Jagged Frontier is a meta-skill.

(new) **Prompt Chaining observability principle**: A single monolithic prompt is a black box — when output is wrong, you can't tell which reasoning step failed. Breaking it into a chain of smaller prompts makes each step independently testable and debuggable. Same reason wiki-coach has ordered steps rather than one giant instruction block.

## n8n as Backend Executor (ref: [[用Claude Code自动编排n8n工作流，告别手搓。|n8n + Claude Code工作流]])

(new) **Community consensus on agentic + n8n architecture**: Don't route every task through the LLM agent directly. Pattern: LLM agent (Claude Code) handles planning/decision → n8n handles *fixed, repetitive execution* via webhook call. Benefits: (1) token costs drop dramatically — fixed workflows don't need an LLM deciding each step; (2) API keys stay in n8n, not in agent context = security. 

(new) **Agent writes the n8n workflow, not you**: With n8n MCP + n8n Skills, you can instruct Claude Code to generate the workflow from natural language. No manual node-dragging. Agent writes it once → n8n runs it N times. This matches the app-as-packaged-automation framing: AI wraps the one-time intelligence into a reusable system.

(new) **Application to KMS future modules**: KMS currently runs entirely via Claude Code CLI (pure agent). Once patterns stabilize, high-frequency execution steps (daily note ingestion, article scanning, POS signal generation) are candidates for n8n backend execution, with Claude Code as the orchestrator calling webhooks.
