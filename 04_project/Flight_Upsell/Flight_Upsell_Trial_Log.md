# Flight Upsell Trial Log

---

## Session 1 — 2026-06-16

**Topic:** Void / 24h Free Cancel Display Override — Initial Quantification (EY)

**Context:**
Product owner shared Oliver Tang's SQL for pulling void/24h policy data from orders. Michael identified that certain tickets display a "24-hour free cancellation" label that overrides the ticket's true refund policy, potentially misleading users and suppressing upsell.

**Key Decisions:**
- Confirmed data source: `trip-ibu-adhoc.ibu_adhoc_temp.MZ_202606_quantification_v2` (pre-aggregated BQ table, 2025-01-01 to 2026-05-31)
- Confirmed metric definitions: upsell rate = `upsell_primary_ord_count / upsell_base_primary_ord_count`; policy share = `free_cancel_or_void_ord_count / primary_ord_count`
- Scoped initial analysis to EY + flagged AA, UA, DL as next priority

**Core Finding (EY, 2026 Jan–May):**
- 88% of EY orders have void/24h policy in the backend
- Of those orders, **86.7% have a ticket that is actually non-refundable** (73.3% Change Only + 13.4% Not Flexible)
- Only 13.3% of orders showing "free cancellation" have a genuinely Flexible ticket
- Absolute scale: ~144,000 users potentially misled in 5 months, EY alone

**Analytical Insight:**
- Initial hypothesis (void/24h suppresses upsell) could not be proven with simple group comparison — the `no_policy` group has lower upsell (56.1%) due to selection bias (structurally different products), not because void/24h boosts upsell
- Reframed: the real issue is **display accuracy**, not upsell rate delta. The customer trust angle is the stronger business case

**Framing for Leadership:**
> "In the first 5 months of 2026, at least 144,000 EY customers saw '24-hour free cancellation' on a ticket that was actually non-refundable after that window. The same display logic also removes the refundability signal that would motivate upgrades to Flexible fares — both problems have the same fix."

**Blockers:**
- BQ not accessible from Claude Code sandbox (corporate proxy blocks googleapis.com CONNECT tunnels) — queries run manually by Michael, results pasted back
- Display trigger logic not yet obtained from FBU PM

**Food for Thought:**
- The `no_policy` group (56.1% upsell rate) might actually be the most interesting segment — these are likely routes/airlines where the supply connection is incomplete. If fixing display also surfaces proper brand fare ladders on those routes, the upsell uplift could be larger than expected.
- UAE (ae) is anomalous for EY: lowest void/24h display rate (72%) among top markets. Could be the natural control group for isolating display effect vs. other factors.

**Next Session Focus:**
- Replicate flexible breakdown query for AA, UA, DL
- Run airline-level overview (Q3) to find other high-impact airlines
- Resolve BQ access from Claude Code (try new session without sandbox network restriction)

**Full analysis doc:** `void_policy_display_analysis.md`

---

## Session 2 — 2026-06-16

**Topic:** Void/24h Display Override — AA/UA/DL Replication + Full-Airline Sizing + EY Region Analysis

**Context:**
Continuing from Session 1. BQ now directly accessible from Claude Code (no sandbox proxy block). All queries run against `trip-ibu-adhoc.ibu_adhoc_temp.MZ_202606_quantification_v2`.

**Key Findings:**

**AA / UA / DL replication:**
EY finding fully replicated across all three US carriers. Misled % of void (non-refundable tickets covered by void/24h label):

| Airline | Misled Exposed | Misled % of Void |
|---------|---------------|-----------------|
| EY | ~140K | 86.4% |
| UA | ~47K | 90.3% |
| DL | ~33K | **92.7%** — most extreme |
| AA | ~26K | 83.3% |
| **Total** | **~246K** | — |

**Booking channel analysis:**
Channel differences are a matter of degree, not binary. TF-WS is the most severely affected channel (AA/UA Not Flexible tickets ~97–100% covered). 1A-WS is relatively lowest but still 60–77%. No channel has a near-zero override rate.

**Important clarification — these numbers are upper bounds:**
We measure "backend has void/24h policy record AND ticket is non-refundable." Whether the frontend actually displayed the void/24h label depends on FBU's display trigger logic, which is unknown. 246K is a risk exposure ceiling, not a confirmed misled user count.

**Source + subchannel exploration:**
Explored `edw_ord_flt_order` `source` + `subchannel` fields (format: `ENGLISHSITE_17`) to identify frontend display differences. Built extended table `MZ_202606_quantification_cc` with these dimensions added. However, void/24h fields are all 0 in the new table — the `f_textdetail` CTE uses `DATE(d) = yesterday` snapshot filter, so today's run cannot retrieve historical policy tokens. Source/subchannel dimensions are correct; void/24h metrics are invalid. Needs Oliver Tang to re-run at original timestamp.

**Full-airline risk exposure ranking:**
All airlines ≥500 orders: top 40 misled_exposed total >1.7M orders. Priority tiers:
- **P0** (high volume + high misled% + healthy upsell rate): EY, WS, UA, BA, AC
- **P1** (large volume, different structure): TG, TK, LH, SK
- **Structural anomaly**: KE — 83.7% void/24h coverage but only 12.9% misled rate (mostly genuine Flexible tickets, low actual risk)

**EY airport pair × region upsell rate analysis:**
Upsell rate spread of 28–45pp across regions on the same route (e.g. JED→CGK: id 96.3% vs sa 69.2%; IST→BKK: th 95.7% vs tr 61.4%). Key finding: void/24h coverage is uniformly high across regions on most routes (both high and low upsell regions have 85–99% void/24h exposure), meaning the upsell spread reflects structural demand differences (e.g. Indonesian migrant workers vs Saudi local buyers), not differential override rates. Hypothesis not confirmed by current data; closest case is KUL→RUH / id (void/24h 37.2%, upsell 40%).

**Display trigger hypotheses — all parked:**
Three open hypotheses, none excludable without FBU confirmation:
1. Booking channel (GDS connection layer)
2. Agency contractual/technical configuration
3. Locale/region regulatory requirements (EU consumer protection, US DOT 24h rule)

**Blockers:**
- FBU display trigger logic still not obtained — critical to convert upper-bound to confirmed numbers
- `MZ_202606_quantification_cc` void/24h data invalid — needs Oliver Tang to re-run at original timestamp

**Food for Thought:**
- EY has highest repair ROI for a counter-intuitive reason: 79% upsell rate was achieved *despite* the wrong label (users upgraded for baggage/other reasons). Fixing the label adds a refundability signal on top — rate can only go higher, not lower
- >1.7M upper-bound across all airlines means this is a systemic display logic issue, not isolated to 4 carriers. One fix covers everything
- To establish causality (void/24h label actually suppresses upsell), cleanest method is a controlled experiment: disable the label on specific routes/regions and measure before/after upsell rate change

**Full analysis doc:** `void_policy_display_analysis.md`

---

## Session 3 — 2026-06-16

**Topic:** Upsell Project — Overall Diagnostic Framework Review & Needle Mover Positioning

**Context:**
Continuing from Sessions 1–2 (void/24h quantification work). This session stepped back from the specific EY/AA/UA/DL analysis to examine the full diagnostic framework and whether it holds up structurally. Also the first session in which team positioning and opportunity type selection were explicitly discussed.

**Key Findings:**

**Framework: five layers, not four**
Ranking confirmed as a distinct layer between Fare Selection and Display. ~80% of users only view top 3 Fares; a correctly-selected Fare ranked 12th has 100% Coverage Rate but near-zero visibility. Coverage Rate cannot detect Ranking problems.

**Three structural weaknesses confirmed:**
1. Coverage Rate denominator is unknown — cannot distinguish "we failed to source it" from "airline never offered it." Coverage Scraper is a partial workaround (airline website as external ground truth) but manually triggered, not systematic.
2. Supply connection configuration is a black box — official connection ≠ correct configuration. Internal mapping may be stale without knowing.
3. Upsell Rate denominator has passive upsell contamination — sold-out lowest tier or route with no low-tier option inflates the rate without reflecting true conversion.

**Fare Family design as precondition:**
Fare Family structure (stepped jump vs gradual vs LCC bare fare) is not a funnel layer — it's a precondition. If design lacks upsell motivation, fixing any downstream layer yields limited ROI. Must be assessed before committing to funnel diagnostics.

**KPI comparability:**
Upsell Rate absolute values are not safely comparable across any dimension (cross-airline, cross-route, cross-market). Most reliable comparison is same cell over time. Framework output = directional hypothesis, not confirmed conclusion. Validate with experiments.

**Priority ordering principle updated:**
"Upper layer first" holds — but only for confirmed problems. If upper-layer problem is unconfirmed, lower-layer fixes (e.g., Display) should not be blocked. Two-step: diagnose first, then prioritize among confirmed problems.

**Two types of needle mover:**
- Type 1 (Volume Capture Gap, EU story model): requires external benchmark + airline-by-airline deep dive → more suited to market teams
- Type 2 (Revenue Quality Gap, void/24h model): internal data only, globally uniform logic, single fix covers all airlines → better fit for Global Strategy team mandate

**Team positioning confirmed:**
Global Strategy team needs global-scale, system-level opportunities. Type 2 (void/24h) is the stronger candidate: 1.7M+ upper bound, no market customization needed, one display logic fix covers 40+ airlines.

**Blockers:**
- FBU display trigger logic still not obtained (needed to convert 1.7M upper bound to confirmed number)
- Oliver Tang re-run still pending (`MZ_202606_quantification_cc` void/24h data invalid)

**Food for Thought:**
- The framework's value is not precision — it's narrowing the search space. Best guess → experiment → correct. Don't over-invest in making the framework perfect before it's been used.
- Fare Family design mapping for 40+ airlines is the biggest unresolved precondition. Without it, low upsell rate interpretation on any airline remains ambiguous.
- Today's discussion clarified what Manager's emphasis on Quantification / Prioritization / Needle Mover actually means in practice: not analytical precision, but a clear selection standard for what's worth the team's attention at all.

**Full framework doc:** `upsell_diagnostic_framework.md`

---

## Session 4 — 2026-06-22/23

**Topic:** Fare Family Design × 24hr Suppression — EY / UA / AC Case Studies + Meeting Page Preparation

**Context:**
Continuing from Sessions 1–3 (void/24h quantification). This session shifted from data quantification to fare family design analysis — pairing airline-level BQ data with actual fare family screenshots to understand what drives upsell at each upgrade step, and what 24hr suppression actually eliminates. Prompted by Jay asking: "what is the implication, and why do we want to include EY or UA?"

---

**Key Findings:**

**Upgrade step anatomy framework:**
Each fare upgrade step can be classified by benefit composition: bag-only, pure refundability, or mixed. The 24hr label fully suppresses only the pure refundability steps. Mixed steps (bags + refund) are only partially suppressed — bag incentive remains. This framework answers Jay's question: the airlines with the most pure-refundability steps immediately above the most-purchased tier are the highest ROI targets.

**EY (lead case):**
- 4-tier structure: Basic / Value / Comfort / Deluxe — uniform across all international routes
- Basic → Value: bag-driven (25kg added). Value → Comfort: pure refundability (only new benefit)
- 24hr suppresses the Value → Comfort step entirely — the sole motivation is the refund signal
- Price to first refundability: +13.4% on long-haul (JED-CGK), +29.9% on short-haul (AUH-BOM) — accessible, not a pricing ceiling issue
- Current fares carry a temporary first-change-free overlay (Middle East waiver) — does not affect refundability analysis
- BQ: Basic and Value both map to `2. Change Only` (both non-refundable). Comfort and Deluxe collapse to `4. Flexible` — indistinguishable
- 86.7% of 109,541 orders are non-refundable. Upsell rate 79% achieved despite wrong label (baggage-driven). Fixing label adds refund signal on top — rate can only increase
- **Conclusion: simplest structure, largest misled volume, highest upsell rate → lead case**

**UA (validation case):**
- 4 cabin tiers (Economy / Economy Plus / Premium Plus / Polaris) × 3 sub-tiers (Basic / Standard / Flexible)
- Economy Plus is NOT a separate cabin class — still economy, just extra legroom rows. Conflated with flat economy in BQ under `cabin_IATAcode = 'Y'`
- Both domestic and international: Standard → Flexible is pure refundability (bags fully exhausted at Basic → Standard step)
- Domestic: 25% of volume, void display (US purchase market). International: 75%, 24hr display
- RouteType field in BQ: ~13,800 domestic, ~41,700 international
- One suppression point vs. two for EY. More complex narrative — validated as replication case, not lead

**AC (structural complexity case):**
- 5-tier economy: Basic / Standard / Flex / Comfort / Latitude
- **Critical route-type correction:** Flex is non-refundable on domestic and US routes (refundability only appears at Comfort, tier 4). On international, Flex is refundable (first refundability at tier 3)
- US origin/destination carved out: 14,144 orders — follow domestic fare structure, not international
- Revised volume: 46% true international (2 suppressed tiers), 54% domestic+US (3 suppressed tiers — deepest suppression of the three airlines)
- Flex, Comfort, Latitude all collapse to `4. Flexible` on international routes — cannot distinguish which tier customers chose in BQ
- 86.6% non-refundable, upsell rate 44.8%

**Jay's question — crystallised answer (Michael's three bullets):**
1. 4% of global FSC orders impacted — one display fix is systemic across all airlines simultaneously
2. Per-airline impact varies by fare family design — case studies show which airlines are highest ROI and why
3. Current upsell% KPI will not capture the improvement — customers moving between tiers already counted as "upsold" are invisible. Correct metric for any A/B test: Flexible-tier share or average revenue per economy order

**KPI blind spot (sharpest insight for J):** Even a successful display fix may appear flat in headline upsell%. The measurement design must be scoped correctly before the test runs.

---

**Documents Updated:**
- `void_policy_display_analysis.md` — new section appended: "Fare Family Design Analysis: Why Suppression Depth Varies by Airline" (upgrade step framework, full EY/UA/AC breakdowns, three-airline comparison table, four cross-airline takeaways)
- Lark meeting page draft prepared (Sections 1–3) covering mutual exclusivity, display rules, and fare family analysis — not yet posted (Feishu CLI auth parked)

---

**Blockers (unchanged):**
- FBU display trigger logic not obtained — 1.7M remains upper bound
- Oliver Tang re-run still pending (`MZ_202606_quantification_cc` snapshot filter issue)
- Revenue leakage quantification still not done — fare delta × conversion lift for EY

---

**Food for Thought:**
- The upgrade step anatomy framework applies beyond EY/UA/AC — it's the filter for ranking all 40+ audit airlines by suppression ROI. Next step is applying it systematically rather than case-by-case
- AC's 54% domestic+US volume in the deeper 3-tier suppression structure means AC's total opportunity may be larger than the simple non-refundable % suggests — worth quantifying separately
- The "temporary waiver" dynamic at EY raises a question: if change rights are temporarily free across all tiers, does the refundability step (Value → Comfort) become even more salient for customers? They already have free changes — the only remaining reason to upgrade is the refund right, which 24hr is masking

---

## Session 3 续 — 2026-06-17

**Topic:** Brand Fare Audit 工作流细节 + Coverage Scraper 开发

**Key Context Added:**

**当前执行路径（已在运行）：**
- 筛选逻辑：行李组合 % < benchmark → 看 Upsell Rate → 验证 Fare Family 设计 → 漏斗逐层排查
- 范围：Economy class only，FSC Long Haul；W/F/J 舱不在本次范围
- 优先级：P0 = Supply 缺失；P1 = Fare Selection 过滤问题 + Void/24h；P2/P3 = 其他 Display 问题
- 优先级升级的关键：量化（Quantification）——Void/24h 能到 P1 是因为有 1.7M upper bound；其他 Display 问题停在 P2/P3 是因为还未量化

**Display Issues 列表（2026-05 归类）：**
8 个已发现问题，全部 P2/P3。核心类型：属性准确性问题（展示 vs 官网不一致）、品牌名缺失、相似权益价差过小（Fare Selection 层问题借用 Display 标签）、TK free 24h cancellation 未展示（Void/24h 的镜像问题）。

**商务合规约束（新增维度）：**
- AF/KL 类：所有市场必须严格展示官方 Brand Fare，名称/权益/顺序完全一致
- AA/DL/LH 类：本土市场（US/DE）同样严格；非本土市场可插入 non-standard fare
- 影响：对 AF/KL 和 AA/DL/LH 本土市场，Coverage Rate 低 = 更硬的问题（无 self-bundle 缓冲）；且这些市场的 Coverage Rate 可解读性最高（无分母污染）

**Self-bundle 与 Gambling Fare 的 Coverage Rate 影响：**
- Coverage Rate 计算：只要 source fare 是 Brand Fare 就计入 covered，不管是否被用作 gambling 或 bundle
- 数据库有 gambling flag，可以分别计算含/不含 gambling 的 coverage rate
- Flexibility Bundle 数据尚未纳入（只有 baggage bundle），Oliver Tang 正在对接中
- Void/24h 与 Flexibility Bundle 应该互斥（不同 display path）——1.7M upper bound 无 Flexibility Bundle 污染风险

**Audit 工作流（5 步）：**
Step 0 准备数据 → Step 1 Brand Mapping 验证（官网 vs Trip 映射）→ Step 2 Coverage 分析（<80% OD 筛选）→ Step 3 Manual Validation（官网对比，区分可修/不可修 gap）→ Step 4 全市场 knowledge transfer

需要亲自做的 4 个市场：日本、北美（US/CA）、土耳其、墨西哥/南美——目前全流程人工。

**Coverage Scraper 开发状态：**
- TK v1（CDP 模式）：已有历史数据（IST→NAV/AYT/ASR/VAN 各 3 日期 OW）
- TK v2（新建）：Path B（自有 Chromium）→ Path A（CDP）fallback；加入 OW + RT 逻辑
  - 文件位置：`Flight Upsell/audit/TK/fetch_fares_tk_v2.py`
  - 首次运行：Path B 成功启动，但日历选择器无法打开
  - 根因：cookie banner 未处理 + 机场选择后表单未完全加载
  - 修复中：加入 cookie banner 自动 dismiss + 表单可见性验证
- 所有文件已从 `/Documents/Audit/` 迁移至 `Flight Upsell/audit/`

**文件结构：**
```
Flight Upsell/audit/
├── routes.csv
├── CLAUDE.md / README.md
└── TK/
    ├── fetch_fares_tk_playwright.py  (v1, CDP)
    ├── fetch_fares_tk_v2.py          (v2, Path B→A fallback)
    ├── parse_tk_html.py
    ├── diagnose_tk.py
    ├── TK_fare_analysis_docs.md
    └── [历史数据 CSV + TXT]
```

**Blockers:**
- TK v2 日历 bug 修复中（已加入 cookie banner 处理，待重新测试）
- Flexibility Bundle 数据待 Oliver Tang 整合完成

**Food for Thought:**
- Scraper 的核心价值不在于 100% 自动化，而在于把"所有低 coverage OD 都要人工查"压缩成"只有和官网差距大的才需要人工查"
- AF/KL 等严格合规航司的 Coverage Rate 数字最干净，最值得优先 audit
- 本阶段策略：统一用 en-int 英语版官网（Phase 1），避免多语言维护成本；如需本土化验证另起专项
- RT-only fare 存在：OW + RT outbound leg 都跑，才能发现只在 RT 语境下出现的 fare tier

---

## Session 5 — 2026-06-24/25

**Topic:** Master Quantification Query — MZ + JN Merge, Architecture Discussion, BQ Refresh

**Context:**
Continuing from Session 4. Focus shifted from fare family analysis to the data infrastructure layer — merging MZ's order-counting query (`MZ_202606_quantification_v2`) with Jay's void/24h query (`JN_202606_void_24`) into a single master table. Goal: eliminate parallel maintenance burden and produce one canonical source for all void/24h + flexibility + baggage analysis.

---

**Key Decisions:**

**MZ vs JN comparison:**
- MZ advantages: cleaner counting logic (early `is_primaryorder = 1` filter, `GROUP BY + MAX()` flexible subquery prevents fan-out), richer analytical dimensions (baggage, RouteType, brand, bundle flexibility)
- JN advantages: `market` dimension (via `BD_ChannelConfigInfo`), `ownerairline`, `service_fee_type` (from `e_customer_cancellation`)
- Neither is objectively "better" — built for different purposes. Merge takes structural backbone from MZ, additional dimensions from JN

**`is_primaryorder` design choice:**
- MZ filters early (in `segment_table WHERE`) → policy lookup runs only against primary sub-order's orderid
- JN filters late (final SELECT) → policy can be picked up from return or connecting leg
- Decision: keep MZ's early-filter approach. Cleaner counting, no self-join inflation. Known trade-off: a round-trip where only the return leg has a void policy will be classified as NULL (no policy found). Edge case is rare since void/24h is typically a booking-level policy, not per-leg
- For primary order **count** only: no difference between the two approaches. Count is identical; only classification (void/24h tagging) could differ in rare round-trip edge cases

**8-point merge implemented in `Order.md`:**
1. Date range → `2026-01-01` to `2026-05-31`
2. `AND a.flightclass = 'I'` added (international orders only)
3. `is_primaryorder = 1` kept in segment_table WHERE (MZ approach, with design note in header)
4. `e_customer_cancellation` CTE added (from JN) → `service_fee_type` in output
5. `datachange_createtime >= "2025-12-01"` applied to both `f_textdetail` and `g_other`
6. MZ/JN quality assessed honestly — merged table takes best of both
7. `ownerairline` + `order_ticketing_airline_name` exposed in final SELECT (dimf2 join)
8. `x_BD_ChannelConfigInfo` CTE added (from JN) → `market` + `channelenname` in output

**BQ table refreshed:**
- `trip-ibu-adhoc.ibu_adhoc_temp.MZ_202606_quantification_v2` replaced successfully via `bq` CLI
- Runtime: ~79 seconds
- Table now covers Jan–May 2026, international only, with all merged dimensions

---

**Blockers (unchanged):**
- FBU display trigger logic not obtained — 1.7M remains upper bound
- Oliver Tang re-run (`MZ_202606_quantification_cc`) still pending
- Revenue leakage quantification still not done — fare delta × conversion lift for EY

---

**Food for Thought:**
- The merged table is now the single source of truth for all void/24h + flexibility + baggage analysis. Any future dimension additions should go into `Order.md` — one place to maintain
- `service_fee_type` from `e_customer_cancellation` is newly available — worth exploring whether it adds signal for classifying cancellation penalty severity (full forfeiture vs. partial fee), which could sharpen the "misleading label" narrative
- The `market` dimension enables a natural next cut: void/24h misled rate by market (CN vs HK vs SG vs EN-INT). If certain markets have dramatically lower override rates, that's potential evidence of locale-specific display trigger logic — the FBU question we've been trying to answer indirectly

---

**Documents Updated:**
- `Order.md` — merged master query (replaces previous MZ v2 with 8 added dimensions/filters)
- `trip-ibu-adhoc.ibu_adhoc_temp.MZ_202606_quantification_v2` — BQ table refreshed

---

**Next Session Focus:**
- Run void/24h analysis against the refreshed table (market + ownerairline dimensions now available)
- Explore `service_fee_type` distribution — does it add narrative value?
- Fill revenue leakage placeholder: fare delta (Non-Flexible → Flexible) × conversion lift for EY

---

## Session 6 — 2026-06-25

**Topic:** Void/24h FBU Alignment — Cross-BU Validation & H2 Roadmap Entry

**Context:**
Following Sessions 1–5 which established the void/24h finding and built the quantification infrastructure, Michael presented the finding to FBU counterparts. This session captures the outcome of that cross-BU discussion and its implications for next steps.

**Key Outcome:**

FBU confirmed the void/24h display override as a real issue. Alignment reached on the following:
1. This is a genuine user experience problem — the display of void/24h policy overriding the long-term refund policy misleads customers
2. Issue confirmed and added to H2 roadmap
3. Two solution directions under consideration:
   - **Display both** — show void/24h label alongside long-term refund policy simultaneously
   - **Redirect to detail page** — link to fare detail page where full policy is shown (precedent: Doris' hotel experience, confirmed as successful pattern)
4. No aligned solution yet — direction TBD
5. J/Michael to ensure correct metrics and scope (airline, market) when FBU designs and runs the ABT

**Why This Is a Milestone:**

This is a complete strategist loop delivered by IBU independently:
- IBU discovered the issue (FBU had not identified it previously)
- IBU quantified it (1.7M upper bound across 40 airlines; 144K EY alone)
- FBU confirmed it as a real problem upon presentation
- Finding entered H2 roadmap as a result

The 1.7M order volume was not discussed — FBU's alignment was based purely on the user experience argument, which is a stronger and more durable foundation for the business case.

**Upsell Implications of Two Directions:**
- Display both: adds refundability signal directly on the middle selection page → more direct path to Flexible-tier upsell
- Redirect: adds friction (user must click through) → lower conversion impact, but cleaner UI
- From upsell perspective, display both is the stronger intervention; redirect may be safer for FBU to implement first

**ABT Metrics — Guard Points for J/Michael:**
- Primary metric: **Flexible-tier share** (not headline upsell%) — void/24h fix targets refundability signal specifically; headline upsell% too broad and diluted by baggage upsell
- Secondary metric: **revenue per economy order**
- Recommended initial scope: **EY first** (88% misled rate; cleanest baseline data)
- Market dimension must be split: CN vs. HK/SG vs. EN-INT — different markets may have different display trigger logic

**Tracking Plan:**
Milestones to monitor:
- [x] FBU confirmed as UX issue
- [x] Added to H2 roadmap
- [ ] FBU aligns on solution direction (display both vs. redirect)
- [ ] FBU confirms ABT排期 (Q3 / Q4)
- [ ] ABT metrics aligned (J/Michael input before design finalized)
- [ ] ABT launches
- [ ] Results read

**H1 Narrative Update:**
The FBU alignment is independently usable in the H1 review narrative — does not require revenue leakage number to be filled:
> "The analysis drove cross-functional alignment — FBU confirmed the issue and added a fix to H2 roadmap. ABT design is next, with IBU involved in metrics spec."

**Food for Thought:**
- The key risk is FBU designing the ABT without IBU input on metrics — if primary metric is set to headline upsell%, the test may show neutral results even if Flexible-tier share improves. Intervene early in the design phase, not after.
- Redirect direction (detail page) has hotel precedent (Doris). Worth asking: in the hotel case, what was the measured uplift from redirect vs. inline display? That data could inform which direction FBU chooses.
- The timing of FBU's H2 execution is uncertain — tracking milestone 3 (solution direction aligned) is the next concrete gate.

**Documents Updated:**
- `Flight_Upsell_Trial_Log.md` — Session 6 appended

**Next Session Focus:**
- Run void/24h misled rate by `market` against refreshed BQ table
- Explore `service_fee_type` distribution
- Revenue leakage quantification: fare delta × conversion lift for EY
- Monitor FBU solution direction discussion; intervene on ABT metrics spec when design starts
- Fill revenue leakage placeholder: fare delta (Non-Flexible → Flexible) × conversion lift for EY


**2026-07-02 — H1 Review Prep**
- H1 narrative narrative framing complete: framework (attributes delta → feasibility/attractiveness → Observed Rate funnel) is Michael's structural contribution, not J's
- 24h free cancellation / void display case identified as quantification target
- Open: order-of-magnitude number in progress with J — must land before H1 review
- Source: [[coaching_20260620]]

---

## Session 7 — 2026-07-04

**Topic:** H1 Performance Review — Self-Evaluation Draft (Part 1: OKR + Part 2: Leadership Competency)

**Context:**
H1 review cycle. Worked through full self-evaluation across O1–O4 and leadership competency assessment iteratively — starting from Michael's honest reflections, refining wording, calibrating tone, and correcting attribution before finalizing.

**Key Decisions:**

**O1:** Attribution on void/24h corrected — J drove initial discovery; Michael supported data synthesis, deep-dives, framework formalization, and FBU resolution. Growth edge framed around two strategist standards: identifying benchmark gaps and needle mover instinct.

**O2:** Communication evolution (bi-weekly email → layered Lark/email/live sync framework) named as a structural contribution. J and Serena's explicit positive feedback on structure and visual clarity included as external validation. Gaps acknowledged honestly: tracking fell behind under pressure, FBU front-end delays (partly their side), data quality self-checks not without exception.

**O3:** Health check deprioritization reframed as a deliberate trade-off aligned with J, not a miss. Core narrative: supply coverage database blocked for months → two parallel self-initiated solutions (Brand Fare Audit with regional teams + scraper prototype). Scraper claim calibrated carefully — proof of concept only, scalability not yet validated.

**O4:** Kept short — limited ad-hoc volume, most requests within audit scope. Forward-looking note on proactive regional engagement added.

**Scoring (Part 1 OKR):**
- O1: 4.0 (Over-fulfilled), O2: 4.1 (Over-fulfilled), O3: 3.7 (Completed), O4: 3.8 (Completed)
- Weighted average: 3.92 (Completed)

**Leadership Competency (Part 2):**
- Systematic Thinking: 4, Lead Team for Quality: 4, Drive for Ownership: 4
- Summary framed around: initiative in ambiguous situations, from a standing start (new role, new industry, chaotic project)
- H2 focus: closing the loop from problem identification to business case and decision

**Key framing decisions:**
- "Level 1 delivered, business results ahead" — the shared understanding with J explicitly named in summary
- Difficulty context (new role, new industry, chaotic project) woven into leadership summary rather than as a disclaimer
- Growth edges stated honestly throughout — reads as self-aware, not defensive

**Documents Updated:**
- `H1_self_evaluation.md` — created; full Part 1 + Part 2 final version