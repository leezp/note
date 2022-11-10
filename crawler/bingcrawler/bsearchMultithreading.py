# ! /usr/bin/env python3
# -*- coding:utf-8 -*-
# __author__:leezp
# __date__:2019-07-07
# Local:  Win7 (python3)
# 从bing搜集子域名，未去重(多线程)
# 线程锁 lock() 这块还是不太懂

import requests
import urllib.parse
from bs4 import BeautifulSoup
import datetime
import threading
import queue

# # maxsize:指定队列中能够存储的最大的数据量
# # dataqueue = queue.Queue(maxsize=40)
# #
# # for i in range(0,50):
# #     if not dataqueue.full():
# #         dataqueue.put(i)
# #
# # #判断队列是否为空
# # isempty = dataqueue.empty()
# # print(isempty)
# #
# # #判断队列是否存满了
# # isfull = dataqueue.full()
# # print(isfull)
# #
# # #判断队列的大小
# # size = dataqueue.qsize()
# # print(size)
# #
# # #先进的先出
# # print(dataqueue.get())

# 注意：队列是线程之间常用的数据交换形式,因为队列在线程间,是线程安全的
"""
1.创建一个任务队列：存放的是待爬取的url地址
2.创建爬取线程：执行任务的下载
3.创建数据队列:存放爬取线程获取的页面源码
4.创建解析线程:解析html源码,提取目标数据,数据持久化
"""


def download_page_data(taskQueue, dataQueue):
    """
    执行下载任务
    :param taskQueue: 从任务队列里面取出任务
    :param dataQueue: 将获取到的页面源码存到dataQueue队列中
    :return:
    """
    while not taskQueue.empty():
        page = taskQueue.get()
        print(threading.currentThread().name, '正在下载第' + str(page) + '页')

        site = 'baidu.com'
        if (page == 1):
            full_url = "https://cn.bing.com/search?q=site%3a" + site + "&go=%E6%90%9C%E7%B4%A2&qs=ds&first=1&FORM=PERE"
        if (page > 1):
            n = 10 * (page - 1)
            full_url = "https://cn.bing.com/search?q=site%3a" + site + "&go=%E6%90%9C%E7%B4%A2&qs=ds&first=" + str(
                n) + "&FORM=PERE"
        req_header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0',
                      'cookie': 'MUID=2CBF14D111AD68023168199A15AD6B49; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=01E493D4FE814DFCB736E70A7EB0F091&dmnchg=1; MUIDB=2CBF14D111AD68023168199A15AD6B49; SRCHUSR=DOB=20190620&T=1562375703000; ENSEARCH=BENVER=0; _EDGE_S=SID=28B84CCECC7B65B1223B415FCD556403; SRCHHPGUSR=CW=1366&CH=157&DPR=1&UTC=480&WTS=63697972503; _SS=SID=28B84CCECC7B65B1223B415FCD556403&HV=1562378631',
                      'accept': '*/*'
                      }
        response = requests.get(full_url, headers=req_header)
        dataQueue.put(response.content)


def parse_data(dataqueue, lock):
    """
    解析数据,从dataQueue中取出数据进行解析
    :param dataQueue:
    :return:
    """
    while not dataqueue.empty():
        print(threading.currentThread().name, '正在解析')
        html = dataqueue.get()
        soup = BeautifulSoup(html, 'lxml')
        job_bt = soup.findAll('h2')
        for j in job_bt:
            link = j.a.get('href')
            domain = str(urllib.parse.urlparse(link).scheme + "://" + urllib.parse.urlparse(link).netloc)

            # lock.acquire()  # 加锁
            # 程序会自行关闭使用完的文件
            with open("bing_result.txt", "a", encoding='utf-8') as f:
                f.write(domain + '\n')
        # lock.release()  # 解锁


if __name__ == '__main__':
    starttime = datetime.datetime.now()
    # 创建任务队列
    taskQueue = queue.Queue()

    # 设置爬取的页数  range(1, 101)  爬取  1-100页
    for i in range(1, 2001):
        taskQueue.put(i)

    # 创建数据队列
    dataQueue = queue.Queue()

    # 创建线程执行下载任务
    threadName = ['下载线程1号', '下载线程2号', '下载线程3号', '下载线程4号']
    crawl_thread = []
    for name in threadName:
        # 创建线程
        thread_crawl = threading.Thread(
            target=download_page_data,
            name=name,
            args=(taskQueue, dataQueue)
        )
        crawl_thread.append(thread_crawl)
        # 开启线程
        thread_crawl.start()

    # 让所有的爬取线程执行完毕,在回到主线程中继续执行
    for thread in crawl_thread:
        thread.join()

    # 加线程锁lock
    lock = threading.Lock()
    # 创建解析线程,从dataQueue队列中取出页面源码进行解析
    threadName = ['解析线程1号', '解析线程2号', '解析线程3号', '解析线程4号']
    parse_thread = []
    for name in threadName:
        # 创建线程
        thread_parse = threading.Thread(
            target=parse_data,
            name=name,
            args=(dataQueue, lock)
        )
        parse_thread.append(thread_parse)
        # 开启线程
        thread_parse.start()

    for thread in parse_thread:
        thread.join()

    endtime = datetime.datetime.now()
    print((endtime - starttime).seconds)
