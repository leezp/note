# -*- coding:utf-8 -*-
__author__ = 'leezp'
__date__ = 20201117

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

# 实例化DummyAuthorizer来创建ftp用户
authorizer = DummyAuthorizer()
# 参数：用户名，密码，目录，权限
authorizer.add_user('admin', '123', 'D:\\', perm='elradfmwMT')
# 匿名登录
# authorizer.add_anonymous('/home/nobody')
handler = FTPHandler
handler.authorizer = authorizer
# 参数：IP，端口，handler
server = FTPServer(('0.0.0.0', 21), handler)  # 设置为0.0.0.0为本机的IP地址
server.serve_forever()

'''
读取权限：

"e" =更改目录（CWD，CDUP命令）

"l" =列表文件（LIST，NLST，STAT，MLSD，MLST，SIZE命令）

"r" =从服务器检索文件（RETR命令）

写入权限：

"a" =将数据追加到现有文件（APPE命令）

"d" =删除文件或目录（DELE，RMD命令）

"f" =重命名文件或目录（RNFR，RNTO命令）

"m" =创建目录（MKD命令）

"w" =将文件存储到服务器（STOR，STOU命令）

"M"=更改文件模式/权限（SITE CHMOD命令）

"T"=更改文件修改时间（SITE MFMT命令）
'''

# 也可以 python -m pyftpdlib 用py 原生ftp服务， -h 查看可选参数
