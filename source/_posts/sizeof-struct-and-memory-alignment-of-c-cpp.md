---
title: 遇坑总结｜结构体大小与内存对齐问题

date: 2022-10-13 19:23:36

index_img: https://raw.githubusercontent.com/wuruofan/image_repo/main/img/Cpp-programming-language.jpeg

banner_img: https://raw.githubusercontent.com/wuruofan/image_repo/main/img/Cpp-programming-language.jpeg

categories:

  - 遇坑总结

tags:

  - 遇坑总结
  - C/C++
  - 内存对齐
  - 极速浏览器
  - Chromium内核


---



## 问题背景

最近做Chromium内核播放器相关功能的优化，很久没写cpp代码了，的确有些忘了，遇到了结构体内存对齐引起的奇怪问题。



**问题背景**是这样的：



极速浏览器提供了全能播放器功能，可以接管网页上的视频播放，提供倍速、快进快退、投屏等等快捷功能。采用的思路是在WebView之上绘制播放器界面，位置的绘制是一开始网页加载时就完成了网页上video标签的位置解析，是**不支持动态解析**的。

因为有些网站自己实现的播放器滚动吸顶的功能，而这种吸顶其实就属于网页的js动态调整了video标签或者video标签父布局的属性。

这种情况就GG了，就会出现播放器位置错位的问题。



## 问题出现



我这次就是修改Chromium内核，支持video及其父布局属性变更的消息通知，简单说就是给父布局增加了一个指针成员变量，指向其包含的视频元素，出现属性变更时就通过视频元素通知到界面上绘制的播放器界面。

问题就出在这里——“**我给原布局成员增加了一个成员**”。



```
error: static_assert failed due to requirement 'sizeof(blink::LayoutObject) == sizeof(blink::SameSizeAsLayoutObject)' "LayoutObject should stay small"
static_assert(sizeof(LayoutObject) == sizeof(SameSizeAsLayoutObject),
^             ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1 error generated.
```





源码里有这么一段代码，声明了一个结构体`struct SameSizeAsLayoutObject`，就是为了保证`LayoutObject`对象的大小始终很小。

```CPP
struct SameSizeAsLayoutObject : ImageResourceObserver, DisplayItemClient {
  // Normally this field uses the gap between DisplayItemClient and
  // LayoutObject's other fields.
  uint8_t paint_invalidation_reason_;
#if DCHECK_IS_ON()
  unsigned debug_bitfields_;
#endif
  unsigned bitfields_;
  unsigned bitfields2_;
  unsigned bitfields3_;
  void* pointers[4];
#if defined(USE_360HACK)
  void* child_video_object_;  // 保证下面的static_assert成立
#endif
  Member<void*> members[1];
  // The following fields are in FragmentData.
  IntRect visual_rect_;
  PhysicalOffset paint_offset_;
  std::unique_ptr<int> rare_data_;
};

static_assert(sizeof(LayoutObject) == sizeof(SameSizeAsLayoutObject),
              "LayoutObject should stay small");
```



当时我已经在`LayoutObject`对象中加入了一个`void* child_video_object_`成员，这里其实补上一个就好了，本来想着加在最后的，结果本着强迫症的原因就把新成员和之前的`void* pointers[4]`放在一起了！



本地测试的时候没问题，一切正常，可是到线上编译release版内核的时候出现了问题！



## 问题定位



一开始还以为是自己漏提交代码了，查了下不是的。当时就觉得很奇怪，本地一切正常啊，该加的成员两边都加了，还去找同事说来着，结果聊着聊着自己就发现不对了！



因为本地测试的时候是编的32位Debug版，线上是64位Release版！这里就是一个静态断言，而`sizeof`运算符在编译时就会确定变量的大小，只有可能是32位和64位编译环境引起的对齐问题！



`void*`是个指针，是一个内存地址值，而内存地址的大小是和平台架构有关的！在32位平台上就是4个字节，64位上是8个字节！



**C/C++编译时会对`class`或`struct`类型进行内存对齐，成员变量的类型与顺序会影响`sizeof`最终值的大小。**

本地编译没问题其实是碰巧，因为在`LayoutObject`中新添加成员的位置和`struct SameSizeAsLayoutObject`是不同的，但32位4个字节对齐碰巧相等了而已，在64位变成了8个字节导致了问题的出现！



## 问题解决



知道了问题的原因，解决起来就很简单了。



**在工程实践中，扩展一个类或者结构体时，新增加的成员最好放在最后**，这样是最保险的，因为之前的类/结构体大小都是计算好的，放在最后一定不会影响整体大小的计算。



**那放在最前面可以么？**

仅考虑`sizeof`的这一场景，其实是ok的。但是想了下，一旦项目里有那种将内存中结构体数据直接保存在本地磁盘的代码时，新旧版本的数据兼容可能会有点问题，反序列化转换时要小心。



如果新增加的成员如果必须要放在中间，那就要考虑到内存对齐的问题，要自己计算好，放在相同的位置。



## 内存对齐



特意去翻了下《C++ Primer》一书，其中是没有讲内存对齐相关知识的，仔细一想也是，应该属于编译器考虑的范畴。下面是我一点点个人理解，可能有不太准确的地方。




### 什么是内存对齐



提到内存对齐的时候，通常会说“**n字节对齐**”。引用wikipedia上的定义：



> 内存地址a被称为n字节对齐，a是n的倍数（n应是2的幂），也可以理解为当被访问的数据长度为n 字节时，数据地址为n字节对齐。如果内存未对齐，称作misaligned。



可能一下子读不懂，没关系。简单来说，**一个变量在内存中的地址其实适合这个变量的长度有关**。

如果变量a是n字节内存对齐的，那么，**a在内存中的地址一定是n的整数倍**。假设变量a在内存中的地址为`addr(a)`，那么，`addr(a) % n`的值应该为0。

莫慌，大部分情况下`n`的值和`sizeof(a)`一致。



> 参考网址：https://www.cs.umd.edu/~meesh/cmsc411/website/projects/outer/memory/align.htm



**像类/结构体这种聚合类型的数据结构，就要求其内部组成的成员元素是对齐的。**



我们单独看结构体内部，第一个成员相对于结构体本身的偏移量是0，可以简单的先把第一个成员地址当作是0，**其余成员的偏移量都应该其实际长度的整数倍**，这样就中间就会空余出一部分内存，这就会造成结构体的内存占用大小，并不一定是所有成员占用的实际空间。



结构体内部对齐后，所占用的空间才确定下来，这时还会针对结构体的大小进行一次对齐，保证结构体自身的内存地址也是对齐的。



再举个例子，假设有这样一个结构体：

```cpp
struct A {
  char a;
  short b;
  short c;
  int d;
  double e;
}
```



在64位CPU架构上，`char`占用1个字节、`short`是2个字节，`int`是4个字节、`double`是8个字节。对齐后的内存空间占用应该如下，其中每一个格子代表一个字节大小：

![struct-with-memory-alignment](https://raw.githubusercontent.com/wuruofan/image_repo/main/img/struct-with-memory-alignment.png)







### 为什么要内存对齐



内存对齐其实是和计算机硬件设计有关系的。32位的CPU意味着拥有32根地址线，这32根地址线上的高低电平表示着0或者1，代表着一个32位的二进制数，运算器一次运算处理的数据宽度就是32，寄存器宽度也是32，等等。

但我们的编程语言中有各种各样的基础类型，它们的占用空间是不一致的）。

为了保证CPU运算的高效，通常都会对内存中的数据进行对齐处理，这样一次寻址可以保证读取到完整的数据。



还是上面那个结构体，假设起始地址都是从0开始，如果没有内存对齐的话，它在内存中大概率是这个样子的。



![struct-without-memory-alignment](https://raw.githubusercontent.com/wuruofan/image_repo/main/img/struct-without-memory-alignment.png)





假如现在想读取`int d`的值，CPU第一次寻址得到的数据是[0, 7]，这时`d`只读了3个字节，再读一次，[8, 15]，才可以把`d`的全部字节读到。

可是，如果CPU想使用`d`的值，还需要额外的移位操作才能把全部字节拼到一个寄存器中。



这显然是效率低下，不能接受的。而对齐后的结构体，一次寻址就OK了。



这张图画的比较清楚，摘自http://www.songho.ca/misc/alignment/dataalign.html

![Accessing Misaligned data](https://raw.githubusercontent.com/wuruofan/image_repo/d0a4237210d9110b06cc02b5ec014b3ba24db2b4/img/cpu-access-misaligned-data.jpeg)





### 需要特别注意的类型



这次问题出现的另一个原因还是CPU架构的变化，之前给钉钉做加密SDK的时候也有遇到过多架构的适配情况，那种情况更复杂，还要不仅要考虑32位和64位，甚至要考虑x86、arm和mips架构。



前面提到n字节对齐时提到大部分场景n都和类型长度相同，下面列一下，n字节对齐和类型长度有区别，以及32位和64位CPU下有区别的情况，一般Android开发就够了。



| 基本类型  | 32位长度 | 32位n字节对齐 | 64位长度 | 64位n字节对齐 |
| --------- | -------- | ------------- | -------- | ------------- |
| long      | 4        | 4             | 8        | 8             |
| long long | 8        | 4             | 8        | 8             |
| 指针      | 4        | 4             | 8        | 8             |



> 参考网址：https://zh.wikipedia.org/wiki/%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84%E5%AF%B9%E9%BD%90





## 如何自己实现`sizeof`



因为出问题是和`sizeof`有关，但其本身是个运算符，看不到源码，网络上有些自己用宏定义实现的方案，有些代码如下：



```c
#define my_sizeof(x) ((&x + 1) - &x)
```



这样真的对么？

其实是错误的，这个宏定义运算得到的值永远为1！



这段代码中，`&x`代表取x的地址，**在C/C++语言中地址/指针的算术运算其实和指针指向的对象长度有关系**！

`指针+1`并不是只是数值上加1，加上的是指针所指向的对象长度，相当于加上了一个`sizeof`。那这样说，不应该实现的没问题么？得到的应该是`sizeof`的值才对啊？



**其实指针也是有类型的，准确的原因是，指向对象的类型是不同的。**

假如这里的x是一个`double`类型，那么，`((&x + 1) - &x)`表达式中的`&x+1`和`&x`的类型其实是是`double*`，**两个`double*`的指针之间的减法的值，其实是几个`double`类型的长度，而不是具体的字节数，有点和指针`+1`中的1有点类似。**



修改一下上面的表达式，都强制转换位`char*`类型即可，因为`char`的长度是1个字节，这样就成功的转换成字节数了。



```c
#define my_sizeof(x) ((char *)(&x + 1) - (char *)&x)
```



> 参考网址：https://stackoverflow.com/questions/14171117/implementation-of-sizeof-operator



## 最后



这就是一个最近的踩坑记录吧，顺便复习了下内存对齐的相关知识，还有些奇奇怪怪的和内存对齐相关、结构体大小相关的知识点没写，下次有空再写。



<p>



---

<p>





以上，欢迎关注公众号“**小黑杂说**”。




![小黑杂说](https://raw.githubusercontent.com/wuruofan/wuruofan.github.io/master/img/qr-wechat-large.png)
