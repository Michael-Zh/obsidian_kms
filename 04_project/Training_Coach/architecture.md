# Danseur Noble S&C Hub — 架构与功能详解
_面向开发者和项目 Owner 的深度说明 · 2026-07-14_

---

## 一、系统定位与设计哲学

这不是一个普通的健身 App，也不是一个普通的任务管理工具。它是一个**个人执行操作系统的移动端界面**，以训练管理为核心，向上延伸到跨领域的日常优先级管理。

**三层架构：**
```
KMS Obsidian Vault（知识/策略层）
        ↓ GitHub Action 自动同步
Supabase PostgreSQL（结构化实时数据层）
        ↓ Next.js API Routes 读写
PWA 前端（执行界面层）
```

- **Obsidian** 是 narrative 层：POS、优先级、项目文档、coaching notes 住在这里
- **Supabase** 是 operational 层：训练记录、日程、身体数据、对话历史住在这里
- **App** 是执行层：两个数据源在这里汇合，AI 在这里做推理，用户在这里行动

---

## 二、数据流与外部集成

### 2.1 AutoSleep → 睡眠数据
```
AutoSleep app
  → iPhone Shortcuts（每天早晨自动触发）
    → POST /api/webhook/health
      → 写入 daily_metrics（sleep_hours, recharge_pct, hrv, rhr, baseline_hrv）
      → 同时推断 inferred_energy_score（recharge_pct → 1-5）
         和 inferred_stress_score（HRV vs baseline）
```
不需要用户手动导出。Shortcuts 运行后数据 1–2 分钟内出现在 Today tab。

### 2.2 Google Calendar ↔ 训练日程
**写方向（App → Calendar）：**
- Coaching tab Schedule panel：生成 2 周日程 → 用户确认 → `POST /api/schedule/approve` → `googleapis` 写入 Google Calendar
- Priming tab：Top 3 任务 → Block 按钮 → `POST /api/priming/block` → 写入「Focus Blocks」专属日历（首次自动创建）

**读方向（Calendar → App）：**
- 每天 UTC 10:00，`/api/cron/reconcile` 读取 Google Calendar，同步训练状态（completed / skipped）到 `workouts` 表
- Today tab 的 7-Day Lookahead 从 `workouts` 表读取

### 2.3 KMS Vault → Supabase（sync-context）
```
obsidian_kms GitHub repo push
  → GitHub Action（路径过滤：_POS.md / _priority.md / 04_project/**）
    → scripts/sync-context.py
      → 解析 markdown → upsert context_snapshots（pos/priority key）
      → 解析 04_project/**/*.md → upsert projects_state（每个项目文件一行）
```
这条管道是单向的（vault → DB），让 App 能在不直接调用 GitHub API 的情况下读取项目状态。目前 Priming tab 和 Coaching tab 在运行时直接读 GitHub API；`context_snapshots` / `projects_state` 表为未来的离线/低延迟访问预留。

### 2.4 OpenRouter → AI 推理
所有 AI 调用走 OpenRouter，两个模型：

| 模型 | 用途 |
|------|------|
| `deepseek/deepseek-v3.2-exp`（DEEPSEEK_MODEL）| Coaching chat — 长上下文推理，规则提议 |
| `google/gemini-2.5-flash-lite`（FLASH_MODEL）| 结构化 JSON 任务 — Pulse 推断、Priming 生成、Insights、摘要 |

DeepSeek 用于需要深度理解训练上下文的对话；Flash 用于有明确输出格式、需要快且便宜的批处理任务。

---

## 三、核心功能模块详解

### 3.1 两级规则系统（Two-Tier Rule System）

训练调度的核心机制，所有 AI 推理都在这两层约束下运行：

**Hard Constraints（`scheduling_constraints`）：**
- 不可违反的外部限制：固定的舞蹈课时间表、身体康复限制
- AI 的调度提议必须绕开这些约束，不能建议冲突时间段

**Soft Guidelines（`scheduling_guidelines`）：**
- AI 可以动态调整的软规则，每条带有 `strength`（0.0–1.0）权重
- 类型：`recovery`、`volume_target`、`sequencing`、`preference`、`deload`、`rolling_window`
- Coaching tab 里 AI 可以提议修改规则参数（`rule_update_proposal` JSON），用户 Apply/Dismiss
- 每次调整都有 `last_updated_by: "coaching_loop"` 记录来源

这套系统的价值在于：规则不是代码写死的，而是数据库里的数据，可以随用户身体状态和训练阶段演进。

### 3.2 Rebellion & Consequence Engine（违规追踪引擎）

当用户的实际行为与 AI 建议冲突时，系统自动标记并追踪后果：

**触发条件（在 reconcile cron 里检测）：**
1. AI 写了 `ai_modification_note`（建议修改）但训练仍标记为 `completed`
2. 当天实际训练次数 > 计划次数，且当天 energy ≤ 2 或 HRV < 85% baseline

**后续逻辑：**
- `workouts.forced_override = true` 标记
- `analyze-state` API 加载 7 天 override 历史 + 次日能量/HRV 后果
- 注入 AI system prompt，让下次 readiness note 能说「上次你在疲劳时强行训练，次日 HRV 下降 15%」

这是「从经验中学习」机制的基础设施。当前数据还少，但随着使用积累会越来越有效。

### 3.3 Gym Logger 的状态管理

GymLoggerSheet 是 App 里最复杂的组件，以下是关键状态逻辑：

**开启流程：**
1. 读取当天 `workout_id`
2. 查询 `gym_logs`，若已有记录（in-progress session）→ 恢复之前的进度
3. 若无记录 → 从 `gym_templates` 加载模板，调用 `generateSessionPlan.ts` 生成 AI 建议（或从 `gym_session_plans` 读缓存）
4. 计算每个肌群的 Freshness（基于 `gym_logs` 历史 + 舞蹈课 drain 系数）

**自动保存：**
每组完成后立即 upsert `gym_logs`，key 是 `(workout_id, exercise_name, set_number, is_warmup)`。Warmup 用负数 set_number（-1/-2）区分。关闭即结束，无需「Finish」按钮。

**1RM 计算：**
Epley 公式（`weight × (1 + reps/30)`），排除 deload session 的历史记录，live 显示 `~XX% 1RM`。

**Deload + Training Mode 叠加：**
- Deload：重量 ×0.8，固定 2 组
- Conditioning：1RM×0.65 / 12 reps / 3 sets / 90s rest
- Strength：1RM×0.82 / 5 reps / 4 sets / 150s rest
- 两者可叠加（Deload Conditioning = 0.65×0.8 = 0.52 × 1RM）

### 3.4 Priming Tab 的数据组装

每次打开 Priming tab，`POST /api/priming` 并行拉取：

```
KMS GitHub API:
  ├─ _POS.md（个人操作系统）
  ├─ _priority.md（当前优先级）
  ├─ 01_raw/coaching/ 最新 coaching 文件
  └─ _in_case_you_are_bored.md（Active Projects + Backlog Ideas）

Supabase:
  ├─ daily_metrics（今日睡眠/精力数据）
  ├─ workouts（今日训练计划）
  └─ priming_backlog（用户积累的 backlog items）
```

所有内容合并成 system prompt，FLASH_MODEL 生成 `{ brief_markdown, top3[], backlog[] }` JSON。

**次日回流逻辑：**
`GET /api/priming` 检测今日无 brief 时，读取昨日 `priming_top3`，过滤 `done=false` 的 item → `POST /api/priming/backlog` 插入（task 名去重）。用户第一次打开时已经能看到昨日未完成的事项在 Backlog 里。

### 3.5 Coaching 多 Scope + 对话持久化

三个 scope 对应三种 AI 人格和数据集：

| Scope | AI 角色 | 数据来源 |
|-------|---------|---------|
| training | 训练分析师 | Supabase 近 7 天训练数据 + 规则 + 体成分 |
| general | 生活教练 | KMS _POS.md + _priority.md + 最新 coaching 文件 |
| priority | 战略复盘 | 同 general + 更聚焦于 P1/P2/P3 审视 |

对话通过 `coaching_messages` 表持久化（`project_id = scope`），切换 scope 自动加载对应 thread 的最近 40 条消息。

**Session 摘要流程：**
```
End Session 按钮点击
  → POST /api/coaching/summarize
    → FLASH_MODEL 分析整段对话
    → 提取 summary（2-3句）/ decisions（[]）/ open_items（[]）
    → INSERT coaching_sessions（带 scope、project_id、session_date）
    → 前端显示 Summary 卡片
```

`decisions` 带 `project` tag，为未来的 `sync-decisions` 脚本（将决策回流到 Obsidian 项目文档）预留接口。

### 3.6 Proactive Insights（主动洞察）

每次打开 Coaching tab（且今日无缓存）时触发：

```
GET /api/coaching/insights
  → 拉取 14 天 daily_metrics + workouts + gym_logs + coaching_context
  → FLASH_MODEL 生成 2-4 条模式发现
    每条：{ title, observation, category, priority }
    category: energy / recovery / training / sleep
  → 缓存到 localStorage（key: dnhub_insights_YYYY-MM-DD）
  → badge 数量同步到 BottomNav
```

同一天刷新不重复调用 AI。用户 dismiss 单条 → 从 localStorage 缓存移除。

---

## 四、数据库表全览

### 核心训练表
| 表 | 用途 |
|----|------|
| `daily_metrics` | 每日体征（睡眠/HRV/RHR/精力评分/脉搏文本） |
| `workouts` | 训练计划条目（日期/类型/状态/AI 修改建议） |
| `gym_logs` | 每组训练记录（动作/组数/重量/次数/warmup标记/顺序） |
| `gym_session_plans` | AI 预生成的每日训练建议（6am cron 缓存） |
| `exercises` | 动作库（肌群/器械类型/默认参数/休息时间） |
| `gym_templates` | 用户自定义训练模板（Gym-A / Gym-B） |
| `body_scans` | 体成分记录（体重/SMM/BFM%） |

### 规则与教练表
| 表 | 用途 |
|----|------|
| `scheduling_guidelines` | 软规则（AI 可调整，带 strength 权重） |
| `scheduling_constraints` | 硬约束（固定课程时间表） |
| `coaching_context` | 持久化用户背景信息（伤病/偏好/限制） |
| `coaching_logs` | 历史 coaching 记录（key findings / action items / rule updates） |
| `coaching_messages` | 对话历史（按 project_id 分 scope thread） |
| `coaching_sessions` | Session 摘要（decisions + open_items，带 project routing tag） |

### 系统 / Life OS 表
| 表 | 用途 |
|----|------|
| `priming_backlog` | Priming tab 的 backlog items（9 pillar 分类，优先级） |
| `context_snapshots` | KMS vault 快照（pos/priority，GitHub Action 写入） |
| `projects_state` | 项目状态快照（标题/status/next_actions，GitHub Action 写入） |

---

## 五、API 路由总览

### Today Tab
| 路由 | 方法 | 用途 |
|------|------|------|
| `/api/today` | GET | 今日 workouts + daily_metrics；`?lookahead=7` 返回 7 天 |
| `/api/infer-pulse` | POST | AM/PM 脉搏文字 → AI 解析精力/压力/修改建议 |
| `/api/analyze-state` | GET | 综合状态分析 → readiness banner 文字 |
| `/api/workouts/[id]` | PATCH | 应用 AI 修改建议到 workout |
| `/api/webhook/health` | POST | AutoSleep → daily_metrics 写入（无 auth） |

### Gym Logger
| 路由 | 方法 | 用途 |
|------|------|------|
| `/api/gym/session-review` | POST | 按需生成 AI 训练建议（lightbulb fallback） |
| `/api/gym/logs` | GET/POST | gym_logs 读写 |
| `/api/gym-templates` | GET | 读取用户模板 |
| `/api/gym-templates/[id]` | PATCH | 更新模板（AI template proposal apply） |
| `/api/exercises` | GET/POST | 动作库读写 |
| `/api/exercises/[id]` | PATCH | 更新动作 |

### Coaching
| 路由 | 方法 | 用途 |
|------|------|------|
| `/api/generate-log` | POST | Coaching chat（支持 scope 参数） |
| `/api/coaching/insights` | GET | 生成/读取 proactive insights |
| `/api/coaching/priorities` | GET | 读取 KMS `_priority.md` 解析结果 |
| `/api/coaching/summarize` | POST | Session 结束摘要 → coaching_sessions |
| `/api/coaching-context` | POST | 保存 context_capture_proposal |

### Schedule
| 路由 | 方法 | 用途 |
|------|------|------|
| `/api/schedule/generate` | GET | 生成 2 周训练日程提案 |
| `/api/schedule/adjust` | POST | 调整日程（chat 指令） |
| `/api/schedule/approve` | POST | 确认日程 → Google Calendar 写入 |
| `/api/cron/reconcile` | GET | 每日 cron：Calendar → workout 状态同步 |

### Priming
| 路由 | 方法 | 用途 |
|------|------|------|
| `/api/priming` | GET/POST | 读取/生成晨间 brief + top3 + backlog |
| `/api/priming/top3` | PATCH | 更新 top3（check/duration/promotion） |
| `/api/priming/backlog` | GET/POST/PATCH | Backlog CRUD + 优先级调整 |
| `/api/priming/block` | POST | Top3 item → Google Calendar Focus Blocks |

### Metrics
| 路由 | 方法 | 用途 |
|------|------|------|
| `/api/metrics` | GET | 体成分 + gym PR + 精力趋势数据 |
| `/api/body-scan` | POST | 录入体成分数据 |

---

## 六、目前能力边界

### 已具备
- 基于睡眠/HRV/精力的动态训练调整，有历史后果追踪
- 完整的 gym 训练记录（warmup、1RM、deload、C/S 模式、断点续记）
- AI 对话中实时提议规则变更、动作新增、训练模板调整
- Coaching session 结束后结构化摘要（decisions 带 project tag）
- 跨域晨间规划（训练 + 项目 + 优先级合并到 Top 3）
- KMS vault 变更自动同步到 Supabase（GitHub Action）
- 对话历史跨设备持久化（按 scope 分 thread）
- Google Calendar 双向集成（读取冲突 + 写入日程/Focus Blocks）

### 尚未具备
- **Web Push 通知**：训练前 30 分钟提醒（技术方案已设计，待实现）
- **营养模块**：减量周热量调整等（规划中）
- **coaching decisions 回流 Obsidian**：`sync-decisions` 脚本（表结构已建好，脚本待写）
- **context_snapshots 的实际消费**：表已建好，App 尚未从这里读取（当前仍直接调 GitHub API）
- **AI Substitution**：swap 动作时按 AI 评分排序候选（前置数据结构已就绪）
- **体成分录入 UI**：当前需要直接操作数据库，in-app 录入在 backlog

---

## 七、关键设计决策记录

**为什么不做原生 iOS App？**
iOS 17+ Web Push 已覆盖通知需求；AutoSleep + Shortcuts 的 webhook 方案对 HealthKit 够用；solo-dev 不值得引入 Xcode + App Store 运维成本。PWA 优先，能力边界被突破时再评估 Capacitor。

**为什么 DeepSeek 而非 GPT-4？**
Coaching 对话需要理解大量中文上下文（训练日志、身体感受描述），DeepSeek V3 在中英混合场景下效果优秀，且成本显著低于 GPT-4o。Flash 任务用 Gemini 2.5 Flash Lite 进一步降低成本。

**为什么规则存数据库而非代码？**
规则会随用户身体状态、训练阶段、季节演进。数据库规则可以被 AI 通过对话修改，不需要代码部署。这是「从经验中学习」能力的基础。

**为什么 coaching_messages 用 project_id 而非 user_id？**
同一用户有多个 scope（training / general / priority），每个 scope 是独立的对话 thread。`project_id = scope` 让切换 scope 时能加载对应历史，互不干扰。未来可以扩展为真正的项目级对话（`project_id = "Training_Coach"`）。
