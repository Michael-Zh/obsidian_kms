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
---

## Session 8 — 2026-07-15

**Topic:** AirAsia VPL 附加率趋势分析 + BA 旁路表 Proposal

**Context:**
AirAsia Value Pack Lite（15kg 托运 + 标准选座）于 6 月 17 日在 TH/MY/PH 国内航线正式上线。本次 session 的核心目标是通过内部 BQ 数据评估 VPL 上线后 attach rate 的实际变化趋势。同时整理了 BA 旁路表的上线请求内容。

**数据范围：**
- 航司：AK / FD / XJ / D7 / Z2 / QZ / KT（全 AirAsia 实体）
- 路线：TH/MY/PH 三国国内（出发 + 到达国一致，region IN ('th','my','ph')）
- 时间：2026-01-01 至 2026-07-15（覆盖 VPL 上线前后完整对比窗口）
- 舱位：Y/W 经济舱 + 超级经济舱
- SQL 存档：`Order_ori.md`（目标表 `MZ_order_ori_AirAsia`）

**Key Finding — VPL Attach Rate 趋势（meta + 1-meta 合并）：**
- **15kg 托运包**：VPL 上线前（W1-W23）占比约 2%；上线后（W24+）稳步增长，最新 week（截至 7/15）达约 8%
- **20kg 托运包**：上线前约 7%；上线后降至 3-4%（部分被 15kg VPL 替代）
- **整体 check bag share**：上线后净增约 3pp（非纯零和置换），方向健康
- **整体 upsell rate**：维持 ~25-27%，VPL 尚未明显拉动 base fare → upsell 的整体转化
- **异常点**：2 月 W5-8 出现 15kg 小幅峰值（VPL 上线前），来源待确认（可能是其他 Reg+Bag 15kg 运价）
- **vs. AA 官网**：AA.com VPL attach rate ~11%；Trip 当前 ~8%，缺口约 3pp；原因尚待 coverage 数据确认

**分析判断：**
- VPL 方向健康，但 base fare 用户向 checkin bag 的增量转化暂不显著 → 问题可能在 Supply/Ranking/Display 层
- 等待 Lulu 的 coverage 数据（当前约 47%），确认 supply 修复完整性后再做下一步诊断

**BA 旁路表 Proposal（2026-07-17 补充）：**
- **内容：** 通过旁路表保留 BA 所有品牌运价（semi-flex / flex / fully flex）至所有 BA 航线
- **Metrics：** BA 整体 CR、upsell%、订单量和订单 share
- **Breakdown 维度：** 品牌运价（监控被保留运价的恢复情况）× 长途 vs. 中短途（长途 + semi-flex/flex 预期效果更强）
- **节奏建议：** 尽快配置 → 最早下周初开始测试；在 BI Personalized Ranking ABT 测试流量增加至 30% 之前先跑（避免 ranking 变量干扰，先确认旁路表本身的效果）
- **后续：** BA 测试开始后，逐步扩展至其他类似情况的航司（清单待补充）

**Parked / 待跟进：**
1. **Coverage 数据（Lulu）**：等回复 → 确认 supply 修复完整性；决定下一步诊断层（Ranking / Display）
2. **Pure Value Pack WS2 filter**：VP 运价被比价算法 PK，用户无法看到/购买 VP；需确认 bypass 方案或旁路表是否可覆盖

**Documents Updated:**
- `Order_ori.md` — 最终 SQL（AirAsia TH/MY/PH domestic，含 `checkin_bagweight` + `orderdate_d`，isBatch1 修正为 CASE 表达式）

---

## Session 9 — 2026-07-20

**Topic:** FBU H2 OKR Review + 用研报告阅读 + PROJECT_CONTEXT 状态清理

**Context:**
读取并分析了三份 FBU H2 文档：
1. **Vivi 的 Upsell 项目文档（v2.2, Jul 9）：** 战略转向——"供给侧补货"→"表达侧提效 + 动机侧强化"。核心判断：不是没货，是货没卖出去，用户没觉得值得买。
2. **丁一团队前端 H2 OKR：** 五个 O。Jessie Li own upsell KR1（Fare Upsell Conversion），Doris own O2（运卡表达提效），孙爽 own post-booking/cross-sell 和 Direct Channel Conversion。
3. **用研报告（UK & SG, n=707）：** 40% 纯最低价，28% L+Extras（最大机会人群），13% Upgrader。行李是唯一通用升级驱动因素。87% 用户想要 upfront add-on cost estimate。"Recommended for you" 排序被 14/15 用户拒绝。

**Key Findings:**

**FBU OKR × IBU workstream 交叉分析：**
- Void/24h 在 FBU OKR 中未被显性命名——隐含在 Jessie KR1（differentiated benefit expression）或 Doris O2（运卡表达）中。需确认实际 owner（可能非孙爽）。
- 用研数据提供了 push void/24h 的新弹药：SG 用户 37% 认为 flexibility 重要（长途跳至 53%），退改规则不可见是用户痛点。
- FBU 定价竞争力标为"中优先级，悬，往后"——短期内不会有 AB 测试资源。IBU Pricing 分析定位需调整：从"驱动 AB 测试"→"提供诊断输入"。
- IBU Pricing Type A（内部 price gap）直接回应用研"不值"的 #1 障碍——33% UK / 46% SG 说"更高的运卡不值这个价"。
- Brand Fare Mapping scraper 恰好与 FBU O4-KR1（自动化缺口发现）对齐。
- Golden Routes / Natural Demand Ceiling 方法论是 FBU 完全未覆盖的盲区，但执行难度较高。

**PROJECT_CONTEXT 状态清理：**
- FBU display trigger logic：已确认获取（之前标为 blocker）
- H1 narrative：已完成
- EY/UA/AC 24h 案例深度分析：已 close
- 移除不再相关的 backlog 项：Ghost Query rate、Natural Demand Ceiling、Void/24h by market cut、service_fee_type 探索、Upgrade step framework（全航司扩展）、RouteType BQ split、航司 scope 扩展
- 两个 Active P0（BA 旁路表、AirAsia VPL）为 ongoing，暂不需主动投入
- Blocker 列表从 5 项精简为 4 项

**H2 优先级建议（更新版）：**
| 优先级 | 事项 | 理由 |
|---|---|---|
| P0 | Void/24h：用用研数据 push，确认 FBU owner | 最大的已知 opportunity；用研是新弹药 |
| P0 | Revenue leakage 量化 | H1 遗留；独立可控；对 business case 必需 |
| P1 | Pricing Type A（内部 price gap）| 不依赖 FBU；回应用研"不值"障碍；差异化贡献 |
| P2 | Golden Routes / Natural Demand Ceiling | 方法论差异化；但执行有难度 |

**Food for Thought:**
- 用研中"总成本估算"（87% 用户想要）是最强的产品信号之一——与 IBU Pricing 分析天然连接：price gap 数据可以 feed 进总成本展示的产品设计。
- "Recommended for you" 排序被用户强烈拒绝（14/15），而 benefit filter 被自发提及（12/15）——FBU 的 Personalized Ranking ABT（Jul 9 上线）如果用了推荐排序逻辑，可能面临用户接受度风险。值得监控 ABT 结果。
- 用研报告本身值得作为 IBU 的 reference document——在 J 沟通中引用第三方用户证据比引用自己的分析更有说服力。

**Documents Updated:**
- `PROJECT_CONTEXT.md` — 多处状态清理、FBU OKR review 发现写入、Pricing 定位调整、Next Steps 精简、Stakeholder Map 更新

---

## Session 9 续 — 2026-07-20

**Topic:** H2 优先级规划 — Q3 工作框架 Draft

**Context:**
在完成 FBU OKR review 和状态清理后，深入讨论了 H2 的实质工作方向。关键约束：作为 Strategy Team，应聚焦 needle mover——单 fix 撬动大范围、共性问题优先。

**Key Decisions:**

**Q3 三部分框架（Draft，待与 J 对齐）：**

**Part 1 — H1 Carry-over：Audit 收尾 + 航司排查**
- 航司 audit 收尾（欧线剩余 FSC + EU LCC + 北美/中东/日本）
- 用现有方法论（baggage share → fare family comparison → root cause diagnosis）补完余下航司
- 旁路表可复用：后续类似 BA 的比价过滤问题可直接套用
- Coverage 基建交接：等 automated brand fare mapping 跑通后，手工 audit 结束

**Part 2 — Net New：前端展示与辅营的量化支持**
- FBU 有方向但缺量化和优先级——IBU 可以做 mapping：用研发现 → BQ 全量数据验证 → 帮 FBU 判断方案优先级
- Void/24h + Service Fee：确认 FBU owner（Jessie/Doris），推动进入执行
- Pricing：方向待定，与 J 确认是否投入
- Service fee alignment 已明确

**Part 3 — Communication & Coordination**
- Keep up 现有 cross-BU 沟通
- 增强与 region 的 collaboration（待细化）

**Fare Family 航司分类框架 讨论结论：**
- 现有手动 approach（baggage share under-index → fare family comparison → benchmark 对比）已经够用
- 系统性分类的 marginal value 有限，且应由 FBU 来做（他们有自己的数据基建和产品方向）
- IBU 不需要做 taxonomy，但可以提供分类维度的设计建议

**Pricing 分层澄清：**
- 供应角度：成本价不合理 → 平台无法亏本卖
- 内部运营角度：business rules/人为操作放大价差 → 可调整
- 目前缺乏可靠数据做深度归因，先 observational：看最终价格差与转化率关系

**Food for Thought:**
- 目前没有发现第二个 void/24h 级别的系统性 bug——这正常，void/24h 也是一个逐步发现的过程。Q3 的重点是把手头的事情推进好，同时保持 judgment 敏锐。
- L+Extras 用户（28%）→ 他们实际花更多 vs. 直接选高一档运卡？这是最 concrete 的用研→BQ 量化切入点。

**Documents Updated:**
- `PROJECT_CONTEXT.md` — Q3 工作框架（Part 1/2/3）、Pricing 精简、Next Steps 重组

---

## Session 10 — 2026-07-20

**Topic:** 11 Airlines Brand Fare Coverage Analysis — Supply vs Selection 全景诊断

**Context:**
H1 carry-over 的航司 audit 收尾。用 `MZ_coverage_check_for_claude` 表（底层：`dw_fltdb_adm_rsc_engine_airline_route_brand_cover_v2_di`，近 90 天），对 EK, KL, AC, UA, AA, DL, CI, BR, VB, VF, NH, JL 共 11 家航司做 supply coverage 和 selection coverage 双口径诊断。目的是为后续人工走查（航司官网验证 + fare family study）提供数据基线。

**Key Decisions:**

**核心发现：品牌运价覆盖问题是结构性、分层的**

按五层漏斗归因：

**1. Data Foundation → Supply 层问题（brand mapping 缺失）**
- **BR Discount: 0%**（949K traces 全局无映射）——最严重
- **CI Discount: 10.8%**（1.55M traces）——接近缺失
- **AA 全 tier <78%**（JP-US 方向 Basic 仅 0.9%）——核心市场大面积缺失
- **EK Special: 41.5%**——最低 tier 映射不完整
- **NH Flex: 56.2%**——特定 tier 缺失
- **UA Economy Plus: 48.6%**（仅覆盖 87 CPs vs. 其他 tier 的 670+ CPs）

**2. Fare Selection 层问题（比价过滤高端 tier）**
- **VF Flex −43pp**（intl）、Ecojet 国内 −95pp——Supply 完美但比价全杀
- **NH Full Flex −79pp**（CN-JP 仅 4.7%）
- **JL Flex −69pp**（JP-VN 仅 0.2%）
- **AC Latitude −79pp**（JP-CA 仅 2.7%）
- **CI Flex −69pp**（HK-TW 仅 4.8%）
- **EK Flex Plus −66pp**（FR-AE 仅 3.3%）
- **BR Up −77pp**、**DL Comfort 系列 −51~57pp**、**UA Fully Refundable −38pp**

**共同规律：最低 price tier 在所有航司都健康（filter drop <10pp），越贵的 tier filter drop 越大。** 这符合比价算法逻辑——最低价始终排最前。

**3. 无重大问题**
- **KL：** 94.6% supply → 92.1% selection，filter drop 仅 2.5pp——但这是 WS5 Airline Compliance（Strict Fare Display）强制要求的效果，不是系统自然表现

**VB 单独说明：**
- US-MX 国际线量不大（~77K traces），但品牌映射和比价表现都相对健康，NDC 接入可能是原因

**下一步行动计划：**
- 每航司人工走查：官网确认 fare family 结构 + Top 3 CPs 比价验证
- P0 走查：AA/BR/CI（supply gap）
- P1 走查：NH/JL/VF（selection gap）
- P2 走查：EK/AC/UA/DL
- KL 作为 reference 对照

**Food for Thought:**
- VB 如果是 NDC 接入导致的良好表现，说明 NDC 是解决 coverage 的可复制路径——值得进一步验证
- JL 的 brand name 有空格不干净问题（`Economy Flex` vs `Economy  Flex`），说明 ATPCO mapping 层面本身有脏数据
- NH 有 6 个 tier，是 11 家里最多的——tier 越多意味着 mapping 和比价过滤的复杂度越高
- Filter drop 模式的规律性（低 tier 健康、高 tier 被杀）说明比价算法有系统性逻辑，可能可以通过旁路表或 compliance 干预

**Documents Updated:**
- `audit/11_airlines_coverage_analysis.md` — 新建，完整 11 航司 coverage 分析
- `PROJECT_CONTEXT.md` — Next Steps 更新

---

## Session 9 续② — 2026-07-20

**Topic:** J 1-on-1 同步 + Regional Sync Agenda + Q3 OKR Proposal

**Context:**
完成 Q3 工作框架讨论后，与 J 进行了 1-on-1 同步。未深入讨论 OKR 细节，但获得了四条重要背景信息。同日起草了 Regional Sync 会议 agenda 和 Q3 OKR Proposal 文档。

**J 1-on-1 关键信息：**
1. **全公司 AI-driven 优化方向：** 后续项目需尽可能 leverage AI 能力
2. **FBU BI team lead 离职：** 新接替待宣布，需重新磨合合作模式
3. **IPU ETL 支持升级：** Phase 1 — IBU 自行 exploration 后要求 copy 到 BQ，次日交付；Phase 2 — IPU 主动帮我们找数据
4. **Q3 OKR：** 具体 KR 未深入讨论；近期重点 — regional sync 尽快完成；需与 Jessie 约会 align void/24h

**Q3 OKR Proposal 起草：**
- `H2_OKR_Proposal.md` — 三个 O：O1 Audit收尾+基建交接 / O2 前端量化支持 / O3 协同维护
- 待与 J 进一步讨论后定稿

**Regional Sync Agenda 起草：**
- `Regional_Sync_Agenda.md` — 30-60 min 会议模板，四个 items：
  1. Circle back on region requests
  2. 24h case share (FYI, dependency noted)
  3. Audit update (verified/quantified only)
  4. ABT update + regional support ask
- 核心原则：brief, concrete, tailored per region

**Documents Created:**
- `H2_OKR_Proposal.md` — Q3 OKR proposal for J discussion
- `Regional_Sync_Agenda.md` — Regional sync meeting template

**Documents Updated:**
- `PROJECT_CONTEXT.md` — Part 3 新增 J 1-on-1 背景、Stakeholder Map 重构（拆分为 Jessie/Doris/孙爽独立行，新增 FBU BI 和 IPU DE）
- `CLAUDE.md` — Trial Log 范围更新至 Session 10

---

## Session 11 — 2026-07-21

**Topic:** NH ATPCO Brand Name 验证 — Fare Family 方向性确认 + 五层问题定位

**Context:**
用订单层 `edw_prd_flt_factfltsegment_eng.atpco_brand_name` 验证 NH 的 fare family 分类是否准确，按航线和方向拆开看实际 tier 分布。同时确认了 Flex 零订单的根因——比价过滤 + Ranking 双杀。

**Key Findings:**

**Tier 映射验证：** 九个主要 tier 的 ATPCO → unified brand name 映射链完整，无错配。国内线专用名（DMS/NHIE/DJ FARE 等）未泄漏到国际线。

**Fare Family 方向性：** 四套 fare family 假设被订单数据广泛验证。新增发现：KR→JP 航线结构不同于中日线和 SEA 线（Standard + Full Flex 为主），需人工走查确定。

**NULL ATPCO name：** 25-37% 订单 `atpco_brand_name IS NULL`，全局均匀，部分 supply 通道不传此字段。低优先级，暂不投入排查。

**Flex 零订单根因 — 双杀：**
- Fare Selection：Flex −44pp 系统性过滤（Standard 同 CP 仅 −8pp），比价算法对 Flex 有系统性不利。中日线例外（JP-CN 仅 −19pp）。
- Ranking：即使活下来的 49.6%，Flex 订单在 JP→SEA 方向仍为 0。Standard 85.6% 可见、定价合理，订单也仅 5.6%——排序问题是更大瓶颈。

**五层最终定位：**

| 层 | 状态 | 证据 |
|---|---|---|
| Data Foundation | 🔴 Light coverage trace 缺失 + KR→JP fare family 不明 | `officialbrandname=NULL` 导致 ETL 过滤 Light |
| Supply | 🟡 JP→Americas Value 偏低（JP→US 71.1%, JP→CA 64.2%） | 方向性限制假象外，存在真实局部缺失 |
| Fare Selection | 🔴 Flex −44pp 系统性过滤 | Standard −8pp 对照 |
| Ranking | 🔴 Standard 85.6% 可见但仅 5.6% 订单 | 能见≠能买 |
| Display | ❓ 待验证 | 权益差异是否清晰展示 |

**Next Step — Scraper 人工走查（本次 session 讨论中）：**
- 用 scraper 爬 NH 官网，做两件事：(a) 验证低 coverage 航线在官网侧是否真的有对应 tier；(b) 确定 KR→JP 航线的 fare family 结构
- 讨论 scraper 开发方向：TK v2 继续修 vs. 换航司/换技术路线

**Documents Updated:**
- `Flight_Upsell_Trial_Log.md` — Session 11 追加

---

## Session 11 续 — 2026-07-21

**Topic:** NH Scraper 开发 + 目录重组

**Scraper 工作流：**
- 确认 NH scraper 用 CDP 模式（复用用户 Chrome session，避免反爬）
- 完整搜索流程跑通：机场选择（click field → type IATA → select from list）→ 键盘输入日期 → Search → 结果页加载
- 问题 1：`wait_until="domcontentloaded"` 不够，需等待 booking widget 渲染（`networkidle` 反而超时）
- 问题 2：RT 回程无航班导致整页 No results，OW 正常
- 问题 3：Fare 提取逻辑未完成——结果页每个日期 tab 需逐个点击展开，提取 tier 价格
- 关键注意：**NH scraper 需先选 One Way tab，再填机场/日期**（当前代码 `set_ow` 调用顺序正确，但 ANA 在 RT default 下可能需先切换 tab）

**Scraping Plan（最终）：**
- 全部 OW、1 pax、每周一、+1 月 + +3 月
- 每航线 4 次搜索（去程 × 2 + 回程 × 2），GMP 仅 2 次
- 一次搜索覆盖 7 天日期窗口

**目录重组：**
- `audit/TK/`、`audit/NH/`、`audit/JL/` → `scraper/` 独立目录
- `audit/` 保留纯数据分析文件

**Documents Updated:**
- `scraper/` 目录新建，TK/NH/JL 移入
- `Flight_Upsell_Trial_Log.md` — Session 11 续追加

---

## Session 12 — 2026-07-21

**Topic:** NH Scraper v2 Debug — 修通全流程

**Context:**
Session 11 续调 NH scraper 发现多处因 Angular 动态渲染导致的 Playwright click/fill 失效。重写 v2，全部改用 JS 直接操作 DOM。

**Key Decisions:**
- **机场选取**：`fill()`+Enter 不触发选择 → JS `el.click()` on `[data-value="IATA"]`，优先 `IATA+` variant（如 BKK+ 是主机场）
- **日期选择**：ANA 双面板日历，JS 按 header text（"August 2026"）定位 month panel → 再按 day text 点日期 → Confirm
- **One Way tab**：不是 `<button>` 而是 `<li role="button" data-value="onewayOrMulticity">`
- **结果页 tab**：Angular `id="c-result-date-navi-btn-N"`，`text_content()` 只返回 "Destination 1"，需从 `<span>` 子元素提取日期和 "From USD"
- **运价解析**：按 "A fare selection screen will be displayed" 分段，跳过 "Not available" 的 screen
- **日期策略**：+1mo Monday（Mon–Thu 4天）+ +3mo Thursday（Thu–Sun 4天），8 天全覆盖
- **进度显示**：每步显示 done/total、剩余数、本次/累计/平均用时、ETA

**Results:**
- `--test` 验证：HND→BKK，7天×273行×16航班，63秒
- 全量预估：24 搜索 × ~60s = ~25 分钟

**Blockers:**
- 待明天（7/22）启动全量运行
- 运价 tier 标签映射需验证（当前页仅显示 Value/Standard/Flex/Full Flex 的 2-3 个）

**Food for Thought:**
- 全天用 JS click 很脆弱——如果 Angular 渲染慢可能取不到日期文本，考虑加 retry + wait
- ANA 某些航线可能不提供全部四个 tier，需区分「页面未展示」vs「航线确实没有」

**Documents Updated:**
- `scraper/NH/fetch_fares_nh_v1.py` — 完整重写
- `Flight_Upsell_Trial_Log.md` — Session 12 新增
- `PROJECT_CONTEXT.md` — Next Steps 更新

---

## Session 13 — 2026-07-21/22/23

**Topic:** Regional Sync Agenda 准备 + Jay v2 版本对比分析 + AirAsia VPL Coverage 初步排查

**Context:**
本次 session 围绕 Regional Sync 会议准备展开，同步处理了 AirAsia VPL coverage 的初步排查，并在 session 末对 Jay 修改后的 v2 版本做了对比学习。

**Key Decisions:**

**Regional Sync Agenda：**
- 受众确认为全球所有 PGM & market（不是单独 per-region 会）
- Section 1（Circle back）：Cristina（EU，BA 高阶运价）和 Peam（TH/SEA，Quick Filter）作为 case 点名感谢——定位为向全体 PGM 展示"region input → IBU action"协作 loop 有效
- 24h case（Section 3）：三步走结构（发现→量化→推动落地），突出 IBU 主导角色；技术细节（void vs. 24h 区别、市场展示规则）保留在正文
- 英文版按中文版内容严格翻译，不增减

**Jay v2 版本对比（可学习点）：**
1. 用 hypothesis 叙事开头，不从 deliverable 列表开头——给受众"为什么这些事重要"的框架
2. 把相关问题归在同一主题下（Full Cost Display + 24h case 并列为 Issue 1/2），比各自独立 section 更有说服力
3. 感谢做成独立 section（"A BIG THANK YOU"），不是 footnote——对 region engagement 激励效果更强
4. 对 region 的 ask 具体到"在 mock-up 阶段给 feedback"——比"随时告诉我们"更能转化为实际行动

**AirAsia VPL Coverage 初步排查（已搁置）：**
- 数据：VPL 15kg pre（命中率）≈ post（胜出率），gap 仅 1–3pp——比价算法不是问题
- 命中率约 35–48%，上线后持续爬升，近两周进入平台期
- Spot check 发现前台有 VPL 但数据显示低 coverage——初步推断是分母定义问题，非真实 supply gap
- 下一步（搁置）：与 FBU 数据同事确认 coverage 指标分母定义；用 spot check 反证直接推进

**Food for Thought:**
- Jay 把 24h case 降格为 Issue 2 并与 Full Cost Display 并列——"退改政策展示不透明"作为系统性主题比两个独立 case 更有说服力。未来向 region 或 leadership 汇报时可复用这种归类方式
- AirAsia pitch 卡在 FBU "先确认 coverage" 的门槛上——如果能快速澄清分母问题，这个拦路虎可以快速移除，不需要等 supply 真正修复

**Documents Updated:**
- `Regional_Sync_Agenda.md` — 中文版完整四 section（工作草稿，供参考）
- `Regional_Sync_Agenda_EN.md` — 定稿同步自飞书 v2（VY68djwUlox1fxxxBXjlAsQigqf，2026-07-23）
- `PROJECT_CONTEXT.md` — Part 3 Next Steps 更新、AirAsia 排查进展更新
- `_in_case_you_are_bored.md` — [[Flight_Upsell]] 行更新
