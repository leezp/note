#!/usr/bin/env python
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import json
import base64
import binascii

skyeye_files = ["/data/2020-02-03.json",
              "/data/2020-02-04-1.json",
              "/data1/2020-02-04-2.json",
              "/data/2020-02-05-2.json",
              "/data1/2020-02-06-1.json",
              "/data/2020-02-06-2.json",
              "/data1/2020-02-06-3.json",
              "/data1/2020-02-11.json",
              "/data1/2020-02-13.json",
              "/data1/2020-01-16-1.json",
              "/data1/2020-01-16-2.json",
              "/data1/2020-01-16-3.json",
              "/data1/2020-02-14TO2020-02-22.json"]


vul_names = dict()
pkt_data_dict = dict()
dport = dict()
select_rule = "木马远控工具KilerRat v1.0.6 Arabic By Ahmed Ibrahim"  # 远程连接工具向日葵dport:443,6064/远程连接工具Teamviewer,dport:53,443
select_rule_en = "kiler106"  # teamviewer/sunlogin


def load_file(sfile):
    global vul_names, pkt_data_dict, dport
    with open(sfile, "r") as f:
        data = json.load(f)
        # print data.keys()
        for vul_type in data:
            if 'total' == vul_type:
                continue
            # print vul_type
            for vul in data[vul_type]:
                rule_name = vul['rule_name']
                if select_rule in rule_name:    # 如果data[vul_type]中这条vul中的rule_name中包括 kiler106
                    # print (rule_name)
                    try:
                        # 查看目的端口号
                        if vul["dport"] in dport:
                            dport[vul["dport"]] += 1
                        else:
                            dport[vul["dport"]] = 1
                    except:
                        print sfile
                    # print vul.keys()
                    pkt_data0 = base64.b64decode(vul['packet_data'])    # 将这条的packet_data进行b64解码
                    # print pkt_data0
                    if pkt_data0 in pkt_data_dict:
                        pkt_data_dict[pkt_data0] += 1
                    else:
                        pkt_data_dict[pkt_data0] = 1


def pkt2hex(pkt):
    vul2hex = binascii.hexlify(pkt)  # 将value[0]内容转化为16进制格式
    id_flg = 0
    res = []
    for i in range(0, len(vul2hex), 32):
        pkt_row = vul2hex[i:32+i]    # 每行32个字符，然后两两一组加空格
        pkt_row_list = list(pkt_row)
        flg = 0
        for j in range(2, 31, 2):
            pkt_row_list.insert(flg+j, ' ')
            flg +=1
        tmp = ''.join(pkt_row_list)    # 每行字符
        idlen = len(str(hex(id_flg))[2:])    # 本轮id的长度
        if idlen == 1:
            row = '00' + str(hex(id_flg))[2:] + '0  ' + tmp
            res.append(row)
        elif idlen == 2:
            row = '0' + str(hex(id_flg))[2:] + '0  ' + tmp
            res.append(row)
        else:
            row =str(hex(id_flg))[2:] + '0  ' + tmp
            res.append(row)
        id_flg +=1
    return res


if __name__ == "__main__":
    for sfile in skyeye_files:
        print sfile
        load_file(sfile)
    slist = sorted(pkt_data_dict.items(), key=lambda x: x[1], reverse=True)
    cnt = 1
    for value in slist:
        try:
            reslist = pkt2hex(value[0])
            # print reslist
            filename = 'kiler106_' + str(cnt) + '.txt'
            path = '/tmp/pycharm_project_896/txt_kiler106/'
            with open(path+filename, "w") as f:
                for line in reslist:
                    f.write(line + '\n')
                print "success to txt"
        except:
            print "error"
        cnt +=1
    print dport
