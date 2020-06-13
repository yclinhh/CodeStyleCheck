# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.tab)
        self.horizontalLayout.setObjectName("horizontalLayout")


        self.textBrowser = QtWidgets.QTextBrowser(self.tab)
        self.textBrowser.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.textBrowser.setFont(font)
        self.textBrowser.setObjectName("textBrowser")
        self.horizontalLayout.addWidget(self.textBrowser)
        '''
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.tab)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.plainTextEdit.setFont(font)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.horizontalLayout.addWidget(self.plainTextEdit)
        
        '''

        self.tabWidget.addTab(self.tab, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.tabWidget_2 = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget_2.setMaximumSize(QtCore.QSize(16777215, 150))
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.tab_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")


        self.textBrowser_2 = QtWidgets.QTextBrowser(self.tab_2)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(10)
        self.textBrowser_2.setFont(font)
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.horizontalLayout_2.addWidget(self.textBrowser_2)
        self.tabWidget_2.addTab(self.tab_2, "")
        self.gridLayout.addWidget(self.tabWidget_2, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_open = QtWidgets.QAction(MainWindow)
        self.action_open.setObjectName("action_open")
        self.action_close = QtWidgets.QAction(MainWindow)
        self.action_close.setObjectName("action_close")
        self.action_quit = QtWidgets.QAction(MainWindow)
        self.action_quit.setObjectName("action_quit")
        self.action_view = QtWidgets.QAction(MainWindow)
        self.action_view.setObjectName("action_view")
        self.action_new = QtWidgets.QAction(MainWindow)
        self.action_new.setObjectName("action_new")
        self.action_edit = QtWidgets.QAction(MainWindow)
        self.action_edit.setObjectName("action_edit")
        self.action_config = QtWidgets.QAction(MainWindow)
        self.action_config.setObjectName("action_config")
        self.action_run = QtWidgets.QAction(MainWindow)
        self.action_run.setObjectName("action_run")
        self.action_result = QtWidgets.QAction(MainWindow)
        self.action_result.setObjectName("action_result")
        self.action_compare = QtWidgets.QAction(MainWindow)
        self.action_compare.setObjectName("action_compare")
        self.action_save = QtWidgets.QAction(MainWindow)
        self.action_save.setObjectName("action_save")
        # 增加一键删除文件错误信息
        self.action_deleteErrorInfo = QtWidgets.QAction(MainWindow)
        self.action_deleteErrorInfo.setObjectName("action_deleteErrorInfo")

        self.menu.addAction(self.action_open)
        self.menu.addAction(self.action_save)
        self.menu.addAction(self.action_close)
        self.menu.addAction(self.action_quit)
        # self.menu_2.addAction(self.action_view)
        # self.menu_2.addAction(self.action_new)
        self.menu_2.addAction(self.action_edit)
        self.menu_2.addAction(self.action_config)
        self.menu_3.addAction(self.action_run)
        self.menu_3.addAction(self.action_result)
        self.menu_3.addAction(self.action_compare)
        self.menu_3.addAction(self.action_deleteErrorInfo)

        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "代码形式规范化检测"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "代码文件"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_2), _translate("MainWindow", "代码分析"))
        self.menu.setTitle(_translate("MainWindow", "文件"))
        self.menu_2.setTitle(_translate("MainWindow", "配置"))
        self.menu_3.setTitle(_translate("MainWindow", "分析"))
        self.action_open.setText(_translate("MainWindow", "打开 "))
        self.action_close.setText(_translate("MainWindow", "关闭"))
        self.action_quit.setText(_translate("MainWindow", "退出"))
        # self.action_view.setText(_translate("MainWindow", "查看规则"))
        # self.action_new.setText(_translate("MainWindow", "新建规则"))
        self.action_edit.setText(_translate("MainWindow", "编辑规则"))
        self.action_config.setText(_translate("MainWindow", "配置规则"))
        self.action_run.setText(_translate("MainWindow", "运行"))
        self.action_result.setText(_translate("MainWindow", "查看结果"))
        self.action_compare.setText(_translate("MainWindow", "分析对比"))
        self.action_save.setText(_translate("MainWindow", "保存"))
        self.action_deleteErrorInfo.setText((_translate("MainWindow", "清空当前文件错误信息")))
