#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# __author__:leezp
# __date__:2019-06-30
# Local:  Win7 (python3)
# 成功配置代理，抓包可证
from urllib import request

if __name__ == "__main__":
    # 访问网址
    # url = 'https://google.com'  # 测试https
    url = 'http://www.gatherproxy.com/zh/'  # 测试http # 国外免费代理ip网站
    # url = 'http://192.168.1.5:8080/one.jsp' # 访问不了本地ip;局域网ip也访问不了，未解决  报错urllib.error.HTTPError: HTTP Error 500: Internal Privoxy Error
    # url = 'http://127.0.0.1:8082/one.jsp'
    # 这是代理IP
    proxy = [{'http': '127.0.0.1:1081', 'https': 'socks5h://127.0.0.1:1081'}]  # 使用时需要ss填写正确，并且关闭代理软件
    '''
    异常： requests.exceptions.SSLError: SOCKSHTTPSConnectionPool(host='www.google.com', port=443): Max retries exceeded with url: / (Caused by SSLError(SSLError("bad handshake: SysCallError(-1, 'Unexpected EOF')")))
    解决： 'https':'socks5://127.0.0.1:1081' 改成 'https':'socks5h://127.0.0.1:1081'
    # the proxy string, socks5h:// and socks4a:// mean that the hostname is to be resolved by the socks server.
    # socks5:// and socks4:// mean the hostname is to be resolved locally
    '''
    # 创建ProxyHandler
    httpproxy_handler = request.ProxyHandler(proxy[0])
    nullproxy_handler = request.ProxyHandler({})
    # 定义一个代理开关
    proxySwitch = True
    # 根据代理开关是否打开，使用不同的代理模式
    if proxySwitch:
        # 创建Opener
        opener = request.build_opener(httpproxy_handler)
    else:
        opener = request.build_opener(nullproxy_handler)

    # 添加User Angent
    opener.addheaders = [('User-Agent',
                          'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')]
    '''
    1. 如果这么写，只有使用opener.open()方法发送请求才使用自定义的代理，而urlopen()则不使用自定义代理。
    #response = opener.open(request)
    
    2. 如果这么写，就是将opener应用到全局，之后所有的，不管是opener.open()还是urlopen() 发送请求，都将使用自定义代理。
    # urllib2.install_opener(opener)
    # response = urlopen(request)
    '''
    # 安装OPener
    # request.install_opener(opener)
    # 使用自己安装好的Opener
    # response = request.urlopen(url)
    # 如果不想安装也可以直接使用opener来执行
    response = opener.open(url)
    # 读取相应信息并解码
    html = response.read().decode("utf-8")
    # 打印信息
    print(html)
