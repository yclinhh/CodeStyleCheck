#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2020/4/17 1:04
# @Author : yachao_lin
# @File : test_regxExpre.py
import re
import sys

import pymysql

global dd

di = ((1, 'char'), (2, 'double'), (3, 'enum'), (4, 'float'), (5, 'int'), (6, 'long'), (7, 'short'),
      (8, 'signed'), (9, 'union'), (10, 'unsigned'), (11, 'struct'), (12, 'void'), (13, 'auto'),
      (14, 'typedef'),(15, 'const'), (16, 'extern'), (17, 'register'), (18, 'static'),
      (19, 'volatile'), (20, 'if'), (21, 'else'), (22, 'switch'), (23, 'for'), (24, 'do'),
      (25, 'while'), (26, 'goto'), (27, 'continue'), (28, 'break'), (29, 'return'), (30, 'default'),
      (31, 'sizeof'), (32, 'case'), (33, '+'), (34, '-'), (35, '*'), (36, '/'), (37, '%'), (38, '++'),
      (39, '--'), (40, '=='), (41, '!='), (42, '>'), (43, '<'), (44, '>='), (45, '<='), (46, '&&'),
      (47, '||'), (48, '!'), (49, '&'), (50, '|'), (51, '^'), (52, '~'), (53, '<<'), (54, '>>'), (55, '='),
      (56, '+='), (57, '-='), (58, '*='), (59, '/='), (60, '%='), (61, '<<='), (62, '>>='), (63, '&='),
      (64, '^='), (65, '|='), (66, '->'), (67, 'sizeof(返回变量大小)'), (68, '&（返回地址）'),
      (69, '*（指向变量）'), (70, '？：（条件表达式）'), (71, '/*（注释）'), (72, '//（注释）'),
      (73, '(（界符）'), (74, '[（界符）'), (75, '{（界符）'), (76, '.（界符）'), (77, '，（界符）'),
      (78, '‘’（单引号界符）'), (79, '标识符'), (80, '空行'), (81, '空格'), (82, '代码行'),
      (83, '）（界符）'), (84, ']（界符）'), (85, '}（界符）'))

word = {'char': 1, 'double': 2, 'enum': 3, 'float': 4, 'int': 5, 'long': 6, 'short': 7,
        'signed': 8, 'union': 9, 'unsigned': 10, 'struct': 11, 'void': 12, 'auto': 13,
        'typedef': 14, 'const': 15, 'extern': 16, 'register': 17, 'static': 18,
        'volatile': 19, 'if': 20, 'else': 21, 'switch': 22, 'for': 23, 'do': 24,
        'while': 25, 'goto': 26, 'continue': 27, 'break': 28, 'return': 29, 'default': 30,
        'sizeof': 31, 'case': 32, '+': 33, '-': 34, '*': 35, '/': 36, '%': 37, '++': 38,
        '--': 39, '==': 40, '!=': 41, '>': 42, '<': 43, '>=': 44, '<=': 45, '&&': 46,
        '||': 47, '!': 48, '&': 49, '|': 50, '^': 51, '~': 52, '<<': 53, '>>': 54, '=': 55,
        '+=': 56, '-=': 57, '*=': 58, '/=': 59, '%=': 60, '<<=': 61, '>>=': 62, '&=': 63,
        '^=': 64, '|=': 65, '->': 66, 'sizeof': 67, '&': 68,
        '*': 69, '？:': 70, '/*': 71, '//': 72,
        '(': 73, '[': 74, '{': 75, '.': 76, '，': 77,
        '‘’': 78, '标识符': 79, '空行': 80, '空格': 81, '代码行': 82,
        '）': 83, ']': 84, '}': 85}
_lineErr = []    # 保存错误行号
_recordTab = []   # 记录表
_keyWord = []  # 保存当前行中关键字的ID,
_lineCount = 0  # 记录当前是第几行
_judgeStr = ''  # 保存当前要判断的字符串
_chBegin = 0  # 当前判断开始，第一个判断字符的位置

#  把整个代码文件都扫描完在进行规则匹配，这样匹配时再按行读取匹配，词法分析还是一个字符一个字符分析
#  把每一行匹配单词的ID保存为一个列表存起来--------------------------------


def Scanner(para):
    global _lineErr, _recordTab, _keyWord, _lineCount,  _judgeStr, _chBegin
    _chBegin = 0  # 判断的字符串的起始位置
    _lineCount += 1  # 行号
    _judgeStr.replace(_judgeStr, '') # 字符串清空
    _keyWord.clear()
    _recordTab.clear()
    code = str(para)
    # print("code:", code, end='')
    length = len(code)
    # print("当前行长度：", length, code[length-2])
    for pos in range(length-1):
        print(code[pos], end='')
        if code[pos] == '/':
            if code[pos+1] == '*':
                pos += 2
                while code[pos] != '*' or code[pos+1] != '/':
                    pos += 1
                    if '\n' == code[pos]:
                        _lineCount += 1  # 行数变了，
                        _chBegin = pos+1    # 字符起始位置也变
                        _recordTab.append(_keyWord)   # 错误记录表记录添加当前检测出的ID列表，ID列表肯能为空
                        _keyWord.clear()  # 关键字列表清空（因为只存当前行的关键字ID,当前行变化了）
                    if pos > (length - 1):
                        print("注释出错，没有*/！！！！！！！！！！！！！！！")
                        return None
                pos += 2  # 找到*/，直接跳过
            elif code[pos+1] == '/':
                while code[pos] != '\n':
                    pos += 1
                _lineCount += 1   # 行数加1
                _chBegin = pos+1
                _recordTab.append(_keyWord)
                _keyWord.clear()
            else:  # 否则认为是除号
                _keyWord.append(word['/'])
        elif code[pos] == '\n':  # 换行符
            _lineCount += 1
            _recordTab.append(_keyWord)
            _keyWord.clear()
        elif code[pos] == '\t' or '\r' or '\v':  # 过滤制表符、回车符、垂直制表符
            pos += 1
        elif code[pos] == ' ':  # 过滤空格
            pos += 1
        elif code[pos].isalpha():  # 判断是否是字母
            _judgeStr += code[pos]
            pos += 1
            while code[pos].isalpha() or code[pos].isdigit() or code[pos] == '_':
                _judgeStr += code[pos]
                pos += 1
            if _judgeStr in word:  # 如果字符串在单词表中存在
                _keyWord.append(word[_judgeStr])
            elif not _judgeStr.isdigit():
                _keyWord.append(79)
        elif code[pos].isdigit():
            pos += 1
        elif not code[pos].isdigit() and not code[pos].isalpha() and code[pos] in word:
            _keyWord.append(word[code[pos]])
        else:
            pass  # 如果以上情况都没有， 跳过，暂时不分析























if __name__ == '__main__':
    '''print(re.match("^[ ]+int[ ][^ ]*", " int dd", flags=0))
    # print(re.match('com', 'www.runoob.com').span())
    print(re.match('www', 'www.runoob.com').span())  # 在起始位置匹配
    print(re.match('com', 'www.runoob.com'))  # 不在起始位置匹配

    db = pymysql.connect("localhost", "root", "123456", "cstyle_db")
    cursor = db.cursor()
    sql = "select * from Word"
    cursor.execute(sql)
    data = cursor.fetchall()
    global dd
    dd = dict(data)
    # print(dd)
    # print(data, end='\n')
    '''
    v = []
    v.append([])
    v.append([1,2])
    v.append([123])
    v.clear()
    print(v)
    v.append([])
    print("1:\n")
    print("2:\t11")
    print("3:11")
    print("4:\v11")
    print('--------------------------------')
    a = 'ss'
    if a == 'a' or 'ee' or 'ss':
        print('ok->????')
    cv = '012hcsdvs'
    i = 2
    if cv[3].isalpha():
        print("k")
    if cv[1].isdigit():
        print("digit:", cv[1])
    jj = ''
    print('1--------->:',jj)
    jj += cv[3]
    print("2--------->:", jj)
    sss = ''
    print("ckdnvdk:",sss)
    sss += cv[0]
    sss += cv[1]
    print(sss)
    sss = sss.replace(sss, '')
    print("-->", sss)
    sss += cv[4]
    print("{0} is {1}".format(type(sss), sss))
    path = 'E:\毕业设计\学生代码规范化检测\CodeStyleCheck\cesi.txt'
    try:
        with open(path, encoding='utf8', mode='r+') as f:
            ''' text = ''.join(f.readlines())
                        print("text类型：", type(text))
                        deal_text = re.sub(r'\/\*[^(*/)]*\*\/|\/\/.*', '1', text)  # 过滤注释
                        print(deal_text)
                        #for line in text.split('\n'):
                        for line in text:
                            line = line.strip()
                            #line = line.replace('\\t', '')
                            #line = line.replace('\\n', '')
                            print("num3:", line, end='')

                            if line == '\n':
                                print('woshi----------------------------------------------------------')
                            if not line:
                                continue
                            else:
                                pass
                            '''
            text = f.read()
            print("check")
           # Scanner(text)
    except IOError as e:
        print(e)
'''

'''