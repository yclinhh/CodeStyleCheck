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
        Form.resize(785, 500)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_7 = QtWidgets.QWidget()
        self.tab_7.setObjectName("tab_7")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_7)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.lineEdit = QtWidgets.QLineEdit(self.tab_7)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_3.addWidget(self.lineEdit, 0, 0, 1, 3)
        self.NewRule_pushButton = QtWidgets.QPushButton(self.tab_7)
        self.NewRule_pushButton.setObjectName("NewRule_pushButton")
        self.gridLayout_3.addWidget(self.NewRule_pushButton, 1, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.tab_7)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_3.addWidget(self.pushButton, 1, 1, 1, 1)
        self.Del_pushButton = QtWidgets.QPushButton(self.tab_7)
        self.Del_pushButton.setObjectName("Del_pushButton")
        self.gridLayout_3.addWidget(self.Del_pushButton, 1, 2, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(self.tab_7)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout_3.addWidget(self.tableWidget, 2, 0, 1, 4)
        self.View_pushButton_2 = QtWidgets.QPushButton(self.tab_7)
        self.View_pushButton_2.setObjectName("View_pushButton_2")
        self.gridLayout_3.addWidget(self.View_pushButton_2, 0, 3, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.tab_7)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_3.addWidget(self.pushButton_2, 1, 3, 1, 1)
        self.tabWidget.addTab(self.tab_7, "")
        self.tab_8 = QtWidgets.QWidget()
        self.tab_8.setObjectName("tab_8")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab_8)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.tableWidget_2 = QtWidgets.QTableWidget(self.tab_8)
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(0)
        self.tableWidget_2.setRowCount(0)
        self.gridLayout_4.addWidget(self.tableWidget_2, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_8, "")
        self.tab_9 = QtWidgets.QWidget()
        self.tab_9.setObjectName("tab_9")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.tab_9)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.tableWidget_3 = QtWidgets.QTableWidget(self.tab_9)
        self.tableWidget_3.setObjectName("tableWidget_3")
        self.tableWidget_3.setColumnCount(0)
        self.tableWidget_3.setRowCount(0)
        self.gridLayout_5.addWidget(self.tableWidget_3, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_9, "")
        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.NewRule_pushButton.setText(_translate("Form", "新建"))
        self.pushButton.setText(_translate("Form", "提交"))
        self.Del_pushButton.setText(_translate("Form", "删除规则"))
        self.View_pushButton_2.setText(_translate("Form", "查询规则"))
        self.pushButton_2.setText(_translate("Form", "更新规则"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_7), _translate("Form", "编辑规则"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_8), _translate("Form", "关键字表信息"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_9), _translate("Form", "规则类型表信息"))
