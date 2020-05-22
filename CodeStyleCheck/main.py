#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2020/4/13 0:55
# @Author : yachao_lin
# @File : main.py

import sys
from PyQt5.QtWidgets import QApplication
from CodeStyleCheck.Controller.main_window_show import QMyWindow, Login
from CodeStyleCheck.GUI.gui_qss import qss

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # ui = QMyWindow()
    # ui.show()
    app.setStyleSheet(qss)
    ui_login = Login()
    uiMyWin = QMyWindow()
    # 连接信号与槽函数
    # ui.showResultSignal.connect(ui.ui2.deal_showResult_emit_slot)
    ui_login.show()
    '''连接子窗口的自定义信号与主窗口的槽函数'''
    ui_login.closeSignal.connect(uiMyWin.deal_emit_slot)

    sys.exit(app.exec_())
