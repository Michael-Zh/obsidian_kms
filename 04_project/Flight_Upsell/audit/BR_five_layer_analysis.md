# BR (EVA Air) — 五层诊断分析
_分析日期: 2026-07-21 | 状态: ✅ Closed — Product Design Ceiling, 非 Trip.com 可修复_

---

## 1. 数据基线

### Coverage Trace 层

`MZ_coverage_check_for_claude`，近 90 天，Economy (Y)，Intl lines：

| Brand Tier | Trace量 | Supply Cov | → Selection Cov | Filter Drop |
|---|---|---|---|---|
| Economy Up | 6.01M | 77.0% | → 28.5% | **−48.5pp** 🔴 |
| Economy Standard | 6.01M | 74.9% | → 68.1% | −6.8pp |
| Economy Basic | 6.01M | 69.0% | → 68.7% | −0.3pp ✅ |
| **Economy Discount** | 1.02M | **0.0%** 🔴🔴 | → 0.0% | 0.0pp |

**关键观察：**
- Discount 全局 0% supply + 0% selection — 1.02M traces 没有任何 brand mapping
- Up 的 filter drop −48.5pp — selection 仅 28.5%，是最大的 fare selection 问题
- Basic/Standard 的 filter drop 很小（−0.3pp / −6.8pp）——比价环节基本健康
- **没有 Domestic 数据** — BR 以台湾为中心，所有数据都是国际线

### 订单层

`MZ_202606_quantification_v4`，Jan–May 2026：

| Brand Name | 订单量 | 占比 | Upsell Rate |
|---|---|---|---|
| **NULL（无 brand mapping）** | 137,888 | **74.7%** 🔴🔴 | — |
| economybasic | 33,786 | 18.3% | 22.0% |
| economystandard | 9,769 | 5.3% | 36.9% |
| economyup | 2,507 | 1.4% | 33.9% |
| 其他杂项（standard, economysaver 等）| ~600 | 0.3% | — |

**BR 全局 Upsell Rate: 21.1%**（485K 总订单，97K upsell 订单）——显著低于 33% 目标。

---

## 2. 五层漏斗排查

### 2.1 Data Foundation — ATPCO Brand Mapping 🔴🔴

#### Coverage 表中有四个 tier name：

| Coverage Brand Name | Traces | 推测对应官网 tier | 备注 |
|---|---|---|---|
| Economy Discount | 1.02M | 轻省 | **0% supply —— 映射完全缺失** |
| Economy Basic | 6.01M | 基本 | 69% supply |
| Economy Standard | 6.01M | 经典 | 75% supply |
| Economy Up | 6.01M | 尊宠 | 77% supply |

#### 订单表中的 brand_name 混乱：

| 订单 brand_name | 订单量 | 对应 Coverage Tier | 状态 |
|---|---|---|---|
| economybasic | 33,786 | Economy Basic | ✅ 对齐 |
| economystandard | 9,769 | Economy Standard | ✅ 对齐 |
| economyup | 2,507 | Economy Up | ✅ 对齐 |
| NULL | **137,888** 🔴 | — | 无法对应到任何 tier |
| standard | 127 | — | 可能是 Standard 的原始名 |
| economysaver | 114 | — | 可能是 Discount 的别名 |
| economyclassic | 90 | — | 可能是 Standard 的别名 |
| economy | 57 | — | 无法归类 |
| basic | 32 | — | 可能是 Basic 的原始名 |
| ecosaver | 27 | — | Discount 别名 |
| economyflex | 23 | — | 可能是 Up 的别名 |

**核心问题：**
1. **74.7% 的订单 brand_name IS NULL** — 这是 Data Foundation 层最严重的问题。NH 才 37%，BR 是 NH 的两倍。绝大多数 BR 订单处于品牌盲区，无法按 tier 做精细化分析。
2. **Economy Discount coverage 0%** — 1.02M traces 全局无映射。虽然订单表中也有少量 `economysaver`/`ecosaver` 条目（合计 141 单），说明 Discount tier 真实存在，但几乎没有被正确识别。
3. **ATPCO mapping 表不可直接访问** — 需要确认 BR 的 ATPCO `officialbrandname` 标记是否完整，类似 NH 的 Light 因为 `officialbrandname=NULL` 导致 coverage 缺失。

#### NULL 订单 Attributes 画像（2026-07-21 新增）

> **假设：NULL 订单里混了大量 Discount tier → 拉低 upsell rate。验证：拉所有 NULL 订单的 baggage + flexibility + ticket operation type 分布。**

**Baggage：**

| Baggage | NULL 订单 | 占比 |
|---|---|---|
| 4.Fare+carry on+checkin（含托运+手提）| 136,574 | **99.0%** |
| 1.fare only（纯票价，不含行李）| 1,131 | 0.8% |
| 其他 | 183 | 0.1% |

**Flexibility（退改政策颗粒度）：**

| Cancel Policy | Change Policy | NULL 订单 | 占比 |
|---|---|---|---|
| paid_cancel | paid_change | 127,434 | **92.4%** |
| no_cancel | paid_change | 6,373 | 4.6% |
| paid_cancel | free_change | 1,660 | 1.2% |
| no_cancel | no_change | 899 | 0.7% |
| 其他 | — | 1,522 | 1.1% |

**Ticket Operation Type（退票窗口类型）：**

| Type | NULL 订单 | 占比 |
|---|---|---|
| void | 88,926 | 64.5% |
| standard (no free cancel policy) | 38,451 | 27.9% |
| 48 hour free cancel | 10,168 | 7.4% |
| 24 hour free cancel | 343 | 0.2% |

**对比 tagged 订单（Basic/Standard/Up）的 baggage 和 flexibility：**

| Brand | 含托运+手提 | paid_cancel + paid_change |
|---|---|---|
| NULL | 99.0% | 92.4% |
| economybasic | 98.8% | 94.9% |
| economystandard | 98.9% | 99.5% |
| economyup | 98.8% | 68.4%（另有 30.6% free_change） |

**Booking Channels（NULL vs 全量，分布完全一致）：**

| Channel | 全部 BR | NULL only |
|---|---|---|
| GDS-WS | 63.5% | 63.4% |
| CSD-WS | 19.9% | 18.2% |
| 1A-WS | 15.0% | 16.7% |
| ZY-WS | 0.7% | 0.9% |
| 1B-WS | 0.5% | 0.5% |
| 1G-WS | 0.4% | 0.3% |

**三个关键结论：**

1. **NULL 订单 ≠ Discount。** Discount 理论上应该是 fare-only + 不可退改。但 NULL 订单 99% 含托运行李 + 92.4% 可付费退改。真正的 Discount 可能只有 ~900 单（fare only + no_cancel/no_change 的组合），而不是 137,888 单。

2. **NULL 订单和 tagged Basic/Standard 的 baggage 分布无法区分**（都 99% 含托运）。这说明 **BR 的所有 Economy 运价很可能默认包含托运+手提行李**——tier 之间的差异不在行李权益，而在退改费用金额、座位选择、里程累积等方面。

3. **Up 是唯一能通过 flexibility 区分出来的 tier**——Up 有 30.6% 的 free_change 率，而 Basic/Standard/NULL 几乎都是 paid_change。这是一个可用的区分信号：如果能结合 free_change 标记，至少能从 NULL 中捞出部分 Up 订单。

4. **Booking channel 分布无异常**——NULL 不是某个特定渠道的问题，而是全局性的 ATPCO mapping 缺失。

**对比 NH：** NH 的 Data Foundation 核心问题是 Light `officialbrandname=NULL` + 37% 订单 NULL。BR 的情况更严重——74.7% NULL + Discount 100% 缺失。

---

### 2.2 Supply — 航线覆盖分析

#### 按方向汇总：

| Brand Tier | TW始发 | →TW回程 | 其他国际线 |
|---|---|---|---|
| **Economy Basic** | 69.0% | 70.6% | 67.4% |
| **Economy Standard** | 74.5% | 78.0% | 72.8% |
| **Economy Up** | 76.8% | 80.2% | 74.4% |
| **Economy Discount** | **0.0%** | **0.0%** | 0.6% |

#### 按航线走廊逐方向：

**TW↔JP（最大走廊，1.19M traces 单方向）：**

| Brand Tier | TW→JP | JP→TW |
|---|---|---|
| Economy Basic | 66.9% → 68.6% (sel) ✅ | 65.1% → 63.0% ✅ |
| Economy Standard | 74.8% → 79.6% ✅ | 77.6% → 77.1% ✅ |
| Economy Up | 77.7% → 28.5% 🔴 | 81.8% → 36.2% 🔴 |
| Economy Discount | **0.1%** 🔴 | **0.1%** 🔴 |

**TW↔CN：**

| Brand Tier | TW→CN | CN→TW |
|---|---|---|
| Economy Basic | 68.1% → 69.4% ✅ | 51.5% → 50.7% ⚠️ |
| Economy Standard | 75.4% → 77.5% ✅ | 67.4% → 65.2% ⚠️ |
| Economy Up | 79.6% → 40.6% 🔴 | 73.2% → 29.5% 🔴 |
| Economy Discount | **0%** 🔴 | 0.1% 🔴 |

**TW↔HK：**

| Brand Tier | TW→HK | HK→TW |
|---|---|---|
| Economy Basic | 81.8% → 82.2% ✅ | 77.3% → 76.5% ✅ |
| Economy Standard | 84.1% → 86.3% ✅ | 81.0% → 80.8% ✅ |
| Economy Up | 85.6% → 27.4% 🔴 | 81.5% → 24.6% 🔴 |
| Economy Discount | **0.1%** 🔴 | **0.1%** 🔴 |

**TW↔TH：**

| Brand Tier | TW→TH | TH→TW |
|---|---|---|
| Economy Basic | 70.6% → 70.5% ✅ | 79.9% → 77.1% ✅ |
| Economy Standard | 78.2% → 80.4% ✅ | 83.9% → 83.4% ✅ |
| Economy Up | 79.6% → 26.8% 🔴 | 84.7% → 21.1% 🔴 |
| Economy Discount | **0%** 🔴 | **0%** 🔴 |

**TW↔US（长航线，关键市场）：**

| Brand Tier | TW→US | US→TW |
|---|---|---|
| Economy Basic | 72.2% → 68.6% ✅ | 70.1% → 67.6% ✅ |
| Economy Standard | 75.4% → 29.0% 🔴 | 77.9% → 32.0% 🔴 |
| Economy Up | 78.8% → 24.1% 🔴 | 80.0% → 25.1% 🔴 |
| Economy Discount | — | — |

**非 TW 航线（中转/第五航权，1.26M traces）：**

| Brand Tier | Supply Cov | → Selection Cov | Filter Drop |
|---|---|---|---|
| Economy Basic | 67.4% | → 63.5% | −3.9pp ✅ |
| Economy Standard | 72.8% | → **42.3%** 🔴 | −30.5pp |
| Economy Up | 74.4% | → 23.7% 🔴 | −50.7pp |
| Economy Discount | 0.6% | → 0.1% 🔴 | — |

**Supply 层结论：**

与 NH 不同，BR 的 supply coverage 在所有方向保持一致（65-85%），**没有明显的方向性限制**。这是合理的——BR 只有一个 hub（TPE），不像 NH 有日本始发 vs 其他始发的产品线分化。

- Basic/Standard/Up 的 supply 在 65-85% 区间，不算差但也不算好——说明品牌运价映射存在但覆盖率中等
- Discount 是唯一的全局 0% supply 问题
- **非 TW 航线**（如 ID-JP、HK-JP、TH-JP、PH-US 等经 TPE 中转）的 supply 和 selection 都更差——可能是中转航线的 brand mapping 复杂度更高

---

### 2.3 Fare Selection — 比价过滤 🔴

这是 BR 五层中最严重的问题。

#### Standard 的过滤：方向性分明

| 方向 | Standard Supply | → Selection | Filter Drop |
|---|---|---|---|
| TW始发（亚洲短途）| 74-84% | → 78-86% | +1~5pp ✅ |
| →TW回程（亚洲短途）| 68-84% | → 65-83% | −0~3pp ✅ |
| TW→US | 75.4% | → 29.0% | **−46.4pp** 🔴 |
| US→TW | 77.9% | → 32.0% | **−45.9pp** 🔴 |
| 其他国际线（中转）| 72.8% | → 42.3% | **−30.5pp** 🔴 |

**Standard 是"两个完全不同的表现"：**
- 亚洲区域线（TW↔JP/KR/HK/TH/VN）：filter drop 极小（0-5pp），比价基本保留 Standard
- 长航线 + 非 TW 航线：Standard 被大幅过滤（30-50pp）

#### Up 的过滤：全局性且严重

| 方向 | Up Supply | → Selection | Filter Drop |
|---|---|---|---|
| TW→JP | 77.7% | → 28.5% | **−49.2pp** 🔴 |
| TW→HK | 85.6% | → 27.4% | **−58.2pp** 🔴 |
| TW→TH | 79.6% | → 26.8% | **−52.8pp** 🔴 |
| TH→TW | 84.7% | → 21.1% | **−63.6pp** 🔴 |
| HK→TW | 81.5% | → 24.6% | **−56.9pp** 🔴 |
| KR→TW | 72.4% | → 61.5% | −10.9pp |
| GB→TH | 83.0% | → 22.6% | **−60.4pp** 🔴 |
| 其他国际线 | 74.4% | → 23.7% | **−50.7pp** 🔴 |

**Up 在所有航线都被严重过滤。** KR→TW 例外（−10.9pp），这是一个值得研究的 case——为什么 KR→TW 的 Up 被保留而其他航线被过滤？

共同规律：**BR 的比价过滤模式与 CI 高度一致**（CI 的 Flex 也是全局 −69pp）。这说明台湾航司的高端 Economy tier 在 Trip.com 的比价系统中面临相同的结构性劣势。

#### 需排查的具体异常 case：

| CP | Brand | Filter Drop | 值得关注的信号 |
|---|---|---|---|
| HK→TW | Standard | **+0.3pp** ✅ | 比价后反而出现了更多？ |
| HK→JP | Standard | **−37.1pp** 🔴 | 经 TPE 中转，比价严重过滤 |
| ID→JP | Standard | **−14.4pp** ⚠️ | 经 TPE 中转 |
| GB→TH | Standard | **−47.1pp** 🔴 | 经 TPE 的欧洲-泰国线 |
| HK→US | Standard | **−49.1pp** 🔴 | 经 TPE 中转 |
| KR→TW | Up | **−10.9pp** ✅ | 唯一 Up filter drop <20pp 的航线 |
| TW→PH | Up | **−32.6pp** | 短途中最健康的 Up |

---

### 2.4 Ranking — 不是瓶颈，因为问题在上游

**升舱经济学（TPE→NRT 为例）：**

| | Basic → Standard | Basic → Up |
|---|---|---|
| 多付 | **+TWD 4,780 (+50%)** | **+TWD 10,895 (+114%)** |
| 得到 | 多 1 件行李 + 改签省 TWD 1,080 + 退票省 TWD 1,550 + 提前选座 | 改签免费 + 退票省 TWD 3,100 + 免费提前选座 |
| 理性判断 | 除非确定要托运第二件行李**且**改签**且**退票，否则 ROI 为负 | 除非确定要改签，否则 ROI 为负 |

> **Note 2 进一步削弱升舱价值：** 起飞前 48 小时内，所有 tier 均可通过线上/手机值机免费选标准座位和特选座位。这意味着 Standard/Up 的「免费选座」优势仅在"提前 >48h 锁定座位"这个场景有效——对大多数休闲旅客来说，这项权益几乎不值钱。

**核心逻辑被官网数据确认：BR 的 Basic 已经包含 1 件托运 + 可付费退改。** 对于大多数短途旅客（一人一箱、不改签不退票），Basic 就是理性最优解。Standard 的 +50% 价格换回来的东西，用户只能通过"非自愿行为"（改签、退票、多带行李）来兑现——而这些行为大概率不会发生。

**这和 NH 的根本区别：**

| | NH Value→Standard | BR Basic→Standard |
|---|---|---|
| 价格差 | +1~10% | **+50%** |
| 行李增量 | 1 件 → 2 件（翻倍） | 1 件 → 2 件（翻倍） |
| 改签弹性增量 | 不可 → 付费 | 付费 → 付费（仅降价） |
| 最小升舱理由 | "多一件行李" | "我确定要改签或者退票" |
| 用户决策 | 高频需求，ROI 清晰 | 低频需求，ROI 模糊 |

**结论：BR 21.1% 的 upsell rate 不是 Ranking 或 Display 的问题，而是产品设计本身就决定了 Basic 对大多数用户是理性最优。** Standard 存在的意义不是让 Basic 用户升舱——而是捕获那些"本来就打算买 Standard"的用户（家庭出行、商务报销、里程玩家）。这个池子天然就小。

### 2.4.1 Product Design Ceiling：BR 的设计哲学

**BR 的 fare family 不是为了"让 Basic 用户升舱"，而是为了市场分割（price discrimination）。**

| | Trip.com 的 Upsell 思维 | BR 的设计思维 |
|---|---|---|
| Basic | 最低价，应该被推动升级 | **最大客户群**——价格敏感休闲旅客 |
| Standard | 升级目标 | **不同的客户群**——需要两件行李的家庭、轻度商务 |
| Up | 高端升级目标 | **报销制商务客**——免费改签是刚需 |
| Discount | 可能是促销 | **对抗 LCC 的价格武器**——0% 里程 + 不可退 |


**各 tier 的目标用户画像：**

| Tier | 典型用户 | 为什么选这个 |
|---|---|---|
| Discount | 纯价格驱动，无行李需求 | 拼最低价，和 LCC 比价时出现 |
| Basic | 休闲单人出行 | 一箱一包、不改签、价格敏感 |
| Standard | 家庭出行 / 轻度商务 / 里程玩家 | 需要两件行李（家庭），或用里程升舱（里程玩家），或公司差旅标准要求含行李 |
| Up | 报销制商务客 / 高频出行 | 免费改签是刚需，里程 100% 累积，选座提前锁定 |

**这意味着：**

1. **BR 不需要让用户从 Basic 升到 Standard。** 他们需要的是让愿付高价的用户进高价池，让只愿付低价的用户进低价池，互相不干扰。

2. **Standard 订单仅 5.3% 不是因为用户看了不买——而是这个群体天然就小。** 亚洲短途线上家庭出行占比低，商务客要么选 Up（报销制），要么公司直接签批团票。

3. **BR 21.1% 的 upsell rate 是策略正确的结果，不是系统缺陷。** 在 Trip.com 上买 BR 机票的用户，大多数就是 Basic 的目标用户。他们选 Basic 不是"错过了升舱机会"——这个产品就是为他们设计的。

**对 Trip.com 的启示：** 强行提高 BR 的 upsell rate（排序操纵、展示优化）可能适得其反——推动不合适的人买 Standard 会导致高退货率、客服纠纷，且与 BR 的品牌策略冲突。BR 是本次 audit 中"产品设计天花板"的标准案例：**不是每个低 upsell rate 的航司都是 Trip.com 的错。**

---

### 2.5 Display — 待验证，但不是瓶颈

- **Void/24h：** BR 不受 void/24h 限制（仅 0.1% 订单受影响，702 单）。✅
- **权益差异展示：** 待验证。Basic vs Standard vs Up 的权益差异（行李 1→2 件、改签费降低、座位免费、里程累积率）是否在运卡上清晰可见？
- **但即使展示完美，升舱经济学也不变。** TPE→NRT 的 Basic→Standard 仍然需要用户为"第二件行李 + 大概率不发生的改签"多付 50%。展示改善可能在边际上有帮助，但不是 needle mover。

#### Upsell Rate 口径校验：

- NULL 订单不是 Discount，而是 unmapped Basic/Standard/Up。Baggage/flexibility/channel 分布与 tagged 订单完全一致
- Discount 确实存在（官网确认 A 舱），但量很小——BQ 中仅 ~900 单匹配 Discount profile（fare only + 不可退），且短途线上 Basic 和 Discount 行李权益相同（均 1 件），在 baggage 字段层面无法区分
- 修正 brand mapping 不会改变 upsell rate——只会让 137,888 单从盲区变为可见，但并不改变这些订单的 tier 构成
- **BR 21.1% upsell rate 的真实性：** 如果 NULL 中 Basic/Standard/Up 的比例和 tagged 订单一致（~73% Basic），那 21.1% 接近真实值——不是数据问题，是产品设计问题

---

## 3. BR 官网 Fare Family 结构（2026-07-21 人工验证）

### 3.1 四层产品完整对比

> 数据来源：EVA Air 官网 Fare Family 页面 + TPE→NRT 实际搜索结果。

| 权益维度 | Discount (轻便, A舱) | Basic (基本, V/W/S) | Standard (经典, Q/H/M) | Up (尊爵, B/Y) |
|---|---|---|---|---|---|
| **里程累积** | 0% | 50% | 75% | 100% |
| **托运行李（长途）¹** | 1 × 23kg | 2 × 23kg | 2 × 23kg | 2 × 23kg |
| **托运行李（短途）¹** | 1 × 23kg | 1 × 23kg | 2 × 23kg | 2 × 23kg |
| **预选座位²** | 付费 | 付费 | 标准座位免费 | 标准+特选座位免费 |
| **里程升舱** | 不允许 | 不允许 | 允许 | 允许 |
| **改签** | 付费 | 付费 | 付费 | **免费** |
| **退票** | **不允许** | 付费 | 付费 | 付费 |
| **未登机费³** | 付费 | 付费 | 付费 | 付费 |

> ¹ 长途：往返美国、加拿大、欧洲、澳洲、新西兰。短途：亚洲区内。
> ² **关键：起飞前 48 小时内，所有 tier 均可通过线上/手机值机免费选标准座位和特选座位。** 这意味着预选座位的权益差异仅在"提前 >48h 选座"这个场景下有效。
> ³ 未取消订座也未登机，后续办理改签或退票时收取。

### 3.2 TPE→NRT 实测价格（短途）

| | Basic (V舱) | Standard (Q舱) | Up (B舱) |
|---|---|---|---|
| 价格 | TWD 9,559 | TWD 14,339 (**+50%**) | TWD 20,454 (**+114%**) |
| 改签费 | TWD 2,480 | TWD 1,400 | 免费 |
| 退票费 | TWD 4,960 | TWD 3,410 | TWD 1,860 |
| 行李 | 1 × 23kg | 2 × 23kg | 2 × 23kg |

> **Discount 在 TPE→NRT 当天搜索结果中未出现**——可能该日期 A 舱售罄，或短途线上 BR 优先展示 Basic。

### 3.3 官网验证 × BQ 数据交叉确认

| BQ 推断 | 官网实测 | 结论 |
|---|---|---|
| 4 层 tier | ✅ 4 层：Discount/Basic/Standard/Up | 全部真实存在 |
| Discount 0% coverage | Discount 存在但不一定每条线出现 | 不是 mapping 错误，是该 tier 量小 |
| 所有 tier 含托运 | ✅ 确认，最少 1 件 | `baggage_allowance_group` 区分不了 1 件 vs 2 件 |
| 退改全部 paid | ✅ 确认，差异在**费用金额** | 只有 Up 改签免费，Discount 不允许退票 |
| Up free_change 30.6% | ✅ 确认，Up 改签免费 | 这个 signal 可以用来从 NULL 中识别 Up |

---

## 4. 五层总结与优先级

### 4.1 逐层评估

| 层 | 发现 | 严重度 | 可操作性 |
|---|---|---|---|
| **Data Foundation** | 🔴 74.7% 订单 brand_name NULL + Discount 0% coverage | 严重 | **高**——ATPCO mapping fix 可解决 |
| **Supply** | ⚠️ 全 tier 65-85%，中等水平；Discount 1.02M traces 无映射 | 中等 | 中——mapping 完善后可改善 |
| **Fare Selection** | 🔴 Up −48.5pp（全局） + Standard 长航线 −30~50pp | 严重 | 中——Up 定价 +114%，部分过滤可能合理 |
| **Ranking** | ✅ 不是瓶颈——升舱 ROI 由产品设计决定，非排序 | 轻微 | 低 |
| **Display** | ✅ 不受 void/24h 影响；展示改善有帮助但不是 needle mover | 轻微 | 低 |
| **Product Design** 🔴 | **BR 的 Basic 太强，升舱经济学不支持大规模 upsell** | **最严重** | **低**——Trip.com 无法改变航司定价 |

### 4.2 BR vs NH 对比

| 维度 | NH | BR |
|---|---|---|
| 核心瓶颈 | **Ranking + Display** | **Product Design + Data Foundation** |
| 为什么升不上去 | Standard 存在、定价合理、但用户看不到 | Standard 定价 +50%、用户看到也不会选 |
| NULL brand_name | 37% | **74.7%** |
| Trip.com 能修复 | ✅ Ranking/Display 改善可显著提升 | ⚠️ 修好 Data Foundation 能看清问题，但不能解决升舱动力 |
| 航司产品特征 | Value→Standard 多一件行李，仅 +1~10% | Basic→Standard 多加一件行李+降改签费，但 +50% |

### Action Plan

**战略定调：** BR 21.1% upsell rate 不是 Trip.com 的问题——是产品设计问题。Basic 已经足够好（1 件行李 + 付费退改），升到 Standard 要多付 50%，理性用户不会升。**修复 Data Foundation 能看到全貌，修复 Fare Selection 能让 Up 出现——但都改变不了升舱经济学。** 真正的 needle mover 是 NH（Trip.com 可以修 Ranking/Display 来解锁已有潜力），而不是 BR（潜力本身就被航司产品设计锁死了）。

**P0 — 立即行动：**

1. **ATPCO mapping 修复：** 目的是让 74.7% NULL 订单可见——不是为了提升 upsell rate，而是为了能正确分析 BR。Discount 的 `officialbrandname` 大概率也是 NULL（类比 NH Light）。
2. **74.7% NULL 订单溯源：** 查询 segment 表 BR 订单的 `atpco_brand_name` 填充率。

**P1 — 近期：**

3. **Up tier 比价过滤排查：** 与 FBU/比价团队确认——Up 定价 +114%，被比价过滤是否合理？如果比价逻辑是正确的（过滤不合理定价），那么保留现状是正确的用户保护行为。
4. **Standard 长航线过滤：** TW↔US、非 TW 中转航线 Standard filter drop 30-50pp——需确认根因。长航线上 Standard 的 2×23kg（vs Basic 的 2×23kg）行李权益无差异，其他差异（座位、改签费）是否值 +50%？
5. **再查 1-2 条航线验证定价 pattern：** TPE→HKG（短途高频）、TPE→LAX（长途），确认 +50% 是统一比例还是航线差异。

5. **人工走查 BR 官网：** 同 NH scraper 流程——确认四层 fare family 结构、权益差异、定价基准（+1 月/+3 月，OW 1pax）。

**P2 — 验证：**

6. **Standard 排序/定价诊断：** 在亚洲区域线（Standard selection 80%+ 但订单 5.3%），拉定价数据确认 Standard vs Basic 的 price gap。如果价差合理但订单低 → 排序/展示问题；如果价差过大 → 定价竞争力问题。

---

## 5. 数据附录

### 订单表 NULL brand_name Top CPs：

| CP | NULL 订单量 |
|---|---|
| JP→TW | 11,805 |
| TW→JP | 9,352 |
| TW→CN | 6,594 |
| TW→PH | 4,540 |
| HK→TW | 4,419 |
| TW→VN | 4,416 |
| TW→TH | 4,291 |
| TW→KR | 4,023 |
| TW→HK | 3,464 |

这些 NULL 订单集中在 BR 的核心航线——说明 brand mapping 问题在 BR 最赚钱的航线上影响最大。

### Global Summary：

| Metric | Value |
|---|---|
| 总订单 | 485,357 |
| Upsell 订单 | 96,725 |
| Upsell Rate | **21.1%** |
| NULL brand % | **74.7%** |
| Void/24h 受影响 | 0.1%（可忽略）|

### Coverage Global Summary：

| Brand Tier | Supply Cov | Sel Cov | Filter Drop | Tier (推测排序) |
|---|---|---|---|---|
| Economy Discount | 0.0% | 0.0% | 0.0pp | 最便宜（缺失） |
| Economy Basic | 69.0% | 68.7% | −0.3pp | 便宜 |
| Economy Standard | 74.9% | 68.1% | −6.8pp | 中等 |
| Economy Up | 77.0% | 28.5% | −48.5pp | 最贵 |
