---
author: yablog
source: 微信公众号
url: https://mp.weixin.qq.com/s?t=pages/image_detail&scene=1&__biz=MzIwNzU5MzY4OQ==&mid=2247486349&idx=1&sn=7fff7337debbc53f76311a8e2e2c36d7&from_masonry=1&sharer_shareinfo_first=c2a0273799e5b9d86df302975e7da5b0&sharer_shareinfo=a428934419b2299525db77b7f59c6e85#wechat_redirect
saved: 2026-05-29 00:03:03
tags:
  - 笔记同步助手
id: 940d84c7-cdd9-4917-8bbc-5ea8309244cf
annotation: Kimi WebBridge tips
summary: "Technical analysis of Kimi WebBridge, a browser extension providing AI agents programmatic browser control via Chrome DevTools Protocol (CDP). Uses WebSocket for local communication, CDP for execution, and an accessibility-tree snapshot+@ref system for element identification — exposing 16 atomic browser tools. Introduces color-coded Session-based tab grouping for multi-task clarity."
---

公众号名称：yablog

发布时间：2026-05-16 12:20

Kimi 官网昨天发布了一款 AI Agent 的浏览器插件：Kimi WebBridge，让 AI 通过 Chrome 插件方式自动帮你操作浏览器，Demo 效果酷炫且使用，AI 离真正接管浏览器真的不远了。  
  
分析了它的源码之后，基本上可以得出这个结论：技术原理和 Vercel 团队出品的agent-browser 产品一模一样（核心都是基于 CDP 协议，然后采用 Snapshot+@ref 方案来定位并操作元素参见图5，详见[agent-browser：为AI Agent 写的浏览器CLI](https://mp.weixin.qq.com/s?__biz=MzIwNzU5MzY4OQ==&mid=2247486082&idx=1&sn=68860cb626f874e6753331df42a06452&scene=142#wechat_redirect)）。  
  
更准确的说：Kimi WebBridge 的技术路线大概率是对 agent-browser 的借鉴（后者已开源）。二者的服务对象是 AI Agent（而非人类用户），只是 Kimi 团队把它封装成了一个浏览器插件的产品形态。  
  
除此之外，Kimi WebBridge 还把所有浏览器操作封装成了16个原子工具（tools），暴露给 AI Agent，每个工具背后都对应一个或多个 CDP 命令如参见图4  
  
如果要说创新，那应该是在交互方式上。对于“要接管用户的浏览器操作，同时又要保持明面上的合规”的 C 端用户场景，浏览器插件是最好的选择。  
  
同时，Kimi WebBridge 还支持了 Session 概念：同一个 AI 任务打开的多个标签页，会自动被归入同一个 Chrome Tab Group，并分配颜色。其他 Session 按轮转分配 green / yellow / cyan / orange / pink / grey，总共 6 种颜色。这让用户在多任务并行时，能从标签栏一眼区分哪些 tab 属于哪个 AI 任务。这对于需要同时操作许多个网站完成一项任务的场景来说非常有价值。  
  
总结一下，Kimi WebBridge 是一个设计目标非常明确的工具：给 AI Agent 提供一个可编程的浏览器控制接口。  
  
它的技术路线可以概括为以下三点：  
\- 1）WebSocket 做通信桥：本地 Daemon 进程通过 ws://127.0.0.1:10086/ws 与插件通信，协议简单清晰。  
\- 2）CDP 做执行层：所有浏览器操作通过 chrome.debugger API 走 CDP 协议完成，无 Content Script 注入，绕过 CSP，零页面污染。  
\-3）snapshot + @ref 做感知层：通过无障碍树提供语义化的页面结构，让 AI 以「角色+名称」的方式操作元素，而非脆弱的 CSS Selector。

图1：

![[01_raw/_inbox/文章/images/dab1a63d9e815360cd69a08b22eea399_MD5.jpg|Image]]

图2：

![[01_raw/_inbox/文章/images/551b525debc98a806e879c283a6f649b_MD5.jpg|Image]]

图3：

![[01_raw/_inbox/文章/images/425d51ff6fc0ab3a15f150f34b6e91d3_MD5.jpg|Image]]

图4：

![[01_raw/_inbox/文章/images/7bbcc926a1994fe41fe8cef117acd213_MD5.jpg|Image]]

图5：

![[01_raw/_inbox/文章/images/86408eae042cd34511148f6fdc34c319_MD5.jpg|Image]]

图6：

![[01_raw/_inbox/文章/images/7bd9986a4c2409a31ef39e04199f0bd7_MD5.jpg|Image]]

---

内容效果不满意？[点此反馈](https://feedback.notebooksyncer.com/feedback/2344c85c_1780005781740?u=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3Ft%3Dpages%2Fimage_detail%26scene%3D1%26__biz%3DMzIwNzU5MzY4OQ%3D%3D%26mid%3D2247486349%26idx%3D1%26sn%3D7fff7337debbc53f76311a8e2e2c36d7%26from_masonry%3D1%26sharer_shareinfo_first%3Dc2a0273799e5b9d86df302975e7da5b0%26sharer_shareinfo%3Da428934419b2299525db77b7f59c6e85%23wechat_redirect&s=obsidian)