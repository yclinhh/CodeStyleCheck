#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2020/5/12 17:23
# @Author : yachao_lin
# @File : test_show_result.py

# -*- coding: utf-8 -*-
"""
@author:daimashiren
@time:2020-04-15
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import traceback
from functools import partial


# 自定义的QTableWidget,使用ToolTip提示用户当前单元格内的详细内容
class MyTableWidget(QTableWidget):
    update_table_tooltip_signal = pyqtSignal(object)

    def __init__(self, row, col):
        super(MyTableWidget, self).__init__()
        self.setRowCount(row)
        self.setColumnCount(col)
        self.ini_table()

    def ini_table(self):
        """---------初始化表格的常用选项(按需修改)------------"""
        QTableWidget.resizeColumnsToContents(self)
        QTableWidget.resizeRowsToContents(self)
        self.setSelectionMode(QAbstractItemView.NoSelection)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 列宽自动分配
        self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 行高自动分配
        # self.verticalHeader().stretchLastSection()                         #自动拓展最后一行适应表格高度
        self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

        """------------关键代码--------------"""
        self.vertical_scrollbar = QScrollBar()
        self.horizon_scrollbar = QScrollBar()
        self.vertical_scrollbar.valueChanged.connect(partial(self.scollbar_change_slot, "vertical"))
        self.horizon_scrollbar.valueChanged.connect(partial(self.scollbar_change_slot, "horizon"))
        self.setVerticalScrollBar(self.vertical_scrollbar)
        self.setHorizontalScrollBar(self.horizon_scrollbar)
        self.init_row = 0
        self.init_col = 0
        self.tool_tip = ""
        self.update_table_tooltip_signal.connect(self.update_table_tooltip_slot)
        self.title_row_height = 0

    # 设置表格列标题
    def set_horizon_title(self, title_list):
        self.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        self.horizontalHeader().setVisible(True)
        col = 0
        for item in title_list:
            item = QTableWidgetItem(str(item))
            item.setSizeHint(QSize(200, 45))  # 这里默认设置了列标题的宽和高分别为200、45,可根据需要修改
            self.setHorizontalHeaderItem(col, item)
            col += 1

        self.title_row_height = 45  # (关键值)这里的值设置为列标题高

    # 为TableWidget安装事件过滤器
    def install_eventFilter(self):
        self.installEventFilter(self)
        self.setMouseTracking(True)

    # 改变滚动条时重置当前页面的初始行和列
    def scollbar_change_slot(self, type):
        if type == "vertical":
            value = self.verticalScrollBar().value()
            self.init_row = value
            print("垂直滚动条当前的值为:",value)
            print("当前页面的起始行为:",self.init_row)
        else:
            value = self.horizontalScrollBar().value()
            self.init_col = value
            print("水平滚动条当前的值为:", value)
            print("当前页面的起始列为:", self.init_col)

    # 通过计算坐标确定当前位置所属单元格
    def update_table_tooltip_slot(self, posit):
        self.tool_tip = ""
        self.mouse_x = posit.x()
        self.mouse_y = posit.y()
        self.row_height = self.title_row_height  # 累计行高,初始值为列标题行高
        for r in range(self.rowCount()):
            current_row_height = self.rowHeight(r)
            self.col_width = 0  # 累计列宽
            if self.row_height <= self.mouse_y <= self.row_height + current_row_height:
                for c in range(self.columnCount()):
                    current_col_width = self.columnWidth(c)
                    if self.col_width <= self.mouse_x <= self.col_width + current_col_width:
                        r = self.init_row + r
                        c = self.init_col + c
                        print("鼠标当前所在的行和列为:({},{})".format(r, c))
                        item = self.item(r, c)
                        if item != None:
                            self.tool_tip = item.text()
                        else:
                            self.tool_tip = ""
                        return self.tool_tip
                    else:
                        self.col_width = self.col_width + current_col_width
            else:
                if self.mouse_y < self.row_height:
                    break
                else:
                    self.row_height = self.row_height + current_row_height

    # 事件过滤器
    def eventFilter(self, object, event):
        try:
            if event.type() == QEvent.ToolTip:
                self.setCursor(Qt.ArrowCursor)
                print("当前鼠标位置为:", event.pos())
                self.update_table_tooltip_signal.emit(event.pos())
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
                       font-size:18px;
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


# 测试自定义TableWidget
class test_table_win(QWidget):
    def __init__(self):
        super(test_table_win, self).__init__(parent=None)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("测试ToolTip")
        self.setGeometry(500, 400, 500, 300)
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)

        """调用自定义TableWidget控件"""
        self.TableWidget = MyTableWidget(5, 3)
        self.TableWidget.resize(self.width(), 225)
        self.TableWidget.verticalHeader().stretchLastSection()
        title_list = ["省份", "省会", "旅游景点"]
        self.TableWidget.set_horizon_title(title_list)
        """为TableWidget安装事件过滤器(关键)"""
        self.TableWidget.install_eventFilter()

        self.main_layout.addWidget(self.TableWidget)

    def set_table_content(self, list1, list2, list3):
        row = 0
        for item1, item2, item3 in zip(list1, list2, list3):
            self.TableWidget.setItem(row, 0, QTableWidgetItem(item1))
            self.TableWidget.setItem(row, 1, QTableWidgetItem(item2))
            self.TableWidget.setItem(row, 2, QTableWidgetItem(item3))
            row = row + 1


if __name__ == "__main__":
    import sys

    province_list = ["四川", "广西", "贵州", "云南", "广东"]
    city_list = ["成都", "南宁", "贵阳", "昆明", "广州"]
    site_list = ["九寨沟、黄龙、峨眉山、青城山、乐山大佛、都江堰",
                 "桂林漓江、钦州三娘湾、北海银滩、大新德天瀑布、百色乐业大石围天坑群",
                 "黄果树瀑布、赤水丹霞、织金洞、红枫湖、梵净山、遵义会址",
                 "怒江、九龙瀑布群、三江并流、西双版纳热带植物园、罗平螺丝田、玉龙雪山、丽江古城、香格里拉",
                 "韶关丹霞山、广州塔、广州白云山、江门开坪碉楼、南澳岛、罗浮山"]
    app = QApplication(sys.argv)
    test_table = test_table_win()
    test_table.set_table_content(province_list, city_list, site_list)
    test_table.show()
    sys.exit(app.exec_())
