using OpenCvSharp;
using Point = OpenCvSharp.Point;
namespace MyNamespace
{
    class MyClass
    {
        // 需要引入OpenCvSharp4 和 OpenCvSharp4.runtime.window, 只是简单展示图片识别的功能，具体待完善
        static void Main()
        {
            // 随便截取两张图片， img1是背景图路径， img2是目标图路径
            Mat img1 = new Mat("xxxxxxxxxxxxxxxxxxx", ImreadModes.Color);
            Mat img2 = new Mat("xxxxxxxxxxxxxxxxxxx", ImreadModes.Color);
            Mat result = new Mat();
            Cv2.MatchTemplate(img1, img2, result, TemplateMatchModes.CCoeffNormed);
            Point minLoc = new Point(0, 0);
            Point maxLoc = new Point(0, 0);
            Point matchLoc = new Point(0, 0);
            Cv2.MinMaxLoc(result, out minLoc, out maxLoc);
            matchLoc = maxLoc;
            Cv2.Rectangle(img1, matchLoc, new Point(matchLoc.X + img2.Cols, matchLoc.Y + img2.Rows), Scalar.Red, 2);
            Cv2.Circle(img1, new Point(matchLoc.X + img2.Cols / 2, matchLoc.Y + img2.Rows / 2), 5, Scalar.Red, 2);
            Cv2.ImShow("win11", img1);
            Cv2.WaitKey(0);
        }
    }
}