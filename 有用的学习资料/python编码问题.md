1.一个简单的爬虫，requests.get 返回一个响应页面，resp.content.decode('utf-8')按理说会返回解码后的中文页面（网页是utf-8编码）。结果pycharm控制台报错：``` 'gbk' codec can't decode byte 0x80 in position 935: illegal multibyte sequence```

resp.text  //  返回的是一个经过解码后的字符串，是unicode类型

resp.content  // 返回的是一个原生字符串，是bytes类型

思来想去也没有发现问题。开始调试：

	H=resp.content.decode('utf-8')
	print (H)

这里的H 是经过解码后的中文，在print这一步出错。

用cmd执行，正常。发现时pycharm控制台编码问题。默认是gbk。在setting修改就好了。

万万没想到 python decode之后，这个pycharm 控制台编码是gbk，所以输出utf-8 会字符报错。



unicode 解码：

py2:

	print(('\u7248\u6743\u6240\u6709').decode('unicode_escape'))

	版权所有

py3:

	print(('\u7248\u6743\u6240\u6709').replace('\\','\\\\'))
	
	版权所有