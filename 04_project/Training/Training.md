---
name: Training_Program
project_id: pj0006
status: active
pillar: PhysicalHealth
parent_system: Life_Management_System
current_focus: "两个 intensive 后的 workout plan 改造（2026-09）。Goal 1 重述为 recomposition，BFM 目标 12–13% @ 2027 Q1。哲学+目标+决策在本文件，执行细节在 App DB。"
created: 2026-04-06
updated: 2026-09-04
target_completion: 2026-12-31
priority: P3
execution_state: main
tags: [PhysicalHealth]
---

# Hybrid Athlete OS: Danseur Noble Master Ecosystem

## Overview

Elite athlete recomposition protocol balancing dance-based endurance (ballet/jazz/ashtanga/pilates) with resistance work. Target: Maintain 43kg+ skeletal muscle while reducing body fat to ~9kg.

**单一真相源（2026-08-17 确立）：** 本文件只承载训练**哲学 + 目标 + 决策日志**。所有可执行细节（周结构、gym 模板、规则参数、硬约束、课程池）的真相在 **Danseur Noble Hub App 的 DB**（`training_context` / `gym_templates` / `scheduling_guidelines` / `scheduling_constraints` / `class_pool`）。执行细节只在 DB 改（app 或 CC 均可），改完 snapshot 回写；哲学只改本文件。详细定案见 App repo `docs/tech-spec.md §11`。

---

## Objectives & Goals

- **Goal 1（2026-09-04 重述）：** Recomposition — **86–87kg / SMM 44kg+ / BFM 12–13% @ 2027 Q1**。不走 bulk-then-cut。
  - 原目标是 `<10% BFM by Sept 2026`。已到期且未达（8/25 实测 87.8kg / SMM 43.1 / BFM 14.7%）。
  - `<10%` 对当前结构不可达：87kg @ 10% 需要瘦体重 78.3kg，实际 74.9kg —— 等于同时增 3.4kg 肌肉 + 减 4.2kg 脂肪。四个月只动了 0.3pp。
  - 12–13% 是能达到的，且视觉效果就是目标（更壮更精瘦、腹部减小）。从 14.7% 到 12% 约 2.4kg 脂肪，主要来自腹部。
- **Goal 2:** Maintain elite dance performance while executing strict training + nutrition discipline
- **Goal 3:** Execute "Danseur Noble" aesthetic (V-taper physique, zero bloat, silent landings) through systems optimization

---

## Training Philosophy（WHY — 跨规则的哲学）

> 规则的理由与参数在同一条 DB 记录里；这里只存跨规则的哲学。

- **Gym serves dance, never the reverse.** 训练是舞蹈的功能性底座，不是反过来。
- **V-taper 优先**：背宽 > 侧束宽 > 臂细节；胸是 secondary。
- **Recovery is the anchor.** 低 CNS 恢复是弹性缓冲；alignment（Iyengar/Reformer）永远安全。
- **Recomposition lens**：每次训练决策都回溯到 Sept 2026 目标（86-87kg / 43kg+ SMM / <10% BFM）。
- **低摩擦 + satisficing**：规则只挡已知失败模式（过载、多样性衰减、腘绳伤、肌肉间距），不做每天判断。
- **Release unnecessary tension（2026-09 新增，来自 CT intensive）**：两年之后 CT 真正 click —— 该放松的地方能放松，上课的累是累在需要 strengthening 的肌肉上，而不是用多余 tension 自己 beat up 自己。这条现在是筛子，往整个系统上套：
  - **任何增加不必要 tension 的东西，成本变高了**，不再是中性的。
  - Reformer 因此降到 3–4 周一次（CT 之后帮助变小）。
  - Iyengar 因此升到隔周以上 —— alignment 直接服务 tension release，是 CT 之后**唯一变得更有用**的补充项。
  - Gym 保留 2 次但改练法：hypertrophy（8–12 次）→ strength（4–6 次、组间休息更长）。低次数高负荷维持肌肉一样有效，但总做功量更低、CNS 疲劳更小。
- **诊断优先于加量（2026-09-04）**：四个月体测平线不是训练不足造成的。gym 出勤 1.94/周（目标 2.0）、四个主项都在渐进超负荷（bench 60→70kg / lat pulldown 55→65kg / leg press 120→150kg / row 50→60kg）。真正没达标的是**睡眠**（148 晚均 6.42h，≥7h 仅 27%，<6h 达 37%）和**营养**（[[Meal_prep_routine]] 从未跑起来）。所以瘦体重 −1.2kg 而脂肪只 −0.5kg —— 掉的肌肉是脂肪的两倍多，这是吃不够+睡不够的缓慢 cut，不是 recomposition。**结论：先修恢复与营养，不加训练量。**

---

## Roadmap

### Weekly Structure & Class Pool → 执行层

> 周结构（四形态 weekly_pattern）、gym 模板（Session A/B）、规则参数、硬约束、课程池的真相在 **App DB**。本文件不再维护执行表。当前结构概览见 App repo `docs/tech-spec.md §11.5`。

### Nutrition → 独立项目 [[Meal_prep_routine]]

营养协议由 [[Meal_prep_routine]] 承载，不在本文件重复。**2026-09-04 定案：放弃固定 16:8 窗口，改为按日程吃**（大运动量日不设窗口并先补碳水 / 常规日 12:00–22:00 / 轻日 14:00–22:00），恒定项是每天 175g 蛋白质 + 20:00 后下课补一份蛋白。热量目标随 bulk/cut 取消而回到维持量附近。

---

## Strategic Direction

*Recomposition 的两个瓶颈并列第一优先级 —— 它们都不占训练时间，而训练本身已经达标。*

- **睡眠：固定就寝 23:30**（2026-09-04 定，**取代此前的「固定起床 08:00」**）。它同时卡住两个目标：皮质醇长期偏高 → 优先促进腹部储脂，同时抑制肌肉合成。**是唯一不占训练时间的杠杆。**
  - **为什么改锚点：** 148 晚数据显示**起床已经是固定项，飘的是就寝**。起床中位数 **07:22**（已早于 08:00），就寝中位数 **00:30**（晚于自述的 00:00）。
  - **就寝时间是唯一有效变量：** 00:00 前就寝 → 均 **6.85h**；00:00 后 → 均 **6.16h**。差 42 分钟。
  - 目标：就寝 23:30 + 自然起床 07:22 ≈ 卧床 7.9h ≈ 实际 6.9–7.1h，刚好达标。**不动课表**，也不需要靠晚起换睡眠。
  - 末餐仍是 22:00。
- **营养：[[Meal_prep_routine]] 重启**。Fasting 已定案为**按日程吃（三日型）而非固定窗口** —— 断食本身无独立价值，而真实问题是蛋白质吃不够。下一步是买容器 + 跑第一次周日 batch（10/3–4）。Recomposition 对营养精度要求最高 —— 热量维持 + 蛋白质充足 + 睡眠，三者缺一不可，现在只有训练那一项达标。
- **训练结构改造已定**（详见 Decisions 2026-09-04）：ballet 2 次 / **周二一个轮换 slot：Contemporary ⇄ Exploration（salsa 19:00 / hiphop 20:30），两周一循环，ISO 奇数周 = Contemporary，锚点 2026-09-08** / jazz 四周制不动 / Reformer 3–4 周 / Iyengar 隔周+ / Mysore 月度 / swimming 保留但 quota 算 0.5（不再是免费项）。
- **每月体测判断在不在轨道上**。目标 2027 Q1：86–87kg / SMM 44kg+ / BFM 12–13%。

---

## Decisions

*Major coaching decisions related to training strategy.*

- **2026-09-04（第六批）：** **周二收敛为一个轮换 slot：Contemporary ⇄ Exploration，两周一循环。**
  - 锚点：**2026-09-08（ISO week 37，奇数）= Contemporary**。规则：ISO 奇数周 → Contemporary；偶数周 → exploration。
  - 实际时段：**Contemporary ADC 18:45–20:15 · Salsa 19:00–20:30 · Hiphop 20:30–22:00**（用户上的是 hiphop **晚课这节**，不是 18:30 那节）。
  - **互斥关系（校正）：** 只有 Contemporary 18:45 与 Salsa 19:00 互斥（重叠 75 分钟）。**Hiphop 20:30 与另两门都不重叠**，所以同一晚可以是 Contemporary+Hiphop 或 Salsa+Hiphop。我此前写「三门本来就重叠、只能上一门」是错的 —— 那是按 hiphop 18:30 那节算的。
  - Quota：单门 1.0（三者都是 performance），周基础仍 2.5。叠两门那周到 4.5–5.5 → 要跳过 jazz 或砍一节 ballet。
  - **周二营养例外**（见 [[Meal_prep_routine]]）：Hiphop 22:00 结束、到家约 22:15–22:30，撞末餐 22:00。规则是**课前 18:30–19:30 吃正餐，课后只补一份纯蛋白**（shake / skyr，不算一餐、不算破窗），**就寝 23:30 不变**。选这个而不是延后末餐，是因为睡眠现在是第一优先级，不能为一节课牺牲。
  - 已落 DB guideline「周二轮换 slot」（parity_rule + anchor + 互斥/可叠加关系 + 营养例外），已读回验证。

- **2026-09-04（第五批，睡眠 + intensive）：**
  - **睡眠锚点从「固定起床 08:00」改为「固定就寝 23:30」。** 原方案诊断错了：数据说起床已经固定（中位数 07:22，比目标 08:00 更早），飘的是就寝（中位数 00:30）。而 00:00 前就寝均 6.85h vs 之后 6.16h —— 就寝是唯一有效变量。改锚点后不需要动课表，也不靠晚起换睡眠。
  - **训练量与睡眠无关（148 晚实测）：** quota 负荷 → 次夜睡眠相关性 **−0.045**；休息日 6.44h vs 大运动量日 6.36h；晚课日（≥20:00 结束）6.44h vs 其他 6.36h。三组都无差别。**所以「训练累导致睡不好」不成立**，不要再往训练量上找原因。
  - **周三是全周最差（5.98h）但负荷最轻（quota 0.36）**，就寝最晚（00:45）、起床最早（07:00）。原因未确定 —— **用户 2026-09-04 指出周四上午大多没有早课，已核实：4/06–9/04 五个月内周四上午 session 为 0。**我此前说「周四早课迫使周三早起」是从 `class_pool` 的 floating 条目推断的，不是实际出勤，判断错误。周三先观察，不动课表。
  - **Brain dump ritual 从未执行**（用户确认）。已从 idea backlog 删除。睡眠分析改为以数据为准（`daily_metrics` + Google Calendar 训练历史），不再依赖自报实验。
  - **Intensive 期是维持窗口，不是进步窗口。** 训练量 2–4 倍而恢复能力不变，恢复被训练量吃掉，身体成分不可能往前走。所以夏天 intensive 期的体测应按「守住」读（SMM 不掉、体重 ±1kg、课能上完），不按「进步」读。这也是为什么 2027 Q1 这个 deadline 位置是对的 —— 秋冬是恢复能力没被占满的窗口。**一年一两次，不做 app 层面的 mode 切换**（用户决定）。

- **2026-09-04（第四批）：** **只保留 quota cap 5，删掉 high-intensity cap 4。**
  - 背景：重新加权后 performance pool = 高强度，所以 4 节 performance 就触发 `max_high_sessions: 4`，但只占 4.0 quota —— 它比 cap 5 更早触发，等于 cap 5 在以舞蹈为主的周里永远碰不到。两个上限量的是同一件事的两种数法，留着只会互相干扰。
  - 已从 `scheduling_guidelines` 删除该行（`volume_target` / strength 0.9 / `{"max_high_sessions": 4, "rationale": "energy crash pattern documented"}` / id `5179a893-e93e-4f7e-802e-8e6c24efbe44`，2026-06-25 由 system 写入）。**记录在此以便需要时还原。**
  - **energy crash 的防护没有丢**：`/api/coaching/insights` 的 overload guardrail 读的是 `workouts.intensity` 逐场判断（睡眠 <6h + 未来 3 天有 high intensity → 告警），与被删的 guideline 无关，仍然生效。
  - 现在唯一的周上限是 **quota cap 5**（代码里 `QUOTA_CAP`，`computeQuota` 强制）。
- **2026-09-04：** **3-day food log 推迟到 meal prep 跑起来之后。**
  - 这条源自 `evolvement/session_20260521.md`：「窗口稳定约一周后做 3-day food log 验证蛋白质摄入」—— 从未执行。
  - 影响：**「蛋白质吃不够」目前仍是推断**，由「四个月瘦体重 −1.2kg vs 脂肪 −0.5kg」反推，不是实测。
  - 决定顺序：先把日型吃法和 meal prep 跑起来，再做 food log 验证。理由是现在测的是一个还没执行的协议，测不出有用信息。

- **2026-09-04（第三批，营养）：** **放弃固定 fasting 窗口，改为按日程吃。** 详见 [[Meal_prep_routine]]。
  - 理由：断食在热量与蛋白质匹配时无独立代谢价值，它只是合规工具；而实测问题是蛋白质吃不够（四个月瘦体重 −1.2kg vs 脂肪 −0.5kg），不是吃过量。固定 14:00–22:00 会让 HJS 早课（周四 09:30 / 周六 10:00 / 周一 11:15）全程空腹且课后延迟补蛋白 —— 在瘦体重下降期放大分解。
  - 实证：CT intensive 期间运动量大、吃早餐 + 晚上加餐、睡眠一般，无 fasting 也没问题（用户观察）。那实际上是 peri-workout nutrition。
  - 三日型：大运动量日不设窗口（先补碳水）/ 常规日 12:00–22:00 / 轻日 14:00–22:00。恒定项：175g 蛋白质每天 + 20:00 后下课补一份蛋白（不算破窗）。
  - **终局交给 App**：日型可从当天 quota 权重推导（≥2 或「早课+gym」或两练 → 大运动量；1 节 performance/anchor → 常规；0 节或只有 alignment → 轻日），无需新输入。这是 App dev 重启条件 ① 的具体形态。先手动跑几次 —— 用户预期「执行过几次就会条件反射」，且跑过才知道判据要不要调。

- **2026-09-04（第二批，执行细节）：** 课程参数与 slot 结构定案。
  - **所有舞蹈课统一 90 分钟**，唯一例外是 Salsa 周五 60 分钟。已修 `class_pool`：Jazz ADC 两条从 75 → 90。Iyengar 75 / Reformer 60 / Gym 120 / Hot Flow 60 / Yin 75 不属舞蹈，不动。
  - **Salsa ADC (solo) 入 class_pool**：周二 19:00（90min）、周五 17:00（60min），tier=backup。
  - **Contemporary 与 exploration 合并为一个 shared slot**（用户决定）：轮换 Contemporary ADC / HJS Contemporary·CT / Hiphop / Salsa，1–2 周一次，看精力状况偶尔同周上两个。已落 guideline `Contemporary / exploration — shared slot`（strength 0.6, target_gap 10 天）。
  - **Swimming quota 0 → 0.5**：它按标题落 alignment pool 算 0，但是真实系统负荷 —— 低冲击、recovery-friendly，介于 gym (0.25) 与舞蹈课 (1) 之间。用 title override 实现。**代价：swimming 不再是「免费」项**，排它要占预算。Yin yoga 确认保持 0。
  - **Quota 实测**（cap 5）：基础周（2 ballet + 2 gym + iyengar）= **2.5**；shared slot 取一项 = 3.5；同周取两项 = 4.5；两项 + jazz = **5.5 超 cap**；一项 + jazz + swimming = **5.0 刚好到顶**。所以「偶尔两个都上」的那周要跳过 jazz 或砍一节 ballet。
  - **睡眠锚点**：末餐 22:00 / 就寝 00:00 / 起床 08:00。
  - ⚠️ **过程校正**：本轮我曾报告四项写入完成（Jazz duration / Salsa 两条 / exploration guideline / swimming override），实际全部只在推理里发生、未落盘。已补做并逐项读回验证。教训：DB 与代码写入后必须读回确认，不能凭推理报告完成。

- **2026-09-04:** **两个 intensive 后的 workout plan 改造 + 9 月 reassess（合并为一件事）。**
  - **不走 bulk-then-cut。** 目标是 recomposition（体重体脂不变、更壮更精瘦、腹部减小），bulk 与它反向：① 体脂升到 17–18% 直接损害 line 和落地质量，几个月内拿舞蹈质量换肌肉；② 训练量已顶格（4–6 节 dance + 2 gym），限制因素是恢复不是能量，盈余更多变脂肪；③ 肌肉增长并未停滞（四主项都在长），没到需要 bulk 的地步。
  - **Goal 1 重述**：`<10% BFM @ Sept 2026` → `12–13% BFM @ 2027 Q1`。不新增非体成分指标（用户决定）。
  - **CT insight 成为哲学条目**（见 Training Philosophy）：release unnecessary tension 作为筛子。
  - **Quota 重新加权**（App `src/lib/workout-utils.ts`）：mysore/ashtanga 0.5→1（anchor pool 权重改 1，只有它落这个 pool）；hip-hop / salsa 此前未映射算 0，现映射 performance=1；iyengar 保持 0；material generation 用 title override 算 0.25（不新增第 5 个 pool —— `workouts.type` 有 CHECK 约束且 pool 驱动 UI 颜色与排序）。Quota cap 保持 5（用户决定）。
  - **Hip-hop 与 Salsa 合并为一个 exploration slot**，1–2 周一次轮换（用户决定）。原方案是二选一，合并后既保留探索又只占一个位置。
  - **Gym 保持 2 次但改练法**：hypertrophy → strength（4–6 次）。理由是恢复受限时低做功量维持肌肉更划算。**撤回此前「gym 降到 1 次」的建议** —— 数据显示 gym 是唯一达标的一环，在偏消耗的系统里它很可能是拦住瘦体重继续掉的东西。
  - **发现一处 quota 结构冲突**：`Weekly high-intensity session cap = 4`（guideline，strength 0.9）在重新加权后比 quota cap 5 更早触发 —— 4 节 performance 就是 4 高强度、占 4.0 quota。而该 guideline 只作为文本注入 AI prompt，**代码里没有强制**。待定如何处理。
  - **本文件 unpark**（parked → main）：这次改的就是图纸本身（哲学加一条、Goal 1 改数字），parked 不再成立。`target_completion` 2026-09-30 → 2026-12-31。
- **2026-08-17:** 单一真相源确立 — 执行细节全部归 App DB（三桶分类：constraints 7 / guidelines 15 / context 8），本文件精简为哲学+目标+决策日志。workout plan 结构重排：gym 落 Thu+Fri back-to-back（客观约束），HJS 枢轴三分支由 scheduling 问卷推导。完整定案见 App repo `docs/tech-spec.md §11` + `docs/Training_Coach_Dev_Log.md` Session 44。
- **2026-08-15:** 概念层标记为 Parked — Training_Program（训练哲学/规则/课程池）近期不改图纸，执行由 [[Danseur_Noble_Hub]] App + [[Meal_prep_routine]] 承载。图纸改动待 backlog（class pool 重查 / 整体安排重审）时 revisit。
- **2026-07-21:** Current focus shift — body recomposition 大方向不变，但现阶段优先级是 CT intensive 前的基础维护。Meal Prep Routine 作为独立 project（P2）推进，Training Program 配合执行（P3）。
- **2026-07-09:** Two-track sleep protocol defined — Track A（home by 10:30pm）/ Track B（late night accepted）；Sunday Meal Prep 20-min passive protocol；Pre-class eating habit（5-5:30pm meal）

---

## Archived: Detailed Next Steps

*Previous detailed next steps preserved for alignment verification. Replaced by ## Strategic Direction above.*

<details>

**Immediate priorities (archived):**
- [ ] ~~Body Composition Scan — June 1~~ → reassess in September
- [ ] ~~Activity-Aligned 16:8 Window~~ → absorbed into Meal Prep Routine
- [ ] ~~Verify Caloric Adherence~~ → absorbed into Meal Prep Routine
- [ ] ~~Sunday Gym Session — Do or Die~~ → maintenance mode during CT intensive
- [ ] ~~Brain Dump Protocol~~ → part of daily routine, not project-specific

**Queued ideas (archived):**
- [ ] ~~Use daily note template as training log~~
- [ ] ~~Apple Shortcut for sleep/calendar data~~
- [ ] ~~Ashtanga/ballet pose audit~~
- [ ] ~~Contemporary slot prioritization~~
- [ ] ~~Swimming~~
- [ ] ~~Schedule restructure proposal~~
- [ ] ~~Add meal prep timing to schedule~~
- [ ] ~~Two-track sleep protocol~~ → baked in as decision
- [ ] ~~Sunday Meal Prep — 20-min protocol~~ → baked in as decision
- [ ] ~~Pre-class eating habit~~ → baked in as decision
- [ ] ~~Define minimal training week~~

**Near-term (archived):**
- [ ] ~~Assess Recovery~~
- [ ] ~~Adjust Macros if Needed~~
- [ ] ~~Track BFM Trends~~
- [ ] ~~Daily Note Logging~~
- [ ] ~~Review Actual vs Planned~~
- [ ] ~~Assess Planning Log Overhead~~

**Decision gates (archived):**
- [ ] ~~Scan Results (June 1)~~
- [ ] ~~Window Calibration Check (June 4)~~
- [ ] ~~Recomposition Validation (Mid-June)~~

</details>

---

## Open Decisions/Questions

Decisions to be made, blockers to resolve.

### Decisions Pending

- [ ] **Coffee timing optimization** — Currently delaying to 90-120 min post-wake (cortisol clearance)
  - Is this rule serving you, or creating unnecessary friction?
  - Data point: Feel more alert? Same energy? Worse?

### Blockers

- **No current blockers** — All training/nutrition elements are within your control

---

## Accomplishments

What's already been completed or achieved in this project.

- **Current Scan (Jun 2, 2026):** 89.1kg | 43.6kg Muscle | 14.8% BFM (13.1kg) — **Flawless recomposition.** *(Win: +1.1kg muscle, -1.3kg fat in 3 weeks by removing Monday double + aligning fasting window.)*
- **Baseline (Apr 6, 2026):** 89.5kg | 43.8kg Muscle (+0.9kg) | 15.0% BFM (-1.8%)
- **Training System (✅):** 7-day modular architecture designed; "Do or Die" gym session locked in
- **Nutrition Protocol (✅):** 16:8 fasting + activity-aligned windows + 2,300 kcal macro split validated and sustainable
- **Recovery Framework (✅):** Sleep modes (A/B/C) defined; Brain Dump + 3-2-1 task system designed
- **Tracking Established (✅):** Weekly weigh-ins + body scans; BFM/SMM as primary metrics (not scale weight)
- **Scheduling System (✅):** Class Pool (all classes, intensity tags, priority tiers) + 9-rule Scheduling Framework (default/alternative/deload week, Mysore placement, muscle spacing, teacher preferences, choreo cycle tracking)
- **Calendar Integration (✅):** Google OAuth (Europe/Amsterdam), interactive planner in Claude Code, bidirectional sync (manual write + Saturday 8am launchd automation). Workflow leverages Class Pool + 9 Scheduling Rules. Weekly Schedule log tracks planned vs actual (auto-appended by Claude Code).
- **Data Architecture (✅):** `training_running_log.md` (daily energy/sleep/lifts), `Training_program_Weekly_Schedule.md` (weekly plans, awk-readable), `Training_program_evolvement/` (monthly session archives). Efficient reads via grep/awk — no full-file scans.
- **Session Roles (✅):** Weekly planning entirely in Claude Code (scheduler + calendar write + log append). Monthly review here in Cowork (pattern analysis, body scan, program decisions, session archive).

---

## Connections

**Parent Pillar:** [[PhysicalHealth)

**Related Pages:**
- [[Movement & Dance]] — Ballet, jazz, ashtanga practice
- [[Nutrition Mastery]] — Macro optimization and fasting protocols
- [[Body Composition]] — Muscle building and fat loss

**Related Coaching Sessions:**
- (To be populated)

**Related Projects:**
- (None yet)

---

**Note:** Weekly progress, body scans, and learnings logged in `_Training_program_trial_log.md`. This overview focuses on systems and current targets.

---

## Suggested Edits for Template Alignment

### What Changed:
1. ✅ **Header:** Simplified name; updated current_focus to specific body composition targets
2. ✅ **Objectives:** 3 clear goals (recomposition target, dance performance, aesthetic)
3. ✅ **Roadmap:** Changed to "Weekly Training Architecture" + "Nutrition Protocol" tables (execution-focused, not research-driven)
4. ✅ **Removed:** Verbose daily protocol descriptions (moved to reference docs if needed)
5. ✅ **Simplified Next Steps:** Focus on THIS WEEK measurements and data collection
6. ✅ **Added Accomplishments:** Current scan data + systems designed

### For Trial Log:
- Create `_Training_program_trial_log.md`
- Purpose: "Testing whether minimal resistance (1x/week) + dance + fasting can achieve <10% BFM while preserving 43kg+ muscle"
- Log: Weekly body weight, scan results, gym performance (e.g., "Deadlift: 150kg x 6"), subjective dance performance
- Track: When/if calories need adjustment, muscle retention metrics, progress toward 9kg BFM


## Deload Decision — 2026-06-12

**Deload week confirmed: June 23–29, 2026**

Context: CT-heavy week June 16 (daily CT replacing normal classes) → deload June 23 → Madrid/Pride travel June 30 (functional disruption, not a structured deload).

Variant A or B TBD in weekly planning session — check choreo cycle week before confirming. Rule 6 flag: confirm June 23 is not week 2 or 4 of choreo cycle.
- [ ] First Track A test: next Wednesday home by 10:30pm — shower + eat + 30-min timer → bed (from: [[coaching_20260620]])
- [ ] Sunday meal prep first execution: rice cooker + 8-10 eggs + one protein source while showering (from: [[coaching_20260620]])
- [ ] Pre-class eating: eat at work 5-5:30pm on training days, starting Monday (from: [[coaching_20260620]])
