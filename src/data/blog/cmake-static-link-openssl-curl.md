---
title: CMake静态链接openssl和curl
description: CMake静态链接openssl和curl
pubDatetime: 2020-05-24T12:19:28Z
modDatetime: 2020-05-24T12:19:28Z
draft: false
tags:
  - CMake
  - curl
  - openssl
  - static link
categories:
  - - 技术总结
---

### 动态链接OpenSSL和Curl

CMake本身提供了对OpenSSL/Curl这种大户人家的库的支持，通过`find_package`命令查找系统安装的OpenSSL/Curl库的路径，动态链接的方式如下即可。

```cmake
# openssl
find_package(OpenSSL REQUIRED)
if(OPENSSL_FOUND)
  include_directories(${OPENSSL_INCLUDE_DIRS})
  message(STATUS "OpenSSL Found!")
endif()

# curl
find_package(CURL REQUIRED)

if(CURL_FOUND)
  include_directories(${CURL_INCLUDE_DIR})
  message(STATUS "Curl Found: ${CURL_VERSION_STRING} ${CURL_LIBRARIES} ${CURL_LINK_LIBRARIES}!")
else(CURL_FOUND)
  message(FATAL_ERROR "Could not find the CURL library and development files.")
endif()

target_link_libraries(target_program ${CURL_LIBRARIES})
target_link_libraries(target_program OpenSSL::Crypto OpenSSL::SSL)
```

由于项目需求需要改成静态链接，其实没太大必要，把需要的动态库一起打包到安装软件，然后指定rpath应该就可以了。

但是甲方爸爸说了算了啊。🤷‍♂️

#### 静态链接配置

Linux发行版仓库安装的OpenSSL和Curl都包含了静态和动态库，但是CMake这两个各自启用静态编译的方法不太一样。

OpenSSL添加`set(OPENSSL_USE_STATIC_LIBS TRUE)`即可，make时可以看到已经找到静态库。

Curl则需要在include头文件之前添加`add_definitions(-DCURL_STATICLIB)`

> 参考：
>
> 1. [Static linking of OpenSSL Crypto in CMake
>    ](https://stackoverflow.com/questions/55165172/static-linking-of-openssl-crypto-in-cmake)
> 2. [C - Cmake compiling program with libcurl](https://stackoverflow.com/questions/49778607/c-cmake-compiling-program-with-libcurl)

```cmake
# openssl using static library
set(OPENSSL_USE_STATIC_LIBS TRUE)

# curl using static library
add_definitions(-DCURL_STATICLIB)
```

但是事实上编译过程中发现Curl好像还是动态链接的，编译完成的使用`ldd -r target_program`，发现还有`libcurl.so.4`之类字样，似乎没有找到静态库。

强行指定绝对路径链接`libcurl.a`的话会爆出找不到定义的错误，因为curl依赖的库也得静态链接才可以，这也说明前面的设置并没有成功静态链接。

![4A47B7DF-6D1C-48FA-9634-1F8FAE521EE1](https://i.loli.net/2021/01/12/QG9UsBf8z2KwXCy.png)

`ls`查看Curl库所在位置可以看到动态库静态库同时都存在，应该还是配置问题。中间绕了些弯弯发现了`${CMAKE_FIND_LIBRARY_SUFFIXES}`选项，本意是设置`find_library`命令查找库时后缀名的优先级，事实上`find_package`内部实现就是前者，一开始配置错误，死活没找到静态`.a`库，在Linux下默认查找顺序是`.so;.a`，改成如下即可找到并链接静态Curl。

```cmake
SET(CMAKE_FIND_LIBRARY_SUFFIXES .lib .a ${CMAKE_FIND_LIBRARY_SUFFIXES})
```

> 参考 [Default values for CMAKE_FIND_LIBRARY_PREFIXES/CMAKE_FIND_LIBRARY_SUFFIXES](https://stackoverflow.com/questions/28194215/default-values-for-cmake-find-library-prefixes-cmake-find-library-suffixes)

使用`curl-config --static-libs`可以看到所依赖的其他库有哪些。

![A6B38899-B756-4D92-B19B-79D04B862164](https://i.loli.net/2021/01/12/8cLbqlVF9KtO3Id.png)

> 参考 [How to get rid of libcurl linking error?](https://stackoverflow.com/questions/36732111/how-to-get-rid-of-libcurl-linking-error)

#### 源码编译Curl静态库

可以发现，Linux发行版仓库中的Curl依赖的其他乱七八糟库过多，不得已还得自己编译，不开启不需要的功能。[Curl官网](https://curl.haxx.se/)下载最新7.70版本源码，执行`./configure --with-ssl --disable-shared`之后可以看到配置开启的功能如下。

```
  Host setup:       x86_64-pc-linux-gnu
  Install prefix:   /usr/local
  Compiler:         gcc
   CFLAGS:          -Werror-implicit-function-declaration -O2 -Wno-system-headers -pthread
   CPPFLAGS:
   LDFLAGS:
   LIBS:            -lssl -lcrypto -lssl -lcrypto -lz

  curl version:     7.70.0
  SSL:              enabled (OpenSSL)
  SSH:              no      (--with-{libssh,libssh2})
  zlib:             enabled
  brotli:           no      (--with-brotli)
  GSS-API:          no      (--with-gssapi)
  TLS-SRP:          enabled
  resolver:         POSIX threaded
  IPv6:             enabled
  Unix sockets:     enabled
  IDN:              no      (--with-{libidn2,winidn})
  Build libcurl:    Shared=no, Static=yes
  Built-in manual:  enabled
  --libcurl option: enabled (--disable-libcurl-option)
  Verbose errors:   enabled (--disable-verbose)
  Code coverage:    disabled
  SSPI:             no      (--enable-sspi)
  ca cert bundle:   /etc/ssl/certs/ca-certificates.crt
  ca cert path:     no
  ca fallback:      no
  LDAP:             no      (--enable-ldap / --with-ldap-lib / --with-lber-lib)
  LDAPS:            no      (--enable-ldaps)
  RTSP:             enabled
  RTMP:             no      (--with-librtmp)
  Metalink:         no      (--with-libmetalink)
  PSL:              no      (libpsl not found)
  Alt-svc:          no      (--enable-alt-svc)
  HTTP2:            disabled (--with-nghttp2)
  HTTP3:            disabled (--with-ngtcp2, --with-quiche)
  ESNI:             no      (--enable-esni)
  Protocols:        DICT FILE FTP FTPS GOPHER HTTP HTTPS IMAP IMAPS POP3 POP3S RTSP SMB SMBS SMTP SMTPS TELNET TFTP
  Features:         SSL IPv6 UnixSockets libz AsynchDNS NTLM NTLM_WB TLS-SRP HTTPS-proxy
```

然后，由于我不需要安装，只执行`make`即可，生成文件路径为`./lib/.libs/libcurl.a`。我也不知道为什么在隐藏目录下。

指定链接自己编译生成的`libcurl.a`可以发现需要的依赖库就少很多了。

![B730BA13-8019-4720-A087-8E2E83F1DCE3](https://i.loli.net/2021/01/12/KvXwOpUIhuisnB2.png)

但是仍然缺少`zlib`、`dl`和`pthread`的库支持。后两者都是基本库，添加下面一行即可。

```cmake
target_link_libraries(target_program ${CMAKE_DL_LIBS} -lpthread)
```

#### 静态链接zlib

zlib是提供压缩算法的库，CMake其实也提供了zlib支持，简单如下即可。

```cmake
find_package(ZLIB REQUIRED)
if(ZLIB_FOUND)
  message(STATUS "Zlib Found!")
  include_directories(${ZLIB_INCLUDE_DIR})
endif()

target_link_libraries(target_program ${ZLIB_LIBRARIES})
```

由于之前配置了`CMAKE_FIND_LIBRARY_SUFFIXES`，默认会找到`libz.a`。

本来以为OK了，结果还是出了问题：Ubuntu软件仓库里的zlib不支持重定位！静态链接时提示如下错误：

```
/usr/bin/ld: /usr/lib/x86_64-linux-gnu/libz.a(inflate.o): relocation R_X86_64_PC32 against symbol `inflateReset' can not be used when making a shared object; recompile with -fPIC
/usr/bin/ld: final link failed: Bad value
```

没办法还是需要源码编译zlib时开启`-fPIC`支持才可以，[zlib官网](https://zlib.net)下载源码，源码目录下执行`CFLAGS="-O3 -fPIC" ./configure && make`即可，生成`libz.a`文件就在当前目录下，指定链接终于可以成功编译啦！

#### 动态链接和静态链接生成库依赖对比

我们再使用`ldd -r target_program`对比一下动态链接和静态链接的库，可以发现静态链接后依赖的库要少很多。

![C9E063C4-7B08-42DC-A074-8B9663C9B2A8](https://i.loli.net/2021/01/12/pDq2LZ6BxcbyS9G.png)

<center>⬆️动态链接</center>

![2A5B9081-700D-4D3F-A00F-B27EB2395702](https://i.loli.net/2021/01/12/X3LC9ZfTOvuAPbd.png)

<center>⬆️静态链接</center>

#### 最终版CMakelists.txt

```cmake
include(CMakeDependentOption)

# static link curl & openssl
option(LINK_CURL_OPENSSL_STATIC "Using static curl & openssl library" ON)
cmake_dependent_option(CUSTOM_CURL_STATIC "Using prebuilt static curl library" ON
        "LINK_CURL_OPENSSL_STATIC" OFF)
cmake_dependent_option(CUSTOM_ZLIB_STATIC "Using prebuilt static zlib library" ON
        "LINK_CURL_OPENSSL_STATIC" OFF)

if(LINK_CURL_OPENSSL_STATIC)
  message(STATUS "Using static curl & openssl library!")
  add_definitions(-DCURL_STATICLIB)
  SET(CMAKE_FIND_LIBRARY_SUFFIXES .lib .a ${CMAKE_FIND_LIBRARY_SUFFIXES})
  message(STATUS "CMAKE_FIND_LIBRARY_SUFFIXES: " ${CMAKE_FIND_LIBRARY_SUFFIXES})
  set(OPENSSL_USE_STATIC_LIBS TRUE)
else()
#  set(CUSTOM_CURL_STATIC OFF)
#  set(CUSTOM_ZLIB_STATIC OFF)
endif()


# openssl
find_package(OpenSSL REQUIRED)
if(OPENSSL_FOUND)
  include_directories(${OPENSSL_INCLUDE_DIRS})
  message(STATUS "OpenSSL Found!")
endif()

# curl
if(NOT CUSTOM_CURL_STATIC)
  find_package(CURL REQUIRED)

  if(CURL_FOUND)
    include_directories(${CURL_INCLUDE_DIR})
    message(STATUS "Curl Found: ${CURL_VERSION_STRING} ${CURL_LIBRARIES} ${CURL_LINK_LIBRARIES}!")
    set(curl_library ${CURL_LIBRARIES})
  else(CURL_FOUND)
    message(FATAL_ERROR "Could not find the CURL library and development files.")
  endif()
else()
  message(STATUS "Using custom compiled static library: libcurl.a !")
  include_directories(${PREBUILTS_BASE_DIRECTORY}/${PLATFORM_NAME}/include/)
  set(curl_library ${PREBUILTS_LIB_DERECTORY}/curl/libcurl.a)
endif()

# zlib
if(NOT CUSTOM_ZLIB_STATIC)
  find_package(ZLIB REQUIRED)
  if(ZLIB_FOUND)
    message(STATUS "Zlib Found!")
    include_directories(${ZLIB_INCLUDE_DIR})
    set(zlib_library ${ZLIB_LIBRARIES})
  endif()
else()
  message(STATUS "Using custom compiled static library: libz.a !")
  set(zlib_library ${PREBUILTS_LIB_DERECTORY}/zlib/libz.a)
endif()

target_link_libraries(target_program ${curl_library})
target_link_libraries(target_program OpenSSL::Crypto OpenSSL::SSL)

if(LINK_CURL_OPENSSL_STATIC)
  target_link_libraries(target_program ${zlib_library})
  target_link_libraries(target_program ${CMAKE_DL_LIBS} -lpthread)
endif()

```

上面的CMakelists提供了3个配置参数:

- `LINK_CURL_OPENSSL_STATIC`：默认开启，静态链接Curl和OpenSSL。

- `CUSTOM_CURL_STATIC`：默认开启，使用工程目录下预编译的libcurl.a。

- `CUSTOM_ZLIB_STATIC`：默认开启，使用工程目录下预编译的libzlib.a。

正常`cmake .. && make`，会静态链接Curl、OpenSSL、zlib，其中Curl和zlib使用预编译版本。使用`cmake -DCUSTOM_CURL_STATIC=OFF -DCUSTOM_ZLIB_STATIC=OFF .. && make`来使用默认系统安装的静态版本。

使用`cmake -DLINK_CURL_OPENSSL_STATIC=OFF .. && make`，则会使用动态链接Curl和OpenSSL。

<center>--- END ---</center>
