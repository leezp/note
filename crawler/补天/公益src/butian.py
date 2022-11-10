#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__:leezp
# __date__:2019-10-16

import json
import requests
import time
from bs4 import BeautifulSoup
import random

headers = {
    'Host': 'www.butian.net',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh,zh-CN;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'https://www.butian.net/Reward/plan',
    'Cookie': 'your cookie',
    'Connection': 'keep-alive'
}
# 禁用安全警告
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
PROXIES = ['http://27.152.90.235:9999',
           'http://59.57.148.193:9999',
           'http://119.23.149.110:8118',
           'http://117.28.97.61:9999',
           'http://59.57.148.125:9999',
           'http://113.194.29.143:9999',
           'http://59.57.148.33:9999',
           'http://27.152.90.154:9999',
           'http://183.164.238.158:9999',
           'http://218.91.112.94:9999',
           'http://59.57.149.199:9999',
           'http://182.35.84.138:9999',
           'http://222.89.32.145:8070',
           'http://120.25.254.75:8118',
           'http://113.124.95.56:9999',
           'http://222.89.32.148:9999',
           'http://119.23.47.95:8118',
           'http://123.101.231.73:9999',
           'http://120.25.237.23:8118']


# s=1&p=38&token=
def spider(allPages):
    '''
    爬取所有公益厂商的ID
    保存为id.txt
    :return:
    '''

    for i in range(108, int(allPages) + 1):
        data = {'s': '1', 'p': i, 'token': ''}
        res = requests.post('https://www.butian.net/Reward/pub', data=data, headers=headers, verify=False)

        allResult = {}
        try:
            allResult = json.loads(res.content.decode('utf-8'))
        except Exception as e:
            print(e)
            print('第' + str(i) + '页')
            continue
        currentPage = str(allResult['data']['current'])
        currentNum = str(len(allResult['data']['list']))
        print('正在获取第' + currentPage + '页厂商数据')
        print('本页共有' + currentNum + '条厂商')
        for num in range(int(currentNum)):
            print('厂商名字:' + allResult['data']['list'][int(num)]['company_name'] + '\t\t厂商ID:' +
                  allResult['data']['list'][int(num)][
                      'company_id'])  # + '\t\t厂商类型:' +allResult['data']['list'][int(num)]['industry']
            base = 'https://www.butian.net/Loo/submit?cid='
            with open('id.txt', 'a') as f:
                f.write(base + allResult['data']['list'][int(num)]['company_id'] + '\n')
        time.sleep(5)  # time.sleep(random.randint(1,5))


def Url():
    '''
    遍历所有的ID
    取得对应的域名
    保存为target.txt
    :return:
    '''
    headers = {
        'Host': 'www.butian.net',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'https://www.butian.net',
        'Cookie': 'your cookie',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    }
    with open('id.txt', 'r') as f:
        # target='https://www.butian.net/Loo/submit?cid=62236'
        count = 0
        for target in f.readlines():
            target = target.strip()
            count += 1
            # print(target)
            getUrl = requests.get(target, headers=headers, verify=False)
            result = getUrl.text
            info = BeautifulSoup(result, 'lxml')
            url = info.find(name='input', attrs={"name": "host"})
            # 获取厂商测试范围：
            all_t = info.find_all("li", class_="comTestArea")
            if len(all_t) != 0:
                for k in all_t:
                    num = k.find_all('var')
                    range = num[0].text
            name = info.find(name='input', attrs={"name": "company_name"})
            try:
                time.sleep(1)
                cs_name = name.attrs['value']
                lastUrl = url.attrs['value']
            except:
                time.sleep(10)
            print('厂商:' + cs_name + '\t网址:' + lastUrl)
            with open('target.txt', 'a', encoding='utf-8') as t:
                t.write(cs_name + ' ' + '厂商测试范围：' + range + ',' + lastUrl + '\n')
            if (count / 40 == 0):
                time.sleep(10)
    print('The target is done!')


if __name__ == '__main__':
    '''
    data = {
            's': '1',
            'p': '1',
            'token': ''
        }
    '''
    res = requests.get('https://www.butian.net/Reward/pub', headers=headers, verify=False)
    resp = res.content.decode('utf-8')
    allResult = {}
    allResult = json.loads(resp)
    allPages = str(allResult['data']['count'])
    print('共' + allPages + '页')
    # 爬取补天的索引url 保存为 id.txt
    spider(allPages)
    # 爬取索引url里厂商的url
    Url()
