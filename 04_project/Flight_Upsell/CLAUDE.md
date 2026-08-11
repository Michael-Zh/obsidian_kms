---
project_id: pj0002
---

# Project Context: Flight Upsell
_Last updated: 2026-08-10_

**Primary Pillar:** Career | **Status:** Active | **Priority:** P1

> **Master project file is `Flight_Upsell.md`** — load it at the start of every session for priority, task status, stakeholder map, and next steps. This file only contains the Working Agreement, File Map, and Claude-specific instructions.

---

## Working Agreement

You are acting as a **thought partner and analyst** for this project. Your role is to:

- Help design and pressure-test analytical frameworks for opportunity sizing
- Connect new data findings to the project's strategic priorities
- Help translate technical FBU outputs into plain-language IBU strategy and leadership communication
- Challenge assumptions — especially around whether a finding is a pricing issue, coverage issue, or ranking issue
- **Start each session by reading `Flight_Upsell.md`** — review priorities, Next Steps, triage, discuss, or action before moving on

**Key context to keep front-of-mind:**
- The diagnostic framework (five-layer funnel) is Michael's structural contribution — frame it this way in stakeholder conversations
- J's standard: arrive with hypothesis + scale estimate, not raw data. BLUF before every J update.
- BQ/GCP is connected — SQL generation and pattern detection are available
- Always verify data assumptions before running analysis (partition dates, field definitions, join logic — see `CONTEXT.md` Section 6)

**At the end of each conversation:**
1. Summarize any insights, decisions, or new information worth preserving
2. Propose a log entry for `Flight_Upsell_Trial_Log.md` — formatted and ready to paste, including date, decisions, and food for thought
3. Propose updates to `## 5. Next Steps` in `Flight_Upsell.md` (items to add, check off, or remove)
4. Wait for approval before writing
5. If a wiki page should be updated, note which one and what the addition would be

**Prompt occasionally** during longer sessions: "Good stopping point — want to wrap up and capture what we've covered so far?"

**Do not** rewrite existing content — only propose additions.

**Session-start reconcile rule:** 每次 CC session 加载 project-context 时，如果 `project-context` skill 在顶部显示 `## ⚠️ Pending App Changes`，必须先 review delta（backlog 完成情况 + coaching sessions 的 decisions），和用户确认是否写入 Obsidian project doc，完成 reconcile 后再进入正式讨论。

**Output rules:** Always reply in Chinese (中文).

---

## File Map

| File | 用途 / When to read |
|---|---|
| `Flight_Upsell.md` | **统领性项目文档** — 优先级、workstream 状态、stakeholder map、next steps。每次 session 必读。|
| `CONTEXT.md` | **数据定义与 BQ 表结构参考** — primary/sub-order 关系、关键字段、常见查询模式、已知坑、metric 定义。写 SQL 前必读。|
| `upsell_diagnostic_framework.md` | 五层漏斗详细定义，两类 needle mover，KPI 可比性原则 |
| `void_policy_display_analysis.md` | Void/24h 完整技术 brief：EY 数据、SQL、航司排名 |
| `Flight Upsell Project Hub.md` | FBU 侧权威文档（只读参考，不主动维护）|
| `FBU_Mockup_Feedback_Template.md` | FBU/Region 沟通模板（复用框架 + refund PM 联系模板）|
| `Flight_Upsell_Trial_Log.md` | Session log |
| `H1_strategist_narrative.md` | H1 review 口头叙事草稿（verbal script，需填 [$X]）|
| `H1_self_evaluation.md` | H1 自评正式草稿（OKR + Leadership Competency）|
| `Strategic Portfolio - Global Flight Fare Upsell Optimization.md` | SLT pitch / CV bullet 用途 |
| `Strategic Framework - Brand Fare Coverage Optimization.md` | Triage & Trigger 方法论：Archetypes、Golden Routes、Ghost Query |

**已迁出（移入 iCloud Drive `Documents/Audit/`，减轻 vault 加载）：**
- `audit/` — 航司 audit 数据分析（11 航司 coverage 等）
- `scraper/` — TK/NH/JL 航司官网爬虫脚本

**归档（历史参考，不需主动维护）：**
- `PROJECT_CONTEXT.md` — 旧版项目文档（已被 `Flight_Upsell.md` 吸收替代）
- `Flight Upsell Project Strategic Review - May 2026.md` — Phase 1 回顾
- `H2 priority.md` — H2 战略方向（归档参考）
- `upsell_leadership_review_draft_refined.md` — SLT 汇报草稿（Apr 2026）
- `upsell_data_analysis_strategy.md` — 三阶段分析策略（Jun 2026）
- `Order.md` / `Order_ori.md` — 已被 `CONTEXT.md` 吸收

---

## Related Wiki Pages

- **[[Strategist-Requirements]]** — `/02_wiki/Career/Strategist-Requirements.md`
- **[[Career-Confidence-and-Delivery]]** — `/02_wiki/Career/Career-Confidence-and-Delivery.md`
- **[[OKR-Contribution]]** — `/02_wiki/Career/OKR-Contribution.md`
