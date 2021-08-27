---
title: 【避坑指北】Python3相对路径导入方法
date: 2021-08-27 16:30:00
categories:

  - 避坑指北

tags:
  - 避坑指北
  - 遇坑总结
  - 相对路径
  - Python
  - 包导入

---

## 前情

最近在优化原项目一部分Python代码，遇到了代码重复拷贝的问题，一个方法拷贝了n多份，这个“坏味道”当然忍不了，准备将方法写到utils.py里，由于Python3已经支持相对路径导入了，utils放到当前包的common目录，用到此方法的代码导入utils使用即可。so easy！



后来？后来我就掉进坑里。

我以为的相对路径导入并不是真实的相对路径导入。



## Python导入包或方法

假设我们的工程项目是这样的：

```bash
.
├── a
│   └── callee.py
├── b
│   └── caller.py
├── c
│   └── hello.py
└── main.py
```

### 常规操作

`hello.py`中实现了一个打印“say hi~”方法`hi()`：

```python
# c/hello.py
def hi():
    print("say hi~")
```



现在想要在`main.py`中调用，那我们只需要加入一行`from c.hello import hi`，然后直接调用`hi()`即可。

```python
# main.py
from c.hello import hi

hi()
```

我们运行`python3 main.py`，正常输出“say hi~”。



python和Java一样都是用目录管理包的，运行时会从当前路径（`main.py`所在目录）开始查找匹配的包名对应的`c/hello.py`文件，然后找到其中名为`hi`的方法，并调用。



### import默认搜索顺序

默认情况下，python的`import`关键字会选择优先查找python的内建模块，若没找到，则会去`sys.path`保存的路径列表中寻找。

`sys.path`保存的路径列表包括几个部分：

1. 当前脚本所在目录
2. 环境变量`$PYTHONPATH`设置的目录
3. python标准库的目录
4. 任何能够找到的.pth文件的内容
5. 第三方扩展的site-package目录，也就是pip安装第三方包的路径



### 相对路径导入的那些坑

现在有一个需求就是`b`目录下的`caller.py`希望执行`a`目录`callee.py`中的方法`caller_test()`方法，这个方法可以对应出调用者的信息。

```python
# a/callee.py
import sys
import os


def caller_test():
    """打印调用者信息"""
    back_frame = sys._getframe().f_back

    if back_frame is None:
        print("back_frame is None, no py caller!")
    else:
        back_filename = os.path.basename(back_frame.f_code.co_filename)
        print("caller: {}".format(back_filename.split('.')[0]))
```



python3已经可以支持相对路径导入包了，简单写一下：



```python
# b/caller.py
import sys

from ..a import callee

def call():
    print('------ caller.py ------')
	print("name: {}".format(__name__))
	callee.caller_test()

if __name__ == '__main__':
	call()
```

这里可以看到`a`包名前额外多了两个点`..`，按照python手册中关于相对导入的介绍：两个点`..`表示从当前目录的父目录开始查找`a/callee.py`文件，一个点`.`表示当前目录，那么如果我想找父目录的父目录中的包呢？那就用三个点`...`，通常用到三个点的情况并不多。



看上去毫无问题，正常极了，一运行就傻眼了。



#### 错误1

执行`./b/caller.py`，提示错误：`ImportError: attempted relative import with no known parent package`。

尝试在import前一行加入打印`__name__`、`__package__`、`sys.path`，结果如下：

```bash
name: __main__
package: None
sys.path: ['/home/rfw/test/b', '/usr/lib/python38.zip', '/usr/lib/python3.8', '/usr/lib/python3.8/lib-dynload', '/home/rfw/.local/lib/python3.8/site-packages', '/usr/local/lib/python3.8/dist-packages', '/usr/lib/python3/dist-packages']
```

很奇怪，看到`sys.path`中当前路径是b目录所在路径，按照相对导入的逻辑，`..a`就应该进入了`test/a`目录才对！



#### 错误2

StackOverflow上查了下，可以使用`python -m b.caller`以模块的方式运行，将包信息告诉python解释器。

尝试了下，这次错误提示变了，`ValueError: attempted relative import beyond top-level package`，提示是说相对导入找到的路径已经超过最顶级的了。

此时再次打印，错误日志如下：

```bash
name: __main__
package: b
sys.path: ['/home/rfw/test', '/usr/lib/python38.zip', '/usr/lib/python3.8', '/usr/lib/python3.8/lib-dynload', '/home/rfw/.local/lib/python3.8/site-packages', '/usr/local/lib/python3.8/dist-packages', '/usr/lib/python3/dist-packages']
```

这时，和上一次打印不一样的地方在与`__package__`的值为`b`，当前运行路径为`test`目录。



由于显示当前目录是`test`，因此，尝试把导入改成`from a.callee import caller_test`，运行正常！打印如下：

```bash
name: __main__
package: b
sys.path: ['/home/rfw/test', '/usr/lib/python38.zip', '/usr/lib/python3.8', '/usr/lib/python3.8/lib-dynload', '/home/rfw/.local/lib/python3.8/site-packages', '/usr/local/lib/python3.8/dist-packages', '/usr/lib/python3/dist-packages']
caller: caller
```



但是这就不是相对导入了啊。百思不得其解。



#### 真相只有一个

查了下python官方文档关于相对导入的说明（[https://www.python.org/dev/peps/pep-0328/](https://www.python.org/dev/peps/pep-0328/) ），恍然大明白。



> Relative imports use a module's `__name__` attribute to determine that module's position in the package hierarchy. If the module's name does not contain any package information (e.g. it is set to '`__main__`') then relative imports are resolved as if the module were a top level module, regardless of where the module is actually located on the file system.



翻译过来就是：



> 1. 相对导入依赖于一个模块的`__name__`属性，根据这个属性去决定该模块在整个包中的层级结构。
>
> 2. 当一个模块的`__name__`属性不包含任何包信息时，如直接运行py脚本时，`__name__`会被设置成`__main__`，这时，不管这个文件位于包目录的哪个位置，相对导入机制会把当前脚本视为顶级模块。



这就意味着，**只要是我从终端运行python脚本，都会遇到`__name__`为`__main__`的问题，当前被运行的python脚本永远无法使用相对导入**。



现在在根目录下修改`main.py`，并在`b/b1`目录下创建`caller_proxy.py`。

```bash
.
├── a
│   └── callee.py
├── b
│   ├── b1
│   │   └── caller_proxy.py
│   └── caller.py
├── c
│   └── hello.py
└── main.py

```

`main.py`的内容如下：

```python
import sys

from c.hello import hi

print("__name__: {}, __package__: {}".format(__name__, __package__))

from b.b1 import caller_proxy

caller_proxy.proxy()
```



`caller_proxy.py`的内容如下：

```python
import sys
from .. import caller # 相对导入

print(__package__)

def proxy():
	print("------ caller_proxy.py ------")
	print("name: {}".format(__name__))
	caller.call()
```



该文件使用了相对导入，现在运行`./main.py`，结果如下。

```python
__name__: __main__, __package__: None
say hi~
------ caller_proxy.py ------
name: b.b1.caller_proxy
------ caller.py ------
name: b.caller
caller: caller
```



这时，`caller_proxy.py`执行时的`__name__`值是正常的包名结构`b.b1.caller_proxy`，因此可以使用相对导入`..`找到`b.caller`。

而`caller.py`执行时的包名结构是`b.caller`，因此，相对导入只能找到`b`包下的文件，所以，只能使用`from a.callee import caller_test`。



### 通常应该怎么做



为了避免一些奇奇怪怪的问题，还是比较推荐在`sys.path`数组追加要导入包绝对路径的方式。



```python
import os
import inspect
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(inspect.getfile(inspect.currentframe())), '../common')))

from utils import xxx_func
```



以之前的`caller.py`为例，想要调用`a/callee.py`，可以写成：

```python
import sys
import os

import inspect
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(inspect.getfile(inspect.currentframe())), '../a')))

from callee import caller_test

def call():
	print('------ caller.py ------')
	print("name: {}".format(__name__))

	caller_test()


if __name__ == '__main__':
	call()
```



这样就不用care是直接运行，还是用`-m`参数以模块去运行了，直接运行`./b/caller.py`，输出结果如下：

```bash
$ ./b/caller.py
------ caller.py ------
name: __main__
caller: caller
```

---

<p>

以上，就是之前处理Python import导入包时遇到的坑，简单记录。


![小黑杂说](https://raw.githubusercontent.com/wuruofan/wuruofan.github.io/master/img/qr-wechat-large.png)
