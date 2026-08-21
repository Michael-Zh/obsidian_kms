---
author: 硅基铁匠
source: 微信公众号
url: https://mp.weixin.qq.com/s?__biz=MzcwNTE3NzI0OA==&mid=2247487131&idx=1&sn=3f6c950b3ea3e923023c0be0587b6b86&chksm=f55b58f48d55532e6ebb2f333380688b694b692121dc76bbcdc1e0de24fceae25224f71fec48&mpshare=1&scene=1&srcid=0817A22FHX1ZcrewMviAq4ta&sharer_shareinfo=c6b4c9838fb57f345dee315bf1c3800a&sharer_shareinfo_first=c6b4c9838fb57f345dee315bf1c3800a#rd
saved: 2026-08-17 08:19:22
tags:
  - 笔记同步助手
annotation:
id: 5cd71c73-f7da-4008-910d-2639b50c8747
---

公众号名称：硅基铁匠

作者名称：硅基铁匠

发布时间：2026-07-08 06:35

![[01_raw/_inbox/文章/images/f82433bcc2d0fa7066d70871ce10060f_MD5.jpg]]

Photoshop 订阅费这件事，对很多普通人不算小钱。

偶尔修图、做封面、抠个图、改一张海报，一年付几百美元的软件费，心里难免不舒服。直接换 GIMP 又会遇到另一个问题：功能够用，但界面、面板、快捷键和 Photoshop 差太多，手已经学会的肌肉记忆全废了。

PhotoGIMP 解决的就是这件小但很疼的事。

它本身不是新的修图软件。它是一个给 GIMP 3.0+ 用的免费补丁。装完以后，GIMP 的工具布局、面板位置、快捷键、启动图、应用图标和默认设置会更接近 Photoshop 。对从 Photoshop 切过来的人来说，打开后不会那么陌生。

项目地址在 GitHub：`Diolinux/PhotoGIMP`。当前仓库显示 GPL-3.0 许可证，Star 已经超过 1.4 万，支持 Windows 、 macOS 、 Linux 。

![[01_raw/_inbox/文章/images/8dec0c6b9c6f428b3d7e1cdba48bcfbf_MD5.jpg]]

PhotoGIMP 官方 README 里写得很清楚，它主要改的是 GIMP 配置，不是魔改 GIMP 本体。

它会替换或新增这些配置：

-   • `shortcutsrc`：把键盘快捷键映射得更像 Photoshop
-   • `toolrc`：调整工具顺序和工具配置
-   • `sessionrc`：调整窗口布局和面板位置
-   • `dockrc`：调整 Dock / 面板配置
-   • `gimprc`：修改画布、网格等通用偏好设置
-   • `contextrc`：设置默认工具和颜色状态
-   • `splashes/`：换成 PhotoGIMP 启动画面
-   • `theme.css`：做一些界面主题调整
-   • `templaterc`：加入预设画布模板

Linux 版本还会加一个 `.desktop` 启动器和应用图标，让系统菜单里显示 PhotoGIMP 的名字和图标。

这类方案的好处是轻。它没有把 GIMP 变成另一个闭源软件，也没有让你额外装一个巨大的编辑器。它只是把 GIMP 调成更接近 Photoshop 的工作习惯。

![[01_raw/_inbox/文章/images/2e8c23b1816cfc934af19716c7f97bfb_MD5.jpg]]

## 适合谁

PhotoGIMP 适合三类人。

第一类是以前用过 Photoshop，但现在只做轻量修图的人。比如做公众号封面、电商图、海报、小红书配图、 PPT 配图，不需要 Photoshop 全家桶，也不想每年付订阅费。

第二类是想用开源软件的人。 GIMP 本身免费、开源、跨平台，PhotoGIMP 也是 GPL-3.0 。图片保存在本机，不需要 Adobe 账号，也没有云端登录这一层。

第三类是公司或团队里的非专业设计岗位。很多运营、产品、内容同学只是偶尔改图，PhotoGIMP 可以让他们用熟悉的快捷键完成基本操作。

它不适合重度 Photoshop 工作流。比如大量依赖 PSD 高级兼容、 Adobe 插件、 Camera Raw 、团队云协作、印刷级色彩管理的专业流程，还是要谨慎迁移。

## 安装前先做两件事

安装前先确认两点。

### 1\. 安装 GIMP 3.0 或更新版本

PhotoGIMP 3 是为 GIMP 3.0+ 做的。 GIMP 2.10 的配置格式不一样，不建议混用。

GIMP 下载入口：

```
https://www.gimp.org/downloads/
```

Linux 用户也可以从 Flathub 安装：

```
https://flathub.org/apps/org.gimp.GIMP
```

### 2\. 先打开一次 GIMP，再关闭

这一步很重要。

GIMP 第一次启动时会生成配置目录。 PhotoGIMP 要覆盖的就是这些配置文件。顺序应该是：

```
安装 GIMP → 打开一次 → 关闭 GIMP → 安装 PhotoGIMP
```

如果 GIMP 还没生成配置目录，你直接复制 PhotoGIMP 文件，很容易放错地方。

## Windows 安装教程

先备份当前配置。

按 `Windows + R` 打开运行窗口，输入：

```
%APPDATA%\GIMP
```

回车后，把里面的 `3.0` 文件夹复制到桌面或其他安全位置。

然后开始安装：

1.  1\. 确认电脑已经安装 GIMP 3.0 或更新版本
2.  2\. 打开一次 GIMP，然后关闭
3.  3\. 下载 PhotoGIMP Windows 压缩包

```
https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP.zip
```

1.  4\. 解压 `PhotoGIMP.zip`
2.  5\. 进入解压后的文件夹，复制里面的 `3.0` 文件夹
3.  6\. 再次按 `Windows + R`，输入：

```
%APPDATA%\GIMP
```

1.  7\. 把 `3.0` 文件夹粘贴进去
2.  8\. 如果系统提示同名文件，选择替换
3.  9\. 重新打开 GIMP

如果界面变成 PhotoGIMP 的布局，说明成功了。

如果你用 Chocolatey，也可以试这个命令：

```
choco install photogimp
```

这个 Chocolatey 包由社区维护，安装前可以先看一下包页面和维护状态。

## macOS 安装教程

先备份配置。

打开 Finder，按：

```
Cmd + Shift + G
```

输入：

```
～/Library/Application Support/GIMP
```

把里面的 `GIMP` 文件夹复制一份保存。

安装步骤：

1.  1\. 安装 GIMP 3.0 或更新版本
2.  2\. 打开一次 GIMP，然后关闭
3.  3\. 下载 PhotoGIMP macOS 压缩包

```
https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP.zip
```

1.  4\. 解压后复制里面的 `3.0` 文件夹
2.  5\. Finder 里按 `Cmd + Shift + G`
3.  6\. 进入：

```
～/Library/Application Support/GIMP
```

1.  7\. 如果里面有旧的 `2.10` 文件夹，先删除，避免冲突
2.  8\. 粘贴 `3.0` 文件夹
3.  9\. 如果系统提示替换或合并，按提示处理
4.  10\. 重新打开 GIMP

## Linux 安装教程

Linux 推荐先用 Flathub 安装 GIMP 。

备份配置：

```
cp -r ～/.config/GIMP/3.0 ～/GIMP-3.0-backup
```

安装步骤：

1.  1\. 确认已经安装 GIMP 3.0 或更新版本
2.  2\. 打开一次 GIMP，然后关闭
3.  3\. 下载 Linux 版本压缩包

```
https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP-linux.zip
```

1.  4\. 把压缩包解压到用户主目录 `～`
2.  5\. 这会把文件放到 `～/.config` 和 `～/.local` 这两个隐藏目录里
3.  6\. 文件管理器里看不到隐藏目录时，按 `Ctrl + H`
4.  7\. 如果提示已有文件，选择替换
5.  8\. 打开 GIMP

如果你不是用 Flatpak 装的 GIMP，大多数发行版的配置目录同样在：

```
～/.config/GIMP/3.0
```

关键还是版本要对，GIMP 要先启动过一次。

## 怎么卸载

PhotoGIMP 的卸载很简单：删掉 GIMP 配置目录，再打开 GIMP，它会重新生成默认配置。

Linux：

```
rm -rf ～/.config/GIMP/3.0
```

如果要恢复备份：

```
cp -r ～/GIMP-3.0-backup ～/.config/GIMP/3.0
```

Windows：

```
Windows + R → 输入 %APPDATA%\GIMP → 删除 3.0 文件夹
```

macOS：

```
Finder → Cmd + Shift + G → ～/Library/Application Support/GIMP → 删除 3.0 文件夹
```

如果提前做了备份，把备份的 `3.0` 文件夹放回去就行。

## 常见问题

### 装完没变化

通常是路径放错了。

Windows 要放在：

```
%APPDATA%\GIMP
```

Linux 要确认 `.config` 和 `.local` 在用户主目录下。

macOS 要放在：

```
～/Library/Application Support/GIMP
```

还要确认复制文件前已经关闭 GIMP 。 GIMP 没关时，退出时可能会把刚复制进去的配置覆盖掉。

### 打开 GIMP 报错

先检查版本。 PhotoGIMP 3 面向 GIMP 3.0+。如果你还在用 GIMP 2.x，建议升级 GIMP 。

也可以先删除配置目录，让 GIMP 重新生成默认配置，再按步骤重装 PhotoGIMP 。

### 会不会删掉自己的画笔、字体、插件

官方 FAQ 里说，PhotoGIMP 主要替换快捷键、布局、偏好设置等配置，不会删除个人画笔、字体、渐变和插件。

不过安装前仍然建议备份。修图软件一旦长期使用，配置里往往有很多个人习惯，备份能省掉很多麻烦。

### 快捷键还能自己改吗

可以。 PhotoGIMP 只是给你一个接近 Photoshop 的起点。装完以后，仍然可以在 GIMP 里进入：

```
Edit → Keyboard Shortcuts
```

继续改成自己的习惯。

## 使用建议

如果你想把 PhotoGIMP 当 Photoshop 平替，建议先做三件事。

第一，拿一张旧图跑一遍常用动作：裁切、调色、抠图、加文字、导出。别直接拿正式项目试。

第二，把常用快捷键试一遍，比如移动、画笔、橡皮、裁切、撤销、保存、导出。 PhotoGIMP 的价值就在这些手感上。

第三，确认 PSD 兼容性。 GIMP 可以打开不少 PSD 文件，但复杂图层、智能对象、特殊效果不一定完全一致。商业项目里，PSD 交付要求越严格，越要提前测试。

## 这东西值不值得装

如果你离不开 Adobe 生态，PhotoGIMP 替不了 Photoshop 。

如果你只是需要一个本机免费修图工具，又想保留 Photoshop 的界面习惯和快捷键，PhotoGIMP 很值得试。

它最好的地方是撤退成本低：备份配置、复制文件、试一下。不合适就删掉配置文件，GIMP 会回到默认状态。

对普通人来说，这比“每年为偶尔修几张图付订阅费”现实多了。

> 来源链接:
> 
> -   • https://github.com/Diolinux/PhotoGIMP
> -   • https://github.com/Diolinux/PhotoGIMP/releases/tag/3.0
> -   • https://www.gimp.org/downloads/

---

内容效果不满意？[点此反馈](https://feedback.notebooksyncer.com/feedback/099e6463_1786947560780?u=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzcwNTE3NzI0OA%3D%3D%26mid%3D2247487131%26idx%3D1%26sn%3D3f6c950b3ea3e923023c0be0587b6b86%26chksm%3Df55b58f48d55532e6ebb2f333380688b694b692121dc76bbcdc1e0de24fceae25224f71fec48%26mpshare%3D1%26scene%3D1%26srcid%3D0817A22FHX1ZcrewMviAq4ta%26sharer_shareinfo%3Dc6b4c9838fb57f345dee315bf1c3800a%26sharer_shareinfo_first%3Dc6b4c9838fb57f345dee315bf1c3800a%23rd&s=obsidian)