__author__ = 'leezp'
# xray 一键部署
# 191210
# -*- coding:utf-8 -*-
# 最后如果能加上扫描端口确认服务已启动就完美了/ 查看进程号，根据结果校验


import time
import paramiko


def creatSShConnectOb(ip_remote, port_remote, username, password):
    print('---------- start to create SSH object')
    print(
        'Remote SSH Info: \'ip:%s  port:%d  username:%s  password:%s\'' % (ip_remote, port_remote, username, password))
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip_remote, port_remote, username=username, password=password, timeout=60)  # timeout protection
        return ssh
    except:
        print('Warning:\nFist connect the ABC failed, now will retry!')
        ssh.connect(ip_remote, port_remote, username=username, password=password, timeout=60)  # timeout re-try
        print('Error:\nAttempt to connect ABC failed!!! Please check the IP / port/ account / password.')


def chanel_exe_cmd(ChanelSSHOb, cmd, t=0.1):
    ChanelSSHOb.send(cmd)
    ChanelSSHOb.send("\n")
    time.sleep(t)
    resp = ChanelSSHOb.recv(9999).decode("utf8")
    # print("Exec Result: %s" % (resp)+'\n')
    return resp


def upload2(ip, port, username, password):
    transport = paramiko.Transport((ip, port))
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)  # 如果连接需要密钥，则要加上一个参数，hostkey="密钥"
    sftp.put('C:\\Users\\Administrator\\Desktop\\poc 扫描\\xray_windows_amd64.exe\\xray-license.lic',
             '/tmp/xray-license.lic')
    sftp.put('C:\\Users\\Administrator\\Desktop\\poc 扫描\\xray_windows_amd64.exe\\ca.crt',
             '/tmp/ca.crt')
    sftp.put('C:\\Users\\Administrator\\Desktop\\poc 扫描\\xray_windows_amd64.exe\\ca.key',
             '/tmp/ca.key')
    sftp.put('C:\\Users\\Administrator\\Desktop\\poc 扫描\\xray_windows_amd64.exe\\config.yaml', '/tmp/config.yaml')
    # sftp.put('C:\\Users\\Administrator\\Desktop\\poc 扫描\\xray_windows_amd64.exe\\xray_linux_amd64',
    #     '/tmp/xray_linux_amd64')
    transport.close()  # 关闭连接


def upload(ip, port, username, password):
    transport = paramiko.Transport((ip, port))
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)  # 如果连接需要密钥，则要加上一个参数，hostkey="密钥"
    sftp.put('C:\\Users\\Administrator\\Desktop\\poc 扫描\\xray_windows_amd64.exe\\xray-license.lic',
             '/home/YOURNAME/xray-license.lic')
    sftp.put('C:\\Users\\Administrator\\Desktop\\poc 扫描\\xray_windows_amd64.exe\\ca.crt',
             '/home/YOURNAME/ca.crt')
    sftp.put('C:\\Users\\Administrator\\Desktop\\poc 扫描\\xray_windows_amd64.exe\\ca.key',
             '/home/YOURNAME/ca.key')
    sftp.put('C:\\Users\\Administrator\\Desktop\\poc 扫描\\xray_windows_amd64.exe\\config.yaml', '/home/YOURNAME/config.yaml')
    # sftp.put('C:\\Users\\Administrator\\Desktop\\poc 扫描\\xray_windows_amd64.exe\\xray_linux_amd64',
    #     '/home/YOURNAME/xray_linux_amd64')
    transport.close()  # 关闭连接


# 杀掉进程
def kill(chanelSSHOb, ip):
    sshCmd = "ps aux|grep xray|grep ?|cut -d.  -f1|cut -dt -f2|tr -s ' '|tr ' ' '$'|cut -d$ -f2|xargs kill -9"
    chanel_exe_cmd(chanelSSHOb, sshCmd)


def remove(chanelSSHOb, ip):
    html_name = ip.split('.')[-1] + '.html'
    sshCmd = 'rm -f /home/YOURNAME/%s' % html_name
    chanel_exe_cmd(chanelSSHOb, sshCmd)
    sshCmd = 'rm -f /home/YOURNAME/nohup.out'
    chanel_exe_cmd(chanelSSHOb, sshCmd)
    sshCmd = 'rm -f /home/YOURNAME/config.yaml'
    chanel_exe_cmd(chanelSSHOb, sshCmd)
    sshCmd = 'rm -f /home/YOURNAME/nohup.out'
    chanel_exe_cmd(chanelSSHOb, sshCmd)
    sshCmd = 'rm -f /home/YOURNAME/xray_linux_amd64'
    # chanel_exe_cmd(chanelSSHOb, sshCmd)
    '''
    sshCmd='rm -f /home/YOURNAME/ca.crt'
    chanel_exe_cmd(chanelSSHOb, sshCmd)
    sshCmd='rm -f /home/YOURNAME/ca.key'
    chanel_exe_cmd(chanelSSHOb, sshCmd)
    sshCmd='rm -f /home/YOURNAME/xray-license.lic'
    chanel_exe_cmd(chanelSSHOb, sshCmd)
    '''


'''
ip = '172.16.1.9'
port = '22'
username = 'XXX'
passwd = 'XXX'
'''
# 需要先 useradd YOURNAME

if __name__ == '__main__':
    host = {
        1: '172.16.1.247:22,root,XXX,7776'
        , 2: '172.16.1.225:22,root,XXX,7775'
        , 3: '172.16.1.209:22,root,XXX,7778'
        , 4: '172.16.1.248:22,root,XXX,7773'
        , 5: '172.16.1.230:22,root,XXX,7772'
        , 6: '172.16.1.249:22,root,XXX,7771'
        , 7: '172.16.1.9:22,root,XXX,7779'
        , 8: '10.1.0.224:22,root,XXX,7774'
        , 9: '172.16.1.220:22,root,XXX,7770'
        , 10: '172.16.1.10:22,root,XXX,7774'
        , 11: '172.16.1.47:22,XXX,XXX,7774'
    }
    for k in range(len(host)):
        ip = host.get(k + 1).split(':')[0].strip()
        port = host.get(k + 1).split(',')[0].split(':')[-1].strip()
        username = host.get(k + 1).split(',')[1].strip()
        password = host.get(k + 1).split(',')[2].strip()
        listen_port = host.get(k + 1).split(',')[-1].strip()

        ssh = creatSShConnectOb(ip, int(port), username=username, password=password)

        chanelSSHOb = ssh.invoke_shell()  # 建立交互式的shel
        # 检查当前用户是否是 root
        Flag = True
        stdin, stdout, stderr = ssh.exec_command("whoami")
        result = stdout.read()
        if result and result.decode().strip() == 'root':
            pass
        else:
            Flag = False
            sshCmd = 'su'
            stdin, stdout, stderr = ssh.exec_command(sshCmd)
            if chanel_exe_cmd(chanelSSHOb, sshCmd).endswith(u"Password: "):
                sshCmd = 'sh_pwd'
                chanel_exe_cmd(chanelSSHOb, sshCmd)

        ''' 非 root 暂不知道怎么上传
        ftp =ssh.open_sftp()
        ftp.put( 'C:\\Users\\Administrator\\Desktop\\poc 扫描\\xray_windows_amd64.exe\\xray-license.lic','/home/YOURNAME/xray-license.lic')
        # 使用之后记得关闭
        #ftp.get() 下载
        ftp.close()
        '''
        kill(chanelSSHOb, ip)
        remove(chanelSSHOb, ip)
        if Flag:
            # root 用户上传 
            # upload('172.16.1.9', 22, 'XXX', 'XXX')
            upload(ip, int(port), username, password)
        else:
            # 非 root 用户上传到 /tmp
            upload2(ip, int(port), username, password)
            sshCmd = 'mv /tmp/xray-license.lic /home/YOURNAME'
            chanel_exe_cmd(chanelSSHOb, sshCmd)
            sshCmd = 'mv /tmp/ca.crt /home/YOURNAME'
            chanel_exe_cmd(chanelSSHOb, sshCmd)
            sshCmd = 'mv /tmp/ca.key /home/YOURNAME'
            chanel_exe_cmd(chanelSSHOb, sshCmd)
            sshCmd = 'mv /tmp/config.yaml /home/YOURNAME'
            chanel_exe_cmd(chanelSSHOb, sshCmd)
            sshCmd = 'mv /tmp/xray_linux_amd64 /home/YOURNAME'
            chanel_exe_cmd(chanelSSHOb, sshCmd)

        sshCmd = 'cd /home/YOURNAME && chmod 555 xray_linux_amd64'
        chanel_exe_cmd(chanelSSHOb, sshCmd)
        # 添加ssl证书
        sshCmd = 'cd /home/YOURNAME && cp ca.crt /etc/pki/ca-trust/source/anchors/'
        chanel_exe_cmd(chanelSSHOb, sshCmd)
        sshCmd = 'update-ca-trust extract'
        chanel_exe_cmd(chanelSSHOb, sshCmd)

        sshCmd = 'cd /home/YOURNAME && nohup ./xray_linux_amd64 webscan --listen 0.0.0.0:%d --webhook-output http://YOURMYSQLIP:5000/webhook' % int(
            listen_port)
        # print(sshCmd)
        print(chanel_exe_cmd(chanelSSHOb, sshCmd))

'''
def upload(ip):
    transport = paramiko.Transport((ip, 22))
    transport.connect(username='XXX', password='XXX')
    sftp = paramiko.SFTPClient.from_transport(transport)  # 如果连接需要密钥，则要加上一个参数，hostkey="密钥"
    # 上传至 tmp 目录，其他目录权限不够
    sftp.put('C:\\Users\\Administrator\\Desktop\\a.txt', '/tmp/a.txt')
    transport.close()  # 关闭连接
'''
# sshCmd = 'mv /tmp/a.txt /home/YOURNAME'
# print(chanel_exe_cmd(chanelSSHOb, sshCmd))
'''
ssh = creatSShConnectOb(ip, int(port), username=username, password=passwd)
stdin, stdout, stderr = ssh.exec_command(cmd)
result = stdout.read()
if result:
    if result.decode().strip() == 'XXX':
        return result.decode()
else:
    print("连接失败!")
    result = stderr.read()
ssh.close()
'''
