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

- **Priming tab（第一位）** — KMS GitHub 读取（_POS.md、_priority.md、最新 coaching 文件、**_in_case_you_are_bored.md Active Projects + Backlog**）+ 今日训练/睡眠数据；结构化 AI JSON 输出（brief_markdown + top3 + backlog）；Top3 可拖动卡片（category chip、suggestedTime、**durationMinutes ±15min stepper**、Block/Edit/Close）；Google Calendar "Focus Blocks" 写入（用 durationMinutes 计算结束时间）；Backlog 面板（优先级/分类双排序，±5 步长，Add/promote）；服务端自动去重 top3 与 backlog 重合项；9-pillar BacklogCategory；**页面加载自动生成（无需用户 brain dump）**；**安全 Promotion（关闭面板直接合并，>3 items 显示冲突面板，未选中 items 放回 backlog）**
- **Today tab** — AM/PM Pulse（AutoSleep webhook）、readiness banner + Apply、Gym Logger（warmup sets、inline edit、rest timer）、7-day lookahead、历史回溯
- **Coaching tab** — AI chat、Rule 提案卡、Body Scan 录入、In-App Weekly Scheduler（drag-and-drop）、Proactive Insights（daily cache + dismiss）
- **Metrics tab** — 体成分趋势图、gym PR 曲线、unified energy score
- **Exercise Library** — 30+ exercises、equipment type、weight steps、Exercise Bank UI、AI coaching card
- **Gym Templates** — DB-backed named templates + mode selector
- **Training modes** — Deload Mode、Training Mode per exercise、Rebellion & Consequence Engine
- **Infrastructure** — Calendar reconcile cron、Google OAuth、Supabase RLS、Dev/Prod split（.env.local = dev `tfwpakuignjlqcrndvbj`；.env.local.prod = prod `mcmlpcfaetkftawezjli`）

---

## Open Backlog

| 优先级 | Item |
|--------|------|
| P1 | Exercise Library v3 — AI Substitution（swap 时 AI 排序候选） |
| P2 | Exercise Library v3 — YouTube links |
| P3 | Nutrition Module（独立 track） |
| P4 | PWA Logo |
| Defer | Timezone Review |

---

_代码已移出 vault。此文件每次开发会话结束后同步更新。_
