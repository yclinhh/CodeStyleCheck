#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2020/5/12 18:46
# @Author : yachao_lin
# @File : RewriteTableWidget.py
import traceback
from functools import partial

from PyQt5 import Qt
from PyQt5.QtCore import pyqtSignal, QSize, QEvent, QRect
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QTableWidget, QAbstractItemView, QHeaderView, QScrollBar, QTableWidgetItem, QApplication, \
    QToolTip, QWidget


# 自定义的QTableWidget,使用ToolTip提示用户当前单元格内的详细内容
class MyTableWidget(QTableWidget):
    updateTableTooltipSignal = pyqtSignal(object)

    def __init__(self):
        super(MyTableWidget, self).__init__()
        """------------关键代码--------------"""
        # 创建两个滚动条
        self.vertical_scrollbar = QScrollBar()
        self.horizon_scrollbar = QScrollBar()
        # 监听滚动条值的改变，滚动条值就是这一页中第一行行号
        self.vertical_scrollbar.valueChanged.connect(partial(self.scrollBarChangedSlot, 'vertical'))
        self.horizon_scrollbar.valueChanged.connect(partial(self.scrollBarChangedSlot, 'horizon'))
        # 设置滚动条
        self.setVerticalScrollBar(self.vertical_scrollbar)
        self.setHorizontalScrollBar(self.horizon_scrollbar)
        # 初始化值
        self.tool_tip = ""
        self.initRow = 0
        self.initCol = 0
        self.titleRowHeight = 27  # ****通过在show_result函数中打印获得***
        self.updateTableTooltipSignal.connect(self.updateTableTooltipSlot)

    # 为TableWidget安装事件过滤器，开始追踪鼠标坐标
    def install_eventFilter(self):
        self.installEventFilter(self)
        self.setMouseTracking(True)

    # 改变滚动条时重置当前页面的初始行和列
    def scrollBarChangedSlot(self, type):
        if type == 'vertical':
            value = self.verticalScrollBar().value()
            self.initRow = value
        else:
            value = self.horizontalScrollBar().value()
            self.initCol = value

    # 通过计算坐标确定当前位置所属单元格
    def updateTableTooltipSlot(self, posit):
        """
        :param posit:鼠标坐标
        :return: 提示框内容
        """
        self.tool_tip = ""
        self.mouse_x = posit.x()
        self.mouse_y = posit.y()
        self.allRowHeight = self.titleRowHeight  # 设置总行高初始值为标题行的高度
        for r in range(self.rowCount()):
            currentRowHeight = self.rowHeight(r)  # 获得第r行的行高
            self.colWidth = 0  # 累计列宽
            if self.allRowHeight <= self.mouse_y <= self.allRowHeight + currentRowHeight:
                for c in range(self.columnCount()):
                    currentColWidth = self.columnWidth(c)  # 获得第c列的列宽
                    if self.colWidth <= self.mouse_x <= self.colWidth + currentColWidth:
                        r = self.initRow + r  # 获得当前鼠标所在行
                        c = self.initCol + c  # 获得当前鼠标所在列
                        print("鼠标当前所在的行和列为:({},{})".format(r, c))
                        item = self.item(r, c)
                        if item is not None:
                            self.tool_tip = item.text()
                        else:
                            self.tool_tip = ""
                        return self.tool_tip
                    else:
                        self.colWidth += currentColWidth
            else:
                if self.mouse_y < self.allRowHeight:
                    break
                else:
                    self.allRowHeight += currentRowHeight

    # 事件过滤器
    def eventFilter(self, object, event):
        try:
            if event.type() == QEvent.ToolTip:
                # self.setCursor(Qt.ArrowCursor)
                print("当前鼠标位置为:", event.pos())
                self.updateTableTooltipSignal.emit(event.pos())
                # 设置提示气泡显示范围矩形框,当鼠标离开该区域则ToolTip消失
                rect = QRect(self.mouse_x, self.mouse_y, 30, 10)  # QRect(x,y,width,height)
                # 设置QSS样式
                self.setStyleSheet(
                    """QToolTip{border:10px;
                       border-top-left-radius:5px;
                       border-top-right-radius:5px;
                       border-bottom-left-radius:5px;
                       border-bottom-right-radius:5px;
                       background:#4F4F4F;
                       color:#00BFFF;
                       font-size:14px;
                       font-family:"微软雅黑";
                    }""")
                QApplication.processEvents()
                # 在指定位置展示ToolTip
                QToolTip.showText(QCursor.pos(), self.tool_tip, self, rect, 1500)

                """
                showText(QPoint, str, QWidget, QRect, int)
                #############参数详解###########
                #QPoint指定tooptip显示的绝对坐标,QCursor.pos()返回当前鼠标所在位置
                #str为设定的tooptip
                #QWidget为要展示tooltip的控件
                #QRect指定tooltip显示的矩形框范围,当鼠标移出该范围,tooltip隐藏,使用该参数必须指定Qwidget!
                #int用于指定tooltip显示的时长(毫秒)
                """
            return QWidget.eventFilter(self, object, event)
        except Exception as e:
            traceback.print_exc()
