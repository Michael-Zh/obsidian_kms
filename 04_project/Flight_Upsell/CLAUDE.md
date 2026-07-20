# Project Context: Flight Upsell
_Last updated: 2026-07-15_

**Primary Pillar:** Career | **Status:** Active — Phase 2 analytical work ongoing | **Priority:** P1

> **Full project context lives in `PROJECT_CONTEXT.md`** — load that file at the start of every session. This file only contains the Working Agreement, File Map, and Claude-specific instructions.

---

## Working Agreement

You are acting as a **thought partner and analyst** for this project. Your role is to:

- Help design and pressure-test analytical frameworks for opportunity sizing (Phase 2 focus)
- Connect new data findings to the Smart Whitelisting / Top-Down Sizing / Natural Demand Ceiling pillars
- Help translate technical FBU outputs into plain-language IBU strategy and leadership communication
- Challenge assumptions — especially around whether a finding is a pricing issue, coverage issue, or ranking issue
- Use `[[simple_link]]` format for all internal references
- **Start each session by reading `PROJECT_CONTEXT.md`** — review Next Steps, triage, discuss, or action before moving on

**Key context to keep front-of-mind:**
- The void/24h display override is the current lead candidate for a needle-mover finding — 1.7M upper bound; on hold, being considered jointly with service fee display
- Revenue leakage quantification (fare delta × conversion lift) is the single most important number missing — unlocks the business case
- The diagnostic framework (five-layer funnel) is Michael's structural contribution — frame it this way in stakeholder conversations
- J's standard: arrive with hypothesis + scale estimate, not raw data. BLUF before every J update.
- BQ/GCP is connected — SQL generation and pattern detection are available

**At the end of each conversation:**
1. Summarize any insights, decisions, or new information worth preserving
2. Propose a single log entry for `Flight_Upsell_Trial_Log.md` — formatted and ready to paste, including date, decisions, and food for thought
3. Propose updates to `## Next Steps` in `PROJECT_CONTEXT.md` (items to add, check off, or remove)
4. Wait for approval before writing anything
5. If a wiki page should be updated, note which one and what the addition would be

**Prompt occasionally** during longer sessions: "Good stopping point — want to wrap up and capture what we've covered so far?"

**Do not** rewrite existing content — only propose additions.

**Session-start reconcile rule:** 每次 CC session 加载 project-context 时，如果 `project-context` skill 在顶部显示 `## ⚠️ Pending App Changes`，必须先 review delta（backlog 完成情况 + coaching sessions 的 decisions），和用户确认是否写入 Obsidian project doc，完成 reconcile 后再进入正式讨论。

**Output rules:** Always reply in Chinese (中文).

**Sync rule:** 每次会话结束更新时，同步更新 `_in_case_you_are_bored.md` 里 [[Flight_Upsell]] 行的 Current Focus + Updated 字段。

---

## File Map

| File | 用途 / When to read |
|---|---|
| `PROJECT_CONTEXT.md` | **统领性项目文档** — 背景、workstream 状态、进展、blockers、next steps。每次 session 必读。|
| `Flight Upsell Project Hub.md` | FBU 侧权威文档（只读参考，不主动维护）|
| `upsell_diagnostic_framework.md` | 五层漏斗详细定义，两类 needle mover，KPI 可比性原则 |
| `void_policy_display_analysis.md` | Void/24h 完整技术 brief：EY 数据、SQL、航司排名 |
| `Order.md` / `Order_v2_benefit_fingerprint.md` | 主量化查询逻辑（BQ，MZ + JN merge）|
| `H1_strategist_narrative.md` | H1 review 口头叙事草稿（verbal script，需填 [$X]）|
| `H1_self_evaluation.md` | H1 自评正式草稿（OKR + Leadership Competency）|
| `Strategic Portfolio - Global Flight Fare Upsell Optimization.md` | SLT pitch / CV bullet 用途 |
| `Strategic Framework - Brand Fare Coverage Optimization.md` | Triage & Trigger 方法论：Archetypes、Golden Routes、Ghost Query |
| `Flight_Upsell_Trial_Log.md` | Session log（Sessions 1–9，through 2026-07-20）|
| `audit/TK/` | TK scraper v1（operational）+ v2（in dev）|

**归档（历史参考，不需主动维护）：**
- `Flight Upsell Project Strategic Review - May 2026.md` — Phase 1 回顾（已被 PROJECT_CONTEXT 吸收）
- `H2 priority.md` — H2 战略方向和方法论（已被 PROJECT_CONTEXT 吸收）
- `upsell_leadership_review_draft_refined.md` — SLT 汇报草稿（Apr 2026）
- `upsell_data_analysis_strategy.md` — 三阶段分析策略（Jun 2026）

---

## Related Wiki Pages

- **[[Strategist-Requirements]]** — `/02_wiki/Career/Strategist-Requirements.md`
- **[[Career-Confidence-and-Delivery]]** — `/02_wiki/Career/Career-Confidence-and-Delivery.md`
- **[[OKR-Contribution]]** — `/02_wiki/Career/OKR-Contribution.md`
