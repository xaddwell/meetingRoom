from PyQt5 import QtWidgets
from UI_main import Ui_Form
import sys
from PyQt5.QtWidgets import QWidget
import cv2


class Face(QWidget, Ui_Form):
    def __init__(self):
        super(Face, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("人脸识别")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # MainWindow = QMainWindow()
    window = Face()
    window.show()
    sys.exit(app.exec_())