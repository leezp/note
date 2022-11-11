# -*- coding:utf-8 -*-
import logrec
def test():
   plain = logrec.log().getcontent()
   with open('out', 'w', encoding='utf-8') as f:
      f.write(plain)
