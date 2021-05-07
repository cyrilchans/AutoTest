import socket
#  点击测试


class Touchscreen:
    def __init__(self):
        self.sockets = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = 1111
        self.sockets.connect(('localhost', port))
        self.sockets.recv(1024)

    def click_screen(self, click):
        '''
        点击屏幕
        :param click: 鼠标点击时的位置
        :return:
        '''
        w = click['w'] * 3
        h = click['h'] * 3
        f = f'd 0 {w} {h} 50\nc\nu 0\nc\n'
        f = (f.encode('utf-8'))
        print(f)
        self.sockets.send(f)

    def slip_screen(self, click, slip):
        '''
        滑动屏幕
        :param click: 鼠标点击时的位置
        :param slip: 鼠标释放时的位置
        :return:
        '''
        w = click['w'] * 3
        h = click['h'] * 3
        w2 = slip['w'] * 3
        h2 = slip['h'] * 3
        f = f'd 0 {w} {h} 50\nc\nm 0 {w2} {h2} 50\nc\nu 0\nc\n'
        f = (f.encode('utf-8'))
        print(f)
        self.sockets.send(f)


touch = Touchscreen()