#!/bin/bash
TXTS=txt_kiler106/
find $TXTS -name "*.txt" > kiler106_2
while read line
do
    echo $line
    echo ${line//txt/pcap} # 把txt替换为pcap
    #text2pcap -T 10851,443  $line  ${line//txt/pcap}
    text2pcap $line  ${line//txt/pcap}  # yum install wireshark
done<kiler106_2  # 表示 while read 这个文件
