## centos ssr 客户端使用

由于工作需要下载国外的资料，服务器不能访问自己电脑网络，所以要在服务器开启SSR客户端。

	pip install shadowsocks

新建一个配置文件：

	/etc/shadowsocks/config.json

	{
	
	"server":"server_ip",
	
	"server_port":13817,
	
	"local_port":"1080",
	
	"password":"hUSyseh9HcvP",
	
	"timeout":600,
	
	"method":"rc4-md5",
	
	"fast_open":false
	
	}

开启fast_open以降低延迟，但要求Linux内核在3.7+。开启方法 ```echo 3 > /proc/sys/net/ipv4/tcp_fastopen```

**注意server一定要使用服务器ip，使用服务器host是不行的，需要获取对应ip。**


开启客户端：

	sslocal -c /etc/shadowsocks/config.json

或者

    nohup sslocal -c /etc/shadowsocks/config.json  /dev/null 2>&1 &

访问一个网站测试：

	curl --socks5 127.0.0.1:1080 http://google.com

获取当前代理获取的ip：

	curl --socks5 127.0.0.1:1080 http://httpbin.org/ip

## 参考资料

[centos如何使用ssr客户端](https://www.wsfnk.com/archives/1208.html)