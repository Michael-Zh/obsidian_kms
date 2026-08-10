# Dev Log — Danseur Noble Hub

> Extracted from Training_Coach.md on 2026-08-09 during LMS restructuring.
> 代码位置：`~/Documents/Apps/danseur-noble-hub`

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
