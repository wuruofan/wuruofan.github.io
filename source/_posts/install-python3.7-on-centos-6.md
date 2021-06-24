---
title: 【避坑指北】CentOS 6安装Python3.7+
date: 2021-06-23 20:01:28
categories:
  - 避坑指北
tags:
  - 遇坑总结
  - 避坑指北
  - python
  - openssl
  - centos

---
由于某种未知原因，一台老服务器上python3环境不见了，不清楚原安装方法与位置，现重新配置。

用`cat /etc/issue`查看了下发行版信息，是CentOS 6.10。CentOS 6默认安装python版本为2.6，安装python3需要自行下载源码编译。


## 编译源码

### 注意

CentOS 6版本yum安装的openssl-devel包版本是1.0.1（使用`openssl version`查看），目前Python3.7以上使用的openssl版本是1.0.2以上版本，使用默认openssl编译会提示[libressl库不兼容此版本的API](https://github.com/libressl-portable/portable/issues/381)，需要本机编译openssl库，编译过程会有很多坑。

### 安装源码依赖软件包

```bash
sudo yum install -y zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel expat-devel
```

这部分依赖软件包有些应该可以不装，可以在编译过程中根据提示错误一个个安装。

注意，由于yum本身就是一个python脚本，在python环境有问题时，这一步安装可能就会有问题，需要先恢复原python2.6的环境。

另外，CentOS 6在2020年11月底官方软件源就停止维护了，如遇到问题，需要更换成阿里云的软件源。

### 编译openssl 1.0.2

此处没有使用最新版本，酌情选择openssl版本。

#### 下载源码

命令行下载或者浏览器下载，命令行可以使用`wget http://www.openssl.org/source/openssl-1.0.2r.tar.gz`

#### 编译安装

```bash
# 这里没配置prefix，默认安装路径在/usr/local/ssl
./config shared zlib

make

# 表示将标准错误2和标准输出1的缓冲区内容都写入install.log
sudo make install > install.log 2>&1
```

#### 配置环境

```bash
# 养成备份源文件的习惯
sudo mv /usr/bin/openssl /usr/bin/openssl.bak
sudo mv /usr/include/openssl /usr/include/openssl.bak

# 链接新openssl
sudo ln -sf /usr/local/ssl/bin/openssl /usr/bin/openssl
sudo ln -sf /usr/local/ssl/include/openssl /usr/include/openssl

# 将openssl lib路径加入链接路径
echo "export LD_LIBRARY_PATH=/usr/local/ssl/lib:$LD_LIBRARY_PATH" >> ~/.bashrc
source ~/.bashrc

# 查看openssl版本
openssl version
```

### 编译python3

#### 下载目标版本源码

去官网https://www.python.org/downloads/，下载完成是一个.tar.gz压缩包，执行解压缩命令：`tar zxvf python****.tar.gz`

#### 编译安装


进入解压后源码目录，执行如下命令：

```bash
# 使用上一步编译的ssl目录
./configure --prefix=/usr/local/python3 --with-openssl=/usr/local/ssl --enable-shared 
 
make
 
sudo make install
```

这里`--enable-shared`记得加上，否则可能会出现找不到so的错误。

由于安装到`/usr/local/`目录下，所有用户都可以访问，需要su权限安装。

卸载如需要卸载，直接删除`/usr/local/python3`目录即可。



## 配置python环境

#### ~~配置环境变量~~

不推荐使用此方式，可能会遇到同名可执行程序优先从此目录定位的问题。我在配置过程中就遇到一次。

~~当前用户的bashrc终端配置文件。如会使用vim，可以使用`vim ~/.bashrc`直接编辑，也可以使用其他终端工具本地编辑后上传替换。~~

~~增加环境变量配置：`export PATH="/usr/local/python3/bin":$PATH`~~

~~编辑完成后使用`source ~/.bashrc`命令，加载终端配置文件使之生效，这样直接执行python3即可找到该命令了。~~

#### 更新软连接

将`/usr/bin/python`链接到`/usr/local/python3/bin/python3`，这样默认使用python3。

```bash
sudo mv /usr/bin/python /usr/bin/python.bak
 
sudo ln -s /usr/local/python3/bin/python3 /usr/bin/python

sudo ln -s /usr/local/python3/bin/python3 /usr/bin/python3

sudo ln -s /usr/local/python3/bin/pip3 /usr/bin/pip
```

#### 配置动态库

```bash
# 将openssl和python3 lib路径加入链接路径。
echo "export LD_LIBRARY_PATH=/usr/local/ssl/lib:/usr/local/python3/lib:$LD_LIBRARY_PATH" >> ~/.bashrc
# 重新加载
source ~/.bashrc
```

这时配置完，bashrc中应当配置了两条LD_LIBRARY_PATH，`export LD_LIBRARY_PATH=/usr/local/ssl/lib:/usr/local/python3/lib:$LD_LIBRARY_PATH`。


#### 配置yum（可选）

由于CentOS的软件管理工具yum是默认依赖python2的，如果运行出现错误，需要修改yum脚本。

用vim编辑`/usr/bin/yum`将首行`#!/usr/bin/python`改为`#!/usr/bin/python2.6`即可。


## 其他

如果在python3配置过程中都已经按照说明进行了配置，但是仍有奇怪的问题，可能和python自身的环境变量有关，python2和python3都会使用`$PYTHONHOME`和`$PYTHONPATH`，可以执行清除命令。 

```bash
unset $PYTHONHOME

unset $PYTHONPATH
```

或者退出当前登陆，重新建立ssh连接。

