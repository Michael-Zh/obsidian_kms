# Flight Upsell — Project Context
_Last updated: 2026-07-21（夜）_

---

## 1. 项目背景与战略定位

**业务问题：** 国际机票中间页用户选择最低价运价，错失更高层级运价的销售机会。EU/AU 等区域团队发现：中文航司默认含行李，非中文市场的高阶运价（含行李 / 更灵活的退改）无论在供应侧还是展示侧都存在结构性缺口，导致 upsell 机会流失。GMV 增长是 2026 年新增战略重点，进一步放大了这个方向的优先级。

**IBU 的角色演变：**
- **Phase 1（已交付）：** Coordinator — 建立 FBU/IBU 协同机制，统一 KPI，启动 Brand Fare Audit
- **Phase 2（进行中）：** Insight Engine — IBU 独立生成颗粒度数据洞察，驱动优先级决策和产品方向

**Primary KPI：** Trip Middle-Page Upsell Rate：33%（当前）→ 38%（2026 目标）
- 计算口径：非最低价运价的主订单数 / 全部主订单数
- Guardrails：CR、用户停留时长、GMV 无负向影响
- 范围：Economy/Premium Economy，1-Meta，全市场

---

## 2. 为什么这件事复杂

### 五层诊断漏斗（Michael 的结构性贡献）

问题可能出现在任何一层，且各层之间相互掩盖：

```
Data Foundation → Supply → Fare Selection → Ranking → Display
```

- **Data Foundation：** 品牌运价映射不完整，brand tier 覆盖率参差不齐（ATPCO name → 官网 brand name → tier 三层映射）
- **Supply：** 运价未被爬取/对接；部分航司缺含行李运价（如 EY、WS）
- **Fare Selection：** 比价算法可能过滤掉本可参与 upsell 的运价（旁路表用于修正）
- **Ranking：** 高阶运价排序靠后，用户看不到
- **Display：** 展示信息错误或缺失（如 void/24h 标签误导，refundability 信号缺失）

### 两类 needle mover

- **Type 1 — Volume Capture Gap：** 供应侧覆盖不足（如 EU 航司缺含行李运价）；范围窄、FBU 可直接修复
- **Type 2 — Revenue Quality Gap：** 展示层错误抑制升舱意愿（如 void/24h）；全局均匀分布、IBU/Global Strategy 主导

### 跨 BU 协调难点

- FBU（产品/前端）、IBU（战略/分析）、Region BA、BD 各有议程和优先级
- FBU 带宽有限，无法主动做深度分析；IBU 需要主动填补 insight gap
- 区域团队自足感强（SEA），数据共享路径不统一
- 多条 ABT 并发，资源争抢导致排期延迟（C/F 算法曾因此被 block）

---

## 3. Workstream 概览与状态

| WS | 名称 | 优先级 | 状态 | 最新进展 |
|---|---|---|---|---|
| WS0 | Perf/Health Monitoring | P1 | Ongoing | Opportunity Exploration Framework 进行中；user research 进行中 |
| WS1 | Supply Coverage | P1 | Ongoing | 40+ 航司 audit 进行中；自动化 Brand Fare Mapping 三阶段推进（当前：Scraping，NH v2 修通待全量运行）；IBU 需提供航线清单 |
| WS2 | Fare Selection | P2 | Ongoing | 旁路表上线；C/F 比价算法 ABT Jul 7 上线 |
| WS3 | Ranking | P3 | Ongoing | Personalized Ranking ABT Jul 9 上线 |
| WS4 | Pure Front-end | P2 | Ongoing | 多个 ABT 同期推进（见下） |
| WS5 | Airline Compliance | P1 | Ongoing | LH/LA/CX 新增；AA/DL US locale 已实施 |
| WS6 | Pricing | P2 | H2 启动 | 框架方向已定（竞争力诊断 → 弹性分析 → Coverage 交叉）；需在 H2 OKR 占位 |

---

## 4. Phase 1 回顾（已交付，2026 Q1）

**交付物：**
- FBU-IBU 协同引擎：bi-weekly sync，单一联络窗口，40% 沟通成本降低，12+ 区域请求统一收口
- 全局 Brand Fare Audit：40+ 航司，识别重复性覆盖问题
- 新比价算法（Y/W）V2 上线：Fare Selection workstream 核心交付
- KPI 定义统一、六大 workstream 识别

**局限：**
- Upsell rate 停滞在 33–34%，离 38% 目标仍有差距
- Bulk optimization 边际收益递减（QoQ +1–2% vs. 初期 +3–4%）
- Q1 无前端变更（FBU PM 资源被 Ctrip 侧占用）

**Leadership 反馈：** J 和 Serena 对 Phase 1 交付明确给予正向肯定。

---

## 5. Phase 2 当前重点（进行中，2026 H1–H2）

### Lead Finding：Void/24h Display Override

**核心问题：** 后端 void/24h policy 标记触发"免费取消"标签，即使该机票实际不可退款。正确展示退款信号会激励用户升舱至 Flexible 运价——当前标签既误导用户，又抑制 upsell。

**数据规模（上界）：**
- EY：~144K 订单（Jan–May 2026），88% 有 void flag，86.7% 实为不可退
- UA：~47K（90.3% misled），DL：~33K（92.7%），AA：~26K（83.3%）
- 全航司 Top 40：>1.7M 订单上界；P0：EY/WS/UA/BA/AC；P1：TG/TK/LH/SK
- **重要限制：** 1.7M 是上界，实际展示量取决于 FBU display trigger logic（已获取）

**FBU 对齐（2026-06-25）：** 确认为 UX 问题，进入 H2 roadmap。FBU display trigger logic 已获取。
**当前状态（Jul 2026）：** On hold，与 service fee display 联合讨论中。前端负责人已换为**孙爽主导，Doris 辅助**；正在与 FBU 团队重新 align 合作模式。FBU 前端 OKR 已确认（Vivi 2.2 版，7 月 9 日）。方向：同时展示两项 vs. 跳转详情页（酒店侧 Doris 有先例）。
**H1 narrative：** 已完成。EY/UA/AC 案例深度分析已 close。

**Upsell 悖论（EY）：** EY 在错误标签下仍达 79% upsell rate（用户为行李升舱）。修正标签增加退款信号，只会进一步提升。

**Blockers：**
- 收益量化（fare delta × conversion lift）尚未完成——H1 叙事已 deliver，但量化数字对 business case 仍然重要
- 新合作模式尚未 align（孙爽接手后需重新建立沟通节奏）
- Void/24h + service fee 联合方案方向未定，影响 ABT metrics spec 设计

### 五层诊断框架（formalized）
详见 `upsell_diagnostic_framework.md`

---

## 6. 近期重要里程碑（Jul 2026）

| 日期 | 类型 | 内容 |
|---|---|---|
| Jul 11 | [ABT] | Web Middle Page Vertical Redesign Phase 1 上线（竖向 slide-out 布局）|
| Jul 9 | [ABT] | Personalized Ranking 上线（按购买概率排序）|
| Jul 7 | [ABT] | C/F 比价算法 ABT 上线（与 Y/W 逻辑一致）|
| Jul 3 | [Rollout] | Full Change/Refund Cost Display 全量（App，总费用 = 服务费 + 航司罚金 + 代理费）|
| Jul 2 | [Rollout] | Quick Filter（行李）全量（App）|
| Jun 30 | [Live] | 旁路表上线（可通过业务规则保留否则被过滤的运价）|
| — | [Closed] | Compact Itinerary V1 结论：Group B 负向；Group E 混合（+0.37% CR，−2.50% upsell）|
| — | [New] | Strict Fare Display Compliance：LH / LA / CX 新增 |

---

## 7. H2 Active Initiatives

### 旁路表 + BA fare recovery（P0）
- BA 发现部分运价因比价算法过滤逻辑被漏售
- 已正式向 FBU 提出，已知会 region
- 待定：监测 metrics + data source alignment；设计 pre-post 测试；决定上线时机

### AirAsia Value Pack Lite（P0）
- AirAsia 是量最大的航司之一，近几个月连续下滑，需要确保新功能发挥最大效益，对 region 影响重大
- AirAsia 正式上线 Value Pack Lite package
- (a) 覆盖率排查：supply 问题据说已解决，需验证完整性
- (b) 价格排查：竞争力验证
- (c) Seat selection 价值评估：Jay 已有 potential 分析；FBU 需时间将 free seat selection 展示在运卡

### Q3 工作框架（Draft，待与 J 对齐）

**Part 1 — H1 Carry-over：Audit 收尾 + 航司排查**

H1 方法论（baggage share → fare family comparison → root cause diagnosis）的继续推进：
- **航司 audit 收尾：** 剩余 FSC（欧线 + 北美/中东/日本）+ LCC（EU LCC 为重点）
- **低 share 航司排查：** 用现有方法论补完余下航司，诊断是 fare family 问题还是 supply/display/pricing 问题
- **旁路表可复用模式：** 后续遇到类似 BA 的比价过滤问题，可直接复用旁路表方案
- **Coverage 基建对接：** 等 automated brand fare mapping 跑通后，coverage tracking 自动化——手工 audit 时代结束

**Part 2 — H2 Net New：前端展示与辅营的量化支持**

FBU 有方向（并排比较、权益筛选、总成本展示、核心权益前置……）但缺量化和优先级判断。IBU 提供：
- **Void/24h + Service Fee：** 确认 FBU OKR owner（Jessie/Doris），推动进入执行；ABT metrics spec 介入
- **展示方案量化：** 用研发现 → BQ 全量数据验证，帮 FBU 判断"这个问题是 1% 用户还是 30% 用户的问题"，为方案排优先级
- **Pricing：** 方向待定。如果做，聚焦 Type A 内部 price gap（BQ 独立完成，为展示策略提供诊断输入）；目前不确定是否投入

**Part 3 — Communication & Coordination**

- Keep up 现有 cross-BU 沟通节奏（bi-weekly sync、Vivi 联络窗口）
- **近期重点：与 regions 建立定期 sync**（方向待细化——可能从 SEA 或 EU 起步）
- **FBU BI team lead 离职**，新接替人选待宣布——需重新认识并磨合合作模式
- **IPU data engineer head 承诺提升 ETL 支持：** Phase 1 — IBU 自行 data exploration 后要求 copy 到 BQ，次日 deliver；Phase 2 — IPU 帮我们 find 对应数据
- **全公司 AI-driven 优化方向：** 后续项目需尽可能 leverage AI 能力

---

**与 J 1-on-1 更新（2026-07-20）：**
- Q3 OKR 具体内容待进一步讨论
- 近期重点：regional sync 需要尽快完成
- 需与 Jessie 约会 align void/24h 合作与新的 OKR 内容

---

**FBU H2 OKR 参考文档（已获取）：**
- [[FBU H2 Upsell 项目文档]]（Vivi 维护，v2.2, Jul 9）— 整体战略转向："供给侧补货"→"表达侧提效 + 动机侧强化"
- [[Flight User Product Team H2 OKRs]]（丁一团队，Jul 2026）— 前端五个 O，关键 owner：Jessie Li（upsell KR1）、Doris（O2 运卡表达）、孙爽（post-booking/cross-sell）
- [[Non-Lowest-Price Fare Option — User Research Report · UK & SG]]（Jul 2026，n=707）— 用研验证："不值"是 #1 障碍，87% 用户想要 upfront add-on cost estimate

**FBU OKR review 关键发现：**
- Void/24h 在 FBU OKR 中未被显性命名——需确认实际 owner（可能为 Jessie 或 Doris，非孙爽）并 push 进入显性 scope
- 用研数据（flexibility 对 SG 用户重要性、退改规则不可见）是 push void/24h 的新弹药
- FBU 定价竞争力标为"中优先级，悬，往后"——IBU Pricing 分析是否投入待与 J 确认

### Pricing（方向待定，与 J 确认是否 H2 投入）

已集成到 Q3 工作框架 Part 2。核心问题：是否投入 Type A 内部 price gap 分析（BQ 独立完成，为 FBU 展示策略提供诊断输入）。目前 FBU 自身定价竞争力方向标为低优先级。

### Backend Capability：自动化 Brand Fare Mapping（WS1 基础设施）

三阶段推进中：
1. **Scraping（当前阶段）：** 爬取航司官网 fare family + 权益信息；已有一家航司跑通
2. **人工审核整理：** 评估爬取内容可用性，map 到 internal data
3. **Apply：** 正式应用到分析体系和数据源

**关于航线清单：** 已做过 audit 的航司都有 fare family 分类和航线数据，可直接提供给 FBU；按航司产量从高往下覆盖。

---

## 8. Open Blockers

| Blocker | 影响 | Owner |
|---|---|---|
| 孙爽接手后合作模式重新 align | Void/24h 推进节奏、ABT 排期 | Michael + FBU |
| Revenue leakage 量化（fare delta × conversion lift）| Business case 精确数字；对 J 叙事和 FBU 推进均有价值 | Michael |
| Void/24h + service fee 方案方向 | ABT metrics spec 的范围设计 | FBU + J/Michael |
| BA 旁路表 metrics alignment | pre-post 测试设计前置条件 | Michael + FBU |

---

## 9. Next Steps（滚动更新）

**Q3 三部分框架详见 [H2 Active Initiatives → Q3 工作框架](#h2-active-initiatives)。以下是具体待办：**

**Part 1 — H1 Carry-over：Audit 收尾 + 航司排查**
- [x] 11 航司 coverage 全景分析完成（EK/KL/AC/UA/AA/DL/CI/BR/VB/VF/NH/JL）— 2026-07-20
- [x] NH ATPCO brand name 验证 + 五层问题定位完成 — 2026-07-21
- [x] **BR 五层诊断完成 → Closed**（Product Design Ceiling，非 Trip.com 可修复）— 2026-07-21
- [x] **CI 数据基线分析完成**（待官网验证 tier 结构和定价）— 2026-07-21
- [ ] **CI 官网人工走查**（TPE→NRT、TPE→HKG、TPE→LAX，验证四层 fare family 权益和定价）
- [ ] **NH scraper v2 全量运行 → 分析覆盖结果 → 对照 trip.com 数据**（v2 已修通，待 7/22 运行；OW/1pax，+1mo Mon + +3mo Thu 各4天）
- [ ] 旁路表可复用模式：BA 测试稳定后扩展至其他类似情况航司

**Part 2 — Net New：前端展示与辅营的量化支持**
- [ ] **Void/24h owner 确认：** 与 Vivi 确认实际 owner（Jessie/Doris），约 align 会议
- [ ] **用研 → BQ 量化：** 识别可量化的用研 hypothesis（L+Extras 真实成本、flexibility 重视度 vs. 实际购买数据等），输出量级为 FBU 方案排优先级
- [ ] **Pricing 方向：** 与 J 确认是否投入；如投入，从 Type A 内部 price gap 起步
- [ ] **Revenue leakage 量化：** fare delta × conversion lift for EY（对 void/24h business case 仍有价值）

**Part 3 — Communication & Coordination**
- [x] Regional Sync agenda 准备完成（中文版 + 英文版）— 2026-07-23
- [x] Regional Sync 定稿（飞书版本）— 2026-07-23
- [ ] 增强与 region 的 collaboration（方向待细化）

**Ongoing P0（执行跟进，不需主动投入）**
- [x] BA 旁路表 Proposal 完成（2026-07-17）
- [ ] 配置旁路表并上线 → 测试 → 监控
- [x] AirAsia VPL attach rate 分析完成（2026-07-15）
- [ ] **AirAsia VPL coverage 排查（续）：** 与 FBU 数据同事确认 coverage 指标分母定义；用 spot check 结果作为反证（初步结论：分母问题，非真实 supply gap）

**Analytical backlog**
- [ ] Monitor Personalized Ranking ABT 早期结果（Jul 9 上线）
- [ ] Monitor C/F 比价算法 ABT 早期结果（Jul 7 上线）

---

## 10. Stakeholder Map & 沟通模式

| 角色 | 姓名 | 沟通要点 |
|---|---|---|
| IBU Project Sponsor | Serena Wang | 项目背书，H1 review 对象 |
| IBU Project PoC | J Nam | BLUF first，带 hypothesis + 量级估算，不带原始数据 |
| FBU Project PoC | Vivi Ye | FBU 侧产品/前端协调，ABT 排期窗口 |
| FBU Upsell KR Owner | Jessie Li | O2-KR1 Fare Upsell Conversion；void/24h 潜在 owner——近期需约 align 会议 |
| 前端 PM（运卡表达）| Doris Xie | O2 运卡表达提效 |
| 前端 PM（post-booking）| 孙爽 | Post-booking/cross-sell（void/24h 确认不落在其 scope） |
| FBU BI | Team lead 离职，新接替待宣布 | 需重新建立合作模式 |
| IPU Data Engineer | 新 head 承诺 ETL 支持升级 | Phase 1: IBU exploration → BQ copy 次日交付；Phase 2: IPU 主动找数据 |

**J 的标准（始终牢记）：**
1. Needle-mover scale：量化，不只是识别
2. Independent judgment：带 hypothesis 来，不带原始数据
3. BLUF before every update：先说结论，再给数据

**Cross-BU escalation pattern：** 以 mandate + shared OKR 开头；从 junior contact 开始早升级；以一个 scoped question 收尾。

---

## 11. 文档索引

| 文件 | 用途 |
|---|---|
| `PROJECT_CONTEXT.md`（本文件）| 统领性上下文，每次 session 加载并实时更新 |
| `Flight Upsell Project Hub.md` | FBU 侧权威文档（只读参考，不主动维护）|
| `upsell_diagnostic_framework.md` | 五层漏斗详细定义，两类 needle mover，KPI 可比性原则 |
| `void_policy_display_analysis.md` | Void/24h 完整技术 brief：EY 数据、SQL、航司排名 |
| `H1_strategist_narrative.md` | H1 review 口头叙事草稿 |
| `H1_self_evaluation.md` | H1 自评正式草稿（OKR + Leadership Competency）|
| `Strategic Portfolio - Global Flight Fare Upsell Optimization.md` | SLT pitch / CV bullet 用途 |
| `Order.md` / `Order_v2_benefit_fingerprint.md` | 主量化查询逻辑（BQ，MZ + JN merge）|
| `Flight_Upsell_Trial_Log.md` | Session log（Sessions 1–7，through 2026-07-04）|
| `audit/TK/` | TK scraper v1（operational）+ v2（in dev）|
| `scraper/` | 航司官网爬虫：TK（operational）+ NH（开发中）+ JL（占位）|
| `Strategic Framework - Brand Fare Coverage Optimization.md` | Triage & Trigger 方法论：Archetypes、Golden Routes、Ghost Query |
| `H2 priority.md` | H2 战略方向 + Smart Whitelisting / Top-Down Sizing / Natural Demand Ceiling 方法论（归档参考）|
