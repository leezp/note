# ! /usr/bin/env python3
# -*- coding:utf-8 -*-
# ftp 弱口令

import ftplib


def ftp_anonymous(ip, port):
    try:
        ftp = ftplib.FTP()
        ftp.connect(ip, port, 2)
        ftp.login()
        ftp.quit()
        print('[+] FTP login for anonymous')
    except:
        print('[-] checking for FTP anonymous fail')


def ftp_login(ip, port, user, pwd):
    try:
        ftp = ftplib.FTP()
        ftp.connect(ip, port, 2)
        ftp.login(user, pwd)
        ftp.quit()
        print('[+] FTP weak password: ' + user, pwd)
    except:
        print('[-] checking for ' + user, pwd + ' fail')


ip = ''
ftp_anonymous(ip, 21)
