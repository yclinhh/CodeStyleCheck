# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'showResult.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from CodeStyleCheck.GUI.RewriteTableWidget import MyTableWidget


# class Ui_Form(object):
#     def setupUi(self, Form):
#         Form.setObjectName("Form")
#         Form.resize(782, 603)
#         self.gridLayout = QtWidgets.QGridLayout(Form)
#         self.gridLayout.setObjectName("gridLayout")
#         # self.tableWidget = QtWidgets.QTableWidget(Form)
#         self.tableWidget = MyTableWidget(Form)
#         self.tableWidget.setObjectName("tableWidget")
#         self.tableWidget.setColumnCount(0)
#         self.tableWidget.setRowCount(0)
#         self.gridLayout.addWidget(self.tableWidget, 0, 0, 1, 1)
#
#         self.retranslateUi(Form)
#         QtCore.QMetaObject.connectSlotsByName(Form)
#
#     def retranslateUi(self, Form):
#         _translate = QtCore.QCoreApplication.translate
#         Form.setWindowTitle(_translate("Form", "Form"))


# 测试自定义TableWidget
class Ui_Form(QWidget):
    def __init__(self):
        super(Ui_Form, self).__init__()
        self.tableWidget = MyTableWidget()
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("错误信息表")
        self.setObjectName("错误信息表")
        self.resize(782, 603)
        self.gridLayout.setObjectName("gridLayout")
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget, 0, 0, 1, 1)
        self.tableWidget.install_eventFilter()

