---
author: RUNOOB
source: 微信公众号
url: https://mp.weixin.qq.com/s?__biz=MzA5NDIzNzY1OQ==&mid=2735635680&idx=1&sn=b93bba76ed44c031b04a4fa8baffc20d&chksm=b72635f7b23ad3ea7eb0e6f09f58efdf8f694aa8b33e70c0eeefb5db5f7dfce5712a94386913&mpshare=1&scene=1&srcid=0622nlVbLZkMWFx2EZoeSAno&sharer_shareinfo=58f97153f00c0193e19d4e25fb419788&sharer_shareinfo_first=58f97153f00c0193e19d4e25fb419788#rd
saved: 2026-06-22 09:36:43
tags:
  - 笔记同步助手
annotation: Useful plugin to monitor state of claude
id: 659c93e1-6016-4f83-bca6-c1232754e250
---

公众号名称：菜鸟教程

作者名称：RUNOOB

发布时间：2026-06-22 11:27

做 AI 编程一段时间之后，很容易进入一种奇怪状态，天天看着终端一直在滚，模型一直在输出，代码一直在生成。

但有个问题，不知道它到底在干什么？

比如这些场景：

-   现在到底用的是哪个模型？Sonnet 还是 Opus？
    
-   当前上下文用了多少，还剩多少？
    
-   这一轮已经消耗多少 Token？
    
-   Claude Code 有没有进入压缩（compaction）？
    
-   当前目录在哪个 Git 分支？
    
-   本周额度还有多少？
    
-   这一轮到底烧了多少钱？
    

很多时候只能，打开另一个终端，执行 `/usage，`切出去看 Git，再回来继续写。

![[01_raw/_inbox/文章/images/c9b868ec9714cd72fd7eb8f8d0a78d1d_MD5.png]]

信息也不是拿不到，就是太分散，不知道当前状态。

终端工具这些年一直在进化，编辑器有状态栏，浏览器有开发者工具，监控平台有 Dashboard。

但到了 AI 编程阶段，终端反而退回了黑盒，模型在运行，上下文在增长，费用在累计，但确没有显示出来。

然后，有问题就有人解决，看到一个 **ccstatusline 项目，专门给 Claude Code 使用的终端状态栏工具。**

**ccstatusline 通过读取 Claude Code 的运行信息，在终端底部持续显示状态内容。**

![[01_raw/_inbox/文章/images/15ea8d2508ee83400f116ba8ebfe3ba7_MD5.png]]

**ccstatusline 基于 Node.js/Bun 开发，通过 npm 发布，提供了一个交互式的 TUI 配置界面，你只需要勾选想显示的内容，调整一下颜色和顺序，就能直接看到效果。**

开源地址：https://github.com/sirmalloc/ccstatusline

Star 数 10k+，还是很多人在用：

![[01_raw/_inbox/文章/images/7c0b0975e4aad6219ebcf773195d86dd_MD5.png]]

这个是英文版本，配置界面不太友好，然后也有对应的汉化版本：

汉化版地址：https://github.com/huangguang1999/ccstatusline-zh

汉化版本使用的都是中文界面：

![[01_raw/_inbox/文章/images/30dabdc9ca3122f992106ded4acbeed8_MD5.png]]

**ccstatusline** 提供了几十种预设的 widget，涵盖几个大类：

-   模型信息：当前模型名称、thinking effort 级别、上下文窗口使用量
    
-   Token 统计：输入/输出 token 数、速度、缓存命中率
    
-   用量监控：会话用量、周用量、额外用量、计费块倒计时
    
-   Git 状态：分支名、PR/MR 链接、未提交改动数、 ahead/behind
    
-   会话信息：会话名称、当前工作目录、会话成本
    
-   自定义：纯文本、自定义命令输出、分隔符
    

渲染模式支持普通的纯文本，也支持 Powerline 风格（带箭头分隔符和渐变颜色），我们可以配置多行状态栏，每行放不同的信息组。

![[01_raw/_inbox/文章/images/9a3ba1e653601344f7266fc3bc7428f7_MD5.png]]

项目技术栈：

-   TypeScript
    
-   React
    
-   Ink（终端 React）
    
-   Node.js / Bun
    

---

## 1、安装与环境准备

**环境要求**

-   Node.js ≥ 18
    
-   npm 或 Bun
    
-   已安装 Claude Code
    

最简单**安装**方式：

```
npx -y ccstatusline@latest
```

或者：

```
bunx -y ccstatusline@latest
```

![[01_raw/_inbox/文章/images/12afe8fb63816d24307f53f7de27fd93_MD5.png]]

直接给 Claude Code 安装上，然后建议选择Pinned global install，这样不会自动跟随最新版升级。

![[01_raw/_inbox/文章/images/3740f23a25d818499438e33f4572bad5_MD5.png]]

在 TUI 里选择 **Pinned global install**，它会把你当前运行的版本全局安装好，并把 `ccstatusline` 命令写入 Claude Code 的配置文件。

![[01_raw/_inbox/文章/images/902f03273cd4c2abc647c22a28a62a7b_MD5.png]]

安装完成后，会自动写入 Claude Code 的 配置文件中 ～/.claude/settings.json：

![[01_raw/_inbox/文章/images/92135d25e3ea6802819eb74f1b3f2ac3_MD5.png]]

```
中文版通过 npm 全局安装：
```

```
npm install -g ccstatusline-zh
```

或者使用 Bun：

```
bun install -g ccstatusline-zh
```

在 Claude Code 设置中添加状态栏配置，编辑 `～/.claude/settings.json`：

![[01_raw/_inbox/文章/images/c41e45bce143570ef30cf3ecfc74f6e5_MD5.png]]

`ccstatusline`配置默认保存在 ～/.config/ccstatusline/settings.json。

---

### 2、启动配置界面

### 启动中文版设置：

```
ccstatusline-zh setup
```

打开交互式 TUI 配置界面，我们可以：

-   添加、删除、重新排列组件
    
-   设置颜色和样式
    
-   选择 Powerline 主题
    
-   实时预览状态栏效果
    

进入编辑状态栏：

![[01_raw/_inbox/文章/images/4d9e182e1dbc38bdef73a3484d547253_MD5.png]]

我们可以回车进入编辑状态栏：

![[01_raw/_inbox/文章/images/d843714f7311df4dee64181f8ce73cd4_MD5.png]]

第一行有 7 个组件，对应信息为：

![[01_raw/_inbox/文章/images/8782b1784d43f30786eb0cf8b82a283f_MD5.png]]

**第一步：添加 widget**

按 `a` 进入添加界面，你会看到分类列表：

![[01_raw/_inbox/文章/images/ede8d59b6b5a6101c22d76805cc3a258_MD5.png]]

用方向键选择分类，回车展开，再选择具体的 widget。

![[01_raw/_inbox/文章/images/69f43893c77dc32a883d017dbcf9797c_MD5.png]]

选择总 Token 后就可以看到设置的预览：

![[01_raw/_inbox/文章/images/569cb362f60db4a1bdc13d1a10f8936f_MD5.png]]

**第二步：调整顺序**

按下 Enter 键可以移动位置：

![[01_raw/_inbox/文章/images/8865fd8c7703a85ed8c23493868e1603_MD5.png]]

移动到最后：

![[01_raw/_inbox/文章/images/76c18f5b1ce04d9b17c93324bdfbf3f3_MD5.png]]

然后回车，就可以看到效果：

![[01_raw/_inbox/文章/images/c25b83da87246311091e3380b3855a05_MD5.png]]

**设置完成后，按 Esc 回退到主界面，然后保存并退出：**

![[01_raw/_inbox/文章/images/4edf4af6d5c8c766eda50e21efed128b_MD5.png]]

配置会自动写入 `～/.config/ccstatusline/settings.json`，同时自动安装到 Claude Code 的 `settings.json` 里，下次启动 Claude Code 时，状态栏就会生效。

![[01_raw/_inbox/文章/images/b28cabed1b7c0f7a10f7b426b6e8f3b7_MD5.png]]

其他的配置可以继续使用 ccstatusline-zh setup，进行设置，比如颜色修改等。

---

内容效果不满意？[点此反馈](https://feedback.notebooksyncer.com/feedback/84a0ded6_1782113800611?u=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzA5NDIzNzY1OQ%3D%3D%26mid%3D2735635680%26idx%3D1%26sn%3Db93bba76ed44c031b04a4fa8baffc20d%26chksm%3Db72635f7b23ad3ea7eb0e6f09f58efdf8f694aa8b33e70c0eeefb5db5f7dfce5712a94386913%26mpshare%3D1%26scene%3D1%26srcid%3D0622nlVbLZkMWFx2EZoeSAno%26sharer_shareinfo%3D58f97153f00c0193e19d4e25fb419788%26sharer_shareinfo_first%3D58f97153f00c0193e19d4e25fb419788%23rd&s=obsidian)