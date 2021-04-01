---
title: MacOS/Linux程序员Win10平台生存指北
date: 2021-04-01 17:46:05
categories:
  - 软件工具
tags:
  - 生产力工具
  - Win10
  - WSL
  - 使用指南
  - 开发工具
---

## 前言

小黑用Linux系统可以追溯到上学时期某一次玩DOTA时候XP系统蓝屏了，一生气就把双系统的XP盘格式化了，只保留了Ubuntu系统，从那时候开始学会使用vim，由于工作内容基本是C/C++，所以之后基本开发都是Ubuntu+Vim为主了。

上班后虽说公司配的是古老的winXP电脑，但是好在有一台带界面的Ubuntu服务器可以供我使用，基本环境也是xlaunch+Ubuntu+Vim。

自己的电脑是Mac，说白了也是Unix系统，出差在外也是Vim为主，涉及Windows版本就虚拟机

去年换了工作后，公司配的依旧是Windows本，不过是Win10了，依旧很难使用。

## 命令行与WSL

现在回过头来看，就我个人而言，Windows平台开发效率低的原因最主要的一个就是命令行孱弱。原来的`cmd`工具和`bat`批处理脚本几乎无法使用，想使用Linux shell，只能选择`MinGW`或者`msys`，痛苦且不优雅。

好在近些年的微软变得越来越开放，发布了适用于Linux的Windows子系统（Windows Subsystem for Linux，简称**WSL**）。

这对我来说简直棒极了，完全解决了我的痛点。

**WSL**不同于模拟Linux命令行，而是原生系统内置的子系统，在内核级别完成Linux系统接口的转换，有点像半虚拟化。（2020下半年发布的`WSL2`有点像是全虚拟化。）

我们可以看一下`WSL`和`WSL2`之间的区别，官网给出的比较如下图：

![WSL1与WSL2功能对比](https://i.loli.net/2021/03/17/JDBljOc2tYkgZeu.png)

WSL2以虚拟机的形式运行完整的Linux内核，也就是说Windows现在可以享受到最新Linux发行版了。

**跨 OS 文件系统的性能**说的是现在不推荐跨操作系统去操作文件，将文件存储在 WSL 文件系统，这样可以获得更快的性能速度。在Windows的文件管理器的地址栏输入`\\wsl$\Ubuntu-20.04\home\`，即可以以网络连接的形式访问WSL的文件系统。

## `WSL`安装与升级

**WSL**整体的安装过程都比较简单，步骤如下：

### 1 开启Windows功能中相关特性

去“控制面板” -  “程序” - “程序和功能” - “启用或关闭Windows功能”中开启“**适用于 Linux 的 Windows 子系统**”，如果需要使用WSL2，还要勾选“**虚拟机平台**”特性。

![启用WSL所需Windows功能](https://i.loli.net/2021/03/18/VyPeo1XvGwkpME8.png)

另外，WSL2要求Windows10版本在2004或更高版本以上。

### 2. 安装WSL2 Linux内核更新包

下载最新[适用于 x64 计算机的 WSL2 Linux 内核更新包](https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi)并安装。

如果时ARM64版本的Windows10，需要下载[ARM64版本内核更新包](https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_arm64.msi)。

### 3. 设置默认WSL版本

在cmd命令行执行`wsl --set-default-version 2`，以后安装的Linux发行版就是WSL2了。

### 4. 下载并安装Linux发行版

去[Microsoft Store](https://aka.ms/wslstore)市场，选择想安装的Linux版本，点击获取，自动安装就可以啦。

![微软市场WSL支持的发行版](https://i.loli.net/2021/03/18/syDrY5ojizauOXS.png)

目前商店里支持的Linux有不少，小黑选择的是Ubuntu-20.04 LTS版本。

安装的过程需要设置账户和密码，常规操作了。

### 5. 更新已安装的WSL1到WSL2

上面流程使用与第一次安装WSL2，如果你和我一样已经安装过WSL1了，需要做的步骤大概就可以简化如下：

1. 开启“虚拟机平台”。
2. 安装“WSL2 Linux内核更新包”。
3. 设置默认安装版本为WSL2。
4. 设置已安装WSL1版本的Linux发行版为WSL2。

在升级WSL之前，需要查看要升级的Linux发行版名称，使用`wsl --list --verbose`查看，缩写命令是`wsl -l -v`。该命令会列出当前已安装所有Linux发行版本的名称、状态、版本号。

![WSL状态](https://i.loli.net/2021/03/18/Yzqm3KZiMk9XQ6l.png)

然后使用`wsl --set-version <distribution name> <versionNumber>`，比如`wsl --set-version Ubuntu-20.04 2`。

这个转换耗时并不是像官方文档说的那样需要花费几分钟，而是和你原来安装WSL系统大小有关，而且转换的时候需要占用额外的C盘空间，我的WSL转换时可以肉眼看到C盘占用空间的增加，大约13GB左右，在转换完成后释放掉。
因此，转换WSL之前最好确保C盘有足够的空间。

## Windows Terminal

Windows Terminal简单来说就是一个命令行程序的终端软件，可以运行/加载命令行工具、 PowerShell 和WSL命令行），它的主要功能包括多个选项卡、窗格、Unicode 和 UTF-8 字符支持、GPU 加速文本呈现引擎，支持各种自定义配置。

![Windows Terminal界面](https://i.loli.net/2021/03/26/D6SQHk1sXd58vTw.png)

上面图片是官方介绍给出的图片，具体如何配置可以参考[官方文档](https://docs.microsoft.com/zh-cn/windows/terminal/)，以及少数派的文章：[新生代 Windows 终端：Windows Terminal 的全面自定义](https://sspai.com/post/59380)。

对于我个人来说，需要解决默认启用WSL Ubuntu的终端即可。`Ctrl + ,`快捷键打开json设置文件，修改`defaultProfile`对应键值，为`profiles` - `list`列表中你想要启用终端的`guid`值即可。

### zsh插件加载失败

`zsh`、`Oh-my-zsh` 、`Powerline字体`当然是必不可少的终端环境了，比`bash`更强大也更美观，需要注意的是zsh的一些插件可能`apt-get`直接安装会加载不成功。

需要卸载apt安装的插件，然后通过git clone安装。

```bash
git clone https://github.com/zsh-users/zsh-autosuggestions ~/.oh-my-zsh/custom/plugins/zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ~/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting
```

### 右键在当前目录打开Windows Terminal

Windows Terminal安装完成后应该会在文件管理器右键添加`Open in Windows Terminal`菜单，旧版本有点问题，右键点击该菜单只会打开用户目录，这时候需要手动删除配置中`profiles` 的`startingDirectory`值设置成`null`，原配置应该是`"%USERPROFILE%"`。

如果已经将默认profile设置成WSL，那么现在已经可以在文件管理器右键打开Linux命令行了。

## 开发工具

### nvim

`NeoVim`命令行版本可用，这就可以解决大部分问题了。

### Visual Studio Code

VSCode的`Remote - WSL`插件支持在WSL环境中打开工程目录，插件会把WSL认为是一台远程机器，然后尝试连接，并在WSL环境下打开工程。

![Remote-WSL插件](https://i.loli.net/2021/03/29/ptQBOmEUkaz2XKv.png)

一旦使用WSL打开，那么编译环境、执行环境、终端都会切换到WSL，VSCode加载的配置文件、插件等都是安装在WSL中的。

![Remote-WSL状态](https://i.loli.net/2021/03/29/XQqhTdNxSrGsvkL.png)

打开后界面左下角会有一个蓝色标注，显示当前是本地环境打开还是用WSL打开；点击即可切换打开方式。

![Remote-WSL指令](https://i.loli.net/2021/03/29/IN4mJPEh7cqY9v8.png)

## WSL运行exe

WSL命令行里其实是可以运行Windows可执行程序（`exe`）文件的，而且Windows系统的环境变量`PATH`也会默认被添加到WSL中。

因此，我们可以在WSL的zsh里直接执行`explorer.exe .`使用文件浏览器打开当前目录。

## WSL与adb

这是调试过程中遇到最坑的地方了。

首先，不要使用`apt-get`安装的adb工具，若已经安装，需要先卸载。从Android开发者官网下载[SDK Platform Tools](https://developer.android.com/studio/releases/platform-tools)，Windows版本和Linux版本都需要下载。

WSL1下的adb使用简单些，只需要Windows和Linux中adb版本一致即可，WSL中adb遇到问题需要在命令行提示符cmd中`adb kill-server`和`adb start-server`即可恢复。

WSL2下的adb就坑一些，保持相同版本号已经不行了，可能和使用了虚拟化平台后，网络连接变化有关，虚拟机中的网卡和真实网卡桥接起来了。不像是原WSL1的系统调用类似半虚拟化，adb直接可以访问到Windows中的adb server，现在必须手动设置Windows中adb服务端和WSL中adb客户端连接了。

### 方案1：alias别名

可以使用`alias`将WSL2中的adb指向Windows中的adb.exe解决问题。

在你使用的`.bashrc`或者`.zshrc`中添加如下设置：

```bash
if [[ ! -z $WSL_DISTRO_NAME ]];then
    alias adb='adb.exe'
    alias fastboot='fastboot.exe'
    alias aapt='aapt.exe'
fi
```

**优点**是配置简单，**缺点**是强迫症要死，而且**无法使用高版本adb shell的补全功能**，比如当前电脑连接了两个Android手机，原生adb输入`adb -s`之后点击`TAB`按键就会列出当前连接设备的id，或者在`adb shell ls /sdcard/`之后点击`TAB`，就会列出该目录下所有文件。

### 方案2：设置adb连接

首先，设置WSL2中adb使用远程服务器的地址。

在你使用的`.bashrc`或`.zshrc`中添加如下设置：

```bash
export WSL_HOST_IP="$(tail -1 /etc/resolv.conf | cut -d' ' -f2)" # 按照Microsoft给出的方法获取宿主机的IP地址，
export ADB_SERVER_SOCKET=tcp:$WSL_HOST_IP:5037 # 设置adb远程服务器地址
```

然后，需要在Windows命令行终端cmd中重新启用adb server。

执行如下操作：

```
adb.exe kill-server
adb.exe -a -P 5037 nodaemon server
```

之后，WSL2中的adb就可以正常运行了！现在还有一点不好的是，cmd还不能关闭，因为adb server还在运行。

解决方案是建立一个vbs脚本并加入开机启动，或者每次手动双击运行。

vbs脚本如下，其中具体adb的路径和个人路径有关，需要自行修改。：

```
CreateObject("WScript.Shell").Run "%USERPROFILE%\AppData\Local\Android\Sdk\platform-tools\adb.exe kill-server", 0, True
CreateObject("WScript.Shell").Run "%USERPROFILE%\AppData\Local\Android\Sdk\platform-tools\adb.exe -a -P 5037 nodaemon server", 0, True
```

我的脚本名称为`start_adb.vbs`，放到系统环境变量所在路径下，使用`Win-R`后输入脚本名称进行运行。

![运行vbs脚本](https://i.loli.net/2021/04/01/wvF2UdahBZV3n8s.png)

## 其他小工具

### PowerToys：小工具合集

这是微软自己出品的小工具集合，包含窗口管理器、颜色选择、批量重命名、快速启动等工具。

![PowerToys设置界面](https://i.loli.net/2021/03/31/6W8ASKJBjY5Twl7.png)

窗口管理器（FancyZones）功能可以自定义各程序窗口的布局。

PowerToys Run也就是快速启动，勉强称为MacOS下`Alfred`的极简版吧，再简陋点还可以用`Win+S`使用Win10自己的搜索功能。

PowerToys Run可以通过快捷键`Win+Space`呼出一个对话框，执行各种快速操作，如启动应用、搜索文件、访问网址、切换窗口等，可惜不支持更多的自定义插件。

![PowerToys Run输入chrome](https://i.loli.net/2021/03/31/PcLSnYuCZbDelhr.png![image-20210331180118973](https://i.loli.net/2021/03/31/saXFRx39pQj4kgT.png)

### uTools：快速启动

也是MacOS下`Alfred`的替代品。

用uTools官方介绍来说，“uTools是一款极简、插件化、跨平台的现代桌面软件，只有一个简单的输入框，你可以在任何时候通过全局快捷键（默认`Alt+Space`）快速打开它”。

其实Windows平台下Wox可能大家推荐的多一些，但是个人觉得uTools的界面更好看，插件中心更易用一些。

![uTools插件中心界面](https://i.loli.net/2021/03/31/VrsB7Jd6Lc3UWeO.png)

uTools的输入框支持拼音、中文联想，激活插件，执行功能。

![uTools翻译插件使用界面](https://i.loli.net/2021/03/31/TG2oWcvKJkDlmFM.png)

总的来说，uTools还是不错的，但是发现PowerToys Run的切换当前运行的窗口功能似乎uTools并不支持。

更多扩展阅读：[uTools | 时隔一年，uTools 这位 Spotlight 新秀现在变得怎么样了?](https://sspai.com/post/56739)

### QuickLook：文件预览

MacOS以及最新Ubuntu相同已经支持选中一个文件后，点击空格即可预览文件内容了，Windows还需要安装QuickLook。

QuickLook支持各种文件类型的插件，Markdown和Office文档都无压力。

![QuickLook预览Markdown文件](https://i.loli.net/2021/03/31/JuXiYV3wWqBm8t6.png)

### CLCL：多粘贴板

Win10其实自己默认支持多剪切板，设置里搜索剪贴板即可，使用快捷键`Win+V`打开。

CLCL是一个比较久远的程序了，支持保存一些自定义的短语，设置界面`Template`右键`New Item`即可。

![CLCL设置界面](https://i.loli.net/2021/03/31/FedtONEC2ZvAohV.png)

### Snipaste：截图工具

Win10自带截图的快捷键是`Win-Shift-S`，支持窗口、全屏、自定义范围等截图模式。

但是Snipaste更强大一些，支持将刚截的图再贴回屏幕上，或者固定在屏幕上。这个功能在对比文字、图片细节时很好用。

![Snipaste固定截图到屏幕](https://i.loli.net/2021/03/31/JEqf1nOpNZWe6dK.png)

### EasyWindowSwitcher：同应用窗口切换

Win10现在的窗口切换器已经支持多个虚拟桌面，也支持类似MacOS的expose窗口展示的功能。但是，同一个应用多个窗口间的切换居然不支持。在Ubuntu和MacOS使用`` Alt+` ``即可切换同一个应用内的多个窗口。还好已经有人实现了这个功能，安装EasyWindowSwitcher接可，这个软件功能很单纯，就这一个功能，开机之后也找不到它，省心。

### Velocity：代码手册阅读

MacOS下有一个神器叫做`dash`，整合了各种语言的参考手册，可以下载离线使用。Velocity就是Windows版的dash，界面还算ok，支持dash的文档源。

![Velocity界面](https://i.loli.net/2021/03/31/2vc7KFy8hqMePTx.png)

在输入框中输入语言名称后，再输入`:`，就可以指定搜索该语言的文档。

该软件可以免费使用，但是每隔一段时间会弹出提示窗口，可以技术上去除。

## 最后

大概就是以上这些，已经足够我日常Windows平台的开发工作了。

