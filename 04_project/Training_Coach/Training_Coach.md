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

- **Priming tab（第一位）** — KMS GitHub 读取（_POS.md、_priority.md、最新 coaching 文件、_in_case_you_are_bored.md Active Projects + Backlog）+ 今日训练/睡眠数据；结构化 AI JSON 输出（brief_markdown + top3 + backlog）；**v6（Session 20）Top3 架构统一**：`is_top3` 作为 `priming_backlog` 上动态标签（Migration 035），`done` 字段统一跨 Top3/Stretch/Backlog，tab 切换不丢失；mount 自动生成；Stretch 区域；Top3 可拖动；9-pillar 颜色系统；Backlog 面板；Google Calendar 写入；**Session 22 新增：Backlog 内联编辑**（task/category/due_date，Migration 037）；**AppIdeas category + 全局 FAB**（Lightbulb 悬浮按钮，chat-style panel，自由文字 → priming_backlog，training-coach-context skill 自动拉取标记 done）；**briefOnly Regenerate**（stale banner 只刷新 brief，保留 Top3；Top3 任何改动只 setBriefStale，手动触发）；**"Today's Focus & Workouts" 统一列表**（Top3 + Google Calendar 训练事件按时间混排，拖拽后自动 recomputeSuggestedTimes 避开训练块）；**Calendar 冲突检查**（block 前验证时间重叠，有冲突弹确认 modal）
- **Today tab** — 两阶段加载；AM/PM Pulse；readiness banner + Apply；Gym Logger；date navigation；WorkoutCard bold solid pillar 颜色；WorkoutStatus 三值（planned/completed/skipped）
- **Coaching tab** — 3-scope；AI chat + rule proposals；Time-Limited Rules；**End Session 改造（Session 22）**：只汇总 lastSessionAt 之后的新消息；summary inline 插入 messages 流；shouldScroll ref 恢复（防历史加载滚底）；`coaching_messages` 按 scope 持久化
- **Metrics tab** — 体成分趋势图、gym PRs；Sleep/HRV/RHR 双 Y 轴图表
- **Exercise Library** — 30+ exercises；Exercise Bank UI；AI coaching card
- **Infrastructure** — Calendar reconcile cron；sync-context GitHub Action；Supabase RLS；Dev/Prod split；prod→dev 数据同步脚本
- **UI 设计系统** — "Grid & Blob"；4 pillar 颜色；浮动 pill dock nav；GymLogger `#0A0A0A` 全深色；`overscroll-behavior-y: none`
- **PWA Icons（Session 22 修复）** — apple-touch-icon.png + icon-192/512.png，正确 PNG 格式（之前为 JPEG 内容 + .png 扩展名，Chrome manifest 校验失败）

---

## Open Backlog

| 优先级 | Item |
|--------|------|
| TBD | Dance Intensive Week Program Builder |
| TBD | Life Management System 整体审视 |
| ~~P1~~ | ~~PWA Logo~~ ✅ Icons 修复 (Session 22) |
| ~~P0~~ | ~~Backlog 内联编辑（task/category/due_date）~~ ✅ Done (Session 22) |
| ~~P0~~ | ~~AppIdeas FAB + category~~ ✅ Done (Session 22) |
| ~~P0~~ | ~~Training Events → Priming 统一列表~~ ✅ Done (Session 22) |
| ~~P0~~ | ~~briefOnly Regenerate~~ ✅ Done (Session 22) |
| ~~P0~~ | ~~Calendar 冲突检查~~ ✅ Done (Session 22) |
| P3 | Priorities panel 显示优化（Short-Term Focus 摘要） |
| P2 | Web Push Notifications |
| P3 | Exercise Library v3 — AI Substitution + YouTube links |
| P4 | Nutrition Module（独立 track） |
| P4 | Calendar 主日程 → Priming 只读卡（低优先级） |
| Defer | Timezone Review |

---

_代码已移出 vault。此文件每次开发会话结束后同步更新。_
