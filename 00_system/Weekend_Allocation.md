---
name: Weekend_Allocation
description: 周末大块时间的分配方法 — 判定规则、四步流程、采购拆分
updated: 2026-09-04
---

# Weekend Allocation — 方法

> 稳定参考。**活的部分（待排队列 + 当前分配）留在 `_priority.md`**，因为那是每次要看的。
> 本文件不进 AI payload（`sync-context.py` 只同步 `_POS.md` 与 `_priority.md`）。

*周末是最稀缺的资源，且部分不可预测（海牙 / 临时演出）。所以不排「哪天做什么」，只排「哪个周末归谁」。*

**已做进 App（Session 53）—— 本节不再手工维护状态**

Coaching tab → `weekends` scope → **Weekend Allocation** 面板。它读 calendar 判可用性，从 backlog 按 deadline 取任务，写 placeholder 进主 calendar。

判定规则（2026-09-03 定）：

| Location calendar | 主 calendar | 判定 |
|---|---|---|
| **为空** | 无硬安排 | 🟢 **可安排** — 默认在阿姆斯特丹 |
| **为空** | 有硬安排（show/office/social/tbc） | ⚠️ **有硬安排** — 通常会吃掉周边时间 |
| **有任何值** | — | 🔒 **外出** — 值只表示「不在家」，不限于海牙 |

**Placeholder 机制：** 写进主 calendar，标题 `LMS: <任务>` 或 `PJ: <任务>`（挂到 KMS 项目的用 `PJ`，其余 `LMS`）。默认**周六 14:00–18:00**。marker 的作用是让 app 下次读的时候认出「这是 AI 放的占位」而不是「我自己承诺的事」——所以它不计入占用判定，可以在 calendar 里自由拖动或删除。

**方法：月初一次，五分钟**

1. **打开面板**，它自动给出建议（每个 🟢 周末一件，按 deadline 最早优先）
2. **逐条跳过不想要的**，然后写入主 calendar
3. **⚠️ 和 🔒 周末不分配任何事**，⚠️ 是缓冲；真的空出来就从队列顶部拿一件
4. **每件大块事项带一个 deadline。** 被挤掉就顺延到下一个 🟢；**顺延到超过 deadline，就是降 scope 或改 deadline 的信号**——不是再顺延一次

第 4 条是这套方法唯一需要人判断的地方，app 不替你做。

**关键拆分：把「采购」从「执行」里拆出来。** 植物这类事之所以吃掉整个下午，是因为「诊断 → 去店里买 supply → 动手」串成了一条链。先用工作日十分钟做诊断、列出 supply 清单，采购挪到工作日晚上或线上，周末那个半天就只剩纯执行——半天变成两小时，而且能排进 ⚠️ 周末。

**队列来源：** App 面板读的是 `priming_backlog`（app DB），不是本文档。所以下方队列是**给人看的策略视图**，实际排序在 app 里跑。两边任务名保持一致即可对上。

**⚠️ 边界（2026-09-03 定）：** backlog 是「要做什么」的唯一真相源；项目文件的 `## Strategic Direction` 是**策略叙述**，只作为 AI 的 prompt 上下文（帮 priming 挑 top3），**不判定任务是否完成**。此前 app 的 re-sync cascade 会把不在 Strategic Direction 里的 backlog 项静默标 done —— 已修（app Session 54）。所以：往 Strategic Direction 里写东西不会创建 task，从里面删东西也不会完成 task。要动 task 就去 backlog。

*（`scripts/weekend_status.py` 是这个功能的前身，需单独走 Google OAuth，已被 app 内实现取代。保留作离线备用，不需要配。）*
