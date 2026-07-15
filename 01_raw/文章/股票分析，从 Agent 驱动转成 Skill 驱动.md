---
author: NPointer
source: AI整理 - 小红书
url: https://www.xiaohongshu.com/discovery/item/6a34f5c5000000001503da33?app_platform=ios&app_version=9.34.4&share_from_user_hidden=true&xsec_source=app_share&type=normal&xsec_token=CB83kHhlswtAWARboUQV0SZOKZuIauyvOqH7MoO-oydoM=&author_share=1&xhsshare=WeixinSession&shareRedId=Nzs4RERHO0tLPD1GOjswPEg5Qk06PjpN&apptime=1781989269&share_id=93330a99cab14c57aefdb57aa9e5febc&code=6PgcKNBWZbJ
saved: 2026-06-20 23:03:13
tags:
  - 笔记同步助手
annotation: Use Claude for investment
id: ee733f6f-df01-45f0-98e2-a43b53cfa2fc
---

# 股票分析，从 Agent 驱动转成 Skill 驱动

## 股票分析，从 Agent 驱动转成 Skill 驱动

### 核心变化：从特定 Agent 架构驱动，到 Skill 驱动

大家应该都知道我的 Agent 股票分析项目，流程是长在某个 agent 上的。

这是“特定 Agent 架构驱动”的方法。

现在换了种干法。

把分析拆成一个个 skill：数据、估值、预期、业绩、研报。每个就是一个 `SKILL.md` 加几段脚本和模板。

agent 只负责按它执行，而不是固定死一个架构。

分析一只股票，可以用自己安装后的 skill，最后吐出带 K 线、估值三角、五维评分的 HTML。

无论是 Claude Code，还是 Cursor，只要有这些 skill，就能复制我的分析流程。

Anthropic 十月发 Agent Skills，原始定义就是“装着指令、脚本和资源的文件夹”；两个月后又作为开放标准发布，理由很直白——跨平台可移植。

意思很明白：Skill 是可移植的方法。

研报就是使用我收集到的几个 skill 产出的。换 agent 跑，结论也一样，因为方法不在 agent 那边。

所以这个转变，核心是方法从工具里解耦。

以前 agent 是主角，方法是它的附属；现在方法沉淀进 Skill 当主角，agent 退成可插拔的执行端。

之后会把自己使用的 skill 分享出来。注意，是我收集的，不是我编写的。

---

### 一套 Skill 跑通股票分析

#### 01 DATA：数据采集

行情、财报、资金面、公告。

#### 02 VALUE：估值建模

多模型交叉验证、敏感度分析。

#### 03 EST：预期追踪

一致评级、修正趋势、目标价。

#### 04 EPS：业绩复盘

营运质量、拐点、同业对标。

#### 05 REPORT：研报生成

分析框架、五维评分、可视化。

---

### Skill 驱动：架构无关、可移植

Skill 是可移植的方法，Agent 只是执行引擎。

换模型、换框架，同一套流程照跑。

关键词：架构无关、可移植、HTML 研报。

---

### 研报示例片段

#### 投资结论

核心矛盾是基本面强劲复苏与低利率环境拖累投资端之间的博弈。

在 10 年期国债收益率约 1.72% 的背景下，市场以过度悲观的、低于 3% 的隐含 EV 投资收益率，已经充分甚至超跌反映利空。

结论上，可在 47—50 元区间左侧分批建仓，跌 3% 加仓，仓位 15%—25%，以约 5.2% 股息率为底，目标区间 59—66 元。

整体属于“估值 + 质量修复”的左侧机会，后续重点跟踪板块盈利与质量修复的持续性。

---

### SOTP 分部价值构成

分部估值法，单位：亿元。

-   寿险及健康险：约 57% 权重，估值约 7150 亿，约 0.65x P/EV。
-   财险：约 16% 权重，约 0.9x PB。
-   银行：约 11% 权重，约 0.7x PB。
-   其他板块：部分按市价或市值法估值。

---

### 关键财务指标

| 指标 | FY2025 | FY2024 | FY2023 | FY2022 | FY2021 |
| --- | --: | --: | --: | --: | --: |
| 营业总收入 | 10505 | 10289 | 9138 | 8804 | 11804 |
| 归母净利润 | 1583 | 1467 | 1093 | 1348 | 1218 |
| 扣非净利润 | 1438 | 1174 | 862 | 842 | 1017 |
| EPS | 7.68 | 7.16 | 4.84 | 6.36 | 5.77 |
| ROE | 14.0% | 13.8% | 9.7% | 13.2% | 13.0% |
| 每股净资产 | 55.25 | 50.99 | 49.37 | 46.97 | 44.44 |

![[01_raw/_inbox/文章/images/5c2a956860f4c2dd1b328751e52a256e_MD5.jpg|Image]]![[01_raw/_inbox/文章/images/79652e7a9e4449aefa018ddea82b3742_MD5.jpg|Image]]![[01_raw/_inbox/文章/images/d4c01f1623d2e31fb5de3bc7d06fe390_MD5.jpg|Image]]![[01_raw/_inbox/文章/images/9c53c070c6752ad6d278d711eb60a25f_MD5.jpg|Image]]

大家应该都知道我的Agent股票分析项目，流程是长在某个 agent 上的。  
  
这是"特定 Agent 架构驱动"的方法。  
  
现在换了种干法。  
把分析拆成一个个 skill：数据、估值、预期、业绩、研报，每个就是一个 SKILL.md 加几段脚本和模板。  
agent 只负责按它执行，而不是固定死一个架构。  
  
分析一只股票，可以用自己安装后的skill ，最后吐出带 K 线、估值三角、五维评分的 HTML。  
无论是Claude code、还是 Cursor，只要有这些skill，就能复制我的分析流程。  
  
Anthropic 年十月发 Agent Skills，原始定义就是「装着指令、脚本和资源的文件夹」；两个月后又作为开放标准发布，理由很直白——跨平台可移植。  
  
意思很明白：Skill 是可移植的方法。  
  
研报（图2 3 4）就是使用我收集到的几个skill产出的。  
换 agent 跑，结论也一样，因为方法不在 agent 那边。  
  
所以这个转变，核心是方法从工具里解耦。  
  
以前 agent 是主角，方法是它的附属；  
现在方法沉淀进 Skill 当主角，agent 退成可插拔的执行端。  
  
之后会把自己的使用的skill分享出来（注意，是我收集的，不是我编写的）  
  
\#a股 \#股票 \#股票分析 \#ai \#Agent \#价值投资 \#量化

---

### 评论

-   **A**: \[暗中观察R\]可以分享一下嘛
    -   **B**: 过几天，最近太忙了
    -   **A**: 好的，关注了兄弟\[暗中观察R\]
    -   **B**: 感谢🙏
-   **C**: 大佬求分享\[害羞R\]
    -   **B**: 再等等
-   **D**: 求分享已关注！谢谢！
    -   **B**: 再等等，这两天放假
-   **E**: 什么时候可以分享交流下呢\[笑哭R\]
    -   **B**: 这几天放假
-   **F**: 求分享
    -   **B**: 再等等

---

内容效果不满意？[点此反馈](https://feedback.notebooksyncer.com/feedback/f51c7378-4d0c-4309-b04e-42062fb014be?u=https%3A%2F%2Fwww.xiaohongshu.com%2Fdiscovery%2Fitem%2F6a34f5c5000000001503da33%3Fapp_platform%3Dios%26app_version%3D9.34.4%26share_from_user_hidden%3Dtrue%26xsec_source%3Dapp_share%26type%3Dnormal%26xsec_token%3DCB83kHhlswtAWARboUQV0SZOKZuIauyvOqH7MoO-oydoM%3D%26author_share%3D1%26xhsshare%3DWeixinSession%26shareRedId%3DNzs4RERHO0tLPD1GOjswPEg5Qk06PjpN%26apptime%3D1781989269%26share_id%3D93330a99cab14c57aefdb57aa9e5febc%26code%3D6PgcKNBWZbJ&s=vtoa)