using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Threading;
using System.Windows;
using System.Windows.Automation;

namespace Project1
{
    /*
       直接使用引用 UIAtuomationClient, UIAutomationTypes, UIA, 复制代码直接Alt+L报错代码看提示添加即可，
      …资料地址：https://learn.microsoft.com/zh-cn/dotnet/api/system.windows.automation?view=windowsdesktop-6.0
                  https://vimsky.com/examples/detail/csharp-method-system.windows.automation.automationelement.getcurrentpattern.html
                  https://vimsky.com/examples/detail/csharp-constructor-system.windows.automation.treewalker.-ctor.html
                  https://vimsky.com/examples/detail/csharp-method-system.windows.automation.invokepattern.invoke.html
      …
     */
    class MyClass
    {
        static Condition condition1 = new PropertyCondition(AutomationElement.IsControlElementProperty, true);
        static Condition condition2 = new PropertyCondition(AutomationElement.IsEnabledProperty, true);
        static TreeWalker rawTreeWalker = new TreeWalker(new AndCondition(condition1, condition2));

        public static List<AutomationElement> searchNameinApp(string _app)
        {
            AutomationElement desktop = AutomationElement.RootElement;
            AutomationElement targetCals = desktop.FindFirst(TreeScope.Children, new PropertyCondition(AutomationElement.NameProperty, "Calculator"));
            AutomationElement firstchild = rawTreeWalker.GetFirstChild(targetCals);
            List<AutomationElement> caughtList = new List<AutomationElement>();
            printAllChildren(firstchild, _app, ref caughtList);
            return caughtList;
        }
        private static void printAllChildren(AutomationElement firstchild, string _app, ref List<AutomationElement> _caughtlist)
        {
            if (firstchild.Current.Name != null && firstchild.Current.Name.Equals(_app))
            {
                _caughtlist.Add(firstchild);
                return;
            }

            // 深度搜索
            AutomationElement child = rawTreeWalker.GetFirstChild(firstchild);
            if (child != null)
            {
                printAllChildren(child, _app, ref _caughtlist);
            }
            // 广度搜索
            AutomationElement sibling = rawTreeWalker.GetNextSibling(firstchild);
            if (sibling != null)
            {
                printAllChildren(sibling, _app, ref _caughtlist);
            }
        }
        public static void clicktest(AutomationElement item)
        {
            InvokePattern invokePattern = item.GetCurrentPattern(InvokePattern.Pattern) as InvokePattern;
            if (invokePattern != null)
            {
                invokePattern.Invoke();
                Thread.Sleep(500);
            }
        }
        public static void StartCalculator() 
        {
            Process process = new Process();
            // 本人电脑设置为英文，如果不是英文因为需要修改成中文
            process.StartInfo.FileName = "calc";
            process.StartInfo.CreateNoWindow = true;
            process.Start();
        }
        static void Main(string[] args)
        {
            StartCalculator();
            Thread.Sleep(1000);
            // 本人电脑设置为英文，如果不是英文因为需要修改成对应中文控件
            string[] collection = { "Nine", "Multiply by", "Nine", "Equals" };
            foreach (string it in collection)
            {
                List<AutomationElement> caughtList = searchNameinApp(it);
                foreach (var item in caughtList)
                {
                    clicktest(item);
                }

            }

        }
    }
}
