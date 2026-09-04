---
name: _idea_backlog
description: Idea backlog — grouped by trigger condition, not by pillar
updated: 2026-09-04
---

# Idea Backlog

从 `_priority.md` 移出（2026-09-04）。原来按 pillar 分组，但 pillar 是**浏览用的结构，不是决策用的结构** —— 三个 pillar 是空的，而真正有用的信息是「什么时候该看它」。所以改按**触发条件**分三组。Pillar 作为每条的 tag 保留。

**不进 AI payload** —— `sync-context.py` 只同步 `_POS.md` 与 `_priority.md`。这是刻意的：这些条目大多在等条件，每次 priming 都读一遍是噪音。

**Review 节奏：** 月度只看第一组「已触发」。第二组等条件到了自己会浮出来。第三组有空才翻。

---

## 1. 已触发，待处理

*触发日已过，需要一个动作：激活、defer 到新日期、或删掉。*

- **Alternative career architecture session** `Career`
  长期职业设计的专门探索 —— 把 location-independence、Movement Lab、content creation、AI assistants 几条平行线连成一个整体设计。结合 [[Design_your_life]] exercise。
  原 trigger: 2026 年 8 月底（summer intensive + travel 之后）→ **已过期**。
  建议：defer 到 Q4。9 月下旬那个窗口已经排了三件（父母 Phase 1 / 超体重启 / plants）。
  ref: [[coaching_discussion_20260530]]

- **Energy Budgeting Framework** `PhysicalHealth` `LifeManagement`
  给 calendar 条目打 energy load 标签（high/low），按精力可用性而非只按时间排日程。对多节舞蹈日 + 重工作周尤其有用。
  原 trigger: 2026 年 8 月底 / 9 月初（新 routine 稳定后评估，只在需要时才正式化）→ **已过期**。
  建议：defer 到 Q4。而且 app 的 quota 系统（weight + cap 5）已经部分承担了这件事，正式化前先看 quota 够不够用。
  ref: [[coaching_discussion_20260530]], [[coaching_session_20260305]]

- **Naval's Almanack prompt as KMS skill** `LifeManagement`
  把 Naval 的决策与财富 prompt 转成可复用的 KMS/Claude skill。
  原 trigger: 2026 年 7 月 → **过期两个月**。
  建议：移到第三组（有空就做）—— 它本来就标着 low priority，挂着一个过期日期没有意义。
  ref: [[coaching_discussion_20260530]]

---

## 2. 等条件

*有明确的前置条件，条件不到不用看。*

### 等 location-independence 问题清楚

这条是 master filter，gate 住下面两个 —— 也 gate 住 family timeline 和财务。
Action: 和 manager 的探索性对话（不是谈判）。
ref: [[coaching_session_20260509]] · quests: [[Portfolio-Career-Design]], [[Location-Independent-Lifestyle]]

- **Portfolio Career Strategy** `Career` — 澄清 70% corporate + 30% teaching 的结构。附带：画出典型一周长什么样。
- **Movement Lab / Teaching venture** `Career` `CreativityCuriosity` — 最有生命力的创业选项，喂养创作热情 + 身体专长。需要 4 周 research sprint。ref: [[coaching_session_20260509_retrospective]]

### 等 Q4（movement certification 方向的低成本试探）

三条是同一件事的三个入口 —— 都在试 Plan 2（movement certification 而非 Master's）。
ref: [[Life_Design_Coaching_Transcript]] · quests: [[Movement-Career-Options]]

- **Iyengar Yoga Institute Amsterdam — 周末 workshop** `PhysicalHealth` — 解剖/对位向的 workshop，低成本测试。**与 [[Training]] 2026-09 的 Iyengar 升频同向**（CT insight 之后 alignment 变得更有用），所以这条现在比原来更值得做。
- **Studio Anna Mora — 1-on-1 Gyrotonic** `PhysicalHealth` — 单次私课，测身体智能的共鸣。
- **Fighting Monkey / Celeste Pereira deep-dive** `PhysicalHealth` — 研究这两位教育者的运作模式。

### 等 KMS MVP

- **Xiaohongshu Content Series** `CreativityCuriosity` — 分享 KMS journey + movement/body tips，杠杆点是策略 + 情感 + 跨文化视角。quests: [[Content-Creator-and-Entrepreneurship-Ideas]], [[Public-Knowledge-Sharing]]

### 等 alternative career session（第一组那条）之后

- **Content creation exploration** `CreativityCuriosity` — 写作 + 演讲。若选中：4 周 sprint。
- **Coaching（identity work）exploration** `CreativityCuriosity` `MindMentalHealth` — somatic intelligence + 情感深度 + authenticity journey 是独特定位。若选中：研究认证路径。
  ref: [[coaching_session_20260509_retrospective]] · quests: [[Identity-Based-Life-Philosophy]]

---

## 3. 有空就做

*没有条件也没有 deadline。无聊且想成长的时候翻这里。*

- **Naval's Almanack prompt as KMS skill** `LifeManagement` — 见第一组，已从「过期」降级到这里
- **Vibe Coding Cloud Executor** `CreativityCuriosity` — 云端跑 Claude Code（GitHub Codespaces 或 Hetzner $5/月 VPS），纯移动端闭环：手机 Plan + 云端执行 + 自动 commit。优势：延迟低、不挂墙、24h 在线、不需要本地 GPU。[[vibe_coding_tool]] 的 backlog idea
- **Learning queue**（2026-05-28）`CreativityCuriosity` — (1) Git/GitHub fundamentals（对 KMS/AI 工作实用）；(2) 哲学通览（西方古典 + 世界哲学，读原著）；(3) 逻辑与论证。三条都是「无聊且想成长」层。见 [[Learning-Curiosity-Queue]]
- **Personal Museum & Cultural Capture System** `CreativityCuriosity` — 轻量系统，记录并编目文化体验（博物馆、剧场、音乐会、电影）+ 个人批注。连到 aesthetic intelligence。ref: [[coaching_discussion_20260530]], [[coaching_session_20260516]]
- **Selective reading experiment** `CreativityCuriosity` — 只读活的东西，停止强迫式「有用阅读」。quests: [[Information-Overload]]
- **AI & automation ideas**（长线）`CreativityCuriosity` — show scraping tool（按城市/场馆）、meal prep assistant、自动买菜（折扣 + 宏量优化）、机场/VPN 替代方案
- **Food experiments** `CreativityCuriosity` — 藏红花蛋糕、抹茶红豆雪芳蛋糕
- **Fitbod CSV → Training Log integration（月度）** `PhysicalHealth` — 每月体测 + review 时导出 Fitbod CSV，跑脚本提取 PR 和近期 session 数据（TBDL/Bench/Lat），整合进月度 review。ref: 2026-06-16 AI system design session

---

## 已解决 / 已删除（2026-09-04 清理）

- ~~**Plants audit project**~~ → 已并入 [[Plant_rearrangement]]，文件在 `04_project/Studio_makeover/Plant_rearrangement/`。Phase 1 换盆完成，Phase 2 待做。原条目只是「指向一个指针」。
- ~~**Relationship Hardware Checklist**~~ → 已进 Weekend Allocation 队列，deadline 12 月对话前。原条目是重复记账。见 [[Strategic_relationship_audit]] December Conversation Framework。
- ~~**Brain dump ritual for sleep**~~ → **从未执行**（用户 2026-09-04 确认）。睡眠分析改为以数据为准（`daily_metrics` + Google Calendar 训练历史），不再依赖自报实验。结论见 [[Training]] Decisions 2026-09-04：真正的变量是就寝时间，不是训练量。
- ~~**Exercise → next-day energy tracking**~~ → 那个问题现在有 Fitbod + body scan + `daily_metrics` 数据能直接回答，不需要单独做四周实验。
- ~~**Parent elderly care + distance strategy**~~ → 大部分已由 [[Parents_relationship]] 项目承载，不再单独挂。剩余的长线部分（养老 + 距离）留在该项目 Phase 3。

---

**Maintenance:** 月度 review 只看第一组。新想法进第二或第三组（带触发条件），不要默认放第一组。
