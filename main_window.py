import sys
from collections import namedtuple
from xml.etree import ElementTree as ET

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from pathlib import Path

Student = namedtuple('Student', 'name surname mark')


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
        text, ok = QtWidgets.QInputDialog.getText(self, 'Input Dialog', 'Enter your name:')
        if ok:
            self.le.setText(str(text))


class MyMainWindow:

    def __init__(self, main_window):
        self.main = main_window
        self.data = dict()
        self.initUi()

    def initUi(self):
        self.main.setObjectName("MainWindow")
        self.main.resize(556, 559)
        self.centralWidget = QtWidgets.QWidget(self.main)
        self.centralWidget.setObjectName("centralWidget")

        self.table = QtWidgets.QTableWidget(self.centralWidget)
        self.table.setGeometry(QtCore.QRect(20, 80, 521, 331))
        self.table.setObjectName("tableWidget")
        self.table.setColumnCount(5)
        self.table.setRowCount(0)
        self.table.setHorizontalHeaderLabels(['ID', 'Name', 'Surname', 'Mark'])

        self.loadFromFileBtn = QtWidgets.QPushButton(self.centralWidget)
        self.loadFromFileBtn.setGeometry(QtCore.QRect(20, 40, 521, 28))
        self.loadFromFileBtn.setObjectName("loadFromFileBtn")
        self.loadFromFileBtn.clicked.connect(self.loadFromFile)
        self.addRowBtn = QtWidgets.QPushButton(self.centralWidget)
        self.addRowBtn.setGeometry(QtCore.QRect(20, 420, 521, 28))
        self.addRowBtn.setObjectName("addRowBtn")
        self.addRowBtn.clicked.connect(self.createNewRow)
        self.saveToFileBtn = QtWidgets.QPushButton(self.centralWidget)
        self.saveToFileBtn.setGeometry(QtCore.QRect(20, 460, 521, 28))
        self.saveToFileBtn.setObjectName("saveToFileBtn")
        self.saveToFileBtn.clicked.connect(self.saveToFile)

        self.main.setCentralWidget(self.centralWidget)
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.main)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.main.setWindowTitle(_translate("MainWindow", "Задание 1"))
        self.loadFromFileBtn.setText(_translate("MainWindow", "Загрузить из файла"))
        self.addRowBtn.setText(_translate("MainWindow", "Добавить строку"))
        self.saveToFileBtn.setText(_translate("MainWindow", "Сохранить в файл"))

    def createNewRow(self):
        pass

    def deleteRowDeco(self, student_id):

        def deleteRow():
            nonlocal self, student_id
            for row in range(self.table.rowCount()):
                if self.table.item(row, 0).text() == student_id:
                    del (self.data[student_id])
                    self.table.removeRow(row)
                    break
            else:
                self.makeErrorMessage('Ошибка с поиском студента по id')

        return deleteRow

    def loadFromFile(self):
        filename = QFileDialog.getOpenFileName(directory=str(Path.home()), filter='(*.xml)')[0]
        if filename:
            try:
                self.data.clear()
                xmldoc = ET.parse(filename).getroot()
                students = xmldoc.findall('student')
                for st in students:
                    self.data[st.find('id').text] = Student(st.find('name').text,
                                                            st.find('surname').text,
                                                            st.find('mark').text)
            except Exception as e:
                self.makeErrorMessage('Ошибка при загрузке файла:\n' + str(e))

            self.table.setRowCount(0)
            for id, student in self.data.items():
                current_row_num = self.table.rowCount()
                self.table.insertRow(current_row_num)
                self.table.setItem(current_row_num, 0, QtWidgets.QTableWidgetItem(id))
                self.table.setItem(current_row_num, 1, QtWidgets.QTableWidgetItem(student.name))
                self.table.setItem(current_row_num, 2, QtWidgets.QTableWidgetItem(student.surname))
                self.table.setItem(current_row_num, 3, QtWidgets.QTableWidgetItem(student.mark))
                btn = QtWidgets.QPushButton(self.table)
                btn.setText('Delete')
                btn.clicked.connect(self.deleteRowDeco(id))
                self.table.setCellWidget(current_row_num, 4, btn)

    def saveToFile(self):
        filename = QFileDialog.getSaveFileName(directory=str(Path.home()), filter='(*.xml)')[0]
        if filename:
            try:
                root = ET.Element('students')
                tree = ET.ElementTree(root)
                for id, student in self.data.items():
                    student_elem = ET.Element('student')
                    for tag, text in [('id', id), ('name', student.name), ('surname', student.surname), ('mark', student.mark)]:
                        new_elem = ET.Element(tag)
                        new_elem.text = text
                        student_elem.append(new_elem)
                    root.append(student_elem)
                tree.write(open(filename, 'wb'))
            except Exception as e:
                self.makeErrorMessage('Ошибка при сохранении файла:\n' + str(e))

    def makeErrorMessage(self, error_string=None):
        self.data.clear()
        msg = QMessageBox()
        msg.setWindowTitle("Ошибка")
        msg.setText(error_string)
        msg.exec()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = MyMainWindow(QtWidgets.QMainWindow())
    ui.main.show()
    sys.exit(app.exec_())
