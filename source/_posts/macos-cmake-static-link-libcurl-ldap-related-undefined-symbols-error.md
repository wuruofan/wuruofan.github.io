---
title: MacOS CMake链接Curl静态库找不到ldap相关符号问题
tags:
  - CMake
  - curl
  - link error
  - undefined symbols
id: '305'
categories:
  - - 技术总结
date: 2020-07-09 15:12:41
---

具体编译过程和前两篇文章类似，但是在链接`libcurl.a`的时候出现找不到ldap相关符号的提示：

<!-- more -->

```
Undefined symbols for architecture x86_64:
  "_ber_free", referenced from:
      _Curl_ldap in libcurl.a(libcurl_la-ldap.o)
  "_ldap_err2string", referenced from:
      _Curl_ldap in libcurl.a(libcurl_la-ldap.o)
  "_ldap_first_attribute", referenced from:
      _Curl_ldap in libcurl.a(libcurl_la-ldap.o)
  "_ldap_first_entry", referenced from:
      _Curl_ldap in libcurl.a(libcurl_la-ldap.o)
  "_ldap_free_urldesc", referenced from:
      _Curl_ldap in libcurl.a(libcurl_la-ldap.o)
  "_ldap_get_dn", referenced from:
      _Curl_ldap in libcurl.a(libcurl_la-ldap.o)
  "_ldap_get_values_len", referenced from:
      _Curl_ldap in libcurl.a(libcurl_la-ldap.o)
  "_ldap_init", referenced from:
      _Curl_ldap in libcurl.a(libcurl_la-ldap.o)
  "_ldap_memfree", referenced from:
      _Curl_ldap in libcurl.a(libcurl_la-ldap.o)
  "_ldap_msgfree", referenced from:
      _Curl_ldap in libcurl.a(libcurl_la-ldap.o)
  "_ldap_next_attribute", referenced from:
      _Curl_ldap in libcurl.a(libcurl_la-ldap.o)
  "_ldap_next_entry", referenced from:
      _Curl_ldap in libcurl.a(libcurl_la-ldap.o)
  "_ldap_search_s", referenced from:
      _Curl_ldap in libcurl.a(libcurl_la-ldap.o)
  "_ldap_set_option", referenced from:
      _Curl_ldap in libcurl.a(libcurl_la-ldap.o)
  "_ldap_simple_bind_s", referenced from:
      _Curl_ldap in libcurl.a(libcurl_la-ldap.o)
  "_ldap_unbind_s", referenced from:
      _Curl_ldap in libcurl.a(libcurl_la-ldap.o)
  "_ldap_url_parse", referenced from:
      _Curl_ldap in libcurl.a(libcurl_la-ldap.o)
  "_ldap_value_free_len", referenced from:
      _Curl_ldap in libcurl.a(libcurl_la-ldap.o)
ld: symbol(s) not found for architecture x86_64
```

看上去是找不到`ldap`相关符号，在Ubuntu上编译没遇到这个问题，查了下资料，`LDAP`是一种轻量级文件夹访问协议（Lightweight Directory Access Protocol），默认MacOS是支持这个协议的。

翻了下配置时的输出日志：

```
  curl version:     7.70.0
  SSL:              enabled (OpenSSL)
  SSH:              no      (--with-{libssh,libssh2})
  zlib:             enabled
  brotli:           no      (--with-brotli)
  GSS-API:          no      (--with-gssapi)
  TLS-SRP:          enabled
  resolver:         POSIX threaded
  IPv6:             enabled
  Unix sockets:     enabled
  IDN:              no      (--with-{libidn2,winidn})
  Build libcurl:    Shared=no, Static=yes
  Built-in manual:  enabled
  --libcurl option: enabled (--disable-libcurl-option)
  Verbose errors:   enabled (--disable-verbose)
  Code coverage:    disabled
  SSPI:             no      (--enable-sspi)
  ca cert bundle:   /etc/ssl/cert.pem
  ca cert path:     no
  ca fallback:      no
  LDAP:             enabled (OpenLDAP)
  LDAPS:            enabled
  RTSP:             enabled
  RTMP:             no      (--with-librtmp)
  Metalink:         no      (--with-libmetalink)
  PSL:              no      (libpsl not found)
  Alt-svc:          no      (--enable-alt-svc)
  HTTP2:            disabled (--with-nghttp2)
  HTTP3:            disabled (--with-ngtcp2, --with-quiche)
  ESNI:             no      (--enable-esni)
  Protocols:        DICT FILE FTP FTPS GOPHER HTTP HTTPS IMAP IMAPS LDAP LDAPS POP3 POP3S RTSP SMB SMBS SMTP SMTPS TELNET TFTP
  Features:         SSL IPv6 UnixSockets libz AsynchDNS NTLM NTLM_WB TLS-SRP HTTPS-proxy
```

可以看到`LDAP`和`LDAPS`功能都使能了，而且识别到了`OpenLDAP`，对比了之前文章里的配置，Linux版本编译Curl的时候这两个选项都是`no`。

查看了Curl官网上关于编译的简要说明，用`curl-config --libs`查看需要链接的库，也多了`-lldap`这一项，因此是链接过程需要指明链接`ldap`相关库才可以。

现在有**几种解决方法**：

1.  禁用libcurl中ldap相关功能：在`./configure`配置的时候加上`--disable-ldap --disable-ldaps`选项。
2.  下载ldap源码，像zlib一样编译静态库并链接。
3.  链接系统ldap库：添加额外的链接`target_link_libraries(my_target -lldap)`即可。

都可以解决问题。


<center>--- END ---</center>