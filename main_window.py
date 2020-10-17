import sys

from PyQt5 import QtWidgets, QtCore


class AddNewString(QtWidgets.QWidget):

    def __init__(self, table):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.btn = QtWidgets.QPushButton('Dialog', self)
        self.btn.move(20, 20)
        self.btn.clicked.connect(self.showDialog)

        self.le = QtWidgets.QLineEdit(self)
        self.le.move(130, 22)

        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Input dialog')
        self.show()


    def showDialog(self):

        text, ok = QtWidgets.QInputDialog.getText(self, 'Input Dialog',
            'Enter your name:')

        if ok:
            self.le.setText(str(text))


class MyMainWindow:

    def __init__(self, main_window):
        self.main = main_window
        self.main.setObjectName("MainWindow")
        self.main.resize(556, 559)
        self.centralWidget = QtWidgets.QWidget(self.main)
        self.centralWidget.setObjectName("centralWidget")

        self.table = QtWidgets.QTableWidget(self.centralWidget)
        self.table.setGeometry(QtCore.QRect(20, 80, 521, 331))
        self.table.setObjectName("tableWidget")
        self.table.setColumnCount(0)
        self.table.setRowCount(0)

        self.loadFromFileBtn = QtWidgets.QPushButton(self.centralWidget)
        self.loadFromFileBtn.setGeometry(QtCore.QRect(20, 40, 521, 28))
        self.loadFromFileBtn.setObjectName("loadFromFileBtn")
        self.addRowBtn = QtWidgets.QPushButton(self.centralWidget)
        self.addRowBtn.setGeometry(QtCore.QRect(20, 420, 521, 28))
        self.addRowBtn.setObjectName("addRowBtn")
        self.saveToFileBtn = QtWidgets.QPushButton(self.centralWidget)
        self.saveToFileBtn.setGeometry(QtCore.QRect(20, 460, 521, 28))
        self.saveToFileBtn.setObjectName("saveToFileBtn")

        main_window.setCentralWidget(self.centralWidget)
        self.retranslate_ui()
        QtCore.QMetaObject.connectSlotsByName(self.main)

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.main.setWindowTitle(_translate("MainWindow", "Задание 1"))
        self.loadFromFileBtn.setText(_translate("MainWindow", "Загрузить из файла"))
        self.addRowBtn.setText(_translate("MainWindow", "Добавить строку"))
        self.saveToFileBtn.setText(_translate("MainWindow", "Сохранить в файл"))

    def add_row(self):
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = MyMainWindow(QtWidgets.QMainWindow())
    ui.main.show()
    sys.exit(app.exec_())
