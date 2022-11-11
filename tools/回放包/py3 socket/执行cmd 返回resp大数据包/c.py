# -*- coding:utf-8 -*-
__author__ = 'shisanjun'

import socket

client = socket.socket()
client.connect(("127.0.0.1", 50050))

while True:
    cmd = input(">>:").strip()
    if len(cmd) == 0: continue
    print(cmd)
    client.send(cmd.encode("utf-8"))
    print("res")
    res_size = client.recv(1024).decode("utf-8")
    size = 0
    while size < int(res_size):
        res = client.recv(1024)
        print(res.decode("gb18030"))
        size += len(res)  # 这里要用len(),因为最后一次长度不固定
