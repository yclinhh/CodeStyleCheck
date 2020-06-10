#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2020/5/20 21:26
# @Author : yachao_lin
# @File : analyzeCompare_ui.py
import traceback

from PyQt5.QtWidgets import QWidget

from CodeStyleCheck.GUI.analyzeCompare_ui import Ui_Form


class AnalyzeCompare(QWidget, Ui_Form):
    def __init__(self):
        super(AnalyzeCompare, self).__init__()
        self.setupUi(self)

    def deal_analyzeCompare_slot(self, pathStr, codeList):

        path_str = pathStr
        code = codeList
        print('接收--路径与正确代码--成功!')
        self.textBrowser.selectAll()
        self.textBrowser.clear()
        self.textBrowser_2.selectAll()
        self.textBrowser_2.clear()
        try:
            with open(path_str, mode='r', encoding='utf8') as f:
                for line in f:
                    self.textBrowser.append(line.rstrip('\n'))
        except Exception as e:
            print(e)
            traceback.print_exc()
        for i in range(len(code)):
            if code[i] != '-1':
                self.textBrowser_2.append(code[i].rstrip('\n'))

