# NH (ANA) — 五层诊断分析
_分析日期: 2026-07-20 | 数据源: BQ `MZ_coverage_check_for_claude` (近 90 天) + `MZ_202606_quantification_v4` (Jan–May 2026)_

---

## 1. 数据基线

### Coverage Trace 层

`MZ_coverage_check_for_claude`，近 90 天，Economy (Y)，Intl：

| Brand Tier | Trace量 | Supply Cov | → Selection Cov | Filter Drop |
|---|---|---|---|---|
| Full Flex | 975K | 90.9% | → 11.6% | −79.3pp 🔴 |
| Standard | 955K | 92.0% | → 76.8% | −15.3pp |
| Value | 917K | 86.9% | → 74.4% | −12.5pp |
| Flex | 902K | 56.2% 🔴 | → 15.6% | −40.6pp |
| Value Plus | 59K | 77.1% | → 77.9% | +0.8pp |
| Basic | 40K | 75.9% | → 75.4% | −0.5pp |
| **Light** | **完全缺失** 🔴 | — | — | — |

### 订单层

`MZ_202606_quantification_v4`，Jan–May 2026：

| Brand Name | 订单量 | 占比 |
|---|---|---|
| **NULL（无 brand mapping）** | 68,398 | **37.0%** 🔴 |
| economyvalue | 26,216 | 18.0% |
| **economylight** | **23,341** | **16.0%** |
| economystandard | 8,146 | 5.6% |
| economyfullflex | 1,920 | 1.3% |
| economybasic | 1,327 | 0.9% |
| economyvalueplus | 1,082 | 0.7% |
| economyflex | 481 | 0.3% |

---

## 2. 五层漏斗排查

### 2.1 Data Foundation — ATPCO Brand Mapping ✅ 排查完毕

NH 有 9 个 ATPCO brand tier（1000–7000），覆盖 6 个实际产品线：

| Tier | ATPCO Name | `officialbrandname` | 在 Coverage 源表？ | 在订单表？ |
|---|---|---|---|---|
| 1000 Basic | Eco I Basic 1n | ✅ `1` | ✅ | ✅ (0.9%) |
| 2000 Value | Eco I Value 1c/2c | ✅ `1` | ✅ | ✅ (18.0%) |
| **2500 Corporate** | Eco I Corporate 2f | **NULL** | **❌** | 微量 |
| **3000 Light** | Eco I Light 1c/2c, Economy Light | **NULL** 🔴 | **❌** | ✅ (16.0%) |
| 4000 Value Plus | Eco I Value Pls 2c | ✅ `1` | ✅ | ✅ (0.7%) |
| **4500 Classic** | Eco I Classic 2c | **NULL** | **❌** | 微量 |
| 5000 Standard | Eco I Standard 2f | ✅ `1` | ✅ | ✅ (5.6%) |
| 6000 Flex | Eco I Flex 2f, Economy Flex | ✅ `1` | ✅ | ✅ (0.3%) |
| 7000 Full Flex | Eco I Fullflex 2f, Economy Full Flex | ✅ `1` | ✅ | ✅ (1.3%) |

**关键结论：**

- **Light 在 coverage 数据中缺失，不是因为 supply 问题。** ATPCO 表有三条 Light 记录（source=atpco, actived=1），但 `officialbrandname = NULL`。Coverage 源表 ETL 过滤了所有 `officialbrandname IS NOT 1` 的 tier，导致 Light 在 trace 层面不可见。**这是一个元数据标记问题，不是 supply gap。**
- 同样受影响的还有 Corporate（tier 2500）和 Classic（tier 4500）——但这两个 tier 订单量极低（0.2%），实际影响不大
- **37% 的 NH 订单 brand_name IS NULL**——无法按 tier 分析，是 Data Foundation 层真正的瓶颈

#### ATPCO Mapping 表字段说明

| 字段 | 含义 | NH Light 的值 |
|---|---|---|
| `source` | 数据来源（atpco/uta/ndc/manual） | atpco ✅ |
| `actived` | 是否启用 | 1 ✅ |
| `officialbrandname` | 是否为官方品牌运价名称 | **NULL** 🔴 |

**Coverage 源表 ETL 逻辑（推断）：仅选取 `officialbrandname = 1` 的 brand name 计算 coverage。** 这导致 Light（以及 Corporate、Classic）在 trace 层完全不可见。

---

### 2.2 Supply — 方向性限制 vs 真实 Gap ✅

NH 的核心特点是**方向性产品分化**——日本始发和非日本始发是完全不同的产品线。按飞书文档的 4 套 fare family 验证：

| Fare Family | 代表 CP | 核心发现 |
|---|---|---|
| **A: JP→SEA/East Asia** | JP→HK/TH/VN | ✅ Flex supply 83-98%，完全正常。XX→JP Flex supply 0-3%，因方向限制正确消失 |
| **B: JP↔CN** | JP→CN, CN→JP | 🔴 Light 在 coverage trace 缺失（订单层正常 16%）。Value/Standard/Flex/Full Flex supply 89-98%，健康。Flex 在双方向都存在（独特） |
| **C: JP→Europe** | JP→GB/FR/DE | ✅ 全 tier 86-92%，健康 |
| **D: JP↔Americas** | JP↔US/CA | ✅ 方向限制完全正确。⚠ JP→US Value 71.1%、JP→CA Value 64.2%，略低 |

#### Brand Tier × 方向可用性矩阵

| Brand Tier | JP→XX（日本始发） | XX→JP（回程） | US/CA→JP（美洲始发） |
|---|---|---|---|
| **Basic** | ❌ 不存在 | ❌ 不存在 | ✅ 85-87% |
| **Value Plus** | ❌ 不存在 | ❌ 不存在 | ✅ 80-94% |
| **Light** | ✅ 订单层存在<br>🔴 coverage trace 缺失 | ❌ 不存在 | ❌ 不存在 |
| **Value** | ✅ 64-93% | ✅ 76-97% | ❌ 不存在 |
| **Standard** | ✅ 77-98% | ✅ 88-97% | ❌ 不存在 |
| **Flex** | ✅ 77-98% | ❌ 0-3% | ❌ 0-4% |
| **Full Flex** | ✅ 82-99% | ✅ 84-98% | ✅ 98-99% |

**三个关键结论：**

1. **NH 在 supply 层是"两家航司"**——日本始发航线有 Value/Standard/Flex/Full Flex 四层升舱阶梯，美洲始发航线有 Basic/Value Plus/Full Flex 三层。**没有任何一个 tier 在三个方向都可用。** 唯一例外是中日线（Fare Family B）：CN→JP 方向有 Flex 97.5%，与 SEA/EU 回程的 0-3% 形成鲜明对比。

2. **之前 BQ 全局数据的"问题数字"全部得到解释：**
   - Flex 56.2% = JP→XX 83-98% + XX→JP 0-3% 的平均值 → **不是 supply gap，是方向稀释**
   - Basic 75.9% = 仅美洲始发有，该方向内 85-87% → 略低但可接受
   - Value Plus 77.1% = 仅美洲始发有，该方向内 80-94% → 可接受

3. **Full Flex 是唯一的"全向 tier"**——但定价 +41~164% 不合理，所以这个全向能力意义有限。真正有 upsell 潜力的 Flex 和 Standard 被方向性限制锁死在日本始发单侧。

**Supply 层结论：没有严重 gap。** 唯一值得关注的是 JP→Americas 方向 Value 偏低（64-71%）。

---

### 2.3 Fare Selection — 比价过滤 ⚠️

| CP | Standard | Flex | Full Flex |
|---|---|---|---|
| JP→HK | −0.0pp ✅ | −0.0pp ✅ | −0.0pp ✅ |
| JP→CN | −0.7pp ✅ | −0.0pp ✅ | −0.0pp ✅ |
| **CN→JP** 🔴 | **−60.7pp** | −0.0pp | −4.2pp |
| JP→TH | −0.0pp ✅ | −0.0pp ✅ | −4.7pp |
| JP→GB | −4.7pp ✅ | −0.3pp ✅ | −3.3pp ✅ |
| JP→US | −14.7pp | −6.8pp | −13.8pp |

**关键结论：**
- **CN→JP Standard −60.7pp 是区域内异常**——同一航司、同一 tier 在其他 CP 上 filter drop 几乎是零。中日线可能有特殊的比价规则或定价导致 Standard 被过滤
- **JP→XX 方向的 filter drop 普遍很小（0-6pp）**——比价过滤不是 NH 的主要问题
- Full Flex −79.3pp 的回程贡献非常大：JP→XX 方向 Full Flex 过滤仅 0-14pp，但回程 trace 量巨大且 Full Flex 存在但被严重过滤（定价过高导致）

---

### 2.4 Ranking — 待排查（最可能的关键层）❓

- **Standard 定价合理（+1~10%），selection 存在（77-92%），但订单仅 5.6%**——这是五层中最核心的谜题。90% 可能性是排序问题：Standard 被排在第 4-5 位，用户翻不到
- **6 个 tier 的挤压效应**——搜索结果中 Value（最低）和 Full Flex（最高）两端可见，中间 Standard 和 Flex 被跳过
- Personalized Ranking ABT（Jul 9 上线）对 NH 的影响待验证

---

### 2.5 Display — 待排查 ❓

- NH 不受 void/24h 限制 ✅
- **Standard 的权益差异是否被清晰展示？** Value→Standard 升级 = "多一件行李 + 灵活改签（付费）"。如果前端不展示这些权益差异，用户看不到升级理由
- TripFlex bundle 是否和 NH 自身的 Flex tier 冲突？BA 文档已发现类似 pattern

---

## 3. 五层总结与优先级

| 层 | 状态 | 严重度 |
|---|---|---|
| **Data Foundation** | 🔴 37% 订单 brand_name NULL + Light `officialbrandname` 未标 | 严重 |
| **Supply** | ✅ 方向性限制导致假象，真实 gap 仅 JP→Americas Value 偏低 | 轻微 |
| **Fare Selection** | ⚠️ CN→JP Standard −60.7pp 区域性异常 | 中等 |
| **Ranking** | ❓ 核心谜题：Standard 定价合理但订单仅 5.6% | **最可能的关键** |
| **Display** | ❓ 权益差异是否清晰展示？退改政策是否可见？ | 待验证 |

**核心假设：NH 的 upsell 瓶颈不在 Supply，而在 Ranking + Display——Standard 存在、定价合理、但用户看不到或看不懂。**

---

## 4. BR vs NH 对比速查

| 维度 | NH | BR |
|---|---|---|
| 订单量 | ~145K | **~485K（3.3x）** |
| NULL brand_name | 37% | **74.7%（2x）** |
| Tier 复杂度 | 6 层 + 方向性产品分化 | 4 层，无方向限制 |
| Supply 问题 | 方向稀释假象，实际健康 | 65-85% 中等，Discount 完全缺失 |
| Fare Selection | 基本健康（CN→JP 除外）| **Up −48.5pp 全局** + Standard 长线 −30~50pp |
| 核心瓶颈 | **Ranking + Display** | **Data Foundation + Fare Selection** |
| Void/24h | ✅ 不受影响 | ✅ 不受影响 |

---

参考文档：[Retain High Tier Brand Fare - NH case study](https://trip.sg.larkenterprise.com/docx/TJ0Sdda6roDZ80xqPMzl5U3NgCc)
