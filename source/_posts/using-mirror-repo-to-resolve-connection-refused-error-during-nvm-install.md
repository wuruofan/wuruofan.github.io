---
title: 解决nvm安装脚本无法连接问题
date: 2023-06-05 19:00:00 
index_img: https://raw.githubusercontent.com/wuruofan/image_repo/main/image/nvm-node-version-manager.png
banner_img: https://raw.githubusercontent.com/wuruofan/image_repo/main/image/nvm-node-version-manager.png
categories: 
  - 技术总结
tags: 
  - 技术总结
  - nvm 
  - nodejs 
  - 镜像仓库
---
Hi，好久不见，最近有些忙，忙着项目，还要忙着准备考试，然后又赶上了二阳，实在是头秃+要命，好在忙完这个阶段了，明后两天出成绩，希望能顺利通过！~~我是真的背不动书了😭！~~

前段时间在看chatGPT相关的项目，很多都用的TS，包括前两周参加一个培训，应用开发使用的也是类似TS的语言，由于公司网络环境问题，github访问并不是很顺畅，总是遇到无法连接的情况，记录一下，方便遇到类似情况的朋友。

## nvm是什么？

nvm是Node.js版本管理工具（Node Version Manager）的简称。它可以帮助用户在同一台机器上安装、管理和切换不同的Node.js版本，而无需手动安装每个版本或卸载旧版本。这对于需要同时处理多个Node.js项目的开发人员来说非常有用。nvm支持在Linux和macOS等操作系统上使用，并且可以通过命令行轻松安装和配置。

## nvm安装方法

[nvm-sh/nvm: Node Version Manager - POSIX-compliant bash script to manage multiple active node.js versions (github.com)](https://github.com/nvm-sh/nvm)

官方给出了脚本直接安装的命令如下：

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
```

这里是用过 `curl`命令去下载 `install.sh`脚本，`-o-`表示输出到标准输出（这里 `-o`参数可以输出到指定文件，后面的 `-`表示标准输出。），然后使用 `bash`执行。

`install.sh`脚本的最后，会尝试将启动命令加入合适的profile文件中去（如 `~/.bash_profile`
、`~/.zshrc`、`~/.profile`、`~/.bashrc`），假如失败了，可以能需要自己将下面的命令加入自己的shell启动脚本中去。，

```bash
export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" # This loads nvm
```

正常情况，按照上面的操作就可以了，但是国内有些网络可能会出现无法访问github的情况，提示下面的错误：

```bash
curl: (7) Failed to connect to [raw.githubusercontent.com](http://raw.githubusercontent.com/ "raw.githubusercontent.com") port 443: Connection refused
```

## 网络错误：Connection refused

网络上给出的都是改hosts的方式直接访问，但是有些情况并不好使。这里给出另一种思路，使用国内镜像源替换。

前面提到默认的安装方法是去github上下载一个安装脚本，这个脚本其实简单说做了两件事：

1. 克隆nvm仓库
2. 将启动命令写入profile文件

这里网络出错其实是第一步克隆nvm仓库时出了问题，改hosts方法也是解决域名无法解析的错误，这里可以尝试使用nvm国内镜像源的方式处理，方法如下：

### 1.仅下载install.sh脚本

在浏览器里访问官网命令中的网址（[https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh](https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh)），复制全部内容并保存到文件中。

### 2.编辑脚本、替换仓库地址

找到如下行：

```bash
    elif [ "_$NVM_METHOD" = "_git" ] || [ -z "$NVM_METHOD" ]; then
      NVM_SOURCE_URL="https://github.com/${NVM_GITHUB_REPO}.git"
    else
```

替换仓库地址后如下：

```bash
    elif [ "_$NVM_METHOD" = "_git" ] || [ -z "$NVM_METHOD" ]; then
      NVM_SOURCE_URL="https://gitee.com/mirrors/nvm.git"
    else
```

### 3.保存并执行文件

命令行执行修改后的脚本，如：`bash install.sh`，执行完成后重启终端即可使用nvm命令。

---

title: nodejs｜解决nvm安装脚本无法连接问题
date: 2023-06-05 19:00:00
index_img: https://raw.githubusercontent.com/wuruofan/image_repo/main/image/nvm-node-version-manager.png
banner_img: https://raw.githubusercontent.com/wuruofan/image_repo/main/img/360-lite-browser.png
categories:

- 技术总结
  tags:
- 技术总结
- nvm
- nodejs
- 镜像仓库

---

Hi，好久不见，最近有些忙，忙着项目，还要忙着准备考试，然后又赶上了二阳，实在是头秃+要命，好在忙完这个阶段了，明后两天出成绩，希望能顺利通过！~~我是真的背不动书了😭！~~

前段时间在看chatGPT相关的项目，很多都用的TS，包括前两周参加一个培训，应用开发使用的也是类似TS的语言，由于公司网络环境问题，github访问并不是很顺畅，总是遇到无法连接的情况，记录一下，方便遇到类似情况的朋友。

## nvm是什么？

nvm是Node.js版本管理工具（Node Version Manager）的简称。它可以帮助用户在同一台机器上安装、管理和切换不同的Node.js版本，而无需手动安装每个版本或卸载旧版本。这对于需要同时处理多个Node.js项目的开发人员来说非常有用。nvm支持在Linux和macOS等操作系统上使用，并且可以通过命令行轻松安装和配置。

## nvm安装方法

[nvm-sh/nvm: Node Version Manager - POSIX-compliant bash script to manage multiple active node.js versions (github.com)](https://github.com/nvm-sh/nvm)

官方给出了脚本直接安装的命令如下：

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
```

这里是用过 `curl`命令去下载 `install.sh`脚本，`-o-`表示输出到标准输出（这里 `-o`参数可以输出到指定文件，后面的 `-`表示标准输出。），然后使用 `bash`执行。

`install.sh`脚本的最后，会尝试将启动命令加入合适的profile文件中去（如 `~/.bash_profile`
、`~/.zshrc`、`~/.profile`、`~/.bashrc`），假如失败了，可以能需要自己将下面的命令加入自己的shell启动脚本中去。，

```bash
export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" # This loads nvm
```

正常情况，按照上面的操作就可以了，但是国内有些网络可能会出现无法访问github的情况，提示下面的错误：

```bash
curl: (7) Failed to connect to [raw.githubusercontent.com](http://raw.githubusercontent.com/ "raw.githubusercontent.com") port 443: Connection refused
```

## 网络错误：Connection refused

网络上给出的都是改hosts的方式直接访问，但是有些情况并不好使。这里给出另一种思路，使用国内镜像源替换。

前面提到默认的安装方法是去github上下载一个安装脚本，这个脚本其实简单说做了两件事：

1. 克隆nvm仓库
2. 将启动命令写入profile文件

这里网络出错其实是第一步克隆nvm仓库时出了问题，改hosts方法也是解决域名无法解析的错误，这里可以尝试使用nvm国内镜像源的方式处理，方法如下：

### 1.仅下载install.sh脚本

在浏览器里访问官网命令中的网址（[https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh](https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh)），复制全部内容并保存到文件中。

### 2.编辑脚本、替换仓库地址

找到如下行：

```bash
    elif [ "_$NVM_METHOD" = "_git" ] || [ -z "$NVM_METHOD" ]; then
      NVM_SOURCE_URL="https://github.com/${NVM_GITHUB_REPO}.git"
    else
```

替换仓库地址后如下：

```bash
    elif [ "_$NVM_METHOD" = "_git" ] || [ -z "$NVM_METHOD" ]; then
      NVM_SOURCE_URL="https://gitee.com/mirrors/nvm.git"
    else
```

### 3.保存并执行文件

命令行执行修改后的脚本，如：`bash install.sh`，执行完成后重启终端即可使用nvm命令。

---

<p>

以上，欢迎关注公众号“**小黑杂说**”。

![小黑杂说](https://raw.githubusercontent.com/wuruofan/wuruofan.github.io/master/img/qr-wechat-large.png)
