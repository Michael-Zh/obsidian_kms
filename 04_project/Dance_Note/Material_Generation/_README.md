---
name: Material_Generation
description: Session log for self-directed improvisation — raw material generated, for later choreographic use
updated: 2026-09-04
tags:
  - PhysicalHealth
  - CreativityCuriosity
---

# Material Generation — Session Log

起因：根特 workshop（2026-08）给了大量 improvisation tools，research 变得有意思，想把 generate 出来的 material 沉淀下来作为日后创作素材。

## 这个文件夹装什么（以及为什么不放进现有的两个地方）

vault 里已经有两层：

| 层 | 位置 | 装什么 |
|---|---|---|
| 原始笔记 | `Dance_Note/`（CT Toolbox A–F、workshop notes） | 课上学到的**工具和原则** |
| 蒸馏知识 | `02_wiki/PhysicalHealth/Improvisation.md`、`Dance_Creation.md` | 对即兴与创作的**理解、方法论、research questions** |

**Material 是第三类**：某次 session 里做出来的一段东西。它既不是学到的道理，也不是课堂记录，而是**未来创作的原料**。混进上面任一层都会被淹没——原则会被素材冲淡，素材会被原则埋掉。

所以这里只装原料，按日期一个文件。可复用的洞察定期蒸馏回 `Improvisation.md`；成形的创作想法去 `Dance_Creation.md`。**这两个 wiki 文件是蒸馏终点，本文件夹是原料库。**

## 节奏

两周一次起步（2026-09-04 定）。Quota 算 0.25——self-paced，没有课堂的强度爬升，CNS 成本接近一次 gym 而不是一节课。

地点待定：CREA（阿姆斯特丹）有 educational / cultural discount，但需要花时间做 setup。Setup 之前可以先在任何有空间的地方做，不要让场地阻塞开始。

## 每次记三样

用 `_TEMPLATE.md` 复制。三样就够，不要写成日记：

1. **用了什么** — tool / prompt / score / constraint
2. **生成了什么** — 文字描述 + 手机录像链接（录像是主，文字是索引）
3. **哪一段值得留** — 这条最重要。不标的话三个月后回看等于没记

## 输入方式（2026-09-04 定）

**直接跟 CC 说**，我整理成文件。练完口述三样即可，不需要自己排版。

先这样跑两次再决定要不要建管道 —— 跑过才知道你实际想记什么。备选是走已有的 Telegram bot（`@Formichae_clipper_bot` → `knowledge_inbox` 表，Session 49 建的），练完立刻发文字 + 录像链接，下次 session 开场批量处理。那条需要加一个 material 分支，约 20 分钟，等真需要即时记录时再做。

## 录像放哪（2026-09-04 定）

```
~/Library/Mobile Documents/com~apple~CloudDocs/Dance_Material/
```

**vault 外、iCloud 内。** 笔记里用绝对路径链接指过去。

为什么不放 vault 里：vault 现在 508M / 1088 个媒体文件，录像会长得很快。而 vault 本身就在 `iCloud~md~obsidian/` 容器下 —— **只要文件在 vault 里就会被 iCloud 同步**，`.gitignore` 和 Obsidian 的 `userIgnoreFilters` 都管不到 iCloud 那一层。放到普通 iCloud Drive 就三层全避开：不进 git、不进 Obsidian 索引、不算进 vault 体积，而手机拍完照样同步（录像是手机拍的，这条是必须的）。

兜底：`.gitignore` 与 `.obsidian/app.json` 的 `userIgnoreFilters` 各加了一条 `Dance_Material/` —— 万一哪天有文件误落进 vault，不会进仓库也不会污染搜索。

## Connections

- [[Improvisation]] — 蒸馏终点：对即兴的理解与方法论
- [[Dance_Creation]] — 蒸馏终点：成形的创作想法
- [[Dance_Note]] — CT Toolbox 与 workshop 原始笔记
- [[Training_Program]] — 训练哲学与 quota（material generation 算 0.25）
