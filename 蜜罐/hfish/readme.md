## 本地通过端口映射在vps搭建一个web蜜罐

### 环境

CentOS 7 

HFish

### HFish 现有端口服务


[rpc] 7879   
 
[admin] 9001 不映射

[plugin] 8989 不映射

[web] 9000 

[deep]   8080    

[ssh]  22      vps 222

[redis] 6379
 
[mysql] 3306  vps 3340   改本地 3340

[telnet] 23   

[ftp] 21

[mem_cache] 11211

[http] 8081   改本地  8089

[tftp] 69

[elasticsearch] 9200

[vnc] 5900



### 端口检查

查看开放端口

	netstat -ntlpu


### 修改mysql 默认端口

	vi /etc/my.cnf
	
	[mysqld]
	port=3340

重启mysql


### 修改ssh端口号

	vim /etc/ssh/sshd_config

取消 Port 22 注释，修改端口号 222

	service sshd restart


### 可能遇到的问题

修改完端口号重启，还是无法连接。


需要如下2步操作

1.关闭防火墙

	查看防火墙状态
	systemctl status firewalld

	关闭防火墙
	systemctl stop firewalld

2.检查 firewall-cmd 开放的端口，**我在centos即使关闭防火墙它也会生效**

	查看开放服务
	
	firewall-cmd --list-all

	public
	  target: default
	  icmp-block-inversion: no
	  interfaces: 
	  sources: 
	  services: dhcpv6-client ssh
	  ports: 3340/tcp
	  protocols: 
	  masquerade: no
	  forward-ports: 
	  source-ports: 
	  icmp-blocks: 
	  rich rules: 

	添加出站端口规则
	
	firewall-cmd --zone=public --add-port=222/tcp --permanent

	不关闭服务重载防火墙

	firewall-cmd --reload

	如需关闭出站端口规则
	
	firewall-cmd --zone=public --remove-port=222/tcp --permanent

配置完一般几分钟内生效。


	重新查看开放服务
	
	firewall-cmd --list-all

	public
	  target: default
	  icmp-block-inversion: no
	  interfaces: 
	  sources: 
	  services: dhcpv6-client ssh
	  ports: 3340/tcp 222/tcp
	  protocols: 
	  masquerade: no
	  forward-ports: 
	  source-ports: 
	  icmp-blocks: 
	  rich rules: 

现在即可用ssh连接。



### 添加7000端口

	firewall-cmd --zone=public --add-port=7000/tcp --permanent

	firewall-cmd --reload

	firewall-cmd --list-all

依次添加蜜罐需要开放的端口


### windows 端配置


frpc.ini


[frp项目地址](https://github.com/fatedier/frp)






## 后记

因为vps内存小，frp 内网映射方式，获取不到 访客真实ip，暂未解决。 https://www.v2ex.com/t/474820