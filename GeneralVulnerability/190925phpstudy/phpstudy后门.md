植入后门版本分别为phpStudy_2016.11.03、phpStudy_2018.02.11
后门只存在于php-5.4.45和php-5.2.17两个版本中：

MD5 (phpStudy20161103_backdoor.exe) = a63ab7adb020a76f34b053db310be2e9
可从VT下载MD5对应样本。


后门文件MD5值：
MD5: 0F7AD38E7A9857523DFBCE4BCE43A9E9
MD5: C339482FD2B233FB0A555B629C0EA5D5

$ grep "@eval" ./* -r
Binary file ./php/php-5.4.45/ext/php_xmlrpc.dll matches
Binary file ./php/php-5.2.17/ext/php_xmlrpc.dll matches



参考链接 : [https://github.com/blackorbird/APT_REPORT/tree/master/phpstudyGhost](https://github.com/blackorbird/APT_REPORT/tree/master/phpstudyGhost)