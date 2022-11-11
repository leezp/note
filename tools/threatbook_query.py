# coding:utf-8
__author__ = 'leezp'
__date__ = 20200606
## 查询微步，验证ip和域名可信度


import requests
import re
import csv
from lxml import etree
import time

headers = {
    'referer': 'XXX',
    'cookie': 'XXX',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}
# //*[@id="wrapper"]/div[3]/div[2]/div[1]/div[3]/div
# //*[@id="wrapper"]/div[3]/div[2]/div[6]/div[2]/p
# 微步在线安全分析实验室暂未标记标签信息。
# //*[@id="wrapper"]/div[3]/div[2]/div[6]/div[2]


r = re.compile(r'\d+?\.\d+?\.\d+?\.\d')
with open('host.csv') as csvfile:
    csv_reader = csv.reader(csvfile)
    birth_header = next(csv_reader)  # 跳过第一行
    for row in csv_reader:
        line = row[0]
        if r.search(line):
            # ip
            url = 'https://x.threatbook.cn/nodev4/ip/' + line
            resp = requests.get(url, headers=headers)
            text = resp.text
            html = etree.HTML(text)
            list = html.xpath('//*[@id="wrapper"]/div[2]/div[2]/div[6]/div[2]/div')
        else:
            # domain
            url = 'https://x.threatbook.cn/nodev4/domain/' + line
            resp = requests.get(url, headers=headers)
            text = resp.text
            html = etree.HTML(text)
            list = html.xpath('//*[@id="wrapper"]/div[3]/div[2]/div[6]/div[2]/div[1]')
        if list:
            print(line + ',' + list[0].text.strip())
        else:
            print(line + ',' + '白')
        time.sleep(20)
