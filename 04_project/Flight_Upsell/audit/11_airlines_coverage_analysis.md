# 11 Airlines Brand Fare Coverage Analysis
_Data snapshot: 2026-07-20 | BQ table: `MZ_coverage_check_for_claude` | Window: last 90 days | Class: Economy (Y)_

> **Purpose:** 为人工走查和航司官网校验提供数据基线。每航司拆解为 supply coverage（品牌运价映射端）和 selection coverage（比价后可见端）两个口径。

---

## 1. Executive Summary

| 优先级 | #   | 航司     | 国际线 Trace量 | Supply Cov | Selection Cov | Filter Drop | 核心问题                          |
| --- | --- | ------ | ---------- | ---------- | ------------- | ----------- | ------------------------------ |
| **P0** | 11 | **NH** | 3.8M       | 81.7%      | 45.4%         | −36.3pp     | 🔴 6层最复杂 + Full Flex **11.6%** + Flex supply 56.2% |
| **P0** | 3  | **BR** | 9.7M       | 78.5%      | 52.4%         | −26.1pp     | 🔴 Discount **0%** + Up −77pp + upsell rate 偏低 |
| **P1** | 4  | **AA** | 0.7M       | 57.6%      | 48.2%         | −9.4pp      | 🔴🔴 Supply 全 tier <78%，JP-US 近乎 0% |
| **P1** | 6  | **CI** | 9.4M       | 76.5%      | 54.4%         | −22.1pp     | 🔴 Discount 10.8% + Flex −69pp |
| **P1** | 9  | **JL** | 1.3M       | 88.7%      | 51.8%         | −36.9pp     | Flex **−69pp** + ATPCO name 脏数据 |
| **P1** | 7  | **VF** | 2.7M       | 98.3%      | 79.1%         | −19.2pp     | Supply 完美，但 Flex −43pp + Ecojet Dom −95pp |
| **P2** | 1  | **EK** | 10.5M      | 76.3%      | 47.7%         | −28.6pp     | Special 41.5% + Flex Plus −66pp |
| **P2** | 5  | **AC** | 3.8M       | 83.4%      | 53.3%         | −30.1pp     | Latitude **4.4%** |
| **P2** | 8  | **UA** | 2.1M       | 79.2%      | 61.1%         | −18.1pp     | Plus **1.9%** + Fully Refundable −38pp |
| **P2** | 10 | **DL** | 1.9M       | 77.7%      | 54.2%         | −23.5pp     | Comfort tiers <15% |
| Ref | 2  | **KL** | 0.9M       | 94.6%      | 92.1%         | −2.5pp      | 🏆 WS5 Compliance 标杆 |
| Ref | 12 | **VB** | 0.08M      | 77.6%      | 71.7%         | −5.9pp      | ✅ NDC 接入，整体健康 |

**诊断框架映射到五层漏斗：**
- **Data Foundation → Supply** 问题：AA、BR、CI、EK（brand mapping 不完整）
- **Fare Selection** 问题：VF、JL、NH、AC、UA、DL（比价过滤大量高端 tier）
- **KL** 是 WS5 Airline Compliance 强制效果，不是系统自然表现

---

## 2. Five-Layer Funnel Matrix

> 行按走查优先级排列：**P0（NH、BR）→ P1 → P2 → Reference**。数据覆盖范围：本次 BQ 查询可观测 **Data Foundation**、**Supply**、**Fare Selection** 三层。**Ranking** 和 **Display** 层仅标注已知信息，需额外数据源验证。

### P0 — 头号优先

| 航司        | Data Foundation<br>（ATPCO brand mapping）                                                                                 | Supply<br>（运价爬取/对接覆盖）                                                               | Fare Selection<br>（比价过滤）                                                      | Ranking<br>（排序位置）                                     | Display<br>（前端展示）                        | 优先级理由                                                                |
| --------- | ------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ----------------------------------------------------- | ---------------------------------------- | -------------------------------------------------------------------- |
| **NH** 🔴 | 6 层映射，最复杂<br>4 套独立 fare family<br>🔴 Light `officialbrandname=NULL`<br>导致 coverage trace 缺失<br>🔴 37% 订单 atpco name NULL | ✅ 方向性限制确认<br>Flex 56.2% = 回程稀释假象<br>JP→XX Flex 83-98%<br>⚠ JP→Americas Value 64-71% | ⚠ CN→JP Standard −60.7pp<br>其余方向 0-15pp 可接受<br>Full Flex −79pp 部分合理<br>（定价过高） | ❓ 核心谜题<br>Standard 定价合理<br>但订单仅 5.6%<br>→ 90% 可能是排序问题 | ❓ 权益差异展示？<br>退改政策可见？<br>不受 void/24h 限制 ✅ | 排查完毕。<br>核心假设：瓶颈<br>在 Ranking + Display<br>而非 Supply                 |
| **BR** 🔴 | 四层映射（Discount/Basic/Standard/Up）                                                                                         | 🔴🔴 Discount **0%**（949K traces 全局无映射）<br>其余 82-90%                                | 🔴 Up −77.1pp（仅 13.2%）<br>Basic/Standard −1~11pp 可接受                          | 待验证                                                   | 待验证                                      | 体量大（9.7M traces）、upsell rate 偏低可能受 fare family 结构决定、Coverage 有明显 gap |

### P1 — 有明显问题但影响范围或复杂度略低

| 航司 | Data Foundation<br>（ATPCO brand mapping） | Supply<br>（运价爬取/对接覆盖） | Fare Selection<br>（比价过滤） | Ranking<br>（排序位置） | Display<br>（前端展示） |
|---|---|---|---|---|---|
| **AA** 🔴🔴 | 三层映射（Basic Economy/Main Cabin/Main Plus） | 🔴🔴 全 tier 38-77%<br>JP-US Basic 仅 0.9%<br>Main Cabin 仅 37%<br>国际线总量 0.7M 偏低（vs UA 2.1M） | Main Plus −20.2pp<br>Basic/Main Cabin −3~6pp ✅<br>（selection 问题轻但 supply 极差） | 待验证 | 待验证 |
| **CI** 🔴 | 四层映射（Discount/Basic/Standard/Flex） | 🔴 Discount 仅 10.8%（接近缺失）<br>其余 85-93% | 🔴 Flex −68.9pp<br>Basic/Standard −1~8pp ✅<br>HK-TW Flex 仅 4.8% | 待验证 | 待验证 |
| **JL** ⚠️ | 有脏数据：`Economy Flex` vs `Economy  Flex` 空格重复 | 无大问题<br>Flex 87.6%, Semi Flex 87.7%, Special 93% | 🔴 Flex −69pp（JP-VN 仅 0.2%）<br>Semi Flex −13pp<br>Special −3pp ✅ | 待验证 | 待验证 |
| **VF** ⚠️ | 无问题 | 无问题<br>97-99% 全 tier，820+ CPs | 🔴 Flex Intl −43pp<br>🔴 Flex Dom −35.5pp<br>🔴 Ecojet Dom −95pp<br>仅 Basic 健康（−1~8pp） | 待验证 | 待验证 |

### P2 — 混合问题，部分 tier 健康

| 航司 | Data Foundation<br>（ATPCO brand mapping） | Supply<br>（运价爬取/对接覆盖） | Fare Selection<br>（比价过滤） | Ranking<br>（排序位置） | Display<br>（前端展示） |
|---|---|---|---|---|---|
| **EK** ⚠️ | 四层映射（Special/Saver/Flex/Flex Plus） | 🔴 Special 仅 41.5%<br>Saver 74.3%<br>Flex/Flex Plus 93-94% | 🔴 Flex Plus −66.2pp<br>Flex −30.9pp<br>Saver −2.6pp ✅<br>FR-AE Flex Plus 仅 3.3% | 待验证 | 待验证 |
| **AC** ⚠️ | 五层映射完整（Basic/Standard/Flex/Comfort/Latitude） | Basic 仅 61.4%<br>其余 83-90% | 🔴 Latitude −78.6pp（仅 4.4%）<br>🔴 Flex −39.8pp<br>Standard/Comfort −2.5~14.7pp 可接受<br>JP-CA Latitude 仅 2.7% | 待验证 | 待验证 |
| **UA** ⚠️ | 四层映射完整 | 🔴 Economy Plus 仅 48.6%（87 CPs vs 其他 tier 670+ CPs）<br>Basic 71.7%<br>Economy/Fully Refundable 85% | 🔴 Fully Refundable −38pp<br>🔴 Plus −46.7pp（仅 1.9%）<br>Basic/Economy −1~6pp ✅<br>HK-US Fully Refundable 仅 2.9% | 待验证 | 待验证 |
| **DL** ⚠️ | 五层映射完整 | Comfort Classic 62.2% 偏低<br>其余 71-91% | 🔴 Comfort Classic −51.5pp<br>🔴 Comfort Extra −57pp<br>Main 系列 −6~7pp ✅<br>JP-US 方向 Comfort Extra 仅 4.3% | 待验证 | 待验证 |

### Reference — 无明显问题

| 航司 | Data Foundation<br>（ATPCO brand mapping） | Supply<br>（运价爬取/对接覆盖） | Fare Selection<br>（比价过滤） | Ranking<br>（排序位置） | Display<br>（前端展示） |
|---|---|---|---|---|---|
| **KL** ✅ | 三层映射完整，brand name 干净 | 94-95% 全 tier 覆盖<br>3,700+ CPs，19,000+ ODs | −1~5pp，几乎无过滤<br>Flex 最差也仅 −4.6pp | 待验证 | ✅ WS5 Strict Fare Display Compliance 强制<br>全量品牌运价展示 |
| **VB** ✅ | 四层映射完整（Zero/Smart/Switch Carry On/Switch Checked） | 74-94% 全 tier<br>US-MX 为主 | −1~15pp，整体健康<br>国际线更优 | 待验证 | 待验证（NDC 接入可能是良好表现的原因） |

**各层已知信息汇总：**

- **Data Foundation：** 本次分析可观测 brand name mapping 质量。JL 有空格的脏数据；NH 6 层 tier 最复杂。更深入的 ATPCO → 官网 → internal name 三层映射准确性需人工走查验证。
- **Supply：** 本次分析核心层。通过 `supply_cov_pct` 观测。11 家中 AA/BR/CI/EK/UA/AC/NH 共 7 家有不同程度 supply gap。
- **Fare Selection：** 本次分析核心层。通过 `filter_drop_pp`（supply cov − selection cov）观测。除 KL/VB 外，9 家均有高端 tier 比价过滤问题。**共同规律：最低 tier 永远健康，越高端 drop 越大。**
- **Ranking：** 本次 BQ 查询未覆盖。需要从 FBU ranking ABT 数据或其他数据源获取。已知个性化 ranking ABT（Jul 9 上线）可能改变高端 tier 的展示位置。
- **Display：** 本次 BQ 查询未覆盖。已知 KL 有 WS5 Compliance 强制展示全部品牌运价。Void/24h display override 见 `void_policy_display_analysis.md`。

---

## 3. Per-Airline Brand-Level Detail

### 2.1 EK — Emirates

| Brand Tier | Trace量 | Supply Cov | → Selection Cov | Filter Drop | CP数 | OD数 |
|---|---|---|---|---|---|---|
| Flex Plus | 2.69M | **94.1%** | → 27.9% | **−66.2pp** 🔴 | 9,300 | 42,824 |
| Flex | 2.69M | **93.1%** | → 62.1% | −30.9pp | 9,261 | 42,630 |
| Saver | 2.64M | 74.3% | → 71.6% | −2.6pp | 7,896 | 35,015 |
| Special | 2.51M | **41.5%** 🔴 | → 28.1% | −13.4pp | 6,492 | 24,146 |

**Top 5 国际 Country Pairs → Flex Plus 的 filter drop：**
| CP | Traces | Flex Plus Cov | Flex Plus Sel | Drop |
|---|---|---|---|---|
| TH-HK | 485K | 87.7% → 14.7% | −73.0pp |
| HK-TH | 329K | 89.7% → 40.9% | −48.7pp |
| GB-AE | 248K | 96.3% → 6.2% | −90.1pp |
| FR-AE | 179K | 99.8% → 3.3% | −96.5pp |
| SA-ID | 161K | 97.0% → 17.5% | −79.5pp |

**诊断：** Supply 侧 Special 仅 41.5%——最大 mapping gap；Flex Plus supply 高但 selection 被比价大幅过滤（最高 −96.5pp）。EK 需要查官网明确 fare family 结构（Special/Saver/Flex/Flex Plus 四层）。

---

### 2.2 BR — EVA Air

| Brand Tier | Trace量 | Supply Cov | → Selection Cov | Filter Drop | CP数 | OD数 |
|---|---|---|---|---|---|---|
| Basic | 2.90M | 82.5% | → 83.9% | +1.4pp | 1,311 | 9,919 |
| Standard | 2.90M | **88.4%** | → 77.0% | −11.4pp | 1,356 | 10,112 |
| Up | 2.90M | **90.3%** | → 13.2% | **−77.1pp** 🔴 | 1,360 | 10,104 |
| Discount | 0.95M | **0.0%** 🔴🔴 | → 0.0% | 0.0pp | 24 | 50 |

**Top 5 CPs → Discount 全部 0%：**
| CP | Traces | Discount Supply |
|---|---|---|
| TW-JP | 1.49M | 0.1% |
| TW-CN | 770K | 0.0% |
| TW-MO | 690K | 0.0% |
| TW-KR | 652K | 0.0% |
| TW-TH | 531K | 0.0% |

**诊断：** Discount 是全局 0%——不是航线问题而是 brand mapping 从未建立。Up 的 selection drop −77pp 与 CI Flex 类似（高端 tier 比价过滤）。BR 人工走查重点：确认 Economy Discount 是否真实存在（官网），以及 Up tier 的权益差异。

---

### 2.3 CI — China Airlines

| Brand Tier | Trace量 | Supply Cov | → Selection Cov | Filter Drop | CP数 | OD数 |
|---|---|---|---|---|---|---|
| Standard | 2.62M | **90.5%** | → 82.7% | −7.8pp | 745 | 5,623 |
| Flex | 2.62M | **92.5%** | → 23.5% | **−68.9pp** 🔴 | 756 | 5,640 |
| Basic | 2.62M | 85.6% | → 84.4% | −1.2pp | 750 | 5,510 |
| Discount | 1.55M | **10.8%** 🔴 | → 8.0% | −2.8pp | 87 | 278 |

**Top 5 CPs → Flex 的 filter drop：**
| CP | Traces | Flex Supply → Sel | Drop |
|---|---|---|---|
| TW-JP | 2.10M | 92.1% → 23.5% | −68.6pp |
| TW-KR | 741K | 91.7% → 52.1% | −39.6pp |
| HK-TW | 690K | 86.9% → 4.8% | −82.1pp |
| TW-TH | 675K | 98.9% → 7.1% | −91.8pp |
| TW-CN | 664K | 88.4% → 36.9% | −51.5pp |

**诊断：** Discount 仅 10.8%，基本缺失。Flex supply 高（92.5%）但比价后跌至 23.5%。HK-TW、TW-TH 方向 Flex 几乎不可见（<8%）。走查重点：官网 Discount tier 的具体命名和权益。

---

### 2.4 AC — Air Canada

| Brand Tier | Trace量 | Supply Cov | → Selection Cov | Filter Drop | CP数 | OD数 |
|---|---|---|---|---|---|---|
| Standard | 823K | 89.9% | → 87.4% | −2.5pp | 1,638 | 17,599 |
| Flex | 822K | 88.4% | → 48.6% | −39.8pp | 1,626 | 17,418 |
| Latitude | 814K | 83.0% | → **4.4%** 🔴 | **−78.6pp** | 1,555 | 16,102 |
| Comfort | 810K | 86.3% | → 71.7% | −14.7pp | 1,487 | 16,454 |
| Basic | 527K | 61.4% | → 54.4% | −7.0pp | 830 | 10,641 |

**Top 5 CPs → Latitude 全线崩溃：**
| CP | Traces | Latitude Supply → Sel | Drop |
|---|---|---|---|
| CA-US | 364K | 88.8% → 11.8% | −77.0pp |
| US-CA | 242K | 92.9% → 9.4% | −83.5pp |
| JP-CA | 234K | 89.3% → 2.7% | −86.7pp |
| TW-CA | 213K | 76.7% → 5.5% | −71.2pp |
| JP-US | 179K | 86.9% → 3.0% | −83.8pp |

**诊断：** Latitude 是 AC 最高 tier（全退全改），supply 健康（83-93%）但比价后近乎归零（2.7-11.8%）。国内线同样问题（5.2%）。Basic supply 偏低（61.4%）。走查重点：确认 AC 官网 Economy 五层结构（Basic/Standard/Flex/Comfort/Latitude）权益表。

---

### 2.5 NH — ANA（P0 头号优先）

#### 数据基线

**Coverage Trace 层（`MZ_coverage_check_for_claude`，近 90 天 Economy）：**

| Brand Tier | Trace量 | Supply Cov | → Selection Cov | Filter Drop | CP数 | OD数 |
|---|---|---|---|---|---|---|
| Full Flex | 975K | 90.9% | → 11.6% | −79.3pp 🔴 | 452 | 4,593 |
| Standard | 955K | 92.0% | → 76.8% | −15.3pp | 267 | 4,766 |
| Value | 917K | 86.9% | → 74.4% | −12.5pp | 234 | 4,290 |
| Flex | 902K | 56.2% 🔴 | → 15.6% | −40.6pp | 211 | 3,350 |
| Value Plus | 59K | 77.1% | → 77.9% | +0.8pp | 77 | 892 |
| Basic | 40K | 75.9% | → 75.4% | −0.5pp | 37 | 719 |
| **Light** | **完全缺失** 🔴 | — | — | — | — | — |

**订单层（量化表 `MZ_202606_quantification_v4`，Jan–May 2026）：**

| Brand Name | 订单量 | 占比 |
|---|---|---|
| **NULL（无 brand mapping）** | 68,398 | **47.0%** 🔴 |
| economyvalue | 26,216 | 18.0% |
| **economylight** | **23,341** | **16.0%** |
| economystandard | 8,146 | 5.6% |
| economyfullflex | 1,920 | 1.3% |
| economybasic | 1,327 | 0.9% |
| economyvalueplus | 1,082 | 0.7% |
| economyflex | 481 | 0.3% |

---

#### 五层排查结论（完整更新 2026-07-20）

##### 1. Data Foundation — ATPCO Brand Mapping ✅ 排查完毕

| Tier | ATPCO Name | `officialbrandname` | 在 Coverage 源表？ | 在 Segment 表？ | 在量化表？ |
|---|---|---|---|---|---|
| 1000 Basic | Eco I Basic 1n | ✅ `1` | ✅ | ✅ (0.9%) | ✅ |
| 2000 Value | Eco I Value 1c/2c | ✅ `1` | ✅ | ✅ (20.3%) | ✅ |
| **2500 Corporate** | Eco I Corporate 2f | **NULL** | **❌** | 微量 | 0.2% |
| **3000 Light** | Eco I Light 1c/2c, Economy Light | **NULL** 🔴 | **❌** | ✅ (20.3%) | 16.0% |
| 4000 Value Plus | Eco I Value Pls 2c | ✅ `1` | ✅ | ✅ | ✅ |
| **4500 Classic** | Eco I Classic 2c | **NULL** | **❌** | 微量 | 0.2% |
| 5000 Standard | Eco I Standard 2f | ✅ `1` | ✅ | ✅ | ✅ |
| 6000 Flex | Eco I Flex 2f, Economy Flex | ✅ `1` | ✅ | ✅ | ✅ |
| 7000 Full Flex | Eco I Fullflex 2f, Economy Full Flex | ✅ `1` | ✅ | ✅ | ✅ |

**关键结论：**
- **Light 在 coverage 数据中缺失，不是因为 supply 问题或 ATPCO mapping 问题。** ATPCO 表有三条 Light 记录（source=atpco, actived=1），但 `officialbrandname = NULL`。Coverage 源表 ETL 过滤了所有 `officialbrandname IS NOT 1` 的 tier，导致 Light 在 trace 层面不可见。**这是一个元数据标记问题，不是 supply gap。**
- **同样受影响的还有 Corporate（tier 2500）和 Classic（tier 4500）**——但这两个 tier 订单量极低（0.2%），实际影响不大
- **37% 的 NH 订单在 Segment 表中 atpco_brand_name IS NULL**——这比 Light 更严重，是 Data Foundation 层真正的瓶颈。大量订单处于品牌盲区，无法按 tier 分析

##### 2. Supply — 方向性限制 vs 真实 Gap

按你飞书文档的 4 套 fare family 结构，逐航线组验证：

| Fare Family | 代表 CP | 核心发现 |
|---|---|---|
| **A: JP→SEA/East Asia** | JP→HK/TH/VN | ✅ Flex supply 83-98%，完全正常。XX→JP Flex supply 0-3%，因方向限制正确消失。之前全局 Flex 56.2% 是回程航线稀释的假象 |
| **B: JP↔CN** | JP→CN, CN→JP | 🔴 **Light 在 coverage trace 中完全缺失**（但在订单层正常存在 16%）。Value/Standard/Flex/Full Flex supply 89-98%，健康。Flex 在双方向都存在（和 A 不同） |
| **C: JP→Europe** | JP→GB/FR/DE | ✅ 全 tier 86-92%，健康。回程 Flex 正确消失 |
| **D: JP↔Americas** | JP↔US/CA | ✅ 方向限制完全正确。JP→US/CA 有 Value/Standard/Flex/Full Flex，US/CA→JP 有 Basic/Value Plus/Full Flex。⚠ JP→US Value 71.1%、JP→CA Value 64.2%，略低于其他方向 |

**关键结论：Supply 层没有严重 gap。** 之前 BQ 数据中看到的"问题"（Flex 56.2%、Basic 75.9%、Value Plus 77.1%）大部分是方向性限制造成的假象，不是真实的 supply 缺失。唯一值得关注的是 JP→Americas 方向 Value 偏低（64-71%）。

#### NH Brand Tier × 方向可用性矩阵（BQ 数据验证）

你的飞书文档提出了 NH 的 tier 按始发地方向分为不同产品线。以下是 BQ coverage 数据按航线方向逐 tier 验证的结果：

| Brand Tier | JP→XX<br>（日本始发） | XX→JP<br>（SEA/EU/CN 回程） | US/CA→JP<br>（美洲始发） |
|---|---|---|---|
| **Basic** | ❌ 不存在 | ❌ 不存在 | ✅ 85-87% |
| **Value Plus** | ❌ 不存在 | ❌ 不存在 | ✅ 80-94% |
| **Light** | ✅ 订单层存在<br>🔴 coverage trace 缺失 | ❌ 不存在（仅 CN 线有） | ❌ 不存在 |
| **Value** | ✅ 64-93% | ✅ 76-97% | ❌ 不存在 |
| **Standard** | ✅ 77-98% | ✅ 88-97% | ❌ 不存在 |
| **Flex** | ✅ 77-98% | ❌ 0-3% | ❌ 0-4% |
| **Full Flex** | ✅ 82-99% | ✅ 84-98% | ✅ 98-99% |

**三个关键结论：**

1. **NH 在 supply 层是"两家航司"**——日本始发航线有 Value/Standard/Flex/Full Flex 四层升舱阶梯，美洲始发航线有 Basic/Value Plus/Full Flex 三层。**没有任何一个 tier 在三个方向都可用。** 唯一例外是中日线（Fare Family B）：CN→JP 方向有 Flex 97.5%，与 SEA/EU 回程的 0-3% 形成鲜明对比。

2. **之前 BQ 全局数据的"问题数字"全部得到解释：**
   - Flex 56.2% = JP→XX 83-98% + XX→JP 0-3% 的平均值 → **不是 supply gap，是方向稀释**
   - Basic 75.9% = 仅美洲始发有，该方向内 85-87% → **略低但可接受**
   - Value Plus 77.1% = 仅美洲始发有，该方向内 80-94% → **可接受**

3. **Full Flex 是唯一的"全向 tier"**——但定价 +41~164% 不合理，所以这个全向能力意义有限。真正有 upsell 潜力的 Flex 和 Standard 被方向性限制锁死在日本始发单侧。

##### 3. Fare Selection — 比价过滤

| CP | Standard filter drop | Flex filter drop | Full Flex filter drop |
|---|---|---|---|
| JP→HK | −0.0pp ✅ | −0.0pp ✅ | −0.0pp ✅ |
| JP→CN | −0.7pp ✅ | −0.0pp ✅ | −0.0pp ✅ |
| **CN→JP** 🔴 | **−60.7pp** | −0.0pp | −4.2pp |
| JP→TH | −0.0pp ✅ | −0.0pp ✅ | −4.7pp |
| JP→GB | −4.7pp ✅ | −0.3pp ✅ | −3.3pp ✅ |
| JP→US | −14.7pp | −6.8pp | −13.8pp |

**关键结论：**
- **CN→JP Standard −60.7pp 是区域内异常**——同一航司、同一 tier 在其他 CP 上 filter drop 几乎是零。这暗示中日线有特殊的比价规则或定价导致 Standard 被过滤
- **JP→XX 方向的 filter drop 普遍很小（0-6pp）**——比价过滤不是 NH 的主要问题
- **Full Flex −79.3pp 的回程贡献非常大**：JP→XX 方向 Full Flex 过滤仅 0-14pp，但 XX→JP（如 TH→JP、HK→JP）覆盖大量 trace 且 Full Flex 回程存在但被严重过滤

##### 4. Ranking — 待排查（最可能的关键层）

- **Standard 定价合理（+1~10%），selection 存在（77-92%），但订单仅 5.6%**——这是五层中最核心的谜题。90% 可能性是排序问题：Standard 被排在第 4-5 位，用户翻不到
- **6 个 tier 的挤压效应**——搜索结果中 Value（最低）和 Full Flex（最高）两端可见，中间 Standard 和 Flex 被跳过
- Personalized Ranking ABT（Jul 9 上线）对 NH 的影响待验证

##### 5. Display — 待排查

- NH 不受 void/24h 限制 ✅
- **Standard 的权益差异是否被清晰展示？** Value→Standard 升级 ="多一件行李 + 灵活改签（付费）"。如果前端不展示这些权益差异，用户看不到升级理由
- TripFlex bundle 是否和 NH 自身的 Flex tier 冲突？BA 文档已发现类似 pattern

---

#### ATPCO Mapping 表字段说明

以下字段来自 `ods_fltairtickets_mysql_fltresourcedb_tb_brandname_unified`：

| 字段 | 含义 | NH Light 的值 |
|---|---|---|
| `source` | 数据来源（atpco/uta/ndc/manual） | atpco ✅ |
| `actived` | 是否启用 | 1 ✅ |
| `officialbrandname` | 是否为官方品牌运价名称 | **NULL** 🔴 |

**Coverage 源表 ETL 逻辑（推断）：仅选取 `officialbrandname = 1` 的 brand name 计算 coverage。** 这导致 Light（以及 Corporate、Classic）在 trace 层完全不可见。

---

#### NH P0 优先级总结

| 层 | 状态 | 严重度 |
|---|---|---|
| Data Foundation | 🔴 37% 订单 atpco brand name NULL + Light `officialbrandname` 未标 | 严重 |
| Supply | ✅ 方向性限制导致假象，真实 gap 仅 JP→Americas Value 偏低 | 轻微 |
| Fare Selection | ⚠️ CN→JP Standard −60.7pp 区域性异常 | 中等 |
| Ranking | ❓ 核心谜题：Standard 定价合理但订单仅 5.6% | **最可能的关键** |
| Display | ❓ 权益差异是否清晰展示？退改政策是否可见？ | 待验证 |

**核心假设：NH 的 upsell 瓶颈不在 Supply，而在 Ranking + Display——Standard 存在、定价合理、但用户看不到或看不懂。**

参考文档：[Retain High Tier Brand Fare - NH case study](https://trip.sg.larkenterprise.com/docx/TJ0Sdda6roDZ80xqPMzl5U3NgCc)

---

### 2.6 JL — JAL

| Brand Tier | Trace量 | Supply Cov | → Selection Cov | Filter Drop | CP数 | OD数 |
|---|---|---|---|---|---|---|
| Flex | 640K | 87.6% | → 18.9% | **−68.7pp** 🔴🔴 | ~300 | ~3,900 |
| Semi Flex | 420K | 87.7% | → 74.6% | −13.1pp | 232 | 2,984 |
| Special | 280K | **93.0%** | → 89.8% | −3.2pp | 158 | 1,934 |

> 注：JL 的 Flex 和 Semi Flex 各有两条几乎相同的记录（名称中空格差异：`Economy Flex` vs `Economy  Flex`），说明 ATPCO brand name mapping 不干净。上表为合并后数据。

**Top 5 CPs → Flex 的严重 drop：**
| CP | Traces | Flex Supply → Sel | Drop |
|---|---|---|---|
| JP-VN | 140K | 97.3% → 0.2% | −97.1pp |
| TH-JP | 94K | 99.0% → 14.5% | −84.5pp |
| JP-US | 71K | 92.9% → 13.6% | −79.3pp |
| JP-TW | 63K | 60.0% → 12.1% | −47.8pp |
| TW-JP | 57K | 66.7% → 11.0% | −55.7pp |

**诊断：** JP-VN Flex 比价后仅 0.2%（几乎完全不可见）。Special（最低 tier）健康。Semi Flex 居中。Flex 在 JP-TW/TW-JP 方向 supply 也偏低（60-67%）。走查重点：官网三层 fare family + 确认 `Economy Flex` 双记录的根因。

---

### 2.7 VF — AJet (TK 旗下 LCC)

| Brand Tier | Trace量 | Supply Cov | → Selection Cov | Filter Drop | CP数 | OD数 |
|---|---|---|---|---|---|---|
| Basic | 892K | **98.8%** | → 90.6% | −8.2pp | 821 | 4,616 |
| Ecojet | 892K | **98.3%** | → 91.8% | −6.5pp | 817 | 4,599 |
| Flex | 892K | **97.9%** | → **54.9%** 🔴 | **−43.0pp** | 817 | 4,596 |

| Domestic | | | | | |
|---|---|---|---|---|---|
| Basic | 229K | 98.5% | → 97.5% | −1.1pp | 2 | 698 |
| Flex | 229K | 98.3% | → 62.8% | −35.5pp | 1 | 692 |
| Ecojet | 226K | 98.0% | → **3.0%** 🔴 | **−95.0pp** | 1 | 630 |

**Top 5 CPs → Flex 的 filter drop：**
| CP | Traces | Flex Supply → Sel | Drop |
|---|---|---|---|
| DE-TR | 569K | 97.5% → 34.8% | −62.7pp |
| TR-DE | 166K | 99.2% → 26.1% | −73.0pp |
| GB-TR | 119K | 96.1% → 26.9% | −69.2pp |
| SA-TR | 91K | 97.2% → 83.3% | −13.9pp |
| RU-TR | 81K | 96.2% → 41.9% | −54.3pp |

**诊断：** Supply 完美（97-99%），问题纯粹在 Fare Selection 层。Flex 国际线 −43pp、国内线 −35.5pp；Ecojet 国内线 −95pp（几乎全杀）。SA-TR 方向 Flex 相对健康（−13.9pp），可作为对比。走查重点：VF 的 Flex vs Ecojet 权益差异 + 国内线 Ecojet 为什么几乎 100% 被比价过滤。

---

### 2.8 UA — United Airlines

| Brand Tier | Trace量 | Supply Cov | → Selection Cov | Filter Drop | CP数 | OD数 |
|---|---|---|---|---|---|---|
| Fully Refundable | 693K | **85.1%** | → 47.1% | −38.0pp | 711 | 12,310 |
| Economy | 690K | 85.4% | → 79.2% | −6.2pp | 671 | 13,377 |
| Basic Economy | 556K | 71.7% | → 70.7% | −1.0pp | 203 | 6,444 |
| Economy Plus | 133K | **48.6%** 🔴 | → **1.9%** 🔴 | **−46.7pp** | 87 | 522 |

**Top 5 CPs：**
| CP | Traces | Fully Refundable Drop | Plus 状态 |
|---|---|---|---|
| JP-US | 370K | 94.2% → 47.9% (−46.3pp) | Plus: 46.2% → 0.6% |
| TW-JP | 143K | 78.4% → 60.3% (−18.1pp) | Plus: 不覆盖 |
| HK-TH | 134K | 70.4% → 61.8% (−8.6pp) | Plus: 不覆盖 |
| HK-US | 124K | 91.7% → 2.9% (−88.8pp) | Plus: 不覆盖 |
| US-JP | 111K | 96.6% → 74.5% (−22.1pp) | Plus: 37.6% → 0.4% |

**诊断：** Plus 仅覆盖 87 CPs（vs Fully Refundable 的 711 CPs）——这不是比价问题而是 supply 问题。Fully Refundable 在 HK-US 方向 −88.8pp 极端。国内线 Plus 同样 −82.4pp。走查重点：确认 UA 官网 Economy Plus 的权益和覆盖航线。

---

### 2.9 DL — Delta Air Lines

| Brand Tier | Trace量 | Supply Cov | → Selection Cov | Filter Drop | CP数 | OD数 |
|---|---|---|---|---|---|---|
| Main Basic | 454K | 81.3% | → 74.2% | −7.1pp | 386 | 11,779 |
| Main Classic | 411K | **90.5%** | → 84.4% | −6.1pp | 843 | 14,352 |
| Comfort Classic | 356K | 62.2% | → **10.7%** 🔴 | **−51.5pp** | 439 | 9,363 |
| Main Extra | 336K | 79.1% | → 72.1% | −7.0pp | 701 | 11,668 |
| Comfort Extra | 301K | 71.3% | → **14.3%** 🔴 | **−57.0pp** | 264 | 8,663 |

**Top 5 CPs → Comfort 系列全线崩溃：**
| CP | Traces | Comfort Classic Drop | Comfort Extra Drop |
|---|---|---|---|
| JP-US | 318K | 86.1% → 12.0% (−74.1pp) | 86.4% → 4.3% (−82.0pp) |
| GB-US | 153K | 61.5% → 2.2% (−59.3pp) | 8.3% → 0.0% (−8.3pp) |
| CA-US | 103K | 57.7% → 25.2% (−32.5pp) | 38.6% → 10.3% (−28.3pp) |
| TW-US | 96K | 不覆盖 | 79.1% → 4.2% (−74.9pp) |
| FR-US | 69K | 7.2% → 0.4% (−6.9pp) | 不覆盖 |

**诊断：** Comfort 系列（经典/Extra）是 DL 的升级 tier，supply 大多在 60-85% 但比价后跌至 10-15%。JP-US 方向尤为严重。走查重点：DL 官网五层 Economy 结构 + Comfort 系列的行李/座位权益差异。

---

### 2.10 AA — American Airlines

| Brand Tier | Trace量 | Supply Cov | → Selection Cov | Filter Drop | CP数 | OD数 |
|---|---|---|---|---|---|---|
| Main Cabin | 305K | **77.4%** | → 71.6% | −5.7pp | 1,351 | 16,561 |
| Basic Economy | 219K | **38.4%** 🔴 | → 35.0% | −3.4pp | 361 | 7,461 |
| Main Plus | 217K | **49.3%** 🔴 | → 29.1% | −20.2pp | 300 | 7,449 |

**Top 5 CPs → 全线偏低：**
| CP | Traces | Basic | Main Cabin | Main Plus |
|---|---|---|---|---|
| JP-US | 116K | 0.9% → 0.8% | 37.0% → 22.6% | 53.7% → 4.9% |
| ES-US | 46K | 67.3% → 67.7% | 98.2% → 93.8% | 49.8% → 24.3% |
| GB-US | 43K | 91.9% → 86.3% | 82.5% → 88.5% | 29.2% → 12.2% |
| CA-US | 37K | 27.2% → 20.5% | 91.0% → 85.4% | 50.5% → 26.4% |
| US-JP | 36K | 3.9% → 3.7% | 97.2% → 88.3% | 67.7% → 59.3% |

**诊断：** 11 家里最严重的 supply 问题。JP-US 方向 Basic 仅 0.9%、Main Cabin 仅 37%——核心市场几乎无品牌映射。ES-US 方向例外（Main Cabin 98%），说明问题不是全局性的而是按航线差异大。国际线总 trace 量 0.7M 显著偏低（对比 UA 2.1M、DL 1.9M）。走查重点：AA 官网 fare family + 按航线确认是否美日线品牌映射大面积缺失。

---

### 2.11 KL — KLM（Benchmark）

| Brand Tier | Trace量 | Supply Cov | → Selection Cov | Filter Drop | CP数 | OD数 |
|---|---|---|---|---|---|---|
| Standard | 288K | 94.5% | → 93.6% | −1.0pp | 3,974 | 19,519 |
| Flex | 288K | 94.1% | → 89.5% | −4.6pp | 3,965 | 19,419 |
| Light | 282K | 95.1% | → 93.1% | −2.0pp | 3,725 | 18,575 |

**诊断：** Supply 94-95%、Selection 89-94%、Filter drop 1-5pp。所有三个 tier 在所有航线表现一致。这是 KL 被纳入 WS5 Airline Compliance（Strict Fare Display）强制要求的结果，代表"全量品牌运价展示"的目标状态。

---

## 4. Diagnosis by Five-Layer Funnel

### Data Foundation → Supply Gap（品牌运价映射缺失）

| 航司 | Brand | Supply Cov | 影响范围 | 可能的根因 |
|---|---|---|---|---|
| **AA** | 全 tier | 38-77% | 国际线 0.7M traces | JP-US 方向大面积缺失 |
| **BR** | Discount | **0.0%** | 949K traces | Mapping 从未建立 |
| **CI** | Discount | 10.8% | 1.55M traces | 接近缺失 |
| **EK** | Special | 41.5% | 2.51M traces | 最低 tier 映射不完整 |
| **NH** | Flex | 56.2% | 902K traces | 特定 tier 缺失 |
| **UA** | Economy Plus | 48.6% | 133K traces | 仅覆盖 87 CPs |
| **AC** | Basic | 61.4% | 527K traces | 最低 tier 映射不完整 |

### Fare Selection Gap（比价过滤）

| 航司 | Brand | Filter Drop | Selection 剩余 | 模式 |
|---|---|---|---|---|
| **VF** | Flex (Intl) | −43.0pp | 54.9% | DE-TR 方向 −62.7pp |
| **VF** | Ecojet (Dom) | −95.0pp | 3.0% | 国内线几乎全杀 |
| **JL** | Flex | −68.7pp | 18.9% | JP-VN 仅 0.2% |
| **NH** | Full Flex | −79.3pp | 11.6% | CN-JP 仅 4.7% |
| **AC** | Latitude | −78.6pp | 4.4% | JP-CA 仅 2.7% |
| **CI** | Flex | −68.9pp | 23.5% | HK-TW 仅 4.8% |
| **EK** | Flex Plus | −66.2pp | 27.9% | FR-AE 仅 3.3% |
| **BR** | Up | −77.1pp | 13.2% | 与 CI Flex 同模式 |
| **DL** | Comfort Classic/Extra | −51~57pp | 10-14% | JP-US 方向最严重 |
| **UA** | Fully Refundable | −38.0pp | 47.1% | HK-US 极端 −88.8pp |

**共同规律：** 最低 price tier 在所有航司都健康（filter drop <10pp）。越往上（更贵的 tier），比价过滤越严重。这符合比价算法逻辑——最低价排最前。

---

## 5. 人工走查 Checklist

对每航司，需要完成以下验证：

1. **航司官网确认 fare family 结构**
   - Tier 数量、命名、权益差异（行李/退改/座位/里程）
   - 与 ATPCO brand name 表中的映射是否一致
   
2. **选取 Top 3 国际 country pairs，逐方向验证**
   - 搜索往返航班，查看比价结果中是否展示了全部 brand tier
   - 记录缺失的 tier（哪些 tier 完全不出现在结果中）
   
3. **对比 selection coverage 数据**
   - 官网展示的 tier 是否与 BQ 数据中 selection cov >50% 的 tier 一致
   - 不一致的 case 是数据问题还是产品问题

### 走查优先级建议

| 优先级 | 航司 | 理由 |
|---|---|---|
| **P0** | **NH, BR** | NH：体量大（3.8M traces）、fare family 6 层最复杂、不受 void/24h 限制——解决 supply+selection 后提升空间最大。BR：体量大（9.7M traces）、upsell rate 偏低可能受 fare family 结构决定、Discount 0% coverage 是明确 gap |
| **P1** | **AA, CI, JL, VF** | AA：supply 最严重（全 tier <78%，JP-US 近乎 0%）。CI：Discount 接近缺失 + Flex −69pp。JL：Flex −69pp + ATPCO name 脏数据。VF：supply 完美但 selection 有极值（Ecojet Dom −95pp） |
| **P2** | **EK, AC, UA, DL** | 混合问题——部分 tier 健康、部分严重。EK Special supply gap + Flex Plus selection；AC Latitude −79pp；UA Plus 覆盖面窄；DL Comfort 系列 −51~57pp |
| Reference | **KL, VB** | KL：WS5 Compliance 标杆。VB：NDC 接入，整体健康 |

---

## 6. 方法与口径说明

- **数据源：** `trip-ibu-adhoc.ibu_adhoc_temp.MZ_coverage_check_for_claude`
  - 底层表：`dw_fltdb_adm_rsc_engine_airline_route_brand_cover_v2_di`
  - 时间窗口：近 90 天（2026-04-21 ~ 2026-07-20）
  - 舱位：Economy (Y)
  - 粒度：airport/city level
- **Supply Coverage =** `has_brand_cnt / total_cnt` — 资源侧（爬取/对接）有 brand name 的 trace 占比
- **Selection Coverage =** `output_has_brand_cnt / output_total_cnt` — 比价后输出的 trace 中有 brand name 的占比
- **Filter Drop =** Supply Cov − Selection Cov — 比价环节损失的覆盖率
- **Intl vs Dom：** 通过 `country_pair` 两端国家代码是否相同区分
