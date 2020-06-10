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
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from CodeStyleCheck.Controller.analyzeCompare import AnalyzeCompare
from CodeStyleCheck.Controller.myEditRule_ui import MyEditRule
from CodeStyleCheck.Controller.show_configRule import MyConfigRule
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
record_align_spaceNum = {}  # 记录对齐行所需要的缩进等级,key:value(行号：等级)
# commmet_word = 'char': 1, 'double': 2, 'enum': 3, 'float': 4, 'int': 5,
#         'long': 6, 'short': 7, 'signed': 8, 'union': 9, 'unsigned': 10,
#         'struct': 11, 'void':12, '标识符': 79, '(': 73
'''注释检测关键字种别码表'''
comment_word = [1, 2, 3, 4, 5, 12]  # 79, 73  '标识符': 79, '(': 73
# 记录正确代码的列表
rightCodeList = []
r1 = []


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
        # self.closeSignal.connect(QMyWindow().deal_emit_slot)

    # 发射自定义信号槽函数，传递参数给主窗口函数
    def emit_signal(self):
        StuID = self.lineEdit.text()  # 获得文本内容
        if len(StuID) != 12 or not StuID.isdigit():  # 163406010404
            QMessageBox.warning(self, "提示", "输入12位数字学号!!!")
        else:
            self.closeSignal.emit(StuID)
            print("成功发射StuID:----->", StuID)
            self.close()


class QMyWindow(QMainWindow, Ui_MainWindow):
    showResultSignal = pyqtSignal(int, str)  # 自定义信号，传递路径、学号给showResult窗口
    analyzeCompareSignal = pyqtSignal(str, list)  # 将当前路径，存有正确代码的列表传递给对比分析函数

    def __init__(self):
        super(QMyWindow, self).__init__()
        self.ui1 = MyEditRule()  # 编辑规则界面
        self.ui2 = MyResult()  # 错误显示界面
        self.ui3 = AnalyzeCompare()  # 对比分析界面
        self.ui4 = MyConfigRule()  # 配置规则页面
        self.setupUi(self)
        self.myTextEditor = QCodeEditor()
        self.horizontalLayout.addWidget(self.myTextEditor)
        self.horizontalLayout.setSpacing(0)  # 去掉文件路径与文本编辑器之间的缝隙
        self.mysqlConnOperation = MysqlOperation("localhost", "root", "123456", "cstyle_db")
        self.rulePermissionList = []  # 规则许可，只可以使用这些规则
        ''''初始化选中所有规则'''
        sql_ruleid = "select RuleID from rule"
        res_id, descri = self.mysqlConnOperation.select_all(sql_ruleid)
        self.rulePermissionList = [i[0] for i in res_id]

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
        self.action_compare.triggered.connect(self.jump_to_3)
        self.action_config.triggered.connect(self.jump_to_4)
        self.showResultSignal.connect(self.ui2.deal_showResult_emit_slot)
        self.analyzeCompareSignal.connect(self.ui3.deal_analyzeCompare_slot)
        self.ui4.transmitRuleSignal.connect(self.deal_emit_transmitRule_slot)

    def jump_to_1(self):
        """
        展示编辑规则页面
        :return:
        """
        self.ui1.show()

    def jump_to_2(self):
        """
        展示分析结果，错误记录页面
        :return:
        """
        self.showResult_emit_signal()  # 发送信号
        self.ui2.show()

    def jump_to_3(self):
        """
        对比分析页面
        :return:
        """
        global glo_file_path, rightCodeList
        self.analyzeCompareSignal.emit(glo_file_path, rightCodeList)  # 发射信号
        self.ui3.show()

    def jump_to_4(self):
        """
        配置规则页面
        :return:
        """
        self.ui4.show()

    # # 输入学号
    # def inputInfo(self):
    #     self.dialog = Login()
    #     '''连接信号与槽函数，连接子窗口的自定义信号与主窗口的槽函数'''
    #     self.dialog.signalInfo.connect(self.deal_emit_slot)
    #     self.dialog.show()
    #     print("12")

    # 获得允许使用的规则的编号
    def deal_emit_transmitRule_slot(self, ruleIdList):
        """
        接收配置规则页面传回来的规则id列表--槽函数
        :param ruleIdList:
        :return:
        """
        print('我是主窗口，我收到了信号：', ruleIdList)
        self.rulePermissionList = ruleIdList

    def deal_emit_slot(self, StuID):
        """
        接收来自登陆界面的信号---接收学号
        打开主界面
        :param StuID:
        :return:
        """
        time.sleep(0.5)
        global student_id
        student_id = ''
        student_id = str(StuID)
        print("成功接收studentID:----->", student_id)
        self.show()
        Login().close()

    def showResult_emit_signal(self):
        """
        发射自定义信号槽函数，传递参数给结果显示窗口函数
        :return:
        """
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
        self.close_file_action()
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
        self.ui3.textBrowser.selectAll()
        self.ui3.textBrowser.clear()
        self.ui3.textBrowser_2.selectAll()
        self.ui3.textBrowser_2.clear()
        global glo_file_path, record_tab, current_file_id
        glo_file_path = ''
        record_tab = []
        current_file_id = -1

    # 重写关闭事件（用函数调用它没有用）
    def closeEvent(self, event, parent=None):
        reply = QMessageBox.question(parent, '提示', '你确定要关闭吗？',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.ui1.close()
            self.ui2.close()
            self.ui3.close()
            self.ui4.close()
            event.accept()
        else:
            event.ignore()

    # 退出
    def mainWindow_quit(self):
        self.ui1.close()
        self.ui2.close()
        self.ui3.close()
        self.ui4.close()
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
            self.mysql_operate(commentLineNum_Tab)
        except IOError as e:
            print(e)
            traceback.print_exc()

    # 核心检测函数
    def mysql_operate(self, commentLineNumTab_para2):
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
                            print('tab:', tab)
                            print('length:', i_length)
                            print('var:', var, 'j:', j)
                            if var is None:
                                while True:
                                    pass
                            select_sql = "select " \
                                         "RuleID, Express, RuleTypeID from rule " \
                                         "where WordID = '%s'" % int(var)
                            # cursor.execute(select_sql)
                            # db.commit()
                            # print("查询成功")
                            # reg_tup = cursor.fetchall()  # 获取所有符合的正则表达式，返回一个元组
                            reg_tup = self.mysqlConnOperation.select_one(select_sql)  # 获取所有符合的正则表达式，返回一个元组
                            print('reg_tup:', reg_tup)
                            # flag_mark = False
                            # if reg_tup and list(reg_tup[0])[0] != '45' and list(reg_tup[0])[0] != '44':
                            #     flag_mark = True
                            if reg_tup and int(reg_tup[0]) in self.rulePermissionList:  # and flag_mark is True:
                                reg_str = str(reg_tup[1])  # 元组转换为字符串
                                _ruleid = int(reg_tup[0])  # 获取ruleid
                                _ruletypeid = int(reg_tup[2])  # 获取ruletypeid
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
                                        update_sql = "update error set error.WrongCode = '%s' where error.ErrorID = '%s'" \
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
                                        if int(var) == 86 and 'for' in str(line_str):  # ';':86,for 语句中可以有多个';'
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
            commentLineNum_Tab = commentLineNumTab_para2
            '''分析注释函数'''
            self.analyze_comment(commentLineNum_Tab)
            '''分析缩进对齐、空行函数'''
            newAlignCode, alignSpaceNow = self.analyze_align()
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
            '''最后一步：生成正确代码'''
            self.produce_right(newAlignCode, alignSpaceNow)

    # 显示分析结果
    def analyze_result(self):
        """
        查询程序分析的结果，从error数据表中查询错误信息
        :return:
        """
        global glo_file_path, current_file_id, student_id, record_align_spaceNum
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
                if txt[3] == '对齐':
                    # 当前行号为 txt[4]
                    print('--', txt[3], type(txt[3]))
                    print('--------------------------', record_align_spaceNum)
                    space = record_align_spaceNum.get('space')
                    indentClass = record_align_spaceNum.get(int(txt[4]))
                    print('indentClass:', indentClass, '序号：', i + 1)
                    txt_str = '序号：' + str(i + 1) + '  错误行号：第 ' + str(txt[4]) + ' 行' + '  错误原因：' + str(txt[1]) + \
                              '  错误类型：' + str(txt[3]) + '  建议：缩进' + str(
                        indentClass * space) + '个ASCAll空格字符' + '  错误代码：' + str(txt[5])
                else:
                    txt_str = '序号：' + str(i + 1) + '  错误行号：第 ' + str(txt[4]) + ' 行' + '  错误原因：' + str(txt[1]) + \
                              '  错误类型：' + str(txt[3]) + '  建议：' + str(txt[2]) + '  错误代码：' + str(txt[5])  # + '\n '
                self.textBrowser_2.append(txt_str)
            if 0 == length:
                self.textBrowser_2.append("未检查出错误!")
        except Exception as e:
            print(e)
            traceback.print_exc()
            print("查询失败：analyze_result函数")
        finally:
            record_align_spaceNum.clear()

    # 分析注释  初始化也可以加上
    def analyze_comment(self, commentTab):
        global glo_file_path, current_file_id
        try:
            with open(glo_file_path, mode='r', encoding='utf8') as f:
                txt = f.readlines()
            print('analyze_comment----->txt----->:', txt)
        except Exception as e:
            print(e)
            traceback.print_exc()
        commentLineNumTab = commentTab  # 注释所在行的行号列表
        global record_tab
        length = len(record_tab)
        print("analyze_comment--->length", length)
        print(record_tab)
        for i in range(length):
            commentFlag = True
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
                            i_pos = i
                            while True:
                                mark = re.match('^[ ]*$', str(txt[i_pos]))
                                if mark:
                                    i_pos -= 1
                                    if i_pos < 0:
                                        break
                                    if i_pos in commentLineNumTab:
                                        print('有注释')
                                        commentFlag = False
                                        break
                                else:
                                    break
                            if commentFlag:
                                # commentFlag = True
                                try:
                                    list_path = glo_file_path.split('/')
                                    file_name = list_path[-1]  # 获取文件名
                                    # ['44', '每个函数前应该有注释声明', '/*注释*/', '每个函数前应该有注释声明', '/*注释*/ int fun(para)', '1', '71']
                                    # ['45', '每个变量声明后应该注释', '//注释', '每个变量声明后应该注释', 'int i=0; //注释', '1', '72']
                                    sql_select = "select RuleID from rule where RuleTypeID = '%s'and WordID = '%s'" % (
                                        1, 71)  # ruleType = 1--->注释
                                    rece = self.mysqlConnOperation.select_one(sql_select)
                                    '''判断当前规则在不在规则许可列表里，如果不在，直接retern None'''
                                    print('rece', rece)
                                    if rece[0] not in self.rulePermissionList:  # 如果不在直接返回
                                        return None
                                    sql_err = "select * from error where Name = '%s'and RuleID = '%d' and RuleTypeID" \
                                              "= '%d'and Line = '%d'and FileID = '%s'" \
                                              % (pymysql.escape_string(file_name),
                                                 rece[0],
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
                                                     % (
                                                         pymysql.escape_string(str(txt[currLineNum - 1])),
                                                         int(response[0]))
                                    else:  # 错误不存在

                                        sql_insert = "insert into error (Name, RuleID, RuleTypeID, Line, WrongCode,FileID)" \
                                                     " values('%s', '%s', '%s', '%s', '%s','%s')" % \
                                                     (pymysql.escape_string(file_name),
                                                      rece[0],
                                                      1,
                                                      currLineNum,
                                                      pymysql.escape_string(str(txt[currLineNum - 1])),
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

    # 分析缩进与对齐,还有空行
    def analyze_align(self):
        """
        关于缩进错误的显示：我采用一个全局字典保存缩进一级所需空格个数目，以及采用错误行为键，缩进数目为值的键值对存储，实时显示运行结果时，显示
        '建议'时：根据当前字典信息显示哪一行需要缩进多少空格。
        其他错误：直接读取数据库中规则表存储的建议即可
        关于空行错误：从数据库读取正则表达式，匹配
        :return:
        """
        # 从数据库查找缩进规则表达式，表达式中存储了缩进一级需要的空格数目
        sql_indent = "select Express from rule where RuleTypeID = '%s'" % 4
        receiveInfo = self.mysqlConnOperation.select_one(sql_indent)
        print('每一级缩进空格数：', receiveInfo[0], type(receiveInfo[0]))  # space[0]为str类型
        # 每一级缩进空格数
        space = int(receiveInfo[0])
        global record_align_spaceNum  # 存储错误行所需要的缩进等级
        record_align_spaceNum['space'] = space  # 此处存储规则中的每一级缩进空格个数
        global glo_file_path  # 当前文件路径
        global current_file_id  # 当前文件id号
        global ErrorID_record  # 记录此次运行出现的问题
        text_list = None
        with open(glo_file_path, mode='r', encoding='utf8') as f:
            text_list = f.readlines()
        txt_length = len(text_list)
        print('text', text_list)
        list_path = glo_file_path.split('/')
        file_name = list_path[-1]  # 获取文件名
        pos = 0  # 位置坐标，记录行号
        indent_class = 0  # 缩进级别为 0
        newText_list = []  # 存储缩进正确后的每一行字符
        '''判断空行语句以及接收返回值'''
        sql_select_blankLine = "select RuleID, Express from rule where RuleTypeID = 2 and WordID = 80"
        blankLineResponse = self.mysqlConnOperation.select_one(sql_select_blankLine)
        while pos < txt_length:
            lineStr = text_list[pos]
            if '{' in lineStr:
                newlineStr = ' ' * indent_class * space + lineStr.strip() + '\n'  # + '\n'   # 去掉两端空格后重新添加正确数目的空格
                indent_class += 1  # 缩进级别加1，这条语句不能提前
            elif '}' in lineStr:
                indent_class -= 1  # 缩进级别减1，遇到'}' *先* 执行缩进级别减1
                newlineStr = ' ' * indent_class * space + lineStr.strip() + '\n'  # + '\n'
            else:
                # if pos == txt_length-1:
                #     newlineStr = ' ' * indent_class * space + lineStr.strip()
                # else:
                newlineStr = ' ' * indent_class * space + lineStr.strip() + '\n'  # + '\n'
                '''接下来判断空行'''
                if blankLineResponse:  # 正则表达式存在：
                    reg_str = str(blankLineResponse[1])  # 元组转换为字符串
                    bl_rule_id = int(blankLineResponse[0])  # 获取ruleid
                    print("reg_str:", reg_str, type(reg_str))
                    print("id:", bl_rule_id, type(bl_rule_id))
                    pattern = re.compile(reg_str)  # 编译正则表达式
                    mark = pattern.match(lineStr)  # 匹配
                    print("mark:", mark)
                    if mark:  # 如果不匹配mark = None,匹配才说明是空行，这行代码形式不规范
                        sql_err = "select ErrorID from error where Name = '%s'and RuleID = '%d' and RuleTypeID" \
                                  "= '%d'and Line = '%d'and FileID = '%s'" \
                                  % (pymysql.escape_string(file_name),
                                     bl_rule_id,
                                     2,
                                     pos + 1,
                                     current_file_id)
                        response0 = self.mysqlConnOperation.select_one(sql_err)
                        if response0:  # 错误已经被记录
                            print('没有空行错误')
                            if response0[0] not in ErrorID_record:
                                ErrorID_record.append(response0[0])
                                print("ErrorId_record:", ErrorID_record)
                                # 更新错误行代码
                                update_sql = "update error set error.WrongCode = '%s' where error.ErrorID = '%s'" \
                                             % (pymysql.escape_string(str(lineStr)), int(response0[0]))
                                self.mysqlConnOperation.update(update_sql)
                        else:  # 错误未被记录
                            # 插入错误行信息
                            sql_insert_1 = "insert into error (Name, RuleID, RuleTypeID, Line, WrongCode,FileID)" \
                                           " values('%s', '%s', '%s', '%s', '%s','%s')" % \
                                           (pymysql.escape_string(file_name),
                                            bl_rule_id,
                                            2,
                                            pos + 1,
                                            pymysql.escape_string(str(lineStr)),
                                            current_file_id)
                            '''该规则在许可列表里才允许插入'''
                            if int(blankLineResponse[0]) in self.rulePermissionList:
                                self.mysqlConnOperation.insert(sql_insert_1)
                    else:  # 不是空行
                        pass
                else:  # 规则不存在
                    pass
            newText_list.append(newlineStr)
            currentPos = pos + 1
            if newlineStr == lineStr:
                print('缩进正确,当前行号：', currentPos)
            else:  # 缩进不正确
                # 存储错误行缩进等级
                record_align_spaceNum[currentPos] = indent_class
                select_sql = "select ErrorID from error where RuleTypeID='%s' and Line = '%s' and FileID = '%s'" \
                             % (4, currentPos, current_file_id)
                response = self.mysqlConnOperation.select_one(select_sql)
                if response:  # 错误已经存在
                    if response[0] not in ErrorID_record:
                        ErrorID_record.append(response[0])
                        print("ErrorId_record:", ErrorID_record)
                        # 更新错误行代码
                        update_sql = "update error set error.WrongCode = '%s' where error.ErrorID = '%s'" \
                                     % (pymysql.escape_string(str(lineStr)), int(response[0]))
                        self.mysqlConnOperation.update(update_sql)
                else:
                    # 查找规则id
                    sql_select_ruleId = "select RuleID from rule where RuleTypeID = 4 and WordID = 82"
                    tup_rule_id = self.mysqlConnOperation.select_one(sql_select_ruleId)
                    # 插入错误行信息
                    sql_insert = "insert into error (Name, RuleID, RuleTypeID, Line, WrongCode,FileID)" \
                                 " values('%s', '%s', '%s', '%s', '%s','%s')" % \
                                 (pymysql.escape_string(file_name),
                                  int(tup_rule_id[0]),
                                  4,
                                  currentPos,
                                  pymysql.escape_string(str(lineStr)),
                                  current_file_id)
                    '''如果该规则在许可列表里，则执行插入'''
                    if int(tup_rule_id[0]) in self.rulePermissionList:
                        self.mysqlConnOperation.insert(sql_insert)
            pos += 1
        print('\nsuojinright:-------------------------------------------------------------------------------')
        for i in range(len(newText_list)):
            print(newText_list[i], end='')
        print('\nyuanlai:++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        for i in range(len(text_list)):
            print(text_list[i], end='')

        return newText_list, space

    # 生成正确代码
    def produce_right(self, newAlignCodePara, spacePara):
        """
        1.查找错误表中当前文件下所有corrected='否'的错误信息，主要查找规则id与行号，返回元组
        2.根据规则id与相应的行号进行改正
        目前只有五类规则：5个列表存储
        1.注释 commentList = []
        2.空行 blankLine = []
        3.代码行 codeLine = []
        4.对齐 用现成的代码文件列表，从缩进函数传进来
        5.空格  spaceLine = []
        对于一行拆成多行以及添加新行的情况，将新增加的行直接添加到当前字符串里没有问题，就是字符型长一点
        ################################################[]()'规则中还没有录入#######################
        :return:
        """
        spaceLine_1 = [',', '=', '&', '-', '/', '%', '==', '!=', '>', '<', '>=', '<=', '&&', '||', '~', '>>', '<<',
                       '-=', '/=', '%=', '<<=', '>>=', '&=', '|=']
        # 需要//转义
        spaceLine_2 = ['|', '?', '+', '*', '^', '+=', '*=', '^=']
        # 3.代码行 codeLine = []
        codeLine_1 = ['return', 'sizeof']
        codeLine_2 = ['{', '}', ';']
        global current_file_id, glo_file_path
        sql_select = "select error.Line, error.RuleID, error.RuleTypeID,rule.Express,word.WordName from error left join rule on error.RuleID = rule.RuleID " \
                     "left join word on rule.WordID = word.WorID where error.Corrected = '否' and error.FileID = '%s'" % current_file_id
        response, descri = self.mysqlConnOperation.select_all(sql_select)
        print('produce_right:------------->', response)

        newAlignCodeList_beforeChange = newAlignCodePara[:]
        newAlignCodeList = newAlignCodePara[:]  # 缩进正确的代码行列表 ,用[:]开辟新的地址
        alignSpace = spacePara  # 每一级缩进空格数目
        # with open(glo_file_path, mode='r', encoding='utf8') as f:
        #     line_list = f.readlines()
        length_response = len(response)
        for i in range(length_response):
            tupContent = response[i]  # 获得第 i 个元组
            lineNum = tupContent[0]  # 行号
            ruleNum = tupContent[1]  # 规则编号
            keyWordName = str(tupContent[4])  # 获得关键词字符串
            print('now----------------------------now:', ruleNum, 'linenum:', lineNum, keyWordName)
            newlineStr = ''
            if tupContent[2] == 5:  # 规则类型为5：空格
                '''根据规则中的正则表达式判断不行，自己根据wordname拼接字符串成为正则表达式比较可行'''
                if keyWordName in spaceLine_1:
                    regExpStr = '[ ]*' + keyWordName + '[ ]*'
                    replaceStr = ' ' + keyWordName + ' '
                    pattern = re.compile(regExpStr)
                    newlineStr = pattern.sub(replaceStr, newAlignCodeList[lineNum - 1])
                    newAlignCodeList[lineNum - 1] = newlineStr
                elif keyWordName in spaceLine_2:
                    regExpStr = '[ ]*\\' + keyWordName + '[ ]*'
                    replaceStr = ' ' + keyWordName + ' '
                    pattern = re.compile(regExpStr)
                    newlineStr = pattern.sub(replaceStr, newAlignCodeList[lineNum - 1])
                    newAlignCodeList[lineNum - 1] = newlineStr
                elif keyWordName == '++' or keyWordName == '--':
                    pass
                elif keyWordName == '!':
                    regExpStr = '[ ]*![ ]*'
                    replaceStr = '[ ]!'
                    pattern = re.compile(regExpStr)
                    newlineStr = pattern.sub(replaceStr, newAlignCodeList[lineNum - 1])
                    newAlignCodeList[lineNum - 1] = newlineStr
                else:
                    pass
            elif tupContent[2] == 3:  # 规则类型3：代码行
                if keyWordName in codeLine_1:  # return\sizeof
                    regExpStr = keyWordName + '[ ]*([a-zA-Z_]+)'
                    replaceStr = keyWordName + '(' + '\\1' + ')'
                    pattern = re.compile(regExpStr)
                    newlineStr = pattern.sub(replaceStr, newAlignCodeList[lineNum - 1])
                    newAlignCodeList[lineNum - 1] = newlineStr
                elif keyWordName in codeLine_2:  # {\}\;   错误情况只有这种没有单独一行的情况  for(){  ，{没有单独在一行
                    if keyWordName == '{':
                        regExpStr = '^([ ]*)' + '(.*)' + '\\' + keyWordName + '[ ]*([\\S]*).*'
                        replaceStr = '\\1' + '\\2' + '\n' + '\\1' + keyWordName + '\n'
                        pattern = re.compile(regExpStr)
                        newlineStr = pattern.sub(replaceStr, newAlignCodeList[lineNum - 1])
                        # 获取缩进空格字符串blankNum
                        countStr = '\\1'
                        blankNumStr = pattern.sub(countStr, newAlignCodeList[lineNum - 1])
                        reg = '^.*\\{[ ]*([^ ]+.*)$'
                        p1 = re.compile(reg)
                        mark = p1.match(newAlignCodeList[lineNum - 1])
                        if mark:  # 匹配 说明{后面有非空字符串 for(){ dfdf
                            jj = p1.sub('\\1', newAlignCodeList[lineNum - 1])
                            newlineStr = newlineStr + ' ' * alignSpace + blankNumStr + jj
                            newAlignCodeList[lineNum - 1] = newlineStr
                    elif keyWordName == '}':  # interesting} 此时整体语句缩进正确，也就是说只需要把interesting再缩进一级就是规范形式
                        regExpStr = '^([ ]*)' + '(.*)' + '\\' + keyWordName + '[ ]*([\\S]*).*'
                        replaceStr = ' ' * alignSpace + '\\1' + '\\2' + '\n' + '\\1' + keyWordName + '\n'
                        pattern = re.compile(regExpStr)
                        newlineStr = pattern.sub(replaceStr, newAlignCodeList[lineNum - 1])
                        newAlignCodeList[lineNum - 1] = newlineStr
                    else:  # ;
                        regExpStr_0 = '^([ ]*)' + '(.*)' + keyWordName + '[ ]*([\\S]*).*'
                        pattern_0 = re.compile(regExpStr_0)
                        countStr = '\\1'
                        blankNum = pattern_0.sub(countStr, newAlignCodeList[lineNum - 1])
                        regExpStr = ';'
                        pattern = re.compile(regExpStr)
                        lineStrRstrip = newAlignCodeList[lineNum - 1].rstrip()
                        if lineStrRstrip[-1] == ';':  # 如果;在最后，那么只需要添加换行符'\n'
                            replaceStr = keyWordName + '\n'
                        else:
                            replaceStr = keyWordName + '\n' + blankNum
                        newlineStr = pattern.sub(replaceStr, newAlignCodeList[lineNum - 1])
                        newAlignCodeList[lineNum - 1] = newlineStr

            elif tupContent[2] == 1:  # 规则类型1:注释
                '''
                函数注释：
                /*
                Function: // 函数名称
                Description: // 函数功能、性能等的描述
                Calls: // 被本函数调用的函数清单
                Called By: // 调用本函数的函数清单
                Input: // 输入参数说明，包括每个参数的作用、取值说明及参数间关系。
                Output: // 对输出参数的说明。
                Return: // 函数返回值的说明
                Others: // 其它说明
                */
                '''
                headStr = '/*' \
                          '\nFunction: // 函数名称 ' \
                          '\nDescription: // 函数功能、性能等的描述 ' \
                          '\nCalls: // 被本函数调用的函数清单' \
                          '\nCalled By: // 调用本函数的函数清单' \
                          '\nInput: // 输入参数说明，包括每个参数的作用、取值说明及参数间关系。' \
                          '\nOutput: // 对输出参数的说明。' \
                          '\nReturn: // 函数返回值的说明' \
                          '\nOthers: // 其它说明' \
                          '\n*/\n'
                newlineStr = headStr + newAlignCodeList[lineNum - 1]
                newAlignCodeList[lineNum - 1] = newlineStr
                print('newlinestr:', newlineStr)
            elif tupContent[2] == 2:  # 规则类型2：空行
                newAlignCodeList[lineNum - 1] = '-1'
            else:
                pass
            # newAlignCodeList[lineNum - 1] = newlineStr
        print('正确代码：')
        global rightCodeList, r1
        # ----------------------------------------------6.9
        rightCodeList = newAlignCodeList
        r1 = newAlignCodeList_beforeChange
        for i in range(len(newAlignCodeList)):
            if newAlignCodeList[i] != '-1':
                print(newAlignCodeList[i], end='')
            else:
                pass
