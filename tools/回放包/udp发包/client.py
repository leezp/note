# -*- coding:utf-8 -*-
# python 实现udp 广播 (模拟飞秋广播包)
# https://www.csdn.net/tags/MtTaEgzsNjUxMzA5LWJsb2cO0O0O.html
# wireshark过滤方法：eth.addr == ff:ff:ff:ff:ff:ff

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # AF_INET ：IPv4  # SOCK_DGRAM 是无保障的面向消息的socket，主要用于在网络上发udp/广播信息

s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # socket默认不支持发送广播报文,通过SO_BROADCAST选项的设置,开启广播发送功能。

PORT = 2425

network = '<broadcast>'
str = '1_lbt6_0#128#C85B76BD9F3F#0#0#0#4001#9:1655805995:Lee:LEE-PC:0:\x00'
str1 = '1_lbt6_0#128#C85B76BD9F3F#0#0#0#4001#9:1655805996:Lee:LEE-PC:6291457:Lee\x00\x00'
print(len(str)) #64
print(len(str1)) #74
s.sendto(str.encode('utf-8'), (network, PORT))
