---
project_id: pj0008
---

# Travel Buddy

**GitHub:** https://github.com/Michael-Zh/travel_buddy  
**本地代码：** `~/Documents/Apps/travel-buddy`  
**Stack:** Next.js 14 App Router, Tailwind, localStorage（MVP）→ Supabase（post-MVP）

---

## Vision

Mobile-first 旅行全程伴侣：规划、实时调整、行后复盘、灵感 backlog。  
核心问题：旅行上下文碎片化——备选方案、半查的餐厅、途中发现的地方，行程结束后全部消失，下次规划从零开始。

---

## 三大功能柱

1. **Plan & Adjust** — 行前行程 + 实时调整；结构化日程（anchor event、博物馆最多1/下午、午晚餐预定 + 位置绑定）；热浪协议（室外 8-11AM / 6PM+，室内 11AM-6PM）；每个场所两个链接：官网 + Google Maps
2. **Reflect & Review** — 行后趁记忆鲜活录入；场所评分 + 笔记；酒店 debrief；整体行程反思 → 回流 backlog
3. **Backlog / Inspiration Pool** — 两类来源：行程残留（未去的备选）+ 日常发现（社媒/朋友/文章）；规划时优先展示目标城市 backlog；标签：城市、类别、状态（unvisited/visited/skip）

---

## 当前状态

MVP in progress（localStorage 方案）。与 Vibe Coding Tool 同 repo，路由在 `/`（Travel App）和 `/dev`（Vibe Tool）。

**Screen 架构：** `/backlog`、`/backlog/new`、`/trips`、`/trips/[id]`、`/reflect/[tripId]`（post-MVP）

---

## Open Backlog

- MVP 完成：Backlog CRUD + Trip 创建 + Day grid + Slot editor
- Post-MVP：Supabase 持久化、Reflect 模块、离线支持

---

_代码已移出 vault。此文件每次开发会话结束后同步更新。_
