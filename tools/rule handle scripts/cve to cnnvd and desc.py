# -*- coding:utf-8 -*-
__author__ = 'leezp'
__date__ = 20211011
import requests
import re

'''
生成 CVE:CNNVD 漏洞名称,漏洞类型,漏洞描述

格式:
"CVE":"CNNVD",漏洞名称,漏洞类型,漏洞描述#000;
"CVE":"CNNVD",漏洞名称,漏洞类型,漏洞描述#000;
'''

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
regex_vuln_long_name = re.compile(r"CNNVD=.*?onmouseover.*?,'(.*?)'")
regex_vuln_short_name = re.compile(r'CNNVD=.*?>([\s\S]*?)</a>')

for chunk in f.readlines():
    search = chunk.strip()
    data = 'CSRFToken=&cvHazardRating=&cvVultype=&qstartdateXq=&cvUsedStyle=&cvCnnvdUpdatedateXq=&cpvendor=&relLdKey=&hotLd=&isArea=&qcvCname=&qcvCnnvdid=' + search + '&qstartdate=&qenddate='
    resp = requests.post('http://www.cnnvd.org.cn/web/vulnerability/queryLds.tag', data=data, headers=headers,
                         verify=False)

    r = re.compile(r'CNNVD=(.*?)"')
    res = r.search(resp.text)
    vuln_name = regex_vuln_long_name.search(resp.text)
    name = ''
    if vuln_name:
        name = vuln_name
    else:
        name = regex_vuln_short_name.search(resp.text)

    url2 = 'http://www.cnnvd.org.cn/web/xxk/ldxqById.tag?CNNVD=' + res.group(1)
    resp2 = requests.get(url2, headers=headers)
    regex_url = re.compile(r'<a href="(.*?)" target="_blank" class="a_title2"')
    regex_desc = re.compile(r'<p  style="text-indent:2em">([\s\S]*?)</p>')
    regex_vuln_type = re.compile(r'<a style="color:#4095cc;cursor:pointer;">([\s\S]*?)</a>')
    desc = regex_desc.search(resp2.text)
    vuln_type = regex_vuln_type.search(resp2.text).group(1).strip()

    with open('cve-cnnvd.json', 'a', encoding='utf-8') as f:
        f.write('"' + chunk.strip() + '":"' + res.group(1) + '",' + name.group(
            1).strip() + ',' + vuln_type + ',' + desc.group(
            1).strip() + '#000;' + '\n')
