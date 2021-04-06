from PyQt5 import QtWidgets, QtGui, QtCore, uic
from PyQt5.QtGui import QImage, QPixmap
import sys
import os
import subprocess
import time

class Ui(QtWidgets.QMainWindow):

    def __init__(self):

        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('ui/home.ui', self) # Load the .ui file
        self.show() # Show the GUI

        self.obj_button.clicked.connect(self.obj_button_pressed)
        self.sub_button.clicked.connect(self.sub_button_pressed)

    def obj_button_pressed(self):
        os.system('python objective.py')
        sys.exit()

    def sub_button_pressed(self):
        os.system('python subjective.py')
        sys.exit()

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()