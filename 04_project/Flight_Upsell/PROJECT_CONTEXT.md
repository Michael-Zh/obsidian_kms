# Flight Upsell — Project Context
_Last updated: 2026-07-15_

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
| WS1 | Supply Coverage | P1 | Ongoing | 40+ 航司 audit 进行中；自动化 Brand Fare Mapping 三阶段推进（当前：Scraping，首家航司跑通）；IBU 需提供航线清单 |
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
- **重要限制：** 1.7M 是上界，FBU display trigger logic 尚未获取，无法确认实际展示量

**FBU 对齐（2026-06-25）：** 确认为 UX 问题，进入 H2 roadmap。
**当前状态（Jul 2026）：** On hold，与 service fee display 联合讨论中。前端负责人已换为**孙爽主导，Doris 辅助**；正在与 FBU 团队重新 align 合作模式。FBU 前端 OKR 据说已定但尚未对外共享。方向：同时展示两项 vs. 跳转详情页（酒店侧 Doris 有先例）。

**Upsell 悖论（EY）：** EY 在错误标签下仍达 79% upsell rate（用户为行李升舱）。修正标签增加退款信号，只会进一步提升。

**Blockers：**
- FBU display trigger logic 未获取（channel / agency / locale 条件下触发规则）——这是把 1.7M 上界转为确认数的关键
- 收益量化（fare delta × conversion lift）尚未完成，H1 叙事缺口仍在
- 新合作模式尚未 align（孙爽接手后需重新建立沟通节奏）

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

### H2 工作框架（Michael）
1. **航司 audit 收尾：** 欧线剩余 + 北美 / 中东 / 日本
2. **FBU H2 计划 review：** FBU 已提交，Michael 需 review 并提 IBU 视角改进建议
3. **FE H2 roadmap 回顾：** IBU 优先级对齐
4. **Pricing 分析框架：** H2 逐步投入，需在 H2 OKR 中占位以保持主动权。方向已初步明确，见下。

### Pricing 分析框架（H2 方向，OKR 待落地）

IBU 定位：**诊断 Pricing 对 upsell 的抑制程度，为 FBU/BD 提供可操作的价格改进建议**（own 诊断和建议，不 own 定价执行）

**三个分析方向：**

**1. 价格竞争力诊断（最近期可交付）**

两类 price gap，性质不同，分开分析：

- **Type A — Upgrade price gap（内部，现在可做）：** 同一条航线上，从低阶运价升一级需要额外付多少？gap 多大用户愿意付，多大就放弃升舱。完全在 BQ 内，不依赖外部数据。这是 upsell 项目最直接相关的定价问题。
- **Type B — Cross-platform price gap（外部，需爬虫/benchmark）：** 同一个 fare（相同 attributes），我们的价格 vs. 竞对/官网。影响的是用户是否选择我们平台，而不是在平台内是否升舱。需要 attribute-based matching 机制，颗粒度建议落在**航司 × 路线类型 × 大市场**。

归因路径（发现 Type B 问题后）：Sourcing 未拿到好价 / 内部加价过高 / GDS/NDC 结构性差异——三者 fix 路径完全不同，归因清楚才能给 BD/FBU 可操作建议。

**2. 价格弹性（H2 中期，WS1 Coverage 有结果后）**
- 不做实验，用 Golden Routes（Coverage 100%）做观测法 Natural Demand Ceiling：price delta 从多少开始 attachment rate 明显下降
- 前提条件：需要 WS1 先输出 Golden Routes 清单，故顺序上在 Coverage 分析之后

**3. Pricing × Coverage 交叉（Secondary check）**
- 顺序诊断：Coverage 补齐后 upsell rate 未按预期提升 → 差值由 Pricing 解释
- 不需要同步分析；目前 Coverage 总体问题不大，此方向暂不优先

**H2 OKR 参考语言：**
- KR1：完成 X 个重点航司的内部 price gap 分析（识别超过弹性阈值的航线/品牌运价组合）
- KR2：建立 Pricing 竞争力基线（vs. 官网/竞对，航司 × 路线类型层面）
- KR3：提出至少 Y 条有明确归因的定价改进建议并提交 FBU/BD review

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
| FBU void/24h display trigger logic | 1.7M 上界→确认数的关键转化 | 孙爽（新负责人） |
| 孙爽接手后合作模式重新 align | Void/24h 推进节奏、ABT 排期 | Michael + FBU |
| Revenue leakage 量化（fare delta × conversion lift）| H1 叙事 [$X] placeholder | Michael |
| Void/24h + service fee 方案方向 | ABT metrics spec 的范围设计 | FBU + J/Michael |
| BA 旁路表 metrics alignment | pre-post 测试设计前置条件 | Michael + FBU |

---

## 9. Next Steps（滚动更新）

**Void/24h（lead finding）**
- [ ] 与孙爽重新 align 合作模式（接手后第一步）
- [ ] 获取 FBU 前端 OKR（据说已定但未对外共享）——确认 void/24h 在 OKR 中的位置
- [ ] Revenue leakage 量化：fare delta × conversion lift for EY；填充 [$X] placeholder
- [ ] FBU display trigger logic：在什么条件下触发？（channel / agency / locale）
- [ ] Void/24h + service fee 联合方案方向确认：一个方案还是两个？影响 ABT metrics spec
- [ ] Track FBU void/24h execution：在 FBU 设计定稿前介入 ABT metrics spec

**旁路表 / BA fare recovery**
- [ ] Metrics + data source alignment（pre-post 测试前置）
- [ ] 决定上线时机，设计 pre-post 测试

**AirAsia Value Pack Lite（P0）**
- [ ] 覆盖率排查：验证 supply 修复完整性
- [ ] 价格排查：竞争力验证
- [ ] Seat selection 价值评估
- [ ] 结合近期连续下滑趋势，评估 Value Pack Lite 对 upsell 恢复的贡献

**Analytical backlog**
- [ ] H1 review narrative：finalize H1_strategist_narrative.md；填充 [$X]
- [ ] Monitor Personalized Ranking ABT 早期结果（Jul 9 上线）
- [ ] Ghost Query rate：建立为 primary diagnostic metric，获取实际 BQ 数字
- [ ] Natural Demand Ceiling：Golden Routes 100% coverage → bag/refund attachment rate baseline
- [ ] Void/24h by market cut：按 market（CN / HK / SG / EN-INT）拆分 misled rate
- [ ] service_fee_type 分布探索（sharpen "misleading label" 叙事）
- [ ] Upgrade step framework（P0/P1 航司：WS, BA, LH, SK）
- [ ] RouteType BQ split for EY / AC
- [ ] Expand airline scope：用 Q3 in void_policy_display_analysis.md 跑剩余 P1/P2 航司

**H2 工作框架**
- [ ] **Pricing H2 OKR 占位：** 确定方向（竞争力诊断为起点），在 HR planning 中落 KR 语言
- [ ] **Pricing 第一步：** 内部 price gap 分析（Eco Basic → Flex，BQ 可做）——不依赖任何外部数据
- [ ] **Brand Fare Mapping scraping 航线清单：** 按航司产量优先级，准备需要 scrape 的航线表格，分批提供给 FBU
- [ ] FBU H2 计划 review（IBU 视角改进建议）
- [ ] FE H2 roadmap 回顾（IBU 优先级对齐）
- [ ] Pricing 分析框架搭建（H2 启动，先定方向）
- [ ] Airline audit 收尾：北美 / 中东 / 日本航司

---

## 10. Stakeholder Map & 沟通模式

| 角色 | 姓名 | 沟通要点 |
|---|---|---|
| IBU Project Sponsor | Serena Wang | 项目背书，H1 review 对象 |
| IBU Project PoC | J Nam | BLUF first，带 hypothesis + 量级估算，不带原始数据 |
| FBU Project PoC | Vivi Ye | FBU 侧产品/前端协调，ABT 排期窗口 |
| 前端 PM (void/24h) | 孙爽（主导），Doris（辅助） | 接手后需重新 align 合作模式；OKR 已定待获取 |

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
| `Strategic Framework - Brand Fare Coverage Optimization.md` | Triage & Trigger 方法论：Archetypes、Golden Routes、Ghost Query |
| `H2 priority.md` | H2 战略方向 + Smart Whitelisting / Top-Down Sizing / Natural Demand Ceiling 方法论（归档参考）|
