# CI (China Airlines) — 五层诊断分析
_分析日期: 2026-07-21 | 状态: 待官网验证_

---

## 1. 数据基线

### Coverage Trace 层

`MZ_coverage_check_for_claude`，近 90 天，Economy (Y)，Intl：

| Brand Tier | Trace量 | Supply Cov | → Selection Cov | Filter Drop |
|---|---|---|---|---|
| Economy Flex | 5.33M | 92.5% | → 46.9% | **−45.6pp** 🔴 |
| Economy Standard | 5.33M | 90.0% | → 85.3% | −4.7pp ✅ |
| Economy Basic | 5.33M | 84.2% | → 82.5% | −1.7pp ✅ |
| Economy Discount | 3.17M | 8.5% 🔴 | → 6.2% | −2.3pp |

### 订单层

`MZ_202606_quantification_v4`，Jan–May 2026：

| Brand Name | 订单量 | 占比 | Upsell Rate |
|---|---|---|---|
| economybasic | 94,459 | 58.3% | 18.7% |
| **NULL（无 brand mapping）** | 31,322 | **19.3%** | — |
| economystandard | 21,373 | 13.2% | 29.9% |
| economyflex | 9,644 | 6.0% | 28.7% |
| economydiscount | 5,263 | 3.2% | 14.3% |

**CI 全局 Upsell Rate: 19.7%**（399K 总订单，75K upsell 订单）——比 BR 的 21.1% 还低。

**CI 的 Data Foundation 比 BR 健康得多：** NULL 仅 19.3%（BR 是 74.7%），五个 tier 全部在订单表中有对应记录。upsell rate 19.7% 是真实的、可分析的。

---

## 2. 五层漏斗排查

### 2.1 Data Foundation — ATPCO Brand Mapping ⚠️

| 订单 brand_name | 订单量 | 对应 Coverage Tier | 状态 |
|---|---|---|---|
| economybasic | 94,459 (58.3%) | Economy Basic | ✅ 清晰 |
| NULL | 31,322 (19.3%) | — | ⚠️ 偏高水平但可接受 |
| economystandard | 21,373 (13.2%) | Economy Standard | ✅ 清晰 |
| economyflex | 9,644 (6.0%) | Economy Flex | ✅ 清晰 |
| economydiscount | 5,263 (3.2%) | Economy Discount | ✅ 清晰但量小 |

**对比 BR：CI 的 brand mapping 完整性不是一个量级。** BR 74.7% NULL，CI 仅 19.3%。CI 的五层问题不始于 Data Foundation。

**Discount 在 coverage 中仅 8.5%，但订单表中实际存在。** 3.17M traces 只有 8.5% supply，但 5,263 单订单分布在 TW-JP、TW-PH、TW-TH 等所有主要航线——Discount 是真实产品，只是 mapping 覆盖率极低，类似 NH Light 的 `officialbrandname=NULL` 问题。

#### NULL 订单 Attributes 画像

| Baggage | NULL 订单 | Flexibility | NULL 订单 |
|---|---|---|---|
| 4.fare+carry on+checkin | 99.1% | 4.Flexible | 80.7% |
| 1.fare only | 0.7% | 2.Change Only | 14.6% |
| — | — | 1.Not Flexible | 3.1% |

| Cancel × Change Policy | NULL 订单 |
|---|---|
| paid_cancel + paid_change | 76.8% |
| no_cancel + paid_change | 16.0% |
| no_cancel + no_change | 3.2% |

**结论：和 BR 一样，NULL 订单就是 unmapped Basic/Standard/Flex，不是 Discount。** 但 CI 的 NULL 率（19.3%）远低于 BR（74.7%），所以对分析的影响小得多。

---

### 2.2 Supply — 航线覆盖分析

#### 全局方向汇总：

| Brand Tier | TW→ | →TW | 非TW |
|---|---|---|---|
| Economy Basic | 83.2% | 83.7% | 87.2% |
| Economy Standard | 88.1% | 91.1% | 91.5% |
| Economy Flex | 89.6% | 93.8% | 92.3% |
| Economy Discount | 8.2% | 6.3% | 3.0% |

Supply 在所有方向和 tier 上基本健康（83-94%），没有方向性限制——和 BR 一样，单一 TPE hub。Discount 的 supply 极低是全局性的。

#### Flex 的比价过滤：全局性严重

| 航线 | Flex Supply | → Selection | Filter Drop |
|---|---|---|---|
| TW→JP | 90.7% | → 45.8% | **−44.9pp** 🔴 |
| TW→TH | 99.2% | → 39.8% | **−59.4pp** 🔴 |
| HK→TW | 88.1% | → 32.1% | **−56.0pp** 🔴 |
| TH→TW | 98.6% | → 41.5% | **−57.1pp** 🔴 |
| SG→TW | 96.9% | → 30.1% | **−66.8pp** 🔴 |
| MY→TW | 96.2% | → 28.7% | **−67.5pp** 🔴 |
| KR→TW | 96.9% | → 82.7% | **−14.2pp** ✅ |
| JP→TH | 96.0% | → 78.6% | −17.4pp ✅ |
| JP→VN | 96.8% | → 80.4% | −16.4pp ✅ |
| JP→ID | 96.6% | → 71.5% | −25.1pp |

**Flex 的过滤模式很清晰：**
- TW 相关航线（TW→XX、XX→TW）：Flex filter drop 40-68pp —— 严重
- 日→东南亚中转航线（JP→TH/VN/ID）：Flex filter drop 14-25pp —— 相对健康
- KR→TW 又是例外（−14.2pp），和 BR 的 KR→TW Up −10.9pp 是同一模式

#### Standard 的过滤：方向性分明

| 航线 | Standard Supply | → Selection | Filter Drop |
|---|---|---|---|
| TW→JP | 89.6% | → 93.5% | **+3.9pp** ✅ |
| TW→TH | 97.8% | → 97.2% | −0.6pp ✅ |
| HK→TW | 87.6% | → 95.0% | **+7.4pp** ✅ |
| TH→TW | 96.4% | → 95.9% | −0.5pp ✅ |
| **TW→AU** 🔴 | 91.7% | → 45.6% | **−46.1pp** |
| **TW→US** 🔴 | 87.6% | → 34.6% | **−53.0pp** |
| **TW→GB** 🔴 | 89.0% | → 43.4% | **−45.6pp** |
| **TW→CA** 🔴 | 89.8% | → 32.2% | **−57.6pp** |
| 中转长线 | 88-96% | → 25-49% | −40~70pp |

**Standard 和 BR 完全一样的 pattern：亚洲区域线健康，长航线+中转线严重过滤。**

---

### 2.3 Fare Selection — 比价过滤 🔴

**Flex 是 CI 五层中最严重的问题。** 模式与 BR 的 Up 完全一致：

| 对比 | CI Flex | BR Up |
|---|---|---|
| 全局 filter drop | −45.6pp | −48.5pp |
| TW→JP drop | −44.9pp | −49.2pp |
| HK→TW drop | −56.0pp | −56.9pp |
| KR→TW drop | **−14.2pp** ✅ | **−10.9pp** ✅ |
| JP→SEA 中转 drop | −14~25pp | — |

**台湾航司的高端 tier 在 Trip.com 比价系统中的劣势是跨航司的结构性问题。** CI Flex 和 BR Up 的过滤模式几乎完全一致，KR→TW 同时是两个航司的例外。

---

### 2.4 Ranking — 待官网验证后判断

**和 BR 的关键区别：CI 的 Standard 订单占比 13.2%，是 BR（5.3%）的 2.5 倍。** 这暗示 CI 的升舱经济学可能比 BR 更合理。

但需要官网验证：
- Standard vs Basic 的价格差是多少？
- 权益差异在哪——行李？里程？退改？
- Flex 的价格差是多少？

**Flex 有 24.1% 的 free_change 率**（2,320/9,630），这是一个强烈的区分信号——可以从 NULL 订单中识别 Flex。

---

### 2.5 Display — 待验证

- **Void/24h：** CI 不受 void/24h 限制（仅 25 单，0.006%）。✅
- **权益差异展示：** 待官网验证。Basic vs Standard vs Flex 的权益差异是否在运卡上清晰可见？

---

## 3. CI 官网 Fare Family 结构（待人工验证）

### 需要确认的航线：

| 优先 | 航线 | 订单量 | 为什么要查 |
|---|---|---|---|
| 1 | **TPE→NRT（台北→东京）** | 51K | CI 最大航线，验证四层 tier 结构和定价 |
| 2 | **TPE→HKG（台北→香港）** | 16K | 短途对照 |
| 3 | **TPE→LAX/SFO（台北→洛杉矶）** | — | 长航线，验证 Standard −53pp 的根因——是定价过高吗？ |

### 重点验证：

1. Discount/Basic/Standard/Flex 四层的完整权益表——尤其行李件数、里程累积率、退改费用
2. TPE→NRT 的实际价格——Basic → Standard → Flex 的价格差
3. 长航线上 Standard 和 Basic 的价格差——是否和 BR 一样 +50%？
4. Flex 的权益差异——免费改签？额外行李？里程？
5. 行李规则：是否全 tier 含托运？（BQ 数据 99% 含托运，暗示全 tier 标配）

---

## 4. 五层总结与优先级

| 层 | 发现 | 严重度 | 可操作性 |
|---|---|---|---|
| **Data Foundation** | ⚠️ 19.3% NULL + Discount 8.5% supply | 中等 | 高——mapping 修复可解决 |
| **Supply** | ✅ 全 tier 83-94%，健康；Discount 除外 | 轻微 | — |
| **Fare Selection** | 🔴 Flex −45.6pp（全局）+ Standard 长线 −40~70pp | **严重** | 中——需验证定价是否合理 |
| **Ranking** | ❓ Standard 订单 13.2%（BR 的 2.5x），可能定价更合理 | **待官网验证** | — |
| **Display** | ✅ 不受 void/24h；❓ 权益展示待验证 | 待验证 | — |

### CI vs BR vs NH 对比

| 维度 | NH | BR | CI |
|---|---|---|---|
| 订单量 | ~145K | ~485K | **~399K** |
| Upsell Rate | 需查 | 21.1% | **19.7%** |
| NULL brand_name | 37% | 74.7% | **19.3%** |
| 核心瓶颈 | Ranking + Display | Product Design | **待官网验证（可能介于两者之间）** |
| 高端 tier 过滤 | Full Flex −79pp | Up −48.5pp | **Flex −45.6pp** |
| Standard 订单占比 | 5.6% | 5.3% | **13.2%** |
| Product Design 风险 | 低（NH 价格差合理） | 高（+50% 价差） | **中等——Standard 订单占比更高，暗示价差可能更合理** |

**CI 是 NH 和 BR 之间的一个中间态：** Data Foundation 比 BR 好得多，Standard 订单占比更高，但 Flex 的比价过滤和 BR Up 一样严重。官网验证后可以判断是更接近 NH（Trip.com 可修复）还是 BR（Product Design Ceiling）。
