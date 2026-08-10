---
name: Danseur_Noble_Hub
project_id: pj0007
status: active
pillar: LifeManagement
parent_system: Life_Management_System
current_focus: "LMS execution layer PWA — Priming + Backlog + Coaching + Training + Scheduling"
updated: 2026-08-09
priority: P1
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

- Priorities Panel 精简 — 直读 `_priority.md` Short-Term Focus section，不再 AI 压缩
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
