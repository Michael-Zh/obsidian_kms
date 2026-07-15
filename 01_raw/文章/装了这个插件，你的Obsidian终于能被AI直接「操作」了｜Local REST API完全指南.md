---
author: obsidian黑曜石
source: 微信公众号
url: https://mp.weixin.qq.com/s?__biz=MzkyODM0MzI3MA==&mid=2247484519&idx=1&sn=3c3b9cfe12618d14448a342659cbd833&chksm=c3786fd19bafde7288ee98f2638ae767b97848543724a6a06a55600e3b319e03a3fd5368f122&mpshare=1&scene=1&srcid=0604icAOHte2fsl6eaUJBz8A&sharer_shareinfo=072a499a6f821a13bbc6ef26c30e7e4e&sharer_shareinfo_first=072a499a6f821a13bbc6ef26c30e7e4e#rd
saved: 2026-06-04 01:13:08
tags:
  - 笔记同步助手
id: 1e68b049-bd14-4147-8d71-6cae44a4a57d
annotation: one way to use AI to manage obsidian
summary: "Complete guide to the Local REST API Obsidian plugin, which opens a local HTTPS server at port 27124 exposing vault operations as REST endpoints and an MCP server. Enables AI agents to create, read, update, and delete notes programmatically, trigger Obsidian commands, and manage periodic notes — demonstrated through three automation scenarios: AI agent auto-tagging, browser bookmark clipping, and a Dataview-powered daily stats dashboard."
processed: 2026-06-06
---

公众号名称：obsidian黑曜石

作者名称：obsidian黑曜石

发布时间：2026-05-25 07:52

# 周一好啊，上班快乐！![[01_raw/_inbox/文章/images/193bb0f4c4f2e21a2876c6800f4abf60_MD5.png||20]]上个月我在服务器上跑 Hermes Agent，想让它自动把每天的学习笔记写入 Obsidian。结果卡在一个问题上：**Agent 能生成内容，但它没法直接把内容写进我的笔记库。**

Obsidian 官方 CLI 要开图形界面，服务器跑不了。第三方 CLI 能写文件，但改个文件名双链就全断了。

**然后我发现了一个装了两年、下载量 1900+ 却几乎没人写教程的插件——Local REST API。**

装好之后，你的 Obsidian 在本地开了一个 HTTPS 接口。任何能发 HTTP 请求的工具——浏览器插件、Python 脚本、AI Agent——都能直接读写你的笔记。笔记库不再是一个封闭的 vault，而是一台可编程的服务器。![[01_raw/_inbox/文章/images/593c61486390b192846752e142294de7_MD5.jpg]]

---

## 它做了什么：把 Obsidian 变成 API 服务器

一句话解释：**这个插件在你电脑上跑了一个小型的 Web 服务器，通过 REST API 暴露了 Obsidian 的核心操作。**

装好之后，打开浏览器访问 [https://127.0.0.1:27124/](https://127.0.0.1:27124/)，你会看到一个 API 文档页面——所有可用的接口都列在上面，可以直接在浏览器里测试。

它是 coddingtonbear 开发的社区插件，目前版本 3.6.0，在社区插件市场可以直接安装。插件描述只有一句话：_"Get, change or otherwise interact with your notes in Obsidian via a REST API."_

翻译成人话：**你的 Obsidian 有了一个可编程的「开关」。**

---

## 能做什么：不止是读写笔记

我花了一个下午把它的 API 文档通读了一遍，整理出四个最实用的能力：

### 1\. 笔记 CRUD（创建、读取、更新、删除）

```
# 读取一篇笔记
curl-k-H"Authorization: Bearer YOUR_API_KEY"\
  https://127.0.0.1:27124/vault/我的笔记.md

# 创建新笔记
curl-k-X POST \
-H"Authorization: Bearer YOUR_API_KEY"\
-H"Content-Type: text/markdown"\
-d"# 新笔记标题"\
  https://127.0.0.1:27124/vault/新笔记.md

# 搜索笔记
curl-k-H"Authorization: Bearer YOUR_API_KEY"\
"https://127.0.0.1:27124/search?query=API"
```

这是最基础的操作，但也是最核心的——有了 CRUD，任何外部程序都能以编程方式管理你的笔记。

### 2\. 周期性笔记（日记/周报）

插件支持通过 API 获取或创建 Daily Note、Weekly Note 等周期性笔记。这意味着你可以写一个定时脚本，每天早上自动在日记里插入当天的天气、日程、待办事项。

### 3\. 执行 Obsidian 命令

API 可以直接调用 Obsidian 的内部命令——相当于你手动按 `Ctrl+P` 然后输入命令名。这个能力让自动化空间大了十倍：你可以远程触发插件功能、切换视图、运行 Dataview 查询。

### 4\. MCP Server（这是真正的杀手锏）

从 3.x 版本开始，这个插件内置了 **MCP（Model Context Protocol）服务器**。

MCP 是 Anthropic 提出的一套标准协议，让 AI 模型能够通过统一的接口和外部工具交互。说人话就是：**装了 Local REST API 之后，支持 MCP 的 AI 工具（比如 Claude Desktop、Hermes、OpenClaw）可以直接操作你的 Obsidian 笔记。**

我现在的用法是：Hermes Agent 跑在服务器上 → 通过 MCP 协议连接我本机的 Obsidian → Agent 自动写笔记、更新 frontmatter、建双链。全程不需要我手动操作 Obisidian。

这比之前用第三方 CLI 的方案稳定多了——因为 API 调用的是 Obsidian 内部接口，改文件名不会断双链，创建笔记不会绕过 Obsidian 的索引机制。

---

## 安装与配置（3 分钟）

社区插件市场搜索 `Local REST API` → 安装 → 启用 → 生成 API Key → 勾选 MCP Server。

配置完成后访问 [https://127.0.0.1:27124/](https://127.0.0.1:27124/) 即可看到完整 API 文档。

---

## 三个我实际在用的场景

### 场景一：AI Agent 自动整理笔记

我在服务器上跑了一个定时任务：每天早上 7 点，Hermes Agent 通过 MCP 连接我的 Obsidian，扫描 `02-草稿/` 目录下的新笔记，根据内容自动打标签、补 frontmatter、归类到对应文件夹。

之前这些事我得手动做——打开笔记、加 YAML、拖到对应文件夹。现在 Agent 全自动处理，我只需要负责写初稿。

### 场景二：浏览器一键剪藏到指定位置

我写了一个简单的浏览器书签脚本——点一下，当前网页的标题和链接自动追加到 Obsidian 的 `素材库/待整理/` 目录下。

原理就是一条 POST 请求：

```
fetch('https://127.0.0.1:27124/vault/素材库/待整理/'+
newDate().toISOString().slice(0,10)+'-'+
document.title+'.md',{
method:'POST',
headers:{
'Authorization':'Bearer YOUR_KEY',
'Content-Type':'text/markdown'
},
body:`# ${document.title}\n\n> 来源：${location.href}\n\n`
})
```

比官方 Web Clipper 快，而且能精确控制存到哪里。

### 场景三：Dataview + API = 活的数据仪表盘

我建了一个 `仪表盘.md`，里面是一段 Dataview 查询——显示本周写了多少篇笔记、每个标签下有多少篇。

然后我写了一个 Python 脚本，每天早上通过 API 读取这张仪表盘笔记的内容，把关键数字推送给我。

这样我不用打开 Obsidian，就能在手机上看到「本周已写 3 篇，标签 \#插件推荐 下有 12 篇」——一个活的知识库健康度面板。

---

## 谁最适合用？

| 场景 | 为什么需要 Local REST API |
| :-- | :-- |
| 用 AI Agent 管理知识库 | MCP Server 让 Agent 直接操作笔记 |
| 写自动化脚本 | HTTP 请求 = 操作笔记，不限语言 |
| 多工具联动 | Obsidian ↔ 浏览器 / Python / Shortcuts |
| 定时任务 | 日记自动填充、数据自动汇总 |
| 开发自己的插件/工具 | 不用学 Obsidian Plugin API，直接调 REST |

如果你只是用 Obsidian 手动记笔记，这个插件可能用不上。但如果你在做任何形式的自动化——AI Agent、脚本、工具链——它几乎是基础设施级别的存在。

---

## 注意事项

1.

**API Key 不要泄露**。这个 Key 相当于你的笔记库密码，任何人拿到都能读写你的笔记。

2.

**本地使用**。API 监听的是 `127.0.0.1`（本机回环地址），默认不接受外部网络连接，数据不会离开你的电脑。

3.

**自签名证书**。HTTPS 用的是本地自签名证书，浏览器会提示不安全——这是正常的，因为证书没有经过 CA 认证。在本地使用完全没问题。

4.

**端口冲突**。如果 27124 端口被其他程序占用，去插件设置里换一个端口。

---

如果你想让你的 Obsidian 真正「活」起来——能被 AI 操作、能和其他工具联动、能自动化处理笔记——试试 Local REST API。装好之后花 3 分钟配置 API Key 和 MCP，打开 [https://127.0.0.1:27124/](https://127.0.0.1:27124/)——那种「我的笔记库变成了一个服务器」的感觉，值得。

**如你无法下载安装或不会使用，后台回复「REST API」，我将提供插件分享和帮助文档。**

我是黑曜石，陪你打造第二大脑。从手写笔记到可编程知识库，只差一个 API 接口。下期见。

![[01_raw/_inbox/文章/images/3084fea627cf302c69bb1f7c6393de4f_MD5.jpg]]

_插件功能经本人实测验证。_🎁 点亮**推荐**❤️，告诉大家：让AI来帮你打工。_  
_

_插件地址：https://community.obsidian.md/plugins/obsidian-local-rest-api_  
_GitHub：https://github.com/coddingtonbear/obsidian-local-rest-api_

---

内容效果不满意？[点此反馈](https://feedback.notebooksyncer.com/feedback/e1830135_1780528386375?u=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzkyODM0MzI3MA%3D%3D%26mid%3D2247484519%26idx%3D1%26sn%3D3c3b9cfe12618d14448a342659cbd833%26chksm%3Dc3786fd19bafde7288ee98f2638ae767b97848543724a6a06a55600e3b319e03a3fd5368f122%26mpshare%3D1%26scene%3D1%26srcid%3D0604icAOHte2fsl6eaUJBz8A%26sharer_shareinfo%3D072a499a6f821a13bbc6ef26c30e7e4e%26sharer_shareinfo_first%3D072a499a6f821a13bbc6ef26c30e7e4e%23rd&s=obsidian)