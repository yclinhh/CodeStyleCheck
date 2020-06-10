#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2020/4/13 0:55
# @Author : yachao_lin
# @File : main.py

import sys
from PyQt5.QtWidgets import QApplication
from CodeStyleCheck.Controller.main_window_show import QMyWindow, Login
from CodeStyleCheck.Controller.show_configRule import MyConfigRule
from CodeStyleCheck.GUI.gui_qss import qss
# if temp == '空格':
#     self.tableWidget.item(i, j).setBackground(QtGui.QColor(171, 208, 188))
# elif temp == '对齐':
#     self.tableWidget.item(i, j).setBackground(QtGui.QColor(255, 153, 255))
# elif temp == '注释':
#     self.tableWidget.item(i, j).setBackground(QtGui.QColor(153, 255, 255))
# elif temp == '代码行':
#     self.tableWidget.item(i, j).setBackground(QtGui.QColor(240, 240, 240))
# else:
#     pass
if __name__ == '__main__':
    app = QApplication(sys.argv)
    # ui = QMyWindow()
    # ui.show()
    app.setStyleSheet(qss)
    ui_mainWindow = QMyWindow()   # 主窗口先建立
    ui_login = Login()

    # 连接信号与槽函数
    # ui.showResultSignal.connect(ui.ui2.deal_showResult_emit_slot)
    ui_login.show()
    '''连接子窗口的自定义信号与主窗口的槽函数'''
    ui_login.closeSignal.connect(ui_mainWindow.deal_emit_slot)
    sys.exit(app.exec_())
