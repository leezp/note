# ! /usr/bin/env python3
# -*- coding:utf-8
# __author__:leezp
# __date__:2019-08-11
import queue
from bs4 import BeautifulSoup
import requests
import time

q = queue.Queue()
file = open('gaoxiao.txt', encoding='UTF-8')
for x in file.readlines():
    q.put(x.split(',')[1].strip())

while not q.empty():
    url = q.get()
    try:
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content.decode('utf-8'), 'lxml')
        all_t = soup.find_all("span", class_="judge-empty")
        if len(all_t) != 0:
            for k in all_t:
                num = k.find_all('a')
                if len(num) ==1:
                    try:
                        with open("gaoxiaoip.txt", "a", encoding='utf-8') as f:
                            f.write(num[0]['href'].strip() + '\n')
                        break
                    except:
                        print(url)
                        pass
                elif len(num)>1:
                    #https://gaokao.chsi.com.cn/sch/schoolInfo--schId-390.dhtml
                    #https://gaokao.chsi.com.cn/sch/schoolInfo--schId-1783356075.dhtml
                    print(url)
                    for x in range(1,len(num)):
                        try:
                            link=num[x]['href']
                            with open("gaoxiaoip.txt", "a", encoding='utf-8') as f:
                                f.write(link.strip() + '\n')
                            break
                        except:
                            pass
    except:
        time.sleep(5)
        print ('except '+url)
        pass
