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

- **Today tab** — AM/PM Pulse（AutoSleep webhook）、readiness banner + Apply、Gym Logger（warmup sets、inline edit、rest timer）、7-day lookahead、历史回溯
- **Coaching tab** — AI chat、Rule 提案卡、Body Scan 录入、In-App Weekly Scheduler（drag-and-drop）、Proactive Insights（daily cache + dismiss）
- **Metrics tab** — 体成分趋势图、gym PR 曲线、unified energy score
- **Exercise Library** — 30+ exercises、equipment type、weight steps、Exercise Bank UI、AI coaching card
- **Gym Templates** — DB-backed named templates + mode selector
- **Training modes** — Deload Mode、Training Mode per exercise、Rebellion & Consequence Engine
- **Infrastructure** — Calendar reconcile cron、Google OAuth、Supabase RLS、Dev/Prod split（develop branch + Vercel Preview）

---

## Open Backlog

| 优先级 | Item |
|--------|------|
| P1 | Priming Integration — AM Pulse 读取 `/priming` 输出 |
| P2 | Exercise Library v3 — AI Substitution（swap 时 AI 排序候选） |
| P3 | Exercise Library v3 — YouTube links |
| P4 | Nutrition Module（独立 track） |
| P5 | PWA Logo |
| Defer | Timezone Review |

---

_代码已移出 vault。此文件每次开发会话结束后同步更新。_
