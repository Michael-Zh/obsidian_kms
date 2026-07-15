---
author: AI产品普洱
source: 微信公众号
url: https://mp.weixin.qq.com/s?__biz=MzkyODkyNjM5Nw==&mid=2247485260&idx=1&sn=d9a8cd0bbeedc1aea10cc5ca222aab9b&chksm=c3ba429894734579e1e627d4a4a89625f79782f336af424b05b14f3a3de2f8c7291c9a510094&mpshare=1&scene=24&srcid=0526QJWl4BOjMeAMHKq8fAL4&sharer_shareinfo=1545d333d9a48c5b0404fb6f3e9eb76c&sharer_shareinfo_first=1545d333d9a48c5b0404fb6f3e9eb76c#rd
saved: 2026-05-29 13:22:13
tags:
  - 笔记同步助手
id: 65d769d7-8394-4c04-808e-87fe012b07f2
annotation: Reference only - tips to gain access to Gemini
summary: Step-by-step guide to obtaining Gemini Pro at 38.88 CNY/year via a third-party card activation service, including security preparation (enabling two-factor auth with backup codes, clearing payment profiles, using a temporary password) and post-activation cleanup to remove the vendor's device from the account.
processed: 2026-06-06
---

公众号名称：AI产品普洱

作者名称：AI产品普洱

发布时间：2026-05-24 10:23

去年带大家靠学生优惠白嫖了一年的 Gemini Pro，前几天发邮件提醒我快到期了。

今天呢，又给大家找到了新的优惠路子（这几天 Gemini 发布的 3.5 flash 做前端效果还不错，对于实时输出的场景，可以尝试使用一下，快到起飞。）

这篇就把我亲测的整套流程写清楚，从准备账号到充值成功再到安全收尾，全程配图，新手照着抄就行。

**整个流程的关键不是充值本身，而是账号的准备工作**，准备好了基本是傻瓜式，没准备好就容易踩风控。

第一步是给账号开**两步验证和备用验证码**，这一步非常关键，因为后面充值要用到。

直接访问[https://myaccount.google.com/security](https://myaccount.google.com/security) 这个地址，进去之后在登录选项里找到两步验证。

![[01_raw/_inbox/文章/images/86c9a3feff070ed5cfd803cc17b15de6_MD5.png]]

进入安全页面打开两步验证

点进去之后，在第二个验证步骤里，能看到一个备用验证码的入口，没开过的话这里会显示获取备用验证码。

![[01_raw/_inbox/文章/images/43da1478090f3e1307910467af1ab3e2_MD5.png]]

点击备用验证码

点进去之后系统会一次性生成10 个备用验证码，**这些码后面充值的时候要填一个进去**，建议先截图保存好。

![[01_raw/_inbox/文章/images/9d604d88a42073ea43a131005842b50e_MD5.png]]

创建备用验证码

第二步是处理支付资料，**这一步是为了避开 Google 的风控**，毕竟咱们这种非常规渠道充值，账号上挂着支付方式更容易触发异常。

访问[https://payments.google.com/gp/w/home/settings](https://payments.google.com/gp/w/home/settings) 这个支付资料的地址。

如果你之前**从来没绑过支付方式**，进去会看到这个空的添加支付方式页面，那你就走运了，直接跳过这一步去下一步。

![[01_raw/_inbox/文章/images/fef08f95aa38ba4ebcf18b1582fce350_MD5.png]]

没有添加过支付的直接跳过

如果之前绑过支付方式，需要往下翻到**支付资料状态**那一栏，能看到一个关闭支付资料的红色入口，点击它。

![[01_raw/_inbox/文章/images/54e37ffb538d954e43c4c9aaf5dc2f2e_MD5.png]]

有添加过付款的点击关闭支付资料

点了之后系统会弹一个确认框，让你选关闭的理由，**随便选一个就行**，比如那个我刚刚发现自己有付款资料但并不需要它，选好之后右下角点关闭支付资料。

![[01_raw/_inbox/文章/images/c6cd594b1fa14d071eaaf7da44478ec9_MD5.png]]

有添加过的随便选一个理由后点击关闭支付资料

关掉之后再回到那个支付资料地址，**已经变成空白页面了**，这就说明账号干净了，可以进入下一步。

![[01_raw/_inbox/文章/images/fef08f95aa38ba4ebcf18b1582fce350_MD5.png]]

再进去已经是没有支付了

还有一个细节我得提一下，**强烈建议你在充值之前先把 Google 密码改一下**，等充值完成再改回来或者改成新的。

原因很简单，**你后面要把邮箱密码填到第三方网站上**，出于安全考虑还是临时密码最稳妥。

忘了密码或者想改密码的去 [https://myaccount.google.com/signinoptions/password](https://myaccount.google.com/signinoptions/password) 这个地址改就行。

准备工作做完，接下来就是**购买卡密这一步**了。

打开 [https://ainana.xyz/products/geminiyear](https://ainana.xyz/products/geminiyear) 这个地址，**38.88 CNY 一年**，这个价格对比官方是真的香（真香.jpg）。

页面填两个东西，一个是邮箱用来收订单信息和后续查订单，一个是订单密码自己设一个简单的就行比如 123 这种。

![[01_raw/_inbox/文章/images/d427d9ca4e74b99cc0e73320403deb2f_MD5.png]]

购买卡密

支付方式选支付宝，直接付款就行。付完之后页面会跳到订单详情，**在子订单交付那一块能看到一串卡密**，把这串卡密复制下来。

![[01_raw/_inbox/文章/images/7597408e1cc1609eecb55746afcdc73a_MD5.png]]

打开充值网站填写卡密等信息

然后**点开订单页面上提示的充值地址**，会跳到一个 Pixel 订阅的激活页面。

激活页面要填四样东西，**卡密、Google 邮箱账号、Google 邮箱密码、还有一个备用验证码**。

备用验证码就是刚才咱们生成的那 10 个里随便挑一个填进去，**记住一个码只能用一次**。

![[01_raw/_inbox/文章/images/c4969213555476d0e7876e4dc1fc9ce7_MD5.png]]

到激活页面填写信息

填完点提交，你可以拿着卡密去查询订单状态，**这一步是看充值有没有处理成功**。

![[01_raw/_inbox/文章/images/3d2621f69f255742cbb55700c8b422b3_MD5.png]]

提交后用卡密查询状态

把卡密粘贴进去点查询，能看到任务列表里状态显示**处理中**，说明系统已经接到单子在跑了。

![[01_raw/_inbox/文章/images/b4b5d22472b73752cc47c6304e0e1e27_MD5.png]]

可以查询到正在处理中

**人不多的时候大概三分钟就好了**，我那天充的时候碰到高峰，等了大概三分钟左右，状态就变成已完成订阅成功了。

![[01_raw/_inbox/文章/images/a3018c4a34777ba83a355dcfac66d8f0_MD5.png]]

三分钟时间就充值好了

这时候打开你的 Google 账号头像，**能看到外面套了一圈红橙黄绿蓝的彩色边框**，这是 Gemini Pro 用户的专属标识，看着还挺有面子的（咱北京的孩子）。

![[01_raw/_inbox/文章/images/af5558fb1150271d0e2f76ee66a84f3a_MD5.png]]

拿下尊贵的红橙绿蓝框

充上之后**还有最后一步非常重要的安全收尾**，千万别图省事跳过。

去你的 Google 账号设备管理页面，**会看到一个陌生的设备登录记录**，一般是 Google Pixel 10 Pro 或者类似的 Android 设备，这是充值服务商的设备。

![[01_raw/_inbox/文章/images/7b9fc07087a68ac20e2fb1b5621e4fa5_MD5.png]]

充值成功后移除充值设备

点进那个设备，直接点退出账号，把那个设备从你的账号里踢出去。

![[01_raw/_inbox/文章/images/d2986ff4ff714fe3ac41337eceb8be9b_MD5.png]]

点击退出账号

然后回头**再去把 Google 密码改一下**，这样就算服务商记录了你的临时密码也用不了了。

至于备用验证码，**用掉一个还剩九个**，剩下的留着自己以后用都行，也不用专门去处理。

![[01_raw/_inbox/文章/images/9e718a43ba2ecb1f53f484b27f8eef97_MD5.png]]

剩下9个备用验证码

到这里整个流程就走完了，**总结一下我的体验**。

价格上 **38.88 一年**真的太香了，相比官方一年小两千的价格，便宜了几十倍，性价比直接拉满。

操作上整个流程加起来不到十分钟，**真正的充值环节只要三分钟**。

风险上**只要按流程做好支付资料关闭和事后改密码这两步**，账号基本不会触发风控，我这个号是去年学生优惠用到现在的，老号没出任何问题。

唯一需要注意的就是**新注册的号别用这个渠道**，激活页面里也写了新号风控特别严，容易封号，建议用养了一段时间的老号。

如果你的 Gemini 也快到期了或者本身就想升级 Pro，**这个渠道我亲测可以放心闭眼冲**。

最后多嘴一句，**这种第三方渠道随时可能涨价或者下架**，看到合适的价格就该出手了，别老犹豫。

如果你也试了试这个流程，欢迎在评论区聊聊你的充值体验，碰到问题也可以留言，我看到都会回。

写到这里突然想给大家整个小福利，**这次直接抽 3 个 Gemini Pro 年卡充值卡密送出去**，到手就是一年的 Pro 会员，自己冲或者送朋友都行。

参与方式特别简单，**给这篇文章点个赞，然后在评论区聊一句你想用 Gemini 干嘛**，凑齐这两步就算参与成功了。

开奖时间定在 **三天后**也就是 2026 年 5 月 27 号，我会从评论区随机抽 3 位，中奖名单直接置顶在评论里，到时候会点赞你的评论，记得联系我喔。

我是 AI 产品普洱，一名 00 后的 AI 产品经理，咱们下期见。

宝藏主包下方点击 **狠狠关注** 👇👇👇

每周深挖一个 AI 工具/技术，帮你省时间、省钱、少踩坑。  
🔹 关注公众号：第一时间获取干货（记得设星标 ⭐）

![[01_raw/_inbox/文章/images/f68ba494100bace6f17d910a1054ba37_MD5.png]]

  

---

![[01_raw/_inbox/文章/images/8b83d7b016d75372aae69be9c7db5185_MD5.jpg|cover_image]]

原创 AI产品普洱 AI产品普洱

---

内容效果不满意？[点此反馈](https://feedback.notebooksyncer.com/feedback/6bb04869_1780053731750?u=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzkyODkyNjM5Nw%3D%3D%26mid%3D2247485260%26idx%3D1%26sn%3Dd9a8cd0bbeedc1aea10cc5ca222aab9b%26chksm%3Dc3ba429894734579e1e627d4a4a89625f79782f336af424b05b14f3a3de2f8c7291c9a510094%26mpshare%3D1%26scene%3D24%26srcid%3D0526QJWl4BOjMeAMHKq8fAL4%26sharer_shareinfo%3D1545d333d9a48c5b0404fb6f3e9eb76c%26sharer_shareinfo_first%3D1545d333d9a48c5b0404fb6f3e9eb76c%23rd&s=obsidian)