#!/usr/bin/env python
# _*_ coding: UTF-8 _*_
import wx
from ProgressGauge import ProgressGauge
import time
import MySQLdb
from ID_DEFINE import *
RELATIVEWIDTHS = False
def Is_Database_Connect():
    try:
        global DB
        DB = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0], charset=charset)
        return True
    except:
        return False
class MyStatusBar(wx.StatusBar):
    def __init__(self, parent):
        wx.StatusBar.__init__(self, parent, -1,style = wx.STB_SIZEGRIP)
        self.second=0
        # This status bar has three fields
        self.SetFieldsCount(5)
        if RELATIVEWIDTHS:
            # Sets the three fields to be relative widths to each other.
            self.SetStatusWidths([-2, -1,-2, -2,-2])
        else:
            self.SetStatusWidths([100,-2,280,90, 140])
        self.sizeChanged = False
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_IDLE, self.OnIdle)
        # Field 0 ... just text
        self.SetStatusText("天外天定制家居智能生产管理系统正在运行.....         ", 1)
        vbox=wx.BoxSizer()
        # This will fall into field 1 (the second field)
        # self.cb = wx.CheckBox(self, 1001, "开启报警事件")
        # self.Bind(wx.EVT_CHECKBOX, self.OnToggleClock, self.cb)
        # self.cb.SetValue(False)
        self.gauge = ProgressGauge(self,size=(55, 15))
        # set the initial position of the checkbox
        self.Reposition()
        # We're going to use a timer to drive a 'clock' in the last field.
        self.timer = wx.PyTimer(self.Notify)
        self.timer.Start(100)
        # self.timer1(60)
        # self.Notify()
        # self.My_timer_Remain = wx.PyTimer(self.My_Notify_Remain_task)  # 添加时间事件，制定时间事件处理函数为My_Notify（）
        # self.My_timer_Remain.Start(2000)  # 设定计时间隔为2000毫秒
        # self.StatisticsOnlineArea()
    # Handles events from the timer we started in __init__().
    # We're using it to drive a 'clock' in field 2 (the third field).
    def Notify(self):
        try:
            self.second+=1
            t = time.localtime(time.time())
            st = time.strftime("%Y年%m月%d日 %H:%M:%S", t)
            self.SetStatusText(st, 4)
            self.gauge.Pulse()
            if self.second==600:
                if Is_Database_Connect():
                    cursor = DB.cursor()
                    cursor.execute("select SUM(Order_area),COUNT(Order_id) from `order_order_online` where 1 ")
                    record = cursor.fetchone()
                    if record[1]==0:
                        area='0'
                    else:
                        # area=record[0]
                        area = round(record[0], 2)
                    OnlineArea="当前在线订单" +str(record[1])+"个   在线面积" + str(area)+"平"
                    self.SetStatusText(OnlineArea, 2)
                    self.gauge.Pulse()
                    self.second=0
            # print '78',self.second
        except:
            self.timer.Stop()
    def Name(self,name):
        try:
            self.SetStatusText(name, 3)
            self.gauge.Pulse()
        except:
            self.timer.Stop()

    def OnSize(self, evt):
        evt.Skip()
        self.Reposition()  # for normal size events
        # Set a flag so the idle time handler will also do the repositioning.
        # It is done this way to get around a buglet where GetFieldRect is not
        # accurate during the EVT_SIZE resulting from a frame maximize.
        self.sizeChanged = True


    def OnIdle(self, evt):
        if self.sizeChanged:
            self.Reposition()


    # reposition the checkbox
    def Reposition(self):
        rect = self.GetFieldRect(2)
        rect.x += 1
        rect.y += 1
        # self.cb.SetRect(rect)
        rect = self.GetFieldRect(0)
        rect=(5,4,100,18)
        self.gauge.SetRect(rect)
        self.sizeChanged = False
