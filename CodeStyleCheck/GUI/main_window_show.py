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
from CodeStyleCheck.GUI.QCodeEditor import QCodeEditor


class QMyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(QMyWindow, self).__init__()
        self.setupUi(self)
        self.ff = QCodeEditor()
        self.horizontalLayout.addWidget(self.ff)
        self.initUI()

    # 后台逻辑处理
    def initUI(self):
        # 打开文件信号与槽关联
        self.action_open.triggered.connect(self.open_file_action)
        # 主窗口退出信号与槽关联
        self.action_quit.triggered.connect(self.mainWindow_quit)

    # 代码文件加载线程
    def open_file_action_thread(self):
        pass

    # 打开代码文件
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
            # 接受选中文件的路径，路径默认保存在列表
            file_path = dialog.selectedFiles()
            # 显示文件路径
            self.textBrowser.setPlainText(str(file_path[0]))
            print(str(file_path[0]))
            # 读写方式打开文件
            f = open(file_path[0], encoding='utf-8', mode='r+')
            with f:
                data = f.read()
                '''
                self.plainTextEdit.appendPlainText(data)
                
                '''
                self.ff.appendPlainText(data)
                print(data)

    # 打开文件
    def open_file(self):
        file_name = QFileDialog.getOpenFileName()

    # 重写关闭事件，当函数调用它没有用
    def closeEvent(self, event):
        reply = QMessageBox.question(self, '提示', '你确定要关闭吗？',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def mainWindow_quit(self):
        qapp = QApplication.instance()
        qapp.exit()
        # 用信号与槽机制  每次点击一个按钮就发射一个信号