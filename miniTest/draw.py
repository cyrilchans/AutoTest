import sys
import threading
from PyQt5 import QtGui, QtWidgets
from miniStream import android

class Screens(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        android.run()
        self.picture = android.picture
        self.frame = None
        self.initUI()

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

    def initUI(self):
        runs = threading.Thread(target=self.getdata)
        runs.start()
        self.setWindowTitle("android")
        self.resize(400, 850)
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

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    screens = Screens()
    sys.exit(app.exec_())