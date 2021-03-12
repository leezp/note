## 2020/2/24



https://mp.weixin.qq.com/s?__biz=MzAxNjg0NzEzNQ==&mid=2247483961&idx=1&sn=a1eddf03c0f0c61d84461e459ccc8047&chksm=9befda49ac98535f355eb49ba4dadd4a39f04755f9732ee71ab86930c1e3165a3a38faf1ba88&mpshare=1&scene=23&srcid=&sharer_sharetime=1582767639076&sharer_shareid=bfb9acc21689fde2307d3d974dc7b091#rd


复现视频：https://youtu.be/7d_HoQ0LVy8
原文：https://www.zerodayinitiative.com/blog/2020/2/24/cve-2020-0688-remote-code-execution-on-microsoft-exchange-server-through-fixed-cryptographic-keys


## 概述

该漏洞是在Exchange Control Panel （ECP）组件中发现的。

与每次软件安装都会产生随机密钥不同，所有Microsoft Exchange Server在安装后的web.config文件中都拥有相同的validationKey和decryptionKey。这些密钥用于保证ViewState的安全性。而ViewState是ASP.NET Web应用以序列化格式存储在客户机上的服务端数据。客户端通过__VIEWSTATE请求参数将这些数据返回给服务器。

由于使用了静态密钥，经过身份验证的攻击者可以欺骗目标服务器反序列化恶意创建的ViewState数据。在YSoSerial.net的帮助下，攻击者可以在Exchange Control Panel web应用上执行任意.net代码。

为了利用这个漏洞，我们需要从经过身份验证的session中收集ViewStateUserKey和VIEWSTATEGENERATOR值。ViewStateUserKey可以从ASP.NET的cookie中获取，而VIEWSTATEGENERATOR可以在一个隐藏字段中找到。

该漏洞是由Exchange Server在安装时未能正确创建唯一的加密密钥导致的。

## 影响范围

•	Microsoft Exchange Server 2010 Service Pack 3

•	Microsoft Exchange Server 2013

•	Microsoft Exchange Server 2016

•	Microsoft Exchange Server 2019

注意：Exchange Server 2010默认使用.net v2.0，而ysoserial.net-V2版没有ViewState插件，漏洞利用有一定难度。


## 漏洞利用条件

所有exchange的漏洞都需要一个普通权限的登录账号，exchange的账号获取方式我们一般采用爆破或者社工等方式


