---
name: _priority
description: Single source of truth — priorities, active & parked projects, ideas, and cross-pillar synergies
updated: 2026-09-03
---
打开这个文档，从上到下依次回答：现在应该关注什么？→ 有哪些项目在推进？→ 为什么是这些？

**Last Updated:** 2026-09-03
**Links:** `/project-review` for priority re-ordering | `/project-context [name]` to start a focused session | `/Project-Initiation` to formalize a backlog idea

---

## Annual Bottom Lines (2026 — 三条并行底线)

*底线 = AND 逻辑：三条都完成，2026 才算达标。不排序、不互相牺牲。*

| 底线 | 内容 | 年度判据 |
|------|------|----------|
| **Foundation 地基** | App dev + Physical（训练 / Meal prep）+ Home | 身体能自动跑（sleep ≥80%、meal prep 3-5 可重复菜、训练有 AI 反馈闭环）；Home 年底前完成 Phase 2 |
| **Leverage 杠杆** | AI learning + 财务 | 超体 Ch5→Ch18 完成并启动变现路径；财务全自动 + Q4 税务落定 |
| **Relationship 关系** | 父母 + 男友 | October gate 出明确结果（cohabitation/ENM/kids 不再 suspended）；父母 Phase 1 启动 |

---

## Execution Cadence (now → Sept 2026)

*执行 = WHEN 逻辑：同一时刻主推 1-2 件，其余到点再动或自动跑。*

| 状态 | 事项 | 时间 | 说明 |
|------|------|------|------|
| 🔥 主战场 | Physical（workout plan 改造） | 9 月 | 两个 dance intensive 后的 inspiration momentum，趁热改；概念层落点见 [[Training]] Decisions |
| 🔥 主战场 | Home（excessive 物品清理 + Plants） | 9 月中旬后 | 基础 clean-up + cleaner ✅ 已完成；剩余部分需要周末大块时间，按 Weekend Allocation 排 |
| 🟡 待重启 | Meal prep | 9 月下旬 | 停滞中。归类从「家务/采购」改为「训练输入」——它是 workout plan 改造的另一半 |
| 🟡 待重启 | AI learning | 9 月下旬 | 超体 Ch5→Ch18，一周两章；晚间 activity 密集期结束后重启 |
| ⏸ 主动暂停 | App dev | 无期限 | 日常只用 scheduling，未 active 使用 → 没痛到需要「先做哪个」决策器。重启条件见下 |
| ⏳ on-deck | Relationship（父母 + 男友） | 父母 9 月下旬 · gate → 12 月 | Jeroen 11/12 搬入自购公寓；10–11 月为思考窗口 |
| 🛟 自动驾驶 | Finance | Q4 | net worth 月度 review + Q4 避税 |

**App dev 重启条件（三者任一成立）：** ① meal prep 需要认真做 priming；② 个人 priority 真的管不过来、需要外置决策器；③ 超体学完后对 app 该怎么长有新的整体判断。在此之前不加新 feature。

**🚫 Parked（不在执行节奏内）：** Training_Program 概念层（图纸不改，但本轮 workout plan 改造的决策要落在这里）· Design_your_life（Q4）· 其余 Q4 deferred ideas

---

## Weekend Allocation（大块时间的分配方法）

*周末是最稀缺的资源，且部分不可预测（海牙 / 临时演出）。所以不排「哪天做什么」，只排「哪个周末归谁」。*

**状态不用手填 —— 直接读 calendar（2026-09-03 定）**

```bash
python3 scripts/weekend_status.py --weeks 8      # 表格
python3 scripts/weekend_status.py --json         # 机器可读
```

判定规则（脚本已实现，只读权限，从不写 calendar）：

| Location calendar | 主 calendar | 判定 |
|---|---|---|
| 有 `DH` | — | 🔒 **已占用** — 在海牙，不排大块事项 |
| 只有 `AMS` | 无演出 | 🟢 **可用** — 在家 |
| 只有 `AMS` | 有演出 | ⚠️ **待定** — 演出通常会吃掉周边时间 |
| 都没有 | 有演出 | 🔒 **已占用** |
| 都没有 | 无演出 | ⚠️ **未填** — 空 = 未定，未定的周末最容易被吃掉，所以不当成 🟢 |

只有标题**严格等于** `AMS` 或 `DH` 的事件才算 location marker（与 App `/api/location/plan` 同规则，Session 27 决策）。主 calendar 侧用关键词识别演出（show/performance/ballet/opera/concert/演出/首演…），并排除 dinner/lunch/gym/reformer 这类日常项——它们不构成占用。

**为什么「空」算待定而不算可用：** 空只说明还没决定，而没决定的周末正是会被临时演出或临时去海牙吃掉的那些。当成 🟢 排了大块事项，等于把计划建在最不稳的格子上。

**方法：月初一次，五分钟**

1. **跑一次脚本**拿到状态（🔒 已占用 / 🟢 可用 / ⚠️ 待定或未填）
2. **每个 🟢 周末只分配一件大块事项。** 一个周末塞两件 = 两件都做不完。
3. **⚠️ 周末不分配任何事**，它是缓冲；真的空出来就从队列顶部拿一件。
4. **每件大块事项带一个 deadline。** 被挤掉就顺延到下一个 🟢；**顺延到超过 deadline，就是降 scope 或改 deadline 的信号**——不是再顺延一次。

**关键拆分：把「采购」从「执行」里拆出来。** 植物这类事之所以吃掉整个下午，是因为「诊断 → 去店里买 supply → 动手」串成了一条链。先用工作日十分钟做诊断、列出 supply 清单，采购挪到工作日晚上或线上，周末那个半天就只剩纯执行——半天变成两小时，而且能排进 ⚠️ 周末。

**分工：** `weekend_status.py` 读 calendar 回答「这个周末我能不能干活」；App 的 Weekend Planner（Coaching tab → `weekends` scope，Session 27）负责**写** AMS/DH（12 周视图 + 批量文本解析 + 写回 Google Calendar）。两者读同两个 calendar ID，规则一致。**「这个周末归哪件事」由下方队列决定**，不需要为此重启 app 开发。

### 待排队列（按 deadline，不按周末）

*每次有 🟢 就从顶部取一件。这样周末状态变化不需要重排整张表。*

1. **Plants Phase 2+3** — 换盆 / 修剪 / 光照分区 · 需半天 · deadline 9 月底 · **前提：supply 已在工作日买齐**
2. **Meal prep 启动** — 容器采购 + 第一次周日 batch · 需半天 · deadline 10 月中
3. **Excessive 物品清理** — 可切块，两小时起 · 无硬 deadline · 适合塞进 ⚠️ 周末
4. **Hardware Checklist**（[[Strategic_Relationship_Audit]]）— 需要安静的整块思考时间 · deadline 12 月对话前

**不占周末（工作日晚间即可）：** 介壳虫**隔离**（2 分钟，本周内——隔离和处理是两件事）· 植物诊断 + supply 清单（10 分钟）· 超体一周两章 · 父母第一次通话（一个安静的晚上）

### 当前分配

*状态由脚本读出，非手填。最近一次核对：待首次运行（需先配 OAuth，见脚本 docstring）。*

| 周末 | 状态 | 归属 |
|------|------|------|
| 9/5–6 | 🔒 已占用 | — |
| 9/12–13 | 🔒 已占用 | — |
| 9/19–20 | 🟢 | 队列 #1 Plants Phase 2+3 |
| 9/26–27 | ⚠️ 待定 | 缓冲；空出来 → 队列 #3 |
| 10/3–4 | 🟢 | 队列 #2 Meal prep 启动 |

---

## Short-Term Focus (now → September 2026)

> **派生视图，不是第三套排序。** 唯一真相源是上方 **Annual Bottom Lines**（AND 逻辑：什么算达标）+ **Execution Cadence**（WHEN 逻辑：现在推哪个）。本节把两者压平成「当下在做什么」，供 App 读取（Priorities Panel / priming top3 / context alignment 三条 route 依赖本节的 `N. **项目名**` 格式，且编号项必须在某个 `###` 小标题之下才会被 Priorities Panel 收录）。改动请先改上方两张表，再同步这里。

### 当前主推（对应 Execution Cadence 的 🔥 + 🟡）
1. **Physical Foundation** — 两个 dance intensive 后的 workout plan 改造进行中；[[Meal_prep_routine]] 为配套营养输入（停滞待重启）
2. **Studio_Makeover** — 基础 clean-up + cleaner 已完成；剩余 excessive 物品清理 + [[Plant_rearrangement]]（9 月中旬后的周末大块时间）
3. **AI_learning** — 超体 Ch5→Ch18，一周两章；9 月下旬重启
4. **Danseur_Noble_Hub** — 已主动暂停开发（见下方 status），仅 scheduling 在日常使用

**Success metrics（Foundation 底线判据）：** Sleep ≥80% compliance · meal prep 3-5 可重复菜 · 训练有 AI 反馈闭环 · Home 年底完成 Phase 2 · cleaner 常态运行 ✅

**Related:** [[Studio_Makeover]], [[Training]], [[Meal_prep_routine]], [[Danseur_Noble_Hub]], [[Plant_rearrangement]]

---

### Finance（🛟 自动驾驶）

系统全自动运行：automated waterfall + 3-tier 架构（Bucket 2/3 已并入 T212）。AI 投资简报 launchd `com.michael.investment-brief` 每天 16:00 → `Brief/YYYY-MM-DD.md`。Net worth €142,247（2026-09-01），月度 review。Surrogacy 基金口径已锁定。待推进：Q4 合理避税。H1 review submitted (3.92)。

**Related:** [[Road_to_2040_Investment_Blueprint]]

---

### Relationship（⏳ on-deck → 时间线已后移）

**2026-09-03 更新：** October gate 后移至 **December**。Jeroen 11/12 搬入自购公寓（另一城市，非租约，无到期压力），所以「是否搬去同住」不是紧急决策；momentum 会在他搬进去之后才变明显。十月至十一月为思考窗口，12 月做正式 discussion。

- **Parents** — Phase 1 推至 9 月下旬启动（CT intensive 安全层分享）
- **Strategic Relationship Audit** — 6 条 backlog 待激活；hardware checklist 建议在 12 月对话前完成

**Related:** [[Strategic_Relationship_Audit]], [[Parents_Relationship]], [[Design_your_life]]

---

### Parked (not currently active)

Dance_Note（reference library, quarterly review）· Design_your_life（Q4 奥德赛 review）· Show_scraper（Q4 评估 Phase 2）· Microaggression（被动收集）· Travel / Travel_Buddy（park）· Vibe_Coding（超体学完后 revisit）· Iyengar/Gyrotonic/Fighting Monkey（Q4）

---

### Pivot Triggers & Review Cadence

- Jeroen's mother's recovery status changes → affects Priority 3 timeline
- Work situation changes → affects Priority 2
- Major life event (health, family, etc.)
- **Quarterly:** Full assessment, pivots if needed
- **Monthly:** Light touch — is the active priority still the right focus?

---

## Quick Decisions Queue

_<2min 拍板项。batch process：有空时一次性过，resolve 后写回对应项目行并移除本条。_

1. ~~**Net worth 更新频率**~~ → ✅ 已定：月度。已写回 [[Road_to_2040_Investment_Blueprint]]，本条关闭（2026-09-03）
2. ~~**Cleaner prep 范围**~~ → ✅ 已完成：cleaner 已请、已清。本条关闭（2026-09-03）
3. **Q4 避税主题** → 待定：Q4 review 聚焦哪个税项？（capital gains realization / 账户结构 / deductions）
4. **Late-Aug 触发项** → 部分澄清（2026-09-03）：Hardware Checklist 挂到 12 月 gate 前完成（不再是「现在 or defer」，有了具体 deadline）；Alternative career session 和 Energy Budgeting 仍待定 — 9 月下旬那个窗口已经排了三件事，这两条建议 defer 到 Q4
5. **Frontmatter `priority` 字段迁移（元决策 B）** → 部分完成（2026-09-03）：Active Projects 表的 Priority 列已换成火候（execution_state）。frontmatter 的 `priority: P1/P2/P3` **暂不动** — App 的 `/api/context/status` alignment check 仍读它做对比，改之前要先改 app 侧三条 route。App dev 已暂停，所以此条随之 defer

---

## Active Projects

*火候 = `execution_state` frontmatter 字段（main / on_deck / ongoing / autopilot / parked），与上方 Execution Cadence 对齐。P1/P2/P3 已从本表移除——frontmatter 里暂时保留，因为 App 的 context alignment check 仍读它（见 Quick Decisions Queue #5）。*

| Project | ID | Pillar | 火候 | Current Focus | Updated |
|---------|-----|--------|------|---------------|---------|
| [[Life_Management_System]] | pj0001 | LifeManagement | ongoing | Meta-system hub — 5-module architecture map: KMS, Coaching, Training, Project Coaching, Daily Ops | 2026-08-10 |
| [[Danseur_Noble_Hub]] | pj0007 | LifeManagement | ⏸ paused | 主动暂停开发 — 日常仅用 scheduling；重启条件见 Execution Cadence。代码 Session 52 (2026-08-31) | 2026-09-03 |
| [[AI_learning]] | pj0012 | LifeManagement | on_deck | 停滞中 — 超体 Ch5 未开始，9 月下旬重启（一周两章）→ IP 变现 → Anthropic Academy → CS50 | 2026-09-03 |
| [[Parents_Relationship]] | pj0003 | Relationships | on_deck | Phase 1 推至 9 月下旬 — CT intensive 安全层分享，建立真实沟通语境 | 2026-09-03 |
| [[Studio_Makeover]] | pj0005 | AdminHome | main | 基础 clean-up + cleaner ✅ 完成；下一步 excessive 物品清理，需周末大块时间 | 2026-09-03 |
| [[Road_to_2040_Investment_Blueprint]] | pj0010 | Finance | autopilot | Surrogacy 基金口径锁定；GOOGL 第一批完成（ABEA EUR €1,493），跟踪第二批；net worth €142,247（2026-09-01，月度）；Q4 tax review | 2026-09-01 |
| [[Strategic_Relationship_Audit]] | pj0011 | Relationships | on_deck | Gate 后移至 12 月（Jeroen 11/12 搬入自购公寓）；10–11 月思考窗口；6 条 backlog 待激活 | 2026-09-03 |
| [[Meal_prep_routine]] | pj0004 | PhysicalHealth | on_deck | 停滞中，9 月下旬重启。重新归类为训练输入而非家务 | 2026-09-03 |
| [[Plant_rearrangement]] | pj0014 | AdminHome | main | Phase 2 待做（介壳虫检查 + Alocasia 抢救）；换盆/分区需 9 月中旬后的周末半天 | 2026-09-03 |
| [[Training_Program]] | pj0006 | PhysicalHealth | parked | 图纸不改，但本轮 workout plan 改造（两个 intensive 后）的决策要落在这里 | 2026-09-03 |
| [[Design_your_life]] | pj0013 | MindMentalHealth | parked | 找系统性 prompt 重走 DYL exercise；Q4 奥德赛计划 review | 2026-08-10 |

---

## Parked

| Project | ID | Pillar | Priority | Notes |
|---------|----|--------|----------|-------|
| [[Travel_Buddy]] | pj0008 | CreativityCuriosity | P3 | Parked — 下次 travel 前 review。MVP 核心流已完成。 |
| [[Vibe_Coding]] | pj0009 | CreativityCuriosity | P3 | Parked — 超体学完后 revisit |
| [[Show_Scraper]] | pj0017 | CreativityCuriosity | P3 | Parked — Q4 评估 Phase 2 多源扩展 |
| [[Microaggression]] | pj0016 | MindMentalHealth | P3 | Parked — 被动收集模式 |
| [[Travel]] | pj0019 | Travel | P3 | Parked — clarify travel preferences |
| [[Dance_Note]] | pj0015 | PhysicalHealth / CreativityCuriosity | P3 | Reference library — quarterly review |
| [[Flight_Upsell]] | pj0002 | Career | — | Reference only — Portfolio/Analysis/Learnings archive; no longer actively managed |

---

## Recently Completed

| Project | Pillar | Status | Notes |
|---------|--------|--------|-------|
| Skincare_Routine | AdminHome | ✅ Complete | Routine established (home + travel) |
| H1 Performance Review | Career | ✅ Closed | Self-evaluation submitted (3.92) |

---

## Cross-Pillar Synergies

Key themes that connect multiple areas:

- **Portfolio Career** (Career + Creativity + PhysicalHealth) — Location-independence is the gate; once clear, everything else (certifications, teaching, energy system) falls into place | [[Portfolio-Career-Design]], [[Location-Independent-Lifestyle]], [[Movement-Career-Options]]
- **Energy Activation System** (PhysicalHealth + LifeManagement + Career) — Brain dump ritual + exercise tracking + sleep optimization all feed work and creative capacity | [[Energy-Management]], [[Sleep-Optimization-Routine]], [[Fitness-Routine]]
- **Entrepreneurship & Identity** (Creativity + Career + MindMentalHealth) — Which venture you choose reflects who you are; principle: plant seeds, don't force harvest | [[Movement-Career-Options]], [[Identity-Based-Life-Philosophy]], [[Content-Creator-and-Entrepreneurship-Ideas]]
- **LMS Integration** (LifeManagement + PhysicalHealth + Career) — LMS 概念层（KMS + Coaching）→ 执行层（[[Danseur_Noble_Hub]] App + [[Training]] 策略）。Meal Prep 为独立策略项目。| [[Life_Management_System]], [[Danseur_Noble_Hub]]

---

## Future Project Ideas

Ideas with enough context to become a project when priority opens up.

- **Portfolio Career Strategy** — Clarify 70% corporate + 30% teaching structure; resolve location-independence question first | Related quests: [[Portfolio-Career-Design]], [[Location-Independent-Lifestyle]] | Trigger: [[coaching_session_20260509]]
- **Movement Lab / Teaching venture** — Most alive entrepreneurship option; feeds creative passion + body expertise | 4-week research sprint needed | Related quests: [[Movement-Career-Options]], [[Dance-Creation]] | Trigger: [[coaching_session_20260509_retrospective]]
- **Movement Certification (Iyengar or Gyrokinesis)** — Better path than Master's degree; modular, professional level, feeds teaching | Research first: which one? | Related quests: [[Movement-Career-Options]] | Trigger: [[coaching_session_20260509]]
- **Xiaohongshu Content Series** — Share KMS journey + movement/body tips; leverages strategy + emotion + cross-cultural perspective | Start after KMS MVP | Related quests: [[Content-Creator-and-Entrepreneurship-Ideas]], [[Public-Knowledge-Sharing]]

---

## Ideas & Exploration

### Career

- **Clarify location-independence status** — Master filter for next phase; gates portfolio career, family timeline, finances | Action: Manager conversation (exploratory, not negotiation) | Related quests: [[Portfolio-Career-Design]], [[Location-Independent-Lifestyle]] | Source: [[coaching_session_20260509]]
- **Portfolio career visualization** — Sketch what 70% corporate + 30% teaching looks like in a typical week | Related quests: [[Portfolio-Career-Design]] | Source: [[coaching_session_20260509]]
- (new) **Alternative career architecture session** — Dedicated exploration of what long-term career beyond standard corporate looks like; connect all parallel explorations (location-independence, Movement Lab, content creation, AI assistants) into a coherent design. Combine with [[Design_your_life]] exercise. **Trigger: end of August 2026** (after summer intensive + travel). (ref: [[coaching_discussion_20260530]])

### Physical Health

- **Brain dump ritual for sleep** — 30 min before bed, physical notebook, dump everything; started 2026-05-10 | Track: sleep quality over 4 weeks | Related quests: [[Sleep-Optimization-Routine]], [[Energy-Management]] | Source: [[coaching_session_20260509]]
- **Exercise → next-day energy tracking** — 4-week data collection; 1-5 scale for intensity and next-day energy | Question: sleep, nutrition, intensity, or recovery gap? | Related quests: [[Fitness-Routine]], [[Energy-Management]] | Source: [[coaching_session_20260509]]
- (new) **Energy Budgeting Framework** — Design a lightweight system for tagging calendar items by energy load (high/low) and planning days around energy availability, not just time. Particularly useful for multi-class dance days + heavy work weeks. **Trigger: late August / early September 2026** — assess after new routine settles; only formalize if needed. (ref: [[coaching_discussion_20260530]], [[coaching_session_20260305]])
- (new) **Fitbod CSV → Training Log integration (monthly)** — At each monthly body scan + review session: export Fitbod CSV, run script to extract PRs and recent session data for TBDL/Bench/Lat columns, integrate into monthly review. Trigger: next monthly review session. (ref: 2026-06-16 AI system design session)
- (new) **Iyengar Yoga Institute Amsterdam — weekend workshop prototype** — Deferred to Q4。Book an anatomy/alignment-focused weekend workshop as low-cost test of Plan 2. (ref: [[Life_Design_Coaching_Transcript]])
- (new) **Studio Anna Mora — 1-on-1 Gyrotonic equipment session** — Deferred to Q4。Single private session to test body intelligence resonance. (ref: [[Life_Design_Coaching_Transcript]])
- (new) **Fighting Monkey / Celeste Pereira deep-dive** — Deferred to Q4。Study operating model of these educators. (ref: [[Life_Design_Coaching_Transcript]])

### Mind & Mental Health

### Finance

### Creativity & Curiosity

- **Content creation exploration** — Writing + speaking; leverage strategy + emotion + expertise combination | If chosen: 4-week sprint | Related quests: [[Content-Creator-and-Entrepreneurship-Ideas]], [[Public-Knowledge-Sharing]] | Source: [[coaching_session_20260509_retrospective]]
- **Coaching (identity work) exploration** — Somatic intelligence + emotional depth + authenticity journey = unique positioning | If chosen: research certification paths | Related quests: [[Identity-Based-Life-Philosophy]] | Source: [[coaching_session_20260509_retrospective]]
- **Selective reading experiment** — Read only what feels alive; stop forcing "productive" reading | Related quests: [[Information-Overload]] | Source: [[coaching_session_20260509]]
- **AI & automation ideas (longer horizon):** Show scraping tool (by city/venue), meal prep assistant, auto grocery planning with discount/macro optimization, airport/VPN alternative (ref: [[coaching_session_20260509_retrospective]], [[coaching_discussion_20260530]])
- **Food experiments backlog:** Saffron cake experiments, baking 抹茶红豆雪芳蛋糕 (ref: [[coaching_discussion_20260530]])
- **Learning queue (new 2026-05-28):** (1) Git/GitHub fundamentals — practical for KMS/AI work; (2) Philosophy survey — classical Western + world philosophy, primary works; (3) Logic & reasoning (philosophical) — argumentation, epistemic discipline. All three are "when bored and want to grow" tier. See [[Learning-Curiosity-Queue]] (from: [[2026-05-28]])
- (new) **Personal Museum & Cultural Capture System** — A lightweight system for capturing and cataloguing cultural experiences (museum visits, theatre, concerts, film) with personal annotation. Connects to aesthetic intelligence work. (ref: [[coaching_discussion_20260530]], [[coaching_session_20260516]])

### Relationships

- **Parent elderly care + distance strategy** — Separate project stream to think through long-term solution to distance/elderly care with parents and communication strategy. Now partly addressed in [[Parents_Relationship]] project. | Related: [[Coming-Out-and-Family-Authenticity]], [[Location-Independent-Lifestyle]]
- (new) **Relationship Hardware Checklist** — A structured checklist of non-negotiable hardware requirements for a long-term partner (physical, cultural, life-vision), distilled from existing relationship audit work. Related to three-category needs taxonomy (taxonomy = what you need; checklist = partner requirements). **Trigger: end of August 2026** — deferred alongside all relationship prep work. Add to [[Strategic_Relationship_Audit]] when ready. (ref: [[coaching_discussion_20260530]], [[coaching_session_20260305]])

### Travel

### Admin & Home

- **Plants audit project** — 已合并入 [[Plant_rearrangement]]（[[Studio_Makeover]] sub-project）。8 月内完成 repotting + root check。

### Life Management / KMS

- (new) **Naval's Almanack prompt as KMS skill** — Convert Naval Ravikant's core decision-making and wealth-building prompts into a reusable KMS/Claude skill. Add to [[Life_Management_System]] backlog or skill development queue. **Trigger: July 2026** — low priority, do when there's a quiet slot. (ref: [[coaching_discussion_20260530]])
- (new) **Vibe Coding Cloud Executor** — 在云端（GitHub Codespaces 或 Hetzner $5/月 VPS）运行 Claude Code，实现纯移动端闭环：手机 Plan + 云端执行 + 自动 commit。优势：到 GitHub/OpenRouter 延迟低、不挂墙、24 小时在线、不需要本地 GPU。[[vibe_coding_tool]] 的 backlog idea。**Trigger: 有空时探索**

---

## Done (Archive)

| Project | Pillar | Status | Notes |
|---------|--------|--------|-------|
| H1 Performance Review | Career | Completed | Self-evaluation submitted (3.92). |
| Flight_Upsell | Career | Archived | Project closed 2026-08. Portfolio/Analysis/Learnings preserved in `04_project/Flight_Upsell/` as reference. |

---

**Maintenance:** Update after each priority or project coaching session. Run `/project-review` monthly to re-order priorities.
