# -*- coding:utf-8 -*-
__author__ = 'leezp'
__date__ = 20210401
import time
from datetime import datetime
import os
import subprocess
import dns.exception
import dns.resolver
import random
import argparse


def exec(cmd, path):
    # cmd = "python " + dir + "/dga.py -t " + "\"" + str(t) + "\""
    popen = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    a = popen.stdout.read()  # print(popen.stderr.read())
    a = a.decode()
    if popen.stderr.read() is not None and popen.stderr.read() != b'':
        print(popen.stderr.read())
        exit(1)
    popen.stdout.close()
    print(a)
    # outfile = open(dir + "/dga.txt", "w", encoding='utf-8')
    outfile = open(path + "\..\dga.txt", "w", encoding='utf-8')
    outfile.write(a.strip())


# 依赖运行机器python环境
def gendgadomain():
    for root, dirs, files in os.walk('./'):
        for f in files:
            path = os.path.join(root, f)
            if '.py' in path:
                if 'bigviktor' in path:
                    exec("python " + path + ' -t ' + "\"" + str(t) + "\"", path)
                if 'ccleaner' in path:
                    exec("python " + path + ' -t ' + "\"" + str(t) + "\" -n 1000 ", path)
                if 'chinad' in path:
                    exec("python " + path + ' -t ' + "\"" + str(t) + "\" -n 1000 -l 16", path)
                if 'enviserv' in path:
                    exec("python36 " + path + " -n 1000 -s " + "\"papa_koli\"" + " -T ""\"com-net-org-info-biz-in\"",
                         path)
                if 'mydoom' in path:
                    exec("python " + path + ' -t ' + "\"" + str(
                        t) + "\" -n 1000 -s " + "\"0xfa8\"" + " -T ""\"com-biz-us-net-org-ws-info-in\"", path)
                if 'padcrypt' in path:
                    t1 = str(datetime.now().date())
                    exec("python " + path + " -d " + t1 + " -v ""\"2.2.86.1\"", path)
                if 'shiotob' in path:
                    exec("python " + path + " -d " + "\"hack1.com\"" + " -v ""\"2\"", path)
                if 'vidro' in path:
                    exec("python " + path + ' -t ' + "\"" + str(t) + "\" -n 1000 ", path)
                if 'xshellghost' in path:
                    exec("python " + path + ' -t ' + "\"" + str(t) + "\" -n 1000 ", path)


t = int(time.time())

parser = argparse.ArgumentParser(prog='PROG', add_help=False)
# 禁用默认的-h/ help标志，只需将add_help=False添加到ArgumentParser()的签名中
parser.add_argument('-h', '--help', help="python3 dga_test.py -c bigviktor")
parser.add_argument('-c', '--family', help="family")

args = parser.parse_args()
gendgadomain()
family = args.family
# dir = input("input:")  # bigviktor
dir = str(family)

# cmd = "python " + dir + "/dga.py -t " + "\"" + str(t) + "\""
# popen = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# a = popen.stdout.read()  # print(popen.stderr.read())
# a = a.decode()
# print(a)
# outfile = open(dir + "/dga.txt", "w", encoding='utf-8')
# outfile.write(a.strip())

input = dir + "/dga.txt"

for line in open(input):
    try:
        domain = line.strip()
        print(domain)
        resolver = dns.resolver.query(domain, rdtype=dns.rdatatype.A)
    except dns.exception.DNSException as e:
        print(e)  # None of DNS query names exist: continueovera-check.com.
    except Exception as e:
        continue
    time.sleep(random.randint(1, 5))
