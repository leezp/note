# ! /usr/bin/env python3
# _*_  coding:utf-8 _*_
# __author__:leezp
# __date__:2019-07-06
# Local:  Win7 (python3)
# 从bing 搜集子域名并去重(单线程)

import requests
import urllib.parse
from bs4 import BeautifulSoup
import datetime

'''
page 规律
1  10  20  30  40
page=1  : 1
page>1  : 10*(page-1)
'''


def file_put(str):
    with open("bing_result.txt", "a", encoding='utf-8') as f:
        f.write(str)


def bing_search(site, page):
    Subdomain = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0',
               'cookie': 'MUID=2CBF14D111AD68023168199A15AD6B49; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=01E493D4FE814DFCB736E70A7EB0F091&dmnchg=1; MUIDB=2CBF14D111AD68023168199A15AD6B49; SRCHUSR=DOB=20190620&T=1562375703000; ENSEARCH=BENVER=0; _EDGE_S=SID=28B84CCECC7B65B1223B415FCD556403; SRCHHPGUSR=CW=1366&CH=157&DPR=1&UTC=480&WTS=63697972503; _SS=SID=28B84CCECC7B65B1223B415FCD556403&HV=1562378631',
               'accept': '*/*'
               }
    for i in range(1, int(page)):
        try:
            if (i == 1):
                url = "https://cn.bing.com/search?q=site%3a" + site + "&go=%E6%90%9C%E7%B4%A2&qs=ds&first=1&FORM=PERE"
            if (i > 1):
                n = 10 * (i - 1)
                url = "https://cn.bing.com/search?q=site%3a" + site + "&go=%E6%90%9C%E7%B4%A2&qs=ds&first=" + str(
                    n) + "&FORM=PERE"
            html = requests.get(url, headers=headers, timeout=3)

            # 也可以提取<cite> 的内容
            soup = BeautifulSoup(html.content, 'lxml')
            job_bt = soup.findAll('h2')
            for j in job_bt:
                link = j.a.get('href')
                ''' 提取域名的新方式
                # print(urllib.parse.urlparse(url))
                # 打印结果：ParseResult(scheme='https', netloc='xin.baidu.com', path='/', params='', query='fl=1&amp;castk=LTE%3D', fragment='')
                '''
                domain = str(urllib.parse.urlparse(link).scheme + "://" + urllib.parse.urlparse(link).netloc)
                Subdomain.append(domain)
        except:
            pass
    Subdomain = list(set(Subdomain))  # 去重
    return Subdomain


if __name__ == '__main__':
    '''
    if len(sys.argv) == 3:
        site = sys.argv[1]
        page = sys.argv[2]
    else:
        print("usage: %s baidu.com 10" % sys.argv[0])
        sys.exit(-1)
    '''
    starttime = datetime.datetime.now()
    site = 'baidu.com'  # 输入爬取站点名称
    page = 1000  # 输入爬取页数
    Subdomain = bing_search(site, page)

    with open("bing_result.txt", "a", encoding='utf-8') as f:
        for i in Subdomain:
            f.write(i + '\n')

    endtime = datetime.datetime.now()
    print((endtime - starttime).seconds)
