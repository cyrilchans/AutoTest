##说明
1.Minicap的配置
```test
    准备需要push到手机的脚本(网上冲浪即可完成)
```
2.cmd启动
```
    ①查看手机分辨率  adb shell wm size
    ②启动minicap(分辨率自行填写,下为命令例子)
        adb shell LD_LIBRARY_PATH=/data/local/tmp /data/local/tmp/minicap -P 1080x1920@1080x1920/0
    ③端口转发(这边代码写死1717端口，可以自行改掉)
        adb forward tcp:1717 localabstract:minicap
```
3.运行draw文件
```
    代码只是简易展示使用pyqt5实现安卓投屏效果，并没有对横屏进行适配
```