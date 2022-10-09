# 主函数
from PyQt5 import QtWidgets
from UI_main import Ui_Form
import cv2
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from socket import socket, AF_INET, SOCK_STREAM
import time


class Face(QWidget, Ui_Form):
    def __init__(self):
        super(Face, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("人脸识别")
        # 打开文件类型，用于类的定义
        self.f_type = 0

    def window_init(self):
        # 设置控件属性
        # 菜单按钮 槽连接 到函数
        CamConfig_init()
        # 自适应窗口缩放
        self.label.setScaledContents(True)


def request_handler(myId):
    sock_client = socket(AF_INET, SOCK_STREAM)
    sock_client.connect(('localhost', 5000))
    sock_client.send(str.encode(myId))
    response = sock_client.recv(8192)
    return response


# 定义摄像头类
class CamConfig:
    def __init__(self):
        # 设置时钟
        self.v_timer = QTimer()
        # 打开摄像头
        self.cap = cv2.VideoCapture(0)
        if not self.cap:
            print("打开摄像头失败")
            return
        # 设置定时器周期，单位毫秒
        self.v_timer.start(20)
        # 连接定时器周期溢出的槽函数，用于显示一帧视频
        self.v_timer.timeout.connect(self.show_pic)
        self.faceCascade = cv2.CascadeClassifier("weights/haarcascade_frontalface_alt2.xml")
        self.fakeFace = cv2.imread('images/2.jpg')
        # 创建我们的LBPH人脸识别器
        self.face_recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.face_recognizer.read('model.yml')
        # 确认验证信息
        self.idNum = -1
        self.timeCounter = 0

    def show_pic(self):
        # 读取摄像头的一帧画面
        success, frame = self.cap.read()
        if success:
            # 将画面显示在前端UI上
            show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)   # 480 * 640 * 3
            faces = self.face_detect(show)
            for (x, y, w, h) in faces:
                face = show[y:y + h, x:x + w]
                face = cv2.resize(face, (face.shape[1] * 2, face.shape[0] * 2))
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                idNum, confidence = self.face_recognizer.predict(face)
                if self.idNum == idNum and confidence <= 40:
                    self.timeCounter += 1
                elif self.idNum == idNum and confidence > 40:
                    self.timeCounter -= 1
                else:
                    self.idNum = idNum
                    self.timeCounter = 0
                    window.label.setText("")
                if self.timeCounter >= 4:
                    response = request_handler(str(idNum))
                    if response:
                        window.label.setText("验证成功")
                elif self.timeCounter <= -4:
                    window.label.setText("陌生人")
                print(idNum, confidence)  # (confidence <= 40) 3 times
                cv2.rectangle(show, (x, y), (x + w, y + h), (0, 255, 0), 2)
            showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
            window.label_2.setPixmap(QPixmap.fromImage(showImage))

    def face_detect(self, frame):
        faces = self.faceCascade.detectMultiScale(frame, 1.2, 4)
        return faces


def CamConfig_init():
    window.f_type = CamConfig()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # MainWindow = QMainWindow()
    window = Face()
    window.window_init()
    window.show()
    sys.exit(app.exec_())