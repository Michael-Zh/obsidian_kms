---
author: Petrichor
source: 微信公众号
url: https://mp.weixin.qq.com/s/k-PBzpi0WE4BfQxqfLFo6Q
saved: 2026-06-06 20:27:58
tags:
  - 笔记同步助手
annotation: Obsidian+workbuddy
id: 94c5a958-429d-42b7-9e0d-1195c716840d
summary: Explains Karpathy's LLM Wiki paradigm (AI as knowledge compiler rather than retriever) and implements it using Tencent's WorkBuddy desktop app as a Chinese-user-friendly alternative to Claude Code. Covers the raw/wiki/outputs folder structure, CLAUDE.md schema, the automatic ingest-update-lint cycle, and WorkBuddy's advantages including WeChat integration, Chinese-language optimization, and a local-only data model.
---

公众号名称：Ollivanders

作者名称：Petrichor

发布时间：2026-04-07 08:59

每天花2小时整理笔记，不如让AI帮你养一个会自己思考的知识库。

如果你像我一样，在Obsidian里积累了成百上千条笔记，却总觉得它们像是散落在沙滩上的贝壳——每一颗都漂亮，但连不成一条项链。手动建立链接、打标签、写摘要的日子，就像老牛拉车，费力不讨好。

直到我发现了AI大神Andrej Karpathy的方法，还有腾讯的WorkBuddy这个神器。今天就来聊聊，怎么用这两样东西，搭建一个会自动进化的个人知识库。

  

## 一、传统笔记的困境：每次都在重新发现

先说说我们大多数人是怎么做知识管理的。

看到一个好文章，剪藏到Obsidian。读了一本好书，摘录几句。有了新想法，新建一个笔记。然后呢？然后就没有然后了。这些笔记静静地躺在文件夹里，等着你某天灵光一现，想起它们的存在。

更糟糕的是，当你需要某个问题的答案时，你得在几十个、几百个文件里翻找。就算用了双向链接和标签，也常常觉得信息是碎片化的，拼不出完整的图景。

这就是Karpathy说的“传统RAG困境”——每次都在重新发现知识，没有积累效应。

  

## 二、新思路：让AI当你的知识架构师

Karpathy提出的LLM Wiki，核心思想很简单：**让AI当知识编译器，而不是检索器。**

![[01_raw/_inbox/文章/images/98cf73a15b6a49a48b84c1e2065d956a_MD5.jpg]]

什么意思呢？传统方法是，你把资料喂给AI，它帮你找答案。新方法是，你把资料喂给AI，它帮你**构建知识库**。

具体来说，就是三个文件夹加一份说明书：

你的知识库`/├── raw/ # 原始材料：论文、文章、笔记，原封不动放进来├── wiki/ # AI编译层：AI读了raw的内容，整理成的结构化文章├── outputs/ # 衍生输出：AI生成的报告、图表、问答归档└── CLAUDE.md # 说明书：告诉AI怎么整理，用什么风格，关注什么主题`

AI的工作流程是这样的：

1.你往raw里扔新材料

2.AI读新材料，更新wiki里的相关文章，建立新的链接

3.你问问题，AI在wiki里找答案，答案会存回outputs

4.AI定期检查wiki，发现矛盾就修正，发现缺失就补充

这样一来，知识库就活了。它不再是被动的存储仓库，而是主动的知识伙伴。

  

## 三、WorkBuddy：中文用户的桌面AI助手

Karpathy用的是Claude Code，对中文用户来说有个问题：它更适应命令行，而我们更习惯桌面操作。

这时候WorkBuddy就派上用场了。

WorkBuddy是腾讯出的桌面AI助手，你可以把它理解成“会说中文的Claude Code加强版”。它的几个优势特别适合我们：

## 1.桌面直控：不用敲命令行，直接告诉它“整理桌面上的文件”、“把这篇公众号文章转成Markdown”

## 2.微信集成：绑定微信后，在外面用手机就能遥控家里的电脑整理知识库

## 3.中文优化：对中文理解和中文办公场景做了专门优化

## 4.技能市场：有2万多个现成技能包，不用写代码就能扩展功能

最重要的是，WorkBuddy的数据全程在本地运行。你的私人笔记、研究资料，不用担心泄露到云端。

  

## 四、手把手搭建指南

说了这么多理念，具体怎么做呢？我总结出下面这个七步法。

### 第一步：准备工具（30分钟）

1.下载安装WorkBuddy

2.如果你还没有Obsidian，也一起装上

3.WorkBuddy新用户有5000免费积分，够用很久了

### 第二步：创建目录结构（5分钟）

在你的Obsidian库里新建一个文件夹，就叫`knowledge-base`。然后在里面创建：

`1.raw/（放原始材料）`

`2.wiki/（AI整理后的知识）`

`3.outputs/（输出和归档）`

```
4.CLAUDE.md（给AI的说明书）
```

### 第三步：写说明书（15分钟）

`CLAUDE.md`是整套系统的灵魂。你要在这里告诉AI：

\# 我的知识库操作指南`## 我是谁## 知识库用途## 写作风格## 目录规范- raw/：只读，你从这里读材料- wiki/：可写，你把整理好的知识放这里- outputs/：可写，问答和报告放这里`

### 第四步：迁移现有笔记（分批进行）

不要一次性把所有笔记都扔进raw。建议：

## 1.先选一个你最熟悉的主题

## 2.把这个主题下的所有笔记移到raw/

## 3.让AI从零开始整理这个主题

给WorkBuddy下指令：“请读取raw/下的所有文件，为它们创建wiki页面，建立相互链接。”

### 第五步：建立自动化流程（10分钟）

在WorkBuddy里设置两个定时任务：

## 1.每日整理：每天早上8点，检查raw/有没有新材料，有就整理

## 2.每周检查：每周日晚，全面检查知识库，修复链接，补充信息

设置方法很简单，在WorkBuddy里说：“创建一个每天8点运行的自动化任务，任务内容是整理知识库的新材料。”

### 第六步：日常使用习惯（养成中）

新的工作流是这样的：

## 1.收集：看到好文章，用Obsidian Web Clipper剪到raw/articles/

## 2.微信同步：微信里的好内容，用笔记同步助手转到raw/wechat/

## 3.整理：每天早上的自动化任务会处理新材料

## 4.查询：在WorkBuddy里问：“知识库里关于WorkBuddy的内容有哪些？”

## 5.创作：写公众号时，让AI从知识库生成素材框架

### 第七步：定期优化（每月一次）

每月花一小时，做三件事：

## 1.让AI全面检查知识库，找矛盾、补缺失

## 2.清理raw/里已经处理完的旧材料

## 3.调整CLAUDE.md，优化AI的整理效果

  

## 五、三个月后你将得到

**第一，知识真的在沉淀。** 以前问“Obsidian有哪些高级用法”，你得回忆、搜索、整理。现在直接问知识库，它会给出一个结构化的答案，而且这个答案会越来越好——因为每次问答都会丰富知识库。

**第二，创作变得轻松。** 写公众号时，你说“帮我从知识库整理一篇WorkBuddy入门指南的框架”，AI能给出一个包含历史、功能、案例、心得的完整大纲。你只需要填充血肉，调整语气。

**第三，学习效率提升。** 读一本新书时，可以边读边把要点扔进raw。读完后，知识库已经有了这本书的摘要、核心观点、与你已有知识的关联。不是你在整理笔记，是AI在帮你构建知识网络。

  

## 六、几个实用小技巧

**1.从一个小主题开始：不要贪多，先做好一个主题（比如“AI工具”），再扩展**

**2.善用微信同步：绑定微信后，路上看到的好内容直接转发给WorkBuddy机器人**

**3.定期备份：虽然数据在本地，还是建议每周备份一次到网盘**

**4.保持CLAUDE.md的更新：你的关注点变了，AI的整理方向也要变**

**5.接受不完美：AI整理的可能不完美，先让它做，你再微调  
**

## 七、你可以这样开始

如果看完你想试试，我建议这样的起步顺序：

**本周**：装好WorkBuddy和Obsidian，创建目录结构，写好CLAUDE.md

**下周**：迁移一个主题的旧笔记，设置每日自动化

**下个月**：养成新的信息收集习惯，体验AI整理的便利

**三个月后**：你的知识库初具规模，开始反哺你的创作和学习

  

## ONE MORE THING

如果你连目录结构也不想写，甚至可以直接向workbuddy提问：

![[01_raw/_inbox/文章/images/e3f062685b9a4d60dccc7dddcf1ed6a1_MD5.jpg]]

然后，一切交给workbuddy吧！

![[01_raw/_inbox/文章/images/ebb03cc0c228ab748eb42da2bc8adb64_MD5.jpg]]

测试一下：

![[01_raw/_inbox/文章/images/77bac1e8cdd7101d04f25bf41cde9b64_MD5.jpg]]

![[01_raw/_inbox/文章/images/695c7d3d4e3035e4d423a88bd8ffe173_MD5.jpg]]

![[01_raw/_inbox/文章/images/189b54b6fc29c6d439b9195c29c35831_MD5.jpg]]

wiki页面也同步更新了，全程无需干预：

![[01_raw/_inbox/文章/images/8edd032ace0e654872c0e97ac22f349e_MD5.jpg]]

  

## 一点感悟

技术应该服务于人，而不是人为技术服务。Karpathy的方法加上WorkBuddy，最打动我的不是技术多先进，而是它真的降低了知识管理的门槛。

你不用懂向量数据库，不用写复杂的提示词，甚至不用记住那些快捷键。你只需要告诉AI：“帮我把这个弄明白”、“帮我把这些整理好”。

知识管理终于从“老牛拉车”变成了“老板指挥”。你把原材料准备好，把大方向定好，剩下的交给AI。

这大概就是AI时代，我们应有的工作方式——不是被工具奴役，而是让工具为我们服务。

  

---

  

---

内容效果不满意？[点此反馈](https://feedback.notebooksyncer.com/feedback/b4ce9f91_1780770474990?u=https%3A%2F%2Fmp.weixin.qq.com%2Fs%2Fk-PBzpi0WE4BfQxqfLFo6Q&s=obsidian)