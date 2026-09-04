---
name: Danseur_Noble_Hub
project_id: pj0007
status: active
pillar: LifeManagement
parent_system: Life_Management_System
current_focus: "Weekend Allocation 上线（Session 53）— 读 calendar 判周末可用性 + 写 LMS:/PJ: placeholder。Migration 054 待手动跑"
updated: 2026-09-03
priority: P1
execution_state: ongoing
---

# Danseur Noble Hub — App Vision

Danseur Noble Hub is the **execution layer of Michael's Life Management System (LMS)** — a PWA that integrates morning priming, cross-domain backlog management, AI coaching across multiple life scopes, training execution, and Google Calendar scheduling into a single daily operating interface.

The name "Danseur Noble" reflects its origin as a dancer's training companion. It has since evolved into a full Life Management OS — the name stays as a nod to where it started.

**Live:** https://danseur-noble-hub.vercel.app
**Code:** `~/Documents/Apps/danseur-noble-hub`
**Stack:** Next.js 14, Supabase PostgreSQL + RLS, OpenRouter → DeepSeek V3 / Gemini Flash, Vercel, Google Calendar API

---

## Architecture

### Three-Layer System

```
KMS Obsidian Vault（策略层） → Supabase PostgreSQL（数据层） → PWA 前端（执行层）
```

- **KMS Obsidian** — knowledge synthesis, wiki, project docs, POS, coaching notes, personal preferences
- **Supabase** — training records, schedules, body metrics, backlog items, coaching conversations
- **App** — the daily operating interface where all data converges and AI provides real-time guidance

### Four Tabs

1. **Priming** — morning brief + Top 3 tasks + cross-domain backlog management
2. **Today** — daily training execution, gym logger, body state tracking
3. **Coaching** — AI coaching across three scopes (Training / General / Priority)
4. **Dashboard** — body composition trends, gym PRs, sleep/HRV metrics

### Integrated Sub-Systems

| Sub-system | How it connects |
|------------|----------------|
| KMS Knowledge Management | Vault → Supabase via GitHub Action sync-context |
| Overall Life Coaching | Coaching tab General + Priority scopes |
| Training Program | Coaching tab Training scope + Today tab execution |
| Project Coaching | Priming tab reads projects_state for Top 3 |
| Daily Operations | Priming + Backlog + Google Calendar scheduling |

---

## Relationship to LMS

Danseur Noble Hub is **Module 3 & 5** (Training Program + Daily Operations) of the LMS architecture, and serves as the execution interface for **Module 2** (Overall Life Coaching).

The full LMS architecture is documented at `04_project/Life_Management_System/LMS.md`.

---

## Key Design Decisions

- **PWA, not native iOS** — iOS 17+ Web Push covers notification needs; avoids Xcode + App Store overhead
- **DeepSeek V3 for coaching** — strong Chinese-English bilingual performance for training/body sensation conversations
- **Rules in DB, not code** — training rules evolve with user state without requiring code deployment
- **Two-layer sync** — KMS (strategy) → App (execution) via GitHub Action; coaching decisions flow back via manual Push to Obsidian

---
## Strategic Direction

- **暂停 → 解除（2026-09-03）**：8 月底因「日常只用 scheduling、未 active 使用」而暂停，定了三个重启条件。**② 已成立** —— 周末大块时间的分配需要外置决策器，且手工维护会变成第二个真相源。Session 53 做了 Weekend Allocation。① meal prep priming 和 ③ 超体后的整体判断仍未到，所以原则不变：只做有真实需求的 feature。
- **核心 KPI（2026-08-15 重定位）**：App dev 的度量 = 把排好的 priority 结构「长」进 app，做外置的「先做哪个」决策器，使 daily 决策不用脑子记/纠结。**Weekend Allocation 是这条 KPI 的第一个真正落地**：它把「哪个周末归哪件事」从 KMS 手工表变成了 app 读 calendar + backlog 自动给建议。
- **Weekend Allocation（Session 53，已上线待验证）**：可用性判定在 `src/lib/weekend-availability.ts`（location calendar 空 = 在阿姆斯特丹可安排；有值 = 外出）；placeholder 以 `LMS:` / `PJ:` 标记写入主 calendar，默认周六 14:00–18:00；`weekend_allocations` 表（Migration 054）记录对应关系。**Migration 054 需手动在 Supabase 跑**，真实 calendar 读写需部署后验证。
- **SchedulePanel 手机可用性修复（Session 58，2026-09-04）**
  - **Dropped session 在手机上拖不动。** Session 51 记的「dropped 可拖拽」只挂了 HTML5 drag（`draggable` + `onDragStart`），而**那套事件在 iOS 上根本不触发**。session 卡片能拖是因为另挂了 `onTouchStart`。所以桌面能用、手机不能 —— 而这是个 iOS PWA，等于该功能对主场景从未生效。已补 touch 路径 + `touch-none`。
  - ⚠️ **教训（写进 app CLAUDE.md）：本 app 是 iOS PWA，任何拖放都必须同时实现 touch 路径。** 只有 HTML5 drag 的功能等于不存在。
  - **Generate 之后回不去改参数。** 问卷只在 `!hasPlan` 时渲染，所以「HJS 哪天上」这类结构参数一旦生成就在窗口内锁死，只能 Approve 或 Adjust（而 Adjust 是 AI 路径、不改 shape）。已加 Params 按钮：重开问卷 → 改参数 → Regenerate 替换当前计划。
- **Rotating slots — generate 开始读 DB guidelines（Session 57，2026-09-04）**
  - 此前 `generate` 完全不读 `scheduling_guidelines`（只有 `adjust` 读），周结构硬编码在 `slotRequestsForShape()`。所以 DB 里定的排期规则永远到不了生成的一周。
  - `src/lib/rotating-slots.ts` 读 `parameters.shared_slot === true` 的 guideline，按 ISO 周 parity 对锚点解析。确定性实现（generate 不走 AI）。
  - **扩展方式：插 guideline，不改代码。** 参数 shape：`{shared_slot: true, day_of_week, anchor: {date, iso_week, kind}, options: {sideA: [{title, start, preferred}], sideB: [...]}}`。
  - 首个用例：周二 Contemporary ⇄ Exploration（见 [[Training]] Decisions 第七批）。
  - 降级：guideline 缺失或格式不对 → 返回空，硬编码 shape 原样工作（6 条断言覆盖）。
  - 这是「把 priority 结构长进 app」KPI 的第二个落地（第一个是 Weekend Allocation）。
- **Meal plan integration — 重启条件 ① 的具体形态（2026-09-04 定 spec，未实现）**
  - 用户原话：「之后有了 meal plan integration 之后，我就不用自己用脑子去想这个了。执行过几次之后就会条件反射。」
  - 要做的事：priming 输出当天的**日型 + 吃法**，取代人脑判断。
  - **日型完全可从已有数据推导，不需要新输入** —— 当天课表已在 `class_pool` + `workouts` 里：
    - 当天 quota 权重合计 ≥ 2，或「早课 + gym」，或一天两练 → **大运动量日**（不设进食窗口，开始前先补碳水）
    - 恰好一节 performance / anchor → **常规日**（12:00–22:00）
    - 0 节，或只有 alignment（Iyengar / Yin / Reformer）→ **轻日**（14:00–22:00）
  - 恒定项（与日型无关）：每天 175g 蛋白质；任何 20:00 后结束的课，回去补一份蛋白（不算破窗）。
  - 输出形态举例：「今天是大运动量日 —— 早餐前补碳水，蛋白质目标 175g，20:30 下课后补一份。」
  - **先手动跑几次再自动化。** 用户预期跑几次就会条件反射，而且跑过才知道日型判据要不要调。判据来源见 [[Meal_prep_routine]] 与 [[Training]] Decisions 2026-09-04。
- Priorities Panel 精简 — 直读 `_priority.md` Short-Term Focus section，不再 AI 压缩
  - ⚠️ 该 section 自 2026-09-03 起改为**派生视图**（真相源 = Annual Bottom Lines + Execution Cadence）。格式契约仍是 `N. **项目名**`，三条 route 依赖：`/api/coaching/priorities`、`/api/context/status`、`/api/priming`。改 `_priority.md` 结构前先确认这三条。
- Web Push Notifications — iOS 17+ 训练提醒（Service Worker + VAPID keys）
- Exercise Library v3 — YouTube links + AI substitution ranking
- `context_snapshots` 实际消费 — 从直接调 GitHub API 迁移到 Supabase 表读取
- Coaching decisions 回流 Obsidian — `sync-decisions` 脚本实现闭环

---
## Decisions

- **2026-08-09:** LMS 重构 — App 文档从 LMS 独立到 `Danseur_Noble_Hub/`，明确执行层定位
- **2026-07-24:** Two-Layer Architecture 明确化（KMS 策略层 + App DB 执行层），Backlog Sync + Stale Review 闭环
- **2026-07-21:** Backlog 重构 — 从 project 层面重新生成，Strategic Direction 替代 Next Steps
- **2026-07-09:** Gym Logger 完整重写（warmup sets, inline edit, rest timer, deload + training mode 叠加）

- **2026-08-22 (Session 51):** Schedule AI 改进 — classifyConflict (office/show/social/tbc→hard)注入 adjust prompt；applicable_titles (Migration 053) 防约束误套；generate class_pool lookup 修复；SchedulePanel 提取为单一 src/components/SchedulePanel.tsx；Coaching chat history 重构（无 welcome bubble，Clear Chat 存时间戳，history 按 cutoff 显示）；Schedule panel 移入对话流