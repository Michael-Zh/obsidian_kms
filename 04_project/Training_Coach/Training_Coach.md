---
project_id: pj0007
---

# Training Coach — Danseur Noble S&C Hub

**GitHub:** https://github.com/Michael-Zh/danseur-noble-hub  
**Live:** https://danseur-noble-hub.vercel.app  
**本地代码：** `~/Documents/Apps/training-coach`  
**Stack:** Next.js 14, Supabase PostgreSQL, OpenRouter → DeepSeek V3, Vercel, Google Calendar API

---

## Vision

Elite body recomposition PWA for a 36-year-old male dancer.  
目标：86-87kg | 43kg+ SMM | <10% BF | 维持 elite dance 耐力。  
核心设计：AI coaching（DeepSeek V3）+ AutoSleep 数据 + gym logging + 动态规则系统，跨 4 个 functional pool 优化训练负荷。

---

## 已上线功能

- **Priming tab** — `projects_state` Supabase 直读；brief + top3 + backlog；9-pillar 颜色；Backlog 内联编辑；AppIdeas FAB；briefOnly Regenerate；Today's Focus + Calendar 训练事件混排；Calendar 冲突检查；BacklogRow done toggle；Priming 去重
- **Today tab** — 两阶段加载；AM/PM Pulse；readiness banner + Apply；Gym Logger（warmup sets、inline edit、rest timer）；date navigation；WorkoutStatus 三值
- **Coaching tab** — 3-scope（Training / General / Priority）；AI chat + rule proposals；Time-Limited Rules；End Session（只汇总新消息，summary inline 插入）；`coaching_messages` 按 scope 持久化；scope 切换时 `projects_state` active projects 自动注入 General/Priority context；End Session 后 Push to Obsidian 按钮
- **Metrics tab** — 体成分趋势图、gym PRs；Sleep/HRV/RHR 双 Y 轴图表
- **Exercise Library** — 30+ exercises；Exercise Bank UI
- **Infrastructure** — Calendar reconcile cron；sync-context GitHub Action（`context_snapshots` + `projects_state`）；Dev/Prod split；Supabase RLS
- **Context 系统（Session 26 大改造）：**
  - `coaching_sessions` carry-forward：每次 AI 对话自动注入最近 3 条同 scope 的 session 摘要
  - `training_context` append-only 历史追溯（Migration 040）：`superseded_by` + `change_reason`，年度回顾可查目标演变
  - `context_snapshots` 切换：generate-log、priming、coaching/priorities 全切为读 Supabase 镜像，移除 GitHub API 依赖
  - DB → Obsidian snapshot：`POST /api/training-context/sync-snapshot` 每次 training_context 更新后自动触发，写入 `training_context_snapshot.md`
  - Training Chat 加载 `scheduling_constraints`（之前只有 guidelines）
  - `training-coach-context` CC skill 加 `training_context` 查询 + 历史追溯字段

---

## Open Backlog

| 优先级 | Item |
|--------|------|
| P1 | Manual Context Sync Reset Dashboard（人工审查所有 context source 同步状态）|
| P2 | `coaching_sessions` 自动回流 Obsidian（目前 Push to Obsidian 按钮手动）|
| P2 | General coaching tab 启动时调 `/api/projects/pending` 批量 reconcile |
| P2 | `google-calendar.ts` + `coaching/insights` 的 `key`/`value` schema mismatch 修复 |
| P2 | Class Pool DB 化 + 管理 UI |
| P2 | Schedule Coaching Integration（schedule_suggestion proposal card）|
| P2 | Backlog `project_id` UI 入口（BacklogRow 编辑模式加 project 下拉）|
| P3 | Pulse 简化（去掉 AM/PM） |
| P3 | Priorities panel 显示优化（Short-Term Focus 摘要） |
| P3 | Schedule Panel 手动内联编辑 |
| P3 | Web Push Notifications |
| P3 | Exercise Library v3 — AI Substitution + YouTube links |
| P3 | Project-specific coaching / docs（低优先级）|
| Later | KMS + App 统一 Context Audit |
| Defer | Timezone Review |

---

_代码已移出 vault。此文件每次开发会话结束后同步更新。_

---

_2026-07-19 更新（Session 27）_

**新增 / 变更：**
- Coaching tab 新增 **Weekends scope** — Weekend Planner：读取 AMS/DH calendar 现有状态，toggle 每个周末的 location，Wand2 auto-fill（从锚点交替填充后续周末），AI 批量日程文本解析，Apply 写回 Google Calendar
- Priming backlog 按钮优化：minus→数字→plus；header pill 纯数字（0=白/橙/>0，激活=黑）
- Metrics：Body Scan Last scan 日期移至标题栏（M/D 格式）
- WorkoutJournal 跨设备 display bug 修复；Edit → Pencil icon

**Backlog 更新：**
- Location Calendar Weekend Planner ✅ Done（已移出 backlog）
- UI 三条 AppIdeas 小调整 ✅ Done


---

_2026-07-20 更新（Session 29）_

**新增 / 变更：**
- **Context Sync Dashboard**：跨端口 context 诊断 + 修复中心（Re-sync / Re-push / View delta / Mark reviewed / Priority Alignment）；Re-sync 只取 valid project 子目录
- **Priority Sync 闭环**：End Session 自动检测 P1/P2/P3 decisions → 写回 `_priority.md` Short-Term Focus + `projects_state.priority`
- **Class Pool DB 化**（Migration 042）：`class_pool` 表替换硬编码；`ClassPoolManager` 管理 UI（match_title 分组，共性字段自动批量 PATCH，slot 增删改）
- **Backlog `project_id` UI 入口**：`GET /api/projects` → BacklogRow 编辑模式 project 下拉
- **Schedule Panel 内联编辑**：MiniSessionCard 点击 → 内联编辑 title/时间/地点
- **Dashboard 重构**：Metrics tab → Dashboard tab；charts 归可折叠 Metrics 区域；三管理按钮横向排列；Gym PR 三条线合并单图；30 天固定窗口；Backlog 按钮改文字 pill
- **Bug 修复**：Priming regenerate done 行污染、Gym PR 7 月数据（FK expansion + ilike 关键词匹配）、Coaching Clear Chat 按钮
- **Service role 权限补充**：workouts + gym_logs

**Backlog 更新（已完成）：**
- Class Pool DB 化 + 管理 UI ✅
- Backlog `project_id` UI 入口 ✅
- Schedule Panel 手动内联编辑 ✅
- Context Sync Dashboard ✅
- Priority 回写 Gap ✅

**当前 Backlog（主要剩余）：**
- P2: Schedule Coaching Integration（schedule_suggestion proposal card）
- P2: Backlog 重构 — 清理现有 items，从 project 层面重新生成，讨论 dynamic prioritization
- P3: Priorities panel 显示优化
- P3: Web Push Notifications
- ⚠ Migration 042 已在 prod 验证（RLS/CRUD 正常），需确认 updated_at trigger

## Session 30 — 2026-07-23

_2026-07-23 更新（Session 30）_

**核心讨论：Backlog 生成架构重新设计**

从 KMS Vision 出发，重新定义了 Training Coach App 在两层架构中的角色：

**两层架构边界：**
- KMS = 策略层：Project overview、design decisions、principles、方向性 next steps。不再逐条追踪执行状态。
- App DB = 执行层：projects_state（bridge）、priming_backlog（to-do list）、coaching_sessions。完成状态完全由 DB 承载。

**Coaching Output 三层 Routing：**
所有 coaching session 产出自动路由到三个去向：
1. Global Decisions → _priority.md / POS（影响日常安排、能量管理）
2. Project Decisions → Project doc（项目内方向性结论、原则）
3. Action Items → priming_backlog（具体下一步执行）

**Push-Through Cascade（两个方向）：**
- 方向 A（Project → Backlog）：Coaching wrap-up → decisions → 和现有 backlog 做 project-scoped diff → suggest 新增/改变状态/stale
- 方向 B（Backlog → Project）：Backlog item done → 检查对应 project → suggest 移除已完成的 → 加入 write-back 队列

**Timestamp-Based Diff：**
- done_at > source.updated_at → source 未刷新 → 跳过
- done_at < source.updated_at → source 又更新但仍保留 action → 建议新增或改变状态

**Stale Review：**
Priming 底部按钮 → sync endpoint → 显示 diff 结果（新增/改变状态/stale/待回写）→ 用户 confirm

**待实现（Session 31+）：**
1. Migration：priming_backlog.source + done_at 字段
2. Shared lib：src/lib/backlog-utils.ts
3. 所有写入路径加 source 值
4. Done toggle 写 done_at
5. Coaching wrap-up cascade（project-scoped diff）
6. Stale Review UI
7. sync-context 触发 cascade
8. 统一去重（normalizeTask()）

**Backlog 清理：**
- Gym PR Chart Done
- Nutrition / Timezone / Calendar events → deferred（标记保留在 tech-spec，不再出现在活跃列表）
