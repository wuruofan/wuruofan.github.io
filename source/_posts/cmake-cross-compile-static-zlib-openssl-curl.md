---
title: CMake 跨平台交叉编译zlib、OpenSSL、Curl
tags:
  - CMake
  - cross compile
  - curl
  - openssl
  - static library
  - toolchain
  - zlib
id: '287'
categories:
  - - 技术总结
date: 2020-06-09 17:35:15
---

项目遇到跨平台交叉编译的问题，需要针对`mips64el`架构和`aarch64`架构进行编译。

CMake本身支持通过指定交叉编译工具链的方式来完成跨平台编译的，通过`cmake -DCMAKE_TOOLCHAIN_FILE=</path/of/toolchain/file> ..`指定交叉编译工具链即可。

以`mips64el.toolchain.cmake`为例：

```cmake
cmake_minimum_required(VERSION 2.6.3)
set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR mips64el)

set(CROSS_COMPILER_PREFIX "/usr/bin/mips64el-linux-gnuabi64")

set(CMAKE_C_COMPILER             ${CROSS_COMPILER_PREFIX}-gcc)
set(CMAKE_C_FLAGS                "-O3 -fPIC" CACHE INTERNAL "")
set(CMAKE_C_FLAGS_DEBUG          "${CMAKE_C_FLAGS} -g -Wall" CACHE INTERNAL "")
set(CMAKE_C_FLAGS_MINSIZEREL     "${CMAKE_C_FLAGS} -Os -DNDEBUG" CACHE INTERNAL "")
set(CMAKE_C_FLAGS_RELEASE        "${CMAKE_C_FLAGS} -O4 -DNDEBUG" CACHE INTERNAL "")
set(CMAKE_C_FLAGS_RELWITHDEBINFO "${CMAKE_C_FLAGS} -O2 -g" CACHE INTERNAL "")

set(CMAKE_CXX_COMPILER             ${CROSS_COMPILER_PREFIX}-g++)
set(CMAKE_CXX_FLAGS                "-O3 -fPIC" CACHE INTERNAL "")
set(CMAKE_CXX_FLAGS_DEBUG          "${CMAKE_CXX_FLAGS} -g -Wall" CACHE INTERNAL "")
set(CMAKE_CXX_FLAGS_MINSIZEREL     "${CMAKE_CXX_FLAGS} -Os -DNDEBUG" CACHE INTERNAL "")
set(CMAKE_CXX_FLAGS_RELEASE        "${CMAKE_CXX_FLAGS} -O4 -DNDEBUG" CACHE INTERNAL "")
set(CMAKE_CXX_FLAGS_RELWITHDEBINFO "${CMAKE_CXX_FLAGS} -O2 -g" CACHE INTERNAL "")

set(CMAKE_AR      ${CROSS_COMPILER_PREFIX}-ar)
set(CMAKE_LINKER  ${CROSS_COMPILER_PREFIX}-ld)
set(CMAKE_NM      ${CROSS_COMPILER_PREFIX}-nm)
set(CMAKE_OBJDUMP ${CROSS_COMPILER_PREFIX}-objdump)
set(CMAKE_RANLIB  ${CROSS_COMPILER_PREFIX}-ranlib)
```

正常无其他第三方依赖库什么的，`cmake`的时候指定toolchain文件，正常编译，解决编译问题即可。可是，项目还需要解决OpenSSL和Curl的问题。

**注意，toolchain文件里`CMAKE_<LANG>_FLAGS`相关参数需要加上`CACHE`缓存，否则，在make编译时并不会生效！** 这个问题是我在编译完zlib链接到项目时发现报错`recompile with -fPIC`，然后`make VERBOSE=1`发现编译时cflags为空，`-fPIC`并没有生效，仔细阅读`opencv`的[toolchain](https://github.com/opencv/opencv/blob/master/platforms/linux/arm.toolchain.cmake "opencv arm.toolchain.cmake")后，找到解决方法！

## 交叉编译zlib

首先是OpenSSl和Curl都有用到的zlib编译，上一篇文章[CMake静态链接OpenSSL和Curl](https://wuruofan.com/2020/05/cmake-static-link-openssl-curl/ "CMake静态链接OpenSSL和Curl")，也有介绍如何编译zlib，[https://zlib.net](https://zlib.net "zlib官网")下载源码，网络上没看到用CMake编译zlib的文章，其实zlib是支持CMake进行编译的，在zlib源码目录下有CMakelists.txt文件。

下面介绍两种方法编译`mips64el`和`aarch64`架构的zlib库：

### 使用CMake交叉编译zlib

新建build目录，并在build目录下执行如下命令即可，默认动态和静态库都会编译出来。

```bash
cmake -DCMAKE_TOOLCHAIN_FILE=/path/of/toolchains/mips64el.toolchain.cmake -DCMAKE_INSTALL_PREFIX=/home/xxx/workspace/cross_compile_libs/mips64el/zlib ..

make

make install
```

执行上面cmake命令配置toolchain文件后，看到如下类似打印，则代表交叉编译工具找到了。

```
-- The C compiler identification is GNU 7.5.0
-- Check for working C compiler: /usr/bin/mips64el-linux-gnuabi64-gcc
-- Check for working C compiler: /usr/bin/mips64el-linux-gnuabi64-gcc -- works
```

### 使用传统方法交叉编译zlib

通常网络上给的方法都是`CC=/path/to/compiler LD=/path/to/linker ./config && make`这种方式去做的，其实可以简单点，使用`CHOST=`完成，如下：

```bash
CHOST=/usr/bin/aarch64-linux-gnu CFLAGS="-O3 -fPIC" ./configure --prefix=/home/xxx/workspace/cross_compile_libs/aarch64/zlib

make

make install
```

> 参考：[https://stackoverflow.com/questions/21396988/zlib-build-not-configuring-properly-with-cross-compiler-ignores-ar](https://stackoverflow.com/questions/21396988/zlib-build-not-configuring-properly-with-cross-compiler-ignores-ar "zlib build not configuring properly with cross compiler, ignores AR?")

## 交叉编译OpenSSL

可以从[https://github.com/openssl/openssl](https://github.com/openssl/openssl "github OpenSSL仓库")下载源码，具体的编译方法可以阅读源码根目录的`INSTALL`文件，查看相关的配置选项。

执行`./Configure --help`查看简要的配置选项说明，`./Configure LIST`查看支持平台架构信息。

### mips64el架构

指定平台架构为`linux64-mips64`和相关路径即可。

```bash
./Configure -fPIC no-shared linux64-mips64 --cross-compile-prefix=/usr/bin/mips64el-linux-gnuabi64- --prefix=/home/xxx/workspace/cross_compile_libs/mips64el/openssl --with-zlib-include=/home/xxx/workspace/cross_compile_libs/mips64el/zlib/include --with-zlib-lib=/home/xxx/workspace/cross_compile_libs/mips64el/zlib/lib

make

make install
```

### aarch64架构

aarch64架构编译方法类似，但是多了`no-asm`选项。

```bash
./Configure -fPIC no-asm no-shared linux-aarch64 --cross-compile-prefix=/usr/bin/aarch64-linux-gnu- --prefix=/home/xxx/workspace/cross_compile_libs/aarch64/openssl --with-zlib-include=/home/xxx/workspace/cross_compile_libs/aarch64/zlib/include --with-zlib-lib=/home/xxx/workspace/cross_compile_libs/aarch64/zlib/lib

make

make install
```

#### dangerous relocation: unsupported relocation 错误

和`mips64el`相同参数编译完成OpenSSL后，链接到项目中的时候，会遇到了奇怪的问题，提示如下错误，需要用`-fPIC`选项重新编译：

```
relocation R_AARCH64_PREL64 against symbol `OPENSSL_armcap_P' which may bind externally can not be used when making a shared object; recompile with -fPIC
****(.text+0x**): dangerous relocation: unsupported relocation
```

可事实上`make VERBOSE=1`，是可以看到已经使用`-fPIC`了的。StackOverFlow上搜索了很久也没看到别人遇到相同的问题，倒是看了一个别的库类似错误的帖子（[https://dev.gnupg.org/T4425](https://dev.gnupg.org/T4425 "libgcrypt relocation error on aarch64")）给了我启发。

这个网友在aarch64平台静态链接libgcrypt时也遇到了重定位的问题，但是他的问题在某个patch包更新后就消失了，patch包更新仅仅包含汇编代码`adr`和`ldr`的变化，如下：

```
diff -uNr libgcrypt-1.8.4/cipher/camellia-aarch64.S libgcrypt-1.8.4_patched/cipher/camellia-aarch64.S
--- libgcrypt-1.8.4/cipher/camellia-aarch64.S   2017-11-23 19:16:58.000000000 +0100
+++ libgcrypt-1.8.4_patched/cipher/camellia-aarch64.S   2019-03-22 18:06:37.635546976 +0100
@@ -208,7 +208,7 @@
         *      x3: keybitlen
         */

-       adr RTAB1,  _gcry_camellia_arm_tables;
+       ldr RTAB1, =_gcry_camellia_arm_tables;
        mov RMASK, #(0xff<<4); /* byte mask */
        add RTAB2, RTAB1, #(1 * 4);
        add RTAB3, RTAB1, #(2 * 4);
@@ -251,7 +251,7 @@
         *      x3: keybitlen
         */

-       adr RTAB1,  _gcry_camellia_arm_tables;
+       ldr RTAB1, =_gcry_camellia_arm_tables;
        mov RMASK, #(0xff<<4); /* byte mask */
        add RTAB2, RTAB1, #(1 * 4);
        add RTAB3, RTAB1, #(2 * 4);
```

就联想到是不是平台汇编语言的问题，正好想起文章[https://shadowllife.wordpress.com/2018/05/03/how-to-cross-compile-openssl/](https://shadowllife.wordpress.com/2018/05/03/how-to-cross-compile-openssl/ "How to cross compile OpenSSL")中有个`no-asm`参数，加上去就OK了。

`no-asm`参数在`INSTALL`文件中有说明，表示不使用汇编代码，通常是调试/解决问题时开启的选项，在某些平台即使开启，仍然可能会使用少量汇编代码。

猜测可能的原因是ARM平台虽然都是`aarch64`架构，但是具体又会细分各种小平台(比如`armv8-a`、`armv8.1-a`等)、各种芯片架构（`cortex-a35`、`cortex-a72`等等），如果想使用汇编代码，可能需要更细节芯片架构配置参数才可以，比如`-march=`、`-mtune=`。具体配置参数详见[https://gcc.gnu.org/onlinedocs/gcc-6.1.0/gcc/AArch64-Options.html](https://gcc.gnu.org/onlinedocs/gcc-6.1.0/gcc/AArch64-Options.html "3.18.1 AArch64 Options")，以后有机会再研究。

## 交叉编译Curl

[https://curl.haxx.se/](https://curl.haxx.se/ "Curl官网")下载最新7.70版本源码。mips64el和aarch64架构的编译方法一致，指定OpenSSL和zlib库路径和交叉编译工具链路径即可。

```bash
# mips64el
./configure --with-ssl=/home/xxx/workspace/cross_compile_libs/mips64el/openssl --with-zlib=/home/xxx/workspace/cross_compile_libs/mips64el/zlib --disable-shared --target=mips64el-linux-gnuabi64 --host=mips64el-linux-gnuabi64 --prefix=/home/xxx/workspace/cross_compile_libs/mips64el/curl

# aarch64
#./configure --with-ssl=/home/xxx/workspace/cross_compile_libs/aarch64/openssl --with-zlib=/home/xxx/workspace/cross_compile_libs/aarch64/zlib --disable-shared --target=aarch64-linux-gnu --host=aarch64-linux-gnu --prefix=/home/parallels/workspace/cross_compile_libs/aarch64/curl

make

make install
```

## 结束

至此，交叉编译方法本质上就是指定好交叉编译工具路径，配置好依赖的库和相关参数，并不难，主要交叉编译的目标平台可能会有些奇奇怪怪的问题需要解决。

  

<center>--- END ---</center>