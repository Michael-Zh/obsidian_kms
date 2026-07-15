---
author: 豆丁奶爸
source: 微信公众号
url: https://mp.weixin.qq.com/s?__biz=MzU4ODAxMzEyOQ==&mid=2247485101&idx=1&sn=dde5490a4affe0a0f72dae5718ccf556&chksm=fcaece773b71cd85a98973531ed78fb2879f1ead3e545d8763de0d2be07b286a93b705826b98&mpshare=1&scene=1&srcid=0521KIfHNiMpbuC0qTkkxrMs&sharer_shareinfo=9fef01a5d81230b16c071cbcc445c18f&sharer_shareinfo_first=342390ea497da87990e0c0b26dd82f7e#rd
saved: 2026-05-29 00:02:27
tags:
  - 笔记同步助手
id: 9e2271eb-812a-4eda-b9f9-1205201a1806
annotation: use draw.io to make flow charts in obsidian (may be useful to update my AI assistant modules)
summary: Tutorial on embedding draw.io architecture diagrams directly in Obsidian using the Diagrams plugin and OpenCode AI agent. Demonstrates creating microservice architecture diagrams and workflow swimlane diagrams using natural language prompts, with the AI generating and styling the XML diagram files in-vault.
processed: 2026-06-06
---

公众号名称：和小丁一起成长

作者名称：豆丁奶爸

发布时间：2026-03-24 07:15

# 一、写在前面

之前写了两篇在vscode和opencode中使用draw.io的文章：  
《vscode+opencode+draw.io用自然语言就能轻松画架构图》  
《opencode+draw.io+skill让你更专注于画图逻辑》

但是我发现一个问题：Obsidian逐渐成了我的主要工作平台，是否能在Obsidian中使用draw.io呢？

我大致研究了下，还果真行，这篇文章记录下**如何用Obsidian+opencode+draw.io画架构图**。

# 二、准备工作

## 1、安装Diagrams插件

在社区插件市场搜索draw.io，发现有两个可选的插件：

![[01_raw/_inbox/文章/images/61f3457991bd1771c61810c9fdf0d757_MD5.png]]

其实我也不知道该选哪个，只是发现左边这个最近有更新，就选择了这个。

安装后启用这个插件即可：

![[01_raw/_inbox/文章/images/e6f15389380bd0932101293747cf9010_MD5.png]]

安装好之后，Obsidian的左上角应该有**New diagram**的图标。

![[01_raw/_inbox/文章/images/d57dc9b30da90e31ae225454032c431b_MD5.png]]

这样，插件应该就算是安装好了。

## 2、安装opencode

这个就不详细说了，如果还不会安装，请翻前面的文章《走了不少弯路，终于完成了Obsidian与OpenCode对接》。

# 三、画图试用

到此为止，所有的准备工作都做好了，下面举两个例子。

## 例子一：画微服务架构图

在opencode对话框里输入：

```
请画一个微服务架构图
```

下面就是画出来的效果：

![[01_raw/_inbox/文章/images/37241a47badd7e3662e3335e28c53361_MD5.png]]

说实话，有点土，这个时候可以用之前的画架构图的skill来美化下。  
美化后的效果如下：

![[01_raw/_inbox/文章/images/a91f62e1dedc855616e40c132eecdfec_MD5.png]]

## 例子二：画TELOS运作泳道图

上篇《用Obsidian+OpenCode搭建了自动进化笔记系统》中完整复刻了TELOS系统，但是这个系统还是比较复杂，当时我并没有完全搞懂其内部的运作原理。

现在有了draw.io工具，正好可以以画微服务架构图为契机，画出TELOS的运作流程图。  
在对话框中输入：

```
现在从你收到“画微服务架构图”的指令开始，请你把TELOS的整个运作流程用draw.io画出来。生成的draw.io图文件放在当前打开的文件的同级目录下。
```

下面这个就是画出来的效果，当然我也做了一点手工微调，主要是把重叠的箭头撑开。

![[01_raw/_inbox/文章/images/1f96466b06eda47d2faadf54c0bfa67c_MD5.png]]

有了这个图，也就能更容易地理解TELOS系统的运作过程了。

# 四、写在最后

这篇文章记录下**如何用Obsidian+opencode+draw.io画架构图**。感兴趣的同学可以亲自尝试下，有疑问也可以在评论区交流。

---

![[01_raw/_inbox/文章/images/657d59ade28d3f24c44409e02d55dcf1_MD5.jpg|cover_image]]

Original 豆丁奶爸 和小丁一起成长

---

内容效果不满意？[点此反馈](https://feedback.notebooksyncer.com/feedback/c42d858b_1780005746774?u=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzU4ODAxMzEyOQ%3D%3D%26mid%3D2247485101%26idx%3D1%26sn%3Ddde5490a4affe0a0f72dae5718ccf556%26chksm%3Dfcaece773b71cd85a98973531ed78fb2879f1ead3e545d8763de0d2be07b286a93b705826b98%26mpshare%3D1%26scene%3D1%26srcid%3D0521KIfHNiMpbuC0qTkkxrMs%26sharer_shareinfo%3D9fef01a5d81230b16c071cbcc445c18f%26sharer_shareinfo_first%3D342390ea497da87990e0c0b26dd82f7e%23rd&s=obsidian)