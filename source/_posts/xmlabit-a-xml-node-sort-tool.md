---
title: XML排序小工具——xmlabit
date: 2021-05-20 20:55:45
categories:
  - 软件工具
tags:
  - 软件工具
  - XML排序工具
  - Git submodule
  - GitHub Actions
---



## 简介

这是小黑去年写的一个小~~公举~~工具，日常工作中有需要比较两个系统生成的XML文件是否相同，但是XML中的节点顺序并不是固定的。当时没有找到合适的工具，于是就自己写了这个工具。


工具名叫`xmlabit`，是`xml alphabet it`的缩写。代码很简单，主要依赖`pugixml`库对XML文件节点进行重排序，仓库地址：[https://github.com/wuruofan/xmlabit](https://github.com/wuruofan/xmlabit)。

`pugixml`是一个C++实现的轻量级XML操作库，支持XPath路径表达式，仓库地址：[https://github.com/zeux/pugixml](https://github.com/zeux/pugixml)。

<!-- more -->


## 功能简介

```bash
xmlabit [options] -t </xpath/to/parent_node@target_node#attributes_name> -o <output_xml_file> <input_xml_file>
```

通常情况，`xmlabit`命令基本格式如上，`[]`方括号中表示可选参数，`<>`表示必选参数。支持参数如下：

- `-v`/`--version`：打印程序版本信息。
- `-h`/`--help`：打印帮助信息。
- `-t`/`--target`：类似XPath的路径表达式来定位需要排序的节点，格式`/xpath/of/parent_node@node#attribute`，其中`#attribute`可以省略。
- `-o <output_xml_file>`/`--output <output_xml_file>`：输入排序后文件。若没有使用此参数，则排序后字符串默认输出到屏幕.
- `-d`/`--desecend`：降序排序。默认将待排序属性或节点名按A-Z字母顺序排序。
- `-i`/`--ignore-case`：忽略大小写，比较时忽略大小写。
- `-n`/`--numeric`：将待排序属性或节点名当作数字进行比较，默认XML解析时会把数字当作字符串处理。

## 编译方法

目前编译使用CMake，仅支持Linux/MacOS，Windows请使用WSL环境编译。

在工程目录，运行如下命令：

```
$ mkdir build
$ cd build
$ cmake ..
$ make
$ make install
```

如果想编译调试版本，使用 `cmake -B build -DCMAKE_BUILD_TYPE=Debug`。

默认情况`make install` 将 `xmlabit`复制到 `/usr/local/bin` 目录，如需卸载直接`rm -i /usr/local/bin`即可。


## 使用示例

### 示例1：按某子节点值排序

这里有一个books.xml如下，保存了书架、书籍的信息。

```xml
<?xml version="1.0" encoding="utf-8"?>
<bookstore>
  <magzine>
    <title lang="eng">Beauty</title>
    <price>129.29</price>
  </magzine>
  <book>
    <title lang="eng">Harry Potter3</title>
    <price>29.29</price>
  </book>
  <book>
    <title lang="eng">Harry Potter2</title>
    <price>39.99</price>
  </book>
  <book>
    <title lang="eng">Harry Potter</title>
    <price>29.19</price>
  </book>
  <book>
    <title lang="eng">readme</title>
    <price>0.95</price>
  </book>
  <book>
    <title lang="eng">readme2</title>
    <price>-0.955</price>
  </book>
  <book>
    <title lang="eng">Learning XML</title>
    <price>39.95</price>
  </book>
  <book>
    <title lang="eng">readme3</title>
    <price>0.95</price>
  </book>
</bookstore>
```

现在如果想对书架上的书籍按书名排序，那么，`-t`参数后面的表达式应该是`/bookstore@book#title`，其中`/`表示根节点，`/bookstore@book`表示待排序的节点名都是`book`，其XPath路径为`/bookstore/book`，排序依据的子节点值或者属性值名为`title`。

进入编译`build`目录，运行`./xmlabit -t /bookstore@book#title books.xml -o output.xml`即可。排序后的结果如下：

```xml
<?xml version="1.0"?>
<bookstore>
	<magzine>
		<title lang="eng">Beauty</title>
		<price>129.29</price>
	</magzine>
	<book>
		<title lang="eng">Harry Potter</title>
		<price>29.19</price>
	</book>
	<book>
		<title lang="eng">Harry Potter2</title>
		<price>39.99</price>
	</book>
	<book>
		<title lang="eng">Harry Potter3</title>
		<price>29.29</price>
	</book>
	<book>
		<title lang="eng">Learning XML</title>
		<price>39.95</price>
	</book>
	<book>
		<title lang="eng">readme</title>
		<price>0.95</price>
	</book>
	<book>
		<title lang="eng">readme2</title>
		<price>-0.955</price>
	</book>
	<book>
		<title lang="eng">readme3</title>
		<price>0.95</price>
	</book>
</bookstore>
```

### 示例2

这里又有一个book2.xml，也保存了一些书籍信息，不同的是XML节点构成不太一样。

```xml
<?xml version="1.0" encoding="utf-8"?>
<bookstore>
  <books>
    <book lang="eng" price="29.99">Harry Potter3</book>
    <book lang="us" price="10">harry potter2</book>
    <book lang="fr" price="2">Harry Potter</book>
    <book lang="eng" price="5">readme</book>
    <book lang="zh-CN" price="0.1">readme2</book>
    <book lang="eng" price="92">Learning XML</book>
    <book lang="eng" price="0.01">readme3</book>
  </books>
</bookstore>
```

#### 2.1 对`books`节点下的所有书籍按名称降序排序

使用命令`./xmlabit -t /bookstore/books@book -d books2.xml`即可：

```xml
<?xml version="1.0"?>
<bookstore>
	<books>
		<book lang="eng" price="0.01">readme3</book>
		<book lang="zh-CN" price="0.1">readme2</book>
		<book lang="eng" price="5">readme</book>
		<book lang="us" price="10">harry potter2</book>
		<book lang="eng" price="92">Learning XML</book>
		<book lang="eng" price="29.99">Harry Potter3</book>
		<book lang="fr" price="2">Harry Potter</book>
	</books>
</bookstore>
```

这里看到有一本小写名称的《harry potter2》排在了《Learning XML》前面，因为小写字符的ASCII数值要比大写字符大。

#### 2.2 对`books`节点下的所有书籍按名称、无视大小写、降序排序

使用命令`./xmlabit -t /bookstore/books@book -di books2.xml`即可：

```xml
<?xml version="1.0"?>
<bookstore>
	<books>
		<book lang="eng" price="0.01">readme3</book>
		<book lang="zh-CN" price="0.1">readme2</book>
		<book lang="eng" price="5">readme</book>
		<book lang="eng" price="92">Learning XML</book>
		<book lang="eng" price="29.99">Harry Potter3</book>
		<book lang="us" price="10">harry potter2</book>
		<book lang="fr" price="2">Harry Potter</book>
	</books>
</bookstore>
```

#### 2.3 对`books`节点下的所有书籍按属性`lang`排序

使用命令`./xmlabit -t /bookstore/books@book#lang books2.xml`即可：

```xml
<?xml version="1.0"?>
<bookstore>
	<books>
		<book lang="eng" price="29.99">Harry Potter3</book>
		<book lang="eng" price="5">readme</book>
		<book lang="eng" price="92">Learning XML</book>
		<book lang="eng" price="0.01">readme3</book>
		<book lang="fr" price="2">Harry Potter</book>
		<book lang="us" price="10">harry potter2</book>
		<book lang="zh-CN" price="0.1">readme2</book>
	</books>
</bookstore>
```

#### 2.4 对`books`节点下的所有书籍按属性`price`进行排序

使用命令`./xmlabit -t /bookstore/books@book#price books2.xml`即可：

```xml
<?xml version="1.0"?>
<bookstore>
	<books>
		<book lang="eng" price="0.01">readme3</book>
		<book lang="zh-CN" price="0.1">readme2</book>
		<book lang="us" price="10">harry potter2</book>
		<book lang="fr" price="2">Harry Potter</book>
		<book lang="eng" price="29.99">Harry Potter3</book>
		<book lang="eng" price="5">readme</book>
		<book lang="eng" price="92">Learning XML</book>
	</books>
</bookstore>
```

因为`price`属性都是字符串，排序也是按照字符串字符进行排序的。


#### 2.5 对`books`节点下的所有书籍按属性`price`以数字模式进行排序


使用命令`./xmlabit -t /bookstore/books@book#price books2.xml -n`即可：

```xml
<bookstore>
	<books>
		<book lang="eng" price="0.01">readme3</book>
		<book lang="zh-CN" price="0.1">readme2</book>
		<book lang="fr" price="2">Harry Potter</book>
		<book lang="eng" price="5">readme</book>
		<book lang="us" price="10">harry potter2</book>
		<book lang="eng" price="29.99">Harry Potter3</book>
		<book lang="eng" price="92">Learning XML</book>
	</books>
</bookstore>
```

## Git子模块（submodule）

由于xml解析逻辑完全依赖于`pugixml`，所以不想在代码里直接放入pugixml的源码文件，Git本身其实提供了submodule子模块组件，用来管理项目中用到的其他Git项目。

### 添加子模块

使用命令`git submodule add https://github.com/zeux/pugixml.git`将`pugixml`仓库添加为`xmlabit`的子模块。

这时运行`git status`会发现本地仓库里多了一个`.gitmodules`文件，里面内容记录了当前仓库包含的子模块信息。

```
[submodule "pugixml"]
	path = pugixml
	url = https://github.com/zeux/pugixml.git
```

### 初始化并检出子模块

```bash
git submodule update --init --recursive
```

这一条命令相当于运行了`git submodule init`以及`git submodule update`各个嵌套子模块。

### CMakeLists增加Git submodule支持

现在虽然不用在仓库里添加pugixml的源代码了，但是需要用户手动克隆仓库时记得使用git submodule相关命令，这样不太好。

好在Cmake可以解决，在编译时自动执行git submodule相关命令，需要在CMakeLists增加如下：

```cmake
find_package(Git QUIET)
if(GIT_FOUND AND EXISTS "${PROJECT_SOURCE_DIR}/.git")
		# Update submodules as needed
    option(GIT_SUBMODULE "Check submodules during build" ON)
    if(GIT_SUBMODULE)
        message(STATUS "Submodule update")
        execute_process(COMMAND ${GIT_EXECUTABLE} submodule update --init --recursive
                        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
                        RESULT_VARIABLE GIT_SUBMOD_RESULT)
        if(NOT GIT_SUBMOD_RESULT EQUAL "0")
            message(FATAL_ERROR "git submodule update --init failed with ${GIT_SUBMOD_RESULT}, please checkout submodules")
        endif()
    endif()
endif()

if(NOT EXISTS "${PROJECT_SOURCE_DIR}/${PUGIXML_REPO}/CMakeLists.txt")
    message(FATAL_ERROR "The submodules were not downloaded! GIT_SUBMODULE was turned off or failed. Please update submodules and try again.")
endif()
```

## GitHub Actions

之前在搭建GitHub Pages时候使用了Travis CI进行持续集成，在每次提交代码到GitHub时自动构建并执行部署与发布任务，这次尝试一下GitHub自家的Actions功能。

GitHub仓库界面上有一个名为Actions的Tab，点击之后会自动推荐此仓库适合使用的workflow，也就是工作流程脚本。GitHub自身提供了一个市场，可以搜索到他人提交的Actions，也可以自己上传。

<img src="https://i.loli.net/2021/05/20/fQXNntKRuYJskA9.png" alt="GitHub Actions" style="zoom:50%;" />



xmlabit使用CMake进行编译，就自动推荐了一个CMake相关的workflow，点击添加即可。以后每次提交代码，就会触发CMake自动编译的workflow。

现在可以使用如下Markdown链接在README中添加一个小徽章来显示当前workflow的状态，自动编译成功之后，会显示一个小绿标<img src="https://i.loli.net/2021/05/20/peVFA8g71OUaEZI.png" alt="编译成功徽章" style="zoom: 50%;" />。

```markdown
![GitHub Action](https://github.com/wuruofan/xmlabit/actions/workflows/cmake.yml/badge.svg)
```



## End

就这样，很简单的代码，欢迎Star和PR。



