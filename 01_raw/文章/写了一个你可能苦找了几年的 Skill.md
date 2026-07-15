---
author: 上班摸鱼
source: 小红书
url: https://www.xiaohongshu.com/discovery/item/69a23c19000000001d013d28?app_platform=ios&app_version=9.31.2&share_from_user_hidden=true&xsec_source=app_share&type=normal&xsec_token=CB0kPCA7NoISwbxpUImSA7Gn_senEqBNVNglkQoxIbc4Y=&author_share=1&xhsshare=WeixinSession&shareRedId=Nzs4RERHO0tLPD1GOjswPEg5Qk06PjpN&apptime=1779657714&share_id=daf9731c943346058c1089e9593c9bca&code=7AWhVWvu4PM
saved: 2026-05-24 23:22:29
tags:
  - 笔记同步助手
id: a76d683f-b7a2-4d0d-9dfa-cde38cfa9c72
annotation: good idea to do video and social media competative and content analysis
summary: An AI skill for video shot analysis that automatically segments video into individual shots, scores each by composition, impact, and memorability using Hollywood editor Walter Murch's principles, and outputs a tiered report (keep/usable/discard) with high-scoring shots exported to a folder.
processed: 2026-06-06
---

作者: 上班摸鱼

发布/编辑时间: 2026年05月24日 05:04

2026.5.22 更新：主页置顶了新版，有更高要求的可以使用新版，旧版不再作功能更新；当前页面最下方有Redskill下载入口  
  
上一个工具是拆文案的，这个是挑镜头的  
  
做这个东西的起因很简单：我经常需要从别人的视频里找可以学习的镜头。比如看到一个拍得好的短片，想拆解一下哪几个镜头是真正撑起整个片子的，光靠肉眼一帧帧翻太慢了，尤其是素材量大的时候根本看不过来，也记不过来  
  
所以就想让 AI 帮我干这件事——把视频自动切成一个个镜头，逐个去「看」画面，按构图、冲击力、记忆度这些维度打分，然后把高分镜头单独导出来  
  
打分的逻辑来自好莱坞剪辑师 Walter Murch 那套东西——情感比技术重要，记得住的比单纯好看的更值钱。AI 会根据镜头类型自动调权重，不是一刀切（但其实也还有一点局限性，建议片子自己先看一遍）  
  
最后分三档：必须留的、能用的、建议扔的。高分镜头自动导出到一个文件夹，不用自己翻  
  
哪些场景用得上：  
  
做混剪的时候，手上几十个视频、几百个镜头，靠这个先筛一遍，效率差很多。之前花一下午干的事情现在半小时搞定  
  
学拍摄的话也挺好用。拿别人拍得好的片子让 AI 拆解，每个镜头的评分理由都会告诉你为什么这个构图好、为什么那个画面有冲击力，算是一种反向学习  
  
做竞品分析也能用。比如想知道竞争对手的广告片里哪几个镜头是核心记忆点，丢进去跑一遍就行  
  
拿了一个B站的AI短片测试，68个镜头里筛出来13个，每个都有评分理由和剪辑建议，最后面的三张截图能看到效果（这里是用了skill做的图，但格式是报告输出格式）  
  
B站、YouTube、抖音、小红书的视频都支持。需要在 IDE/Openclaw 里用，Gemini 3.0 效果最好，Kimi K2.5 也行。注意必须是能看图的模型，纯文本LLM 的不行  
\#Claude \#Skill \#Openclaw \#Antigravity \#时间管理 \#精力管理 \#摸鱼 \#REDSkill

  

![[01_raw/_inbox/文章/images/cdf854c75058dc7d04e019d594cf1018_MD5.jpg|Image]]![[01_raw/_inbox/文章/images/645edb6515e3266531ca5e57ffde9510_MD5.jpg|Image]]![[01_raw/_inbox/文章/images/3e29010fa8513e9c721d4edb15346bb4_MD5.jpg|Image]]![[01_raw/_inbox/文章/images/3425044df4f19d5be5ad0e85efd235d6_MD5.jpg|Image]]![[01_raw/_inbox/文章/images/eb5caac3f651b7958188cc4728e88f79_MD5.jpg|Image]]![[01_raw/_inbox/文章/images/168c9aacb6259fb7665d7916e7136a4c_MD5.jpg|Image]]

---

### 评论

-   **A**: 如果是画面理解的话 应该挺消耗 token 的
    -   **B**: 所以建议 coding plan，并且非常推荐 kimi\[doge\]
    -   **C**: 装Kimi里面吗
    -   **B**: kimi 的 coding plan
-   **D**: 我来试试实力\[doge\]
    -   **B**: \[doge\]直接去用新版试试
    -   **D**: 下午开完会就用\[doge\]
    -   **D**: 下午开完会就用\[doge\]
-   **E**: 问一个基础问题，只要把视频网站的视频文件先扒下来，然后在本地分析还是直接在线分析？\[微笑R\]另外，怎么设置视频网站的api，扒视频不会被block么？
    -   **B**: \[微笑R\]你需要有 IDE/openclaw 里面配置了带有多模态能力的模型，本地完成素材的切分，把图像传到云分析，云回传结果报告。不同网站方式不太一样，你都在你的默认浏览器登录过的话基本都行
    -   **F**: \[石化R\]听着有点费token的样子
    -   **B**: 包费的\[doge\]不是 coding plan 或者必要项目不要用
-   **G**: 可以增加模型吗？千问3.5plus
    -   **B**: 安装 skill 之后让你的 agent 帮你改就行\[doge\]
    -   **G**: 大概操作指令可以分享吗 已安装 非常感谢 中国大好人！
    -   **G**: 好人一生融化富贵
-   **H**: 这应该很吃硬件
    -   **B**: \[doge\]mac mini16g 都能跑
    -   **H**: 你要看skill的量 与复杂程度
    -   **B**: \[doge\]…我自己做的我能不知道

---

内容效果不满意？[点此反馈](https://feedback.notebooksyncer.com/feedback/ce27f5a8_1779657746878?u=https%3A%2F%2Fwww.xiaohongshu.com%2Fdiscovery%2Fitem%2F69a23c19000000001d013d28%3Fapp_platform%3Dios%26app_version%3D9.31.2%26share_from_user_hidden%3Dtrue%26xsec_source%3Dapp_share%26type%3Dnormal%26xsec_token%3DCB0kPCA7NoISwbxpUImSA7Gn_senEqBNVNglkQoxIbc4Y%3D%26author_share%3D1%26xhsshare%3DWeixinSession%26shareRedId%3DNzs4RERHO0tLPD1GOjswPEg5Qk06PjpN%26apptime%3D1779657714%26share_id%3Ddaf9731c943346058c1089e9593c9bca%26code%3D7AWhVWvu4PM&s=obsidian)