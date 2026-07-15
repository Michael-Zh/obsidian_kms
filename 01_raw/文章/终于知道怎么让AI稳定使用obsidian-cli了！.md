---
author: 农民伯伯
source: 微信公众号
url: https://mp.weixin.qq.com/s?__biz=MzkzODkxMzA2OQ==&mid=2247484337&idx=1&sn=584328a18458574c0c01259f2d740c21&chksm=c3ce1fcdeef87456a04670048b6d7ed2bd09291a07c2273fc66ffaecda33326f0eec47e9bef1&mpshare=1&scene=1&srcid=0419EQ9fEsxyuyocXTFLGeDE&sharer_shareinfo=76e67bbafe7c2980cee92ca253dfa914&sharer_shareinfo_first=a4715e14d78a0a0234f7be0ba8f4ec26#rd
saved: 2026-05-29 00:03:21
tags:
  - 笔记同步助手
id: 22151028-4a2a-4542-8962-188dd7a336a1
annotation: Obsidian Cli x AI tips
summary: "Documents four recurring problems when using AI with obsidian-cli for Obsidian automation: AI ignoring CLI docs (fixed by a SessionStart hook), incorrect task cancellation syntax, misuse of task tags, and incomplete error logging due to exit codes not capturing stderr. Provides concrete fixes for each using Claude Code's hook mechanism and CLAUDE.md rule improvements."
processed: 2026-06-06
---

公众号名称：农民伯伯吖

作者名称：农民伯伯

发布时间：2026-04-18 19:13

# 关于《普通人如何驾驭AI》的问题复盘

大家好，这期内容是对《普通人如何驾驭AI——维护人脉关系》视频中AI的执行问题复盘。

对视频演示感兴趣的小伙伴请移步B站或小红书观看原视频。

![[01_raw/_inbox/文章/images/54b04eef08485fdc764d1ad4d25a3fed_MD5.png]]

原视频封面

## 前情提要

下面的这些是在视频里让AI执行的三个指令：

```
# 指令1 创建人物档案
我有一个贵人朋友名叫张三，每次在我有困难的时候他都会出手帮助度过危机，请帮我建立一个人物档案。另外后天我准备去杭州拜访他，也帮我建立一个代办任务。

# 指令2 更新任务档案
原本打算后台去拜访张三的，没想到他今天出差顺便就来看我了，还给我带了西湖醋鱼。帮我取消后天的拜访。

# 指令3 批量创建物品
请帮我分类保管以下物品信息：
公众号AppID、Office 激活码、仓耳今楷字体下载地址、Windows激活码、Syncthing下载地址

# 执行难点
✅任务拆解，AI需判断指令涉及哪些业务模块
✅领域判断，AI需判断代办任务属于哪个领域
✅多任务执行，AI需往备忘录及行动管理特定文件夹和笔记位置写入数据
✅使用特定笔记模板新增的人物档案
✅遵循html注释规则更新人物档案
✅使用emoji语法规则创建代办任务
❌使用emoji语法规则取消代办任务
```

## 问题1 AI不会用obsidian-cli

**问题描述**：虽然知识库根目录的CLAUDE文档里要求AI看obsidian-cli文档，但总被忽略执行，AI靠自己试错猜测走了不少弯路。

**问题排查**：CLAUDE文件性质依旧是提示词，约束力不强，AI有可能不遵守。

**解决办法**：考虑到现阶段AI对obsidian-cli命令语法训练不够，且该命令在知识库里使用频率较高，决定用hook机制，_强制AI在对话开始时（SessionStart）读取obsidian-cli文档_（1157字，token消耗尚可接受）。等未来AI模型熟悉obsidian-cli命令之后再删除该hook，以节约token。

下图是hook的生命周期，让AI在SessionStart时触发读取文档，整个会话读一遍文档就够了。

![[01_raw/_inbox/文章/images/943dc736225d27c6155a63170bf9bad3_MD5.png]]

hook生命周期

**这里我踩了一个坑。  
**

我写代码比较保守，在没确认AI提供的代码有效之前会用`//`注释源代码而不是直接删除。

当我在`settings.json`文件里使用`//`之后，_这个举动会让整个json文件失效_，导致我在`settings.json`里添加的hook无法正常被触发。

## 问题2 取消任务语法错误

**问题描述**：取消任务AI做对了一半，我在演示视频里也只说对了一半。视频里我介绍的方式可以将任务标记为删除，而AI的做法则是标记任务取消的时间。正确的做法是将两者结合。

```
# 我在视频里的做法 → 没有取消日期
- [-] #实践 准备拜访张三的礼物 📅2026-04-13
  
# AI在视频里的做法 → 任务没有标记为取消
- [ ] #实践 准备拜访张三的礼物 📅2026-04-13 ❌ 2026-04-12 张三已来访，原拜访计划取消

# 正确做法
- [-] #实践 准备拜访张三的礼物 📅2026-04-13 ❌ 2026-04-12
```

**解决办法**：在行动管理（CLAUDE.md）规则里介绍教任务规则的时候，附上一个取消任务的示例。

## 问题3 滥用任务标签

**背景信息**：为了跟踪我的知识来源，我允许AI在创建任务的时候使用任务标签，默认有以下两种：

-   • `#学习`：侧重理论学习，例如看书、看教程
    
-   • `#实践`：侧重实践学习，例如科学实验、上机实操
    

**问题描述**：我发现AI将`#实践`标签滥用在张三拜访这件事上。拜访任务根本不需要用到实践标签。

**解决办法**：在行动管理（CLAUDE.md）规则里提供两种标签的具体示例。

## 问题4 报错日志漏报

**问题描述**：报错日志里看不到obsidian-cli命令的报错记录。

**问题排查**：一开始我尝试用 hook 去捕获非 0 退出码，想用这个办法记录错误日志，但这里有个坑。因为退出码为0并不代表任务执行成功，这会漏掉很多错误日志。

**背景信息**：在计算机程序里，退出码（Exit Code）是程序在执行命令之后告知主程序执行结果用的。在 bash 脚本里，_0 代表成功_，而_除了 0 之外的其他退出码则代表失败_，例如：

-   • 126 → 无法执行（权限不够）
    
-   • 127 → 命令未找到
    
-   • 130 → 程序被中断。
    

以下图为例，虽然我们看到 `Bashobsidian.com note create` 命令的返回结果是 `Error: Command "note" not found...`，但右侧的 status 却显示 `completed`。

![[01_raw/_inbox/文章/images/51263f53e5786a5ba556818368ee3935_MD5.png]]

使用obsidian-cli创建笔记

这说明，在 AI 的眼里，这个任务是已经执行完了，至于结果怎么样，那是另一个问题。

我举一个例子大家就明白了。

假如你的老板让你去楼下买蜜雪冰城给大家当下午茶，你下楼之后发现奶茶店倒闭了，只好无功而返。那么：

-   • 下楼再回来这个动作，你确实执行完了 → 对应的`status`是`completed`
    
-   • 但由于店铺倒闭，你没买到奶茶 → 对应的`ERROR`是`The shop has closed`
    

**这就是退出码和报错信息的区别**：

-   • 退出码只告诉你：_程序有没有正常跑完_（0 = 跑完了，非0 = 中途崩了）
    

-   • 报错信息才告诉你：事情到底办没办成
    

所以_0 退出码 ≠ 结果正确_。这就是为什么_不能只靠检查退出码来捕获所有报错_，因为程序可能返回 0（事情没办成，但程序觉得自己跑完了），真正的错误信息只写在屏幕日志里。

**解决办法**：用hook捕获错误不是很完美，在执行结束之后让AI自己总结又费token。现阶段还是人工看操作记录分析问题吧，这个问题留给以后处理。

## 一个注意事项

obsidian-cli在创建笔记的时候支持传入`template=`

---

![[01_raw/_inbox/文章/images/b0aa3c00f39c6fd52d9cbf8204b14bbc_MD5.jpg|cover_image]]

原创 农民伯伯 农民伯伯吖

---

内容效果不满意？[点此反馈](https://feedback.notebooksyncer.com/feedback/e68544a1_1780005799371?u=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzkzODkxMzA2OQ%3D%3D%26mid%3D2247484337%26idx%3D1%26sn%3D584328a18458574c0c01259f2d740c21%26chksm%3Dc3ce1fcdeef87456a04670048b6d7ed2bd09291a07c2273fc66ffaecda33326f0eec47e9bef1%26mpshare%3D1%26scene%3D1%26srcid%3D0419EQ9fEsxyuyocXTFLGeDE%26sharer_shareinfo%3D76e67bbafe7c2980cee92ca253dfa914%26sharer_shareinfo_first%3Da4715e14d78a0a0234f7be0ba8f4ec26%23rd&s=obsidian)