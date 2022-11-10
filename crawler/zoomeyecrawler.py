# ! /usr/bin/env python3
# coding: utf-8
# __date__:2019-08-11

import urllib
import os
import requests
import json
from urllib import request

access_token = ''
ip_list = []

# 输入用户名，密码
def login():
    user = ''
    passwd = ''
    data = {
        'username': user,
        'password': passwd
    }
    data_encoded = json.dumps(data)  # dumps 将 python 对象转换成 json 字符串
    try:
        r = requests.post(url='https://api.zoomeye.org/user/login', data=data_encoded)
        r_decoded = json.loads(r.text)  # loads() 将 json 字符串转换成 python 对象
        global access_token
        access_token = r_decoded['access_token']
    except Exception as e:
        print('[-] info : username or password is wrong, please try again ')
        exit()


def saveStrToFile(file, str):
    with open(file, 'w') as output:
        output.write(str)


# 将列表逐行写如文件中    # a 追加，w覆盖
def saveListToFile(file, list):       
    s = '\n'.join(list)
    with open(file, 'a') as output:
        output.write(s+'\n')


def apiTest():
    """
        进行 api 使用测试
    :return:
    """
    page = 1
    global access_token
    with open('access_token.txt', 'r') as input:
        access_token = input.read()
    # 将 token 格式化并添加到 HTTP Header 中
    headers = {
        'Authorization': 'JWT ' + access_token,
    }
    # print headers
    while (True):
        try:

            r = requests.get(url='https://api.zoomeye.org/host/search?query="dedecms"&facet=app,os&page=' + str(page),
                             headers=headers)
            r_decoded = json.loads(r.text)
            # print r_decoded
            # print r_decoded['total']
            for x in r_decoded['matches']:
                print(x['ip'])
                ip_list.append(x['ip'])
            print('[-] info : count ' + str(page * 20))

        except Exception as e:
            # 若搜索请求超过 API 允许的最大条目限制 或者 全部搜索结束，则终止请求
            if str(e.args) == 'matches':
                print('[-] info : account was break, excceeding the max limitations')
                break
            else:
                print('[-] info : ' + str(e.args))
        else:
            if page == 5:  # 设定页码
                break
            page += 1


def main():
    # 访问口令文件不存在则进行登录操作
    if not os.path.isfile('access_token.txt'):
        print('[-] info : access_token file is not exist, please login')
        login()
        saveStrToFile('access_token.txt', access_token)

    apiTest()
    saveListToFile('ip_list.txt', ip_list)


def apileftcount():
    req = urllib.request.Request('https://api.zoomeye.org/resources-info')
    ida = open('access_token.txt').read()
    req.add_header('Authorization', 'JWT %s' % (ida))
    re = urllib.request.urlopen(req)
    ae = (re.read().decode('utf-8'))
    ae = target = json.loads(ae)
    dict_web = ae['resources']['search']
    print('your left search count:%s' % (dict_web))


if __name__ == '__main__':
    main()
    apileftcount()  # 查询剩余api
