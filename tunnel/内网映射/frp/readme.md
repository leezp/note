
[frp](https://github.com/fatedier/frp)

	
	server 端配置

	[common]
	bind_port = 7000
	token = token
	dashboard_port = 7500
	dashboard_user = admin
	dashboard_pwd = admin
	vhost_http_port = 8080
	vhost_https_port = 10443


	服务端启动

	nohup ./frps -c ./frps.ini


	客户端配置

	[ssh]
	type = tcp
	local_ip = 127.0.0.1
	local_port = 3389
	remote_port = 6000
	[smb]
	type = tcp
	local_ip = 127.0.0.1
	local_port = 445
	remote_port = 6001
	[web01]
	type = http
	local_ip = 127.0.0.1
	local_port = 9001
	use_encryption = false
	use_compression = true
	custom_domains= your domain registrated




