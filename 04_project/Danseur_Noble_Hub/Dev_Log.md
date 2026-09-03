# Dev Log — Danseur Noble Hub

> Extracted from Training_Coach.md on 2026-08-09 during LMS restructuring.
> 代码位置：`~/Documents/Apps/danseur-noble-hub`

> ⚠️ **本文件不是真相源。** 完整逐 session 日志在 app repo：
> `~/Documents/Apps/danseur-noble-hub/docs/Training_Coach_Dev_Log.md`
> 本文件只保留 KMS 侧需要知道的里程碑。详细代码变更不往这里同步。

---

## 状态（2026-09-03）

**开发已主动暂停。** 原因：日常只用 scheduling，未 active 使用整个 app → 还没痛到需要「把 priority 结构长进 app、做外置决策器」那条 KPI。重启条件（三者任一）：① meal prep 需要认真做 priming；② 个人 priority 管不过来；③ 超体学完后对 app 整体方向有新判断。

**代码最新：** Session 52（2026-08-31）。

---

## Session 35–52 里程碑摘要（2026-08-11 → 08-31）

*KMS 侧此前停在 Session 34，中间 18 个 session 压缩如下。逐条见 app repo 日志。*

**信息架构**
- Today 合并进 Priming，后改名 Today；回溯简化为 Gym History 入口（S39–41）
- Priming 去工作化，Backlog section 可折叠；Flight Upsell 移除（S37）

**Training 单一真相源（S44–47）**
- 执行细节全部落 App DB，三桶分类：constraints 7 / guidelines 15 / context 8
- Workout plan 结构定案：gym 落 Thu+Fri back-to-back；HJS 枢轴三分支由 scheduling 问卷推导
- class_pool 完整目录重建 + tier 字段；两轴 quota + deload cadence；肌肉间距软参考
- 对应 KMS 决策见 [[Training]] Decisions 2026-08-17

**Priority 系统（S42）**
- `execution_state` 火候轴上线 + 存量 backfill，与 `_priority.md` Execution Cadence 对齐

**KMS Knowledge Intake（S49）**
- 5 段知识流：捕捉 → 处理 → 写回 → 调用 → 归档
- Telegram bot (@Formichae_clipper_bot) → `knowledge_inbox` 表（Migration 052）
- YouTube pipeline：yt-dlp 字幕 → whisper 转录 → AI 判断三类（drop / pass_to_project / write_kms）
- 原则：AI 建议，用户一字确认，**永不自动写 KMS**

**Scheduling（S48, S51–52）**
- Calendar 实时同步 + 跳课补课；classifyConflict（office/show/social/tbc → hard）注入 adjust prompt
- `applicable_titles`（Migration 053）防约束误套；HJS 约束已填（S52）
- SchedulePanel 提取为共享组件，移入对话流；Stretch section 过滤已完成条目

**其他**
- project-context skill 重构 + 项目更新通路架构定稿（S50）
- Autosleep webclip 修复 + 历史数据回填 Aug 12–19（S49）

---

## Session 34 — 2026-07-26

**新增 / 变更：**
- Review 面板重构 — 从底部 fixed overlay 改为内联卡片，与 Backlog 面板同位置 toggle
- re-sync dual auth — service role key OR session cookie
- Middleware bypass — `/api/context/re-sync` + `/api/backlog/review/cc` 跳过 session auth
- Dashboard 图表 7-day moving average
- KMS H1 wikilink strip

**Backlog 更新：**
- Review UI 重构 Done
- Schedule Coaching → Drop
- Web Push → Defer
- 当前 P1：Review 每个 project 确保最新状态 → Backlog 重构

---

## Session 32 — 2026-07-25

**新增 / 变更：**
- CC Backlog Review API
- KMS Project 文档格式统一（Strategic Direction + Decisions + Archived）
- re-sync 严格文件名
- Prod DB 清理 + 18 KMS project docs 全部更新 + 4 新主文档
- Project 模板 + Skills 更新

---

## Session 31 — 2026-07-24

**新增 / 变更：**
- 移除 regenerate 路由
- 提取共享工具库 backlog-utils.ts（normalizeTask, guessProjectId, guessCategory）
- Migration 044：priming_backlog 加 source + done_at
- Stale Review 面板
- re-sync cascade：自动检测 stale backlog items

**架构决策：**
- Two-Layer Architecture 明确化
- 双向同步链路
- done_at timestamp 作为 stale 判断基础

---

## Session 30 — 2026-07-23

**核心讨论：Backlog 生成架构重新设计**
- 两层架构边界：KMS 策略层 vs App DB 执行层
- Coaching Output 三层 Routing（Global Decisions / Project Decisions / Action Items）
- Push-Through Cascade（Project → Backlog, Backlog → Project）
- Timestamp-Based Diff + Stale Review

---

## Session 29 — 2026-07-20

**新增 / 变更：**
- Context Sync Dashboard
- Priority Sync 闭环
- Class Pool DB 化（Migration 042）
- Backlog project_id UI 入口
- Schedule Panel 内联编辑
- Dashboard 重构（Metrics → Dashboard，charts 可折叠）
- Bug 修复 + Service role 权限补充

---

## Session 27 — 2026-07-19

**新增 / 变更：**
- Coaching tab 新增 Weekends scope（Location Calendar Weekend Planner）
- Priming backlog 按钮优化 + header pill
- WorkoutJournal 跨设备 display bug 修复
