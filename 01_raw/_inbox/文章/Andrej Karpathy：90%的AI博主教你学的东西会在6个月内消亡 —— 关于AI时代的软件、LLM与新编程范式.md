---
author: 笔记同步助手
source: 微信公众号
url: https://mp.weixin.qq.com/s?__biz=MzIxNjkwODcxOQ==&mid=2247483868&idx=1&sn=4720de0681ec48fb523502493fc1ea99&chksm=969713e019f105912f8fc9dbf00932d6c90d7545f95fe7fc1cdef08e72669b48dff334c1e162&mpshare=1&scene=1&srcid=0624OsBghPJsz4Br48TdWhPt&sharer_shareinfo=6ed8cee904ab8f47e35864cf847fa7f1&sharer_shareinfo_first=6ed8cee904ab8f47e35864cf847fa7f1#rd
saved: 2026-06-23 21:00:30
tags:
  - 笔记同步助手
annotation: Thoughts about the future of AI and how to live with it
id: 238c130a-8577-4c40-b63b-c3ec8061e277
---

公众号名称：Obsidian剪藏

作者名称：笔记同步助手

发布时间：2026-06-03 16:24

作者: Andrej Karpathy (演讲) / 0xMorty (视频) | 整理: 笔记同步助手

```
把链接发给笔记同步助手，助手会帮你把视频链接整理为图文方便阅读
```

## 一、引言：软件正在再次改变

这是一场关于AI时代软件的演讲。许多学生即将进入这个行业，而我认为这是一个极其独特且有趣的时机，因为软件正在再次发生根本性变化。我过去做过类似的演讲，但软件一直在变，所以我总有新内容可讲。在过去70年里，软件在基础层面几乎没有太大变化，但在最近几年里，却发生了大约两次快速变革。因此，有大量的工作要做，大量的软件需要编写和重写。

About software in the era of AI. And I'm told that many of you are students, like bachelors, masters, PhD and so on, and you're about to enter the industry. And I think it's actually like an extremely unique and very interesting time to enter the industry right now. And I think fundamentally the reason for that is that software is changing again. And I say again because I actually gave this talk already. But the problem is that software keeps changing. So I actually have a lot of material to create new talks. And I think it's changing quite fundamentally. I think roughly speaking, software has not changed much on such a fundamental level for 70 years. And then it's changed, I think, about twice quite rapidly in the last few years. And so there's just a huge amount of work to do, a huge amount of software to write and rewrite.

![[01_raw/_inbox/文章/images/9a8813d0bb69cce616e509fc574a68b7_MD5.jpg]]

GitHub软件地图可视化

## 二、软件1.0、2.0、3.0：编程范式演进

### 软件1.0 vs 软件2.0

几年前我提出了“软件2.0”的概念：软件1.0是你为计算机编写的代码，而软件2.0是神经网络的权重，你通过调整数据集和运行优化器来间接创建它们。当时神经网络常被看作另一种分类器，但这个框架更恰当。现在，Hugging Face 相当于软件2.0领域的GitHub。

And a few years ago, I kind of observed that software was kind of changing. And there was kind of like a new type of software around. And I called this software 2.0 at the time. And the idea here was that software 1.0 is the code you write for the computer. Software 2.0 are basically neural networks. And in particular, the weights of a neural network. And you're not writing this code directly. You are more kind of like tuning the data sets. And then you're running an optimizer to create the parameters of this neural net. And I think like at the time, neural nets were kind of seen as like just a different kind of classifier, like a decision tree or something like that. And so I think it was kind of like I think this framing was a lot more appropriate. And now actually what we have is kind of like an equivalent of GitHub in the realm of software 2.0. And I think the hugging face is basically equivalent of GitHub in software 2.0.

![[01_raw/_inbox/文章/images/033371b22b8347edd99172b050eeeabf_MD5.jpg]]

软件1.0与软件2.0对比示意图

### 软件3.0：可编程的LLM

现在有了更大的变化：神经网络通过大语言模型变得可编程，我称之为“软件3.0”。你的提示词（prompts）就是编程LLM的程序，而它们是用英语写的——这是一种极其有趣的编程语言。通过一个情感分类的例子可以对比三种范式：用Python写固件（软件1.0）、训练神经网络（软件2.0）、用Few-shot提示词（软件3.0）。

And I think what's changed and I think is a quite fundamental change is that neural networks became programmable with large language models. And so I see this as quite new, unique. It's a new kind of a computer. And so in my mind, it's worth giving it a new designation of software 3.0. And basically your prompts are now programs that program the LLM. And remarkably, these prompts are written in English. So it's kind of a very interesting programming language. So maybe to summarize the difference, if you're doing sentiment classification, for example, you can imagine writing some amount of Python to basically do sentiment classification. Or you can train a neural net. Or you can prompt a large language model.

![[01_raw/_inbox/文章/images/676bd3c3ee8a927ce544c8d0b8ec667e_MD5.jpg]]

三种编程范式对比图

### 特斯拉自动驾驶中的范式吞噬

在特斯拉Autopilot项目中，我发现随着神经网络能力增长，原本用C++（软件1.0）编写的功能逐步被神经网络（软件2.0）取代，大量代码被删除。现在同样的事情再次发生，软件3.0正在吞噬整个技术栈。建议新入行的工程师掌握所有三种范式，并根据情况灵活选择。

So as an example, a lot of the stitching up of information across images from the different cameras and across time was done by a neural network, and we were able to delete a lot of code. And so the software 2.0 stack quite literally ate through the software stack of the autopilot. So I thought this was really remarkable at the time. And I think we're seeing the same thing again, where basically we have a new kind of software, and it's eating through the stack. We have three completely different programming paradigms. And I think if you're entering the industry, it's a very good idea to be fluent in all of them.

![[01_raw/_inbox/文章/images/0a3f225e9474dde46695e65fd8e24eec_MD5.jpg]]

斯拉Autopilot中代码被神经网络吞噬的示意图

## 三、LLM的新类比：电力、晶圆厂与操作系统

Andrew Ng说“AI是新电力”，这个比喻很贴切：LLM实验室花费资本支出训练模型（相当于建设电网），运营支出通过API提供服务（仪表化访问），用户要求低延迟、高可用、一致质量。像OpenRouter这样的工具允许在不同LLM之间切换，就像电力切换开关。当最先进的LLM宕机时，会感到“智力褐变”——全球变笨了。

I was struck by this quote from Andrew actually many years ago now, I think. And I think Andrew is going to be speaking right after me. But he said at the time, AI is the new electricity. And I do think that it kind of captures something very interesting in that LLMs certainly feel like they have properties of utilities right now. ... And I think what's also really fascinating, and we saw this in the last few days actually, a lot of the LLMs went down and people were kind of like stuck and unable to work. And I think it's kind of fascinating to me that when the state-of-the-art LLMs go down, it's actually kind of like an intelligence brownout in the world.

![[01_raw/_inbox/文章/images/dd16bed9bdabd9d6fd1ff026409a00bd_MD5.jpg]]

电力与LLM类比示意图

同时LLM也有晶圆厂的属性：构建LLM所需的资本支出庞大，技术树快速生长，研究开发秘密集中。但也有不同之处——软件更灵活，防御性较弱。例如“4纳米工艺节点”对应“集群峰值算力”，使用NVIDIA GPU只做软件是“无晶圆厂模式”，谷歌自研TPU是“Intel自有晶圆厂模式”。

But LLMs don't only have properties of utilities. I think it's also fair to say that they have some properties of fabs. And the reason for this is that the capex required for building LLMs is actually quite large. ... Like a four nanometer process node maybe is something like a cluster with certain max flops. You can think about when you're using NVIDIA GPUs and you're only doing the software and you're not doing the hardware, that's kind of like the fabless model.

![[01_raw/_inbox/文章/images/4adb364099c45b92457beabc4f185444_MD5.jpg]]

晶圆厂与LLM类比图

最有力的类比是操作系统：LLM类似CPU，上下文窗口是内存，LLM编排记忆和计算。Apps如Cursor可以在不同模型（GPT/Claude/Gemini）上运行，就像跨平台应用。当前处于1960年代左右的阶段：LLM计算昂贵，集中在云端，通过时分共享使用，个人计算革命尚未到来。Mac Mini或许是个苗头。与ChatGPT直接对话就像通过终端操控操作系统，图形界面尚未被通用地发明。

But actually I think the analogy that makes the most sense perhaps is that in my mind, LLMs have very strong kind of analogies to operating systems in that this is not just electricity or water. ... So the LLM is a new kind of a computer. It's setting. It's kind of like the CPU equivalent. The context windows are kind of like the memory. And then the LLM is orchestrating memory and compute for problem solving using all of these capabilities here. ... And I think a lot of people are getting way over excited with AI agents and it's not useful to me to get a diff of 1,000 lines of code to my repo. I have to, I'm still the bottleneck, right, even though that 1,000 lines come out instantly, I have to make sure that this thing is not introducing bugs.

操作系统与LLM类比图

### 翻转的技术扩散方向

LLM翻转了技术扩散方向：通常政府和企业最先用新技术，消费者最后；但LLM首先被用来帮我煮鸡蛋，而不是军事弹道。企业和政府反而滞后于个人消费者的采用。这很疯狂：ChatGPT瞬间部署到数十亿人的电脑上，现在轮到我们进入行业编程这些计算机了。

It's that LLMs like flip, they flip the direction of technology diffusion that is usually present in technology. ... But with LLMs, it's all about how do you boil an egg or something like that. This is certainly like a lot of my use. And so it's really fascinating to me that we have a new magical computer and it's like helping me boil an egg. It's not helping the government do something really crazy like some military ballistics or some special technology. Indeed corporations or governments are lagging behind the adoption of all of us, of all of these technologies.

![[01_raw/_inbox/文章/images/3f46af889ae7b9c9fe2a6bfb526bcb37_MD5.jpg]]

技术扩散方向翻转示意图

## 四、LLM的心理学：超人类能力与认知缺陷

LLM像是“人灵”（people spirits）——对人类的随机模拟，由自回归Transformer实现。它们有百科全书式的记忆（类似《雨人》中的自闭学者），但也存在诸多认知缺陷：幻觉、知识自知不足、锯齿状智能（超人在某些任务上，但在另一些任务上犯人类不会犯的错误，比如认为9.11大于9.9）、顺行性遗忘（工作记忆是上下文窗口，每早被清空，类似《记忆碎片》和《初恋50次》）。此外LLM易受提示注入攻击、泄露数据等安全问题。

So the way I like to think about LLMs is that they're kind of like people spirits. They are stochastic simulations of people. And the simulator in this case happens to be an autoregressive transformer. ... So the first thing you'll notice is, of course, LLMs have encyclopedic knowledge and memory. ... But they also have a bunch of, I would say, cognitive deficits. So they hallucinate quite a bit. ... They display jagged intelligence. So they're going to be superhuman in some problem-solving domains. And then they're going to make mistakes that basically no human will make. Like, you know, they will insist that 9.11 is greater than 9.9 or that there are two R's in strawberry.

## 五、机会：部分自主应用（Partial Autonomy Apps）

### Cursor —— 一个典范

与其直接与ChatGPT对话（像操作系统的终端），更明智的做法是使用专用应用如Cursor。它具备几个关键特征：

-   大量的上下文管理
    
-   编排多次LLM调用（嵌入模型、聊天模型、差分应用模型）
    
-   应用特定的GUI（如代码差异显示为红绿变化，允许人类审计）
    
-   自主滑块（Autonomy Slider）：从补全→修改→整个文件→整个代码库，自主程度可调
    

So in particular, you will notice that we have a traditional interface that allows a human to go in and do all the work manually, just as before. But in addition to that, we now have this LLM integration that allows us to go in bigger chunks. ... Number one, the LLMs basically do a ton of the context management. Number two, they orchestrate multiple calls to LLMs, right? ... A really big one that I think also may be not fully appreciated always is application-specific GUI and the importance of it. ... And the last kind of feature I want to point out is that there's what I call the autonomy slider.

Cursor部分自主应用界面截图

### Perplexity —— 另一个例子

Perplexity也有类似架构：打包信息、编排多模型、提供GUI（引用来源）、自主滑块（快速搜索→研究→深度研究）。

Maybe to show one more example of a fairly successful LLM app, Perplexity. It also has very similar features to what I've just pointed out in cursor. It packages up a lot of the information. It orchestrates multiple LLMs. It's got a GUI that allows you to audit some of its work. So for example, it will cite sources. And you can imagine inspecting them. And it's got an autonomy slider.

![[01_raw/_inbox/文章/images/dd1be074b5a642a38757a371a9ed5d80_MD5.jpg]]

Perplexity界面截图

### 原理：生成-验证循环与AI的缰绳

我们与AI合作：AI做生成，人类做验证。目标是让这个循环尽可能快。两种加速方式：GUI利用人类视觉GPU（看比读快）；让AI保持在缰绳上（keep AI on the leash）。不要追求过大的差异（1000行代码差异难以审查），要小步增量、具体提示。在特斯拉自动驾驶中我也学到了同样教训——这是一个持续多年的部分自主产品。2025年不是agent年，而是agent十年。需要人机协作，严肃对待软件。

There are two major ways that I think this can be done. Number one, you can speed up verification a lot. And I think GUIs, for example, are extremely important to this because a GUI utilizes your computer vision GPU in all of our head. Reading text is effortful and it's not fun. But looking at stuff is fun and it's just kind of like a highway to your brain. So I think GUIs are very useful for auditing systems and visual representations in general. And number two I would say is we have to keep the AI on the leash.

![[01_raw/_inbox/文章/images/84642ed7d581b7d6d620698284afbf18_MD5.jpg]]

生成-验证循环示意图

## 六、Vibe Coding：自然语言编程与新程序员

英语是自然接口，每个人都有成为程序员的机会。Vibe Coding（氛围编程）概念来自一条意外走红的推文：你只需要描述想要什么，AI就生成代码。甚至维基百科都有了对应词条。孩子们在Hugging Face的视频中展示了氛围编程，我极为鼓舞。我自己也尝试了：构建了一个iOS应用（虽然不会Swift），仅用一天就运行在手机上；还做了Menugen.app——拍菜单生成图片。代码部分很容易，但难的是让应用真实可用（认证、支付、域名、部署等DevOps工作）。我不得不手动点击浏览器完成操作，这非常痛苦。

I also vibe coded this app called Menugen. And this is live. You can try it in Menugen.app. ... Most of it actually was when I tried to make it real so that you can actually have authentication and payments and the domain name and the virtual deployment. This was really hard. ... I had to follow all these instructions. This was crazy. So I think the last part of my talk, therefore, focuses on can we just build for agents? I don't want to do this work. Can agents do this?

![[01_raw/_inbox/文章/images/0a1e2a1c9d53b58e3b85e2fe585a95d8_MD5.jpg]]

Menugen应用截图

## 七、为Agent构建基础设施：从人类GUI到LLM原生接口

新的数字信息消费者和操纵者出现了：不仅是人类（通过GUI）和计算机（通过API），还有AI Agent——它们是人灵。我们需要为它们构建友好接口。示例：

-   在网站放lms.txt文件，用Markdown告诉LLM网站内容（类似robots.txt）
    
-   文档应改为LLM友好：用Markdown而非HTML，避免“点击”指令，改用curl命令（如Vercel、Stripe正这样做）
    
-   Model Context Protocol (MCP) 让Agent直接与工具交互
    
-   工具如GitIngest（将GitHub仓库合并为单一文本）、DeepWiki（AI分析仓库生成文档页）
    

Roughly speaking, I think there's a new category of consumer and manipulator of digital information. It used to be just humans through GUIs or computers through APIs. And now we have a completely new thing. And agents are their computers, but they are human-like kind of, right? They're people spirits. There's people spirits on the internet, and they need to interact with their software infrastructure. What can we build for them? It's a new thing. So as an example, you can have robots.txt on your domain, and you can instruct or like advise, I suppose, web crawlers on how to behave on your website. In the same way, you can have maybe lms.txt file, which is just a simple markdown that's telling LLMs what this domain is about.

![[01_raw/_inbox/文章/images/711e940b933b61c21d15edd6f787615d_MD5.jpg]]

为Agent构建基础设施的示意图

## 八、结尾：钢甲套与自主滑块

总结：进入行业的绝佳时机。我们需要重写大量代码。LLM像电力、晶圆厂，尤其像操作系统，但处于1960年代水平。我们要学习与这些有缺陷的人灵合作，调整基础设施。构建部分自主产品：用GUI加速生成-验证循环，并提供自主滑块。在未来十年里，我们会将滑块从左推到右。我更倾向于建造“钢铁侠战甲”（人类增强）而非“钢铁侠机器人”（完全自主）。不要被闪亮的自主agent演示迷惑，要落地成真正的产品。

And I think what we'll see over the next decade, roughly, is we're going to take the slider from left to right. And I'm very interesting. It's going to be very interesting to see what that looks like. And I can't wait to build it with all of you. Thank you.

钢铁侠战甲与自主滑块概念图

  

---

内容效果不满意？[点此反馈](https://feedback.notebooksyncer.com/feedback/09ef38b5_1782241224877?u=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzIxNjkwODcxOQ%3D%3D%26mid%3D2247483868%26idx%3D1%26sn%3D4720de0681ec48fb523502493fc1ea99%26chksm%3D969713e019f105912f8fc9dbf00932d6c90d7545f95fe7fc1cdef08e72669b48dff334c1e162%26mpshare%3D1%26scene%3D1%26srcid%3D0624OsBghPJsz4Br48TdWhPt%26sharer_shareinfo%3D6ed8cee904ab8f47e35864cf847fa7f1%26sharer_shareinfo_first%3D6ed8cee904ab8f47e35864cf847fa7f1%23rd&s=obsidian)