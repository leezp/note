# -*- coding:utf-8 -*-
import socket

# 客户端
ip = "127.0.0.1"
port = 52052
new_socket = socket.socket()
new_socket.connect((ip, port))
new_socket.send("请求给我计算下1+5=多少？".encode(encoding='utf-8'))  # 发生数据
print("客户端发给服务端：请求给我计算下1+5=多少？")
back_str = new_socket.recv(80000).decode()  # 结束数据
print("服务端发给客户端：" + back_str)
new_socket.close()  # 关闭客户端
print("客户端结束运行")
