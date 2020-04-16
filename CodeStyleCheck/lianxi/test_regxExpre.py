#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2020/4/17 1:04
# @Author : yachao_lin
# @File : test_regxExpre.py
import re
if __name__ == '__main__':
    print(re.match("^[ ]+int[ ][^ ]*", " int dd", flags=0))
    #print(re.match('com', 'www.runoob.com').span())
    print(re.match('www', 'www.runoob.com').span())  # 在起始位置匹配
    print(re.match('com', 'www.runoob.com'))  # 不在起始位置匹配