import socket
import queue
import threading


class Banner:
    '''
    开头信息
    '''
    def __init__(self):
        self.Version = 0  # 版本信息
        self.Length = 0  # banner长度
        self.Pid = 0  # 进程ID
        self.RealWidth = 0  # 设备的真实宽度
        self.RealHeight = 0  # 设备的真实高度
        self.VirtualWidth = 0  # 设备的虚拟宽度
        self.VirtualHeight = 0  # 设备的虚拟高度
        self.Orientation = 0  # 设备方向
        self.Quirks = 0  # 设备信息获取策略

    def toString(self):
        message = "Banner [Version=" + str(self.Version) + ", length=" + str(self.Length) + ", Pid=" + str(
            self.Pid) + ", realWidth=" + str(self.RealWidth) + ", realHeight=" + str(
            self.RealHeight) + ", virtualWidth=" + str(self.VirtualWidth) + ", virtualHeight=" + str(
            self.VirtualHeight) + ", orientation=" + str(self.Orientation) + ", quirks=" + str(self.Quirks) + "]"
        return message

class Android(Banner):
    '''
    解析minicap数据流
    '''
    def __init__(self):
        super().__init__()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = 1717
        self.s.connect(("localhost", port))
        self.picture = queue.Queue()

    def ImageStream(self):
        readBannerBytes = 0
        bannerLength = 2
        readFrameBytes = 0
        frameBodylength = 0
        data = b''
        while True:
            chunk = self.s.recv(4096)
            length = len(chunk)
            cursor = 0
            while cursor < length:
                # 开头信息文件
                if readBannerBytes < bannerLength:
                    if readBannerBytes == 0:
                        self.Version = (chunk[cursor])
                    elif readBannerBytes == 1:
                        bannerLength = (chunk[cursor])
                        self.Length = bannerLength
                    elif readBannerBytes in [2, 3, 4, 5]:
                        self.Pid += ((chunk[cursor]) << ((readBannerBytes - 2) * 8)) >> 0
                    elif readBannerBytes in [6, 7, 8, 9]:
                        self.RealWidth += ((chunk[cursor]) << ((readBannerBytes - 6) * 8)) >> 0
                    elif readBannerBytes in [10, 11, 12, 13]:
                        self.RealHeight += ((chunk[cursor]) << ((readBannerBytes - 10) * 8)) >> 0
                    elif readBannerBytes in [14, 15, 16, 17]:
                        self.VirtualWidth += ((chunk[cursor]) << ((readBannerBytes - 14) * 8)) >> 0
                    elif readBannerBytes in [18, 19, 20, 21]:
                        self.VirtualHeight += ((chunk[cursor]) << ((readBannerBytes - 18) * 8)) >> 0
                    elif readBannerBytes == 22:
                        self.Orientation = (chunk[cursor]) * 90
                    elif readBannerBytes == 23:
                        self.Quirks = (chunk[cursor])
                    cursor += 1
                    readBannerBytes += 1
                    if readBannerBytes == bannerLength:
                        print(self.toString())
                elif readFrameBytes < 4:
                    frameBodylength += ((chunk[cursor] << (readFrameBytes * 8)) >> 0)
                    cursor += 1
                    readFrameBytes += 1
                else:
                    if length - cursor >= frameBodylength:
                        # data 为二进制照片流数据
                        data += chunk[cursor:cursor + frameBodylength]
                        if (data[0]) != 0xFF or (data[1]) != 0xD8:
                            return
                        # save_picture(file_name, data)
                        self.picture.put(data)
                        cursor += frameBodylength
                        frameBodylength = 0
                        readFrameBytes = 0
                        data = b''
                    else:
                        data += chunk[cursor:length]
                        frameBodylength -= length - cursor
                        readFrameBytes += length - cursor
                        cursor = length

    def run(self):
        ImageTask = threading.Thread(target=self.ImageStream)
        ImageTask.start()

android = Android()






