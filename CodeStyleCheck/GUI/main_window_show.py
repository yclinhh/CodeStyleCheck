#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2020/4/12 22:04
# @Author : yachao_lin
# @File : main_window_show.py

import fileinput
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
# from GUI.main_window import Ui_MainWindow
from CodeStyleCheck.GUI.main_window import Ui_MainWindow


class QFileDialogDemo(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(QFileDialogDemo, self).__init__()
        self.setupUi(self)
        self.initUI()

    # 后台逻辑处理
    def initUI(self):
        self.action.triggered.connect(self.open_file_action)

    # 代码文件加载线程
    def open_file_action_thread(self):
        pass

    # 代码文件加载
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
            print('OK')
            filenames = dialog.selectedFiles()
            print(str(filenames[0]))
            f = open(filenames[0], encoding='utf-8', mode='r+')
            with f:
                data = f.read()
                self.plainTextEdit.appendPlainText(data)
                print(data)

