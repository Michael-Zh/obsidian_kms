---
name: "Flight_Upsell"
project_id: "pj0002"
status: "active"
pillar: "Career"
current_focus: "AirAsia VP/VPL 排查与优化；Refund/Change Policy 前端展示推动；AI-augmented discovery"
created: "2026-04-15"
updated: "2026-08-10"
target_completion: "ongoing"
priority: "P1"
tags: [Career]
---

# Flight Upsell — Commercial Opportunity Analysis
_Last updated: 2026-08-10_

## 1. 项目背景与战略定位

**业务问题：** 国际机票中间页用户选择最低价运价，错失更高层级运价的销售机会。GMV 增长是 2026 年新增战略重点，放大了这个方向的优先级。

**IBU 的角色演变：**
- **Phase 1（已交付）：** Coordinator — 建立 FBU/IBU 协同机制，统一 KPI，启动 Brand Fare Audit
- **Phase 2（进行中）：** Insight Engine — IBU 独立生成颗粒度数据洞察，驱动优先级决策和产品方向
- **Phase 3（H2 新增方向）：** AI-Augmented Discovery — 用 AI 辅助 strategic opportunity 发现和数据 exploration，减少人工整理工作量

**Primary KPI：** Trip Middle-Page Upsell Rate：33% → 38%（2026 目标）
- 计算口径：非最低价运价的主订单数 / 全部主订单数
- Guardrails：CR、用户停留时长、GMV 无负向影响
- 范围：Y/W 舱，1-Meta，全市场

---

## 2. 当前工作流（2026 年 8 月）

### Priority 1：AirAsia Value Pack / Value Pack Lite（VP & VPL）

AirAsia 是量最大的航司之一。VP（Value Pack：20kg 托运 + 选座 + 餐食）和 VPL（Value Pack Lite：15kg 托运 + 选座）是 AirAsia 的 bundle 运价，目前在 Trip.com 上的 coverage 和展示均有问题。

#### 正在解决中（In Progress）

| # | 事项 | 状态 | 下一步 |
|---|------|------|--------|
| 1 | **VPL highlight label** | Region 已提交申请，审核中 | 等待审批通过；使用 existing capability 实现 |
| 2 | **运价 loading time 过长** | 技术部门讨论解决方案中 | 跟进技术方案和时间线 |
| 3 | **Free seat selection / free meal wording 修改** | 流程已启动，等待更改结果 | 确认更改生效后验证前端展示 |

#### 需要进一步分析（Needs Analysis）

| # | 事项 | 假设 | 下一步 |
|---|------|------|--------|
| 4 | **Return trip 中 VPL 显示与排名** | VPL 在 return trip 中未显示或排名低；可能是 pricing 不 competitive 或 mixed airline 未配置 VPL | (a) 前端排查 return trip 中 VPL 是否有显示及排名；(b) 与 mixed airline 团队讨论 configuration include 选项 |
| 5 | **VP/VPL coverage rate（AI-assisted 查询显示 ~50%）** | 不确定是真实 supply gap 还是计算口径问题 | 排查 50% 数据的根因：区分真实 coverage 问题 vs. 分母/计算逻辑问题 |

---

### Priority 2：Refund/Change Policy 前端展示

从 Q2 的 void/24h 分析延伸而来。核心问题是退改政策在前端的展示不准确、不透明，抑制了用户向 Flexible 运价升舱的动机。

| 事项 | 状态 | 下一步 |
|------|------|--------|
| **Issue collection 已发送给 FBU 前端同事** | FBU 正在 review | 跟进 review 进展；推动进入执行 |
| **关联：void/24h 标签覆盖真实退改政策** | 已量化（~11% 订单 affected），FBU 确认 UX 问题，进入 H2 roadmap | 与 refund/change PM（O4-KR3 mid-tier owner）建立联系；推动方案落地 |

---

### Priority 3：AI-Augmented 工作方式

目标：减少人工整理和分散搜集材料的工作量，让 AI 能辅助 strategic opportunity discovery。

| 事项 | 状态 | 下一步 |
|------|------|--------|
| **AI context 建设** | `CONTEXT.md` 已建立（BQ 表结构、字段定义、metric 定义、已知坑） | 持续维护；新增 SQL template 库 |
| **GitHub repo 连接** | Repo: `github.com/Michael-Zh/obsidian_kms`，已验证 fetch/log 正常 | 保持正常 commit 节奏 |
| **AI 辅助 analysis** | 已实验性使用（如 AirAsia mixed airline 分析） | 后续 BQ analysis 优先让 AI 跑，减少手动 SQL 编写 |

---

### Priority 4：Q2 Airline Audit 收尾

| 事项 | 状态 |
|------|------|
| 11 航司 coverage 全景分析 | ✅ 已完成（2026-07-20） |
| BR 五层诊断 | ✅ Closed — Product Design Ceiling，非 Trip.com 可修复 |
| CI 五层诊断 | ✅ 数据基线完成，待官网人工走查 |
| NH ATPCO brand name 验证 | ✅ 完成 |
| 剩余 FSC + EU LCC audit | 待完成 |

---

## 3. Five-Layer Diagnostic Framework

```
Data Foundation → Supply → Fare Selection → Ranking → Display
```

每一层的问题类型和诊断信号详见 `upsell_diagnostic_framework.md` 和 `CONTEXT.md` Section 7。

**两类 needle mover：**
- **Type 1 — Volume Capture Gap：** 供应侧覆盖不足（如 VP/VPL coverage）
- **Type 2 — Revenue Quality Gap：** 展示层错误抑制升舱意愿（如 void/24h、退改展示）

---

## 4. Stakeholder Map

| 角色 | 姓名 | 关联事项 |
|------|------|----------|
| IBU Project Sponsor | Serena Wang | 项目背书 |
| IBU Project PoC | J Nam | BLUF first，带 hypothesis + 量级估算 |
| FBU Project PoC | Vivi Ye | 产品/前端协调，ABT 排期 |
| FBU Upsell KR Owner | Jessie Li | O2-KR1 Fare Upsell Conversion |
| 前端 PM（运卡表达）| Doris Xie | O2 运卡表达提效 |
| 前端 PM（post-booking/cross-sell）| 孙爽 | O4-KR3 Order Detail + refund/change mid-tier（mid-tier 标注 multiple owners） |
| FBU BI | 新接替待宣布 | 数据合作 |
| IPU Data Engineer | — | ETL 支持升级 |

**J 的标准（始终牢记）：**
1. Needle-mover scale：量化，不只是识别
2. Independent judgment：带 hypothesis 来，不带原始数据
3. BLUF before every update：先说结论，再给数据

---

## 5. Next Steps

**AirAsia VP/VPL**
- [ ] 跟进 VPL highlight label 审批
- [ ] 跟进 loading time 技术方案
- [ ] 确认 wording 更改生效
- [ ] 前端排查 return trip 中 VPL 显示与排名（是否存在、排名 position）
- [ ] 与 mixed airline 团队讨论 VPL configuration
- [ ] 排查 VP/VPL coverage 50% 的根因（真实 supply gap vs. 计算逻辑）

**Refund/Change Policy**
- [ ] 跟进 FBU review issue collection 的进展
- [ ] 与 refund/change mid-tier PM 建立联系，确认 scope
- [ ] 推动 void/24h + service fee display 联合方案落地

**AI Infrastructure**
- [ ] 持续维护 `CONTEXT.md`
- [ ] 保持 GitHub commit 节奏
- [ ] 后续 BQ analysis 优先让 AI 代跑

**Airline Audit Carryover**
- [x] CI 官网人工走查（TPE→NRT、TPE→HKG、TPE→LAX）
- [ ] 完成剩余 FSC（欧线 + 北美/中东/日本）+ EU LCC audit

---

## 6. Connections

**Parent Pillar:** [[Career]]

**Related Projects:**
- [[AI_learning]] — AI-driven commercial analysis skills

**Key Reference Docs:**
- [[FBU H2 Upsell 项目文档]]（Vivi 维护）
- Flight User Product Team H2 OKRs: https://trip.larkenterprise.com/docx/RD7hdAzmZoAnU9xwt5aczLffnPb
