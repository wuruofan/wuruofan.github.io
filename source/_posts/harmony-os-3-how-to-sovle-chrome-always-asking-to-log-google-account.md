title: 鸿蒙3.0解决Chrome等应用登录账户无效的问题

date: 2023-04-16 20:30:00

index_img: https://raw.githubusercontent.com/wuruofan/image_repo/main/img/high%20quality%2C%204k%20resolution%2C%20girl%20look%20at%20sunset%20aboving%20reflecting%20water%2C%20crepuscular%20rays%2C%20digital%20art%2C%20art%20by%20monet.png

banner_img: https://raw.githubusercontent.com/wuruofan/image_repo/main/img/high%20quality%2C%204k%20resolution%2C%20girl%20look%20at%20sunset%20aboving%20reflecting%20water%2C%20crepuscular%20rays%2C%20digital%20art%2C%20art%20by%20monet.png

categories:

- 软件工具

tags:

- HarmonyOS
- GMS

---

# 鸿蒙3.0 解决Chrome应用登录账户无效的问题



## 问题现象



我一直用着华为Mate30手机，装了谷歌服务GMS，目前除了电池有些衰减，存储空间快用满了，其他都还好。

前段时间更新过一次系统，最近一周想在Chrome上找书签的时候发现**提示我“需要登录账户才可以同步”，等到输入账户之后，又告诉我“此账号已在您的设备上”。**



大概截图如下：

![此账号已在您的设备上](https://raw.githubusercontent.com/wuruofan/image_repo/main/img/harmony-os-3-chrome-google-account-already-login.jpg)





## 解决方法



这种现象在鸿蒙2.0升级3.0的时候遇到过一次，之前偶尔升级系统也遇到过，但不是Chrome。

方法很简单，记录下，以免下次忘记了。



### 1. 卸载Chrome并重新安装



⚠️**注意，卸载重新安装后，不要立刻打开应用！不要立刻打开应用！不要立刻打开应用！**



打开“设置 - 应用和服务 - 应用管理“，找到Chrome应用，点击”存储”，清除所有数据和缓存，这时候占用大概23MB左右。



> 这里因为是卸载重装，清除数据其实不是必须，记得之前有些版本有问题，保险起见清理一下。
>
> **其他一些谷歌应用，如果出现类似问题，可以先尝试不卸载，只做数据清理。**



### 2. 授予Chrome所有权限



还是在“应用管理”的Chrome设置页，点击”权限“，**授予全部权限！授予全部权限！授予全部权限！**



### 3. 重新启动Chrome应用



这是重启Chrome就会发现已经识别到了当前Play服务已经登录的账户信息，大功告成！

这时，第二步授予的权限可以酌情撤销。



![Chrome成功识别账户信息](https://raw.githubusercontent.com/wuruofan/image_repo/main/img/harmony-os-3-chrome-google-account-login-success.jpg)



<p>




以上，欢迎关注公众号“**小黑杂说**”。




![小黑杂说](https://raw.githubusercontent.com/wuruofan/wuruofan.github.io/master/img/qr-wechat-large.png)
