import gui
import sys
from arithmetic_of_GF import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Form(QMainWindow, gui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.button_calculated)
        self.pushButton_2.clicked.connect(self.button_cleared)
        self.a, self.b, self.p = 2, 1, 3
        self.abp = self.a, self.b, self.p
        self.lineEdit.setText(str(self.p))
        self.lineEdit_2.setText(str(self.a))
        self.lineEdit_3.setText(str(self.b))

    def button_calculated(self):
        self.p = int(self.lineEdit.text())
        self.a = int(self.lineEdit_2.text())
        self.b = int(self.lineEdit_3.text())
        self.lineEdit_4.setText(str(find_ord_val_GF(self.a, self.p)))
        self.lineEdit_5.setText(str(add_of_GF(*self.abp)))
        self.lineEdit_6.setText(str(sub_of_GF(*self.abp)))
        self.lineEdit_7.setText(str(mul_of_GF(*self.abp)))
        self.lineEdit_8.setText(str(div_of_GF(*self.abp)))

    def button_cleared(self):
        self.lineEdit_4.clear()
        self.lineEdit_5.clear()
        self.lineEdit_6.clear()
        self.lineEdit_7.clear()
        self.lineEdit_8.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    app.exec()
