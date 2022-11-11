#!/bin/bash 
find . -name "*.pcap"> cve.txt
while read line
do
    echo $line
    cp -f $line /data1/cve_pcaps/
done<cve.txt


# ls *.zip | xargs -n1 unzip -o -P infected 批量解压zip 到当前目录