---
author: 阿东玩AI
source: AI整理 - 小红书
url: https://www.xiaohongshu.com/discovery/item/6a43aa61000000000702177a?app_platform=ios&app_version=9.36&share_from_user_hidden=true&xsec_source=app_share&type=normal&xsec_token=CBndlfXrQ58YHJvGjCmEkBsgypYkHBxM0CHyTzhml-kgQ=&author_share=1&xhsshare=WeixinSession&shareRedId=Nzs4RERHO0tLPD1GOjswPEg5Qk06PjpN&apptime=1783020785&share_id=1fcac8e354b84111a96276134c2c4159&xstag=1&code=AtVCzBbDV5j
saved: 2026-07-02 21:36:28
tags:
  - 笔记同步助手
annotation:
id: 6a1a717e-1f83-4df8-a9dd-59398c64fce9
---

# 做Agent前，请先把Stanford CS336过一遍

## 做Agent前，请先把Stanford CS336过一遍

### 课程是什么

Stanford CS336，全称 **Language Modeling from Scratch**。从零手搓语言模型。

这门课的核心哲学就一句话：**自己实现一切**。

你得动手写 Tokenizer、写 Transformer Block、写 Attention、写优化器、写分布式训练代码。五个大 Assignment 全公开在 GitHub。

跟操作系统的思路一样。你不自己写一遍进程调度和内存管理，光看概念，永远差一层皮。

课程由 Percy Liang、Tatsunori Hashimoto、Marcel Rod 等主讲，2026 年是第三次开课，前一轮（Spring 2025）的 Lecture 视频已上传 YouTube。

---

### 做 Agent 的人，为什么特别需要过一遍 CS336

说实话，现在太多人做 Agent 的路径是这样的：

装个 LangGraph 或者 CrewAI，照着 tutorial 跑通一个 demo，觉得"我会了"。然后遇到问题就开始调 prompt、换模型、加 memory、加 retry——但说不清为什么不行，也不知道该改哪儿。

这不叫会做 Agent。这是在**碰运气**。

| 调框架路径 | CS336 路径 |
| --- | --- |
| 装 LangGraph / CrewAI | 手写 Tokenizer + Attention |
| 跑通 Tutorial Demo | 理解全链路机制 |
| 遇到问题 | 知道瓶颈在哪 |
| 调 Prompt → 换模型 → 加 Memory | 精准定位问题 → 高效解决 |
| 说不清为什么不行 | 框架只是底层能力上的一层皮 |

---

### CS336 能给的东西

#### LLM 全栈 Pipeline

1.  **数据收集与清洗**：Common Crawl、数据过滤、去重
2.  **Tokenization**：BPE、SentencePiece、词表构建
3.  **Transformer 架构**：Attention、FFN、LayerNorm、残差连接
4.  **训练与优化**：FlashAttention、Triton Kernel、分布式训练
5.  **Post-training**：SFT、RLHF / RLVR、数学推理、安全对齐
6.  **评估与部署**：Benchmark、推理优化、生产部署

#### 几个具体的连接点

-   你亲手写过 Tokenizer 之后，才会明白为什么 Agent 做 JSON 结构化输出时老出幺蛾子。某些 token 边界切分方式，天然就容易断裂格式。
-   你亲手写过 Attention 之后，才会懂为什么 long-horizon reasoning 和 tool calling 在长对话里不稳定。
-   Position encoding 和上下文窗口的物理限制，不是加 prompt 能绕过去的。

这些东西不是"优化的细节"。它们直接决定了你 Agent 的**能力上限**。

#### Post-training 与 Agent

课程后半段重点讲 SFT + RL，数学推理、安全对齐都在里面。这在 Agent 开发里直接就对上了：

-   模型怎么学会可靠地做 tool use 和 ReAct？本质是个 post-training 问题，不是 prompt engineering 问题。
-   Reward modeling 和 preference optimization 怎么做？这决定了你的 Agent 评测和迭代能不能形成闭环。
-   Hallucination 怎么控制？课程里有完整的讨论。

你做过一遍这些，再回头看那些 Agent 框架，就知道它们不过是在底层能力上包了一层皮。

#### 系统层

Assignment 2 还要求实现 FlashAttention、Triton kernel、分布式训练、内存优化。做生产级 Agent 系统的人绕不开这些。高并发、长上下文、成本控制，每一项都压在系统肩膀上。

---

### Stanford 自己怎么用 Agent

还有一件事特别触动我。

Stanford 给 CS336 专门写了个 Agent 使用规范（CLAUDE.md），明确规定 AI Agent 在这门课里的角色：

-   **Agent 是 teaching assistant，不是 solution generator**
-   禁止直接写代码、完成 TODO、给出最终实现
-   可以解释概念、review 代码、引导调试、提问题
-   核心原则就一个：**Learn by doing**

这门课自己在用最严格的方式告诉你：想真正掌握 Agentic 系统，必须自己动手。不是让 Agent 替你动手。

---

### 怎么开始：先过一遍，再决定做多深

先花 1–2 周把所有 Lecture 过一遍，建立全局框架。知道 LLM 从数据收集到部署的完整 pipeline 长什么样。然后再挑重点 Assignment 动手。至少做 Assignment 1（Tokenizer + Transformer 基础），Assignment 2 和 5 看时间。

#### CS336 五大 Assignment

1.  **Tokenizer + Transformer 基础**（建议必做） 手写 BPE Tokenizer，实现 Transformer Block、前向传播
2.  **系统优化** FlashAttention、Triton Kernel、内存优化、分布式训练
3.  **Scaling Laws** 模型规模实验、数据规模实验、计算最优分配
4.  **Post-training** SFT 监督微调、RLHF / RLVR、数学推理能力
5.  **综合项目** 端到端 LLM 训练、评估、安全对齐、部署

---

### 一点感受

我见过太多从业者，对整个 pipeline 只有零散的认知。这里读一篇论文、那里看一个 tutorial，但从来没有系统性地串起来过。

CS336 给你的就是这张**地图**。之后再读论文、看新技术，你能快速定位：它在哪个环节、动了什么、为什么有效。

课程主页 cs336.stanford.edu，YouTube 有 Spring 2026 完整播放列表，只开英文字幕看。GitHub 上 stanford-cs336 组织下五个 assignment 全部公开。想热身的话，先跑一遍 Karpathy 的 nanoGPT。

框架年年换。底层机制就那么几样东西。地基打牢了再往上盖楼，弯路会少走非常多。

![[01_raw/_inbox/文章/images/8cf6bad0e484241ead3110c9cc023e4f_MD5.jpg|Image]]![[01_raw/_inbox/文章/images/dbdbf9222067b9e2c035084ef7107dbf_MD5.jpg|Image]]![[01_raw/_inbox/文章/images/15c74103529a0b3632d608a1374bde08_MD5.jpg|Image]]![[01_raw/_inbox/文章/images/2b7769c37d16033e5c1f26e580b6331d_MD5.jpg|Image]]![[01_raw/_inbox/文章/images/0fc937055b4c32a50da8d556a94100e8_MD5.jpg|Image]]![[01_raw/_inbox/文章/images/e5862e9156d6add25fa5e23e70167a51_MD5.jpg|Image]]![[01_raw/_inbox/文章/images/ab227a4e1b3fef768323473c9872b8e5_MD5.jpg|Image]]![[01_raw/_inbox/文章/images/5683ed61b9555cf9641ac5e7fdd02870_MD5.jpg|Image]]![[01_raw/_inbox/文章/images/5fb12178c019b4fa72b0eda95b15e13c_MD5.jpg|Image]]![[01_raw/_inbox/文章/images/d0a99284f059140afa199136429f0f4b_MD5.jpg|Image]]

每一个计算机系大学生都应该在大学期间把CS336啃完。啃完后，你对LLM的理解和英语能力至少能到国内前1%。  
  
其实做Agent不是装个LangGraph跑通demo就叫会了。遇到问题就调prompt、换模型、加memory，但说不清为什么不行—— 碰运气。  
CS336的哲学就一句：自己实现一切。 Tokenizer、Attention、Transformer Block、分布式训练，五个Assignment全手写。  
  
\[一R\]写过Tokenizer，才知道为什么JSON结构化输出老出幺蛾子。  
\[二R\]写过Attention，才懂为什么长对话里tool calling不稳定。  
\[三R\]position encoding的物理限制，不是加prompt能绕过去的。  
  
这些不是优化细节，是Agent的能力上限。  
  
先花1-2周过完所有Lecture，建立LLM完整pipeline的全局框架。地基打牢再盖楼，弯路会少走非常多。  
  
代码在github.com/stanford-cs336，视频在youtobe。  
  
\#agent \#cs336 \#llm \#agent算法 \#动手学

---

### 评论

-   **A**: 还记得前两年刚开始接触LLM的时候，不能理解对话是怎么做的，为什么是model/user这种格式，也不理解LLM如何能调用工具。后来才知道这只是训练出来的，和其他神经网络没有本质区别，输入输出的是token罢了，没什么魔法\[捂脸R\]所以说确实得过一遍基础，即使不能完全掌握也要有点概念，不然总是在隔靴搔痒，头痛医头。
    -   **B**: 最近在做harness，做着做着又得回去复习基础\[笑哭R\]
    -   **C**: harness咋做的\[偷笑R\]\[偷笑R\]\[偷笑R\]是写权限 沙箱 工具 上下文 记忆这些吗？我感觉很多所谓的业务agent就是写prompt skill啥的
    -   **D**: 没必要做harness了，claude code codex已经把harness做得特别好了，如果做应用直接用现有的sdk可以更快落地，不用重新造轮子
-   **E**: 要不要再学习一下怎么写 cuda 核，怎么写汇编语言，怎么设计芯片？\[doge\]
    -   **F**: 有时间确实也该学\[微笑R\]
    -   **E**: 那你要不然把半导体制造也学一遍吧\[doge\]
-   **G**: 根本没必要 上学手推过所有ML/DL公式 写过所有算法代码 照样忘掉
    -   **H**: 还是有必要的 大概知道哪里是什么遇到问题了能定位 要不然两眼一黑毫无头绪
    -   **G**: 我感觉知道个大概就行 60分及格 多了真的没必要
-   **I**: 请问harness走什么好的教程吗
    -   **B**: 可以蹲一下，今晚出，本来说端午出的，拖到今天了
    -   **J**: 蹲一下
    -   **K**: 蹲一下，出了求踢
-   **L**: 一切都是promt+tool，nothing else
    -   **B**: harness的本质是这样的，思考一个问题，如何让你的harness去适配不同的模型？
    -   **M**: 太傲慢了
    -   **N**: 你一定很喜欢装skill吧\[doge\]

---

内容效果不满意？[点此反馈](https://feedback.notebooksyncer.com/feedback/19d18316-2dfb-47ae-aa91-38ee32b20ec5?u=https%3A%2F%2Fwww.xiaohongshu.com%2Fdiscovery%2Fitem%2F6a43aa61000000000702177a%3Fapp_platform%3Dios%26app_version%3D9.36%26share_from_user_hidden%3Dtrue%26xsec_source%3Dapp_share%26type%3Dnormal%26xsec_token%3DCBndlfXrQ58YHJvGjCmEkBsgypYkHBxM0CHyTzhml-kgQ%3D%26author_share%3D1%26xhsshare%3DWeixinSession%26shareRedId%3DNzs4RERHO0tLPD1GOjswPEg5Qk06PjpN%26apptime%3D1783020785%26share_id%3D1fcac8e354b84111a96276134c2c4159%26xstag%3D1%26code%3DAtVCzBbDV5j&s=vtoa)