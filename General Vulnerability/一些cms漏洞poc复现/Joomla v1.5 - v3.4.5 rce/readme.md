

### 参考链接

https://www.seebug.org/vuldb/ssvid-90106

https://www.exploit-db.com/exploits/38977


## poc使用方法

先用 joomla_rce.py 生成payload

注意：\x5C0\x5C0\x5C0  需要 打印完变成\0\0\0 需要手动恢复

末尾添加截断字符串：\xF0\x9D\x8C\x86

再复制到joomla.py中执行 可以上传一句话木马

## 复现环境

joomla 3.4.5

php 5.4.16

mysql 5.7.27

Centos7


windows 下复现未成功。原因未知。