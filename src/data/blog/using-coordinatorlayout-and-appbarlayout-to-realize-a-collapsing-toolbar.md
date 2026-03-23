---
title: Android｜CoordinatorLayout+AppBarLayout实现可折叠工具栏
pubDatetime: 2023-02-01T20:20:00Z
modDatetime: 2023-02-01T20:20:00Z
heroImage: ...
description: Android｜CoordinatorLayout+AppBarLayout实现可折叠工具栏
draft: false
tags:
  - 技术总结
  - 开发记录
  - Android开发
  - CoordinatorLayout
  - AppBarLayout
  - CollapsingToolbarLayout
categories:
  - 技术总结
---
## 需求背景

22年12月中旬的时候，由于其他迭代缺人，让我支援一下，其中有个页面的需求如下，要求实现一个可折叠效果的信息展示卡片，实现完大概就是下面动图的效果。

![折叠效果](https://raw.githubusercontent.com/wuruofan/image_repo/main/img/collapsing-toolbar-animation.gif)



查了下资料，其实就是Android Studio里ScrollingActivity那个模版里的效果，大概如下，也可以扩展实现很多更高级的样式，比如B站视频播放页面视频上划折叠的效果。



![ScrollingActivity效果](https://raw.githubusercontent.com/wuruofan/image_repo/main/img/scrolling-activity-collapsing-toolbar-sample.webp)





其实信息展示卡片随着划动折叠，还有别的方法，为了防止后面产品有奇怪的需求，就选择了ScrollingActivity的实现方案。





## 实现方案

方案其实也不难，我也不太擅长写界面，也是我第一次使用`CoordinatorLayout`布局。这里使用了`CoordinatorLayout`、`AppBarLayout`和`CollapsingToolbarLayout`，然后使用默认提供的`appbar_scrolling_view_behavior`进行实现的。





### 界面布局



主要通过xml布局文件进行适配即可，真正的代码量倒是不多，大概拆一下布局，如下。



![布局示意图](https://raw.githubusercontent.com/wuruofan/image_repo/main/img/collapsing-toolbar-layout.png)

整体是个`CoordinatorLayout`，coordinator翻译过来就是“协调员”的意思，个人理解，它**通过`behavior`协调其中各个`View`的展示。**



上面的部分整体是`AppBarLayout`，里面包裹着一个`CollapsingToolbarLayout`和一个`XTabLayout`。



最下面是个`ViewPager`，承载着一个`Fragment`，里面有一个`RecyclerView`，需要设置ViewPager的属性：`app:layout_behavior="@string/appbar_scrolling_view_behavior"`。



主体的xml文件大致如下：

```xml
<?xml version="1.0" encoding="utf-8"?>
<android.support.design.widget.CoordinatorLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="@color/white"
    android:orientation="vertical"
    tools:context=".activity.MineActivity">

    <android.support.design.widget.AppBarLayout
        android:id="@+id/app_bar"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="vertical">

        <android.support.design.widget.CollapsingToolbarLayout
            android:id="@+id/collasping_toolbar"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:minHeight="44dp"
            app:layout_scrollFlags="scroll|exitUntilCollapsed">

            <!-- 此处是作者信息相关的布局 -->

          	<!-- 此处是标题栏的布局 -->

        </android.support.design.widget.CollapsingToolbarLayout>

        <com.androidkun.xtablayout.XTabLayout
            android:id="@+id/mine_tab_layout"
            android:layout_width="match_parent"
            android:layout_height="39dp"
            android:layout_marginBottom="1dp"
            app:layout_collapseMode="pin"
            app:xTabIndicatorColor="#0079ff"
            app:xTabIndicatorWidth="20dp"
            app:xTabIndicatorHeight="2dp"
            app:xTabPaddingEnd="20dp"
            app:xTabPaddingStart="20dp"
            app:xTabIndicatorRoundX="1dp"
            app:xTabIndicatorRoundY="1dp"
            app:xTabMode="scrollable"
            app:xTabSelectedTextColor="@color/c2_2"
            app:xTabSelectedTextSize="16dp"
            app:xTabTextBold="false"
            app:xTabTextColor="@color/c07"
            app:xTabTextSelectedBold="true"
            app:xTabTextSize="16dp" />

    </android.support.design.widget.AppBarLayout>

    <android.support.v4.view.ViewPager
        android:id="@+id/mine_view_pager"
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        app:layout_behavior="@string/appbar_scrolling_view_behavior" />
</android.support.design.widget.CoordinatorLayout>
```





### 属性设置



一开始我也有点晕，后来发现很简单，**根据用户操作滚动的控件**需要设置`layout_behavior`，需要**根据用户滚动事件进行变化的控件**放到`AppBarLayout`里，**需要进行折叠的部分**放到`CollapsingToolbarLayout`中，相应的**触发场景**需要配置`app:layout_scrollFlags`，定制折叠样式需要配置`app:layout_collapseMode`。



这里`CollapsingToolbarLayout`设置了最小高度`minHeight`，`layout_scrollFlags`设置为`scroll|exitUntilCollapsed`，意味着“**此布局和滚动时间关联**，且**在滚动到达这个最小高度的时候开始折叠**“。



被折叠的控件设置了`layout_collapseMode`属性为`parallax`，意味着“**当触发折叠时，此控件会有视差折叠效果**”，`layout_collapseParallaxMultiplier`系数设置为0.5，可以自行调节。



对于在折叠过程中不希望被隐藏的控件，需要设置`layout_collapseMode="pin"`，这样就会出现`XTabLayout`**吸顶**的效果了。



> 具体更详细的属性设置，可以参考下面的链接：[https://www.jianshu.com/p/06c0ae8d9a96](https://www.jianshu.com/p/06c0ae8d9a96)



### 设置监听事件



由于这里需要在工具栏完全折叠的时候在标题展示作者名字和关注按钮，还需要在代码里设置监听事件。



```java
// 设置监听
mAppBarLayout.addOnOffsetChangedListener(new AppBarStateChangeListener() {
  @Override
  public void onStateChanged(AppBarLayout appBarLayout, State state) {
    if (state == State.COLLAPSED) {
      showTitleBarUserInfo(true);
    } else {
      showTitleBarUserInfo(false);
    }
  }
});

// 监听实现
public abstract class AppBarStateChangeListener implements AppBarLayout.OnOffsetChangedListener {

  public enum State {
    EXPANDED,
    COLLAPSED,
    IDLE
  }

  private State mCurrentState = State.IDLE;

 /**
  * Called when the {@link AppBarLayout}'s layout offset has been changed. This allows
  * child views to implement custom behavior based on the offset (for instance pinning a
  * view at a certain y value).
  *
  * @param appBarLayout the {@link AppBarLayout} which offset has changed
  * @param verticalOffset the vertical offset for the parent {@link AppBarLayout}, in px
  */
  @Override
  public final void onOffsetChanged(AppBarLayout appBarLayout, int verticalOffset) {
    if (verticalOffset == 0) {
      if (mCurrentState != State.EXPANDED) {
        onStateChanged(appBarLayout, State.EXPANDED);
      }
      mCurrentState = State.EXPANDED;
    } else if (Math.abs(verticalOffset) >= appBarLayout.getTotalScrollRange()) {
      if (mCurrentState != State.COLLAPSED) {
        onStateChanged(appBarLayout, State.COLLAPSED);
      }
      mCurrentState = State.COLLAPSED;
    } else {
      if (mCurrentState != State.IDLE) {
        onStateChanged(appBarLayout, State.IDLE);
      }
      mCurrentState = State.IDLE;
    }
  }

  public abstract void onStateChanged(AppBarLayout appBarLayout, State state);
}
```



这里监听的其实是AppBarLayout的`onOffsetChanged`事件，垂直偏移量`verticalOffset`改变时就会回调这个方法，当AppBarLayout展开时`verticalOffset`的值为0，折叠过程中`verticalOffset`为一个**负值**，其绝对值小于`appBarLayout.getTotalScrollRange()`。



### 其他注意



1. `AppBarLayout`的父类是`LinearLayout`，写布局时需要注意方向。

2. `CollapsingToolbarLayout`的父类是`FrameLayout`，写布局时需要**注意控件的添加顺序**，避免折叠时控件显示层级的问题。



## 问题：Theme.AppCompat 错误



写完布局的时候，run的时候遇到了一个错误：“**The style on this component requires your app theme to be Theme.AppCompat (or a descendant)**”，有点奇怪。



大致错误如下：

```
Caused by: android.view.InflateException: Binary XML file line #100 in xxx_layout: Binary XML file line #100 in xxx_layout: Error inflating class com.google.android.material.XXX
Caused by: android.view.InflateException: Binary XML file line #100 in xxx_layout: Error inflating class com.google.android.material.XXX
Caused by: java.lang.reflect.InvocationTargetException
        at java.lang.reflect.Constructor.newInstance0(Native Method)
        ...
Caused by: java.lang.IllegalArgumentException: The style on this component requires your app theme to be Theme.AppCompat (or a descendant).
```



是在初始化界面解析xml布局文件时出错了，错误大概的原因是，当前Activity用了Material Design控件，但是Activity的theme并不是Material Design。                                                                            



### 解决方法



很简单，实现一个`Theme.AppCompat`的style就行了，具体颜色看情况即可。



```xml
<style name="WithAppBarTheme" parent="@android:style/Theme.Material.Light.NoActionBar">
  ...
  <!--添加下面三个名称的颜色(颜色值随便)，样式满足Theme.AppCompat-->
  <item name="colorPrimary">#ffffff</item>
  <item name="colorPrimaryDark">#000000</item>
  <item name="colorAccent">#AAAAAA</item>
</style>
```



### 兼容问题：Vivo安卓7崩溃



在实际测试的过程中发现，在Vivo X9 7.1.2系统进入作者/个人页退出会出现系统的onResume崩溃，无法处理，错误堆栈如下：



```java
E/VivoSystemReflect: Failure register UserProfilingManager
java.lang.ClassNotFoundException: com.vivo.services.userprofiling.UserProfilingManager
     at java.lang.Class.classForName(Native Method)
     at java.lang.Class.forName(Class.java:400)
     at java.lang.Class.forName(Class.java:326)
     at android.app.VivoSystemReflect.getServiceConstructor(VivoSystemReflect.java:461)
     at android.app.VivoSystemReflect.-wrap0(VivoSystemReflect.java)
     at android.app.VivoSystemReflect$6.createService(VivoSystemReflect.java:446)
     at android.app.SystemServiceRegistry$CachedServiceFetcher.getService(SystemServiceRegistry.java:858)
     at android.app.SystemServiceRegistry.getSystemService(SystemServiceRegistry.java:799)
     at android.app.ContextImpl.getSystemService(ContextImpl.java:1518)
     at android.content.ContextWrapper.getSystemService(ContextWrapper.java:659)
     at android.app.Application.getVivoUserProfilingManager(Application.java:327)
     at android.app.Activity.onResume(Activity.java:1287)
     at android.support.v4.app.FragmentActivity.onResume(FragmentActivity.java:514)
     at com.qihoo.browser.activity.ActivityBase.onResume(ActivityBase.kt:117)
     at android.app.Instrumentation.callActivityOnResume(Instrumentation.java:1276)
     at android.app.Activity.performResume(Activity.java:6963)
     at android.app.ActivityThread.performResumeActivity(ActivityThread.java:3469)
```



页面是可以进入使用的，功能也都正常，但是退出回到上一页面时就触发崩溃，很恼火。经过测试发现是`WithAppBarTheme`的原因，应该是Vivo 7系统做了什么魔改，导致兼容问题，测试了后面的几个版本都没有问题。

这个问题我暂时没有什么好办法处理，只能针对这一类别设备做了一个没有AppBarLayout的布局文件，改为`Acitivity.onCreate()`时动态设置theme，在AppBarLayout使用的地方使用非空判断！



```java
public static boolean isEvilVivoDevice() {
  return "vivo".equals(Build.MANUFACTURER) && Build.VERSION.RELEASE.startsWith("7.");
}

@Override
protected void onCreate(@Nullable Bundle savedInstanceState) {
  if (!AndroidUtil.isEvilVivoDevice())
    setTheme(R.style.WithAppBarTheme); // 需要在super.onCreate之前设置Theme

  super.onCreate(savedInstanceState);
  // ...
}
```



注意，这里需要在super.onCreate之前设置Theme。




## 最后

这里简单记录了下如何使用`CoordinatorLayout`和`AppBarLayout`去实现折叠工具栏，第一次使用，还挺有意思。



其实，本来还打算写一个开发中遇到的“坑”，写了一半去分析源码时，越分析越不对劲，分析了两天，结果发现是自己的问题，感觉自己是个智障🤣🤣🤣🤣🤣🤣，不过分析的过程对`CoordinatorLayout`测量和绘制的流程理解更深刻了一点，下次单独再写吧。




最后的最后，兔年第一篇文章，祝大家都“**💰🐰无量**”～


<p>



---

<p>





以上，欢迎关注公众号“**小黑杂说**”。




![小黑杂说](https://raw.githubusercontent.com/wuruofan/wuruofan.github.io/master/img/qr-wechat-large.png)