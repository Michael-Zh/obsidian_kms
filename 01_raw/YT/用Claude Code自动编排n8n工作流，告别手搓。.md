---
author:
  - "[[杰森的效率工坊]]"
source: "YT"
url: "https://www.youtube.com/watch?v=XrCifDo8Rdo"
saved: "2026-06-06T20:35:12+02:00"
tags:
  - "YT"
published: 2026-03-31
description: "n8n被智能体淘汰了？大错特错，在智能体时代，n8n才是最佳搭档。把所有任务都交给大龙虾才是致命的，Token消耗极度夸张不说，还有极大的安全隐患。社区普遍共识就是把 n8n 作为后端执行器，接入智能体。并且，使用n8n mcp，n8n skills，在 Claude Code 中，可以让智能体直接帮你生成工作流。不用再手动拖节点，把固定流程放入工作流，节省 Token、保住密钥安全。"
id: "用Claude Code自动编排n8n工作流，告别手搓。"
annotation: "pov: n8n vs opencode"
summary: "Tutorial showing how to use Claude Code or OpenCode agents with n8n MCP and n8n Skills to automatically generate n8n workflows from natural language, replacing manual node-dragging. Argues that the community consensus is to use n8n as a backend executor (called via webhook) rather than having an agent execute every step directly, reducing token costs and protecting API keys stored in n8n."
---
![](https://www.youtube.com/watch?v=XrCifDo8Rdo)

n8n被智能体淘汰了？大错特错，在智能体时代，n8n才是最佳搭档。  
把所有任务都交给大龙虾才是致命的，Token消耗极度夸张不说，还有极大的安全隐患。  
社区普遍共识就是把 n8n 作为后端执行器，接入智能体。  
并且，使用n8n mcp，n8n skills，在 Claude Code 中，可以让智能体直接帮你生成工作流。  
  
不用再手动拖节点，把固定流程放入工作流，节省 Token、保住密钥安全。  
这期视频带你完整跑通智能体（Claude Code / OpenCode）+ n8n MCP + n8n skills，自动化编排工作流。  
  
时间戳：  
00:00 为什么在智能体时代，我们还需要 n8n？  
00:58 n8n 环境搭建与隐藏节点解锁 (npm/Docker 部署方式)  
02:17 创建 n8n API 与本地配置大模型密钥  
02:59 Claude Code 安装与国内转接大模型配置  
03:57 核心步骤：n8n Skills 与 MCP 的配置文件修改  
04:34 OpenCode 桌面端安装与配置  
05:58 实操演示：让 Claude 自动创建谷歌 DeepMind 论文情报抓取工作流  
07:49 注意事项：节点报错处理，以及先计划后执行。  
08:36 实操演示：用 OpenCode 创建 OpenAI 资讯追踪自动化  
09:40 成本与安全核算：为什么坚决不用 OpenClaw 大龙虾直接跑固定任务？  
11:34 总结与资料获取  
  
视频里用到的配置文件、环境搭建代码和 AI 提示词，我已经全部整理在我的个人网站里了，去频道主页就能获取。  
  
记得点赞订阅~  
  
#openclaw #n8n #claudecode #opencode #agentskills #aiagents #mcp #ai

## Transcript

### 为什么在智能体时代，我们还需要 n8n？

**0:00** · 在AI智能体横行的时代 N8N工作流并没有被淘汰 相反它是智能体最好的搭档 比如OpenClaw大龙虾 然后国外社区最普遍最认可的 方式就是与n8n工作流集成 把固定性的任务放到工作流中 OpenClaw只通过Webhook调用n8n 既能降低TOKEN消耗 又能把隐私密钥封装在n8n中 降低安全风险 GitHub上也有现成的应用 案例和打包好的n8n镜像 而N8N本身也在不停地更新迭代

**0:31** · 云端付费版本提供了 AI生成工作流功能 而社区中也有N8N MCP和N8N skills 让你彻底告别手搓工作流 让Claude Code这样的智能体根据 你的需求帮你创建工作流 今天我就来为大家展示如何 使用Claude Code或OpenCode这样的 智能体工具来帮你创建N8N工作流

**0:52** · 具体的安装和配置步骤以及 提示词我都整理成了文档 最后会分享给大家 那我们就正式开始 首先是环境搭建 虽然环境搭建需要一系列步骤 但是搭建好之后就可以 一劳永逸的使用智能体创建工作流了 首先我们要确保电脑上安装了N8N 我们可以通过NPM install来安装 也可以通过Docker安装 如果你想快速进行尝试 那么NPM install是最快捷的 电脑上安装了nodejs之后 执行npm install -g n8n

### n8n 环境搭建与隐藏节点解锁 (npm/Docker 部署方式)

**1:24** · 就可以安装了 安装好之后 呃先设置几个环境变量 解锁N8N的隐藏节点和系统级能力 然后重启命令行 输入N8N然后回车 就可以打开N8N界面了 用Docker安装也很简单 下载Docker Desktop这个工具 双击安装之后 在search界面搜索n8n安装即可

**1:47** · 不过我更推荐的方式 是安装Docker Desktop之后 在一个空白的文件夹内 创建一个compose.yaml文件 在文件中输入我屏幕 上的这些配置内容 保存后在当前文件夹打开命令行 执行docker-compose up -d

**2:07** · 就可以启动n8n了 那这个方式主要是 一次性的做了一些配置 解锁了隐藏节点 并向Docker中挂载了本地文件夹 那N8N启动之后 我们来到主页面 先要做两件事 第一件事就是点击左下角的设置按钮

### 创建 n8n API 与本地配置大模型密钥

**2:23** · 选择N8N API 然后创建一个API 起一个名字 然后把创建出来的密钥复制出来 一会配置MCP的时候会用到 那第二件事就是创建credential 也就是密钥 比如你使用的AI大模型的API key 那这里我们点击左上角的加号 选择credential 然后创建 那搜索OpenAI 然后在窗口中填入AI的API key即可

**2:48** · 那你可以使用DeepSeek GLM 或者任何你常用的AI 那这和你使用OpenClaw大龙虾是一样的 那做完这两件事之后 我们的N8N就已经准备就绪了 那接下来我们来到智能体工具 你可以选择Claude Code OpenCode或者 Codex Gemini CLI Antigravity都可以

### Claude Code 安装与国内转接大模型配置

**3:06** · 那我今天主要介绍Claude code和OpenCode的桌面端 那安装Claude Code也很简单 我之前讲agent skill的 视频中已经讲过了 通过NPM install来安装Claude Code 安装成功后 如果你所在的地区没有被Claude所限制

**3:21** · 那么你可以直接申请Claude账号 然后登录 那如果你在受限制地区 比如中国大陆 那么你可以转接兼容 模型来跳过Claude的认证 那具体的方法就是 依次输入这4个命令 指定你转接的大模型 那我这里使用的是OpenRouter 你同样也可以使用DeepSeek或者GLM 大多数主流模型都有 兼容Anthropic的接口 我屏幕上展示的就是DeepSeek的官方 文档中兼容Anthropic接口的具体内容 设置完这几个变量之后 就可以输入claude回车来启动claude code了

**3:54** · 不过先别急 我们先配置一下skills和MCP 那首先配置skills 那很简单 我们在GitHub上搜索N8N skills 找到这个星标最多的仓库 那下载下来之后 把skills文件夹复制到你 claude的配置文件夹里 那地址就是你用户目录 下的点claude文件夹里 那其次是MCP 我们来到你的用户目录下 找到这个点claude.json文件 那在里面添加一段MCP配置

### 核心步骤：n8n Skills 与 MCP 的配置文件修改

**4:22** · 那具体的配置内容我 已经展示在屏幕上了 那其中你要把N8N API key换成你 刚才自己创建的那个API密钥 那保存文件之后关闭 我们的配置就做完了 那如果你使用的是OpenCode 我们直接下载安装 OpenCode的桌面客户端 那这个图形化的客户端是非常直观的 并且OpenCode有大量的 免费AI额度可以使用 比如最近小米新出的大 模型就在OpenCode里免费使用 那所以我还是很推荐 大家使用OpenCode的 那在OpenCode中配置skill和MCP也很简单

### OpenCode 桌面端安装与配置

**4:55** · 那skill文件夹的路径是用户目录下 的点config文件夹里的OpenCode文件夹 那创建一个skills文件夹 然后把刚才下载的N8N skills复制进来就可以了 那同样是这个文件夹里 有一个OpenCode.json 那点开之后在MCP这里添加一段MCP配置

**5:13** · 那具体的内容我也展示在屏幕上了 要注意的是OpenCode和Claude Code 的MCP结构有一定的差异 那大家如果懒得去看官方文档 那直接用我给的就可以了 同样要把n8n api key换 成我们刚才创建的key 那保存之后 我们来到智能体界面 在AI对话框中输入指令来 验证一下AI是否已经与N8N mcp

**5:37** · 和你本地的mcp实例连接成功 那输入提示词 然后AI就列出了它具备的n8n能力 以及成功连通了本地的n8n 那这个时候你要确保你 本地的n8n是运行起来的 那么到此所有的环境 配置就已经完成了 那虽然有一点麻烦啊 但是配置好之后 后续就没有任何难度了 那接下来 我们让智能体为我们实现 一个AI资讯获取的工作流

### 实操演示：让 Claude 自动创建谷歌 DeepMind 论文情报抓取工作流

**6:02** · 从谷歌的DeepMind的订阅中 获取谷歌最新发布的AI论文 并调用AI进行翻译整理 然后对数据进行格式化 保存到N8N内置的数据表格中 那提示词我已经展示在屏幕上了 那这里要注意一点 我们刚才在N8N中创建的 带有你API key的credential 我们要把credential ID发送给智能体

**6:23** · 那这样它在创建工作流节点的时候 就会使用你已经创建 好的credential密钥了 那我们先来到Claude Code 把提示词发送给智能体 那智能体就开始工作了 我在Claude Code中转接的是 智谱GLM-5-Turbo这个模型 那这个最新发布的 模型能力还是很强的 那其实这一类的任务 国产的御三家大模型都可以完成得很好 那小米最近发布的模型也没有问题

**6:47** · 那我对视频进行了一下快进 那因为智能体需要一定 时间来完成工作流的创建 那创建成功之后 它列出了所有的节点以及验证结果 那我们来到浏览器的N8N界面中 那刷新一下就能看到 最新创建的工作流了 那点进来之后点击执行按钮 那工作流没一会就执行成功了 那数据保存到了N8N内置的数据表格中

**7:11** · 我们回到N8N主页 点击DataTables选项卡 打开这个AI论文情报站表格 就可以看到谷歌DeepMind最新 的10篇文章已经被翻译好 并保存到表格中了 那包括文章标题内容简介和文章地址

**7:27** · 那我们打开谷歌 DeepMind的RSS订阅看一眼 那可以看到最新的一篇文章 标题就是这个Gemini 3.1 Flash live 那数据表格中的翻译还是非常不错的 那么到此我们就实现了工作流的创建 那全程我们都没有 自己手动拖拽工作流 而是只发送了自然语言提示词

**7:46** · 给智能体 那智能体就可以自己编排工作流了 那这里我要强调几个注意事项 那第一呢 就是如果你执行工作流的时候 发现某一个节点报错 那么你可以点开这个节点 把错误信息复制出来 然后把它发给Claude Code 那智能体会自己进行 错误排查并修复工作流 那修复好之后你就可以再次测试了

### 注意事项：节点报错处理，以及先计划后执行。

**8:09** · 那第二点就是 如果你的工作流很复杂 那么我建议你先让 智能体进行分析和计划 然后先给出方案 等你确认之后再执行 那我笔记中的提示词 就是要求AI先做规划 我确认了之后再创建工作流 那视频中我为了省事就直接执行了 那不然每一步都要手动确认 那当然呢 越复杂的工作流就越有可能出错

**8:32** · 那出错了你把错误发给 Claude Code让它修复就可以了 而OpenCode则更简单 那全部都是图形化界面 我们来到OpenCode界面 那这次我们修改一下提示词 我我们不再使用谷歌的DeepMind了 我们使用OpenAI的RSS订阅 让工作流拉取OpenAI发布的文章

### 实操演示：用 OpenCode 创建 OpenAI 资讯追踪自动化

**8:51** · 然后进行翻译润色 那提示词中 我要求OpenCode把工作流 名称命名为杰森的情报站 以便于和Claude Code刚才 创建的工作流区分开 那输入提示词之后 OpenCode就开始工作了 我们对视频进行一个加速 那这里需要注意 我使用的是OpenCode提供的免费模型 也就是小米的MIMO V2Pro模型

**9:13** · 那这个模型目前在OpenCode中免费试用 那估计过几天就不免费了 所以大家赶紧趁这个机会多用用 那么工作流创建完毕 我们来到N8N 那刷新页面 直接执行这个杰森的情报站工作流 那执行成功之后 我们来到DataTables页面 点开刚才的数据表格 那可以看到表格中多了10条记录 那这10条记录就是OpenAI 最新发布的AI文章了 那么到此 OpenCode的执行也顺利完成 那虽然智能体为你创建这个

### 成本与安全核算：为什么坚决不用 OpenClaw 大龙虾直接跑固定任务？

**9:42** · 工作流的时候会消耗一些TOKEN 但工作流创建完毕之后 你每一次执行都是非常节省TOKEN的 那类似这样的信息获取的工作流 我自己有4条 啊有爬取Arxiv上的论文 那有爬取Reddit上的帖子 也有获取OpenAI和谷歌的开发者blog

**10:01** · 以及Anthropic的blog 那像Arxiv上的论文也有不少水货 那我会让AI为我分析并打分 进行一个初级筛选 那像前几天 Kimi团队就发布了一篇有 关注意力残差的论文 那非常有价值 连马斯克都点赞 那这样的工作流有助于我 获取到AI相关的第一手资讯 那如果你不使用工作流 而是在OpenClaw大龙虾中 每天都让大龙虾给你爬取数据 发送什么每日信息日报 那么你的TOKEN消耗简直就是灾难级的

**10:32** · 那对应的工作流中的每一步 在大龙虾中都要消耗TOKEN 那更重要的是 你的很多身份验证和 密钥都直接暴露给大龙虾 那非常的危险 而使用N8N工作流 你的credential密钥是封装在N8N里的 对外只暴露API接口 那大龙虾是拿不到你的密钥的 那么类似你的notion知识库 google drive文档或者Email邮箱 就不会因为OpenClaw大龙虾自己 出错而影响你的私人数据了 那另外工作流的执行如果出现错误

**11:03** · 在N8N中是非常直观且容易调试的 是精确到具体节点的 但是在OpenClaw大龙虾 中则是非常难定位 那对于没有技术背景的 普通人来说简直是灾难 那所以把固定性的 流程编排成N8N工作流 与智能体结合使用 是目前社区普遍最认可的方式 那我屏幕上展示的 这个awesome-openclaw-usecases 仓库那就有N8N的案例 里面还有专门为OpenClaw准备的N8N镜像

**11:31** · 那大家感兴趣的话 可以直接使用 那么今天的视频内容就结束了 大家现在可以来我的 个人主页下载知识笔记 然后一步一步来实现了 你可以在我的频道信息 中找到我的个人主页 那如果你有任何的问题 欢迎给我留言 记得点赞关注 谢谢大家