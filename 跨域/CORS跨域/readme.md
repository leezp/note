## CORS 跨域

CORS（Cross Origin Resource Sharing），跨域资源共享，为了弥补JSONP等跨域常见技术的缺陷，而提出的安全方便的跨域方案。它允许浏览器想跨域服务器，发出XMLHttpRequest请求，从而克服AJAX只能同源使用的限制。

CORS需要浏览器和服务器同时支持，相比JSONP更加复杂，但是一般目前的浏览器都是支持的，服务器只需要进行相应配置，其通信过程都是浏览器自动完成，对于开发人员来说，跟写AJAX的代码没有区别，只是会在发送跨域请求时在HTTP请求头中添加一些字段来验证，关键字段如下:

1、Access-Control-Allow-Origin：指定哪些域可以访问域资源。例如，如果requester.com想要访问provider.com的资源，那么开发人员可以使用此标头安全地授予requester.com对provider.com资源的访问权限。

2、Access-Control-Allow-Credentials：指定浏览器是否将使用请求发送cookie。仅当allow-credentials标头设置为true时，才会发送Cookie。

3、Access-Control-Allow-Methods：指定可以使用哪些HTTP请求方法（GET，PUT，DELETE等）来访问资源。此标头允许开发人员通过在requester.com请求访问provider.com的资源时，指定哪些方法有效来进一步增强安全性。

### CORS实现流程

1、服务器配置支持CORS，默认认可所有域都可以访问

2、浏览器客户端把所在的域填充到Origin发送跨域请求

3、服务器根据资源权限配置，在响应头中添加Access-Control-Allow-Origin Header，返回结果

4、浏览器比较服务器返回的Access-Control-Allow-Origin Header和请求域的Origin，如果当前域获得授权，则将结果返回给页面

代码演示见 [浅谈跨域威胁与安全](https://www.freebuf.com/articles/web/208672.html)

### CORS安全威胁

CORS一般最常见的安全威胁就是CORS错误配置导致资源信息泄漏，与JSONP劫持基本上一致。

**漏洞原理：通常开发人员使用CORS一般默认允许来自所有域或者由于错误的正则匹配方式造成绕过规定的白名单域**

### 环境

CORS服务器 192.168.255.151 phpstudy集成环境 ```http://192.168.255.151:8081/DoraBox-master/csrf/userinfo.php```页面

存储cors信息的vps  192.168.0.103 

用户访问 localhost:8081/CORS.html