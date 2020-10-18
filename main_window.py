import sys
from collections import namedtuple
from xml.etree import ElementTree as ET

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from pathlib import Path

Student = namedtuple('Student', 'name surname mark')


class MyMainProgram:

    def __init__(self, main_window):
        self.main = main_window
        self.data = dict()
        self._initUi()

    def _initUi(self):
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
        self._setLastRow()

        self.loadFromFileBtn = QtWidgets.QPushButton(self.centralWidget)
        self.loadFromFileBtn.setGeometry(QtCore.QRect(20, 40, 521, 28))
        self.loadFromFileBtn.setObjectName("loadFromFileBtn")
        self.loadFromFileBtn.clicked.connect(self.loadFromFile)
        self.saveToFileBtn = QtWidgets.QPushButton(self.centralWidget)
        self.saveToFileBtn.setGeometry(QtCore.QRect(20, 460, 521, 28))
        self.saveToFileBtn.setObjectName("saveToFileBtn")
        self.saveToFileBtn.clicked.connect(self.saveToFile)

        self.main.setCentralWidget(self.centralWidget)
        self._retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.main)

    def _retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.main.setWindowTitle(_translate("MainWindow", "Задание 1"))
        self.loadFromFileBtn.setText(_translate("MainWindow", "Загрузить из файла"))
        self.saveToFileBtn.setText(_translate("MainWindow", "Сохранить в файл"))

    def _insertNewRow(self, id, student, current_row_num):
        self.table.insertRow(current_row_num)
        self.table.setItem(current_row_num, 0, QtWidgets.QTableWidgetItem(id))
        self.table.setItem(current_row_num, 1, QtWidgets.QTableWidgetItem(student.name))
        self.table.setItem(current_row_num, 2, QtWidgets.QTableWidgetItem(student.surname))
        self.table.setItem(current_row_num, 3, QtWidgets.QTableWidgetItem(student.mark))
        btn = QtWidgets.QPushButton(self.table)
        btn.setText('Delete')
        btn.clicked.connect(self.deleteRowDeco(id))
        self.table.setCellWidget(current_row_num, 4, btn)

    def _setLastRow(self):
        current_row_num = self.table.rowCount()
        self.table.insertRow(current_row_num)
        btn = QtWidgets.QPushButton(self.table)
        btn.setText('Add')
        btn.clicked.connect(self.createNewRow)
        self.table.setCellWidget(current_row_num, 4, btn)

    def createNewRow(self):
        new_row = self.table.rowCount() - 1 if self.table.rowCount() > -1 else 0
        try:
            if self.table.item(new_row, 0) and self.table.item(new_row, 0).text() not in self.data.keys():
                id = self.table.item(new_row, 0).text()
                student = Student(self.table.item(new_row, 1).text(), self.table.item(new_row, 2).text(),
                                  self.table.item(new_row, 3).text())
                self.data[id] = student
                self._insertNewRow(id, student, new_row)
                for col in range(4):
                    self.table.item(new_row + 1, col).setText('')
            else:
                raise KeyError()
        except Exception:
            self.makeErrorMessage('Ошибка при добавлении студента')

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
                self._insertNewRow(id, student, self.table.rowCount())
            self._setLastRow()

    def saveToFile(self):
        filename = QFileDialog.getSaveFileName(directory=str(Path.home()), filter='(*.xml)')[0]
        if filename:
            try:
                root = ET.Element('students')
                tree = ET.ElementTree(root)
                for id, student in self.data.items():
                    student_elem = ET.Element('student')
                    for tag, text in [('id', id), ('name', student.name),
                                      ('surname', student.surname), ('mark', student.mark)]:
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
    ui = MyMainProgram(QtWidgets.QMainWindow())
    ui.main.show()
    sys.exit(app.exec_())
