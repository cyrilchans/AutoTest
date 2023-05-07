using System;
using System.Drawing;
using System.Runtime.InteropServices;
using System.Threading;
using System.Windows.Forms;

namespace ConsoleApp9
{
    //调用最新版微软官方接口重新封装鼠标和键盘事件， 键盘事件安装好环境直接运行即可， 鼠标点击事件需要结合坐标来实践，
    //后面会上传c#OPencv识别图片位置方式结合起来使用，
    // 需要注意的是需要引入System.Windows.Forms， 接下来只需要使用ALT+T哪里报错点哪里
    //https://learn.microsoft.com/windows/win32/api/winuser/nf-winuser-sendinput
    //https://learn.microsoft.com/windows/win32/api/winuser/nf-winuser-mouse_event
    class Program
    {
        /// <summary>
        /// 可以根据官方文档提前将参数封装
        /// </summary>
        #region Parameter definition
        enum MouseEventFlag
        {
            // <summary>
            // 鼠标移动事件
            // </summary>
            Move = 0x0001,

            // <summary>
            // 鼠标左键按下事件
            // </summary>
            LeftDown = 0x0002,
            LeftUp = 0x0004,
            RightDown = 0x0008,
            RightUp = 0x0010,
            MiddleDown = 0x0020,
            MiddleUp = 0x0040,
            XDown = 0x0080,
            XUp = 0x0100,
            Wheel = 0x0800,
            VirtualDesk = 0x4000,
            // <summary>
            // 设置鼠标坐标为绝对位置（dx,dy）,否则为距离最后一次事件触发的相对位置
            // </summary>
            Absolute = 0x8000
        }
        [StructLayout(LayoutKind.Explicit)]
        public struct Input
        {
            [FieldOffset(0)] public Int32 type;
            [FieldOffset(4)] public MouseInput mi;
            [FieldOffset(4)] public KeybdInput ki;
            [FieldOffset(4)] public TagHARDWAREINPUT hi;
        }
        [StructLayout(LayoutKind.Sequential)]
        public struct MouseInput
        {
            public int dx;
            public int dy;
            public int Mousedata;
            public int dwFlag;
            public int time;
            public IntPtr dwExtraInfo;
        }
        [StructLayout(LayoutKind.Sequential)]
        public struct KeybdInput
        {
            public short wVk;
            public short wScan;
            public int dwFlags;
            public int time;
            public int dwExtraInfo;
        }
        [StructLayout(LayoutKind.Sequential)]
        public struct TagHARDWAREINPUT
        {
            int uMsg;
            short wParamL;
            short wParamH;
        }
        #endregion

        #region GetScreenScaling
        [DllImport("gdi32.dll")]
        static extern int GetDeviceCaps(IntPtr hdc, int nIndex);
        public enum DeviceCap
        {
            VERTRES = 10,
            DESKTOPVERTRES = 117,
        }
        public static float GetScalingFactor()
        {
            Graphics g = Graphics.FromHwnd(IntPtr.Zero);
            IntPtr desktop = g.GetHdc();
            int LogicalScreenHeight = GetDeviceCaps(desktop, (int)DeviceCap.VERTRES);
            int PhysicalScreenHeight = GetDeviceCaps(desktop, (int)DeviceCap.DESKTOPVERTRES);
            float ScreenScalingFactor = (float)PhysicalScreenHeight / (float)LogicalScreenHeight;
            return ScreenScalingFactor;
        }
        #endregion

        [DllImport("user32.dll")]
        public static extern void keybd_event(byte bVk, byte bScan, int dwFlags, int dwExtraInfo);

        public static void ClickWinKey()
        {
            keybd_event((byte)Keys.LWin, 0, 0, 0);
            keybd_event((byte)Keys.LWin, 0, 2, 0);
            Thread.Sleep(1000);
        }

        [DllImport("user32.dll")]
        public static extern int mouse_event(int dwFlags, int dx, int dy, int dwData, int dwExtraInfo);

        //鼠标移动到指定位置
        public static void MoveMouseToSpecifyLocation(int x, int y)
        {
            float scaling = GetScalingFactor();//Screen.PrimaryScreen.Bounds的大小=分辨率/缩放比，即1920x1080的分辨率 & 1.25缩放比 =>屏幕大小是1536*1.25
            int dx = (int)((double)x / (Screen.PrimaryScreen.Bounds.Width * scaling) * 0xffff); //屏幕分辨率映射到0~65535(0xffff,即16位)之间
            int dy = (int)((double)y / (Screen.PrimaryScreen.Bounds.Height * scaling) * 0xffff); //转换为double类型运算，否则值为0、1
            mouse_event((int)MouseEventFlag.Move | (int)MouseEventFlag.Absolute, dx, dy, 0, 0);
        }
        //使用左键点击（右键点击RightDown）
        public static void LeftMouseButtonClickSpecifyLocation(int x, int y, string about = "left")
        {
            float scaling = GetScalingFactor();//Screen.PrimaryScreen.Bounds的大小=分辨率/缩放比，即1920x1080的分辨率 & 1.25缩放比 =>屏幕大小是1536*1.25
            int dx = (int)((double)x / (Screen.PrimaryScreen.Bounds.Width * scaling) * 0xffff); 
            int dy = (int)((double)y / (Screen.PrimaryScreen.Bounds.Height * scaling) * 0xffff); 
            int ACTION = about.ToLower().Trim().Equals("left") ? (int)MouseEventFlag.LeftDown : (int)MouseEventFlag.RightDown;
            int ACTIONAFTER = about.ToLower().Trim().Equals("left") ? (int)MouseEventFlag.LeftUp : (int)MouseEventFlag.RightUp;

            mouse_event((int)MouseEventFlag.Move | ACTION | (int)MouseEventFlag.Absolute, dx, dy, 0, 0);
            mouse_event(ACTIONAFTER | (int)MouseEventFlag.Absolute, dx, dy, 0, 0);
        }


        [DllImport("user32.dll")]
        public static extern void SendInput(uint nInputs, Input[] pInputs, int cbSize);

        //输入键位封装
        public static void KeyboardInputFunction()
        {
            byte[] virtualkeycode = { (byte)Keys.LWin };
            Input[] input = new Input[2 * virtualkeycode.Length];
            input[0].type = 1;
            input[0].ki.wVk = (byte)Keys.LWin;
            input[0].ki.dwFlags = 0;

            input[1].type = 1;
            input[1].ki.wVk = (byte)Keys.LWin;
            input[1].ki.dwFlags = 2;
            SendInput((uint)input.Length, input, Marshal.SizeOf(input[0].GetType()));
        }

        //输入字符串封装
        public static void UseSendInputSendString(string targetString)
        {
            foreach (var item in targetString)
            {
                Console.WriteLine(item);
                Input[] input = new Input[2];
                input[0].type = 1;
                input[0].ki.wVk = 0;
                input[0].ki.wScan = (short)item;
                input[0].ki.dwFlags = 4;
                input[1].type = 1;
                input[1].ki.wVk = 0;
                input[1].ki.wScan = (short)item;
                input[1].ki.dwFlags = 2;
                SendInput(2U, input, Marshal.SizeOf(input[0].GetType()));
            }
        }

        static void Main() {
            KeyboardInputFunction();
            Thread.Sleep(1000);
            UseSendInputSendString("i love you");
        }

    }
}
