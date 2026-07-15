---
author: K博
source: AI整理 - 小红书
url: https://www.xiaohongshu.com/discovery/item/6a36acb8000000001603d65d?app_platform=ios&app_version=9.34.4&share_from_user_hidden=true&xsec_source=app_share&type=normal&xsec_token=CB_CiCLnumKw77qMpw66REY4g3KoJ05IZpkWDguM38XUE=&author_share=1&xhsshare=WeixinSession&shareRedId=Nzs4RERHO0tLPD1GOjswPEg5Qk06PjpN&apptime=1782096333&share_id=041e021d0e654fdc9c1fc571ba0f1cbb&code=7KdtOPUxg7U
saved: 2026-06-22 04:48:59
tags:
  - 笔记同步助手
annotation: Google OKF for structural knowledge for AI
id: 80d8112d-ac93-4d0e-9c36-aa5a028a9272
---

# 给LLM喂知识的标准格式，谷歌OKF来了

## Google 悄悄发了个东西，可能统一 AI 读懂世界的方式

6 月 12 号，Google Cloud 博客上发了一篇文章，没有发布会，没有铺天盖地的宣传。

介绍了一个叫 OKF 的东西。

全称 Open Knowledge Format，开放知识格式。

我读完之后的第一反应就是，这东西是对的，是一个实用的知识框架。

再仔细看看规范本身，就是一堆 Markdown 文件放在文件夹里，你可能会觉得，简单得有点出乎意料。

但，这个「简单」恰好就是它对的地方。

### OKF 到底是什么

OKF 就是一种把知识整理成 AI 能直接读懂的格式的规范。

它的核心其实三句话就能讲完。

#### 1\. 一个文件夹就是一个知识库

这个文件夹叫 Knowledge Bundle（知识包），里面放着一堆 `.md` 文件。

每个文件代表一个「概念」，可以是一张数据库表、一个业务指标、一份运维手册、一个 API 接口，什么都行。

#### 2\. 每个文件顶上有一小段标签信息

用 YAML 格式写几个字段，这东西是什么类型（type）、叫什么名字（title）、一句话简介（description）、原始资源在哪（resource）。

其中只有 type 是必填的，其他都随意。

#### 3\. 文件之间用普通的 Markdown 链接互相指向

就这么形成了一张知识图谱。

没有新的编程语言。不需要安装任何 SDK。不需要注册任何账号。

你用记事本就能写，GitHub 上能直接看，文件系统里能直接浏览。

这个想法也不是 Google 凭空冒出来的。

2026 年 4 月，前特斯拉 AI 总监 Andrej Karpathy 在 GitHub 上发了一篇叫 LLM Wiki 的 Gist，核心观点挺有意思：

人类维护 Wiki 总是失败的，写了几天就懒得更新了，交叉引用越来越乱，最后变成一堆过时的文档。但 LLM 天生适合干这个活，它不会无聊，不会忘记更新交叉引用，一次能改 15 个文件。

Karpathy 的设想是，人类负责策展和审核，LLM 负责记账式的维护工作，知识库变成一个「人机共写」的活文档。

Google 做的事情，就是把这个设想从一个个人想法变成了一个正式的、有巨头背书的开放标准。

Google 在官方博客里直接引用了 Karpathy 的原话，这在 Google Cloud 的发布中很少见，说明他们认可这条思路，而且愿意在产品层面推动它。

### 具体长什么样

假设你是一家公司的数据团队，有个「销售」相关的知识库。

用 OKF 组织起来长这样：

```
sales/
├── index.md                 # 目录索引，这个文件夹里有什么
├── datasets/
│   └── orders_db.md          # 描述「订单数据集」的文件
├── tables/
│   ├── orders.md             # 描述「订单表」的文件
│   └── customers.md          # 描述「客户表」的文件
└── metrics/
    └── weekly_active_users.md # 描述「周活跃用户」这个指标
```

其中 `orders.md` 这个文件打开来长这样：

```
---
type: BigQuery Table
title: 订单表
description: 每一行代表一笔已完成的客户订单
tags: [销售, 订单, 收入]
---

# 字段说明

| 字段名 | 类型 | 含义 |
|---|---|---|
| order_id | STRING | 订单唯一标识 |
| customer_id | STRING | 客户 ID，关联[客户表](/tables/customers.md) |
| total_usd | NUMERIC | 订单金额（美元） |

# 关联关系

通过 customer_id 与[客户表](/tables/customers.md)进行关联查询。
```

注意那些方括号里的链接。

`[客户表](/tables/customers.md)` 就是一个普通的 Markdown 链接，但它把两个概念连接起来了。

AI Agent 读到这个文件的时候，它不仅知道「订单表有哪些字段」，还知道「订单表和客户表之间怎么关联」。

这层关系信息，是很多知识管理方式里容易丢掉的东西。

### 针对的是什么问题

#### 一个真实场景

假设你是一家电商公司的数据分析师。

老板问你：「我们上周的周活跃用户是多少？」

你觉得这是个简单问题。但真动手去查，你发现事情没那么顺利。

「周活跃用户」这个指标的计算公式，写在一个内部 Wiki 的某个角落。数据存在公司数据仓库的某张表里，但字段名和 Wiki 上写的对不上。两张表之间怎么做关联查询，只有团队里那个干了六年的老工程师记得。

他上个月刚离职了。

这就是绝大多数公司的现实。知识散落在 Wiki、代码注释、共享文档，甚至某个人的脑子里。

格式不统一，系统不互通，谁走了一部分知识就跟着消失了。

现在把这个场景里的「你」换成一个 AI Agent，它面临的困境是一样的，甚至更糟。

人好歹还能走过去问同事，AI Agent 连这个选项都没有。

OKF 就是冲着这类问题来的。

### 知识碎片化

企业内部的知识散落在十几个系统里，每个系统有自己的格式和接口。

每个想做 AI Agent 的团队，都在从零开始解决同一个问题：怎么把这些碎片拼起来喂给模型。

OKF 的思路很直接，与其让每个 Agent 都去适配十几种格式，不如大家把知识都导出成同一种格式。

这就像 PDF 对文档做的事情。不管你用 Word、Pages 还是 WPS 写的，导出成 PDF 谁都能读。

OKF 想做的是 AI 时代的知识 PDF。

### 人人都在造 Wiki，但没有标准

过去一年，AI 圈里涌现了一大堆「用 Markdown 给 AI 建知识库」的做法。

Karpathy 写了 LLM Wiki 的 Gist，Obsidian 玩家把笔记库接进 AI，开发者在项目里放 `CLAUDE.md` 或 `AGENTS.md`。

这些做法在形态上几乎一样，都是 Markdown + 元数据头 + 交叉链接。

但每个团队的实现都是自己定的规矩。你的 Wiki 和我的 Wiki 长得差不多，互相就是读不懂。因为没有人规定过「文件头必须有哪几个字段」、「index.md 应该长什么样」、「链接应该怎么写」。

OKF 做的就是把这些最小公约数定下来，不多管闲事，只管互操作必需的那几条规则。

### 给 Agentic RAG 一个干净的知识源头

现在主流的 Agentic RAG 已经进化到以文件为单位做管线了，AI Agent 能直接读文档、遍历目录、按需检索。能力没问题，问题出在它读到的那些文件本身。

大多数企业的内部文档是什么样的？

PDF、Word、Confluence 页面、Notion 数据库、代码注释，格式五花八门。

Agent 得为每种格式写一套解析逻辑，而且这些文档之间的关系往往没有显式标注，全靠 Agent 自己推断。

OKF 解决的是管线上游的问题，给 Agent 一个干净的、结构统一的知识源头。

每个概念是一个完整文件，概念之间的关系通过 Markdown 链接显式标注。

Agent 不用再猜「这两个东西有没有关系」，链接就摆在那里。

打个比方，Agentic RAG 是一个很能干的图书管理员，什么书都能找。

OKF 做的是把图书馆的书按统一规格编目、标好交叉引用。

管理员再能干，面对一个编目清晰的图书馆和一个书堆在地上的仓库，效率也是天差地别。

### OKF 和你已经知道的那些东西有什么区别

看到这里你可能会想，「让 AI 更好地理解内容」这件事，之前不是已经有好几种方案在做了吗？

`sitemap`、`llms.txt`、结构化数据，这些名字你多少听过。它们和 OKF 到底是什么关系？

`sitemap.xml` 是给搜索引擎爬虫看的页面目录，「我有这些页面，请来爬。」

`llms.txt` 是给 AI 模型看的精选入口，一个单文件，放在网站根目录，「如果你想了解我，先读这几篇」。相当于一张名片。

`Schema.org` 结构化数据是嵌在 HTML 里的语义标注，告诉搜索引擎「这段文字是价格」「那段文字是人名」。

`CLAUDE.md` 和 `AGENTS.md` 是开发者放在代码仓库里的 AI 行为指令文件，告诉 AI「在这个项目里你应该怎么干活」。

OKF 是一套完整的知识交付格式。把知识本身整理好、编好索引、标注好关系，打包成 AI 可以直接消费的知识库。

简单打个比方吧。

`llms.txt` 是「这里有家餐厅，推荐你看看菜单」。

OKF 是「这是整本菜单，每道菜的原料、做法、搭配推荐都写好了，菜和菜之间的关系也标清楚了」。

它们之间的关系是叠加的。

`llms.txt` 可以指向你的 OKF 知识库，配合用效果最好。

### 谁应该关注这个东西

#### 如果你是做 AI 产品的开发者，OKF 可能会成为你组织内部知识的标准格式

与其每次接新项目都重新写知识整理脚本，不如一次导出成 OKF，所有 Agent 都能直接读。

#### 如果你是内容创作者或知识博主，这是一个让你的内容被 AI 更理解的机会

把你的内容库整理成 OKF 格式，相当于在 AI 时代给你的知识加了一层「机器可读」的索引。

用 Obsidian 做笔记的同学尤其值得关注。

Obsidian 的笔记库天然就是 Markdown + YAML 元数据 + 双向链接，和 OKF 几乎一个模子刻出来的。

只需要简单的格式转换，你的 Obsidian 笔记库就能变成一个合格的 OKF 知识包。

#### 如果你是企业的技术决策者，OKF 提供了一条低成本的知识管理升级路径

不需要买新平台，不需要重构现有系统，只需要把现有知识导出成一种标准格式。而且这个格式是开源的、厂商中立的，不会被锁定在任何一家供应商身上。

### 社区的看法

OKF 发布一周内 GitHub 拿到了 4,400+ Stars，Google Cloud 的推特公告 117,000+ 浏览、1,800+ 点赞。

社区里有人第二天就做出了支持 SQLite、MySQL、PostgreSQL 等 6 种数据源的连接器工具包。

但质疑也同样真实。

有人说，「这就是把 Markdown 放进文件夹，有什么了不起？」技术上确实简单。

但标准的价值从来都不在技术复杂度上，而在于大家约定俗成按同一套规矩来。

USB 接口技术上也不复杂，但它统一了充电和数据传输的方式。

有人说，「v0.1 太初期了，能不能成还不好说。」确实如此。

目前只有 BigQuery 有官方参考实现，其他数据源靠社区补。

跨知识包的引用机制还没定义，权限控制也完全不在规范范围内。

还有人担心 Google 主导的标准会不会变成 Google 的私有标准。

这个担忧有道理，不过 OKF 发布在 Apache 2.0 许可证下，规范本身刻意做到了厂商中立。

最终能不能成为真正的社区标准，取决于 Google 之外的主要 AI 框架是否跟进。

### 我的判断

OKF 今天的状态，有点像十年前的 Schema.org 结构化数据。

刚发布那会儿绝大多数人不关心，觉得「这跟我有什么关系」。

十年后回头看，早期就在网站里嵌入结构化数据的人，在搜索引擎里积累了巨大的结构性优势。

OKF 吸引我的地方在于它的不对称性。

做的成本极低，几个 Markdown 文件、一点 YAML 元数据、一个文件夹，不需要花钱买工具，不需要改现有系统，不需要学新技术。

但如果 AI Agent 真的开始把 OKF 当作标准知识输入格式来消费，早期把知识整理好的人就多了一层被 AI 优先理解和引用的可能。

投入几乎为零，收益的想象空间不小。

这种做了不亏的事情，我觉得值得早点了解。

![[01_raw/_inbox/文章/images/73e306bcd0d0a044b104948f4a2e976a_MD5.jpg|Image]]![[01_raw/_inbox/文章/images/3f4ad5e241213c4431211c8ee477a3c7_MD5.jpg|Image]]![[01_raw/_inbox/文章/images/93700de82479d14687c9272813dafd0b_MD5.jpg|Image]]![[01_raw/_inbox/文章/images/116b646911982cf6d8284314f053888a_MD5.jpg|Image]]![[01_raw/_inbox/文章/images/edd7daf2412dc0fdef106d7d9c06bef2_MD5.jpg|Image]]![[01_raw/_inbox/文章/images/b11e9ba79cd0c4df868cf1c852b8f3e6_MD5.jpg|Image]]![[01_raw/_inbox/文章/images/4eb13b71104c8bee20e310fedfca40b0_MD5.jpg|Image]]![[01_raw/_inbox/文章/images/a14c43bfc849cdeffc8bb9dcc86d828f_MD5.jpg|Image]]![[01_raw/_inbox/文章/images/1b6a99d7a446c832fc831577aa9403dd_MD5.jpg|Image]]![[01_raw/_inbox/文章/images/42ef7569b77121259cb55627fe7d9440_MD5.jpg|Image]]![[01_raw/_inbox/文章/images/0195e1d06e1323c85ca5871b8f772dc6_MD5.jpg|Image]]![[01_raw/_inbox/文章/images/3a5e126f8503b72e69c3ed4c62904ccc_MD5.jpg|Image]]![[01_raw/_inbox/文章/images/0b0c9a73f32dd065622c233d770fa329_MD5.jpg|Image]]![[01_raw/_inbox/文章/images/e58a483908f97e719d1cfc96ee2ce4ce_MD5.jpg|Image]]

6月12号，Google 悄悄发了个东西叫 OKF（Open Knowledge Format，开放知识格式）  
  
没有发布会，没有大张旗鼓  
  
但我觉得这个东西值得做 AI 的朋友们关注关注  
  
📌 OKF 是什么？  
  
三句话讲完：  
  
\[一R\] 一个文件夹就是一个知识库，里面放 \`.md\` 文件，每个文件代表一个概念  
\[二R\] 每个文件顶上用 YAML 写几个标签：类型、名字、简介、来源  
\[三R\] 文件之间用 Markdown 链接互相指向，自动形成知识图谱  
  
不需要新语言，不需要 SDK，不需要注册账号，记事本就能写  
  
📌 为什么需要它？  
  
现在企业知识散落在 Wiki、文档、代码注释、甚至某个人的脑子里  
  
格式不统一，系统不互通，谁离职了一部分知识就跟着消失  
  
AI Agent 面临的困境还更糟  
  
人好歹还能走过去问同事，Agent 连这个选项都没有  
  
OKF 的思路很直接  
  
与其让每个 Agent 都去适配十几种格式，不如大家把知识导出成同一种格式  
  
就像 PDF 统一了文档阅读，OKF 想做 AI 时代的知识 PDF  
  
📌 潜在影响  
  
这东西有点像十年前的 Schema.org 结构化数据  
  
当时绝大多数人不关心，十年后回头看，早期做了的人在搜索引擎里积累了巨大的结构性优势  
  
OKF 的不对称性在于  
  
做的成本极低，几个 Markdown 文件加一点 YAML，不花钱不改系统  
  
但如果 AI Agent 真的把 OKF 当作标准输入格式  
  
早期整理好知识的人就多了一层被 AI 优先理解和引用的可能  
  
发布一周 GitHub 4400+ Stars，已经有人做出了支持 6 种数据源的连接器  
  
投入几乎为零，收益想象空间不小  
  
做了不亏的事情，值得早点了解  
  
💡 我读完规范后做了一个 OKF 转换工具（Claude Code Skill），丢进去文档、笔记、知识库片段，自动转成符合规范的 OKF 知识包，感兴趣的可以评论区聊  
\#REDSkill \#OKF \#okf \#llmwiki \#智能体 \#LLM \#知识库 \#RAG \#科研 \#谷歌

---

### 评论

-   **A**: 是不是obisidian有类似的操作
    -   **B**: 对的\[笑哭R\]
    -   **B**: okf可以看做，对于现有的一些method进行一个框架性约束
-   **C**: 数据量很大的话，读写md会不会变的很慢？
    -   **B**: 还是要结合检索的\[笑哭R\] 语义检索+关键词检索
    -   **D**: 怎么结合?
-   **E**: 和knowledge skill区别是？
    -   **B**: skill是一种执行流程约束，okf是一种格式规范，可以基于okf的格式规范来做对应的skill
-   **F**: 这是倒退吧
    -   **B**: Agent领域不缺method，但是真的很缺Framework和theory\[捂脸R\]
-   **G**: 东西都给了AI，然后AI代替我？高低得给AI下点儿毒！\[大笑R\]\[大笑R\]

---

内容效果不满意？[点此反馈](https://feedback.notebooksyncer.com/feedback/6876703a-36ba-4a6b-8dc9-c0a7f953c9de?u=https%3A%2F%2Fwww.xiaohongshu.com%2Fdiscovery%2Fitem%2F6a36acb8000000001603d65d%3Fapp_platform%3Dios%26app_version%3D9.34.4%26share_from_user_hidden%3Dtrue%26xsec_source%3Dapp_share%26type%3Dnormal%26xsec_token%3DCB_CiCLnumKw77qMpw66REY4g3KoJ05IZpkWDguM38XUE%3D%26author_share%3D1%26xhsshare%3DWeixinSession%26shareRedId%3DNzs4RERHO0tLPD1GOjswPEg5Qk06PjpN%26apptime%3D1782096333%26share_id%3D041e021d0e654fdc9c1fc571ba0f1cbb%26code%3D7KdtOPUxg7U&s=vtoa)