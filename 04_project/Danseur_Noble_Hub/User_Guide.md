# Danseur Noble S&C Hub — 使用指南
_简明说明书 · 适合首次接触本系统的用户_

---

## 这是什么

一个为职业舞者设计的 AI 训练教练 PWA（可安装到手机桌面）。核心理念是：**系统替你做决策，你只需要执行或推翻。**

每天早上，它已经读取了你的睡眠数据、了解你今天的训练计划、知道你手头有哪些项目，然后直接给你一个具体的日程提案——不需要你先开口。

---

## 四个 Tab 是什么

### 1. Priming（晨间启动）
**目标：** 当天开始前，整理出今天最重要的 3 件事。

打开后会自动生成：
- 一段晨间简报（你的状态、今天的重点）
- **Top 3 任务卡**：每张卡有分类标签、建议时间、原因说明、时长调整
- 点击卡片上的 **Block** → 直接写入 Google Calendar「Focus Blocks」日历
- 点击卡片上的 ✓ → 完成后划掉，系统自动推出备选任务（Stretch 区域）
- 底部的 **Backlog 面板**：按 9 个生活领域分类，可调优先级、提升到 Top 3

> 未完成的 Top 3 任务会在次日早晨自动回流到 Backlog，不会丢失。

---

### 2. Today（今日训练）
**目标：** 执行当天的训练计划，实时记录。

页面结构从上到下：
- **Pulse（脉搏检测）**：填写今天的精力/压力评分（1–5）和身体感受；AutoSleep 自动写入睡眠数据（HRV、RHR、睡眠质量）
- **Readiness Banner（准备状态条）**：AI 根据你的状态给出今天的推荐（执行/降量/休息），有「Apply」按钮一键应用修改建议
- **Workout Cards（训练卡）**：今天的计划课表，点击 Gym 课程进入记录界面
- **Gym Logger（健身记录器）**：
  - 自动加载今日训练模板（Gym-A 或 Gym-B 交替）
  - 按组记录重量、次数，完成后自动保存
  - 右上角灯泡 💡 → 查看 AI 的本次训练建议（调整动作/减量）
  - 右上角 Deload 按钮 → 开启减量模式（重量 ×0.8，2 组）
  - 右上角 C/S 切换 → 每个动作可单独切换「条件/力量」模式
  - Rest Timer：固定在顶部，随时可见；完成组后振动提醒

> 7-Day Lookahead：Today 底部展示未来 7 天的计划，方便提前知道训练密度。

---

### 3. Coaching（教练对话）
**目标：** 回顾训练规律，讨论调整方向，AI 会主动提议具体改动。

**三个 Scope（右上角切换）：**
- **Training**：训练教练模式 — 加载你的训练数据（近 7 天），讨论能量趋势、训练合规性、gym 进展
- **Life**：生活教练模式 — 加载你的 POS（个人操作系统）和当前优先级，讨论任何生活领域
- **Priority**：优先级复盘模式 — 专注审视 P1/P2/P3 项目，找出需要重新排序或放弃的事情

**Training scope 专属面板（左上角按钮）：**
- **Active Rules**：查看当前所有调度规则（强度/频率/组合约束）
- **Insights**：AI 分析近 14 天数据生成的 2–4 条规律性发现
- **Schedule**：在 App 内生成 2 周训练日程，可拖动调整，确认后写入 Google Calendar

**AI 会自动做的事：**
- 当你分享身体信息 → 弹出「Save this?」卡，保存到教练背景知识库
- 当 AI 建议修改训练规则 → 弹出「Proposed rule update」卡，你选择 Apply 或 Dismiss
- 当 AI 建议新动作 → 弹出「Add to Exercise Bank?」卡，点击进入 Exercise Bank 确认

**End Session（结束会话）：**
消息累计 3 条以上后，输入框上方出现 End Session 按钮。点击后 AI 自动总结本次对话的决策和开放问题，保存到数据库供后续回顾。

---

### 4. Metrics（数据总览）
**目标：** 查看身体成分趋势和健身进展。

- **Body Scan**：体重、骨骼肌质量（SMM）、体脂率趋势图（14/30/90 天）
- **Gym PR 曲线**：每个动作的历史最大重量进展
- **Energy 趋势**：精力/睡眠/HRV 趋势（AM、PM、AutoSleep 推断值整合）
- **Exercise Bank 入口**：页面底部，管理和浏览所有训练动作

---

## 数据是怎么进来的

| 数据 | 来源 | 方式 |
|------|------|------|
| 睡眠（HRV、RHR、睡眠时长）| AutoSleep app | iPhone Shortcuts 自动推送 webhook |
| 精力/压力评分 | 用户手动 | Today tab AM/PM Pulse 填写 |
| 训练计划 | Google Calendar | Coaching tab Schedule 生成后写入 |
| 训练记录 | 用户手动 | Gym Logger 按组记录 |
| 身体成分 | 用户手动 | Metrics tab 录入体测数据 |
| 项目/优先级 | KMS Obsidian vault | GitHub Action 自动同步 |
| 晨间 Top 3 | AI 生成 | Priming tab 自动加载 |

---

## 几个常见操作

**修改今天训练强度：**
Today tab → Pulse 填好 → Readiness Banner 出现后点「Apply」

**记录一次 Gym 训练：**
Today tab → 点击 Gym 训练卡 → Gym Logger 打开 → 按组输入 → X 关闭（自动保存）

**生成下 2 周训练计划：**
Coaching tab → Training scope → Schedule 按钮 → Generate → 调整 → Confirm

**和 AI 聊想法并保存决策：**
Coaching tab → 对话 → 结束时点 End Session → 查看摘要卡

**提升明天要做的事到 Top 3：**
Priming tab → Backlog 面板 → 找到该 item → 点 Add → 关闭面板（处理合并冲突）

---

## 系统目前不做的事

- 营养追踪（Nutrition Module 在规划中）
- 原生 iOS 通知（Web Push 在规划中）
- 多用户支持（单人系统）
