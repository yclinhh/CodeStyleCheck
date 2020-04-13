#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2020/4/13 0:55
# @Author : yachao_lin
# @File : main.py.py

import sys
from PyQt5.QtWidgets import QApplication, QWidget
from GUI.main_window_show import QFileDialogDemo

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = QFileDialogDemo()
    ui.show()
    sys.exit(app.exec_())

    '''
    with open('E:/林.指针/c++/程序片段练习/从小到大输出/从小到大输出/从小到大输出.cpp','r+') as f:
        print(f.read())
    '''