#!/usr/bin/env python
# _*_ coding: UTF-8 _*_
import wx
import time
import datetime
import MySQLdb
from ID_DEFINE import *
class MyLog(wx.Log):
    def __init__(self, textCtrl, logTime=0):
        wx.Log.__init__(self)
        self.tc = textCtrl
        self.logTime = logTime

    def DoLogText(self, message):
        if self.tc:
            self.tc.AppendText(message + '\n')
class MyTextCtrl(wx.TextCtrl):
    def __init__(self, parent,id=-1,title="",position=wx.Point(0,0),size=wx.Size(150,90),style=wx.NO_BORDER | wx.TE_MULTILINE|wx.TE_READONLY):
        self.parent=parent
        wx.TextCtrl.__init__(self, parent,id,title, position,size,style)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_DCLICK,self.OnLeftDown)
        # self.My_timer = wx.PyTimer(self.My_Notify)  # 添加时间事件，制定时间事件处理函数为My_Notify（）
        # self.My_timer.Start(1000)  # 设定计时间隔为1秒
        # self.t = time.localtime(time.time())
        # self.filename = time.strftime("%Y%m%d%H.log", self.t)
        # repeat=0
    def OnLeftDown(self,evt):
        pass
    def SaveLogFile(self):
        t = time.localtime(time.time())
        filename = time.strftime("%Y%m%d%H.log", t)
        file=open(filename,'w+')
        content=self.GetValue().encode('UTF-8')
        file.write(content)
        file.close()
        self.SetValue("")
    def WriteText(self, text, enable=True, font=wx.NORMAL_FONT, colour=wx.BLACK):
        if (enable):
            t = time.localtime(time.time())
            st = time.strftime("%Y年%m月%d日 %H:%M:%S  ", t)
            # db = MySQLdb.connect(host=local_server_ip, user=local_user_list[0], passwd=local_password, db=local_database[0], charset=charset)
            # cursor = db.cursor()
            # sql1 = "INSERT INTO `info_log`(`error_occurance_time`,`event`)VALUES('%s','%s')"%(datetime.datetime.now(),text)
            # cursor.execute(sql1)
            # db.commit()
            text = st + text
            # wx.TextCtrl.SetFont(self, font)
            # wx.TextCtrl.SetForegroundColour(self, colour)
            # wx.TextCtrl.SetBackgroundColour(self,backgroundcolour)
            try:
                wx.TextCtrl.WriteText(self, text)
            except:
                pass
