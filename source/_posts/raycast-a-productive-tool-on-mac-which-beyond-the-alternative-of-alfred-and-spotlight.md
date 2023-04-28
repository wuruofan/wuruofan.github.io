---

title: 🌈效率工具｜MacOS下好用的快捷启动器Raycast，Alfred再见👋
date: 2023-04-28 12:50:00
index_img: https://raw.githubusercontent.com/wuruofan/image_repo/main/image/raycast-introduction-on-official-website.png
banner_img: https://raw.githubusercontent.com/wuruofan/image_repo/main/image/raycast-introduction-on-official-website.png
categories:
- 软件工具
tags:
- MacOS
- 效率工具

---

![官网简介](https://raw.githubusercontent.com/wuruofan/image_repo/main/image/raycast-introduction-on-official-website.png)

## Intro

***⚠️⚠️ 本文多图预警！⚠️⚠️***

我个人一直在用免费版的Alfred，就我个人而言，大部分使用场景免费版已经足够了，但是有些快捷查词典翻译的需求，却必须Powerpack才可以。

这两天找到了一款非常好用的软件——Raycast，完全解决我的痛点，赶紧和大家分享下！


## Raycast简介

“Raycast”直译过来是“光线投射”的意思，[官网](https://www.raycast.com/)上对自己的介绍如下：

> Raycast is a blazingly fast, totally extendable launcher. It lets you complete tasks, calculate, share common links, and much more.
> ⇒ Raycast 是一个极快、可扩展的启动器。它让你能够完成任务、计算、共享常用链接等等。

使用下来，Raycast设计的思路和Alfred类似，也是命令式操作，都是希望手指不用离开键盘就可以完成大部分操作。


### UI 界面

Raycat本身设计的很简洁，默认快捷键“Option+空格键”呼出界面。UI风格和系统自带的Spotlight（聚焦搜索）很像，但是默认界面会比Spotlight下面多出几排信息来。

![默认UI](https://raw.githubusercontent.com/wuruofan/image_repo/main/image/raycast-default-ui.png)

如上图，下面主要两个部分：

- 一部分是**Walkthrough**，也就是“新手教程”，按照底部的快捷键提示可以“回车”进入，或者“Cmd+K”标记为已完成。这部分“新手任务”完成了，下次快捷键呼出就会消失。
- 另一部分是**Suggestion**，也就是“推荐”，按照你之前使用的频率进行推荐**命令**。

当然，如果不喜欢下面这部分推荐命令，可以在设置里关闭，在Window Mode项，选择Compact（紧凑的）即可。

![UI设置项](https://raw.githubusercontent.com/wuruofan/image_repo/main/image/raycast-ui-settings.png)

效果如下：

![紧凑模式UI](https://raw.githubusercontent.com/wuruofan/image_repo/main/image/raycast-compact-ui.png)

其中，Walkthrough在新手任务做完也会消失。假如你收藏了一些命令，就会显示在输入框的最右侧，支持快捷键`Cmd+1`、`Cmd+2`等，进行访问。

⚠️ 目前，Raycast还没有中文界面，但是界面英文都比较简单。实际使用过程中，输入**拼音**的时候是可以顺利找到本机的相关应用的！

### Walkthrough 新手任务

![Walkthrough](https://raw.githubusercontent.com/wuruofan/image_repo/main/image/raycast-walkthrough-tasks.png)

## 基础功能

通常情况就是快捷键呼出界面，直接输入你想要启动的程序、你想执行的命令即可，包括设置里的一些设置项，如WiFi、Bluetooth，也可以直接搜索的。

![应用支持拼音搜索](https://raw.githubusercontent.com/wuruofan/image_repo/main/image/raycast-searching-app-in-pinyin.png)

⚠️注意：在搜索系统设置项的时候，这里仅支持英文命令，具体查看设置里对应的分类。

### Actions 更多动作

Raycast所有的命令都支持`Cmd+K`查看更多动作。

![更多动作](https://raw.githubusercontent.com/wuruofan/image_repo/main/image/raycast-command-actions.png)

长按`Cmd`键会出现1、2、3、4快捷键显示，和Alfred一样，按下`Cmd+1/2/3/…`就可以直接选择第1/2/3/…个候选项。

⚠️ **注意，Actions里展开时提示的这些快捷键，在不展示的时候是可以直接使用的！** 因此，记住一些常用快捷键，是不需要`Cmd+K`多一步操作的，非常方便！

### **Quicklinks** 快捷链接

可以实现一个快速的网页访问功能，通过自定义快捷链接，可以迅速的将输入的文字，替换到配置的链接中，打开指定应用进行访问。

官网给了一个比较复杂的例子，谷歌翻译，支持选择语言、目标语言、文字，`{}`中的是占位提示符。

```
https://translate.google.com/?sl={source language:auto}&tl={target language}&text={word}&op=translate
```

![官网Quicklinks示例](https://raw.githubusercontent.com/wuruofan/image_repo/main/image/raycast-official-quicklinks-example.png)

另外，Quicklinks还支持自动使用当前选中的文字作为参数传入，这样可以再次提速。

![Quicklinks设置读取当前选中文字](https://raw.githubusercontent.com/wuruofan/image_repo/main/image/raycast-quicklinks-settings.png)

### Reminders 提醒事项

Raycast支持系统的“提醒事项”应用，可以查看和创建提醒事项，标记任务已完成，甚至都不用打开应用。

![创建提醒事项](https://raw.githubusercontent.com/wuruofan/image_repo/main/image/raycast-create-a-reminder.png)

### Calculator 计算器

说是计算器，其实不止是计算器，包含了各种转换的功能，比如国外的时间、几周后的周三是几号啊、1米等于多少英尺啊之类的。

![计算器转换货币](https://raw.githubusercontent.com/wuruofan/image_repo/main/image/raycast-calculator-convert.png)

这个功能不需要命令，直接在主界面输入要计算的内容，或者英文描述转换时间之类的短语：如“time in tokyo”。

另外，计算结果还可以直接作为其他命令的输入，快速使用。

### File Search 文件搜索

支持搜索电脑上的文件，需要授予权限，默认命令为`File Search`，直接输入`fs`就行，需要按回车进入下一个页面搜索，esc返回。

![文件搜索](https://raw.githubusercontent.com/wuruofan/image_repo/main/image/raycast-file-search.png)

### Define Word 词典

这个其实是系统默认的词典，但是在命令里给了`Define Word`，可以快速查词。

### Floating Notes 浮动笔记

默认命令为`Floating Notes`，显示在窗口最顶层，支持改变主题，分享到备忘录、提醒事项。

功能比较简单，颜值在线，临时做一个笔记还算凑合，就不截图了。

## 杀手功能

“杀手功能”是我自己划分的，是我觉得非常好用的功能。

### Window Management 窗口管理器

支持快速调整窗口大小、分屏、2/3、3/4分屏等等，默认命令为`Window Management`，`wm`就行。

![窗口管理](https://raw.githubusercontent.com/wuruofan/image_repo/main/image/raycast-window-manager.png)

这个功能基本就可以代替`Magnet`类似软件了，而Alfred本身是不具备的。

### Clipboard History 剪切板历史

默认命令为`Clipboard History`，这里会展示复制过的图片和文字，都支持**预览**，同时支持**输入关键字过滤**（filter**）**，支持**固定**（pin），直接回车键粘贴当前选中项到当前窗口，`Cmd+数字`可以粘贴对应第几个选项。

![剪切板历史](https://raw.githubusercontent.com/wuruofan/image_repo/main/image/raycast-clipboard-history.png)

🎉 特别喜欢的一点是，Raycast**会自动识别图片中的文字**，这样输入文字就可以过滤图片了！！

Alfred也有剪切板功能，但是似乎不能识别图片中的文字，现在已经完全代替我之前用的Clipy软件了。

类似，还有Snippets（片段）功能，通常用于文字替换，我用的不多，系统其实也自带一个，和剪切板功能类似，就不做介绍了。

### Switch Window 切换窗口

属于**Navigation**（导航）的子功能，支持**关键字过滤当前打开的所有窗口**，比默认的`Cmd+Tab`或者`Alt-Tab`软件一个个找窗口要高效很多！

![切换窗口](https://raw.githubusercontent.com/wuruofan/image_repo/main/image/raycast-switch-window.png)

这个功能Alfred也是不具备的！

### Search Menu Items 搜索菜单项

也属于**Navigation**（导航）的子功能，支持**关键字过滤当前应用菜单栏里的所有项**。

![搜索菜单项](https://raw.githubusercontent.com/wuruofan/image_repo/main/image/raycast-search-menu-item.png)

其实这个功能MacOS系统默认也提供了，在`Help`菜单项里可以搜索，默认的快捷键是`Cmd+Shift+/`，但是估计绝大部分人都不知道，或者记不住。

### Alias & Hotkey 别名 & 快捷键

这个功能我认为才是绝对的王牌🃏🃏，提效一大截！直接起飞！

![别名/快捷键设置](https://raw.githubusercontent.com/wuruofan/image_repo/main/image/raycast-alias-hotkey-settings.png)

这么多命令，要输入这么多字符其实很难搞，但是Raycast很方便的支持了Alias（别名）和全局快捷键。

这里我设置了剪切板快捷键是`Option+C`，这样直接按键就可以进入搜索剪切板的界面，一步到位！

关于别名，词典是`dw`，文件搜索是`f`，切换窗口是`w`，搜索菜单是`m`，还是需要快捷键呼出Raycast界面，这时输入`命令别名+空格键`或者`命令别名+Tab键`即可进入对应功能界面！

在使用的过程中不是方便一点点，因为正常情况是需要点击回车才可以的，不够流畅，简短的别名+空格/TAB，畅享丝滑！

## 扩展功能

Raycast支持插件和自定义脚本。

程序内置了插件商店，快捷键是`Store`。

插件还没怎么研究明白，看介绍是可以实现Github合并、拉取，Jira等等相关操作，有些过于专业化了，不是所有人用的到。

这里推荐一个词典插件`EasyDict`，很好用，远胜于系统词典，支持各大在线翻译接口同时查询，单词朗读。

![EasyDict查词](https://raw.githubusercontent.com/wuruofan/image_repo/main/image/raycast-plugin-easydict.png)

关于自定义脚本，一样还没研究，看介绍支持各类语言，比如Bash、Apple Script、Swift、Python、Ruby、Node.js等等，等我研究明白了再说。

## 定价

目前，个人和基础团队功能都是免费的，功能都没啥区别，只不过团队功能多了，可以共享的Quicklinks、Snippets配置，以及可以建立私有插件商店。

![各版本定价](https://raw.githubusercontent.com/wuruofan/image_repo/main/image/raycast-pricing.png)

## End

总的来说，除了没有本地化，一切都很满足我个人的需求，看看以后有没有机会能帮忙本地化一下。

最后，Notion AI总结如下：

> Raycast是一款MacOS下的快捷启动器，支持快速启动程序、执行命令、搜索系统设置、文件搜索、窗口管理、剪切板历史、词典、快捷链接、提醒事项等功能。支持别名和全局快捷键，还有插件和自定义脚本功能。个人和基础团队功能都是免费的。


最后的最后，祝大家五一快乐！🤗

<p>

以上，欢迎关注公众号“**小黑杂说**”。

![小黑杂说](https://raw.githubusercontent.com/wuruofan/wuruofan.github.io/master/img/qr-wechat-large.png)

