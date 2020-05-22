# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'analyzeCompare.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(878, 619)
        Form.setToolTip("")
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("微软雅黑 Light")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)
        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 1, 0, 1, 1)
        self.line = QtWidgets.QFrame(Form)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 1, 1, 1, 1)
        self.textBrowser_2 = QtWidgets.QTextBrowser(Form)
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.gridLayout.addWidget(self.textBrowser_2, 1, 2, 1, 1)
        self.label = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("微软雅黑 Light")
        font.setPointSize(12)
        # ------------------------------------------------------
        self.textBrowser.setFont(font)
        self.textBrowser_2.setFont(font)
        # ------------------------------------------------------
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setWordWrap(False)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "对比分析"))
        self.label_2.setText(_translate("Form", "                                    正确格式"))
        self.label.setText(_translate("Form", "                                 当前代码文件"))
