#!/usr/bin/env python
# _*_ coding: UTF-8 _*_
import os
import sys
import wx
import MySQLdb
import time
import datetime
from wx.adv import CalendarCtrl, GenericCalendarCtrl, CalendarDateAttr
# import wx.lib.popupctl as pop
#
# import wx.grid as gridlib
# from read import Read
import wx.lib.popupctl as pop
try:
    dirName = os.path.dirname(os.path.abspath(__file__))
except:
    dirName = os.path.dirname(os.path.abspath(sys.argv[0]))
bitmapDir = os.path.join(dirName, 'bitmaps')
sys.path.append(os.path.split(dirName)[0])
try:
    from agw import aquabutton as AB
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.aquabutton as AB
class LYB_Search_TopPanel(wx.Panel):
    def __init__(self, parent,log):
        self.log = log
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition,
                          wx.DefaultSize)
        self.dict = {}
        # self.staticbox_sort = wx.StaticBox(self, -1)
        # self.staticboxsizer_sort=wx.StaticBoxSizer(self.staticbox_sort)
        # self.staticboxsizer_sort_v1=wx.BoxSizer(wx.VERTICAL)
        # self.staticboxsizer_sort_v2=wx.BoxSizer(wx.VERTICAL)
        # self.unappeared=wx.CheckBox(self,-1,"未出工单")
        # self.unappeared.SetValue(True)
        # self.appeared=wx.CheckBox(self,-1,"已出工单")
        # self.appeared.SetValue(True)
        # self.unfinished=wx.CheckBox(self,-1,"未完成工单")
        # self.unfinished.SetValue(True)
        # self.finished=wx.CheckBox(self,-1,"已完成工")
        # self.finished.SetValue(True)
        # self.errored=wx.CheckBox(self,-1,"出错工单")
        # self.errored.SetValue(True)
        # self.Bind(wx.EVT_CHECKBOX, self.Start_Browse, self.unappeared)
        # self.Bind(wx.EVT_CHECKBOX, self.Start_Browse, self.appeared)
        # self.Bind(wx.EVT_CHECKBOX, self.Start_Browse, self.finished)
        # self.Bind(wx.EVT_CHECKBOX, self.Start_Browse, self.unfinished)
        # self.Bind(wx.EVT_CHECKBOX, self.Start_Browse, self.errored)
        #
        # self.staticboxsizer_sort_v1.Add(self.unappeared,0,wx.ALL,5)
        # self.staticboxsizer_sort_v1.Add(self.appeared,0,wx.ALL,5)
        # self.staticboxsizer_sort_v1.Add(self.unfinished,0,wx.ALL,5)
        # self.staticboxsizer_sort_v1.Add(self.finished,0,wx.ALL,5)
        # self.staticboxsizer_sort_v1.Add(self.errored,0,wx.ALL,5)
        # btn1=wx.Button(self,-1,"默认")
        # btn1.Bind(wx.EVT_BUTTON,self.On_Button_Default)#########
        # btn2=wx.Button(self,-1,"全选")
        # btn2.Bind(wx.EVT_BUTTON,self.On_Button_Default)
        # btn3=wx.Button(self,-1,"全清")
        # btn3.Bind(wx.EVT_BUTTON,self.On_Button_ClearAll)
        # self.staticboxsizer_sort_v2.Add(btn1,0,wx.ALL,5)
        # self.staticboxsizer_sort_v2.Add(btn2,0,wx.ALL,5)
        # self.staticboxsizer_sort_v2.Add(btn3,0,wx.ALL,5)
        # self.staticboxsizer_sort.Add(self.staticboxsizer_sort_v1)
        # self.staticboxsizer_sort.Add(self.staticboxsizer_sort_v2)
        self.hbox=wx.BoxSizer()
        # self.hbox.Add(self.staticboxsizer_sort,proportion=0,flag=wx.EXPAND|wx.ALL,border=3)
        self.staticbox_date = wx.StaticBox(self, -1)
        self.staticboxsizer_date=wx.StaticBoxSizer(self.staticbox_date,wx.HORIZONTAL)
        #静态wx.HORIZONTAL水平放时间、合同查询、订单查询控件的盒子

        self.staticbox_time = wx.StaticBox(self, -1)#垂直wx.VERTICAL存放'从:起始时间'、'至:截止时间'
        self.staticboxsizer_time = wx.StaticBoxSizer(self.staticbox_time, wx.VERTICAL)
        self.staticbox_time_1 = wx.StaticBox(self, -1)
        self.staticboxsizer_time_1 = wx.StaticBoxSizer(self.staticbox_time_1, wx.HORIZONTAL)
        self.statictext1=wx.StaticText(self,label="从：")#分别水平放'从:起始时间'、'至:截止时间'后，将两个盒子垂直放，最后跟其他盒子一起水平放
        self.date_begin = PopDateControl(self, -1, pos=(10, 10))
        self.staticboxsizer_time_1.Add(self.statictext1, border=3)
        self.staticboxsizer_time_1.Add(self.date_begin, border=3)
        self.staticbox_time_2 = wx.StaticBox(self, -1)
        self.staticboxsizer_time_2 = wx.StaticBoxSizer(self.staticbox_time_2, wx.HORIZONTAL)
        self.statictext2=wx.StaticText(self,label="至：")
        self.date_end = PopDateControl(self, -1, pos=(10, 10))

        self.staticboxsizer_time_2.Add(self.statictext2,border=3)
        self.staticboxsizer_time_2.Add(self.date_end,border=3)
        self.staticboxsizer_time.Add(self.staticboxsizer_time_1, proportion=0,flag=wx.EXPAND, border=3)
        self.staticboxsizer_time.Add(self.staticboxsizer_time_2, proportion=0,flag=wx.EXPAND, border=3)
        self.staticboxsizer_date.Add(self.staticboxsizer_time, proportion=0,flag=wx.EXPAND, border=3)

        # self.hbox.Add(self.staticboxsizer_date,flag=wx.EXPAND,border=3)#添加合同查询的控件
        self.staticbox_contract = wx.StaticBox(self, -1)  # 垂直存放查询合同号控件
        self.staticboxsizer_contract = wx.StaticBoxSizer(self.staticbox_contract, wx.VERTICAL)
        self.statictext3 = wx.StaticText(self, label="选择查询的合同号：")
        self.contract_combox = wx.ComboBox(self, -1, pos=(20, 10))
        self.staticboxsizer_contract.Add(self.statictext3, proportion=0,flag=wx.ALIGN_CENTER|wx.ALL, border=3)
        self.staticboxsizer_contract.Add(self.contract_combox, proportion=0,flag=wx.ALIGN_CENTER|wx.ALL, border=3)
        self.staticboxsizer_date.Add(self.staticboxsizer_contract, proportion=1,flag=wx.EXPAND, border=3)
        #proportion=1,flag=wx.EXPAND几个查询盒子在整个静态盒子中按1：1比例水平放置

        self.staticbox_order = wx.StaticBox(self, -1)  # 垂直存放起始时间
        self.staticboxsizer_order = wx.StaticBoxSizer(self.staticbox_order, wx.VERTICAL)
        self.statictext4 = wx.StaticText(self, label="选择查询的订单号：")#添加订单查询的控件
        self.order_combox = wx.ComboBox(self, -1, pos=(20, 10))
        self.staticboxsizer_order.Add(self.statictext4, proportion=0,flag=wx.ALIGN_CENTER|wx.ALL, border=3)
        self.staticboxsizer_order.Add(self.order_combox, proportion=0,flag=wx.ALIGN_CENTER|wx.ALL, border=3)
        self.staticboxsizer_date.Add(self.staticboxsizer_order, proportion=1,flag=wx.EXPAND, border=3)

        self.staticbox_component = wx.StaticBox(self, -1)  # 垂直存放起始时间
        self.staticboxsizer_component = wx.StaticBoxSizer(self.staticbox_component, wx.VERTICAL)#垂直放选择查询的组件号：combobox
        self.statictext5 = wx.StaticText(self, label="选择查询的组件号：")#添加组件查询的控件
        self.component_combox = wx.ComboBox(self, -1, pos=(20, 10))
        self.staticboxsizer_component.Add(self.statictext5, proportion=0,flag=wx.ALIGN_CENTER|wx.ALL, border=3)
        self.staticboxsizer_component.Add(self.component_combox, proportion=0,flag=wx.ALIGN_CENTER|wx.ALL, border=3)#添加查询控件到
        self.staticboxsizer_date.Add(self.staticboxsizer_component, proportion=1,flag=wx.EXPAND, border=3)#添加查询控件到
          # 添加组件查询的控件staticbox_date盒子中，再添加到wx.BoxSizer()中

        self.staticbox_number_x = wx.StaticBox(self, -1)  # 垂直存放x:文本框z:文本框
        self.staticboxsizer_number_x = wx.StaticBoxSizer(self.staticbox_number_x, wx.VERTICAL)
        self.staticbox_time_number_x_1 = wx.StaticBox(self, -1)
        self.staticboxsizer_number_x_1 = wx.StaticBoxSizer(self.staticbox_time_number_x_1, wx.HORIZONTAL)
        self.statictext6 = wx.StaticText(self, label="界面中合同个数:")  # 分别水平放'从:起始时间'、'至:截止时间'
        self.number_x =wx.TextCtrl(self, -1, pos=(10, 10),size=(35,20))
        self.staticboxsizer_number_x_1.Add(self.statictext6, proportion=0,flag=wx.EXPAND, border=3)
        self.staticboxsizer_number_x_1.Add(self.number_x, proportion=0,flag=wx.EXPAND, border=3)
        self.staticbox_time_number_z = wx.StaticBox(self, -1)
        self.staticboxsizer_number_z = wx.StaticBoxSizer(self.staticbox_time_number_z, wx.HORIZONTAL)
        self.statictext7 = wx.StaticText(self, label="界面中组件个数个数:")
        self.number_z = wx.TextCtrl(self, -1, pos=(10, 10),size=(35,20))

        self.staticboxsizer_number_z.Add(self.statictext7, proportion=0,flag=wx.EXPAND, border=3)
        self.staticboxsizer_number_z.Add(self.number_z, proportion=0,flag=wx.EXPAND, border=3)
        self.staticboxsizer_number_x.Add(self.staticboxsizer_number_x_1, proportion=0,flag=wx.EXPAND, border=3)
        self.staticboxsizer_number_x.Add(self.staticboxsizer_number_z, proportion=0,flag=wx.EXPAND, border=3)
        self.staticboxsizer_date.Add(self.staticboxsizer_number_x, proportion=1,flag=wx.EXPAND, border=3)

        self.staticbox_number_y = wx.StaticBox(self, -1)  # 垂直存放y:文本框m:文本框
        self.staticboxsizer_number_y = wx.StaticBoxSizer(self.staticbox_number_y, wx.VERTICAL)
        self.staticbox_time_number_y_1 = wx.StaticBox(self, -1)
        self.staticboxsizer_number_y_1 = wx.StaticBoxSizer(self.staticbox_time_number_y_1, wx.HORIZONTAL)
        self.statictext8 = wx.StaticText(self, label="界面中订单个数:")  # 分别水平放'x:文本框'、'm:文本框'
        self.number_y = wx.TextCtrl(self, -1, pos=(10, 10),size=(35,20))
        self.staticboxsizer_number_y_1.Add(self.statictext8, proportion=0,flag=wx.EXPAND, border=3)
        self.staticboxsizer_number_y_1.Add(self.number_y, proportion=0,flag=wx.EXPAND, border=3)
        self.staticbox_time_number_m = wx.StaticBox(self, -1)
        self.staticboxsizer_number_m = wx.StaticBoxSizer(self.staticbox_time_number_m, wx.HORIZONTAL)
        self.statictext9 = wx.StaticText(self, label="界面中部件个数:")
        self.number_m = wx.TextCtrl(self, -1, pos=(10, 10),size=(35,20))

        self.staticboxsizer_number_m.Add(self.statictext9, proportion=0,flag=wx.EXPAND, border=3)
        self.staticboxsizer_number_m.Add(self.number_m, proportion=0,flag=wx.EXPAND, border=3)
        self.staticboxsizer_number_y.Add(self.staticboxsizer_number_y_1, proportion=0,flag=wx.EXPAND, border=3)
        self.staticboxsizer_number_y.Add(self.staticboxsizer_number_m, proportion=0,flag=wx.EXPAND, border=3)
        self.staticboxsizer_date.Add(self.staticboxsizer_number_y, proportion=1,flag=wx.EXPAND, border=3)

        self.hbox.Add(self.staticboxsizer_date, proportion=1,flag=wx.EXPAND|wx.ALL,border=3)



        self.bt_go=wx.Button(self,-1,label="检索",style=0)
        self.hbox.Add(self.bt_go,proportion=0,flag=wx.ALIGN_CENTRE ,border=3)
        self.SetSizer(self.hbox)
        self.bt_go.Bind(wx.EVT_BUTTON,self.Start_Browse)
        self.get_contract_id_list = []  # 初始化列表为空
        self.get_order_id_list = []
        self.get_component_id_list = []
        self.order_combox.Enable(False)
        self.component_combox.Enable(False)
        self.contract_combox.Bind(wx.EVT_COMBOBOX_DROPDOWN, self.contract_information_display)  #触发合同combobox下拉事件
        self.contract_combox.Bind(wx.EVT_COMBOBOX, self.contract_id_click)#触发合同combobox下拉框中内容被选中事件
        self.contract_combox.Bind(wx.EVT_TEXT,self.contract_text_change)#触发合同号combobox文本内容改变事件

        self.order_combox.Bind(wx.EVT_COMBOBOX_DROPDOWN, self.order_information_display)  #触发订单号combobox下拉事件
        self.order_combox.Bind(wx.EVT_COMBOBOX, self.order_id_click)#触发订单号combobox下拉框中内容被选中事件
        self.order_combox.Bind(wx.EVT_TEXT,self.order_text_change)#触发订单号combobox文本内容改变事件

        self.component_combox.Bind(wx.EVT_COMBOBOX_DROPDOWN, self.component_information_display)  #触发组件号combobox下拉事件
        # self.timer = wx.PyTimer(self.Contract_refresh)
        # self.timer.Start(5000)  # 设定计时间隔为10000毫秒
        # self.Contract_refresh()

    def contract_information_display(self,evt):#合同号combobox下拉列表时触发的事件
        self.get_contract_id_list=[]
        self.order_combox.Clear()#下拉列表筛选时，其下属combobox控件内容清零、且不使能
        self.component_combox.Clear()
        self.order_combox.Enable(False)  # 开始使订单查询不使能，当有部件号后使能
        self.component_combox.Enable(False)
        self.contract_combox.Clear()#初始化 清空合同号combobox
        db = MySQLdb.connect("localhost", "root", "12345678", "hanhai_manufacture",
                             charset='utf8')  # 打开数据库连接注charset是否需要
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        self.contract_combox.Append('ALL')
        cursor.execute(
            "SELECT `Contract_id` FROM `order_part_online` WHERE 1 ")
        get_contract_id = cursor.fetchall()  # 获取合同号

        for i in range(len(get_contract_id)):
            if get_contract_id[i][0] != None or get_contract_id[i][0] != '':
                if get_contract_id[i] not in self.get_contract_id_list:  # 对读到的单号去重后放入列表get_contract_id_list
                    self.get_contract_id_list.append(get_contract_id[i])#
        for i in range(len(self.get_contract_id_list)):
            self.contract_combox.Append(self.get_contract_id_list[i])  # 添加查询到的合同号到界面合同编号的combobox中
        db.close()

    def contract_id_click(self, evt):#当合同号combobox下拉框选择内容后触发的事件
        self.order_combox.Enable(True)
    def contract_text_change(self, evt):#当合同号combobox文本框内容改变后触发的事件
        contrct_text = self.contract_combox.GetValue()#当combobox文本框内容其下属combobox控件不使能
        if contrct_text == '':
            self.order_combox.Enable(False)
            self.component_combox.Enable(False)


    def order_information_display(self,evt):#订单号combobox下拉列表时触发的事件
        self.get_order_id_list=[]
        self.order_combox.Clear()# 初始化 清空组件号combobox
        self.component_combox.Clear()  # 下拉列表筛选时，其下属combobox控件内容清零、且不使能
        self.component_combox.Enable(False)
        db = MySQLdb.connect("localhost", "root", "12345678", "hanhai_manufacture",
                             charset='utf8')  # 打开数据库连接注charset是否需要
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        if self.contract_combox.GetValue() != '' and self.contract_combox.GetValue() != 'ALL':  # 当合同号不为空时，读取合同号对应的订单号
                self.order_combox.Append('ALL')
                cursor.execute(
                    "SELECT `Order_id` FROM `order_part_online` WHERE `Contract_id`='%s' " % self.contract_combox.GetValue())
                get_order_id = cursor.fetchall()  # 获取订单编号
                # for i in range(len(get_order_id)):
                #     if get_order_id[i][0] != None or get_order_id[i][0] != '':
                #         self.order_combox.Append(get_order_id[i][0])
                for i in range(len(get_order_id)):#对订单号去重 填入界面查询订单的combobox
                    if get_order_id[i][0] != None or get_order_id[i][0] != '':
                        if get_order_id[i] not in self.get_order_id_list:  # 对读到的单号去重
                            self.get_order_id_list.append(get_order_id[i])
                for i in range(len(self.get_order_id_list)):
                    self.order_combox.Append(self.get_order_id_list[i])  # 添加查询到的订单号到界面合同订单号的combobox中
        if self.contract_combox.GetValue() == 'ALL':
            self.order_combox.Append('ALL')
            for i in range(len(self.get_contract_id_list)):
                cursor.execute(
                    "SELECT `Order_id` FROM `order_part_online` WHERE `Contract_id`='%s' " % self.get_contract_id_list[
                        i])
                get_order_id = cursor.fetchall()  # 获取订单编号
                for k in range(len(get_order_id)):  # 对订单号去重 填入界面查询订单的combobox
                    if get_order_id[k][0] != None or get_order_id[k][0] != '':
                        if get_order_id[k] not in self.get_order_id_list:  # 对读到的单号去重
                            self.get_order_id_list.append(get_order_id[k])
            for i in range(len(self.get_order_id_list)):
                self.order_combox.Append(self.get_order_id_list[i])  # 添加查询到的订单号到界面合同订单号的combobox中

        db.close()
    def order_id_click(self, evt):#当合同号combobox下拉框选择内容后触发的事件
        self.component_combox.Enable(True)
    def order_text_change(self, evt):#当合同号combobox文本框内容改变后触发的事件
        order_text = self.order_combox.GetValue()
        if order_text == '':
            self.component_combox.Clear()
            self.component_combox.Enable(False)

    def component_information_display(self,evt):#组件号combobox下拉列表时触发的事件
        self.component_combox.Clear()
        db = MySQLdb.connect("localhost", "root", "12345678", "hanhai_manufacture",
                             charset='utf8')  # 打开数据库连接注charset是否需要
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        self.get_component_id_list=[]
        if self.order_combox.GetValue() != '' and self.order_combox.GetValue() != 'ALL':  # 当订单号不为空时，读取订单号对应的订单号
            self.component_combox.Append('ALL')
            cursor.execute(
                "SELECT `Sec_id` FROM `order_part_online` WHERE `Order_id`='%s' " % self.order_combox.GetValue())
            get_component_combox_id = cursor.fetchall()  # 获取组件编号
            for i in range(len(get_component_combox_id)):  # 对订单号去重 填入界面查询订单的combobox
                if get_component_combox_id[i][0] != None or get_component_combox_id[i][0] != '':
                    if get_component_combox_id[i] not in self.get_component_id_list:  # 对读到的组件号去重
                        self.get_component_id_list.append(get_component_combox_id[i])
            for i in range(len(self.get_component_id_list)):
                self.component_combox.Append(self.get_component_id_list[i])#把去重后单号数据放入界面查询控件的文本框中
        if self.order_combox.GetValue() == 'ALL':  # 当订单号不为空时，读取订单号对应的订单号
            self.component_combox.Append('ALL')
            for i in range(len(self.get_order_id_list)):
                cursor.execute(
                    "SELECT `Sec_id` FROM `order_part_online` WHERE `Order_id`='%s' " % self.get_order_id_list[i])
                get_component_combox_id = cursor.fetchall()  # 获取组件编号
                for i in range(len(get_component_combox_id)):  # 对订单号去重 填入界面查询订单的combobox
                    if get_component_combox_id[i][0] != None or get_component_combox_id[i][0] != '':
                        if get_component_combox_id[i] not in self.get_component_id_list:  # 对读到的组件号去重
                            self.get_component_id_list.append(get_component_combox_id[i])
            for i in range(len(self.get_component_id_list)):
                self.component_combox.Append(self.get_component_id_list[i])#把去重后单号数据放入界面查询控件的文本框中

        db.close()




    def On_Button_Default(self,e):#做信息查询部分程序
        # self.appeared.SetValue(True)
        # self.unappeared.SetValue(True)
        # self.unfinished.SetValue(True)
        # self.finished.SetValue(True)
        # self.errored.SetValue(True)
        self.Start_Browse(e)
    def On_Button_ClearAll(self,e):
        # self.appeared.SetValue(False)
        # self.unappeared.SetValue(False)
        # self.unfinished.SetValue(False)
        # self.finished.SetValue(False)
        # self.errored.SetValue(False)
        self.Start_Browse(e)

    def Start_Browse(self,e):#点击检索后的执行函数
    #     # self.MyChoice = "操作员选择对包装工位中"
        print 1
        self.get_part_id_list=[]
        begin_time = self.date_begin.GetValue()
        end_time = self.date_end.GetValue()
    #当有合同号或者订单号或者组件号时从`order_part_online`查询部件号
        db = MySQLdb.connect("localhost", "root", "12345678", "hanhai_manufacture",
                             charset='utf8')  # 打开数据库连接注charset是否需要
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        if 'ALL' in self.contract_combox.GetValue():
            if 'ALL' in self.order_combox.GetValue():
                if 'ALL' in self.component_combox.GetValue():
                    for i in range(len(self.get_order_id_list)):
                        cursor.execute(
                            "SELECT `Part_id` FROM `order_part_online` WHERE `Order_id`='%s' "%self.get_order_id_list[i])
                        get_part_id=cursor.fetchall()  # 获取部件编号
                        self.get_part_id_list.append(get_part_id)
                    print self.get_part_id_list
                    self.query_fill_information()
                    self.timer = wx.PyTimer(self.query_fill_information())
                    self.timer.Start(10000)  # 设定计时间隔为10000毫秒


    #     if begin_time=='' and end_time=='':
    def query_fill_information(self):
        db = MySQLdb.connect("localhost", "root", "12345678", "hanhai_manufacture",
                             charset='utf8')  # 打开数据库连接注charset是否需要
        db_management = MySQLdb.connect("localhost", "root", "12345678", "hanhai_management",
                                        charset='utf8')
        cursor_management = db_management.cursor()
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        cursor.execute("SELECT `workposition_name`,`state` FROM `state_online` WHERE 1")
        get_state = cursor.fetchall()  # 获取工位状态
        for i in range(len(get_state)):#把读到的状态值与工序状态一对一写入字典
            self.dict[get_state[i][1]] = get_state[i][0]
        # print self.dict
        fyf_get_operater_id_list = []  # 存放每个部件的各工号人员工号和时间
        fyf_get_element_id = []
        fyf_insert_operator_name = ''  # 界面显示工号对应的员工姓名
        fyf_door_type_list = ['', '', '', '', '']  # 定义门板的网格（百叶）、玻璃、压条、套色、仿古
        fyf_get_operater_station = ['CNC_operation_station', 'Drilling_station', 'Edge_milling_station',
                                    'Surface_grinding_station', 'Trim_station', 'Half_check_station',
                                    'Sortting_before_membrane_station', 'Membrane_station', 'All_check_station',
                                    'Packaged_station', 'Packaged_putaway_station', 'Delivery_station']
        # 各工序信息列表
        print 2
        print self.get_part_id_list
        print 3
        for i in range(len(self.get_part_id_list)):  # 读取单个部件编号的各工位的员工编号和开始时间
            cursor.execute(
                "SELECT `Machining_operator_id`,`Start_Machining_Time`,`Drilling_operator_id`,`Drilling_begin_time`,`Edge_milling_operator_id`,`Edge_milling_begin_time`,`Polish_operator_id`,`Polish_begin_time`,`Regula_operator_id`,`Regula_begin_time`,`Half_test_operator_id`,`Half_test_begin_time`,`Sort_before_membrane_operator_id`,`Sort_before_membrane_begin_time`,`Membrane_operator_id`,`Membrane_begin_time`,`Quality_testing_operator_id`,`Quality_testing_begin_time`,`Package_operator_id`,`Package_begin_time`,`Shelf_after_package_operator_id`,`Shelf_after_package_begin_time`,`Deliver_operator_id`,`Deliver_begin_time` FROM `order_element_online` WHERE `Part_id`='%s' and `Element_type_id`='1'" %
                self.get_part_id_list[i])
            # ,`Drilling_operator_id`,`Drilling_begin_time`,`Sort_before_membrane_operator_id`,`Sort_before_membrane_begin_time`,`Membrane_work_order_ap_id`,`Membrane_work_order_creat_time`,`Quality_testing_operator_id`,`Quality_testing_begin_time`,`Package_work_order_ap_id`,`Package_work_order_create_time`
            fyf_get_operater_id = cursor.fetchone()
            # 读为门板的加工工序
            if fyf_get_operater_id == None:  # 当读不到此部件的门板工序的情况
                cursor.execute(
                    "SELECT `Machining_operator_id`,`Start_Machining_Time`,`Drilling_operator_id`,`Drilling_begin_time`,`Edge_milling_operator_id`,`Edge_milling_begin_time`,`Polish_operator_id`,`Polish_begin_time`,`Regula_operator_id`,`Regula_begin_time`,`Half_test_operator_id`,`Half_test_begin_time`,`Sort_before_membrane_operator_id`,`Sort_before_membrane_begin_time`,`Membrane_operator_id`,`Membrane_begin_time`,`Quality_testing_operator_id`,`Quality_testing_begin_time`,`Package_operator_id`,`Package_begin_time`,`Shelf_after_package_operator_id`,`Shelf_after_package_begin_time`,`Deliver_operator_id`,`Deliver_begin_time` FROM `order_element_online` WHERE `Part_id`='%s' and `Element_type_id`!='1'" %
                    self.get_part_id_list[i])
                fyf_get_operator_other = cursor.fetchall()
                if fyf_get_operator_other == None:
                    self.SetCellValue(i, 2, str(self.get_part_id_list[i]) + '没有零件号')
                else:
                    self.SetCellValue(i, 2, str(self.get_part_id_list[i]) + '没有门板号')
                fyf_get_operater_id = ''
                # 读到门板零件时
                # 将每次读到的门板各工序信息元组fyf_get_operater_id放入到工序信息列表fyf_get_operater_id_list中
                # #当循环结束时，全部部件的门板工序信息都放入到fyf_get_operater_id_list
            fyf_get_operater_id_list.append(list(fyf_get_operater_id))

            # 通过各工序信息中员工工位号查询到员工姓名，把员工姓名和时间组合在一起，放入工序信息列表fyf_get_operater_id_list中
        try:
            for i in range(len(fyf_get_operater_id_list)):  # 得到部件号的行数
                now_rows = self.GetNumberRows()#得到Grid列表实际行数
                if i + 1 > now_rows:  # 当部件行大于原表格行数，增加表格行数，并填入部件号
                    self.AppendRows(numRows=1)
                cursor.execute("SELECT `State` FROM `order_part_online` WHERE `Part_id`='%s'" % fyf_get_part_id[i][0])
                get_state_number = cursor.fetchone()#读取部件号所在状态值，通过字典读取部件状态填入Grid列表中
                # a = self.dict[get_state_number[0]]
                # unicode(self.dict[get_state_number[0]]).encode("utf8")#对读到的值进行转码
                self.SetCellValue(i, 2, '正在' + unicode(self.dict[get_state_number[0]]).encode("utf8"))
                for k in range(0, len(fyf_get_operater_id_list[i]), 2):


                    if fyf_get_operater_id_list[i][k] == None or fyf_get_operater_id_list[i][k] == '':  # 当读到员工工位为空时
                        fyf_insert_operator_name = ''
                        if fyf_get_operater_id_list[i][k + 1] == None:  # 当读到开始时间为空时
                            fyf_get_operater_id_list[i][k + 1] = ''

                    else:  # 当读到有效员工工位时，查询员工姓名
                        cursor_management.execute(
                            "SELECT `Name` FROM `info_staff_new` WHERE `Job_id`='%s'" %
                            fyf_get_operater_id_list[i][k])
                        fyf_operater_name = cursor_management.fetchone()  # 得到一条数据
                        if fyf_operater_name == None:  # 当读不到员工姓名时
                            fyf_insert_operator_name = 'Job_id IS ERROR'
                        else:
                            fyf_insert_operator_name = fyf_operater_name[0]
                            if fyf_insert_operator_name == None or fyf_insert_operator_name == '0':
                                fyf_insert_operator_name = ''  # 如果读到姓名为空或者姓名为零时，将姓名赋值为空

                    if fyf_insert_operator_name == '':  # 当没有工序操作员时，则没有此工位工序信息
                        fyf_get_operater_id_list[i][k] = ''
                    else:  # 有操作员时，输出员工姓名此工序开始时间
                        fyf_get_operater_id_list[i][k] = fyf_insert_operator_name + ',' + str(
                            fyf_get_operater_id_list[i][k + 1])
                        # for i in range(len(fyf_get_operater_id_list)):
                        # 以上部分得到部件号长度不变，但原工序位置，经过程序转换为员工姓名+时间

                # for m in range(len(fyf_get_operater_id_list[i]) / 2):  # 工位人员和时间成对存在，计算姓名、时间应该在某列显示
                #     self.SetCellValue(i, m + 3, fyf_get_operater_id_list[i][2 * m])

                self.SetCellValue(i, 0, self.get_part_id_list[i])

                # for k in range(len(fyf_grid_operater_station)):
                #     self.SetColLabelValue(k, fyf_grid_operater_station[k])
                for m in range(len(fyf_get_operater_id_list[i]) / 2):  # 工位人员和时间成对存在，计算姓名、时间应该在某列显示
                    self.SetCellValue(i, m + 3, fyf_get_operater_id_list[i][2 * m])

                    # 在界面显示工序状态
                    # 读取加工日期，计算工期计划
                    # #通过for 循环计算每个部件的工期计划，并在页面显示
                if fyf_get_operater_id_list[i] != []:  # 当能得到门板的工序信息时则判断进行到哪个工序
                    cursor.execute(
                        "SELECT `First_day` FROM `order_part_online` WHERE `Part_id`='%s'" % fyf_get_part_id[i][0])
                    fyf_get_first_time = cursor.fetchone()
                    # 获得此部件的开始时间
                    if '网格' in 'fyf_get_door_type[0]' or '百叶' in 'fyf_get_door_type[0]':
                        fyf_door_type_list[0] = 1
                    else:
                        fyf_door_type_list[0] = 0
                    if '玻璃' in 'fyf_get_door_type[0]':
                        fyf_door_type_list[1] = 1
                    else:
                        fyf_door_type_list[1] = 0
                    cursor.execute(
                        "SELECT `Bar_type`,`Double_color`,`Archaize` FROM `order_element_online` WHERE `Part_id`='%s'" %
                        self.get_part_id_list[i])
                    fyf_get_bar_type = cursor.fetchone()
                    for j in range(len(fyf_get_bar_type)):
                        if fyf_get_bar_type[j] == None or fyf_get_bar_type[j] == '0':
                            fyf_door_type_list[j + 2] = '0'
                        else:
                            fyf_door_type_list[j + 2] = '1'
                            # fyf_get_operater_id_list[i]!=[]当读到部件为门板时，在order_element_online表单查询此门板是否有网格、玻璃、压条、、套色、仿古

                    now_time_str = str(time.strftime('%Y-%m-%d', time.localtime()))  # 本地当前时间
                    if fyf_get_first_time[0] == None:
                        b = ''
                    else:
                        receive_time_str = str(fyf_get_first_time[0].strftime('%Y-%m-%d'))  # 开始时间的日期时间
                        localtime = datetime.datetime.strptime(now_time_str, '%Y-%m-%d')  # 将当前时间、开始时间转化为 年——月——日，并相减
                        Time = datetime.datetime.strptime(receive_time_str, '%Y-%m-%d')
                        N = (localtime - Time).days  # 由相减的差值，获得进入加工后的第几天

                        for k in range(0, len(fyf_get_operater_id_list[i]), 2):  # 工序、时间成对存在，以步长为二则可以每次得到工序位置
                            if fyf_get_operater_id_list[i][k] != '':  # 当能读到加工工位时，查询最后工位应在的工作时间
                                cursor.execute(
                                    "SELECT `%s` FROM `info_working_procedure` WHERE `Grid_index`='%s' AND `Glass_index`='%s' AND `Bar_index`='%s' AND `Double_color_index`='%s' AND `Antique`='%s'" % (
                                        fyf_get_operater_station[(k + 2) / 2 - 1], fyf_door_type_list[0],
                                        fyf_door_type_list[1], fyf_door_type_list[2], fyf_door_type_list[3],
                                        fyf_door_type_list[4]))  # 得到所在工序fyf_get_operater_station[(k+2)/2-1]
                                m = cursor.fetchone()  # 根据是哪种类型的门板，在info_working_procedure表单筛选符合此类型的条件的门板各工序应该在第几天完成
                                a = float(m[0])
                                a = int(a) - 1
                                b = N - a
                                b = str(b)
                                # 所在工位应在第几天
                                # 当上面循环做完时，会得到部件最后所在的工序，应该在第几天完成。

                                # 输出工期计划

                    # self.SetCellValue(i, 1, b)
                    # self.SetCellAlignment(i, 1, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)#设置内容居中
                    # # self.SetCellTextColour(i, 1, wx.CYAN)
                    # if b=='-1':
                    #     self.SetCellBackgroundColour(i, 1, wx.GREEN)
                    # if b=='0':
                    #     self.SetCellBackgroundColour(i, 1, wx.GREEN)
                    # if b=='1':
                    #     self.SetCellBackgroundColour(i, 1, wx.CYAN)
                    # if b=='2':
                    #     self.SetCellBackgroundColour(i, 1, wx.YELLOW)#设置背景颜色
                    #     self.SetCellTextColour(i, 1, wx.BLUE )#设置字体颜色
                    # if b>='3':
                    #     self.SetCellBackgroundColour(i, 1, wx.RED)


                    # 将工期计划更新到数据库order_part_online表单的Time_schedule字段中
                    try:
                        cursor.execute("UPDATE order_part_online SET Time_schedule='%s' WHERE `Part_id`='%s'" % (
                        b, self.get_part_id_list[i]))
                        db.commit()
                    except:
                        print "Error: unable to update data"
        # 部件各工序的员工姓名及开始时间在Grid界面上显示。
        # for i in range(now_rows - 0):
        #     self.DeleteRows(numRows=1)
        except:
            self.DeleteRows(numRows=1)
        db.close()
        db_management.close()
        # Grid界面自适应
        self.AutoSizeColumns(True)
        self.AutoSizeRows(True)





        # if self.date_begin.GetValue():
        #     begin_time=self.date_begin.GetValue()
        #     # begin_time='begin_time'
        #     print str(begin_time.strftime('%Y-%m-%d'))
        # if self.date_end.GetValue():
        #     end_time=self.date_end.GetValue()
        #     print end_time
        # if self.appeared.GetValue():
        #     self.MyChoice+="'appeared'"
        # if self.unfinished.GetValue():
        #     self.MyChoice+="'unfinished'"
        # if self.finished.GetValue():
        #     self.MyChoice+="'finished'"
        # if self.errored.GetValue():
        #     self.MyChoice+="'errored'"
        # self.MyChoice+="工单进行查询操作\r\n"
        # self.log.WriteText(self.MyChoice)
class LYB_Search_LeftPanel(wx.Panel):
    def __init__(self, parent,log):
        self.log = log
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition,
                          wx.DefaultSize)
        self.staticbox_sort = wx.StaticBox(self, -1, "请选择工单类型   ")
        self.staticboxsizer_sort=wx.StaticBoxSizer(self.staticbox_sort)
        self.staticboxsizer_sort_v1=wx.BoxSizer(wx.VERTICAL)
        self.staticboxsizer_sort_v2=wx.BoxSizer(wx.VERTICAL)
        self.unappeared=wx.CheckBox(self,-1,"未出工单")
        self.unappeared.SetValue(True)
        self.appeared=wx.CheckBox(self,-1,"已出工单")
        self.appeared.SetValue(True)
        self.unfinished=wx.CheckBox(self,-1,"未完成工单")
        self.unfinished.SetValue(True)
        self.finished=wx.CheckBox(self,-1,"已完成工")
        self.finished.SetValue(True)
        self.errored=wx.CheckBox(self,-1,"出错工单")
        self.errored.SetValue(True)
        self.staticboxsizer_sort_v1.Add(self.unappeared,0,wx.ALL,5)
        self.staticboxsizer_sort_v1.Add(self.appeared,0,wx.ALL,5)
        self.staticboxsizer_sort_v1.Add(self.unfinished,0,wx.ALL,5)
        self.staticboxsizer_sort_v1.Add(self.finished,0,wx.ALL,5)
        self.staticboxsizer_sort_v1.Add(self.errored,0,wx.ALL,5)
        btn1=wx.Button(self,-1,"默认")
        btn1.Bind(wx.EVT_BUTTON,self.On_Button_Default)
        btn2=wx.Button(self,-1,"全选")
        btn2.Bind(wx.EVT_BUTTON,self.On_Button_Default)
        btn3=wx.Button(self,-1,"全清")
        btn3.Bind(wx.EVT_BUTTON,self.On_Button_ClearAll)
        self.staticboxsizer_sort_v2.Add(btn1,0,wx.ALL,5)
        self.staticboxsizer_sort_v2.Add(btn2,0,wx.ALL,5)
        self.staticboxsizer_sort_v2.Add(btn3,0,wx.ALL,5)
        self.staticboxsizer_sort.Add(self.staticboxsizer_sort_v1)
        self.staticboxsizer_sort.Add(self.staticboxsizer_sort_v2)
        self.vbox=wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.staticboxsizer_sort,proportion=0,flag=wx.EXPAND,border=3)
        self.staticbox_date = wx.StaticBox(self, -1, "请选择查询起止时间")
        self.staticboxsizer_date=wx.StaticBoxSizer(self.staticbox_date,wx.VERTICAL)
        self.statictext1=wx.StaticText(self,label="起始于：")
        self.date_begin = PopDateControl(self, -1, pos=(30, 30))
        self.statictext2=wx.StaticText(self,label="\r\n终止于：")
        self.date_end = PopDateControl(self, -1, pos=(30, 30))
        self.staticboxsizer_date.Add(self.statictext1,border=3)
        self.staticboxsizer_date.Add(self.date_begin,border=3)
        self.staticboxsizer_date.Add(self.statictext2,border=3)
        self.staticboxsizer_date.Add(self.date_end,border=3)
        self.vbox.Add(self.staticboxsizer_date,flag=wx.EXPAND,border=3)
        bitmap = wx.Bitmap(
            os.path.normpath(os.path.join(bitmapDir, "aquabutton.png")),
            wx.BITMAP_TYPE_PNG)
        self.btn1 = AB.AquaButton(self, -1, bitmap, "  检     索  ")
        self.btn1.SetForegroundColour(wx.BLACK)
        self.btn2 = AB.AquaButton(self, -1, None, "  检      索  ")
        self.bt_go=wx.Button(self,-1,label="检索",style=0)
        self.vbox.Add(self.bt_go,proportion=0,flag=wx.ALIGN_CENTRE ,border=3)
        self.vbox.Add(self.btn1,proportion=0,flag=wx.ALIGN_CENTRE ,border=3)
        self.vbox.Add(self.btn2,proportion=0,flag=wx.ALIGN_CENTRE ,border=3)
        self.SetSizer(self.vbox)
        self.bt_go.Bind(wx.EVT_BUTTON,self.Start_Browse)
    def On_Button_Default(self,e):
        self.appeared.SetValue(True)
        self.unappeared.SetValue(True)
        self.unfinished.SetValue(True)
        self.finished.SetValue(True)
        self.errored.SetValue(True)
        self.Start_Browse(e)
    def On_Button_ClearAll(self,e):
        self.appeared.SetValue(False)
        self.unappeared.SetValue(False)
        self.unfinished.SetValue(False)
        self.finished.SetValue(False)
        self.errored.SetValue(False)
        self.Start_Browse(e)

    def Start_Browse(self,e):
        self.MyChoice = "操作员选择对包装工位中"
        if self.unappeared.GetValue():
            self.MyChoice+="'unappeard'"
        if self.appeared.GetValue():
            self.MyChoice+="'appeared'"
        if self.unfinished.GetValue():
            self.MyChoice+="'unfinished'"
        if self.finished.GetValue():
            self.MyChoice+="'finished'"
        if self.errored.GetValue():
            self.MyChoice+="'errored'"
        self.MyChoice+="工单进行查询操作\r\n"
        self.log.WriteText(self.MyChoice)
class Contract_Manage_Panel(wx.Panel):
    def __init__(self,parent,log):
    # def __init__(self, parent, log):
        wx.Panel.__init__(self, parent,-1)
        self.left_panel = LYB_Search_LeftPanel(self,log)
        # self.top_panel = LYB_Search_TopPanel(self, log)
        grid=wx.TextCtrl(self)
        box=wx.BoxSizer()
        box.Add(self.left_panel,proportion=0,flag=wx.EXPAND|wx.ALL,border=5)
        box.Add(grid,proportion=1,flag=wx.EXPAND|wx.ALL,border=5)
        self.SetSizer(box)

class PopDateControl(pop.PopupControl):
    def __init__(self,*_args,**_kwargs):
        pop.PopupControl.__init__(self, *_args, **_kwargs)

        self.win = wx.Window(self,-1,pos = (0,0),style = 0)
        self.cal = CalendarCtrl(self.win,-1,pos = (0,0))

        bz = self.cal.GetBestSize()
        self.win.SetSize(bz)

        # This method is needed to set the contents that will be displayed
        # in the popup
        self.SetPopupContent(self.win)

        # Event registration for date selection
        self.cal.Bind(wx.adv.EVT_CALENDAR,     self.OnCalSelected)


    # Method called when a day is selected in the calendar
    def OnCalSelected(self,evt):
        self.PopDown()
        date = self.cal.GetDate()

        # Format the date that was selected for the text part of the control
        self.SetValue('%02d/%02d/%04d' % (date.GetDay(),
                                          date.GetMonth()+1,
                                          date.GetYear()))
        evt.Skip()


    # Method overridden from PopupControl
    # This method is called just before the popup is displayed
    # Use this method to format any controls in the popup
    def FormatContent(self):
        # I parse the value in the text part to resemble the correct date in
        # the calendar control
        txtValue = self.GetValue()
        dmy = txtValue.split('/')
        didSet = False

        if len(dmy) == 3:
            date = self.cal.GetDate()
            d = int(dmy[0])
            m = int(dmy[1]) - 1
            y = int(dmy[2])

            if d > 0 and d < 31:
                if m >= 0 and m < 12:
                    if y > 1000:
                        self.cal.SetDate(wx.DateTime.FromDMY(d,m,y))
                        didSet = True

        if not didSet:
            self.cal.SetDate(wx.DateTime.Today())
