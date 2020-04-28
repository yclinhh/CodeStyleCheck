#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2020/4/13 0:55
# @Author : yachao_lin
# @File : main.py.py

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDialog
from CodeStyleCheck.GUI.main_window_show import QMyWindow, QCodeEditor, Login
from CodeStyleCheck.GUI.InputStuID import Ui_Dialog


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # ui = QMyWindow()
    # ui.show()
    ui = Login()
    uiMyWin = QMyWindow()
    ui.show()
    ui.closeSignal.connect(uiMyWin.deal_emit_slot)
    sys.exit(app.exec_())
