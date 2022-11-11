# -*- coding:utf-8 -*-
__author__ = 'leezp'
__date__ = 20220307
import requests
import re

url = "http://192.168.255.153:8080"
resp = requests.get(url)
r = resp.text
re1 = re.compile(r'<title>(.*?)</title>')
re2 = re.compile(r'title"><h1>(.*?)</h1>')
r2 = re1.search(r)
r3 = re2.search(r)
if r2 and r3:
    if 'Burp Suite'.lower() in r2.group(1).lower() and 'Burp Suite'.lower() in r3.group(1).lower():
        print('Burp Suite')
