# -*- coding:utf-8 -*-
__author__ = 'leezp'
__date__ = 20200722
# select protocol,remark,ip_dir,item,nocase,apfield,item1,offset,item2,tag,deep from sys_sig_rule where remark like "%Metasploit%" ;
'''
HTTP	HackTool.w3af.scan.user_agent.A	EXPORT	"User-Agent|3a20|w3af.sourceforge.net"	NOCASE	HTTP_Request_Header	NA	0	NA	T-:w3af	0


if item2 is NA:

alert %protocol% any any -> any any (msg:"%remark%"; flow:%apfield%; content:%item%; %nocase%; %apfield%; )


'''


def handle(l):
    if l[2] == 'EXPORT':
        apfield = 'established,to_server'  # EXPORT
    elif l[2] == 'IMPORT':
        apfield = 'established,to_client'
    else:
        apfield = 'established'
    if l[4] == 'NOCASE':
        case = 'nocase;'
    else:
        case = ''
    if l[5] == 'HTTP_Request_Header':
        weizhi = ' http_header;'
    elif l[5] == 'HTTP_Request_Body':
        weizhi = ' http_client_body;'
    elif l[5] == 'HTTP_Response_Body':
        weizhi = ' http_server_body;'
    else:
        weizhi = ''
    classtype = ' classtype:web-attack;'
    if 'pcre' not in l[3]:
        str = 'alert ' + l[0].lower() + ' any any -> any any (msg:"' + l[1] + '"; flow:' + apfield + '; content:' + l[
            3] + '; ' + case + weizhi + classtype + ')'
    else:
        str = 'alert ' + l[0].lower() + ' any any -> any any (msg:"' + l[1] + '"; flow:' + apfield + ';' + ' ' + l[
            3] + '; ' + weizhi + classtype + ')'
    if l[6] != 'NA':
        if 'pcre' not in l[6]:
            if 'pcre' not in l[3]:
                str = 'alert ' + l[0].lower() + ' any any -> any any (msg:"' + l[
                    1] + '"; flow:' + apfield + '; content:' + \
                      l[
                          3] + '; ' + case + weizhi + ' fast_pattern;' + ' content:' + l[6] + '; ' + classtype + ')'
            else:
                str = 'alert ' + l[0].lower() + ' any any -> any any (msg:"' + l[
                    1] + '"; flow:' + apfield + ';' + ' ' + l[
                          3] + '; ' + weizhi + ' content:' + l[6] + '; ' + classtype + ')'
        else:
            if 'pcre' not in l[3]:
                str = 'alert ' + l[0].lower() + ' any any -> any any (msg:"' + l[
                    1] + '"; flow:' + apfield + ';' + ' content:' + l[
                          3] + '; ' + weizhi + l[6] + '; ' + classtype + ')'
            else:
                str = 'alert ' + l[0].lower() + ' any any -> any any (msg:"' + l[1] + '"; flow:' + apfield + ';' + ' ' + \
                      l[
                          3] + '; ' + weizhi + l[6] + '; ' + classtype + ')'
    if l[8] != 'NA':
        if 'pcre' not in l[8]:
            if 'pcre' not in l[6]:
                if 'pcre' not in l[3]:
                    str = 'alert ' + l[0].lower() + ' any any -> any any (msg:"' + l[
                        1] + '"; flow:' + apfield + '; content:' + \
                          l[
                              3] + '; ' + case + weizhi + ' fast_pattern;' + ' content:' + l[6] + '; ' + ' content:' + \
                          l[
                              8] + '; ' + classtype + ')'
                else:
                    str = 'alert ' + l[0].lower() + ' any any -> any any (msg:"' + l[
                        1] + '"; flow:' + apfield + ';' + ' ' + l[
                              3] + '; ' + weizhi + ' content:' + l[6] + '; ' + ' content:' + l[8] + classtype + ')'
            else:
                if 'pcre' not in l[3]:
                    str = 'alert ' + l[0].lower() + ' any any -> any any (msg:"' + l[
                        1] + '"; flow:' + apfield + ';' + ' content:' + l[
                              3] + '; ' + weizhi + l[6] + '; ' + ' content:' + l[8] + classtype + ')'
                else:
                    str = 'alert ' + l[0].lower() + ' any any -> any any (msg:"' + l[
                        1] + '"; flow:' + apfield + ';' + ' ' + \
                          l[
                              3] + '; ' + weizhi + l[6] + '; ' + ' content:' + l[8] + classtype + ')'
        else:
            if 'pcre' not in l[6]:
                if 'pcre' not in l[3]:
                    str = 'alert ' + l[0].lower() + ' any any -> any any (msg:"' + l[
                        1] + '"; flow:' + apfield + '; content:' + \
                          l[
                              3] + '; ' + case + weizhi + ' fast_pattern;' + ' content:' + l[6] + '; ' + \
                          l[
                              8] + '; ' + classtype + ')'
                else:
                    str = 'alert ' + l[0].lower() + ' any any -> any any (msg:"' + l[
                        1] + '"; flow:' + apfield + ';' + ' ' + l[
                              3] + '; ' + weizhi + ' content:' + l[6] + '; ' + l[8] + classtype + ')'
            else:
                if 'pcre' not in l[3]:
                    str = 'alert ' + l[0].lower() + ' any any -> any any (msg:"' + l[
                        1] + '"; flow:' + apfield + ';' + ' content:' + l[
                              3] + '; ' + weizhi + l[6] + '; ' + l[8] + classtype + ')'
                else:
                    str = 'alert ' + l[0].lower() + ' any any -> any any (msg:"' + l[
                        1] + '"; flow:' + apfield + ';' + ' ' + \
                          l[
                              3] + '; ' + weizhi + l[6] + '; ' + l[8] + classtype + ')'
    print(str)
    # with open('2.txt', 'a') as out:
    #  out.write(str + '\n')


f = open('1.txt', "r", encoding='utf-8')
for line in f:
    # print(line)
    l = line.strip().split('\t')
    handle(l)  # item; item2 ; item3
