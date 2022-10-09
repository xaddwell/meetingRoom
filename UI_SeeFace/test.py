# 主函数
from PyQt5 import QtWidgets
from UI_main import Ui_Form
import cv2
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


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
        # # 在前端UI输出提示信息
        # window.statusbar.showMessage("正在使用摄像头...")

    def show_pic(self):
        # 全局变量
        # 在函数中引入定义的全局变量
        # 读取摄像头的一帧画面
        success, frame = self.cap.read()
        if success:
            # 检测
            # 摄像头读到frame
            # 将画面显示在前端UI上
            show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
            window.label_2.setPixmap(QPixmap.fromImage(showImage))


def CamConfig_init():
    window.f_type = CamConfig()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # MainWindow = QMainWindow()
    window = Face()
    window.window_init()
    window.show()
    sys.exit(app.exec_())
