# -*- coding:utf-8 -*-
import socket

# 服务端
new_socket = socket.socket()  # 创建 socket 对象
ip = "127.0.0.1"  # 获取本地主机名
port = 52052  # 设置端口
new_socket.bind((ip, port))  # 绑定端口
new_socket.listen(5)  # 等待客户端连接并设置最大连接数
while True:
    new_cil, addr = new_socket.accept()  # 建立客户端连接。
    print('新进来的客户端的地址：', addr)
    print(new_cil.recv(80000).decode())
    new_cil.send(bytes("答案为6", encoding='utf8'))
    new_cil.close()  # 关闭连接
