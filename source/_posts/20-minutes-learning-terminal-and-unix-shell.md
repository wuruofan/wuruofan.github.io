---

title: 20分钟入门｜Terminal与Unix Shell——程序员应该知道的那些事儿

date: 2022-03-21 20:00:00

index_img: https://raw.githubusercontent.com/wuruofan/image_repo/main/img/unix-logo.jpeg

categories:

  - 技术总结

tags:

  - Linux
  - MacOS
  - Unix
  - Terminal
  - Shell

---


![Unix](https://raw.githubusercontent.com/wuruofan/image_repo/main/img/unix-logo.jpeg)



## 写在前面

这是一篇一直想写的东西，在上一份工作的时候给新员工培训，我就发现不止新入职的员工，很多多年工作经验的同事也对Unix系统和Shell知之甚少，然而**这些知识可以更好点帮你认识你所使用的系统原理、语言设计思想、提高工作效率。**



**整篇文章包含两部分，这是下半部分**，主要介绍**什么是Terminal**、**什么是Shell**、以及**一些好用的Shell命令**和**Terminal快捷键**。

全文1.2w字，大部分都是我个人这些年使用类Unix系统的理解和总结，适合开发、测试同学阅读。

> 上半部分参见：[20分钟入门｜Unix系统与设计哲学——程序员应该知道的那些事儿 ](https://wuruofan.com/2022/03/09/20-minutes-learning-unix-system-and-its-philosophy/)

<p>

阅读完上下整篇文章，你会：

- ✅ 了解Unix系统特性与设计思想，了解Unix系统目录结构，以及各个目录功能。
- ✅ 了解什么是终端和Shell，以及关于环境变量。
- ✅ 获得一些实用的居家旅行、高效工作的 ~~*装X技巧*~~ Shell和终端使用技巧。



## 什么是Terminal？

维基百科的解释：**终端其实就是一种输入输出设备**，相对于计算机主机而言属于外设，本身并不提供运算处理功能。

![终端与中心主机](https://raw.githubusercontent.com/wuruofan/image_repo/34d4ed9f54bf5fbb60e9104e6b57e9a6342059a3/img/terminal-network-workgroup.png)

Unix系统的设计初衷便是多用户、多任务的，因此才会产生了多个终端同时访问一台计算机的情况。

这个概念和今天的云主机很像，用户不需要拥有一台完整的主机，只需要一套输入（键盘鼠标）输出（显示器）设备即可，前提是网络通畅。腾讯在搞的云游戏主机也是这种。



我个人的理解，这个单词的词根是**term**，“界限，终点”的意思，**对于“终端”来说，起点是计算机，终点是用户，用户所使用的和计算机交互的设备便是终端。**在通讯行业，我们的手机也是个人终端，起点是中心网络，终点也是用户。



通讯是双向的，从用户到计算机的连接，**用户与计算机沟通的载体便是Shell。**





## 什么是Shell？



维基百科的定义：**Shell**（也称为**壳层**）在计算机科学中指**“为用户提供用户界面”的软件**，通常指的是命令行界面的解析器。

Shell的直译是“壳”，就是只包裹在内核外层的部分，作为和用户之间交互的接口暴露的部分；广义上讲，Shell包括了命令行界面（CLI，**C**ommand-**L**ine **I**nterface）和图形交互界面（GUI，**G**raphical **U**ser **I**nterface）。

> 参考资料：[维基百科 - 壳层](https://zh.wikipedia.org/wiki/%E6%AE%BC%E5%B1%A4)



我个人的理解：Shell程序主要用于管理你与操作系统之间的交互：**等待你输入操作，并向操作系统解释你的输入；同时处理各种各样的操作系统的输出结果，并展示给你。**

除此之外，**Shell也是控制系统的脚本语言，提供了很简单的控制语句。**在Windows系统，大部分用户从来都不会使用到shell，然而在Unix系统中，shell仍然控制着系统启动、各种软件的运行。





我找了两张图来说明Shell在Unix系统中的位置。

![Section 1.2. UNIX Architecture | Advanced Programming in the UNIX  Environment, Second Edition (Addison-Wesley Professional Computing Series)](https://raw.githubusercontent.com/wuruofan/image_repo/34d4ed9f54bf5fbb60e9104e6b57e9a6342059a3/img/UNIX%20Architecture.gif)



第一张是《Unix高级编程》一书的插图，这本书非常好，有兴趣的同学可以作为工具书翻阅一下。

这张图绘制的很好，我们可以看到在system calls（系统调用）的外层并不是一个完整的圈层，就意味着shell不是唯一和内核交互的通道，应用程序可以直接和内核通过系统调用进行调用，这个调用的过程通常被称为系统陷入（trap），用户态程序通过trap指令切换到内核中进行执行。



第二张图是一张地球地质结构的图，地球大致分为三层，从外往内是地壳、地幔、地核。

我们日常生活接触的山川、湖泊、森林、平原都属于地壳，是我们和地球“交互”进而生存的环境，当然也存在火山、地震引起的裂缝这样不寻常的“接口”。

![地幔- 维基百科，自由的百科全书](https://raw.githubusercontent.com/wuruofan/image_repo/25f3b4d04aae9525ba61a9da8da71c2eb791e378/img/earth-crust-cutaway.png)






### 常用Shell程序

我们可以通过`cat /etc/shells`，查看当前系统支持的shell程序。

Unix历史第一个shell是由其作者实现的，被称作**Thompson Shell**，缩写是`sh`，支持重定向`>`、`<`和流水线`|`命令。

后来被**Bourne Shell**同名替换了，缩写也是`sh`，但是扩展支持了管道功能。

这两个shell都是以作者的名字进行命名的。



#### bash 

bash的全称是**Bourne-Again Shell**，也是一个双关语（ born again），替换了之前的Bourne Shell，支持了更多的特性。

bash可以说是应用最广泛的Shell程序，是绝大部分Linux发行版的默认shell，MacOS Mojave及之前的版本的默认shell也是它。



#### zsh

zsh对Bourne shell做出了大量改进，同时加入了bash、ksh及tcsh的某些功能。macOS Catalina，默认Shell以zsh取代。

个人觉得zsh最直观的功能增强就是命令行补全功能，



个人感觉：**zsh总体上来说，比bash更“时髦”一些**，一个名为“Oh-My-Zsh”的社区，一直在维护、收集zsh可用的各类插件、主题配置，很多特性可以通过安装是“Oh-My-Zsh”扩展工具集，进行体验和使用。

zsh提供了一个`z`命令，输入`z <目录名称>`，便会跳转到你最经常使用的目录中。通常默认shell支持单击Tab键补全命令/文件的剩余字符，双击Tab键提示候选词列表，这个`z`本质上是基于历史输入记录的补全。

其实这个实现原理并不难，Unix系统`history`命令对于历史运行的命令都有记录，一个加权评分策略的设计与应用就可以让用户体验提升，这是值得我们反思的。

对于脚本，zsh还提供了更强大的自定义补全功能，交互上更友善。



> **扩展阅读**：
>
> 这里有一个意思的点，zsh是作者（Paul Falstad）在普林斯顿上学时开发的，zsh的命名来自于他的老师Zhong Shao（邵中）的名字，作者觉得这位邵中老师的shell用户名“zsh”很适合作为一个shell程序的名字。[The Z-Shell (ZSH) Lovers' Page](http://www.guckes.net/zsh/lover.html)
>
> 查了下资料，Zhong Shao, B.S., University of Science and Technology of China, 1988 M.A., Ph.D., Princeton University, 1991, 1994. Joined Yale Faculty 1994.。





### 什么是环境变量？

作为程序员，我们经常会遇到环境变量（Environment variable）这个词汇，不管是Windows还是Unix系统，我们遇到最多的场景就是，把xxx路径加入到$PATH环境变量中去。

环境变量，就是指**计算机配置的一些影响进程运行状态的变量值**。维基百科的原文是：An environment variable is a dynamic-named value that can affect the way running processes will behave on a computer.



简单举个例子帮助大家理解，“领导/老板”这就是个典型的环境变量，你我他代表着不同的进程，你、我、他的老板都是老板，但是未必是同一个老板，当然，工作部门的变更也会导致“老板”这个值的变更。



我们常见的`$PATH`、`$HOME`、`$TEMP`等等，这些变量的值是可变的，一个进程运行时会去查询当前运行环境中这些值是什么，然后在决定运行路径、查询路径或保存路径等。

在UNIX系统中，每个进程都有其各自的环境变量设置。缺省情况下, 当一个进程被创建时，除了创建过程中的明确更改外，它继承了其父进程的绝大部分环境设置（fork的原理）。



#### 环境变量存储在哪儿？

默认环境变量的值，通常保存在shell程序的配置文件里。

对于bash来说，系统默认的全局配置存储在`/etc/bashrc`，个人配置通常位于当前用户的Home目录中的`~/.bash_profile`、`~/.bashrc`配置文件中。

zsh与之类似，默认在`/etc/zprofile`、`/etc/zshrc`，个人配置在`~/.zshrc`中。



Shell程序启动时，会默认加载`/etc/`目录下对应shell程序的配置文件，然后再去加载HOME目录下的个人配置文件。



经常我们会看到网络上教你配置$PATH环境变量的文章，但凡让你用`修改`/etc`目录下配置文件的帖子，都可以立刻关闭了。

默认`/etc`下文件都是只读的，所有用户共享的一份数据，通常的做法是拷贝一份`/etc`下的配置文件到你的Home目录，在前面加上`.`变成隐藏文件。由于Unix系统会最后加载个人Home目录下的配置文件，后加载的同名配置会覆盖之前的变量定义。



#### 查看环境变量



通常使用`echo`命令查看一个环境变量，比如：`echo $PATH`，PATH是环境变量名称，$符号表示后面的字符串是变量名。

这个语法是不是和很多脚本语言一样？Unix对很多后期语言的设计产生了深远的影响。



我们可以看到shell输出的PATH环境变量值：

```
/Users/qihoo/devkits/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/pkg_uninstaller:/Users/qihoo/Library/Android/sdk/ndk/20.0.5594570:/Users/qihoo/Library/Android/sdk:/Library/Java/JavaVirtualMachines/jdk1.8.0_311.jdk/Contents/Home:/Users/qihoo/Library/Android/sdk/emulator:/Users/qihoo/Library/Android/sdk/platform-tools:/Users/qihoo/Library/Android/sdk/tools:/Users/qihoo/Library/Android/sdk/tools/bin:/Users/qihoo/Library/Android/sdk/build-tools/29.0.3:/Users/qihoo/Library/Android/sdk/ndk/20.0.5594570/toolchains/aarch64-linux-android-4.9/prebuilt/darwin-x86_64/bin
```

这个变量值的组成是一个一个的路径，然后使用`:`连接起来，本质上是一个路径列表。

系统执行命令时首先要查找命令，默认的查找顺序是

1. 当前环境变量中定义的`alias`别名，也就是用户自定义的一些名称。
2. 导出的函数方法：shell脚本语言支持定义方法。
3. 系统内建命令（built-in shell commands）。
4. PATH环境变量中定义的路径：这个路径列表会从左至右解析，找到便停止继续查找。

> 参考资料：[How does Unix search for executable files?](https://superuser.com/questions/238987/how-does-unix-search-for-executable-files)



我们可以用`which <command-name>`命令，查看当前该可执行程序所在路径。



#### 配置环境变量



通过`export PATH=<path>:$PATH`进行配置，其中PATH是系统环境变量，必须大写，$PATH表示取变量值。



```bash
# 定义了一个自定义环境变量ANDROID_SDK
export ANDROID_SDK=~/Library/Android/sdk
# 将ANDROID_SDK下的build-tools加入PATH
export PATH=$PATH:$ANDROID_SDK/build-tools/29.0.3
```



这里我先是定义了一个自定义环境变量ANDROID_SDK，然后将ANDROID_SDK下的build-tools加入PATH。

其中，`~`可以用另一个环境变量`$HOME`代替。



这里我们可以拆解一下上面的命令为两部分：

```bash
# 定义一个变量
ANDROID_SDK=~/Library/Android/sdk
# 导出成环境变量
export ANDROID_SDK
```



我们可以使用`export -p`命令列出所有环境变量。



**注意**：这段配置通常需要写入你当前使用shell的个人配置文件中去，否则不会生效，bash需要写入`~/.bashrc`，zsh则写入`~/.zshrc`。

**如果没有写入配置文件中去，仅仅是在shell中运行这两行也是可以的，只不过这两行配置的环境变量仅会对当前终端打开的shell窗口生效，重新打开一个shell窗口是不会起作用的。**



通常我们编辑完shell程序的个人配置文件，已经打开的窗口也是不会生效的，前面讲过了，在启动shell的过程才会去加载配置文件。这时，需要使用`source ~/.bashrc`命令**重新加载配置文件**，这个命令等价于`. ~/.bashrc`。



#### 为什么不把当前目录`.`加入环境变量？

在Windows下用过命令行的同学可能有疑问，为啥不把当前路径加入环境变量？Windows默认是可以直接运行当前目录下可执行程序的，而在Unix里必须使用`./<exec-name>`进行运行，shell会自动将`.`和`..`补全成当前路径和父路径，以绝对地址找到可执行程序，并运行之。



我们理论上是可以将`.`加入到环境变量中，但是会引入安全性问题。

在Unix系统的树形目录结构中，有些`/tmp`或者`/vars`等目录是所有用户都有权限进行访问的，假如有些恶意程序，在这些目录中保存了一个和常用命令同名的二进制恶意程序，如`ls`（ls并不是系统内建命令），但你不小心进入该目录，运行了ls，那么就会执行了那个恶意程序！







## 一些好用的Shell命令

### man

如果我只能推荐一个shell命令，那么这个命令一定是`man`。在Unix系统里，“有问题找男人（man）”。

**man**ual（手册）的缩写，Unix系统中绝大多数的可执行程序都有完善的文档和详细的例子。



遇到不记得用法或者参数的命令，第一个可以尝试在命令后面加上`--help`或者`-h`参数，这是Unix世界约定俗成、几乎通用的参数。你也可以在输入`-`之后，尝试两下TAB按键，shell程序也会列出参数和具体功能。



### ls

**l**i**s**t的缩写，列出当前指定目录/文件的信息。

```bash
ls -lh <file_path>
```



有一些有用的参数：

- `-l`：以列表的形式查看，会列出更多的属性
- `-a`：列出所有文件
- `-A`：列出所有文件，除去`.`和`..`
- `-h`：以人类可读方式列出文件大小，仅在和`-l`参数一起使用时生效

其中`file_path`可以是目录，也可以是文件，也支持包含`*`或者`?`的通配符。

比如，`ls haha*`，则会列出当前目录下所有以“haha”开头的文件。



### cd

**c**hange **d**irectory的缩写，之后通常跟上目录的绝对或者相对路径。

我们可以如下使用：

```bash
# 进入当前用户的Home目录
cd ~

# 进入上一个目录
cd -
```



> **TIPS**：
>
> 很多不常用命令行的同事在使用此命令时，总是会习惯`ls`以下，然后`cd`进入一个目录，然后再`ls`，如此反复。在我看来这就是Windows文件管理器操作方式的延续，这其实是很低效的。
>
> **更好的使用方式是输入`cd `双击TAB键，shell会提示可选的目录名称。**
>
> 这种使用方式的**另一个好处**就可以用上`cd -`命令了，快速高效的切换工作目录。



### pwd

**p**rint **w**orking **d**irectory的缩写，打印当前工作目录。



### alias

别名，通常用与缩写替代一个较长的路径。

与之相反的命令是`unalias`，另外可以直接输入`alias`查看当前定义的别名。



下面就是一些小技巧：

```bash
# 快速返回到父目录
alias ..='cd ..'
alias ...='cd ../../'

# 带颜色的ls，并显示目录／
alias ls='ls -Gp'
# 显示B/KB/MB大小
alias ll='ls -lh'
```



### echo

echo本意是“回声”，就是你说一句，shell给你回复一句相同的话。

通常使用的场景是用于输出日志、输出变量。比如，`echo $PATH`。



> **TIPS**：
>
> `echo`命令默认会在输出文字最后加上换行符`\n`，某些场景可以使用`-n`去除换行符。



### cat

concatenate的缩写，本意是“连接”，具体使用那几个字母我不确定。

常用于**以文本方式显示文件内容**，可以理解为一只小猫（cat）从老鼠洞里往里偷看，因为洞比较小，所以只能看到文本数据。

通常用法就是`cat <filename>`，查看文件内容。



### less/more

这两个命令很类似，其实都是提供一个分页器的功能。这两个命令的出现就是为了解决`cat`一个文件内容过长时、屏幕无法显示下的时候会被flush冲掉的问题。

使用方法类似：

```bash
less <filename>
more <filename>
```



使用之后默认只会展示一屏幕的信息，使用`j`/`k`快捷键进行上下滚动一行，使用`space`空格键进行翻页，按`q`退出，还有一些快捷键类似`vi`，暂时不介绍了。



### 打开文件/目录

很多同学在一开始使用shell的时候会遇到这样的问题：

想用shell提效，费了半天劲`cd`到指定目录，也`ls`找到指定文件了，但是却尴尬的发现不知道怎么打开文件/目录！



其实很简单，不同的操作系统都提供了类似的方法，使用用户默认程序打开：

- **open**：MacOS
- **xdg-open**：Linux
- **start**：Windows



例如：

```bash
# 用文件管理器打开当前目录
open . # MacOS
xdg-open . # Linux
start . # Windows
```



### 管道

英文是pipeline，在shell中使用`|`符合，其含义是将管道符号`|`前命令的输出信息作为管道符号`|`后命令的输入信息。

比如，可以在包含过多文件的目录如下使用：

```bash
ls -l | less
```



### 重定向输出

常用的重定向输出符号有`>`和`>>`，还有一些其他符号感兴趣可以自行搜索。

`>`符号可以将上一条命令的输出信息，重定向到一个文件。

`>>`符号可以将上一条命令的输出信息，重定向追加到一个文件的末尾。



例如：

```bash
adb logcat > log.txt

cat file1 file2 > file3 # 把两个文件的内容连接在一次输出到file3文件中
```



### find

查找文件命令，这个命令比较复杂，给出一种我常用的参数。

```bash
find <search_directory> -name <name_pattern> -type <d/f>
```

很简单，`search_directory`参数是要搜索的目录路径，绝对路径或者相对路径，如果想搜索当前路径传入`.`即可；`name_pattern`参数传入的可以是一个匹配符，支持正则表达式。

假如你想只搜索目录名称，那么额外加上`-type d`；只搜索文件，使用`-type f`即可。



例如：

```bash
# 仅搜索当前目录txt文件
find . -name "*.txt" -type f
```



### grep

搜索文件内容，**G**lobally search a **R**egular **E**xpression and **P**rint的缩写，常用的方法就是结合管道一起使用，所谓过滤输出。

通常需要和管道联合使用，比如，我们日常工作常用的：`adb logcat | grep "TAG"`。



`grep`命令用法也很复杂，这里给出常用的参数版本：

```bash
grep -e <search_patter> -A <line_num> -B <line_num>
```

参数：

- `-e <search_patter>`：表示搜索内容，支持正则表达式。
- `-A <line_num>`：**after**的意思，表示同时输出匹配内容的之后line_num行数的信息。
- `-B <line_num>`：**before**的意思，表示同时输出匹配内容的之后line_num行数的信息。
- `-C <line_num>`：**center**的意思，`-C10`等于`-A10 -B10`。
- `-v`：反转匹配的意思。



### 组合使用



举个例子：

```bash
pid=`adb shell ps | grep com.es | awk '{ print $2 }'` && echo "es pid: $pid" && adb logcat --pid=$pid > log3.txt
```



脚本示例：

```bash
#!/bin/bash
# ====================================================
#   Copyright (C) 2021  All rights reserved.
#
#   Author        : rf.w
#   Email         : demonsimon#gmail.com
#   File Name     : logcat_pid.sh
#   Last Modified : 2021-02-02 16:33
#   Describe      : 
#
# ====================================================


usage="$0 <app_package_name> [log_file_name]"

if [ $# -lt 1 ] || [ $# -gt 2 ]; then
  echo ${usage}
  exit
fi

echo $# $1 $2

app_pkg_name=$1
pwd=`pwd`

pid=`adb shell ps | grep -m1 "${app_pkg_name}" | awk '{ print $2 }'`

logcat="adb logcat"

cmd="${logcat} --pid=${pid}"

if [ $# -eq 2 ]; then
  if [[ "$2" =~ ^/.* ]]; then
    log=$2
  else
    log="${pwd}/$2"
  fi

  `${cmd} > ${log}`
else
  `${cmd}`
fi
```





## Terminal快捷键

Terminal的快捷键一开始我只知道TAB和任务相关的那些，直到某一天我无意中试到了一些输入相关的神奇按键，才发现**命令行原来可以更好用。**



### 常规快捷键

#### TAB

绝对是使用频率最高的快捷键。单击补全，补全失败时，双击提示。



#### Ctrl-C

任务相关快捷键：中断当前任务。



#### Ctrl-Z

任务相关快捷键：将当前任务切换到后台，并挂起（suspend）暂停。

后台未完成的任务可以使用`fg`命令切换到前台。



#### Ctrl-D

输出一个EOF（End-of-file）标志符，表示任务结束。通常交互式命令接收到这个字符（`^D`）时会主动退出。

比如，未执行其他命令时shell接收到`Ctrl-D`就会立即退出；`python`交互式命令等待输入时，按下`Ctrl-D`也会退出。



#### Ctrl-L

清除屏幕上信息。



### 输入相关快捷键

#### Ctrl-A

移动光标至当前行起始位置。



#### Ctrl-E

移动光标至当前行起始位置。



#### Ctrl-W

清除当前光标前一个单词。



#### Ctrl-U

清除当前行所有内容。



## 最后

没想到这个主题能写这么多内容，很多地方并没有展开讲清楚，也算是我这Unix ~~*“脑残粉”*~~ 簇拥者的一个阶段性总结。

贝尔实验室计算机技术研发部门的主管、管道和diff工具的创始人道格拉斯·麦克罗伊曾这么说到：“**你可以安心地在几乎所有的贡献后面都加上丹尼斯·里奇和肯·汤普逊的名字。**”



最后，Unix yyds！



---

<p>




以上，欢迎关注公众号“**小黑杂说**”。




![小黑杂说](https://raw.githubusercontent.com/wuruofan/wuruofan.github.io/master/img/qr-wechat-large.png)

