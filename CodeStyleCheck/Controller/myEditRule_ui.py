#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2020/5/3 15:56
# @Author : yachao_lin
# @File : myEditRule_ui.py
import sys

from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QFrame, QTableWidgetItem, QApplication

from CodeStyleCheck.GUI.edit_rule import Ui_Form
from CodeStyleCheck.model.mydb import MysqlOperation


class MyEditRule(QWidget, Ui_Form):
    def __init__(self):
        super(MyEditRule, self).__init__()
        self.setupUi(self)
        self.ConnMysql = MysqlOperation("localhost", "root", "123456", "cstyle_db")
        self.initUI()
        sql = "SELECT * FROM rule"
        data, descr = self.ConnMysql.select_all(sql)
        # 数据列名
        col_lst = [tup[0] for tup in descr]
        # 表格行数与列数
        row = len(data)
        vol = len(data[0])
        # 插入表格
        self.tableWidget.setRowCount(row)
        self.tableWidget.setColumnCount(vol)
        # 设置字体、表头
        font = QtGui.QFont("微软雅黑", 10)
        self.tableWidget.horizontalHeader().setFont(font)
        self.tableWidget.setHorizontalHeaderLabels(col_lst)
        # 设置竖直方向表头不可见
        self.tableWidget.verticalHeader().setVisible(True)
        self.tableWidget.setFrameShape(QFrame.NoFrame)
        # 设置表格颜色
        self.tableWidget.horizontalHeader().setStyleSheet('QHeaderView::section{background:skyblue}')
        '''构建表格插入数据'''
        for i in range(row):
            for j in range(vol):
                temp_data = data[i][j]
                data0 = QTableWidgetItem(str(temp_data))
                self.tableWidget.setItem(i, j, data0)



    def initUI(self):
        self.NewRule_pushButton.clicked.connect(self.add_data)
        self.pushButton.clicked.connect(self.ok_data)
        self.View_pushButton_2.clicked.connect(self.view_data)
        self.Del_pushButton.clicked.connect(self.del_data)

    def add_data(self):
        pass

    def ok_data(self):
        pass

    def view_data(self):
        pass

    def del_data(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MyEditRule()
    ui.show()
    sys.exit(app.exec_())