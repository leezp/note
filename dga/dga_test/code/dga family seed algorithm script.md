# DGA of vidro

```
$ python dga.py -n 100 -t `date +%s -d "2021-12-22"`
  python dga.py -n 100 -t 1640102400
  -n 指定要生成的DGA域名数量
  -t 指定时间戳
```

# DGA of bigviktor

```
$ python dga.py -n 100 -t `date +%s -d "2021-12-22"`
  python dga.py -n 100 -t 1640102400
  -n 指定要生成的DGA域名数量
  -t 指定时间戳
```

# DGA of ccleaner

```
$ python dga.py -n 100 -t `date +%s -d "2021-12-22"`
  python dga.py -n 100 -t 1640102400
  -n 指定要生成的DGA域名数量
  -t 指定时间戳
```

有点问题，-n参数无法使用

分析：没设置循环，也没做随机处理

代码修改：dga函数

```
def dga(year, month, nr, tlds):

    for i in range(nr):
        seed = i % 100 + (year * 10000 + month)

        r1, seed = msvcrt_rand(seed)
        r2, seed = msvcrt_rand(seed)
        r3, seed = msvcrt_rand(seed)

        domain=''
        sld = 'ab%x%x' %(r2 * r3, r1)

        domain = sld + '.' + tlds[0]
        print(domain)
```

# DGA of chinad

```
$ python dga.py -n 100 -t `date +%s -d "2021-12-22"` -l 10
  python dga.py -n 100 -t 1640102400 -l 10
  -n 指定要生成的DGA域名数量
  -t 指定时间戳
  -l 限制域名长度
```

# DGA of Enviserv

```
$ python dga.py -n 100 -s "papa_koli" -T "com-net-org-info-biz-in"
  -n 指定要生成的DGA域名数量
  -s 随便一个字符串
  -T 指定后缀
```

# DGA of Mydoom

```
$ python dga.py -n 100 -t `date +%s -d "2021-12-22"` -s "0xfa8" -T "com-biz-us-net-org-ws-info-in"
  python dga.py -n 100 -t 1640102400 -s "0xfa8" -T "com-biz-us-net-org-ws-info-in"
  -n 指定要生成的DGA域名数量
  -t 指定时间戳
  -s 随便一个16进制数
  -T 指定后缀
```

# DGA of PadCrypt 

```
$ python dga.py -d "2021-09-06" -v "2.2.86.1"
  -d 指定年月日
  -v 指定版本
```

将```'nr_domains': 24``` 改成了 ```'nr_domains': 100*10```

# DGA of shiotob

```
$ python dga.py -d "hack1.com" -v 1
  -d 指定一个初始的域名
  -v 指定版本
```

# DGA of suppobox

需要字典，暂时不做。

```
$ python3 dga.py -t "2021-09-06 15:31:54" 1
  -t 指定一个时间
  1 （words1.txt） 2的话就是words2.txt
  同目录下放置一个words1.txt 里面放置你的字典，最少328行
```


# DGA of xshellghost

```
$ python dga.py -t `date +%s -d "2021-12-22"` -n 100
  python dga.py -t 1640102400 -n 100
  -t 指定时间戳
  -n 指定数量
```

脚本有问题，没有使用到-n，没有生成随机数。


代码修改：dga函数

	'''
	    DGA of XshellGhost
	'''
	
	import argparse
	from datetime import datetime
	from ctypes import c_uint
	
	def dga(year, month, nr, tlds):
	    for i in range(nr):
	        _year = c_uint(year)
	        _month = c_uint(month)
	        seed = c_uint(0)
	        #print(_year.value)
	        #print(_month.value)
	
	
	        seed.value = 0x90422a3a * _month.value * i
	        #print("%x" %(seed.value))
	        seed.value -= 0x39d06f76 * _year.value
	        #print("%x" %(seed.value))
	        seed.value -= 0x67b7fc6f
	        #print("%x" %(seed.value))
	
	        sld_len = seed.value % 6 + 10
	        sld = ''
	        for i in range(sld_len):
	            sld += chr(seed.value % 0x1a + ord('a'))
	            seed.value = 29 * seed.value + 19
	
	        domain = sld + '.' + tlds[0]
	        print(domain)
	
	if __name__=="__main__":
	    parser = argparse.ArgumentParser()
	    parser.add_argument('-t', '--time', help="Seconds since January 1, 1970 UTC")
	    parser.add_argument("-n", "--nr", help="nr of domains to generate")
	    args = parser.parse_args()
	
	    tlds = ['com']
	        
	    d = datetime.utcfromtimestamp(int(args.time))
	    dga(d.year, d.month, int(args.nr), tlds)
	

## reference

[360netlab/DGA](https://github.com/360netlab/DGA/tree/master/code)