# -*- coding:utf-8 -*-
__author__ = 'leezp'
__date__ = 20220304
import pycurl  # https://www.lfd.uci.edu/~gohlke/pythonlibs/#pycurl
# pycurl 提取证书信息 (不推荐)
url = "https://10.10.40.63:50050"


def probe_assets(url):
    c = pycurl.Curl()
    c.setopt(pycurl.URL, url)  # (网址)
    c.setopt(pycurl.VERBOSE, 1)  # -v
    c.setopt(pycurl.SSL_VERIFYPEER, 0)  # 禁用证书验证和host验证
    c.setopt(pycurl.SSL_VERIFYHOST, 0)
    return c.perform()  # 提交


try:
    probe_assets(url)
except Exception as e:
    # print(e)
    pass

# 问题：直接回显了获取不到返回值
