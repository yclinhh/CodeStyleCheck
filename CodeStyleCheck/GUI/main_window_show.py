#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2020/4/12 22:04
# @Author : yachao_lin
# @File : main_window_show.py
import sys

import pymysql
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from CodeStyleCheck.GUI.text_editor import QCodeEditor
from CodeStyleCheck.GUI.main_window import Ui_MainWindow
# from CodeStyleCheck.lianxi.QCodeEditor1 import QCodeEditor
# 全局变量存储：文件路径
glo_file_path = ""


class QMyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(QMyWindow, self).__init__()
        self.setupUi(self)
        self.myTextEditor = QCodeEditor()
        self.horizontalLayout.addWidget(self.myTextEditor)
        self.initUI()

    # 后台逻辑处理
    def initUI(self):
        # 关联信号与槽函数
        self.action_open.triggered.connect(self.open_file_action)
        self.action_save.triggered.connect(self.save_file_action)
        self.action_close.triggered.connect(self.close_file_action)
        self.action_quit.triggered.connect(self.mainWindow_quit)
        self.action_run.triggered.connect(self.code_check_action)

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
            # 接受选中文件的路径，路径默认保存在列表
            file_path = dialog.selectedFiles()
            # 显示文件路径
            global glo_file_path
            glo_file_path = file_path[0]
            print("保存文件路径：", glo_file_path)
            self.textBrowser.setPlainText(str(file_path[0]))
            try:
                # 读写方式打开文件
                with open(file_path[0], encoding='utf-8', mode='r+') as f:
                    data = f.read()
                    self.myTextEditor.appendPlainText(data)
            except IOError as e:
                print(e)

    # 保存文件
    def save_file_action(self):
        global glo_file_path
        # if glo_file_path is not None:
        print("打印文件路径：", glo_file_path)
        try:
            with open(glo_file_path, mode='r+', encoding='utf8') as f:
                f.write(self.myTextEditor.toPlainText())
                print("保存成功！")
        except IOError as e:
            print(e)
            print("exception:glo_file_path")

    # 清屏
    def close_file_action(self):
        self.myTextEditor.selectAll()
        self.myTextEditor.clear()
        self.textBrowser.selectAll()
        self.textBrowser.clear()

    # 重写关闭事件（用函数调用它没有用）
    def closeEvent(self, event):
        reply = QMessageBox.question(self, '提示', '你确定要关闭吗？',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def mainWindow_quit(self):
        sapp = QApplication.instance()
        sapp.exit()

    # 代码检查
    def code_check_action(self):
        db = pymysql.connect("localhost", "root", "123456", "cstyle_db" )
        cursor = db.cursor()
        cursor.execute("select VERSION()")
        data = cursor.fetchall()
        print(data)
        try:
            global glo_file_path
            with open(glo_file_path, mode='r', encoding='utf8') as f:
                for line in f:
                    line = f.readline()
                    result = self.lexical_analyzer(line)
                    self.check(result)

        except IOError as e:
            print(e)

    @staticmethod
    def lexical_analyzer(line):
        string = line

        return []

    @staticmethod
    def check(line):
        print(line, end='')
        print(1)
        # sys.exit()
