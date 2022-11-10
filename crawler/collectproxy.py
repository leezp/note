# coding=utf-8
# grab ip proxies from xicidaili
import time, requests
from multiprocessing.dummy import Pool as ThreadPool
from lxml import etree

IP_POOL = 'ip_pool.txt'
URL = 'http://www.xicidaili.com/nn/'  # IP代理 高匿
# URL = 'http://www.xicidaili.com/wt/' #IP代理 http
RUN_TIME = time.strftime("%Y-%m-%d %H:%M", time.localtime())  # 执行时间

# 用字典存放有效ip代理
alive_ip = {'http': [], 'https': []}
# 多线程
pool = ThreadPool(20)


# 返回html文本
def get_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0",
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
                alive_ip['https'].append(proxy)
            else:
                alive_ip['http'].append(proxy)
    except:
        print("%s无效!" % proxy)


# 解析html文本，获取ip代理
def get_alive_ip_address():
    iplist = []
    html = get_html(URL)
    selector = etree.HTML(html)
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
    pool.map(test_alive, iplist)


# 把抓取到的有效ip代理写入到本地
def write_txt(output_file):
    with open(output_file, 'w') as f:
        f.write('#create time: %s\n\n' % RUN_TIME)
        f.write('http_ip_pool = \\\n')
        f.write(str(alive_ip['http']).replace(',', ',\n'))
        f.write('\n\n')
    with open(output_file, 'a') as f:
        f.write('https_ip_pool = \\\n')
        f.write(str(alive_ip['https']).replace(',', ',\n'))
    print('write successful: %s' % output_file)


def main():
    get_alive_ip_address()
    write_txt(output_file)


if __name__ == '__main__':
    try:
        output_file = 'ip_pool.txt'  # sys.argv[1] #第一个参数作为文件名
    except:
        output_file = IP_POOL
    main()
