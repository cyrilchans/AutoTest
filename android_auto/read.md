#说明
1.注意事项
```
    1.请确认测试手机里面有对应的minicap和minitouch工具
    2.运行main的时候确定启动了minicap和minitouch
    3.此代码是使用pyqt5简易实现安卓投屏以及在投屏上操作手机，供学习使用
```
2.minicap和minitouch的启动
```
    minicap：
        ①查看手机分辨率  adb shell wm size
        ②启动minicap(分辨率自行填写,下为命令例子)
            adb shell LD_LIBRARY_PATH=/data/local/tmp /data/local/tmp/minicap -P 1080x1920@1080x1920/0
        ③端口转发(这边代码写死1717端口，可以自行改掉)
            adb forward tcp:1717 localabstract:minicap
    minitouch：
        ①启动minitouch：
             adb shell /data/local/tmp/minitouch
        ②端口转发： 
            adb forward tcp:1111 localabstract:minitouch
```
3.如何使用
```
    git到本地，前置条件准备完成，启动main.py即可。(记得安装pyqt5)
    注意: 端口号可以随意，但是需要去对应文件中修改端口，默认最佳
```