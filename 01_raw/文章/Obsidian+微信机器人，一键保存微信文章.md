---
author: 文科佬爱捣腾
source: 小红书
url: https://www.xiaohongshu.com/discovery/item/675d9a1c0000000002017e59?app_platform=ios&app_version=9.30.1&share_from_user_hidden=true&xsec_source=app_share&type=normal&xsec_token=CBRN2M-rmcG3c1j99WedDO-18zuXLodP2lTRiEstQU__Y=&author_share=1&xhsshare=WeixinSession&shareRedId=Nzs4RERHO0tLPD1GOjswPEg5Qk06PjpN&apptime=1779350145&share_id=6873020fab9c401f92d055a219a03ccd&code=9ciknWpSS4
saved: 2026-05-21 09:57:46
tags:
  - 笔记同步助手
id: 4ab02b9c-f021-46ec-bbbd-1ace22452392
annotation: one of the ways to clip wechat content, but I already have better solutions. for reference in the future only as an additional option
summary: "Describes integrating a WeChat chatbot (chatgpt_on_wechat) with Obsidian to auto-save WeChat articles, images, and files as Markdown notes. Uses Selenium for web scraping, Alibaba Cloud OSS for image storage, and a TimeTask plugin for scheduled reminders, positioning itself as a replacement for tools like Cubox and flomo."
---

# Obsidian+微信机器人，一键保存微信文章

## Obsidian + 微信机器人，一键保存微信文章

Obsidian 是一款基于 Markdown 的笔记软件，最近我刚刚从 flomo 迁移到 Obsidian，用来搭建个人知识库。

微信机器人助理（基于开源项目 chatgpt\_on\_wechat）则是一个能在微信平台上实现智能交互的工具。通过使用另一个微信小号在本地电脑登录，它可以接收主微信号的消息并进行自动化处理。

两者结合后潜力巨大：

1.  移动端随时分享灵感和互联网文章到 Obsidian，替代 flomo 的移动端记录功能。
2.  Obsidian 作为本地知识库，可被大模型读取，实现与微信端的互动分析。
3.  替代 Cubox 的文章收藏功能，通过机器人自动抓取微信分享链接的内容。
4.  利用插件实现类似滴答清单的定时任务提醒功能，特别适合微信群协作场景。

这篇文章不深入技术细节，有代码基础的朋友结合 Cursor 等 AI 编程工具可以快速实现。以下内容中，我用“微信机器人助理”指代 chatgpt\_on\_wechat。

### 1\. 文字信息收藏

微信机器人助理可以接收来自单聊或群聊的消息，并将其保存为 Markdown 格式，自动存入 Obsidian 的指定文件夹。配合 Obsidian 的多端同步功能，可以在任意设备上随时查看和整理这些信息。

我目前设置为：当我与微信机器人私聊时，所有聊天记录都会被自动保存。因此，只要有灵感或需要记录的内容，直接发给机器人即可完成存档。

当收到微信分享的链接时，机器人会自动提取标题和正文内容，生成 Markdown 文件保存到 Obsidian 中。这相当于在移动端实现了 Web Clipper 功能。

由于微信近年对分享功能限制严格，大多数第三方工具已无法抓取文章内容。过去一年里，只有 Cubox 能稳定实现这一功能，因此我也曾长期依赖它来收藏文章和文件。

早期迁移到 Obsidian 时，我还购买过 Message 插件，试图实现微信分享到 Obsidian 的功能。但体验很差——只能保存文本和图片，无法抓取链接中的正文内容，使用场景非常有限。

现在这套方案的具体实现方式是：  
微信机器人接收到链接 → 使用 Selenium 库调用本地浏览器打开页面 → 抓取标题和正文 → 生成 .md 文件 → 保存至 Obsidian。

由于个人使用对速度要求不高，Selenium 方案已经足够，且较少触发微信的反爬机制。

示例日志：

```
[INFO][TimeTask][ObsidianHandler] 消息已保存：D:\BaiduSyncdisk\笔记\WeChat\doc\chat\private\2024-12-14\183135\OpenAI吹哨人被证实死亡！年仅26岁曾参与GPT-4预训练团队-今日头条.md
```

抓取的文章内容如下：

> **OpenAI吹哨人被证实死亡！年仅26岁曾参与GPT-4预训练团队**  
> 财联社12月14日讯（编辑 马兰）OpenAI吹哨人、年仅26岁的前研究员 Suchir Balaj，几周前被发现死于旧金山的一间公寓中。旧金山首席法医办公室执行主任 David Serrano Sewell 已在一封邮件中证实此消息，死因为自杀。
> 
> 旧金山警方表示，11月26日下午接到报警前往布坎南街某公寓进行健康检查，发现一名成年男子已无生命体征，初步调查未发现谋杀证据。
> 
> Balaj 今年早些时候离开 OpenAI，并曾发出警告，称 ChatGPT 涉嫌违反美国版权法。
> 
> OpenAI 发言人确认了 Balaj 的死讯，表示公司上下深感悲痛，“在这个艰难时刻，我们的心与他的亲人同在”。
> 
> Balaj 是一名印度裔美国人，毕业于加州大学伯克利分校计算机科学专业，曾在 OpenAI 和 Scale AI 实习，后正式加入 OpenAI，参与过 WebGPT、GPT-4 预训练、o1 推理团队及 ChatGPT 后训练工作。
> 
> 在 OpenAI 工作四年后，他突然辞职，强调“人工智能技术带来的社会危害将远超其益处”。
> 
> 10月，《纽约时报》专门报道了他的担忧：他认为 ChatGPT 等聊天机器人正在破坏原创数字内容创作者的商业未来，而这些数据正被广泛用于训练 AI 模型。

### 2\. 图片与文件保存

图片和文件的保存功能是我熬夜调试出来的。平时看书截图、收集资料图片，都希望能一键存入 Obsidian。过去没有自动化手段，只能依赖 Cubox 临时保存。

现在的处理流程是：

-   微信机器人接收到图片后，先上传至阿里云 OSS（对象存储服务）
-   将生成的外链插入 Markdown 文件中

这样做的好处是避免本地图片过多导致 Obsidian 运行卡顿。使用 OSS 图床性价比很高，一年仅需 9 元，完全够个人使用。

对于文件类内容（如 PDF、Word、PPT），我设置为直接保存到 Obsidian 的指定文件夹中，不做格式转换。虽然目前只是当作网盘使用，但未来可以将这些文件内容纳入知识库，通过 RAG 技术让大模型进行分析和检索。

### 3\. 定时提醒功能

微信机器人助理支持插件扩展，其中有一个 TimeTask 插件，可以通过关键词指令创建定时任务提醒。

虽然微信本身也有定时发送功能，但无法在群聊中设置提醒。而微信机器人可以在群内定时推送通知，非常适合会议频繁、需要团队协作的场景。

示例交互：

> 我发送：`$time1、会议时间：2024.12.12（周四）下午 16:00-`  
> 机器人回复：`[bot] 定时任务创建成功！任务ID：9a2b19d8，时间：16:00:00，周期：2024-12-12`

到点后机器人会自动提醒：

> 叮铃铃，定时任务时间已到啦~  
> 【当前时间】：2024-12-12 16:00:00  
> 【任务详情】：主题：会议提醒

### 4\. 总结

总结一下，如果你喜欢折腾，将 Obsidian 和微信机器人助理结合起来，完全可以替代 Cubox、flomo、滴答清单等工具的核心功能。未来还有可能实现“All-in-One”的理想笔记系统。

在这个 AI 时代，我们比以往任何时候都更容易开发属于自己的个性化工具，不再只能被动等待厂商更新功能。自己动手，丰衣足食，真的太爽了！

\#AI工具 \#效率工具 \#知识管理 \#Obsidian \#程序员

![[01_raw/_inbox/文章/images/f440ec67715a6e293dfd5b638c20f9c5_MD5.jpg|Image]]![[01_raw/_inbox/文章/images/d42e96cf382272ebe7a6c20b07cb1fd1_MD5.jpg|Image]]![[01_raw/_inbox/文章/images/201ce5d53e5879085005b3301de5941e_MD5.jpg|Image]]![[01_raw/_inbox/文章/images/6232c0a3650aef11bbbcf8915c2e0d7d_MD5.jpg|Image]]![[01_raw/_inbox/文章/images/ac9c6d43029ba43bed75b791e81e7597_MD5.jpg|Image]]

大家好, 我是文科佬爱编程 👋  
今天给大家分享一个超实用的 AI 工具组合玩法~  
🔥 核心功能亮点:  
1\. 一键保存微信文章到 Obsidian  
2\. 自动提取文章内容生成笔记  
3\. 智能图片云端存储  
4\. 群聊智能定时提醒  
✨ 为什么要这么做?  
\- 告别手动复制粘贴  
\- 随时随地记录灵感  
\- 打造个人知识库  
\- 替代多个付费软件  
🛠 具体实现方案:  
\- 使用 chatgpt\_on\_wechat 项目搭建微信机器人  
\- 通过 selenium 实现文章内容抓取  
\- 阿里云 OSS 存储图片 (每年仅需 9 元)  
\- Obsidian 多端同步实现随时查看  
💡 进阶玩法:  
\- 结合大模型实现知识库智能分析  
\- 自定义定时提醒功能  
\- RAG 技术打造专属 AI 助手  
🎉小红书体验分享:  
之前我用过很多工具: Cubox/flomo/滴答清单, 现在通过这套组合, 不仅省钱还能实现个性化定制, 真的是太爽了!  
\#AI工具 \#效率工具 \#知识管理 \#Obsidian \#程序员  
记得点赞收藏噢! 有问题可以在评论区交流~

---

### 评论

-   **A**: 统一回复一下，感兴趣的朋友很多。说实话，这个联动只适合会点python的编程，愿意折腾的人，用的都是github公开的微信机器人项目配合cursor改的，不推荐不会编程的朋友实践哈。有同样爱折腾的朋友可以加好友随时交流。
-   **B**: 会封号吗？这样爬微信
    -   **A**: 很早的项目了，已经不行了
    -   **C**: 我现在用的这个 自己做的\[偷笑R\]![[01_raw/_inbox/文章/images/93e122464025791445992baaa62b6ab8_MD5.jpg|Image]]
-   **D**: how to？
    -   **A**: 谢谢朋友关注，可以看看我的上面回复。