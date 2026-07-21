---
title: "Regional Sync Agenda — Upsell Q3"
created: 2026-07-20
updated: 2026-07-21
purpose: Global PGM & market sync — project update and regional collaboration
---
# ABT & product update (5–10 min)

**已全量上线：**
- **Quick Filter（行李筛选）** — Jul 2，App 端 100% 全量
    - 特别感谢 Peam 之前提出的想法，并帮助我们一起向 FBU 推进落实——这是一个非常成功的合作案例
- **Full Change/Refund Cost Display** — Jul 3，App 端全量；展示总退改费用（服务费 + 航司罚金 + 代理费）

### 当前 Active ABTs

| ABT                                       | 上线时间   | 内容                                 |
| ----------------------------------------- | ------ | ---------------------------------- |
| C/F 比价算法                                  | Jul 7  | 与 Y/W 逻辑一致，扩展至 C/F 舱               |
| Personalized Ranking                      | Jul 9  | 按用户购买概率排序；当前 16% traffic，预计扩大至 30% |
| Web Middle Page Vertical Redesign Phase 1 | Jul 11 | 竖向 slide-out 布局                    |
| Compact Itinerary V2                      | Jul 22 | 允许有查看航班细节的顾客主动查看细节，没有需要的可以跳过       |

### 我们需要 region 的支持
- 分享你的想法和竞争对手的 inspiration
- **航司 / 市场特殊情况：** 如果你们知道某个航司或市场有我们不一定掌握的情况，随时 flag

---

# Audit update: 24h free cancellation display

### Step 1 — 在前端走查中发现问题

（截图）

**问题表现：** "24 小时免费退"标签覆盖了 24 小时后的长期退款政策，导致用户误以为自己有退票保障，或无法区分不同运价之间的差异，从而失去升舱的动机。

### Step 2 — 寻找数据源，了解问题原因，量化影响范围

机票后端存在两种相关政策：
- **24h 免费退**（对客）：用户购票后 24 小时内可免费取消
- **Void 政策**（对商）：agent 定错票后 24 小时内可免费更正

两者互斥，不同时存在。不同航司的占比差异较大——总体而言 void 占比更高，24h 免费退占比较小（EY / AA / DL 等为例外）。

Trip 在 US/BR/KR 市场将 void 这一对商政策包装为 USP 展示给用户。24小时免费退则在全球市场都展示。无论哪种政策，中间页均以"24 小时免费取消"标签展示，**覆盖了 24 小时窗口之后的长期退款政策**——即使该机票实际不可退款，用户看到的退改信息并不完整。

通过历史订单分析，影响约**全球 11% 的订单**：
- 以 EY 为例：近 90% 有此标记的订单，实际票为不可退票
- UA、DL、AA、BA、AC 等主要 FSC 均有发现——是系统性逻辑问题，不是个别航司问题

### Step 3 — 量化分析推动 FBU 对齐，进入 H2 roadmap

IBU 带着量化分析与 FBU align 后，**FBU 确认这是对用户不友好的展示体验**，具体修复方案将进入 FBU H2 roadmap 讨论。IBU 将在 H2 持续跟进修复方案的落地与 ABT 设计。

这是 IBU 作为 **Insight Engine** 的定位——主动发现系统性盲点，量化业务影响，推动高 impact 问题的解决方案落地。