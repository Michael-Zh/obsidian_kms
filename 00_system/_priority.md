---
name: _priority
description: Single source of truth — 现在做什么、有哪些项目在推进、为什么是这些
updated: 2026-09-04
---
打开这个文档，从上到下依次回答：现在应该关注什么？→ 有哪些项目在推进？→ 为什么是这些？

**Last Updated:** 2026-09-04
**Links:** `/project-review` 月度重排 | `/project-context [name]` 开始专注 session | `/Project-Initiation` 把 backlog idea 正式化

> **2026-09-04 精简：** 本文件只留「现在」。搬出去的三部分都不进 AI payload
> （`sync-context.py` 只同步 `_POS.md` 与本文件）：
> `Weekend_Allocation.md`（方法）· `Cross_Pillar_Synergies.md` · `_idea_backlog.md`（想法，按触发条件分组）
> 已删 `Short-Term Focus` —— 它是 Bottom Lines + Cadence 的派生视图，是唯一剩下的重复。

---

## Annual Bottom Lines (2026 — 三条并行底线)

*底线 = AND 逻辑：三条都完成，2026 才算达标。不排序、不互相牺牲。*

| 底线 | 内容 | 年度判据 |
|------|------|----------|
| **Foundation 地基** | App dev + Physical（训练 / Meal prep）+ Home | 身体能自动跑（sleep ≥80%、meal prep 3-5 可重复菜、训练有 AI 反馈闭环）；Home 年底前完成 Phase 2 |
| **Leverage 杠杆** | AI learning + 财务 | 超体 Ch5→Ch18 完成并启动变现路径；财务全自动 + Q4 税务落定 |
| **Relationship 关系** | 父母 + 男友 | October gate 出明确结果（cohabitation/ENM/kids 不再 suspended）；父母 Phase 1 启动 |

---

---

## Execution Cadence (now → Sept 2026)

*执行 = WHEN 逻辑：同一时刻主推 1-2 件，其余到点再动或自动跑。*

| 状态 | 事项 | 时间 | 说明 |
|------|------|------|------|
| 🔥 主战场 | Physical（workout plan 改造） | 9 月 | 两个 dance intensive 后的 inspiration momentum，趁热改；概念层落点见 [[Training]] Decisions |
| 🔥 主战场 | Home（excessive 物品清理 + Plants） | 9 月中旬后 | 基础 clean-up + cleaner ✅ 已完成；剩余部分需要周末大块时间，按 Weekend Allocation 排 |
| 🟡 待重启 | Meal prep | 9 月下旬 | 停滞中。归类从「家务/采购」改为「训练输入」——它是 workout plan 改造的另一半 |
| 🟡 待重启 | AI learning | 9 月下旬 | 超体 Ch5→Ch18，一周两章；晚间 activity 密集期结束后重启 |
| 🟡 持续底色 | App dev | 全年 | **2026-09-03 解除暂停** — 重启条件 ② 成立（需要外置决策器管周末大块时间）。Session 53 已做 Weekend Allocation。仍不做无需求的 feature |
| ⏳ on-deck | Relationship（父母 + 男友） | 父母 9 月下旬 · gate → 12 月 | Jeroen 11/12 搬入自购公寓；10–11 月为思考窗口 |
| 🛟 自动驾驶 | Finance | Q4 | net worth 月度 review + Q4 避税 |

**App dev 暂停 → 解除（2026-09-03）：** 原三个重启条件是 ① meal prep 需要认真做 priming；② 个人 priority 管不过来、需要外置决策器；③ 超体学完后有新整体判断。**② 已成立** —— 周末大块时间的分配正是「先做哪个」决策器要解决的事，且手工维护会变成第二个真相源。Session 53 做了 Weekend Allocation。原则不变：只做有真实需求的 feature，① 和 ③ 仍未到。

**🚫 Parked（不在执行节奏内）：** Training_Program 概念层（图纸不改，但本轮 workout plan 改造的决策要落在这里）· Design_your_life（Q4）· 其余 Q4 deferred ideas

---

---

## Weekend Allocation

*方法见 `00_system/Weekend_Allocation.md`。这里只放活的部分。*

> **⚠️ 边界（2026-09-03 定，勿删）：** backlog（app DB `priming_backlog`）是「要做什么」的**唯一真相源**；项目文件的 `## Strategic Direction` 是**策略叙述**，只作 AI prompt 上下文（帮 priming 挑 top3），**不判定任务是否完成**。
> 往 Strategic Direction 写东西**不会**创建 task，从里面删东西**不会**完成 task。要动 task 就去 backlog。
> 起因：app 的 re-sync cascade 曾把不在 Strategic Direction 里的 backlog 项静默标 done（已修，app Session 54 / commit 6dfb4d3）。
> 下方队列是**给人看的策略视图**，实际排序在 app 里跑，两边任务名一致即可对上。

### 待排队列（按 deadline，不按周末）

*每次有 🟢 就从顶部取一件。这样周末状态变化不需要重排整张表。*

1. **Plants Phase 2+3** — 换盆 / 修剪 / 光照分区 · 需半天 · deadline 9 月底 · **前提：supply 已在工作日买齐**
2. **Meal prep 启动** — 容器采购 + 第一次周日 batch · 需半天 · deadline 10 月中
3. **Excessive 物品清理** — 可切块，两小时起 · 无硬 deadline · 适合塞进 ⚠️ 周末
4. **Hardware Checklist**（[[Strategic_Relationship_Audit]]）— 需要安静的整块思考时间 · deadline 12 月对话前

**不占周末（工作日晚间即可）：** 介壳虫**隔离**（2 分钟，本周内——隔离和处理是两件事）· 植物诊断 + supply 清单（10 分钟）· 超体一周两章 · 父母第一次通话（一个安静的晚上）

### 当前分配

*不在本文档维护 —— 打开 App 面板看实时状态（它读 calendar + backlog）。*

9 月的预期形状（按你 2026-09-03 给的信息，待 app 首次跑确认）：9/5–6 和 9/12–13 已满；9/19–20 是第一个可用周末，归 Plants；9/26–27 留作缓冲；10/3–4 归 Meal prep 启动。

---

## Quick Decisions Queue

_<2min 拍板项。batch process：有空时一次性过，resolve 后写回对应项目行并移除本条。_

1. ~~**Net worth 更新频率**~~ → ✅ 已定：月度。已写回 [[Road_to_2040_Investment_Blueprint]]，本条关闭（2026-09-03）
2. ~~**Cleaner prep 范围**~~ → ✅ 已完成：cleaner 已请、已清。本条关闭（2026-09-03）
3. **Q4 避税主题** → 待定：Q4 review 聚焦哪个税项？（capital gains realization / 账户结构 / deductions）
4. **Late-Aug 触发项** → 部分澄清（2026-09-03）：Hardware Checklist 挂到 12 月 gate 前完成（不再是「现在 or defer」，有了具体 deadline）；Alternative career session 和 Energy Budgeting 仍待定 — 9 月下旬那个窗口已经排了三件事，这两条建议 defer 到 Q4
5. **Frontmatter `priority` 字段迁移（元决策 B）** → 部分完成（2026-09-03）：Active Projects 表的 Priority 列已换成火候（execution_state）。frontmatter 的 `priority: P1/P2/P3` **暂不动** — App 的 `/api/context/status` alignment check 仍读它做对比，改之前要先改 app 侧三条 route。App dev 已暂停，所以此条随之 defer

---

---

## Active Projects

*火候 = `execution_state` frontmatter 字段（main / on_deck / ongoing / autopilot / parked），与上方 Execution Cadence 对齐。P1/P2/P3 已从本表移除——frontmatter 里暂时保留，因为 App 的 context alignment check 仍读它（见 Quick Decisions Queue #5）。*

| Project | ID | Pillar | 火候 | Current Focus | Updated |
|---------|-----|--------|------|---------------|---------|
| [[Life_Management_System]] | pj0001 | LifeManagement | ongoing | Meta-system hub — 5-module architecture map: KMS, Coaching, Training, Project Coaching, Daily Ops | 2026-08-10 |
| [[Danseur_Noble_Hub]] | pj0007 | LifeManagement | ongoing | 暂停已解除（重启条件 ② 成立）。Session 53：Weekend Allocation — 读 calendar 判可用性 + 写 LMS:/PJ: placeholder 进主 calendar。**Migration 054 待手动跑** | 2026-09-03 |
| [[AI_learning]] | pj0012 | LifeManagement | on_deck | 停滞中 — 超体 Ch5 未开始，9 月下旬重启（一周两章）→ IP 变现 → Anthropic Academy → CS50 | 2026-09-03 |
| [[Parents_Relationship]] | pj0003 | Relationships | on_deck | Phase 1 推至 9 月下旬 — CT intensive 安全层分享，建立真实沟通语境 | 2026-09-03 |
| [[Studio_Makeover]] | pj0005 | AdminHome | main | 基础 clean-up + cleaner ✅ 完成；下一步 excessive 物品清理，需周末大块时间 | 2026-09-03 |
| [[Road_to_2040_Investment_Blueprint]] | pj0010 | Finance | autopilot | Surrogacy 基金口径锁定；GOOGL 第一批完成（ABEA EUR €1,493），跟踪第二批；net worth €142,247（2026-09-01，月度）；Q4 tax review | 2026-09-01 |
| [[Strategic_Relationship_Audit]] | pj0011 | Relationships | on_deck | Gate 后移至 12 月（Jeroen 11/12 搬入自购公寓）；10–11 月思考窗口；6 条 backlog 待激活 | 2026-09-03 |
| [[Meal_prep_routine]] | pj0004 | PhysicalHealth | on_deck | 停滞中，9 月下旬重启。重新归类为训练输入而非家务 | 2026-09-03 |
| [[Plant_rearrangement]] | pj0014 | AdminHome | main | Sub-project of [[Studio_Makeover]]（2026-09-03 移入其文件夹）。Phase 2 待做（介壳虫检查 + Alocasia 抢救）；换盆/分区需 9/19–20 周末半天 | 2026-09-03 |
| [[Training_Program]] | pj0006 | PhysicalHealth | parked | 图纸不改，但本轮 workout plan 改造（两个 intensive 后）的决策要落在这里 | 2026-09-03 |
| [[Design_your_life]] | pj0013 | MindMentalHealth | parked | 找系统性 prompt 重走 DYL exercise；Q4 奥德赛计划 review | 2026-08-10 |

---

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

---

## Completed / Archive

| Project | Pillar | Status | Notes |
|---------|--------|--------|-------|
| Skincare_Routine | AdminHome | ✅ Complete | Routine established (home + travel) |
| H1 Performance Review | Career | ✅ Closed | Self-evaluation submitted (3.92) |
| Flight_Upsell | Career | 📦 Archived | Closed 2026-08. Portfolio/Analysis/Learnings 保留在 `04_project/Flight_Upsell/` 作 reference |

---

**Maintenance:** 每次 priority 或 project coaching session 后更新。月度跑 `/project-review` 重排。
想法进 `_idea_backlog.md`，不要堆回本文件。
