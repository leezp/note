[docker安装知识库](https://www.runoob.com/docker/centos-docker-install.html)



启动docker

docker run -it -d -p 8866:80 -p 8867:81 -p 8868:22 kalilinux/kali-linux-docker


没有端口，端口任意指定，映射22端口，


进入容器内部安装ssh


apt-get update


apt-get install openssh-client


apt-get install openssh-server


/etc/init.d/ssh start

返回即为启动成功
Starting OpenBSD Secure Shell server: sshd.

查看ssh状态

service ssh status


安装 netstat

	apt-get install net-tools


**记得给docker里的kali配置密码，否则可能无法登陆成功**