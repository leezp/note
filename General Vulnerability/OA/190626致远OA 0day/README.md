payload.txt 为 post 在和payload,**注意：payload 第一行的内容和间距不可修改**

Main.java 为 payload 加密 解密 脚本

index.jsp 为 payload 中 webshell部分


含有漏洞 页面
```ip/seeyon/htmlofficeservlet```

如果出现 ```DBSTEP V3.0     0               21              0               htmoffice operate err```，则可能有漏洞

构造post请求

请求头保留 POST，Host,User-Agent 三行字段

请求体为poc 内容

在burp中复现

Seeyon/A8/ApacheJetspeed/   log目录

漏洞版本 致远A8-V5协同管理软件V6.1sp1，V7.0sp1、V7.0sp2、V7.0sp3，V7.1

fofa搜索

```
app="用友-致远OA" && title=="致远A8-V5协同管理软件 V6.1"     
app="用友-致远OA" && title=="致远A8-V5协同管理软件 V6.1SP2"  
app="用友-致远OA" && title=="致远A8-V5协同管理软件 V6.1SP1"  
app="用友-致远OA" && title=="致远A8-V5协同管理软件 V7.0SP3"
app="用友-致远OA" && title=="致远A8-V5协同管理软件 V7.0SP2"  
app="用友-致远OA" && title=="致远A8-V5协同管理软件 V7.0SP1" 
app="用友-致远OA" && title=="致远A8-V5协同管理软件 V7.1"
```

ping.js为js下载shell的脚本，因为直接上传其他shell会出错   

```https://github.com/leezp/note/blob/master/cmd%E4%B8%8B%E8%BD%BD%E6%96%87%E4%BB%B6/ping.js```

singleuptest.py 为单个ip vul 测试脚本，根据返回时打印的html可判断是否成功

batchvultest.py 为批量ip vul 测试脚本

batchtqadmin.py 为用户提权代码，有时当前登陆用户权限不够，统一提权到admin

batchup.py      为批量上传代码，利用js下载shell到目标

使用方法，batchvultest.py 提取vul ip 到success.txt,batchtqadmin.py 统一对当前用户提权, batchup.py 批量上传 保存到 webshell.txt


