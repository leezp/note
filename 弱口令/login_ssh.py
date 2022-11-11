# ! /usr/bin/env python3
# -*- coding:utf-8 -*-
# ssh 弱口令

import paramiko

ip = '192.168.255.147'
port = '22'
username = 'root'
passwd = 'toor'


# ssh 用户名 密码 登陆
def ssh_base_pwd(ip, port, username, passwd, cmd='ls'):
    port = int(port)
    ssh = paramiko.SSHClient()

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(hostname=ip, port=port, username=username, password=passwd)

    stdin, stdout, stderr = ssh.exec_command(cmd)

    result = stdout.read()
    if not result:
        print("无结果!")
        result = stderr.read()
    ssh.close()

    return result.decode()


a = ssh_base_pwd(ip, port, username, passwd)
print(a)
