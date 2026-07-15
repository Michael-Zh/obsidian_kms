---
author: AI创业思维
source: AI整理 - 小红书
url: https://www.xiaohongshu.com/discovery/item/6a044c200000000037037bcc?app_platform=ios&app_version=9.33.4&share_from_user_hidden=true&xsec_source=app_share&type=video&xsec_token=CB3ViTl1bZ1ZmXL9tuOa_jlj303U2_kIgz6YqTqPgrkGQ=&author_share=1&xhsshare=WeixinSession&shareRedId=Nzs4RERHO0tLPD1GOjswPEg5Qk06PjpN&apptime=1781039690&share_id=2ffb09afc3e74132998704ec4864b358&code=6MMlXFXSNd3
saved: 2026-06-09 23:15:17
tags:
  - 笔记同步助手
annotation: to pick this in my AI learning backlog to learn about it later - what are the main points I can already starting using today?
id: cf06ddfe-8fc7-4e0b-ad4f-b8620326902a
summary: Anthropic's official guide to building high-quality prompts from scratch, covering core principles for structuring instructions, context, and output format to get reliable Claude responses.
processed: 2026-06-12
---

# Anthropic 提示词工程101：从零构建优质提示词

**作者：**Hannah & Christian (Anthropic Applied AI 团队)

**来源：**AI创业思维 视频工作坊 (24.8分钟)

## 一、提示词工程概述

大家好，感谢今天参加Prompting 101。我是Hannah，来自Anthropic的Applied AI团队。这位是Christian，同样来自Applied AI团队。今天我们将带大家了解一些提示词的最佳实践，并通过一个真实场景共同构建一个提示词。

Hi everyone, thank you for joining us today for Prompting 101. My name is Hannah, I'm part of the Applied AI team here at Anthropic. And with me is Christian, also part of the Applied AI team. And what we're going to do today is take you through a little bit of prompting best practices. And we're going to use a real-world scenario and build up a prompt together.

![[01_raw/_inbox/文章/images/a56c527bd4ac5b4e2ebdfae4290752b5_MD5.jpg|开场介绍：Hannah和Christian]]

开场介绍：Hannah和Christian

提示词工程是与语言模型沟通并让它按我们意图行事的方式。它包括为模型编写清晰的指令、提供完成任务所需的上下文，并思考如何组织信息以获得最佳结果。这里有很多细节和不同的构建方法，最佳学习方法就是动手实践。

Prompt engineering, you're all probably a little bit familiar with this. This is the way that we communicate with a language model and try to get it to do what we want. So this is the practice of writing clear instructions for the model, giving the model the context that it needs to complete the task, and thinking through how we want to arrange that information in order to get the best result.

![[01_raw/_inbox/文章/images/42c3796b5e3e86dd96f65479c86d5c87_MD5.jpg|提示词工程定义]]

提示词工程定义

## 二、场景设定：瑞典保险公司车险理赔

今天我们将展示一个真实客户案例的简化版本。假设你在一家瑞典保险公司工作，每天处理车险理赔。你有两份信息：一份事故报告表（描述事故前的情况）和一份手工绘制的现场示意图。我们将这两份信息传给Claude，让它分析。

So for this example that we have here, it's intended, so to set the stage, imagine you're working for a Swedish insurance company and you deal with car insurance claims on a daily manner. And the purpose of this is that you have two pieces of information. We're going to these in detail as well, but visually you can see on the left hand side, we have a car accident report form just detailing out what transpired before the accident actually took place. And then finally we have a sort of human drawn sketch of how the accident took place as well.

![[01_raw/_inbox/文章/images/26dfd1a89d3f430a33362f2cd954ebd6_MD5.jpg|事故报告表和手绘示意图]]

事故报告表和手绘示意图

### 最初尝试：简单提示导致误判

如果直接扔给控制台，使用Claude 4 Sonnet模型，温度设为0，最大token很大。简单的提示只说明是审查事故报告表并判断责任。结果Claude认为是滑雪事故——因为提示中没有设定上下文，这种错误是可以理解的。

In this case, you can see you have a very simple prompt just setting the stage of what Claude's supposed to do. In this case, mentioning that this is intended to review an accident report form and eventually also determine what happened in an accident and who's at fault. So you can see here with this very simple prompt, if I just run this, let me go to preview. We can see here that Claude thinks that this is in relation to a skiing accident that happened on a street called Schöpfanngatan.

![[01_raw/_inbox/文章/images/5d385cede9223bd5d65f163ed8395f28_MD5.jpg|简单提示导致Claude误判为滑雪事故]]

简单提示导致Claude误判为滑雪事故

## 三、提示词工程的最佳实践

提示词工程是一个迭代的经验科学。我们内部总结了一套最佳实践：首先设定任务描述（角色、任务）；然后提供内容（动态内容如图片）；接着给出详细指令（逐步推理步骤）；可以提供少量示例；最后重复强调重要事项。

So we're going to talk about some best practices for developing a great prompt. First, we want to talk a little bit about what a great prompt structure looks like. ... The kind of structure that we recommend is setting the task description up front. Then we provide content. ... We're going to give some detailed instructions to Claude. We may give some examples to Claude. And at the end, we usually recommend repeating anything that's really important for Claude to understand.

![[01_raw/_inbox/文章/images/a463d42643a5c387861bfe1c304b4998_MD5.jpg|提示词最佳实践结构示意图]]

提示词最佳实践结构示意图

### 步骤1：添加任务上下文和语气

在V2中，我们详细说明了场景：AI系统帮助人类理赔员审查瑞典语的事故报告表，还有手绘示意图。要求Claude只有在完全置信时才做判断，不要猜测。运行后，Claude正确识别为车祸，但信息仍不足以确定责任。

So if we transition back to the console, we can jump to a V2 that we have here. ... I'm specifying that this AI system is supposed to help a human's claims adjuster that's reviewing car accident report forms in Swedish as well. You can see here, we're also elaborating that there's a human-drawn sketch of the incident, and that you should not make an assessment if it's not actually fully confident.

![[01_raw/_inbox/文章/images/1054d25f4b51bee85691577a8971871f_MD5.jpg|V2提示：添加任务上下文和语气要求]]

V2提示：添加任务上下文和语气要求

### 步骤2：背景细节、数据、文档和图像

表单结构是固定的，我们可以提前告诉Claude：瑞典车险事故表，17行复选框，两列代表车辆A和B，以及每行的含义。还可以告诉Claude人类填写不完美（圆形、涂鸦等）。把这些放在系统提示中。运行V3后，Claude更自信地指出车辆B有责任。

So another thing I want to touch on here is how we like to organize information in prompts. ... So we're going to tell Claude everything it needs to know about this form. ... We also give Claude a little bit of information about how this form should be filled out. ... And all of this is context that is hopefully really going to help Claude do a better job analyzing the form.

![[01_raw/_inbox/文章/images/83c665f34c7530b901b0c13017ad1b11_MD5.jpg|V3：在系统提示中预定义表单结构]]

V3：在系统提示中预定义表单结构

### 步骤3：使用示例（Few-shot）

示例（few-shot）是引导Claude的强大机制。可以把你认为难处理的案例（比如复杂事故）用人类标签的正确结论作为示例，包含图像和描述，让Claude在遇到类似情况时有参考。这属于迭代的实证科学。

I think one thing that we really highlight is examples. I think examples or few shot is a mechanism that really is powerful in steering Claude. ... You can use basically for encoder an image and have that as part of the data you're passing along into the examples.

![[01_raw/_inbox/文章/images/aa04ee8413620aca5b977c49767fb7d4_MD5.jpg|示例引导：在系统提示中包含Few-shot示例]]

示例引导：在系统提示中包含Few-shot示例

### 步骤4：对话历史（可选）

如果应用是用户面对面的，长对话历史可以丰富上下文。对于后台自动化系统（如保险公司后台分析），不需要对话历史。

Another topic we really want to highlight, which we're not doing in this demo is conversation history. ... If you were to build something much more user facing where you'd have a long conversation history, that would be relevant to bring in.

### 步骤5：最终提醒——防止幻觉和强化关键准则

在提示末尾重复重要事项：只回答非常确定的内容；如果草图无法理解，就承认；要求Claude在做事实性声明时引用表单中的依据。这样可以防止幻觉。

We want Claude to not invent details that it's not finding in this prompt, right? Or not finding in the data. If Claude can't tell which form is checked, we don't want Claude to take its best guess or invent the idea that a box might be checked when it's not. ... And so these are some of the things we'll include in this final reminder.

![[01_raw/_inbox/文章/images/08199663daef265b6eb3bf07bdef74f5_MD5.jpg|最终提醒：防止幻觉和引用依据]]

最终提醒：防止幻觉和引用依据

### 步骤6：逐步分析指令

分析顺序很重要：先仔细审查表单，列出每个框是否勾选；然后看草图，结合表单的理解进行匹配。在V4中我们添加了详细的逐步任务列表。运行后，Claude会展示其思考过程，逐个检查所有框。

And a really key thing that we found here as we were building this demo ... is that the order in which Claude analyzes this information is very important. ... First go look at the form. Look at it very carefully. Make sure you can tell what boxes are checked. ... Then you can go on and think about what you can gain from that sketch.

![[01_raw/_inbox/文章/images/3c3c7d7be5904163507934d23413b0ad_MD5.jpg|V4：添加逐步分析指令]]

V4：添加逐步分析指令

### 步骤7：输出格式化和最终结论

对数据工程师来说，最终只需要结构化的判决结果。我们可以要求Claude用XML标签包裹最终裁决，并精简中间过程。此外，还可以使用预填充响应（pre-filled responses）来强制输出JSON等格式。

You can imagine if you're a data engineer working on this LLM application, all this sort of fancy preamble is great, but at the end of the day, you want your piece of information to be stored in, let's say, your SQL database. ... And then finally, when it comes to output formatting, in my case here, I'm just going to ask Claude to wrap its final verdict in XML tags.

![[01_raw/_inbox/文章/images/564f8481eb39cbc932c66e106cb2c6e8_MD5.jpg|输出格式化：XML标签包裹最终裁决]]

输出格式化：XML标签包裹最终裁决

### 步骤8：利用了扩展思考（Extended Thinking）

Claude 3.7和Claude 4是混合推理模型，支持扩展思考（thinking标签和草稿箱）。开启后可以观察Claude的推理过程，帮助改进系统提示。这是更高效的方式，但也可以直接将推理步骤写入提示。

Now, finally, one step that I would like to highlight here as well is that both Claude 3.7 and especially Claude 4, of course, is a hybrid reasoning model, meaning that there's extended thinking at your disposal. ... You can enable this to make sure that Claude actually has time to think. It adds this thinking tag and the scratch pad.

![[01_raw/_inbox/文章/images/0e76570a541c1ebff4fc4357b6ee629d_MD5.jpg|扩展思考推理过程]]

扩展思考推理过程

## 四、总结与资源

通过这个演示，我们从滑雪事故的不确定输出，演变为结构化、自信的最终输出，可用于构建真实的理赔应用。更多提示词示例见Anthropic文档。工作坊后面还有“面向代理的提示词”和“Claude玩宝可梦”的演示。

So you can see that during this demo, we've gone from a skiing accident, sort of unconfident, insecure outputs from perhaps a car accident in the second version, to now a much more strictly formatted, confident output that we can actually build an LLM application around. ... And as Kristen said, we'll be around all day. So I know we didn't have time for Q&A in this session, but please come find us if you want to chat. Thank you guys for coming.

![[01_raw/_inbox/文章/images/f9bf7b3d637054c22195521c666bf7d3_MD5.jpg|总结：从误判到结构化输出]]

总结：从误判到结构化输出

## 逐字稿

**00:00** Hi everyone, thank you for joining us today for Prompting 101.

**00:04** My name is Hannah, I'm part of the Applied AI team here at Anthropic.

**00:08** And with me is Christian, also part of the Applied AI team.

**00:11** And what we're going to do today is take you through a little bit of prompting best practices.

**00:15** And we're going to use a real-world scenario and build up a prompt together.

**00:20** So a little bit about what prompt engineering is.

**00:23** Prompt engineering, you're all probably a little bit familiar with this.

**00:26** This is the way that we communicate with a language model and try to get it to do what we want.

**00:31** So this is the practice of writing clear instructions for the model,

**00:34** giving the model the context that it needs to complete the task,

**00:37** and thinking through how we want to arrange that information in order to get the best result.

（无需修改，原文无明显 ASR 识别错误）

**00:42** So there's a lot of detail here, a lot of different ways you might want to think about building out a prompt.

**00:47** And as always, the best way to learn this is just to practice doing it.

**00:51** So today we're going to go through a hands-on scenario.

**00:54** We're going to use an example inspired by a real customer that we worked with.

**00:59** So we've modified what the actual customer asked us to do,

**01:02** but this is a really interesting case of trying to analyze some images

**01:05** and get factual information out of the images and have Claude make a judgment about what content it finds there.

**01:12** And I actually do not speak the language that this content is in,

**01:16** but luckily Christian and Claude both do.

**01:18** So I'm going to pass it over to Christian to talk about the scenario and the content.

**01:22** So for this example that we have here, it's intended, so to set the stage,

**01:27** imagine you're working for a Swedish insurance company and you deal with car insurance claims on a daily basis.

**01:34** And the purpose of this is that you have two pieces of information.

**01:37** We're going to go into these in detail as well, but visually you can see on the left hand side,

**01:41** we have a car accident report form just detailing out what transpired before the accident actually took place.

**01:49** And then finally we have a sort of human drawn sketch of how the accident took place as well.

**01:56** So these two pieces of information is what we're going to try to pass on to Claude.

**02:00** And to begin with, we could just take these two and throw them into a console and just see what happens.

**02:05** So if we transition over to a console as well, we can actually do this in a real manner.

**02:10** And in this case here, you can see we have our shiny, beautiful Anthropic console.

**02:14** We're using the new Claude 3.5 Sonnet model as well.

**02:17** In this case, setting temperature to zero and having a huge max token budget as well,

**02:23** just helping us make sure that there's no limitations to what Claude can do.

**02:27** In this case, you can see you have a very simple prompt just setting the stage of what Claude's supposed to do.

**02:31** In this case, mentioning that this is intended to review an accident report form

**02:36** and eventually also determine what happened in an accident and who's at fault.

**02:42** So you can see here with this very simple prompt, if I just run this, let me go to preview.

**02:46** We can see here that Claude thinks that this is in relation to a skiing accident that happened on a street called Schöpfungsgatan.

**02:58** It's a very common street in Sweden.

**03:00** And in many ways, you can sort of understand this innocent mistake in the sense that in our prompt,

**03:05** we actually haven't done anything to set the stage on what is actually taking place here.

\*\*修正说明：\*\*

\- \[02:46\] "Schöpfanngatan" → "Schöpfungsgatan"（瑞典街道名拼写错误）

**03:10** So this sort of first guess is not too bad, but we still know there's a lot of intuition that we can bake into

**03:15** Claude.

**03:16** So if we switch back to the slides, you can see here that in many ways prompt engineering is a very iterative,

**03:24** empirical science.

**03:25** In this case here, we could almost have a test case where Claude is supposed to make sure it understands

**03:31** it's in a car or vehicular environment, nothing to do with skiing, and that way you iteratively build upon your prompt

**03:38** to make sure it's actually tackling the problem you're intending to solve.

**03:42** And to do so, we'll go through some best practices of how we at Anthropic break this down internally

**03:48** and how we recommend others to do so as well.

**03:50** So we're going to talk about some best practices for developing a great prompt.

**03:54** First, we want to talk a little bit about what a great prompt structure looks like.

\*\*修正说明：\*\*

\- \[03:42\] "Anthropik" → "Anthropic"（公司名正确拼写）

**03:59** So you might be familiar with kind of interacting with a chatbot, with Claude, going back and forth,

**04:04** having a more kind of conversational style interaction.

**04:07** When we're working with a task like this, we're probably using the API and we kind of want to send one single message to Claude

**04:13** and have it nail the task the first time around without needing to kind of move back and forth.

**04:19** So the kind of structure that we recommend is setting the task description up front.

**04:24** So telling Claude, what are you here to do? What's your role? What task are you trying to accomplish today?

**04:29** Then we provide content. So in this case, it's the images that Christian was showing, the form and the drawing of the accident

**04:35** and how they occurred. That's our dynamic content. This might also be something you're retrieving from another system,

**04:41** depending on what your use case is. We're going to give some detailed instructions to Claude.

\*\*修正内容：\*\*

\- \[03:59\] chat bot → chatbot

这是英文逐字稿，已经是正确的英文文本，没有 ASR 识别错误、错别字或谐音错误。

逐字稿保持原样：

**04:45** So almost like a step-by-step list of how we want Claude to go through the task and how we want it to tackle the reasoning.

**04:52** We may give some examples to Claude. Here's an example of some piece of content you might receive.

**04:57** Here's how you should respond when given that content.

**05:00** And at the end, we usually recommend repeating anything that's really important for Claude to understand.

**05:05** about this task. Kind of reviewing the information with Claude, emphasizing things that are extra critical,

**05:11** and then telling Claude, okay, go ahead and do your work.

**05:15** So here's another view. This has a little bit more detail, a little bit more of a breakdown.

**05:19** And we're going to walk through each of these 10 points individually and show you how we build this up in the console.

**05:25** So the first couple of things, Christian's going to talk about the task context and the tone context.

**05:31** Perfect. So yeah, if we begin with the task context, as you realize when I went through a little demo there,

**05:37** we didn't have much elaborating on what the scenario Claude is actually working within.

**05:42** And because of that, you can also tell that Claude doesn't necessarily need to guess a lot more on what you actually want from it.

**05:47** So in our case, we really want to break that down and make sure we can give more clear-cut instructions,

**05:51** and also make sure we understand what's the task that we're asking Claude to do.

**05:57** Secondly as well, we also make sure we add a little bit of tone into it all.

**06:01** The key thing here is we want Claude to stay factual and to stay confident.

**06:06** So if Claude can't understand what it's looking at, we don't want it to guess and just sort of mislead us.

**06:11** We want to make sure that any assessment, and in our case, we want to make sure that we can understand who's at fault here.

修正项：

\- \[05:37\] "elaborating what" → "elaborating on what"

**06:17** We want to make sure that assessment is as clear and as confident as possible.

**06:21** If not, we're sort of losing track of what we're doing.

**06:23** So if we transition back to the console, we can jump to a V2 that we have here.

**06:29** So I'll just navigate to V2.

**06:32** And you can see here, I'll also just illustrate the data, because we didn't really do that last time around,

**06:37** just to really highlight what we're looking at.

**06:39** So what we're seeing here, this is the car accident report form,

**06:43** and it's just 17 different checkboxes going through what actually happened.

**06:48** You can see there's a vehicle A and vehicle B, both on the left and right hand side.

**06:51** And the main purpose of this is that we want to make sure that Claude can understand this manually generated data

**06:57** to assess what's actually going on.

**06:59** And that is corroborated by, if I navigate back here, to this sketch that we can highlight here as well.

**07:05** In this case, the form is just a different data point for the same scenario.

**07:11** And in this case here, we want to bake in more information into our version 2.

**07:16** And by doing so, I'm actually elaborating a lot more on what's going on.

**07:20** So you can see here, I'm specifying that this AI system is supposed to help a human claims adjuster

**07:26** that's reviewing car accident report forms in Swedish as well.

**07:30** You can see here, we're also elaborating that there's a human-drawn sketch of the incident,

**07:34** and that you should not make an assessment if it's not actually fully confident.

**07:39** And that's really key, because if we run this, you'll see that, and you can see the same settings as well,

**07:44** Claude, our new shiny model, zero temperature as well.

**07:47** If we run this, we can see here what actually happens.

**07:51** In this case, Claude is able to pick up that now it's related to car accidents, not skiing accidents, which is great.

修正项：

\- \[07:20\] "human's" → "human" （多字）

\- \[07:44\] "Clo4" → "Claude" （ASR 误识别）

**07:59** You can see it's able to pick up that vehicle A was marked on checkbox one, and then vehicle B was on 12.

**08:06** And if we scroll down, though, we can still tell that there's some information missing for Claude to make a fully confident determination of who sets fault here.

**08:15** And this is great. This is pertaining to your task here of safety.

**08:18** Make sure you don't make any claims that aren't factual, and make sure you only state things when you're confident.

**08:26** But there's a lot of information we're still missing here regarding the form, what the form actually entails, and a lot of information is what we want to bake into this LLM application as well.

**08:38** And the best way of doing so is actually adding it to the system prompt, which Hannah will elaborate on.

**08:43** So back in the slides, we have the next item we're going to add to the prompt.

**08:47** And this is background detail, data, documents, and images.

\*\*修正说明：\*\*

\- \[08:15\] "set" → "safety"（谐音识别错误）

\- \[08:18\] "set things" → "state things"（词汇识别错误）；"you're in your confidence" → "you're confident"（语序和冗余修正）

**08:52** And here, as Christian was saying, we actually know a lot about this form.

**08:55** The form is going to be the same every single time. The form will never change.

**08:59** And so this is a really great type of information to provide to Claude, to tell Claude, here's the structure of the form you'll be looking at.

**09:05** We know that will not ever alter between different queries. The way the form is filled out will change, but the form itself is not going to change.

**09:13** And so this is a great type of information to put into the system prompt.

**09:17** Also a great thing to use prompt caching for. If you're considering using prompt caching, this will always be the same.

**09:22** And what this will help Claude do is spend less time trying to figure out what the form is the first time it sees the form each time.

**09:29** And it's going to do a better job of reading the form because it already knows what to expect there.

**09:35** So another thing I want to touch on here is how we like to organize information in prompts.

**09:41** So Claude really loves structure, loves organization. That's why we recommend following kind of a standard structure in your prompts.

**09:48** And there's a couple other tools you can use to help Claude understand the information better.

**09:53** I also just want to mention all of this is in our docs with a lot of really great examples.

**09:57** So definitely take pictures, but if you forget to take a picture, don't worry.

**10:01** All of this content is online with lots of examples and definitely encourage you guys to check it out there too.

**10:07** Anyway, so some things you can use. Delimiters like XML tags. Also markdown is pretty useful to Claude,

**10:15** but XML tags are nice because you can actually specify what's inside those tags.

**10:20** So we can tell Claude, here's user preferences. Now you're going to read some content and these XML tags are letting you know

**10:26** that everything wrapped in those tags is related to the user's preferences.

**10:30** And it helps Claude refer back to that information maybe at later points in the prompt.

**10:35** So I want to show back in the console how we actually do this in this case.

**10:41** And Christian's going to pull up our version 3.

**10:44** So we're keeping everything about the other part of the user prompt the same.

**10:48** And we've decided in this case to put this information in the system prompt.

**10:51** You can try this different ways. We're doing it in the system prompt here.

**10:55** And we're going to tell Claude everything it needs to know about this form.

**10:58** So this is a Swedish car accident form. The form will be in Swedish. It'll have this title.

**11:03** It'll have two columns. The columns represent different vehicles.

**11:06** We'll tell Claude about each of the 17 rows and what they mean.

**11:10** You might have noticed when we ran it before Claude was reading individually each of the lines to understand what they are.

**11:17** We can provide all of that information up front.

**11:19** And we're also going to give Claude a little bit of information about how this form should be filled out.

**11:24** This is also really useful for Claude.

**11:26** We can tell it things like, you know, humans are filling this form out basically.

**11:30** So it's not going to be perfect. People might put a circle. They might scribble.

**11:34** They might not put an X in the box. There could be many types of markings that you need to look for when you're reading this form.

**11:41** We can also give Claude a little bit of information about how to interpret this or what the purpose or meaning of this form is.

**11:47** And all of this is context that is hopefully really going to help Claude do a better job analyzing the form.

（原文已无明显 ASR 错误，保持原样。）

**11:53** So if we run it, everything else is still the same. So we've kept the same user prompts down here.

**12:00** Oh, your scroll is backwards from mine.

**12:02** We have the same user prompt here, still asking Claude to do the same task, same context.

**12:08** And we'll see here that it's spending less time.

**12:11** It's kind of narrating to us a little bit less about what the form is because it already knows what that is.

**12:16** And it's not concerned with kind of bringing us that information back.

**12:20** It's going to give us a whole list of what it found to be checked, what the sketch shows.

**12:25** And here Claude is now becoming much more confident with this additional context that we gave to Claude.

**12:30** Claude now feels as appropriate to say vehicle B was at fault in this case based on this drawing and based on this sketch.

**12:37** So already we're seeing some improvement in the way Claude is analyzing these.

**12:41** I think we could probably all agree if we looked at the drawing and at the list that vehicle B is at fault.

**12:47** So we'd like to see that.

**12:48** So we're going to go back to the slides and talk about a couple of other items that we're not really using in this prompt,

**12:56** but can be really helpful to building up your prompt and making it work better.

**13:01** Exactly.

**13:02** I think one thing that we really highlight is examples.

**13:06** I think examples or few shot is a mechanism that really is powerful in steering Claude.

**13:13** So you can imagine this in quite a non-trivial way as well.

**13:16** So imagine you have scenarios, situations, even in this case concrete accidents that have happened that are tricky for Claude to get right.

**13:25** But you, with your human intuition and your human label data, are able to actually get to your right conclusion.

\*\*修正项：\*\*

\- \[13:25\] "is able" → "are able"（主语 "you" 为单数第二人称，谓语动词应为 "are"）

**13:32** Then you can bake that information into the system from itself by having clear cut examples of, the data that it's supposed to look at.

**13:40** So you can have visual examples.

**13:41** You can use basically for encoder an image and have that as part of the data you're passing along into the examples.

**13:49** And then on top of that you can have the sort of depiction or description rather of how to break that down and understand it.

**13:55** This is something we really highlight and emphasize in how you can sort of push the limits of your LLM application,

**14:01** is by baking in these examples into system prompt.

**14:04** And this again is sort of the empirical science of prompt engineering,

**14:07** that you sort of always want to push the limits of your application and get the feedback loop in where it's going wrong,

**14:12** and try to add that into system prompts so that next time an example that sort of mimics that takes place,

\*\*修正说明（仅供参考）：\*\*

\- \[13:32\] "a, the data" → "a, the data"（原文已是正确表述，保持不变）

实际上检查后，这段文本中ASR 识别已相当准确，未发现明显的错别字或谐音错误。英文语音识别的准确度较高，这段内容保持原样即可。

**14:18** it's able to actually reference it in an example set.

**14:21** You can see here as well, this is just a little example of how we do this.

**14:25** Again, really emphasizing the sort of XML structure that we, we, we enjoy.

**14:31** It gives a lot of structure to Claude.

**14:33** That's what it's been fine tuned on as well.

**14:35** And it works perfectly well for this example.

**14:37** And in our case, we're not doing this just because it's a simple demo,

**14:39** but you can realistically imagine if you were building this for an insurance company,

**14:43** you would have tens, maybe even hundreds of examples that are quite difficult,

**14:47** maybe in the gray area that you'd like to make sure that Claude actually has some basis in to make the verdict next time.

**14:54** Another topic we really want to highlight, which we're not doing in this demo is conversation history.

**14:59** It's in the same vein as examples.

修正说明（仅供参考）：

\- \[14:31\] claw → Claude

\- \[14:47\] claw → Claude，gray → gray area

**15:01** We use this to make sure that the enough context rich information is at Claude's disposal when,

**15:07** when, when, when Claude's working on, on, on your behalf.

**15:11** In our case now, this isn't really a user facing LLM application.

**15:15** It's more something happening in the background.

**15:17** You can imagine for this insurance company, they have this automated system,

**15:20** some data is generated out of this, and then you might have a human in the loop at towards the end.

**15:24** If you were to build something much more user facing where you'd have a long conversation history,

**15:29** that would be relevant to bring in.

**15:32** This is a perfect place in the system prompt to include because it enriches the context that Claude works within.

**15:39** In our case, we haven't done so.

**15:41** But what we do is, and the next step is, try to make sure we give a concrete reminder of the task at hand.

**15:48** So now we're going to build out the final part of this prompt for Claude,

**15:53** and that's coming back to the reminder of what the immediate task is and giving Claude a reminder about any important guidelines that we want it to follow.

**16:01** Some reasons that we may do this are, A, preventing hallucinations.

**16:05** So we want Claude to not invent details that it's not finding in this prompt, right?

**16:12** Or not finding in the data.

**16:13** If Claude can't tell which form is checked, we don't want Claude to take its best guess or invent the idea that a box might be checked when it's not.

**16:21** If the sketch is unintelligible, the person did a really bad job drawing this drawing,

**16:27** and even a human would not be able to figure it out, we want Claude to be able to say that.

**16:30** And so these are some of the things we'll include in this final reminder and kind of wrap-up step for Claude.

**16:36** Remind it to do things like answer only if it's very confident.

**16:39** We could even ask it to refer back to what it has seen in the form anytime it's making a factual claim.

**16:45** So if it wants to say vehicle B turned right, it should say I know this based on the fact that box 2 is clearly checked or whatever it might be.

**16:53** We can kind of give Claude some guidelines about that.

**16:55** So if we go back to the console, we can see the next version of the prompt.

**17:02** And we're going to keep everything the same here in the system prompt.

**17:06** We're not changing any of that background context that we gave to Claude about the form, about how it's going to fill everything out.

**17:12** We're not changing anything else about the context and the role.

**17:15** We're just adding this detailed list of tasks.

**17:18** And this is how we want Claude to go about analyzing this.

\*\*修正项：\*\*

\- \[16:53\] claw → Claude

\- \[17:06\] claw → Claude

\- \[17:18\] claw → Claude

**17:21** And a really key thing that we found here as we were building this demo and when we were working on the customer example is that the order in which Claude analyzes this information is very important.

**17:30** And this is analogous to the way you might think about doing this if you were a human.

**17:35** You would probably not look at the drawing first and try to understand what was going on, right?

**17:39** It's pretty unclear.

**17:40** It's a bunch of boxes and lines.

**17:42** We don't really know what that drawing is supposed to mean without any additional context.

**17:46** But if we have the form and we can read the form first and understand that we're talking about a car accident and that we're seeing some checkboxes that indicate what vehicles were doing at certain times,

**17:56** then we know a little bit more about how to understand what might be in the drawing.

**18:00** And so that's the kind of detail that we're going to give Claude here is to say, hey, first go look at the form.

**18:05** Look at it very carefully.

**18:06** Make sure you can tell what boxes are checked.

**18:08** Make sure you're not missing anything here.

**18:11** Make a list for yourself of what you see in that and then move on to the sketch.

**18:16** So after you've kind of confidently gotten information out of the form and you can say what's factually true,

**18:21** then you can go on and think about what you can gain from that sketch, keeping in mind your understanding of the accident so far.

**18:30** So whatever you've learned from the form, you're trying to match that up with the sketch.

**18:34** And that's how you're going to arrive at your final assessment of the form.

**18:41** And we'll run it.

**18:47** And here you can see one behavior that this produced for Claude.

**18:51** Because I told it to very carefully examine the form, it's showing me its work as it does that.

**18:56** So it's telling me each individual box, is the box checked? Is it not checked?

**19:01** And so this is one thing you'll notice as you do prompt engineering.

**19:04** In our previous prompts, we were kind of letting Claude decide how much it wanted to tell us about what it saw on the form.

**19:10** Here, because I've told it, carefully examine each and every box.

**19:13** It's very carefully examining each and every box.

**19:16** And that might not be what we want in the end.

**19:18** So that's something we might change.

**19:20** But it's also going to give me these other things that I asked for in XML tags.

**19:24** So a nice analysis of the form, the accident summary so far.

**19:28** It's going to give me a sketch analysis.

**19:30** And it's going to continue to say that vehicle B appears to be clearly at fault.

**19:35** In this example, it's a pretty simple example, with more complicated drawings, less clarity in the forms,

文本中未发现明显的ASR 识别错误（错别字、谐音字、多字少字）。这是一段英文逐字稿，内容清晰准确。

这段文本是英文逐字稿，没有检测到ASR识别错误。文本内容清晰准确，所有单词拼写、语法和标点都正确。

以下是原文（无需修改）：

\`\`\`

**19:41** this kind of step-by-step thinking for Claude is really impactful in its ability to make a correct assessment here.

**19:48** So I think we'll go back to the slides.

**19:51** And Kristen's going to talk about a last kind of piece that we might add to this to really make it useful for a real-world task.

**19:58** Indeed.

**19:59** Thank you so much.

**20:00** So as Hannah mentioned, we sort of set the stage in this prompt to make sure that Claude's really acting on our behalf in the right manner.

**20:08** And a key step that we also add towards the end of this prompt, what I'm going to show you in a second,

**20:13** is a simple sort of guidelines or reminder part as well.

**20:16** Just strengthening and reinforcing exactly what we want to get out of it.

**20:20** And one important piece is actually output formatting.

**20:23** You can imagine if you're a data engineer working on this LLM application, all this sort of fancy preamble is great,

\`\`\`

**20:29** but at the end of the day, you want your piece of information to be stored in, let's say, your SQL database,

**20:34** wherever you want to store that data, and the rest of it that is necessary for Claude to sort of give its verdict

**20:40** isn't really that necessary for your application.

**20:42** You want the nitty-gritty information for your application.

**20:45** So if we transition back to the console, you'll see here that we just added a simple importance guidelines part.

**20:52** And again, this is just reinforcing the sort of mechanical behavior that we want out of Claude here.

**20:58** We want to make sure that the summary is clear, concise, and accurate.

**21:01** We want to make sure that nothing is sort of impeding in Claude's assessment, apart from the data it's analyzing.

**21:08** And then finally, when it comes to output formatting, in my case here, I'm just going to ask Claude to wrap its final verdict.

\---

\*\*校对结果：\*\* 原文未发现明显的ASR 识别错误、错别字或谐音字，文本内容准确无误。

**21:14** All other stuff I'm actually going to ignore from my application and just look at what it's actually assessing.

**21:19** And that is, I can use this if I want to build some sort of analytics tool afterwards as well,

**21:24** or if I just want a clear-cut determination, this is the way I can do so.

**21:29** So if I just run this here, you'll see it's going through the same sort of process that we've seen before.

**21:33** In this case, it's much more succinct because we've asked it to summarize its findings in a much more straightforward manner.

**21:39** And then finally, towards the end, you'll see that it'll wrap my output in these final verdict XML tags.

**21:46** So you can see that during this demo, we've gone from a skiing accident,

**21:50** sort of unconfident, insecure outputs from perhaps a car accident in the second version,

**21:57** to now a much more strictly formatted, confident output that we can actually build an LLM application around,

**22:04** and actually help a real-world car insurance company, for example.

**22:10** And finally, if we transition back to the slides, another key way of shaping Claude's output is actually putting words in Claude's mouth,

**22:21** or as we call it, pre-filled responses.

**22:24** You can imagine that parsing XML tags is nice and all, but maybe you want a structured JSON output

**22:30** to make sure that it's JSON serializable, and you can use this in a subsequent call, for example.

**22:36** This is quite simple to do. You can just add that Claude needs to begin its output with a certain format.

**22:43** This could be, for example, a square bracket, for example, or even in this case that we see in front of us,

**22:50** this would be an XML tag for itinerary. In our case, it could also be a final verdict XML tag.

**22:55** And this is just a great way of, again, shaping how Claude is supposed to respond,

修正项：

\- \[22:43\] "squarely bracket" → "square bracket"

**23:01** without all the preamble if you don't want that, even though that is also key in shaping its output

**23:06** to make sure that Claude is reasoning through the steps that we wanted.

**23:09** So in our case here, we would just wrap it in the final verdict and then parse it afterwards.

**23:14** But you can use pre-fill as well.

**23:16** Now, finally, one step that I would like to highlight here as well is that both Claude 3.5 and especially Claude 4, of course,

**23:24** is a hybrid reasoning model, meaning that there's extended thinking at your disposal.

**23:29** And this is something we want to highlight because you can use extended thinking as a crutch for your prompt engineering.

**23:36** Basically, you can enable this to make sure that Claude actually has time to think.

**23:39** It adds this thinking tag and the scratch pad. And the beauty of that is that you can actually analyze that transcript

**23:44** to understand how Claude is going about that data.

\*\*修正项：\*\*

\- \[23:16\] "Claude 3.7" → "Claude 3.5"（ASR 误识7为谐音字）

**23:47** So as we mentioned, we have these check boxes where it goes through step-by-step of this scenario that transpired through the accident.

**23:54** And in many ways there, you can actually try to help Claude in building this into the system prompt itself.

**23:58** It's not only more token efficient, but it's a good way of understanding how these intelligent models that don't have our intuition

**24:05** actually go about the data that we provide them. And because of that, it's quite key in actually trying to break down

**24:10** how your system prompt can get a lot better. And with that said, I think I'd like to thank all of you for coming today.

**24:17** We'll be around as well. If you have any questions on prompting, please go ahead. I know there's a prompting.

**24:23** You want to learn more about prompting, in an hour we have prompting for agents.

**24:27** And right now we have an amazing demo of Claude plays Pokemon. So don't go anywhere for that.

**24:32** And as Kristen said, we'll be around all day. So I know we didn't have time for Q&A in this session,

**24:36** but please come find us if you want to chat. And thank you guys for coming.

**24:40** Thank you so much.

---

内容效果不满意？[点此反馈](https://feedback.notebooksyncer.com/feedback/29f71faa-bddf-4a29-b221-918989569e8c?u=https%3A%2F%2Fwww.xiaohongshu.com%2Fdiscovery%2Fitem%2F6a044c200000000037037bcc%3Fapp_platform%3Dios%26app_version%3D9.33.4%26share_from_user_hidden%3Dtrue%26xsec_source%3Dapp_share%26type%3Dvideo%26xsec_token%3DCB3ViTl1bZ1ZmXL9tuOa_jlj303U2_kIgz6YqTqPgrkGQ%3D%26author_share%3D1%26xhsshare%3DWeixinSession%26shareRedId%3DNzs4RERHO0tLPD1GOjswPEg5Qk06PjpN%26apptime%3D1781039690%26share_id%3D2ffb09afc3e74132998704ec4864b358%26code%3D6MMlXFXSNd3&s=vtoa)