#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2020/4/15 11:18
# @Author : yachao_lin
# @File : text_editor.py
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import QWidget, QTextEdit, QPlainTextEdit, QApplication
from PyQt5.QtGui import QColor, QPainter, QFont, QTextFormat
import sys

global sec, num
sec = 0
num = 0


class QCodeEditor(QPlainTextEdit):

    class NumberBar(QWidget):
        # 初始化将外部类作为参数editor带进来
        def __init__(self, editor):
            super().__init__(editor)
            # 传递一个参数
            self.editor = editor
            # 信号触发条件：更新字符块，并且会传递当前行数
            #self.editor.blockCountChanged.connect(self.updateWidth)
            # 区域更新
            self.editor.updateRequest.connect(self.updateContents)
            self.font = QFont()
            self.numberBarColor = QColor("#F5F5F5")
        '''
        重写行号小部件的绘画事件
        '''
        def paintEvent(self, event):
            # 建立一个绘画设备，用前面设置的灰色填充
            painter = QPainter(self)
            painter.fillRect(event.rect(), self.numberBarColor)
            # 返回第一个可见块，即文本块
            block = self.editor.firstVisibleBlock()
            '''
            若文本块有效，进入循环，获取该文本块的块号，返回此文本块的编号（行号），
            如果块无效，则返回-1。
            使用blockBoundingGeometry()函数以内容坐标返回文本块的边界矩形，
            并使用contentOffset()转义得到矩形以获得视口上的视觉坐标。
            这里得到top。
            '''
            while block.isValid():
                global num
                num += 1
                blockNumber = block.blockNumber()
                block_top = self.editor.blockBoundingGeometry(block).translated(self.editor.contentOffset()).top()

                if blockNumber == self.editor.textCursor().blockNumber():
                    self.font.setBold(True)
                    painter.setPen(QColor("#000000"))
                else:
                    self.font.setBold(False)
                    painter.setPen(QColor("#717171"))

                # 行号绘画的区域是paint_rect，这里使用QRect对象实现的；居中对齐，具体的内容是str(blockNumber+1)，不加1就是0开始了。
                paint_rect = QRect(0, block_top, self.width(), self.editor.fontMetrics().height())
                painter.drawText(paint_rect, Qt.AlignCenter, str(blockNumber+1))
                # 获取下一块，如果是最后一个，返回空文本块。
                block = block.next()
        '''
        如果存在垂直滚动，且像素dy > 0，那么将小部件向下滚动。
        滚动后，小部件将接收需要重新绘制区域的绘画事件。
        否则更新--行号--小部件内的矩形（x，y，w，h）。
        '''
        def updateContents(self, rect, dy):
            global sec
            sec += 1
            # print(sec, rect, dy)
            if dy:
                self.scroll(0, dy)
            else:
                self.update(0, rect.y(), self.width(), self.height())

            # 我们返回编辑器输入框中插入新文本时使用的字体的磅值。并将其设置为NumberBar这个小部件的字体样式。
            if rect.contains(self.editor.viewport().rect()):
                fontSize = self.editor.currentCharFormat().font().pointSize()
                self.font.setPointSize(fontSize)
                self.font.setStyle(QFont.StyleNormal)

    def __init__(self):
        super(QCodeEditor, self).__init__()
        # 设置编辑器名字
        self.setWindowTitle("当前代码文件")
        self.setFont(QFont("Ubantu Mono", 12))
        # 设置软换行模式为不自动换行,自动生成水平滚动条
        self.setLineWrapMode(QPlainTextEdit.NoWrap)
        # 设置当前需要标记的行号初始值为None
        self.currentLineNumber = None
        # 实例化一个行号栏小部件
        self.number_bar = self.NumberBar(self)
        # 光标位置改变信号与槽函数连接，设置当前光标所在行为高亮显示
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        # 设置当前视口边缘
        self.setViewportMargins(40, 0, 0, 0)
        # 调用高亮函数让第一行初始化为高亮
        # self.highlightCurrentLine()

    # 重写resizeEvent事件，为窗口小部件设置形状
    def resizeEvent(self, *e):
        cr = self.contentsRect()
        rec = QRect(cr.left(), cr.top(), 40, cr.height())
        self.number_bar.setGeometry(rec)
        QPlainTextEdit.resizeEvent(self, *e)

    def highlightCurrentLine(self):
        extraSelections=[]
        # 获取当前光标所在块的编号（块以回车划分）无效返回0
        newCurrentLineNumber = self.textCursor().blockNumber()
        # 如果光标换行
        if newCurrentLineNumber !=self.currentLineNumber:
            self.currentLineNumber = newCurrentLineNumber
            # 设置行的颜色
            lineColor = QColor(Qt.green).lighter(160)
            # QTextEdit.ExtraSelection结构提供了一种为文档中已选择指定字符格式的方法
            selection = QTextEdit.ExtraSelection()
            # print("{1}:{0}".format(selection, newCurrentLineNumber))
            # 指定选区的背景
            selection.format.setBackground(lineColor)
            # 设置文本的整个宽度为选中状态
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            # 将锚点设置为光标位置，清楚当前选择
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
            # 允许用指定的颜色临时标记文档中的某些区域，并将其指定为选项,括号中为列表形式
            self.setExtraSelections(extraSelections)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = QCodeEditor()

    editor.show()

    sys.exit(app.exec_())