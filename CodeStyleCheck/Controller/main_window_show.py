#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2020/4/12 22:04
# @Author : yachao_lin
# @File : main_window_show.py
import fileinput
import re
import time
import traceback
from typing import List, Any

import pymysql
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from CodeStyleCheck.Controller.myEditRule_ui import MyEditRule
from CodeStyleCheck.Controller.show_result import MyResult
from CodeStyleCheck.GUI.InputStuID import Ui_Dialog
from CodeStyleCheck.GUI.text_editor import QCodeEditor
from CodeStyleCheck.GUI.main_window import Ui_MainWindow
from CodeStyleCheck.Controller.test_regxExpre import Scanner
from CodeStyleCheck.model.mydb import MysqlOperation

# from CodeStyleCheck.lianxi.QCodeEditor1 import QCodeEditor

glo_file_path = ""  # 全局变量存储：文件路径
record_tab: List[Any] = []  # 全局记录表：存储所有行的单词种别码
ErrorID_record = []  # 错误记录表，记录本次运行检查获取的所有错误ID
student_id = 1
current_file_id = -1  # 当前文件id
data_lst = []  # 打开文件时，获取当前文件错误信息，id 保存在此列表中

# commmet_word = 'char': 1, 'double': 2, 'enum': 3, 'float': 4, 'int': 5,
#         'long': 6, 'short': 7, 'signed': 8, 'union': 9, 'unsigned': 10,
#         'struct': 11, 'void':12, '标识符': 79, '(': 73
'''注释检测关键字种别码表'''
comment_word = [1, 2, 3, 4, 5, 12]  # 79, 73  '标识符': 79, '(': 73


class Login(QDialog, Ui_Dialog):
    closeSignal = pyqtSignal(str)  # 自定义信号，传递一个字符串参数

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        # 设置为模态对话框/只有当前对话框可用
        self.setWindowModality(Qt.ApplicationModal)
        self.initUI()

    def initUI(self):
        self.pushButton.clicked.connect(self.emit_signal)
        self.pushButton_2.clicked.connect(self.close)

    # 发射自定义信号槽函数，传递参数给主窗口函数
    def emit_signal(self):
        StuID = self.lineEdit.text()  # 获得文本内容
        if len(StuID) == 0:
            QMessageBox.warning(self, "提示", "输入不能为空!!!")
        else:
            self.closeSignal.emit(StuID)
            print("成功发射StuID:----->", StuID)
            self.close()


class QMyWindow(QMainWindow, Ui_MainWindow):
    showResultSignal = pyqtSignal(int, int)  # 自定义信号，传递路径、学号给showResult窗口

    def __init__(self):
        super(QMyWindow, self).__init__()
        self.ui2 = MyResult()  # 错误显示界面
        self.setupUi(self)
        self.myTextEditor = QCodeEditor()
        self.horizontalLayout.addWidget(self.myTextEditor)
        self.mysqlConnOperation = MysqlOperation("localhost", "root", "123456", "cstyle_db")
        self.initUI()

    # 后台逻辑处理
    def initUI(self):
        # 关联信号与槽函数
        self.action_open.triggered.connect(self.open_file_action)
        self.action_save.triggered.connect(self.save_file_action)
        self.action_close.triggered.connect(self.close_file_action)
        self.action_quit.triggered.connect(self.mainWindow_quit)
        self.action_run.triggered.connect(self.code_check_action)
        self.action_run.triggered.connect(self.analyze_result)
        self.action_edit.triggered.connect(self.jump_to_1)
        self.action_result.triggered.connect(self.jump_to_2)

    def jump_to_1(self):
        self.ui1 = MyEditRule()  # 配置规则界面
        self.ui1.show()

    def jump_to_2(self):
        global glo_file_path, student_id
        self.showResult_emit_signal()
        self.ui2.show()

    # # 输入学号
    # def inputInfo(self):
    #     self.dialog = Login()
    #     '''连接信号与槽函数，连接子窗口的自定义信号与主窗口的槽函数'''
    #     self.dialog.signalInfo.connect(self.deal_emit_slot)
    #     self.dialog.show()
    #     print("12")

    # 获得学号，打开主界面
    def deal_emit_slot(self, StuID):
        time.sleep(0.5)
        global student_id
        student_id = ''
        student_id += StuID
        self.show()
        print("studentID:", student_id)

    # 结果显示界面，发射信号函数   # 发射自定义信号槽函数，传递参数给结果显示窗口函数
    def showResult_emit_signal(self):
        global current_file_id, student_id
        self.showResultSignal.emit(current_file_id, student_id)
        print("成功发射current_file_id, student_id:----->", current_file_id, student_id)

    # 代码文件加载线程
    def open_file_action_thread(self):
        pass

    # 打开代码文件
    def open_file_action(self):
        # global ErrorID_record
        # ErrorID_record = []  # 初始化错误记录表,记录本次运行检查获取的所有错误ID   **注意****检查已经改为运行前检查****
        # 建立一个文件对话框
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)  # 设置文件模式（这里操作对象为任何文件）
        dialog.setFilter(QDir.Files)  # 设置过滤器（这里显示所有文件列表）
        # 打开对话框
        if dialog.exec():
            file_path = dialog.selectedFiles()  # 接受选中文件的路径，路径默认保存在列表
            print("file_path: ", file_path)
            global glo_file_path
            glo_file_path = file_path[0]  # 获取文件路径
            print("保存文件路径：", glo_file_path)
            self.textBrowser.setPlainText(glo_file_path)  # 显示文件路径
            text_content = ''
            try:
                # 读写方式打开文件
                with open(glo_file_path, mode='r', encoding='utf-8') as f:
                    for line in f:
                        text_content += line  # 获取文件内容
                        # print(line.rstrip('\n'))
                        self.myTextEditor.appendPlainText(line.rstrip('\n'))
            except IOError as e:
                print(e)
                print("打开文件失败!")
            # self.myTextEditor.appendPlainText(text_content)
            list_path = glo_file_path.split('/')
            file_name = list_path[-1]  # 获取文件名
            print("open_file_action_______list_path", list_path)
            print("open_file_action_______textName:", file_name)
            global student_id
            sql1 = "select * from code where FilePath = '%s' and StudentID = '%s' " % (
                pymysql.escape_string(glo_file_path), student_id)
            print(sql1)
            res = None
            res = self.mysqlConnOperation.select_one(sql1)
            if res:  # 如果数据库中有该代码文件信息，不处理
                print("该文件信息已经存储过!")
            else:  # 没有代码文件信息，保存至数据库
                datetime = QDateTime.currentDateTime()  # 获取当前时间精确到秒
                strTime = datetime.toString()  # 转化为字符串
                sql2 = "insert into `code` " \
                       "(`FileName`,`FileContent`,`SaveDate`,`ModifyDate`,`FilePath`,`StudentID`)" \
                       "VALUES('%s','%s','%s','%s','%s','%s')" % \
                       (pymysql.escape_string(file_name),
                        pymysql.escape_string(text_content),
                        pymysql.escape_string(strTime),
                        pymysql.escape_string(strTime),
                        pymysql.escape_string(glo_file_path),
                        pymysql.escape_string(str(student_id)))
                rowNum = None
                rowNum = self.mysqlConnOperation.insert(sql2)
                print("受影响行号rowNum：", rowNum)
            sql_findCodeId = "select CodeID from code where FilePath = '%s' and StudentID = '%s'" % \
                             (pymysql.escape_string(glo_file_path), pymysql.escape_string(str(student_id)))
            res1 = None
            res1 = self.mysqlConnOperation.select_one(sql_findCodeId)
            print('res1:', res1)
            global current_file_id
            current_file_id = res1[0]
            print(current_file_id, type(current_file_id))

    # 文件另存为
    def save_other_file_action(self):
        pass

    # 保存文件
    def save_file_action(self):
        global glo_file_path, student_id, current_file_id
        # if glo_file_path is not None:
        print("保存文件路径：", glo_file_path)
        try:
            with open(glo_file_path, mode='w', encoding='utf-8') as f:
                cont = self.myTextEditor.toPlainText()
                f.write(cont)  # 重新对该文件写入
                datetime = QDateTime.currentDateTime()
                datetime = datetime.toString()
                print("保存文件->时间：", datetime)
                '''sql语句书写不标准，修改多个属性的值，用逗号隔开，不用and(不用and好像不对)'''
                sql = "update code set FileContent = '%s', ModifyDate = '%s' where CodeID = '%s'" % \
                      (pymysql.escape_string(cont),
                       pymysql.escape_string(datetime),
                       current_file_id)
                self.mysqlConnOperation.update(sql)
                print("保存成功！")
        except IOError as e:
            print("exception:glo_file_path", e)

    # 清屏
    def close_file_action(self):
        self.myTextEditor.selectAll()
        self.myTextEditor.clear()
        self.textBrowser.selectAll()
        self.textBrowser.clear()
        self.textBrowser_2.selectAll()
        self.textBrowser_2.clear()
        global glo_file_path, record_tab
        glo_file_path = ''
        record_tab = []

    # 重写关闭事件（用函数调用它没有用）
    def closeEvent(self, event, parent=None):
        reply = QMessageBox.question(parent, '提示', '你确定要关闭吗？',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    # 退出
    @staticmethod
    def mainWindow_quit():
        app = QApplication.instance()
        app.exit()

    # 代码检查
    def code_check_action(self):
        """
        分析文件中的代码，运行前先获取所有错误信息，保存在 data_lst 中
        :return:
        """
        global current_file_id
        # 查找所有错误条目
        sql_findAllError = "select * from error where FileID = '%s'" % current_file_id
        error_all, descr = self.mysqlConnOperation.select_all(sql_findAllError)
        global data_lst
        data_lst = [error_all[i][0] for i in range(len(error_all))]
        print('data', error_all)
        print('list-->', data_lst)
        print('record-->', ErrorID_record)
        global glo_file_path, record_tab
        try:
            with open(glo_file_path, mode='r', encoding='utf8') as f:
                text0 = f.read()
                record_tab, commentLineNum_Tab = Scanner(text0)  # commentLineNum_Tab = []  保存注释所在行行号
                print("record_tab:", record_tab)
                self.mysql_operate(text0, commentLineNum_Tab)
                # self.analyze_align(text0)

        except IOError as e:
            print(e)

    def mysql_operate(self, text0_para1, commentLineNumTab_para2):
        """
        逐个分析单词，将分析结果保存在error数据表里
        Error表中的corrected属性值有两种：是，否；代表该条错误是否已经更改，在设置一个类属性ErrorID_record[]为列表，每次打开文件时
        在打开文件函数中初始化这个列表，每次运行"完毕",--运行完---，之后获取所有ErrorID，将ErrorID与ErrorID_record比较，如果不在
        ErrorID_record 中的编号ErrorID中没有，则将corrected改为是，否则pass

        空行:设置一个标志，遇到一个空行激活标志，连续遇到就用正则表达式匹配
        :return:
        """
        global glo_file_path, record_tab, student_id, current_file_id, ErrorID_record
        # db = pymysql.connect("localhost", "root", "123456", "cstyle_db")
        # cursor = db.cursor()
        # cursor.execute("select VERSION()")
        # data = cursor.fetchall()
        # print(data)

        try:
            list_path = glo_file_path.split('/')
            file_name = list_path[-1]  # 获取文件名
            print("list_path", list_path)
            print("textName:", file_name)
            len_record_tab = len(record_tab)  # 列表长度
            print("length:", len_record_tab)
            i = 0
            with open(glo_file_path, mode='r', encoding='utf8') as f:
                for line_str in f:
                    print("第{0}行代码{1}".format(i, line_str))
                    if not record_tab[i]:  # 元素为空，行号加1
                        i += 1
                        if i >= len_record_tab:
                            break
                    else:
                        tab = record_tab[i]
                        i_length = len(tab)  # 第i行单词表长度
                        for j in range(i_length):
                            var = tab[j]
                            # try:
                            select_sql = "select " \
                                         "RuleID, Express, RuleTypeID from rule " \
                                         "where WordID = '%s'" % int(var)
                            # cursor.execute(select_sql)
                            # db.commit()
                            # print("查询成功")
                            # reg_tup = cursor.fetchall()  # 获取所有符合的正则表达式，返回一个元组
                            reg_tup, descr = self.mysqlConnOperation.select_all(select_sql)  # 获取所有符合的正则表达式，返回一个元组
                            print('reg_tup:', reg_tup)
                            # flag_mark = False
                            # if reg_tup and list(reg_tup[0])[0] != '45' and list(reg_tup[0])[0] != '44':
                            #     flag_mark = True
                            if reg_tup:  # and flag_mark is True:
                                reg_str = str(list(reg_tup[0])[1])  # 元组转换为字符串
                                _ruleid = list(reg_tup[0])[0]  # 获取ruleid
                                _ruletypeid = list(reg_tup[0])[2]  # 获取ruletypeid
                                # reg_str = ''.join(reg_tup[0])   # 元组转换为字符串
                                print("reg_str:", reg_str, type(reg_str))
                                pattern = re.compile(reg_str)  # 编译正则表达式
                                print("line----->:", type(line_str), line_str)
                                mark = pattern.match(line_str)  # 匹配
                                print("mark:", mark)
                                if not mark:  # 如果不匹配mark = None,这行代码形式不规范   # WrongCode = '%s'and
                                    sql_err = "select * from error where Name = '%s'and RuleID = '%d' and RuleTypeID" \
                                              "= '%d'and Line = '%d'and FileID = '%s'" \
                                              % (pymysql.escape_string(file_name),
                                                 _ruleid,
                                                 _ruletypeid,
                                                 int(i) + 1,
                                                 #  pymysql.escape_string(str(line_str)),
                                                 current_file_id)
                                    # response = cursor.execute(sql_err)
                                    # db.commit()
                                    response = self.mysqlConnOperation.select_one(sql_err)  # 查询此条错误记录是否已经存在,返回一个元组或者空
                                    if response:
                                        print("错误已存在！")
                                        print("response:", response[0], type(response[0]))
                                        if response[0] not in ErrorID_record:
                                            ErrorID_record.append(response[0])  # 将此次查询到的--已经存在--的错误的错误Id保存下来，
                                            print("ErrorId_record:", ErrorID_record)
                                        # 更新错误行代码
                                        update_sql = "update error set error.WrongCode = '%s' where error.ErrorID = '%s'"\
                                                     % (pymysql.escape_string(str(line_str)), response[0])
                                        self.mysqlConnOperation.update(update_sql)
                                    else:
                                        # # try:
                                        # select_fileID_sql = "select CodeID from Code where FilePath = '%s'and " \
                                        #                     "StudentID = '%s'" % (
                                        #                         pymysql.escape_string(glo_file_path), student_id)
                                        # file_id = self.mysqlConnOperation.select_one(select_fileID_sql)
                                        # print("文件ID查询成功!", file_id)
                                        insert_sql = "insert into error (Name, RuleID, RuleTypeID, Line, " \
                                                     "WrongCode,FileID) values('%s', '%s', '%s', '%s', '%s','%s')" % \
                                                     (pymysql.escape_string(file_name),
                                                      _ruleid,
                                                      _ruletypeid,
                                                      pymysql.escape_string(str(int(i) + 1)),
                                                      pymysql.escape_string(str(line_str)),
                                                      current_file_id)
                                        # cursor.execute(insert_sql)
                                        # db.commit()
                                        if int(var) == 86 and 'for' in str(line_str):    # ';':86,for 语句中可以有多个';'
                                            pass
                                        else:
                                            self.mysqlConnOperation.insert(insert_sql)
                                            print("Error插入成功!")
                                        # except Exception as e:
                                        #     print(e)
                                        #     print("插入错误")
                                        #     db.rollback()
                            else:
                                pass
                            # except Exception as e:
                            #     print(e)
                            #     print("查询出错")
                            #     db.rollback()
                            # finally:
                            #     cursor.close()
                            #     db.close()
                        i += 1
                        if i >= len_record_tab:
                            break
        except IOError as e1:
            print("文件打开问题", e1)
            traceback.print_exc()
        finally:
            text0 = text0_para1
            commentLineNum_Tab = commentLineNumTab_para2
            self.analyze_comment(text0, commentLineNum_Tab)
            '''将以前检查出来，而此次未查询到的错误条目信息中的是否更改属性置为--是-- '''
            error_length = len(ErrorID_record)
            print('error_length:', error_length)
            # if 0 == error_length:
            #     pass
            # else:
            # data_lst - ErrorID_record ：差集
            try:
                global data_lst
                print('list-->', data_lst)
                print('record-->', ErrorID_record)
                ret = None
                ret = list(set(data_lst).difference(set(ErrorID_record)))
                print('ret:', ret)
                ErrorID_record.clear()
                if ret:
                    for i in range(len(ret)):
                        sql_Corrected = "update error set error.Corrected = '是'where ErrorID = '%s'" % ret[i]
                        self.mysqlConnOperation.update(sql_Corrected)
            except Exception as e:
                print('空集', e)

    def analyze_result(self):
        """
        查询程序分析的结果，从error数据表中查询错误信息
        :return:
        """
        global glo_file_path, current_file_id, student_id
        # db = pymysql.connect("localhost", "root", "123456", "cstyle_db")
        # cursor = db.cursor()
        list_path = glo_file_path.split('/')
        file_name = list_path[-1]  # 获取文件名
        print("list_path", list_path)
        print("textName:", file_name)
        sql = "select  error.Name, rule.Name,rule.Advice, ruletype.Name, error.Line, error.WrongCode, error.Corrected" \
              " from error left join rule on error.RuleID = rule.RuleID left join ruletype on " \
              "error.RuleTypeID = ruletype.RuleTypeID left join code c on error.FileID = c.CodeID" \
              " where c.CodeID = '%s' and c.StudentID = '%s'and error.Corrected = '否' order by error.Line " % (
                  current_file_id, student_id)
        try:
            # cursor.execute(sql)
            # data = cursor.fetchall()
            data, descr = self.mysqlConnOperation.select_all(sql)
            print("代码分析结果查询成功！")
            # print(data)
            length = len(data)
            '''清空显示器，再更新显示'''
            self.textBrowser_2.selectAll()
            self.textBrowser_2.clear()
            for i in range(length):
                txt = (list(data[i]))
                print(txt)
                # for j in range(len(txt)): '  当前文件名称：' + str(txt[0]) +
                txt_str = '序号：' + str(i) + '  错误行号：第 ' + str(txt[4]) + ' 行' + '错误原因：' + str(txt[1]) + \
                          '  错误类型：' + str(txt[3]) + '  建议：' + str(txt[2]) + '  错误代码：' + str(txt[5])  # + '\n '
                self.textBrowser_2.append(txt_str)
            if 0 == length:
                self.textBrowser_2.append("未检查出错误!")
        except Exception as e:
            print(e)
            print("查询失败：analyze_result函数")

    # 分析注释  初始化也可以加上
    def analyze_comment(self, para, commentTab):
        text = para
        commentLineNumTab = commentTab  # 注释所在行的行号列表
        global record_tab
        length = len(record_tab)
        print("analyze_comment--->length", length)
        print(record_tab)
        for i in range(length):
            tab = record_tab[i]
            if len(tab) >= 4:  # 定义一个函数，比如int abc(),至少有四个关键字，int, abc,(,),长度大于4，过滤信息，增加执行速度
                for j in range(len(tab)):
                    '''分析这行代码操作是否是定义一个***函数***'''
                    if tab[j] in comment_word and 79 == tab[j + 1] and 73 == tab[j + 2]:
                        print("行号：", i + 1)
                        print("hang:", tab)
                        currLineNum = i + 1
                        if i in commentLineNumTab:
                            print("该函数有注释")
                        else:
                            global glo_file_path, current_file_id
                            with open(glo_file_path, mode='r', encoding='utf8') as f:
                                txt = f.readlines()
                            print('analyze_comment----->txt----->:', txt)
                            try:
                                list_path = glo_file_path.split('/')
                                file_name = list_path[-1]  # 获取文件名
                                # ['44', '每个函数前应该有注释声明', '/*注释*/', '每个函数前应该有注释声明', '/*注释*/ int fun(para)', '1', '71']
                                # ['45', '每个变量声明后应该注释', '//注释', '每个变量声明后应该注释', 'int i=0; //注释', '1', '72']
                                sql_err = "select * from error where Name = '%s'and RuleID = '%d' and RuleTypeID" \
                                          "= '%d'and Line = '%d'and FileID = '%s'" \
                                          % (pymysql.escape_string(file_name),
                                             44,
                                             1,
                                             currLineNum,
                                             current_file_id)
                                response = self.mysqlConnOperation.select_one(sql_err)  # 查询此条错误记录是否已经存在,返回一个元组或者空
                                if response:  # 错误存在
                                    print("错误已存在！")
                                    print("response:", response[0], type(response[0]))
                                    if response[0] not in ErrorID_record:
                                        ErrorID_record.append(response[0])  # 将此次查询到的--已经存在--的错误的错误Id保存下来，
                                        print("ErrorId_record:", ErrorID_record)
                                    # 更新错误行代码
                                    update_sql = "update error set error.WrongCode = '%s' where error.ErrorID = '%s'" \
                                                 % (pymysql.escape_string(str(txt[currLineNum])), response[0])
                                else:  # 错误不存在

                                    sql_insert = "insert into error (Name, RuleID, RuleTypeID, Line, WrongCode,FileID)" \
                                                 " values('%s', '%s', '%s', '%s', '%s','%s')" % \
                                                 (pymysql.escape_string(file_name),
                                                  44,
                                                  1,
                                                  currLineNum,
                                                  pymysql.escape_string(str(txt[currLineNum])),
                                                  current_file_id)
                                    self.mysqlConnOperation.insert(sql_insert)
                            except Exception as e:
                                print(e)
                                traceback.print_exc()
                            break
                    else:
                        j += 1
            else:
                pass

    # 分析缩进与对齐
    def analyze_align(self, para):
        text = para
        sql = "select Express from rule where RuleTypeID = '%s'" % 4
        receiveInfo = self.mysqlConnOperation.select_one(sql)
        print('每一级缩进空格数：', receiveInfo[0], type(receiveInfo[0]))  # space[0]为str类型
        # 每一级缩进空格数
        space = int(receiveInfo[0])
