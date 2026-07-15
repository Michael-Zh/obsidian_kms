---
author: 维客笔记
source: 微信公众号
url: https://mp.weixin.qq.com/s?__biz=Mzk2NDU0NDczMg==&mid=2247493708&idx=1&sn=97493ec1c99eb415c81e17e62a026daa&chksm=c58278f21fba92efef781e60d0e9b0eaf5d11f7c7814864e5c1ab960219ef6ca11c7dfef8be9&mpshare=1&scene=1&srcid=0521G2o3f1Dw50tW6oqqrANk&sharer_shareinfo=3677adee39c8cc6709f0ecb63000fd19&sharer_shareinfo_first=e62aea93f447247bbfb3a7db15fa12b3#rd
saved: 2026-05-29 00:03:03
tags:
  - 笔记同步助手
id: e039f969-a9ba-468a-9b8c-13354409fdc1
annotation: Obsidian Web Clipper templates (put to backlog)
summary: "Shares and analyzes 13 Obsidian Web Clipper templates (12 from Obsidian CEO kepano plus one custom WeChat template), covering YouTube, Wikipedia, arXiv, Goodreads, IMDB, Letterboxd, Google Maps, Redfin, and ChatGPT pages. Explains key design patterns: Schema.org JSON-LD extraction, CSS selector chains, wikilink filters for graph connections, and multi-step HTML cleaning pipelines."
processed: 2026-06-06
---

公众号名称：维客笔记

作者名称：维客笔记

发布时间：2026-05-08 18:06

![[01_raw/_inbox/文章/images/c5e9487f05776adf925a8002948e97bf_MD5.png]]

大家好，我是来自1037号森林的维客！

# 01 聊几句

前段时间打通了微信和Obsidian，可以方便地在移动端进行各种剪藏～

但我相信有很多小伙伴的剪藏场景是在电脑端，大屏不管是阅读还是编辑体验都更加不错。

关于电脑端的剪藏插件，我之前也分享过很多款（简悦、cubox等），目前我最推荐剪藏插件是Ob官方开发的web clipper插件\[1\]，剪藏十分丝滑！

  

![[01_raw/_inbox/文章/images/eb74ed5e6032fa430b5dfff3ddf72c8f_MD5.png]]

  

这个插件支持 Chrome、Firefox、Safari、Edge 等主流浏览器。

它的功能用一句话概括：能把网页内容一键转成 Markdown 格式，直接保存进你的 Obsidian 知识库。

Note

如果你对Obsidian web clipper剪藏插件还不了解，可以去查阅我之前撰写的使用教程：

-   [初次发布](https://mp.weixin.qq.com/s?__biz=Mzk2NDU0NDczMg==&mid=2247492345&idx=1&sn=01fbb4466e5ad92b76cbd0beeda72390&scene=21&poc_token=HD6r_WmjZMnfJGttkXHpARU54c9vTpBm4yxfS9cD#wechat_redirect)
    
-   [支持全文剪藏&高亮剪藏](https://mp.weixin.qq.com/s?__biz=Mzk2NDU0NDczMg==&mid=2247492349&idx=1&sn=5dd959d3d86fd16d6b4796071aa26b42&scene=21&poc_token=HHir_WmjP5srUDkFt0c1tTcNZEPk62Sv6kDXwUDT#wechat_redirect)
    
-   [AI加持](https://mp.weixin.qq.com/s?__biz=Mzk2NDU0NDczMg==&mid=2247492367&idx=1&sn=f726b181ba67c692ae3b21ad61649da0&scene=21#wechat_redirect)
    
-   [嵌入式侧边栏](https://mp.weixin.qq.com/s?__biz=Mzk2NDU0NDczMg==&mid=2247492410&idx=1&sn=7eca8ecec62ce0773fdc800821c042a6&scene=21&poc_token=HMmr_WmjZxzY2gGAIRky-awpaRLDR9cFmHB2faIj#wechat_redirect)
    
-   [支持阅读模式](https://mp.weixin.qq.com/s?__biz=Mzk2NDU0NDczMg==&mid=2247492972&idx=1&sn=fd2674300b8a29f5ec3dfb9d60b227dc&scene=21&poc_token=HPiq_WmjyrcEN4iX6YleXnEf0cqklm06KlVmbFgQ#wechat_redirect)
    
-   [支持与油管交互，剪藏油管字幕了](https://mp.weixin.qq.com/s?__biz=Mzk2NDU0NDczMg==&mid=2247493098&idx=1&sn=368c3df399f7c0a46babe14f9e42f6f8&scene=21#wechat_redirect)
    

  

我是看着Ob长大的🤣

其实它除了"一键剪藏"这个强大的特性之外，还有一个更强的但被很多人忽略的**模板系统**。

不同的网站，信息结构完全不同。YouTube 视频有标题、频道、描述；豆瓣（以及 Goodreads）有书名、作者、评分；学术论文有摘要、作者、发表日期……通用的剪藏方案往往一锅乱炖，而模板让你能为每种内容类型**定制专属的字段结构**，剪进来就是整齐的结构化笔记。

Obsidian 的 CEO **Steph Ango（即 kepano）** 在 GitHub 上开源了一批他自用的剪藏模板，目前已收获 **1,200+ Stars**。

本篇文章，就分享他的12个模板，并拆解几个，理解它们的设计思路，帮你找到最适合自己的那几个。

第13个，是我构建的一个微信公众号剪藏模板🤣～

好了，任务清楚了，开干！

# 02 12个剪藏模板

我看了一下这个仓库的readme\[2\],写得非常简洁😅

Example

![[01_raw/_inbox/文章/images/3faf553b7c04af2a5851ae60a0ead831_MD5.png]]

就将模板分为了两类：

  

> 模板下载，请在本公众号后台回复关键字：20260508

**通用模板**

-   Recipes（食谱）
    
-   Product（商品）  
    **特定网站模板**
    
-   YouTube
    
-   Wikipedia
    
-   arXiv
    
-   Goodreads
    
-   IMDB（两个版本）
    
-   Letterboxd
    
-   Google Maps
    
-   Redfin
    
-   ChatGPT
    

  

# 03 来学习一下

## 3.1 一点基础，读懂模板 JSON 的结构

具体参考web clipper帮助文档\[3\]，这里我简单总结概括一下～

每个模板本质上是一个结构化配置文件，包含以下核心字段：

| 字段 | 作用 |
| --- | --- |
| `schemaVersion` | 模板格式版本（目前均为 `"0.1.0"`） |
| `name` | 模板名称，显示在扩展界面 |
| `behavior` | 行为：`"create"`（创建新笔记）或 `"append"`（追加到已有笔记） |
| `noteNameFormat` | 笔记文件名的生成规则，支持变量 |
| `path` | 笔记保存路径（相对于 Vault 根目录） |
| `noteContentFormat` | 笔记正文内容的模板，支持变量和过滤器 |
| `properties` | YAML Front Matter 字段列表，每项包含 `name`/`value`/`type` |
| `triggers` | 触发条件（URL 前缀、正则、schema 类型） |
| **五类数据提取方式：** | <br> |

1.  **`{{schema:字段名}}`** — 读取页面内嵌的 Schema.org 结构化数据（JSON-LD）
    
2.  **`{{selector:CSS选择器}}`** — 用 CSS 选择器直接抓取 DOM 元素文本
    
3.  **`{{selectorHtml:CSS选择器}}`** — 抓取 DOM 元素的 HTML，再做后续处理
    
4.  **`{{meta:name:属性名}}`** — 读取 HTML  标签
    
5.  **`{{url}}`、`{{title}}`、`{{date}}`** 等 — 页面通用变量
    

  

**过滤器（Filter）链式语法：**

  

> ```
> {{变量|过滤器1|过滤器2|...}}
> ```

  

常用过滤器包括：`wikilink`（转为 `[[...]]` 格式）、`join`（数组合并）、`split:分隔符`（字符串分割）、`slice:起:止`（切片）、`date:格式`（日期格式化）、`markdown`（HTML 转 Markdown）、`unique`（去重）、`replace`（替换）、`table`（对象转 Markdown 表格）、`list:task`（转为任务列表）等。

  

## 3.2 拆解几个

### 🎥 YouTube Clipper

**适用场景**：保存视频笔记、记录值得复看的内容

YouTube 是信息密度极高的平台，但视频本身难以检索。这个模板可以把一个 YouTube 视频页面转化为结构化笔记，通常会抓取：视频标题、频道名、发布日期、视频描述、来源 URL。

有了这个模板，你的 Obsidian 里可以建立一个"已看视频库"，随时用 Dataview/bases 检索"我看过哪些视频"或"我保存了哪些关于 AI 的内容"。

但这个模板竟然没有把web clipper的最新功能—[直接获取油管字幕](https://mp.weixin.qq.com/s?__biz=Mzk2NDU0NDczMg==&mid=2247493098&idx=1&sn=368c3df399f7c0a46babe14f9e42f6f8&scene=21#wechat_redirect)给用上，这里我们可以自己添加一下。

  

![[01_raw/_inbox/文章/images/772af560293d3bec4920fd0a8c58fb29_MD5.png]]

  

> ```
> {{transcript}}
> ```

  

这样添加之后，再去剪藏，就会包含字幕了。

Example

![[01_raw/_inbox/文章/images/781560f0af6715b7a1651f197d73b9e4_MD5.png]]

设计解析

-   **笔记命名设计**：`{{schema:author}} – {{schema:name}}` 使用破折号分隔频道名和视频标题，生成如 `3Blue1Brown – 线性代数的本质` 这样的文件名，兼顾可读性与可检索性。
    
-   **正文内容设计**：只有一行 `![{{schema:name}}](https://mp.weixin.qq.com/%7B%7Burl%7D%7D)`，这是 Obsidian 支持的视频嵌入语法。打开笔记时，视频会直接嵌入显示，实现"笔记即播放器"的效果，而不是仅仅存一个链接。
    
-   **数据来源全部依赖 Schema.org**：YouTube 在每个视频页面都内嵌了完整的 `VideoObject` 类型的 JSON-LD 数据，包含 `name`（视频名）、`author`（频道名）、`uploadDate`（发布日期）、`thumbnailUrl`（缩略图 URL）。使用 `schema:` 变量比 DOM 选择器更稳定——YouTube 经常更新页面结构，但 Schema.org 数据相对固定。
    
-   **`slice:0` 的用法**：`{{schema:thumbnailUrl|slice:0}}` 中的 `slice:0` 是取数组第一个元素，因为 YouTube 的 `thumbnailUrl` 有时以数组形式返回多个尺寸的图片 URL，这里取第一个。
    
-   **`wikilink` 的设计意图**：`author` 字段使用了 `wikilink` 过滤器，将频道名转为 `[[频道名]]` 格式。这意味着多次保存该频道的视频后，Obsidian 图谱中会自然形成"频道节点"，所有相关视频都会连接到它，无需手动建立关联。
    
-   **存储路径**：保存到 `Clippings` 文件夹，这是 kepano 个人 Vault 的惯例，使用者可按需修改。
    
-   **触发条件**：URL 前缀 [https://www.youtube.com/watch?v=](https://www.youtube.com/watch?v=)
    

  

### 📖 Wikipedia Clipper

**适用场景**：知识研究、概念整理

Wikipedia 页面内容复杂，包含大量导航栏、脚注、参考文献框。这个模板使用 CSS 选择器精准抓取正文主体，同时**过滤掉** navbox、printfooter、side-box 等干扰内容，只保留真正有价值的百科正文。

设计解析

这个模板的核心是一行非常精炼的 `noteContentFormat`：`{{selectorHtml:#mw-content-text|remove_html:(\".navbox,.printfooter,.side-box\")|markdown}}`，我们可以学习一下它的多过滤器链式处理方法：

**第一步 `selectorHtml:#mw-content-text`**：`#mw-content-text` 是 MediaWiki 引擎（维基百科所用的 Wiki 引擎）中包含所有文章正文的标准 DOM 容器 ID。使用 `selectorHtml` 而非 `selector` 是因为要保留内部的 HTML 结构，以便后续处理成 Markdown（包括标题层级、加粗、链接等）。

**第二步 `remove_html:(".navbox,.printfooter,.side-box")`**：精准移除三类干扰元素：

  

-   `.navbox`：文章底部的导航框（如"参见"、"相关主题"框）
    
-   `.printfooter`：打印页脚
    
-   `.side-box`：侧边信息框（某些语言版维基的特有元素）
    

  

这个过滤器背后的思路是：只需要文章正文，其他所有导航性、辅助性内容都是噪音。

**第三步 `|markdown`**：将清洁后的 HTML 转为 Markdown 格式，保留标题、段落结构、内部链接等。

  

### 🤖 ChatGPT Clipper

**适用场景**：保存重要对话、沉淀 AI 使用心得

这是最独特的一个模板。可以将对话内容直接"剪"进 Obsidian。

可以保存：对话标题、对话内容（Markdown 格式），保留对话顺序。

但是目前这个模板剪藏不了内容了（主要是因为chatgpt网站的变更）：

  

![[01_raw/_inbox/文章/images/a3db97a058d3dca38cc52a34e42fa8b5_MD5.png]]

  

我对其进行了修改：

```
{{selectorHtml:[data-message-author-role]|join:"\n\n"|replace:"/(<[^>]*data-message-author-role=\"user\"[^>]*>)/g":"$1You:"|replace:"/(<[^>]*data-message-author-role=\"assistant\"[^>]*>)/g":"$1ChatGPT:"|markdown}}
```

  

### 🔆 微信公众号模板

这个是我设计的一个模板，用于剪藏微信公众号文章。

  

![[01_raw/_inbox/文章/images/b25b05a697081e94e6db8ea529e350e3_MD5.png]]

  

-   published：可以获取文章发布时间
    
-   cover：可以获取文章封面
    
-   tags：集成了AI解释器
    
-   comments：集成了AI解释器，一句话总结
    

  

该模板和其他12个放在一起了，可以一起下载～

# 04 使用教程

简单说一下模板配置吧

  

-   下载模板（在本公众号后台聊天界面，回复关键字：`20260508`）
    
    ![[01_raw/_inbox/文章/images/8e25e6102a8f4eac143b5da1731e3d28_MD5.png]]
    
-   批量导入，打开插件的设置➡️导入
    

  

![[01_raw/_inbox/文章/images/58562b44a410d050abb044f9ba44fd82_MD5.png]]

  

![[01_raw/_inbox/文章/images/f84ac73b6ec9a3371ad98a79aa6be088_MD5.png]]

  

# 05 写在最后

今天的分享就到这里吧！

关于我修改的几个模板，我在github上建了一个公开的仓库分享，方便后续的维护，并且会DIY更多模板。

仓库链接：[https://github.com/BCS1037/obsidian-web-clipper-templates](https://github.com/BCS1037/obsidian-web-clipper-templates)

  

欢迎关注维客笔记，一起探索解决问题的极简方式！

  

A better you, A bigger world！

少一点儿空谈，多一些真实交付！

-   我写了一个 [给大家的 AI 实战案例专栏](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=Mzk2NDU0NDczMg==&action=getalbum&album_id=4469519143632912386#wechat_redirect)，分享我亲身实践的 25+ 个 AI 实战案例，让 AI 真正为我们所用！
    
-   [第1期：学术图片修复](https://mp.weixin.qq.com/s?__biz=Mzk2NDU0NDczMg==&mid=2247493088&idx=1&sn=70ab020307c86415118912ce598ac864&scene=21#wechat_redirect)
    
-   [第2期：Vibe Coding实战，为Obsidian插件添加自己想要的功能](https://mp.weixin.qq.com/s?__biz=Mzk2NDU0NDczMg==&mid=2247493133&idx=1&sn=6f05adbaecae93fb8a85ffec04577fd4&chksm=c47377bef304fea80fd97853b2ae62f1325106caa654c8fd34d7c9298f3c412825f0127b4a98&scene=21&cur_album_id=4469519143632912386&search_click_id=#wechat_redirect)
    
-   [第3期：脏活累活，交给AI](https://mp.weixin.qq.com/s?__biz=Mzk2NDU0NDczMg==&mid=2247493166&idx=1&sn=5c0c5cd99b188001bcc727a79485c06c&scene=21#wechat_redirect)
    
-   [第4期：用AI搞定证据处理](https://mp.weixin.qq.com/s?__biz=Mzk2NDU0NDczMg==&mid=2247493210&idx=1&sn=4554e4188e64cbe96231e6877f878024&scene=21#wechat_redirect)
    
-   [第5期：开庭前，用 AI 把对方的牌提前摸一遍](https://mp.weixin.qq.com/s?__biz=Mzk2NDU0NDczMg==&mid=2247493261&idx=1&sn=adebcfb7e37419a469e195fb0ff01416&scene=21#wechat_redirect)
    
-   [第6期：用AI撰写5种法律文书](https://mp.weixin.qq.com/s?__biz=Mzk2NDU0NDczMg==&mid=2247493334&idx=1&sn=5a2244ef310be684ba877719b11dcaf4&scene=21#wechat_redirect)
    
-   [第7期：AI助我搞定期刊论文封面，已发表！](https://mp.weixin.qq.com/s?__biz=Mzk2NDU0NDczMg==&mid=2247493490&idx=1&sn=7c55f23d88ca5a5d8579308a2dbfc938&scene=21#wechat_redirect)
    
-   [第8期：用AI搞定期刊论文封面，一句话顶一堂PS课](https://mp.weixin.qq.com/s?__biz=Mzk2NDU0NDczMg==&mid=2247493637&idx=1&sn=dd4cc62dfef934dd62ca5cdf8d152387&scene=21#wechat_redirect)
    
-   [第9期：接单了！欢迎找我私人定制 Obsidian 插件～](https://mp.weixin.qq.com/s?__biz=Mzk2NDU0NDczMg==&mid=2247493686&idx=1&sn=0d31f58e4752575eb971d6701044dcde&scene=21#wechat_redirect)
    

非常感谢【点赞👍、推荐❤️、赞赏💰】，因为有你，所以坚定前行！

---

1.  https://obsidian.md/zh/clipper#more\-browsers ↩
    
2.  https://github.com/kepano/clipper-templates ↩
    
3.  https://obsidian.md/help/web-clipper/filters ↩
    

---

![[01_raw/_inbox/文章/images/21f69f6f26f7a70467c6fbc35a47cfdf_MD5.jpg|cover_image]]

Original 维客笔记 维客笔记

---

内容效果不满意？[点此反馈](https://feedback.notebooksyncer.com/feedback/603fbb97_1780005780767?u=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzk2NDU0NDczMg%3D%3D%26mid%3D2247493708%26idx%3D1%26sn%3D97493ec1c99eb415c81e17e62a026daa%26chksm%3Dc58278f21fba92efef781e60d0e9b0eaf5d11f7c7814864e5c1ab960219ef6ca11c7dfef8be9%26mpshare%3D1%26scene%3D1%26srcid%3D0521G2o3f1Dw50tW6oqqrANk%26sharer_shareinfo%3D3677adee39c8cc6709f0ecb63000fd19%26sharer_shareinfo_first%3De62aea93f447247bbfb3a7db15fa12b3%23rd&s=obsidian)