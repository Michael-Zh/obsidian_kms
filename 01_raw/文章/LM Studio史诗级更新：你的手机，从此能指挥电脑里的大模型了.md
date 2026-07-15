---
author: Bubble
source: 微信公众号
url: https://mp.weixin.qq.com/s?__biz=MzkyNjcyNjczMA==&mid=2247494678&idx=1&sn=1326a43b7cb42ee456cc3caa1ee9b6de&chksm=c3b7eb4f115a808fdca5d9b0a3df66bcf86acb77823e6f28e10d69d6ad37cc0d8af4d34f2d3d&mpshare=1&scene=1&srcid=0608A3NToDoiWrj5NrCTzoLR&sharer_shareinfo=2e366e71f2144e4778ad26cbeb593186&sharer_shareinfo_first=2e366e71f2144e4778ad26cbeb593186#rd
saved: 2026-06-08 08:34:41
tags:
  - 笔记同步助手
annotation: useful guide to setup local LLM
id: a16f5027-1d73-42fc-bc6d-72eda4cd9c7d
summary: LM Studio update enabling phone-to-desktop control of locally running large language models, addressing the mobile/desktop integration gap for local AI workflows.
processed: 2026-06-12
---

公众号名称：BubbleBrain

作者名称：Bubble

发布时间：2026-06-08 08:46

> Hello，大家好！
> 每次新模型发布，把老模型下架的时候，都会在小红书还有X上看到有不少朋友说新模型没有自己调教过的原来模型的那种**有人味**的感觉了。
> 无论是DeepSeek 还是之前OpenAI闹的全网轰轰烈烈的**Keep 4o**，都有人在吐槽模型的人味随着代码能力的更新升级越来越回去了。。
> ![[01_raw/_inbox/文章/images/64109dcb74120277dfa117c8e900049c_MD5.png]]
> 那其实这种时候真的没什么万全之策，
> 因为模型毕竟不是我们自己的，而且从现在的更新方向来看，很难说新模型真的就比旧模型强，因为体验这个东西真的是很主观，特别这是一些没法量化的东西。
> 但，也不是完全解法。
> Section 01什么是本地部署？
> **本地部署的优势这个时候就显示出来了**。
> 可能有小伙伴不太懂这个本地部署和我们平时在网页上用DeepSeek、千问、豆包或者调用它们的API的差别，我来先简单解释一下。
> 我们讲的本地部署其实一般分为两种。
> **一种是在自己的GPU机器上部署开源的模型，比如DeepSeek或者千问，这种是一般企业里会有的需求。**
> 因为企业里有很多比较敏感的数据，调用API 或者在网页上使用，就等于是把数据给送到对方手里了。
> 但是，这种算力的价格通常来说都是非常高的。
> **还有一种是部署在自己的个人电脑，甚至是手机。也就是常说的端侧部署。**
> 端侧部署在价格上会便宜很多，那当然能部署用的模型一般都是一些小尺寸的模型，大点的模型通常都不太行。
> 虽然尺寸小，但是日常拿来聊天，翻译，做点简单的任务肯定是没问题的了。
> Section 02如何部署
> 正好，前两天看到我最常用的端侧部署的软件LM Studio 有一波重大的更新：
> ![[01_raw/_inbox/文章/images/c72ae553b3e403647fa226f6ff489560_MD5.png]]
> **你现在可以用手机调用你部署在本地电脑的模型了。**
> OK，那我们一步步看是怎么做的吧。
> 我们先要去LM Studio 官网下载好它的软件。
> ![[01_raw/_inbox/文章/images/fff23dbcbba7eaf4bd6026c677ea369e_MD5.png]]
> 选择对应自己电脑系统的版本。
> 安装好之后，我们直接打开，然后找到下面这个地方。
> ![[01_raw/_inbox/文章/images/f805318b2f28860f336c3d9dca793ac4_MD5.png]]
> 就可以看到一系列的本地可部署的模型。
> 如果你不知道自己的电脑适合部署什么样的模型其实也没关系。LM Studio 针对每个模型都会去看是否匹配你的设备。
> ![[01_raw/_inbox/文章/images/fc0f15f7040d685f30385cc574eb39c2_MD5.png]]
> 如果选的模型不合适的话，它会显示对于此设备可能过大的提示。
> 因为最近Google 刚发了新模型 Gemma 4 12B Unified，是一个多模态模型。
> 所以这里，我们先来下载这个模型尝尝鲜。
> ![[01_raw/_inbox/文章/images/a461b36c21758f6f46ce4a3e1224e7b6_MD5.png]]
> Q4 量化版本只有7.56个G，基本上是对端侧设备最友好的模型了。
> 下载完成之后，加载模型。
> ![[01_raw/_inbox/文章/images/e975f9582333e5a515e93bf709c2ebc3_MD5.png]]
> 然后可以看到如果只开到4096的上下文，对内存的消耗其实是非常小的，128G的内存，只消耗了6.94GB。
> ![[01_raw/_inbox/文章/images/b833ea74f1790c048cfff3097c373980_MD5.png]]
> 测试一下，能够正常对话输出就没什么问题了，可以正常对话使用。
> 现在可以试试关掉网络，看看是不是还能够正常对话了。
> 本地部署的一大好处就是，你和模型所有的聊天对话都属于你自己，不会被模型公司所拥有。
> Section 03如何在手机上运用
> 那有的小伙伴可能除了想要在电脑上用之外，还想要能在手机上使用端侧的模型。
> 其实也是可以的。
> 手机上有个APP，叫**Locally AI**。
> ![[01_raw/_inbox/文章/images/2b486d10ca182b6171e955788d26f8a7_MD5.jpg]]
> **它可以下载端侧模型直接使用手机上的算力来使用，也可以配置连接到电脑上的LM Studio，使用电脑的算力来使用。**
> 我们一个个来说。
> 先看如何直接下载模型到手机上，用手机上的算力来使用。
> ![[01_raw/_inbox/文章/images/3c13e56efeacb4a66368840342a7ae5c_MD5.png]]
> 按照图上的这三步之后，我们就能看到一堆比较合适的模型了，选择自己任意喜欢的模型下载就可以。
> **这里要注意的是，模型的输出速度，响应时间取决于手机设备，设备越好，那模型的输出表现也会越好。**
> 我这里下载的还是Google 的Gemma 4 模型以及Qwen 3.5 的2B 参数的模型。
> 下载好它们之后，就可以直接对话了。
> ![[01_raw/_inbox/文章/images/7d6111282e5e3d7de77d15606b60ebfd_MD5.png]]
> 实测这两个模型在我的iPhone 17 ProMax 上日常交流、写点简单代码都没什么问题，而且响应速度还挺快的。
> Section 04LM Studio 的新功能
> 终于要讲到LM Studio 新推出的功能，
> **可以用Locally AI 搭配LM Studio ，使用你部署在个人电脑上的模型了。**
> 其实配置本身不难。
> ![[01_raw/_inbox/文章/images/0c627219748179392e629919d45d0ebe_MD5.png]]
> 我们点开LM Studio 的设置页面，然后注册一个账号登录，
> ![[01_raw/_inbox/文章/images/0d3e53b073600b06ec762f223d29e8e6_MD5.png]]
> 确保设置里的LM Link是开启的，这样等会儿可以识别到我们的设备。
> 然后我们需要到Locally AI 中的设置中去登录刚刚在LM Studio 中注册的账号，然后把LM Link 同样开启，这样才能同步发现可使用的设备。
> ![[01_raw/_inbox/文章/images/e044789c524564be943fdc6ec363b9c9_MD5.jpg]]
> 这里要稍微等待一会儿才会出现你的设备。
> 显示出你要连接的设备之后配置上了之后，就可以调用部署在它上面的模型了。
> ![[01_raw/_inbox/文章/images/28efe783cbf1ab0316fcd167c1568433_MD5.jpg]]
> 回到Locally AI的主对话界面，点击上方的模型选择的地方，如果看到你在电脑上下载的模型，就说明配置成功了。
> 这样你就可以直接依赖电脑上的模型，来进行对话了。
> Section 05最后写点
> 坦白讲，端侧模型的能力现在肯定是还跟不上我们日常主力使用的那些大模型的。
> 但我觉得这并不代表它没有使用场景。
> 真正重要的或许在于选择权本身。
> 当所有对话都发生在别人的服务器上，我们其实只是在租借一段随时可能被收回的关系。模型说下架就下架，风格说调整就调整，你花了大半年磨合出来的那个熟悉的语气，可能某天更新之后就再也找不回来了。
> > **端侧部署提供的是一种朴素的确定性。**
> 你的数据留在你的设备里，你的偏好不会被上传到某个训练管道里去被平均化掉，你也不用担心哪天醒来发现常用的模型已经不在了。
> 对于那些花了很多时间调教出特定风格的用户来说，这几乎算是一种必须的兜底方案。
> 哪怕平时用不上，知道它一直在那里，本身就是一种安心。
> 在这个一切都拼命涌向云端的智能时代，这种可以触摸的自主感，反而越来越稀缺，也越来越值得我们认真对待。
> 模型会一代代更新，也会一个个下架，
> 但留在你自己机器里的那一个，永远都听你的。
> 以上，
> End Note
> **若觉得内容有帮助，欢迎点赞、推荐、关注。别错过更新，给公众号加个星标⭐️吧！**
> 祝您在2026年里天天开心，快乐，身体健康，万事如意！期待与您的再次相遇～

  

---

内容效果不满意？[点此反馈](https://feedback.notebooksyncer.com/feedback/c7bf893e_1780900480087?u=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzkyNjcyNjczMA%3D%3D%26mid%3D2247494678%26idx%3D1%26sn%3D1326a43b7cb42ee456cc3caa1ee9b6de%26chksm%3Dc3b7eb4f115a808fdca5d9b0a3df66bcf86acb77823e6f28e10d69d6ad37cc0d8af4d34f2d3d%26mpshare%3D1%26scene%3D1%26srcid%3D0608A3NToDoiWrj5NrCTzoLR%26sharer_shareinfo%3D2e366e71f2144e4778ad26cbeb593186%26sharer_shareinfo_first%3D2e366e71f2144e4778ad26cbeb593186%23rd&s=obsidian)