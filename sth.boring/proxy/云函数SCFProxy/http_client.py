# -*- coding:utf-8 -*-
import sys
sys.path.append("/usr/local/lib/python3.6/site-packages")
sys.path.append("/usr/lib/python3.6/site-packages")
import http
import json
import pickle
from typing import List
from random import choice
from urllib.parse import urlparse
from base64 import b64encode, b64decode
from mitmproxy import ctx
import mitmproxy
from mitmproxy import http
from mitmproxy.net.http import Headers

scf_servers: List[str] = ['https://service-fe2l4nq9-XXX.sh.apigw.tencentcs.com/release/helloworld-api']
SCF_TOKEN = "Token"


def request(flow: mitmproxy.http.HTTPFlow):
    scf_server = choice(scf_servers)
    info = ctx.log.info
    
    r = flow.request
    info(str(r.headers))
    data = {
        "method": r.method,
        "url": r.pretty_url,
        "headers": dict(r.headers),
        "cookies": dict(r.cookies),
        "params": dict(r.query),
        "data": b64encode(r.raw_content).decode("ascii")
    } 
    flow.request = flow.request.make(
        "POST",
        url=scf_server,
        content=json.dumps(data),
        headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, compress",
            "Accept-Language": "en-us;q=0.8",
            "Cache-Control": "max-age=0",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
            "Connection": "close",
            "Host": urlparse(scf_server).netloc,
            "SCF-Token": SCF_TOKEN,
        },
    )
    
def response(flow):
    if flow.response.status_code != 200:
        mitmproxy.ctx.log.warn("Error")

    if flow.response.status_code == 401:
        flow.response.headers = Headers(content_type="text/html;charset=utf-8")
        return

    if flow.response.status_code == 433:
        flow.response.headers = Headers(content_type="text/html;charset=utf-8")
        flow.response.content = (
            "<html><body>操作已超过云函数服务最大时间限制，可在函数配置中修改执行超时时间</body></html>",
        )
        return

    if flow.response.status_code == 200:
        resp = flow.response
        headers=resp.headers
        statusCode=resp.status_code
        info = ctx.log.info
        info(str(statusCode))
        flow.response = flow.response.make(
            content=resp.content
        )
