# Pricing Analysis Framework
_Created: 2026-07-15 | Owner: Michael Zhang_

> IBU 定位：**诊断 Pricing 对 upsell 的抑制程度，为 FBU/BD 提供可操作的价格改进建议**
> Own 诊断和建议，不 own 定价执行。

---

## 核心问题

当 upsell rate 偏低时，Pricing 是可能的原因之一。但在 Pricing 方向投入深度分析之前，需要先确认：**哪一类 Pricing 问题对我们的影响最大？** 这是目前最缺的一块。

---

## 第一步：Screening Pass（优先执行）

在深入任何一个方向之前，先做一次**快速分布扫描**，识别哪个问题最值得 deep dive。

**方法：**
- 维度：升级价差（Eco Basic → Flex/Full）× upsell rate
- 数据源：BQ 内部数据，不依赖外部
- 目标航司：AirAsia 或 EY（量大、数据基础好）

**期待输出：**
- 价差分布图：当升级价差落在哪个区间时，upsell rate 开始显著下降？
- 是否存在明显的"cliff"——某个价格点之后 attachment rate 断崖？
- 哪条航线/市场组合的价差最极端（潜在问题最大）？

**判断逻辑：**
- 如果看到明显 cliff + 大量高价差订单 → Type A 问题显著，值得 deep dive
- 如果价差分布合理但 upsell rate 仍偏低 → Pricing 可能不是主因，问题在 Supply/Display
- 如果发现平台间明显价差 → 触发 Type B 调查

---

## 三类 Pricing 问题（性质不同，分开分析）

### Type A — Upgrade Price Gap（升级价差）
**本质：** 用户在同一平台内，从低阶运价升级到高阶运价需要额外付多少钱？

- **数据来源：** 完全在 BQ 内，不依赖外部数据
- **分析方法：** 计算各航线 Eco Basic → Eco Standard → Eco Flex 的价差分布；与 upsell rate 做交叉
- **核心问题：** gap 多大用户愿意升舱，多大就放弃？
- **影响机制：** 直接影响"用户是否选择更高运价"——是 upsell 项目最直接相关的定价问题
- **可操作性：** 高（可识别哪些航线/舱位组合的价差过高，建议 BD 与航司谈判）
- **H2 优先级：** P1，可立即启动

### Type B — Cross-Platform Price Gap（跨平台价格差）
**本质：** 同一个 fare（相同 attributes），我们的价格 vs. 竞对（OTA）/ 航司官网。

- **数据来源：** 需要爬虫或 benchmark 数据（外部），颗粒度：航司 × 路线类型 × 大市场
- **分析方法：** Attribute-based matching（相同出发/到达/日期/舱位属性下比价）
- **核心问题：** 我们是否因为价格偏高而失去选择我们平台的用户？
- **影响机制：** 影响"用户是否选择 Trip 平台"，而非平台内升舱行为——本质是平台竞争力问题
- **归因路径（发现 Type B 问题后必须做）：**
  1. **Sourcing 没拿到好价**（航司 NDC/GDS 结构性问题）→ fix owner: BD/供应团队
  2. **内部加价过高**（Trip 自身 markup policy）→ fix owner: Revenue/Pricing team
  3. **GDS/NDC 结构性差异**（非我方可控）→ fix owner: 技术/对接层
  - 三条路径的 fix 方式完全不同，**归因清楚才能给可操作建议**
- **可操作性：** 中（依赖外部数据，且归因链条长）
- **H2 优先级：** P2，需要 scraper 基础设施支持

### Type C — Price Elasticity（价格弹性）
**本质：** 在 Coverage 完整的情况下，用户对 bag/refund 等属性的支付意愿上限在哪里？

- **数据来源：** BQ 内部（Golden Routes，Coverage = 100% 的航线）
- **分析方法：** 观测法 Natural Demand Ceiling——非实验设计，用"纯净环境"近似弹性曲线
  - Golden Routes 上，按 price delta 分桶，观察 bag/refund attachment rate 变化
  - 找到 attachment rate 开始明显下降的价差节点 → 这是"弹性阈值"
- **核心问题：** 用户 want it（有需求），但 willing to pay 的上限在哪？
- **影响机制：** 为 Type A 分析提供基准线；判断哪些路线的价差已超过弹性阈值
- **前提条件：** 需要 WS1 先输出 Golden Routes 清单（Coverage 100% 的航线），顺序在 Type A 之后
- **可操作性：** 高（为所有 pricing 建议提供"是否值得付"的证据基础）
- **H2 优先级：** P2，依赖 WS1 先交付

---

## 三类问题的关系

```
Screening Pass
    ↓
Type A (升级价差)  ←→  Type C (弹性阈值作为 Type A 的基准线)
    ↓（发现平台价格偏高时触发）
Type B (跨平台差)
    ↓
归因：Sourcing / Markup / GDS结构
```

- **Type A + C** 是一对：A 发现问题，C 提供"合理价差上限"的判断基准
- **Type B** 是独立分支：需要外部数据，影响的是平台竞争力而非升舱行为
- **Screening** 是前置步骤：决定先做 A 还是先做 B

---

## Benefit Tier 划分（Screening 前置分类）

价差本身不是完整信号，需要控制"升级买到了什么"才能隔离 Pricing 效果。

| Tier | 权益增量 | 优先级 |
|---|---|---|
| Tier 1 | 仅增加 refundability（无行李变化） | ✅ 纳入分析 |
| Tier 2 | 增加 bag + refundability | ✅ 纳入分析 |
| Tier 3 | 增加 bag + seat + refundability | 作为 X factor，附加分析 |

**Tier 3 备注：** Seat selection 的重要性因市场而异。
- LCC 主导市场（如 AirAsia）：seats 权益权重高
- 其他市场：Priority Boarding / 餐食可能更重要
→ Tier 3 作为灵活选项，按市场单独评估，不纳入主线 Screening

**Benefit 数据前提（待确认）：**
- BQ 里 fare benefit attributes 是结构化字段（可直接 query）？还是存在人工 mapping 表里需要 JOIN？
- Compliance 航司的 benefit 字段可信度最高（前端只展示官方运价 → 与航司官网一致）

---

## Compliance 市场作为 Benchmark

**为什么干净：** Trip 在 Compliance 市场只在前端展示官方运价（BQ 里仍有多种运价，但前端只出官方）。Supply 干净、Coverage 不是变量 → 观察到的价差/转化关系基本可归因为 Pricing 信号本身，天然控制了 Supply/Coverage 噪音。

**两种用途：**
1. **市场内横向：** 同一市场内，用 Compliance 航司的价差/upsell rate 作为基线，对比非 Compliance 航司的表现差距 → 差值指向 Display/Ranking/Pricing 问题
2. **航线类型横向：** 用 LH（欧洲长途）、CX（亚太长途）、AA/DL（北美）等建立各航线类型的通用基准，judge 同类型其他航线表现

---

## 转化率计算方法（方法论待解决）

**核心问题：分母是什么？**

| 数据条件 | 分母 | 结论强度 |
|---|---|---|
| 有 display/impression 数据（用户看到了哪些运价、对应价差）| 该价差被展示的 session 数 | 强：可以说"价差超过 $X 时 upsell rate 下降" |
| 只有 order 数据 | 该航线全部订单数（近似） | 弱：只能说"价差大的 fare 组合里，选高阶的比例更低" |

**⚠️ 待确认（数据探索 Action Item）：**
- BQ 里是否有前端 display/impression 层数据？（用户进入中间页时，展示了哪些运价、对应价格）
- 具体可用性需 Michael 数据探索后确认

---

## H2 OKR 参考语言

- **KR1：** 完成 X 个重点航司的内部 price gap 分析（Type A），识别超过弹性阈值的航线/品牌运价组合
- **KR2：** 建立 Pricing 竞争力基线（Type B vs. 官网/竞对，航司 × 路线类型层面）
- **KR3：** 提出至少 Y 条有明确归因的定价改进建议并提交 FBU/BD review

---

## 当前状态

| 步骤 | 状态 | 下一步 |
|---|---|---|
| Screening Pass | ❌ 未启动 | 选 AirAsia 或 EY，BQ 跑价差 × upsell rate 分布 |
| Type A 深度分析 | ❌ 未启动 | Screening 完成后决定是否值得 |
| Type B 平台比价 | ❌ 未启动 | 需要 scraper 支持；H2 OKR 占位先 |
| Type C 弹性分析 | ❌ 未启动 | 依赖 WS1 Golden Routes 交付 |
| H2 OKR 占位 | ❌ 待落地 | 在 HR planning 中确认 KR 语言 |
