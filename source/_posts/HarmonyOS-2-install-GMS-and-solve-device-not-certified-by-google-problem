
---
title: 鸿蒙OS 2.0安装谷歌服务框架 & 解决设备未经Play认证问题
date: 2021-10-18 16:00:00
index_img: https://raw.githubusercontent.com/wuruofan/image_repo/main/img/Huawei-GMS.jpg
banner_img: https://raw.githubusercontent.com/wuruofan/image_repo/main/img/Huawei-GMS.jpg
categories:
  - 避坑指北
tags:
  - 避坑指北
  - 遇坑总结
  - 鸿蒙OS
  - 安装GMS
  - 此设备未经过Play认证

---

## 前情

由于美国对华为的制裁，谷歌不再为华为设备提供服务，导致华为手机安装Google服务框架和Google Play商店会遇到各种问题。这种情况，已经安装GMS服务的手机并不会受到影响，可以继续使用。

同时，谷歌也不再为华为新款设备提供认证，会导致新款手机以及鸿蒙OS即使安装上了Google服务框架也会提示“此设备未经过Play认证”，无法使用Chrome、Gmail、日历等程序。



我的Mate30手机去年安装的Google服务框架，一直使用正常，最近几天开始出现“此设备未经过Play认证”的提示，一打开Chrome就闪退了。尝试了很多方法都不行，最后卸载所有组件重新安装才解决问题，记录下过程。



![此设备未经过Play认证](https://raw.githubusercontent.com/wuruofan/image_repo/main/img/device_not_certified_by_google.jpg)



整篇文章涉及的视频和所使用的软件工具，我一并上传到360云盘上：

> https://yunpan.360.cn/surl_yM3C9aCLah5 提取码：0a8a



## 环境

手机：华为Mate30手机，鸿蒙OS2.0系统

网络：轻快VPN（[https://qingkuai.org/#/register?code=2LEPMSrc](https://qingkuai.org/#/register?code=2LEPMSrc)）



如果之前有安装过谷歌服务框架，但是遇到和小黑一样的问题，最好卸载之前安装的GMS服务。

进入“设置 - 应用与服务 - 应用管理”，搜索栏输入“Google”，然后右上角菜单键“显示系统程序”，卸载Google服务框架、Google Play服务、Google通讯录同步等应用。

注意：“谷歌安装助手”应用可以不用卸载，因为重新安装的第一步就是要装这个软件。



## 安装GMS

我安装时候参考的是Youtube上 @工匠先森 的一个视频：[https://www.youtube.com/watch?v=0bMesV_en3M](https://www.youtube.com/watch?v=0bMesV_en3M)，教程中涉及的操作有一小部分需要在电脑端进行操作，绝大部分手机即可。



> 这一步骤涉及的文件如下：
>
> 1. 01-华为手机鸿蒙2.0系统Ha...40 Mate30荣耀v30.mp4
> 2. 01a-电脑端.zip，
> 3. 01b-手机端.zip



### 电脑端操作

主要就是使用adb工具，**卸载鸿蒙OS新版的“备份”APP，并安装旧版本“备份”APP。**

其目的就是为了后面可以使用旧版本“备份”APP恢复特殊版本备份的“谷歌安装助手”。



按照视频中的操作即可，`01a-电脑端.zip`解压后包括了adb工具和一个包含命令的txt文档。

这一步操作，其实可以写一个bat批处理脚本，双击一键完成。回头我补上。



### 手机端操作

下载`01b-手机端.zip`到手机，用自带“文件管理”解压即可。



#### 1. 通过“备份”APP恢复“谷歌安装助手”

按照视频操作一步步完成即可。

1. 将解压出来的`Huawei`目录拷贝到手机内部存储目录；
2. 点击“设置 - 系统与更新 - 备份与恢复”，进入后授予权限，返回退出，然后再次进入，右上角点击菜单，选择本机备份文件，恢复即可。
3. 返回桌面，找到“谷歌安装助手”，激活设备管理器，点击下载，回到桌面。



#### 2. 安装Googlefier

打开之前解压出来的`GMS`目录，安装Googlefier软件，这是一个半自动化的安装Google服务所需要的软件。



Googlefier的主界面用01、02、03等图片标注了安装顺序，01是添加Google账户、02是添加更多账户、03是安装一系列Google服务所需软件；大部分用户用到的只有01、03两个步骤。

1. 点击01，安装`MiCrOG - HUAWEI FIX ElOyGomezTV`软件并运行，添加Google账号
2. 点击03，半自动化安装所有需要安装的软件一系列
3. 卸载01步骤安装的`MiCrOG - HUAWEI FIX ElOyGomezTV`。



#### 3. 卸载重装Google通讯录同步、Google Play服务

卸载Googlefier默认安装的Google通讯录同步和Google Play服务软件，安装解压出来`GMS`目录中的对应软件即可。

1. 点击“设置-用户账户-google-同步联系人” 打开，此时会同步失败。
2. 点击“设置-应用与服务 - 应用管理”，搜索栏输入google，右上角菜单点击“显示系统程序”，卸载。
3. 重新安装`GMS`目录中的两个软件




## 解决“此设备未获得Play授权”弹窗和通知问题

参考视频：[https://www.youtube.com/watch?v=XAk2nYNDfMU](https://www.youtube.com/watch?v=XAk2nYNDfMU)

> 涉及文件：
> 1. 02-谷歌商店保护机制弹窗问题，华为mate40promate30手机解决谷歌商店保护机制弹窗问题转载John Wang.mp4
> 2. 02-DeviceID.apk：用于获取手机的内部谷歌服务框架特征值，用于将当前手机在线注册成自定义ROM。

![DeviceID应用](https://raw.githubusercontent.com/wuruofan/image_repo/main/img/device_id.jpg)



### 操作步骤

1. 安装并运行`02-DeviceID.apk`。
2. 复制界面上GSF ID（第二行），打开[g.co/AndroidDeviceRegistration](g.co/AndroidDeviceRegistration)，在线注册设备。
3. 打开飞行模式断网。
4. 第一次清除数据，“设置 - 应用与服务 - 应用管理”，搜索Google，右上角点击菜单选择“显示系统程序”。
   1. 点击“Google服务框架”，点击“存储 - 清理数据”，后退并点击“停止运行”，直到按钮变成灰色。
   2. 点击“Google Play服务”，点击“存储 - **清理缓存**”，后退并点击“停止运行”，直到按钮变成灰色。
   3. 点击“Google Play商店”，点击“存储 - 清理数据”，后退并点击“停止运行”，直到按钮变成灰色。
5. 重启手机。
6. 第二次清除数据，“设置 - 应用与服务 - 应用管理”，搜索Google。
  1. 点击“Google Play服务”，点击“存储 - **管理空间 - 清除所有数据**”，后退并点击“停止运行”，直到按钮变成灰色。
7. 重启手机。
8. 关闭手机飞行模式，打开VPN网络，应该就可以正常使用了。



---

<p>

以上，欢迎关注公众号“**小黑杂说**”。


![小黑杂说](https://raw.githubusercontent.com/wuruofan/wuruofan.github.io/master/img/qr-wechat-large.png)
