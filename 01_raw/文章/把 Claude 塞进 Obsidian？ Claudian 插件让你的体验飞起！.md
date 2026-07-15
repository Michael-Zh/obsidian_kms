---
author: 科叔
source: 微信公众号
url: https://mp.weixin.qq.com/s?__biz=MzkzODkwODYwMA==&mid=2247487783&idx=1&sn=bdb27fc94201de55df6f335b079813b8&chksm=c37812895dc17e8a0bbad16233d32741a102149fa8adb466fc61adcb6a255b79519d4f44996c&mpshare=1&scene=1&srcid=0502Ez78fmtFQ94fBc3aKLxB&sharer_shareinfo=99507b1f049141b382e73daa54c63a00&sharer_shareinfo_first=f557e77fa30c6683f6e405f556d4d308#rd
saved: 2026-05-29 00:04:09
tags:
  - 笔记同步助手
id: 498eb995-6bfb-47f0-b771-2e3a5cb78196
annotation: use claude code in obsidian
summary: Introduction to Claudian, an Obsidian plugin that embeds Claude Code as an in-vault AI agent with inline editing (diff preview), multi-tab persistent conversations, Plan Mode, MCP server connections, and @mention file references. All conversation data and settings are stored locally in the vault, with support for domestic Chinese model providers.
processed: 2026-06-06
---

公众号名称：科叔AI进化记

作者名称：科叔

发布时间：2026-04-20 22:29

![[01_raw/_inbox/文章/images/312c491a8bc2e7338988b6e12945a8e8_MD5.png]]

## 为什么你需要 Claudian？

你有没有遇到过这样的场景：

-   在 Obsidian 写笔记时，想要 AI 帮你润色、扩展内容，却得来回切换应用？
    
-   手动复制粘贴到 Claude，再复制回来，效率低到怀疑人生？
    
-   想让 AI 直接操作你的 vault，帮你整理文件、搜索内容、甚至写代码？
    

**Claudian** 就是来解决这些痛点的！

## 什么是 Claudian？

Claudian 是一个 Obsidian 插件，它能把 Claude Code 这样的 AI 编码代理**直接嵌入到你的 vault 中**，让它成为你的协作助手。

![[01_raw/_inbox/文章/images/644021815176824a770c7bdf911478a2_MD5.png]]

下载地址：https://github.com/YishenTu/claudian

你的 vault 不再只是笔记存储库，而变成了代理的工作目录——所有文件读/写、搜索、命令执行都能无缝完成。

## ✨ 核心功能亮点

-   📝 **Inline Edit**：选中文字，一键让 AI 帮你改，还能预览差异
    
-   💬 **多标签页聊天**：同时进行多个对话，历史记录自动保存
    
-   🎯 **Plan Mode**：AI 先给你设计方案，你点头了它再动手
    
-   🔌 **MCP 服务器**：连接外部工具，扩展能力无上限
    
-   📁 **@mention 文件**：直接引用 vault 里的文件，让 AI 处理特定内容
    
-   🛠️ **Slash Commands**：输入 `/` 就能调用预设的提示模板
    

## 💾 数据完全本地化，隐私不用担心！

这是 Claudian 最大的优势——**所有数据都保存在本地**：

| 数据类型 | 保存位置 |
| --- | --- |
| Claudian 设置和会话元数据 | `vault/.claudian/` |
| Claude 提供者文件 | `vault/.claude/` |
| Claude 对话记录 | `～/.claude/projects/` |
| Codex 会话记录 | `～/.codex/sessions/` |

你的笔记、对话、配置都在自己的机器上，安全可控。

## 📦 安装步骤

### 手动安装（稳妥适合所有人）

1.https://github.com/YishenTu/claudian/releases 下载这三个文件：

![[01_raw/_inbox/文章/images/a2920bd7112570f817e9631ab3fe47d6_MD5.png]]

### 2\. 在你的 obsidian仓库里，根据下面路径创建claudian文件夹：

```
/vault/.obsidian/plugins/claudian/
```

### 3.把下载的三个文件复制进去

![[01_raw/_inbox/文章/images/a2941b3625fd2b18b5efd9f42ed57ab7_MD5.png]]

### 3.打开 Obsidian：设置 → 社区插件 → 启用 "Claudian"

![[01_raw/_inbox/文章/images/952d47a900fa35a84110e155873411ed_MD5.png]]

## 配置这块最关键：

![[01_raw/_inbox/文章/images/293e07b245873f8887b91e28e4e22f22_MD5.png]]

![[01_raw/_inbox/文章/images/f6ebf879947e13a46a8665637b771762_MD5.png]]

填入接入的模型配置参数

ANTHROPIC\_API\_KEY=your-key

ANTHROPIC\_BASE\_URL=https://api.example.com

ANTHROPIC\_MODEL=custom-model

国内用户可以直接接入 智谱、MiniMax、Kimi、这些支持 Claude Code 的平台，按各自文档配就行，最推荐智谱GLM 5.1。

我目前用的是方舟 Coding Plan https://volcengine.com/L/HpmhTOz9yFY/邀请码：WDRBL3GB

发一条消息收到回复，就说明搞定了。

![[01_raw/_inbox/文章/images/1708c54d05bdcaba2ed38d8e53c7a4e6_MD5.png]]

## 🎯 工作流示例

### 场景 1：写作润色

**痛点**：写文章时反复修改文字，但总觉得不够通顺，想要 AI 帮你优化风格和表达。

![[01_raw/_inbox/文章/images/da47a94018fc61ff8e3a9a24eedc176c_MD5.png]]

**操作步骤**：

1.  在 Obsidian 中选中你想要润色的段落
    
2.  点击工具栏的 Claudian 图标
    
3.  输入你的需求，比如：
    

-   "帮我润色这段话，让它更专业、更有说服力"
    
-   "把这段改写成小红书风格，增加一些emoji"
    
-   "简化这段表达，让它更容易理解"
    

5.  Claude 会直接在你笔记里修改，你还能看到**差异对比**：
    

-   ✅ 绿色显示新增内容
    
-   ❌ 红色显示删除内容
    
-   一键接受或拒绝修改
    

**实际效果**：

-   不用复制粘贴到外部 AI 工具
    
-   修改过程完全在 Obsidian 内完成
    
-   可以反复迭代，直到满意为止
    
-   保留了原文和修改记录，方便回溯
    

---

### 场景 2：知识整理

**痛点**：笔记越写越多，但散落在各个文件里，想要快速整合某个主题的所有内容。

**操作步骤**：

1.  用 `@mention` 语法引用你想要整理的笔记：
    

![[01_raw/_inbox/文章/images/b8d598a37a081b1ab20d672d2cabfa3e_MD5.png]]

```
@笔记A @笔记B @笔记C 帮我总结这三篇笔记的核心观点，找出它们之间的关联
```

1.  Claude 会读取这些文件的内容，进行分析和总结
    
2.  它可以帮你：
    

-   提取每篇笔记的核心观点
    
-   找出笔记之间的共性和差异
    
-   识别知识图谱中的空缺
    
-   自动生成一篇新的整理笔记
    

4.  你可以继续追问："基于这个总结，帮我列一个后续学习计划"
    

**实际效果**：

-   一键整合多篇笔记，不用逐个打开阅读
    
-   AI 帮你发现笔记之间隐含的关联
    
-   自动建立知识网络，而不是孤立的笔记
    
-   可以根据整理结果，快速生成新的笔记
    

**进阶技巧**：

-   用 `@文件夹名/*` 引用整个文件夹的笔记
    
-   让 AI 生成一个该主题的知识图谱
    
-   让 AI 标出你尚未覆盖的知识盲点
    
-   让 AI 推荐相关的阅读材料
    

---

### 场景 3：创建索引和汇总

**痛点**：每天写了很多笔记，但缺少一个统一的入口来快速查看当天的所有内容。

![[01_raw/_inbox/文章/images/96291a1f3ea50d2110e19091f677240f_MD5.png]]

**操作步骤**：

1.  让 Claudian 搜索今天创建的所有笔记：
    
    ```
    搜索今天（2026-04-20）创建的所有笔记，帮我汇总一个今日工作清单
    ```
    
2.  AI 会自动：
    

-   扫描 vault 中的时间戳或文件名
    
-   提取每篇笔记的标题、核心内容、标签
    
-   按类别分组整理（如：文章创作、学习笔记、任务记录）
    
-   生成一个结构化的汇总文档
    

4.  你可以让 AI 进一步优化：
    

-   "在这个汇总中，帮我标注哪些是优先完成的"
    
-   "添加一个今日产出统计表格"
    
-   "生成一个明日待办建议"
    

**实际效果**：

-   一键生成今日工作清单，不用手动整理
    
-   自动识别笔记类型和优先级
    
-   可以形成日复日记，便于回顾
    
-   支持多维度统计（字数、篇数、主题分布）
    

**进阶技巧**：

-   把这个流程保存为 Skill，每天自动执行
    
-   让 AI 识别笔记之间的关联，生成知识网络
    
-   结合 Dataview 插件，动态展示数据
    
-   生成周报、月报模板
    

---

### 场景 4：优化内容质量

**痛点**：写完文章后，想要系统性地提升文案质量，但不知道从哪里入手。

**操作步骤**：

1.  选中你写的整篇文章或某个章节
    
2.  在 Claudian 中发送指令：
    

1.  ```
    Prompt:                                     帮我从以下几个维度分析这段文案：
    逻辑是否清晰，论证是否充分
    语言是否简洁，有无冗余表达
    标题是否吸引人，开头是否抓眼球
    结尾是否有力，是否有行动号召
    是否有错别字或语法错误
    请给出具体的修改建议
    ```
    
2.  AI 会提供：
    

-   问题清单：具体指出哪里需要改进
    
-   修改建议：给出多个优化方案
    
-   对比示例：展示修改前后的效果
    
-   评分：给出当前文案的质量分数
    

4.  你可以选择让 AI 直接修改，或者手动采纳建议
    

**实际效果**：

-   系统性的质量检查，不遗漏细节
    
-   提供多个优化方案，有选择性
    
-   边改边学，提升自己的写作能力
    
-   可以建立个性化的评分标准
    

**进阶技巧**：

-   针对不同平台制定不同的评估标准
    
-   让 AI 学习你的写作风格，给出更贴合的建议
    
-   批量处理多篇旧文章
    
-   建立文案质量追踪表
    

---

### 场景 5：统一标签和分类

**痛点**：笔记多了之后，标签五花八门，文件夹结构混乱，难以搜索和管理。

![[01_raw/_inbox/文章/images/6497dce3ececfa3df76da1319e198abe_MD5.png]]

操作步骤：

1.  让 Claudian 扫描你的 vault：
    
    ```
    扫描我的知识库，分析所有笔记的标签和分类情况：
    找出重复或相似的标签（如 \#AI 和 \#人工智能）
    找出使用频率低的孤立标签
    找出应该建立关联的分散笔记
    识别文件结构是否合理
    请给出优化建议
    ```
    
2.  AI 会提供：
    

-   标签整顿方案：合并、重命名、删除的建议
    
-   分类重组建议：如何调整文件夹结构
    
-   缺失标签提示：哪些笔记缺少标签
    
-   关联建议：哪些笔记应该建立双向链接
    

4.  你可以让 AI 自动执行：
    
    ```
    帮我执行以下操作：
    - 把 \#AI 和 \#人工智能 合并为 \#AI
    - 给所有"Obsidian教程"系列的笔记添加 \#教程 标签
    - 建立这些笔记之间的双向链接
    ```
    
5.  或者你手动审查后再操作
    

**实际效果**：

-   标签系统规范，搜索更高效
    
-   文件夹结构清晰，维护成本低
    
-   发现隐藏的知识关联
    
-   形成结构化的知识网络
    

**进阶技巧**：

-   建立标签命名规范（层级、格式）
    
-   定期执行标签审计，保持系统健康
    
-   结合 Dataview 插件，生成标签统计报告
    
-   为不同类型的笔记预设标准标签模板
    

## 🌟 结语

如果你是 Obsidian 重度用户，同时又在使用 Claude，那么 Claudian 基本上是必装的。

它让两个强大的工具产生了化学反应——你的知识库变成了强大的 AI 的工作台，AI 变成了你笔记的一部分。

**试试吧，你会发现效率提升不止一个台阶！**

如果本文恰好帮到你，不妨点赞+收藏+分享，让科叔知道你来过！❤️

以上就是今天的分享内容，我们下期见。

> END

**<精选教程合集>**

**[Obsidian+AI打造人生管理系统](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzkzODkwODYwMA==&action=getalbum&album_id=4355166178646786051#wechat_redirect)**

![[01_raw/_inbox/文章/images/d209e8fe99f772cb2b6a8d17fb02d576_MD5.png|![]]](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzkzODkwODYwMA==&action=getalbum&album_id=4355166178646786051#wechat_redirect)

#Obsidian #claude code #AI自动化#AI工作流#skills

---

![[01_raw/_inbox/文章/images/1e2dc3c4626cf3fab602a2aa0e69718b_MD5.jpg|cover_image]]

Original 科叔 科叔AI进化记

---

内容效果不满意？[点此反馈](https://feedback.notebooksyncer.com/feedback/c2b9c4d3_1780005847765?u=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzkzODkwODYwMA%3D%3D%26mid%3D2247487783%26idx%3D1%26sn%3Dbdb27fc94201de55df6f335b079813b8%26chksm%3Dc37812895dc17e8a0bbad16233d32741a102149fa8adb466fc61adcb6a255b79519d4f44996c%26mpshare%3D1%26scene%3D1%26srcid%3D0502Ez78fmtFQ94fBc3aKLxB%26sharer_shareinfo%3D99507b1f049141b382e73daa54c63a00%26sharer_shareinfo_first%3Df557e77fa30c6683f6e405f556d4d308%23rd&s=obsidian)