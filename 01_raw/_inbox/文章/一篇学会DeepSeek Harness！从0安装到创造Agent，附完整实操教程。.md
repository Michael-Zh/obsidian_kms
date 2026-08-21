---
author: 水哥哥
source: 微信公众号
url: https://mp.weixin.qq.com/s?__biz=MzUzOTAzMDA2MQ==&mid=2247494858&idx=1&sn=eb9e229723517bb2e69b1250f008c53f&chksm=fb70b8c77fa42dad58f3324de8f0c79c694488f8515d0b16d1f28da813e5d19935816d210115&mpshare=1&scene=1&srcid=0816PS620qN82FRbn0ul75pc&sharer_shareinfo=39dd9e15dd8e4362838c9ea42b8db523&sharer_shareinfo_first=39dd9e15dd8e4362838c9ea42b8db523#rd
saved: 2026-08-16 12:26:47
tags:
  - 笔记同步助手
annotation:
id: 5b99896e-0fdd-4dea-8f6d-fb065c6fb31f
---

公众号名称：水哥AIGC

作者名称：水哥哥

发布时间：2026-08-14 13:38

## 

关注**▲水哥AIGC****▲** 探索AI时代的一人公司活法

  

![[01_raw/_inbox/文章/images/002e83809efbcf726718dbbd90e1c2d1_MD5.png]]

这是水哥的第 **174** 期分享

你好，我是水哥。

DeepSeek这两天又整了个新东西。

预告了一段时间的**DeepSeek Harness**，终于正式开放了。

![[01_raw/_inbox/文章/images/245c107de0138fd4cc44661d4600bf62_MD5.png]]

是的，国产之光Deepseek终于也有了自家的Agent产品。

不过这玩意刚出来的时候，我估计很多朋友跟我一样，多少有点疑问，其它家的Agent产品不是work、就是code。

Deepseek的Agent为啥带个Harness？Harness到底是个啥？

**而且真准备上手以后，问题会更多。比如怎么安装？标准、PTC、极简、创造这4种模式到底选哪个？**

官方一直在喊的Everything is a Plugin，一切皆插件，到底有什么用？

所以今天早上我直接拿Mac和Windows各装了一遍，又连续跑了3轮完整实测。

第一轮，我让DeepSeek Harness从0做了一个可以交互的「Agent组装实验室」。

![[01_raw/_inbox/文章/images/e8d6d38a06fd97c5130558417fa45ede_MD5.jpg]]

> 📹 此处为视频内容（vid: wxv\_4648682856146534405）（上图为封面），未能直接提取，请前往原文查看：[在公众号原文中观看](https://mp.weixin.qq.com/s?__biz=MzUzOTAzMDA2MQ==&mid=2247494858&idx=1&sn=eb9e229723517bb2e69b1250f008c53f&chksm=fb70b8c77fa42dad58f3324de8f0c79c694488f8515d0b16d1f28da813e5d19935816d210115&mpshare=1&scene=1&srcid=0816PS620qN82FRbn0ul75pc&sharer_shareinfo=39dd9e15dd8e4362838c9ea42b8db523&sharer_shareinfo_first=39dd9e15dd8e4362838c9ea42b8db523#rd)

第二轮，我切到创造模式，让它**给自己新造了一个独属于我的「网页换肤模式」**。

![[01_raw/_inbox/文章/images/b135f3825a760181b117b7ec0839df1c_MD5.png]]

第三轮，我再用这个刚造出来的新Agent，回过头把前面的网页从现代科技风，直接改成了复古像素街机风。

![[01_raw/_inbox/文章/images/330f96c8a048df2394d220705f6ec8f3_MD5.jpg]]

> 📹 此处为视频内容（vid: wxv\_4648687862467362820）（上图为封面），未能直接提取，请前往原文查看：[在公众号原文中观看](https://mp.weixin.qq.com/s?__biz=MzUzOTAzMDA2MQ==&mid=2247494858&idx=1&sn=eb9e229723517bb2e69b1250f008c53f&chksm=fb70b8c77fa42dad58f3324de8f0c79c694488f8515d0b16d1f28da813e5d19935816d210115&mpshare=1&scene=1&srcid=0816PS620qN82FRbn0ul75pc&sharer_shareinfo=39dd9e15dd8e4362838c9ea42b8db523&sharer_shareinfo_first=39dd9e15dd8e4362838c9ea42b8db523#rd)

三轮全跑完，API累计花了1.92元。

![[01_raw/_inbox/文章/images/308654262d57317fb5f5a93f73099e18_MD5.png]]

所以这篇咱们不聊虚的。

就从0开始，把DeepSeek Harness怎么安装、界面怎么看、4种模式怎么选、标准模式怎么干活，以及最特别的“创造Agent”，全部给完整跑一遍。

如果你最近也准备折腾DeepSeek Harness，这篇建议先收藏。

  

#### 

02

DeepSeek Harness怎么安装？

先从0把它跑起来

正式开始之前，有一个词还是得先简单解释一下。

  

其实今年4月份，我就[**专门写过一篇Harness Engineering。**](https://mp.weixin.qq.com/s?__biz=MzUzOTAzMDA2MQ==&mid=2247491669&idx=1&sn=a45a21a6041e033d09ef53eb0b3d6d08&scene=21#wechat_redirect)

当时里面讲过一个很经典的公式，就是Agent = Model + Harness。

![[01_raw/_inbox/文章/images/5ea1bad2b7726192297e0366e003fa4d_MD5.png]]

大白话理解的话，如果把一个Agent比成一辆汽车。

那Model，也就是大模型，像发动机。它决定这辆车动力强不强、脑子聪不聪明。

但你光有发动机，是开不起来的。

你还得有方向盘、底盘、轮胎、刹车、导航、仪表盘。

放到Agent里面，对应的就是文件读写、Shell、联网搜索、Skill、记忆、上下文管理、任务规划、沙箱、子Agent、工作流等等。

把这些东西组织起来，让模型真的可以在电脑和真实任务环境里持续干活的这一整套系统，就是Harness。

所以简单记住一句就够了，Model决定Agent聪不聪明。Harness决定它怎么把这份聪明真正用起来。

这次DeepSeek更狠。他们直接把Harness本身做成了产品。

![[01_raw/_inbox/文章/images/e00dbee15013612124095261c99c9ebb_MD5.png]]

而且核心理念就一句Everything is a Plugin，也就是一切皆插件。

这个咱们后面实测的时候再详细讲。

**先把它装起来。**

目前DeepSeek Harness还是开发者预览版。所以没有我们平时熟悉的Windows、Mac桌面客户端。

它更像是一个跑在自己电脑上的Web应用。

官方快速启动命令是npx @deepseek-ai/dsh web

前提是你的电脑已经安装了Node.js。

![[01_raw/_inbox/文章/images/21e9cc13acdb6be2dde7896c503d276c_MD5.png]]

当然，现在都2026年了。

让我自己从头配环境，多少有点懒，所以我先把我的Mac用Workbuddy安装下。

直接把DeepSeek Harness项目地址丢给它，让它安装就行。下面是具体的提示词，需要的朋友可以直接复制发给你的任意Agent工具。

  

> 帮我在电脑上安装并启动DeepSeek Harness。
> 
> 项目地址：https://github.com/deepseek-ai/deepseek-harness
> 
> 你先看官方项目说明，然后检查我电脑现在的环境，缺什么依赖就帮我装什么，尽量按照官方推荐的方法安装。
> 
> 安装过程中如果遇到报错，你自己排查解决。
> 
> 最后帮我把DeepSeek Harness启动起来，能正常打开使用就行。

  

![[01_raw/_inbox/文章/images/3025c88e16b8b7fd9b85192ac9870bcf_MD5.png]]

然后它自己检查环境、安装依赖、启动服务，基本不用我管。就能安装好，会直接帮我们打开一个3080端口的网址，直接就能用。

![[01_raw/_inbox/文章/images/2f2f680d4145bc535ddbb0404336986c_MD5.png]]

现在已经开始流行让一个Agent帮你安装另一个Agent了嘿嘿嘿。

不过这里也踩了一个坑。刚装好的时候网页还能正常打开，我出去转了一圈回来。

没了。。。

后来重新启动`dsh web`才恢复。

所以如果大家也是让WorkBuddy这类Agent帮忙安装，最好顺手让它把以后怎么独立启动Harness也告诉你。

![[01_raw/_inbox/文章/images/96fda30c07d2ae8c37f0c6e7999e01d4_MD5.png]]

不然Agent把Agent接生出来以后，自己下班了。。。

Windows这边，我也尝试自己手动装了一遍。想手动试试的朋友也可以看看，很简单。

先打开Windows的PowerShell终端，输入node --version，看看有没有安装Node.js，出现版本号就是安装了。

![[01_raw/_inbox/文章/images/32d1d7674597af02a098635ba02f3cf0_MD5.png]]

然后再输入DeepSeek Harness给的安装命令npx @deepseek-ai/dsh web

结果PowerShell直接给我一片红。提示因为在此系统上禁止运行脚本。

![[01_raw/_inbox/文章/images/9824b69d6f885d52c3c8b0965411a77c_MD5.png]]

好家伙。

果然Windows安装开发者工具，多少还是得给你来点经典节目。这个问题其实不是Harness本身。而是PowerShell把`npx.ps1`拦住了。

解决也很简单。换成npx.cmd @deepseek-ai/dsh web

第一次运行会提示是否安装。

输入y，然后回车继续。最后如果看到dsh web: http://127.0.0.1:3080

![[01_raw/_inbox/文章/images/a7872bc9c81de2d8f86211e67a3a2fd1_MD5.png]]

就说明成功了，只需要在浏览器打开这个网址就行了。

或者直接按住Ctrl点按一下这个网址，就能直接帮我们在浏览器直接打开。

第一次会先看到开发者预览版提示。

![[01_raw/_inbox/文章/images/319cb8efb581c2242ad93db1d176b0cb_MD5.png]]

继续之后，再填一下自己的 DeepSeek API Key。

![[01_raw/_inbox/文章/images/6f1be28673d38dcf5def723604607ee7_MD5.png]]

如果还没有API Key，需要自己去DeepSeek的开放平台获取一个。

比如我这里就在开放平台上面创建了一个新的叫做DeepSeek Harness的API Key。

![[01_raw/_inbox/文章/images/ab43e5a7dee0bc96467004aaacf8d6e2_MD5.png]]

创建好之后，直接把API Key复制下来就行，切记这个Key不要发给别人哈。

![[01_raw/_inbox/文章/images/fabbba7d5b3867ec6a458186942fe241_MD5.png]]

**先花30秒认识一下界面。**

正式进入DeepSeek Harness以后，界面其实没有想象中那么复杂。

左边主要是工作区+对话列表。中间可以选择工作区、Agent 模式、权限、模型和推理等级。

![[01_raw/_inbox/文章/images/fecf03a0e6c793934f520cce3cd10641_MD5.png]]

这里的工作区，小白可以简单理解成让Agent干活的文件夹。

比如我准备让它做一个网页。就在电脑里新建一个文件夹，再把这个文件夹选成工作区。

后面生成的HTML、CSS、JS等文件，都会放进去。

**4种模式到底怎么选？**

DeepSeek Harness现在还内置了四种Agent预设，分别是标准模式、PTC 模式、极简模式、创造模式。

![[01_raw/_inbox/文章/images/5f34b9c5d28c685ba87ef31a02cb42d4_MD5.png]]

普通用户第一次用，其实不用研究太多。

标准模式最常用。文件编辑、Shell、网页搜索、Skill、计划、目标、子代理、工作流这些能力基本都有。

平时写代码、做网页、改文件，直接用它。

PTC模式的PTC可以理解成让模型把一大串工具操作编成一段程序，再一次性执行。

比较适合步骤很多、工具调用频繁的复杂任务。小白前期没必要碰。

极简模式故意把大量能力拿掉，只保留很基础的Shell和文件编辑能力。

更适合测试模型本身裸Agent能力到底怎么样，日常干活不推荐。

创造模式最特别了，它拥有标准模式的能力。同时还能检查自己正在运行的Cordis环境、实验插件、创建新的Agent预设。

翻译成人话的话就是Agent不仅可以干活，还可以给自己重新组装一套新的干活方式。

这个我们后面重点测。

另外还有一个权限设置，跟大多数Agent一样，通常默认就行。

![[01_raw/_inbox/文章/images/efb2255296b49ead0adf521f8a3f9366_MD5.png]]

如果觉得需要自己反复审核太麻烦，可以选择Full access。

![[01_raw/_inbox/文章/images/d2610a81016f956632f4d769f2643889_MD5.png]]

开启以后，Harness 会减少很多确认步骤，可以直接执行更多文件修改、外部命令和敏感操作。

功能很爽，风险也更高。

如果只是刚开始体验，我不建议啥都不看直接开满。特别是工作区里面有重要文件时，还是悠着点好。

另外上面也是支持模型选择的。

甚至可以选择推理强度，有三个挡位可以选择。

![[01_raw/_inbox/文章/images/6ed48572bff0928c7b84fe3ae5fc406b_MD5.gif]]

当然，也是支持自定义添加其他产商模型的。

![[01_raw/_inbox/文章/images/57b804547c60d736d84b2a92c9b1d05d_MD5.png]]

  

#### 

02

我让DeepSeek Harness

做了一个解释自己的实验室网页

界面差不多认识以后，咱们开始第一轮正式实测。

既然这篇文章本身就在讲Harness。那干脆让DeepSeek Harness自己解释下自己。

所以我新建了一个叫做Agent组装实验室的工作区。

![[01_raw/_inbox/文章/images/2f66f435a90eb44744410d18c6dfb3a0_MD5.png]]

然后给它一个需求。

大致意思就是让它帮我做一个可以交互的「Agent组装实验室」网页，用来给普通人解释Agent = Model + Harness。

把Agent比成一辆汽车。Model像发动机，Harness是让发动机真正跑起来的一整套系统。

同时还要表现普通Agent和DeepSeek Harness的区别。普通Agent像一辆已经组装好的汽车。DeepSeek Harness更像一个乐高式汽车平台。

Model、Tool、Skill、Memory、Context、Agent Loop、UI等能力都可以像组件一样自由安装、替换和组合。

最后自然引出Everything is a Plugin。网页不要只展示文字，要真的可以玩。

![[01_raw/_inbox/文章/images/13431bd8f22aa8c5ac320bd1f3d6749c_MD5.png]]

发出去后。

它没有直接开始狂写代码，而是先给自己拆出了**8个任务**。

![[01_raw/_inbox/文章/images/91f04cc657c32c3dc274a17096276344_MD5.png]]

包括页面骨架、Hero区、Model / Harness / Agent三大件、Harness内部组件。

普通Agent和DeepSeek Harness对比、Agent组装实验室、Everything is a Plugin。

以及后续检查，然后开始一个个往下干。

比如它自己发现SVG里面有一处拼写错误，没有等我提醒，直接自己搜索、定位、修改。

![[01_raw/_inbox/文章/images/b7a34415d3ba6365ba2b518081750d49_MD5.png]]

改完后继续自查。

这就是现在Agent和普通聊天 AI 最大的区别之一。

聊天AI很多时候是回答完就结束。Agent则更像先做 → 检查 → 出问题 → 返工 → 再检查。

后面它甚至觉得光看代码还不保险。

准备自己调用Chrome，把刚生成的网页真实渲染出来，然后截图检查视觉效果。

结果这一步被Harness的沙箱拦了下来。它需要启动Chrome的一些进程通信。

当前权限不够。于是Harness弹出等待审批弹窗，问我要不要临时提升权限。

![[01_raw/_inbox/文章/images/4adeae1686662d245824a5ad1449134b_MD5.png]]

这个过程其实我感觉就能很好的帮我们理解Agent为什么需要Harness了。

因为模型只负责我想打开Chrome验收网页。

真正怎么调用Chrome、有没有权限、命令能不能执行、沙箱允不允许、碰到风险要不要让人确认等待，这些全是Harness在处理。

最后这一轮一共跑了大概18分钟吧，共33步。

Harness里还能看到LLM 时间、工具调用时间、缓存命中率等数据。

![[01_raw/_inbox/文章/images/13d1b707b52be80d5dd73562896631e5_MD5.png]]

最终它还自己做了一轮交互测试，然后把完整网页交给我。

![[01_raw/_inbox/文章/images/e8d6d38a06fd97c5130558417fa45ede_MD5.jpg]]

> 📹 此处为视频内容（vid: wxv\_4648682856146534405）（上图为封面），未能直接提取，请前往原文查看：[在公众号原文中观看](https://mp.weixin.qq.com/s?__biz=MzUzOTAzMDA2MQ==&mid=2247494858&idx=1&sn=eb9e229723517bb2e69b1250f008c53f&chksm=fb70b8c77fa42dad58f3324de8f0c79c694488f8515d0b16d1f28da813e5d19935816d210115&mpshare=1&scene=1&srcid=0816PS620qN82FRbn0ul75pc&sharer_shareinfo=39dd9e15dd8e4362838c9ea42b8db523&sharer_shareinfo_first=39dd9e15dd8e4362838c9ea42b8db523#rd)

成品已经不只是一个静态页面了。

里面可以从Agent = Model + Harness，一路往下看，Model是什么，Harness是什么，两者组合以后为什么才是完整Agent。

还可以切换不同组件，进入组装实验室，根据不同任务选择能力。

最后落到Everything is a Plugin.

这个网页本身，后面我甚至可以直接拿来给大家解释Harness。

这轮我用了DeepSeek V4 Pro + High + 标准模式。

API后台看了一下。大概跑了221万Tokens，34 次API请求。

然后一看费用0.57元。

![[01_raw/_inbox/文章/images/6134a763bdb9e7c1a91a54c7a8d26831_MD5.png]]

221万Token看着挺夸张，最后五毛七，还是挺便宜的。

这里还有一个功能我觉得值得单独说一下，就是对话旁边的轨迹。

![[01_raw/_inbox/文章/images/207dee434feb078cca720797b77cc62c_MD5.png]]

平时我们在对话界面看到的，是Agent整理过后的过程。

但打开轨迹。你能看到模型什么时候思考，什么时候调用Tool，什么时候改文件，什么时候搜索，哪个步骤耗时多久。

上面甚至还有Model、Tools等调用时间分布。

右上角还可以导出Session log。

Agent以后一次任务跑半小时、一个小时甚至更长。那这种轨迹功能会越来越重要。

不然Agent在后台狂干几十分钟，最后做烂了，你都不知道它到底从哪一步开始抽风的。

做到这里的时候，我对DeepSeek Harness的体感确实还不错，干起活来还是挺能干的。

但是，如果仅仅是这样，好像跟Codex、WorkBuddy没啥太大区别，这种活儿基本上所有Agent都能干。

更有意思的是它的创造模式。

  

#### 

03

创造模式怎么用？

我让Harness给自己造了一个新Agent

DeepSeek推出的创造模式，据他们自己的解释就是DeepSeek Harness底层建立在一个叫**Cordis**的系统上。

这个词看起来又很工程师。小白可以把Cordis理解成一块乐高底板。

![[01_raw/_inbox/文章/images/dc567dcb4be1c318afd4a22972bd229a_MD5.png]]

它自己并不负责写代码、搜索网页、管理记忆、做UI等等工作。

它主要负责把各种插件装上去、卸下来，并管理这些插件之间怎么协作。

所以你可以在这块底板上插Model、Tool、Skill、Storage、Sandbox、UI、Agent Loop。

然后组合出不同Agent。

这也是为什么DeepSeek Harness一直强调Everything is a Plugin的原因。

看着真挺牛逼的，所以我立马就实测了一下。

我立马创建了一个新的工作区，然后选择了创造模式。

然后跟他说帮我创建一个新的Agent预设，名字就叫「网页换肤模式」。

这个模式专门用来给已有网页更换视觉风格。

以后我只需要告诉它想换成什么风格，它就先读取现有网页，在尽量不改变原有文字内容、页面结构和交互功能的情况下，重新设计配色、字体、背景、按钮、卡片、动效等视觉效果。

修改完成后还要自己检查页面能不能正常运行。

![[01_raw/_inbox/文章/images/2e452d8fa23ee5207773aa4db78fea82_MD5.png]]

这里顺便解释一下Agent预设又是什么？

你可以把它理解成一套提前组装好的Agent工作方式。

比如标准模式。里面已经提前给你装好了文件编辑、Shell、搜索、Skill、计划、工作流等等。

创造模式做的事情，就是帮你再组一套属于自己的模式。

发出去以后。

它先给自己列了**6个任务**。然后开始注册一个临时的Cordis Plugin。

中间第一次运行的时候还报错了。

![[01_raw/_inbox/文章/images/d93db666cf41dbc89f0c5663766034da_MD5.png]]

看到红字的时候我还以为要G了。

结果它自己读了报错信息，改了参数，然后重新注册插件继续跑。

我全程没有帮它调试。后面它继续完成复制标准模式、写`preset.yml、`修改`agent.cordis.yml、`挂载校验。

最后再把临时插件清理掉。然后告诉我新的预设已经搞定了。

![[01_raw/_inbox/文章/images/f76d00d591d88228a90b63ec63f33133_MD5.png]]

我去看了下，Agent预设确实有了这个自定义的模式，而且电脑本地，还真的多了一个文件夹。

![[01_raw/_inbox/文章/images/841ea5ba3d9cae1a75fe1a7e255f5bc5_MD5.png]]

这里就能看出来了。

所谓创造一个Agent预设，并不是在聊天框里让它记住你现在是网页换肤专家就完了。

它是真正在Harness的配置目录里面新建了一套Agent配置。

更关键的是，在对话框内打开模式下拉菜单。原本只有标准模式、PTC模式、极简模式、创造模式的。

现在下面真的多出来了一个网页换肤模式。

![[01_raw/_inbox/文章/images/b135f3825a760181b117b7ec0839df1c_MD5.png]]

我看了下，它是基于标准模式复制了一整套能力。

文件编辑、Shell、搜索、Skill、计划、目标、子代理这些都还在。

但是它把Agent的行为规则改成了先理解，再动手。

只改视觉层、统一风格体系。修改后自查，发现问题继续修。

![[01_raw/_inbox/文章/images/6772a8d432485c2f9962335ffefa928a_MD5.png]]

这就相当于保留标准Agent的四肢和工具。再重新给它换了一套岗位+工作方法。

而创建这个新模式，也不是瞬间完成的。从API后台看，前一轮结束以后累计是0.57元，创造模式跑完以后变成1.13元。

也就是说真正给自己造出这么一个新Agent，大概又花了0.56元。

那问题就来了。它到底只是创建成功，看起来很酷。还是真的能用？

我决定再跑一轮。

  

#### 

04

自定义Agent怎么用？

一句话给整个网站换了一套皮

我把上一轮做好的Agent组装实验室复制了一份，作为换肤测试项目。

  

然后新建一个会话。

工作区选择Agent组装实验室-换肤测试。

模式这次不选标准，而是选择刚才Harness自己创造出来的网页换肤模式。

![[01_raw/_inbox/文章/images/f25ea0a5a1736fccd3b731111852b855_MD5.png]]

提示词就更简单了，只是简单的一句话。

<u>把这个网站整体改成复古像素街机游戏风格。原来的内容和功能都保留，其他你自己发挥。</u>

我这里特意没有再告诉它先读项目、别乱改结构、最后做检查。

这些规则，前面创建网页换肤模式的时候已经写进去了。

现在正好验证这个新Agent到底是不是真的生效。

结果它一上来就说我先了解现有项目的技术栈和结构，再决定如何换肤。

![[01_raw/_inbox/文章/images/be72f372920e0699fa8b5ac067e1c9e0_MD5.png]]

然后开始读整个项目。

它识别出原来的网页是一套工业暗色 + 电路霓虹的设计风格。

同时明确告诉我原来的拖拽装配、任务模拟、换发动机、插件添加、粒子背景、加载动画、滚动显现等逻辑全部保留，只重做视觉层。

看到这里。基本已经可以确定前面创造模式写进去的工作规则，真的影响了这个新Agent后面的行为。

接下来它自己规划了5项换肤任务。

开始重新做像素字体、8-bit霓虹调色板、CRT扫描线、街机顶栏、像素边框、街机按钮。

甚至连原来的SVG汽车，也重新做成了像素风。

![[01_raw/_inbox/文章/images/30082e3d4037ad910042d857a2adafe3_MD5.png]]

二十多分钟以后，它就搞定了。

左边的是原来的网页，右边的是换肤后的网页效果。

![[01_raw/_inbox/文章/images/aefe307aeac7b0b37ce18784e082b87b_MD5.png]]

可以看下整体的效果。

![[01_raw/_inbox/文章/images/330f96c8a048df2394d220705f6ec8f3_MD5.jpg]]

> 📹 此处为视频内容（vid: wxv\_4648687862467362820）（上图为封面），未能直接提取，请前往原文查看：[在公众号原文中观看](https://mp.weixin.qq.com/s?__biz=MzUzOTAzMDA2MQ==&mid=2247494858&idx=1&sn=eb9e229723517bb2e69b1250f008c53f&chksm=fb70b8c77fa42dad58f3324de8f0c79c694488f8515d0b16d1f28da813e5d19935816d210115&mpshare=1&scene=1&srcid=0816PS620qN82FRbn0ul75pc&sharer_shareinfo=39dd9e15dd8e4362838c9ea42b8db523&sharer_shareinfo_first=39dd9e15dd8e4362838c9ea42b8db523#rd)

**皮换了，功能没丢。**

证明前面创造出来的网页换肤模式，不是摆在模式列表里看着玩的。是真的可以跨项目重新调用，然后继续干活。

这次换肤完成以后。API总消费从1.13元变成1.92元。也就是说这一轮大概又花了0.79元。

三轮实测全部跑完，标准模式做Agent组装实验室、创造模式造网页换肤Agent、再调用网页换肤Agent改造原网站。

累计花费1.92元，虽然DeepSeek涨价了一波，但是这个价格，我觉得依旧配得上价格屠夫这个称号。

写在最后。

DeepSeek Harness现在可能还不是最好用的Agent，但应该是目前最敢把Agent拆开给你玩的产品之一了。

如果你只是想让AI帮你写代码、查资料、干点日常工作，WorkBuddy、Codex这些成熟工具明显更省心。

但如果你想自己决定一个Agent应该有什么能力、怎么干活，甚至让它缺什么就现场给自己造什么。

那DeepSeek Harness就很有意思了。

四个月前我还在文章里解释Agent = Model + Harness。

四个月后的今天，我已经可以让Harness给自己造出一个新的Agent，然后再拿这个Agent继续干活了。

这事儿，确实挺有想象空间的。

至于这块“Agent 乐高底板”最后能被大家搭成什么样。

**我觉得游戏才刚刚开始。**

  

#### 

以上，有启发，请帮忙点个赞、小爱心和分享～

感谢！

  

####   

**END**

  

**看完记得关注@水哥AIGC**

**及时收看更多好文**

**↓↓↓**

  

---

内容效果不满意？[点此反馈](https://feedback.notebooksyncer.com/feedback/1139713c_1786876000587?u=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzUzOTAzMDA2MQ%3D%3D%26mid%3D2247494858%26idx%3D1%26sn%3Deb9e229723517bb2e69b1250f008c53f%26chksm%3Dfb70b8c77fa42dad58f3324de8f0c79c694488f8515d0b16d1f28da813e5d19935816d210115%26mpshare%3D1%26scene%3D1%26srcid%3D0816PS620qN82FRbn0ul75pc%26sharer_shareinfo%3D39dd9e15dd8e4362838c9ea42b8db523%26sharer_shareinfo_first%3D39dd9e15dd8e4362838c9ea42b8db523%23rd&s=obsidian)