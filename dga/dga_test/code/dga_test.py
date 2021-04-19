# -*- coding:utf-8 -*-
__author__ = 'leezp'
__date__ = 20210401
import dns.exception
import dns.resolver
import random
import time
import subprocess
import argparse

parser = argparse.ArgumentParser(prog='PROG', add_help=False)
# 禁用默认的-h/ help标志，只需将add_help=False添加到ArgumentParser()的签名中
parser.add_argument('-h', '--help', help="python3 dga_test.py -c bigviktor")
parser.add_argument('-c', '--family', help="family")

args = parser.parse_args()
family = args.family
# dir = input("input:")  # bigviktor
dir = str(family)
t = int(time.time())
cmd = "python " + dir + "/dga.py -t " + "\"" + str(t) + "\""
popen = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
a = popen.stdout.read()  # print(popen.stderr.read())
a = a.decode()
print(a)
outfile = open(dir + "/dga.txt", "w", encoding='utf-8')
outfile.write(a.strip())

input = dir + "/dga.txt"
for line in open(input):
    try:
        domain = line.strip()
        resolver = dns.resolver.query(domain, rdtype=dns.rdatatype.A)
    except dns.exception.DNSException as e:
        print(e)  # None of DNS query names exist: continueovera-check.com.
    time.sleep(random.randint(1, 5))
