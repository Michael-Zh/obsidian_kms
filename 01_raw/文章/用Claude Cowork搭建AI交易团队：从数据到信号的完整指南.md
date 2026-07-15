---
author: chia Y
source: AI整理 - 小红书
url: https://www.xiaohongshu.com/discovery/item/6a1c8743000000003501d960?app_platform=ios&app_version=9.34.3&share_from_user_hidden=true&xsec_source=app_share&type=video&xsec_token=CBwXLGrbKVK_LyrlOyCaQsdbjZE_3wa-bcIb4StmVbMNg=&author_share=1&xhsshare=WeixinSession&shareRedId=Nzs4RERHO0tLPD1GOjswPEg5Qk06PjpN&apptime=1781908712&share_id=af7c7c8ed2af43dba5ee0a716c21a451&code=8J2pN2zxFRz
saved: 2026-06-20 00:38:55
tags:
  - 笔记同步助手
annotation: Use Claude for investment
id: 5485b3f3-cd13-43ab-9e88-960d6e6bf037
---

# 用Claude Cowork搭建AI交易团队：从数据到信号的完整指南

作者：chia Y

本笔记整理自视频教程，记录如何利用Claude Cowork构建一个由四个智能体组成的AI交易团队，自动完成数据采集、宏观分析、组合策略和交易信号生成。无需编程背景，仅需付费订阅Claude Cowork即可。

## 1\. 为什么需要AI交易团队

机构交易员拥有完整的团队（市场研究员、风险分析师、执行监督），而个人交易者通常只靠直觉和图表。本教程旨在用Claude Cowork搭建AI团队，弥补个人短板。注意：这不是一个自动浏览新闻并执行交易的“交易机器人”——单纯浏览新闻只会增加噪音。正确做法是：接入可靠的金融数据源，让AI基于真实数据（而非市场情绪）进行评分和分析。

![[01_raw/_inbox/文章/images/7ec33ce6eeef5ee18f243976ba50c4ba_MD5.jpg|开场：机构与个人交易者的对比]]

开场：机构与个人交易者的对比

## 2\. 数据源选择与工具准备

### 2.1 数据源

-   **Yahoo Finance**：用于获取市场数据（股价、成交量等）。
-   **FRED（联邦储备经济数据）**：用于获取美国宏观经济数据（CPI、通胀率、失业率等）。两者均为免费。

### 2.2 必要条件

-   安装Claude Cowork（桌面端）。
-   需要付费订阅才能使用Cowork功能。
-   在FRED官网注册账号并申请API Key。路径：My Profile → API Keys → Request API Key（填写用途如“analysis/research”），复制生成的密钥。

![[01_raw/_inbox/文章/images/752c42afa0d6327a1f74f4a22952e93c_MD5.jpg|FRED网站API Key申请页面]]

FRED网站API Key申请页面

## 3\. 安装环境依赖

### 3.1 macOS用户需先安装Homebrew

访问 brew.sh，复制安装命令。在Claude Cowork中打开Terminal（Code → 新Session → 右上角Dropdown → Terminal），粘贴命令并回车安装。可能需要输入Mac解锁密码。

![[01_raw/_inbox/文章/images/72b17a5eb9a06e94dcd02a08ab03b950_MD5.jpg|在Claude Terminal中安装Homebrew]]

在Claude Terminal中安装Homebrew

### 3.2 安装UV（Python包管理器）

在终端输入：`brew install uv`

![[01_raw/_inbox/文章/images/3703eff5a18bb9b23af7c58e3b745477_MD5.jpg|安装UV命令]]

安装UV命令

## 4\. 配置MCP服务器（数据连接器）

进入Claude Cowork设置：Profile → Settings → Developer → Edit Config。打开`claudedesktopconfig.json`，在其中添加Yahoo Finance和FRED的MCP服务器配置（具体脚本见视频描述）。保存后重启Claude，即可在MCP服务器列表中看到两个连接器运行。

![[01_raw/_inbox/文章/images/1f2745e30956b6d0b4d6f1007ace4013_MD5.jpg|编辑config.json添加MCP服务器]]

编辑config.json添加MCP服务器

![[01_raw/_inbox/文章/images/118393496cc85fcbac9fab61c081bc4a_MD5.jpg|MCP服务器运行状态]]

MCP服务器运行状态

## 5\. 设计AI交易团队的四位智能体

### 5.1 数据智能体（Data Agent）

**性格：**冷静、负责、结构化

-   **首次任务：**拉取2年历史数据，写入Excel的“历史数据”工作表，供后续回测。
-   **定时任务（每小时）：**从Yahoo Finance获取固定股票池（如前20大美国科技股或5只指定ETF）的OHLCV（开盘、最高、最低、收盘、成交量）数据，写入“市场数据”工作表。
-   **每天：**从FRED获取宏观数据（CPI、通胀率、失业率等），写入“宏观数据”工作表。
-   数据智能体会检查数据质量，通过后通知项目。

### 5.2 研究智能体（Research Agent）

**性格：**好奇、大胆、数据驱动

-   **定时任务：**分析市场数据的波动率模式、成交量异常、相关性变化，标记显著偏离；分析宏观数据，给出当前经济体制（扩张/收缩）的叙事；检测潜在需求信号（如基于航运数据的实物需求）。
-   **报告时间：**每天上午7点（盘前简报）和晚上11点（后市总结）。
-   **输出：**Research Report（Markdown文件），包含宏观叙事、波动率发现、模式标记、需求信号，以及为投资组合智能体提供的三个最佳思路。

### 5.3 投资组合智能体（Portfolio Agent）

**性格：**直接、野心、冷静、聪明

-   **首次任务：**与用户进行完整访谈，了解投资偏好和财务状况。
-   **每周一：**发送5个轻量问题，确认是否需要调整策略。
-   **定时任务：**提出一个策略调整方案（包含假设、入场逻辑、出场逻辑、仓位大小）。经用户确认后，将策略以机器可读方式写入文件，供信号智能体直接使用。
-   **输出：**Portfolio Strategy（Markdown文件）。

### 5.4 信号智能体（Signal Agent）

**性格：**敏感、冷静、批判

-   **定时任务：**读取并理解策略规则，结合当前宏观体制和技术指标触发信号；将信号反馈给投资组合智能体，用于回测。
-   **输出：**Signal（Markdown文件）。

![[01_raw/_inbox/文章/images/02bc374f2a0e4f45f62e036743c0e82e_MD5.jpg|四大智能体架构图]]

四大智能体架构图

## 6\. 智能体之间的数据流（Handoff）

明确每个智能体读取/写入哪些文件：

-   **数据智能体：**从Yahoo Finance和FRED数据连接器读取 → 写入Market Data Excel文件。
-   **研究智能体：**读取Market Data Excel + 网页搜索 → 写入Research Report Markdown。
-   **投资组合智能体：**读取Research Report + Market Data Excel + 用户输入 → 写入Portfolio Strategy Markdown。
-   **信号智能体：**读取Portfolio Strategy + Market Data + Research Report → 写入Signal Markdown。

![[01_raw/_inbox/文章/images/cc7253021f2818777aaf7fbab18db3e1_MD5.jpg|数据流示意图]]

数据流示意图

## 7\. 在Claude Cowork中创建项目

### 7.1 新建项目

回到Claude Cowork → 点击“Start from scratch” → 项目名称“AI Trading Team” → 指令留空（后续生成） → 选择本地文件夹 → 建议开启Memory（让AI记住你的偏好） → 创建。

![[01_raw/_inbox/文章/images/0c14213b5dd5b6599095e064b9287eb3_MD5.jpg|新建项目界面]]

新建项目界面

### 7.2 通过聊天让Claude创建智能体文件

在聊天窗口输入每个智能体的详细描述（包括性格、任务、输出），要求Claude为每个智能体创建一个Markdown文件，并生成所有配套文件。建议使用Opus模型（如Opus 4.6/4.7）进行首次设置，后续定时任务可使用较便宜的模型（如Haiku、Sonny）。

![[01_raw/_inbox/文章/images/3776db13c8c915bc8a964b54daf53c4f_MD5.jpg|在聊天中让Claude创建Agent文件]]

在聊天中让Claude创建Agent文件

### 7.3 生成项目指令（Instruction）

将上述智能体描述和Handoff总结复制到聊天中，要求Claude生成一个`claude.markdown`文件作为项目顶层指令。指令会告诉所有智能体“做什么、何时做、如何做”。

![[01_raw/_inbox/文章/images/c6fa2947cf447d82b3d37ece5466871a_MD5.jpg|生成Instruction过程]]

生成Instruction过程

### 7.4 创建定时任务

将表格形式的任务安排（每个智能体的触发时间）粘贴到聊天中，Claude会自动创建相应的Scheduled Task。完成后，只要电脑开机，定时任务就会按计划运行，无需手动触发。

![[01_raw/_inbox/文章/images/c3d05cc4328fc48bfa3d2a976175cc25_MD5.jpg|设置定时任务]]

设置定时任务

## 8\. 测试与优化

创建完成后，逐个点击Scheduled Task中的“Run Now”进行测试。如果失败，与Claude讨论修复。确保所有数据流正常后，第二天即可收到自动生成的报告。注意：要给予智能体一些时间“磨合”，才能产生更优质的分析结果。真正盈利的策略不会公开在YouTube上，需要你与AI交易团队一起开发。

![[01_raw/_inbox/文章/images/38cc4455f34331c7b927f521016f766a_MD5.jpg|运行测试任务]]

运行测试任务

## 9\. 注意事项

-   首次设置时使用最强模型（Opus），后续日常任务可用更经济的模型。
-   数据质量检查很重要，确保只有通过检查的数据才被后续智能体使用。
-   定时任务依赖电脑开启状态（Claude Cowork需保持运行）。

## 逐字稿

**00:00** Institutional traders have an entire team behind them.

**00:03** They have market researcher, they have risk analyst, they have execution oversight.

**00:08** But you and me will only have our gut feeling and the chart.

**00:11** That's not enough.

**00:12** So today I built an AI team with Claude Code Co-Work.

**00:16** After today's video, you will also have one team.

**00:19** To start, this is not a trading bot that browse all the finance headlines and make

**00:23** guesses and trade for you.

**00:25** If your agent only browsed the headlines, it will only add up noise to your trade.

**00:30** So what we're doing today is find valid data source and use that as the main power technical

**00:36** indicators.

**00:37** That's what we're looking at.

**00:38** We'll plug the data into Cloud and use it from there.

**00:41** So instead of AI talking about the market, we ask AI to rate the actual data for us.

**00:47** Yahoo Finance will be used to rate all the market data.

**00:51** And Claude will be used to rate all the US macroeconomy data.

**00:55** And why I want to use Claude as the brand of our agents?

**00:59** If you look at the benchmark, Claude is ranking the top on almost all the domain like

**01:06** finance, physics, math.

**01:08** And those domain is really important for trading.

**01:11** Now let's start with the first part.

**01:12** You need to have a Claude Code installed on your computer.

**01:15** And remember a paid subscription is required to use Claude Code.

**01:20** Now let's open up Claude.

**01:22** So here you can see there are three tabs.

**01:24** The chat, Claude Work, Code.

**01:26** I have a quick introduction.

**01:28** Chat is for chatting on ad hoc ideas.

**01:31** Claude Work can do things for you in an agentic way.

**01:34** Code is for building something like software or dashboard.

**01:37** Today we will create our team in Claude.

**01:40** Claude Work.

**01:40** It's project based.

**01:41** So everything is organized in a project.

**01:44** It feels like you put everything you needed in the same box.

**01:47** And just like you work in a company, if you carry on the project, most likely there will be a lot

**01:53** of tasks.

**01:54** There are two types of tasks you can create in Cloud Work.

**01:57** The scheduled task or the ad hoc task.

**02:00** The scheduled task can be created here.

**02:02** If you click scheduled on the right side, you can see this new task button.

**02:07** Then the task will be triggered by the frequency.

**02:10** Let's say if you set up daily, then it will run daily.

**02:14** And you can also create some ad hoc task by just hitting the new task.

**02:18** In the Cloud Work, you need to give the project an instruction.

**02:22** It's like the top level cooking menu.

**02:25** It will tell all the agents live inside this project what, when, and how to do things.

**02:30** And the instruction is just plain English.

**02:33** The best way to create an instruction is to write with Cloud.

**02:37** So we covered the workspace, which is the code work for our agents.

**02:41** Now the data for our agents.

**02:43** We have two data sources and both are free.

**02:46** One is Yahoo Finance for market data and Fred for macro economy data.

**02:52** I will put all the links and scripts in the description down below.

**02:56** First, we need to register an account in Fred.

**03:00** Let's get into the webpage for Fred.

**03:03** And we need to register our account.

**03:06** You can see here, I already have my account.

**03:09** So just click on my profile.

**03:12** And you can see there is a tab for API key.

**03:17** Just click the API key.

**03:19** And here you can see a button with the plus sign says request API key.

**03:25** Click that.

**03:25** And here you need to give it a short description on what is this API key used for.

**03:34** Just write you use it for analysis or research.

**03:37** So now if you are in the same page, you will have the API key.

**03:42** Under this API key column, you can see this very long string.

**03:47** Just copy this and save it somewhere safe.

**03:50** We're going to use it later.

**03:52** If you are using Mac, you need to download a thing called brew.

**03:55** Go to this website brew.sh.

**03:58** Copy this line of code.

**03:59** We will go back to cloud.

**04:02** If you click the code and just create a new session type anything.

**04:06** On the right corner, you can see there is a drop down.

**04:11** Click terminal.

**04:12** Paste whatever you have copied from the brew website here.

**04:16** Return.

**04:17** Now it will start to install brew.

**04:19** If you don't know what is brew, it's just a thing to manage all the hidden software on your computer.

**04:23** You probably need to give it a password if you have a password to unlock your Mac.

**04:28** So we have it here.

**04:29** And next we need to use something called UV.

**04:32** Just type this line in the terminal again.

**04:35** Brew install UV.

**04:37** And hit return.

**04:38** And it will start the installation.

**04:40** The next thing we need to do is go into cloud and click on your profile and go to setting.

**04:46** And under developer, there is something called edit config.

**04:52** Just click this.

**04:53** And when you click edit config, it will show up a clouddeskupconfig.json.

**05:00** It may look a bit complicated, but don't worry.

**05:03** Just open it.

**05:05** And now you can see a lot of text and some brackets.

**05:09** And put this screen.

**05:39** tab you can see you have two mcp servers running and if you don't know what is mcp it's just two

**05:45** data plug the yahoo finance and FRED data connector will also show up here all right now we're all

**05:52** set with the data part now it's the most exciting part we need to design our agent in a trading team

**05:58** we're going to have four agents the data agent the research agent the portfolio agent and last

**06:03** the signal agent let's start with data agent we need to give it a character when you're talking

**06:09** about data you normally want it to be very reliable so the character i gave it is calm responsible and

**06:17** structured there are two types of tasks for the data agent the first type is the starting task

**06:23** when we first start the project the data agent will put two years data it will write the data to

**06:29** historical sheet in market data excel portfolio agent can use it for back testing and then it has

**06:36** recurring tasks it will collect hourly open high low close volume data from yahoo finance for a fixed

**06:43** universe for example the top 20 us tech stocks or five designated etf the data agent will write the

**06:50** data to market data excel sheet second task for the data agent is to collect the daily macro data from fred

**06:58** data for example the CPI data the inflation data unemployment rate it will write the data to a

**07:05** separate sheet called macro data the data agent will check if the data quality is good it will notify this

**07:12** project when the data passed the quality check and the second agent is researcher agent it's like an idea

**07:18** generator so just think of someone who is really creative i gave the agent the character curious bold and

**07:27** data driven this agent has some recurring tasks first one is analyze the market data volatility patterns

**07:35** of normal volume some correlation change it will flag all the significant deviation besides the market data

**07:43** the researcher will also analyze the macro data and produce a narrative under the current economy regime

**07:50** is it expansion or contraction the agent will also try to detect the underlying demand signals for example

**07:58** the physical demand based on shipping data the our research agent will report every morning 7 a.m pre-market

**08:05** brief also 11 pm after the synthesis and the output file will be a research report that md file in this

**08:13** file it will give us the macro narrative the volatility findings the pattern flags on demand signals

**08:19** and it will come up with three top ideas for our portfolio agent next one is our portfolio agent think

**08:27** of someone who is managing all your assets as a portfolio manager and the character i give this agent is

**08:34** direct ambitious calm and smart on the first round it will conduct a full interview with you to get your

**08:42** investment preference and also the finance situation and every monday it will run a five question

**08:48** light will check with you to know if we need to adjust the portfolio strategy portfolio agent also have

**08:54** recurring tasks the agent will try to propose one strategy adjustment the proposed adjustment will

**09:01** include hypothesis the entry logic exit logic also the position size after the weekly discussion with

**09:09** you it will write down the strategy into a machine readable way so the signal agent can use it directly

**09:16** output file will be a portfolio strategy as we talked about so last but not least the signal agent the

**09:23** character I gave to this agent is sensitive calm critical and the recurrent task for this agent is to

**09:31** first read and understand the strategy rules it will combine current macro regime with the technical

**09:37** indicator to trigger the signal and it will also give the signal back to the portfolio agents so the data can

**09:43** be used for back testing again now we have our full ai trading team we need to give more specific guidance

**09:50** on how they work together there are so many files inside this project so we need to tell co-workers which

**09:56** agent is reading which file and which agent is writing which file the data agent will read from yahoo finance

**10:04** and thread data connector and then it writes to the market excel file and researcher will read from the market

**10:13** excel file plus the website searching and write to the research report markdown file and the portfolio agent and it will read the research report markdown file the market data excel and some user input and it will write to the portfolio strategy markdown

**10:31** the last signal agent will read the portfolio strategy market data research report and then write to the signal markdown file we have the handoff clear so now what we need to do is paste all this description for our agent

**10:47** give it one by one to claude code final step let's get into the practical part get back to claude code we need to create a new project click start from scratch

**10:59** and now you need to give it project name ai trading team so here is the instruction that i mentioned in the beginning

**11:06** it's like a top level menu you give to the project we will just leave this part empty for now choose a location you

**11:13** want it to be just use you can use any folder on your computer and memory on i would prefer to have memory on

**11:21** because the ai will know you better and then we click create you can see there is a chat window and

**11:27** instruction on the side scheduled context and we are going to create this agent team

**11:32** by chatting with Claude and here is the details of all our agents and you can also be very explicit

**11:39** just to tell Claude to create a markdown file for each of your agents and now Claude will start to think

**11:45** and create all the markdown files for me also all the files used by the agent it has a very clear progress

**11:51** on the right side to tell what it's doing now to set up this trading agent team if you just get started

**11:58** with Claude I would recommend to use the Opus model Opus 4.6 or Opus 4.7 those are smartest models and you

**12:07** always want to use the best model to set up your project if you're just running some repetitive tasks

**12:13** use cheaper models like Haiku or Sonnet Opus is good but it's also very expensive token wise all right now we

**12:19** have all the agent files also the output files team overview thing is all the output file they live in

**12:29** the folder there is no instruction created let's give the claude the story we have and ask claude to create

**12:36** something instruction format we can use i will just copy paste the handoff summary and the full story

**12:44** and in the chat i will just say can you help me create an instruction for this project based on the

**12:50** following handoff and the full story use the claude.markdown file and what should the instruction

**12:58** focus on while we're waiting the last thing we need to do is to ask claude to create a scheduled task

**13:04** for us so it will be a fully automatic team without your guide you don't need to ask an agent to work they

**13:11** will just start work based on the schedule as long as your computer is on so now the instruction is

**13:17** ready the claude.markdown file will work as the instruction now what you do is ask claude to create

**13:24** a scheduled task for us just copy paste the table we had before into this chat and then claude will help

**13:30** you create the scheduled task I will just try to run now to test if everything works in our project

**13:38** and now it's running collect all data and try to store the data in excel so now you have all the

**13:44** scheduled tasks set it up what you need to do is go into each of the scheduled tasks and try to run now

**13:51** if it's not working just discuss with cloud to figure out what's wrong once you have all the scheduled

**13:58** tasks tested validated next day you will just wait for your report you always need to take your agent a

**14:05** little bit to make sure they produce better results better analysis you know if there is a very

**14:11** profitable strategy it will never be advertised on youtube you need to develop your own strategy

**14:17** strategy together with this AI trading team

视频时长 14分19秒 · 消耗 72 积分 · 积分余额 548

---

内容效果不满意？[点此反馈](https://feedback.notebooksyncer.com/feedback/4c75a0be-22e8-47cf-8885-db6ecc06412f?u=https%3A%2F%2Fwww.xiaohongshu.com%2Fdiscovery%2Fitem%2F6a1c8743000000003501d960%3Fapp_platform%3Dios%26app_version%3D9.34.3%26share_from_user_hidden%3Dtrue%26xsec_source%3Dapp_share%26type%3Dvideo%26xsec_token%3DCBwXLGrbKVK_LyrlOyCaQsdbjZE_3wa-bcIb4StmVbMNg%3D%26author_share%3D1%26xhsshare%3DWeixinSession%26shareRedId%3DNzs4RERHO0tLPD1GOjswPEg5Qk06PjpN%26apptime%3D1781908712%26share_id%3Daf7c7c8ed2af43dba5ee0a716c21a451%26code%3D8J2pN2zxFRz&s=vtoa)