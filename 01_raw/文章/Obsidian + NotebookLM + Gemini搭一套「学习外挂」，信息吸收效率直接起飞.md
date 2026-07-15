---
author:
  - "[[AI的岔路口]]"
source: "web"
url: "https://mp.weixin.qq.com/s/uCuEV6EpSYzZXDptU9MpCg"
saved: "2026-06-06T20:30:21+02:00"
tags:
  - "article"
published:
description: "三件免费工具搭建学习外挂你有没有过这种体验——收藏了 20 个 YouTube 视频、下载了 10 篇 PD"
id: "Obsidian + NotebookLM + Gemini搭一套「学习外挂」，信息吸收效率直接起飞"
annotation: "Obsidian + NotebookLM + Gemini"
summary: "Step-by-step guide to building a learning compression system using three free tools: NotebookLM as a unified source ingestion brain, Gemini connected to NotebookLM for deep analysis against your own materials, and Obsidian as long-term structured memory. The workflow filters 20+ sources down to only the 10–20% of genuinely new knowledge, using a verification prompt to confirm each tool integration before proceeding."
---
AI的岔路口 *2026年4月1日 19:45*

![三件免费工具搭建学习外挂](https://mmbiz.qpic.cn/mmbiz_jpg/G3Jzuyxj7NdbVUzrr5L3YqiaFEibrt5aKtvnInibibiakiaYRwGyOdVayskkFgwAYdTfx33lUHeKlUMJvgpohUCksxfZgicf5viaG9cf9FJrYXyEpq0/640?wx_fmt=jpeg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=0)

三件免费工具搭建学习外挂

你有没有过这种体验——收藏了 20 个 YouTube 视频、下载了 10 篇 PDF、存了 15 篇博客，结果一个月后还是没看？

或者更扎心的：你真的花时间看了，却发现这些内容 80% 都在讲同样的东西，真正有价值的新知识可能只有 10%。

今天分享一套我实测有效的学习系统： **Obsidian + NotebookLM + Gemini** 。它的核心逻辑很简单——把海量资料扔进去，系统帮你自动去重、过滤掉你已经知道的内容，最后只把那 10%~20% 真正值得学的新知识喂给你。

说白了，这是一台 **学习压缩机** 。

![信息压缩原理](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

信息压缩原理

下面是完整的搭建步骤，手把手带你跑通。

## 先搞清楚：三个工具各自干什么

- • **NotebookLM** = 资料大脑。把 PDF、YouTube 字幕、文章、幻灯片全部扔进去，它会帮你消化、索引、建立引用关系。
- • **Gemini** = 推理引擎。它能直接连接 NotebookLM 里的资料，基于你的内容做深度分析——这种事普通 AI 聊天窗口根本搞不定。
- • **Obsidian** = 长期记忆。所有经过压缩的精华内容最终都沉淀到这里，变成一个互相链接的知识网络。

三者协同的效果：20 个视频 + 10 篇 PDF + 15 篇博客 -> **一套干净的个性化笔记** ，只包含你还不知道的东西。

![学习知识库搭建流程](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

学习知识库搭建流程

![NotebookLM：你的资料大脑](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

NotebookLM：你的资料大脑

## 第 1 步：在 NotebookLM 里建「资料仓库」

1. 1\. 打开 **NotebookLM** ，为一个主题创建一个新笔记本（比如「AI 在营销中的应用」）。
2. 2\. 把你的资料全丢进去：PDF、Google Docs、幻灯片、网页文章、YouTube 链接——NotebookLM 会自动消化。
3. 3\. 等它跑完索引，直到「笔记本指南」出现（包含摘要、主题、问题）。

搞定。现在这个笔记本就是你在这个主题下的 **统一资料入口** 。

## 第 2 步：把 NotebookLM 接进 Gemini

这一步是关键——让 Gemini 直接「看到」你的资料，不用手动复制粘贴。

1. 1\. 打开 **Gemini** 。
2. 2\. 在聊天框里点 **「+」按钮** （添加文件/上下文）。
3. 3\. 从列表里选 **NotebookLM** 。
4. 4\. 选择你刚建的笔记本。

连接成功后，你在这个对话里问的每个问题，Gemini 都能基于你的 PDF、视频、笔记来回答。

**验证连接是否成功，发这条 prompt：**

**What are the 5 main ideas across all sources in this NotebookLM notebook? Cite which PDF / video each point comes from.**

如果 Gemini 能准确引用你笔记本里的具体资料名，就说明打通了。

**划重点：这一步别跳过。** 不验证就直接往下走，后面出问题你根本不知道哪里断了。

![NotebookLM → Gemini 连接验证](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

NotebookLM → Gemini 连接验证

## 第 3 步：在 Obsidian 里装 Gemini 插件

现在把长期记忆也接上。

1. 1\. 打开 **Obsidian -> 设置 -> 第三方插件** 。
2. 2\. 启用第三方插件。
3. 3\. 点 **浏览** ，搜索 **"Gemini Scribe"** 。
4. 4\. **安装** ，然后 **启用** 。

配置插件：

1. 1\. 去 Google AI Studio 拿一个 **Gemini API key** 。
2. 2\. 在 Obsidian 中打开 **Gemini Scribe 设置** 。
3. 3\. 粘贴 API key，选好默认模型（推荐 Gemini 1.5 Pro），设置是否自动以当前笔记作为上下文。

打开聊天面板：

1. 1\. 命令面板（ **Cmd/Ctrl+P** ）-> "Gemini Scribe: Open Chat"。

现在你的 Obsidian 侧边栏里多了一个 Gemini 面板，它能同时看到：

- • 你当前正在编辑的 Obsidian 笔记
- • 你关联的 NotebookLM 笔记本

而且可以直接把结果写回你的知识库。闭环了。

![Obsidian + Gemini Scribe闭环](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Obsidian + Gemini Scribe闭环

## 第 4 步：给 Gemini 设定「压缩」指令

回到已连接 NotebookLM 的 Gemini 对话，发一条系统级 prompt：

**You are my learning compressor. - Use the attached NotebookLM notebook as ground truth. - Treat Obsidian as my permanent knowledge base. - Your job: 1. Merge duplicate explanations across sources. 2. Strip out content I almost certainly know already (basic definitions, repeated intros). 3. Output only the new / difficult / high‑leverage ideas in a format I can paste into Obsidian notes.**

这个对话窗口别关——它就是你针对这个主题的 **「压缩工作台」** 。

![压缩指令：只输出你不知道的](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

压缩指令：只输出你不知道的

## 第 5 步：跑第一次「20 个视频 -> 1 篇笔记」的压缩

在 Gemini 对话里发这条 prompt：

This NotebookLM notebook has ~20 YouTube videos and several PDFs on the same topic. **Step 1:** Identify where they repeat the same concepts. **Step 2:** Collapse each repeated concept into one clear explanation (with citations). **Step 3:** Separate the output into: Section A: basic, widely repeated points Section B: advanced, less‑mentioned, or counter‑intuitive points **Step 4:** Output only Section B in bullet form so I can paste it into Obsidian.

Gemini 会用 NotebookLM 里的资料做交叉比对，找出重叠内容，然后输出一份 **「差异清单」** ——只保留那 10%~20% 真正新颖或有深度的信息。

80% 的 YouTube 样板内容？直接干掉。

## 第 6 步：把精华存进 Obsidian

两种方式，选一个：

![两种存入方式](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

两种存入方式

### 方式 A：手动粘贴（推荐）

1. 1\. 复制 Gemini 输出的「Section B」。
2. 2\. 在 Obsidian 里新建一篇笔记，命名类似「主题 -- 差异笔记」。
3. 3\. 粘贴，稍作整理：把要点拆成小标题，加上指向已有笔记的链接。

### 方式 B：用 Gemini Scribe 自动写入

在 Obsidian 里打开当前笔记，在 Gemini Scribe 面板输入：

Here is the compressed 'new/difficult' content Gemini generated based on my NotebookLM notebook.

Rewrite it as: One Obsidian note with H2 per concept Short bullets, each with a suggested backlink target (just the note titles, I will link). Do not repeat basic definitions—assume I already know them."

Gemini Scribe 会直接把格式化好的内容写进你正在编辑的笔记，同时参考笔记中已有的内容作为上下文。

![学习冲刺循环](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

学习冲刺循环

## 第 7 步：变成可重复的「学习冲刺」循环

到这里，整个系统已经跑通了。接下来就是把它变成习惯。

每次遇到一个大主题，按这个循环跑：

1. 1\. **收集** 发现好资源（视频、论文、文章），别收藏到播放列表——直接丢进对应的 **NotebookLM 笔记本** 。
2. 2\. **压缩** 打开 Gemini 对话，重新跑一遍 prompt：「根据最新添加的资料，跟上次比有什么真正新的东西？更新差异清单。」
3. 3\. **沉淀** 用 Gemini Scribe 把差异内容转化成 Obsidian 里干净的、互相链接的笔记。

**复习的时候只看 Obsidian。** 不看 YouTube，不翻 PDF。NotebookLM + Gemini 是后台的压缩引擎，Obsidian 才是你唯一的知识真相源。

每周针对一个大主题跑一次这个循环，你就不用再在 20 个视频里反复听同样的解释了——只需要深度处理 **真正的新内容** ，一次就够。

![传统学习 vs 压缩学习](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

传统学习 vs 压缩学习

这才是所谓「省下几百个小时」的正确打开方式。

继续滑动看下一个

AI的岔路口

向上滑动看下一个

<iframe src="chrome-extension://cnjifjpddelmedmihgijeibhnjfabmlf/side-panel.html?context=iframe"></iframe>