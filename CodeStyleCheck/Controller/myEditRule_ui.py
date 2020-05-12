#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2020/5/3 15:56
# @Author : yachao_lin
# @File : myEditRule_ui.py
import sys
from functools import partial

import pymysql
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QFrame, QTableWidgetItem, QApplication, QHeaderView, QMessageBox, QItemDelegate, \
    QAbstractItemView

from CodeStyleCheck.GUI.edit_rule import Ui_Form
from CodeStyleCheck.model.mydb import MysqlOperation

flag_ok = False   # 一个标志，用于防止多次重复提交


class EmptyDelegate(QItemDelegate):
    def __init__(self, parent):
        super(EmptyDelegate, self).__init__(parent)

    def createEditor(self, QWidget, QStyleOptionViewItem, QModelIndex):
        return None


class MyEditRule(QWidget, Ui_Form):
    def __init__(self):
        super(MyEditRule, self).__init__()
        self.setupUi(self)
        self.ConnMysql = MysqlOperation("localhost", "root", "123456", "cstyle_db")
        self.initUI()
        sql = "SELECT * FROM rule"
        # descr存储数据库表列名
        data, descr = self.ConnMysql.select_all(sql)
        # 数据列名
        # col_name = [tup[0] for tup in descr]
        col_name = ['规则编号', '规则名称', '规则表示', '建议', '标准', '规则类型ID', '关键字ID']
        # 表格行数与列数
        row = len(data)
        vol = len(data[0])
        # 插入表格
        self.tableWidget.setRowCount(row)
        self.tableWidget.setColumnCount(vol)
        # 第一列不可编辑
        self.tableWidget.setItemDelegateForColumn(0, EmptyDelegate(self))
        # 设置字体、表头
        font = QtGui.QFont("微软雅黑", 10)
        self.tableWidget.horizontalHeader().setFont(font)
        self.tableWidget.setHorizontalHeaderLabels(col_name)
        # 设置表头自适应窗口伸缩
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 设置竖直方向表头不可见
        self.tableWidget.verticalHeader().setVisible(True)  # 可见
        self.tableWidget.setFrameShape(QFrame.NoFrame)
        # 设置表格颜色
        self.tableWidget.horizontalHeader().setStyleSheet('QHeaderView::section{background:skyblue}')
        '''构建表格插入数据'''
        for i in range(row):
            for j in range(vol):
                temp_data = data[i][j]
                data0 = QTableWidgetItem(str(temp_data))
                self.tableWidget.setItem(i, j, data0)

        self.NewRule_pushButton.clicked.connect(partial(self.add_data, col_name))
        self.pushButton.clicked.connect(partial(self.ok_data, col_name))

    def initUI(self):
        self.lineEdit.setPlaceholderText("模糊查询：请输入规则名称中的一个关键字!")
        self.View_pushButton_2.clicked.connect(self.view_data)
        self.Del_pushButton.clicked.connect(self.del_data)
        self.pushButton_2.clicked.connect(self.up_data)
        self.ruleType_init()
        self.word_init()

    # 增加一行
    def add_data(self, col_name):
        row = self.tableWidget.rowCount()
        print(row)
        self.tableWidget.insertRow(row)
        temp_data = row+1
        data0 = QTableWidgetItem(str(temp_data))
        self.tableWidget.setItem(row, 0, data0)
        global flag_ok
        flag_ok = True   # 置该标记为True,表示可以执行提交操作，否则提交按钮锁定

    def ok_data(self, col_name):
        row = self.tableWidget.rowCount()
        print(row)
        print(len(col_name))
        val_lst = []
        try:
            for i in range(len(col_name)):
                if len(self.tableWidget.item(row - 1, i).text()) == 0:
                    val_lst.append(-1)
                else:
                    val_lst.append(self.tableWidget.item(row - 1, i).text())
        except Exception as e:
            print(e)
            print('新插入行中输入信息不完整导致报错!')
        print(val_lst)
        print(len(val_lst))
        if len(val_lst) != len(col_name):
            QMessageBox.warning(self, '提醒', '新插入行输入信息不全!\n请重新输入!')
        else:
            global flag_ok
            if flag_ok:
                sql = "insert into rule(name, express, advice, standard, ruletypeid, wordid) VALUES" \
                      "('%s', '%s', '%s', '%s', '%s','%s')" % (val_lst[1], val_lst[2], val_lst[3], val_lst[4],
                                                               val_lst[5], val_lst[6])
                self.ConnMysql.insert(sql)
                flag_ok = False

    def view_data(self):
        txt = self.lineEdit.text()
        # 模糊查询
        if 0 != len(txt):
            sql = "select * from rule where rule.Name like '%" + pymysql.escape_string(txt) + "%'"
            data, description = self.ConnMysql.select_all(sql)
            self.tableWidget.clearContents()
            row = len(data)
            vol = len(description)
            # 重新设置行号与列号
            self.tableWidget.setRowCount(row)
            self.tableWidget.setColumnCount(vol)
            # 查询到内容，更新显示表格
            for i_row in range(row):
                for j_col in range(vol):
                    temp_data = data[i_row][j_col]  # 临时数据，不能直接插入表格
                    tabData = QTableWidgetItem(str(temp_data))  # 转换后才可以插入表格
                    self.tableWidget.setItem(i_row, j_col, tabData)
        # 查询不到，返回原来表格
        else:
            self.tableWidget.clearContents()
            sql_1 = "SELECT * FROM rule"
            # descr存储数据库表列名
            data_1, descr = self.ConnMysql.select_all(sql_1)
            # 数据列名
            col_name = ['规则编号', '规则名称', '规则表示', '建议', '标准', '规则类型ID', '关键字ID']
            # 表格行数与列数
            row_1 = len(data_1)
            vol_1 = len(data_1[0])
            for i in range(row_1):
                for j in range(vol_1):
                    temp_data = data_1[i][j]
                    data0 = QTableWidgetItem(str(temp_data))
                    self.tableWidget.setItem(i, j, data0)

    def del_data(self):
        # 是否删除的对话框
        reply = QMessageBox.question(self, '提示', '确定删除该行信息吗?', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            # 当前行
            row = self.tableWidget.currentRow()
            print(row)
            # del_d = self.tableWidget.item(row, 0).text()
            # print(del_d)
            lst = []
            for i in range(7):
                lst.append(self.tableWidget.item(row, i).text())
            print('lst:', lst)
            # 在数据库删除数据
            sql = "delete from rule where RuleID = '%s' and Name = '%s'and Express = '%s'and Advice = '%s'" \
                  "and Standard = '%s' and RuleTypeID = '%s'and WordID = '%s'" % (lst[0], lst[1], lst[2],
                                                                                  lst[3], lst[4], lst[5],
                                                                                  lst[6])
            self.ConnMysql.delete(sql)
            # 删除表格
            self.tableWidget.removeRow(row)

    def up_data(self):
        """更新某一行数据"""
        # 当前行
        try:
            row_1 = self.tableWidget.currentRow()
            print(row_1)
            del_d = [self.tableWidget.item(row_1, i).text() for i in range(7)]
            print(del_d)
            # 在数据库删除数据
            sql = "update rule set rule.Name = '%s',rule.Express = '%s', rule.Advice = '%s', rule.Standard = '%s'," \
                  "rule.RuleTypeID = '%s', rule.WordID = '%s' where rule.RuleID= '%s'" % \
                  (pymysql.escape_string(del_d[1]),
                   pymysql.escape_string(del_d[2]),
                   pymysql.escape_string(del_d[3]),
                   del_d[4], del_d[5], del_d[6],
                   pymysql.escape_string(del_d[0]))
            self.ConnMysql.update(sql)
        except Exception as e:
            print(e)
            print('当前行号为-1')
        '''更新整个表格'''
        sql = "SELECT * FROM rule"
        # descr存储数据库表列名
        data, descr = self.ConnMysql.select_all(sql)
        # 数据列名
        # 表格行数与列数
        row = len(data)
        vol = len(data[0])
        # 插入表格
        self.tableWidget.setRowCount(row)
        self.tableWidget.setColumnCount(vol)
        '''构建表格插入数据'''
        for i in range(row):
            for j in range(vol):
                temp_data = data[i][j]
                data0 = QTableWidgetItem(str(temp_data))
                self.tableWidget.setItem(i, j, data0)

    def ruleType_init(self):
        sql = "SELECT * FROM ruletype"
        # descr存储数据库表列名
        data, descr = self.ConnMysql.select_all(sql)
        # 数据列名
        # col_name = [tup[0] for tup in descr]
        col_name = ['规则类型编号', '规则类型名称']
        # 表格行数与列数
        row = len(data)
        vol = len(data[0])
        # 插入表格 不可编辑
        self.tableWidget_2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget_2.setRowCount(row)
        self.tableWidget_2.setColumnCount(vol)
        self.tableWidget_2.setItemDelegateForColumn(0, EmptyDelegate(self))
        # 设置字体、表头
        font = QtGui.QFont("微软雅黑", 10)
        self.tableWidget_2.horizontalHeader().setFont(font)
        self.tableWidget_2.setHorizontalHeaderLabels(col_name)
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 设置竖直方向表头不可见
        self.tableWidget_2.verticalHeader().setVisible(True)  # 可见
        self.tableWidget_2.setFrameShape(QFrame.NoFrame)
        # 设置表格颜色
        self.tableWidget_2.horizontalHeader().setStyleSheet('QHeaderView::section{background:skyblue}')
        '''构建表格插入数据'''
        for i in range(row):
            for j in range(vol):
                temp_data = data[i][j]
                data0 = QTableWidgetItem(str(temp_data))
                self.tableWidget_2.setItem(i, j, data0)

    def word_init(self):
        sql = "SELECT * FROM word"
        # descr存储数据库表列名
        data, descr = self.ConnMysql.select_all(sql)
        # 数据列名
        # col_name = [tup[0] for tup in descr]
        col_name = ['规则类型编号', '规则类型名称']
        # 表格行数与列数
        row = len(data)
        vol = len(data[0])
        # 插入表格,不可编辑
        self.tableWidget_3.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget_3.setRowCount(row)
        self.tableWidget_3.setColumnCount(vol)
        self.tableWidget_3.setItemDelegateForColumn(0, EmptyDelegate(self))
        # 设置字体、表头
        font = QtGui.QFont("微软雅黑", 10)
        self.tableWidget_3.horizontalHeader().setFont(font)
        self.tableWidget_3.setHorizontalHeaderLabels(col_name)
        self.tableWidget_3.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 设置竖直方向表头不可见
        self.tableWidget_3.verticalHeader().setVisible(True)  # 可见
        self.tableWidget_3.setFrameShape(QFrame.NoFrame)
        # 设置表格颜色
        self.tableWidget_3.horizontalHeader().setStyleSheet('QHeaderView::section{background:skyblue}')
        '''构建表格插入数据'''
        for i in range(row):
            for j in range(vol):
                temp_data = data[i][j]
                data0 = QTableWidgetItem(str(temp_data))
                self.tableWidget_3.setItem(i, j, data0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MyEditRule()
    ui.show()
    sys.exit(app.exec_())
