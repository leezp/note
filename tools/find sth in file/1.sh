#!/bin/bash
while read line
do
   #echo $line
   flag=`grep -E -i "$line" *.rules`
   if [ -n "$flag" ]  # -n 表示flag非空, if [ -z "$flag" ] 表示 flag 为空
   then
        echo $line
   fi
done<1.txt
