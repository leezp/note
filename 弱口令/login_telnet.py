# ! /usr/bin/env python3
# -*- coding:utf-8 -*-
# telnet 弱口令

import telnetlib


def check_23_port(ip):
    try:
        tn = telnetlib.Telnet(ip, timeout=5)
        tn.set_debuglevel(0)
        tn.read_until("login:", 10)  # login/user
        tn.write(user + '\r\n')
        tn.read_until("assword:")  # password/Password
        tn.write(pwd + '\r\n')
        result = tn.read_some()
        result = result + tn.read_some()
        if result.find('Login Fail') > 0 or result.find('incorrect') > 0:
            print("[-] Checking for " + user, pwd + " fail")
        else:
            print("[+] Success login for " + user, pwd)
        tn.close()
    except:
        print('[-] Something Error' + username, password + " fail")


ip = ''
user = ''
pwd = ''
check_23_port(ip)
