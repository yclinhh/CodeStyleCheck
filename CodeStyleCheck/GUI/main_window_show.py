#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2020/4/12 22:04
# @Author : yachao_lin
# @File : main_window_show.py
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from CodeStyleCheck.GUI.InputStuID import Ui_Dialog
from CodeStyleCheck.GUI.text_editor import QCodeEditor
from CodeStyleCheck.GUI.main_window import Ui_MainWindow
from CodeStyleCheck.model.test_regxExpre import *
from CodeStyleCheck.model.mydb import MysqlOperation

# from CodeStyleCheck.lianxi.QCodeEditor1 import QCodeEditor

glo_file_path = ""  # 全局变量存储：文件路径
record_tab = []  # 全局记录表：存储所有行的单词种别码
studentID = ''


class Login(QDialog, Ui_Dialog):
    closeSignal = pyqtSignal(str)  # 自定义信号，传递一个字符串参数

    def __init__(self):
        super().__init__()
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
            print("ok:----->", StuID)
            self.close()


class QMyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(QMyWindow, self).__init__()
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

    # # 输入学号
    # def inputInfo(self):
    #     self.dialog = Login()
    #     '''连接子窗口的自定义信号与主窗口的槽函数'''
    #     self.dialog.signalInfo.connect(self.deal_emit_slot)
    #     self.dialog.show()
    #     print("12")

    # jies
    def deal_emit_slot(self, StuID):
        self.show()
        global studentID
        studentID = ''
        studentID += StuID
        print("studentID:", studentID)


    # 代码文件加载线程
    def open_file_action_thread(self):
        pass

    # 打开代码文件
    def open_file_action(self):
        print("ok")
        # 建立一个文件对话框
        dialog = QFileDialog()
        # 设置文件模式（这里操作对象为任何文件）
        dialog.setFileMode(QFileDialog.AnyFile)
        # 设置过滤器（这里显示所有文件列表）
        dialog.setFilter(QDir.Files)
        # 打开对话框
        if dialog.exec():
            # 接受选中文件的路径，路径默认保存在列表
            file_path = dialog.selectedFiles()
            # 显示文件路径
            global glo_file_path
            glo_file_path = file_path[0]  # 获取文件路径
            print("保存文件路径：", glo_file_path)
            self.textBrowser.setPlainText(str(file_path[0]))
            try:
                # 读写方式打开文件
                with open(file_path[0], encoding='utf-8', mode='r+') as f:
                    data = f.read()
                    self.myTextEditor.appendPlainText(data)
                    self.mysqlConnOperation.connect()
                    # sql = "select * from code where FilePath = %s" % glo_file_path
                    # res = None
                    # res = self.mysqlConnOperation.select_one(sql)
                    # if res:
                    #     pass
                    # else:
                    #     sql
            except IOError as e:
                print(e)
                print("打开文件失败!")

    # 保存文件
    def save_file_action(self):
        global glo_file_path
        # if glo_file_path is not None:
        print("打印文件路径：", glo_file_path)
        try:
            with open(glo_file_path, mode='r+', encoding='utf8') as f:
                f.write(self.myTextEditor.toPlainText())
                print("保存成功！")
        except IOError as e:
            print(e)
            print("exception:glo_file_path")

    # 清屏
    def close_file_action(self):
        self.myTextEditor.selectAll()
        self.myTextEditor.clear()
        self.textBrowser.selectAll()
        self.textBrowser.clear()
        self.textBrowser_2.selectAll()
        self.textBrowser_2.clear()

    # 重写关闭事件（用函数调用它没有用）
    def closeEvent(self, event):
        reply = QMessageBox.question(self, '提示', '你确定要关闭吗？',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    # 退出
    def mainWindow_quit(self):
        sapp = QApplication.instance()
        sapp.exit()

    # 代码检查
    def code_check_action(self):
        """
        分析打开文件的代码
        :return:
        """
        global glo_file_path, record_tab
        try:
            with open(glo_file_path, mode='r', encoding='utf8') as f:
                text0 = f.read()
                record_tab = Scanner(text0)
                print(record_tab)
                self.mysql_operate()
                # for line in f:
                #     result = self.lexical_analyzer(line)
                #     self.check(result)
        except IOError as e:
            print(e)

    #        插入时没有检查是否重复
    @staticmethod
    def mysql_operate():
        """
        逐个分析单词，将分析结果保存在error数据表里
        :return:
        """
        global glo_file_path, record_tab
        db = pymysql.connect("localhost", "root", "123456", "cstyle_db")
        cursor = db.cursor()
        cursor.execute("select VERSION()")
        data = cursor.fetchall()
        print(data)
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
                    else:
                        tab = record_tab[i]
                        i_length = len(tab)  # 第i行单词表长度
                        for j in range(i_length):
                            var = tab[j]
                            # try:
                            select_sql = "select ruleid, express, ruletypeid from rule where WordID = %s" % var
                            cursor.execute(select_sql)
                            db.commit()
                            print("查询成功")
                            reg_tup = cursor.fetchall()  # 获取所有符合的正则表达式，返回一个元组
                            if reg_tup:
                                reg_str = str(list(reg_tup[0])[1])  # 元组转换为字符串
                                _ruleid = list(reg_tup[0])[0]  # 获取ruleid
                                _ruletypeid = list(reg_tup[0])[2]  # 获取ruletypeid
                                # reg_str = ''.join(reg_tup[0])   # 元组转换为字符串
                                print("reg_str:", reg_str, type(reg_str))
                                pattern = re.compile(reg_str)  # 编译正则表达式
                                print("line----->:", type(line_str), line_str)
                                mark = pattern.match(line_str)  # 匹配结果
                                if not mark:  # 如果不匹配mark = None
                                    sql_err = "select * from error where Name = '%s'and  RuleID = '%d' and RuleTypeID" \
                                              "= '%d'and Line = '%d'and WrongCode = '%s'" \
                                              % (file_name, _ruleid, _ruletypeid, int(i) + 1, str(line_str))
                                    response = cursor.execute(sql_err)
                                    db.commit()
                                    print("response:", response)
                                    if response == 1:
                                        print("数据已存在！")
                                    else:
                                        try:
                                            insert_sql = "insert into error (Name, RuleID, RuleTypeID, Line, " \
                                                         "WrongCode) values('%s', '%d', '%d', '%d', '%s')" % \
                                                         (file_name, _ruleid, _ruletypeid, int(i) + 1, str(line_str))
                                            cursor.execute(insert_sql)
                                            db.commit()
                                            print("插入成功")
                                        except Exception as e:
                                            print(e)
                                            print("插入错误")
                                            db.rollback()
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
        except IOError as e1:
            print("文件打开问题")
            print(e1)
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def check(line):
        print(line, end='')
        print(1)
        # sys.exit()

    def analyze_result(self):
        """
        查询程序分析的结果，从error数据表中查询错误信息
        :return:
        """
        global glo_file_path
        db = pymysql.connect("localhost", "root", "123456", "cstyle_db")
        cursor = db.cursor()
        list_path = glo_file_path.split('/')
        file_name = list_path[-1]  # 获取文件名
        print("list_path", list_path)
        print("textName:", file_name)
        sql = "select  error.Name, rule.Name,rule.Advice, ruletype.Name, line, wrongcode, corrected" \
              " from error left join rule on error.RuleID = rule.RuleID left join ruletype on " \
              "error.RuleTypeID = ruletype.RuleTypeID order by error.Line "
        try:
            cursor.execute(sql)
            data = cursor.fetchall()
            print("analyze_result函数查询成功！")
            print(data)
            length = len(data)
            for i in range(length):
                txt = (list(data[i]))
                print(txt)
                # for j in range(len(txt)):
                txt_str = '序号：' + str(i) + '  当前文件名称：' + str(txt[0]) + '  错误行号：第 ' + str(txt[4]) + ' 行' + \
                          '  错误代码：' + str(txt[5]) + '错误原因：' + str(txt[1]) + '  错误类型：' + str(txt[3]) + '  建议：' + str(
                    txt[2]) + '\n '
                self.textBrowser_2.append(txt_str)
        except Exception as e:
            print(e)
            print("查询失败：analyze_result函数")
        finally:
            cursor.close()
            db.close()
