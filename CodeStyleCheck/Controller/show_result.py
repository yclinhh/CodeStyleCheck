#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2020/5/10 21:10
# @Author : yachao_lin
# @File : show_result.py
import sys

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QFrame, QHeaderView, QAbstractItemView, QApplication

from CodeStyleCheck.GUI.RewriteTableWidget import MyTableWidget
from CodeStyleCheck.model.mydb import MysqlOperation

fileId = -1
stuId = -1


# class MyResult(Ui_Form, QWidget):
class MyResult(QWidget):

    def __init__(self):
        super(MyResult, self).__init__()
        # self.setupUi(self)
        self.ConnMysqlOne = MysqlOperation("localhost", "root", "123456", "cstyle_db")
        self.initLayout()
        # self.initUI()  #-----------注意，下面还有一个initUI,这个最后要删除

    #  处理接收到的信号
    def deal_showResult_emit_slot(self, FileId, StuID):
        global fileId, stuId
        fileId = FileId
        stuId = StuID
        print('成功接收信号--------------------', fileId, stuId)
        self.initUI()

    # 初始化当前页面布局，表格等。
    def initLayout(self):
        self.tableWidget = MyTableWidget()
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.setWindowTitle("错误信息表")
        self.setObjectName("错误信息表")
        self.resize(782, 603)
        self.gridLayout.setObjectName("gridLayout")
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget, 0, 0, 1, 1)
        self.tableWidget.install_eventFilter()

    # 初始化表格
    def initUI(self):
        global fileId, stuId
        sql = "select  error.Name, rule.Name,rule.Advice, ruletype.Name, error.Line, error.WrongCode, error.Corrected" \
              " from error left join rule on error.RuleID = rule.RuleID left join ruletype on " \
              "error.RuleTypeID = ruletype.RuleTypeID left join code c on error.FileID = c.CodeID" \
              " where c.CodeID = '%s' and c.StudentID = '%s'order by error.Line " % (
                  fileId, stuId)
        # descr存储数据库表列名
        data, descr = self.ConnMysqlOne.select_all(sql)
        # 数据列名
        # col_name = [tup[0] for tup in descr]
        col_name = ['文件名称', '规则名称', '建议', '规则类型', '行号', '错误代码', '是否改正']
        # 表格行数与列数
        row = len(data)
        vol = len(col_name)
        # 插入表格
        self.tableWidget.setRowCount(row)
        self.tableWidget.setColumnCount(vol)
        # 设置字体、表头
        font = QtGui.QFont("微软雅黑", 10)
        self.tableWidget.horizontalHeader().setFont(font)
        self.tableWidget.setHorizontalHeaderLabels(col_name)
        print('****************', self.tableWidget.horizontalHeader().height())
        # 行列根据窗口自适应调整
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 单元格根据内容调整行列大小
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()
        # 表格不可编辑
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 设置竖直方向表头不可见
        self.tableWidget.verticalHeader().setVisible(True)  # 可见
        self.tableWidget.setFrameShape(QFrame.NoFrame)
        # 设置表头颜色
        self.tableWidget.horizontalHeader().setStyleSheet('QHeaderView::section{background:skyblue}')
        '''构建表格插入数据'''
        for i in range(row):
            for j in range(vol):
                temp_data = data[i][j]
                data0 = QTableWidgetItem(str(temp_data))
                self.tableWidget.setItem(i, j, data0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MyResult()
    ui.show()
    sys.exit(app.exec_())
