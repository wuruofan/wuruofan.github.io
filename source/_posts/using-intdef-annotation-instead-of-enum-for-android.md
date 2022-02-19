---
title: Android｜使用IntDef注解代替枚举类
date: 2022-02-19 23:30:00
index_img: https://raw.githubusercontent.com/wuruofan/image_repo/main/img/android-robot-logo.jpg

categories:
  - 技术总结
tags:
  - 技术总结
  - Android开发
  - 注解
  - Intdef
  - 枚举类
  - Java
---



## Java枚举类型的问题



枚举类型，理解起来还是比较容易的，通常用于维护有限个的常量元素，当一个变量的类型有几种可能的情况时，我们就用**枚举类型**将这些可能值“枚举”出来。



枚举类型，在C/C++中比较单纯，就是代表了一个整型值；而Java中，枚举类型是一个类，支持多态和各种扩展方法，有很多玩法和奇怪的实现，比如，用枚举类型实现的工厂模式等等。



Java中枚举类型支持的各种扩展，**带来的问题就是内存占用，其代码实现过于繁重。**



假如我只有一个维护三个常量元素的需求，如EnumTest.java中代码所示，我只需要三个常量MODE_A/B/C。



```java
// EnumTest.java
package com.rfw.androiddemo;

/**
 * Created by rf.w on 2022/2/15.
 */
class EnumTest {
    public enum EnumMode {
        MODE_A,
        MODE_B,
        MODE_C
    }
}
```



我们使用`java2smali`插件可以将此文件转换成对应的smali文件，这里会转换成两个文件：EnumTest.smali和EnumTest$EnumMode.smali，因为这里的`EnumMode`会被当作是内部类。



```smali
# EnumTest$EnumMode.smali部分内容
# ...

.annotation system Ldalvik/annotation/Signature;
    value = {
        "Ljava/lang/Enum",
        "<",
        "Lcom/rfw/androiddemo/EnumTest$EnumMode;",
        ">;"
    }
.end annotation


# static fields
.field private static final synthetic $VALUES:[Lcom/rfw/androiddemo/EnumTest$EnumMode;

.field public static final enum MODE_A:Lcom/rfw/androiddemo/EnumTest$EnumMode;

.field public static final enum MODE_B:Lcom/rfw/androiddemo/EnumTest$EnumMode;

.field public static final enum MODE_C:Lcom/rfw/androiddemo/EnumTest$EnumMode;

# ...
```



通过反编译后的smali代码可以看到，`EnumMode`类生成的签名类型其实是`java.lang.Enum<EnumTest.EnumMode>`；枚举类型中的每个变量，都会生成一个该类型的静态变量。



在`EnumTest.EnumMode`的静态代码块中会将变量名`MODE_A`和对应值，作为参数依次调用`java.lang.Enum`的构造函数；最后，构造了一个数组`VALUES`，存储这三个静态变量。



```smali
# EnumTest.EnumMode的静态代码块
# direct methods
.method static constructor <clinit>()V
    .registers 5

    .prologue
    const/4 v4, 0x2

    const/4 v3, 0x1

    const/4 v2, 0x0

		# 实例化MODE_A
    .line 8
    new-instance v0, Lcom/rfw/androiddemo/EnumTest$EnumMode;

    const-string v1, "MODE_A"

    invoke-direct {v0, v1, v2}, Lcom/rfw/androiddemo/EnumTest$EnumMode;-><init>(Ljava/lang/String;I)V

    sput-object v0, Lcom/rfw/androiddemo/EnumTest$EnumMode;->MODE_A:Lcom/rfw/androiddemo/EnumTest$EnumMode;

		# 省略MODE_B/C的实例构造 ...

		# 构造了一个数组存储三个实例
    const/4 v0, 0x3

    new-array v0, v0, [Lcom/rfw/androiddemo/EnumTest$EnumMode;

    sget-object v1, Lcom/rfw/androiddemo/EnumTest$EnumMode;->MODE_A:Lcom/rfw/androiddemo/EnumTest$EnumMode;

    aput-object v1, v0, v2

    sget-object v1, Lcom/rfw/androiddemo/EnumTest$EnumMode;->MODE_B:Lcom/rfw/androiddemo/EnumTest$EnumMode;

    aput-object v1, v0, v3

    sget-object v1, Lcom/rfw/androiddemo/EnumTest$EnumMode;->MODE_C:Lcom/rfw/androiddemo/EnumTest$EnumMode;

    aput-object v1, v0, v4

    sput-object v0, Lcom/rfw/androiddemo/EnumTest$EnumMode;->$VALUES:[Lcom/rfw/androiddemo/EnumTest$EnumMode;

    return-void
.end method

# 省略构造函数、valueOf与values方法...
```



虽然枚举类型具有很多好处，但在这个需求场景下，显然Java枚举类型实现的代价有点大了。



这里完全可以用三个静态整型值加边界值判断进行轻量级实现，但是恶心之处在于，所有使用到这三个值的地方，我可能都需要进行异常值判断，来保证程序的鲁棒性。



## IntDef注解

在这种情况下，Android提供的`IntDef`注解可以很好的解决枚举类型内存占用问题，可以说是一种更轻量级的“枚举功能”的实现。



官方文档地址：
[https://developer.android.com/reference/androidx/annotation/IntDef](https://developer.android.com/reference/androidx/annotation/IntDef)



其定义如下：

```java
@Retention(value = SOURCE)  @Target(value = ) annotation IntDef
```



官方文档对IntDef注解的说明如下：

> “Denotes that the annotated element of integer type, represents a logical type and that its value should be one of the explicitly named constants. If the IntDef#flag() attribute is set to true, multiple constants can be combined.”



翻译过来就是：

> “被IntDef注解修饰的整型表示一个逻辑上的类型，其值需是一系列定义的常量之一。如果IntDef#flag()属性设置为true，那么这些常量可以组合在一起使用。”



## IntDef使用方法



我们可以利用`IntDef`实现一个注解`Mode`，代码如下：



```java
// IntDefTest.java
class IntDefTest {
    public static final int MODE_A = 0;
    public static final int MODE_B = 1;
    public static final int MODE_C = 2;

    @IntDef({MODE_A, MODE_B, MODE_C}) // Mode注解定义取值范围
    @Retention(RetentionPolicy.SOURCE) // 声明Mode保留策略是源码级别
    public @interface Mode {}

    @Mode
    private static int sMode = MODE_A;

    @Mode
    public static int getMode() {
        return sMode;
    }

    public static void setMode(@Mode int mode) {
        sMode = mode;
    }
}
```



这里我们先声明了三个静态int常量，然后利用`IntDef`声明我们的`Mode`注解取值范围为`MODE_A`、`MODE_B`、`MODE_C`，以及`Retention`保留策略为只保留源码中、编译时删除。



在`setMode()`方法的参数中，我们用`@Mode`注解修饰参数，这样，在我们的正常编码过程中，一旦出现传入参数并不是`MODE_A`、`MODE_B`、`MODE_C`三个值其中之一的情况，Android Studio就会提示你，参数有问题以及正确的取值范围是什么。

另外，即使这里传入的参数是1，即`MODE_B`的值，Android Studio也会提示参数错误的。



![@Indef 传入参数](https://raw.githubusercontent.com/wuruofan/image_repo/main/img/20220219221905.png)





这样便用最简单的方法，满足了我们对枚举类型最基本的功能诉求。



最后，**值得注意的是，虽然这里IDE会提示参数错误，但是并不会影响代码的编译过程，还是可以编译成功的！**





## IntDef的flag属性



IntDef注解还有一个flag属性也很有用：当flag属性设置为true时，IntDef定义的值可以当作标志位，用`|`运算符组合使用。



修改之前`@Mode`注解的定义和各个模式的值如下：



```java
public static final int MODE_A = 1;
public static final int MODE_B = 1 << 1;
public static final int MODE_C = 1 << 2;

@IntDef(flag = true, value = {MODE_A, MODE_B, MODE_C}) // Mode注解定义取值范围，设置flag属性为true
@Retention(RetentionPolicy.SOURCE) // Mode注解保留策略是源码级别
public @interface Mode {}
```



这时，我们在调用`setMode()`的地方，便可以支持如下方式使用：



```java
IntDefTest.setMode(IntDefTest.MODE_A | IntDefTest.MODE_C);
```



## 最后



类似`IntDef`的还有`LongDef`、`StringDef`，使用的方法基本一致，其中`StringDef`不支持flag属性。



Android已经为我们提供了这么有用的注解，还不赶快用起来？



---

<p>


以上，欢迎关注公众号“**小黑杂说**”。




![小黑杂说](https://raw.githubusercontent.com/wuruofan/wuruofan.github.io/master/img/qr-wechat-large.png)
