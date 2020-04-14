#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2020/4/13 0:55
# @Author : yachao_lin
# @File : main.py.py

import sys
from PyQt5.QtWidgets import QApplication, QWidget
from CodeStyleCheck.GUI.main_window_show import QMyWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = QMyWindow()
    ui.show()
    sys.exit(app.exec_())
