---
author: 丛林
source: 微信公众号
url: https://mp.weixin.qq.com/s?__biz=MzU2MTI4MjI0MQ==&mid=2247544897&idx=1&sn=ef8eb39cf6a5c553241102c7cca067c4&chksm=fd9413712317db7e556e81aff0a8207cd4b3ac2adaf4235920b704a7c4de00a89817debbba69&mpshare=1&scene=1&srcid=0730AiviOi9Lg1zAZYn96ry2&sharer_shareinfo=2856aad1e895ec5a9ae675ed7a1d34d5&sharer_shareinfo_first=2856aad1e895ec5a9ae675ed7a1d34d5#rd
saved: 2026-07-30 11:05:09
tags:
  - 笔记同步助手
annotation:
id: 8b73d77c-4ffa-484e-92fb-44d8b48775c8
---

公众号名称：极客之家

作者名称：丛林

发布时间：2026-07-25 16:08

我每天都要让AI帮我干一件事，联网找资料，盯GitHub热榜、翻项目文档、看热门信息，基本靠它。

但 Codex 自带的联网功能是真的弱，静态HTML能读，碰到JS渲染的页面直接抓瞎，抓回来一个空壳，它还会一本正经地告诉我这页面没内容。没内容个鬼，我自己浏览器打开明明好好的。后来我把Firecrawl接上，同一个页面，干净的Markdown直接出来了，当时我就觉得这玩意儿值得写一篇。

现在这个开源项目已经15.5万 Star了，进了GitHub全站前100，用的人已经非常多了，相对比较成熟了。

![[01_raw/_inbox/文章/images/3c738a8a28a29832318559fed375bccd_MD5.png]]

# 这个项目是干什么的

Firecrawl是个网页数据API，开源，2024年4月才放出来的，干的事说起来特别简单：**我们丢给它一个网址，它还给我们干净的Markdown、结构化JSON或者截图，没了。**

![[01_raw/_inbox/文章/images/492078da580868eea41100e1c6a20750_MD5.png]]

但这事的价值在于，网页是给人看的，不是给AI看的。导航栏、广告、页脚、弹窗，全塞在HTML里，直接喂给模型，一个普通页面能吃掉几万token，喂进去的还大半是垃圾。Firecrawl只把正文抠出来，官网的说法是输入token能省93%。

用的人数据也摆着：125万开发者，15万家公司接了它的服务，SDK在npm和PyPI加起来每周下载250万次。

# 功能详情

### 抓单个页面 Scrape

最基础的用法，也是我调用频率最高的。给一个URL，返回正文Markdown。JS渲染的页面它自己会渲染完再抠内容，代理、反爬、等待加载这些脏活累活，全不用我们操心。

除了Markdown，还能要原始HTML、页面截图、页面元数据。挂个schema，它直接按字段返回JSON，比如只要标题和价格，别的不要。

还有个我用得挺多的点，网页上挂着的PDF和DOCX它能直接解析。很多白皮书和财报都是PDF挂在官网上的，以前得下载下来再处理，现在省了这步。

### 爬整个网站 Crawl

Scrape管一页，Crawl管一站。给一个起始URL，它顺着链接把整个站点的页面全抓回来。

深度、页面数上限、路径过滤，这些参数都能配。我之前做RAG知识库的时候，导入整个文档站就是一条命令的事。SDK里它自己轮询任务状态，抓完一次性返回，不用我们写循环等结果。

### 列出全站URL Map

抓之前想知道一个站有多大，先跑Map。它不抓内容，只把域名下所有已索引的URL列出来，秒回。

还能带搜索词，我只要一个站点里跟定价相关的页面，给Map加个search参数，结果按相关度排好返回，写竞品监控脚本的时候这个功能省了不少事。

### 网页搜索 Search

不需要URL，直接给关键词，它搜完网页，把每条结果的完整页面内容一起带回来。

老做法是搜一遍再抓一遍，两步走，中间还得自己处理去重。它一步出结果，适合做深度研究类的Agent。

### 自动干活的Agent

连URL都不用给，我们说找一下Notion的定价方案，它自己去搜、去读，返回结果和来源链接。

挂schema能拿结构化输出，模型有两档：spark-1-mini便宜60%，日常够用；spark-1-pro贵一些，适合跨多个站点对比、要钻复杂导航的活。我平时用mini，pro只有在结果明显不对的时候才切。

### 页面交互 Interact

有些数据藏在点击后面，电商的搜索结果、要翻页的列表，普通抓取够不着。

Interact先抓页面，然后我们用人话指挥它：搜一下机械键盘，点第一个结果。它会真的去操作页面再返回，输出里还带一个实时浏览器画面的链接，能看见它确实在点。第一次看到这个live view的时候我还截了图发群里，挺科幻的。

### 接进AI编程工具

这部分是我写这篇文章的真正原因，它有官方MCP服务器，Cursor、Claude Code、Windsurf这些MCP客户端填几行配置就能用，装机量过了40万。

Claude Code和Codex还有现成的Skill，一条命令装好：

```
npx -y firecrawl-cli@latest init --all --browser
```

装完我的 Codex 就有了搜索、抓取、爬站全套本事，页面交互也带上了，前面说的抓瞎问题，就是这么治好的。

# 实操

我用的是 Codex，装完我直接试了两个活：

```
搜一下最新的Next.js App Router更新日志，给我总结一下
```

![[01_raw/_inbox/文章/images/d5a10359cd2acbdc8e8efc1bf19821e0_MD5.png]]

```
抓取 https://docs.firecrawl.dev 这个页面，列出顶级章节
```

![[01_raw/_inbox/文章/images/c667c2be139359fc60a031ccad58190e_MD5.png]]

两个可能踩的坑提前说，报`spawn npx ENOENT`说明本地没装Node，装个Node 18以上版本就行。

实在不想装Node也有办法，不用本地跑npx，配置直接换成远程地址即可。

# 适合什么人用

做RAG的，拿它把文档站和资料站灌进知识库，比手写爬虫省心太多。

做竞品监控的，定时Crawl对手的官网和定价页，字段级JSON直接进库。

玩AI编程的，给Claude Code或者Codex接上MCP，AI就有了靠谱的眼睛，不再靠训练数据里的旧信息瞎猜。我属于这一类，也是我用得最狠的场景。

n8n、Zapier、Lovable这些平台也有现成集成，不写代码也能接。

# 我的看法

这个项目火得有道理，网页抓取是个脏活，反爬、代理、JS渲染，自己搞一套要脱层皮，搞完还得天天维护。Firecrawl把这些打包成一个API，输出还直接对齐了AI的胃口，省下来的时间拿去做正事不香吗？

但有两件事我得说清楚，它的网页覆盖率官方说96%，剩下那4%大多是防护最严的站，抓不动就是抓不动，别指望它万能，该手写的时候还得手写。开源版是AGPL-3.0协议，商用场景先想清楚协议问题，想不清楚就用云版，别给自己埋雷。

爬虫这事本身也有合规边界，Firecrawl默认遵守`robots.txt`，但守规矩的责任在于用的人，拿它抓什么、怎么用，自己掂量。合规是必须的，不确定的事情不要干。

15.5万 Star不是刷出来的，网页数据这层基础设施，做AI应用的绕不开，Firecrawl目前是这个生态位里最能打的开源选手，我用了几个月，暂时没找到换掉它的理由。

# 开源地址

> https://github.com/firecrawl/firecrawl

_****点击下方卡片，关注极客之家****_

这个公众号曾分享过许多有趣的开源项目。如果你不想逐篇翻阅历史文章，也可以直接关注微信公众号“极客之家”，通过后台留言与我们互动交流

![[01_raw/_inbox/文章/images/596a49b625f0621d118deb17e8ca5be9_MD5.jpg]]

---

内容效果不满意？[点此反馈](https://feedback.notebooksyncer.com/feedback/e96011aa_1785402307977?u=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzU2MTI4MjI0MQ%3D%3D%26mid%3D2247544897%26idx%3D1%26sn%3Def8eb39cf6a5c553241102c7cca067c4%26chksm%3Dfd9413712317db7e556e81aff0a8207cd4b3ac2adaf4235920b704a7c4de00a89817debbba69%26mpshare%3D1%26scene%3D1%26srcid%3D0730AiviOi9Lg1zAZYn96ry2%26sharer_shareinfo%3D2856aad1e895ec5a9ae675ed7a1d34d5%26sharer_shareinfo_first%3D2856aad1e895ec5a9ae675ed7a1d34d5%23rd&s=obsidian)