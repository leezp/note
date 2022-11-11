# ! /usr/bin/env python3
# -*- coding:utf-8 -*-
# __author__:leezp
# __date__:2019-07-07
# ! 去除txt 中重复的行

readDir = "old.txt"  # old
writeDir = "new.txt"  # new
lines_readed = set()
outfile = open(writeDir, "w", encoding='utf-8')
f = open(readDir, "r", encoding='utf-8')
a = 0
for line in f:
    if line.strip() not in lines_readed:
        a += 1
        outfile.write(line.strip()+'\n')
        lines_readed.add(line.strip())  # 已读取的存 set
        print(a)
outfile.close()
print("success")
