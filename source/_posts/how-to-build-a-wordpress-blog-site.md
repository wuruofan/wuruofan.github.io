---
title: VPS搭建WordPress博客全记录
tags:
  - build a website
  - lnmp
  - vps
  - wordpress
id: '228'
categories:
  - - 技术总结
date: 2020-04-11 11:44:45
---

之前小黑在半闲置的`VPS`（Virtual Private Server虚拟专用服务器）上搭了个WordPress博客“小黑杂说”（[wuruofan.com](wuruofan.com)），记录下这次建站的大致过程。

总的来说，建站本身并不是很难的一件事情，相比之下，找到建站的理由、搞清楚为何而“站”这件事，其实更难一些。

就我个人来说，除去人生阶段的转换带来的紧迫感、动力和反思之外，最近在读的几本书（《mactalk：人生元编程》、《前方的路》、《Google工作整理术》、《程序员的成长课》、《程序员必读的职业规划书》）也让我有了搭建一个个人主页的想法。当然，小伙伴的离职、项目上的压力、原领导的调动，这些事情也是一部分促因吧。

正如《Google工作整理术》一书中所说，我现在相信“**知识不是力量，共享知识才是力量**”。

### 0x00 开始之前

由于之前我在[Vultr](vultr.com)上已有一个半闲置的VPS主机，选的是最便宜那种，3.5刀/月、10 GB SSD存储、单核vCPU、512 MB内存、500GB带宽的贫穷配置，之前操作系统为CentOS 7 x64。

Vultr性价比较高，支持支付宝，按小时计费，全球机房，迁移机房和[搬瓦工](bandwagonhost.com)相比似乎收费的，新人优惠送的金额可以用来多建几个VPS试试IP是否存在异常情况（you know why），免费快照记得可以用来迁移虚拟主机的机房，会比直接使用迁移机房功能便宜。当然十分欢迎使用我的[邀请链接](https://www.vultr.com/?ref=8432644-6G "vultr邀请链接")。

### 0x01 LNMP

与`LNMP`相对应的是`LAMP`，都是主流的搭建网站的开源Web框架。

> LNMP = Linux+Nginx+Mysql+PHP
> 
> LAMP = Linux+Apache+Mysql+PHP

不同点就在于`Nginx`和`Apache`之间。Apache可以说是传统主流服务器选项，“老大哥”，时至今日仍是世界上使用排名第一的服务器软件，详细数据见[Comparison of the usage statistics of Apache vs. Nginx vs. Microsoft-IIS for websites](https://w3techs.com/technologies/comparison/ws-apache,ws-microsoftiis,ws-nginx "Comparison of the usage statistics of Apache vs. Nginx vs. Microsoft-IIS for websites")。稳定、擅长处理动态请求、模块众多，Apache是负载PHP的Web服务器最佳选择。

和`Nginx`相比最大的区别就在于响应请求时`Apache`是同步，而Nginx是异步处理。因此，在处理高并发请求时，Nginx消耗的资源更少，响应更快。这也是其设计的初衷之一。轻量级、善于处理静态请求、支持反向代理等这些都是Nginx的优点。

但是对我来说，消耗的资源少这一点就足够了。毕竟只是个个人博客，毕竟自己是个乞丐版的VPS。（是的，真的是这样子的，LAMP的一键安装脚本竟然编译出错，好像是内存不足，我还特意配置了swap分区。苦涩。ðððð）

#### 0x01a LNMP安装

我选择的是一键安装脚本，过程详细参见其主页[lnmp.org](https://lnmp.org/)。

由于安装时间过长，通常ssh登录VPS会因为网络波动断开连接，强烈建议使用`screen`工具进行安装。详细参见[screen教程](https://www.vpser.net/manage/screen.html "screen教程")。

Screen是一个可以在多个进程之间多路复用一个物理终端的全屏窗口管理器。Screen中有会话的概念，我们这里利用的就是会话的保存恢复功能。

1.  首先，使用`screen -S lnmp` 创建名为`lnmp`的screen会话，一旦网络断开重连，可以使用`screen -r lnmp`进行恢复。
  
2.  然后，下载并执行安装脚本。
  

```
wget http://soft.vpser.net/lnmp/lnmp1.7.tar.gz -cO lnmp1.7.tar.gz && tar zxf lnmp1.7.tar.gz && cd lnmp1.7 && ./install.sh lnmp
```

3.  之后一路默认选项安装，除了在`MySQL`安装时需要设置默认数据库`root`账户的密码（需牢记）之外，还有几点不太一样。
    *   `PHP`选择`7`以上版本，目的和WordPress兼容，暂时不要选择`7.4.4`版本，目前（2020年4月）最新WordPress有些问题。
    *   最后会提示是否安装`Memory Allocator`，PHP的内存分配插件，这个我好像随便选了一个，忘记了ð¤¦，可能是`Jemalloc`。这里选默认不安装也没关系，可以之后使用插件脚本按需安装。

然后，就是漫长的等待，大概20分钟，安装完成后终端会输出安装信息和运行信息。若是看到

```
Nginx: OK
MySQL: OK
PHP: OK
PHP-FPM: OK
```

和各个服务`is running`就说明安装成功了。这是浏览器地址栏输入VPS的IP地址应该就会显示一个`LNMP一键安装包`的介绍页面，这个页面的相关内容在目录`/home/wwwroot/default/`。

#### 0x01b 插件安装

在执行上面第二条命令的目录下生成`lnmp1.7`目录，目录中有个名为`addons.sh`的脚本，用于安装PHP相关插件。安装或卸载命令如下：

```
./addons.sh {installuninstall} {eacceleratorxcachememcachedopcacheredisapcuimagemagickioncube} 
```

我安装了缓存插件`memcached`。执行`./addons.sh install memcached`，然后 选择 2 （`php-memcached`），等待安装成功即可。

#### 0x01c 其他命令

在其官网和[GitHub README说明](https://github.com/licess/lnmp/blob/master/readme.md "LNMP on GitHub")中都有一些管理命令，常用摘录如下。

```
LNMP/LNMPA/LMAP状态管理：lnmp {startstopreloadrestartkillstatus}

Nginx状态管理：lnmp nginx或/etc/init.d/nginx {startstopreloadrestart}

MySQL状态管理：lnmp mysql或/etc/init.d/mysql {startstoprestartreloadforce-reloadstatus}

MariaDB状态管理：lnmp mariadb或/etc/init.d/mariadb {startstoprestartreloadforce-reloadstatus}

PHP-FPM状态管理：lnmp php-fpm或/etc/init.d/php-fpm {startstopquitrestartreloadlogrotate}

PureFTPd状态管理：lnmp pureftpd或/etc/init.d/pureftpd {startstoprestartkillstatus}
```

### 0x02 域名申请与绑定

我个人名字的域名是在`GoDaddy`上申请的，因为印象中这是最大的域名托管平台，后来才知道还有一个[NameSilo](https://www.namesilo.com)，国内就选阿里的万网或者腾讯云之类的，只不过国内域名申请需备案，而我懒得折腾。而且GoDaddy这个域名我总觉得有娃在后面督促我努力工作。

GoDaddy一般都有优惠，但是这个网站似乎有点杀熟的倾向。比如你在上面搜索过几次心仪的域名，有可能会出现域名地址价格不相同的情况，可能会越来越贵，比如我的域名有一天半夜2点哄睡娃去搜是第一年20元、第二年100+；白天我再去搜索价格就变化了，而且一旦你使用了别的网站提供的优惠折扣信息，cookies里似乎会存储相关数据，这样价格一直就是别人折扣码的价格了，你只能用无痕模式/隐私模式重新登陆，才能看到最初的优惠价格。总之，十分迷。

不管怎么样，选择好了域名后，可以选择支付宝支付，还算比较方便。

上一步中完成了`LNMP`的安装，已经可以在浏览器里访问VPS的IP地址了，我们可以在GoDaddy的管理界面绑定IP和域名。

登陆GoDaddy管理界面，点击`DNS`进入域名解析管理界面，点击`ADD`添加一条DNS信息，这里选择`Type`为`A`，即IP指向，`Host`填之前购买的域名，`Points to`填VPS的IP地址，`TTL`默认缓存时间为1小时，然后点击`SAVE`即可。一般1～2分钟即可生效。

建议添加两条，同时保证无www前缀的网址和有www前缀网址的访问，以防遇到和我一样在更新Let's Encrypt证书时遇到DNS解析失败的问题。

| 类型  | 名称 |   值   |   TTL    |
| :---: | :--: | :----: | :------: |
|   A   |  @   | vps ip | 1/2 小时 |
| CNAME | www  |   @    | 1/2 小时 |

其中`@`表示无www前缀的域名，`www`表示完整域名，意思就是添加一条`A`记录 将域名指向你的vps ip地址，然后添加了一个`CNAME`别名，指向完整域名。

这样就完成域名的绑定工作。现在浏览器输入域名应该就可以显示上一步LNMP安装成功后的网页了。关于添加DNS时，Type一栏里的`A`（IP指向）、`CNAME`（别名指向）、`NS`（域名解析记录）等不同类别的区别可以参见网页[DNS域名解析中A、AAAA、CNAME、MX、NS、TXT、SRV、SOA、PTR各项记录的作用](https://itbilu.com/other/relate/EyxzdVl3.html "DNS域名解析中A、AAAA、CNAME、MX、NS、TXT、SRV、SOA、PTR各项记录的作用")。

### 0x03 WordPress安装

#### 0x03a 添加虚拟主机

在WordPress安装之前，我们还需要向LNMP添加虚拟主机，配置LNMP相关设置。

执行`lnmp vhost add`完成相关操作，按提示输入：

*   主机域名（wuruofan.com/www.wuruofan.com）
*   网站文件默认存储路径（使用默认/home/wwwroot/wuruofan.con/即可）
*   选择是否使用rewrite规则（使用，并设置默认rewrite规则为wordpress）
*   是否使能PHP pathinfo功能（y）
*   是否使用访问日志（y）和默认位置（默认即可）
*   是否创建MySQL数据库和同名管理员账户（我这里选择了n，后面我会自己创建，如果没有特殊需求可以按提示选y）
*   是否添加SSL证书（y，然后选择2，使用`Let's Encrypt`提供的SSL证书，这里会影响后面的全站https）

之后按回车等待安装完成即可。

#### 0x03b MySQL数据库创建

在命令行输入`mysql -u root -p`，按照提示输入数据库root账户密码登陆。

然后执行`create database wordpress;`创建名为wordpress的数据库，创建成功会出现如下提示。

```
mysql> create database wordpress;
Query OK, 1 row affected (0.01 sec)
```

最后输入`exit`退出数据库管理程序。

> **注意**： 如果不小心，像小黑后来一样忘记了`mysql`数据库的`root`密码，重试了一下午也没试出来，不妨看看`/home/wwwroot/www.xxxx.com/wp-config.php`。

#### 0x03c 安装WordPress

下面才是真正的WordPress安装过程，也就是著名的5分钟安装。

*   创建网站目录

```
cd /home/wwwroot/
mkdir www.wuruofan.com
```

*   下载最新安装包并解压

```
# 回到home目录
cd ~

# 获取最新安装包
wget https://cn.wordpress.org/latest-zh_CN.tar.gz

# 解压到当前目录
tar -zxvf latest-zh_CN.tar.gz

# 将解压后文件内容移动到网站根目录下
mv wordpress/* /home/wwwroot/wuruofan.com/

```

这里以防后面可能会出现的乱七八糟权限问题，还需要修改网站根目录的读写权限和用户归属。

```
# 修改网站根目录的读写权限（所有人可读可访问、仅所有者可以更改）
chmod -R 755 /home/wwwroot/www.wuruofan.com/

# 修改网站根目录所有者为www用户组
chown -R www /home/wwwroot/www.wuruofan.com/
```

这里可能会提示，`.user.ini`文件的权限和用户无法修改，需要执行`chattr -i /home/wwwroot/www.wuruofan.com/.user.ini`，修改该文件为可修改，再执行上面操作即可。

*   配置你的网站

这时已经可以通过浏览器输入域名去执行下一步的配置工作。

这时你需要准备好之前创建的数据库信息，再网站页面配置数据库名、数据库用户、数据库密码、表名等信息。

根据提示输入信息即可，最后会跳转页面，输入网站名称、账户名称、密码等信息，之后就大功告成，你也拥有了一个个人博客站点了！

### 0x04 其他

#### 0x04a 全站HTTPS

简单的推荐使用插件`Really Simple SSL`。注意，**一定要搭建完成后先做**，不然会遇到一些奇奇怪怪的问题！会影响google/baidu的站点收录。

比如已发表的博客上的多媒体资源链接默认是http的，如果你先发表博客然后再做全站https的操作，就会出现`mixed content errors`错误，通常解决方案就是通过搜索替换数据库中http相关内容去解决，可以用插件`Better Search Replace`或者`SSL 不安全内容修复器`去解决。

我当时配置全站HTTPS的时候绕了点弯路，手工配置的，简直头秃，推荐阅读[How to Properly Move WordPress from HTTP to HTTPS (Beginner's Guide)](https://www.wpbeginner.com/wp-tutorials/how-to-add-ssl-and-https-in-wordpress/ "How to Properly Move WordPress from HTTP to HTTPS (Beginner's Guide")，文章介绍了使用插件和手工配置两种方式。

#### 0x04b 主题选择

WordPress的主题茫茫多，本着简洁就是美和能少设置一项是一项（懒）的原则，我选择了MDx主题[MDx：轻于形，悦于心](https://mdx.flyhigher.top/ "MDx：轻于形，悦于心")，这是一款采用Material Design 风格 WordPress 主题，必须给个好评。

除了好看之外，主题还自带了移动端网页、夜间模式切换、延迟加载、SEO设置、ImageBox、微信微博等社交媒体分享图片生成等等，但是也带来一些意想不到的问题，主要原因是会和WordPress一些插件的功能冲突。

比如MDx主题自带的Lazyload功能和WordPress官方的Jetpack插件中的相关功能可能会有冲突，从而导致页面上的图片显示不太正常，我把Jetpack里的功能关闭了，记得当时生成分享到社交媒体的二维码图片时遇到过图片无法显示的问题，好像就是这个原因；还有SEO设置，如果有其他插件，就不要在主题设置里去配置了。

MDx主题里有些特别细小的点，我很喜欢，比如页脚格言，可以使用一言API。

#### 0x04c 文末版权声明

通常我们在其他网站看帖子的时候总会看一些版权声明，建议大家也加上。在WordPress的设置里可以加，我选择在MDx主题的`文末信息`里添加如下HTML代码。

```
<div class="open-message"  style="border:#eeeeee 1px solid;border-radius:5px 5px 5px 5px;padding-left:5px; padding-righ5:5px"><i class="fa fa-bullhorn"></i><p>Copyright &copy; 2019<script>new Date().getFullYear()>2019&&document.write("-"+new Date().getFullYear());</script> <a href="https://wuruofan.com">小黑杂说</a>. All Rights Reserved.</p><strong>版权声明</strong>：除非注明，文章均为原创！</br>本网站采用<a href="http://creativecommons.org/licenses/by-nc-sa/3.0/" rel="nofollow" target="_blank" title="BY-NC-SA 授权协议">BY-NC-SA</a>协议进行授权，转载请以链接形式标明本文地址：--PostURL--.</div>
```

#### 0x04d 插件列表

WordPress的插件也是茫茫多，这里记录下使用中的一些插件以防万一。

*   Jetpack：WordPress官方增强功能
  
*   Akismet Anti-Spam：反垃圾评论，要和Jetpack连接使用
  
*   Better Search Replace：替换数据库中信息
  
*   Really Simple SSL：一键开启HTTPS
  
*   SSL 不安全内容修复器：修复页面中混杂http和https的问题
  
*   Redirection：管理网站的301重定向页面和404页面，之前手工重定向http主页到https主页时用的
  
*   Google XML Sitemaps：Google站点地图，用于Google搜索收录
  
*   百度搜索推送管理： 百度搜索收录相关
  
*   多合一SEO包：设置搜索引擎相关关键字信息
  
*   Rename wp-login.php：重命名WordPress登陆页面地址，以防被别人暴力登陆
  
*   WP Super Cache：快速缓存插件
  
*   WP Alu2Button：MDx主题评论区表情需要使用的插件
  
*   WP-Optimize - Clean, Compress, Cache：WordPress站点优化插件
  
*   Wordfence Security & Wordfence Assistant：安全插件，不太会用，开启后我的梯子无法正常工作，看iptables里似乎追加了配置，目前暂未使用。
  
*   UpdraftPlus-备份/恢复：必须有姓名！我的命都是它给的（破音）！免费版也支持备份到云盘，我选择每周备份一次到Dropbox！
  
*   PHP Compatibility Checker：php版本兼容性检查
  

#### 0x04e PHP更新

由于种种原因和骚操作，我不得不重装LNMP和WordPress，~~顺便检查一下之前的过程记录是不是有问题，~~在我装完最新版WordPress进入设置页面时，提示我升级到更安全的PHP版本。

LNMP安装脚本里的php是`5.6.10`，而目前最新版本已经是`7.4.4`了，LNMP的安装目录下提供了`upgrade.sh`升级脚本，运行即可升级各种组件。

**注意**，这里请不要想我之前一样，直接升级最新版本，导致一会儿找不到`php-fpm`一会儿nginx启动不了等等问题，我不得不再次重装同时再检查一下之前的过程记录是不是有问题。

**注意**，重装LNMP时也不要再安装时选择最新版php，虽然LNMP1.7的安装脚本已经支持安装`7.4.4`版本的php，也会无法启动，不要问我怎么知道的。

正确的做法是安装上面提到的插件`PHP Compatibility Checker`，检查当前WordPress程序、插件及主题，和php哪个版本兼容，目前看这个插件支持检测`7.0`～`7.3`版本，检测完成之后，再去执行`./upgrade.sh php`选择相应版本号升级，最终我选择了`7.0`版本，才结束我的重装之旅。吐血！

#### 0x04f HTTPS证书过期

HTTPS证书的有效期是90天，我的站点证书过期，而网上找的教程又不符合我的情况，一阵操作猛如虎的我，果然成功，把网站搞崩溃了。

其实LNMP的官网上有说明的帖子[建议用户更新Let'sEncrypt SSL证书续期规则](https://lnmp.org/notice/fix-certbot-renew.html "建议用户更新Let'sEncrypt SSL证书续期规则")，只是也比较早期了，但本质没变化。

> 自动更新命令：wget -O - http://soft.vpser.net/lnmp/ext/fix\_renewssl.shbash 也可以直接升级到1.5使用acme.sh生成证书，wget http://soft.vpser.net/lnmp/lnmp1.5beta.tar.gz -O lnmp1.5beta.tar.gz && tar zxf lnmp1.5beta.tar.gz && cd lnmp1.4 && ./upgrade1.x-1.5.sh ssl

重点就是更新`crontab`加入定时任务去更新证书，旧版使用`certbot`或者新版`acme.sh`更新证书。

之前出问题估计是我的VPS又装了其他服务，导致`crontab`出了问题，正常安装完LNMP之后，使用`crontab -l`可以看到如下配置`44 0 * * * "/usr/local/acme.sh"/acme.sh --cron --home "/usr/local/acme.sh" > /dev/null`，即每天0点44分执行一次，证书过期会自动申请。

### 0x05 最后

这篇文章拖拖拉拉的，中间又遇到几个月的频繁出差深夜加班就耽搁了。等到再次下决心把它写完的时候突然发现网站证书过期了，php版本过高，Let's Encrypt证书申请太频繁限制次数不能申请的一堆乱七八糟问题，折腾来折腾去wordpress重装了好几次，我也崩溃了好几回，不过换个角度，也算重复多次检验了文章内容的可靠性，顺便补了些截图。还好当初装了Updraft备份插件，真心好评。

这次给我的教训就是，写东西时一开始的规划就要简短，尽可能一次写完，太长了自己容易泄劲，再一忙又失去动力，我现在算是理解网文小说为何如此容易鸽了。

路漫漫，加油。