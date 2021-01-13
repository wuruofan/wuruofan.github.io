---
title: 使用dotfiles管理配置文件
tags:
  - dotfiles
  - git
  - vim
  - zsh
  - 技术
id: '237'
categories:
  - - 技术总结
date: 2020-04-13 21:53:27
---

之前也是无意中看到别的大佬github上的dotfiles仓库了解到dotfiles这个名次，后来专门搜索了一下，其实原理很简单，就是把常用的软件配置文件都集中在一个git仓库里管理备份，然后通过软链接的形式把这些配置文件安放到合适的位置。

由于那些Unix系统中的配置文件通常以`.`(英文：dot)开头，以隐藏文件的形式保存在用户的主目录(home目录)下，所以这个仓库被成为`dotfiles`。

这和我之前用Dropbox或Google Drive备份配置思路差不多，只不过缺少了`ln -s`软链接的过程。

今天趁着搭建Ubuntu下开发环境的机会，我也实践了一把dotfiles管理。其实说实话，像我这种被同事戏称开发前得先治病的强迫症患者，dotfiles真香。

整理下MacOS和Ubuntu下公用的软件，vim、zsh、git这三个是必需品，以前还备份过Ubuntu Compiz软件的各种特效、主题图标之类的，实在折腾不动了。

整理完的目录结构大致如下。

```
dotfiles
├── README.md
├── git
│   ├── _git-completion.bash
│   └── _gitconfig
├── link.sh
├── sh
│   └── _shrc.local.bak
├── vim
│   ├── _vimrc
│   ├── nvim
│   │   └── init.vim
│   └── plugins.vim
└── zsh
    ├── _zshrc
    ├── agnoster-rfw.zsh-theme
    └── install_zsh_plugins.sh
```

git主要就`～/.gitconfig`文件，这里有一些我的奇怪的alias配置；`.git-completion.bash`主要防止在某些版本，git之后无法自动补全子命令，需要在终端启动脚本（具体文件和使用终端程序有关）里加载（`source`）一下。

sh中的`.shrc.local`主要是我本地的开发环境有些环境变量的配置，我会在终端的启动脚本里加载，由于这些变量和本机的目录有关，暂时以备份文件的形式，当一个模版使用。

vim是多年的老伙计了，最近投入了neovim的怀抱，有些配置为了兼容还是保留在`.vimrc`里；neovim的默认启动脚本为`~/.config/nvim/init.vim`，这里简单处理加载了vim的环境信息;`plugins.vim`是我自己使用插件的合集，用于`vim-plug`插件管理器读取，vim第一次运行时就会自动下载安装`plugins.vim`中的插件。



zsh也是最近新欢，比老伙计`bash`多了很多贴心功能，而且主题皮肤很多（适合我这种闷骚的强迫症），`.zshrc`是其主要配置文件，`agnoster-rfw.zsh-theme`是我修改的`agnoster`主题，`install_zsh_plugins.sh`包含了著名zsh插件组合`oh-my-zsh`、`zsh autosuggestions`、`zsh syntax highlighting`插件安装的命令。



`link.sh`就是我简单写的`ln -s`命令合集，需要`sudo ./link.sh`执行，实现功能就是将各个文件放置到合适的目录中去，做的好一些的话可以添加一些交互式操作，让用户选择链接哪些文件，以后再完善吧。

我的dotfiles仓库地址如下：[dotfiles.git](https://github.com/wuruofan/dotfiles.git)，基本可以即开即用。

以Ubuntu 18.04为例。

1.  vim

推荐安装`neovim`，使用上和vim普通没有什么区别，有些neovim专用的插件。使用`sudo apt-get install neovim`安装。

由于第一次运行会执行`curl`去下载`vim-plug`插件管理器，因此，还需要事先执行`sudo apt-get install curl`安装。

另外，插件中包含自动补全代码的神器`YouCompleteMe`需要python3.6支持，在第一次运行完`nvim`/`vim`安装完插件后，建议完成YCM的安装。

首先执行`sudo apt-get install python3.6 python3.6-dev`安装所需依赖。 然后`cd ~/.vim/bundle/YouCompleteMe`，执行`./install.py --clang-completer`，如不需要`clang`支持，可以不加入参数。

vim的配置文件中的一些按键设置，可以按需修改`_vimrc`文件。

2.  zsh

运行`sudo apt-get install zsh`安装zsh程序，然后执行`sudo chsh -s /bin/zsh`将默认终端程序替换成zsh，重启或者退出当前用户重登录即可。

正常情况这里就OK了，使用`echo $SHELL`查看当前运行的shell程序是什么。

我今天遇到个奇怪的问题就是`chsh`始终没法替换成功，一直是bash无法改变。

在stackoverflow上看到有个答案，可以修改`/etc/passwd`文件，把包含当前登录用户名的那一行最后`/bin/bash`改成`/bin/zsh`，重启电脑即可。

3.  git

建议修改`_gitconfig`中用户名邮箱相关，主要是些alias别名配置，我比较懒，所以大多数子命令都用两个字母缩写。

以上，就是今天的dotfiles初探，以后再补充其他配置。