##############################################
#
# QPlainTextEdit()
#
# 普通文本编辑器
#
#     描述   : 适用于段落和字符,默认情况下,读取纯文本,一个换行符表示一个段落
#               段落中每个字符都有自己的属性,例如字体和颜色
#
#     内容编辑 : 由光标类 QTextCursor 选择文本,检索文本内容
#               QPlainTextEdit()包含 QTextDocument 对象,使用document()方法获取文本内容
#
#     优点:   QPlainTextEdit对纯文本处理进行了优化
#            QPlainTextEdit是一个简略版本的类,
#                           使用QTextEdit ,QTextDocument 作为背后技术支撑(文本编辑,文本文档)
#           QPlainTextEdit性能比QTextEdit更好,
#                           原因是因为其在文档中使用了QPlainTextDocumentLayout 简化布局

#           QPlainTextEdit不支持表格,框架,使用逐行逐段滚动方法替代像素滚动,故速度更快

#     继承: QAbstractScrollArea
#############################

from PyQt5.Qt import *
##############################################在任意位置出鼠标点击，则添加文本内容，
#
# 现在需求:
#           在普通文本编辑器中，在鼠标点击的任意位置处，插入文本
#
# 解决方法:
#           继承QPlainTextEdit类 并且重写mousePressEvent方法
#           在窗口MyWindow类中，使用MyQPlainTextEdit创建普通文本编辑器(code1)，并将其绑定为窗口对象的属性self.pte
#           并在MyQPlainTextEdit类中 直接使用 win.pte 文本框对象创建光标 te2
class MyPlainTextEdit(QPlainTextEdit):
    def mousePressEvent(self, evt):
        super().mouseMoveEvent(evt)
        # 创建光标对象（创建特定位置处的光标对象，）
        te2 = win.pte.cursorForPosition(evt.pos())
        # te2.insertText('星分翼轸，地接衡庐')
#############################在任意位置出鼠标点击，则添加文本内容，

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('QTextEdit_文本光标')
        self.resize(1200, 800)
        self.iniUI()
        self.plaintext_Event()



    def iniUI(self):
        self.pte = MyPlainTextEdit(self)#(code1)
        self.pte.resize(self.width() * 7 / 8, self.height() * 7 / 8)
        self.pte.move((self.width() - self.pte.width()) / 2, 2)
        self.pte.setStyleSheet('background-color:cyan;font-size:20px')
        self.pte.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        btn = QPushButton(self)
        self.btn = btn
        self.btn_w = self.width() / 3
        self.btn_h = self.height() * 3 / 32
        self.btn.resize(self.btn_w, self.btn_h)
        self.btn_x = (self.width() - self.btn_w) / 2
        self.btn_y = self.height() * 7 / 8 + (self.height() / 8 - self.btn_h) / 2
        self.btn.setText('测试按钮')
        self.btn.setStyleSheet('font-size:30px')
        self.btn.move(self.btn_x, self.btn_y)

        self.btn.clicked.connect(self.btn_text)




    def btn_text(self):
        # self.plaintextSetPlaceholderText()
        self.plaintextSetCurrentCharFormat()
        # self.plaintextSetLineWrapMode()
        # self.plaintextSetOverwriteMode()
        # self.plaintextSetTabChangesFocus()
        # self.plaintextFiles()
        # self.plaintextBlocks()
        # self.plaintextEditOperation()
        # self.plaintextCenterCursor()
        self.plaintextCursor()
        # self.plaintextMoveCursor()
        # self.plaintext_Event()


    #设置占位文本说明符
    def plaintextSetPlaceholderText(self):
        self.pte.setFocus()
        self.pte.setPlaceholderText('请输入你的信息:')
        self.pte.setReadOnly(False)

    #设置当前字符格式
    def plaintextSetCurrentCharFormat(self):
        self.pte.setFocus()
        tcf = QTextCharFormat()
        tcf.setFontPointSize(25)
        tcf.setFontFamily('华文新魏')
        tcf.setFontUnderline(True)
        tcf.setUnderlineColor(QColor(1,1,300))
        self.pte.setCurrentCharFormat(tcf)


    #设置换行模式
    def plaintextSetLineWrapMode(self):
        self.pte.setFocus()
        self.pte.setLineWrapMode(QPlainTextEdit.WidgetWidth)#默认设置,自动换行,保留单词完整性
        # self.pte.setLineWrapMode(QPlainTextEdit.NoWrap)#不换行,自动生成水平滚动条

    #设置覆盖模式是否开启
    def plaintextSetOverwriteMode(self):
        self.pte.setFocus()
        self.pte.setOverwriteMode(True)

    #Tab键是否设置为焦点切换
    def plaintextSetTabChangesFocus(self):
        self.pte.setFocus()
        self.pte.setTabChangesFocus(True)

    #QPlainTextEdit文件操作
    def plaintextFiles(self):
        self.pte.setFocus()

        self.pte.setPlainText('文本内容：删掉所有之前的内容，只把这句话作为新的唯一的内容。')
        self.pte.insertPlainText('文本内容：在光标右侧添加新的内容，按照正常的 从左向右写字顺序')
        self.pte.insertPlainText('123456')
        self.pte.insertPlainText('789')
        self.pte.appendPlainText('文本内容：在整个文档末尾追加新内容')
        # self.pte.appendHtml('文本内容：在整个文档末尾追加HTML字符串，不支持追加表格图片')
        #注意：pte.setPlainText()  左边API设置文本内容的时候，光标的位置并不会和锚点分离，

        # print(self.pte.toPlainText())# te中的内容 转换成纯文本，打印出来


    #QPlainTextEdit限制普通文本编辑器 文本框中 段落个数
    def plaintextBlocks(self):
        self.pte.setFocus()

        print(self.pte.blockCount())     #  pte.blockCount()  返回当前块个数
        self.pte.setMaximumBlockCount(3)  #


    #QPlainTextEdit 普通文本编辑器的编辑操作,视野缩放操作，正数放大
    def plaintextEditOperation(self):
        self.pte.setFocus()
        # self.pte.selectAll()
        # self.pte.copy()
        # self.pte.paste()
        # self.pte.clear()
        # self.pte.redo()
        # self.pte.undo()
        # self.pte.find('文本内容')
        self.pte.zoomIn(5)


    #一键快速滚动到光标所在的那一行
    def plaintextCenterCursor(self):
        self.pte.setFocus()
        self.pte.centerCursor()#尽可能让光标所在行处于中间位置
        self.pte.ensureCursorVisible()#让文本框滚动最短的距离 以保证光标可见


    #创建QPlainTextEdit普通文本编辑器 光标对象
    def plaintextCursor(self):
        self.pte.setFocus()
        # 创建光标对象
        te1 = self.pte.textCursor()
        te1.insertText('豫章故郡，洪都新府。')

    #移动光标，创建选中效果，moveCursor()
    def plaintextMoveCursor(self):
        self.pte.moveCursor(QTextCursor.EndOfLine,QTextCursor.KeepAnchor)
        self.pte.setFocus()
    #与155_文本光标的选中，setPosition movePosition
#               有一定相似性，可对比来看


    #普通文本编辑器 信号相关
    def plaintext_Event(self):
        self.setFocus()
        # self.pte.textChanged.connect(lambda :print('文本内容发生改变'))
        # self.pte.selectionChanged.connect(lambda :print('所选内容发生改变'))
        # self.pte.cursorPositionChanged.connect(lambda :print('光标位置发生改变'))
        # self.pte.modificationChanged.connect(lambda :print('编辑状态发生改变'))
        # self.pte.blockCountChanged.connect(lambda :print('段落个数发生改变'))
        # self.pte.copyAvailable.connect(lambda bool: print('复制按钮是否灰色:', not bool))
        # self.pte.redoAvailable.connect(lambda bool:print('重做按钮是否灰色:',not bool))
        # self.pte.undoAvailable.connect(lambda bool:print('撤销按钮是否灰色:',not bool))

        ##############################################普通文本编辑器 更新请求 信号的发射
        #
        # 现在需求:
        #           现在想要在pte左侧添加一个竖向编号标签
        #           随着文本框内容的滚动，实时追踪当前显示行号
        #
        # 解决方法:
        #           pte.updateRequest.connect(lambda rect,dy: label.move(const,dy))
        #
        label_background = QWidget(self)
        label_background.resize((self.width() - self.pte.width()) / 2, self.pte.height())
        label_background.move(0, self.pte.y())#(0,2)
        label_background.setStyleSheet('background-color:blue')
        label_line = QLabel(label_background)

        label_str = '\n'.join([str(i) for i in range(1, 101)])
        label_line.setText(label_str)
        # 这里有一个疑问 label_line标签的y() 为啥不能直接设为0，，还得是-180 才能在正确的竖向位置，，设为第二行时y值的始终不对
        label_line.move(label_background.width()/6,-180)
        # label_line.move(label_background.geometry().x()+label_background.width()*1/6,label_background.geometry().y())#(0,-150)
        label_line.resize(label_background.width()*2/3,3000)

        label_line.setStyleSheet('font-size:20px;background-color:white')
        label_line.adjustSize()

        self.pte.insertPlainText(label_str)
        self.pte.updateRequest.connect(lambda rect, dy : label_line.move(label_line.x(),label_line.y() + dy))

        #############################普通文本编辑器 更新请求 信号的发射

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())