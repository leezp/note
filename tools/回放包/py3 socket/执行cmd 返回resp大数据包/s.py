# -*- coding:utf-8 -*-
__author__ = 'shisanjun'

import socket
import subprocess

server = socket.socket()

server.bind(("127.0.0.1", 50050))
server.listen(5)

while True:
    conn, addr = server.accept()
    print("new conn:", addr)

    while True:
        print(addr)
        data = conn.recv(1024)
        print(len(data))
        print(data.decode())
        if not data:
            print("conn close ", addr)
            break
        print(data.decode())
        cmd_res = subprocess.Popen(data.decode(), shell=True, stdout=subprocess.PIPE)
        outread = cmd_res.stdout.read()
        print(len(outread))
        conn.send(("%s" % len(outread)).encode("utf-8"))

        print(outread.decode("gb2312"))
        conn.send(outread)
