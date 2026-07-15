---
author: Simonlin
source: 微信公众号
url: https://mp.weixin.qq.com/s?__biz=MzU1MDk3MzEwOA==&mid=2247488148&idx=1&sn=0c777d7160cb94c5179e36191e64ef7c&chksm=fa5f22f320be1791edaa59fe8ad05666aab8d1e64737bc08f040224fea10314117aa79378471&mpshare=1&scene=1&srcid=0521KCosNeHFr6vfhyoznS5O&sharer_shareinfo=0aab8b6e7c08f2612dc49a28c63daa20&sharer_shareinfo_first=c12c34b848c5cbddde20ec69a003d0a4#rd
saved: 2026-05-29 00:02:41
tags:
  - 笔记同步助手
id: 9af717ef-626d-44f2-b2d8-c67773f4c6a1
annotation: Karpathy wiki LLM
summary: "Step-by-step guide to building an Obsidian knowledge base using Karpathy's 3-layer LLM Wiki framework: install Obsidian, create a 4-folder structure (Inbox/Wiki/Areas/Projects), leverage direct Markdown file access for AI integration, and use four content input methods. Warns against over-complex taxonomy, perfectionism, and storing without ever querying."
processed: 2026-06-06
---

公众号名称：Simonlin的精神世界

作者名称：Simonlin

发布时间：2026-05-07 18:37

Hello啊朋友们，我是Simonlin，用通俗易懂的语言，手把手带你玩转AI，提升10倍效率！

你知道那种感觉吗？

三个月前你看到一篇特别好的文章，你把它存进了某个地方——也许是微信收藏，也许是备忘录，也许是桌面上的一个文件夹。

三个月后，你想找它。

你想不起来它叫什么名字，想不起来存在哪个平台，甚至想不起来它是不是还存在。然后你就放弃了。

这就是我三年前的状态。那时候我的"知识管理"就是一堆微信收藏夹和备忘录，每天接收大量信息，但真正能调用出来的几乎没有。

后来我遇到了Obsidian。再后来，我遇到了Karpathy。

今天这篇文章，就是把这两件事结合起来：怎么用Obsidian从零搭建一个真正能用的知识库，怎么让AI帮你维护这个知识库。

  

## 一、什么是知识库

  

很多人听到"知识库"三个字就觉得很复杂，其实说白了就是两件事：你把东西存进去，AI能帮你找出来。

就这么简单。

你每天看文章、读资讯、刷视频、听播客——这些信息进来的时候是散的，存在脑子里很快就忘了，存在微信里就再也找不着。但如果你有一个系统专门接收这些内容，并且AI能读懂、能调用，那这些信息才真正变成了你的资源。

这就是"第二大脑"的意思：不是说你有第二个脑子，而是说你的知识不再是散落在各处的碎片，而是有一个集中管理的地方，AI能访问、能整理、能帮你执行任务。

Karpathy管这个叫"LLM as OS"——AI是你数字生活的操作系统，知识库就是这个系统的硬盘。

  

## 二、为什么是Obsidian

  

市面上知识库工具很多，Notion、飞书、印象笔记、Logseq，各有优劣。我选Obsidian，理由就三条。

第一，它是本地的。存在你自己电脑上的文件夹里，不依赖任何平台。你今天用Notion，明天Notion收费了，你就得迁移。但Obsidian存的就是纯文本markdown文件，哪天你不想用了，直接打开文件夹就能看到所有内容，没有任何绑定。

第二，它免费。核心功能完全免费。付费功能是一些高级插件，但对大多数人来说，免费功能已经足够用了。

第三，它和AI天然兼容。Obsidian存的是markdown——一种纯文本格式。AI工具读markdown完全没有障碍。你不需要做格式转换，不需要导出导入，Obsidian写完的东西，AI直接就能读。

  

## 三、从下载到建好文件夹

  

这是整篇文章最简单的一步。打开浏览器，访问 obsidian.md，点击"Download"。它会自动识别你的操作系统——Mac会显示"Download for MacOS"，Windows会显示"Download for Windows"。点一下，下载，安装，和装任何软件一样。

![[01_raw/_inbox/文章/images/98bed8bc493df2307ec8c1f3895ab636_MD5.png]]

装完之后打开，你会先进入一个初始化的界面，是为了让你先选择你要存放东西的“保险库”（Vault）。如果你看到的界面是英文，别忘了点一下最下方的列表，展开来，选择“简体中文”。

![[01_raw/_inbox/文章/images/0c3c0167d12edf48a3350bb76fad3f30_MD5.png]]

然后，你需要创建一个"保险库"（Vault）。保险库就是你的知识库文件夹，你在哪里存放markdown文件，哪里就是你的保险库。

![[01_raw/_inbox/文章/images/6e9d8b451b669c10c92e05f8449fdb8a_MD5.png]]

你需要给仓库起一个名称，随便起，叫“知识库”啥的，都可以，只要你自己记得住。仓库的位置，需要你在文件管理器里挑选一个文件夹，用来存放。

为了方便，你可以像我一样，直接选择桌面或者Doucments（文档）文件夹。

![[01_raw/_inbox/文章/images/3e809e019c03a41723510c7958fa3853_MD5.png]]

然后，点一下“创建”，就搞定了。

创建好了一个仓库，接下来的所有操作，都基于仓库内的文件进行，包括新增文件夹，也只是在这个仓库底下创建了个文件夹而已。

![[01_raw/_inbox/文章/images/3a914b951fcc9e218dee7e1b382ce8ea_MD5.png]]

刚建好知识库的时候，左边的文件夹列表是空的。很多人就卡在这里：文件夹怎么建？东西怎么放？

我的建议是：先建最基本的四层结构，不要一上来就搞复杂的分类体系。

```
00-Inbox/ —— 每天随手记的东西，看到什么随手存进去
```

```
01-Wiki/ —— 整理好的主题卡片，按知识点组织
```

```
02-Areas/ —— 按领域分类的资源，比如"AI工具"、"学习方法"
```

```
03-Projects/ —— 正在做的具体项目，相关内容都放这里
```

为什么要用"00-""01-"这种编号？因为Obsidian默认按字母顺序排列文件，加上数字编号能让文件夹按你想要的顺序排。

  

## 四、AI怎么读你的Obsidian

  

这件事说出来特别反直觉——你装了一个笔记软件，然后要让AI能读它，结果发现：不需要装任何插件。

Obsidian存的是什么？markdown文件，就是纯文本。只要AI工具能访问你电脑上的文件夹，它就能读Obsidian里的所有内容。

第一步，找到知识库的路径。在你的Obsidian界面，随便点一个文件夹，右键选择"在 Finder 中显示"（Mac）或者"在系统资源管理器中显示"（Windows）。文件夹在磁盘上的路径就出来了。Mac上大概是：/Users/你的用户名/Documents/MyKnowledgeBase/。

Windows的话，在文件管理器中，右键单击文件夹，然后选择“属性”，里边有一个“位置”，在它右边就是你知识库的路径了。

![[01_raw/_inbox/文章/images/4f3035315d56a2f69b3c08af0bc08d44_MD5.png]]

![[01_raw/_inbox/文章/images/9dc80481fd32e923cb39c8f19d19acca_MD5.png]]

直接把这个路径记住，存进AI助手的记忆里。

第二步，把路径告诉AI。在你和AI助手开始对话的时候，告诉它"我的知识库在/Users/你的用户名/Documents/MyKnowledgeBase/，里面是markdown格式的笔记"，然后把四层结构告诉它。

就这样，AI能读你Obsidian里的所有内容了。没有任何插件，没有任何配置，没有任何技术门槛。AI读你电脑上的文件夹，和你打开文件夹看到的内容完全一样。

这才是Obsidian最大的优势：它不是一个封闭的App，而是一个开放的文件系统，AI天然能读它。

  

## 五、四种往里存的方式

  

说完了AI怎么读，再说你怎么往里存。这里有四种方式，各有各的用处。

第一种，Obsidian Web Clipper。

它是一个浏览器插件，装好之后，你在任何网页上点一下，就能把整个页面存成markdown格式，扔进你的Obsidian知识库。整个过程五秒钟。

第一步，去插件商店安装。Chrome、Safari、Firefox、Edge都能装，直接在浏览器的扩展商店里搜"Obsidian Web Clipper"，找到官方出品那个，点安装。

![[01_raw/_inbox/文章/images/37fc55200ce2c4eaa27e5bff4bd4c17f_MD5.png]]

第二步，在需要剪藏的页面，直接点开Obsidian Web Clipper，“添加到Obsidian”。这个时候，它就会先打开你的Obsidian，然后把内容放到你的知识库里面。

![[01_raw/_inbox/文章/images/06a5108aa28bb7e103a9779f13f9ead8_MD5.png]]

第二种，直接让AI帮你写进去。

这是最省力的方式，也是目前我用的最爽的方式，非常适用于已经在IM平台里连接了本地Agent的用户，比如说养虾的，养马的，或者是Cola、Alice这些本地的Agent助手。

能举的例子太多了。你让龙虾帮你整理了一份会议记录，你说一句"存知识库"，它直接把记录写成markdown文件，写进你Obsidian知识库的对应文件夹里。你打开Obsidian，记录已经在那里了。

你让Cola帮你写了份学习笔记，你把书里的核心观点发给它，它整理完之后你说"存知识库"，于是，写进对应的主题卡片里。整个过程：你只说了一句话，AI帮你完成了创建文件、写入内容、归类存放全部动作。

![[01_raw/_inbox/文章/images/1acfa8ebbaeda500b52eb76062e926df_MD5.png]]

第三种，手动复制粘贴。最简单粗暴的方式，适合临时看到一段话想存进去的场景。

第四种，X收藏工具。这个跟前三种都不太一样——Clipper剪不了X上的动态内容（推文、回复流），Web Clipper是"剪藏整篇文章"，但X上的内容是实时动态的，你总不能为了存一条推文去装Clipper。

我做了一个Chrome扩展，叫xcolab。装好之后，在X上刷到有用的内容，点一下扩展图标，扫描一下，再点一下“发送”，内容就进了你的知识库。整个过程不到一分钟。

![[01_raw/_inbox/文章/images/407600f6353be553d443e073b45333d6_MD5.png]]

核心解决的是：你在X上刷到一条AI工具的使用经验、一个好用的提示词、一篇干货分享——这些东西以前没法进你的知识库，现在可以了。

GitHub开源地址：https://github.com/simonlin000/xcolab，完全免费，Mac和Windows都能用。

这个虽然不是很完美，但是我还会持续迭代。

这四种方式配合起来，Obsidian就是你的知识进出中枢。

  

## 六、Karpathy的三层架构

  

到这里，我们实际用的是Karpathy（Andrej Karpathy，OpenAI早期核心成员）的LLM Wiki方案，他在Twitter上分享过，核心就是三层。

第一层是Raw层，也就是原始资料层。网页、文章、随手笔记——所有原始内容都先扔进Raw层。用Clipper一键保存，不用整理，不用分类，先存进去再说。这一层的作用是接收，你看到什么，第一时间收进来，不丢失。

第二层是Wiki层，也就是整理层。AI读取Raw层的内容，自动生成整理好的笔记页面、加标签、加双链、整理目录。这一层的作用是组织，原始资料杂乱无章，Wiki层让它们变得可检索、可关联。

第三层是查询层，也就是执行层。你向AI提问，AI从Wiki层找答案，直接生成文件输出——可以是新的笔记、可以是摘要、可以是方案。这一层的作用是调用，知识只有被用起来才有价值。

三层加在一起，就是：存进去→AI整理好→需要时调出来。

一个具体的场景是这样的。你用Clipper存了一篇AI工具的文章进Raw层。AI读到之后，自动在Wiki层生成一张主题卡片，标注"这篇文章讲了三个AI工作流技巧"。三个月后你想找这方面的内容，你问AI："我在学AI工作流，之前存过相关资料吗？"AI翻你的Wiki层，找到那篇文章，帮你提炼出核心内容，直接生成一份学习笔记。整个过程：你只做了存那一步，剩下的全是AI在干活。

  

## 七、三个常见的坑

  

说完正向的，说三个最常见的坑。

第一个坑，一上来就建复杂的分类体系。建知识库的热情很高，一上来就设计了20个文件夹，写了详细的分类说明。结果三个月后自己都找不到东西。解决方式是先用一个简单的四层结构开始，让分类体系随着实际使用慢慢生长。

第二个坑，追求完美笔记。有人觉得知识库里的每篇笔记都必须写得特别好、有深度、有结构。结果每次想记录点东西就卡在"不知道怎么写才够好"上面，最后干脆不写了。Obsidian的每日笔记就是随手记，不需要完美。你今天看到一个句子特别好，复制进去；明天想到一个点子，三个字写进去。这才是可持续的使用方式。

第三个坑，只存不看。知识库建好了，每天往里面塞东西，但从来不让AI去读它。这样你的知识库就是一个数字垃圾堆。最低的使用频率是每周让AI帮你读一次你本周的每日笔记，帮你做个总结。你会惊讶地发现，你这一周零零碎碎记录的东西，其实比你以为的多得多。

如果你看完这篇文章觉得有道理，今天可以做的最小行动就一件事：去obsidian.md下载安装Obsidian，创建一个知识库，建四个文件夹：00-Inbox、01-Wiki、02-Areas、03-Projects。然后今天看到什么有用的信息，随手复制一段进00-Inbox。就这一件事，五分钟。剩下的一切，慢慢来。

---

觉得这篇文章不错的话，欢迎点赞、推荐、转发给你的朋友，让ta跟着手把手操作，搭建一个自己的本地知识库。

我建了一个微信群，都是一群玩AI的小伙伴，在群里彼此交流分享，感兴趣的，移步到公众号后台，回复“进群”。

我是Simonlin，下次见。

  

---

Original Simonlin Simonlin的精神世界

---

内容效果不满意？[点此反馈](https://feedback.notebooksyncer.com/feedback/e1d4066d_1780005758875?u=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzU1MDk3MzEwOA%3D%3D%26mid%3D2247488148%26idx%3D1%26sn%3D0c777d7160cb94c5179e36191e64ef7c%26chksm%3Dfa5f22f320be1791edaa59fe8ad05666aab8d1e64737bc08f040224fea10314117aa79378471%26mpshare%3D1%26scene%3D1%26srcid%3D0521KCosNeHFr6vfhyoznS5O%26sharer_shareinfo%3D0aab8b6e7c08f2612dc49a28c63daa20%26sharer_shareinfo_first%3Dc12c34b848c5cbddde20ec69a003d0a4%23rd&s=obsidian)