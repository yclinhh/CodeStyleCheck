# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'edit_rule.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(722, 500)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.NewRule_pushButton = QtWidgets.QPushButton(Form)
        self.NewRule_pushButton.setObjectName("NewRule_pushButton")
        self.gridLayout.addWidget(self.NewRule_pushButton, 2, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 0, 1, 2)
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget, 3, 0, 1, 4)
        self.View_pushButton_2 = QtWidgets.QPushButton(Form)
        self.View_pushButton_2.setObjectName("View_pushButton_2")
        self.gridLayout.addWidget(self.View_pushButton_2, 2, 3, 1, 1)
        self.Del_pushButton = QtWidgets.QPushButton(Form)
        self.Del_pushButton.setObjectName("Del_pushButton")
        self.gridLayout.addWidget(self.Del_pushButton, 2, 2, 1, 1)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 2, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.NewRule_pushButton.setText(_translate("Form", "新建规则"))
        self.View_pushButton_2.setText(_translate("Form", "查询规则"))
        self.Del_pushButton.setText(_translate("Form", "删除规则"))
        self.pushButton.setText(_translate("Form", "提交"))
