#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2020/4/18 18:35
# @Author : yachao_lin
# @File : test.py
import pymysql

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
    # d = []
    # v = []
    # v.append(d)
    # d.clear()
    # d = copy.deepcopy(d)
    # d.append(1)
    # print(v)
    # d.clear()
    # d = copy.deepcopy(d)
    # d.append(1)
    # d.append(2)
    # d.append(3)
    # v.append(d)
    # print(v)
    # d = copy.deepcopy(d)
    # d.clear()
    # d.append(12)
    # v.append(d)
    # print(v)
    # jieshou = []
    # path = 'E:\毕业设计\学生代码规范化检测\CodeStyleCheck\cesi.txt'
    # try:
    #     with open(path, encoding='utf8', model='r+') as f:
    #         text = f.read()
    #         print("check")
    #         jieshou = Scanner(text)
    #         print("---------------------------------------------------------------\n", jieshou)
    # except IOError as e:
    #     print(e)for
    # reg = '^[\\s\\S]+[^ ]{1},[ ][^ ]+.*$$'
    # pattern = re.compile(reg)
    # string = ' int a , b,b,c'
    # f = pattern.match(string)
    # g = re.match(r'^12$', string)
    # print(f)
    # print(g)
    # if not f:
    #     print("f:ok!")
    # if g:
    #     print("g:ok!")
    # path = 'E:\毕业设计\学生代码规范化检测\CodeStyleCheck\cesi.txt'
    # p = path.split('\\')
    # print(type(p))
    # print(p)
    # print(p[-1])
    tab = [[], [], [1], [1, 2], []]
    a = []
    if not a:
        print(123)
    print("a:", a)
    if not tab[0]:
        print("is")
    i = len(tab[2])
    print(i)

    # print(type(tab[2]))
    db = pymysql.connect("localhost", "root", "123456", "cstyle_db")
    cursor = db.cursor()
    idd = '5'
    try:
        sql = "select ruleid, name, express, advice, standard, ruletypeid from rule where WordID = %s" % idd
        cursor.execute(sql)
        db.commit()
        ss = cursor.fetchall()
        print(ss)
        ss = str((list(ss[0]))[0])
        print(ss)
        print(type(ss))
    except Exception as e:
        print("Failed")
        print(e)
    # s =(('^[\\\\s\\\\S]+[^ ]{1},[ ][^ ]+.*$',), (123))
    # db.close()
    # print("s:", s, type(s))
    # s = ''.join(s[0])

