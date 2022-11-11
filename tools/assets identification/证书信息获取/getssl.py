# -*- coding:utf-8 -*-
__author__ = 'leezp'
__date__ = 20220304
import ssl
import OpenSSL
from dateutil import parser
import re
# 证书信息获取

def judge(ip, port):
    # 获取证书返回信息，公钥
    resp = ssl.get_server_certificate(
        (ip, port))  # 获取公钥   get_server_certificate(('www.qq.com', 443))
    # print(resp)
    # 解析证书信息
    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, resp)
    subject = x509.get_subject()
    issuer = x509.get_issuer()
    time1 = parser.parse(x509.get_notBefore().decode("UTF-8"))
    time2 = parser.parse(x509.get_notAfter().decode("UTF-8"))
    return subject, time1, time2, issuer


subject, time1, time2, issuer = judge('10.10.40.63', 50050)
print(subject)
print(time1)
print(time2)
print(issuer)
# print(type(subject))


m = re.search('cobaltstrike', str(subject).replace("<", "").replace(">", ""), re.I)
if m:
    print("cs")
