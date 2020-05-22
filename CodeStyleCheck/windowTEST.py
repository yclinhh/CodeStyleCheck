from PyQt5 import QtWidgets, QtGui, QtCore


class Main(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # create table:
        self.table = QtWidgets.QTableWidget()
        self.table.setRowCount(3)
        self.table.setColumnCount(2)
        for i, letter in enumerate("ABC"):
            self.table.setItem(i, 0, QtWidgets.QTableWidgetItem(letter))
        for i in range(self.table.rowCount()):
            ch = QtWidgets.QCheckBox(parent=self.table)

            ch.clicked.connect(lambda checked, row=1, col=i: self.onStateChanged(checked, row, col))
            self.table.setCellWidget(i, 1, ch)
        self.setCentralWidget(self.table)
        self.setWindowTitle('TableWidget, CheckBoxes')
        self.show()

    def onStateChanged(self, checked, row, column):
        print(checked, row, column)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())