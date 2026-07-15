---
author: 发现明日产品的
source: 微信公众号
url: https://mp.weixin.qq.com/s?__biz=MjgzMTAwODI0MA==&mid=2652455487&idx=1&sn=80aa707894fab75ff560893a147eb44f&chksm=9a482e3cf9b20e2a267594716dee9d7cb1e8ec9fb92e5831cf0e5859207020649709afb8a080&mpshare=1&scene=1&srcid=0621T53dftARrmwx8CSKjXM7&sharer_shareinfo=3d5a1bbff8ddab5cf91c8deaa04853e1&sharer_shareinfo_first=3d5a1bbff8ddab5cf91c8deaa04853e1#rd
saved: 2026-06-20 22:50:00
tags:
  - 笔记同步助手
annotation: Codex ne function
id: 23691824-7239-41de-ad59-6073e4468153
---

公众号名称：爱范儿

作者名称：发现明日产品的

发布时间：2026-06-20 11:30

![[01_raw/_inbox/文章/images/4cd781974ed163d801d16dd6c9b378f5_MD5.gif]]

你坐在电脑前干活，旁边有个家伙一声不吭盯着你。你点哪它看哪，你填什么它记什么，等你做完，它说一句：下次这活我来。

这就是 Codex 近期发布的重磅功能，叫 Record & Replay。

![[01_raw/_inbox/文章/images/f8d3d244d59ab9c4e3533174fcc97cc0_MD5.png]]

翻译过来就是录制加复现。

你把一套操作完整演示一遍，Codex 在旁边观察学习，然后把整套流程打包成一个 skill（技能）。下回要干同样的活，新开个对话，让它调这个 skill，再告诉它这次哪里不一样，剩下的它自己搞定。

图形界面，这个原本为了让人类摆脱命令行而发明的伟大创造，现在有望成了 AI 接管电脑的现成基础设施。

「学徒」模式上线，Codex 开始复制你的工作流

当然，不是所有任务都适合这么玩。

Record & Replay 瞄准的是那种重复、看个人偏好、说不清楚但做一遍你就懂的活。适用场景有这么几个：报销、订停车位、建一个配置正确的 issue、发视频、拉周期性报表。

这些活有个共同点。要么步骤又固定又繁琐，要么里头藏着一堆只有你自己知道的隐性规则。

比如文件该怎么命名、某个字段默认填啥、到了某个岔路口该往哪走。这种东西你要用文字一条条写清楚给 AI，成本极高。不如直接做一遍，让它自己看。

![[01_raw/_inbox/文章/images/9de21c4920888dcd7b3cdc7114a115ca_MD5.png]]

操作过程也比想象中省事，主要拆成了七步。

先在 Codex 应用里打开 Plugins（插件），搜索并添加 Record & Replay 插件。

![[01_raw/_inbox/文章/images/ef8d1367bee66482c8c9f19747f1ab5b_MD5.png]]

然后它来要录制权限，你准备好了就点同意。

![[01_raw/_inbox/文章/images/5faf448b0df6d52659cb170adf9d3ff7_MD5.png]]

剩下的就是你在 Mac 上正常把活干一遍。

![[01_raw/_inbox/文章/images/64facb4f33783422f9920e285d53f9b5_MD5.png]]

这期间 Codex 全程观察，学这套操作要点哪些地方、动哪些窗口的内容。

![[01_raw/_inbox/文章/images/24db83f05f2cff2b3c63dceee3896f06_MD5.gif]]

录制会一直开着，直到你主动停止。所以记住，专心做那一个任务就行，别录着录着开始干别的。

干完从菜单栏或悬浮层停止，或者直接跟 Codex 说一声已经录完。

![[01_raw/_inbox/文章/images/cb55d3e8306267634743890a5a254028_MD5.gif]]

录完之后 Codex 会复盘一遍刚捕捉到的流程，自己起草一个 skill。这个 skill 里写得很清楚：什么时候该用这套流程、需要哪些输入、按什么步骤走、做完怎么验证结果。

你要是觉得它写得不够好，还能让它再打磨。

几条录制建议值得照做：

演示尽量短而完整；录之前先把目标和那些每次会变的输入告诉 Codex；用真实输入，但密码和敏感数据千万别录进去；录完后补上那些重要的隐性偏好，比如命名规范、字段默认值、决策点怎么选；流程做完就停，别拖到无关的收尾动作上。

至于，下次复现就简单了。新开对话，让它调这个 skill，把这次的具体值喂给它，比如要传哪个文件、建哪个 issue、报表要哪段时间。

![[01_raw/_inbox/文章/images/a5dedd5209c9b8a845434a84aff7d606_MD5.gif]]

有个关键设定需要注意：Codex 会把这个 skill 当作可复用的上下文（reusable context）。

什么意思呢？这个 skill 不是一段写死的脚本，而是一份它每次都能拿来参考、再结合当前环境灵活执行的说明书。所以同一个 skill，这次传 A 文件、下次传 B 文件，它都能套着用。

具体干活的时候，它会调动当前环境里能用的工具，包括 Computer Use、浏览器操作和已安装的插件，把流程跑完。

Codex 到底怎么「用电脑」

来看一次公开演示。

这回 Codex 要学的是上传 YouTube 视频的完整流程。它的工作方式是盯着用户在 YouTube Studio 里操作，把点击、选文件、敲文字这一整串动作全捕捉下来。

诸如选视频文件、填标题和描述、传缩略图、加字幕、设隐私选项等等，Codex 全记下来了，随后展示了独立复现的能力。

![[01_raw/_inbox/文章/images/d092295a87ebbf920ac7190e4f52467d_MD5.jpg]]

> 📹 此处为视频内容（vid: wxv\_4567396790886301697）（上图为封面），未能直接提取，请前往原文查看：[在公众号原文中观看](https://mp.weixin.qq.com/s?__biz=MjgzMTAwODI0MA==&mid=2652455487&idx=1&sn=80aa707894fab75ff560893a147eb44f&chksm=9a482e3cf9b20e2a267594716dee9d7cb1e8ec9fb92e5831cf0e5859207020649709afb8a080&mpshare=1&scene=1&srcid=0621T53dftARrmwx8CSKjXM7&sharer_shareinfo=3d5a1bbff8ddab5cf91c8deaa04853e1&sharer_shareinfo_first=3d5a1bbff8ddab5cf91c8deaa04853e1#rd)

更有意思的是，它不只是机械地照着步骤复读，还试图搞懂背后的逻辑和门道。

比如什么时候该把视频设成 Private、什么时候设 Unlisted，怎么管 .mp4 视频文件和 .srt 字幕文件这种成对的东西，元数据字段该怎么填，字幕怎么跟视频对上号。

它甚至现场处理了一次报错：

缺 Python 环境的时候，它直接从已安装的 skill 位置读信息，自己适配过去了。而这一整段录下来，转译成一个随时能调用的 skill。

换句话说，Codex 一旦学会，理论上就能在没人盯着的情况下反复执行。对那些天天要传一堆视频的内容工作流来说，这事确实有用。

![[01_raw/_inbox/文章/images/ab61eb266fa8b8f832555881c258a002_MD5.jpg]]

要搞懂它凭什么能复现，得先看 Codex 到底怎么操作电脑。

OpenAI 工程师 Jason 之前梳理过 Codex 用电脑的三条路，能力有重叠，各有各的地盘。总原则是：能用插件或 MCP 就先用，视觉控制留给结构化工具够不着的边角。

第一种叫 Computer Use，覆盖面最广。

它能在 macOS 和 Windows 上看见并操作图形界面，通过窗口、菜单、键盘、剪贴板来动那些授权过的应用。

代价是慢，因为它得看界面、判断点哪、等响应、再确认状态，一步一回头。但好处也明显，那些没有 API 的应用它也能对付，比如 Spotify、Xcode、系统设置、iOS 模拟器，甚至能通过 iPhone 镜像去操作 iPhone。

在 macOS 上它还能后台跑，你能同时干别的。它信任边界也最宽，凡涉及钱、账户、支付、凭据的改动，建议你全程在场盯着。

这也解释了为什么 Record & Replay 只能跟着 Computer Use 一起开启。它录下来的操作要复现，靠的就是 Computer Use 这套看界面、动鼠标键盘的底层能力。

![[01_raw/_inbox/文章/images/d62da6d2d706496aa72a385bd37cc37e_MD5.png]]

第二种是 Chrome 扩展。

它接管你已经登录好的 Chrome，适合那种靠账号、cookie、已认证标签页的任务，比如 Gmail、Salesforce、内部仪表盘。它能玩多标签，把同一个任务的好几个标签页串成一个完整工作流来理解。

代价是它带着你的身份在动，网站会把它的点击和提交都当成你本人，所以发送、发布、购买这种步骤一般得先过你审核。

第三种是应用内浏览器。

它活在 Codex 对话内部，跟你共享同一个渲染页面，特别适合开发调试 Web 应用。它最大的特点是隔离，不碰你的浏览器配置、cookie、扩展和登录会话。

需要的时候这是限制，不需要的时候反而是个干净的边界。开发者能让它改代码、操作页面、截图、修完再跑一遍，形成一个紧密的反馈循环，还能直接点页面元素留设计意见。

另外还有个叫 Appshot 的机制，它不操作电脑，只负责把 Codex 的注意力指到你眼前的东西上。在 Mac 上连按两下 CMD 键，它就抓最前面那个窗口，把图像和文字附进对话。你对着一个报错、一封邮件、一个看不懂的表单直接发问就行。

用 Jason 的话说，Appshot 负责指方向，浏览器、Chrome 扩展和 Computer Use 负责动手。而 Record & Replay 录下来的 skill，正是可以随时调动上面任意一种或几种方式来复现。

![[01_raw/_inbox/文章/images/fd215aaba08394d33ca227b37f631c87_MD5.png]]

人类操作软件的经验，正在变成 AI 技能

从今年以来，Codex 的发布节奏仍在不断加速，许多人都不知道的是，Codex 应用、CLI 和 SDK 不是只能配 OpenAI 自家模型。

在 config.toml 里配一下 model\_providers，你可以把 Codex 指向 Ollama、LM Studio 这类本地开源模型，也能接 Mistral、Azure、Amazon Bedrock 这些第三方。传个 --oss 参数就能跑本地 provider，不指定的话默认走 oss\_provider。

![[01_raw/_inbox/文章/images/cfbbf69a9db194b8a371cf62a4b8a287_MD5.png]]

🔗 https://developers.openai.com/codex/config-advanced#oss\-mode-local-providers

也就是说，Record & Replay 这种能力，载体本身是个对模型开放的客户端。

它也有适用范围。Record & Replay 是从一次演示里快速造 skill 的捷径，但如果你想把一个稳定的包发给整个团队、捆绑好几个 skill、加应用集成或 MCP 服务器、管安装元数据，那就别停在录制层面，老实打包成独立插件。

还有几个上手前最好先知道的限制。

Record & Replay 目前只在 macOS 上能用，首发不覆盖欧盟、英国和瑞士，而且必须先开启 Computer Use 功能。

如果你是组织管理员，还有个坑得避开：

要是你们用 requirements.toml 统一管 Codex，那 \[features\].computer\_use 这一项是连 Record & Replay 一起管的。

![[01_raw/_inbox/文章/images/e4dd44b097ddd645cd1008d7556e47d9_MD5.png]]

🔗 https://developers.openai.com/codex/record-and-replay

哪天把 computer\_use 设成 false，你会发现这俩功能一起消失。所以要是你发现「我这儿压根看不到 Record & Replay」，先去查这一项是不是被关了。

「Record & Replay」的上线，看起来只是一个录制和复现操作的小功能，但放到更大的背景里，它代表的是 AI 与软件交互方式的一次变化。

过去，自动化的基础是 API。软件必须先开放接口，把能力封装成机器能够调用的服务，自动化工具和 AI 才能接手流程。没有 API，没有结构化入口，很多任务就无法实现自动化。

因此，传统自动化的边界，往往取决于软件愿意开放多少能力。

但现在，OpenAI 试图绕开这层限制。它不再要求软件专门为 AI 提供接口，而是让 AI 直接学习人类使用软件的方式。人能看懂按钮、菜单和窗口，它也去理解；人能完成点击、输入和切换页面，它也去执行。

![[01_raw/_inbox/文章/images/b8d4a7a5c08cd934e04a8f003bc45669_MD5.png]]

这意味着，AI 的工作对象开始从 API 扩展到整个图形界面。换言之，「Computer Use」负责赋予 AI 操作电脑的能力，而「Record & Replay」则负责把人的操作经验沉淀成可复用的技能。

这背后对应的，其实是操作系统角色的变化。过去，操作系统是所有软件的组织者。我们在 Mac 或 Windows 上安装各种应用，再由人自己在不同软件之间切换、复制、整理和传递信息。

人始终是连接各个软件的中间层。

而当 AI 能够跨应用观察、理解并执行任务时，它开始承担这层角色。对于用户来说，关注点逐渐从「如何操作软件」，转向「想完成什么事情」。

![[01_raw/_inbox/文章/images/514092b2efc174c6c04808cf26cd1c0d_MD5.png]]

报销软件怎么填、视频后台怎么配置、多个系统之间如何来回切换，这些细节理论上都可以交给 AI 处理。照这样发展下去，未来真正频繁使用软件的，未必是人，而是 AI。

对于 AI 来说，漂亮的界面没有意义，复杂的菜单也没有意义。它更关心的是：这个软件能不能完成任务、能不能被调用、能不能稳定执行流程。

从这个角度看，「Record & Replay」真正有意思的地方，不是又多了一个自动化功能，而是它透露出一种新的趋势：人正在从软件的直接操作者，逐渐变成软件能力的训练者。

今天我们学习怎么使用工具，未来或许更重要的一项能力，是教会 AI 使用工具。

我们正在招募伙伴

**📮 简历投递邮箱**hr@ifanr.com

**✉️ 邮件标题**「姓名+岗位名称」（请随简历附上项目/作品或相关链接）

[更多岗位信息请点击这里🔗](https://mp.weixin.qq.com/s?__biz=MjgzMTAwODI0MA==&mid=2652396877&idx=2&sn=dfef25453a6bf0dca147b0adca3deaf7&scene=21#wechat_redirect)

![[01_raw/_inbox/文章/images/37b4a035eff41fb69eb2c3e43f95a5b9_MD5.png]]

---

内容效果不满意？[点此反馈](https://feedback.notebooksyncer.com/feedback/a1a5fe5f_1781988598684?u=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMjgzMTAwODI0MA%3D%3D%26mid%3D2652455487%26idx%3D1%26sn%3D80aa707894fab75ff560893a147eb44f%26chksm%3D9a482e3cf9b20e2a267594716dee9d7cb1e8ec9fb92e5831cf0e5859207020649709afb8a080%26mpshare%3D1%26scene%3D1%26srcid%3D0621T53dftARrmwx8CSKjXM7%26sharer_shareinfo%3D3d5a1bbff8ddab5cf91c8deaa04853e1%26sharer_shareinfo_first%3D3d5a1bbff8ddab5cf91c8deaa04853e1%23rd&s=obsidian)