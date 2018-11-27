#!/usr/bin/env python
# _*_ coding: UTF-8 _*_
from wx.adv import SplashScreen as SplashScreen
import wx.lib.mixins.inspection
import os
import wx
from AUI import MyAuiFrame
def opj(path):
    """Convert paths to the platform-specific separator"""
    st = os.path.join(*tuple(path.split('/')))
    # HACK: on Linux, a leading / gets lost...
    if path.startswith('/'):
        st = '/' + st
    return st
class MySplashScreen(SplashScreen):
    def __init__(self):
        bmp = wx.Image(opj("bitmaps/splash.jpg")).ConvertToBitmap()
        SplashScreen.__init__(self, bmp,
                              wx.adv.SPLASH_CENTRE_ON_SCREEN | wx.adv.SPLASH_TIMEOUT,
                              3000, None, -1)  # 这里的3000为splash窗口显示的时间，以毫秒为单位
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.fc = wx.CallLater(0,self.ShowMain)  # 这里的1000是ShowMain函数延迟多久被调用，这个数应该比前面的2000相等或小一点儿，形成程序后splash窗口才关闭的表象
    def OnClose(self, evt):
        # Make sure the default handler runs too so this window gets
        # destroyed
        evt.Skip()
        self.Hide()
        if self.fc.IsRunning():
            self.fc.Stop()
            self.ShowMain()
    def ShowMain(self):
        mainwin =MyAuiFrame(None, wx.ID_ANY, "  天外天定制家居智能生产管理系统                                                        天津定智科技有限公司 2018年10月   Version 0.181126B", size=(1500,700),style=wx.MAXIMIZE|wx.CAPTION|wx.CLOSE_BOX|wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX)
        mainwin.CenterOnParent(wx.BOTH)
        mainwin.Show()
        mainwin.Center(wx.BOTH)
        # mainwin.ShowFullScreen(1)
        if self.fc.IsRunning():
            self.Raise()
            # wx.CallAfter(mainwin.ShowTip)
class MyApp(wx.App, wx.lib.mixins.inspection.InspectionMixin):
    def OnInit(self):
        import images as i
        global images
        images = i
        splash = MySplashScreen()
        splash.Show()
        return True
def main():
    app = MyApp(False)   #MyApp类，定义在程序前部
    app.MainLoop()
if __name__ == '__main__':
    __name__ = 'Main'
    main()
