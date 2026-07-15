---
author: 小宅
source: 微信公众号
url: https://mp.weixin.qq.com/s?__biz=MzI2ODA5OTY0NA==&mid=2247486913&idx=1&sn=3c02665e83d815d2a4dc2a607da53ff4&chksm=eb5046553925f376b0ba4e75da64358354d0687108f2ec8885a69e75ead8b9b95ec8bc509b36&mpshare=1&scene=1&srcid=0521nV0MBwnM3X7p3NeefFCd&sharer_shareinfo=640b24edff19282a9fc981428b3cd705&sharer_shareinfo_first=c1ff328cea7b00f264640965f977d1d9#rd
saved: 2026-05-29 00:03:03
tags:
  - 笔记同步助手
id: c4f160c6-c5d3-4c4b-bf57-90aa162f2e6a
annotation: tips to organize image files in obsidian
---

公众号名称：obsidian指南

作者名称：小宅

发布时间：2026-04-26 22:40

Obsidian 里的各种图片，一保存就会变成一长串看不懂的乱码，全堆在根目录里，找起来特别费劲？

我以前就是这样：每次粘贴图片，都像在垃圾堆里翻东西。文件名看不懂，格式乱套，图片越存越多，笔记库越来越乱。

![[01_raw/_inbox/文章/images/a95c418aac04916dffa0f99a46f69ebe_MD5.png]]

而前几天有朋友留言也提到了这个问题！那今天要分享的这个方法，通过一个插件，就能让 Obsidian 的图片管理变得井井有条。这个插件叫做 **Image Converter**，它能自动做两件事：**给图片起好名字**、**优化图片格式**。

## 🌟 **第一步：先搞定图片放哪儿**

网上有各种方案，有用图床的，有本地存储的。我试了一圈，发现最简单有效的方法就是：**在 Obsidian 里设个固定地方放图片**。

这样做特别简单：

1.  打开 Obsidian 的**设置**
    
2.  找到 **文件与链接** → **附件默认存放路径**
    
3.  把默认的"仓库根目录"，改成"当前文件所在文件夹下指定的子文件夹"
    
4.  输入文件夹名字：`images`
    
    ![[01_raw/_inbox/文章/images/8477c63c21f4f0e3964c0d6605aa2b09_MD5.png]]
    

设置好后，效果是这样的：

-   在"写作总结"笔记里贴图片 → 图片自动放在"写作总结"文件夹的 `images` 子文件夹里
    
-   在"项目计划"笔记里贴图片 → 图片自动放在"项目计划"文件夹的 `images` 子文件夹里
    

每篇笔记的图片都独立存放，再也不乱套了！

自动在笔记文件夹内生成图片文件夹进行存放！

![[01_raw/_inbox/文章/images/bab4506485a69ef8f9787f1947444cce_MD5.png]]

## 🎯 **第二步：安装主角插件 Image Converter**

虽然图片有地方放了，但文件名还是乱七八糟的乱码。而且像我这种习惯用 微信截图的人，或者同步文章时，默认出来都是 PNG 格式，图片体积很大。

这时候就需要 **Image Converter** 上场了。它专治两个毛病：

-   **文件名看不懂**
-   **图片体积大**

安装很简单：

-   打开 Obsidian 的**社区插件市场**
    
-   搜索 **Image Converter**
    
-   点击安装并启用。
    
-   大家网络不好的可以通过小程序网盘安装！
    
    小宅的软件空间
    

## 🔧 **第三步：让图片都有"名字"**

安装完成后，打开 Image Converter 的设置页面。我们要让每张图片都有一个看得懂的名字。

关键设置在这里：**Filename** 格式

默认格式是：`{{noteName}}-{{timestamp}}`

-   `{{noteName}}`
    
    \= 笔记名字
    
-   `{{timestamp}}`
    
    \= 时间戳
    

你也可以自己修改格式，比如：

-   `{{noteName}}-图片`
-   `{{year}}年{{month}}月-{{noteName}}`

**设置后的效果：**

-   在"公众号写作"笔记里贴截图 → 图片自动命名为"公众号写作-1776250760498"
    
-   在"教程大纲"笔记里贴图片 → 图片自动命名为"教程大纲-1776250761234"
    

现在每张图片都带着笔记的名称了！

![[01_raw/_inbox/文章/images/d87fd19728ba0020518c5d080c0a00ed_MD5.png]]

## 💾 **第四步：自动压缩图片体积**

Image Converter 另一个超实用的功能是：**自动转换图片格式**。

很多人喜欢截图保存，或者从微信传图片，这些默认都是 PNG 格式。PNG 文件大，占空间不说，而且公众号还不支持！我平时写文章上传到公众号还要折腾格式转换。

我的设置是这样的：

-   **输出格式**
    
    ：JPEG
    
-   **压缩质量**
    
    ：85%（兼顾清晰度和体积）
    

为什么选 JPEG？

1.  公众号文章支持 JPEG
    
2.  体积比 PNG 小很多
    
3.  大部分网页都兼容
    

如果你主要在本地使用，也可以选 WebP（更省空间）。

![[01_raw/_inbox/文章/images/cad5b05d9e0fc5b28eac0a594cca44cb_MD5.png]]

📁 **完整工作流：粘贴 → 自动完成**

经过四步设置后，现在的工作流程变得超级简单：

1.  碰到好内容 → 截图（或 Ctrl+C 复制图片）
    
2.  回到 Obsidian → Ctrl+V 粘贴
    
3.  **系统自动完成**

-   图片放在对应笔记的 `images` 文件夹
    
-   文件名变成"笔记名-时间戳.jpeg"
    
-   格式自动从 PNG 优化为 JPEG
    

## 🏆 **这样做的好处**

### **1\. 管理方便**

以前找张截图要翻半天，现在一看名字就知道是哪篇笔记的图片。

### **2\. 节省空间**

PNG 转 JPEG，图片体积能减少 50-70%，也让我们云储存会轻松不少！

### **3\. 发布省事**

做公众号的朋友特别有体会：不用再手动转格式，或者遇到大于2M的情况就会少很多！

### **4\. 查找快捷**

文件名带笔记名，搜索时一找一个准。

## 💡 **实用小技巧**

### **组合拳打法**

把 **Image Converter** 插件和 **Excalidraw** 一起用，做图解笔记特别方便：

-   Excalidraw 画图 → 导出图片
    
-   粘贴进 Obsidian → Image Converter 自动处理
    

### **配合模板使用**

设置自动图片引用格式，让图片在笔记里显示得更整齐。

## 🔍 **如果遇到问题**

❓ **问题**：某些网站图片保存不出来  
💡 **试试**：看看有没有特殊的脚本限制

❓ **问题**：转换后图片模糊  
💡 **试试**：可以尝试调高一下图片质量！

## ✨ 可以说Image Converter 用最小的代价，解决了 Obsidian 图片管理最难搞的两个问题：**命名乱**和**体积大**。

如果你也受够了 Obsidian 里的图片管理混乱，这个插件绝对值得一试。花 5 分钟设置，换来的是清晰整洁的笔记库。

关注obsidian指南，更多小技巧等着你！

---

![[01_raw/_inbox/文章/images/541d3e69b0f5c5e483abc25b4a68e809_MD5.jpg|cover_image]]

原创 小宅 obsidian指南

---

内容效果不满意？[点此反馈](https://feedback.notebooksyncer.com/feedback/d65405dd_1780005778998?u=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzI2ODA5OTY0NA%3D%3D%26mid%3D2247486913%26idx%3D1%26sn%3D3c02665e83d815d2a4dc2a607da53ff4%26chksm%3Deb5046553925f376b0ba4e75da64358354d0687108f2ec8885a69e75ead8b9b95ec8bc509b36%26mpshare%3D1%26scene%3D1%26srcid%3D0521nV0MBwnM3X7p3NeefFCd%26sharer_shareinfo%3D640b24edff19282a9fc981428b3cd705%26sharer_shareinfo_first%3Dc1ff328cea7b00f264640965f977d1d9%23rd&s=obsidian)