#-*- encoding: utf-8 -*-
import json
import socket
import sys
import binascii
reload(sys)
sys.setdefaultencoding('utf-8')
if __name__=="__main__":
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(("ip", 8080))
    s.send('''\xabsth.''') # 十六进制数据，字符串等正文
    print s.recv(1024)
    s.close()