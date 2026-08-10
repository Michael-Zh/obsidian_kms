---
name: Dance_Note
project_id: pj0015
status: reference
pillar: PhysicalHealth
type: reference-library
maintenance_rule: quarterly-review
last_reviewed: 2026-08-09
created: 2026-06-13
updated: 2026-08-09
priority: P3
tags:
  - PhysicalHealth
  - CreativityCuriosity
---

# Dance Note — Personal Movement Reference Library

## What This Is

个人舞蹈与身体技术的参考笔记库。不是 active project（无 deliverables、无开发任务），而是长期累积的课堂纠错、技术原则和身体感知记录的汇总。内容主要来自芭蕾、Countertechnique、Gaga/即兴、Hiphop、瑜伽、物理治疗等课堂。

**维护方式：人工维护**。每次课后或练习后，若有新的 cue 或 insights，直接追加到对应文件即可。

**App 读取规则：**
- `type: reference-library` + `status: reference` → 不生成常规 backlog items
- `maintenance_rule: quarterly-review` → 每季度检查一次是否需要整理回顾

## Maintenance — Quarterly Review

**触发条件：距上次整理超过 3 个月，或每个 quarter 开始时**

需要做的事：
- 扫一遍所有笔记文件，将仍然 relevant 的内容保留
- 将不再使用或已被更新的内容移到 _archive
- 确认 CT_Toolbox 分类是否仍然适用
- 标记任何需要补充或重新整理的领域
- 更新 `last_reviewed` 日期

## File Map

- CT_Toolbox.md — Countertechnique A–F 分类参考手册
- Ballet_Notes.md — 芭蕾课堂纠错 + 营养
- Dance_Creation.md — 艺术方向、即兴哲学、编舞思维
- Gaga_Improv_Notes.md — Gaga 原则 + 身体感知 + 练习
- Hiphop_Notes.md — Hiphop 课堂笔记
- Yoga_Notes.md — 瑜伽体式 + 辅助调整
- Physio_Notes.md — 身体结构不平衡 + 针对性训练
- Running_Notes.md — 跑姿 + 训练模式
- _archive/ — 已归档的旧版本
