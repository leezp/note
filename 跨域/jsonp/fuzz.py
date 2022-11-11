import requests
import argparse
import re
from tld import get_fld
jsonps = ["callback", "_callback", "func", "cb", "_cb", "jsonp", "jsonpcallback", "jsonpcb", "json", "jsoncallback", "jbc", "jsonp_cb", "call", "callBack", "jsonCallback", "jsonpCb", "ca", "jsonp_Cb"]
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
}
def send(url):
    rep = requests.get(url, headers=headers)
    return rep
def CorsFuzz(url):
    # 获取本域名
    subdomin = re.findall(r'(http.*://[^/]*)', url, re.DOTALL)[0]
    protocol = re.findall(r'(http.*://)', url, re.DOTALL)[0]
    # 获取主域名
    domain = get_fld(subdomin)
    # print(subdomin,domain)
    # 创建 cors 字典 本身 主域名 任意域名 以其开头 其他子域名
    cors = [subdomin, protocol + domain, protocol + "test.com", protocol + domain + ".test.com", protocol + "test." + domain]
    # print(cors)
    flag = 0
    for cor in cors:
        headers["Origin"] = cor
        print("------Origin: " + cor)
        try:
            # 获取响应头
            # print(url)
            reph = send(url).headers
            # print(reph)
            if "Access-Control-Allow-Origin" in str(reph):
                print(url + "存在 CORS，其 Origin 头为" + cor + "\n返回值为 Access-Control-Allow-Origin:" + reph["Access-Control-Allow-Origin"])
                flag = 1
        except:
            print(url + " 请求错误")
    if flag == 0:
        print(url+" 不存在 CORS 漏洞")
def JsonpFuzz(url):
    flag = 0
    for jsonp in jsonps:
        jsonp = jsonp + "=myJsonpFunc"
        try:
            if "?" in url:
                newurl = url + "&" + jsonp
                print("------" + newurl)
                rep = send(newurl).content.decode("utf-8")
            else:
                newurl = url + "?" + jsonp
                print("------" + newurl)
                rep = send(newurl).content.decode("utf-8")
            if "myJsonpFunc" in rep:
                flag = 1
                print(url + "可能存在 jsonp 劫持，回调函数为：" + jsonp)
                break
        except:
            print(url + " 请求错误")
    if flag == 0:
        print(url+" 不存在 jsonp 回调函数")
def ImgFuzz(url):
    # 获取原数据大致大小
    repl = len(send(url).content)
    par = "height=250&width=250&w=250&h=250&size=250&margin=250&font_size&=250length=250"
    try:
        if "?" in url:
            print(url + "&" + par)
            newl = len(send(url + "&" + par).content)
        else:
            print(url + "&" + par)
            newl = len(send(url + "?" + par).content)
    except:
        print(url + " 请求错误")
    if abs(newl - repl) >= 1000:
        # 当数据大小相差 1000 时
        print(url + "可能存在验证码 Dos\n测试参数为：" + par)
def main(url, method):
    if method=="cors":
        CorsFuzz(url)
    elif method=="jsonp":
        JsonpFuzz(url)
    else:
        ImgFuzz(url)
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Easy Fuzz')
    parser.add_argument("-u", "--url", help="指定URL", default="img")
    parser.add_argument("-m", "--method", help="指定操作")
    args = parser.parse_args()
    url = args.url
    method = args.method
    # url = "https://baidu.com"
    # method = "cors"
    main(url, method)