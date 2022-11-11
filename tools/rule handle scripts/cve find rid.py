# -*- coding:utf-8 -*-
__author__ = 'leezp'
__date__ = 20211011
import os
import re

# 根据CVE编号查找ruleid

regex_msg = re.compile(r'msg:.*?"(.*?)"')
regex_sid = re.compile(r'sid:(.*?);')


def merge():
    find_comment = re.compile(r'^#')
    for root, dirs, files in os.walk('./folder'):
        # 遍历文件
        for f in files:
            path = os.path.join(root, f)
            if '.rules' in path:
                f = open(path, "r", encoding='utf-8')
                for chunk in f.readlines():
                    if find_comment.search(chunk.strip()):
                        continue
                    l = chunk.strip()
                    with open('all.rules', 'a', encoding='utf-8') as f:
                        f.write(l + '\n')


merge()
f = open('cve 编号', "r", encoding='utf-8')
for chunk in f.readlines():
    search = chunk.strip()
    f1 = open('all.rules', "r", encoding='utf-8')
    for chunk1 in f1:
        if chunk1.strip() != "":
            msg = regex_msg.search(chunk1.strip()).group(1)
            sid = regex_sid.search(chunk1.strip()).group(1).strip()
            if search in msg:
                print(sid, chunk.strip())
                with open('sid-cve.txt', 'a', encoding='utf-8') as f:
                    f.write(sid + ',' + chunk.strip() + '\n')
