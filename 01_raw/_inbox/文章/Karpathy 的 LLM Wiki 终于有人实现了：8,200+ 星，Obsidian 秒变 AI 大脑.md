---
author: 新世界圆圆圆
source: 微信公众号
url: https://mp.weixin.qq.com/s?__biz=MzYzNDI1MTg0Nw==&mid=2247484120&idx=1&sn=59132d978f5a7400eeb0f9a2311ba3c8&chksm=f198c5e4242b17a93ba186f441d45b8b9a62db54076a607b206bee583104721dd63c17317846&mpshare=1&scene=1&srcid=0730IX5U58VmUCQsFZjr6a8Y&sharer_shareinfo=cd3f12741c62be2c96743dcdbdcc0775&sharer_shareinfo_first=cd3f12741c62be2c96743dcdbdcc0775#rd
saved: 2026-07-30 11:53:42
tags:
  - 笔记同步助手
annotation:
id: 7613ddfb-7bbb-4b2d-b709-d726d424d4fb
---

公众号名称：赛博虾酱

作者名称：新世界圆圆圆

发布时间：2026-06-30 07:50

> 项目：claude-obsidian / AgriciDaniel  
> Stars：8,221 ⭐ | Forks：942  
> 兼容：Claude Code + Obsidian  
> 基于：Karpathy 的 LLM Wiki pattern

## 一句话介绍

**把 Obsidian 变成一个会自己长大、自己维护的 AI 知识库。** 往里面扔任何资料——论文、文章、网页、本地文件，Claude 自动读取、提取实体和概念、交叉引用、分类归档。下次提个问题，Claude 从你读过的所有内容里综合回答，引用的是具体的知识图谱页面，不是训练数据。15 个 Skills 覆盖从资料摄入到自主研究到知识审查的完整工作流。支持 LYT / PARA / Zettelkasten 四种方法论模式。

![[01_raw/_inbox/文章/images/5ba860f0058ccc6bc476648bbd6d1af3_MD5.gif]]

---

## 开篇：一个研究者的周二下午

你关注了一个领域三个月。收藏了 47 篇 PDF，浏览器书签攒了两百多个，笔记散落在 Notion、Apple Notes、Obsidian 各个角落。

周二下午，有人问了一句："你觉得这个领域最近最值得关注的方向是哪个？"

你翻了十分钟笔记，发现你在三篇不同的文章里记过相关的信息。但你记得你还看过一篇去年夏天的大部头，讲了很深刻的判断——那篇放在哪了？

大多数人的结局是：打开 Google 重新搜一遍，然后回复一个不那么自信的答案。

如果用 claude-obsidian 的话：那个大部头被 Claude 消化过，里面提取的实体和概念已经在你的知识图谱里了。你问 Claude "这个领域关注什么"，它直接从知识库里综合生成答案——引用的是你自己的 wiki 页面，不是训练数据。你不用再搜，**因为知识库替你记住了。**

![[01_raw/_inbox/文章/images/85544889f9b7d416b67d8d8b8ebf018b_MD5.png]]

---

## 为什么值得关注

### 1\. Karpathy 的 LLM Wiki 模式，这次有人完整实现了

2024 年，Andrej Karpathy 公开了一个 Obsidian 仓库的片段，展示了他怎么用 Obsidian + LLM 做知识管理。他管这个模式叫"LLM Wiki"。

核心思路：

-   • 你把原始资料扔进 Obsidian
    
-   • LLM 读资料，提取实体和概念
    
-   • 生成页面，交叉引用
    
-   • 你的知识图谱越长越大，越用越值钱
    

Karpathy 发出来的只是片段——几页截图、一段描述、一句"Cool idea"。没人做成完整的工具。

claude-obsidian 把那个模式做成了一个完整工具：

-   • 自动摄入（1 个命令，3 种方式）
    
-   • 自动提取（实体、概念、关系）
    
-   • 自动分类（按你选的方法论模式组织）
    
-   • 自动维护（死去的节点、悬空链接、过时声明）
    
-   • 混合检索（BM25 + 上下文前缀 + 余弦重排）
    

### 2\. 自动摄入资料，Claude 帮你做"第一次阅读"

这个工具最省时间的部分是摄入（Ingest）。

你扔一个文件（PDF、网页、说不清格式的文档）进去。Claude 做四件事：

-   -   **提取实体**——资料里提到了哪些人、哪些概念、哪些组织
-   -   **提取概念**——资料在讲什么主题，核心观点是什么
-   -   **建立交叉引用**——这些实体和概念在你的知识图谱里已经存在吗？如果有，怎么关联？
-   -   **生成页面**——按你的方法论模式（LYT / PARA / Zettelkasten / Generic）把东西归档

整个过程你不用打开资料。你扔，Claude 读，Claude 写。

### 3\. 15 个 Skills，覆盖知识管理的全生命周期

项目自带 15 个 Skills。不是硬塞进来凑数的——每个 Skill 对应知识管理的一个阶段：

## 摄入阶段

-   -   `/wiki-ingest` —— 读资料，提取，生成页面
-   -   `/save` —— 把当前对话归档为 wiki 页面
-   -   `/wiki` —— 第一次进入时的脚手架，引导你配置

## 查询阶段

-   -   `/wiki-query` —— 从知识库里问问题，Claude 按「热度缓存 → 索引 → 钻取页面」三步走
-   -   `/wiki-retrieve` —— 混合检索，三管齐下找最相关的页面

## 维护阶段

-   -   `/wiki-lint` —— 死去的节点、悬空链接、过时声明、缺少交叉引用，8 类问题一次扫清
-   -   `/wiki-fold` —— 日志归档折叠（DragonScale 扩展，可选）

## 扩展阶段

-   -   `/autoresearch` —— 自主研究循环，自己定问题、自己搜、自己综合、自己归档
-   -   `/wiki-mode` —— 方法论模式路由器，按 LYT / PARA / Zettelkasten / Generic 组织
-   -   `/wiki-cli` —— Obsidian CLI 传输层，多写安全

## 高阶能力

-   -   `/canvas` —— 视觉层，图片、PDF、wiki 页面钉在画布上
-   -   `/defuddle` —— 网页提取包装器，清洗不安全的输入
-   -   `/think` —— 10 条原则的思考框架，适合"这个问题我想不清楚"的时候
-   -   `/obsidian-bases` —— Bases dashboard schema 参考
-   -   `/obsidian-markdown` —— Obsidian Flavored Markdown 语法参考
-   -   `/wiki-fold` —— 日志折叠归档

### 4\. 知识库不是存放笔记的地方，是"第二大脑"的载体

大多数 Obsidian AI 插件做的是"在你的笔记上做聊天界面"。你把它当一个更聪明的搜索框。

claude-obsidian 做的不一样：

-   -   **笔记不是死的，是活的。** 新资料进来，旧笔记会自动被交叉引用、重新关联
-   -   **知识不是按文件夹堆的，是按图谱长的。** 你的 wiki 的连接密度随每次摄入增加
-   -   **记忆不是靠你手动维护的，是靠热度缓存。** 每次会话结束，Claude 刷新一份热度上下文（～500 字）——下次进入时，它记得上次你们聊到过哪里

用项目自己的话：

> "Knowledge compounds like interest."

### 5\. 四种方法论模式，不用重新发明轮子

过去用 Obsidian 最纠结的是"我的笔记应该怎么组织"。

claude-obsidian 直接把四种主流方法论做成了第一级别的配置（v1.8+）：

| 模式 | 哲学 | 适合的人 |
| :-- | :-- | :-- |
| **Generic** | 没有主张，纯按来源、实体、概念归档 | 不想被任何体系约束的人 |
| **LYT（Linking Your Thinking）** | 笔记之间链接，文件夹不重要 | 喜欢网状结构、讨厌分类目录的人 |
| **PARA（Tiago Forte）** | 按行动性组织——项目、领域、资源、归档 | 讲究 GTD 和项目管理的人 |
| **Zettelkasten（Luhmann）** | 原子化笔记、时间戳唯一 ID、密集双向链接 | 做深度学术研究、写长篇论文的人 |

四种模式可以随时切换。切换后不会自动迁移已有文件——新进来的资料按新模式归档，旧笔记保持不变。

### 6\. 多写安全，团队协作不掉链子

项目从 v1.7 开始有完整的 per-file advisory locking：

-   • 多个摄入 agent 并行工作时，同一文件不会被两个 agent 同时写
    
-   • 锁文件 60 秒自动释放，不会因为异常导致死锁
    
-   • PostToolUse hook 在提交前检查锁列表，写入中的文件不提交
    

这看起来是个小细节，但对于多人共用同一个知识库的团队来说，是唯一能保证数据安全的做法。

![[01_raw/_inbox/文章/images/0437e3bca2639e78a342656e88f20a1a_MD5.gif]]

---

## 核心工作流

### 第一次进入（5 分钟）

```
git clone https://github.com/AgriciDaniel/claude-obsidian
cd claude-obsidian
bash bin/setup-vault.sh
```

打开 Obsidian → 把这个文件夹当 vault → 打开 Claude Code：

```
/wiki
```

Claude 问你唯一一个问题："这个知识库是做什么用的？"（你做科研？做商业调研？是个人笔记？写一本书？）

它按你的回答自动生成完整结构——索引页、热度缓存、日志、Dashboard、模板、颜色配置。

### 日常使用

你每看到一篇相关的文章：

1.  1\. 扔进 `.raw/` 文件夹
    
2.  2\. 告诉 Claude："digest this file"
    
3.  3\. Claude 读完，提取，建页面
    

你想回忆之前的发现：

1.  1\. 问："我记得之前看过一篇关于 X 的论文，是什么情况？"
    
2.  2\. Claude 先从热度缓存查
    
3.  3\. 没有就翻索引
    
4.  4\. 还不够就钻到具体 wiki 页
    
5.  5\. 综合回答你，引用具体页面
    

你想自己探索：

```
/autoresearch 当前领域最值得关注的研究方向
```

跑三轮：广泛探测（5-8 个查询）→ 填补空白（目标搜索）→ 综合检验（最终一轮）。最终输出一份综合页 + N 个来源页 + N 个实体页，全部交叉引用。

---

## 和其他 AI 笔记插件的区别

<table style="color: rgb(63, 63, 63); border-collapse: collapse"><caption></caption><colgroup><col><col><col><col></colgroup><tfoot><tr><td style="border: 1px solid \#ddd; padding: 6px 10px"></td></tr></tfoot><colgroup><col><col><col><col></colgroup></table>

| <br> | claude-obsidian | Smart Connections | Obsidian Copilot |
| :-- | :-- | :-- | :-- |
| 自动组织笔记 | 建实体、概念、引用 | ❌ 仅相似匹配 | ❌ 仅对话 |
| 矛盾检测 | `[!contradiction]`标注 | ❌ | ❌ |
| 会话记忆 | 热度缓存跨会话持久 | ❌ | ❌ |
| 知识库维护 | 8 类 lint 检查 | ❌ | ❌ |
| 自主研究 | 3 轮自动研究 | ❌ | ❌ |
| 方法论模式 | LYT/PARA/Zettelkasten/Generic | ❌ | ❌ |
| 思考框架 | 10 条原则可调用 | ❌ | ❌ |
| 多模型支持 | Claude, Gemini, Codex, Cursor, Windsurf... | 仅 Claude | 部分多模型 |
| 视觉画布 | canvas 布置 | ❌ | ❌ |
| 多写安全 | per-file advisory locks | ❌ | ❌ |
| 引用具体页面 | 引用 wiki 页 | 引用相似笔记 | 引用笔记 |
| 批量摄入 | 并行 agents | ❌ | ❌ |

---

## 快速开始

```
git clone https://github.com/AgriciDaniel/claude-obsidian
cd claude-obsidian
bash bin/setup-vault.sh
```

然后：打开 Obsidian → 打开这个文件夹作为 vault → 打开 Claude Code：`/wiki`

完整 5 分钟。想跳过 setup 脚本？直接把仓库根目录的 `WIKI.md` 复制到你的 vault 根目录也行。

---

## 适用场景

-   -   **研究人员** —— 论文读了 30 篇，但每篇的核心观点散落在各处？全部扔进来，Claude 一次性整理
-   -   **内容创作者** —— 写稿需要查以前做的笔记？提问时要引用具体来源页面
-   -   **投资人 / 咨询** —— 行业研究、竞品分析，需要长时间积累
-   -   **学生** —— 课程笔记积累了大半个学期，考前想快速发现联系
-   -   **Obsidian 深度用户** —— 爱 Obsidian 但恨手动维护，想要"自己长大"的笔记库

不太适合：

-   • 只需要对话式问答（不要用这个——直接用网页版 Claude 就行）
    
-   • 没有 Claude Code（虽然兼容 Codex、Cursor 等，但生产级测试只覆盖 Claude Code）
    
-   • 需要实时云端同步多设备（需要自己搭 Obsidian Sync 或 Git）
    

---

## 常见问题

**和 Karpathy 原始版本有什么区别？**  
Karpathy 发的只是片段——几十页截图，没有代码。claude-obsidian 是完整的可运行工具。15 个 Skills、四种方法论、多写安全、混合检索——都是 Karpathy 那个片段里没展开的。

**要不要付费？**  
不用。MIT 协议，所有核心功能完全免费。付费渠道（AI Marketing Hub Pro）只是提前拿到开发中的功能——收费的功能最终也会免费放回公开版。

**多设备怎么办？**  
知识库本质是一个 Markdown 文件夹。配合 Obsidian Sync、Obsidian Git 或任意文件同步工具就行。

**数据隐私呢？**  
默认所有检索都在本地（BM25 + 本地 ollama 向量检索）。上下文前缀 API 层需要一个单独的 `--allow-egress` 参数才会启用——默认不启用。

---

## 总结

claude-obsidian 的核心洞察：**大多数 Obsidian AI 插件做的是"在你现有的笔记上做更好的搜索"。它做的是"让笔记自己长大"。**

1.  1.  **自动摄入** —— 扔资料，Claude 读完、提取、归档。不用手动建页面
2.  2.  **知识图谱** —— 按图谱组织，而不是按文件夹堆。连接密度随时间增加
3.  3.  **自然成长** —— 每次摄入，已有的笔记被重新交叉引用。你在长大，它在长大
4.  4.  **跨项目复用** —— 把任何 Claude Code 项目指向这个知识库，不同项目可以共享同一个知识基底
5.  5.  **不锁定** —— 所有文件都是纯 Markdown，随时拿走，随时导出

Karpathy 说的"compounding knowledge is the highest-leverage habit a thinking person can build"——这个工具让"compounding"这件事变成自动的。

---

---

内容效果不满意？[点此反馈](https://feedback.notebooksyncer.com/feedback/c2dffb30_1785405220254?u=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzYzNDI1MTg0Nw%3D%3D%26mid%3D2247484120%26idx%3D1%26sn%3D59132d978f5a7400eeb0f9a2311ba3c8%26chksm%3Df198c5e4242b17a93ba186f441d45b8b9a62db54076a607b206bee583104721dd63c17317846%26mpshare%3D1%26scene%3D1%26srcid%3D0730IX5U58VmUCQsFZjr6a8Y%26sharer_shareinfo%3Dcd3f12741c62be2c96743dcdbdcc0775%26sharer_shareinfo_first%3Dcd3f12741c62be2c96743dcdbdcc0775%23rd&s=obsidian)