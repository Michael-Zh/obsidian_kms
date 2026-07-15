---
author: Ali Abdaal
source: 小红书
url: https://www.xiaohongshu.com/discovery/item/69fde2da000000001a035a7d?app_platform=ios&app_version=9.32.2&share_from_user_hidden=true&xsec_source=app_share&type=video&xsec_token=CB7E7pqs0kRZqI9MKPhwYappeWEaKwjcoYGndxAbbbB0o=&author_share=1&xhsshare=WeixinSession&shareRedId=Nzs4RERHO0tLPD1GOjswPEg5Qk06PjpN&apptime=1780090790&share_id=4fbfe933d47b4a08a5eab35498b9dcaa&code=40bK2WRPM8p
saved: 2026-05-29 23:40:21
tags:
  - 笔记同步助手
id: f56af5a0-dc17-49c8-81d0-ebac50e4f095
annotation: Claude code usage tips
summary: "Ali Abdaal's weekend Claude Code learning guide built around an 'AI flywheel': let AI interview you to find automation opportunities, then build something real. Walks through building a YouTube competitor tracker from scratch using the YouTube Data API, iterating via natural language, and deploying as a web app with authentication."
processed: 2026-06-06
---

作者: Ali Abdaal

## 引言：Claude Code 如何改变一切

在过去的三个月里，有一款名为 Claude Code 的软件彻底改变了我的生活。如果你像我几个月前一样，对输入代码感到恐惧，或者因为不是开发者而认为 Claude Code 与你无关，那么这篇文章就是为你准备的。也许你仍停留在与 ChatGPT 或 Claude 聊天的阶段，认为这就是 AI 的全部能力；又或者你知道应该学习 Claude Code，但只是没有时间。无论哪种情况，这个视频和这篇文章都将帮助你突破这些障碍。

核心思路是启动一个“AI 飞轮”：你让 AI 面试你，了解你业务和生活中的痛点，然后 AI 会建议你构建一些能节省时间并赚钱的东西。接着，你在让 AI 构建这些东西的过程中，会逐渐了解 AI 的工作原理，从而激发更多创意，进一步构建更多工具来节省时间和金钱。

每一天，那些只会免费使用 ChatGPT 的人与懂得使用 Claude Code 构建工具的人之间的差距都在扩大。我希望这篇文章能成为你的入门指南，帮助你缩小这个差距。

## 准备工作：你需要什么

在开始之前，有两件事会极大帮助你：

1.  **下载桌面应用**：不要使用网页版 Claude，而是下载桌面应用。它完全免费，并且包含“工作台”和“代码”功能。
2.  **安装语音输入软件**：用语音代替打字会快很多。我使用的是 Whisper，可以按 F4 和空格键开始语音输入，几乎实时出现在屏幕上。

![[01_raw/_inbox/文章/images/1e0c5ad8b82da6c72c80b37c8d56bff8_MD5.jpg|Claude桌面应用界面，显示聊天、工作和代码三个入口]]

Claude桌面应用界面，显示聊天、工作和代码三个入口

这两个先决条件能让你更快地与 AI 交互，避免打字成为瓶颈。

## 第一步：让 AI 帮你决定构建什么

很多人不知道从何开始。我的方法是：直接让 AI 面试我。我告诉它：“我想学习使用 AI，但不想随机找教程。我想构建一个真正对工作或生活有用的东西。请问我问题，帮我找出应该构建什么。” 我的业务主要包括三部分：YouTube 频道（内容创作）、在线商业学校（Life’s Business Academy）以及几个软件产品（VoicePal、SuperFocus、CreatorGreed）。

我们团队有很多数据抓取的繁琐工作，比如手动查看 YouTube 和 Instagram 的分析数据，复制粘贴到 Google Sheets。我们还需要追踪竞争对手（同行创作者）的表现，以便及时调整策略。这些工作耗费大量时间，非常烦人。

![[01_raw/_inbox/文章/images/f092aafa79193359b9ed2ae7f3f5c72a_MD5.jpg|AI面试过程，Claude提出问题帮助确定自动化方向]]

AI面试过程，Claude提出问题帮助确定自动化方向

Claude 立刻理解了痛点，并建议从 YouTube 竞争对手追踪开始，因为它有公开 API，相对容易实现。我们还讨论了 Instagram 的问题（API 更封闭），但决定先专注于 YouTube。

## 理解终端与 Claude Code

如果你对终端（那个黑底绿字的界面）感到恐惧，别担心。终端只是一种通过键盘与电脑交互的方式，而不是图形界面。在 Mac 上，你可以通过“终端”应用访问。Claude Code 运行在终端里，它本质上是同一个 Claude 大脑，但可以直接在你的计算机上执行操作：创建文件、运行代码、修复错误。你不再需要手动复制粘贴代码，只需用自然语言描述需求，Claude Code 就会完成工作。

![[01_raw/_inbox/文章/images/fd49f44003bcec3e79db3b74d24c8eeb_MD5.jpg|Mac 终端界面，显示命令行提示符]]

Mac 终端界面，显示命令行提示符

### 安装 Claude Code

在终端中运行一条命令即可安装：`curl -sS https://docs.anthropic.com/claude-code/install.sh | bash`。如果你不理解这条命令，可以让 Claude 解释——这是学习的一部分。安装后，输入 `claude` 启动，它会要求你登录 Anthropic 账户。

![[01_raw/_inbox/文章/images/db6a83c94515f84acd41e886e4a1fc37_MD5.jpg|Claude Code 登录成功后的欢迎消息]]

Claude Code 登录成功后的欢迎消息

第一次使用时，你可能会担心安全性。Claude Code 会先询问你的权限：创建文件、运行命令前都会请求批准。你可以控制一切。

## 构建你的第一个项目：YouTube 竞争对手追踪器

### 创建项目文件夹并启动

在终端中，用 `mkdir youtube-tracker` 创建文件夹，`cd youtube-tracker` 进入文件夹，然后运行 `claude`。现在，你可以在 Claude Code 窗口中用自然语言描述你的需求。

我的提示词是：“我想构建一个 YouTube 竞争对手追踪器。我有大约 50 个 YouTube 频道名称。请编写一个脚本，使用 YouTube Data API 获取每个频道的最新 10 条视频，包括标题、缩略图 URL、观看次数和发布日期，并将结果保存在本地 JSON 文件中。先测试 3 个频道。”

![[01_raw/_inbox/文章/images/307c1194abe09bea6ded64bc1e119e53_MD5.jpg|在 Claude Code 中输入构建命令的界面]]

在 Claude Code 中输入构建命令的界面

Claude Code 开始工作：它询问是否可以创建文件、运行命令。你逐一批准它。它会生成 Python 脚本 `fetch_videos.py`、一个简单的 HTML 页面和数据文件。

### 获取 YouTube API 密钥

这一步可能会有点令人沮丧，但别放弃。你需要访问 Google Cloud Console，创建一个新项目，启用 YouTube Data API v3，然后创建 API 密钥。Claude Code 会指导你每个步骤。如果你感到困惑，可以直接把屏幕截图或错误信息复制给 Claude 求助。

![[01_raw/_inbox/文章/images/b273e6c5e7751e7c0e6bbf4968c076ca_MD5.jpg|Google Cloud Console 界面，显示创建 API 密钥的过程]]

Google Cloud Console 界面，显示创建 API 密钥的过程

API 密钥就像密码，不要公开分享。

### 运行脚本并查看结果

脚本运行后，会抓取数据保存为 `videos.json`。Claude 还会生成一个 `index.html` 来可视化数据。但由于浏览器安全限制，直接打开 HTML 文件无法加载本地 JSON。Claude 会建议启动一个本地服务器：`python3 -m http.server 8000`，然后在浏览器中打开 `http://localhost:8000`。

![[01_raw/_inbox/文章/images/2689f029e988fd799eb2ee2cb8d1a7ee_MD5.jpg|本地服务器运行后，浏览器中显示的仪表板界面，显示三个频道的视频列表]]

本地服务器运行后，浏览器中显示的仪表板界面，显示三个频道的视频列表

成功！现在你能看到一个漂亮的仪表板，列出了 Thomas Frank、Matt D'Avella 和我自己的频道最新视频，包括标题、缩略图、观看次数和发布时间。

### 迭代改进：过滤 Shorts

我不喜欢看到 YouTube Shorts，只想显示长视频。我告诉 Claude：“请过滤掉时长少于 60 秒的 Shorts。” Claude 修改脚本，添加了过滤逻辑。它显示文件的改动（绿色新增，红色删除），确认后再次运行。

![[01_raw/_inbox/文章/images/c23532682f0af1ad9e6106ecc1a97606_MD5.jpg|Claude Code 显示代码改动，新增过滤 Shorts 的逻辑]]

Claude Code 显示代码改动，新增过滤 Shorts 的逻辑

再次刷新浏览器，Shorts 消失了。这种迭代开发非常自然。

## 部署到网络并添加用户认证

本地仪表板虽然好用，但我想让团队也能访问。Claude 建议部署到网上，并自动更新数据。最简单的方式是使用 GitHub Pages（免费托管静态文件），配合 GitHub Actions 定时运行脚本并重新部署。Claude 会一步步教你设置。更进阶的需求是添加登录功能，保护页面不被公开访问。Claude 会教你怎么用简单的用户名密码认证，或者使用 Google OAuth。甚至可以添加 Stripe 支付，变成付费 SaaS 产品。

![[01_raw/_inbox/文章/images/7acd3ef757695ad75b3a445683a6b600_MD5.jpg|GitHub Pages 部署设置界面，Claude 指导如何配置]]

GitHub Pages 部署设置界面，Claude 指导如何配置

整个过程你不需要知道如何编码，只需要会用自然语言与 Claude 交流，并保持好奇心去追问你不懂的概念。

## 更多实际用例：我在过去两个月构建的工具

为了展示 Claude Code 的潜力，我列举了我为业务和个人生活构建的一些工具：

-   **支持工单管道**：自动检测 Slack 频道中学生的问题，创建工单并提醒团队及时回复。还建了一个网页界面供教练查看待回复工单。
-   **Slack 机器人**：将原来分散在多个平台的 AI 助手（自定义 GPT）集成到 Slack 中，学生可以直接在 Slack 里使用机器人获取帮助。例如“Dumbledore” DM 机器人帮助撰写冷消息，“Loopin” LinkedIn 机器人等。我们可以查看对话记录，确保机器人给出合理建议。
-   **内容分析仪表板**：自动分析 YouTube、Instagram、LinkedIn、TikTok 等平台的历史表现，找出最佳内容格式，生成新话题建议，并追踪竞争对手。
-   **MCP 服务器**：创建了一个 MCP（Model Context Protocol）服务器，让 Claude 可以实时访问我的项目、目标和待办事项，提供更个性化的帮助。

![[01_raw/_inbox/文章/images/25ebeac241457373d8fd6c5590599634_MD5.jpg|Slack 机器人 Dumbledore 的对话界面，学生正在使用它生成冷消息]]

Slack 机器人 Dumbledore 的对话界面，学生正在使用它生成冷消息

这些工具为我的学生和团队带来了真实的价值，每天都有学生赞叹这些工具的强大。而这一切都始于一个周末的学习。

## 克服摩擦：开发者 vs 非开发者心态

构建过程中你会遇到技术摩擦，比如配置 API 密钥时界面不直观。开发人员习惯了这种摩擦，他们会谷歌搜索、查 Stack Overflow。现在你有一个更强大的助手：直接把错误信息粘贴给 Claude，它会告诉你解决方法。秘诀就是：**不要被摩擦吓倒，坚持下去**。如果你能比其他人更愿意跨越一点障碍，你就能获得巨大的优势。

![[01_raw/_inbox/文章/images/d19079158c420c3323418b8189ce3c52_MD5.jpg|Claude 解释 Google Cloud Console 界面的对话，帮助用户理解如何创建项目]]

Claude 解释 Google Cloud Console 界面的对话，帮助用户理解如何创建项目

## 提高效率：多个终端并行工作

当 Claude Code 在运行一个任务时，你可以打开第二个终端窗口，启动另一个 Claude Code 实例，并行开发不同功能。我甚至买了 52 英寸的显示器来同时运行四个终端窗口。注意不要在同一文件上冲突，但要充分利用并行能力。

![[01_raw/_inbox/文章/images/07feade14e0bb808c0fc29eec1f61956_MD5.jpg|多显示器设置，显示四个 Claude Code 终端窗口同时工作]]

多显示器设置，显示四个 Claude Code 终端窗口同时工作

## 总结：立即行动

每个周末，学会使用 Claude Code 的人都将获得越来越大的优势。你不需要会编码，只需要有好奇心、愿意与 AI 对话并推动一些技术摩擦。我从两个月前的完全门外汉，到现在能构建出价值非凡的工具，感觉像变了一个人。现在，轮到你了。

如果你觉得这篇文章有用，请在评论区告诉我。你想了解更多关于 AI 提升生产力的内容吗？我会继续制作深度教程。

![[01_raw/_inbox/文章/images/b826b1b84edba0edf030f652154faf89_MD5.jpg|最终完成的竞争对手追踪仪表板，显示多个频道的统计数据]]

最终完成的竞争对手追踪仪表板，显示多个频道的统计数据

感谢观看，下次见！

## 逐字稿

**00:00** there is an incredible piece of software called cloud code that i've been using for the last three months and it is completely utterly changed my life and this video is the video that i'm sending to my friends my family my team members who have not yet started using cloud code maybe you're like me a few months ago where you were intimidated by this thought of typing stuff into a code maybe you're intimidated by a name like cloud code maybe you're not a coder i'm not a developer i'm intimidated by code maybe you're still stuck in the paradigm of talking to chat gpt or cloud on the weather and thinking that that is all ai has to offer or maybe you're one of those people you're like man i know i should get into this cloud code thing or this code coding

**00:31** just generally have time purposefully this video will help you solve all and this video is going to introduce you to the idea of the ai fly you basically get ai to interview you about what you're doing in your business your life life you work based on that you get the ai to suggest what cool things things can can use ai to help build that would help save you time and make you more money and then in the process of getting ai to build those things for you you were also learning about how the ai works the more that feeds into ai ideas which means you you get a more update in your brain which now you know what's possible which means you can then build even more things to help save you time and make you more money

**01:05** using these c k a i features i've built stuff for my team and for my customers that literally add value to a customer every single day where people are raving about the tools that i've managed to build for them over the last couple of months just by learning how to use code i the final thing to say before we get into the video is that every single day the gap between the people that just use the free version of chat g p t and talk to it on whatever verses people that know how to build stuff using code i even if you don't know how to code every single day that gap is getting wider and wider and what i hope this video will do is give you a sort of beginning guide and how to narrow the gap and what i time to everything in the video so let's get started

**01:35** ok so there are a couple of prerequisites that will really really help you if you have these down and done before we try doing the stuff the first thing is you do not want to be using the web app for something like code instead you want to download the desktop app this is totally free but when you download the code desktop app you will notice it says chat which is the thing that you are used to which also has access to cowork which sounds somewhat scary if you have not used it before and it says code which sounds even scarier if you have not used it before the second thing you want to do is you do not want to type you want to have some kind of dictation software or install that does a speech to text

**02:06** there are lots of these in my case the one i use is called whisper for are put an entirely because something the video transcription if you are interested and the cool thing about whisper is i can hit f five spacebar and then i can say whatever i want and then it will appear on screen within like maybe a few seconds okay

**02:19** this is tighter works this is a far quicker way of speaking to an ai rather than having to type to an ai and are basically the only two prerequisites you need

**02:27** so step number one is we're gonna ask ai what we should build with ai i am trying to learn how to use ai my current ai skill set is i just use uh chatgpt and claude and use the chat feature but i recently watched the video that tells me about cursor and how code is the best thing ever

**02:43** so to that and I want to learn how to use AI, but I don't want to just randomly try and learn how to use AI by following tutorials. I actually want to build something that's really useful in my work, in my life. The problem is I'm not really sure what to build, so I want you to ask me questions and interview me and help me figure out, within the context of my work, I want to build something that saves me meaningfully, uh, I mean, making money in the context of my business, and in the process I want to sort of learn how to use AI, my programming work and cold code as well. Okay, so my business actually does, I guess I say, three main things, and firstly we do as content, so I have a YouTube channel and I save me in engagement

**03:16** passion stuff on living and the content in west china so of help people build on life they love and so of changed lives in stuff personal development things are the second thing the business does is we have an online business school called the life stuff business academy that helps people for and grow and six big life fuel business success and the the thing that we do is that we are building various software products we've got a platform voice pal which is a sort of a i platform which a building and app called superfocus which is a software productivity app which which a a building app called platform one course creator grid which um um is a platform for help help creators grow and monetise audience success actually we know one thing that i wish i didn't have to do

**03:52** or i wish that my team didn't have to do is that we do a lot of data scraping so for example for youtube for instagram for LinkedIn we spend we you know my team spends a lot of time each week looking at analytics and looking at view counts and adding up saves and um impressions and stuff and and some of that data we need to send to sponsor or if we use to figure out whether our social media stuff is going well we also need to do this across our competitors i am not don't really think of them most competitors i think of those colleagues but we have to keep an eye on what other friends in the space are doing so that if someone is growing particularly fast or

**04:23** hits on a format that is particularly good and we can experiment with that format ourselves and so all of this stuff takes actually many many hours for my team um every week so i wonder if there's some cool stuff we can build that will help us automate some of that do you think that would be possible

**04:37** kind of present possible and honesty is a great candidate because that takes both boxes is genuinely painful i was like we can manually work and it's the kind of thing where you learn a ton by building it now this is good it is asking you really really useful questions about how we can automate this data collection process i'm not going to read into the responses you can pause the video when i'm like just read the stuff you you can you can like okay so the current video like um yeah ah the guy on my team and the two on my team literally go to youtube studio or to instagram analytics basically they go to instagram and see and they write down numbers and they manually write the numbers into a good sheet and then

**05:09** used to some functions would count up like impressions this week or something could you? I don't know, I actually don't know what's a little Instagram insight maybe they don't have to do that anymore but either way it's a manual process of copying and pasting numbers into a Google Sheet. Second, how many of these colleagues are you tracking are we talking five channels or fifty? More like what? Fifty fifty YouTube fifty on Instagram? and on TikTok? That sort of thing and what does the process look like it sort of goes into a Google page but it sort of goes on random notion pages that are all over the place it rarely goes into slide decks but yeah primarily Google Sheets and notion databases

**05:40** that's where it goes once it's collected and then you know we always think you'd like to see it more often but then because it's told over the place it's kind of hard to look at more often in reality what we often do is check into a i and be like can you give us some interesting insight but i think it's the the collection of the data itself that like is kind of annoying

**05:56** you know let's not worry about this sponsor stuff i think let's just focus on the competitor tracking um what i want to know i think yeah it's how many views that the recent videos get is also what topics are performing well for them i like if thinking about youtube i i never want to watch the video itself because i don't want accidentally copy it but i'm very interested in what the title and the thumbnail are and if we thinking about instagram reel i you in a tracking world we build it to transcribe the reel to get the hook but i always interested in what's the first line so if if the instagram carousel like what was the format so if it's the challenge of instagram i would go all these different formats so yeah i just don't let me know how we would go about

**06:28** now as this is telling me when we going to start with youtube is easy when you you have a public api where you can pull video titles some selves you can publish ed dates any public channel you give a fifty channel names and it gives you back everything you want that's what we project sick instagram is hook a dit able meters a p i is more locked down so so going to get a more more creative here here's what i imagine you en a path toward could be webpage and you see something like here the fifty channels of about trk here the lost ten videos of about about years k here of was popular of this week that could be great you could see a aniles and titles of all balance without watching anything you could could have ai let intelligent time the topics you can spot patterns like here of my colleagues posted about morning routine this week and they did well sick

**06:59** beautiful things that this is a perfect project for learning cloud code because it involves real app, real data processing, and optionally a real frontend, but none of it so complex that you'll get stuck for days. That's the right thing to focus on. Do you have a preference for the output? Like, what would you rather see—a nice-looking dashboard you open in a browser, or would you rather just automatically save the data? A data file that your team uses? This is so sick, man. You'd rather read back right now and be like, "Wow, Claude has such a good understanding of what I'm trying to do, what I'm trying to build. It's suggesting things that I don't even think of." Like, what a time to be alive. You literally ask the AI

**07:31** build stuff for you and also teach you how to build the stuff in the process like in the past i paid thousand thousand thousand dollars for like you automation consultants to ask us these our own questions to figure what we can automate the business business none of what they've spent of the fifty thousand all those dollars that we paid to automation companies and automation agencies and consulting whatever people comes close to the level of interesting that talk about here so i i a rule of thumb with me this is incredible now at this point this also something something superinteresting that i would love to talk about here so i happen to know what an a p i is i think but if i didn't know what an a p i was it's like my rule for the a i stuff is any time i don't understand something what i do

**08:05** i asked him to explain it to me okay this one is very cool but i want to understand the foundations and the philosophy and so when you say a p i what does an api actually mean why it's useful and how did api

**08:17** get developed like why are why are they a thing in the first place and i could just just really go explaining stuff the fact that you now know that those things exist means that you might realize wait a minute that

**08:27** this this program that i use in my work called blablaa i wonder if they have an a p i you google does bublabla have an a p i and if you won't familiar with the word a p i you wouldn't have known that you could even ask that that question and you might find know it doesn't have an a p i but it does have an m c p server now if you are not at all curious and you're a mental person and you don't put in that threat and you like m c p server and it sounds technical i don't care but if you're an intelligent person you would think an m c p server i you've heard of that i don't know anything about it what's an m c p server and you understand all a m c p servers and you realized it a minute and you other ideas it things i can build

**09:01** that will help me save time and make more money that involving cp service ver could look with my own n c p server what about own n c p client okay this super interesting and you start to learn this stuff without trying to learn this stuff like you never had to sit down on a chat tutorial about like what the n s a n d m c p server and how does it work but before we do that we have to dive down into this it or youtube sc p p re implement youtube competitors for social media management unless you're a social media manager or your job or your business involves social media in some way or that specific that case is probably not relevant obviously because you're 're intelligent person you know that i'm using that use case as an example and you know that you could

**09:33** obviously just like to interview you about your own needs as it will help you figure out what you should build for your own stuff but just for the sake of opening your brain up with more examples i want to tell you a little bit about some of the other tools that i basically built for my business and my life over the last two months if you want to give this spin the video because you don't carry you just want to get to the core stuff the the time stamps and the case for the only thing in the video and the fact to make students and i'm to to ask one of my open code agents open core is kind of my cold code on steeroii you you using open cw for the last like two months well if you just getting started with this stuff i won't worry about it i would start off with co-co-work or court code initially and then you can double around with the open cw if you feel like i let let tell you you about various of my open code agents i have elus who is my primary open code agent this is what else ks like like i have money who is my curriculum architect for our live ital business academy es es the one who helps me basically think through the the different things that we are teaching students and the research and what's the current stuff and the world of building in on something in in twenty something and it except for this is what she looks like

**10:25** i have innover who is the vice principal of the life's business business academy and she helps with all of the operational associated with trying to give give students of best experience to build their and then six six of left of businesses and then innover along with court code essentially helps me build automations that make our lives and our students lives a lot easier next we have remiss who is my content boss so i remiss who i talk to when i'm my telegram you have get content ideas and he's the one who helps build out all of ves like competitive analysis like docs and stuff that were doing in addition to ves coa we have dobby who is my general assistant that runs on a very cheap so and thropic model called hike or is all we other runal sonor opops sso so the a ba more expensive so dobes like my cheap personal assistant we have sederate who is my my intention coach and so i told to seerurand he is research around around homeschooling and like

**11:05** and know gives me ideas for like romantic date nights with my wife and stuff like that so that's cool and then recently i added callin it who is my health coach and so callin it tracks my protein i take everyday and he's also my work out app i i'm at the gym um he's got access to all of my dexa scans all of my like work out history which i exported from the app strong for like for the last like five years and so he knows exactly where i left off he knows that i had like a um i i had my arm recently i had a left radius fracture he knows that therefore he has to modify exercises based on that so so i'm i'm at the gym because currently my personal trainer is on holiday so what i'm at the gym callin it is my personal trainer i'm talking to callin it to figure out what i should do any modification i need to make what i'm my groin hurts warming up squats callin it will tell me to back off and so do another exercise instead

**11:44** this sort of fiasco with that digression i was actually going to ask ask Elon

**11:49** yeah Elon i'm actually working on a YouTube video where i explain how to train an AI in a weekend and you know for the last two months that we've been building stuff using open core and using code can you just give me a list of real business and life use cases that we have built in our startup i can show uh my lovely videos on YouTube as an example of what we've built for each one i just want to like a quick one line alright here's an example of all of the stuff that i built using code month of the last two months firstly a support ticket pipeline so but one a life of business example we have two hundred support students for all of our students because currently we have about two hundred students

**12:22** and each student has their own like private slack channel where they get added to a slack channel with themselves and like me and the coach and like angels and various of the team members where they can pose anything they want we aim to get back to them within like twenty four hours ideally no previously this was a manual process of like the coaches having to keep on top of like which slack channel is on red and which one is red and if students replying on a thread you can't see the notifications you can't see the messages and so what I created in code code is the thing that like automatically creates like support tickets any time a student messages in slack and so that's automatable and a trello board and also optimizable todos

**12:52** to a private like channel that we have in a team which says that hey John Smith posted this support request it's about to be twenty four hours someone please reply to him here at that kind of idea on top of that i created a web interface that the coaches can log into so they can see which slack channels for which students need response and so they are able to then click a button it takes them directly to slack and they can respond to the students and then i created a handful of student facing slack bots so the problem we are having is that previously we were giving our students a bunch of custom gps like we created custom gpt for things like each generation and first draft offer creation and like content and like giving them feedback on the sales calls and things like that

**13:24** but the problem we found the custom g p s is that we couldn't actually see how students were interacting with the custom g p t was kind of a te because then i could see all the custom g p s actually giving the students used so advice and then the students were coming up with these things and was like we them and where did you get that from and they got it from the custom g p t and i can't see like what things went wrong with the custom g p t that don't top that we have students who were any complaints that we don't like too many platforms like you know some stuff on google of a students on slack and all the happening on slack we got the have custom and a sycle and now we have to have even over a account and do so in a custom g p t and and a a stolocal code like is it possible that we can recreate the functionality of the custom g p t using a slack bot and so the students on slack anyway that is able to message a bot and get the same kind of stuff but then we as the custom team have access to custom positions we can see we can sort of like control the agents and make sure they are doing sensible things and so over the course of up using code i we did all of this up using code using python servers making sure that we have everything and databases that i set up to compile that and i accidentally enable security so that we don't like accidentally leak complaints that students are having

**14:19** and we created a bunch of LLM bots that that students have been engaging with and are having a great time talking to for example there is a Dumbledore or the DM agent and so we've like over a hundred of our students and thousands of thousands of messages and Dumbledore the chatbot and Dumbledore has been trained on our like internal the methodology for how to sort of convert a cold customer objections into a lead in a sales call so they can grow the business and so have students like copying and pasting LinkedIn profiles of their prospects into Dumbledore and Dumbledore is helping them with outreach message so we have Dumbledore the DM agent and have Loopin the LinkedIn agent we have rolled out the sales agent by the time this video comes out we like released Floyd who is like the delight agent that help students like creating AI for customer experience for their coaching or consulting or service business and we have a bunch more which is super exciting but the really cool thing about this is about the students can give us feedback I can see the stats on how how much people are interacting with agents I can literally read the conversations that students are having with the agents I can flag to them that like I can read the conversations I read the conversations to see like are the agents giving students sensible advice I see the stats about that like like the students' interactions to see like in terms of like competitors on YouTube like

**15:17** who has released videos and what's been their views in the last twenty four hours so will see that you know who mozyou recently released a video called whatever whatever whatever and that's got one point four thousand views in the last twenty four hours that's like an outlier for all like exmomois channels so then it prompts us to think could we like take inspiration from the fact that that video is popping for homoses that the things of work works on now is a sort of atshos which is a sort of web team can and that me and entire team can use across youtube instagram linking and to take tok and ttter that automatically analyses that of of content we've put up of the last like nine years and these platforms figures out what of the things that worked kind of the things that did not generate content ideas based on transcripts from stuff that i said when i have done workshops for a students and l b a automatically tracks all of the competitors and it helps us face ideas for that content that we can make

**15:57** just perform better I topped that I also created my own MCP server which then Claude and Cursor have access to, which means that they can automatically see all of the projects and working on within the business where my goals are all of the outstanding to-do's any kind of journal items that have been put in there because I want it to have access to that and so now any time I talk to Claude AI the chat now has way more context about me added it and it happens through sync to the and I'm keeping it to court when I'm using Claude Code when I'm using OpenAI when I'm using code and it all happens through an MCP server that might have been a lot to a ggand I did not know what any of this stuff meant two months ago until I decided to you know spend a weekend just try to build something useful using Claude Code and

**16:33** over the last two months like every day as I've done this learning loop this sort of i fly well I've built more and more things and there is a danger with those this like AI stuff that you end up in this in this zone where you spend so long like building agents that talk to other agents and that like help you orchestrate other agents that you don't actually end up doing anything useful useful I would define as it adds value to your customers it saves you time personally it makes you money personally and that I was very mindful of that that like I don't I don't want this to be one of those like people spending

**17:03** days making notion set ups to theoretically try to be more productive but not actually being more productive

**17:09** so going back to our data analytics project for mutual competitors yes ok i know ready to start writing this thing can you help me understand what the cocode actually is i i really have a background and coding and so i have been intimidated by cocode in the past when i see people using the terminal with like the black and the green text it feels like some hackers out of the matrix and i feel like i'm not tech savvy enough to use cocode can you help me figure this out okay let's kill the intimidation now the terminal is not what you think it is that black screen with a green text let's demystify it because

**17:40** before we talk about code you need to understand the terminal because code runs inside it is the thing you already know how to use a computer using a graphical user interface a g u i you see i can let you take buttons you you drag things around mac os windows your phone all graphical user interfaces but u s weren't there there nineteen eighty four when apple released and macintosh virally all computers were operated by typing commands you type something like l s to see a list of files or cd documents to go into your documents folder that's it that's the terminal is a way of talking to your computer by terminal instead of clicking the terminal didn't go away when u s arrived it just got hidden on your mac right now i open terminal this is what it looks like um

**18:16** if we go i think on the make by default white with black text rather than black with white text but whatever it's basically the same thing you can type whatever you want doctor dog if you open it you're looking at the exact same computer the exact same files the exact same everything you're just doing with a keyboard instead of a mouse think of it like driving a gui automatic car your computer handled out little the details for you the terminal is a way when you have a road and destination you just have more direct control yes for certain code like the one one about the build how the code also actually goes faster and simpler and clicking through menus so what is code code specifically you know how when you used code in the china and type message and clo responses the code code is the same code the same brain but instead of living in a browser window it lives in your terminal and here is the key difference it can actually do things on your computer when you child with code and and ada ai and give you code but when you have to figure out what to do how to to run it out to install you the middleman cloud tells out what to do you you do however code code removes the middle man you you say build or is that what you let us get a hold of the the technology you when code code actually create the the files and you you however the code fixes the error and and you web come on your error line you're sitting next to it watching and you continue and not like that do it this way but you not doing the mechanical work of copying and pasting code between windows but this is nice a concrete technology why it feels like the hacking but isn't the magic the aesthetic of the terminal the genuine leading when you you code code most things what you doing is just talking to it in plain text

**19:32** you type things like can you create a new project photo for my youtube tracker and it just goes and does it it asks you questions if it's unsure it'll show you what it's about to do before it does it you can say yes or no it's a conversation just like this one except the AI actually touches your files amazing like you need to watch it to learn how to do this oh you it was a lot to explain what Claude Code is oh you can ask it like okay how do i install it okay this sounds really cool how do i install it you can do it using the desktop if the terminal feels it or you can type in one command in the terminal okay so on mac open the terminal app command based top terminal and enter and paste in one single command curl -fsSL to the air session style s h h h so this is now where it starts to feel like coding it feels like hacking feels like go go this is intimidating but

**20:13** super simple thing i'm going to copy this explain to me what the hell is going on here before i do it please start a dog

**20:23** you don't have to do this with every single terminal command but like it's good habit to understand the code that the machine is trying to run on you a machine good instinct. You should never type something into a terminal without understanding what it does really break down every single piece reading the right code this is the program that been on basically every computer since nineteen ninety eight the program stands for the resource you are about to it does a fetch stuff from the internet you it does a web address and download the URL there like a browser but instead of displaying pretty web page just grabs the raw content issuing flags like settings that modify command behaves fail cleanly silent still show errors follow redirects so ok so -f -s -L -o together and to download this quite you follow any redirects only told to me something something long long long ld a i ash installed just a web address points in a file on an http service if you curious you can actually open that URL in the browser read the script for running ook great that one of installed clone you literally just type and code into a terminal

**21:11** and look what happens ask singandwork space uses er i though is this a project you created or one you trust like your own code or work from your team so yes i trust ted this folder

**21:22** great now you'll see this doesn't look scary anymore this doesn't feel like code from a hack away in a black and green terminal welcome back alally this a little icon appears four point five plot team sppok studios hello what the hell is going on here

**21:36** coa lessing god please run loggokay i need to login to my colo account let me do that great i would like to connect the proper studio with his name of my business yes i'm happy to for to dustuff ff great login successful presento to continue wonderful hello what what the hell is going on on here um hey you 're in coloco and and ropis com and line line facace bc colco your logating was successful i can help you with soft engineering tofi can king engineering explahere but h can forgetting an stanand basis running command and maging files and weering techical questions what can i help you with we basically have code running inside the terminal that is able to the access files and do stuff on our computer what our perpersion crucially you might be thinking of my god but also the security concerns here what i'm scared about it's deleting all my files if that's a case actually you know what let's tala colo code

**22:19** this is the first time that i actually installed code and i am a little scared i'm worried about the security implications of having an ai that can touch my files and potentially delete everything on my computer can you help me understand what is going on totally fair concern giving an ai access to a filesystem is a big deal here what you should know you can control it asks the system before running commands or editing files you see exactly what it's about to do and can approve or deny you can configure the system to the mission systems so now what you basically have is yes you can chat to claude via claude ai or claude chatbot but once you use it on your computer on your terminal you can also

**22:53** literally talk to Claude Code via your terminal it's just that the terminal version gives you the option where you command to access your files and add files and remove files that once you got be careful about and be able to write code build to run code where there's the Claude chat it can still create websites and powerful presentations but it does it in a web browser so you have to complete the file or I won't be able to actually run a web application for you because you have to run it on your computer okay now now I install Claude Code where do we go from here how do I build this here or you you be be complete analysis

**23:24** drastic situation that we were talking about ok here's what gets fun and starts before you start to to to launch create a project folder in your terminal you want to create a dedicated folder for this project think a bit like creating a new folder on desktop providing the terminal so i could do mkdir which means make a directory a create a folder cd means change directory then let's go code inside that folder that's not interesting let's do to do do so i'm i'm gonna go like terminal

**23:47** and get d d of launch code i happened to know they use control c to like exit out a program if i didn't know that i would ask program so now exited program and i'm now back within the terminal interacting with my computer directly so what i could do it like i go on my desktop i write create i i can do new folder and i could call it

**24:05** youtube tracker then i kind not open the folder youtube tracker but i can do the same thing from the terminal itself i can use mkdir so that's going terminal

**24:14** and type in mkdir youtube tracker and hit enter

**24:18** and it looks like nothing has happened but if i look inside my home folder

**24:23** turns out there is now a new folder called youtube tracker i was able to run a command from the terminal the terminal understood what i was trying to do and it created the folder for me sick so that was like cd youtube tracker okay let's pin pace that let me make sure i understand what it means cd means change directory okay ah ah that means very homeless folder

**24:43** and you'll notice that it's gone all the way to tilde with this little wavy symbol what's this wavy symbol called me tilde and it's l d l d l d r ok fine so previously we were running commands in my home folder tilde all the way to this which is shorthand by this tilde amount as i just found out from c c e r and now we are inside the folder hutue tracker so then it's telling me now start cloud code inside the folder but just typing and cloud okay just typing and cloud oh yes i'm sing workspace hutututracker this i trust it folder it got nothing in it i just created it

**25:14** and now i run code within the context of this youtube tracker folder next step get a youtube api key got this are going to be complicated so go to console cloud dot google com creating new project search for the data api go to credential and create api key it takes about three minutes i tested three three lines of code will to build this is the magic part once you're in code and new project order you literally just describe what you want in plain english this is like super english so i could literally say i want to build a youtube video tracker i have listed about fifty youtube channel names i want to script that uses the youtube data api to pull the ten latest video for each channel

**25:46** including title of a neural you'll have a view council and publish the results in a local journal and now maybe I'll restart which just three channels to teach and then the code will stop building will create files write code and probably run it to test you'll see it asking for permissions along the way can i create this file can i run the command and you just approve each step can you can understand words that before you approve the step you can see prompt time you'll realize that you'll you'll start to get a feel of what you need to worry about and what you don't my suggestion start tiny don't try build the whole short in one go start with just three channels get the data pulling work and at the output and say okay now can you make this into a simple webpage where i can see the family names in a standing layout go from there that you type of code that you can state and conversation

**26:23** actually can you solve by views can you add a call to him for hold the videos can you hit anything over a million views you are starting from scratch but building that's workable one of the things that really holds people back from running this AI fly well is encountering friction and being unwilling to figure it out and developers don't have this problem when you are software developer you encounter friction all the time you encounter a bug and the bug shows that something things are not working you're right on track

**26:50** connect on an API and you realize that like the API documentation is that a day back in the day the skill of being a good developer was knowing what to google because it's like knowing what error you google and what you copy and paste into Google to then go to a website like Stack Overflow which is like a forum where developers discuss how to fix things and then figuring out what the fixes that someone else has and then trying to run it on a new machine and seeing if the fix is still valid and if you are a very good developer and you were good to the developer community you would then update the Stack Overflow forum post with the latest version of the fix these days you actually need to do the Google Stack Overflow for things because you can just copy the error message to LLM and it will tell you exactly what to do and then

**27:23** you know this kind of stuff so developers are naturally good at pushing through friction most people who are not developers in the context of their work have probably not encountered like technical friction unless you are a particularly technical role you might have entered human friction like what you do when your boss refuses your annual leave request then then you have to figure it out but when it comes to doing stuff like this you will encounter some technical friction and the thing that will separate you from your grandma is that you are going to be willing to push through the technical friction and figure it out but getting a p i e s from platforms is an example of technical friction

**27:56** in particular with like google project is a little annoying and it's a little it it can be a little how to get your head around but i trust you you're intelligent you will be able to figure it out if if you can't figure out again if you have like you have ChatGPT that you can just like copy and paste into to figure it out for you so let's get a youtube API key so go to console of cloud of google dot com ok yeah open link create a new project call it youtube track or whatever how the heck do i create a new project uh uh i think project google cloud okay maybe you like like a new new project

**28:34** we're going to come come down we're going to relax and i'm going to ask clocloyou'cloud i'm on the google cloud console thing but i can't see a button to create a new project of what the break do i do no do with our counclors know the most intuitive interface in the world let me look at the currently out se i don't think you you know world you jchase you you cloi can't yeah google clcouncounillors a touriislike comsing sing it's is the way to look at didithe top of the page of the ft of tion okay the budirecct conpulook okay okay so if i like click on that i can type a new project youtube tracker test okay that's fine

**29:05** notifications create project you want to track a test okay cool all great i click select project ah okay i just say you track a test you are now incurring charges new billing account i set up a google for an organization uh yeah i don't know what any of the stuff means what are we going to do what i want to ask to do this is what i like to do what ever i want to do id what i have never included in going on i command command c copy paste it command d

**29:35** help me understand what the fuck is going on on this page do that take a deep breath you could ignore almost everything on this page thank you close the good a left sidebar hamburger menu in the top left like like kind of APIs and services ah i click on APIs and services like library okay i love it i i want the instructions of the arguments me you actually matches what what i on on screen doesn't happen this is not the action that sometimes you to go through library okay in the soda time youtube data API be three youtube data API

**30:06** be three outset

**30:08** nice the YouTube data API and API price actually a youtube data of just video that is in channels click the result that he enable now can't be that easy can it enable surely now will be easy I like dealing with them from Google old stuff ok what's happening okay 嗯嗯 stuff is happening okay ok what's happening once enable go back API and services credentials okay well APIs and services credentials okay click create credentials API key and the focus quick okay create credentials API key okay

**30:40** oh to get keys gives you they know terrify form make no difference in up up in my creation on to a cute amount center i am no a blob a b b d as enterprise stuff you describing it keen leaving i think about like checking into a hotel that offering you just far package the re form reservation the concierge to and the the lot of program you just want the room key ok back in the day you'd see see paste like ess s i b y like name does n't name matter h h and you you stand the ag g g b i n g on stack of flow i n g like doesn't matter what name my youtube a p i k a p s that can an a c e x using the key you go like h h helps this enormous terror h it that's it's this less manual atic big query and it c u s big query on like god cloud a shit it but now you just copy and paste it all of it into cloud and it helps you understand it directly

**31:15** you know what i'm just going to cop in peace to to all this it's giving me all these options what do i type in where doctor to class a google over complicating things again here's what to do name type something like youtube tracker this is just a label for your reference you you remember the key for okay you tube tracker thank you a p i that can be accessed using the key and yes a p i restrictions click re create then find youtube data api okay okay okay so when everything else ignore it you you don't touch application restrictions don't trust the service account don't know about i websites a p address and relay i p us and that this supplies

**31:47** just given a name restricted to atata p i i three he create a atroa blobbba it 'll show a long string of characters copy that immediately and paste it somewhere safe okay don't share this key publicly don't paste it in future video don't commit it to a public git repository it's like a password it's tied to your google account someone else gets it they could use up your free app i quota for the video or selling you won't be able to use it or cut away when it's on screen no to edit it please can you do that okay so i have it i want you to give it and i i i i'm going to copy i want you go to key copy you back back a a load cold codestop buildbuild i've got a couple what i do i do next so no

**32:21** the open terminal these three commands make directory you track cd you track and clone okay so i already done that actually great so i'm in a new subdirectory and run clone okay one clone clone clone clone run you'll see the prompt paste something like this i want to build the youtube metadata tracker at starter at track and just copy and paste you'll see pasted text lines onto nine nine i p i k is and i use the board thing here then just hit enter and watch it work two tips to your post time don't try to be perfect with a prompt you can always they actually can you change text words that's that's the whole point it's a conversation not a one shot

**32:51** and read what it's doing even if you don't fully understand the code I agree you'll start picking up patterns naturally and if you see something you're curious about just ask it hey what is this line you you right there in the code okay so can see like this is what clockwork is now doing I'm I'm like things is going to happen ah and see let's see a listing one directory ok yeah I'm in directory let me build the trainer of python script default atturn and html patience is key ah if I don't know what python was or what html was again I would just be like copy I interpreted what does this mean

**33:21** oh shit now is all this code oh my god intimidating it's code it's code it's code I'm totally terrified about okay so it's creating a file fetch video spy fetch latest videos from mutual channels using the data API b three okay they're doing all of this stuff is writing all this code API key based URL channels automatically for a format deal cool okay at this point this will feel like fiction and so people will stop doing because they'll be intimidated by the fact that it's writing code but trick is to not get intimidated by the fact that it's writing code

**33:52** as you're browsing code you don't need to understand what every single line of the code does but the AI will usually do a good job and this is what could develop as you as well as commenting the code as they go along so I'll help someone reading the code further understand the gist of the code is trying to do okay cool for a channel get the output playlist for each channel ideas that make sense can the latest video ideas from playlists okay have them make sense can the for details relate to video ideas ok ok okay so all the stuff for the videos my view count is sending ok so do i want to create this file

**34:23** i i'm just creating a file not actually running it yes i i'm to take yes if i wanted to i could copy and paste into Claude and i can you explain everything along the code and i i think about Claude Code is that i'll give you the tips for using Claude Code as you go along like use slash b w w to ask quick question without interrupting Claude's current work i i use that a lot a a a an you can just come to the chat and just ask the questions there i i you going to do to to on a sky i get Claude Code to build the stuff and i use Claude chat i i i understand things as a building stuff okay now you're running about current work this command about the approval so python three fresh videos fresh video to p a

**34:56** this command requires approval this is where unlike no a acis command okay it seems like a kind of run this as a batch command is this something i should be concerned about i making a big deal of the security things like because because i see so many comments from people on YouTube being like oh my god security as like lei it all this is exactly what was to happen it's great example of how it works but it's finish writing a popoand hoppof a blod a bloa asking video approval it's just running the code at road atatatata great let allow it run the the and and ok so it's running the command fish video s of p y but then what happens it's fetching a a the all

**35:26** patching tomas s ank plus five lines control l to expand and what happens thirty contcontrol i does matter of thirty with videos fetch okay now it's going to ask me me for commission math command preview top five video by view count by view count doh at this point of a ok i'm just going to to cable because that's it's to reasonable i i'm an verify the data looks i it's king perfectly he what what was built fetvivideo a p p hthe the youtube data api i was the latest ten videos from each channel s ws ws for the channel name it's a applicable a lua index or h t ml dog seemed ed ed display that read of the videos jason ws ws some new title view count bad channel name time ago that that seera oh interesting

**36:03** to view a web page open it via a local server needed for the fresh clone of a json file three m h t t p server eight thousand then open localhost in your browser what would you like to add next now and like okay this is confusing what the heck is going on here so i'm going to you know what i don't don't need to come pastative way what's me understand what this stand what what's a local server the first time you try to create an http server and running things on localhost you might be that confused as what the heck is going on but if just ask ask to explain it to you you understand what

**36:34** this is what local server and then you want to worry about again again good question let me break it down simply the problem when you drop index.html to open in a browser the page tries to load video.json using JavaScript browsers block this for security reasons when opening file directly from your computer i i like to test this if i go to find folder ah when i look at my you tube track folder i see three files i see fetch video.js i see index.html and i see video.json turns out i can actually open all these files and i can verify by going on and if i open this with and i i tested it or something

**37:05** a sick was was the code of the cloud group for me okay nice if i look at index.html i can open it in a code reader and i can read like readers or this HTML code whatever and then i can look at video that jason i can open it with text editor it have plainly that loaded i can see all it's basic readers data video i d title from new sick kay channel name from sometimes also channel name times ms from channel name the okay kind of rdsk know what happens i just trying to open index.html run load videos run python three fresh video of your life okay so it's not working

**37:38** but but Claude already knows that it's not gonna work because it knows that this is problem problem so solution python3 -m http server starts a tiny web server on your own computer and makes your files available at local host 8000 which is a URL the browser trust so their fetch works local hosts is your own machine nothing routes to the internet so nobody else can connect a nobody else to stand and a random number while the server needs to be ongoing and only runs while the terminal commands active you can control it to stop with Ctrl+C nobody else can see it as just local local only to do up for short to nobody else asking me to run this bash command

**38:10** python3 -m http.server 8000 okay sure so it was running open this new browser local host 8000 okay i i if it works when a copy and paste this URL open it in my browser localhost 8000 ow

**38:25** that was really cool look i've literally just opened this in localhost eight thousand and i can see that we have automatically scraped data from thomas frank mattieella and me oh i see we've scraped some short youtube shorts for me that was not my intention uh i like ows and then i can filter it wow at that we have just created an online dashboard that's running purely on a local machine but when one on the network has access of this but then one because it's on local host but if i wanted to make this accessible by the web what do i do an online call

**38:55** um but this is on local host um how do i make this accessible on a website so that my team can have access to it because this is really nice and then cloud will teach me all about what deploying stuff to the web means and then i can ask more questions about it and i can deploy it to the web and i haven't actual website and then i might it to it but like i don't use one in the world to be able to see it the website like you know how do i prevent people from accessing it and then it will teach me about authentication and say that you should just add a user a app pass but i would like how do we do and you'll tell you you can do it manually or you can use google's old o auth but or you can use the rule authentication i be like what the how is a google of

**39:27** understand about that and now before you know it I have built it into a fully fledged web app that only me and trusted people have access to or if I want I can allow anyone access it and make an account I could even get them to pay for it if I wanted to make a paid app by just asking cloud t y I'd like to make this app available to page subscribers I want to be I want to charge nineteen dollars a month how do we make it happen and and it will happen uh great great way of thinking about it what you want is a billing app I make a stripe account I'm on stripe account making account give me an API and I'd it all up for you now anyone in the world can sign up for your app that can only use if they pay you nineteen dollars a month

**39:59** amazing you've now built a web app SaaS a software as a service that could potentially make you some money you have not needed to know anything about how to code in order to do this because all you've needed to know is how to talk to Claude how to be curious to ask Claude to explain stuff that you don't know the answer to and the little skill of being able to push through the small frictions that you will encounter okay so anyway how do I make it a SaaS version of the website versus the easier thing one command deploys it to or you are all like you tired of the site how are you fear of getting visitors sick even I need to pay for it

**40:30** get it the pages push to get her her possible pages settings free okay nice neatly finement of very nice all three static files for free the one thing think about right now the data is a snapshot to step by step fresh with set up to get up action which runs a script on a schedule and redeploy them automatically which option sounds you you I recommend for yourself and how fast to get running nice and in the process of building the thing we are learning about how websites to build your friends how deployments work at platform and before you know it you will be so far ahead of your previous self will be so far ahead in terms of understanding the ship compared to your friends

**41:01** didn't give it the time that like you will feel like a different person i feel like a different person now than i did two months ago when i first started discovering the stuff and i know how to code i've been putting it in since i was thirteen and built a lot of service myself wasn't particularly but like you know me and my brother had built stuff when we were at university that was making like hundred and fifty thousand dollars years and revenue it's not it's not but it's not like million but it's it's it's not bad to like university kids i knew how to code and still my mind been freakin blown by the power of cloud code the power of just being able to speak to the AI to get it to interview you about what to build that saves you time and makes you money

**41:33** helps you follow your curiosity to understand things like web servers of various in a situation this one funky stuff push through the friction associated with dealing with an API and stuff like that and before you know you've built some really cool stuff that usually add value to your life your customers your your boss's life if you want to try to get a raise at work you then start realizing all of the cool stuff you can build to automate aspects of your life and save you time it's so cool uh a time to be alive showing anyway before we do this thing you i'm like i want to look at this page i'm like i this is mine but i don't like the fact that youtube shorts are showing

**42:03** okay let's forget about the web developer for now i don't like the fact that's showing youtube shorts i don't really care about youtube shorts i only want to show long form youtube videos

**42:12** let's see what Claude says I'll try to shorts by checking video duration shorts of sixty one just need to pull content details and KPI and switch videos six do you want to make this edit to fetch video of PY okay well ok now here it's like green means it's adding it and red means removing the line so here it's like fetch for channel thirty here this more tentative all confeal all confututo all are are you sure do you want to make this edit ok so it's removing some stuff adding some stuff ok it's something residual yes that's a good meme of like what it feels like to be using code all these days here this

**42:46** I run the fetch script that's fine number really getting my mind like a lot of this is his personality uh you you recently expanded shots to be three minutes long so let me bump the filter to exclude the things less than three minutes fifty five out out it took a few attempts to figure out but it figures out as you doing the sorting stuff but you're really out is that you know while we're doing things so be your challenge to figure out what you do well waiting for it to do stuff so what you do so you either chat out or think about life or like a this a meditation and mindfulness or you do what all the pros do

**43:18** and you create a second terminal window so while the first one is doing working on one feature or one thing you've got a second clone instance that that's working on another thing and then you realize that you still have time on your hands so then what you do is you have four terminal windows open each of which you're running a different instance of code code and you're working on a different feature for each one you're wondering if you try to work on four terminals for the same feature because then they step like not realizing that each other are working on the same files i i we are counting but like you keep things simple you start off with one you realize with diminishing i can just be twice productive if i had another window open so then you make a new terminal window you just sticking the the side of screen like this one

**43:56** you do this one like this, then you zoom out and now you got one terminal window there, you even in here because you don't like that, but you don't like to read and code over here. And now we have another another code code window here, and then you're doing stuff here, you're like doing stuff here, you're working on a feature here, working on something there, and then you're doing stuff, you're like actually to your time, and eventually you get to this four-way set up where you do windows like this, this kind of thing, where you have a terminal window here, a terminal window or the top of the terminal window, or you have everything, everything of a terminal window all over the place. I literally just bought a fifty-two inch Dell ultra sharp monitor for the sake of being able to have multiple terminal windows

**44:28** because my max to do just labour which is like using my laptop anyway um okay open localhost:3000 in your browser or copy to window and see what happens it worked nice so now the shots have been got rid of amazing that's cool see you I mean this is an interesting thing it's just waste token to cost but I like a mental cloud when it's doing a job but let's work and let me know what when you want to build on it things like adding more channels or refreshing the data or deploying it for your team now this is a very basic use case but you just start without anything about how to code

**44:59** literally by asking Claude to interview me about what i do that i find annoying download Claude code try to understand what comments it's getting me to do i have just built this dashboard and this is so so so ridiculous basic this is like the most basic thing you could possibly build and it's still ridiculous and a great thing about this is that you know i'm really not sure what i want to build on top of this you you ask me some questions and help me figure out like what what we should build you the same thing is when you build a i stuff you don't want to build stuff for the sake of it you want to build stuff that actually helps you in your work or in your life

**45:30** so for example you want to build things that add value to your customers or that save you time or that make you money and generally Claude is very smart and helping you figure out what that stuff actually is

**45:38** here you go a few questions what's the goal and you track competitors to learn from content strategy or is it more about benchmarking your performance against this quick questions what decisions does this help you make when you look at this data for what do you wish you could immediately answer for example what topics are trending in money right now or which of my competitors is growing the fastest who and your team introduce this how many channels you want to track how often do you check this this daily weekly before a weekly meeting that affect that that we need all regular notifications of it's sure okay how is more tedious the session good very how how per person's business business start with whichever question feels interesting we don't need to answer all of them in every person's job and and person's business there is annoying tedious work

**46:10** that needs to be done which is so so so easy to automate these days and the way you access this power is that you spend a few hours you spend a weekend just choosing to go through the friction of like setting down with a terminal window talking to cloud and asking cloud how can cloud help you make more progress in your job or in your life in your business help you save time help you save your money money is an incredible time to be alive okay if you go to the end of this video i would love to see a comment video did you find this useful you and hopefully it if you go to the end of video um but i would really love to know what more would you like gacy in article ai education series

**46:41** i'm diving deep into all of this stuff i love doing like trials about knowing this this stuff because this is the future of productivity back in the day it was like notion notion and art to change the game for people like productivity set up and stuff like that before then it was to be like how to type really fast but now it's about like how to use ai tools and how can you make really good money just by using incredible tools about this i would love to make a video about this and i would love to know what you guys would find interesting or useful this this and i would like to make this video and if you want to see another video about how specifically i use ai and a whole suite of tools to improve my own productivity within the business context check out this video over here

**47:12** thank you so much for watching and i will see you in the next one bye

---

内容效果不满意？[点此反馈](https://feedback.notebooksyncer.com/feedback/b61f2187-9916-48b2-b4be-8dd0340cb61e?u=https%3A%2F%2Fwww.xiaohongshu.com%2Fdiscovery%2Fitem%2F69fde2da000000001a035a7d%3Fapp_platform%3Dios%26app_version%3D9.32.2%26share_from_user_hidden%3Dtrue%26xsec_source%3Dapp_share%26type%3Dvideo%26xsec_token%3DCB7E7pqs0kRZqI9MKPhwYappeWEaKwjcoYGndxAbbbB0o%3D%26author_share%3D1%26xhsshare%3DWeixinSession%26shareRedId%3DNzs4RERHO0tLPD1GOjswPEg5Qk06PjpN%26apptime%3D1780090790%26share_id%3D4fbfe933d47b4a08a5eab35498b9dcaa%26code%3D40bK2WRPM8p&s=vtoa)