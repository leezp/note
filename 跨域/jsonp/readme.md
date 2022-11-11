##同源策略

### 概述

同源指的是：同协议，同域名和同端口。

同源策略是浏览器的行为，是为了保护本地数据不被JavaScript代码获取回来的数据污染，因此拦截的是客户端发出的请求回来的数据接收，即请求发送了，服务器响应了，但是无法被浏览器接收。

如果没有浏览器的同源策略，那么CSRF攻击就变得很容易。

### IE 中的特例

Internet Explorer 的同源策略有两个主要的差异点：

1.授信范围（Trust Zones）：两个相互之间高度互信的域名，如公司域名（corporate domains），则不受同源策略限制。

2.端口：IE 未将端口号纳入到同源策略的检查中，因此 https://company.com:81/index.html 和 https://company.com/index.html  属于同源并且不受任何限制。

### 如何允许跨源访问

1.可以使用 CORS（Cross-origin resource sharing，跨域资源共享） 来允许跨源访问。CORS 是 HTTP 的一部分，它允许服务端来指定哪些主机可以从这个服务端加载资源。

CORS背后的基本思想，就是使用自定义的HTTP头部让浏览器与服务器进行沟通，从而决定请求或响应是应该成功，还是应该失败。

CORS需要浏览器和服务器同时支持。目前，所有浏览器都支持该功能，IE 浏览器不能低于 IE10。

整个CORS通信过程，都是浏览器自动完成，不需要用户参与。

对于开发者来说，CORS通信与同源的AJAX通信没有差别，代码完全一样。浏览器一旦发现AJAX请求跨源，就会自动添加一些附加的头信息，有时还会多出一次附加的请求，但用户不会有感觉。

因此，实现CORS通信的关键是服务器。只要服务器实现了CORS接口，就可以跨源通信。


优点：

    CORS通信与同源的AJAX通信没有差别，代码完全一样，容易维护。

    支持所有类型的HTTP请求。

缺点：

    存在兼容性问题，特别是IE10以下的浏览器。

    第一次发送非简单请求时会多一次请求。

CORS细节见下文：

[什么是浏览器同源策略--CORS（跨域资源共享）](https://www.cnblogs.com/laixiangran/p/9064769.html)

2.**html标签中的 script、img、iframe、link 这几个标签是允许进行资源的跨域获取的。**
	
	<script src="..."> //加载图片到本地执行
	
	<img src="..."> //图片  只能浏览器与服务器的单向通信，因为浏览器不能访问服务器的响应文本。
	
	<link href="...">//css
	
	<iframe src="...">//任意资源

3.服务器代理

浏览器有跨域限制，但是服务器不存在跨域问题，所以可以由服务器请求所要域的资源再返回给客户端。服务器代理是万能的。例如ssrf等。

4.document.domain跨域

对于主域名相同，而子域名不同的情况，可以使用document.domain来跨域。这种方式非常适用于iframe跨域的情况。

document.domain 的设置是有限制的，我们只能把 document.domain 设置成自身或更高一级的父域，且主域必须相同。

例如：分别打印id.qq.com的document.domain和www.qq.com的document.domain，发现前者是id.qq.com，而后者是qq.com，这时我们手动设置一下id.qq.com页面的document.domain，设置为qq.com，再次访问www.qq.com的window对象的document，发现访问成功。

[通过document.domain实现跨域访问](https://blog.csdn.net/nlznlz/article/details/79506655)

5.window.name跨域 （未测试）

window对象有个name属性，该属性有个特征：即在一个窗口（window）的生命周期内，窗口载入的所有的页面（不管是相同域的页面还是不同域的页面）都是共享一个window.name的，每个页面对window.name都有读写的权限，window.name是持久存在一个窗口载入过的所有页面中的，并不会因新页面的载入而进行重置。

6.location.hash跨域（未测试）

location.hash方式跨域，是子框架具有修改父框架src的hash值，通过这个属性进行传递数据，且更改hash值，页面不会刷新。但是传递的数据的字节数是有限的。

7.postMessage跨域

window.postMessage(message, targetOrigin)方法是HTML5新引进的特性，可以使用它来向其它的window对象发送消息，无论这个window对象是属于同源或不同源。这个应该就是以后解决dom跨域通用方法了。

调用postMessage方法的window对象是指要接收消息的那一个window对象，该方法的第一个参数message为要发送的消息，类型只能为字符串；第二个参数targetOrigin用来限定接收消息的那个window对象所在的域，如果不想限定域，可以使用通配符*。

需要接收消息的window对象，可是通过监听自身的message事件来获取传过来的消息，消息内容储存在该事件对象的data属性中。

8.JSONP跨域

由于script标签不受浏览器同源策略的影响，允许跨域引用资源。因此可以通过动态创建script标签，然后利用src属性进行跨域，这也就是JSONP跨域的基本原理。

优点：

    使用简便，没有兼容性问题，目前最流行的一种跨域方法。

缺点：

    只支持GET请求。

    由于是从其它域中加载代码执行，因此如果其他域不安全，很可能会在响应中夹带一些恶意代码。

    要确定JSONP请求是否失败并不容易。虽然HTML5给script标签新增了一个onerror事件处理程序，但是存在兼容性问题。

[**JSONP--维基百科**](https://zh.wikipedia.org/wiki/JSONP)

## jsonp利用

水坑攻击



## jsonp挖掘

测试之前需要登录。

chrome F12 network--Preserve log 勾选；

然后 F5 刷新，进入 NetWork 标签 ，CTRL+F 查找一些关键词 如 callback json jsonp email等。

对所有的jsonp请求自动用不同的域进行访问来确认是否有jsonp的问题

[```jsonp_info_leak```](https://github.com/qiaofei32/jsonp_info_leak)

## jsonp防御

	1、严格安全的实现 CSRF 方式调用 JSON 文件：限制 Referer 、部署一次性 Token 等。
	2、严格安照 JSON 格式标准输出 Content-Type 及编码（ Content-Type : application/json; charset=utf-8 ）。
	3、严格过滤 callback 函数名及 JSON 里数据的输出。
	4、严格限制对 JSONP 输出 callback 函数名的长度(如防御上面 flash 输出的方法)。
	5、其他一些比较“猥琐”的方法：如在 Callback 输出之前加入其他字符(如：/**/、回车换行)这样不影响 JSON 文件加载，又能一定程度预防其他文件格式的输出。还比如 Gmail 早起使用 AJAX 的方式获取 JSON ，听过在输出 JSON 之前加入 while(1) ;这样的代码来防止 JS 远程调用。

## 参考资料

[浏览器的同源策略](https://developer.mozilla.org/zh-CN/docs/Web/Security/Same-origin_policy)

[JSONP 劫持原理与挖掘方法](https://www.k0rz3n.com/2019/03/07/JSONP%20%E5%8A%AB%E6%8C%81%E5%8E%9F%E7%90%86%E4%B8%8E%E6%8C%96%E6%8E%98%E6%96%B9%E6%B3%95/)

[github find person](https://www.ixiqin.com/2020/01/how-to-find-a-person-through-making/)