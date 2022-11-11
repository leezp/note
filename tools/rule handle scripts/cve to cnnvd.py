# -*- coding:utf-8 -*-
__author__ = 'leezp'
__date__ = 20211011
import requests
import re

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept-Encoding': "gzip, deflate",
    'Host': 'www.cnnvd.org.cn',
    'Origin': 'http://www.cnnvd.org.cn',
    'Referer': 'http://www.cnnvd.org.cn/web/vulnerability/queryLds.tag',
    'Connection': 'Keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
}
f = open('cve 编号', "r", encoding='utf-8')
for chunk in f.readlines():
    search = chunk.strip()
    data = 'CSRFToken=&cvHazardRating=&cvVultype=&qstartdateXq=&cvUsedStyle=&cvCnnvdUpdatedateXq=&cpvendor=&relLdKey=&hotLd=&isArea=&qcvCname=&qcvCnnvdid=' + search + '&qstartdate=&qenddate='
    resp = requests.post('http://www.cnnvd.org.cn/web/vulnerability/queryLds.tag', data=data, headers=headers,
                         verify=False)

    r = re.compile(r'CNNVD=(.*?)"')
    res = r.search(resp.text)
    with open('cve-cnnvd.json', 'a', encoding='utf-8') as f:
        f.write('"' + chunk.strip() + '":"' + res.group(1) + '",' + '\n')
