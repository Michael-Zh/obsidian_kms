---
name: Road_to_2040_Investment_Blueprint
project_id: pj0010
status: active
pillar: Finance
current_focus: "Surrogacy 基金执行口径锁定（Wise $18.3k 种子 + €850/月 → 2029 Q3 €50k）；GOOGL 第一批已完成、仅跟踪第二批；net worth 月度 review；Q4 tax optimization。"
created: 2026-04-15
updated: 2026-09-01
target_completion: 2040-12-31
priority: P2
execution_state: autopilot
tags:
  - Finance
---
# Road to 2040 Investment Blueprint

## Overview

Build a retirement portfolio targeting age 50 (2040) via a "Barista FIRE" strategy. The system runs on automated Waterfall Cashflow and a 3-Tier Investment Architecture. Core decisions follow Vanguard principles and Dutch tax optimization. Active tiers (Tier 2/3) are rule-driven by [[Daily_Tactical_SOP]] — no active research or manual monitoring required.

---

## Objectives & Goals

- **Goal 1:** Reach €50k CapEx fund (surrogacy) with zero market risk by Q3 2029 — held in T212 cash at 3.5% interest. **Funding（2026-09-01 定）:** 种子 Wise $18,340（≈€15,803）+ €850/月 → Q3 2029 达标 €50k。
- **Goal 2:** Hit Barista FIRE target of **€684,000** in retirement portfolio by 2040 via €1,600/month automated contributions (100% EUNL/IWDA).
- **Goal 3:** Shield capital from Box 3 wealth tax (€57,684 threshold) via Pillar 3 (Box 1) pension structures.

---

## Roadmap

| Phase | Timeline | Goal | Status |
|---|---|---|---|
| **Phase 1: Foundation** | Q2 2026 | Pension consolidation, baseline net worth setup. Waardeoverdracht completed 2026-06-20: €9,722.32 transferred to current employer pension. Net Worth mapped at €121k. | ✅ Completed |
| **Phase 2: Accumulation** | Q3 2026 – Q3 2029 | Reach €50k CapEx fund; push Bucket 2. Monthly €1,600 EUNL drip; Box 1 (Brand New Day) funding to lower Box 3 exposure. | 🔄 In Progress |
| **Phase 3: Deployment** | Q4 2029 onward | Execute surrogacy; continue retirement portfolio growth. | ⏳ Planned |

---

## 3-Tier Investment Architecture

| Tier | Time Horizon | Purpose | Capital | Risk | How It Runs |
|---|---|---|---|---|---|
| **1. Core** | To 2040 | Retirement (Goal 2) + CapEx buffer (Goal 1) | €1,600/month → T212 EUNL; CapEx cash in T212 3.5% | Medium | Fully automated. Never touch. |
| **2. Tactical** | Weeks–Months | Capture medium-term opportunities (event arbitrage) | €7,000 — T212 Custom Pie | High | Rule-driven. Daily Tactical SOP triggers at 16:00 CET. No manual research. |
| **3. Sandbox** | Days–Weeks | Experimental short-term trades (learning by doing) | ~$1,000 — Schwab USD | Very High | Rule-driven. Daily Tactical SOP. Physically isolated from Core. |

**卫星仓（Tier 2/3）退出规则（2026-09-02 定）** — 把止盈从「区间」改成「具体动作」：

| 触发 | 动作 |
|---|---|
| 浮盈 ≥ +5% | 减半 |
| 浮盈 ≥ +10% | 清仓（或按标的特定目标价） |
| +5% 后回撤 ≥ 3% | 离场（移动止盈） |
| 浮亏收窄至 −10% 内 | 主动换仓 |
| 跌破保护线 | 减仓 |

> 各标的特定阈值优先（MSFT €340/€480、AAPL $275、GOOGL P/E、IKRA −10%）。Tier 1（EUNL/CapEx）不适用此规则，长期持有不触及。

---

## Waterfall Cash Management (The €5,000 Engine)

Automated monthly flow:

1. **ABN（中转）** — 仅中转房贷/固定账单等必经荷兰账户的款项，不存现金（≈€118）。
2. **Wise（Surrogacy 种子）** — $18,340（≈€15,803）作为 Surrogacy 启动种子，一次性迁至 T212 3.5% 稳定基金。
3. **T212 稳定基金（3.5%，三个现金桶，物理隔离）**：
   - Surrogacy 桶：种子 €15,803 + €850/月 → 2029 Q3 达标 €50k（Goal 1），不得挪用。
   - GOOGL 第二批子弹：~€2,000，触发 P/E < 16 或价格 ~$318。
   - Spending pot：日常花销（T212 借记卡）。
4. **T212 Invest（FIRE）** — €1,600/月（或全部剩余）自动投入 Core EUNL Pie（Goal 2）。

---

## Annual Tax Protocol (Q4)

**Peildatumarbitrage:** Review October/November annually. Temporarily sell Box 3 assets to cash before Jan 1 to lower fictitious return tax; buy back in April. Execute only if tax savings > historical Q1 market return + spread costs.

---

## Current Focus

- 系统运行中 — automated waterfall + 3-tier 已运行；AI 投资简报（/investment-brief）每日 16:00 自动跑；net worth 月度 review。
- 近期已定（2026-09-01）：
  1. Surrogacy 基金：Wise $18,340 种子 + €850/月 → 2029 Q3 €50k（见 Goal 1）
  2. GOOGL 第一批已完成（ABEA EUR 线 €1,493），仅跟踪第二批
  3. Wise 弃用（息无竞争力），现金统一迁至 T212 3.5% 稳定基金
- 待推进：Q4 tax optimization — Box 3 / Peildatumarbitrage / Pillar 3（Pillar 3 低优先级，Q4 用真实税率算）

## Connections

- [[Daily_Tactical_SOP]] — Daily execution script for Tier 2/3 trades
- [[Road_to_2040_Investment_Blueprint_networth]] — Net worth tracker

---

*Full decision log, quarterly reviews, and closed decisions: see `_Road_to_2040_trial_log.md`.*


## Strategic Direction

- Net worth 月度 review — 已定（对齐 monthly review + body scan 节奏）；最近一次 2026-09-01，€142,247
- AI 投资监控系统 — 已上线：launchd `com.michael.investment-brief` 每天 16:00 → `Brief/YYYY-MM-DD.md`
- GOOGL 第二批进场 — 第一批已完成（ABEA EUR 线 €1,493），仅跟踪第二批临界点
- Q4 tax optimization review — Box 3 / Peildatumarbitrage / Pillar 3（Pillar 3 低优先级，Q4 用真实税率算）

---

## Decisions

- **2026-07-24:** Status changed from parked → active P3. System fully operational — passive monitoring only.
- **2026-08-09:** Priority P3 → P2（重要但不紧急，大部分 setup 已完成）。Current focus 调整为：net worth 更新频率 TBD、AI 投资监控系统开发、Q4 tax optimization review。
- **2026-09-01:** Surrogacy 基金执行口径锁定：Wise $18,340（≈€15,803）为启动种子，迁至 T212 3.5% 稳定基金，另 €850/月转入，2029 Q3 达标 €50k。GOOGL 两批进场第一批已完成（ABEA EUR 线 €1,493），后续仅跟踪第二批。net worth 更新至 €142,247。
