---

title: 极速浏览器｜开发者教你自定义网页暗黑模式颜色

date: 2022-09-01 19:23:36

index_img: https://raw.githubusercontent.com/wuruofan/image_repo/main/img/360-lite-browser.png

categories:

  - 软件工具

tags:

  - 极速浏览器
  - 开发者设置
  - 自定义

---



## 写前面的废话

酷安好久没上了，搞内核太费精力，就一直拖欠着没看酷安的反馈，实在不好意思。



上个教程『[极速浏览器｜开发者教你自定义底部菜单](https://wuruofan.com/2022/07/31/how-to-custom-bottom-menu-of-360-lite-browser-by-developer/)』写了如何自定义底部菜单，当时的版本没法恢复默认设置，现在已经可以支持保存空白字符串恢复默认设置啦，有需要的小伙伴可以再尝试下。



之前看到酷安有同学反馈新的暗黑模式在Amoled屏幕显示灰蒙蒙的，看上去像是LCD屏幕，有点难受也不够省电。😂😂

其实，『开发者设置』里我留了一个设置网页暗黑模式调试的接口，今天简单教大家如何设置一下，方便Amoled屏手机同学使用全黑样式。





## 进入开发者设置



进入『开发者设置』有两种方法：



第一种，进入“设置” - “关于”页面，然后**连续、快速点击顶部标题栏**“关于360极速浏览器”，直到进入开发者设置页。



第二种，点击**地址栏或者首页搜索框**，输入`rfw://config`，即可进入。





## 设置内核主题颜色



开启『调试内核主题颜色』设置开关，之后就会看到『设置内核主题颜色』的设置项。



![开发者设置页](https://raw.githubusercontent.com/wuruofan/image_repo/c1906ef22c202e8882a0b0cae972bde7b117b122/img/360-lite-browser-settings-dev-activity.png)



点击之后，会弹出一个对话卡，这里列举了可以设置的6个选项，我们主要关注的几个设置是**背景颜色**、**文字颜色**、**超链接颜色**、以及**图片亮度**。



![设置内核主题颜色](https://raw.githubusercontent.com/wuruofan/image_repo/c1906ef22c202e8882a0b0cae972bde7b117b122/img/360-lite-browser-webview-color-config.png)



以之前提到的Amoled屏幕全黑背景的需求为例，这里我们只需要把`背景颜色`一栏设置为`#000000`即可。



![设置网页全黑背景](https://raw.githubusercontent.com/wuruofan/image_repo/main/img/360-lite-browser-webview-black-background.gif)



关于颜色值可以去百度上搜索“网页颜色代码”类似关键字，找你满意的背景或文字颜色。**这里支持的颜色代码可以是6位不带透明度的颜色代码，也可以是8位带透明度的颜色代码。**



**注意**：目前这个接口支持调试网页上的颜色，还没法调整其他控件的颜色。



关于`渐变颜色亮度`，就是网页上的有些渐变会采用降低亮度的方式处理，这里后期可能会改；`边框颜色`看代码应该适合表格边框有关系，这两项可以暂时忽略。



## 最后

后期我想重写下强制暗黑的逻辑，现在统一替换背景色有点粗暴，会导致网页上很多层次和颜色丢失，还得看看有没有更好的方案。



希望大家多多支持极速浏览器！🙏



<p>

---

<p>



以上，欢迎关注公众号“**小黑杂说**”。




![小黑杂说](https://raw.githubusercontent.com/wuruofan/wuruofan.github.io/master/img/qr-wechat-large.png)

