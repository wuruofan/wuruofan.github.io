---
title: JEB2Deobsecure反混淆脚本修改记录
date: 2021-02-01 18:30:44
categories:
  - 技术总结
tags:
  - JEB2
  - JEB2DeobscureClass
  - Smali
  - Deobfuscate
  - 反编译
  - 反混淆

---

## 脚本仓库

文章涉及脚本为`JEB2DeobscureClass.py`，原版仓库地址：[S3cuRiTy-Er1C/JebScripts](https://github.com/S3cuRiTy-Er1C/JebScripts)，修改版地址：[wuruofan/JebScripts](https://github.com/wuruofan/JebScripts)

## 实现原理

通常smali文件中的source字段用来说明这个smali文件对应的java文件是什么。

很多时候，为了便于定位崩溃问题，有些厂商在编译完成app release包时，仅做了代码混淆，并未去除smali文件的source字段。

![smali文件中source字段](https://i.loli.net/2021/02/01/4A72VmzsotefwcK.png)

`JEB2DeobscureClass.py`脚本的工作原理就是去取smali文件中source字段值，然后将类名重命名为该值。

## 现有问题

原脚本在某些情况下运行的很糟糕：

1. 混淆时未去除smali中source字段，而是统一修改成另外值时：即修改成非`*.java`

2. 修改成同名`*.java`：即多个smali对应一个Java文件

**第一种情况**会导致逆向包的所有类都被重命名为同一个奇怪的字符，哪怕是原来没有混淆的Activity名称也会被重命名，失去可读性。

**第二种情况**会导致JEB对class解析出错，例如：`La/b/c/d.smali`和`La/b/c/e.smali`的`source`都是`ABC.java`，那么重命名完`a.b.c`下就会有两个`ABC`类，左侧大纲里视图里可以看到这两个同名类，但是点击第二个ABC类或者成员、方法的时候，JEB默认仍解析成第一个ABC类，没办法准确的定位到代码。

其中，第二个现象是逆向小米文件管理器时发现，同一个目录下，几个类都有相同的`.source "StorageVolumeUtil.java"`，如下图所示。导致JEB反编译的时候无法正确的定位到类，比如我想访问`O`，JEB会取第一个`StorageVolumeUtil`类也就是`L`，就找不到方法了！

![4个类的source字段相同](https://i.loli.net/2021/02/01/C3oizHjJrTPpx4y.png)

![N个类的source字段相同](https://i.loli.net/2021/02/01/VUgrJ3pT8cfZsAl.png)

## 解决思路

### 第一种情况

修改了原脚本对source中字符串的判断，获取一个类的source字符串之后，判断不包含`.java`就不重命名，跳过此类。

### 第二种情况

将**source相同** 且 **同一个包目录下** 的类重命名成不同的名字。

1. 遍历所有类，将发现的source字段保存成字典映射，对应一个嵌套字典，外层字典的键Key为待重命名成的类名，即`source`字段或者source字段加一个后缀组成的字符串。
2. 内层嵌套字典的键Key为当前类地址的父路径，即所在模块名称，内层字典的值为列表，储存JEB重命名操作所需的`IDexUnit`和`IDexClass`对象，即`{ source, { parent_pkg_name, [unit, class] } }`。
3. 一旦发现已记录的source字段，就字符串自增为`source_N`判断下一个，直到找到不存在的source，并加入字典记录下来。
4. 遍历字典调用JEB重命名接口。

## 修改结果

可以看到小米文件管理器的`FileInformationFactory`有22个同名类，现在JEB可以双击正确的跳转显示了，其实有一部分是匿名内部类，可以再优化一下。

![22个同名类](https://i.loli.net/2021/01/31/mWbk9YwyBeVdlZQ.png)

![脚本运行日志](https://i.loli.net/2021/02/01/fKUZn6kRFbd1O8S.png)

## 进一步优化

存在这么多同名source，除去混淆引入，其实还有个另外的可能，就是小米文件管理器使用了太多的匿名内部类。

![匿名内部类](https://i.loli.net/2021/02/01/bOuwMkZrQvWRSIp.png)

可以看到有些类中`annotation`注解字段有说明自己是`name = null`的`InnerClass`，也指出自己的`EnclosingClass`是哪个类了。只是修改反混淆脚本解析时，发现当前是`InnerClass`时但是获取`EnclosingClass`的名称和已有已存在匿名类个数有点麻烦。

下一次优化再处理。

## 参考

1. [JEB脚本(一)(指令解析 反编译 抽象语法树) ](https://bbs.pediy.com/thread-263011.htm)

2. [JEB脚本(二)(交叉引用 调用图)](https://bbs.pediy.com/thread-263012.htm)

3. [JEB2 API文档](https://www.pnfsoftware.com/jeb/apidoc/reference/packages.html)

