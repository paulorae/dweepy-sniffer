from PyQt5 import QtCore, QtGui, QtWidgets
import dweepy
import sqlite3 as db
import time
from SAVE import Ui_Form as xsav
import os
import subprocess

conn = db.connect("portemp.db")
curs = conn.cursor()

class Ui_Form(object):

    def messagebox(self,title,message):
        mess=QtWidgets.QMessageBox()
        mess.setWindowTitle(title)
        mess.setText(message)
        mess.setStandardButtons(QtWidgets.QMessageBox.Ok)
        mess.exec_()

    def Xdata(self):
        try:
            thing = self.lineEdit.text()
            url = dweepy.get_latest_dweet_for(thing)
            dict = url[0]

            thingv1 = self.lineEdit_2.text()
            thingv2 = self.lineEdit_3.text()

            val1 = dict['content'][str(thingv1)]
            val2 = dict['content'][str(thingv2)]

            longdate = dict['created']
            date = longdate[:10]
            stamptime = longdate[11:19]

            curs.execute("SELECT * FROM portrecord")
            conn.commit()
            curs.execute("INSERT OR IGNORE INTO portrecord (Thingname, Thingvisual1, Value1, Thingvisual2, Value2, Time, Date)VALUES(?,?,?,?,?,?,?)",(thing,thingv1,val1,thingv2, val2, date, stamptime))
            print('Done')
            conn.commit()
        except Exception as error:
            self.messagebox("INFO", "Fill all the Blanks")

    def xdate(self):
        query = "SELECT * FROM portrecord"
        result = curs.execute(query)
        self.tableWidget.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        conn.commit()
        item1 = QtWidgets.QTableWidgetItem('Thing Name')
        self.tableWidget.setHorizontalHeaderItem(0, item1)
        item2 = QtWidgets.QTableWidgetItem('Thing Visual 1')
        self.tableWidget.setHorizontalHeaderItem(1, item2)
        item3 = QtWidgets.QTableWidgetItem('Visual Value 1')
        self.tableWidget.setHorizontalHeaderItem(2, item3)
        item4 = QtWidgets.QTableWidgetItem('Thing Visual 2')
        self.tableWidget.setHorizontalHeaderItem(3, item4)
        item5 = QtWidgets.QTableWidgetItem('Visual Value 2')
        self.tableWidget.setHorizontalHeaderItem(4, item5)
        item6 = QtWidgets.QTableWidgetItem('Time')
        self.tableWidget.setHorizontalHeaderItem(5, item6)
        item7 = QtWidgets.QTableWidgetItem('Date')
        self.tableWidget.setHorizontalHeaderItem(6, item7)
        self.tableWidget.resizeColumnToContents(2)
        self.tableWidget.resizeColumnToContents(4)

    def xsave(self):
        self.xsave = QtWidgets.QWidget()
        self.ui = xsav()
        self.ui.setupUi(self.xsave)
        self.xsave.show()

    def timez(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.xdate)
        self.timer.start(1000)

    def destination(self):  # Now instead of "self" is "MainWindow".
        subprocess.Popen(r'explorer /open,"Record"')

    def xclear(self):
        try:
            query = "DELETE FROM portrecord"
            curs.execute(query)
            conn.commit()
            self.messagebox("INFO", "Cleared")
        except Exception as error:
            self.messagebox("INFO", "Blank Record")


    def setupUi(self, Form):
        self.timez()
        Form.setObjectName("Form")
        Form.setFixedSize(918, 268)
        Form.resize(918, 268)
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setGeometry(QtCore.QRect(230, 10, 681, 201))
        self.tableWidget.setRowCount(100)
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setObjectName("tableWidget")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 0, 191, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(10, 40, 211, 31))
        self.lineEdit.setMaxLength(100)
        self.lineEdit.setObjectName("lineEdit")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(10, 70, 191, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(10, 110, 211, 31))
        self.lineEdit_2.setMaxLength(50)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(10, 140, 191, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.lineEdit_3 = QtWidgets.QLineEdit(Form)
        self.lineEdit_3.setGeometry(QtCore.QRect(10, 180, 211, 31))
        self.lineEdit_3.setMaxLength(50)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(810, 220, 101, 41))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.Xdata)
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(690, 220, 111, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.xclear)
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(10, 220, 211, 41))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.destination)
        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(570, 220, 111, 41))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.xsave)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Dweepy Sniffer"))
        self.label.setText(_translate("Form", "Name of Thing"))
        self.label_2.setText(_translate("Form", "Name of Thing\'s Visual 1"))
        self.label_3.setText(_translate("Form", "Name of Thing\'s Visual 2"))
        self.lineEdit.setPlaceholderText(_translate("Dialog", "DWEET'S NAME FROM DWEET.IO/SEE"))
        self.lineEdit_2.setPlaceholderText(_translate("Dialog", "INPUT DWEET'S VISUAL ONE"))
        self.lineEdit_3.setPlaceholderText(_translate("Dialog", "INPUT DWEET'S VISUAL TWO"))
        self.pushButton.setText(_translate("Form", "SNIFF"))
        self.pushButton_2.setText(_translate("Form", "CLEAR"))
        self.pushButton_3.setText(_translate("Form", "YOUR THINGS RECORD"))
        self.pushButton_4.setText(_translate("Form", "SAVE "))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

