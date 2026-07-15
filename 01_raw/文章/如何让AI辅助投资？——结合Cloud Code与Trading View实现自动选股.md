---
author: 不老登AI
source: 小红书
url: https://www.xiaohongshu.com/discovery/item/6a196fb20000000035021d2c?app_platform=ios&app_version=9.32.2&share_from_user_hidden=true&xsec_source=app_share&type=video&xsec_token=CBiSPLlNUr-HpQM-Cx0u_xmdpS7N_TperdjRmZz85JaSk=&author_share=1&xhsshare=WeixinSession&shareRedId=Nzs4RERHO0tLPD1GOjswPEg5Qk06PjpN&apptime=1780178312&share_id=68ece722775a4218999314a501232247&code=3LouIa6wipM
saved: 2026-05-31 00:01:33
tags:
  - 笔记同步助手
id: e956f2bb-64b0-47fe-b448-b5a8081ed65f
annotation: how to use AI to pick stocks
summary: "Demonstrates connecting Claude Code to TradingView via an open-source GitHub project to automate stock screening: the AI interprets a natural-language investment strategy, screens all A-share stocks for moat characteristics, adds 13 qualifying stocks to a TradingView watchlist, and sets 52-week low price alerts."
processed: 2026-06-06
---

# 如何让AI辅助投资？——结合Cloud Code与Trading View实现自动选股

作者：不老登AI

## 引言：AI与看盘软件的融合

本文将展示如何让AI与看盘软件（如Trading View）深度结合，自动执行投资策略，提升决策效率。整个过程无需复杂编程，仅需借助Cloud Code平台和开源代码即可快速搭建。

## 实现步骤

首先，在GitHub上找到相关的开源项目链接。复制项目中的提示词（Prompt），然后将其粘贴到Cloud Code的输入框中。按下回车键后，Cloud Code便会自动执行脚本，完成与Trading View的连接配置。

笔者已预先完成连接，下面直接演示AI如何协助投资。

## AI自动执行投资策略

在Cloud Code中输入投资策略：例如，在A股各板块中挑选具有护城河且扼住行业瓶颈的企业股票。AI接收到指令后，会自动进行以下操作：

-   从全市场筛选符合条件的股票
-   将选中的股票自动加入Trading View的监控列表
-   监控这些股票的价格，当价格触及52周内最低点时发送提醒

最终，AI成功筛选出13只股票，并自动添加到监控列表，实现了全流程的智能化管理。

![[01_raw/_inbox/文章/images/b13f8513eb8240b6c1a166868c4ab431_MD5.jpg|AI根据投资策略自动筛选出13只股票并加入监控列表的界面]]

AI根据投资策略自动筛选出13只股票并加入监控列表的界面

## 风险提示

需要注意的是，股市有风险，投资需谨慎。AI提供的建议仅供参考，切勿盲目迷信。投资者应结合自身判断和市场分析做出最终决策。

## 逐字稿

**00:00** 让 ai 和看盘软件结合自动执行你的投资策略是一种什么体验今天我给大家展示一下

**00:07** 现在比较有名的看盘软件就是 trading view 我今天把 cloud code 跟 trading view 结合方法很简单在 GitHub 上找到这个开源链接复制这段提示词然后粘贴到 cloud code 输入框里回车 cloud code 就会自动执行

**00:22** 我这里已经让他俩无缝连接好了接下来演示 a i 怎么协助投资我在 cloud code 里输入我的投资策略在 a 股各个板块中挑选具有护城河的扼住行业瓶颈的企业股票然后加入到 TradingView的列表里监控他们最低价的时候提醒我然后 cloud code 就自动执行最后帮我选出十三只股票自动加入 TradingView的列表在五十二周内股价最低的时候提醒我以后就可以用 a i 来帮助我投资了最后提醒大家股市有风险投资需谨慎 a i 只能作为参考

**00:53** 不能迷信 ai

---

内容效果不满意？[点此反馈](https://feedback.notebooksyncer.com/feedback/44d04fb7-f066-41eb-af1d-3df0c21b5dd6?u=https%3A%2F%2Fwww.xiaohongshu.com%2Fdiscovery%2Fitem%2F6a196fb20000000035021d2c%3Fapp_platform%3Dios%26app_version%3D9.32.2%26share_from_user_hidden%3Dtrue%26xsec_source%3Dapp_share%26type%3Dvideo%26xsec_token%3DCBiSPLlNUr-HpQM-Cx0u_xmdpS7N_TperdjRmZz85JaSk%3D%26author_share%3D1%26xhsshare%3DWeixinSession%26shareRedId%3DNzs4RERHO0tLPD1GOjswPEg5Qk06PjpN%26apptime%3D1780178312%26share_id%3D68ece722775a4218999314a501232247%26code%3D3LouIa6wipM&s=vtoa)