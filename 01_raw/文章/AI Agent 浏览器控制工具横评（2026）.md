---
author: MYandong
source: 微信公众号
url: https://mp.weixin.qq.com/s?t=pages/image_detail&scene=1&__biz=MzkwNTcyMzg4OQ==&mid=2247485287&idx=1&sn=a0360342f49ab00a9ecb1f9b560aa836&from_masonry=1&sharer_shareinfo_first=7e1b510a92cea60cd5ae77f8dc0f129d&sharer_shareinfo=d48fafb03a1e7110f01e5cc8016eb182#wechat_redirect
saved: 2026-06-06 16:42:42
tags:
  - 笔记同步助手
annotation: AI control browser tips
id: 30acb83e-d108-45eb-bc73-558824507760
summary: "Compares two technical routes for AI browser control: Raw CDP tools (web-access, Browser Use, Claude in Chrome) which offer direct browser access with login state and anti-detection, versus Playwright-based tools (new CLI at 27K tokens vs classic MCP at 114K tokens). Recommends CDP for login/scraping tasks and Playwright for cross-browser testing."
processed: 2026-06-06
---

公众号名称：MYandong

发布时间：2026-04-12 12:23

让 AI Agent 操控浏览器，工具选错了差距很大 👇  
  
两条技术路线正在分化：  
  
🔵 Raw CDP 路线（直连浏览器，无中间层）  
· web-access — 带登录态，内置浏览策略，积累站点经验  
· Browser Use — 2026年初从Playwright迁移至CDP  
· Claude in Chrome — Anthropic官方Chrome扩展  
  
🔷 Playwright 路线（框架封装）  
· Playwright CLI — 2026新出，专为AI Agent设计，27,000 tokens/次  
· Playwright MCP — 经典款，跨浏览器，但114,000 tokens/次  
  
💡 核心趋势：Raw CDP = 无中间层，Browser Use的迁移是一次市场投票  
  
选型建议：  
✅ 需要登录态/反爬/社交媒体 → CDP系  
✅ 测试套件/跨浏览器验证 → Playwright系  
  
数据来源：各工具官方文档 + 2026年实测

图1：

![[01_raw/_inbox/文章/images/301cb453b4273d8b80d224aef72939f7_MD5.png|Image]]

图2：

![[01_raw/_inbox/文章/images/7801761fba1e55eed61e0f5e06174525_MD5.png|Image]]

图3：

![[01_raw/_inbox/文章/images/1eef3bcaecbc132049267bdc2ba07bf3_MD5.png|Image]]

图4：

![[01_raw/_inbox/文章/images/2f23484fc9a5e8a33d574f735a6193d2_MD5.png|Image]]

---

内容效果不满意？[点此反馈](https://feedback.notebooksyncer.com/feedback/1512237c_1780756959544?u=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3Ft%3Dpages%2Fimage_detail%26scene%3D1%26__biz%3DMzkwNTcyMzg4OQ%3D%3D%26mid%3D2247485287%26idx%3D1%26sn%3Da0360342f49ab00a9ecb1f9b560aa836%26from_masonry%3D1%26sharer_shareinfo_first%3D7e1b510a92cea60cd5ae77f8dc0f129d%26sharer_shareinfo%3Dd48fafb03a1e7110f01e5cc8016eb182%23wechat_redirect&s=obsidian)