---
title: CMake学习笔记
tags:
  - CMake
  - 技术总结
id: '248'
categories:
  - - 技术总结
date: 2020-05-11 17:32:05
---

> CMake是个一个开源的跨平台自动化建构系统，用来管理软件建置的程序，并不依赖于某特定编译器，并可支持多层目录、多个应用程序与多个库。
> 
> CMake并不直接建构出最终的软件，而是产生标准的建构档（如Unix的Makefile或Windows Visual C++的projects/workspaces），然后再依一般的建构方式使用。这使得熟悉某个集成开发环境（IDE）的开发者可以用标准的方式建构他的软件，这种可以使用各平台的原生建构系统的能力是CMake和SCons等其他类似系统的区别之处。
> 
> “CMake”这个名字是"Cross platform Make"的缩写。虽然名字中含有"make"，但是CMake和Unix上常见的“make”系统是分开的，而且更为高端。 它可与原生建置环境结合使用，例如：make、苹果的Xcode与微软的Visual Studio。
> 
> ——以上，摘自维基百科：[CMake](https://zh.wikipedia.org/wiki/CMake)

以下是在做Windows版本程序迁移至Linux平台遇到的一些问题，记录下来。

* * *

### 获取系统信息

`${CMAKE_SYSTEM}`、`${CMAKE_SYSTEM_NAME}` 需要在 `project(xxx)` 之后使用，否则为空。

`${CMAKE_HOST_SYSTEM_NAME}` 可以在 `project(xxx)` 之前使用，获取结果类似于 `uname -s`命令。

* * *

### install路径设置

`cmake -DCMAKE_INSTALL_PREFIX=< install_path > ..`或者在CMakelists.txt里`SET(CMAKE_INSTALL_PREFIX < install_path >)`

**需要在 `project(xxx)`之前设置，否则无效！**

或者使用cmake手册中的方法，可以在`project(xxx)`之后设置。

```cmake
if(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
  set(CMAKE_INSTALL_PREFIX "/my/default" CACHE PATH "..." FORCE)
endif()
```

* * *

### 变量设置失效的问题

遇到奇怪的现象，就是我在根目录的CMakelists.txt里配置了`${CMAKE_INSTALL_PREFIX}`和`$CMAKE_BUILD_TYPE}`，但是在`rm -r *`清空build目录，**重新**`cmake ..`执行到配置`install`相关选项的时候会遇到打印这两个变量值变为默认值`/usr/local`和空的问题。

第二次执行`cmake ..`这两个变量值就OK了。

有时修改CMakelists之后，再执行`make install`看到打印

```
Install the project...
-- Install configuration: ""
```

查了下资料和CMake的缓存机制有关。

> 参考 [CMake"变量污染"](https://xyz1001.xyz/articles/53989.html)

在build目录下有一个CMakeCache.txt，里面会缓存一些配置信息，用于第二次编译加速，但是有些值会从Cache中去读，在第二次运行时`set()`并不会更新Cache的缓存，需要加上强制写缓存的设置才可以。

CMake手册上对`set()`有说明：

> `set(<variable> <value>... CACHE <type> <docstring> [FORCE])`
> 
> 其中，`<type>`值如下：
> 
> *   `BOOL`: Boolean ON/OFF value. cmake-gui(1) offers a checkbox.
> *   `FILEPATH`: Path to a file on disk. cmake-gui(1) offers a file dialog.
> *   `PATH`: Path to a directory on disk. cmake-gui(1) offers a file dialog.
> *   `STRING`: A line of text. cmake-gui(1) offers a text field or a drop-down selection if the STRINGS cache entry property is set.
> *   `INTERNAL`: A line of text. cmake-gui(1) does not show internal entries. They may be used to store variables persistently across runs. Use of this type implies FORCE.
> 
> `<docstring>`是说明字符串，用于`cmake-gui`展示。must be specified as a line of text providing a quick summary of the option for presentation to cmake-gui(1) users.

因此，改为如下就OK了。

```cmake
set(CMAKE_INSTALL_PREFIX ${CMAKE_BINARY_DIR}/install CACHE PATH "install prefix" FORCE)

set(CMAKE_BUILD_TYPE "Release" CACHE STRING "build type" FORCE)
```

* * *

### 链接动态库时使用相对路径rpath using relatived path

> [CMAKE和RPATH](https://blog.csdn.net/i7thTool/article/details/80718559)
> 
> [How to link a shared library with CMake with relative path](https://stackoverflow.com/questions/43330165/how-to-link-a-shared-library-with-cmake-with-relative-path)
> 
> [linux下生成动态链接库并使用（使用cmake）](https://blog.csdn.net/ktigerhero3/article/details/68941252)

`rpath`指的是`runpath`，Unix系统运行可执行程序时默认搜索所需要动态库的路径，链接器ld搜索路径的优先级是这样的：

1.  `RPATH`，编译链接时加入 -rpath 参数指明所谓的 RUNPATH ，这样可执行文件（或者依赖其他动态链接库的动态链接库）就能告诉 ld.so 到哪里去搜索对应的动态链接库了。
  
2.  `LD_LIBRARY_PATH` ，对于没有设定 RPATH 的可执行文件或者动态链接库，我们可以用 `LD_LIBRARY_PATH` 这个环境变量通知 ld.so 往哪里查找链接库。
  
3.  `/etc/ld.so.conf`，系统对 ld.so 的路径配置文件。
  
4.  `/usr/lib` 、 `/lib` 和 `/usr/local/lib`，系统默认路径。
  

关于rpath，CMake默认设置为：

```cmake
# use, i.e. don't skip the full RPATH for the build tree
SET(CMAKE_SKIP_BUILD_RPATH  FALSE)

# when building, don't use the install RPATH already
# (but later on when installing)
SET(CMAKE_BUILD_WITH_INSTALL_RPATH FALSE) 

# the RPATH to be used when installing
SET(CMAKE_INSTALL_RPATH "")

# don't add the automatically determined parts of the RPATH
# which point to directories outside the build tree to the install RPATH
SET(CMAKE_INSTALL_RPATH_USE_LINK_PATH FALSE)
```

改为

```cmake
## On platforms that support runtime paths (RPATH) with the $ORIGIN token, setting CMAKE_BUILD_RPATH_USE_ORIGIN to TRUE enables relative paths in the build RPATH for executables and shared libraries that point to shared libraries in the same build tree.
set(CMAKE_BUILD_RPATH_USE_ORIGIN true)
set(CMAKE_INSTALL_RPATH "$ORIGIN")

## Do not include RPATHs in the build tree.
set(CMAKE_SKIP_BUILD_RPATH FALSE)
## Use the install path for the RPATH.
set(CMAKE_BUILD_WITH_INSTALL_RPATH FALSE)
## Add paths to linker search and installed rpath.
set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)

```

或者，设置链接属性包含`$ORIGIN`路径

```cmake
SET(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -Wl,-rpath -Wl,$ORIGIN")
```

* * *

### MacOS下编译遇到找不到OpenSSL的问题

```
CMake Error at /usr/local/Cellar/cmake/3.17.1/share/cmake/Modules/FindPackageHandleStandardArgs.cmake:164 (message):
  Could NOT find OpenSSL, try to set the path to OpenSSL root folder in the
  system variable OPENSSL_ROOT_DIR (missing: OPENSSL_INCLUDE_DIR)
Call Stack (most recent call first):
  /usr/local/Cellar/cmake/3.17.1/share/cmake/Modules/FindPackageHandleStandardArgs.cmake:445 (_FPHSA_FAILURE_MESSAGE)
  /usr/local/Cellar/cmake/3.17.1/share/cmake/Modules/FindOpenSSL.cmake:450 (find_package_handle_standard_args)
  src/CMakeLists.txt:44 (find_package)
```

> 参考[https://github.com/udacity/CarND-PID-Control-Project/issues/2](https://github.com/udacity/CarND-PID-Control-Project/issues/2)

解决方案是 `cmake ..` 时加上参数

```
cmake -DOPENSSL_ROOT_DIR=/usr/local/Cellar/openssl/1.0.2k -DOPENSSL_LIBRARIES=/usr/local/Cellar/openssl/1.0.2k/lib ..
```

* * *

### option选项

CMake支持自定义编译选项，语法：

```cmake
option(<variable> "<help_text>" [value])
```

注意双引号内的字符串是变量的说明注解并不是值！ 通常value为`ON`/`OFF`，如果不设置值，则默认为`OFF`。

之前就犯傻了，直接把`set(USE_FAKE_SCS "on")`改成`option`就出问题了。

* * *

### `add_custom_command`/`add_custom_target`执行命令

使用`add_custom_command`/`add_custom_target`的`COMMAND`参数执行命令时**只能执行`cmake -E`支持的系统命令**，解压文件的话只能使用`tar`不能用`unzip`。

在终端下执行`cmake -E`可以查看支持哪些命令。

另外，`add_custom_command`/`add_custom_target`的`WORKING_DIRECTORY`参数指定目录时，实际会先`cd`到该目录，因此需实现保证该目录存在。

* * *

### cmake创建目录

> 参考 [creating-a-directory-in-cmake](https://stackoverflow.com/questions/3702115/creating-a-directory-in-cmake)

*   生成编译目录时创建
  
    > 我理解是`cmake ..`时创建。
    
    ```cmake
    file(MAKE_DIRECTORY ${directory})
    ```
    
*   编译时创建
  
    > `make`时创建
    
    ```cmake
    add_custom_target(build-time-make-directory ALL
      COMMAND ${CMAKE_COMMAND} -E make_directory ${directory})
    ```
    
*   安装时创建
  
    > `make install`时创建
    
    ```cmake
    install(DIRECTORY DESTINATION ${directory})
    ```
    

  