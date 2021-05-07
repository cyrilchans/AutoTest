import sys
import time
import threading
from PyQt5 import QtGui, QtWidgets
from pictureStream import android
from touchScreen import touch

class Screens(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        android.run()
        # minicap是线程，预防画布启动过快丢失width和height
        time.sleep(0.2)
        self.picture = android.picture
        self.frame = None
        self.clickDict = None
        self.slipDict = None
        self.initUI()


    def initUI(self):
        runs = threading.Thread(target=self.getdata)
        runs.start()
        # 鼠标事件
        self.setMouseTracking(True)
        self.setWindowTitle("android")
        # 根据分辨率来设置宽高
        width = android.RealWidth
        height = android.RealHeight
        p_width = int(width/3)
        p_height = int(height/3)
        self.resize(p_width, p_height)
        self.show()

    def paintEvent(self, event):
        '''
        使用画布绘图
        '''
        if self.frame is not None:
            painter = QtGui.QPainter(self)
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(self.frame)
            painter.drawPixmap(self.rect(), pixmap)

    def getdata(self):
        while 1:
            frame = self.picture.get()
            self.refreshpic(frame)

    def refreshpic(self, frame):
        '''
        刷新绘图
        '''
        self.frame = frame
        self.update()

    def mousePressEvent(self, event):
        '''
        点击鼠标事件
        '''
        s = event.windowPos()
        self.setMouseTracking(True)
        click_dict = {
            'w': int(s.x()),
            'h': int(s.y()),
        }
        self.clickDict = click_dict

    def mouseReleaseEvent(self, event):
        '''
        释放鼠标事件
        '''
        x = event.windowPos()
        slip_dict = {
            "w": int(x.x()),
            "h": int(x.y()),
        }
        self.slipDict = slip_dict
        self.setMouseTracking(True)
        # 判断位置是否偏移
        if self.clickDict['w'] == self.slipDict['w']:
            touch.click_screen(self.clickDict)
        elif self.clickDict['w'] != self.slipDict['w']:
            touch.slip_screen(self.clickDict, slip_dict)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    screens = Screens()
    sys.exit(app.exec_())