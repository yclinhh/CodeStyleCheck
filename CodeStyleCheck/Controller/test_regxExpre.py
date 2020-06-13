#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2020/4/17 1:04
# @Author : yachao_lin
# @File : test_regxExpre.py
import re
import sys
import copy
import traceback

import pymysql
# di = ((1, 'char'), (2, 'double'), (3, 'enum'), (4, 'float'), (5, 'int'), (6, 'long'), (7, 'short'),
#       (8, 'signed'), (9, 'union'), (10, 'unsigned'), (11, 'struct'), (12, 'void'), (13, 'auto'),
#       (14, 'typedef'),(15, 'const'), (16, 'extern'), (17, 'register'), (18, 'static'),
#       (19, 'volatile'), (20, 'if'), (21, 'else'), (22, 'switch'), (23, 'for'), (24, 'do'),
#       (25, 'while'), (26, 'goto'), (27, 'continue'), (28, 'break'), (29, 'return'), (30, 'default'),
#       (31, 'sizeof'), (32, 'case'), (33, '+'), (34, '-'), (35, '*'), (36, '/'), (37, '%'), (38, '++'),
#       (39, '--'), (40, '=='), (41, '!='), (42, '>'), (43, '<'), (44, '>='), (45, '<='), (46, '&&'),
#       (47, '||'), (48, '!'), (49, '&'), (50, '|'), (51, '^'), (52, '~'), (53, '<<'), (54, '>>'), (55, '='),
#       (56, '+='), (57, '-='), (58, '*='), (59, '/='), (60, '%='), (61, '<<='), (62, '>>='), (63, '&='),
#       (64, '^='), (65, '|='), (66, '->'), (67, 'sizeof(返回变量大小)'), (68, '&（返回地址）'),
#       (69, '*（指向变量）'), (70, '？：（条件表达式）'), (71, '/*（注释）'), (72, '//（注释）'),
#       (73, '(（界符）'), (74, '[（界符）'), (75, '{（界符）'), (76, '.（界符）'), (77, '，（界符）'),
#       (78, '‘’（单引号界符）'), (79, '标识符'), (80, '空行'), (81, '空格'), (82, '代码行'),
#       (83, '）（界符）'), (84, ']（界符）'), (85, '}（界符）'))

word = {'char': 1, 'double': 2, 'enum': 3, 'float': 4, 'int': 5,
        'long': 6, 'short': 7, 'signed': 8, 'union': 9, 'unsigned': 10,
        'struct': 11, 'void': 12, 'auto': 13, 'typedef': 14, 'const': 15,
        'extern': 16, 'register': 17, 'static': 18, 'volatile': 19, 'if': 20,
        'else': 21, 'switch': 22, 'for': 23, 'do': 24, 'while': 25, 'goto': 26,
        'continue': 27, 'break': 28, 'return': 29, 'default': 30, 'sizeof': 31,
        'case': 32, '+': 33, '-': 34, '*': 35, '/': 36, '%': 37, '++': 38, '--': 39,
        '==': 40, '!=': 41, '>': 42, '<': 43, '>=': 44, '<=': 45, '&&': 46, '||': 47,
        '!': 48, '&': 49, '|': 50, '^': 51, '~': 52, '<<': 53, '>>': 54, '=': 55,
        '+=': 56, '-=': 57, '*=': 58, '/=': 59, '%=': 60, '<<=': 61, '>>=': 62, '&=': 63,
        '^=': 64, '|=': 65, '->': 66, 'sizeof(返回变量大小)': 67, '&（返回地址）': 68, '*（指向变量）': 69,
        '?:': 70, '/*': 71, '//': 72, '(': 73, '[': 74, '{': 75, '.': 76, ',': 77, '\'\'': 78,
        '标识符': 79, '空行': 80, '空格': 81, '代码行': 82, ')': 83, ']': 84, '}': 85, ';': 86}
# 运算符
operator = ['+', '-', '*', '/', '%', '++', '--', '+=', '-=', '/=',  # 算术运算符
            '==', '!=', '>', '<', '>=', '<=',  # 关系运算符
            '&', '|', '^', '~', '<<', '>>',  # 位运算符
            '&&', '||', '!',  # 逻辑运算符
            '=', '+=', '-=', '*=', '/=', '%=', '<<=', '>>=', '&=', '^=', '|=',  # 赋值运算符
            '?:']  # 条件运算符
# 界符
delimiters = ['{', '}', '[', ']', '(', ')', '.', ',', ';']
_lineErr = []    # 保存错误行号
_recordTab = []   # 记录表
_keyWord = []  # 保存当前行中关键字的ID,
_lineCount = 0  # 记录当前是第几行
_judgeStr = ''  # 保存当前要判断的字符串
_chBegin = 0  # 当前判断开始，第一个判断字符的位置
li = []  # 记录一行都分析出了哪些保留字界符操作符
_allLineLi = []  # 记录所有行的标识符
_commentLineNumTab = []  # 保存注释出现的行号
#  把整个代码文件都扫描完在进行规则匹配，这样匹配时再按行读取匹配，词法分析还是一个字符一个字符分析
#  把每一行匹配单词的ID保存为一个列表存起来--------------------------------


def Scanner(para):
    """
    为了在for语句中';'可以多次出现，方法:检测到for 时不用再将当前行';'的种别码加入到列表中，
    设计一个标志位forFlag= False 遇到for,forFlag = True,当行号变化时，forFlag =False,等于True时，
    检测到';'不添加入列表中
    :param para:
    :return:
    """
    forFlag = False  # for ( ; ; ) 标志位
    global _lineErr, _recordTab, _keyWord, _lineCount,  _judgeStr, _chBegin, li, _commentLineNumTab, _allLineLi
    _recordTab = []  # 初始化
    _commentLineNumTab = []
    _chBegin = 0  # 判断的字符串的起始位置
    _lineCount = 0  # 初始化
    _lineCount += 1  # 行号
    _judgeStr = ''  # 字符串清空
    _allLineLi = []
    li = copy.deepcopy(li)  # 深拷贝
    li.clear()
    _keyWord = copy.deepcopy(_keyWord)  # 深拷贝
    _keyWord.clear()
    # _recordTab.clear()
    code = str(para)
    length = len(code)
    print("当前行长度：", length)
    pos = 0  # 坐标
    # a = word.get('/')
    # print("a--->:", a)

    # _keyWord.append(a)a/x
    # _keyWord.append(a)
    # print(_keyWord)
    while pos < length:
        # print("num{0}:{1}".format(pos, code[pos]),)
        _judgeStr += code[pos]
        if code[pos] == '#':    # 过滤头文件
            while code[pos] != '\n':
                pos += 1
        if code[pos] == '/':
            if code[pos+1] == '*':  # 进入注释，清空_judgeStr
                _commentLineNumTab.append(_lineCount)  # 记录注释第一行行号
                _judgeStr = ''
                pos += 2
                if code[pos] == '\n':
                    _lineCount += 1
                    _commentLineNumTab.append(_lineCount)
                    '''添加'''
                    _recordTab.append(_keyWord)
                    _keyWord = copy.deepcopy(_keyWord)  # 深拷贝
                    _keyWord.clear()  # 关键字列表清空（因为只存当前行的关键字ID,当前行变化了）
                    _allLineLi.append(li)
                    li = copy.deepcopy(li)
                    li.clear()
                while code[pos] != '*' or code[pos+1] != '/':
                    pos += 1
                    if '\n' == code[pos]:
                        _lineCount += 1  # 行数变了，
                        # _chBegin = pos+1    # 字符起始位置也变
                        _commentLineNumTab.append(_lineCount)  # 记录注释第_lineCount行
                        _judgeStr = ''
                        '''
                        必须进行深拷贝再清空的原因是：_recordTab列表中存_keyWord列表为元素（相当引用关系），直接执行celar函数会导致
                        _recordTab表中元素也是清空的，深拷贝则会产生一个新地址，这样再清空_keyWord就不会影响_recordTab
                        '''
                        _recordTab.append(_keyWord)  # 错误记录表记录添加当前检测出的ID列表，ID列表可能为空
                        _keyWord = copy.deepcopy(_keyWord)  # 深拷贝
                        _keyWord.clear()  # 关键字列表清空（因为只存当前行的关键字ID,当前行变化了）
                        _allLineLi.append(li)
                        li = copy.deepcopy(li)
                        li.clear()
                    # try:
                    #     if pos < length:
                    #         pass
                    # except IndexError as ex:
                    #     print(ex)
                    #     print("注释出错，没有*/！！！！！！！！！！！！！！！")

                pos += 2  # 找到*/，直接跳过
                # _commentLineNumTab.append(_lineCount+1)  # 由于直接跳过*/,所以本应该在*/之后判断一次\n，这里提前添加
            elif code[pos+1] == '/':
                while code[pos] != '\n':  # code[pos] == '\n'退出循环
                    pos += 1
                _commentLineNumTab.append(_lineCount)  # 直接将当前行号添加
                pos += 1
                _lineCount += 1   # 行数加1
                # _chBegin = pos+1
                _keyWord.append(word.get('//'))
                _judgeStr = ''  # 清空
                _recordTab.append(_keyWord)
                _keyWord = copy.deepcopy(_keyWord)  # 深拷贝
                _keyWord.clear()
                _allLineLi.append(li)
                li = copy.deepcopy(li)
                li.clear()
            # elif code[pos+1] == ' ' or code[pos+1].isdigit() or code[pos+1].isalpha() or code[pos+1] in word:
            #     _keyWord.append(word.get('/'))          # 认为是除号
            # else:  # 否则认为是除号
            #   _keyWord.append(word['/'])
        elif code[pos] == '\n':  # 换行符
            pos += 1
            _lineCount += 1
            _recordTab.append(_keyWord)
            # print("行号是：{0}，这一行分析出的单词码是：{1}，单词表是{2}".format(_lineCount, _keyWord, _recordTab))
            _keyWord = copy.deepcopy(_keyWord)  # 深拷贝
            _keyWord.clear()
            # ----------------------
            _allLineLi.append(li)
            li = copy.deepcopy(li)
            li.clear()
            _judgeStr = ''
            forFlag = False
        elif code[pos] == '\t' or code[pos] == '\r' or code[pos] == '\v':  # 过滤制表符、回车符、垂直制表符
            pos += 1
        elif code[pos] == '"':
            pos += 1
            while code[pos] != '"':
                pos += 1
            pos += 1
        elif code[pos] == ' ' or code[pos] in delimiters or code[pos] in operator:
            if _judgeStr[0].isalpha() or _judgeStr[0] == '_':   # or _judgeStr[0] == '#'
                _judgeStr = _judgeStr[:-1]
                if _judgeStr in word:
                    # 保留字
                    get_value = word.get(_judgeStr)
                    if get_value is not None:
                        _keyWord.append(get_value)
                    li.append(_judgeStr)
                    if _judgeStr == 'for':
                        forFlag = True
                # elif _judgeStr[0] != '#':
                #     # 标识符
                #     _keyWord.append(word.get('标识符'))
                #     li.append(_judgeStr)
                # else:  # 以'#'开头
                #     li.append(_judgeStr)
                #     pass  # incldue
                else:
                    # 标识符
                    _keyWord.append(word.get('标识符'))
                    li.append(_judgeStr)
            # 常数
            elif _judgeStr[:-1].isdigit():
                pass
            # 字符是界符
            if code[pos] in delimiters:
                if forFlag and code[pos] == ';':  # 过滤for中的；
                    pass
                else:
                    get_value = word.get(code[pos])
                    if get_value is not None:
                        _keyWord.append(get_value)
                li.append(code[pos])
            # 字符是运算符
            elif code[pos] in operator:
                # s = code[pos]+code[pos+1]+code[pos+2]
                # s = _judgeStr
                s = ''
                s += code[pos]
                if code[pos+1] in operator:
                    pos += 1
                    s += code[pos]
                    # s = _judgeStr+code[pos]

                # if code[pos+1] in operator:
                #     pos += 1
                #     s += code[pos]
                get_value = word.get(s)
                if get_value is not None:
                    _keyWord.append(get_value)
                li.append(s)
            _judgeStr = ''
            pos += 1
        else:
            pos += 1
        # elif code[pos] == ' ':  # 过滤空格
        #     pos += 1
        # elif code[pos].isalpha():  # 如果是字母
        #     _judgeStr += code[pos]
        #     pos += 1
        #     while code[pos].isalpha() or code[pos].isdigit() or code[pos] == '_':
        #         _judgeStr += code[pos]
        #         pos += 1
        #     if _judgeStr in word:  # 如果字符串在单词表中存在
        #         _keyWord.append(word[_judgeStr])
        #     elif _judgeStr not in word:
        #         _keyWord.append(79)   # 标识符：79
        # elif code[pos].isdigit():  # 如果是数字
        #     _judgeStr += code[pos]  # 保存字符
        #     pos += 1
        #     while code[pos].isalpha() or code[pos].isdigit() or code[pos] == '_':
        #         _judgeStr += code[pos]
        #         pos += 1
        #     if _judgeStr in word:  # 如果字符串在单词表中存在
        #         _keyWord.append(word[_judgeStr])
        #     elif _judgeStr not in word and not _judgeStr.isdigit():
        #         #_keyWord.append(word[_judgeStr])
        #         pass
        #     else:
        #         pos += 1
        #         pass
        # elif not _judgeStr.isdigit() and not _judgeStr.isalpha() and _judgeStr in word:  # 其他字符如+=-/*界符等
        #     _keyWord.append(word[code[pos]])
        # else:
        #     pos += 1
        #     _judgeStr.replace(_judgeStr, '')
        #     # pass 如果以上情况都没有， 跳过，暂时不分
    '''最后一句如果没有回车符，keyword不会添加到_recordTab中去，这里在添加一次'''
    _recordTab.append(_keyWord)
    # print("行号是：{0}，这一行分析出的单词码是：{1}，单词表是{2}".format(_lineCount, _keyWord, _recordTab))
    _keyWord = copy.deepcopy(_keyWord)  # 深拷贝
    _keyWord.clear()
    _allLineLi.append(li)
    li = copy.deepcopy(li)
    li.clear()
    _judgeStr = ''
    print("扫描完毕")
    print(_recordTab)
    leng = len(_recordTab)
    print("leng:", leng)
    sec = 0
    for i in li:
        print(i, end='')
        sec += 1
        if sec == 15:
            sec = 0
            print('\n')
    return _recordTab, _commentLineNumTab, _allLineLi


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
    _9 = 2
    print(_9)
'''
    path = 'E:/毕业设计/学生代码规范化检测/CodeStyleCheck/ceshi2.txt'
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
            print("text:",text)
            a, b = Scanner(text)
            print('b', b)
    except IOError as e:
        print(e)
        traceback.print_exc()
    path = 'E:/毕业设计/学生代码规范化检测/CodeStyleCheck/ceshi2.txt'
    print('***************************_recordTab:', _recordTab)
    # try:
    #     with open(path, encoding='utf8', mode='r+') as f:
    #         ''' text = ''.join(f.readlines())
    #                     print("text类型：", type(text))
    #                     deal_text = re.sub(r'\/\*[^(*/)]*\*\/|\/\/.*', '1', text)  # 过滤注释
    #                     print(deal_text)
    #                     #for line in text.split('\n'):
    #                     for line in text:
    #                         line = line.strip()
    #                         #line = line.replace('\\t', '')
    #                         #line = line.replace('\\n', '')
    #                         print("num3:", line, end='')
    #
    #                         if line == '\n':
    #                             print('woshi----------------------------------------------------------')
    #                         if not line:
    #                             continue
    #                         else:
    #                             pass
    #                         '''
    #         text = f.read()
    #         print("check")
    #         a, b = Scanner(text)
    #         print('\nb', b)
    # except IOError as e:
    #     print(e)
    #     traceback.print_exc()
