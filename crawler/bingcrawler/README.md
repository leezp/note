## 利用bing爬取网站子域名

bingsearch.py  为爬取bing的单线程脚本，包含去重


bsearchMultithreading.py   为爬取bing的多线程脚本，不包含去重，需要配合quchong.py


性能对比：


bsearchMultithreading.py 采用4个线程


100条数据：bingsearch.py  40s
bsearchMultithreading.py 10s

1000条数据：bingsearch.py 475s
bsearchMultithreading.py 107s

2000条数据：bsearchMultithreading.py 251s
