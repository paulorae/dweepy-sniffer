from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import sqlite3 as db
import csv
import time
import os

conn = db.connect("portemp.db")
c = conn.cursor()

class Ui_Form(object):

    def messagebox(self,title,message):
        mess=QtWidgets.QMessageBox()
        mess.setWindowTitle(title)
        mess.setText(message)
        mess.setStandardButtons(QtWidgets.QMessageBox.Ok)
        mess.exec_()

    def xdit(self):
        timestr = time.strftime("%m-%d-%Y")
        fname = self.lineEdit.text()
        season = self.lineEdit_2.text()
        self.createFolder("Record/" + str(season))

        conn.row_factory = db.Row
        try:
            data = c.execute("SELECT * FROM portrecord")
            headers = ['Thingname', 'Thingvisual1', 'Value1', 'Thingvisual2', 'Value2', 'Time', 'Date']
            if sys.version_info < (3,):
                f = open('Record/' + str(season) + '/' + str(fname) + '-' + str(timestr) + '.csv', 'wb', )
            else:
                f = open('Record/' + str(season) + '/' + str(fname) + '-' + str(timestr) + '.csv', 'w',
                         newline="")

            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(headers)  # keys=title you're looking for
            # write the rest
            writer.writerows(data)
            self.messagebox("ATTENTION!", "Successfully Saved,Go to Records! Close the Window.")
            f.close()
        except Exception as error:
            print('eror')
        self.xclear()


    def createFolder(self, directory):
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except OSError:
            print("eror")

    def xclear(self):
        query = "DELETE FROM portrecord"
        c.execute(query)
        conn.commit()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setFixedSize(462, 52)
        Form.resize(462, 52)
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(10, 10, 221, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(240, 10, 141, 31))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(390, 10, 61, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.xdit)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "EXPORTER"))
        self.lineEdit.setPlaceholderText(_translate("Form", "YOUR FILE NAME HERE"))
        self.lineEdit_2.setPlaceholderText(_translate("Form", "YOUR MONTH OR SEASON "))
        self.pushButton.setText(_translate("Form", "SAVE"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

