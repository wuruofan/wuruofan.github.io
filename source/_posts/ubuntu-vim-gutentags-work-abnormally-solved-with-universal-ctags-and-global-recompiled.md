---
title: vim-gutentags插件异常问题解决 & gtags源码编译安装
tags:
  - GNU Global
  - gtags
  - gtags-scope
  - source code compilation
  - Universal Ctags
  - vim
  - vim-gutentags
id: '300'
categories:
  - - 软件工具
date: 2020-07-07 22:18:19
---

在ubuntu上gtags总是运行不正常，`ctrl-]`无法找到tags，`gutentags`有报错信息，今天找了下原因，记录下坎坷过程。

首先在`.vimrc`中加上`let g:gutentags_trace = 1`，然后就可以用`:messages`查看具体出错日志。

发现**默认`exuberant-ctags`不支持`--output-format=e-ctags`，这个参数是给universal-ctags(gtags)用的，因此生成tags数据库出错了。**

## apt仓库安装universal-ctags

**在Ubuntu的apt仓库用`sudo apt-get install global`安装。**

实际运行发现生成tags的时候在`~/.cache/tags/xxx_project/`目录下有gtags相关文件，**但是始终不去生成`~/.cache/tags/xxx_project.tags`数据库文件**，这就是找不到tags的原因。

### 用snap安装universal-ctags

**用`sudo snap install universal-ctags`安装。**

实际运行发现生成tags数据库的时候遇到权限错误：

```
gutentags: [job stderr]: ['ctags: cannot open option file "/home/parallels/.vim/bundle/v
im-gutentags/res/ctags_recursive.options" : Permission denied', '']
```

把ctags\_recursive.options文件的权限改成666或者777，仍然是这个错误，依旧无法生成tags数据库。

搜了很久在一个网站看到有人遇到相同的问题，似乎是snap上gtags的问题。

> This is more of a warning to other users since i discovered the hard-way that universal-ctags installed by snap is NOT compatible with gutentags. For me it manifested as permission errors reading the ctags\_recursive.options file, but I could imagine different file perm errors depending on your config. The fs limitations are mentioned at https://snapcraft.io/universal-ctags and in https://github.com/universal-ctags/ctags-snap/issues/26. I don't think there is anything for gutentags to do except maybe include a warning in the doc about snap installed ctags.
> 
> 参考：[https://www.bountysource.com/issues/90002621-universal-ctags-installed-by-snap-not-compatible-with-vim-gutentags](https://www.bountysource.com/issues/90002621-universal-ctags-installed-by-snap-not-compatible-with-vim-gutentags "universal-ctags installed by snap not compatible with vim-gutentags")

## 源码安装universal-ctags

```bash
git clone https://github.com/universal-ctags/ctags.git
cd ctags
./autogen.sh
./configure
make
sudo make install
```

其中，`./autogen.sh`这一步使用`autotools`进行配置，依赖`autoconf`和`pk-config`包，需要apt安装。

```bash
sudo apt-get install autoconf
sudo apt-get install pk-config
```

编译安装完成之后，默认会装到`/usr/local/bin/ctags`目录，`ctags --version`已经可以看到`Universal Ctags`相关字样了。

```
Universal Ctags 0.0.0(3671ad72), Copyright (C) 2015 Universal Ctags Team
Universal Ctags is derived from Exuberant Ctags.
Exuberant Ctags 5.8, Copyright (C) 1996-2009 Darren Hiebert
  Compiled: May  7 2020, 17:26:30
  URL: https://ctags.io/
  Optional compiled features: +wildcards, +regex, +iconv, +option-directory, +packcc
```

然后世界就恢复正常了！tags数据库已经可以正常生成了。

## 源码安装gtags（GNU Global）

`vim-gutentags`插件此时还没法用`cscope`相关命令，搜索符号引用相关功能，还需要`gtags`支持，即`GNU Global`，是一套跨环境的源码标签系统（GNU GLOBAL is a source code tagging system that works the same way across diverse environments）。

可以使用`sudo apt-get install global`从默认源安装，但是，以防万一，还是源码编译安装好了。

从[https://www.gnu.org/software/global/download.html](https://www.gnu.org/software/global/download.html "Getting GLOBAL")官网下载最新软件包，配置、编译并安装。

> 注意：安装过程中，会依赖`curses`库，执行`./configure`的时候会提示`curses library is required but not found`，需要执行`sudo apt-get install libncurses5-dev`安装相关库。

```bash
wget http://tamacom.com/global/global-6.6.4.tar.gz
tar xzvf global-6.6.4.tar.gz
cd global-6.6.4

./configure --with-universal-ctags=`which ctags` # 指定使用universal-ctags路径
make
sudo make install
```

默认安装到`/usr/local/bin/gtags`，运行`gtags --version`，得到如下信息。

```
gtags (GNU GLOBAL) 6.6.4
Powered by Berkeley DB 1.85.
Copyright (c) 1996-2019 Tama Communications Corporation
License GPLv3+: GNU GPL version 3 or later <http://www.gnu.org/licenses/gpl.html>
This is free software; you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
```

大功告成！

* * *

最后，附上tags相关的VIM配置。

```vim
""设置标签tags
set tags=./.tags;,.tags
"设置根据打开文件自动更换目录
"set autochdir

" gutentags 搜索工程目录的标志，当前文件路径向上递归直到碰到这些文件/目录名
let g:gutentags_project_root = ['.root', '.svn', '.git', '.hg', '.project']
" 所生成的数据文件的名称
let g:gutentags_ctags_tagfile = '.tags'

" 同时开启 ctags 和 gtags 支持：
let g:gutentags_modules = []
if executable('ctags')
    let g:gutentags_modules += ['ctags']
endif
if executable('gtags-cscope') && executable('gtags')
    let g:gutentags_modules += ['gtags_cscope']
endif

" 将自动生成的 ctags/gtags 文件全部放入 ~/.cache/tags 目录中，避免污染工程目录
let s:vim_tags = expand('~/.cache/tags')
let g:gutentags_cache_dir = s:vim_tags
" 检测 ~/.cache/tags 不存在就新建 "
if !isdirectory(s:vim_tags)
   silent! call mkdir(s:vim_tags, 'p')
endif

" 配置 ctags 的参数
let g:gutentags_ctags_extra_args = ['--fields=+niazSl']
let g:gutentags_ctags_extra_args += ['--c++-kinds=+px']
let g:gutentags_ctags_extra_args += ['--c-kinds=+px']

" Get ctags version
let g:ctags_version = system('ctags --version')[0:8]

" 如果使用 universal ctags 需要增加下面一行
if g:ctags_version == "Universal"
  let g:gutentags_ctags_extra_args += ['--extras=+q', '--output-format=e-ctags']
endif

" 禁用 gutentags 自动加载 gtags 数据库的行为
let g:gutentags_auto_add_gtags_cscope = 1
"Change focus to quickfix window after search (optional).
let g:gutentags_plus_switch = 1
"Enable advanced commands: GutentagsToggleTrace, etc.
let g:gutentags_define_advanced_commands = 1
let g:gutentags_trace = 0

""cscope
if has("cscope")
    if executable('gtags-cscope') && executable('gtags')
        "禁用原GscopeFind按键映射
        let g:gutentags_plus_nomap = 1
        "Find this C symbol 查找C语言符号，即查找函数名、宏、枚举值等出现的地方
        nmap <C-\>s :GscopeFind s <C-R>=expand("<cword>")<CR><CR>
        "Find this difinition 查找函数、宏、枚举等定义的位置，类似ctags所提供的功能
        nmap <C-\>g :GscopeFind g <C-R>=expand("<cword>")<CR><CR>
        "Find functions called by this function 查找本函数调用的函数
        nmap <C-\>d :GscopeFind d <C-R>=expand("<cword>")<CR><CR>
        "Find functions calling this function 查找调用本函数的函数
        nmap <C-\>c :GscopeFind c <C-R>=expand("<cword>")<CR><CR>
        "Find this text string 查找指定的字符串
        nmap <C-\>t :GscopeFind t <C-R>=expand("<cword>")<CR><CR>
        "Find this egrep pattern 查找egrep模式，相当于egrep功能，但查找速度快多了
        nmap <C-\>e :GscopeFind e <C-R>=expand("<cword>")<CR><CR>
        "Find this file 查找并打开文件，类似vim的能
        nmap <C-\>f :GscopeFind f <C-R>=expand("<cfile>")<CR><CR>
        "Find files #including this file 查找包含本文件的文件
        nmap <C-\>i :GscopeFind i ^<C-R>=expand("<cfile>")<CR>$<CR>
    else
        set csto=1
        set cst
        set nocsverb
        " add any database in current directory
        if filereadable("cscope.out")
            cs add cscope.out
        endif
        set csverb

        nmap <C-\>s :cs find s <C-R>=expand("<cword>")<CR><CR>
        nmap <C-\>g :cs find g <C-R>=expand("<cword>")<CR><CR>
        nmap <C-\>d :cs find d <C-R>=expand("<cword>")<CR><CR>
        nmap <C-\>c :cs find c <C-R>=expand("<cword>")<CR><CR>
        nmap <C-\>t :cs find t <C-R>=expand("<cword>")<CR><CR>
        nmap <C-\>e :cs find e <C-R>=expand("<cword>")<CR><CR>
        nmap <C-\>f :cs find f <C-R>=expand("<cfile>")<CR><CR>
        nmap <C-\>i :cs find i ^<C-R>=expand("<cfile>")<CR>$<CR>

        nmap <C-F12> :cs add cscope.out<CR>
        "F12用ctags生成tags
        nmap <F12> :!ctags -R --c++-kinds=+p --fields=+ialS --extra=+q -f .tags<CR>
        "--language-force=C++
        nmap <S-F12> :!cscope -Rbkq<CR>
        " cscope参数
        "-R: 在生成索引文件时，搜索子目录树中的代码
        "-b: 只生成索引文件，不进入cscope的界面
        "-d: 只调出cscope gui界面，不跟新cscope.out
        "-k: 在生成索引文件时，不搜索/usr/include目录
        "-q: 生成cscope.in.out和cscope.po.out文件，加快cscope的索引速度
        "-i: 如果保存文件列表的文件名不是cscope.files时，需要加此选项告诉cscope到哪儿去找源文件列表。可以使用"-"，表示由标准输入获得文件列表。
        "-I dir: 在-I选项指出的目录中查找头文件
        "-u: 扫描所有文件，重新生成交叉索引文件
        "-C: 在搜索时忽略大小写
        "-P path: 在以相对路径表示的文件前加上的path，这样，你不用切换到你数据库文件所在的目录也可以使用
    endif
endif

```