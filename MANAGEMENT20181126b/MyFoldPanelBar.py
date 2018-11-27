#!/usr/bin/env python
# _*_ coding: UTF-8 _*_

import wx.adv
from MyPane import *
from six import BytesIO
try:
    dirName = os.path.dirname(os.path.abspath(__file__))
except:
    dirName = os.path.dirname(os.path.abspath(sys.argv[0]))

sys.path.append(os.path.split(dirName)[0])
try:
    from agw import foldpanelbar as fpb
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.foldpanelbar as fpb

def GetCollapsedIconData():
    return \
b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\
\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\
\x00\x01\x8eIDAT8\x8d\xa5\x93-n\xe4@\x10\x85?g\x03\n6lh)\xc4\xd2\x12\xc3\x81\
\xd6\xa2I\x90\x154\xb9\x81\x8f1G\xc8\x11\x16\x86\xcd\xa0\x99F\xb3A\x91\xa1\
\xc9J&\x96L"5lX\xcc\x0bl\xf7v\xb2\x7fZ\xa5\x98\xebU\xbdz\xf5\\\x9deW\x9f\xf8\
H\\\xbfO|{y\x9dT\x15P\x04\x01\x01UPUD\x84\xdb/7YZ\x9f\xa5\n\xce\x97aRU\x8a\
\xdc`\xacA\x00\x04P\xf0!0\xf6\x81\xa0\xf0p\xff9\xfb\x85\xe0|\x19&T)K\x8b\x18\
\xf9\xa3\xe4\xbe\xf3\x8c^#\xc9\xd5\n\xa8*\xc5?\x9a\x01\x8a\xd2b\r\x1cN\xc3\
\x14\t\xce\x97a\xb2F0Ks\xd58\xaa\xc6\xc5\xa6\xf7\xdfya\xe7\xbdR\x13M2\xf9\
\xf9qKQ\x1fi\xf6-\x00~T\xfac\x1dq#\x82,\xe5q\x05\x91D\xba@\xefj\xba1\xf0\xdc\
zzW\xcff&\xb8,\x89\xa8@Q\xd6\xaaf\xdfRm,\xee\xb1BDxr#\xae\xf5|\xddo\xd6\xe2H\
\x18\x15\x84\xa0q@]\xe54\x8d\xa3\xedf\x05M\xe3\xd8Uy\xc4\x15\x8d\xf5\xd7\x8b\
~\x82\x0fh\x0e"\xb0\xad,\xee\xb8c\xbb\x18\xe7\x8e;6\xa5\x89\x04\xde\xff\x1c\
\x16\xef\xe0p\xfa>\x19\x11\xca\x8d\x8d\xe0\x93\x1b\x01\xd8m\xf3(;x\xa5\xef=\
\xb7w\xf3\x1d$\x7f\xc1\xe0\xbd\xa7\xeb\xa0(,"Kc\x12\xc1+\xfd\xe8\tI\xee\xed)\
\xbf\xbcN\xc1{D\x04k\x05#\x12\xfd\xf2a\xde[\x81\x87\xbb\xdf\x9cr\x1a\x87\xd3\
0)\xba>\x83\xd5\xb97o\xe0\xaf\x04\xff\x13?\x00\xd2\xfb\xa9`z\xac\x80w\x00\
\x00\x00\x00IEND\xaeB`\x82'
def GetCollapsedIconBitmap():
    return wx.Bitmap(GetCollapsedIconImage())
def GetCollapsedIconImage():
    stream = BytesIO(GetCollapsedIconData())
    return wx.Image(stream)
def GetExpandedIconData():
    return \
b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\
\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\
\x00\x01\x9fIDAT8\x8d\x95\x93\xa1\x8e\xdc0\x14EO\xb2\xc4\xd0\xd2\x12\xb7(mI\
\xa4%V\xd1lQT4[4-\x9a\xfe\xc1\xc2|\xc6\xc2~BY\x83:A3E\xd3\xa0*\xa4\xd2\x90H!\
\x95\x0c\r\r\x1fK\x81g\xb2\x99\x84\xb4\x0fY\xd6\xbb\xc7\xf7>=\'Iz\xc3\xbcv\
\xfbn\xb8\x9c\x15 \xe7\xf3\xc7\x0fw\xc9\xbc7\x99\x03\x0e\xfbn0\x99F+\x85R\
\x80RH\x10\x82\x08\xde\x05\x1ef\x90+\xc0\xe1\xd8\ryn\xd0Z-\\A\xb4\xd2\xf7\
\x9e\xfbwoF\xc8\x088\x1c\xbbae\xb3\xe8y&\x9a\xdf\xf5\xbd\xe7\xfem\x84\xa4\
\x97\xccYf\x16\x8d\xdb\xb2a]\xfeX\x18\xc9s\xc3\xe1\x18\xe7\x94\x12cb\xcc\xb5\
\xfa\xb1l8\xf5\x01\xe7\x84\xc7\xb2Y@\xb2\xcc0\x02\xb4\x9a\x88%\xbe\xdc\xb4\
\x9e\xb6Zs\xaa74\xadg[6\x88<\xb7]\xc6\x14\x1dL\x86\xe6\x83\xa0\x81\xba\xda\
\x10\x02x/\xd4\xd5\x06\r\x840!\x9c\x1fM\x92\xf4\x86\x9f\xbf\xfe\x0c\xd6\x9ae\
\xd6u\x8d \xf4\xf5\x165\x9b\x8f\x04\xe1\xc5\xcb\xdb$\x05\x90\xa97@\x04lQas\
\xcd*7\x14\xdb\x9aY\xcb\xb8\\\xe9E\x10|\xbc\xf2^\xb0E\x85\xc95_\x9f\n\xaa/\
\x05\x10\x81\xce\xc9\xa8\xf6><G\xd8\xed\xbbA)X\xd9\x0c\x01\x9a\xc6Q\x14\xd9h\
[\x04\xda\xd6c\xadFkE\xf0\xc2\xab\xd7\xb7\xc9\x08\x00\xf8\xf6\xbd\x1b\x8cQ\
\xd8|\xb9\x0f\xd3\x9a\x8a\xc7\x08\x00\x9f?\xdd%\xde\x07\xda\x93\xc3{\x19C\
\x8a\x9c\x03\x0b8\x17\xe8\x9d\xbf\x02.>\x13\xc0n\xff{PJ\xc5\xfdP\x11""<\xbc\
\xff\x87\xdf\xf8\xbf\xf5\x17FF\xaf\x8f\x8b\xd3\xe6K\x00\x00\x00\x00IEND\xaeB\
`\x82'
def GetExpandedIconBitmap():
    return wx.Bitmap(GetExpandedIconImage())
def GetExpandedIconImage():
    stream = BytesIO(GetExpandedIconData())
    return wx.Image(stream)
def GetMondrianData():
    return \
b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00 \x00\x00\x00 \x08\x06\x00\
\x00\x00szz\xf4\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\x00\x00qID\
ATX\x85\xed\xd6;\n\x800\x10E\xd1{\xc5\x8d\xb9r\x97\x16\x0b\xad$\x8a\x82:\x16\
o\xda\x84pB2\x1f\x81Fa\x8c\x9c\x08\x04Z{\xcf\xa72\xbcv\xfa\xc5\x08 \x80r\x80\
\xfc\xa2\x0e\x1c\xe4\xba\xfaX\x1d\xd0\xde]S\x07\x02\xd8>\xe1wa-`\x9fQ\xe9\
\x86\x01\x04\x10\x00\\(Dk\x1b-\x04\xdc\x1d\x07\x14\x98;\x0bS\x7f\x7f\xf9\x13\
\x04\x10@\xf9X\xbe\x00\xc9 \x14K\xc1<={\x00\x00\x00\x00IEND\xaeB`\x82'
def GetMondrianBitmap():
    return wx.Bitmap(GetMondrianImage())
def GetMondrianImage():
    stream = BytesIO(GetMondrianData())
    return wx.Image(stream)
def GetMondrianIcon():
    icon = wx.Icon()
    icon.CopyFromBitmap(GetMondrianBitmap())
    return icon
class Collapsed(wx.Frame):

    def __init__(self, parent, id=wx.ID_ANY, title="", pos=wx.DefaultPosition,
                 size=(400,300), style=wx.DEFAULT_FRAME_STYLE):

        wx.Frame.__init__(self, parent, id, title, pos, size, style)

        self.SetIcon(GetMondrianIcon())
        self.SetMenuBar(self.CreateMenuBar())

        self.statusbar = self.CreateStatusBar(2)
        self.statusbar.SetStatusWidths([-4, -3])
        self.statusbar.SetStatusText("Andrea Gavana @ 23 Mar 2005", 0)
        self.statusbar.SetStatusText("Welcome to wxPython!", 1)

        self.CreateFoldBar()


    def CreateFoldBar(self, vertical=True):

        if vertical:
            self.SetSize((500,600))
        else:
            self.SetSize((700,300))

        newstyle = (vertical and [fpb.FPB_VERTICAL] or [fpb.FPB_HORIZONTAL])[0]

        bar = fpb.FoldPanelBar(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                               agwStyle=fpb.FPB_COLLAPSE_TO_BOTTOM|newstyle)

        item = bar.AddFoldPanel("Test me", collapsed=False)
        button1 = wx.Button(item, wx.ID_ANY, "Collapse Me")
        button1.Bind(wx.EVT_BUTTON, self.OnCollapseMe)

        bar.AddFoldPanelWindow(item, button1, fpb.FPB_ALIGN_LEFT)

        item = bar.AddFoldPanel("Test me too!", collapsed=True)

        button2 = wx.Button(item, wx.ID_ANY, "Expand First One")
        button2.Bind(wx.EVT_BUTTON, self.OnExpandMe)

        bar.AddFoldPanelWindow(item, button2)
        bar.AddFoldPanelSeparator(item)

        newfoldpanel = FoldTestPanel(item, wx.ID_ANY)
        bar.AddFoldPanelWindow(item, newfoldpanel)

        bar.AddFoldPanelSeparator(item)

        bar.AddFoldPanelWindow(item, wx.TextCtrl(item, wx.ID_ANY, "Comment"),
                               fpb.FPB_ALIGN_LEFT, fpb.FPB_DEFAULT_SPACING, 20)

        item = bar.AddFoldPanel("Some Opinions ...", collapsed=False)
        bar.AddFoldPanelWindow(item, wx.CheckBox(item, wx.ID_ANY, "I Like This"))

        if vertical:
            # do not add this for horizontal for better presentation
            bar.AddFoldPanelWindow(item, wx.CheckBox(item, wx.ID_ANY, "And also this"))
            bar.AddFoldPanelWindow(item, wx.CheckBox(item, wx.ID_ANY, "And gimme this too"))

        bar.AddFoldPanelSeparator(item)

        bar.AddFoldPanelWindow(item, wx.CheckBox(item, wx.ID_ANY, "Check this too if you like"))

        if vertical:
            # do not add this for horizontal for better presentation
            bar.AddFoldPanelWindow(item, wx.CheckBox(item, wx.ID_ANY, "What about this"))

        item = bar.AddFoldPanel("Choose one ...", collapsed=False)
        bar.AddFoldPanelWindow(item, wx.StaticText(item, wx.ID_ANY, "Enter your comment"))
        bar.AddFoldPanelWindow(item, wx.TextCtrl(item, wx.ID_ANY, "Comment"),
                               fpb.FPB_ALIGN_WIDTH, fpb.FPB_DEFAULT_SPACING, 20)

        if hasattr(self, "pnl"):
            self.pnl.Destroy()

        self.pnl = bar

        size = self.GetClientSize()
        self.pnl.SetSize(0, 0, size.GetWidth(), size.GetHeight())


    def CreateMenuBar(self):

        FoldPanelBarTest_Quit = wx.NewId()
        FoldPanelBarTest_About = wx.NewId()
        FoldPanelBarTest_Horizontal = wx.NewId()
        FoldPanelBarTest_Vertical = wx.NewId()

        menuFile = wx.Menu()
        menuFile.Append(FoldPanelBarTest_Horizontal, "&Horizontal\tAlt-H")
        menuFile.Append(FoldPanelBarTest_Vertical, "&Vertical\tAlt-V")
        menuFile.AppendSeparator()
        menuFile.Append(FoldPanelBarTest_Quit, "E&xit\tAlt-X", "Quit This Program")

        helpMenu = wx.Menu()
        helpMenu.Append(FoldPanelBarTest_About, "&About...\tF1", "Show About Dialog")

        self.FoldPanelBarTest_Vertical = FoldPanelBarTest_Vertical
        self.FoldPanelBarTest_Horizontal = FoldPanelBarTest_Horizontal

        self.Bind(wx.EVT_MENU, self.OnQuit, id=FoldPanelBarTest_Quit)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=FoldPanelBarTest_About)
        self.Bind(wx.EVT_MENU, self.OnOrientation, id=FoldPanelBarTest_Horizontal)
        self.Bind(wx.EVT_MENU, self.OnOrientation, id=FoldPanelBarTest_Vertical)

        value = wx.MenuBar()
        value.Append(menuFile, "&File")
        value.Append(helpMenu, "&Help")

        return value


    def OnOrientation(self, event):
        self.CreateFoldBar(event.GetId() == self.FoldPanelBarTest_Vertical)


    def OnQuit(self, event):
        # True is to force the frame to close
        self.Close(True)


    def OnAbout(self, event):

        msg = "This is the about dialog of the FoldPanelBarTest application.\n\n" + \
              "Welcome To wxPython " + wx.VERSION_STRING + "!!"
        dlg = wx.MessageDialog(self, msg, "About FoldPanelBarTest",
                               wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()


    def OnCollapseMe(self, event):

        item = self.pnl.GetFoldPanel(0)
        self.pnl.Collapse(item)

    def OnExpandMe(self, event):

        self.pnl.Expand(self.pnl.GetFoldPanel(0))
        self.pnl.Collapse(self.pnl.GetFoldPanel(1))
class NotCollapsed(wx.Frame):
    def __init__(self, parent, id=wx.ID_ANY, title="", pos=wx.DefaultPosition,
                 size=(400,300), style=wx.DEFAULT_FRAME_STYLE):

        wx.Frame.__init__(self, parent, id, title, pos, size, style)

        self.SetIcon(GetMondrianIcon())
        self.SetMenuBar(self.CreateMenuBar())

        self.statusbar = self.CreateStatusBar(2)
        self.statusbar.SetStatusWidths([-4, -3])
        self.statusbar.SetStatusText("Andrea Gavana @ 23 Mar 2005", 0)
        self.statusbar.SetStatusText("Welcome to wxPython!", 1)

        pnl = fpb.FoldPanelBar(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                               agwStyle=fpb.FPB_VERTICAL)

        item = pnl.AddFoldPanel("Test Me", collapsed=False)

        button1 = wx.Button(item, wx.ID_ANY, "Collapse Me")

        pnl.AddFoldPanelWindow(item, button1, fpb.FPB_ALIGN_LEFT)
        pnl.AddFoldPanelSeparator(item)

        button1.Bind(wx.EVT_BUTTON, self.OnCollapseMe)

        item = pnl.AddFoldPanel("Test Me Too!", collapsed=True)
        button2 = wx.Button(item, wx.ID_ANY, "Expand First One")
        pnl.AddFoldPanelWindow(item, button2, fpb.FPB_ALIGN_LEFT)
        pnl.AddFoldPanelSeparator(item)

        button2.Bind(wx.EVT_BUTTON, self.OnExpandMe)

        newfoldpanel = FoldTestPanel(item, wx.ID_ANY)
        pnl.AddFoldPanelWindow(item, newfoldpanel)

        pnl.AddFoldPanelSeparator(item)

        pnl.AddFoldPanelWindow(item, wx.TextCtrl(item, wx.ID_ANY, "Comment"),
                               fpb.FPB_ALIGN_LEFT, fpb.FPB_DEFAULT_SPACING, 20)

        item = pnl.AddFoldPanel("Some Opinions ...", collapsed=False)
        pnl.AddFoldPanelWindow(item, wx.CheckBox(item, wx.ID_ANY, "I Like This"))
        pnl.AddFoldPanelWindow(item, wx.CheckBox(item, wx.ID_ANY, "And Also This"))
        pnl.AddFoldPanelWindow(item, wx.CheckBox(item, wx.ID_ANY, "And Gimme This Too"))

        pnl.AddFoldPanelSeparator(item)

        pnl.AddFoldPanelWindow(item, wx.CheckBox(item, wx.ID_ANY, "Check This Too If You Like"))
        pnl.AddFoldPanelWindow(item, wx.CheckBox(item, wx.ID_ANY, "What About This"))

        item = pnl.AddFoldPanel("Choose One ...", collapsed=False)
        pnl.AddFoldPanelWindow(item, wx.StaticText(item, wx.ID_ANY, "Enter Your Comment"))
        pnl.AddFoldPanelWindow(item, wx.TextCtrl(item, wx.ID_ANY, "Comment"),
                               fpb.FPB_ALIGN_WIDTH, fpb.FPB_DEFAULT_SPACING, 20, 20)
        self.pnl = pnl


    def CreateMenuBar(self):

        FoldPanelBarTest_Quit = wx.NewId()
        FoldPanelBarTest_About = wx.NewId()

        menuFile = wx.Menu()
        menuFile.Append(FoldPanelBarTest_Quit, "E&xit\tAlt-X", "Quit This Program")

        helpMenu = wx.Menu()
        helpMenu.Append(FoldPanelBarTest_About, "&About...\tF1", "Show About Dialog")

        self.Bind(wx.EVT_MENU, self.OnQuit, id=FoldPanelBarTest_Quit)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=FoldPanelBarTest_About)

        value = wx.MenuBar()
        value.Append(menuFile, "&File")
        value.Append(helpMenu, "&Help")

        return value


    # Event Handlers

    def OnQuit(self, event):

        # True is to force the frame to close
        self.Close(True)


    def OnAbout(self, event):

        msg = "This is the about dialog of the FoldPanelBarTest application.\n\n" + \
              "Welcome To wxPython " + wx.VERSION_STRING + "!!"
        dlg = wx.MessageDialog(self, msg, "About FoldPanelBarTest",
                               wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()


    def OnCollapseMe(self, event):

        item = self.pnl.GetFoldPanel(0)
        self.pnl.Collapse(item)

    def OnExpandMe(self, event):

        self.pnl.Expand(self.pnl.GetFoldPanel(0))
        self.pnl.Collapse(self.pnl.GetFoldPanel(1))

