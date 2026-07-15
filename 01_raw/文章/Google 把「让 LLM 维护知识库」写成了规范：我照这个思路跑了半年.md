---
author: 橙研所
source: 微信公众号
url: https://mp.weixin.qq.com/s?__biz=MzA4MTU0Nzc2MQ==&mid=2453073394&idx=1&sn=b9bf21521e0bc28f451d2edfee6ec419&chksm=89c13a7657dca3afd645b11b5ca5f71f9649fef804b8c5c91d70c5a898b3b3358260b667a59a&mpshare=1&scene=1&srcid=0622Kv00O4D8dI8GjqjMHKSh&sharer_shareinfo=19de0bfc02f6ed3051f9e91d240b898d&sharer_shareinfo_first=19de0bfc02f6ed3051f9e91d240b898d#rd
saved: 2026-06-22 04:29:46
tags:
  - 笔记同步助手
annotation: Google OKF for structural knowledge for AI
id: 5506fdf8-9d52-4cdf-a290-1e6905876f43
---

公众号名称：橙研所

作者名称：

发布时间：2026-06-15 10:31

![[01_raw/_inbox/文章/images/fc386662572795a27fa0fc29c2db860b_MD5.png]]

个人知识库几乎都会荒废。不管是 Obsidian、Notion 还是一个塞满 markdown 的文件夹，开头都很有热情，几个月后大多沦为坟场。原因不是它没价值，而是维护成本：每记一条，你得想它该归到哪类、要不要更新某处的交叉引用、回头还得修一下索引。这套「记账」工作量，才是人放弃的真正根因。

Karpathy 去年那条 gist 把这件事点破了：LLM 不会厌倦记账，不会忘记更新交叉引用，一次能改 15 个文件。让人类放弃个人 wiki 的那些琐碎簿记，恰恰是 LLM 最擅长的。换句话说，知识库荒废这个老问题，可能不需要更自律的人，只需要一个不嫌烦的维护者。

2026 年 6 月，Google Cloud 把这个观察形式化成了一份规范：OKF（Open Knowledge Format）v0.1。它不是一个产品，也不是一个平台，而是一份「知识该怎么存，才能让人和 agent 都直接读」的开放约定。值得注意的是，OKF 在介绍它要标准化的「既有实践」时，点名了三样东西：连着 coding agent 的 Obsidian vault、`CLAUDE.md` / `AGENTS.md` 这类约定文件、带 `index.md` 和 `log.md` 的仓库。

这三样我都在跑，而且跑了半年。所以这篇不谈「OKF 是什么新东西」——它恰恰不是新东西，它标准化的是一群人已经各自在做的事。我想做的是反过来：用 OKF 这把刚出炉的官方尺子，量一量我那套自建的 LLM-as-wiki-agent——结构上和规范有多契合、哪些跑通了、哪些还差一截。

## 01真正难的不是模型，是「上下文在哪、怎么凑齐」

context assembly problem——个人和组织是同一个问题

给 agent 喂上下文，卡点很少在模型本身，而在「有用的知识到底散在哪、怎么把它凑齐」。OKF 原文把组织里这种碎片化列了一张清单：一张表的 schema、某个指标在你们业务里的真实含义、一次事故的 runbook、两个系统之间的 join 路径、一个旧 API 的弃用通知——这些知识原子，散落在元数据目录（各有各的 API）、wiki 和网盘、代码注释与 docstring，以及资深工程师的脑子里。

后果是双重浪费：每个做 agent 的人都要从零再解一遍同样的「上下文拼装」问题，每个目录厂商都在重新发明同一套数据模型；而知识被锁死在它的创建系统里，没法跨产品、跨组织迁移。OKF 把这个叫 context-assembly problem——agent 真正干活之前，得先把散落各处的相关信息凑齐，这一步今天人人都在重复造轮子。

个人层面是同一个问题的缩小版。我的知识散在三处：自动记忆文件、与 Claude 的历史对话、随手写的临时 md。想回答「我之前研究过 X 吗」，得人肉翻。荒废的根因从来不是「没记」，而是「记完之后的维护记账」压垮了人——而这恰好是 LLM 的强项。所以解法的方向很清楚：把记账这件苦差，交给那个不嫌烦的维护者。

![[01_raw/_inbox/文章/images/c2789b53578c644a5e14570268a1febd_MD5.png]]

图 1 · 有用的知识散在五处，agent 用之前得先凑齐——这就是 context-assembly problem

## 02OKF：一份「最少意见」的知识格式规范

三个设计原则 + 一个 bundle 长什么样

OKF 的核心定义很朴素：把知识表示成一个目录的 markdown 文件，每个文件就是一个 concept，文件之间用标准 markdown 链接互连成一张图；再加一点 YAML frontmatter，存那些需要被查询的少量结构化字段。用它自己的话说——「就是 markdown」（任何编辑器可读、GitHub 可渲染、任何搜索能索引）、「就是文件」（能打成 tarball、能放任何 git 仓库、能挂任何文件系统）、「就是一点 YAML frontmatter」。不需要压缩方案，不需要新运行时，不需要 SDK。

sales/ ├── index.md ├── tables/ │   ├── orders.md          # 一个文件 = 一个 concept│   └── customers.md └── metrics/     └── weekly\_active\_users.md# orders.md 的开头：--- type: BigQuery Table        # 唯一强制字段title: Orders description: 每行一笔已完成订单 tags: \[sales, revenue\] --- # Schema customer\_id → 链到 \[customers\](/tables/customers.md)

它的克制体现在三条设计原则上，逐条看：

**一、最少意见（Minimally Opinionated）。**OKF 对每个 concept 只强制一件事：一个 `type` 字段。其余全部留给生产者自己定——有哪些 type、还加什么字段、正文分几节，规范一概不管。它定义的是「互操作面」，不是「内容模型」。这一条是整个规范的骨气所在：它只约定大家怎么对接，不规定你脑子里该装什么。

**二、生产者/消费者解耦。**谁写知识，和谁消费知识，被干净地分开。一个人手写的 bundle，可以被 agent 消费；一个由元数据导出管线生成的 bundle，可以被可视化工具浏览；一个由某个 LLM 合成的 bundle，可以被另一个 LLM 查询。写和读不必是同一方、同一时刻、同一工具。

**三、格式而非平台（Format, Not Platform）。**它不绑任何云、数据库、模型厂或 agent 框架，永远不需要专有账号或 SDK 才能读写。这是它和「又一个知识管理 SaaS」的本质区别——它赌的是格式本身成为通用语，而不是把你锁进某个产品。

一个 bundle 长什么样？一个装着 concept 文件的目录，加上可选的 `index.md`（层级导航）和 `log.md`（变更历史）。Google 还附了三件参考实现：一个富化 agent（遍历 BigQuery 数据集，为每张表自动起草 OKF concept，再用第二轮 LLM 爬权威文档补引用和 join 路径）、一个纯静态 HTML 可视化工具（把任意 bundle 转成交互图，无后端、免安装、数据不出页面）、以及三个示例 bundle（GA4 电商 / Stack Overflow / Bitcoin，全是 BigQuery 公开数据集）。

## 03为什么是 Google Cloud 发它：一个「商品化互补品」的打法

从产品视角看，OKF 不是孤立开源项目，是数据平台的上游标准层

读到这里容易把 OKF 当成一个中立的开源理想主义项目。但从产品视角看清它，得先认准发布方的真身——这不是「Google」，是 **Google Cloud 的 data analytics 团队**。三条证据钉死归属：博客挂在 `cloud.google.com/blog/products/data-analytics/` 下；OKF 直接绑定 Google Cloud Knowledge Catalog（Catalog 已更新支持 OKF ingestion）；参考实现遍历的是 BigQuery 数据集，三个示例 bundle 全是 BigQuery 公开数据集。所以 OKF 是 Google Cloud 数据平台的「上游标准层」，不是飘在空中的开源善意。

认清这一点，动机就清楚了，而且是几条算盘并行：

**一、把互补品做成免费标准（commoditize your complement）。**Google Cloud 真正卖钱的是 BigQuery 的存储算力、Vertex 上跑的 agent。「知识格式」是这些核心商品的互补品——互补品越标准、越免费、越通用，核心商品需求越大。把知识格式开源，降低企业上 agent 的门槛，结果是更多数据进 BigQuery、更多 agent 跑 Vertex。OKF 自己不赚钱，它让底下的云服务更好卖。

**二、抢一个还没人占的标准空位。**看 agent 生态的协议分层：MCP（Anthropic）卡的是「模型↔工具/数据」的运行时拉取；A2A 卡的是「agent↔agent」的通信；而 OKF 卡的是第三层——静态知识怎么存储，一个之前没人正经占的空位。谁定义了知识怎么存，谁就在 agent 知识供应链最上游有话语权。这也是防御性的：Anthropic 已经靠 MCP 拿了「连接层」心智，Google 不想在「知识层」再被对手定义一次。

**三、给自家 Catalog 解冷启动。**Knowledge Catalog 要有用，得先有海量结构化知识喂进去，手工录入没人干。OKF 加那个富化 agent，让「从 BigQuery 自动生成知识」零成本——等于把自家产品的进料口标准化了。

![[01_raw/_inbox/文章/images/aa5af79aaff5c1a8e2ec2ec142b57145_MD5.png]]

图 2 · OKF 卡的是 MCP/A2A 之外的「知识存储层」；format 开源、infra 收钱的双层结构

这背后是一个清晰的产品哲学：**开放 format，专有 infra**。开源一个 format 几乎没有采纳阻力、容易成事实标准；但 Google 真正的护城河不在 format，在 format 之上的消费基础设施（Catalog 检索、BigQuery 算力、Vertex agent）。Format 免费送，infra 收钱——这和 Android 之于 GMS、Kubernetes 之于 GKE 是同一套结构：把地基开源做大蛋糕，把最赚钱的那层攥在手里。「vendor-neutral」既是真诚（格式确实开放），也是话术（用中立降低对手与客户的戒心、提高采纳率）。

能不能成，不取决于规范多优雅，取决于生态采纳——盯一个指标：有没有非 Google 阵营开始写 OKF producer。

三个变数要盯：目前只有 Google 一家 producer/consumer，要成通用语得有别家也来写 producer；OKF 与 MCP 的边界要讲清（静态存储格式 vs 运行时拉取），讲不清会被 MCP 心智吃掉；以及「中立」的可信度——参考实现全指向 BigQuery，社区一定会问它是否真中立。

## 04我的 LLM-as-wiki-agent：从 schema 到自动升格

v0.1 → v0.4，每版解决上一版暴露的问题

我这套东西的载体是一个 Obsidian vault：根目录一个 `CLAUDE.md` 定义全部规则，`wiki/` 目录由 LLM 全权维护。它不是一次设计出来的，是踩着问题长出来的。

### v0.1立 schema

最初的问题是：让 LLM 帮我建知识页，每次的风格、分类、字段都不一样，攒不成体系。做法是把规则当「宪法」写死进 `CLAUDE.md`——目录结构（`raw/` 只读原料、`wiki/` LLM 维护、`daily/` 流水）、页面 frontmatter 规范（`title / type / tags / created / updated / sources / related / summary`）、以及 type 四分类：entity（命名实体）、concept（可复用知识）、source（原始素材摘要）、synthesis（结合具体场景的分析）。每次操作前先读这部宪法。效果是页面结构稳定了；局限是全靠 LLM 自觉遵守，没有强制校验。

### v0.2定 ingest 流程

schema 解决了「单页长什么样」，但没解决「新知识怎么接进已有的图」。于是把摄入固化成 8 步：阅读原料 → 与我对齐 2-3 个关注点 → 建 source 摘要卡 → 更新相关 entity/concept 页 → 评估并更新 overview（强制，不得跳过）→ 更新 index → 追加 log。关键不是「存下来」，而是每次摄入都强制把新知识交叉链接进已有结构。效果是单次摄入产出 3-5 个互链页面；局限是这套流程要人在场才跑得动，成本不低。

### v0.3双料流 + 自动升格

v0.2 的人工流程跟不上日增的对话和 feed 流水。于是分成两条料流：料流 A 是手动 ingest（人在场，走全 8 步，溯源严谨）；料流 B 是自动升格（launchd 定时任务，用更便宜的 haiku，无人值守，省掉「对齐视角」和「建 source 卡」两步，直接把 daily 流水里的洞见升格进相关 concept/synthesis 正文）。具体做法是一个 wiki-autoupdate 的 launchd，每 6 小时跑一次，把记忆、聊天、信息流摘要升格成 wiki 页面。效果是历史 55 页一次性 backfill 完成，日常增量自动跑，切到 Claude Max 订阅后这条链路零成本；局限也如实写在规范里——自动料流的溯源严谨度低于手动，因为没有 source 卡硬钉出处。

### v0.4双向链接 + lint

图的价值在连接密度。所以正文里积极用 `[[页面名]]` 交叉引用，目标页不存在就先建一个空壳页再链。再加一个 lint：定期扫矛盾（同一事实不同页冲突）、孤儿页（无入链）、过时点、被反复引用却还没建的缺失页。效果是整个 vault 可以语义触发「检索 / 查询 / lint」三种操作；局限是 lint 目前还是手动触发，没接进自动闭环。

![[01_raw/_inbox/文章/images/97ff4cafa644e4f5c3785de06b9a360b_MD5.png]]

图 3 · 一套 schema、两条进料流、一个 LLM 全权维护的自动升格闭环

## 05拿 OKF 当尺子量一遍：契合、约束、差距

七个维度逐条对照，差距如实写

把我的实现和 OKF 规范并排，逐维度看，会发现契合得相当深，但也有两处真实差距。

![[01_raw/_inbox/文章/images/1596bf809dab942946acd9e4a64bbff6_MD5.png]]

图 4 · 我的实现 × OKF 规范 · 七维对照（绿=契合，橙=约束，红=差距）

契合的几处不意外：存储形式（md 目录 + frontmatter）完全一致，这正是我半年前就在跑的形态；导航与历史我有 index、log、overview 三件，甚至比 OKF 的可选项更全。约束类的两处是程度问题：我的 frontmatter 必带五个字段，比 OKF「只强制一个 type」重得多——信息更全，但这套字段是我的私有约定，不是 OKF 的互操作面；互链用的 `[[wikilink]]` 是 Obsidian 方言，语义和标准 markdown 链接一致，但语法要改。

真正的差距有两处，得说清楚。一是**生产者/消费者没有解耦**：我跑的是同一个 LLM 既写又读的闭环，不是一个能被任意第三方消费的标准格式。二是**可移植性**：整套东西绑死在 Obsidian 加我自己那部 CLAUDE.md 约定上，一旦离开我的环境就散了——这恰恰是 OKF 的核心卖点。反过来，我也有规范之外的东西：那条 launchd 每 6 小时自动升格的闭环，OKF 完全不管（它只定格式，不管维护）。

我跑通的是「自动维护的闭环」，OKF 标准化的是「可移植的格式」——两件不同的事，但 OKF 给了我一个把私有约定升级成标准的迁移目标。

## 06别等标准，先把记账交出去

OKF 的真正贡献不是发明了什么，而是把一群人各自在跑的私有实践，收敛成一个最小可互操作的约定。它赌的是「格式即护城河」——谁的格式成了通用语，谁就定义了知识在 agent 之间怎么流动。这个赌注能不能赢还不好说，但方向是对的：当越来越多工作交给 agent，知识的「可交换格式」会和当年的 HTML、JSON 一样重要。

对已经在跑私有 wiki-agent 的人，OKF 的价值是给了一个迁移目标。对我具体而言，就是把 `[[wikilink]]` 收敛成标准 markdown 链接、把 frontmatter 对齐到 OKF 的字段约定——做完这两步，我的 vault 就从「只有我能用」变成「任何 OKF 消费者能读」。这不是推倒重来，是给一套已经跑通的东西换一身能出门的衣服。

对还没开始的人，我的建议很直接：别等标准齐全再动手。Karpathy 那句话是真的——记账负担交给 LLM。先用最糙的版本跑起来：一个 `CLAUDE.md` 定规则、让 LLM 维护一堆 md、再加一个定时任务把流水自动升格成知识页。跑上一个月，你会比读十篇规范更懂自己需要什么。我这套东西从 v0.1 到现在，全是被真实问题逼出来的，没有一版是设计出来的。

我自己的下一步，是写一个 producer，把 vault 导出成 OKF bundle，喂给官方那个静态可视化工具看看效果。跑通了，再写一篇造物日志。

  

---

内容效果不满意？[点此反馈](https://feedback.notebooksyncer.com/feedback/7bbdf0b6_1782095384718?u=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzA4MTU0Nzc2MQ%3D%3D%26mid%3D2453073394%26idx%3D1%26sn%3Db9bf21521e0bc28f451d2edfee6ec419%26chksm%3D89c13a7657dca3afd645b11b5ca5f71f9649fef804b8c5c91d70c5a898b3b3358260b667a59a%26mpshare%3D1%26scene%3D1%26srcid%3D0622Kv00O4D8dI8GjqjMHKSh%26sharer_shareinfo%3D19de0bfc02f6ed3051f9e91d240b898d%26sharer_shareinfo_first%3D19de0bfc02f6ed3051f9e91d240b898d%23rd&s=obsidian)