centos：


	vim /etc/proxychains.conf
	
	[ProxyList]
	
	socks5 vps_ip port


socks5转发 tcp udp 不支持 icmp。


wget 基于tcp ，可以使用配置好socks5后，用来作测试网络连通性；

![](1.png)