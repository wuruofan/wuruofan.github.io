---
title: C++如何在类的构造函数中调用另一个构造函数
tags:
  - call another constructor
  - cpp
  - delegating constructor
  - placement new
  - 委托构造函数
  - 调用另一个构造函数
id: '309'
categories:
  - - 技术总结
date: 2020-07-22 23:46:59
---


## 简单的需求

构造函数中调用另一个构造函数，这个操作在Java里其实是很普遍的，在C++里可能就会有点问题了。

<!-- more -->

举个例子，现在有这么一段程序。

```cpp
#include <iostream>
using namespace std;

struct DataA {
  int aa;
  int bb;
  bool cc;
  char dd;

  DataA(int a, int b, bool c, char d) : aa(a), bb(b), cc(c), dd(d) {}
};

class A {
  int a_;
  int b_;
  bool c_;

 public:
  A() { std::cout << "hello @default ctor!" << std::endl; }
  
  A(int a, int b, bool c) : a_(a), b_(b), c_(c) {
    std::cout << "hello @ctor 1!" << std::endl;
  }
  
  A(const DataA& data) {
    std::cout << "hello @ctor 2!" << std::endl;
    A(data.aa, data.bb, data.cc);
  }

  ~A() { std::cout << "bye @dtor!" << std::endl; }

  friend std::ostream& operator<<(std::ostream& os, const A& a) {
    os << "a: " << a.a_ << ", b: " << a.b_ << ", c: " << a.c_;
    return os;
  }
};

int main(void) {
  DataA data(1, 2, true, 'x');

  std::cout << "before new A instance ..." << std::endl;

  A* a = new A(data);
  std::cout << *a << std::endl;

  std::cout << "before delete A instance ..." << std::endl;
  delete a;

  return 0;
}
```

`class A`拥有两个自定义构造函数，一个接受几个值进行成员初始化，另一个构造函数的本意接受一个结构体常量并进行成员初始化。

整个程序使用`g++ -g b.cpp -o b.out`编译是没问题的，但是执行的效果却不是想象中的abc分别为1、2、1，而是0、0、0。输出日志如下。

```
before new A instance ...
hello @ctor 2!
hello @ctor 1!
bye @dtor!
a: 0, b: 0, c: 0
before delete A instance ...
bye @dtor!
```

**由于构造函数并没有返回值，在构造函数里调用另一个构造函数，只会导致重新声明并初始化一个新的匿名对象，并不会初始化原来的`this`对象，这个匿名对象在构造函数结束后便销毁了。**

上面日志也可以看出来，在`ctor 2`调用后紧接着调用了`ctor 1`和`dtor`完成了内部匿名对象的实例化和销毁，用`lldb`或者`gdb`调试也可以看的更清楚些。之前编译时已经使用了`-g`参数加入了调试信息，直接`lldb b.out`运行加断点即可。

```bash
(lldb) s
hello @ctor 2!
Process 17565 stopped
* thread #1, queue = 'com.apple.main-thread', stop reason = step in
    frame #0: 0x0000000100000f85 b.out`A::A(this=0x0000000100304150, data=0x00007ffeefbff4d0) at b.cpp:38:7
   35
   36  	  A(const DataA& data) {
   37  	    std::cout << "hello @ctor 2!" << std::endl;
-> 38  	    A(data.aa, data.bb, data.cc);
   39  	  }
   40
   41  	  ~A() { std::cout << "bye @dtor!" << std::endl; }
Target 0: (b.out) stopped.
(lldb) p this
(A *) $0 = 0x0000000100304150

```

可以看到在使用`ctor 2`构造A实例时，this指针的地址为`0x0000000100304150`，我们在继续单步执行。

```bash
Process 17565 stopped
* thread #1, queue = 'com.apple.main-thread', stop reason = step in
    frame #0: 0x0000000100001024 b.out`A::A(this=0x00007ffeefbff430, a=1, b=2, c=true) at b.cpp:32:32
   29  	 public:
   30  	  A() { std::cout << "hello @default ctor!" << std::endl; }
   31
-> 32  	  A(int a, int b, bool c) : a_(a), b_(b), c_(c) {
   33  	    std::cout << "hello @ctor 1!" << std::endl;
   34  	  }
   35
Target 0: (b.out) stopped.
(lldb) p this
(A *) $1 = 0x00007ffeefbff430
```

执行到调用`ctor 1`时，再次打印this指针，发现此时this指向`0x00007ffeefbff430`，使用`bt`命令查看调用堆栈也可以看到this指针的变化，可以看到此时类中成员a、b、c的值都是我们所期望的，可惜下一步就消失了。

```bash
(lldb) bt
* thread #1, queue = 'com.apple.main-thread', stop reason = step in
  * frame #0: 0x0000000100001059 b.out`A::A(this=0x00007ffeefbff430, a=1, b=2, c=true) at b.cpp:34:3
    frame #1: 0x0000000100000ff0 b.out`A::A(this=0x00007ffeefbff430, a=1, b=2, c=true) at b.cpp:32:49
    frame #2: 0x0000000100000fac b.out`A::A(this=0x0000000100304150, data=0x00007ffeefbff4d0) at b.cpp:38:5
    frame #3: 0x0000000100000e4d b.out`A::A(this=0x0000000100304150, data=0x00007ffeefbff4d0) at b.cpp:36:24
    frame #4: 0x0000000100000c4e b.out`main at b.cpp:54:14
    frame #5: 0x00007fff6d981cc9 libdyld.dylib`start + 1
```

### 推荐的做法

那么，应该怎么做才是正确的呢？

通常推荐做法有两种，一是把通用的初始化逻辑抽出来放到类似`init()`的函数中实现，在不同构造函数中分别调用；另一种就是利用C++11的新特性：**委托构造函数(delegating constructor)**来实现。

委托构造函数的语法有点类似成员初始化列表，在构造函数声明之后使用冒号+需要调用的构造函数名即可。上面的`class A`中现在可以增加一个新的构造函数，委托给`ctor 1`。

```cpp
  A(int a, bool c) : A(a, 22, c) {
    std::cout << "hello @ctor 3!" << std::endl;
    b_ = 33;
  }
```

另外，被委托的构造函数只能有一个，否则编译会提示错误`error: an initializer for a delegating constructor must appear alone`。

使用委托构造函数后，编译需指明C++11版本，即`g++ -g b.cpp -o b.out -std=c++11`。

### 极不推荐的做法

当然，还有一种**极不推荐**的做法也可以达到目的：~~`placement new`~~，也就是在已经分配好的内存区域重新实例化对象。cpp-references上有如下说明：

> Placement new
> 
> If placement_params are provided, they are passed to the allocation function as additional arguments. Such allocation functions are known as "placement new", after the standard allocation function void* operator new(std::size_t, void*), which simply returns its second argument unchanged. This is used to construct objects in allocated storage:

> ```cpp
> char* ptr = new char[sizeof(T)]; // allocate memory
> T* tptr = new(ptr) T;            // construct in allocated storage ("place")
> tptr->~T();                      // destruct
> delete[] ptr;                    // deallocate memory
> ```

上面代码中的`ctor 2`用`placement new`实现如下：

```cpp
  A(const DataA& data) {
    std::cout << "hello @ctor 2!" << std::endl;
    this->~A();
    new (this) A(data.aa, data.bb, data.cc);
  }
```

我们先销毁了原实例，并在原this指针位置构造了一个新的A实例去替代原实例，运行后日志如下：

```bash
before new A instance ...
hello @ctor 2!
bye @dtor!
hello @ctor 1!
a: 1, b: 2, c: 1
before delete A instance ...
bye @dtor!
```

我们在用lldb调试一下，看一下调用构造函数`ctor 1`时的堆栈信息：

```bash
(lldb) bt
* thread #1, queue = 'com.apple.main-thread', stop reason = step in
  * frame #0: 0x0000000100001184 b.out`A::A(this=0x00000001002052b0, a=1, b=2, c=true) at b.cpp:32:32
    frame #1: 0x0000000100001150 b.out`A::A(this=0x00000001002052b0, a=1, b=2, c=true) at b.cpp:32:49
    frame #2: 0x0000000100001113 b.out`A::A(this=0x00000001002052b0, data=0x00007ffeefbff4d0) at b.cpp:39:16
    frame #3: 0x0000000100000f9d b.out`A::A(this=0x00000001002052b0, data=0x00007ffeefbff4d0) at b.cpp:36:24
    frame #4: 0x0000000100000dbe b.out`main at b.cpp:60:14
    frame #5: 0x00007fff6d981cc9 libdyld.dylib`start + 1
```

此时，`frame #2`和`frame #1`包含的A实例的this指针地址时相同的！可以看到，我们最早期望的目标是达到了，但是，用cpp-references上的原话来说，这种方式是**ill-formed**，病态的。

**使用`placement new`操作最危险的地方在于，需要编程者自己去注意原空间的分配是否足够、原空间的内存对齐与否会不会对新构造对象产生影响，还需要自己负责去析构实例、去释放空间，因为一旦使用这种方法，除了上帝和编程者，编译器和运行环境是无法检测到这些错误的。**

以上。

<center> --- END --- </center>

参考链接：
1. [https://isocpp.org/wiki/faq/ctors#init-methods](https://isocpp.org/wiki/faq/ctors#init-methods "Can one constructor of a class call another constructor of the same class to initialize the this object?")
2. [https://isocpp.org/wiki/faq/dtors#placement-new](https://isocpp.org/wiki/faq/dtors#placement-new "What is “placement new” and why would I use it?")
3. [https://www.cnblogs.com/chio/archive/2007/10/20/931043.html](https://www.cnblogs.com/chio/archive/2007/10/20/931043.html "从一道题谈C++中构造函数调用构造函数")


