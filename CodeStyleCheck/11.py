#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2020/6/9 14:48
# @Author : yachao_lin
# @File : 11.py
import re

keyWordName = ';'
str1 = '  int fun()\n{  int a = 0;  int b=0;  \n\n    }'
regExpStr_0 = '^([ ]*)' + '(.*)' + keyWordName + '[ ]*([\\S]*).*'
pattern_0 = re.compile(regExpStr_0)
countStr = '\\1'

it = re.finditer("{", str1)
print(it)
pat = re.compile("[ ]*{[ ]*")
it = re.split(pat, str1)
# pat = re.compile("[ ]*\n*[ ]*}[ ]*")
# it = re.split(pat, str1)
# pat = re.compile("[ ]*;[ ]*\n*[ ]*")
# it = re.split(pat, it[0])
# print(it)
spaceNum = 0
# for i_num in range(len(it)):
#     if it[i_num] == '':
#         spaceNum = i_num + 1
#     if it[i_num] != '':
#         break
# print(spaceNum
# )
newAlignCodeList = []
lineNum = 1
newAlignCodeList.append("int a;int b;}")
regExpStr = '}'
pattern = re.compile(regExpStr)
splitStr = re.split(pattern, "int a;int b;")
newlineStr = splitStr[0] + '\n' + ' '*spaceNum + '}'  # -----------------加了回车

print("newStr:\n",newlineStr)

if __name__ == '__main__':
    keyWordName = ';'
    lineNum = 1
    spaceNum = 0
    print("1:",spaceNum)
    newAlignCodeList = ['int fun{int a=1;int b=3;  }']
    if keyWordName == '{':
        pattern = re.compile(" ")  # 先统计这一行开头空格数目
        spaceList = re.split(pattern, newAlignCodeList[lineNum - 1])
        print("1:", spaceNum)
        for i_num in range(len(spaceList)):
            if spaceList[i_num] == '':
                spaceNum = i_num + 1
            if spaceList[i_num] != '':
                break
        print("1:", spaceNum)
        regExpStr = '[ ]*{[ ]*'
        pattern = re.compile(regExpStr)
        splitStr = re.split(pattern, newAlignCodeList[lineNum - 1])  # 返回一个列表
        newlineStr = splitStr[0] + '\n' + ' ' * spaceNum + '{' + '\n' + ' ' * spaceNum * 2 + splitStr[1]
        newAlignCodeList[lineNum - 1] = newlineStr
        print("2:\n", newlineStr, newAlignCodeList)
    elif keyWordName == '}':
        regExpStr = '[ ]*}[ ]*'
        pattern = re.compile(regExpStr)
        splitStr = re.split(pattern, newAlignCodeList[lineNum - 1])
        newlineStr = splitStr[0] + '\n' + ' ' * spaceNum + '}' + '\n'  # -----------------加了回车
        newAlignCodeList[lineNum - 1] = newlineStr
        print("3:\n", newlineStr, newAlignCodeList)
    else:  # ;
        myFlag1 = False
        myFlag2 = False
        it = None
        qian = ''
        hou = ''
        print("kaishi")
        if '{' in newAlignCodeList[0]:
            myFlag1 = True
            pattern = re.compile("[ ]*{[ ]*")
            it = re.split(pattern, newAlignCodeList[lineNum - 1])
            qian = it[0]+ '{'
            print(qian)
        if '}' in newAlignCodeList[0]:
            myFlag2 = True
            pattern = re.compile("[ ]*\n*[ ]*}[ ]*")
            if myFlag1:
                it = re.split(pattern, it[1])
            else:
                it = re.split(pattern, newAlignCodeList[lineNum - 1])
            hou = it[0]
        if myFlag1 and not myFlag2:
            it = it[1]
        if myFlag2:
            it = it[0]
        if not myFlag1 and not myFlag2:
            it = newAlignCodeList[lineNum - 1]
        pattern = re.compile("[ ]*;[ ]*\n*[ ]*")
        it = re.split(pattern, it)  # it现在存着一个列表，保存着多条语句
        newlineStr = qian
        for j_num in range(len(it)):
            newlineStr += it[j_num].strip(' ')
        newlineStr += hou
        newAlignCodeList[lineNum - 1] = newlineStr
    print("1ast:\n", newAlignCodeList[0])
