## 加解密shell脚本

a.sh

	#!/bin/sh 
	touch a

加密：

	cat a.sh|openssl aes-128-cbc -a -salt -in a.sh -out yourscript.enc.sh -k 123

解密：

	cat yourscript.enc.sh | openssl aes-128-cbc -a -d -salt -k 123 > yourscript.dec.sh

## 混淆shell脚本

	yum install shc
	shc -rf a.sh -o a.bin 

a.sh.x.c 是生成的 c语言代码， **a.bin 是生成可执行的二进制文件，它的使用方法和原始脚本是一样的**

注意: 编译出来的二进制文件func.bin，如果想让它在其他机器也能运行的话，一定要指定 -r 选项

shc 除了将把脚本编译成二进制，还能为二进制设置过期时间，下面还是以 func.sh 脚本为例来说明

	执行 shc -e 11/1/2022 -m "The script is expired, Please contact test@qq.com" -rf func.sh -o func.bin 命令把脚本的过期时间设置为 2022年1月11日
	执行过期后的脚本提示语设置为 "The script is expired, Please contact test@qq.com"

### 安全性

shc 使用的加密类型是叫做 RC4流密码的一个变体，目前它已经被证实存在弱点，存在被破解的可能， 尤其在 shc 中，密钥被携带到加密脚本本身中，所以，是存在通过反汇编破解出密钥，进而通过密钥还原原始脚本的可能性。

## reference

[如何隐藏Shell脚本内容](https://os.51cto.com/art/202107/669468.htm)

[Patch Bash5.0，让 -x 只打印而不执行，静态解混淆 Shell 脚本](https://jiayu0x.com/2019/03/27/patch-bash5.0-for-deobfuscation/#x-echo-command-at-execute)