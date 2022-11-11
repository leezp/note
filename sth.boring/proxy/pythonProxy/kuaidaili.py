# -*- coding:utf-8 -*-
__author__ = 'leezp'
__date__ = 20220617
import requests
import re
import time
import random
import urllib.request

# 爬取快代理
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36"}


def getHtml(url, charSet="utf-8"):
    resp = requests.get(url, headers=headers)

    return resp.text


def createOpenner(ipList):
    m_proxy = urllib.request.ProxyHandler({"http": random.choice(ipList)})
    openner = urllib.request.build_opener(m_proxy)
    urllib.request.install_opener(openner)


def getProxyList(url, iPage=10):
    ipList = []
    for i in range(1, iPage + 1):
        html_str = getHtml(url + str(i))

        ip = re.findall("IP\">((?:\d{1,3}\.){3}(?:\d{1,3}))(?:[\s\S]{0,50})\"PORT\">(\d{2,4})", html_str)
        for addr in ip:
            ipList.append(addr[0] + ":" + addr[1])
        time.sleep(2)

    return ipList


n = 10  # 爬取n页
ipList = getProxyList("https://free.kuaidaili.com/free/inha/", n)

print(ipList)

# resp=requests.get("https://free.kuaidaili.com/free/inha/",headers=headers)
# print(resp)
