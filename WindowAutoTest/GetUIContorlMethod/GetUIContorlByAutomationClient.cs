using System.Collections.Generic;
using System.Diagnostics;
using System.Threading;
using Interop.UIAutomationClient;


namespace Project1
{
    /*
     直接使用引用 COM引用 Interop.UIAutomationClient 实现计算机简单加减法自动化
     */
    class MyClass
    {
        static readonly CUIAutomation cUIAutomation = new CUIAutomation();
        static readonly IUIAutomationTreeWalker rawTreeWalker = cUIAutomation.CreateTreeWalker(cUIAutomation.RawViewCondition);
        public static List<IUIAutomationElement> SearchNameinApp(string _app)
        {
            IUIAutomationElement elemDesktop = cUIAutomation.GetRootElement();
            //切进 UIA_PropertyIds.UIA_NamePropertyId 查看id  也可以直接调用UIA （需要导入UIAutomationcore.dll）
            IUIAutomationElement targetCals = elemDesktop.FindFirst(TreeScope.TreeScope_Children, cUIAutomation.CreatePropertyCondition(30005, "Calculator"));
            IUIAutomationElement firstchild = rawTreeWalker.GetFirstChildElement(targetCals);
            List<IUIAutomationElement> caughtList = new List<IUIAutomationElement>();
            PrintAllChildren(firstchild, _app, ref caughtList);
            return caughtList;
        }
        private static void PrintAllChildren(IUIAutomationElement firstchild, string _app, ref List<IUIAutomationElement> _caughtlist)
        {
            if (firstchild.CurrentName != null && firstchild.CurrentName.Equals(_app))
            {
                _caughtlist.Add(firstchild);
                return;
            }

            // 深度搜索
            IUIAutomationElement child = rawTreeWalker.GetFirstChildElement(firstchild);
            if (child != null)
            {
                PrintAllChildren(child, _app, ref _caughtlist);
            }
            // 广度搜索
            IUIAutomationElement sibling = rawTreeWalker.GetNextSiblingElement(firstchild);
            if (sibling != null)
            {
                PrintAllChildren(sibling, _app, ref _caughtlist);
            }
        }
        public static void Clicktest(IUIAutomationElement item)
        {
            //切进UIA_PatternIds.UIA_InvokePatternId查看id， 也可以直接调用UIA （需要导入UIAutomationcore.dll）
            IUIAutomationInvokePattern invokePattern = item.GetCurrentPattern(10000) as IUIAutomationInvokePattern;
            if (invokePattern != null)
            {
                invokePattern.Invoke();
                Thread.Sleep(500);
            }
        }

        public static void StartCalculator()
        {
            Process process = new Process();
            // 进程打开计算机， 本人电脑是英文设置
            process.StartInfo.FileName = "calc";
            process.StartInfo.CreateNoWindow = true;
            process.Start();
        }
        static void Main()
        {
            StartCalculator();
            Thread.Sleep(1000);

            // 如果不是纯因为设置需要更改一下控件名
            string[] collection = { "Nine", "Multiply by", "Nine", "Equals" };
            foreach (string it in collection)
            {
                List<IUIAutomationElement> caughtList = SearchNameinApp(it);
                foreach (var item in caughtList)
                {
                    Clicktest(item);
                }

            }

        }
    }
}
