---
author: 逛逛
source: 微信公众号
url: https://mp.weixin.qq.com/s?__biz=MzUxNjg4NDEzNA==&mid=2247534429&idx=1&sn=c918119b30f6fd50fceeac4e1aa61423&chksm=f8e871efacb3e30c36d0d65a89bf30f3ed79c5d9f0b2c59b9f085f5edbe19ec08e891ae23af3&mpshare=1&scene=1&srcid=0612mptodZYpTfctEPtrPmdy&sharer_shareinfo=bc03efea935dc2d42dc86a7da83d7d61&sharer_shareinfo_first=bc03efea935dc2d42dc86a7da83d7d61#rd
saved: 2026-06-12 15:45:06
tags:
  - 笔记同步助手
annotation: connect wechat to claude code
id: d4ec1a39-cbe0-4487-a344-5e8ab6f6f913
summary: Updated open-source Skill for using Claude Code through WeChat, enabling mobile chat interaction with Claude Code running on desktop for on-the-go capture and task delegation.
processed: 2026-06-12
---

公众号名称：逛逛GitHub

作者名称：逛逛

发布时间：2026-06-11 11:39

原文链接：[https://github.com/Wechat-ggGitHub/wechat-claude-code](https://github.com/Wechat-ggGitHub/wechat-claude-code)

我发现，用多了 OpenClaw、Hermes 这些 AI 个人助理。

最终都会回到 Claude Code 或者 Codex。

![[01_raw/_inbox/文章/images/a7c6116ae09c24d10966d4f254af55a2_MD5.jpg]]

原因很简单， 大部分用到 Agent 的场景都是偏创作和生产力的。

我对 AI Agent 嘘寒问暖、设置一个定时任务没啥真实的诉求。

玩一玩热情就退却了。

最终还是用 Claude Code 或者 Codex 去完成那些比较重的活。

而且我常用的 Skill 在 Claude Code 里面。

所以我把我之前开源的 wechat-claude-code 又捡了起来，体验又优化了几版。

目标是把它做成移动端微信操纵电脑上的 Claude Code 的最佳方案。

![[01_raw/_inbox/文章/images/436979418f883bd5e4840253ec403d76_MD5.png]]

01

**开源项目简介**

这个 Skill 可以让你在微信中链接你的 Claude Code。

扫码绑定微信后，在你微信会出现一个好友。

给这个好友发的消息都会转给你电脑上在运行的 Claude Code，回复也会实时推送到微信，就像在跟一个真人朋友聊天一样。

它支持发送图片、语音、文件，同时它也能把你电脑上的文件发给你。

![[01_raw/_inbox/文章/images/aef85eedd7eed868655d36cf170f9f85_MD5.png]]

```
开源地址：https://github.com/Wechat-ggGitHub/wechat-claude-code
```

02

**最近优化了啥？**

微信消息阅读体验变好了

微信内只展示 Claude Code 吐出来的核心信息，有用但不繁杂

之前会发各种各样乱七八糟的消息，看起来很累。

目前，只把那些干到哪儿了、怎么干的有效信息发出来。

![[01_raw/_inbox/文章/images/ee05c5353786b9d5d467a80d751b3364_MD5.png]]

长时间不响应安抚情绪

而且，我还设置了一个有意思的点。

如果 Claude Code 超过 5 分钟没有响应（可能有一个任务一直在处理，但是并没交付呢）

就会从一个安抚话术的池子里挑句话发给你。

安抚你的情绪的同时，能让你感受到 Agent 没挂呢，还在干活。

![[01_raw/_inbox/文章/images/30c05bc138ce9e54f84561ce023a333a_MD5.png]]

对方正在输入中...

之前一直没做，现在支持了。

如果 Agent 在干活，顶部会显示“对方正在输入中...”

![[01_raw/_inbox/文章/images/9803a2c23b42b16e3abac26feb506947_MD5.jpg]]

电脑体验一致

这个我觉得是最重要的是一点。

很多微信或者飞书接入自己电脑上的 Claude Code 的插件，用起来感觉不很对。

像是电脑上面对是一个 AI，手机上用是另外一个 AI。

体验很不一致。

这个问题也解决了，主要是之前微信发一个消息，走到的是 SDK 模式而不是 CLI 。

你可以试一下，在电脑上打开 Claude Code 输入一个指令，它怎么编排怎么输出的。

手机上输入同一个指令，效果也差不多。

这一点我觉得还挺重要的。而且现在不需要反复确认，默认是全自动模式。

支持文件收发

你不光能发送图片、语音、Word、PDF 等等文件给 Claude Code。

它生成了一个文件也能通过微信发给你。

![[01_raw/_inbox/文章/images/be83320ba16aaf1e5e6be17918fa352b_MD5.png]]

比如让它写个文章，不只是说：我写完了，我放在了电脑的桌面上。

而是会直接推给你，你能在微信上看到这个文件内容。

![[01_raw/_inbox/文章/images/3c5a637fe21cea11ed0de4d25574c9d0_MD5.jpg]]

甚至你电脑上没在手边，你直接告诉他，把我电脑上的 xxxx 文件发给我。

它会直接发给你，这个还挺方便的。

02

**后面想做啥？**

目前有一个很大的问题，就是消息队列的问题。

我们的习惯是微信里面连续发多个指令，但是 Claude Code 一般是一个个的去处理的。

![[01_raw/_inbox/文章/images/23df2a4940f73d71f0654080346c8c5a_MD5.png]]

有时候你连着发多个指令，AI 的回复就会驴唇不对马嘴。

这个我后面会优化一下，但是还没想好怎么去做。大家有想法吗？可以聊一聊。

电脑休眠不中断

比如电脑锁屏或者合上盖子， Claude Code 进程就停止了，你给它发消息它不会回复。

但是有一些命令是可以设置的。 macOS 自带一个命令叫 `caffeinate`，可以阻止系统睡眠。

我后面研究一下融入到 Skill 里面。

![[01_raw/_inbox/文章/images/2d3b0032b67198177479451ca16afc26_MD5.png]]

基于当前会话接着聊

目前使用这个 Skill 其实和当前聊天的 Claude Code 实例是独立的，工作空间可能也不一致。

但是很多场景是电脑上聊了很长时间，但是要出去吃饭，想接着处理。

就需要基于当前电脑上的会话接着聊，这个还没想好怎么做。

记个代办。

03

**如何使用**

直接把下面这句话发给你的 Claude Code：

```
请你读取这个开源项目，把这个 skill 安装、部署一下：
https://github.com/Wechat-ggGitHub/wechat-claude-code
```

然后你就等着安装 Skill、部署就行了。然后重启 Claude Code，输入 /wechat-claude-code

它会弹出来一个二维码，你拿微信扫一下就行了。

可以通过 /wechat-claude-code 来管理微信和 Claude Code 通信的进程。

启动/重启/停止等等。

![[01_raw/_inbox/文章/images/9e92d6fa1339ef1fef02d57810da78be_MD5.png]]

04

**另外想聊**

这些 feature 都是我在持续用的过程中，发现问题直接微信给 Claude Code 说，让它：

分析问题 -> 给出解法 -> 我检查一下 -> 修复 -> 重启 Skill -> 我再体验一下，没问题就推送到 GitHub 上了。

一边聊一边去修改，哪里体验不好改哪里，迭代还挺快的。

另外为啥不支持飞书、企业微信等等其它 IM？

因为习惯。

大家用微信的习惯刻在骨子里，飞书可能更开放一些，体验可能更好，比如 markdown 格式的阅读体验。

但是我确实没有用飞书的习惯，刚开始 OpenClaw 火的时候用的很多。

热度退了，我就切回到微信了。 就好像你用了 Notion、Obsidian 等等各种笔记软件，最终又回到了备忘录。。。

为啥不支持 Codex？

因为我使用 Claude Code 更深度，能在体验上有所打磨。

后面 Codex 用多了也会支持 Codex。

05点击下方卡片，关注逛逛 GitHub这个公众号历史发布过很多有趣的开源项目，如果你懒得翻文章一个个找，你直接关注微信公众号：逛逛 GitHub ，后台对话聊天就行了：

---

内容效果不满意？[点此反馈](https://feedback.notebooksyncer.com/feedback/b8464c71_1781271904533?u=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzUxNjg4NDEzNA%3D%3D%26mid%3D2247534429%26idx%3D1%26sn%3Dc918119b30f6fd50fceeac4e1aa61423%26chksm%3Df8e871efacb3e30c36d0d65a89bf30f3ed79c5d9f0b2c59b9f085f5edbe19ec08e891ae23af3%26mpshare%3D1%26scene%3D1%26srcid%3D0612mptodZYpTfctEPtrPmdy%26sharer_shareinfo%3Dbc03efea935dc2d42dc86a7da83d7d61%26sharer_shareinfo_first%3Dbc03efea935dc2d42dc86a7da83d7d61%23rd&s=obsidian)