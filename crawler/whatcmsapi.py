#! /usr/bin/env python3
# coding=utf-8
# __author__:leezp
# __date__:2019-08-19
# whatweb cms指纹识别api示例 每天每个ip1500次
# http://whatweb.bugscaner.com/
# 进行json压缩传输,经测试,压缩后可节省将近5-10倍的宽带
try:
    import requests
except:
    print(u"返回桌面,Shift+鼠标右键,在此处打开命令窗口(W),输入:pip install requests")
import zlib
import json
import queue


def whatweb(url):
    requests.packages.urllib3.disable_warnings()
    response = requests.get(url, verify=False, timeout=5)
    # 上面的代码可以随意发挥,只要获取到response即可
    # 下面的代码您无需改变，直接使用即可
    whatweb_dict = {"url": response.url, "text": response.text, "headers": dict(response.headers)}
    whatweb_dict = json.dumps(whatweb_dict)
    whatweb_dict = whatweb_dict.encode()
    whatweb_dict = zlib.compress(whatweb_dict)
    data = {"info": whatweb_dict}
    return requests.post("http://whatweb.bugscaner.com/api.go", files=data)

# 次数用完的响应：response.json() {'status': 555, 'info': 'limit'}
if __name__ == '__main__':
    q = queue.Queue()
    file = open('input.txt', encoding='UTF-8')  # encoding='UTF-8'
    for x in file.readlines():
        q.put(x.strip())
    while not q.empty():
        url = q.get()
        try:
            response = whatweb(url)
            print(u"今日识别剩余次数")
            print(response.headers["X-RateLimit-Remaining"])
            print(u"识别结果")
            print(url + ' ' + str(response.json()))
            with open('api.txt', 'a', encoding='UTF-8') as f:
                f.write(url + ',' + str(response.json()) + '\n')
        except Exception as e:
            print(e)
            print(url + ' except')
            with open('excepturl2.txt', 'a', encoding='UTF-8') as f:
                f.write(url + '\n')
            pass
