cmd```powershell (new-object System.Net.WebClient).DownloadFile('http://img5.cache.netease.com/photo/0001/2013-03-28/8R1BK3QO3R710001.jpg','E:\1.jpg')```


在powershell换行输入

ps    ```$p = new-object system.net.webclient```
ps    ```$p.downloadfile("http://img5.cache.netease.com/photo/0001/2013-03-28/8R1BK3QO3R710001.jpg","E:\1.jpg")```


默认情况下是无法执行powershell脚本的，需要在管理员权限下修改配置

```powershell set-executionpolicy unrestricted```

