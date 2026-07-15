---
author: 蛋仔成长笔记
source: 微信公众号
url: https://mp.weixin.qq.com/s?__biz=MzIwNjg4NjE0MA==&mid=2247484112&idx=1&sn=09789ccc20f2fdb55b9eb9e0c2e6f182&chksm=96592c009d4b151168006fd0e1aff0fe763715440ab383ab3774aa0f423cada1b3a6b50cd329&mpshare=1&scene=1&srcid=0518DBfrnYyOxHI5JI12NAZh&sharer_shareinfo=5680e11cd92be5869b998ba79aa82b1c&sharer_shareinfo_first=1aed597f7fe0db46c28f212472163a4f#rd
saved: 2026-05-29 00:04:16
tags:
  - 笔记同步助手
id: a3ab3ae1-6c16-4e17-bee2-a132812bd38e
annotation: how to deal with symbols in obsidian
summary: "A practical guide to standardized punctuation and symbol usage in Obsidian notes: use full-width Chinese punctuation (「」《》【】——) for Chinese prose and half-width ASCII for code/technical contexts. Establishes semantic conventions for each symbol type and a color-highlight system (red=concepts, orange=opinions, green=examples)."
processed: 2026-06-06
---

公众号名称：蛋仔成长笔记

作者名称：蛋仔成长笔记

发布时间：2026-03-19 18:18

之前分享过[文件命名规范](https://mp.weixin.qq.com/s?__biz=MzIwNjg4NjE0MA==&mid=2247484083&idx=1&sn=532b02722df2141d7074901d07311583&scene=21#wechat_redirect)了，但笔记内容里符号混用——这个问题我遇到过。

「直角引号」和"双引号"混着写，括号有时全角有时半角，书名号《》和【】黑括号不知道该用哪个。表面看是小问题，但笔记一多，整篇读下来总觉得哪里不对劲。

后来专门整理了一套符号应用规范，用到现在，笔记可读性确实上了一个台阶。

## 为什么符号规范比你想的重要

先说个真实场景。

之前看别人的Obsidian笔记，同一篇文章里，一会儿用「直角引号」引用对话，一会儿用"双引号"引用名词，再过几行又冒出来一个『』或者其他奇怪符号。内容是好内容，但读起来像流水线工人没校对的初稿。

符号的本质是什么？**是语义的标记**。

「直角引号」表示特指名词，【黑括号】表示文件标签，——《》表示书籍电影——这些是约定俗成的用法。你不遵守，读的人就得靠猜。

笔记是给自己看的，也是给未来某个时间点的自己看的。规范统一，未来扫一眼就知道结构层次在哪、省得回头猜自己当时写的是什么。

## 常见误区：符号混用的典型场景

先说几个我见过最多的错误：

### 1\. 引号混用

```
他说："这个问题很重要，要用「直角引号」处理。"
```

一顿话里同时出现三种引号，读起来像绕口令。标准用法：「」用于名词和特指内容，""用于原话引用，其他场景少用或不用。

### 2\. 括号中英文混搭

```
这是函数 test() 的用法（注意参数是字符串）。
```

一句话里同时出现英文()和中文（），视觉上很乱。解决方案：代码相关的用英文括号，中文语境用全角。

### 3\. 黑括号【】滥用

【】黑括号本来是文件命名标签专用，但很多人拿来当万能括号用，标题用、内容用、强调也用——结果就是失去强调效果，变成噪音。

### 4\. 省略号随手打

```
这也太...
```

六个点..... VS 三个点VS...，不同地方用不同的省略号。统一用...就行。

## 我的符号应用规范：分场景、记清楚

下面这套规范是我参考出版规范、结合Obsidian使用场景整理的，不复杂，记住几条就行。

### 标号规范：记住这个优先级

### 全角标号 - 中文语境

| 符号 | 名称 | 场景 |
| --- | --- | --- |
| （） | 小括号 | 前置条件/后置条件/补充说明 |
| 【】 | 黑括号 | 文件命名标签、功能名称 |
| 「」 | 直角引号 | 名词、特指内容引用 |
| 《》 | 书名号 | 书籍、电影、电视剧、游戏 |
| —— | 破折号 | 解释说明 |
| ... | 省略号 | 文中简化，用三个点 |

### 半角标号 - 代码/技术语境

| 符号 | 名称 | 场景 |
| --- | --- | --- |
| () | 小括号 | 函数参数、代码表达式、单位 |
| \[\] | 中括号 | 数组索引、正则分组 |
| {} | 大括号 | 代码块、对象字面量 |
| `` ` `` | 代码块 | 行内代码标记 |
| \- | 连接号 | 减号、连接号 |

**核心原则：中文内容用全角，技术内容用半角。两条线分开，不混用。**

### 组合符号：直观表达

<table style="border-collapse: collapse"><tfoot><tr><th data-colwidth="80" style="color: rgb(63, 63, 63); border: 1px solid \#ddd; padding: 6px 10px"><div style="color: rgb(0, 0, 0)"><span>符号</span></div></th><th data-colwidth="117" style="color: rgb(63, 63, 63); border: 1px solid \#ddd; padding: 6px 10px"><div style="color: rgb(0, 0, 0)"><span>名称</span></div></th><th style="color: rgb(63, 63, 63); border: 1px solid \#ddd; padding: 6px 10px"><div style="color: rgb(0, 0, 0)"><span>场景</span></div></th></tr><tr><td data-colwidth="80" style="border: 1px solid \#ddd; padding: 6px 10px"><span style="font-size: 15px; text-align: left">----&gt;</span></td><td data-colwidth="117" style="border: 1px solid \#ddd; padding: 6px 10px"><div style="font-size: 15px; text-align: left; color: rgb(0, 0, 0)"><span style="font-size: 15px; text-align: left">长箭头</span></div></td><td style="border: 1px solid \#ddd; padding: 6px 10px"><span style="font-size: 15px; text-align: left">从 A 到 B，应用于流程路径、地点路径</span></td></tr></tfoot></table>

### 例如：武汉天河机场--✈️-->丽江三义国际机场，丽江XXX酒店--🚌-->泸沽湖景区

### 特殊符号：几个高频场景

-   • **★五角星**：放在标题头部用于置顶，表示文中重点
    
-   • **🔴🟠🟢**：任务状态标记，未完成/进行中/已完成
    
-   • **✅❌**：正确/错误的判断标记
    
-   • **/** 和 **\\**：文件路径用正斜杠，代码公式用反斜杠
    

![[01_raw/_inbox/文章/images/d04d6dca16b0ee1fc64ee65816353b8d_MD5.png]]

### 颜色高亮：按语义选颜色

Obsidian支持高亮颜色，别乱用，固定语义：

-   • **红色**：概念、方法论、重点、问题
    
-   • **橙色**：观点、总结、经验
    
-   • **绿色**：案例、应用
    

  

![[01_raw/_inbox/文章/images/65abfeb8af74fb68ab05e70000ca781d_MD5.png]]

  

---

# 怎么执行：从今天开始

规范不用背，记住三个动作就行：

1.  1\. **新建笔记时，先确认符号环境**：中文语境默认全角，技术笔记默认半角
    
2.  2\. **同类内容用同类符号**：引号只选一种，括号只选一种
    
3.  3\. **每月检查10分钟**：扫一遍最近写的笔记，有混用的随手改
    

规范这东西，不怕慢，就怕乱。一旦立了规矩，后面就是肌肉记忆。

你在Obsidian里写笔记时，有遇到过符号混用的困扰吗？现在是怎么处理的？欢迎评论区分享你的经验，或者提出具体问题，我来帮你解答。

## 往期推荐：

[Obsidian双链都用不对，怎么可能做得好知识体系](https://mp.weixin.qq.com/s?__biz=MzIwNjg4NjE0MA==&mid=2247484103&idx=1&sn=f9d2e45664e12fa15d44fb055ce7ef14&scene=21#wechat_redirect)

[如何用 Obsidian 把碎片变成资产](https://mp.weixin.qq.com/s?__biz=MzIwNjg4NjE0MA==&mid=2247484090&idx=1&sn=200d0e07e54cbd88c3161b17748a2d67&scene=21#wechat_redirect)

[别再乱命名了！Obsidian文件命名规范，让你的笔记井井有条](https://mp.weixin.qq.com/s?__biz=MzIwNjg4NjE0MA==&mid=2247484083&idx=1&sn=532b02722df2141d7074901d07311583&scene=21#wechat_redirect)

[用 Obsidian 做项目管理：一份完整的实践指南](https://mp.weixin.qq.com/s?__biz=MzIwNjg4NjE0MA==&mid=2247484068&idx=1&sn=b19bad721c209fdd8a057d63d169095b&scene=21#wechat_redirect)

[我用Obsidian如何搞定复杂任务](https://mp.weixin.qq.com/s?__biz=MzIwNjg4NjE0MA==&mid=2247484049&idx=1&sn=d1000951d49f5cb343a59e632e364c19&scene=21#wechat_redirect)

---

![[01_raw/_inbox/文章/images/001ca3a5006dd3bcaa8af626877963f1_MD5.jpg|cover_image]]

Original 蛋仔成长笔记 蛋仔成长笔记

---

内容效果不满意？[点此反馈](https://feedback.notebooksyncer.com/feedback/195a843c_1780005854502?u=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzIwNjg4NjE0MA%3D%3D%26mid%3D2247484112%26idx%3D1%26sn%3D09789ccc20f2fdb55b9eb9e0c2e6f182%26chksm%3D96592c009d4b151168006fd0e1aff0fe763715440ab383ab3774aa0f423cada1b3a6b50cd329%26mpshare%3D1%26scene%3D1%26srcid%3D0518DBfrnYyOxHI5JI12NAZh%26sharer_shareinfo%3D5680e11cd92be5869b998ba79aa82b1c%26sharer_shareinfo_first%3D1aed597f7fe0db46c28f212472163a4f%23rd&s=obsidian)