#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2020/5/22 15:37
# @Author : yachao_lin
# @File : show_configRule.py
import sys
import traceback
from functools import partial

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QItemDelegate, QHeaderView, QFrame, QTableWidgetItem, QApplication

from CodeStyleCheck.GUI.configRule import Ui_Form
from CodeStyleCheck.model.mydb import MysqlOperation


# 设置一个代理，返回空editor
class EmptyDelegate(QItemDelegate):
    def __init__(self, parent):
        super(EmptyDelegate, self).__init__(parent)

    def createEditor(self, QWidget, QStyleOptionViewItem, QModelIndex):
        return None


class MyConfigRule(QWidget, Ui_Form):
    transmitRuleSignal = pyqtSignal(list)  # 传递已经选择的规则编号给主窗口

    def __init__(self):
        super(MyConfigRule, self).__init__()
        self.setupUi(self)
        self.initUi()
        self.ConnMysql = MysqlOperation("localhost", "root", "123456", "cstyle_db")
        self.chBox_list = []  # 保存复选框
        self.choseRuleId = []  # 保存选择的ruleid
        # 设置第1,2，3，4列不可编辑
        self.tableWidget.setItemDelegateForColumn(1, EmptyDelegate(self))
        self.tableWidget.setItemDelegateForColumn(2, EmptyDelegate(self))
        self.tableWidget.setItemDelegateForColumn(3, EmptyDelegate(self))
        self.tableWidget.setItemDelegateForColumn(4, EmptyDelegate(self))
        # 设置字体、表头
        sql_rule = "SELECT r2.Name, r.Name, w.WordName, r.RuleID FROM rule r left join word w on r.WordID = w.WorID " \
                   "left join ruletype r2 on r.RuleTypeID = r2.RuleTypeID order by r2.Name"
        # descr存储数据库表列名
        data, descr = self.ConnMysql.select_all(sql_rule)
        # 数据列名
        col_name = ['选择', '规则类型', '规则名称', '关键字', '规则编号']
        # 表格行数与列数
        row = len(data)
        vol = len(data[0])
        # 设置表格行号与列号
        self.tableWidget.setRowCount(row)
        self.tableWidget.setColumnCount(vol + 1)  # 多设立一列用于插入复选框
        # 第一列不可编辑
        # self.tableWidget.setItemDelegateForColumn(0, EmptyDelegate(self))
        # 设置字体、表头
        font = QtGui.QFont("微软雅黑", 10)
        self.tableWidget.horizontalHeader().setFont(font)
        self.tableWidget.setHorizontalHeaderLabels(col_name)
        # 设置表头自适应窗口伸缩
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setFrameShape(QFrame.NoFrame)
        # 重新设置前两列列宽
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)
        self.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Interactive)
        self.tableWidget.setColumnWidth(0, 100)  # 设置第0列列宽
        self.tableWidget.setColumnWidth(1, 100)
        # 设置表头颜色
        self.tableWidget.horizontalHeader().setStyleSheet('QHeaderView::section{background:skyblue}')
        if data:  # 规则表不为空
            try:
                for i in range(row):
                    for j in range(vol):
                        temp = str(data[i][j])  # 获得一项数据
                        temp_data = QTableWidgetItem(str(temp))  # 转化成表格类型才能显示,temp必须为字符串类型，否则不显示
                        temp_data.setTextAlignment(Qt.AlignCenter)  # 居中显示
                        self.tableWidget.setItem(i, j + 1, temp_data)  # 添加到表格中
                        if j == 0:  # 添加复选框
                            chBox = QtWidgets.QCheckBox('')
                            chBox.stateChanged.connect(lambda checked, row1=i: self.onStateChanged(checked, row1))
                            self.tableWidget.setCellWidget(i, j, chBox)
                            self.chBox_list.append(chBox)
                        if j == 5:
                            self.tableWidget.item(i, j).setBackground(QtGui.QColor(97, 215, 97))
                        elif data[i][0] == '注释':
                            self.tableWidget.item(i, 1).setBackground(QtGui.QColor(240, 240, 240))
                        elif data[i][0] == '代码行':
                            self.tableWidget.item(i, 1).setBackground(QtGui.QColor(240, 240, 240))
                        else:
                            pass
            except Exception as e:
                print(e)
            finally:
                self.btn_selectAll()  # 默认全选
                print("默认全选状态：", self.choseRuleId)
                self.transmitRuleSignal.emit(self.choseRuleId)
        else:  # 规则表为空，不添加复选框控件
            pass

    def initUi(self):
        self.pushButton.clicked.connect(self.btn_ok)
        self.pushButton_2.clicked.connect(self.btn_cancel)
        self.pushButton_3.clicked.connect(self.btn_selectAll)
        self.pushButton_4.clicked.connect(self.btn_cancelAll)

    def onStateChanged(self, checked, row):
        stateFlag = checked
        rowNum = int(row)
        itemRuleId = int(self.tableWidget.item(rowNum, 4).text())  # 获得选中行的ruleid
        if stateFlag:  # 选中状态
            if itemRuleId not in self.choseRuleId:
                self.choseRuleId.append(itemRuleId)
                self.chBox_list[rowNum].setText('规则{0}已选中'.format(itemRuleId))
        else:  # 未选中
            if itemRuleId in self.choseRuleId:
                self.choseRuleId.remove(int(itemRuleId))
                self.chBox_list[rowNum].setText('')
        print('后：', end='')
        print('\n')
        labelStr = ''
        for i in range(len(self.choseRuleId)):
            print(self.choseRuleId[i], end=' ')
        self.label.setText('您目前选择了{0}条规则'.format(len(self.choseRuleId)))
        print('\n')

    def emit_transmitRuleSignal(self):
        """
        发送信号
        :return:
        """
        self.transmitRuleSignal.emit(self.choseRuleId)

    def btn_ok(self):
        self.emit_transmitRuleSignal()
        self.close()

    def btn_cancel(self):
        self.close()

    def btn_selectAll(self):
        """
        一键全选
        :return:
        """
        for i in range(len(self.chBox_list)):
            self.chBox_list[i].setChecked(True)  # 设置选中
        self.label.setText('您选择了全部规则，一共{0}条规则。'.format(len(self.choseRuleId)))

    def btn_cancelAll(self):
        """
        一键全部取消
        :return:
        """
        for i in range(len(self.chBox_list)):
            self.chBox_list[i].setChecked(False)  # 设置bu选中
        self.label.setText('您没有选择规则--')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MyConfigRule()
    ui.show()
    sys.exit(app.exec_())
