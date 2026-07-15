---
author: 火箭君
source: 微信公众号
url: https://mp.weixin.qq.com/s?__biz=MzI2MjEyODE4OA==&mid=2650484126&idx=1&sn=2c822d264be0f0770197f510e8a9ed3d&chksm=f3c6c5ac5221b90446ff961fb3113ca95c6effd629262946a4f2fec2d4fca07ebb80acf55149&mpshare=1&scene=1&srcid=0502lsmWtknosW3p7GtJMPdR&sharer_shareinfo=0ab2d16bb62e202f4c20785348d12c35&sharer_shareinfo_first=b701807364c0dbae5b8b02070000d8bf#rd
saved: 2026-05-29 00:03:40
annotation: new options for note taking app (Tolaria)
tags:
  - 笔记同步助手
id: 00e15fae-6342-41f9-8240-c7ff12d1a915
summary: Review of Tolaria, an open-source local-first note-taking app combining Obsidian's file-over-app philosophy with Notion-like block editing. Differentiators include built-in Git versioning replacing a recycle bin, 'Types as lenses' non-mandatory classification, and a built-in MCP server enabling direct AI read/write access to the vault.
processed: 2026-06-06
---

公众号名称：效率火箭

作者名称：火箭君

发布时间：2026-04-26 15:30

![[01_raw/_inbox/文章/images/7847726fb1ee450c83bff9741def1f0d_MD5.png]]

Tolaria，这款工具很新，也挺火。

如果你看过或者用过它，很难不被它吸引。且不论它能走多远，在大家以为 PKM 已经没什么新花样的年代，Tolaria 这样一个真正的后来者，能做到如此出色，确实让人感叹。

# 什么叫做后发优势？

经常读我文章的各位，想必已经对 Notion / Obsidian 之类的知识管理工具耳熟能详了，各种优劣点也能如数家珍。

先说 Notion。它的界面和操作足够友好，也有原生 AI 集成；但它锁定云端，没有本地优先的数据主权，也很难给用户留下自由折腾的空间。

再说 Obsidian。它插件众多，适合折腾，本地优先，数据自主；但云同步相对孱弱，协作也基本不要想了，AI 集成目前也仍在推进中。

还有一些 PKM 工具也各有特色，有的引入了 Type「类型」的概念，我个人很喜欢；有的则主打短平快，而且开源。

到了 2026 年，在 AI Coding 的加持下，少数人也终于可以打造出大家心目中的 PKM 工具，而且功能上几乎没有妥协。这个站在后发者角度出现的产品，就是 Tolaria。

和 Notion 相比，它有类似的 / 命令和文档模块，编辑界面也有相似之处；但 Tolaria 更像是一个本地优先的 Notion。

和 Obsidian 相比，它也有双向链接、纯本地 Markdown 文件和 YAML 支持；但 Tolaria 更像是一个开源取向的 Obsidian 替代品。

其实还不止这些。我只是想说，Tolaria 这个后来者非常熟悉它的前辈们，并且有针对性地找到了各自的差异点。这不像是一个笔记爱好者吹牛的作品，也不像是什么知识管理体系卖课的套路，反倒像是真正懂行的人出手做出来的结果。它虽然后发，却有一种集大成作品的气质。

# Tolaria 登场

![[01_raw/_inbox/文章/images/f8a7eab26fc7b607e5a021d0251dc143_MD5.png]]

这款产品的常规特性我就不再介绍了，有常见笔记工具经验的用户肯定上手就会用。什么模块化笔记、双向链接、Markdown 语法……它基本都支持。

![[01_raw/_inbox/文章/images/bbd20e0e31feb34a7495bde49d108cf4_MD5.png]]

我就讲讲几个给我留下深刻印象的地方。

## Obsidian File Over App 理念的继承者

在 Tolaria 里，没有黑盒数据库，没有云端同步的强制绑定。每一个笔记，就是一个干干净净的 .md 文本文件。

这意味着哪怕明天 Tolaria 这个软件彻底从地球上消失，我们的知识库依然完好无损。你可以用系统自带的文本编辑器打开它，我们的数据永远只属于我们自己。

这是 Obsidian 的核心理念之一，Tolaria 也是这一理念的继承者。这意味着 Obsidian 和 Tolaria 之间几乎没有太大隔阂，迁移和共存的成本都比较低，用户的选择空间和安全感也都得到了明显提升。

## Git 成了内置标配

大多数笔记软件都有个「回收站」，但 Tolaria 没有。它直接把整个笔记库「Vault」变成了一个 Git 仓库。每一次修改和删除，都会在底层版本控制里留下痕迹。

对于非技术人员来说，这可能是噩梦，太极客了。但熟悉这种设定的用户，会获得一种前所未有的安全感：永远可以回滚到某个历史版本，再也不用担心误删或者改废了一篇长文。

看到那些 Diff 视图，我估计有人会感动到要哭。其实 Obsidian 也是可以集成 Git 插件的，只不过，在 Tolaria 里，Git 是内置标配。

![[01_raw/_inbox/文章/images/0610209fe15b297acc5051f252a01283_MD5.png]]

  

## 引入了 Type 和视图

如果说上面两点只是技术选型上的偏好，那么 Tolaria 对「分类与标签」的处理，则展现了相当不错的产品判断。

用过 Notion 的人都知道，它的核心是 Schema「模式」。要建一个表格，往往需要先定义字段：这个是文本，那个是日期，另一个是单选框。这种「结构先行」的设计，导致很多人在记笔记前，要先花半小时搭框架。

Tolaria 提出了一个截然相反的理念：Types as lenses「类型作为透镜，而不是强制结构」。

在 Tolaria 里，你可以给笔记打上各种「类型」，比如 Project、Topic、Journal，并为它们设置不同的颜色和图标。但重点是：这些类型并不会强制你填写某些字段，也不会进行严格的字段验证。

它们只是帮助你在这个庞大的文本库里导航的「视觉提示」。你想填属性就填，不想填就空着；你想给这篇随笔标个红色的灵感图标就标，不想标，它就是一个普通的文档。

当我们需要汇总或查询特定类型、特定条件的文档时，可以创建一个筛选或查询视图，并保存下来供以后复用。

这种理念在其他笔记工具里也有体现。比如 Obsidian 其实也可以通过笔记关联、标签和查询视图达到类似效果，我也一直是这样做的。Tolaria 只是把它显式地表现了出来，并作为内置标配。

## 更独立的 AI 集成方式

过去一两年，几乎所有的笔记软件都在疯狂加 AI 功能：右键帮你总结、帮你润色、帮你扩写。

多数厂商出于商业目的，都希望用户使用 PKM 工具内置的 AI，并把它作为订阅收费的一部分。这其实和提供云存储一样，属于锁定基础设施并收费。各类云笔记几乎都是这样做的，这是重要的收入来源。

Obsidian 显然不会走这条路，所以它更像是在摸索一种独立于 App 自身的 AI 集成方式。用户可以选择与 Claude、ChatGPT 或其他 AI 客户端结合使用，Obsidian 只提供接口。这和 Obsidian 的一贯理念是吻合的。

Tolaria 本质上还是 Obsidian 的精神继承者，保留了用户对 AI 的独立选择。只要用户装过 Codex 或 Claude Code，就可以一键连接，开箱即用。至少在这一点上，它似乎走在了 Obsidian 前面。

Tolaria 内置了一个完整的 MCP「Model Context Protocol」服务器。通过 MCP，AI 可以直接读取整个笔记库，理解目录结构，甚至直接在里面新建文件、修改内容。

我们可以对 AI 说：「把过去一周我写的关于『管理学』的散碎笔记，整理成一篇结构化的长文，并更新到我的主页目录里。」

Tolaria 不做自己的封闭 AI，而是把自己变成了一个对所有外部 AI 极度友好的「容器」。这种 AI-first 但不 AI-only 的策略，也就是优先拥抱 AI，但不把用户锁死在某个 AI 服务里，确实聪明。

无论未来是 OpenAI 还是 Anthropic 出了更强的模型，Tolaria 的用户都可以持续接入更前沿的 AI 能力，而不必被绑定在某个软件的订阅费上。

![[01_raw/_inbox/文章/images/8c9076485ee005b544b0b2eb2e9c17fa_MD5.png]]

  

# 最后

我已经简单试用了一会儿 Tolaria，但这个产品还很新，更新也很频繁。我建议大家先不要冲动迁移整个知识库，观察一段时间后，再做结论。原因如下：

1.  目前还存在不少小 bug，我都忍不住想提交修改了。
    
2.  AI 集成还需要更稳固的支持。这已经不是单纯挂一个 MCP 就能解决的问题，还需要更多真实使用场景的打磨。
    
3.  目前支持 Mac（好像也支持 Linux，但我还没试过）；不过现在竟然还没有 Windows 版本。（这种 Tauri 项目居然还要挑挑拣拣……）
    

总体来说，Tolaria 潜力很高，作者一看就是懂行的人，非常清楚现有笔记产品的优劣点。

问题是，Tolaria 还太新，缺少时间积累，也没有插件生态支持。它看起来很像 AI Coding 或 Vibe Coding 加速下的产物，后续维护和修整仍有待考验。

但它的开源特性，又让这些问题有了被解决的可能。只要人气足够高，就可能有贡献者持续维护下去。再加上 AI Coding 的发展，这些问题也许并没有过去那么难解决。

所以，它现在最缺的，其实就是时间。

有兴趣的小伙伴可以立刻去试试看。不用注册账号，也不会让你月付、年付去订阅什么 AI 套餐。（AI 工具得自备，也就是 BYO。）

再强调一遍，Tolaria 不是一款 AI 套壳骗订阅的闪亮新鲜产品，它更像是 Obsidian 精神上的继承者。

Tolaria 官网地址

https://tolaria.md/

![[01_raw/_inbox/文章/images/9806ffab6c14c182069ad9d932aa03dd_MD5.png]]

  

---

![[01_raw/_inbox/文章/images/ffe026322641e5b638bdf7227102140b_MD5.jpg|cover_image]]

Original 火箭君 效率火箭

---

内容效果不满意？[点此反馈](https://feedback.notebooksyncer.com/feedback/64c588a8_1780005818208?u=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzI2MjEyODE4OA%3D%3D%26mid%3D2650484126%26idx%3D1%26sn%3D2c822d264be0f0770197f510e8a9ed3d%26chksm%3Df3c6c5ac5221b90446ff961fb3113ca95c6effd629262946a4f2fec2d4fca07ebb80acf55149%26mpshare%3D1%26scene%3D1%26srcid%3D0502lsmWtknosW3p7GtJMPdR%26sharer_shareinfo%3D0ab2d16bb62e202f4c20785348d12c35%26sharer_shareinfo_first%3Db701807364c0dbae5b8b02070000d8bf%23rd&s=obsidian)