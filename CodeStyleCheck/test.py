#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2020/4/18 18:35
# @Author : yachao_lin
# @File : test.py
import fileinput
import re

import pymysql
from PyQt5.QtCore import QDateTime

word = {'char': 1, 'double': 2, 'enum': 3, 'float': 4, 'int': 5, 'long': 6, 'short': 7,
        'signed': 8, 'union': 9, 'unsigned': 10, 'struct': 11, 'void': 12, 'auto': 13,
        'typedef': 14, 'const': 15, 'extern': 16, 'register': 17, 'static': 18,
        'volatile': 19, 'if': 20, 'else': 21, 'switch': 22, 'for': 23, 'do': 24,
        'while': 25, 'goto': 26, 'continue': 27, 'break': 28, 'return': 29, 'default': 30,
        'sizeof': 31, 'case': 32, '+': 33, '-': 34, '*': 35, '/': 36, '%': 37, '++': 38,
        '--': 39, '==': 40, '!=': 41, '>': 42, '<': 43, '>=': 44, '<=': 45, '&&': 46,
        '||': 47, '!': 48, '&': 49, '|': 50, '^': 51, '~': 52, '<<': 53, '>>': 54, '=': 55,
        '+=': 56, '-=': 57, '*=': 58, '/=': 59, '%=': 60, '<<=': 61, '>>=': 62, '&=': 63,
        '^=': 64, '|=': 65, '->': 66, 'sizeof(返回变量大小)': 67, '&（返回地址）': 68,
        '*（指向变量）': 69, '？:': 70, '/*': 71, '//': 72,
        '(': 73, '[': 74, '{': 75, '.': 76, ',': 77,
        '\'\'': 78, '标识符': 79, '空行': 80, '空格': 81, '代码行': 82,
        '）': 83, ']': 84, '}': 85}
print(type(word))


def sca():
    a = 'nckn+'
    if a[3] in word:
        print("md", word.get(a[3]))
    print('word type:', type(word))


if __name__ == '__main__':
    # jieshou = []
    # path = 'E:\毕业设计\学生代码规范化检测\CodeStyleCheck\cesi.cpp'
    # try:
    #     with open(path, encoding='utf8', model='r+') as f:
    #         text = f.read()
    #         print("check")
    #         jieshou = Scanner(text)
    #         print("---------------------------------------------------------------\n", jieshou)
    # except IOError as e:
    #     print(e)for
    # reg = '^.*(?<!([ ]\\+[ ])).*(([\\S]\\+)|([ ]*\\+[\\S])|([ ]*\\+[ ])*).*$'
    headStr = '/*' \
              '\nFunction: // 函数名称 ' \
              '\nDescription: // 函数功能、性能等的描述 ' \
              '\nCalls: // 被本函数调用的函数清单' \
              '\nCalled By: // 调用本函数的函数清单' \
              '\nInput: // 输入参数说明，包括每个参数的作用、取值说明及参数间关系。' \
              '\nOutput: // 对输出参数的说明。' \
              '\nReturn: // 函数返回值的说明' \
              '\nOthers: // 其它说明' \
              '\n*/'
    print(headStr)
    ll = '    int i=1; int f;   \n'
    print('lll:',ll)
    ll = ll.rstrip()
    print('lll:',ll)
    keyWordName = ';'
    regExpStr = '^([ ]*)' + '(.*)' + keyWordName + '[ ]*([\\S]*).*'
    # replaceStr = '\\1' + '\\2' + '\n' + '\\1' + keyWordName + '\n'
    pattern = re.compile(regExpStr)
    # newlineStr = pattern.sub(replaceStr, '    for (i;i<1;i++)   } dvd  ')
    countStr = '\\1'
    blankNum = pattern.sub(countStr, '    for (i;i<1;i++)   }   ')
    print(blankNum, type(blankNum))
    regExpStr = ';'
    pattern = re.compile(regExpStr)
    replaceStr = keyWordName + '\n' + blankNum
    newlineStr = pattern.sub(replaceStr, '    int i =1;int a;  ')
    print(newlineStr)
    reg = '\\' + keyWordName + '[ ]*([\\w]*).*'
    reg = '^.*\\{[ ]*([^ ]+.*)$'
    print(reg)
    p1 = re.compile(reg)
    s = '    for (i;i<1;i++)   {   d  dd'
    jieguo = p1.match(s)
    jj = p1.sub('\\1', s)
    print('jieguo:', jieguo)
    print('jj:',jj)
    aa = '^.*[^ ][ ]\\|=[ ][^ ]+.*$'
    line = 'int i=i+1,j=j +1 c|= b     a  s'
    pattern = re.compile(aa)
    a = pattern.sub(' + ', line)
    b = pattern.match(line)
    print('a', a)
    print('b', b)
    print('te', pattern)
    cc = aa.lstrip('^')
    print('cc', cc)
    h = '    sc             '
    print('h:', h)
    pos = 1
    s = ' ' * pos + h.strip()
    print('s:', s)
    reg = '^[ ]*$'
    pattern = re.compile(reg)
    string = '\n'
    f = pattern.match(string)
    h = pattern.finditer(string)
    g = re.match(r'^12$', string)
    print('f:', f)
    print('g:', g)
    print(h)
    for match in h:
        print(match.group())
    if f:
        print("匹配f:ok!")
    if not f:
        print('不匹配')
    if g:
        print("g:ok!")
    # path = 'E:\毕业设计\学生代码规范化检测\CodeStyleCheck\cesi.cpp'
    # p = path.split('\\')
    # print(type(p))
    # print(p)
    # print(p[-1])
    # tab = [[], [], [1], [1, 2], []]
    # a = []
    # if not a:
    #     print(123)
    # print("a:", a)
    # if not tab[0]:
    #     print("is")
    # i = len(tab[2])
    # print(i)

    # # print(type(tab[2]))
    db = pymysql.connect("localhost", "root", "123456", "cstyle_db")
    cursor = db.cursor()
    idd = '5'
    try:
        # sql = "select ruleid, name, express, advice, standard, ruletypeid from rule where WordID = %s" % idd
        # sql_err = "select * from error where Name = '%s'and  RuleID = '%d' and RuleTypeID" \
        #           "= '%d'and Line = '%d'and WrongCode = '%s'" \
        #           % (file_name, _ruleid, _ruletypeid, int(i) + 1, str(line_str))
        datetime = QDateTime.currentDateTime()  # 获取当前时间精确到秒
        strTime = datetime.toString()  # 转化为字符串
        file_name = 'ceshi2.txt'
        data = 'dvjisdjvnjksnvksnvksn' \
               'dnvlksdnvksnvksd' \
               'dvvsdmvlsdvsdv' \
               'dvmdkvmdslv' \
               'sdvdvs'
        glo_file_path = 'E:/林.指针/程序设计基础/函数计分作业/面积/面积/1.cpp'
        studentID = '1'
        # sql = "insert into code (FileName, FileContent, SaveDate, ModifyDate, FilePath, StudentID)VALUES('%s', '%s', '%s', '%s', '%s', '%s')" % (
        #     file_name, data, strTime, strTime, glo_file_path, studentID)
        a = 1826
        sql = "update error set error.Corrected = '否'where ErrorID = '%s'" % 1826
        print(sql)
        cursor.execute(sql)
        db.commit()
        # ss = cursor.fetchall()
        # print(ss)
        # ss = str((list(ss[0]))[0])
        # print(ss)
        # print(type(ss))
    except Exception as e:
        print("Failed")
        print(e)
    # s =(('^[\\\\s\\\\S]+[^ ]{1},[ ][^ ]+.*$',), (123))
    # db.close()
    # print("s:", s, type(s))
    # s = ''.join(s[0])
    # a = (23,)
    # print(a[0])
    # print(type(a[0]))
    # glo_file_path ='E:/林.指针/数据结构/账簿管理系统/1.txt'
    # i = 0
    # with open(glo_file_path, mode='r') as f:
    #     for line_str in f:
    #         i += 1
    #         print("第{0}行代码{1}".format(i, line_str.strip('\n')))
