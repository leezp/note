# coding=utf-8
# grab ip proxies from xicidaili
import requests
from multiprocessing.dummy import Pool as ThreadPool
from lxml import etree
import json
import time

# 测试 ，爬50页，休眠20s，没有被封ip
# 输出格式{"http": ["http://114.226.245.15:9999", "http://114.99.14.208:9999"], "https": ["https://223.199.26.204:9999", "https://223.199.21.106:9999"]}


IP_POOL = 'ip_pool.txt'
URL = 'http://www.xicidaili.com/nn/'  # IP代理 高匿
# URL = 'http://www.xicidaili.com/wt/' #IP代理 http
RUN_TIME = time.strftime("%Y-%m-%d %H:%M", time.localtime())  # 执行时间

# 用字典存放有效ip代理
alive_ip = {"http": [], "https": []}
# 多线程
pool = ThreadPool(20)
iplist = []


# 返回html文本
def get_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate",
        "Referer": "https://www.xicidaili.com/",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    r = requests.get(url, headers=headers)
    r.encoding = 'utf-8'
    return r.text


# 测试ip代理是否存活
def test_alive(proxy):
    global alive_ip
    proxies = {'http': proxy}
    try:
        r = requests.get('https://www.baidu.com', proxies=proxies, timeout=3)
        if r.status_code == 200:
            if proxy.startswith('https'):
                alive_ip["https"].append(proxy)
            else:
                alive_ip["http"].append(proxy)
    except:
        print("%s无效!" % proxy)


# 解析html文本，获取ip代理
def get_alive_ip_address(page):
    for i in range(1, page):
        url = URL + str(i)
        print('开始爬行第' + str(i) + '页' + ' ' + url)
        html = get_html(url)
        selector = etree.HTML(html)  # 'NoneType' object has no attribute 'xpath'
        if selector is not None:
            table = selector.xpath('//table[@id="ip_list"]')[0]
            lines = table.xpath('./tr')[1:]
            for line in lines:
                speed, connect_time = line.xpath('.//div/@title')
                data = line.xpath('./td')
                ip = data[1].xpath('./text()')[0]
                port = data[2].xpath('./text()')[0]
                anonymous = data[4].xpath('./text()')[0]
                ip_type = data[5].xpath('./text()')[0]
                # 过滤掉速度慢和非高匿的ip代理
                if float(speed[:-1]) > 1 or float(connect_time[:-1]) > 1 or anonymous != '高匿':
                    continue
                iplist.append(ip_type.lower() + '://' + ip + ':' + port)
            time.sleep(20)
        else:
            print('ip被封锁')
            break
    pool.map(test_alive, iplist)


# 把抓取到的有效ip代理写入到本地
def write_txt(output_file):
    with open(output_file, 'w') as f:
        json.dump(alive_ip, f)
    print('write successful: %s' % output_file)


def main():
    # xici 每页显示100条
    get_alive_ip_address(51)  # 输出 1-50 页
    write_txt(output_file)


if __name__ == '__main__':
    try:
        output_file = 'ip_pool.txt'  # sys.argv[1] #第一个参数作为文件名
    except:
        output_file = IP_POOL
    main()
