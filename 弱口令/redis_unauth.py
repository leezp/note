# -*- coding:utf-8 -*-
__author__ = 'leezp'
__date__ = 20200116
import time
import queue
import socket
from threading import Thread
from urllib.parse import urlparse

sock = socket.socket()  # 创建套接字
ip = '192.168.1.101'


def poc(url):
    url = url2ip(url)  # 将url转换成ip地址
    if url:
        port = int(url.split(':', -1)) if ':' in url else 6379  # redis默认端口是6379
        host = url.split(':')[0]
        payload = b'*1\r\n$4\r\ninfo\r\n'  # 发送的数据
        s = socket.socket()
        socket.setdefaulttimeout(3)  # 设置超时时间
        try:
            s.connect((host, port))
            s.send(payload)  # 发送info命令
            response = s.recv(1024).decode()
            s.close()
            if response and 'redis_version' in response:
                return True, '%s:%s' % (host, port)
        except (socket.error, socket.timeout):
            pass

    return False, None


def url2ip(url):
    """
    url转换成ip
    argument: url
    return: 形如www.a.com:80格式的字符串 若转换失败则返回None
    """

    try:
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://' + url
        ip = urlparse(url).netloc
        return ip
    except (ValueError, socket.gaierror) as e:
        pass

    return None


def create_queue(file_name):
    """
    创建数据队列
    argument: file_name -> 输入文件名
    return: data,total 数据队列,数据总数
    """
    total = 0
    data = queue.Queue()
    for line in open(file_name):
        url = line.strip()
        if url:
            # 跳过空白的行
            data.put(url)
            total += 1

    data.put(None)  # 结束标记
    return data, total


def start_jobs(data, num):
    """
    启动所有工作线程
    """
    is_alive = [True]

    def job():
        """工作线程"""
        while is_alive[0]:
            try:
                url = data.get()
                if url == None:
                    # 遇到结束标记
                    break
                code, result = poc(url)  # 验证漏洞
                if code:
                    print(result)  # 存在漏洞
            except:
                is_alive[0] = False
        data.put(None)  # 结束标记

    jobs = [Thread(target=job) for i in range(num)]  # 创建多线程
    for j in jobs:
        j.setDaemon(True)
        j.start()  # 启动线程

    for j in jobs:
        j.join()  # 等待线程退出


def main():
    import sys
    file_name = sys.argv[1]  # 输入文件
    num = 16  # 线程数
    data, total = create_queue(file_name)  # 创建数据队列
    print('total: %s' % total)
    begin = time.time()
    start_jobs(data, num)  # 启动工作线程
    end = time.time()
    print('spent %ss' % str(end - begin))


def singeip(ip):
    sock = socket.socket()  # 创建套接字
    try:
        sock.connect((ip, 6379))  # 连接
        sock.send(b'*1\r\n$4\r\ninfo\r\n')  # 发送info命令
        response = sock.recv(1024).decode()  # 接收响应数据
        if 'redis_version' in response:
            result = True  # 存在漏洞
        else:
            result = False  # 不存在漏洞
    except (socket.error, socket.timeout) as e:
        # 连接失败，可能端口6379未开放，或者被拦截，此时认为漏洞不存在
        result = False
    print(result)


if __name__ == '__main__':
    main()  # 文件批量验证 python36 redis_unauth.py input.txt
    # singeip('192.168.1.101') # 单ip验证
