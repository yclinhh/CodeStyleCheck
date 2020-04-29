#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2020/4/13 0:55
# @Author : yachao_lin
# @File : main.py.py

import sys
from PyQt5.QtWidgets import QApplication
from CodeStyleCheck.Controller.main_window_show import QMyWindow, Login

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = QMyWindow()
    # ui.show()
    # ui = Login()
    # uiMyWin = QMyWindow()
    ui.show()
    '''连接子窗口的自定义信号与主窗口的槽函数'''
    # ui.closeSignal.connect(uiMyWin.deal_emit_slot)
    sys.exit(app.exec_())
