#!/bin/bash 
find . -name "*.zip"> cve.txt
while read line
do
    echo $line
	unzip -P infected $line -d ../apcaps/
done<cve.txt


# ls *.zip | xargs -n1 unzip -o -P infected 批量解压zip 到当前目录 -P 密码