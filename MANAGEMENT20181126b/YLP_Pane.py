#!/usr/bin/env python
# _*_ coding: UTF-8 _*_
#20180730b:
#  部件grid增加型号一栏，将现在类型栏的内容放在型号栏显示，而在类型栏下显示门板，罗马柱眉板等类型信息.
# 状态显示数字，而显示数字对应的文字描述的信息，比如：入库完毕，正在cnc加工
#20180802c:
#查询时间增加了“昨天"，并且每点击一个时间按钮，都把获得的时间填入时间框里。
#右击树的Item，不仅显示”查询工期进度'，还增加了“展开”选项。
#组件Grid类里也加入滚动条，通过在Show_Inform_Panel类的Gride_Page方法里增加wx.adv.LayoutAlgorithm().LayoutWindow(self, self.ylp_Section_Inform_Grid)。
#20180921b:
#初步完成了报错报废管理界面
#20181008b:
#人力资源管理界面，左侧的工位是读info_staff_new表单获得的。
#20181010a:
#pdf表格合并出现问题，没有合并到一起。
#20181011a:
#解决合并问题
#20181013a:
#合同订单管理属性页，DrawTable_PDF()函数增加了一个参数number，这个参数的目的是确定是读在线部件表单还是完成部件表单。
#有的组件是没有部件的，所以画pdf的时候没有考虑这种情况会报错，加了个判断，如果组件下没有部件，就continue 继续搜索下一个组件的部件即可。
#20181020e:
#财务管理界面让柱状图嵌入了面板里。
#20181020f:
#增加了物流管理界面，有增加物流公司的按钮，鼠标左键单击双击修改物流公司名字，右键单击删除该物流公司
#20181022a:
#物流管理界面，又加入了经销商与快递公司的小属性页。
#20181025a:
#修改合同的订单管理界面，需要跟排产任务单保持格式一样。还未修改好
#20181026a:
#继续修改。
#20181122b:
#修改了合同订单管理界面，整套组件在合同订单管理查询的时候信息没有显示出来(在产与已完成都是)。

import wx.lib.delayedresult as delayedresult
try:
    from agw import pybusyinfo as PBI
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.pybusyinfo as PBI
import  string
import  wx
import  images
from TreeCtrl import *
import wx.adv
import os
import sys
import MySQLdb
import time
import datetime
import wx.grid as gridlib
from MyPane import *
from six import BytesIO
from ID_DEFINE import *
from compiler.ast import flatten
#-----------------------------------------
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('msyh', 'msyh.ttf'))
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer,Image,Table,TableStyle
try:
    from wx.lib.pdfviewer import pdfViewer, pdfButtonPanel
    havePyPdf = True
except ImportError:
    havePyPdf = False
#----------------------------------------

# from reportlab.pdfbase import pdfmetrics
# from reportlab.pdfbase.cidfonts import UnicodeCIDFont
# pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
# from reportlab.pdfbase.ttfonts import TTFont
# pdfmetrics.registerFont(TTFont('msyh', 'msyh.ttf'))
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.lib import colors
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer,Image,Table,TableStyle
# from reportlab.pdfgen import canvas
# from reportlab.platypus.frames import Frame
# from reportlab.platypus.flowables import *
# from reportlab.platypus.flowables import _ContainerSpace
# from reportlab.lib.units import inch
# from reportlab.platypus.paragraph import Paragraph


#画柱状图导入模块
import numpy as np
import matplotlib.mlab as mlab
# import matplotlib.pyplot as plt



try:
    import agw.flatnotebook as FNB
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.flatnotebook as FNB

try:
    dirName = os.path.dirname(os.path.abspath(__file__))
except:
    dirName = os.path.dirname(os.path.abspath(sys.argv[0]))

sys.path.append(os.path.split(dirName)[0])

try:
    from agw import foldpanelbar as fpb
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.foldpanelbar as fpb


try:
    from agw import aui
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.aui as aui


from six import BytesIO
# from PIL import Image

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
#---------------------------------------------------------------------------
def Is_Database_Connect():
    try:
        global DB
        global DB1
        global DB2
        DB =  MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password,db=database[0], charset=charset)
        DB1 =  MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password,db=database[1], charset=charset)
        DB2 =  MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password,db=database[2], charset=charset)
        return True
    except:
        return False

def Is_Database_Connect_Cloud():
    try:
        global DB_cloud
        DB_cloud = MySQLdb.connect(host=Cloud_ip, user=Cloud_username[0], passwd=Cloud_password, db=Cloud_manufacturerDB[2], charset=charset)
        return True
    except:
        return False
#  下面建了一个字典，分别是部件类型与编号的对应关系，比如“门板”---“1”  “罗马柱”--“3”,以及工位编号和工位名称的对应关系。
try:
    global dict_element_type
    global dict_workposition_name

    dict_element_type = {}
    dict_workposition_name = {}
    if Is_Database_Connect():
        cursor = DB1.cursor()
        cursor.execute("select `Index`,`Element_name` from `info_element_type` where 1 ")
        element_type = cursor.fetchall()
        for i in range(len(element_type)):
            dict_element_type[element_type[i][0]]=element_type[i][1]
        cursor = DB.cursor()
        cursor.execute("select `state`,`workposition_name` from `info_state_online` where 1 ")
        workposition_name = cursor.fetchall()
        for i in range(len(workposition_name)):
            dict_workposition_name[workposition_name[i][0]]=workposition_name[i][1]

        global base_type
        base_type = {0: '无'}
        cursor = DB1.cursor()
        cursor.execute("select `Base_material_name`,`Index` from `info_base_material_charge` where 1 ")
        base_type_record = cursor.fetchall()
        for l in range(len(base_type_record)):
            base_type[base_type_record[l][1]] = base_type_record[l][0]
except:
    pass



global tree_id
#********* 最右侧主面板调用的 表格、PDF、画板 类********************************************************
class Section_Inform_Grid(gridlib.Grid): ##, mixins.GridAutoEditMixin):
    def __init__(self, parent):
        gridlib.Grid.__init__(self, parent,-1)

        self.data=[]
        self.CreateGrid(1, 14)
        self.field_name=['部件号','型号','类型','颜色','高','宽','厚','仿古色','面积','价格','打孔位置','开门方式','边型','状态']
        for i in range(len(self.field_name)):  # 用来填写所有表头信息
            self.SetColLabelValue(i, self.field_name[i])
        self.AutoSize()
    def Show_Part_Inform(self,sec_inform):
        try:
            self.AutoSizeColumn(False)
            field_name = ['部件号','型号', '类型', '颜色', '高', '宽', '厚', '仿古色', '面积', '价格', '打孔位置', '开门方式', '边型','状态']
            self.data=[]
            for i in range(len(sec_inform)):
                self.data.append(list(sec_inform[i]))
                try:
                    self.data[i][2]=dict_element_type[self.data[i][2]]
                except:
                    pass
                try:
                    self.data[i][13] = dict_workposition_name[self.data[i][13]]
                except:
                    pass
            if self.data is  None:
                return
            now_rows = self.GetNumberRows()
            if len(self.data) > now_rows:
                for i in range(len(self.data) - now_rows):
                    self.AppendRows(numRows=1)
            if len(self.data) < now_rows:
                for i in range(now_rows - len(self.data)):
                    self.DeleteRows(numRows=1)
            if (len(self.data) != 0):
                for i in range(len(field_name)):  # 用来填写所有表头信息
                    self.SetColLabelValue(i, field_name[i])
                self.SetColLabelAlignment(wx.ALIGN_LEFT, wx.ALIGN_BOTTOM)
                for i in range(len(self.data)):  # 填数据
                    for j in range(len(self.data[i])):
                        self.SetCellValue(i, j, str(self.data[i][j]))
            else:
                self.CreateGrid(1, 14)
                self.field_name = ['部件号','型号','类型','颜色','高','宽','厚','仿古色','面积','价格','打孔位置','开门方式','边型','状态']
                for i in range(len(self.field_name)):  # 用来填写所有表头信息
                    self.SetColLabelValue(i, self.field_name[i])
            self.AutoSize()
        except:
            pass
class part_test_panel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent,-1,size=(100,100))
        self.grid=Part_test(self)
class Part_test(gridlib.Grid):
    def __init__(self,parent):
        gridlib.Grid.__init__(self,parent,-1)
        self.CreateGrid(1,12)
        self.test_name=['零件号','型号', '类型', '颜色', '高', '宽', '厚', '仿古色','打孔位置', '开门方式', '边型','状态']
        for i in range(len(self.test_name)):
            self.SetColLabelValue(i,self.test_name[i])
        self.AutoSize()
    def Show_Part_Inform(self,sec_inform):
        try:
            self.AutoSizeColumn(False)
            field_name = ['零件号','型号', '类型', '颜色', '高', '宽', '厚', '仿古色','打孔位置', '开门方式', '边型','状态']
            self.data=[]
            for i in range(len(sec_inform)):
                self.data.append(list(sec_inform[i]))
                try:
                    self.data[i][2]=dict_element_type[self.data[i][2]]
                except:
                    pass
                try:
                    self.data[i][11] = dict_workposition_name[self.data[i][11]]
                except:
                    pass
            if self.data is  None:
                return
            now_rows = self.GetNumberRows()
            if len(self.data) > now_rows:
                for i in range(len(self.data) - now_rows):
                    self.AppendRows(numRows=1)
            if len(self.data) < now_rows:
                for i in range(now_rows - len(self.data)):
                    self.DeleteRows(numRows=1)
            if (len(self.data) != 0):
                for i in range(len(field_name)):  # 用来填写所有表头信息
                    self.SetColLabelValue(i, field_name[i])
                self.SetColLabelAlignment(wx.ALIGN_LEFT, wx.ALIGN_BOTTOM)
                for i in range(len(self.data)):  # 填数据
                    for j in range(len(self.data[i])):
                        self.SetCellValue(i, j, str(self.data[i][j]))
            else:
                self.CreateGrid(1, 14)
                self.field_name = ['零件号','型号','类型','颜色','高','宽','厚','仿古色','打孔位置','开门方式','边型','状态']
                for i in range(len(self.field_name)):  # 用来填写所有表头信息
                    self.SetColLabelValue(i, self.field_name[i])
            self.AutoSize()
        except:
            pass

class Order_Inform_PDF(wx.Panel):
    def __init__(self, parent,log):
        wx.Panel.__init__(self, parent, -1)
        self.log=log
        vsizer = wx.BoxSizer(wx.VERTICAL)
        self.buttonpanel = pdfButtonPanel(self, wx.ID_ANY,wx.DefaultPosition, wx.DefaultSize, 0)
        vsizer.Add(self.buttonpanel, 0,wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT | wx.TOP, 5)
        self.viewer = pdfViewer(self, wx.ID_ANY, wx.DefaultPosition,wx.DefaultSize, wx.HSCROLL | wx.VSCROLL | wx.SUNKEN_BORDER)
        vsizer.Add(self.viewer, 1, wx.GROW | wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)
        self.SetSizer(vsizer)
        self.SetAutoLayout(True)
        self.buttonpanel.viewer = self.viewer
        self.viewer.buttonpanel = self.buttonpanel
        #self.DrawTable_PDF()  # 画pdf表
        wx.BeginBusyCursor()
        #self.viewer.LoadFile('order_pdf.pdf')
        wx.EndBusyCursor()

    def DrawTable_PDF(self,order_inform,sec_inform,state_number):
        # try:
            story = []
            stylesheet = getSampleStyleSheet()
            normalStyle = stylesheet['Normal']
            # 标题：段落的用法详见reportlab-userguide.pdf中chapter 6 Paragraph

            contract_id=order_inform[0].split('O')
            cursor = DB.cursor()
            cursor.execute("select `Customer_name`,`Customer_tel` ,`Customer_address` from `order_contract_internal` where `Contract_id`='%s' " %
                contract_id[0])
            contract_inform_record = cursor.fetchone()
            rpt_title = '<para autoLeading="off" fontSize=15 align=center><b><font face="msyh">订单号：%s</font></b><br/><br/><br/></para>' \
                        '<para autoLeading="off" fontSize=10 ><b><font face="msyh">客户名：%s  </font></b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</para>' \
                        '<para autoLeading="off" fontSize=10 ><b><font face="msyh">客户电话：%s </font></b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</para>' \
                        '<para autoLeading="off" fontSize=10 ><b><font face="msyh">客户地址：%s </font></b><br/></para>' \
                        '<para autoLeading="off" fontSize=10 ><b><font face="msyh">终端客户名：%s  </font></b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</para>' \
                        '<para autoLeading="off" fontSize=10 ><b><font face="msyh">终端客户电话：%s </font></b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</para>' \
                        '<para autoLeading="off" fontSize=10 ><b><font face="msyh">终端客户地址：%s </font></b><br/></para>' \
                        '<para autoLeading="off" fontSize=10 ><b><font face="msyh">订单价格：%s </font></b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</para>' \
                        '<para autoLeading="off" fontSize=10 ><b><font face="msyh">订单面积：%s </font></b><br/><br/><br/></para>' % (
                        order_inform[0],contract_inform_record[0],contract_inform_record[1],contract_inform_record[2], order_inform[1], order_inform[2], order_inform[3], order_inform[4],
                        order_inform[5])
            story.append(Paragraph(rpt_title, normalStyle))
            # component_data = [('组件号', '套系', '颜色', '厚度', '边型', '型号', '高', '宽', '面积')]
            component_data = [( '基材', '颜色', '套系', '边型','门型', '高', '宽','深度', '数量', '打孔', '特殊工艺')]
            if Is_Database_Connect():
                part_inform = []
                cursor = DB.cursor()
                row = 0
                for i in range(len(sec_inform)):
                    sec_part = []
                    if state_number==2:
                        cursor.execute(
                            "select `Door_type`,`Door_height` ,`Door_width`,`Open_way`,`Straightening_device`,`Double_color`,`Archaize`,`heterotype`,`Single_double`,`Glass`,`Hole` from `order_part_online` where `Sec_id`='%s' " %
                            sec_inform[i][0])
                        part_inform_record = cursor.fetchall()
                    else:
                        cursor.execute(
                            "select `Door_type`,`Door_height` ,`Door_width`,`Open_way`,`Straightening_device`,`Double_color`,`Archaize`,`heterotype`,`Single_double`,`Glass`,`Hole` from `order_part_complete` where `Sec_id`='%s' " %
                            sec_inform[i][0])
                        part_inform_record = cursor.fetchall()

                    row += len(part_inform_record)
                    if part_inform_record!=():
                        for j in range(len(part_inform_record)):
                            part_inform.append(list(part_inform_record[j]))
                            if 'MY' in part_inform[j][0]:
                                Door_type = part_inform[j][0].split('_')
                                number = Door_type[1]
                                number_style = number[-1]
                                if number_style == 'B':
                                    style = '单拱B型'
                                elif number_style == 'C':
                                    style = '肩膀拱C型'
                                elif number_style == 'D':
                                    style = '多拱D型'
                                elif number_style == 'E':
                                    style = '复杂拱E型'
                                else:
                                    style = '普通A型'
                                Door_type_split = style + Door_type[-1]
                                # part_inform[j][0] = Door_type[-1]
                            else:
                                Door_type_split = part_inform_record[j][0]
                            if part_inform_record[j][4] == 1:
                                remark1 = '拉直器' + '\n'
                            else:
                                remark1 = ''
                            if part_inform_record[j][5] != None:
                                remark2 = part_inform_record[j][5] + '\n'
                            else:
                                remark2 = ''
                            if part_inform_record[j][6] != None:
                                remark3 = part_inform_record[j][6] + '\n'
                            else:
                                remark3 = ''
                            if part_inform_record[j][7] == 0:
                                remark5 = ''
                            else:
                                remark5 = '异形' + '\n'
                            if part_inform_record[j][8] == 0:
                                remark6 = ''
                            else:
                                remark6 = '双面板' + '\n'
                            if part_inform_record[j][9] == None or part_inform_record[j][9] == 0:
                                remark7 = ''
                            else:
                                remark7 = part_inform_record[j][9] + '\n'
                            #---------------------------------
                            if part_inform_record[j][1] < 1000:
                                hole = str(120) + '/' + str(0) + '/' + str(0) + '/' + str(0) + '/' + str(120)
                            elif part_inform_record[j][1] >= 1000 and part_inform_record[j][1] < 1530:
                                hole = str(120) + '/' + str(0) + '/' + str(
                                    int(part_inform_record[j][1] * 0.5)) + '/' + str(0) + '/' + str(120)
                            elif part_inform_record[j][1] >= 1530 and part_inform_record[j][1] < 1645:
                                hole = str(120) + '/' + str(550) + '/' + str(0) + '/' + str(
                                    int(part_inform_record[j][1] - 550)) + '/' + str(120)
                            elif part_inform_record[j][1] >= 1645 and part_inform_record[j][1] < 1800:
                                hole = str(120) + '/' + str(600) + '/' + str(0) + '/' + str(
                                    int(part_inform_record[j][1] - 600)) + '/' + str(120)
                            elif part_inform_record[j][1] >= 1800 and part_inform_record[j][1] < 1900:
                                hole = str(120) + '/' + str(650) + '/' + str(0) + '/' + str(
                                    int(part_inform_record[j][1] - 650)) + '/' + str(120)
                            elif part_inform_record[j][1] >= 1900 and part_inform_record[j][1] < 2100:
                                hole = str(120) + '/' + str(700) + '/' + str(0) + '/' + str(
                                    int(part_inform_record[j][1] - 700)) + '/' + str(120)
                            elif part_inform_record[j][1] >= 2100 and part_inform_record[j][1] < 2250:
                                hole = str(120) + '/' + str(750) + '/' + str(0) + '/' + str(
                                    int(part_inform_record[j][1] - 750)) + '/' + str(120)
                            elif part_inform_record[j][1] >= 2250 and part_inform_record[j][1] < 2300:
                                hole = str(120) + '/' + str(800) + '/' + str(0) + '/' + str(
                                    int(part_inform_record[j][1] - 800)) + '/' + str(120)
                            elif part_inform_record[j][1] >= 2300:
                                hole = str(120) + '/' + str(850) + '/' + str(0) + '/' + str(
                                    int(part_inform_record[j][1] - 850)) + '/' + str(120)
                            else:
                                hole = '尺寸错误'
                            if part_inform_record[j][3] != '不开' and part_inform_record[j][10] != None and hole != \
                                    part_inform_record[j][10]:
                                remark4 = part_inform_record[j][10] + '\n'
                            else:
                                remark4 = ''
                            remark_total = remark1 + remark2 + remark3 + remark5 + remark6 + remark7 + remark4  # 增加备注
                            # if j == 0:
                            #     sec_inform1 = list(sec_inform[i][1:])
                            # else:
                            #     #sec_inform1 = [None, None, None, None, None]
                            #     sec_inform1 = [None, None, None, None]
                            sec_inform1 = list(sec_inform[i][1:])
                            #sec_part.append(sec_inform1 + part_inform[j])
                            inform=[base_type[sec_inform1[0]],sec_inform1[1],sec_inform1[2],sec_inform1[3], Door_type_split,part_inform_record[j][1],part_inform_record[j][2],'','',part_inform_record[j][3],remark_total]
                            sec_part.append(inform)
                        sec_part_num = list(set([tuple(t) for t in sec_part]))
                        for k in range(len(sec_part_num)):
                            num=[]
                            count=sec_part.count(sec_part[k])
                            if count>1:
                                for k1 in range(len(sec_part)-(k+1)):
                                    if sec_part[k1+k+1]==sec_part[k]:
                                        num.append(k1+k+1)
                                for k1 in range(len(num)-1,-1,-1):
                                    del sec_part[num[k1]]
                            sec_part[k][8] = count
                        #sec_part=list(set(sec_part))
                        component_data += (sec_part)
                    else:
                        if state_number == 2:
                            cursor.execute("select `Sec_height` ,`Sec_length`,`Sec_width`,`Archaize`,`Sec_series` from `order_section_online` where `Sec_id`='%s' " %
                                sec_inform[i][0])
                            ZT_section = cursor.fetchone()    #整套组件的信息
                        else:
                            cursor.execute(
                                "select `Sec_height` ,`Sec_length`,`Sec_width`,`Archaize`,`Sec_series` from `order_section_complete` where `Sec_id`='%s' " %
                                sec_inform[i][0])
                            ZT_section = cursor.fetchone()  # 整套组件的信息
                        if ZT_section!=() and ZT_section!=None:
                            inform = [base_type[sec_inform[i][1]], sec_inform[i][2],ZT_section[4], '', '',
                                      ZT_section[0], ZT_section[1], ZT_section[2], '1','',ZT_section[3]]
                            sec_part.append(inform)
                            component_data += (sec_part)
                        else:
                            pass

                    # 创建表格对象，并设定各列宽度
                    component_table = Table(component_data, colWidths=[60, 60, 55, 55, 100, 45, 45, 45, 20, 45,60])
                    # 添加表格样式
                    # if i == 0:
                    #     h = 1
                    #     h1 = row
                    # else:
                    #     h = h1 + 1
                    #     h1 = row
                    component_table.setStyle(TableStyle([
                        ('FONTNAME', (0, 0), (-1, -1), 'msyh'),  # 字体
                        ('FONTSIZE', (0, 0), (-1, -1), 10),  # 字体大小
                        # ('SPAN',(0,h),(0,h1)),#合并第一行前三列
                        # ('BACKGROUND',(0,0),(-1,0), colors.lightskyblue),#设置第一行背景颜色
                        # ('SPAN',(1,h),(1,h1)), #合并第一行后两列
                        # ('SPAN', (2, h), (2, h1)),  # 合并第一行后两列
                        # ('SPAN', (3, h), (3, h1)),  # 合并第一行后两列
                        # ('SPAN', (4, h), (4, h1)),  # 合并第一行后两列
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # 对齐
                        # ('ALIGN',(-1,0),(-2,0),'RIGHT'),#对齐
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # 对齐
                        ('LINEBEFORE', (0, 0), (0, -1), 0.1, colors.grey),  # 设置表格左边线颜色为灰色，线宽为0.1
                        # ('TEXTCOLOR',(0,1),(-2,-1),colors.royalblue),#设置表格内文字颜色
                        ('TEXTCOLOR', (0, 1), (-2, -1), colors.black),  # 设置表格内文字颜色
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # 设置表格框线为红色，线宽为0.5
                    ]))
                    story.append(component_table)
                    component_data = []
            rootdir = os.getcwd()
            doc = SimpleDocTemplate(os.getcwd() + '\\order_pdf.pdf')
            doc.build(story)
            self.viewer.LoadFile('order_pdf.pdf')
        # except:
        #     self.log.WriteText("Order_Inform_PDF类 DrawTable_PDF方法 报错，画pdf表格出错 \r\n")
    def OnLoadButton(self, event):
        dlg = wx.FileDialog(self, wildcard="*.pdf")
        if dlg.ShowModal() == wx.ID_OK:
            wx.BeginBusyCursor()
            self.viewer.LoadFile(dlg.GetPath())
            wx.EndBusyCursor()
        dlg.Destroy()
class Part_ID_Inform_Panel(wx.Panel):
        def __init__(self, parent,log):
            wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition,
                          wx.DefaultSize,style=wx.SUNKEN_BORDER)
            self.log=log
            # self.grid = Part_test(self)
            self.panel = part_test_panel(self)
            self.panel.grid.Bind(gridlib.EVT_GRID_SELECT_CELL, self.display)
            self.hbox = wx.BoxSizer(wx.HORIZONTAL)
            self.staticBmp = wx.StaticBitmap(self, -1, wx.NullBitmap, pos=(10, 10), size=(200, 200))
            self.hbox.Add(self.staticBmp, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
            self.door_type_text = wx.StaticText(self, -1, "门型：%s" % str(10), pos=(10, 10),size=(160,20))
            self.color_text = wx.StaticText(self, -1, "颜色：%s" % str(20), pos=(10, 10),size=(120,20))
            self.height_text = wx.StaticText(self, -1, "高：%s" % str(30), pos=(10, 10),size=(120,20))
            self.width_text = wx.StaticText(self, -1, "宽：%s" % str(40), pos=(10, 10),size=(120,20))
            self.thick_text = wx.StaticText(self, -1, "厚：%s" % str(50), pos=(10, 10),size=(120,20))
            self.staticbox_date = wx.StaticBox(self, -1,size=(150,20))
            self.tbox = wx.StaticBoxSizer(self.staticbox_date, wx.VERTICAL)
            self.staticbox_date_1 = wx.StaticBox(self, -1)
            self.gbox = wx.StaticBoxSizer(self.staticbox_date_1, wx.HORIZONTAL)
            self.gbox.Add(self.door_type_text, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
            self.gbox.Add(self.color_text, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
            self.gbox.Add(self.height_text, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
            self.gbox.Add(self.width_text, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
            self.gbox.Add(self.thick_text, proportion=1, flag=wx.EXPAND | wx.ALL, border=3)
            self.tbox.Add(self.gbox, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
            self.tbox.Add(self.panel, proportion=1, flag=wx.EXPAND | wx.ALL, border=3)
            self.hbox.Add(self.tbox, proportion=1, flag=wx.EXPAND | wx.ALL, border=3)
            self.SetSizer(self.hbox)
        # 重置Image对象尺寸的函数
        def resizeBitmap(self,image, width=100, height=100):
            bmp = image.Scale(width, height).ConvertToBitmap()
            return bmp
        def opj(self, path):
            st = os.path.join(*tuple(path.split('/')))
            # HACK: on Linux, a leading / gets lost...
            if path.startswith('/'):
                st = '/' + st
            return st
        def Part_OnPaint(self,part_inform):
            try:
                self.staticBmp.SetBitmap(wx.NullBitmap)
                ImgPath_origin = "C:\image\\"
                if part_inform[0]!=None and part_inform[0]!='':
                    try:
                        ImgPath = ImgPath_origin + str(part_inform[0]) + ".png"#默认初始化读取此部件号的门板零件
                        # ImgPath = ImgPath_origin + "b.png"
                        self.imgType = wx.BITMAP_TYPE_ANY
                        def getImg():
                            path = self.opj(ImgPath)
                            type = self.imgType
                            return wx.Image(path, type)
                        if '高柜' in str(part_inform[0]):
                            self.scale = getImg().Scale(width=200, height=560)
                        else:
                            self.scale = getImg().Scale(width=200, height=350)
                        self.staticBmp.SetBitmap(self.scale.ConvertToBitmap())
                    except:
                        ImgPath = ImgPath_origin + "暂无图片.png"
                        self.imgType = wx.BITMAP_TYPE_ANY
                        def getImg():
                            path = self.opj(ImgPath)
                            type = self.imgType
                            return wx.Image(path, type)
                        self.scale = getImg().Scale(width=200, height=350)
                        self.staticBmp.SetBitmap(self.scale.ConvertToBitmap())
                        # self.log.WriteText('合同订单管理，YLP_Pane.py中Part_ID_Inform_Panel中Part_OnPaint()未获取需要显示的图片，请进行检查 \r\n')
                self.door_type_text.Label="门型：%s"% str(part_inform[0])
                self.color_text.Label="颜色：%s"% str(part_inform[1])
                self.height_text.Label="高：%s"% str(part_inform[2])
                self.width_text.Label="宽：%s"% str(part_inform[3])
                self.thick_text.Label="厚：%s"% str(part_inform[4])
            except:
                pass
        def display(self, event):
            try:
                row = event.GetRow()  # 获得鼠标单击的单元格所在的行
                ImgPath_origin= "C:\image\\"
                picture=self.panel.grid.GetCellValue(row, 1)
                if picture!=None and picture!='':
                    try:
                        self.staticBmp.SetBitmap(wx.NullBitmap)
                        ImgPath=ImgPath_origin+str(picture)+".png"
                        self.imgType = wx.BITMAP_TYPE_ANY
                        def getImg():
                            path = self.opj(ImgPath)
                            type = self.imgType
                            return wx.Image(path, type)
                        if '高柜' in str(picture):
                            self.scale = getImg().Scale(width=200, height=560)
                        else:
                            self.scale = getImg().Scale(width=200, height=350)
                        self.staticBmp.SetBitmap(self.scale.ConvertToBitmap())
                    except:
                        ImgPath = ImgPath_origin + "暂无图片.png"
                        self.imgType = wx.BITMAP_TYPE_ANY
                        def getImg():
                            path = self.opj(ImgPath)
                            type = self.imgType
                            return wx.Image(path, type)
                        self.scale = getImg().Scale(width=200, height=350)
                        self.staticBmp.SetBitmap(self.scale.ConvertToBitmap())
                        self.log.WriteText('合同订单管理，YLP_Pane.py中Part_ID_Inform_Panel中display()未获取需要显示的图片，请进行检查 \r\n')
                    self.door_type_text.Label = "门型：%s" % str(picture)
                    self.color_text.Label = "颜色：%s" % str(self.panel.grid.GetCellValue(row, 3))
                    self.height_text.Label = "高：%s" % str(self.panel.grid.GetCellValue(row, 4))
                    self.width_text.Label = "宽：%s" % str(self.panel.grid.GetCellValue(row, 5))
                    self.thick_text.Label = "厚：%s" % str(self.panel.grid.GetCellValue(row, 6))
            except:
                pass
        def ID_OnPaint(self, ID_inform):
            self.imgPath = "C:\image\\b.png"
            img_big = wx.Image(self.imgPath, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            staticBmp = wx.StaticBitmap(self, -1, img_big, pos=(10, 10), size=(200, 200))
            staticBmp.SetBackgroundColour("#a8a8a8")
            self.imgType = wx.BITMAP_TYPE_ANY
            def getImg():
                path = self.opj(self.imgPath)
                type = self.imgType
                return wx.Image(path, type)
            self.scale = getImg().Scale(width=200, height=300)
            staticBmp.SetBitmap(self.scale.ConvertToBitmap())
            wx.StaticText(self, -1, "门型：%s" % str(ID_inform[0]), (300, 20))
            wx.StaticText(self, -1, "颜色：%s" % str(ID_inform[1]), (300, 70))
            wx.StaticText(self, -1, "高：%s" % str(ID_inform[2]), (300, 120))
            wx.StaticText(self, -1, "宽：%s" % str(ID_inform[3]), (300, 170))
            wx.StaticText(self, -1, "厚：%s" % str(ID_inform[4]), (300, 220))
            # self.grid=Part_test(self)

#******** 最右侧主面板的显示 ************************************************************
class Show_Inform_Panel(wx.Panel):
    def __init__(self, parent,log):
        wx.Panel.__init__(self, parent, -1,)
        self.log=log
        # self.ctrl = aui.AuiNotebook(self)
        bookStyle = FNB.FNB_NODRAG
        self.AutoScroll=True
        self.ctrl = FNB.FlatNotebook(self, wx.ID_ANY, agwStyle=bookStyle)

        self.ylp_Order_Inform_PDF=Order_Inform_PDF(self,self.log)
        self.ctrl.AddPage(self.ylp_Order_Inform_PDF, "订单")

        self.ylp_Section_Inform_Grid = Section_Inform_Grid(self)
        self.ctrl.AddPage(self.ylp_Section_Inform_Grid, "组件")

        self.ylp_Part_ID_Inform_Panel=Part_ID_Inform_Panel(self,self.log)
        self.ctrl.AddPage(self.ylp_Part_ID_Inform_Panel, "部件")
        bookStyle |= FNB.FNB_HIDE_TABS
        self.ctrl.SetAGWWindowStyleFlag(bookStyle)
        sizer = wx.BoxSizer()
        sizer.Add(self.ctrl, 1, wx.EXPAND | wx.ALL)
        self.SetSizer(sizer)
        wx.CallAfter(self.ctrl.SendSizeEvent)
    def PDF_Page(self,order_inform,sec_inform,number):
        self.ctrl.SetSelection(0)
        self.ylp_Order_Inform_PDF.DrawTable_PDF(order_inform,sec_inform,number)
    def Gride_Page(self,part_inform):
        self.ctrl.SetSelection(1)
        self.ylp_Section_Inform_Grid.Show_Part_Inform(part_inform)
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.ylp_Section_Inform_Grid)
    def Show_Part_Inform(self,part_inform,part_information):
        self.ctrl.SetSelection(2)
        # self.ylp_Part_ID_Inform_Panel.Show_Part_Inform(part_information)#直接放grid可实现
        self.ylp_Part_ID_Inform_Panel.Part_OnPaint(part_inform)
        self.ylp_Part_ID_Inform_Panel.panel.grid.Show_Part_Inform(part_information)
        wx.adv.LayoutAlgorithm().LayoutWindow(self.ylp_Part_ID_Inform_Panel.panel, self.ylp_Part_ID_Inform_Panel.panel.grid)
    def Show_ID_Inform(self,ID_inform):
        self.ctrl.SetSelection(2)
        self.ylp_Part_ID_Inform_Panel.ID_OnPaint(ID_inform)
#******** 主框架 *********************************************************
class MyTreeCtrl(wx.TreeCtrl):
    def __init__(self, parent, id, pos, size, style, log):
        wx.TreeCtrl.__init__(self, parent, id, pos, size, style)
        self.log = log

    def OnCompareItems(self, item1, item2):
        t1 = self.GetItemText(item1)
        t2 = self.GetItemText(item2)
        self.log.WriteText('compare: ' + t1 + ' <> ' + t2 + '\n')
        if t1 < t2: return -1
        if t1 == t2: return 0
        return 1
class YLP_Contract_Order_Management_Panel(wx.Panel):
    def __init__(self, parent,log,fyf_progress_order,fyf_progress_sec,FYF_Progress_Manage_Panel,fyf_progress_id,Port, id=wx.ID_ANY, title="", pos=wx.DefaultPosition,
                 size=(700,650), style=wx.DEFAULT_FRAME_STYLE):
        wx.Panel.__init__(self, parent)
        self.fyf_progress_order = fyf_progress_order
        self.fyf_progress_sec = fyf_progress_sec
        self.FYF_Progress_Manage_Panel = FYF_Progress_Manage_Panel
        self.fyf_progress_id = fyf_progress_id
        self.parent = parent
        self.Port = Port
        self.select_code = 0
        self._flags = 0
        self.log = log
        self._leftWindow1 = wx.adv.SashLayoutWindow(self, 101, wx.DefaultPosition,
                                                wx.Size(200, 1000), wx.NO_BORDER |
                                                wx.adv.SW_3D | wx.CLIP_CHILDREN)
        self._leftWindow1.SetDefaultSize(wx.Size(220, 1000))
        self._leftWindow1.SetOrientation(wx.adv.LAYOUT_VERTICAL)
        self._leftWindow1.SetAlignment(wx.adv.LAYOUT_LEFT)
        self._leftWindow1.SetSashVisible(wx.adv.SASH_RIGHT, True)
        self._leftWindow1.SetExtraBorderSize(10)
        self._pnl = 0
        #self.ylp_Section_Inform_Grid=Section_Inform_Grid(self)
        self.ylp_Show_Inform_Panel=Show_Inform_Panel(self,self.log)

        self.ID_WINDOW_LEFT1 = 101
        self.ID_WINDOW_RIGHT1 = 102
        self._leftWindow1.Bind(wx.adv.EVT_SASH_DRAGGED_RANGE, self.OnFoldPanelBarDrag,
                               id=101, id2=102)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        self.Bind(wx.EVT_SCROLL, self.OnSlideColour)
        self.ReCreateFoldPanel(0)

        self._leftWindow2 = wx.adv.SashLayoutWindow(self, 102, wx.DefaultPosition,
                                                    wx.Size(300, 800), wx.NO_BORDER |
                                                    wx.adv.SW_3D | wx.CLIP_CHILDREN)
        self._leftWindow2.SetDefaultSize(wx.Size(320, 800))
        self._leftWindow2.SetOrientation(wx.adv.LAYOUT_VERTICAL)
        self._leftWindow2.SetAlignment(wx.adv.LAYOUT_LEFT)
        self._leftWindow2.SetSashVisible(wx.adv.SASH_RIGHT, True)
        self._leftWindow2.SetExtraBorderSize(10)
        self._leftWindow2.Bind(wx.adv.EVT_SASH_DRAGGED_RANGE, self.OnFoldPanelBarDrag,
                               id=101, id2=102)
        self._pnl = 0
        self.Create_TreeCtrl()
        self.time_deal()
        self.TreeCtrl_Refresh(self.start_time,self.end_time)

    def Get_Seek_DateTime(self,event):
        self.time_deal()
        self.TreeCtrl_Refresh(self.start_time,self.end_time)
        # date_start = self.calendar_begin.GetValue()
        # date_end = self.calendar_end.GetValue()
       #  if "从" in date_start or "至"in date_end :
       #      self.TreeCtrl_Refresh(0,0)
       #  else:
       #      if '/' in date_start:
       #          date_start=date_start.split("/")
       #          date_end = date_end.split("/")
       #          date_start=date_start[2],date_start[1],date_start[0]
       #          date_end=date_end[2],date_end[1],date_end[0]
       #          st='-'
       #          date_start = st.join(date_start)
       #          date_end = st.join(date_end)
       #      self.TreeCtrl_Refresh(date_start,date_end)
       #
       # # wx.adv.LayoutAlgorithm().LayoutWindow(self._leftWindow2,self.tree)
    def Get_Today(self,event):
        date_start_display = time.strftime("%d/%m/%Y", time.localtime())
        date_start=time.strftime("%Y-%m-%d", time.localtime())
        date_end=date_start
        self.store_combox.SetValue('ALL')
        self.member_combox.SetValue('ALL')
        self.Terminal_customer.SetValue('ALL')
        self.calendar_begin.textCtrl.SetValue(date_start_display)
        self.calendar_end.textCtrl.SetValue(date_start_display)
        self.TreeCtrl_Refresh(date_start, date_end)

        #wx.adv.LayoutAlgorithm().LayoutWindow(self._leftWindow2,self.tree)
    def Get_Yesterday(self,event):
        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        yesterday = today - oneday
        now_time = (today - oneday).strftime('%d/%m/%Y')  # 本地当前时间
        self.store_combox.SetValue('ALL')
        self.member_combox.SetValue('ALL')
        self.Terminal_customer.SetValue('ALL')
        self.TreeCtrl_Refresh(str(yesterday), str(yesterday))
        self.calendar_begin.textCtrl.SetValue(now_time)
        self.calendar_end.textCtrl.SetValue(now_time)
        #wx.adv.LayoutAlgorithm().LayoutWindow(self._leftWindow2, self.tree)
    def Get_Byesterday(self,event):
        today = datetime.date.today()
        oneday = datetime.timedelta(days=2)
        yesterday = today - oneday
        now_time = (today - oneday).strftime('%d/%m/%Y')  # 本地当前时间
        self.store_combox.SetValue('ALL')
        self.member_combox.SetValue('ALL')
        self.Terminal_customer.SetValue('ALL')
        self.TreeCtrl_Refresh(str(yesterday), str(yesterday))
        self.calendar_begin.textCtrl.SetValue(now_time)
        self.calendar_end.textCtrl.SetValue(now_time)
        #wx.adv.LayoutAlgorithm().LayoutWindow(self._leftWindow2, self.tree)
    def Get_Bbyesterday(self,event):
        today = datetime.date.today()
        oneday = datetime.timedelta(days=3)
        yesterday = today - oneday
        now_time = (today - oneday).strftime('%d/%m/%Y')  # 本地当前时间
        self.store_combox.SetValue('ALL')
        self.member_combox.SetValue('ALL')
        self.Terminal_customer.SetValue('ALL')
        self.TreeCtrl_Refresh(str(yesterday), str(yesterday))
        self.calendar_begin.textCtrl.SetValue(now_time)
        self.calendar_end.textCtrl.SetValue(now_time)
        #wx.adv.LayoutAlgorithm().LayoutWindow(self._leftWindow2, self.tree)
    def time_clear(self,event):
        self.calendar_begin.textCtrl.SetValue('从')
        self.calendar_end.textCtrl.SetValue('至')
        self.store_combox.SetValue('ALL')
        self.member_combox.SetValue('ALL')
        self.Terminal_customer.SetValue('ALL')
        self.time_deal()
        self.TreeCtrl_Refresh(self.start_time, self.end_time)
    def time_deal(self):
        try:
            begin_time = self.calendar_begin.GetValue()  # 获得开始时间
            end_time = self.calendar_end.GetValue()
            if begin_time != "从":
                t2 = str(begin_time).split('/')
                t3 = t2[2], t2[1], t2[0]
                st = '-'
                self.start_time = st.join(t3)
            else:
                self.start_time='1900-01-01'
            # 转化截止时间格式函数为20180719
            if end_time != "至":
                t2_1 = str(end_time).split('/')
                t3_1 = t2_1[2], t2_1[1], t2_1[0]
                st_1 = '-'
                self.end_time = st_1.join(t3_1)
            else:
                now_time = str(time.strftime('%Y-%m-%d', time.localtime()))  # 本地当前时间
                self.end_time=now_time
            if begin_time == "从" and end_time != "至":
                self.start_time='1900-01-10 00:00:00'
        except:
            pass
    def store_information_display(self, evt):  # 合同号combobox下拉列表时触发的事件
        try:
            self.store_combox.Clear()
            self.store_combox.SetValue('ALL')
            # self.AllCancel(self)
            self.get_store_id_list=[]
            self.type = []
            try:
                db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0],
                                     charset=charset)  # 打开数据库连接注charset是否需要
                cursor = db.cursor()  # 使用cursor()方法获取操作游标
                cursor.execute("SELECT `Contract_C_Time`,`Dealer` FROM `order_contract_internal` WHERE 1 ")
                get_store_time= cursor.fetchall()  # 获取开始时间、合同号
                db.close()
            except:
                self.log.WriteText('生产进度管理，YLP_Pane.py中YLP_Contract_Order_Management_Panel连接数据库失败，请进行检查 \r\n')
            self.time_deal()
            if len(get_store_time)==0:
                # print '未查询到合同号'
                pass
            else:
                if self.calendar_begin.GetValue() != "从" and self.calendar_end.GetValue() != "至":
                    # 转化开始时间格式函数为20180719   ##在获取合同号时读取时间范围内的合同号
                    if self.start_time > self.end_time:
                        self.log.WriteText( '生产进度管理，YLP_Pane.py中YLP_Contract_Order_Management_Panel类门店查询时间范围有误，请进行检查 \r\n')
                    else:
                        self.store_id_time_list_get(self.start_time,self.end_time,get_store_time,self.get_store_id_list)
                elif self.calendar_begin.GetValue() != "从" and self.calendar_end.GetValue() == "至":  # 筛选大于某一个值
                    self.store_id_time_list_get(self.start_time, self.end_time, get_store_time, self.get_store_id_list)
                elif self.calendar_begin.GetValue() == "从" and self.calendar_end.GetValue() != "至":  # 筛选大于某一个值
                    self.store_id_time_list_get(self.start_time, self.end_time, get_store_time, self.get_store_id_list)
                else:  # 筛选大于某一个值
                    for i in range(len(get_store_time)):
                        self.store_id_list_get(get_store_time[i][1], self.get_store_id_list)
                if len(self.get_store_id_list) == 0:
                    self.log.WriteText('生产进度管理，YLP_Pane.py中YLP_Contract_Order_Management_Panel类门店查询此时间范围无门店号，请进行检查 \r\n')
                else:
                    self.store_combox.Append('ALL')
                    for i in range(len(self.get_store_id_list)):
                        self.store_combox.Append(self.get_store_id_list[i])
            # self.Refresh()
        except:
            self.log.WriteText('生产进度管理，YLP_Pane.py中YLP_Contract_Order_Management_Panel类门店查询下拉触发事件部分出现错误，请进行检查 \r\n')
    def store_id_list_get(self,date3,date4):
        if date3 != None or date3 != '' or date3 != '0':
            if date3 not in date4:  # 对读到的单号去重后放入列表get_contract_id_list
                date4.append(date3)  #
    def store_id_time_list_get(self,time1,time2,date1,date3):
        for i in range(len(date1)):
            if date1[i][0] == None or date1[i][0] == '' or date1[i][0] == '0':
                pass
            else:
                get_time_str = str(date1[i][0].strftime('%Y-%m-%d'))
                if get_time_str >= time1 and get_time_str <= time2:
                    if date1[i][1] != None or date1[i][1] != '' or date1[i][1] != '0':
                        if date1[i][1] not in date3:  # 对读到的单号去重后放入列表get_contract_id_list
                            date3.append(date1[i][1])  #
    def store_id_click(self,event):
        self.member_combox.SetValue('ALL')
        self.Terminal_customer.SetValue('ALL')
        self.time_deal()
        self.TreeCtrl_Refresh(self.start_time, self.end_time)
    def member_information_display(self, evt):  # 订单号combobox下拉列表时触发的事件
        try:
            self.member_combox.Clear()
            self.member_combox.SetValue('ALL')
            # self.AllCancel(self)
            self.get_member_id_list=[]
            try:
                db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0],
                                     charset=charset)  # 打开数据库连接注charset是否需要
                cursor = db.cursor()  # 使用cursor()方法获取操作游标
                cursor.execute("SELECT `Contract_C_Time`,`Customer_name` FROM `order_contract_internal` WHERE 1 ")
                get_member_time= cursor.fetchall()  # 获取开始时间、合同号
                db.close()
            except:
                self.log.WriteText('生产进度管理，YLP_Pane.py中YLP_Contract_Order_Management_Panel连接数据库失败，请进行检查 \r\n')
            self.time_deal()
            if len(get_member_time)==0:
                pass
            else:
                if self.calendar_begin.GetValue() != "从" and self.calendar_end.GetValue() != "至":
                    # 转化开始时间格式函数为20180719   ##在获取合同号时读取时间范围内的合同号
                    if self.start_time > self.end_time:
                        self.log.WriteText( '生产进度管理，YLP_Pane.py中YLP_Contract_Order_Management_Panel类下单员查询时间范围有误，请进行检查 \r\n')
                    else:
                        self.store_id_time_list_get(self.start_time, self.end_time, get_member_time,self.get_member_id_list)
                elif self.calendar_begin.GetValue() != "从" and self.calendar_end.GetValue() == "至":  # 筛选大于某一个值
                    self.store_id_time_list_get(self.start_time, self.end_time, get_member_time,self.get_member_id_list)
                elif self.calendar_begin.GetValue() == "从" and self.calendar_end.GetValue() != "至":  # 筛选大于某一个值
                    self.store_id_time_list_get(self.start_time, self.end_time, get_member_time,self.get_member_id_list)
                else:  # 筛选大于某一个值
                    for i in range(len(get_member_time)):
                        self.store_id_list_get(get_member_time[i][1], self.get_member_id_list)
                if len(self.get_member_id_list) == 0:
                    self.log.WriteText('生产进度管理，YLP_Pane.py中YLP_Contract_Order_Management_Panel类下单员查询此时间范围无下单员，请进行检查 \r\n')
                else:
                    self.member_combox.Append('ALL')
                    for i in range(len(self.get_member_id_list)):
                        self.member_combox.Append(self.get_member_id_list[i])
            # self.Contract_refresh()
        except:
            self.log.WriteText('生产进度管理，YLP_Pane.py中YLP_Contract_Order_Management_Panel类下单员查询下拉触发事件部分出现错误，请进行检查 \r\n')
    def member_id_click(self,event):
        self.store_combox.SetValue('ALL')
        self.Terminal_customer.SetValue('ALL')
        self.time_deal()
        self.TreeCtrl_Refresh(self.start_time, self.end_time)
    def terminal_information_time_get(self,time1,time2,date1,date4):
        for i in range(len(date1)):
            if date1[i][0] == None or date1[i][0] == '' or date1[i][0] == '0':
                pass
            else:
                get_time_str = str(date1[i][0].strftime('%Y-%m-%d'))
                if get_time_str >= time1 and get_time_str <= time2:
                    if date1[i][1] != None or date1[i][1] != '' or date1[i][1] != '0':
                        if date1[i][1] not in date4:  # 对读到的单号去重后放入列表get_contract_id_list
                            date4.append(date1[i][1])  #
    def terminal_information_get(self,date3,date4):
        if date3 != None or date3 != '' or date3 != '0':
            if date3 not in date4:  # 对读到的单号去重后放入列表get_contract_id_list
                date4.append(date3)  #
    def Terminal_information_display(self, evt):  # 订单号combobox下拉列表时触发的事件
        try:
            self.Terminal_customer.Clear()
            self.Terminal_customer.SetValue('ALL')
            # self.AllCancel(self)
            self.get_terminal_customer_id_list=[]
            self.type = []
            try:
                db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0],
                                     charset=charset)  # 打开数据库连接注charset是否需要
                cursor = db.cursor()  # 使用cursor()方法获取操作游标
                cursor.execute("SELECT `Contract_C_Time`,`Customer_name` FROM `order_order_online` WHERE 1 ")
                get_terminal_customer_time= cursor.fetchall()  # 获取开始时间、合同号
                db.close()
            except:
                self.log.WriteText('生产进度管理，YLP_Pane.py中YLP_Contract_Order_Management_Panel连接数据库失败，请进行检查 \r\n')
            self.time_deal()
            if len(get_terminal_customer_time)==0:
                pass
            else:
                if self.calendar_begin.GetValue() != "从" and self.calendar_end.GetValue() != "至":
                    # 转化开始时间格式函数为20180719   ##在获取合同号时读取时间范围内的合同号
                    if self.start_time > self.end_time:
                        self.log.WriteText( '生产进度管理，YLP_Pane.py中YLP_Contract_Order_Management_Panel类终端客户查询时间范围有误，请进行检查 \r\n')
                    else:
                        self.terminal_information_time_get(self.start_time,self.end_time,get_terminal_customer_time,self.get_terminal_customer_id_list)
                elif self.calendar_begin.GetValue() != "从" and self.calendar_end.GetValue() == "至":  # 筛选大于某一个值
                    self.terminal_information_time_get(self.start_time, self.end_time, get_terminal_customer_time,self.get_terminal_customer_id_list)
                elif self.calendar_begin.GetValue() == "从" and self.calendar_end.GetValue() != "至":  # 筛选大于某一个值
                    self.terminal_information_time_get(self.start_time, self.end_time, get_terminal_customer_time,self.get_terminal_customer_id_list)
                else:  # 筛选大于某一个值
                    for i in range(len(get_terminal_customer_time)):
                        self.terminal_information_get(get_terminal_customer_time[i][1],self.get_terminal_customer_id_list)
                if len(self.get_terminal_customer_id_list) == 0:
                    self.log.WriteText('生产进度管理，YLP_Pane.py中YLP_Contract_Order_Management_Panel类终端客户查询此时间范围无终端客户，请进行检查 \r\n')
                else:
                    self.Terminal_customer.Append('ALL')
                    for i in range(len(self.get_terminal_customer_id_list)):
                        self.Terminal_customer.Append(self.get_terminal_customer_id_list[i])
        except:
            self.log.WriteText(
                '生产进度管理，YLP_Pane.py中YLP_Contract_Order_Management_Panel类终端客户查询下拉触发事件部分出现错误，请进行检查 \r\n')
        # self.Contract_refresh()
    def Terminal_id_click(self,event):
        self.store_combox.SetValue('ALL')
        self.member_combox.SetValue('ALL')
        self.time_deal()
        self.TreeCtrl_Refresh(self.start_time, self.end_time)
    def OnSize(self, event):
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.ylp_Show_Inform_Panel)
        event.Skip()
    def OnQuit(self, event):
        self.Destroy()
    def OnToggleWindow(self, event):

        self._leftWindow1.Show(not self._leftWindow1.IsShown())
        # Leaves bits of itself behind sometimes
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.ylp_Show_Inform_Panel)
        self.ylp_Show_Inform_Panel.Refresh()

        event.Skip()
    def OnFoldPanelBarDrag(self, event):

        # if event.GetDragStatus() == wx.SASH_STATUS_OUT_OF_RANGE:
        #     return

        if event.GetId() == self.ID_WINDOW_LEFT1:
            self._leftWindow1.SetDefaultSize(wx.Size(event.GetDragRect().width, 1000))
        if event.GetId() == self.ID_WINDOW_RIGHT1:
            self._leftWindow2.SetDefaultSize(wx.Size(event.GetDragRect().width, 1000))
        # Leaves bits of itself behind sometimes
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.ylp_Show_Inform_Panel)
        # wx.adv.LayoutAlgorithm().LayoutWindow(self, self.ylp_Show_Inform_Panel)
        self.ylp_Show_Inform_Panel.Refresh()

        event.Skip()
    def ReCreateFoldPanel(self, fpb_flags):

        # delete earlier panel
        self._leftWindow1.DestroyChildren()

        # recreate the foldpanelbar
        self._pnl = fpb.FoldPanelBar(self._leftWindow1, -1, wx.DefaultPosition,
                                     wx.Size(-1,-1), agwStyle=fpb_flags)

        Images = wx.ImageList(16,16)
        Images.Add(GetExpandedIconBitmap())
        Images.Add(GetCollapsedIconBitmap())
        item = self._pnl.AddFoldPanel("按日期查询", collapsed=False,
                                      foldIcons=Images)
        self.date_start=wx.DateTimeFromDMY
        self.date_end=wx.DateTimeFromDMY
        date_start_display = time.strftime("%d/%m/%Y", time.localtime())
        self.calendar_begin=PopDateControl(item, -1)
        self.calendar_begin.textCtrl.SetValue(date_start_display)
        self._pnl.AddFoldPanelWindow(item,self.calendar_begin,fpb.FPB_ALIGN_WIDTH,2,20)
        self.calendar_end=PopDateControl(item, -1)
        self.calendar_end.textCtrl.SetValue(date_start_display)
        self._pnl.AddFoldPanelWindow(item,self.calendar_end,fpb.FPB_ALIGN_WIDTH,2,20)
        btn_date_start=wx.Button(item, wx.ID_ANY, "开始日期查询")
        self._pnl.AddFoldPanelWindow(item, btn_date_start)
        self.btn_today = wx.Button(item, wx.ID_ANY, "今天")
        self._pnl.AddFoldPanelWindow(item, self.btn_today)

        self.btn_yesterday = wx.Button(item, wx.ID_ANY, "昨天")
        self._pnl.AddFoldPanelWindow(item, self.btn_yesterday,spacing=0)
        self.btn_byesterday = wx.Button(item, wx.ID_ANY, "前天")
        self._pnl.AddFoldPanelWindow(item, self.btn_byesterday,spacing=0)
        self.btn_bbyesterday = wx.Button(item, wx.ID_ANY, "大前天")
        self._pnl.AddFoldPanelWindow(item, self.btn_bbyesterday,spacing=0)
        self._pnl.AddFoldPanelSeparator(item)
        btn_date_clear = wx.Button(item, wx.ID_ANY, "清除日期索引")
        self._pnl.AddFoldPanelWindow(item, btn_date_clear)
        item = self._pnl.AddFoldPanel("按客户查询", False, foldIcons=Images)
        self.statictext6 = wx.StaticText(item, -1, label="选择查询的门店：")
        self._pnl.AddFoldPanelWindow(item, self.statictext6)
        self.store_combox = wx.ComboBox(item, -1, pos=(20, 10), style=wx.CB_DROPDOWN)
        self._pnl.AddFoldPanelWindow(item, self.store_combox)

        self.statictext7 = wx.StaticText(item, -1, label="选择查询的下单员：")
        self._pnl.AddFoldPanelWindow(item, self.statictext7)
        self.member_combox = wx.ComboBox(item, -1, pos=(20, 10), style=wx.CB_DROPDOWN)
        self._pnl.AddFoldPanelWindow(item, self.member_combox)

        self.statictext8 = wx.StaticText(item, -1, label="选择查询的终端客户：")
        self._pnl.AddFoldPanelWindow(item, self.statictext8)
        self.Terminal_customer = wx.ComboBox(item, -1, pos=(20, 10), style=wx.CB_DROPDOWN)
        self._pnl.AddFoldPanelWindow(item, self.Terminal_customer)
        self.store_combox.SetValue('ALL')
        self.member_combox.SetValue('ALL')
        self.Terminal_customer.SetValue('ALL')
        btn_date_start.Bind(wx.EVT_BUTTON, self.Get_Seek_DateTime)
        self.btn_today.Bind(wx.EVT_BUTTON, self.Get_Today)
        self.btn_yesterday.Bind(wx.EVT_BUTTON, self.Get_Yesterday)
        self.btn_byesterday.Bind(wx.EVT_BUTTON, self.Get_Byesterday)
        self.btn_bbyesterday.Bind(wx.EVT_BUTTON, self.Get_Bbyesterday)
        btn_date_clear.Bind(wx.EVT_BUTTON, self.time_clear)
        self.store_combox.Bind(wx.EVT_COMBOBOX_DROPDOWN, self.store_information_display)  # 触发合同combobox下拉事件
        self.store_combox.Bind(wx.EVT_COMBOBOX, self.store_id_click)  # 触发合同combobox下拉框中内容被选中事件
        self.member_combox.Bind(wx.EVT_COMBOBOX_DROPDOWN, self.member_information_display)  # 触发订单号combobox下拉事件
        self.member_combox.Bind(wx.EVT_COMBOBOX, self.member_id_click)  # 触发订单号combobox下拉框中内容被选中事件
        self.Terminal_customer.Bind(wx.EVT_COMBOBOX_DROPDOWN, self.Terminal_information_display)  # 触发组件号combobox下拉事件
        self.Terminal_customer.Bind(wx.EVT_COMBOBOX, self.Terminal_id_click)  # 触发组件号combobox下拉事件
        self._leftWindow1.SizeWindows()

    #---------- TreeCtrl 相关的3个函数 -----------------------
    def Create_TreeCtrl(self):
            self._leftWindow2.DestroyChildren()
            date_start = time.strftime("%Y-%m-%d", time.localtime())
            self.TreeCtrl_Refresh(date_start,date_start)

            self.Bind(wx.EVT_CONTEXT_MENU, self.OnContextMenu)
            self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.right_click)
    def TreeCtrl_Refresh(self, start_time, end_time):
        try:
            #self.tree.DeleteAllItems()
            self._leftWindow2.DestroyChildren()
            self.tree = MyTreeCtrl(self._leftWindow2, wx.ID_ANY, wx.DefaultPosition, (400,1000),
                                   wx.TR_HAS_BUTTONS
                                   | wx.TR_EDIT_LABELS
                                   , self.log)
            isz = (16, 16)
            il = wx.ImageList(isz[0], isz[1])
            self.fldridx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, isz))
            self.fldropenidx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_OTHER, isz))
            self.fileidx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, isz))
            self.smidleix = il.Add(images.Smiles.GetBitmap())
            self.tree.SetImageList(il)
            self.il = il
            self.root = self.tree.AddRoot("全部订单")
            self.tree.SetItemData(self.root, None)
            self.tree.SetItemImage(self.root, self.fldridx, wx.TreeItemIcon_Normal)
            self.tree.SetItemImage(self.root, self.fldropenidx, wx.TreeItemIcon_Expanded)
            Order_id_list=[]

            if Is_Database_Connect():
                cursor = DB.cursor()
                #time1 = '2018-07-25'
                if start_time=='1900-01-01':
                    if self.store_combox.GetValue()!='ALL':
                        cursor.execute( "select `Order_id`,`Contract_id` from `order_order_online` where `Dealer`='%s' "% self.store_combox.GetValue())
                        Order_id = cursor.fetchall()
                    elif self.Terminal_customer.GetValue()!='ALL':
                        cursor.execute(
                            "select `Order_id`,`Contract_id` from `order_order_online` where `Customer_name`='%s' " % self.Terminal_customer.GetValue())
                        Order_id = cursor.fetchall()
                    else:
                        cursor.execute(
                            "select `Order_id`,`Contract_id` from `order_order_online` where 1")
                        Order_id = cursor.fetchall()
                else:
                    if self.store_combox.GetValue()!='ALL':
                        cursor.execute( "select `Order_id`,`Contract_id` from `order_order_online` where `First_day`>='%s' and `First_day`<='%s' and `Dealer`='%s' "% (start_time, end_time,self.store_combox.GetValue()))
                        Order_id = cursor.fetchall()
                    elif self.Terminal_customer.GetValue()!='ALL':
                        cursor.execute(
                            "select `Order_id`,`Contract_id` from `order_order_online` where `First_day`>='%s' and `First_day`<='%s' and `Customer_name`='%s' " % (start_time, end_time,self.Terminal_customer.GetValue()))
                        Order_id = cursor.fetchall()
                    else:
                        cursor.execute("select `Order_id`,`Contract_id` from `order_order_online` where `First_day`>='%s' and `First_day`<='%s' " % (start_time, end_time))
                        Order_id = cursor.fetchall()

                if Order_id!=():
                    if self.member_combox.GetValue()!='ALL':
                        cursor.execute(
                            "select `Contract_id` from `order_contract_internal` where `Customer_name`='%s'"% self.member_combox.GetValue())
                        contract_order_id = cursor.fetchall()
                        for i in range(len(Order_id)):
                            for k in range(len(contract_order_id)):
                                if Order_id[i][1]==contract_order_id[k][0]:
                                    Order_id_list.append(list(Order_id[i]))
                                    break
                    else:
                        for i in range(len(Order_id)):
                            Order_id_list.append(list(Order_id[i]))
                    for x in range(len(Order_id_list)):
                        child = self.tree.AppendItem(self.root, '订单：'+str(Order_id[x][0]))
                        self.tree.SetItemData(child, None)
                        self.tree.SetItemImage(child, self.fldridx, wx.TreeItemIcon_Normal)
                        self.tree.SetItemImage(child, self.fldropenidx, wx.TreeItemIcon_Expanded)

                        cursor.execute("select `Sec_id` from `order_section_online` where `Order_id`='%s' " % Order_id[x][0])
                        Sec_id = cursor.fetchall()
                        for y in range(len(Sec_id)):
                            second = self.tree.AppendItem(child, '组件：'+str(Sec_id[y][0]))
                            self.tree.SetItemData(second, None)
                            self.tree.SetItemImage(second, self.fldridx, wx.TreeItemIcon_Normal)
                            self.tree.SetItemImage(second, self.fldropenidx, wx.TreeItemIcon_Expanded)

                            cursor.execute("select `Part_id` from `order_part_online` where `Sec_id`='%s' " % Sec_id[y][0])
                            Part_id = cursor.fetchall()
                            for z in range(len(Part_id)):
                                last = self.tree.AppendItem(second, '部件：'+str(Part_id[z][0]))
                                self.tree.SetItemData(last, None)
                                self.tree.SetItemImage(last, self.fldridx, wx.TreeItemIcon_Normal)
                                self.tree.SetItemImage(last, self.fldropenidx, wx.TreeItemIcon_Expanded)

                                cursor.execute("select `Id` from `order_element_online` where `Part_id`='%s' " % Part_id[z][0])
                                Id = cursor.fetchall()
                                # for h in range(len(Id)):
                                #     item = self.tree.AppendItem(last,  '零件：'+str(Id[h][0]))
                                #     self.tree.SetItemData(item, None)
                                #     self.tree.SetItemImage(item, self.fileidx, wx.TreeItemIcon_Normal)
                                #     self.tree.SetItemImage(item, self.smidleix, wx.TreeItemIcon_Selected)
                else:
                    pass
            self.tree.Expand(self.root)
            self.Bind(wx.EVT_TREE_SEL_CHANGED, self.Datebase_Inform, self.tree)
            #self.tree.AppendItem(self,"")
            wx.adv.LayoutAlgorithm().LayoutWindow(self._leftWindow2, self.tree)    #主要是为了每次刷新数据时，树界面都不变形，且有滚动条。
        except:
            self.log.WriteText("YLP_Contract_Order_Management_Panel类 TreeCtrl_Refresh函数报错，从数据库读取数据失败，本数据用于显示树结构 \r\n")
    def Datebase_Inform(self, event):
        # try:
            self.item = event.GetItem()
            if self.item:
                tree_id = self.tree.GetItemText(self.item)
                if tree_id == '全部订单':
                    pass
                else:
                    if 'O' in tree_id and 'S' not in tree_id and 'P' not in tree_id and 'ID' not in tree_id:
                        if Is_Database_Connect():
                            cursor = DB.cursor()
                            tree_id=tree_id.split("：")
                            cursor.execute( "select `Order_id`,`Customer_name`,`Customer_tel`,`Customer_address`,`Order_price`,`Order_area` from `order_order_online` where `Order_id`='%s' " % tree_id[-1])
                            order_inform = cursor.fetchone()
                            #cursor.execute( "select `Sec_id`,`Sec_series`,`Sec_color`,`Sec_thick`,`Sec_edge` from `order_section_online` where `Order_id`='%s' " % tree_id[-1])
                            #cursor.execute( "select `Sec_id`,`Sec_thick`,`Sec_color`,`Sec_series`,`Sec_edge` from `order_section_online` where `Order_id`='%s' " % tree_id[-1])
                            cursor.execute( "select `Sec_id`,`Index_of_base_material_thickness`,`Sec_color`,`Sec_series`,`Sec_edge` from `order_section_online` where `Order_id`='%s' " % tree_id[-1])
                            sec_inform = cursor.fetchall()
                            self.ylp_Show_Inform_Panel.PDF_Page(order_inform,sec_inform,2)
                    if 'S' in tree_id and 'P' not in tree_id and 'ID' not in tree_id:
                        if Is_Database_Connect():
                            cursor = DB.cursor()
                            tree_id = tree_id.split("：")
                            cursor.execute("select `Part_id`,`Door_type`,`Element_type_id`,`Door_color`,`Door_height` ,`Door_width`,`Door_thick`,`Archaize`,`Door_area`,`Door_price`,`Hole`,`Open_way`,`Edge_type`,`State` from `order_part_online` where `Sec_id`='%s' " % tree_id[-1])
                            part_inform = cursor.fetchall()
                            self.ylp_Show_Inform_Panel.Gride_Page(part_inform)
                    if 'P' in tree_id and 'ID' not in tree_id:
                        # pass
                        if Is_Database_Connect():
                            cursor = DB.cursor()
                            tree_id = tree_id.split("：")
                            cursor.execute("select `Door_type`,`Door_color`,`Door_height`,`Door_width`,`Door_thick` from `order_part_online` where `Part_id`='%s'" % tree_id[-1])
                            part_inform = cursor.fetchone()
                            cursor.execute(
                                "select `Id`,`Board_type`,`Element_type_id`,`Color`,`Board_height`,`Board_width`,`Board_thick`,`Archaize`,`Hole`,`Open_way`,`Edge_type`,`State` from `order_element_online` where `Part_id`='%s' " %
                                tree_id[-1])
                            part_information_transfer = cursor.fetchall()
                            part_information_list=list(part_information_transfer)
                            part_information_list.sort(key=lambda x: [x[2]])
                            part_information=tuple(part_information_list)
                            self.ylp_Show_Inform_Panel.Show_Part_Inform(part_inform,part_information)
                    # if 'ID' in tree_id:
                    #     if Is_Database_Connect():
                    #         cursor = DB.cursor()
                    #         tree_id = tree_id.split("：")
                    #         cursor.execute( "select `Board_type`,`Color`,`Board_height`,`Board_width`,`Board_thick` from `order_element_online` where `Id`='%s' " % tree_id[-1])
                    #         id_inform = cursor.fetchone()
                    #         self.ylp_Show_Inform_Panel.Show_ID_Inform(id_inform)
            event.Skip()
        # except:
        #     self.log.WriteText("YLP_Contract_Order_Management_Panel类 Datebase_Inform函数报错，从数据库读取数据失败，本数据用于提供右侧主面板的信息显示 \r\n")

    def right_click(self,event):
        self.item = event.GetItem()
        if self.item:
            self.select_code = self.tree.GetItemText(self.item)

     #鼠标右击弹出的菜单
    def OnContextMenu(self, event):
        pass
            # if not hasattr(self, "popupID1"):
            #     #self.popupID3 = wx.NewId()
            #     self.Bind(wx.EVT_MENU, self.OnPopupOne, id=YLP_popupID1)
            #     self.Bind(wx.EVT_MENU, self.Expend, id=YLP_popupID2)
            #     #self.Bind(wx.EVT_MENU, self.Expend, id=self.popupID3)
            #
            # menu = wx.Menu()
            # item = wx.MenuItem(menu, YLP_popupID1, "查询工期进度")
            # bmp = images.Smiles.GetBitmap()
            # item.SetBitmap(bmp)
            # menu.Append(item)
            # menu.Append(YLP_popupID2, "展开")
            # #menu.Append(self.popupID3, "合起")
            # self.PopupMenu(menu)
            #menu.Destroy()
    def OnPopupOne(self, event):
        self.parent.SetSelection(0)
        select_code1 = self.select_code.split("：")
        if 'P' in select_code1[1] :
            self.Port.SetSelection(4)
            select_code2 = select_code1[-1]
            self.fyf_progress_id.YLP_Combox_Setvalue(select_code2)
        elif 'S' in select_code1[1] :
            self.Port.SetSelection(3)
            select_code2 = select_code1[-1]
            self.FYF_Progress_Manage_Panel.YLP_Combox_Setvalue(select_code2)
        else:
            self.Port.SetSelection(2)
            select_code2 = select_code1[-1]
            self.fyf_progress_sec.YLP_Combox_Setvalue(select_code2)
    def Expend(self,event):
        self.tree.ExpandAllChildren(self.item)
        # self.tree.Expand(self.item)
    #----------------------------------------
    def onDateStart(self,event):
        self.date_start=self.calendar_begin.GetValue()
        self.date_end=self.calendar_end.GetValue()
        self.log.WriteText("天外天系统收到操作员控制指令，开始执行日期查询操作，起始日期："+str(self.date_start)+"，终止日期："+str(self.date_end)+"\r\n")
    def OnCreateBottomStyle(self, event):

        # recreate with style collapse to bottom, which means
        # all panels that are collapsed are placed at the bottom,
        # or normal

        if event.IsChecked():
            self.GetMenuBar().Check(self._singlestyle, False)
            self.GetMenuBar().Check(self._exclusivestyle, False)
            self._flags = self._flags & ~fpb.FPB_SINGLE_FOLD
            self._flags = self._flags & ~fpb.FPB_EXCLUSIVE_FOLD
            self._flags = self._flags | fpb.FPB_COLLAPSE_TO_BOTTOM
        else:
            self._flags = self._flags & ~fpb.FPB_COLLAPSE_TO_BOTTOM

        self.ReCreateFoldPanel(self._flags)
        #self.Create_TreeCtrl()
    def OnCreateNormalStyle(self, event):

        # recreate with style where only one panel at the time is
        # allowed to be opened

        if event.IsChecked():
            self.GetMenuBar().Check(self._bottomstyle, False)
            self.GetMenuBar().Check(self._exclusivestyle, False)
            self._flags = self._flags & ~fpb.FPB_EXCLUSIVE_FOLD
            self._flags = self._flags & ~fpb.FPB_COLLAPSE_TO_BOTTOM
            self._flags = self._flags | fpb.FPB_SINGLE_FOLD
        else:
            self._flags = self._flags & ~fpb.FPB_SINGLE_FOLD

        self.ReCreateFoldPanel(self._flags)
        #self.Create_TreeCtrl()
    def OnCreateExclusiveStyle(self, event):
        # recreate with style where only one panel at the time is
        # allowed to be opened and the others are collapsed to bottom
        if event.IsChecked():
            self.GetMenuBar().Check(self._singlestyle, False)
            self.GetMenuBar().Check(self._bottomstyle, False)
            self._flags = self._flags & ~fpb.FPB_SINGLE_FOLD
            self._flags = self._flags & ~fpb.FPB_COLLAPSE_TO_BOTTOM
            self._flags = self._flags | fpb.FPB_EXCLUSIVE_FOLD
        else:
            self._flags = self._flags & ~fpb.FPB_EXCLUSIVE_FOLD
        self.ReCreateFoldPanel(self._flags)
        #self.Create_TreeCtrl()
    def OnCollapseMe(self, event):
        for i in range(0, self._pnl.GetCount()):
            item = self._pnl.GetFoldPanel(i)
            self._pnl.Collapse(item)
    def OnExpandMe(self, event):
        style = fpb.CaptionBarStyle()
        counter = 0
        for items in self.radiocontrols:
            if items.GetValue():
                break
            counter = counter + 1
        if counter == 0:
            mystyle = fpb.CAPTIONBAR_GRADIENT_V
        elif counter == 1:
            mystyle = fpb.CAPTIONBAR_GRADIENT_H
        elif counter == 2:
            mystyle = fpb.CAPTIONBAR_SINGLE
        elif counter == 3:
            mystyle = fpb.CAPTIONBAR_RECTANGLE
        else:
            mystyle = fpb.CAPTIONBAR_FILLED_RECTANGLE

        # style.SetCaptionStyle(mystyle)
        # self._pnl.ApplyCaptionStyleAll(style)
    def OnSlideColour(self, event):

        col1 = wx.Colour(self._rslider1.GetValue(), self._gslider1.GetValue(),
                         self._bslider1.GetValue())
        col2 = wx.Colour(self._rslider2.GetValue(), self._gslider2.GetValue(),
                         self._bslider2.GetValue())

        style = fpb.CaptionBarStyle()

        counter = 0
        for items in self.radiocontrols:
            if items.GetValue():
                break

            counter = counter + 1

        if counter == 0:
            mystyle = fpb.CAPTIONBAR_GRADIENT_V
        elif counter == 1:
            mystyle = fpb.CAPTIONBAR_GRADIENT_H
        elif counter == 2:
            mystyle = fpb.CAPTIONBAR_SINGLE
        elif counter == 3:
            mystyle = fpb.CAPTIONBAR_RECTANGLE
        else:
            mystyle = fpb.CAPTIONBAR_FILLED_RECTANGLE

        style.SetFirstColour(col1)
        style.SetSecondColour(col2)
        style.SetCaptionStyle(mystyle)

        item = self._pnl.GetFoldPanel(0)
        self._pnl.ApplyCaptionStyle(item, style)
    def OnStyleChange(self, event):

        style = fpb.CaptionBarStyle()

        eventid = event.GetId()

        if eventid == self.ID_USE_HGRADIENT:
            style.SetCaptionStyle(fpb.CAPTIONBAR_GRADIENT_H)

        elif eventid == self.ID_USE_VGRADIENT:
            style.SetCaptionStyle(fpb.CAPTIONBAR_GRADIENT_V)

        elif eventid == self.ID_USE_SINGLE:
            style.SetCaptionStyle(fpb.CAPTIONBAR_SINGLE)

        elif eventid == self.ID_USE_RECTANGLE:
            style.SetCaptionStyle(fpb.CAPTIONBAR_RECTANGLE)

        elif eventid == self.ID_USE_FILLED_RECTANGLE:
            style.SetCaptionStyle(fpb.CAPTIONBAR_FILLED_RECTANGLE)

        else:
            raise "ERROR: Undefined Style Selected For CaptionBar: " + repr(eventid)

        col1 = wx.Colour(self._rslider1.GetValue(), self._gslider1.GetValue(),
                         self._bslider1.GetValue())
        col2 = wx.Colour(self._rslider2.GetValue(), self._gslider2.GetValue(),
                         self._bslider2.GetValue())

        style.SetFirstColour(col1)
        style.SetSecondColour(col2)

        if self._single.GetValue():
            item = self._pnl.GetFoldPanel(1)
            self._pnl.ApplyCaptionStyle(item, style)
        else:
            self._pnl.ApplyCaptionStyleAll(style)
    def CreateMenuBar(self, with_window=False):

        # Make a menubar
        file_menu = wx.Menu()

        FPBTEST_QUIT = wx.NewId()
        FPBTEST_REFRESH = wx.NewId()
        FPB_BOTTOM_FOLD = wx.NewId()
        FPB_SINGLE_FOLD = wx.NewId()
        FPB_EXCLUSIVE_FOLD = wx.NewId()
        FPBTEST_TOGGLE_WINDOW = wx.NewId()
        FPBTEST_ABOUT = wx.NewId()

        file_menu.Append(FPBTEST_QUIT, "&Exit")

        option_menu = None

        if with_window:
            # Dummy option
            option_menu = wx.Menu()
            option_menu.Append(FPBTEST_REFRESH, "&Refresh picture")

        # make fold panel menu

        fpb_menu = wx.Menu()
        fpb_menu.AppendCheckItem(FPB_BOTTOM_FOLD, "Create with &fpb.FPB_COLLAPSE_TO_BOTTOM")

        # Now Implemented!
        fpb_menu.AppendCheckItem(FPB_SINGLE_FOLD, "Create with &fpb.FPB_SINGLE_FOLD")

        # Now Implemented!
        fpb_menu.AppendCheckItem(FPB_EXCLUSIVE_FOLD, "Create with &fpb.FPB_EXCLUSIVE_FOLD")

        fpb_menu.AppendSeparator()
        fpb_menu.Append(FPBTEST_TOGGLE_WINDOW, "&Toggle FoldPanelBar")

        help_menu = wx.Menu()
        help_menu.Append(FPBTEST_ABOUT, "&About")

        menu_bar = wx.MenuBar()

        menu_bar.Append(file_menu, "&File")
        menu_bar.Append(fpb_menu, "&FoldPanel")

        if option_menu:
            menu_bar.Append(option_menu, "&Options")

        menu_bar.Append(help_menu, "&Help")

        self.Bind(wx.EVT_MENU, self.OnAbout, id=FPBTEST_ABOUT)
        self.Bind(wx.EVT_MENU, self.OnQuit, id=FPBTEST_QUIT)
        self.Bind(wx.EVT_MENU, self.OnToggleWindow, id=FPBTEST_TOGGLE_WINDOW)
        self.Bind(wx.EVT_MENU, self.OnCreateBottomStyle, id=FPB_BOTTOM_FOLD)
        self.Bind(wx.EVT_MENU, self.OnCreateNormalStyle, id=FPB_SINGLE_FOLD)
        self.Bind(wx.EVT_MENU, self.OnCreateExclusiveStyle, id=FPB_EXCLUSIVE_FOLD)

        self._bottomstyle = FPB_BOTTOM_FOLD
        self._singlestyle = FPB_SINGLE_FOLD
        self._exclusivestyle = FPB_EXCLUSIVE_FOLD

        return menu_bar
class YLP_Contract_Order_Complete_Management_Panel(wx.Panel):
    def __init__(self, parent,log, id=wx.ID_ANY, title="", pos=wx.DefaultPosition,
                 size=(700,650), style=wx.DEFAULT_FRAME_STYLE):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.select_code = 0
        self._flags = 0
        self.log = log
        self._leftWindow1 = wx.adv.SashLayoutWindow(self, 101, wx.DefaultPosition,
                                                wx.Size(200, 1000), wx.NO_BORDER |
                                                wx.adv.SW_3D | wx.CLIP_CHILDREN)
        self._leftWindow1.SetDefaultSize(wx.Size(220, 1000))
        self._leftWindow1.SetOrientation(wx.adv.LAYOUT_VERTICAL)
        self._leftWindow1.SetAlignment(wx.adv.LAYOUT_LEFT)
        self._leftWindow1.SetSashVisible(wx.adv.SASH_RIGHT, True)
        self._leftWindow1.SetExtraBorderSize(10)
        self._pnl = 0
        #self.ylp_Section_Inform_Grid=Section_Inform_Grid(self)
        self.ylp_Show_Inform_Panel=Show_Inform_Panel(self,self.log)

        self.ID_WINDOW_LEFT1 = 101
        self.ID_WINDOW_RIGHT1 = 102
        self._leftWindow1.Bind(wx.adv.EVT_SASH_DRAGGED_RANGE, self.OnFoldPanelBarDrag,
                               id=101, id2=102)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        self.Bind(wx.EVT_SCROLL, self.OnSlideColour)
        self.ReCreateFoldPanel(0)

        self._leftWindow2 = wx.adv.SashLayoutWindow(self, 102, wx.DefaultPosition,
                                                    wx.Size(300, 800), wx.NO_BORDER |
                                                    wx.adv.SW_3D | wx.CLIP_CHILDREN)
        self._leftWindow2.SetDefaultSize(wx.Size(320, 800))
        self._leftWindow2.SetOrientation(wx.adv.LAYOUT_VERTICAL)
        self._leftWindow2.SetAlignment(wx.adv.LAYOUT_LEFT)
        self._leftWindow2.SetSashVisible(wx.adv.SASH_RIGHT, True)
        self._leftWindow2.SetExtraBorderSize(10)
        self._leftWindow2.Bind(wx.adv.EVT_SASH_DRAGGED_RANGE, self.OnFoldPanelBarDrag,
                               id=101, id2=102)
        self._pnl = 0
        self.Create_TreeCtrl()
        self.time_deal()
        self.TreeCtrl_Refresh(self.start_time,self.end_time)

    def Get_Seek_DateTime(self,event):
        self.time_deal()
        self.TreeCtrl_Refresh(self.start_time,self.end_time)
    def Get_Today(self,event):
        date_start_display = time.strftime("%d/%m/%Y", time.localtime())
        date_start=time.strftime("%Y-%m-%d", time.localtime())
        date_end=date_start
        self.store_combox.SetValue('ALL')
        self.member_combox.SetValue('ALL')
        self.Terminal_customer.SetValue('ALL')
        self.calendar_begin.textCtrl.SetValue(date_start_display)
        self.calendar_end.textCtrl.SetValue(date_start_display)
        self.TreeCtrl_Refresh(date_start, date_end)

        #wx.adv.LayoutAlgorithm().LayoutWindow(self._leftWindow2,self.tree)
    def Get_Yesterday(self,event):
        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        yesterday = today - oneday
        now_time = (today - oneday).strftime('%d/%m/%Y')  # 本地当前时间
        self.store_combox.SetValue('ALL')
        self.member_combox.SetValue('ALL')
        self.Terminal_customer.SetValue('ALL')
        self.TreeCtrl_Refresh(str(yesterday), str(yesterday))
        self.calendar_begin.textCtrl.SetValue(now_time)
        self.calendar_end.textCtrl.SetValue(now_time)
        #wx.adv.LayoutAlgorithm().LayoutWindow(self._leftWindow2, self.tree)
    def Get_Byesterday(self,event):
        today = datetime.date.today()
        oneday = datetime.timedelta(days=2)
        yesterday = today - oneday
        now_time = (today - oneday).strftime('%d/%m/%Y')  # 本地当前时间
        self.store_combox.SetValue('ALL')
        self.member_combox.SetValue('ALL')
        self.Terminal_customer.SetValue('ALL')
        self.TreeCtrl_Refresh(str(yesterday), str(yesterday))
        self.calendar_begin.textCtrl.SetValue(now_time)
        self.calendar_end.textCtrl.SetValue(now_time)
        #wx.adv.LayoutAlgorithm().LayoutWindow(self._leftWindow2, self.tree)
    def Get_Bbyesterday(self,event):
        today = datetime.date.today()
        oneday = datetime.timedelta(days=3)
        yesterday = today - oneday
        now_time = (today - oneday).strftime('%d/%m/%Y')  # 本地当前时间
        self.store_combox.SetValue('ALL')
        self.member_combox.SetValue('ALL')
        self.Terminal_customer.SetValue('ALL')
        self.TreeCtrl_Refresh(str(yesterday), str(yesterday))
        self.calendar_begin.textCtrl.SetValue(now_time)
        self.calendar_end.textCtrl.SetValue(now_time)
        #wx.adv.LayoutAlgorithm().LayoutWindow(self._leftWindow2, self.tree)
    def time_clear(self,event):
        self.calendar_begin.textCtrl.SetValue('从')
        self.calendar_end.textCtrl.SetValue('至')
        self.store_combox.SetValue('ALL')
        self.member_combox.SetValue('ALL')
        self.Terminal_customer.SetValue('ALL')
        self.time_deal()
        self.TreeCtrl_Refresh(self.start_time, self.end_time)
    def time_deal(self):
        begin_time = self.calendar_begin.GetValue()  # 获得开始时间
        end_time = self.calendar_end.GetValue()
        if begin_time != "从":
            t2 = str(begin_time).split('/')
            t3 = t2[2], t2[1], t2[0]
            st = '-'
            self.start_time = st.join(t3)
        else:
            self.start_time='1900-01-01'
        # 转化截止时间格式函数为20180719
        if end_time != "至":
            t2_1 = str(end_time).split('/')
            t3_1 = t2_1[2], t2_1[1], t2_1[0]
            st_1 = '-'
            self.end_time = st_1.join(t3_1)
        else:
            now_time = str(time.strftime('%Y-%m-%d', time.localtime()))  # 本地当前时间
            self.end_time=now_time
        if begin_time == "从" and end_time != "至":
            self.start_time='1900-01-10 00:00:00'
    def store_information_display(self, evt):  # 合同号combobox下拉列表时触发的事件
        try:
            self.store_combox.Clear()
            self.store_combox.SetValue('ALL')
            # self.AllCancel(self)
            self.get_store_id_list=[]
            self.type = []
            try:
                db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0],
                                     charset=charset)  # 打开数据库连接注charset是否需要
                cursor = db.cursor()  # 使用cursor()方法获取操作游标
                cursor.execute("SELECT `Contract_C_Time`,`Dealer` FROM `order_contract_internal` WHERE `State`>=130 ")
                get_store_time= cursor.fetchall()  # 获取开始时间、合同号
                db.close()
            except:
                self.log.WriteText('生产进度管理，YLP_Pane.py中YLP_Contract_Order_Complete_Management_Panel连接数据库失败，请进行检查 \r\n')
            self.time_deal()
            if len(get_store_time)==0:
                # print '未查询到合同号'
                pass
            else:
                if self.calendar_begin.GetValue() != "从" and self.calendar_end.GetValue() != "至":
                    # 转化开始时间格式函数为20180719   ##在获取合同号时读取时间范围内的合同号
                    if self.start_time > self.end_time:
                        self.log.WriteText( '生产进度管理，YLP_Pane.py中YLP_Contract_Order_Complete_Management_Panel类门店查询时间范围有误，请进行检查 \r\n')
                    else:
                        self.store_id_time_list_get(self.start_time,self.end_time,get_store_time,self.get_store_id_list)
                elif self.calendar_begin.GetValue() != "从" and self.calendar_end.GetValue() == "至":  # 筛选大于某一个值
                    self.store_id_time_list_get(self.start_time, self.end_time, get_store_time, self.get_store_id_list)
                elif self.calendar_begin.GetValue() == "从" and self.calendar_end.GetValue() != "至":  # 筛选大于某一个值
                    self.store_id_time_list_get(self.start_time, self.end_time, get_store_time, self.get_store_id_list)
                else:  # 筛选大于某一个值
                    for i in range(len(get_store_time)):
                        self.store_id_list_get(get_store_time[i][1], self.get_store_id_list)
                if len(self.get_store_id_list) == 0:
                    self.log.WriteText('生产进度管理，YLP_Pane.py中YLP_Contract_Order_Complete_Management_Panel类门店查询此时间范围无门店号，请进行检查 \r\n')
                else:
                    self.store_combox.Append('ALL')
                    for i in range(len(self.get_store_id_list)):
                        self.store_combox.Append(self.get_store_id_list[i])
            # self.Refresh()
        except:
            self.log.WriteText('生产进度管理，YLP_Pane.py中YLP_Contract_Order_Complete_Management_Panel类门店查询下拉触发事件部分出现错误，请进行检查 \r\n')
    def store_id_list_get(self,date3,date4):
        if date3 != None or date3 != '' or date3 != '0':
            if date3 not in date4:  # 对读到的单号去重后放入列表get_contract_id_list
                date4.append(date3)  #
    def store_id_time_list_get(self,time1,time2,date1,date3):
        for i in range(len(date1)):
            if date1[i][0] == None or date1[i][0] == '' or date1[i][0] == '0':
                pass
            else:
                get_time_str = str(date1[i][0].strftime('%Y-%m-%d'))
                if get_time_str >= time1 and get_time_str <= time2:
                    if date1[i][1] != None or date1[i][1] != '' or date1[i][1] != '0':
                        if date1[i][1] not in date3:  # 对读到的单号去重后放入列表get_contract_id_list
                            date3.append(date1[i][1])  #
    def store_id_click(self,event):
        self.member_combox.SetValue('ALL')
        self.Terminal_customer.SetValue('ALL')
        self.time_deal()
        self.TreeCtrl_Refresh(self.start_time, self.end_time)
    def member_information_display(self, evt):  # 订单号combobox下拉列表时触发的事件
        try:
            self.member_combox.Clear()
            self.member_combox.SetValue('ALL')
            # self.AllCancel(self)
            self.get_member_id_list=[]
            try:
                db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0],
                                     charset=charset)  # 打开数据库连接注charset是否需要
                cursor = db.cursor()  # 使用cursor()方法获取操作游标
                cursor.execute("SELECT `Contract_C_Time`,`Customer_name` FROM `order_contract_internal` WHERE `State`>=130 ")
                get_member_time= cursor.fetchall()  # 获取开始时间、合同号
                db.close()
            except:
                self.log.WriteText('生产进度管理，YLP_Pane.py中YLP_Contract_Order_Complete_Management_Panel连接数据库失败，请进行检查 \r\n')
            self.time_deal()
            if len(get_member_time)==0:
                pass
            else:
                if self.calendar_begin.GetValue() != "从" and self.calendar_end.GetValue() != "至":
                    # 转化开始时间格式函数为20180719   ##在获取合同号时读取时间范围内的合同号
                    if self.start_time > self.end_time:
                        self.log.WriteText( '生产进度管理，YLP_Pane.py中YLP_Contract_Order_Complete_Management_Panel类下单员查询时间范围有误，请进行检查 \r\n')
                    else:
                        self.store_id_time_list_get(self.start_time, self.end_time, get_member_time,self.get_member_id_list)
                elif self.calendar_begin.GetValue() != "从" and self.calendar_end.GetValue() == "至":  # 筛选大于某一个值
                    self.store_id_time_list_get(self.start_time, self.end_time, get_member_time,self.get_member_id_list)
                elif self.calendar_begin.GetValue() == "从" and self.calendar_end.GetValue() != "至":  # 筛选大于某一个值
                    self.store_id_time_list_get(self.start_time, self.end_time, get_member_time,self.get_member_id_list)
                else:  # 筛选大于某一个值
                    for i in range(len(get_member_time)):
                        self.store_id_list_get(get_member_time[i][1], self.get_member_id_list)
                if len(self.get_member_id_list) == 0:
                    self.log.WriteText('生产进度管理，YLP_Pane.py中YLP_Contract_Order_Complete_Management_Panel类下单员查询此时间范围无下单员，请进行检查 \r\n')
                else:
                    self.member_combox.Append('ALL')
                    for i in range(len(self.get_member_id_list)):
                        self.member_combox.Append(self.get_member_id_list[i])
            # self.Contract_refresh()
        except:
            self.log.WriteText('生产进度管理，YLP_Pane.py中YLP_Contract_Order_Complete_Management_Panel类下单员查询下拉触发事件部分出现错误，请进行检查 \r\n')
    def member_id_click(self,event):
        self.store_combox.SetValue('ALL')
        self.Terminal_customer.SetValue('ALL')
        self.time_deal()
        self.TreeCtrl_Refresh(self.start_time, self.end_time)
    def terminal_information_time_get(self,time1,time2,date1,date4):
        for i in range(len(date1)):
            if date1[i][0] == None or date1[i][0] == '' or date1[i][0] == '0':
                pass
            else:
                get_time_str = str(date1[i][0].strftime('%Y-%m-%d'))
                if get_time_str >= time1 and get_time_str <= time2:
                    if date1[i][1] != None or date1[i][1] != '' or date1[i][1] != '0':
                        if date1[i][1] not in date4:  # 对读到的单号去重后放入列表get_contract_id_list
                            date4.append(date1[i][1])  #
    def terminal_information_get(self,date3,date4):
        if date3 != None or date3 != '' or date3 != '0':
            if date3 not in date4:  # 对读到的单号去重后放入列表get_contract_id_list
                date4.append(date3)  #
    def Terminal_information_display(self, evt):  # 订单号combobox下拉列表时触发的事件
        try:
            self.Terminal_customer.Clear()
            self.Terminal_customer.SetValue('ALL')
            # self.AllCancel(self)
            self.get_terminal_customer_id_list=[]
            self.type = []
            try:
                db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0],
                                     charset=charset)  # 打开数据库连接注charset是否需要
                cursor = db.cursor()  # 使用cursor()方法获取操作游标
                cursor.execute("SELECT `Contract_C_Time`,`Customer_name` FROM `order_order_complete` WHERE 1 ")
                get_terminal_customer_time= cursor.fetchall()  # 获取开始时间、合同号
                db.close()
            except:
                self.log.WriteText('生产进度管理，YLP_Pane.py中YLP_Contract_Order_Complete_Management_Panel连接数据库失败，请进行检查 \r\n')
            self.time_deal()
            if len(get_terminal_customer_time)==0:
                pass
            else:
                if self.calendar_begin.GetValue() != "从" and self.calendar_end.GetValue() != "至":
                    # 转化开始时间格式函数为20180719   ##在获取合同号时读取时间范围内的合同号
                    if self.start_time > self.end_time:
                        self.log.WriteText( '生产进度管理，YLP_Pane.py中YLP_Contract_Order_Complete_Management_Panel类终端客户查询时间范围有误，请进行检查 \r\n')
                    else:
                        self.terminal_information_time_get(self.start_time,self.end_time,get_terminal_customer_time,self.get_terminal_customer_id_list)
                elif self.calendar_begin.GetValue() != "从" and self.calendar_end.GetValue() == "至":  # 筛选大于某一个值
                    self.terminal_information_time_get(self.start_time, self.end_time, get_terminal_customer_time,self.get_terminal_customer_id_list)
                elif self.calendar_begin.GetValue() == "从" and self.calendar_end.GetValue() != "至":  # 筛选大于某一个值
                    self.terminal_information_time_get(self.start_time, self.end_time, get_terminal_customer_time,self.get_terminal_customer_id_list)
                else:  # 筛选大于某一个值
                    for i in range(len(get_terminal_customer_time)):
                        self.terminal_information_get(get_terminal_customer_time[i][1],self.get_terminal_customer_id_list)
                if len(self.get_terminal_customer_id_list) == 0:
                    self.log.WriteText('生产进度管理，YLP_Pane.py中YLP_Contract_Order_Complete_Management_Panel类终端客户查询此时间范围无终端客户，请进行检查 \r\n')
                else:
                    self.Terminal_customer.Append('ALL')
                    for i in range(len(self.get_terminal_customer_id_list)):
                        self.Terminal_customer.Append(self.get_terminal_customer_id_list[i])
        except:
            self.log.WriteText('生产进度管理，YLP_Pane.py中YLP_Contract_Order_Complete_Management_Panel类终端客户查询下拉触发事件部分出现错误，请进行检查 \r\n')
    def Terminal_id_click(self,event):
        self.store_combox.SetValue('ALL')
        self.member_combox.SetValue('ALL')
        self.time_deal()
        self.TreeCtrl_Refresh(self.start_time, self.end_time)
    def OnSize(self, event):
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.ylp_Show_Inform_Panel)
        event.Skip()
    def OnSashDrag(self, event):
        if event.GetDragStatus() == wx.adv.SASH_STATUS_OUT_OF_RANGE:
            return
        eobj = event.GetEventObject()
        if eobj is self.leftWindow1:
            self.leftWindow1.SetDefaultSize((event.GetDragRect().width, 1000))
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.ylp_Show_Inform_Panel)
    def OnQuit(self, event):
        self.Destroy()
    def OnToggleWindow(self, event):

        self._leftWindow1.Show(not self._leftWindow1.IsShown())
        # Leaves bits of itself behind sometimes
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.ylp_Show_Inform_Panel)
        self.ylp_Show_Inform_Panel.Refresh()

        event.Skip()
    def OnFoldPanelBarDrag(self, event):

        # if event.GetDragStatus() == wx.SASH_STATUS_OUT_OF_RANGE:
        #     return

        if event.GetId() == self.ID_WINDOW_LEFT1:
            self._leftWindow1.SetDefaultSize(wx.Size(event.GetDragRect().width, 1000))
        if event.GetId() == self.ID_WINDOW_RIGHT1:
            self._leftWindow2.SetDefaultSize(wx.Size(event.GetDragRect().width, 1000))
        # Leaves bits of itself behind sometimes
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.ylp_Show_Inform_Panel)
        # wx.adv.LayoutAlgorithm().LayoutWindow(self, self.ylp_Show_Inform_Panel)
        self.ylp_Show_Inform_Panel.Refresh()

        event.Skip()
    def ReCreateFoldPanel(self, fpb_flags):

        # delete earlier panel
        self._leftWindow1.DestroyChildren()

        # recreate the foldpanelbar
        self._pnl = fpb.FoldPanelBar(self._leftWindow1, -1, wx.DefaultPosition,
                                     wx.Size(-1,-1), agwStyle=fpb_flags)

        Images = wx.ImageList(16,16)
        Images.Add(GetExpandedIconBitmap())
        Images.Add(GetCollapsedIconBitmap())
        item = self._pnl.AddFoldPanel("按日期查询", collapsed=False,
                                      foldIcons=Images)
        self.date_start=wx.DateTimeFromDMY
        self.date_end=wx.DateTimeFromDMY
        date_start_display = time.strftime("%d/%m/%Y", time.localtime())
        self.calendar_begin=PopDateControl(item, -1)
        self.calendar_begin.textCtrl.SetValue(date_start_display)
        self._pnl.AddFoldPanelWindow(item,self.calendar_begin,fpb.FPB_ALIGN_WIDTH,2,20)
        self.calendar_end=PopDateControl(item, -1)
        self.calendar_end.textCtrl.SetValue(date_start_display)
        self._pnl.AddFoldPanelWindow(item,self.calendar_end,fpb.FPB_ALIGN_WIDTH,2,20)
        btn_date_start=wx.Button(item, wx.ID_ANY, "开始日期查询")
        self._pnl.AddFoldPanelWindow(item, btn_date_start)
        self.btn_today = wx.Button(item, wx.ID_ANY, "今天")
        self._pnl.AddFoldPanelWindow(item, self.btn_today)

        self.btn_yesterday = wx.Button(item, wx.ID_ANY, "昨天")
        self._pnl.AddFoldPanelWindow(item, self.btn_yesterday,spacing=0)
        self.btn_byesterday = wx.Button(item, wx.ID_ANY, "前天")
        self._pnl.AddFoldPanelWindow(item, self.btn_byesterday,spacing=0)
        self.btn_bbyesterday = wx.Button(item, wx.ID_ANY, "大前天")
        self._pnl.AddFoldPanelWindow(item, self.btn_bbyesterday,spacing=0)
        self._pnl.AddFoldPanelSeparator(item)
        btn_date_clear = wx.Button(item, wx.ID_ANY, "清除日期索引")
        self._pnl.AddFoldPanelWindow(item, btn_date_clear)
        item = self._pnl.AddFoldPanel("按客户查询", False, foldIcons=Images)
        self.statictext6 = wx.StaticText(item, -1, label="选择查询的门店：")
        self._pnl.AddFoldPanelWindow(item, self.statictext6)
        self.store_combox = wx.ComboBox(item, -1, pos=(20, 10), style=wx.CB_DROPDOWN)
        self._pnl.AddFoldPanelWindow(item, self.store_combox)

        self.statictext7 = wx.StaticText(item, -1, label="选择查询的下单员：")
        self._pnl.AddFoldPanelWindow(item, self.statictext7)
        self.member_combox = wx.ComboBox(item, -1, pos=(20, 10), style=wx.CB_DROPDOWN)
        self._pnl.AddFoldPanelWindow(item, self.member_combox)

        self.statictext8 = wx.StaticText(item, -1, label="选择查询的终端客户：")
        self._pnl.AddFoldPanelWindow(item, self.statictext8)
        self.Terminal_customer = wx.ComboBox(item, -1, pos=(20, 10), style=wx.CB_DROPDOWN)
        self._pnl.AddFoldPanelWindow(item, self.Terminal_customer)
        self.store_combox.SetValue('ALL')
        self.member_combox.SetValue('ALL')
        self.Terminal_customer.SetValue('ALL')
        btn_date_start.Bind(wx.EVT_BUTTON, self.Get_Seek_DateTime)
        self.btn_today.Bind(wx.EVT_BUTTON, self.Get_Today)
        self.btn_yesterday.Bind(wx.EVT_BUTTON, self.Get_Yesterday)
        self.btn_byesterday.Bind(wx.EVT_BUTTON, self.Get_Byesterday)
        self.btn_bbyesterday.Bind(wx.EVT_BUTTON, self.Get_Bbyesterday)
        btn_date_clear.Bind(wx.EVT_BUTTON, self.time_clear)
        self.store_combox.Bind(wx.EVT_COMBOBOX_DROPDOWN, self.store_information_display)  # 触发合同combobox下拉事件
        self.store_combox.Bind(wx.EVT_COMBOBOX, self.store_id_click)  # 触发合同combobox下拉框中内容被选中事件
        self.member_combox.Bind(wx.EVT_COMBOBOX_DROPDOWN, self.member_information_display)  # 触发订单号combobox下拉事件
        self.member_combox.Bind(wx.EVT_COMBOBOX, self.member_id_click)  # 触发订单号combobox下拉框中内容被选中事件
        self.Terminal_customer.Bind(wx.EVT_COMBOBOX_DROPDOWN, self.Terminal_information_display)  # 触发组件号combobox下拉事件
        self.Terminal_customer.Bind(wx.EVT_COMBOBOX, self.Terminal_id_click)  # 触发组件号combobox下拉事件
        self._leftWindow1.SizeWindows()

    #---------- TreeCtrl 相关的3个函数 -----------------------
    def Create_TreeCtrl(self):
            self._leftWindow2.DestroyChildren()
            date_start = time.strftime("%Y-%m-%d", time.localtime())
            self.TreeCtrl_Refresh(date_start,date_start)

            self.Bind(wx.EVT_CONTEXT_MENU, self.OnContextMenu)
            self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.right_click)
    def TreeCtrl_Refresh(self, start_time, end_time):
        try:
            #self.tree.DeleteAllItems()
            self._leftWindow2.DestroyChildren()
            self.tree = MyTreeCtrl(self._leftWindow2, wx.ID_ANY, wx.DefaultPosition, (400,1000),
                                   wx.TR_HAS_BUTTONS
                                   | wx.TR_EDIT_LABELS
                                   , self.log)
            isz = (16, 16)
            il = wx.ImageList(isz[0], isz[1])
            self.fldridx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, isz))
            self.fldropenidx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_OTHER, isz))
            self.fileidx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, isz))
            self.smidleix = il.Add(images.Smiles.GetBitmap())
            self.tree.SetImageList(il)
            self.il = il
            self.root = self.tree.AddRoot("全部订单")
            self.tree.SetItemData(self.root, None)
            self.tree.SetItemImage(self.root, self.fldridx, wx.TreeItemIcon_Normal)
            self.tree.SetItemImage(self.root, self.fldropenidx, wx.TreeItemIcon_Expanded)
            Order_id_list=[]

            if Is_Database_Connect():
                cursor = DB.cursor()
                #time1 = '2018-07-25'
                if start_time=='1900-01-01':
                    if self.store_combox.GetValue()!='ALL':
                        cursor.execute( "select `Order_id`,`Contract_id` from `order_order_complete` where `Dealer`='%s' "% self.store_combox.GetValue())
                        Order_id = cursor.fetchall()
                    elif self.Terminal_customer.GetValue()!='ALL':
                        cursor.execute(
                            "select `Order_id`,`Contract_id` from `order_order_complete` where `Customer_name`='%s' " % self.Terminal_customer.GetValue())
                        Order_id = cursor.fetchall()
                    else:
                        cursor.execute(
                            "select `Order_id`,`Contract_id` from `order_order_complete` where 1")
                        Order_id = cursor.fetchall()
                else:
                    if self.store_combox.GetValue()!='ALL':
                        cursor.execute( "select `Order_id`,`Contract_id` from `order_order_complete` where `First_day`>='%s' and `First_day`<='%s' and `Dealer`='%s' "% (start_time, end_time,self.store_combox.GetValue()))
                        Order_id = cursor.fetchall()
                    elif self.Terminal_customer.GetValue()!='ALL':
                        cursor.execute(
                            "select `Order_id`,`Contract_id` from `order_order_complete` where `First_day`>='%s' and `First_day`<='%s' and `Customer_name`='%s' " % (start_time, end_time,self.Terminal_customer.GetValue()))
                        Order_id = cursor.fetchall()
                    else:
                        cursor.execute("select `Order_id`,`Contract_id` from `order_order_complete` where `First_day`>='%s' and `First_day`<='%s' " % (start_time, end_time))
                        Order_id = cursor.fetchall()

                if Order_id!=():
                    if self.member_combox.GetValue()!='ALL':
                        cursor.execute(
                            "select `Contract_id` from `order_contract_internal` where `Customer_name`='%s'"% self.member_combox.GetValue())
                        contract_order_id = cursor.fetchall()
                        for i in range(len(Order_id)):
                            for k in range(len(contract_order_id)):
                                if Order_id[i][1]==contract_order_id[k][0]:
                                    Order_id_list.append(list(Order_id[i]))
                                    break
                    else:
                        for i in range(len(Order_id)):
                            Order_id_list.append(list(Order_id[i]))
                    for x in range(len(Order_id_list)):
                        child = self.tree.AppendItem(self.root, '订单：'+str(Order_id[x][0]))
                        self.tree.SetItemData(child, None)
                        self.tree.SetItemImage(child, self.fldridx, wx.TreeItemIcon_Normal)
                        self.tree.SetItemImage(child, self.fldropenidx, wx.TreeItemIcon_Expanded)

                        cursor.execute("select `Sec_id` from `order_section_complete` where `Order_id`='%s' " % Order_id[x][0])
                        Sec_id = cursor.fetchall()
                        for y in range(len(Sec_id)):
                            second = self.tree.AppendItem(child, '组件：'+str(Sec_id[y][0]))
                            self.tree.SetItemData(second, None)
                            self.tree.SetItemImage(second, self.fldridx, wx.TreeItemIcon_Normal)
                            self.tree.SetItemImage(second, self.fldropenidx, wx.TreeItemIcon_Expanded)

                            cursor.execute("select `Part_id` from `order_part_complete` where `Sec_id`='%s' " % Sec_id[y][0])
                            Part_id = cursor.fetchall()
                            for z in range(len(Part_id)):
                                last = self.tree.AppendItem(second, '部件：'+str(Part_id[z][0]))
                                self.tree.SetItemData(last, None)
                                self.tree.SetItemImage(last, self.fldridx, wx.TreeItemIcon_Normal)
                                self.tree.SetItemImage(last, self.fldropenidx, wx.TreeItemIcon_Expanded)

                                cursor.execute("select `Id` from `order_element_complete` where `Part_id`='%s' " % Part_id[z][0])
                                Id = cursor.fetchall()
                                # for h in range(len(Id)):
                                #     item = self.tree.AppendItem(last,  '零件：'+str(Id[h][0]))
                                #     self.tree.SetItemData(item, None)
                                #     self.tree.SetItemImage(item, self.fileidx, wx.TreeItemIcon_Normal)
                                #     self.tree.SetItemImage(item, self.smidleix, wx.TreeItemIcon_Selected)
                else:
                    pass
            self.tree.Expand(self.root)
            self.Bind(wx.EVT_TREE_SEL_CHANGED, self.Datebase_Inform, self.tree)
            #self.tree.AppendItem(self,"")
            wx.adv.LayoutAlgorithm().LayoutWindow(self._leftWindow2, self.tree)    #主要是为了每次刷新数据时，树界面都不变形，且有滚动条。
        except:
            self.log.WriteText("YLP_Contract_Order_Complete_Management_Panel类 TreeCtrl_Refresh函数报错，从数据库读取数据失败，本数据用于显示树结构 \r\n")
    def Datebase_Inform(self, event):
    # try:
        self.item = event.GetItem()
        if self.item:
            tree_id = self.tree.GetItemText(self.item)
            if tree_id == '全部订单':
                pass
            else:
                if 'O' in tree_id and 'S' not in tree_id and 'P' not in tree_id and 'ID' not in tree_id:
                    if Is_Database_Connect():
                        cursor = DB.cursor()
                        tree_id=tree_id.split("：")
                        cursor.execute( "select `Order_id`,`Customer_name`,`Customer_tel`,`Customer_address`,`Order_price`,`Order_area` from `order_order_complete` where `Order_id`='%s' " % tree_id[-1])
                        order_inform = cursor.fetchone()
                        cursor.execute( "select `Sec_id`,`Sec_series`,`Sec_color`,`Sec_thick`,`Sec_edge` from `order_section_complete` where `Order_id`='%s' " % tree_id[-1])
                        sec_inform = cursor.fetchall()
                        self.ylp_Show_Inform_Panel.PDF_Page(order_inform,sec_inform,3)
                if 'S' in tree_id and 'P' not in tree_id and 'ID' not in tree_id:
                    if Is_Database_Connect():
                        cursor = DB.cursor()
                        tree_id = tree_id.split("：")
                        cursor.execute("select `Part_id`,`Door_type`,`Element_type_id`,`Door_color`,`Door_height` ,`Door_width`,`Door_thick`,`Archaize`,`Door_area`,`Door_price`,`Hole`,`Open_way`,`Edge_type`,`State` from `order_part_complete` where `Sec_id`='%s' " % tree_id[-1])
                        part_inform = cursor.fetchall()
                        self.ylp_Show_Inform_Panel.Gride_Page(part_inform)
                if 'P' in tree_id and 'ID' not in tree_id:
                    # pass
                    if Is_Database_Connect():
                        cursor = DB.cursor()
                        tree_id = tree_id.split("：")
                        cursor.execute("select `Door_type`,`Door_color`,`Door_height`,`Door_width`,`Door_thick` from `order_part_complete` where `Part_id`='%s'" % tree_id[-1])
                        part_inform = cursor.fetchone()
                        cursor.execute(
                            "select `Id`,`Board_type`,`Element_type_id`,`Color`,`Board_height`,`Board_width`,`Board_thick`,`Archaize`,`Hole`,`Open_way`,`Edge_type`,`State` from `order_element_complete` where `Part_id`='%s' " %
                            tree_id[-1])
                        part_information_transfer = cursor.fetchall()
                        part_information_list=list(part_information_transfer)
                        part_information_list.sort(key=lambda x: [x[2]])
                        part_information=tuple(part_information_list)
                        self.ylp_Show_Inform_Panel.Show_Part_Inform(part_inform,part_information)
                # if 'ID' in tree_id:
                #     if Is_Database_Connect():
                #         cursor = DB.cursor()
                #         tree_id = tree_id.split("：")
                #         cursor.execute( "select `Board_type`,`Color`,`Board_height`,`Board_width`,`Board_thick` from `order_element_online` where `Id`='%s' " % tree_id[-1])
                #         id_inform = cursor.fetchone()
                #         self.ylp_Show_Inform_Panel.Show_ID_Inform(id_inform)
        event.Skip()
    # except:
    #     self.log.WriteText("YLP_Contract_Order_Complete_Management_Panel类 Datebase_Inform函数报错，从数据库读取数据失败，本数据用于提供右侧主面板的信息显示 \r\n")

    def right_click(self,event):
        self.item = event.GetItem()
        if self.item:
            self.select_code = self.tree.GetItemText(self.item)

     #鼠标右击弹出的菜单
    def OnContextMenu(self, event):
        pass
        # if not hasattr(self, "popupID1"):
        #
        #     self.Bind(wx.EVT_MENU, self.Expend, id=YLP_complete_popupID1)
        #
        # menu = wx.Menu()
        # item = wx.MenuItem(menu, YLP_complete_popupID1, "展开")
        # bmp = images.Smiles.GetBitmap()
        # item.SetBitmap(bmp)
        # menu.Append(item)
        # self.PopupMenu(menu)
        # menu.Destroy()
    def Expend(self,event):
        self.tree.ExpandAllChildren(self.item)
    #----------------------------------------
    def onDateStart(self,event):
        self.date_start=self.calendar_begin.GetValue()
        self.date_end=self.calendar_end.GetValue()
        self.log.WriteText("天外天系统收到操作员控制指令，开始执行日期查询操作，起始日期："+str(self.date_start)+"，终止日期："+str(self.date_end)+"\r\n")
    def OnCreateBottomStyle(self, event):

        # recreate with style collapse to bottom, which means
        # all panels that are collapsed are placed at the bottom,
        # or normal

        if event.IsChecked():
            self.GetMenuBar().Check(self._singlestyle, False)
            self.GetMenuBar().Check(self._exclusivestyle, False)
            self._flags = self._flags & ~fpb.FPB_SINGLE_FOLD
            self._flags = self._flags & ~fpb.FPB_EXCLUSIVE_FOLD
            self._flags = self._flags | fpb.FPB_COLLAPSE_TO_BOTTOM
        else:
            self._flags = self._flags & ~fpb.FPB_COLLAPSE_TO_BOTTOM

        self.ReCreateFoldPanel(self._flags)
        #self.Create_TreeCtrl()
    def OnCreateNormalStyle(self, event):

        # recreate with style where only one panel at the time is
        # allowed to be opened

        if event.IsChecked():
            self.GetMenuBar().Check(self._bottomstyle, False)
            self.GetMenuBar().Check(self._exclusivestyle, False)
            self._flags = self._flags & ~fpb.FPB_EXCLUSIVE_FOLD
            self._flags = self._flags & ~fpb.FPB_COLLAPSE_TO_BOTTOM
            self._flags = self._flags | fpb.FPB_SINGLE_FOLD
        else:
            self._flags = self._flags & ~fpb.FPB_SINGLE_FOLD

        self.ReCreateFoldPanel(self._flags)
        #self.Create_TreeCtrl()
    def OnCreateExclusiveStyle(self, event):

        # recreate with style where only one panel at the time is
        # allowed to be opened and the others are collapsed to bottom

        if event.IsChecked():
            self.GetMenuBar().Check(self._singlestyle, False)
            self.GetMenuBar().Check(self._bottomstyle, False)
            self._flags = self._flags & ~fpb.FPB_SINGLE_FOLD
            self._flags = self._flags & ~fpb.FPB_COLLAPSE_TO_BOTTOM
            self._flags = self._flags | fpb.FPB_EXCLUSIVE_FOLD
        else:
            self._flags = self._flags & ~fpb.FPB_EXCLUSIVE_FOLD

        self.ReCreateFoldPanel(self._flags)
        #self.Create_TreeCtrl()
    def OnCollapseMe(self, event):

        for i in range(0, self._pnl.GetCount()):
            item = self._pnl.GetFoldPanel(i)
            self._pnl.Collapse(item)
    def OnExpandMe(self, event):
        style = fpb.CaptionBarStyle()
        counter = 0
        for items in self.radiocontrols:
            if items.GetValue():
                break
            counter = counter + 1

        if counter == 0:
            mystyle = fpb.CAPTIONBAR_GRADIENT_V
        elif counter == 1:
            mystyle = fpb.CAPTIONBAR_GRADIENT_H
        elif counter == 2:
            mystyle = fpb.CAPTIONBAR_SINGLE
        elif counter == 3:
            mystyle = fpb.CAPTIONBAR_RECTANGLE
        else:
            mystyle = fpb.CAPTIONBAR_FILLED_RECTANGLE

        # style.SetCaptionStyle(mystyle)
        # self._pnl.ApplyCaptionStyleAll(style)
    def OnSlideColour(self, event):

        col1 = wx.Colour(self._rslider1.GetValue(), self._gslider1.GetValue(),
                         self._bslider1.GetValue())
        col2 = wx.Colour(self._rslider2.GetValue(), self._gslider2.GetValue(),
                         self._bslider2.GetValue())

        style = fpb.CaptionBarStyle()

        counter = 0
        for items in self.radiocontrols:
            if items.GetValue():
                break

            counter = counter + 1

        if counter == 0:
            mystyle = fpb.CAPTIONBAR_GRADIENT_V
        elif counter == 1:
            mystyle = fpb.CAPTIONBAR_GRADIENT_H
        elif counter == 2:
            mystyle = fpb.CAPTIONBAR_SINGLE
        elif counter == 3:
            mystyle = fpb.CAPTIONBAR_RECTANGLE
        else:
            mystyle = fpb.CAPTIONBAR_FILLED_RECTANGLE

        style.SetFirstColour(col1)
        style.SetSecondColour(col2)
        style.SetCaptionStyle(mystyle)

        item = self._pnl.GetFoldPanel(0)
        self._pnl.ApplyCaptionStyle(item, style)
    def OnStyleChange(self, event):

        style = fpb.CaptionBarStyle()

        eventid = event.GetId()

        if eventid == self.ID_USE_HGRADIENT:
            style.SetCaptionStyle(fpb.CAPTIONBAR_GRADIENT_H)

        elif eventid == self.ID_USE_VGRADIENT:
            style.SetCaptionStyle(fpb.CAPTIONBAR_GRADIENT_V)

        elif eventid == self.ID_USE_SINGLE:
            style.SetCaptionStyle(fpb.CAPTIONBAR_SINGLE)

        elif eventid == self.ID_USE_RECTANGLE:
            style.SetCaptionStyle(fpb.CAPTIONBAR_RECTANGLE)

        elif eventid == self.ID_USE_FILLED_RECTANGLE:
            style.SetCaptionStyle(fpb.CAPTIONBAR_FILLED_RECTANGLE)

        else:
            raise "ERROR: Undefined Style Selected For CaptionBar: " + repr(eventid)

        col1 = wx.Colour(self._rslider1.GetValue(), self._gslider1.GetValue(),
                         self._bslider1.GetValue())
        col2 = wx.Colour(self._rslider2.GetValue(), self._gslider2.GetValue(),
                         self._bslider2.GetValue())

        style.SetFirstColour(col1)
        style.SetSecondColour(col2)

        if self._single.GetValue():
            item = self._pnl.GetFoldPanel(1)
            self._pnl.ApplyCaptionStyle(item, style)
        else:
            self._pnl.ApplyCaptionStyleAll(style)
    def CreateMenuBar(self, with_window=False):

        # Make a menubar
        file_menu = wx.Menu()

        FPBTEST_QUIT = wx.NewId()
        FPBTEST_REFRESH = wx.NewId()
        FPB_BOTTOM_FOLD = wx.NewId()
        FPB_SINGLE_FOLD = wx.NewId()
        FPB_EXCLUSIVE_FOLD = wx.NewId()
        FPBTEST_TOGGLE_WINDOW = wx.NewId()
        FPBTEST_ABOUT = wx.NewId()

        file_menu.Append(FPBTEST_QUIT, "&Exit")

        option_menu = None

        if with_window:
            # Dummy option
            option_menu = wx.Menu()
            option_menu.Append(FPBTEST_REFRESH, "&Refresh picture")

        # make fold panel menu

        fpb_menu = wx.Menu()
        fpb_menu.AppendCheckItem(FPB_BOTTOM_FOLD, "Create with &fpb.FPB_COLLAPSE_TO_BOTTOM")

        # Now Implemented!
        fpb_menu.AppendCheckItem(FPB_SINGLE_FOLD, "Create with &fpb.FPB_SINGLE_FOLD")

        # Now Implemented!
        fpb_menu.AppendCheckItem(FPB_EXCLUSIVE_FOLD, "Create with &fpb.FPB_EXCLUSIVE_FOLD")

        fpb_menu.AppendSeparator()
        fpb_menu.Append(FPBTEST_TOGGLE_WINDOW, "&Toggle FoldPanelBar")

        help_menu = wx.Menu()
        help_menu.Append(FPBTEST_ABOUT, "&About")

        menu_bar = wx.MenuBar()

        menu_bar.Append(file_menu, "&File")
        menu_bar.Append(fpb_menu, "&FoldPanel")

        if option_menu:
            menu_bar.Append(option_menu, "&Options")

        menu_bar.Append(help_menu, "&Help")

        self.Bind(wx.EVT_MENU, self.OnAbout, id=FPBTEST_ABOUT)
        self.Bind(wx.EVT_MENU, self.OnQuit, id=FPBTEST_QUIT)
        self.Bind(wx.EVT_MENU, self.OnToggleWindow, id=FPBTEST_TOGGLE_WINDOW)
        self.Bind(wx.EVT_MENU, self.OnCreateBottomStyle, id=FPB_BOTTOM_FOLD)
        self.Bind(wx.EVT_MENU, self.OnCreateNormalStyle, id=FPB_SINGLE_FOLD)
        self.Bind(wx.EVT_MENU, self.OnCreateExclusiveStyle, id=FPB_EXCLUSIVE_FOLD)

        self._bottomstyle = FPB_BOTTOM_FOLD
        self._singlestyle = FPB_SINGLE_FOLD
        self._exclusivestyle = FPB_EXCLUSIVE_FOLD

        return menu_bar
class Waiting_Contract_Management_Panel(wx.Panel):
    def __init__(self, parent,log,FYF_Progress_Manage_Panel, id=wx.ID_ANY, title="", pos=wx.DefaultPosition,
                 size=(700,650), style=wx.DEFAULT_FRAME_STYLE):
        wx.Panel.__init__(self, parent)
        self.FYF_Progress_Manage_Panel=FYF_Progress_Manage_Panel
        self.parent=parent
        self.select_code=0
        self._flags = 0
        self.log=log
        self._leftWindow1 = wx.adv.SashLayoutWindow(self, 101, wx.DefaultPosition,
                                                wx.Size(200, 1000), wx.NO_BORDER |
                                                wx.adv.SW_3D | wx.CLIP_CHILDREN)
        self._leftWindow1.SetDefaultSize(wx.Size(220, 1000))
        self._leftWindow1.SetOrientation(wx.adv.LAYOUT_VERTICAL)
        self._leftWindow1.SetAlignment(wx.adv.LAYOUT_LEFT)
        self._leftWindow1.SetSashVisible(wx.adv.SASH_RIGHT, True)
        self._leftWindow1.SetExtraBorderSize(10)
        self._pnl = 0

        #self.ylp_Section_Inform_Grid=Section_Inform_Grid(self)
        self.ylp_Show_Inform_Panel=Show_Inform_Panel(self,self.log)

        self.ID_WINDOW_TOP = 100
        self.ID_WINDOW_LEFT1 = 101
        self.ID_WINDOW_RIGHT1 = 102
        self.ID_WINDOW_BOTTOM = 103
        self._leftWindow1.Bind(wx.adv.EVT_SASH_DRAGGED_RANGE, self.OnFoldPanelBarDrag,
                               id=100, id2=103)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        self.Bind(wx.EVT_SCROLL, self.OnSlideColour)
        self.ReCreateFoldPanel(0)

        self._leftWindow2 = wx.adv.SashLayoutWindow(self, 101, wx.DefaultPosition,
                                                    wx.Size(300, 1000), wx.NO_BORDER |
                                                    wx.adv.SW_3D | wx.CLIP_CHILDREN)
        self._leftWindow2.SetDefaultSize(wx.Size(320, 1000))
        self._leftWindow2.SetOrientation(wx.adv.LAYOUT_VERTICAL)
        self._leftWindow2.SetAlignment(wx.adv.LAYOUT_LEFT)
        self._leftWindow2.SetSashVisible(wx.adv.SASH_RIGHT, True)
        self._leftWindow2.SetExtraBorderSize(10)
        self._pnl = 0
        self.Create_TreeCtrl()
        self.abortEvent = delayedresult.AbortEvent()
        self.jobID = 0

    def Get_Seek_DateTime(self,event):
        date_start = self.calendar_begin.GetValue()
        date_end = self.calendar_end.GetValue()
        if "从" in date_start or "至"in date_end :
            self.TreeCtrl_Refresh(0,0)
        else:
            if '/' in date_start:
                date_start=date_start.split("/")
                date_end = date_end.split("/")

                date_start=date_start[2],date_start[1],date_start[0]
                date_end=date_end[2],date_end[1],date_end[0]
                st='-'
                date_start = st.join(date_start)
                date_end = st.join(date_end)

            self.TreeCtrl_Refresh(date_start,date_end)

       # wx.adv.LayoutAlgorithm().LayoutWindow(self._leftWindow2,self.tree)

    def Get_Today(self,event):
        date_start=time.strftime("%Y-%m-%d", time.localtime())
        date_end=date_start
        self.TreeCtrl_Refresh(date_start, date_end)
        self.calendar_begin.textCtrl.SetValue(date_start)
        self.calendar_end.textCtrl.SetValue(date_end)
        if (self.jobID < 2):
            self.jobID += 1
            jobID=1
            delayedresult.startWorker(self.End_Thread, self.Start_Thread,
                                      wargs=(jobID, self.abortEvent), jobID=1)
    def Start_Thread(self, jobID, abortEvent):
        massage=["Please wait 5 seconds, working...","系统工作中，请等待15秒钟"]
        busy = PBI.PyBusyInfo(massage[jobID-1], parent=None, title="Really Busy",
                              icon=images.Smiles.GetBitmap())

        wx.Yield()
        if(jobID==1):
            for indx in range(5):
                wx.MilliSleep(1000)
        if(jobID==2):
            for indx in range(15):
                wx.MilliSleep(1000)
        del busy
        return jobID

    def End_Thread(self, delayedResult):
        #wx.adv.LayoutAlgorithm().LayoutWindow(self._leftWindow2,self.tree)
        jobID = delayedResult.getJobID()
        if(jobID>0):
            self.jobID-=1

    def Get_Yesterday(self,event):
        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        yesterday = today - oneday
        self.TreeCtrl_Refresh(str(yesterday), str(yesterday))
        self.calendar_begin.textCtrl.SetValue(str(yesterday))
        self.calendar_end.textCtrl.SetValue(str(yesterday))
        #wx.adv.LayoutAlgorithm().LayoutWindow(self._leftWindow2, self.tree)
        if (self.jobID < 2):
            self.jobID += 1
            jobID=2
            delayedresult.startWorker(self.End_Thread, self.Start_Thread,
                                      wargs=(jobID, self.abortEvent), jobID=2)
    def OnSize(self, event):
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.ylp_Show_Inform_Panel)
        event.Skip()

    def OnQuit(self, event):
        self.Destroy()
    def OnToggleWindow(self, event):

        self._leftWindow1.Show(not self._leftWindow1.IsShown())
        # Leaves bits of itself behind sometimes
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.ylp_Show_Inform_Panel)
        self.ylp_Show_Inform_Panel.Refresh()

        event.Skip()
    def OnFoldPanelBarDrag(self, event):

        # if event.GetDragStatus() == wx.SASH_STATUS_OUT_OF_RANGE:
        #     return

        if event.GetId() == self.ID_WINDOW_LEFT1:
            self._leftWindow1.SetDefaultSize(wx.Size(event.GetDragRect().width, 1000))


        # Leaves bits of itself behind sometimes
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.ylp_Show_Inform_Panel)
        self.ylp_Show_Inform_Panel.Refresh()

        event.Skip()
    def ReCreateFoldPanel(self, fpb_flags):

        # delete earlier panel
        self._leftWindow1.DestroyChildren()

        # recreate the foldpanelbar
        self._pnl = fpb.FoldPanelBar(self._leftWindow1, -1, wx.DefaultPosition,
                                     wx.Size(-1,-1), agwStyle=fpb_flags)

        Images = wx.ImageList(16,16)
        Images.Add(GetExpandedIconBitmap())
        Images.Add(GetCollapsedIconBitmap())
        item = self._pnl.AddFoldPanel("按日期查询", collapsed=False,
                                      foldIcons=Images)
        self.date_start=wx.DateTimeFromDMY
        self.date_end=wx.DateTimeFromDMY
        self.calendar_begin=PopDateControl(item, -1)
        self.calendar_begin.textCtrl.SetValue("从")
        self._pnl.AddFoldPanelWindow(item,self.calendar_begin,fpb.FPB_ALIGN_WIDTH,2,20)
        self.calendar_end=PopDateControl(item, -1)
        self.calendar_end.textCtrl.SetValue("至")
        self._pnl.AddFoldPanelWindow(item,self.calendar_end,fpb.FPB_ALIGN_WIDTH,2,20)
        btn_date_start=wx.Button(item, wx.ID_ANY, "开始日期查询")
        btn_date_start.Bind(wx.EVT_BUTTON, self.Get_Seek_DateTime)
        self._pnl.AddFoldPanelWindow(item, btn_date_start)
        btn_date_start.Bind(wx.EVT_BUTTON,self.Get_Seek_DateTime)
        self._pnl.AddFoldPanelSeparator(item)
        self.btn_today = wx.Button(item, wx.ID_ANY, "今天")
        self.btn_today.Bind(wx.EVT_BUTTON, self.Get_Today)
        self._pnl.AddFoldPanelWindow(item, self.btn_today)

        self.btn_yesterday = wx.Button(item, wx.ID_ANY, "昨天")
        self.btn_yesterday.Bind(wx.EVT_BUTTON, self.Get_Yesterday)
        self._pnl.AddFoldPanelWindow(item, self.btn_yesterday,spacing=0)

        # btn_Byesterday = wx.Button(item, wx.ID_ANY, "前天")
        # btn_Byesterday.Bind(wx.EVT_BUTTON, self.OnExpandMe)
        # self._pnl.AddFoldPanelWindow(item, btn_Byesterday,spacing=0)
        # btn_BByesterday = wx.Button(item, wx.ID_ANY, "大前天")
        # btn_BByesterday.Bind(wx.EVT_BUTTON, self.OnExpandMe)
        # self._pnl.AddFoldPanelWindow(item, btn_BByesterday,spacing=0)
        # self._pnl.AddFoldPanelSeparator(item)
        # btn_date_clear=wx.Button(item, wx.ID_ANY, "清除日期索引")
        # btn_date_clear.Bind(wx.EVT_BUTTON, self.OnExpandMe)
        # self._pnl.AddFoldPanelWindow(item, btn_date_clear)
        # item = self._pnl.AddFoldPanel("按经销商查询", False, foldIcons=Images)
        # self.ID_USE_VGRADIENT = wx.NewId()
        # self.ID_USE_HGRADIENT = wx.NewId()
        # self.ID_USE_SINGLE = wx.NewId()
        # self.ID_USE_RECTANGLE = wx.NewId()
        # self.ID_USE_FILLED_RECTANGLE = wx.NewId()
        #
        # currStyle =  wx.RadioButton(item, self.ID_USE_VGRADIENT, "&Vertical Gradient")
        # self._pnl.AddFoldPanelWindow(item, currStyle, fpb.FPB_ALIGN_WIDTH,
        #                              fpb.FPB_DEFAULT_SPACING, 10)
        #
        # currStyle.SetValue(True)
        #
        # radio1 = wx.RadioButton(item, self.ID_USE_HGRADIENT, "&Horizontal Gradient")
        # radio2 = wx.RadioButton(item, self.ID_USE_SINGLE, "&Single Colour")
        # radio3 = wx.RadioButton(item, self.ID_USE_RECTANGLE, "&Rectangle Box")
        # radio4 = wx.RadioButton(item, self.ID_USE_FILLED_RECTANGLE, "&Filled Rectangle Box")
        #
        # currStyle.Bind(wx.EVT_RADIOBUTTON, self.OnStyleChange)
        # radio1.Bind(wx.EVT_RADIOBUTTON, self.OnStyleChange)
        # radio2.Bind(wx.EVT_RADIOBUTTON, self.OnStyleChange)
        # radio3.Bind(wx.EVT_RADIOBUTTON, self.OnStyleChange)
        # radio4.Bind(wx.EVT_RADIOBUTTON, self.OnStyleChange)
        #
        # self._pnl.AddFoldPanelWindow(item, radio1, fpb.FPB_ALIGN_WIDTH, fpb.FPB_DEFAULT_SPACING, 10)
        # self._pnl.AddFoldPanelWindow(item, radio2, fpb.FPB_ALIGN_WIDTH, fpb.FPB_DEFAULT_SPACING, 10)
        # self._pnl.AddFoldPanelWindow(item, radio3, fpb.FPB_ALIGN_WIDTH, fpb.FPB_DEFAULT_SPACING, 10)
        # self._pnl.AddFoldPanelWindow(item, radio4, fpb.FPB_ALIGN_WIDTH, fpb.FPB_DEFAULT_SPACING, 10)
        #
        # self._pnl.AddFoldPanelSeparator(item)
        #
        # self._single = wx.CheckBox(item, -1, "&Only This Caption")
        # self._pnl.AddFoldPanelWindow(item, self._single, fpb.FPB_ALIGN_WIDTH,
        #                              fpb.FPB_DEFAULT_SPACING, 10)
        #
        # # one more panel to finish it
        #
        # cs = fpb.CaptionBarStyle()
        # cs.SetCaptionStyle(fpb.CAPTIONBAR_RECTANGLE)
        #
        # item = self._pnl.AddFoldPanel("按用户查询", collapsed=True, foldIcons=Images,
        #                               cbstyle=cs)
        #
        # button2 = wx.Button(item, wx.NewId(), "Collapse All")
        # self._pnl.AddFoldPanelWindow(item, button2)
        # self._pnl.AddFoldPanelWindow(item, wx.StaticText(item, -1, "Enter Some Comments"),
        #                              fpb.FPB_ALIGN_WIDTH, 5, 20)
        # self._pnl.AddFoldPanelWindow(item, wx.TextCtrl(item, -1, "Comments"),
        #                              fpb.FPB_ALIGN_WIDTH, fpb.FPB_DEFAULT_SPACING, 10)
        #
        # button2.Bind(wx.EVT_BUTTON, self.OnCollapseMe)
        # self.radiocontrols = [currStyle, radio1, radio2, radio3, radio4]

        self._leftWindow1.SizeWindows()

    #---------- TreeCtrl 相关的3个函数 -----------------------
    def Create_TreeCtrl(self):
            self.tID = wx.NewId()
            self._leftWindow2.DestroyChildren()
            date_start = time.strftime("%Y-%m-%d", time.localtime())
            self.TreeCtrl_Refresh(date_start,date_start)

            self.Bind(wx.EVT_CONTEXT_MENU, self.OnContextMenu)
            self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.right_click)
    def TreeCtrl_Refresh(self, start_time, end_time):
        try:
            #self.tree.DeleteAllItems()
            self.tID = wx.NewId()
            self._leftWindow2.DestroyChildren()
            self.tree = MyTreeCtrl(self._leftWindow2, self.tID, wx.DefaultPosition, (400,1000),
                                   wx.TR_HAS_BUTTONS
                                   | wx.TR_EDIT_LABELS
                                   , self.log)
            isz = (16, 16)
            il = wx.ImageList(isz[0], isz[1])
            self.fldridx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, isz))
            self.fldropenidx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_OTHER, isz))
            self.fileidx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, isz))
            self.smidleix = il.Add(images.Smiles.GetBitmap())
            self.tree.SetImageList(il)
            self.il = il
            self.root = self.tree.AddRoot("全部订单")
            self.tree.SetItemData(self.root, None)
            self.tree.SetItemImage(self.root, self.fldridx, wx.TreeItemIcon_Normal)
            self.tree.SetItemImage(self.root, self.fldropenidx, wx.TreeItemIcon_Expanded)

            if Is_Database_Connect():
                cursor = DB.cursor()
                #time1 = '2018-07-25'
                if start_time==0 or  end_time==0:
                    cursor.execute( "select `Order_id` from `order_order_online` where 1 ")
                    Order_id = cursor.fetchall()
                else:
                    cursor.execute("select `Order_id` from `order_order_online` where `First_day`>='%s' and `First_day`<='%s' " % (start_time, end_time))
                    Order_id = cursor.fetchall()

                if Order_id!=():
                    for x in range(len(Order_id)):
                        child = self.tree.AppendItem(self.root, '订单：'+str(Order_id[x][0]))
                        self.tree.SetItemData(child, None)
                        self.tree.SetItemImage(child, self.fldridx, wx.TreeItemIcon_Normal)
                        self.tree.SetItemImage(child, self.fldropenidx, wx.TreeItemIcon_Expanded)
                        cursor.execute("select `Sec_id` from `order_section_online` where `Order_id`='%s' " % Order_id[x][0])
                        Sec_id = cursor.fetchall()
                        for y in range(len(Sec_id)):
                            second = self.tree.AppendItem(child, '组件：'+str(Sec_id[y][0]))
                            self.tree.SetItemData(second, None)
                            self.tree.SetItemImage(second, self.fldridx, wx.TreeItemIcon_Normal)
                            self.tree.SetItemImage(second, self.fldropenidx, wx.TreeItemIcon_Expanded)

                            cursor.execute("select `Part_id` from `order_part_online` where `Sec_id`='%s' " % Sec_id[y][0])
                            Part_id = cursor.fetchall()
                            for z in range(len(Part_id)):
                                last = self.tree.AppendItem(second, '部件：'+str(Part_id[z][0]))
                                self.tree.SetItemData(last, None)
                                self.tree.SetItemImage(last, self.fldridx, wx.TreeItemIcon_Normal)
                                self.tree.SetItemImage(last, self.fldropenidx, wx.TreeItemIcon_Expanded)

                                cursor.execute("select `Id` from `order_element_online` where `Part_id`='%s' " % Part_id[z][0])
                                Id = cursor.fetchall()
                                for h in range(len(Id)):
                                    item = self.tree.AppendItem(last,  '零件：'+str(Id[h][0]))
                                    self.tree.SetItemData(item, None)
                                    self.tree.SetItemImage(item, self.fileidx, wx.TreeItemIcon_Normal)
                                    self.tree.SetItemImage(item, self.smidleix, wx.TreeItemIcon_Selected)
                else:
                    pass
            self.tree.Expand(self.root)
            self.Bind(wx.EVT_TREE_SEL_CHANGED, self.Datebase_Inform, self.tree)
            #self.tree.AppendItem(self,"")
            wx.adv.LayoutAlgorithm().LayoutWindow(self._leftWindow2, self.tree)    #主要是为了每次刷新数据时，树界面都不变形，且有滚动条。
        except:
            self.log.WriteText("YLP_Contract_Order_Management_Panel类 TreeCtrl_Refresh函数报错，从数据库读取数据失败，本数据用于显示树结构 \r\n")
    def Datebase_Inform(self, event):
        try:
            self.item = event.GetItem()
            if self.item:
                tree_id = self.tree.GetItemText(self.item)
                if tree_id == '全部订单':
                    pass
                else:
                    if 'O' in tree_id and 'S' not in tree_id and 'P' not in tree_id and 'ID' not in tree_id:
                        if Is_Database_Connect():
                            cursor = DB.cursor()
                            tree_id=tree_id.split("：")
                            cursor.execute( "select `Order_id`,`Customer_name`,`Customer_tel`,`Customer_address`,`Order_price`,`Order_area` from `order_order_online` where `Order_id`='%s' " % tree_id[-1])
                            order_inform = cursor.fetchone()

                            cursor.execute( "select `Sec_id`,`Sec_series`,`Sec_color`,`Sec_thick`,`Sec_edge` from `order_section_online` where `Order_id`='%s' " % tree_id[-1])
                            sec_inform = cursor.fetchall()

                            self.ylp_Show_Inform_Panel.PDF_Page(order_inform,sec_inform,1)
                    if 'S' in tree_id and 'P' not in tree_id and 'ID' not in tree_id:
                        if Is_Database_Connect():
                            cursor = DB.cursor()
                            tree_id = tree_id.split("：")
                            cursor.execute("select `Part_id`,`Door_type`,`Element_type_id`,`Door_color`,`Door_height` ,`Door_width`,`Door_thick`,`Archaize`,`Door_area`,`Door_price`,`Hole`,`Open_way`,`Edge_type`,`State` from `order_part_online` where `Sec_id`='%s' " % tree_id[-1])
                            part_inform = cursor.fetchall()
                            self.ylp_Show_Inform_Panel.Gride_Page(part_inform)
                    if 'P' in tree_id and 'ID' not in tree_id:
                        # pass
                        if Is_Database_Connect():
                            cursor = DB.cursor()
                            tree_id = tree_id.split("：")
                            cursor.execute("select `Door_type`,`Door_color`,`Door_height`,`Door_width`,`Door_thick` from `order_part_online` where `Part_id`='%s' " % tree_id[-1])
                            part_inform = cursor.fetchone()
                            self.ylp_Show_Inform_Panel.Show_Part_Inform(part_inform)
                    if 'ID' in tree_id:
                        if Is_Database_Connect():
                            cursor = DB.cursor()
                            tree_id = tree_id.split("：")
                            cursor.execute( "select `Board_type`,`Color`,`Board_height`,`Board_width`,`Board_thick` from `order_element_online` where `Id`='%s' " % tree_id[-1])
                            id_inform = cursor.fetchone()
                            self.ylp_Show_Inform_Panel.Show_ID_Inform(id_inform)
            event.Skip()
        except:
            self.log.WriteText("YLP_Contract_Order_Management_Panel类 Datebase_Inform函数报错，从数据库读取数据失败，本数据用于提供右侧主面板的信息显示 \r\n")

    def right_click(self,event):
        self.item = event.GetItem()
        if self.item:
            self.select_code = self.tree.GetItemText(self.item)

     #鼠标右击弹出的菜单
    def OnContextMenu(self, event):
            if not hasattr(self, "popupID1"):
                YLP_waiting_popupID1 = wx.NewId()
                YLP_waiting_popupID2 = wx.NewId()
                #self.popupID3 = wx.NewId()
                self.Bind(wx.EVT_MENU, self.OnPopupOne, id=YLP_waiting_popupID1)
                self.Bind(wx.EVT_MENU, self.Expend, id=YLP_waiting_popupID2)
                #self.Bind(wx.EVT_MENU, self.Expend, id=self.popupID3)

            menu = wx.Menu()
            item = wx.MenuItem(menu, YLP_waiting_popupID1, "查询工期进度")
            bmp = images.Smiles.GetBitmap()
            item.SetBitmap(bmp)
            menu.Append(item)
            menu.Append(self.YLP_waiting_popupID2, "展开")
            #menu.Append(self.popupID3, "合起")
            self.PopupMenu(menu)
            menu.Destroy()
    def OnPopupOne(self, event):
        self.parent.SetSelection(0)
        select_code1 = self.select_code.split("：")
        if select_code1[0]=='部件' or select_code1=='零件':
            select_code2=select_code1[-1].split("P")
        else:
            select_code2=select_code1[-1]
        #self.FYF_Progress_Manage_Panel.ReCreateFoldPanel().self.contract_combox.SetValue(self, 'abc')
        self.FYF_Progress_Manage_Panel.YLP_Combox_Setvalue(select_code2)
    def Expend(self,event):
        self.tree.ExpandAllChildren(self.item)
        # self.tree.Expand(self.item)
    #----------------------------------------
    def onDateStart(self,event):
        self.date_start=self.calendar_begin.GetValue()
        self.date_end=self.calendar_end.GetValue()
        self.log.WriteText("天外天系统收到操作员控制指令，开始执行日期查询操作，起始日期："+str(self.date_start)+"，终止日期："+str(self.date_end)+"\r\n")
    def OnCreateBottomStyle(self, event):

        # recreate with style collapse to bottom, which means
        # all panels that are collapsed are placed at the bottom,
        # or normal

        if event.IsChecked():
            self.GetMenuBar().Check(self._singlestyle, False)
            self.GetMenuBar().Check(self._exclusivestyle, False)
            self._flags = self._flags & ~fpb.FPB_SINGLE_FOLD
            self._flags = self._flags & ~fpb.FPB_EXCLUSIVE_FOLD
            self._flags = self._flags | fpb.FPB_COLLAPSE_TO_BOTTOM
        else:
            self._flags = self._flags & ~fpb.FPB_COLLAPSE_TO_BOTTOM

        self.ReCreateFoldPanel(self._flags)
        #self.Create_TreeCtrl()
    def OnCreateNormalStyle(self, event):

        # recreate with style where only one panel at the time is
        # allowed to be opened

        if event.IsChecked():
            self.GetMenuBar().Check(self._bottomstyle, False)
            self.GetMenuBar().Check(self._exclusivestyle, False)
            self._flags = self._flags & ~fpb.FPB_EXCLUSIVE_FOLD
            self._flags = self._flags & ~fpb.FPB_COLLAPSE_TO_BOTTOM
            self._flags = self._flags | fpb.FPB_SINGLE_FOLD
        else:
            self._flags = self._flags & ~fpb.FPB_SINGLE_FOLD

        self.ReCreateFoldPanel(self._flags)
        #self.Create_TreeCtrl()
    def OnCreateExclusiveStyle(self, event):

        # recreate with style where only one panel at the time is
        # allowed to be opened and the others are collapsed to bottom

        if event.IsChecked():
            self.GetMenuBar().Check(self._singlestyle, False)
            self.GetMenuBar().Check(self._bottomstyle, False)
            self._flags = self._flags & ~fpb.FPB_SINGLE_FOLD
            self._flags = self._flags & ~fpb.FPB_COLLAPSE_TO_BOTTOM
            self._flags = self._flags | fpb.FPB_EXCLUSIVE_FOLD
        else:
            self._flags = self._flags & ~fpb.FPB_EXCLUSIVE_FOLD

        self.ReCreateFoldPanel(self._flags)
        #self.Create_TreeCtrl()
    def OnCollapseMe(self, event):

        for i in range(0, self._pnl.GetCount()):
            item = self._pnl.GetFoldPanel(i)
            self._pnl.Collapse(item)
    def OnExpandMe(self, event):
        style = fpb.CaptionBarStyle()
        counter = 0
        for items in self.radiocontrols:
            if items.GetValue():
                break
            counter = counter + 1

        if counter == 0:
            mystyle = fpb.CAPTIONBAR_GRADIENT_V
        elif counter == 1:
            mystyle = fpb.CAPTIONBAR_GRADIENT_H
        elif counter == 2:
            mystyle = fpb.CAPTIONBAR_SINGLE
        elif counter == 3:
            mystyle = fpb.CAPTIONBAR_RECTANGLE
        else:
            mystyle = fpb.CAPTIONBAR_FILLED_RECTANGLE

        # style.SetCaptionStyle(mystyle)
        # self._pnl.ApplyCaptionStyleAll(style)
    def OnSlideColour(self, event):

        col1 = wx.Colour(self._rslider1.GetValue(), self._gslider1.GetValue(),
                         self._bslider1.GetValue())
        col2 = wx.Colour(self._rslider2.GetValue(), self._gslider2.GetValue(),
                         self._bslider2.GetValue())

        style = fpb.CaptionBarStyle()

        counter = 0
        for items in self.radiocontrols:
            if items.GetValue():
                break

            counter = counter + 1

        if counter == 0:
            mystyle = fpb.CAPTIONBAR_GRADIENT_V
        elif counter == 1:
            mystyle = fpb.CAPTIONBAR_GRADIENT_H
        elif counter == 2:
            mystyle = fpb.CAPTIONBAR_SINGLE
        elif counter == 3:
            mystyle = fpb.CAPTIONBAR_RECTANGLE
        else:
            mystyle = fpb.CAPTIONBAR_FILLED_RECTANGLE

        style.SetFirstColour(col1)
        style.SetSecondColour(col2)
        style.SetCaptionStyle(mystyle)

        item = self._pnl.GetFoldPanel(0)
        self._pnl.ApplyCaptionStyle(item, style)
    def OnStyleChange(self, event):

        style = fpb.CaptionBarStyle()

        eventid = event.GetId()

        if eventid == self.ID_USE_HGRADIENT:
            style.SetCaptionStyle(fpb.CAPTIONBAR_GRADIENT_H)

        elif eventid == self.ID_USE_VGRADIENT:
            style.SetCaptionStyle(fpb.CAPTIONBAR_GRADIENT_V)

        elif eventid == self.ID_USE_SINGLE:
            style.SetCaptionStyle(fpb.CAPTIONBAR_SINGLE)

        elif eventid == self.ID_USE_RECTANGLE:
            style.SetCaptionStyle(fpb.CAPTIONBAR_RECTANGLE)

        elif eventid == self.ID_USE_FILLED_RECTANGLE:
            style.SetCaptionStyle(fpb.CAPTIONBAR_FILLED_RECTANGLE)

        else:
            raise "ERROR: Undefined Style Selected For CaptionBar: " + repr(eventid)

        col1 = wx.Colour(self._rslider1.GetValue(), self._gslider1.GetValue(),
                         self._bslider1.GetValue())
        col2 = wx.Colour(self._rslider2.GetValue(), self._gslider2.GetValue(),
                         self._bslider2.GetValue())

        style.SetFirstColour(col1)
        style.SetSecondColour(col2)

        if self._single.GetValue():
            item = self._pnl.GetFoldPanel(1)
            self._pnl.ApplyCaptionStyle(item, style)
        else:
            self._pnl.ApplyCaptionStyleAll(style)
    def CreateMenuBar(self, with_window=False):

        # Make a menubar
        file_menu = wx.Menu()

        FPBTEST_QUIT = wx.NewId()
        FPBTEST_REFRESH = wx.NewId()
        FPB_BOTTOM_FOLD = wx.NewId()
        FPB_SINGLE_FOLD = wx.NewId()
        FPB_EXCLUSIVE_FOLD = wx.NewId()
        FPBTEST_TOGGLE_WINDOW = wx.NewId()
        FPBTEST_ABOUT = wx.NewId()

        file_menu.Append(FPBTEST_QUIT, "&Exit")

        option_menu = None

        if with_window:
            # Dummy option
            option_menu = wx.Menu()
            option_menu.Append(FPBTEST_REFRESH, "&Refresh picture")

        # make fold panel menu

        fpb_menu = wx.Menu()
        fpb_menu.AppendCheckItem(FPB_BOTTOM_FOLD, "Create with &fpb.FPB_COLLAPSE_TO_BOTTOM")

        # Now Implemented!
        fpb_menu.AppendCheckItem(FPB_SINGLE_FOLD, "Create with &fpb.FPB_SINGLE_FOLD")

        # Now Implemented!
        fpb_menu.AppendCheckItem(FPB_EXCLUSIVE_FOLD, "Create with &fpb.FPB_EXCLUSIVE_FOLD")

        fpb_menu.AppendSeparator()
        fpb_menu.Append(FPBTEST_TOGGLE_WINDOW, "&Toggle FoldPanelBar")

        help_menu = wx.Menu()
        help_menu.Append(FPBTEST_ABOUT, "&About")

        menu_bar = wx.MenuBar()

        menu_bar.Append(file_menu, "&File")
        menu_bar.Append(fpb_menu, "&FoldPanel")

        if option_menu:
            menu_bar.Append(option_menu, "&Options")

        menu_bar.Append(help_menu, "&Help")

        self.Bind(wx.EVT_MENU, self.OnAbout, id=FPBTEST_ABOUT)
        self.Bind(wx.EVT_MENU, self.OnQuit, id=FPBTEST_QUIT)
        self.Bind(wx.EVT_MENU, self.OnToggleWindow, id=FPBTEST_TOGGLE_WINDOW)
        self.Bind(wx.EVT_MENU, self.OnCreateBottomStyle, id=FPB_BOTTOM_FOLD)
        self.Bind(wx.EVT_MENU, self.OnCreateNormalStyle, id=FPB_SINGLE_FOLD)
        self.Bind(wx.EVT_MENU, self.OnCreateExclusiveStyle, id=FPB_EXCLUSIVE_FOLD)

        self._bottomstyle = FPB_BOTTOM_FOLD
        self._singlestyle = FPB_SINGLE_FOLD
        self._exclusivestyle = FPB_EXCLUSIVE_FOLD

        return menu_bar
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
class FoldTestPanel(wx.Panel):

    def __init__(self, parent, id, pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.NO_BORDER | wx.TAB_TRAVERSAL):

        wx.Panel.__init__(self, parent, id, pos, size, style)

        self.CreateControls()
        self.GetSizer().Fit(self)
        self.GetSizer().SetSizeHints(self)
        self.GetSizer().Layout()

        self.Bind(fpb.EVT_CAPTIONBAR, self.OnPressCaption)


    def OnPressCaption(self, event):
        event.Skip()

    def CreateControls(self):

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        subpanel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                            wx.NO_BORDER | wx.TAB_TRAVERSAL)
        sizer.Add(subpanel, 1, wx.GROW | wx.ADJUST_MINSIZE, 5)

        subsizer = wx.BoxSizer(wx.VERTICAL)
        subpanel.SetSizer(subsizer)
        itemstrings = ["One", "Two", "Three"]

        item5 = wx.Choice(subpanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                          itemstrings, 0)

        subsizer.Add(item5, 0, wx.GROW | wx.ALL, 5)

        item6 = wx.TextCtrl(subpanel, wx.ID_ANY, "", wx.DefaultPosition, wx.DefaultSize,
                            wx.TE_MULTILINE)
        subsizer.Add(item6, 1, wx.GROW | wx.ALL, 5)

        item7 = wx.RadioButton(subpanel, wx.ID_ANY, "I Like This", wx.DefaultPosition,
                               wx.DefaultSize, 0)
        item7.SetValue(True)
        subsizer.Add(item7, 0, wx.ALIGN_LEFT | wx.ALL, 5)

        item8 = wx.RadioButton(subpanel, wx.ID_ANY, "I Hate It", wx.DefaultPosition,
                               wx.DefaultSize, 0)
        item8.SetValue(False)
        subsizer.Add(item8, 0, wx.ALIGN_LEFT | wx.ALL, 5)
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


#******** 人力资源管理界面************************************************************
class Staff_Inform_Management_Grid(gridlib.Grid):
    def __init__(self, parent):
        gridlib.Grid.__init__(self, parent, -1)
        self.CreateGrid(1, 7)
        self.field_name = ['姓名', '性别', '工号', '卡号', '工位ID','工位名', '电话']
        for i in range(len(self.field_name)):
            self.SetColLabelValue(i, self.field_name[i])
        self.Show_Part_Inform('全部')
        self.AutoSize()

    def Show_Part_Inform(self,label):
        try:
            self.data = []
            new_staff_inform=[]
            if Is_Database_Connect():
                cursor = DB2.cursor()
                if '全部'in label:
                    cursor.execute("select `Name`,`Gender`,`Job_id`,`IC_id`,`Position`,`Position_name`,`Phone` from `info_staff_new` where 1 " )
                    staff_inform = cursor.fetchall()
                else:
                    for i in range(len(label)):
                        cursor.execute("select `Name`,`Gender`,`Job_id`,`IC_id`,`Position`,`Position_name`,`Phone` from `info_staff_new` where `Position_name`= '%s' " % label[i])
                        part_staff_inform = cursor.fetchall()
                        for j in range(len(part_staff_inform)):
                            new_staff_inform.append(part_staff_inform[j])
                    staff_inform=new_staff_inform

                if staff_inform is not None or staff_inform!=():
                    self.data=staff_inform
                    global position
                    position = [x[5] for x in self.data]
                    now_rows = self.GetNumberRows()
                    if len(self.data) > now_rows:
                        for i in range(len(self.data) - now_rows):
                            self.AppendRows(numRows=1)
                    if len(self.data) < now_rows:
                        for i in range(now_rows - len(self.data)):
                            self.DeleteRows(numRows=1)
                if (len(self.data) != 0):
                    for i in range(len(self.field_name)):  # 用来填写所有表头信息
                        self.SetColLabelValue(i, self.field_name[i])
                    self.SetColLabelAlignment(wx.ALIGN_LEFT, wx.ALIGN_BOTTOM)
                    for i in range(len(self.data)):  # 填数据
                        for j in range(len(self.data[i])):
                            self.SetCellValue(i, j, str(self.data[i][j]))
                else:
                    self.CreateGrid(1, 7)
                    self.field_name = ['姓名', '性别', '工号', '卡号', '工位ID','工位名', '电话']
                    for i in range(len(self.field_name)):  # 用来填写所有表头信息
                        self.SetColLabelValue(i, self.field_name[i])
                self.AutoSize()
        except:
            pass
class YLP_Staff_Inform_Management_Panel(wx.Panel):
    def __init__(self, parent,log, id=wx.ID_ANY, title="", pos=wx.DefaultPosition,
                 size=(700,650), style=wx.DEFAULT_FRAME_STYLE):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.select_code = 0
        self._flags = 0
        self.log = log
        self.label_list=[]
        self._leftWindow1 = wx.adv.SashLayoutWindow(self, 101, wx.DefaultPosition,
                                                wx.Size(200, 1000), wx.NO_BORDER |
                                                wx.adv.SW_3D | wx.CLIP_CHILDREN)
        self._leftWindow1.SetDefaultSize(wx.Size(220, 1000))
        self._leftWindow1.SetOrientation(wx.adv.LAYOUT_VERTICAL)
        self._leftWindow1.SetAlignment(wx.adv.LAYOUT_LEFT)
        self._leftWindow1.SetSashVisible(wx.adv.SASH_RIGHT, True)
        self._leftWindow1.SetExtraBorderSize(10)
        self._pnl = 0
        self.ylp_Staff_Inform_Management_Grid=Staff_Inform_Management_Grid(self)

        self.ID_WINDOW_LEFT1 = 101
        self.ID_WINDOW_RIGHT1 = 102
        self._leftWindow1.Bind(wx.adv.EVT_SASH_DRAGGED_RANGE, self.OnFoldPanelBarDrag,
                               id=101, id2=102)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        self.Bind(wx.EVT_SCROLL, self.OnSlideColour)
        self.ReCreateFoldPanel(0)

    def Get_Seek_DateTime(self,event):
        self.time_deal()
        self.TreeCtrl_Refresh(self.start_time,self.end_time)
        # date_start = self.calendar_begin.GetValue()
        # date_end = self.calendar_end.GetValue()
       #  if "从" in date_start or "至"in date_end :
       #      self.TreeCtrl_Refresh(0,0)
       #  else:
       #      if '/' in date_start:
       #          date_start=date_start.split("/")
       #          date_end = date_end.split("/")
       #          date_start=date_start[2],date_start[1],date_start[0]
       #          date_end=date_end[2],date_end[1],date_end[0]
       #          st='-'
       #          date_start = st.join(date_start)
       #          date_end = st.join(date_end)
       #      self.TreeCtrl_Refresh(date_start,date_end)
       #
       # # wx.adv.LayoutAlgorithm().LayoutWindow(self._leftWindow2,self.tree)
    def time_clear(self,event):
        self.calendar_begin.textCtrl.SetValue('从')
        self.calendar_end.textCtrl.SetValue('至')
        self.store_combox.SetValue('ALL')
        self.member_combox.SetValue('ALL')
        self.Terminal_customer.SetValue('ALL')
        self.time_deal()
        self.TreeCtrl_Refresh(self.start_time, self.end_time)
    def time_deal(self):
        try:
            begin_time = self.calendar_begin.GetValue()  # 获得开始时间
            end_time = self.calendar_end.GetValue()
            if begin_time != "从":
                t2 = str(begin_time).split('/')
                t3 = t2[2], t2[1], t2[0]
                st = '-'
                self.start_time = st.join(t3)
            else:
                self.start_time='1900-01-01'
            # 转化截止时间格式函数为20180719
            if end_time != "至":
                t2_1 = str(end_time).split('/')
                t3_1 = t2_1[2], t2_1[1], t2_1[0]
                st_1 = '-'
                self.end_time = st_1.join(t3_1)
            else:
                now_time = str(time.strftime('%Y-%m-%d', time.localtime()))  # 本地当前时间
                self.end_time=now_time
            if begin_time == "从" and end_time != "至":
                self.start_time='1900-01-10 00:00:00'
        except:
            pass
    def store_information_display(self, evt):  # 合同号combobox下拉列表时触发的事件
        try:
            self.store_combox.Clear()
            self.store_combox.SetValue('ALL')
            # self.AllCancel(self)
            self.get_store_id_list=[]
            self.type = []
            try:
                db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0],
                                     charset=charset)  # 打开数据库连接注charset是否需要
                cursor = db.cursor()  # 使用cursor()方法获取操作游标
                cursor.execute("SELECT `Contract_C_Time`,`Dealer` FROM `order_contract_internal` WHERE 1 ")
                get_store_time= cursor.fetchall()  # 获取开始时间、合同号
                db.close()
            except:
                self.log.WriteText('生产进度管理，YLP_Pane.py中YLP_Contract_Order_Management_Panel连接数据库失败，请进行检查 \r\n')
            self.time_deal()
            if len(get_store_time)==0:
                # print '未查询到合同号'
                pass
            else:
                if self.calendar_begin.GetValue() != "从" and self.calendar_end.GetValue() != "至":
                    # 转化开始时间格式函数为20180719   ##在获取合同号时读取时间范围内的合同号
                    if self.start_time > self.end_time:
                        self.log.WriteText( '生产进度管理，YLP_Pane.py中YLP_Contract_Order_Management_Panel类门店查询时间范围有误，请进行检查 \r\n')
                    else:
                        self.store_id_time_list_get(self.start_time,self.end_time,get_store_time,self.get_store_id_list)
                elif self.calendar_begin.GetValue() != "从" and self.calendar_end.GetValue() == "至":  # 筛选大于某一个值
                    self.store_id_time_list_get(self.start_time, self.end_time, get_store_time, self.get_store_id_list)
                elif self.calendar_begin.GetValue() == "从" and self.calendar_end.GetValue() != "至":  # 筛选大于某一个值
                    self.store_id_time_list_get(self.start_time, self.end_time, get_store_time, self.get_store_id_list)
                else:  # 筛选大于某一个值
                    for i in range(len(get_store_time)):
                        self.store_id_list_get(get_store_time[i][1], self.get_store_id_list)
                if len(self.get_store_id_list) == 0:
                    self.log.WriteText('生产进度管理，YLP_Pane.py中YLP_Contract_Order_Management_Panel类门店查询此时间范围无门店号，请进行检查 \r\n')
                else:
                    self.store_combox.Append('ALL')
                    for i in range(len(self.get_store_id_list)):
                        self.store_combox.Append(self.get_store_id_list[i])
            # self.Refresh()
        except:
            self.log.WriteText('生产进度管理，YLP_Pane.py中YLP_Contract_Order_Management_Panel类门店查询下拉触发事件部分出现错误，请进行检查 \r\n')
    def store_id_list_get(self,date3,date4):
        if date3 != None or date3 != '' or date3 != '0':
            if date3 not in date4:  # 对读到的单号去重后放入列表get_contract_id_list
                date4.append(date3)  #
    def store_id_time_list_get(self,time1,time2,date1,date3):
        for i in range(len(date1)):
            if date1[i][0] == None or date1[i][0] == '' or date1[i][0] == '0':
                pass
            else:
                get_time_str = str(date1[i][0].strftime('%Y-%m-%d'))
                if get_time_str >= time1 and get_time_str <= time2:
                    if date1[i][1] != None or date1[i][1] != '' or date1[i][1] != '0':
                        if date1[i][1] not in date3:  # 对读到的单号去重后放入列表get_contract_id_list
                            date3.append(date1[i][1])  #
    #-----------------------------------------
    def store_id_click(self,event):
        self.getstring=event.GetString()
        # self.member_combox.SetValue('ALL')
        # self.Terminal_customer.SetValue('ALL')
        # self.time_deal()
        # self.TreeCtrl_Refresh(self.start_time, self.end_time)

    def search_button(self,event):
        pass
    #-----------------------------------------
    def member_information_display(self, evt):  # 订单号combobox下拉列表时触发的事件
        try:
            self.member_combox.Clear()
            self.member_combox.SetValue('ALL')
            # self.AllCancel(self)
            self.get_member_id_list=[]
            try:
                db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0],
                                     charset=charset)  # 打开数据库连接注charset是否需要
                cursor = db.cursor()  # 使用cursor()方法获取操作游标
                cursor.execute("SELECT `Contract_C_Time`,`Customer_name` FROM `order_contract_internal` WHERE 1 ")
                get_member_time= cursor.fetchall()  # 获取开始时间、合同号
                db.close()
            except:
                self.log.WriteText('生产进度管理，YLP_Pane.py中YLP_Contract_Order_Management_Panel连接数据库失败，请进行检查 \r\n')
            self.time_deal()
            if len(get_member_time)==0:
                pass
            else:
                if self.calendar_begin.GetValue() != "从" and self.calendar_end.GetValue() != "至":
                    # 转化开始时间格式函数为20180719   ##在获取合同号时读取时间范围内的合同号
                    if self.start_time > self.end_time:
                        self.log.WriteText( '生产进度管理，YLP_Pane.py中YLP_Contract_Order_Management_Panel类下单员查询时间范围有误，请进行检查 \r\n')
                    else:
                        self.store_id_time_list_get(self.start_time, self.end_time, get_member_time,self.get_member_id_list)
                elif self.calendar_begin.GetValue() != "从" and self.calendar_end.GetValue() == "至":  # 筛选大于某一个值
                    self.store_id_time_list_get(self.start_time, self.end_time, get_member_time,self.get_member_id_list)
                elif self.calendar_begin.GetValue() == "从" and self.calendar_end.GetValue() != "至":  # 筛选大于某一个值
                    self.store_id_time_list_get(self.start_time, self.end_time, get_member_time,self.get_member_id_list)
                else:  # 筛选大于某一个值
                    for i in range(len(get_member_time)):
                        self.store_id_list_get(get_member_time[i][1], self.get_member_id_list)
                if len(self.get_member_id_list) == 0:
                    self.log.WriteText('生产进度管理，YLP_Pane.py中YLP_Contract_Order_Management_Panel类下单员查询此时间范围无下单员，请进行检查 \r\n')
                else:
                    self.member_combox.Append('ALL')
                    for i in range(len(self.get_member_id_list)):
                        self.member_combox.Append(self.get_member_id_list[i])
            # self.Contract_refresh()
        except:
            self.log.WriteText('生产进度管理，YLP_Pane.py中YLP_Contract_Order_Management_Panel类下单员查询下拉触发事件部分出现错误，请进行检查 \r\n')
    def member_id_click(self,event):
        self.store_combox.SetValue('ALL')
        self.Terminal_customer.SetValue('ALL')
        self.time_deal()
        self.TreeCtrl_Refresh(self.start_time, self.end_time)
    def terminal_information_time_get(self,time1,time2,date1,date4):
        for i in range(len(date1)):
            if date1[i][0] == None or date1[i][0] == '' or date1[i][0] == '0':
                pass
            else:
                get_time_str = str(date1[i][0].strftime('%Y-%m-%d'))
                if get_time_str >= time1 and get_time_str <= time2:
                    if date1[i][1] != None or date1[i][1] != '' or date1[i][1] != '0':
                        if date1[i][1] not in date4:  # 对读到的单号去重后放入列表get_contract_id_list
                            date4.append(date1[i][1])  #
    def terminal_information_get(self,date3,date4):
        if date3 != None or date3 != '' or date3 != '0':
            if date3 not in date4:  # 对读到的单号去重后放入列表get_contract_id_list
                date4.append(date3)  #
    def Terminal_information_display(self, evt):  # 订单号combobox下拉列表时触发的事件
        try:
            self.Terminal_customer.Clear()
            self.Terminal_customer.SetValue('ALL')
            # self.AllCancel(self)
            self.get_terminal_customer_id_list=[]
            self.type = []
            try:
                db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0],
                                     charset=charset)  # 打开数据库连接注charset是否需要
                cursor = db.cursor()  # 使用cursor()方法获取操作游标
                cursor.execute("SELECT `Contract_C_Time`,`Customer_name` FROM `order_order_online` WHERE 1 ")
                get_terminal_customer_time= cursor.fetchall()  # 获取开始时间、合同号
                db.close()
            except:
                self.log.WriteText('生产进度管理，YLP_Pane.py中YLP_Contract_Order_Management_Panel连接数据库失败，请进行检查 \r\n')
            self.time_deal()
            if len(get_terminal_customer_time)==0:
                pass
            else:
                if self.calendar_begin.GetValue() != "从" and self.calendar_end.GetValue() != "至":
                    # 转化开始时间格式函数为20180719   ##在获取合同号时读取时间范围内的合同号
                    if self.start_time > self.end_time:
                        self.log.WriteText( '生产进度管理，YLP_Pane.py中YLP_Contract_Order_Management_Panel类终端客户查询时间范围有误，请进行检查 \r\n')
                    else:
                        self.terminal_information_time_get(self.start_time,self.end_time,get_terminal_customer_time,self.get_terminal_customer_id_list)
                elif self.calendar_begin.GetValue() != "从" and self.calendar_end.GetValue() == "至":  # 筛选大于某一个值
                    self.terminal_information_time_get(self.start_time, self.end_time, get_terminal_customer_time,self.get_terminal_customer_id_list)
                elif self.calendar_begin.GetValue() == "从" and self.calendar_end.GetValue() != "至":  # 筛选大于某一个值
                    self.terminal_information_time_get(self.start_time, self.end_time, get_terminal_customer_time,self.get_terminal_customer_id_list)
                else:  # 筛选大于某一个值
                    for i in range(len(get_terminal_customer_time)):
                        self.terminal_information_get(get_terminal_customer_time[i][1],self.get_terminal_customer_id_list)
                if len(self.get_terminal_customer_id_list) == 0:
                    self.log.WriteText('生产进度管理，YLP_Pane.py中YLP_Contract_Order_Management_Panel类终端客户查询此时间范围无终端客户，请进行检查 \r\n')
                else:
                    self.Terminal_customer.Append('ALL')
                    for i in range(len(self.get_terminal_customer_id_list)):
                        self.Terminal_customer.Append(self.get_terminal_customer_id_list[i])
        except:
            self.log.WriteText(
                '生产进度管理，YLP_Pane.py中YLP_Contract_Order_Management_Panel类终端客户查询下拉触发事件部分出现错误，请进行检查 \r\n')
        # self.Contract_refresh()
    def Terminal_id_click(self,event):
        self.store_combox.SetValue('ALL')
        self.member_combox.SetValue('ALL')
        self.time_deal()
        self.TreeCtrl_Refresh(self.start_time, self.end_time)
    def OnSize(self, event):
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.ylp_Staff_Inform_Management_Grid)
        event.Skip()
    def OnQuit(self, event):
        self.Destroy()
    def OnToggleWindow(self, event):

        self._leftWindow1.Show(not self._leftWindow1.IsShown())
        # Leaves bits of itself behind sometimes
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.ylp_Show_Inform_Panel)
        self.ylp_Show_Inform_Panel.Refresh()

        event.Skip()
    def OnFoldPanelBarDrag(self, event):

        # if event.GetDragStatus() == wx.SASH_STATUS_OUT_OF_RANGE:
        #     return

        if event.GetId() == self.ID_WINDOW_LEFT1:
            self._leftWindow1.SetDefaultSize(wx.Size(event.GetDragRect().width, 1000))
        # if event.GetId() == self.ID_WINDOW_RIGHT1:
        #     self._leftWindow2.SetDefaultSize(wx.Size(event.GetDragRect().width, 1000))
        # Leaves bits of itself behind sometimes
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.ylp_Staff_Inform_Management_Grid)
        # wx.adv.LayoutAlgorithm().LayoutWindow(self, self.ylp_Show_Inform_Panel)
        self.ylp_Staff_Inform_Management_Grid.Refresh()
        event.Skip()
    #-------------------------------------------
    def EvtCheckListBox(self,event):
        index = event.GetSelection()
        label = self.lb.GetString(index)
        status = 'False'
        if self.lb.IsChecked(index):
            status = 'True'
            self.label_list.append(label)
        else:
            self.label_list.remove(label)
        self.ylp_Staff_Inform_Management_Grid.Show_Part_Inform(self.label_list)
        #self.lb.SetSelection(index)

    def ReCreateFoldPanel(self, fpb_flags):

        self._leftWindow1.DestroyChildren()

        self._pnl = fpb.FoldPanelBar(self._leftWindow1, -1, wx.DefaultPosition,
                                     wx.Size(-1,-1), agwStyle=fpb_flags)

        Images = wx.ImageList(16,16)
        Images.Add(GetExpandedIconBitmap())
        Images.Add(GetCollapsedIconBitmap())
        item = self._pnl.AddFoldPanel("搜索", False, foldIcons=Images)
        self.statictext6 = wx.StaticText(item, -1, label="按工位搜索员工信息：")
        self._pnl.AddFoldPanelWindow(item, self.statictext6)


        # sampleList = ['全部','管理员','接单', '下单', '技术审核', '财务审核', '下料待排样', '加工中心下料',
        #               '铣边前分拣', '铣边', '异形机砂', '压条', '手工打磨', '模压前分拣',
        #               '真空膜压预排样', '喷胶与烘干', '真空膜压', '真空膜压后分包', '发货', '质量检查'
        #     , '仿古', '拆单', '审核拆单', '软包', '入库', '打孔', '管理员', '附件', '特殊工艺及组装'
        #     , '拉手安装套色扣线', '打胶磨', '摆盘', '开机', '上膜', '削皮', '背面清理', '玻璃门修板'
        #     , '负压机', '半检分色', '线条加工', '硬包']
        if Is_Database_Connect():
            cursor = DB2.cursor()
            cursor.execute("select `Position_name` from `info_staff_new` where 1 ")
            Position_name = cursor.fetchall()
            Position_name=flatten(Position_name)
            sampleList=list(set(Position_name))
            sampleList.insert(0, "全部")
            if None in sampleList:
                sampleList.remove(None)
            else:
                pass
        else:
            return
        self.lb = wx.CheckListBox(item, -1, (80, 50), wx.DefaultSize, sampleList)
        self.Bind(wx.EVT_CHECKLISTBOX, self.EvtCheckListBox, self.lb)
        self.lb.SetSelection(0)
        pos = self.lb.GetPosition().x + self.lb.GetSize().width + 25
        self._pnl.AddFoldPanelWindow(item, self.lb)

        # search = wx.Button(item, wx.ID_ANY, "搜索")
        # self._pnl.AddFoldPanelWindow(item, search)
        # search.Bind(wx.EVT_BUTTON, self.search_button)
        self._leftWindow1.SizeWindows()

    #----------------------------------------
    def onDateStart(self,event):
        self.date_start=self.calendar_begin.GetValue()
        self.date_end=self.calendar_end.GetValue()
        self.log.WriteText("天外天系统收到操作员控制指令，开始执行日期查询操作，起始日期："+str(self.date_start)+"，终止日期："+str(self.date_end)+"\r\n")
    def OnCreateBottomStyle(self, event):

        # recreate with style collapse to bottom, which means
        # all panels that are collapsed are placed at the bottom,
        # or normal

        if event.IsChecked():
            self.GetMenuBar().Check(self._singlestyle, False)
            self.GetMenuBar().Check(self._exclusivestyle, False)
            self._flags = self._flags & ~fpb.FPB_SINGLE_FOLD
            self._flags = self._flags & ~fpb.FPB_EXCLUSIVE_FOLD
            self._flags = self._flags | fpb.FPB_COLLAPSE_TO_BOTTOM
        else:
            self._flags = self._flags & ~fpb.FPB_COLLAPSE_TO_BOTTOM

        self.ReCreateFoldPanel(self._flags)
        #self.Create_TreeCtrl()
    def OnCreateNormalStyle(self, event):

        # recreate with style where only one panel at the time is
        # allowed to be opened

        if event.IsChecked():
            self.GetMenuBar().Check(self._bottomstyle, False)
            self.GetMenuBar().Check(self._exclusivestyle, False)
            self._flags = self._flags & ~fpb.FPB_EXCLUSIVE_FOLD
            self._flags = self._flags & ~fpb.FPB_COLLAPSE_TO_BOTTOM
            self._flags = self._flags | fpb.FPB_SINGLE_FOLD
        else:
            self._flags = self._flags & ~fpb.FPB_SINGLE_FOLD

        self.ReCreateFoldPanel(self._flags)
        #self.Create_TreeCtrl()
    def OnCreateExclusiveStyle(self, event):
        # recreate with style where only one panel at the time is
        # allowed to be opened and the others are collapsed to bottom
        if event.IsChecked():
            self.GetMenuBar().Check(self._singlestyle, False)
            self.GetMenuBar().Check(self._bottomstyle, False)
            self._flags = self._flags & ~fpb.FPB_SINGLE_FOLD
            self._flags = self._flags & ~fpb.FPB_COLLAPSE_TO_BOTTOM
            self._flags = self._flags | fpb.FPB_EXCLUSIVE_FOLD
        else:
            self._flags = self._flags & ~fpb.FPB_EXCLUSIVE_FOLD
        self.ReCreateFoldPanel(self._flags)
        #self.Create_TreeCtrl()
    def OnCollapseMe(self, event):
        for i in range(0, self._pnl.GetCount()):
            item = self._pnl.GetFoldPanel(i)
            self._pnl.Collapse(item)
    def OnExpandMe(self, event):
        style = fpb.CaptionBarStyle()
        counter = 0
        for items in self.radiocontrols:
            if items.GetValue():
                break
            counter = counter + 1
        if counter == 0:
            mystyle = fpb.CAPTIONBAR_GRADIENT_V
        elif counter == 1:
            mystyle = fpb.CAPTIONBAR_GRADIENT_H
        elif counter == 2:
            mystyle = fpb.CAPTIONBAR_SINGLE
        elif counter == 3:
            mystyle = fpb.CAPTIONBAR_RECTANGLE
        else:
            mystyle = fpb.CAPTIONBAR_FILLED_RECTANGLE

        # style.SetCaptionStyle(mystyle)
        # self._pnl.ApplyCaptionStyleAll(style)
    def OnSlideColour(self, event):

        col1 = wx.Colour(self._rslider1.GetValue(), self._gslider1.GetValue(),
                         self._bslider1.GetValue())
        col2 = wx.Colour(self._rslider2.GetValue(), self._gslider2.GetValue(),
                         self._bslider2.GetValue())

        style = fpb.CaptionBarStyle()

        counter = 0
        for items in self.radiocontrols:
            if items.GetValue():
                break

            counter = counter + 1

        if counter == 0:
            mystyle = fpb.CAPTIONBAR_GRADIENT_V
        elif counter == 1:
            mystyle = fpb.CAPTIONBAR_GRADIENT_H
        elif counter == 2:
            mystyle = fpb.CAPTIONBAR_SINGLE
        elif counter == 3:
            mystyle = fpb.CAPTIONBAR_RECTANGLE
        else:
            mystyle = fpb.CAPTIONBAR_FILLED_RECTANGLE

        style.SetFirstColour(col1)
        style.SetSecondColour(col2)
        style.SetCaptionStyle(mystyle)

        item = self._pnl.GetFoldPanel(0)
        self._pnl.ApplyCaptionStyle(item, style)
    def OnStyleChange(self, event):

        style = fpb.CaptionBarStyle()

        eventid = event.GetId()

        if eventid == self.ID_USE_HGRADIENT:
            style.SetCaptionStyle(fpb.CAPTIONBAR_GRADIENT_H)

        elif eventid == self.ID_USE_VGRADIENT:
            style.SetCaptionStyle(fpb.CAPTIONBAR_GRADIENT_V)

        elif eventid == self.ID_USE_SINGLE:
            style.SetCaptionStyle(fpb.CAPTIONBAR_SINGLE)

        elif eventid == self.ID_USE_RECTANGLE:
            style.SetCaptionStyle(fpb.CAPTIONBAR_RECTANGLE)

        elif eventid == self.ID_USE_FILLED_RECTANGLE:
            style.SetCaptionStyle(fpb.CAPTIONBAR_FILLED_RECTANGLE)

        else:
            raise "ERROR: Undefined Style Selected For CaptionBar: " + repr(eventid)

        col1 = wx.Colour(self._rslider1.GetValue(), self._gslider1.GetValue(),
                         self._bslider1.GetValue())
        col2 = wx.Colour(self._rslider2.GetValue(), self._gslider2.GetValue(),
                         self._bslider2.GetValue())

        style.SetFirstColour(col1)
        style.SetSecondColour(col2)

        if self._single.GetValue():
            item = self._pnl.GetFoldPanel(1)
            self._pnl.ApplyCaptionStyle(item, style)
        else:
            self._pnl.ApplyCaptionStyleAll(style)
    def CreateMenuBar(self, with_window=False):

        # Make a menubar
        file_menu = wx.Menu()

        FPBTEST_QUIT = wx.NewId()
        FPBTEST_REFRESH = wx.NewId()
        FPB_BOTTOM_FOLD = wx.NewId()
        FPB_SINGLE_FOLD = wx.NewId()
        FPB_EXCLUSIVE_FOLD = wx.NewId()
        FPBTEST_TOGGLE_WINDOW = wx.NewId()
        FPBTEST_ABOUT = wx.NewId()

        file_menu.Append(FPBTEST_QUIT, "&Exit")

        option_menu = None

        if with_window:
            # Dummy option
            option_menu = wx.Menu()
            option_menu.Append(FPBTEST_REFRESH, "&Refresh picture")

        # make fold panel menu

        fpb_menu = wx.Menu()
        fpb_menu.AppendCheckItem(FPB_BOTTOM_FOLD, "Create with &fpb.FPB_COLLAPSE_TO_BOTTOM")

        # Now Implemented!
        fpb_menu.AppendCheckItem(FPB_SINGLE_FOLD, "Create with &fpb.FPB_SINGLE_FOLD")

        # Now Implemented!
        fpb_menu.AppendCheckItem(FPB_EXCLUSIVE_FOLD, "Create with &fpb.FPB_EXCLUSIVE_FOLD")

        fpb_menu.AppendSeparator()
        fpb_menu.Append(FPBTEST_TOGGLE_WINDOW, "&Toggle FoldPanelBar")

        help_menu = wx.Menu()
        help_menu.Append(FPBTEST_ABOUT, "&About")

        menu_bar = wx.MenuBar()

        menu_bar.Append(file_menu, "&File")
        menu_bar.Append(fpb_menu, "&FoldPanel")

        if option_menu:
            menu_bar.Append(option_menu, "&Options")

        menu_bar.Append(help_menu, "&Help")

        self.Bind(wx.EVT_MENU, self.OnAbout, id=FPBTEST_ABOUT)
        self.Bind(wx.EVT_MENU, self.OnQuit, id=FPBTEST_QUIT)
        self.Bind(wx.EVT_MENU, self.OnToggleWindow, id=FPBTEST_TOGGLE_WINDOW)
        self.Bind(wx.EVT_MENU, self.OnCreateBottomStyle, id=FPB_BOTTOM_FOLD)
        self.Bind(wx.EVT_MENU, self.OnCreateNormalStyle, id=FPB_SINGLE_FOLD)
        self.Bind(wx.EVT_MENU, self.OnCreateExclusiveStyle, id=FPB_EXCLUSIVE_FOLD)

        self._bottomstyle = FPB_BOTTOM_FOLD
        self._singlestyle = FPB_SINGLE_FOLD
        self._exclusivestyle = FPB_EXCLUSIVE_FOLD

        return menu_bar

#********* 报错报废管理界面****************************************************
global dict_test_position
global dict_test_position1
dict_test_position={37:'半检工位',18:'质检工位'}
dict_test_position1={'半检工位':37,'质检工位':18}

class YLP_Now_Element_Scrap_Grid(gridlib.Grid):
    def __init__(self, parent):
        gridlib.Grid.__init__(self, parent, -1)
        self.CreateGrid(1, 5)
        self.field_name = ['零件号','生产计划','报错时间','报错工位','报错员工']
        for i in range(len(self.field_name)):
            self.SetColLabelValue(i, self.field_name[i])
        #self.Now_Show_ERROR_Part_Inform()
        self.AutoSize()
        self.Bind(wx.EVT_TIMER, self.TimerEvent)
        self.timer = wx.Timer(self)
        self.timer.Start(3000)
    def TimerEvent(self,event):
        self.Now_Show_ERROR_Part_Inform()
        self.Insert_Staff_Workload()
    def Now_Show_ERROR_Part_Inform(self):
        try:
            self.now_data_error = []
            new_staff_inform = []
            if Is_Database_Connect():
                cursor = DB.cursor()
                cursor.execute(
                    "select `Id`,`Time_schedule`,`staff_report_error_time`,`staff_report_error_workposition`,`report_error_staff` from `order_element_report_error` where `state`=1000 " )
                record = cursor.fetchall()
                if record is not None or record != ():
                    for i in range(len(record)):
                        self.now_data_error.append(record[i])
                    self.now_data_error.sort(key=lambda x: [-x[1]])
                    for i in range(len(self.now_data_error)):
                        try:
                            self.now_data_error[i]=list(self.now_data_error[i])
                            self.now_data_error[i][3]=str(dict_test_position[self.now_data_error[i][3]])   #
                        except:
                            pass
                    now_rows = self.GetNumberRows()
                    if len(self.now_data_error) > now_rows:
                        for i in range(len(self.now_data_error) - now_rows):
                            self.AppendRows(numRows=1)
                    if len(self.now_data_error) < now_rows:
                        for i in range(now_rows - len(self.now_data_error)):
                            self.DeleteRows(numRows=1)
                if (len(self.now_data_error) != 0):
                    for i in range(len(self.field_name)):  # 用来填写所有表头信息
                        self.SetColLabelValue(i, self.field_name[i])
                    self.SetColLabelAlignment(wx.ALIGN_LEFT, wx.ALIGN_BOTTOM)
                    for i in range(len(self.now_data_error)):  # 填数据
                        for j in range(len(self.now_data_error[i])):
                            self.SetCellValue(i, j, str(self.now_data_error[i][j]))
                else:
                    self.CreateGrid(1,5)
                    self.field_name = ['零件号','生产计划','报错时间','报错工位','报错员工']
                    for i in range(len(self.field_name)):  # 用来填写所有表头信息
                        self.SetColLabelValue(i, self.field_name[i])
                self.AutoSize()
        except:
            pass
    def Insert_Staff_Workload(self):
        try:
            if Is_Database_Connect():
                cursor = DB.cursor()
                cursor.execute(
                    "select `Id`,`principal`,`process_time`,`responsible_workposition`,`state` from `order_element_report_error` where `state`=1003 or `state`=1005")
                record = cursor.fetchall()

                if record!=() and record is not None:
                    work_day = record[0][2].strftime('%Y-%m-%d')
                    for i in range(len(record)):
                        if '&' in record[i][1]:
                            job_id=record[i][1].split('&')
                        else:
                            job_id=[]
                            job_id.append(record[i][1])
                        for j in range(len(job_id)):
                            cursor.execute(
                                "select `fault_area`,`Id_list` from `work_staff_workload_manual_area` where `Job_id`='%s' and `Work_day`='%s' " %(job_id[j],work_day))
                            staff_workload_record = cursor.fetchone()
                            cursor.execute(
                                "select `Board_height`,`Board_width` from `order_element_online` where `Id`='%s'  " % (record[i][0]))
                            height_width = cursor.fetchone()
                            board_area=height_width[0]*height_width[1]
                            if staff_workload_record==() or staff_workload_record is None:
                                cursor.execute("insert into `work_staff_workload_manual_area` (`Job_id`,`Position`,`fault_area`,`Work_day`,`Id_list`) VALUES ('%s','%s','%s','%s','%s')" %(job_id[j],record[i][3],board_area,work_day,record[i][0]))
                            else:
                                if record[i][0] in staff_workload_record[1]:  #判断有无重复统计工人工作量
                                    pass
                                else:
                                    fault_area=staff_workload_record[0]+board_area
                                    Id_list=staff_workload_record[1]+'&'+record[i][0]
                                    cursor.execute("update `work_staff_workload_manual_area` set `fault_area`='%s',`Id_list`='%s' where `Job_id`='%s'and `Work_day`='%s' " % (fault_area, Id_list, job_id[j],work_day))
                        if record[i][4]==1003:
                            cursor.execute("update `order_element_report_error` set `state`=1004 where `Id`='%s'" % ( record[i][0]))
                        else:
                            cursor.execute(
                                "update `order_element_report_error` set `state`=1007 where `Id`='%s'" % (record[i][0]))
                        DB.commit()
                else:
                    pass
        except:
            pass
class YLP_Now_Element_Scrap_Panel(wx.Panel):
    def __init__(self, parent,log, id=wx.ID_ANY, title="", pos=wx.DefaultPosition,
                 size=(700,650), style=wx.DEFAULT_FRAME_STYLE):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.log = log
        self.Element_Scrap_Grid=YLP_Now_Element_Scrap_Grid(self)

class YLP_History_Element_Scrap_Grid(gridlib.Grid):
    def __init__(self, parent):
        gridlib.Grid.__init__(self, parent, -1)
        self.CreateGrid(1, 11)
        self.field_name = ['零件号','生产计划','报错时间','报错工位','报错员工','管理员报错时间','责任工位','负责人','加工时间','管理员姓名','状态']
        for i in range(len(self.field_name)):
            self.SetColLabelValue(i, self.field_name[i])
        self.History_Show_ERROR_Part_Inform('全部')
        self.AutoSize()
    #     self.Bind(wx.EVT_TIMER, self.TimerEvent)
    #     self.timer = wx.Timer(self)
    #     self.timer.Start(3000)
    # def TimerEvent(self,event):
    #     self.History_Show_ERROR_Part_Inform('全部')
    def History_Show_ERROR_Part_Inform(self,label):
        try:
            self.history_data_error = []
            new_staff_inform = []
            if Is_Database_Connect():
                cursor = DB.cursor()
                if '全部'in label:
                    cursor.execute(
                        "select `Id`,`Time_schedule`,`staff_report_error_time`,`staff_report_error_workposition`,`report_error_staff`,`manage_report_error_time`,`responsible_workposition`,`principal`,`process_time`,`report_error_manage`,`state` from `order_element_report_error` where `state`=1004 or`state`=1003")
                    self.history_data_error = cursor.fetchall()
                else:
                    for i in range(len(label)):
                        cursor.execute(
                            "select `Id`,`Time_schedule`,`staff_report_error_time`,`staff_report_error_workposition`,`report_error_staff`,`manage_report_error_time`,`responsible_workposition`,`principal`,`process_time`,`report_error_manage`,`state` from `order_element_report_error` where (`state`=1004 or `state`=1003) and `staff_report_error_workposition`='%s' " % (dict_test_position1[str(label[i])])  )
                        self.history_data_error.extend(cursor.fetchall())
                if self.history_data_error is not None or self.history_data_error != ():
                    for i in range(len(self.history_data_error)):
                        try:
                            self.history_data_error[i]=list(self.history_data_error[i])
                            self.history_data_error[i][3]=str(dict_test_position[self.history_data_error[i][3]])
                        except:
                            pass
                    now_rows = self.GetNumberRows()
                    if len(self.history_data_error) > now_rows:
                        for i in range(len(self.history_data_error) - now_rows):
                            self.AppendRows(numRows=1)
                    if len(self.history_data_error) < now_rows:
                        for i in range(now_rows - len(self.history_data_error)):
                            self.DeleteRows(numRows=1)
                if (len(self.history_data_error) != 0):
                    for i in range(len(self.field_name)):  # 用来填写所有表头信息
                        self.SetColLabelValue(i, self.field_name[i])
                    self.SetColLabelAlignment(wx.ALIGN_LEFT, wx.ALIGN_BOTTOM)
                    for i in range(len(self.history_data_error)):  # 填数据
                        for j in range(len(self.history_data_error[i])):
                            self.SetCellValue(i, j, str(self.history_data_error[i][j]))
                else:
                    self.CreateGrid(1,11)
                    self.field_name = ['零件号','生产计划','报错时间','报错工位','报错员工','管理员报错时间','责任工位','负责人','加工时间','管理员姓名','状态']
                    for i in range(len(self.field_name)):  # 用来填写所有表头信息
                        self.SetColLabelValue(i, self.field_name[i])
                self.AutoSize()
        except:
            pass
class YLP_History_Element_Scrap_Panel(wx.Panel):
    def __init__(self, parent,log, id=wx.ID_ANY, title="", pos=wx.DefaultPosition,
                 size=(700,650), style=wx.DEFAULT_FRAME_STYLE):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.select_code = 0
        self._flags = 0
        self.log = log
        self.label_list=[]
        self._leftWindow1 = wx.adv.SashLayoutWindow(self, 101, wx.DefaultPosition,
                                                wx.Size(200, 1000), wx.NO_BORDER |
                                                wx.adv.SW_3D | wx.CLIP_CHILDREN)
        self._leftWindow1.SetDefaultSize(wx.Size(220, 1000))
        self._leftWindow1.SetOrientation(wx.adv.LAYOUT_VERTICAL)
        self._leftWindow1.SetAlignment(wx.adv.LAYOUT_LEFT)
        self._leftWindow1.SetSashVisible(wx.adv.SASH_RIGHT, True)
        self._leftWindow1.SetExtraBorderSize(10)
        self._pnl = 0
        self.ylp_History_Element_Scrap=YLP_History_Element_Scrap_Grid(self)
        self.ID_WINDOW_LEFT1 = 101
        self.ID_WINDOW_RIGHT1 = 102
        self._leftWindow1.Bind(wx.adv.EVT_SASH_DRAGGED_RANGE, self.OnFoldPanelBarDrag,
                               id=101, id2=102)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        self.Bind(wx.EVT_SCROLL, self.OnSlideColour)
        self.ReCreateFoldPanel(0)
    def Get_Seek_DateTime(self,event):
        self.time_deal()
        self.TreeCtrl_Refresh(self.start_time,self.end_time)
        # date_start = self.calendar_begin.GetValue()
        # date_end = self.calendar_end.GetValue()
       #  if "从" in date_start or "至"in date_end :
       #      self.TreeCtrl_Refresh(0,0)
       #  else:
       #      if '/' in date_start:
       #          date_start=date_start.split("/")
       #          date_end = date_end.split("/")
       #          date_start=date_start[2],date_start[1],date_start[0]
       #          date_end=date_end[2],date_end[1],date_end[0]
       #          st='-'
       #          date_start = st.join(date_start)
       #          date_end = st.join(date_end)
       #      self.TreeCtrl_Refresh(date_start,date_end)
       #
       # # wx.adv.LayoutAlgorithm().LayoutWindow(self._leftWindow2,self.tree)
    def time_clear(self,event):
        self.calendar_begin.textCtrl.SetValue('从')
        self.calendar_end.textCtrl.SetValue('至')
        self.store_combox.SetValue('ALL')
        self.member_combox.SetValue('ALL')
        self.Terminal_customer.SetValue('ALL')
        self.time_deal()
        self.TreeCtrl_Refresh(self.start_time, self.end_time)
    def time_deal(self):
        try:
            begin_time = self.calendar_begin.GetValue()  # 获得开始时间
            end_time = self.calendar_end.GetValue()
            if begin_time != "从":
                t2 = str(begin_time).split('/')
                t3 = t2[2], t2[1], t2[0]
                st = '-'
                self.start_time = st.join(t3)
            else:
                self.start_time='1900-01-01'
            # 转化截止时间格式函数为20180719
            if end_time != "至":
                t2_1 = str(end_time).split('/')
                t3_1 = t2_1[2], t2_1[1], t2_1[0]
                st_1 = '-'
                self.end_time = st_1.join(t3_1)
            else:
                now_time = str(time.strftime('%Y-%m-%d', time.localtime()))  # 本地当前时间
                self.end_time=now_time
            if begin_time == "从" and end_time != "至":
                self.start_time='1900-01-10 00:00:00'
        except:
            pass
    def store_information_display(self, evt):  # 合同号combobox下拉列表时触发的事件
        try:
            self.store_combox.Clear()
            self.store_combox.SetValue('ALL')
            # self.AllCancel(self)
            self.get_store_id_list=[]
            self.type = []
            try:
                db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0],
                                     charset=charset)  # 打开数据库连接注charset是否需要
                cursor = db.cursor()  # 使用cursor()方法获取操作游标
                cursor.execute("SELECT `Contract_C_Time`,`Dealer` FROM `order_contract_internal` WHERE 1 ")
                get_store_time= cursor.fetchall()  # 获取开始时间、合同号
                db.close()
            except:
                self.log.WriteText('生产进度管理，YLP_Pane.py中YLP_Contract_Order_Management_Panel连接数据库失败，请进行检查 \r\n')
            self.time_deal()
            if len(get_store_time)==0:
                # print '未查询到合同号'
                pass
            else:
                if self.calendar_begin.GetValue() != "从" and self.calendar_end.GetValue() != "至":
                    # 转化开始时间格式函数为20180719   ##在获取合同号时读取时间范围内的合同号
                    if self.start_time > self.end_time:
                        self.log.WriteText( '生产进度管理，YLP_Pane.py中YLP_Contract_Order_Management_Panel类门店查询时间范围有误，请进行检查 \r\n')
                    else:
                        self.store_id_time_list_get(self.start_time,self.end_time,get_store_time,self.get_store_id_list)
                elif self.calendar_begin.GetValue() != "从" and self.calendar_end.GetValue() == "至":  # 筛选大于某一个值
                    self.store_id_time_list_get(self.start_time, self.end_time, get_store_time, self.get_store_id_list)
                elif self.calendar_begin.GetValue() == "从" and self.calendar_end.GetValue() != "至":  # 筛选大于某一个值
                    self.store_id_time_list_get(self.start_time, self.end_time, get_store_time, self.get_store_id_list)
                else:  # 筛选大于某一个值
                    for i in range(len(get_store_time)):
                        self.store_id_list_get(get_store_time[i][1], self.get_store_id_list)
                if len(self.get_store_id_list) == 0:
                    self.log.WriteText('生产进度管理，YLP_Pane.py中YLP_Contract_Order_Management_Panel类门店查询此时间范围无门店号，请进行检查 \r\n')
                else:
                    self.store_combox.Append('ALL')
                    for i in range(len(self.get_store_id_list)):
                        self.store_combox.Append(self.get_store_id_list[i])
            # self.Refresh()
        except:
            self.log.WriteText('生产进度管理，YLP_Pane.py中YLP_Contract_Order_Management_Panel类门店查询下拉触发事件部分出现错误，请进行检查 \r\n')
    def store_id_list_get(self,date3,date4):
        if date3 != None or date3 != '' or date3 != '0':
            if date3 not in date4:  # 对读到的单号去重后放入列表get_contract_id_list
                date4.append(date3)  #
    def store_id_time_list_get(self,time1,time2,date1,date3):
        for i in range(len(date1)):
            if date1[i][0] == None or date1[i][0] == '' or date1[i][0] == '0':
                pass
            else:
                get_time_str = str(date1[i][0].strftime('%Y-%m-%d'))
                if get_time_str >= time1 and get_time_str <= time2:
                    if date1[i][1] != None or date1[i][1] != '' or date1[i][1] != '0':
                        if date1[i][1] not in date3:  # 对读到的单号去重后放入列表get_contract_id_list
                            date3.append(date1[i][1])  #
    #-----------------------------------------
    def store_id_click(self,event):
        self.getstring=event.GetString()
        # self.member_combox.SetValue('ALL')
        # self.Terminal_customer.SetValue('ALL')
        # self.time_deal()
        # self.TreeCtrl_Refresh(self.start_time, self.end_time)
    def search_button(self,event):
        pass
    #-----------------------------------------
    def member_information_display(self, evt):  # 订单号combobox下拉列表时触发的事件
        try:
            self.member_combox.Clear()
            self.member_combox.SetValue('ALL')
            # self.AllCancel(self)
            self.get_member_id_list=[]
            try:
                db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0],
                                     charset=charset)  # 打开数据库连接注charset是否需要
                cursor = db.cursor()  # 使用cursor()方法获取操作游标
                cursor.execute("SELECT `Contract_C_Time`,`Customer_name` FROM `order_contract_internal` WHERE 1 ")
                get_member_time= cursor.fetchall()  # 获取开始时间、合同号
                db.close()
            except:
                self.log.WriteText('生产进度管理，YLP_Pane.py中YLP_Contract_Order_Management_Panel连接数据库失败，请进行检查 \r\n')
            self.time_deal()
            if len(get_member_time)==0:
                pass
            else:
                if self.calendar_begin.GetValue() != "从" and self.calendar_end.GetValue() != "至":
                    # 转化开始时间格式函数为20180719   ##在获取合同号时读取时间范围内的合同号
                    if self.start_time > self.end_time:
                        self.log.WriteText( '生产进度管理，YLP_Pane.py中YLP_Contract_Order_Management_Panel类下单员查询时间范围有误，请进行检查 \r\n')
                    else:
                        self.store_id_time_list_get(self.start_time, self.end_time, get_member_time,self.get_member_id_list)
                elif self.calendar_begin.GetValue() != "从" and self.calendar_end.GetValue() == "至":  # 筛选大于某一个值
                    self.store_id_time_list_get(self.start_time, self.end_time, get_member_time,self.get_member_id_list)
                elif self.calendar_begin.GetValue() == "从" and self.calendar_end.GetValue() != "至":  # 筛选大于某一个值
                    self.store_id_time_list_get(self.start_time, self.end_time, get_member_time,self.get_member_id_list)
                else:  # 筛选大于某一个值
                    for i in range(len(get_member_time)):
                        self.store_id_list_get(get_member_time[i][1], self.get_member_id_list)
                if len(self.get_member_id_list) == 0:
                    self.log.WriteText('生产进度管理，YLP_Pane.py中YLP_Contract_Order_Management_Panel类下单员查询此时间范围无下单员，请进行检查 \r\n')
                else:
                    self.member_combox.Append('ALL')
                    for i in range(len(self.get_member_id_list)):
                        self.member_combox.Append(self.get_member_id_list[i])
            # self.Contract_refresh()
        except:
            self.log.WriteText('生产进度管理，YLP_Pane.py中YLP_Contract_Order_Management_Panel类下单员查询下拉触发事件部分出现错误，请进行检查 \r\n')
    def member_id_click(self,event):
        self.store_combox.SetValue('ALL')
        self.Terminal_customer.SetValue('ALL')
        self.time_deal()
        self.TreeCtrl_Refresh(self.start_time, self.end_time)
    def terminal_information_time_get(self,time1,time2,date1,date4):
        for i in range(len(date1)):
            if date1[i][0] == None or date1[i][0] == '' or date1[i][0] == '0':
                pass
            else:
                get_time_str = str(date1[i][0].strftime('%Y-%m-%d'))
                if get_time_str >= time1 and get_time_str <= time2:
                    if date1[i][1] != None or date1[i][1] != '' or date1[i][1] != '0':
                        if date1[i][1] not in date4:  # 对读到的单号去重后放入列表get_contract_id_list
                            date4.append(date1[i][1])  #
    def terminal_information_get(self,date3,date4):
        if date3 != None or date3 != '' or date3 != '0':
            if date3 not in date4:  # 对读到的单号去重后放入列表get_contract_id_list
                date4.append(date3)  #
    def Terminal_information_display(self, evt):  # 订单号combobox下拉列表时触发的事件
        try:
            self.Terminal_customer.Clear()
            self.Terminal_customer.SetValue('ALL')
            # self.AllCancel(self)
            self.get_terminal_customer_id_list=[]
            self.type = []
            try:
                db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0],
                                     charset=charset)  # 打开数据库连接注charset是否需要
                cursor = db.cursor()  # 使用cursor()方法获取操作游标
                cursor.execute("SELECT `Contract_C_Time`,`Customer_name` FROM `order_order_online` WHERE 1 ")
                get_terminal_customer_time= cursor.fetchall()  # 获取开始时间、合同号
                db.close()
            except:
                self.log.WriteText('生产进度管理，YLP_Pane.py中YLP_Contract_Order_Management_Panel连接数据库失败，请进行检查 \r\n')
            self.time_deal()
            if len(get_terminal_customer_time)==0:
                pass
            else:
                if self.calendar_begin.GetValue() != "从" and self.calendar_end.GetValue() != "至":
                    # 转化开始时间格式函数为20180719   ##在获取合同号时读取时间范围内的合同号
                    if self.start_time > self.end_time:
                        self.log.WriteText( '生产进度管理，YLP_Pane.py中YLP_Contract_Order_Management_Panel类终端客户查询时间范围有误，请进行检查 \r\n')
                    else:
                        self.terminal_information_time_get(self.start_time,self.end_time,get_terminal_customer_time,self.get_terminal_customer_id_list)
                elif self.calendar_begin.GetValue() != "从" and self.calendar_end.GetValue() == "至":  # 筛选大于某一个值
                    self.terminal_information_time_get(self.start_time, self.end_time, get_terminal_customer_time,self.get_terminal_customer_id_list)
                elif self.calendar_begin.GetValue() == "从" and self.calendar_end.GetValue() != "至":  # 筛选大于某一个值
                    self.terminal_information_time_get(self.start_time, self.end_time, get_terminal_customer_time,self.get_terminal_customer_id_list)
                else:  # 筛选大于某一个值
                    for i in range(len(get_terminal_customer_time)):
                        self.terminal_information_get(get_terminal_customer_time[i][1],self.get_terminal_customer_id_list)
                if len(self.get_terminal_customer_id_list) == 0:
                    self.log.WriteText('生产进度管理，YLP_Pane.py中YLP_Contract_Order_Management_Panel类终端客户查询此时间范围无终端客户，请进行检查 \r\n')
                else:
                    self.Terminal_customer.Append('ALL')
                    for i in range(len(self.get_terminal_customer_id_list)):
                        self.Terminal_customer.Append(self.get_terminal_customer_id_list[i])
        except:
            self.log.WriteText(
                '生产进度管理，YLP_Pane.py中YLP_Contract_Order_Management_Panel类终端客户查询下拉触发事件部分出现错误，请进行检查 \r\n')
        # self.Contract_refresh()
    def Terminal_id_click(self,event):
        self.store_combox.SetValue('ALL')
        self.member_combox.SetValue('ALL')
        self.time_deal()
        self.TreeCtrl_Refresh(self.start_time, self.end_time)
    def OnSize(self, event):
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.ylp_History_Element_Scrap)
        event.Skip()
    def OnQuit(self, event):
        self.Destroy()
    def OnToggleWindow(self, event):

        self._leftWindow1.Show(not self._leftWindow1.IsShown())
        # Leaves bits of itself behind sometimes
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.ylp_Show_Inform_Panel)
        self.ylp_Show_Inform_Panel.Refresh()

        event.Skip()
    def OnFoldPanelBarDrag(self, event):

        # if event.GetDragStatus() == wx.SASH_STATUS_OUT_OF_RANGE:
        #     return

        if event.GetId() == self.ID_WINDOW_LEFT1:
            self._leftWindow1.SetDefaultSize(wx.Size(event.GetDragRect().width, 1000))
        if event.GetId() == self.ID_WINDOW_RIGHT1:
            self._leftWindow2.SetDefaultSize(wx.Size(event.GetDragRect().width, 1000))
        # Leaves bits of itself behind sometimes
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.ylp_Show_Inform_Panel)
        # wx.adv.LayoutAlgorithm().LayoutWindow(self, self.ylp_Show_Inform_Panel)
        self.ylp_Show_Inform_Panel.Refresh()

        event.Skip()
    #-----------搜索面板--------------------------------
    def EvtCheckListBox(self,event):
        index = event.GetSelection()
        label = self.lb.GetString(index)
        status = 'False'
        if self.lb.IsChecked(index):
            status = 'True'
            self.label_list.append(label)
        else:
            self.label_list.remove(label)
        self.ylp_History_Element_Scrap.History_Show_ERROR_Part_Inform(self.label_list)
        #self.lb.SetSelection(index)
    def ReCreateFoldPanel(self, fpb_flags):

        self._leftWindow1.DestroyChildren()

        self._pnl = fpb.FoldPanelBar(self._leftWindow1, -1, wx.DefaultPosition,
                                     wx.Size(-1,-1), agwStyle=fpb_flags)

        Images = wx.ImageList(16,16)
        Images.Add(GetExpandedIconBitmap())
        Images.Add(GetCollapsedIconBitmap())
        item = self._pnl.AddFoldPanel("搜索", False, foldIcons=Images)
        self.statictext6 = wx.StaticText(item, -1, label="按报错工位搜索：")
        self._pnl.AddFoldPanelWindow(item, self.statictext6)


        sampleList = ['全部','半检工位','质检工位']

        self.lb = wx.CheckListBox(item, -1, (80, 50), wx.DefaultSize, sampleList)
        self.Bind(wx.EVT_CHECKLISTBOX, self.EvtCheckListBox, self.lb)
        self.lb.SetSelection(0)
        pos = self.lb.GetPosition().x + self.lb.GetSize().width + 25
        self._pnl.AddFoldPanelWindow(item, self.lb)

        # search = wx.Button(item, wx.ID_ANY, "搜索")
        # self._pnl.AddFoldPanelWindow(item, search)
        # search.Bind(wx.EVT_BUTTON, self.search_button)
        self._leftWindow1.SizeWindows()
    #----------------------------------------
    def onDateStart(self,event):
        self.date_start=self.calendar_begin.GetValue()
        self.date_end=self.calendar_end.GetValue()
        self.log.WriteText("天外天系统收到操作员控制指令，开始执行日期查询操作，起始日期："+str(self.date_start)+"，终止日期："+str(self.date_end)+"\r\n")
    def OnCreateBottomStyle(self, event):

        # recreate with style collapse to bottom, which means
        # all panels that are collapsed are placed at the bottom,
        # or normal

        if event.IsChecked():
            self.GetMenuBar().Check(self._singlestyle, False)
            self.GetMenuBar().Check(self._exclusivestyle, False)
            self._flags = self._flags & ~fpb.FPB_SINGLE_FOLD
            self._flags = self._flags & ~fpb.FPB_EXCLUSIVE_FOLD
            self._flags = self._flags | fpb.FPB_COLLAPSE_TO_BOTTOM
        else:
            self._flags = self._flags & ~fpb.FPB_COLLAPSE_TO_BOTTOM

        self.ReCreateFoldPanel(self._flags)
        #self.Create_TreeCtrl()
    def OnCreateNormalStyle(self, event):

        # recreate with style where only one panel at the time is
        # allowed to be opened

        if event.IsChecked():
            self.GetMenuBar().Check(self._bottomstyle, False)
            self.GetMenuBar().Check(self._exclusivestyle, False)
            self._flags = self._flags & ~fpb.FPB_EXCLUSIVE_FOLD
            self._flags = self._flags & ~fpb.FPB_COLLAPSE_TO_BOTTOM
            self._flags = self._flags | fpb.FPB_SINGLE_FOLD
        else:
            self._flags = self._flags & ~fpb.FPB_SINGLE_FOLD

        self.ReCreateFoldPanel(self._flags)
        #self.Create_TreeCtrl()
    def OnCreateExclusiveStyle(self, event):
        # recreate with style where only one panel at the time is
        # allowed to be opened and the others are collapsed to bottom
        if event.IsChecked():
            self.GetMenuBar().Check(self._singlestyle, False)
            self.GetMenuBar().Check(self._bottomstyle, False)
            self._flags = self._flags & ~fpb.FPB_SINGLE_FOLD
            self._flags = self._flags & ~fpb.FPB_COLLAPSE_TO_BOTTOM
            self._flags = self._flags | fpb.FPB_EXCLUSIVE_FOLD
        else:
            self._flags = self._flags & ~fpb.FPB_EXCLUSIVE_FOLD
        self.ReCreateFoldPanel(self._flags)
        #self.Create_TreeCtrl()
    def OnCollapseMe(self, event):
        for i in range(0, self._pnl.GetCount()):
            item = self._pnl.GetFoldPanel(i)
            self._pnl.Collapse(item)
    def OnExpandMe(self, event):
        style = fpb.CaptionBarStyle()
        counter = 0
        for items in self.radiocontrols:
            if items.GetValue():
                break
            counter = counter + 1
        if counter == 0:
            mystyle = fpb.CAPTIONBAR_GRADIENT_V
        elif counter == 1:
            mystyle = fpb.CAPTIONBAR_GRADIENT_H
        elif counter == 2:
            mystyle = fpb.CAPTIONBAR_SINGLE
        elif counter == 3:
            mystyle = fpb.CAPTIONBAR_RECTANGLE
        else:
            mystyle = fpb.CAPTIONBAR_FILLED_RECTANGLE

        # style.SetCaptionStyle(mystyle)
        # self._pnl.ApplyCaptionStyleAll(style)
    def OnSlideColour(self, event):

        col1 = wx.Colour(self._rslider1.GetValue(), self._gslider1.GetValue(),
                         self._bslider1.GetValue())
        col2 = wx.Colour(self._rslider2.GetValue(), self._gslider2.GetValue(),
                         self._bslider2.GetValue())

        style = fpb.CaptionBarStyle()

        counter = 0
        for items in self.radiocontrols:
            if items.GetValue():
                break

            counter = counter + 1

        if counter == 0:
            mystyle = fpb.CAPTIONBAR_GRADIENT_V
        elif counter == 1:
            mystyle = fpb.CAPTIONBAR_GRADIENT_H
        elif counter == 2:
            mystyle = fpb.CAPTIONBAR_SINGLE
        elif counter == 3:
            mystyle = fpb.CAPTIONBAR_RECTANGLE
        else:
            mystyle = fpb.CAPTIONBAR_FILLED_RECTANGLE

        style.SetFirstColour(col1)
        style.SetSecondColour(col2)
        style.SetCaptionStyle(mystyle)

        item = self._pnl.GetFoldPanel(0)
        self._pnl.ApplyCaptionStyle(item, style)
    def OnStyleChange(self, event):

        style = fpb.CaptionBarStyle()

        eventid = event.GetId()

        if eventid == self.ID_USE_HGRADIENT:
            style.SetCaptionStyle(fpb.CAPTIONBAR_GRADIENT_H)

        elif eventid == self.ID_USE_VGRADIENT:
            style.SetCaptionStyle(fpb.CAPTIONBAR_GRADIENT_V)

        elif eventid == self.ID_USE_SINGLE:
            style.SetCaptionStyle(fpb.CAPTIONBAR_SINGLE)

        elif eventid == self.ID_USE_RECTANGLE:
            style.SetCaptionStyle(fpb.CAPTIONBAR_RECTANGLE)

        elif eventid == self.ID_USE_FILLED_RECTANGLE:
            style.SetCaptionStyle(fpb.CAPTIONBAR_FILLED_RECTANGLE)

        else:
            raise "ERROR: Undefined Style Selected For CaptionBar: " + repr(eventid)

        col1 = wx.Colour(self._rslider1.GetValue(), self._gslider1.GetValue(),
                         self._bslider1.GetValue())
        col2 = wx.Colour(self._rslider2.GetValue(), self._gslider2.GetValue(),
                         self._bslider2.GetValue())

        style.SetFirstColour(col1)
        style.SetSecondColour(col2)

        if self._single.GetValue():
            item = self._pnl.GetFoldPanel(1)
            self._pnl.ApplyCaptionStyle(item, style)
        else:
            self._pnl.ApplyCaptionStyleAll(style)
    def CreateMenuBar(self, with_window=False):

        # Make a menubar
        file_menu = wx.Menu()

        FPBTEST_QUIT = wx.NewId()
        FPBTEST_REFRESH = wx.NewId()
        FPB_BOTTOM_FOLD = wx.NewId()
        FPB_SINGLE_FOLD = wx.NewId()
        FPB_EXCLUSIVE_FOLD = wx.NewId()
        FPBTEST_TOGGLE_WINDOW = wx.NewId()
        FPBTEST_ABOUT = wx.NewId()

        file_menu.Append(FPBTEST_QUIT, "&Exit")

        option_menu = None

        if with_window:
            # Dummy option
            option_menu = wx.Menu()
            option_menu.Append(FPBTEST_REFRESH, "&Refresh picture")

        # make fold panel menu

        fpb_menu = wx.Menu()
        fpb_menu.AppendCheckItem(FPB_BOTTOM_FOLD, "Create with &fpb.FPB_COLLAPSE_TO_BOTTOM")

        # Now Implemented!
        fpb_menu.AppendCheckItem(FPB_SINGLE_FOLD, "Create with &fpb.FPB_SINGLE_FOLD")

        # Now Implemented!
        fpb_menu.AppendCheckItem(FPB_EXCLUSIVE_FOLD, "Create with &fpb.FPB_EXCLUSIVE_FOLD")

        fpb_menu.AppendSeparator()
        fpb_menu.Append(FPBTEST_TOGGLE_WINDOW, "&Toggle FoldPanelBar")

        help_menu = wx.Menu()
        help_menu.Append(FPBTEST_ABOUT, "&About")

        menu_bar = wx.MenuBar()

        menu_bar.Append(file_menu, "&File")
        menu_bar.Append(fpb_menu, "&FoldPanel")

        if option_menu:
            menu_bar.Append(option_menu, "&Options")

        menu_bar.Append(help_menu, "&Help")

        self.Bind(wx.EVT_MENU, self.OnAbout, id=FPBTEST_ABOUT)
        self.Bind(wx.EVT_MENU, self.OnQuit, id=FPBTEST_QUIT)
        self.Bind(wx.EVT_MENU, self.OnToggleWindow, id=FPBTEST_TOGGLE_WINDOW)
        self.Bind(wx.EVT_MENU, self.OnCreateBottomStyle, id=FPB_BOTTOM_FOLD)
        self.Bind(wx.EVT_MENU, self.OnCreateNormalStyle, id=FPB_SINGLE_FOLD)
        self.Bind(wx.EVT_MENU, self.OnCreateExclusiveStyle, id=FPB_EXCLUSIVE_FOLD)

        self._bottomstyle = FPB_BOTTOM_FOLD
        self._singlestyle = FPB_SINGLE_FOLD
        self._exclusivestyle = FPB_EXCLUSIVE_FOLD

        return menu_bar

#****************财务管理*******************************************************
from wx.lib import plot as wxplot
import numpy as np

class Finance_Management_Grid(gridlib.Grid):
    def __init__(self, parent):
        gridlib.Grid.__init__(self, parent, -1)
        self.CreateGrid(1, 12)
        self.field_name = ['1月', '2月', '3月', '4月', '5月','6月', '7月','8月', '9月', '10月', '11月', '12月']
        for i in range(len(self.field_name)):
            self.SetColLabelValue(i, self.field_name[i])
        self.Show_Income_Grid('全部')
        self.AutoSize()
    def Show_Income_Grid(self,search_years):
        try:
            self.data = []
            new_staff_inform=[]
            global years
            years=[]
            if Is_Database_Connect_Cloud():
                cursor = DB_cloud.cursor()
                self.year_income_list=[]
                cursor.execute("select `Operate_time` from `finance_log` where 1")
                operate_time=cursor.fetchall()
                if operate_time!=() and operate_time is not None:
                    for i in range(len(operate_time)):
                        years.append(operate_time[i][0].strftime('%Y'))
                    years=list(set(years))

                    month_12 = ['-1-1', '-2-1', '-3-1', '-4-1', '-5-1', '-6-1', '-7-1',
                                '-8-1', '-9-1', '-10-1', '-11-1', '-12-1']
                    # current_month=time.strftime('%Y-%m-%d', time.localtime(time.time()))
                    if search_years=='全部':
                        global dict_yesrs_income
                        dict_yesrs_income = {}      #新建一个字典，用于存储每年的每个月的收入，以‘年’为字典的键，以‘每个月收入总和列表’为字典的值。字典的初始化最好放在这个位置。
                        #self.dict_yesrs_income = {}      #新建一个字典，用于存储每年的每个月的收入，以‘年’为字典的键，以‘每个月收入总和列表’为字典的值。字典的初始化最好放在这个位置。
                        for i1 in range(len(years)):
                            for i in range(len(month_12)):
                                monthly_income = 0
                                cursor.execute(
                                    "select `Payment_amount` from `finance_log` where DATE_FORMAT(`Operate_time`, '%%Y%%m')=DATE_FORMAT(('%s'), '%%Y%%m') " %
                                    (years[i1] + month_12[i]))
                                part_staff_inform = cursor.fetchall()
                                if part_staff_inform != () and part_staff_inform is not None:
                                    for j in range(len(part_staff_inform)):
                                        monthly_income += part_staff_inform[j][0]
                                    monthly_income=monthly_income/100
                                    self.year_income_list.append(monthly_income)
                                else:
                                    self.year_income_list.append(0)
                            self.data.append(self.year_income_list)
                            dict_yesrs_income[years[i1]]=self.year_income_list

                    else:
                        self.data.append(dict_yesrs_income[search_years])
                else:
                    pass
            now_rows = self.GetNumberRows()
            if len(self.data) > now_rows:
                for i in range(len(self.data) - now_rows):
                    self.AppendRows(numRows=1)
            if len(self.data) < now_rows:
                for i in range(now_rows - len(self.data)):
                    self.DeleteRows(numRows=1)

            if (len(self.data) != 0):
                for i in range(len(self.field_name)):  # 用来填写所有表头信息
                    self.SetColLabelValue(i, self.field_name[i])
                self.SetColLabelAlignment(wx.ALIGN_LEFT, wx.ALIGN_BOTTOM)
                for i in range(len(self.data)):  # 填数据
                    self.SetRowLabelValue(0, years[i])
                    for j in range(len(self.data[i])):
                        self.SetCellValue(i, j, str(self.data[i][j]))
            else:
                self.CreateGrid(1, 12)
                self.field_name = ['1月', '2月', '3月', '4月', '5月','6月', '7月','8月', '9月', '10月', '11月', '12月']
                for i in range(len(self.field_name)):  # 用来填写所有表头信息
                    self.SetColLabelValue(i, self.field_name[i])
                #self.SetRowLabelValue(0, '2018')
            self.AutoSize()
        except:
            pass
    def Show_Income_BarGraph(self,search_years):
        name_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        num_list=dict_yesrs_income[search_years]
        plt.bar(range(len(num_list)), num_list, color='rgb', tick_label=name_list)
        plt.savefig("barChart.jpg")
        plt.show()
    def Show_Income_LineChart(self,search_years):
        x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        y = dict_yesrs_income[search_years]
        plt.figure(figsize=(8, 4))
        plt.plot(x, y, "b--", linewidth=1)
        plt.xlabel("Time(s)")
        plt.ylabel("Volt")
        plt.title("Line plot")
        plt.show()
        plt.savefig("line.jpg")
class Finance_Draw_Panel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition,
                          wx.DefaultSize, style=wx.SUNKEN_BORDER)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.dra=wxplot.PlotCanvas(self)
        hbox.Add(self.dra, proportion=1, flag=wx.EXPAND | wx.ALL, border=3)
        self.SetSizer(hbox)
        #self.dra.Draw(self._draw10Objects('2018'))
    def Refresh(self,search_years):
        self.dra.Draw(self._draw10Objects(search_years))
    def _draw10Objects(self,search_years):
        bar_height = np.array(dict_yesrs_income[search_years])
        bar_location = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
        self.dra.xSpec=11
        data = list(zip(bar_location, bar_height))
        bars = [wxplot.PolyBars(data)]
        return wxplot.PlotGraphics(bars)
class Show_Finance_Inform_Panel(wx.Panel):
    def __init__(self, parent,log):
        wx.Panel.__init__(self, parent, -1,)
        self.log=log
        # self.ctrl = aui.AuiNotebook(self)
        bookStyle = FNB.FNB_NODRAG
        self.AutoScroll=True
        self.ctrl = FNB.FlatNotebook(self, wx.ID_ANY, agwStyle=bookStyle)

        # self.ylp_Order_Inform_PDF=Order_Inform_PDF(self,self.log)
        # self.ctrl.AddPage(self.ylp_Order_Inform_PDF, "订单")

        self.ylp_finance_management_grid = Finance_Management_Grid(self)
        self.ctrl.AddPage(self.ylp_finance_management_grid, "图表")

        self.ylp_Finance_Draw_Panel=Finance_Draw_Panel(self)
        self.ctrl.AddPage(self.ylp_Finance_Draw_Panel, "画图")
        bookStyle |= FNB.FNB_HIDE_TABS
        self.ctrl.SetAGWWindowStyleFlag(bookStyle)
        sizer = wx.BoxSizer()
        sizer.Add(self.ctrl, 1, wx.EXPAND | wx.ALL)
        self.SetSizer(sizer)
        wx.CallAfter(self.ctrl.SendSizeEvent)
    # def PDF_Page(self,order_inform,sec_inform):
    #     self.ctrl.SetSelection(0)
    #     self.ylp_Order_Inform_PDF.DrawTable_PDF(order_inform,sec_inform)
    def Gride_Page(self,value):
        self.ctrl.SetSelection(0)
        #if isinstance(value, int):  # 判断是否为整数
        if value[0]==1:
            self.ctrl.SetSelection(0)
            self.ylp_finance_management_grid.Show_Income_Grid(value[1])
        if value[0]==2:
            #self.Draw_Bar_Chart()
            self.ctrl.SetSelection(0)
            if value[1]=='全部':
                search_years=current_year
            else:
                search_years = value[1]

            self.Draw_Bar_Chart(search_years)
            # self.ylp_finance_management_grid.Show_Income_BarGraph(search_years)
        if value[0] == 3:
            self.ctrl.SetSelection(0)
            if value[1]=='全部':
                search_years=current_year
            else:
                search_years = value[1]

            self.Draw_Bar_Chart(search_years)
            # self.ylp_finance_management_grid.Show_Income_LineChart(search_years)

        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.ylp_finance_management_grid)
    # def Show_Part_Inform(self,part_inform,part_information):
    #     self.ctrl.SetSelection(2)
    #     # self.ylp_Part_ID_Inform_Panel.Show_Part_Inform(part_information)#直接放grid可实现
    #     self.ylp_Part_ID_Inform_Panel.Part_OnPaint(part_inform)
    #     self.ylp_Part_ID_Inform_Panel.panel.grid.Show_Part_Inform(part_information)
    #     wx.adv.LayoutAlgorithm().LayoutWindow(self.ylp_Part_ID_Inform_Panel.panel, self.ylp_Part_ID_Inform_Panel.panel.grid)
    # def Show_ID_Inform(self,ID_inform):
    #     self.ctrl.SetSelection(2)
    #     self.ylp_Part_ID_Inform_Panel.ID_OnPaint(ID_inform)
    def Draw_Bar_Chart(self,search_years):
        self.ctrl.SetSelection(1)
        self.ylp_Finance_Draw_Panel.Refresh(search_years)
class YLP_Finance_Management_Panel(wx.Panel):
    def __init__(self, parent,log, id=wx.ID_ANY, title="", pos=wx.DefaultPosition,
                 size=(700,650), style=wx.DEFAULT_FRAME_STYLE):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.select_code = 0
        self._flags = 0
        self.log = log
        self.label_list=[]
        global current_year
        current_year=time.strftime('%Y', time.localtime(time.time()))
        self._leftWindow1 = wx.adv.SashLayoutWindow(self, 101, wx.DefaultPosition,
                                                wx.Size(200, 1000), wx.NO_BORDER |
                                                wx.adv.SW_3D | wx.CLIP_CHILDREN)
        self._leftWindow1.SetDefaultSize(wx.Size(220, 1000))
        self._leftWindow1.SetOrientation(wx.adv.LAYOUT_VERTICAL)
        self._leftWindow1.SetAlignment(wx.adv.LAYOUT_LEFT)
        self._leftWindow1.SetSashVisible(wx.adv.SASH_RIGHT, True)
        self._leftWindow1.SetExtraBorderSize(10)
        self._pnl = 0
        self.ylp_show_finance_inform_panel=Show_Finance_Inform_Panel(self,self.log)

        self.ID_WINDOW_LEFT1 = 101
        self.ID_WINDOW_RIGHT1 = 102
        self._leftWindow1.Bind(wx.adv.EVT_SASH_DRAGGED_RANGE, self.OnFoldPanelBarDrag,
                               id=101, id2=102)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        self.Bind(wx.EVT_SCROLL, self.OnSlideColour)
        self.ReCreateFoldPanel(0)
    def Get_Seek_DateTime(self,event):
        self.time_deal()
        self.TreeCtrl_Refresh(self.start_time,self.end_time)
        # date_start = self.calendar_begin.GetValue()
        # date_end = self.calendar_end.GetValue()
       #  if "从" in date_start or "至"in date_end :
       #      self.TreeCtrl_Refresh(0,0)
       #  else:
       #      if '/' in date_start:
       #          date_start=date_start.split("/")
       #          date_end = date_end.split("/")
       #          date_start=date_start[2],date_start[1],date_start[0]
       #          date_end=date_end[2],date_end[1],date_end[0]
       #          st='-'
       #          date_start = st.join(date_start)
       #          date_end = st.join(date_end)
       #      self.TreeCtrl_Refresh(date_start,date_end)
       #
       # # wx.adv.LayoutAlgorithm().LayoutWindow(self._leftWindow2,self.tree)
    def time_clear(self,event):
        self.calendar_begin.textCtrl.SetValue('从')
        self.calendar_end.textCtrl.SetValue('至')
        self.store_combox.SetValue('ALL')
        self.member_combox.SetValue('ALL')
        self.Terminal_customer.SetValue('ALL')
        self.time_deal()
        self.TreeCtrl_Refresh(self.start_time, self.end_time)
    def time_deal(self):
        try:
            begin_time = self.calendar_begin.GetValue()  # 获得开始时间
            end_time = self.calendar_end.GetValue()
            if begin_time != "从":
                t2 = str(begin_time).split('/')
                t3 = t2[2], t2[1], t2[0]
                st = '-'
                self.start_time = st.join(t3)
            else:
                self.start_time='1900-01-01'
            # 转化截止时间格式函数为20180719
            if end_time != "至":
                t2_1 = str(end_time).split('/')
                t3_1 = t2_1[2], t2_1[1], t2_1[0]
                st_1 = '-'
                self.end_time = st_1.join(t3_1)
            else:
                now_time = str(time.strftime('%Y-%m-%d', time.localtime()))  # 本地当前时间
                self.end_time=now_time
            if begin_time == "从" and end_time != "至":
                self.start_time='1900-01-10 00:00:00'
        except:
            pass
    def store_information_display(self, evt):  # 合同号combobox下拉列表时触发的事件
        try:
            self.store_combox.Clear()
            self.store_combox.SetValue('ALL')
            # self.AllCancel(self)
            self.get_store_id_list=[]
            self.type = []
            try:
                db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0],
                                     charset=charset)  # 打开数据库连接注charset是否需要
                cursor = db.cursor()  # 使用cursor()方法获取操作游标
                cursor.execute("SELECT `Contract_C_Time`,`Dealer` FROM `order_contract_internal` WHERE 1 ")
                get_store_time= cursor.fetchall()  # 获取开始时间、合同号
                db.close()
            except:
                self.log.WriteText('生产进度管理，YLP_Pane.py中YLP_Contract_Order_Management_Panel连接数据库失败，请进行检查 \r\n')
            self.time_deal()
            if len(get_store_time)==0:
                # print '未查询到合同号'
                pass
            else:
                if self.calendar_begin.GetValue() != "从" and self.calendar_end.GetValue() != "至":
                    # 转化开始时间格式函数为20180719   ##在获取合同号时读取时间范围内的合同号
                    if self.start_time > self.end_time:
                        self.log.WriteText( '生产进度管理，YLP_Pane.py中YLP_Contract_Order_Management_Panel类门店查询时间范围有误，请进行检查 \r\n')
                    else:
                        self.store_id_time_list_get(self.start_time,self.end_time,get_store_time,self.get_store_id_list)
                elif self.calendar_begin.GetValue() != "从" and self.calendar_end.GetValue() == "至":  # 筛选大于某一个值
                    self.store_id_time_list_get(self.start_time, self.end_time, get_store_time, self.get_store_id_list)
                elif self.calendar_begin.GetValue() == "从" and self.calendar_end.GetValue() != "至":  # 筛选大于某一个值
                    self.store_id_time_list_get(self.start_time, self.end_time, get_store_time, self.get_store_id_list)
                else:  # 筛选大于某一个值
                    for i in range(len(get_store_time)):
                        self.store_id_list_get(get_store_time[i][1], self.get_store_id_list)
                if len(self.get_store_id_list) == 0:
                    self.log.WriteText('生产进度管理，YLP_Pane.py中YLP_Contract_Order_Management_Panel类门店查询此时间范围无门店号，请进行检查 \r\n')
                else:
                    self.store_combox.Append('ALL')
                    for i in range(len(self.get_store_id_list)):
                        self.store_combox.Append(self.get_store_id_list[i])
            # self.Refresh()
        except:
            self.log.WriteText('生产进度管理，YLP_Pane.py中YLP_Contract_Order_Management_Panel类门店查询下拉触发事件部分出现错误，请进行检查 \r\n')
    def store_id_list_get(self,date3,date4):
        if date3 != None or date3 != '' or date3 != '0':
            if date3 not in date4:  # 对读到的单号去重后放入列表get_contract_id_list
                date4.append(date3)  #
    def store_id_time_list_get(self,time1,time2,date1,date3):
        for i in range(len(date1)):
            if date1[i][0] == None or date1[i][0] == '' or date1[i][0] == '0':
                pass
            else:
                get_time_str = str(date1[i][0].strftime('%Y-%m-%d'))
                if get_time_str >= time1 and get_time_str <= time2:
                    if date1[i][1] != None or date1[i][1] != '' or date1[i][1] != '0':
                        if date1[i][1] not in date3:  # 对读到的单号去重后放入列表get_contract_id_list
                            date3.append(date1[i][1])  #
    #-----------------------------------------
    def store_id_click(self,event):
        self.getstring=event.GetString()
        # self.member_combox.SetValue('ALL')
        # self.Terminal_customer.SetValue('ALL')
        # self.time_deal()
        # self.TreeCtrl_Refresh(self.start_time, self.end_time)
    def search_button(self,event):
        pass
    #-----------------------------------------
    def member_information_display(self, evt):  # 订单号combobox下拉列表时触发的事件
        try:
            self.member_combox.Clear()
            self.member_combox.SetValue('ALL')
            # self.AllCancel(self)
            self.get_member_id_list=[]
            try:
                db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0],
                                     charset=charset)  # 打开数据库连接注charset是否需要
                cursor = db.cursor()  # 使用cursor()方法获取操作游标
                cursor.execute("SELECT `Contract_C_Time`,`Customer_name` FROM `order_contract_internal` WHERE 1 ")
                get_member_time= cursor.fetchall()  # 获取开始时间、合同号
                db.close()
            except:
                self.log.WriteText('生产进度管理，YLP_Pane.py中YLP_Contract_Order_Management_Panel连接数据库失败，请进行检查 \r\n')
            self.time_deal()
            if len(get_member_time)==0:
                pass
            else:
                if self.calendar_begin.GetValue() != "从" and self.calendar_end.GetValue() != "至":
                    # 转化开始时间格式函数为20180719   ##在获取合同号时读取时间范围内的合同号
                    if self.start_time > self.end_time:
                        self.log.WriteText( '生产进度管理，YLP_Pane.py中YLP_Contract_Order_Management_Panel类下单员查询时间范围有误，请进行检查 \r\n')
                    else:
                        self.store_id_time_list_get(self.start_time, self.end_time, get_member_time,self.get_member_id_list)
                elif self.calendar_begin.GetValue() != "从" and self.calendar_end.GetValue() == "至":  # 筛选大于某一个值
                    self.store_id_time_list_get(self.start_time, self.end_time, get_member_time,self.get_member_id_list)
                elif self.calendar_begin.GetValue() == "从" and self.calendar_end.GetValue() != "至":  # 筛选大于某一个值
                    self.store_id_time_list_get(self.start_time, self.end_time, get_member_time,self.get_member_id_list)
                else:  # 筛选大于某一个值
                    for i in range(len(get_member_time)):
                        self.store_id_list_get(get_member_time[i][1], self.get_member_id_list)
                if len(self.get_member_id_list) == 0:
                    self.log.WriteText('生产进度管理，YLP_Pane.py中YLP_Contract_Order_Management_Panel类下单员查询此时间范围无下单员，请进行检查 \r\n')
                else:
                    self.member_combox.Append('ALL')
                    for i in range(len(self.get_member_id_list)):
                        self.member_combox.Append(self.get_member_id_list[i])
            # self.Contract_refresh()
        except:
            self.log.WriteText('生产进度管理，YLP_Pane.py中YLP_Contract_Order_Management_Panel类下单员查询下拉触发事件部分出现错误，请进行检查 \r\n')
    def member_id_click(self,event):
        self.store_combox.SetValue('ALL')
        self.Terminal_customer.SetValue('ALL')
        self.time_deal()
        self.TreeCtrl_Refresh(self.start_time, self.end_time)
    def terminal_information_time_get(self,time1,time2,date1,date4):
        for i in range(len(date1)):
            if date1[i][0] == None or date1[i][0] == '' or date1[i][0] == '0':
                pass
            else:
                get_time_str = str(date1[i][0].strftime('%Y-%m-%d'))
                if get_time_str >= time1 and get_time_str <= time2:
                    if date1[i][1] != None or date1[i][1] != '' or date1[i][1] != '0':
                        if date1[i][1] not in date4:  # 对读到的单号去重后放入列表get_contract_id_list
                            date4.append(date1[i][1])  #
    def terminal_information_get(self,date3,date4):
        if date3 != None or date3 != '' or date3 != '0':
            if date3 not in date4:  # 对读到的单号去重后放入列表get_contract_id_list
                date4.append(date3)  #
    def Terminal_information_display(self, evt):  # 订单号combobox下拉列表时触发的事件
        try:
            self.Terminal_customer.Clear()
            self.Terminal_customer.SetValue('ALL')
            # self.AllCancel(self)
            self.get_terminal_customer_id_list=[]
            self.type = []
            try:
                db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0],
                                     charset=charset)  # 打开数据库连接注charset是否需要
                cursor = db.cursor()  # 使用cursor()方法获取操作游标
                cursor.execute("SELECT `Contract_C_Time`,`Customer_name` FROM `order_order_online` WHERE 1 ")
                get_terminal_customer_time= cursor.fetchall()  # 获取开始时间、合同号
                db.close()
            except:
                self.log.WriteText('生产进度管理，YLP_Pane.py中YLP_Contract_Order_Management_Panel连接数据库失败，请进行检查 \r\n')
            self.time_deal()
            if len(get_terminal_customer_time)==0:
                pass
            else:
                if self.calendar_begin.GetValue() != "从" and self.calendar_end.GetValue() != "至":
                    # 转化开始时间格式函数为20180719   ##在获取合同号时读取时间范围内的合同号
                    if self.start_time > self.end_time:
                        self.log.WriteText( '生产进度管理，YLP_Pane.py中YLP_Contract_Order_Management_Panel类终端客户查询时间范围有误，请进行检查 \r\n')
                    else:
                        self.terminal_information_time_get(self.start_time,self.end_time,get_terminal_customer_time,self.get_terminal_customer_id_list)
                elif self.calendar_begin.GetValue() != "从" and self.calendar_end.GetValue() == "至":  # 筛选大于某一个值
                    self.terminal_information_time_get(self.start_time, self.end_time, get_terminal_customer_time,self.get_terminal_customer_id_list)
                elif self.calendar_begin.GetValue() == "从" and self.calendar_end.GetValue() != "至":  # 筛选大于某一个值
                    self.terminal_information_time_get(self.start_time, self.end_time, get_terminal_customer_time,self.get_terminal_customer_id_list)
                else:  # 筛选大于某一个值
                    for i in range(len(get_terminal_customer_time)):
                        self.terminal_information_get(get_terminal_customer_time[i][1],self.get_terminal_customer_id_list)
                if len(self.get_terminal_customer_id_list) == 0:
                    self.log.WriteText('生产进度管理，YLP_Pane.py中YLP_Contract_Order_Management_Panel类终端客户查询此时间范围无终端客户，请进行检查 \r\n')
                else:
                    self.Terminal_customer.Append('ALL')
                    for i in range(len(self.get_terminal_customer_id_list)):
                        self.Terminal_customer.Append(self.get_terminal_customer_id_list[i])
        except:
            self.log.WriteText(
                '生产进度管理，YLP_Pane.py中YLP_Contract_Order_Management_Panel类终端客户查询下拉触发事件部分出现错误，请进行检查 \r\n')
        # self.Contract_refresh()
    def Terminal_id_click(self,event):
        self.store_combox.SetValue('ALL')
        self.member_combox.SetValue('ALL')
        self.time_deal()
        self.TreeCtrl_Refresh(self.start_time, self.end_time)
    def OnSize(self, event):
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.ylp_show_finance_inform_panel)
        event.Skip()
    def OnQuit(self, event):
        self.Destroy()
    def OnToggleWindow(self, event):

        self._leftWindow1.Show(not self._leftWindow1.IsShown())
        # Leaves bits of itself behind sometimes
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.ylp_show_finance_inform_panel)
        self.ylp_show_finance_inform_panel.Refresh()

        event.Skip()
    def OnFoldPanelBarDrag(self, event):

        # if event.GetDragStatus() == wx.SASH_STATUS_OUT_OF_RANGE:
        #     return

        if event.GetId() == self.ID_WINDOW_LEFT1:
            self._leftWindow1.SetDefaultSize(wx.Size(event.GetDragRect().width, 1000))
        if event.GetId() == self.ID_WINDOW_RIGHT1:
            self._leftWindow2.SetDefaultSize(wx.Size(event.GetDragRect().width, 1000))
        # # Leaves bits of itself behind sometimes
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.ylp_show_finance_inform_panel)
        # # wx.adv.LayoutAlgorithm().LayoutWindow(self, self.ylp_Show_Inform_Panel)
        self.ylp_show_finance_inform_panel.Refresh()

        event.Skip()
    #-------------------------------------------
    def EvtCheckListBox(self,event):
        index = event.GetSelection()
        label = self.lb.GetString(index)
        status = 'False'
        if self.lb.IsChecked(index):
            status = 'True'
            self.label_list.append(label)
        else:
            self.label_list.remove(label)
        self.ylp_Staff_Inform_Management_Grid.Show_Part_Inform(self.label_list)
        #self.lb.SetSelection(index)

    def ReCreateFoldPanel(self, fpb_flags):
        self._leftWindow1.DestroyChildren()

        self._pnl = fpb.FoldPanelBar(self._leftWindow1, -1, wx.DefaultPosition,
                                     wx.Size(-1,-1), agwStyle=fpb_flags)

        Images = wx.ImageList(16,16)
        Images.Add(GetExpandedIconBitmap())
        Images.Add(GetCollapsedIconBitmap())
        item = self._pnl.AddFoldPanel("搜索", False, foldIcons=Images)
        self.statictext6 = wx.StaticText(item, -1, label="显示方式：")
        self._pnl.AddFoldPanelWindow(item, self.statictext6)

        self.display_year=[1,current_year]
        sampleList1 = ['图表','柱状图', '点线图']
        self.display = wx.ComboBox(item, 500, "图表", (90, 50),(160, -1), sampleList1,wx.CB_DROPDOWN)
        self._pnl.AddFoldPanelWindow(item, self.display)
        self.Bind(wx.EVT_TEXT, self.EvtText, self.display)

        self.statictext7 = wx.StaticText(item, -1, label="查找年份：")
        self._pnl.AddFoldPanelWindow(item, self.statictext7)
        #sampleList2 = ['全部','2018']
        sampleList2 = years
        if '全部' in sampleList2:
            pass
        else:
            sampleList2.append('全部')
        self.display1 = wx.ComboBox(item, 500, current_year, (90, 50), (160, -1), sampleList2, wx.CB_DROPDOWN)
        self._pnl.AddFoldPanelWindow(item, self.display1)
        # self.Bind(wx.EVT_TEXT, self.EvtText1, self.display1)
        #self.Bind(wx.EVT_COMBOBOX, self.EvtText1, self.display1)
        # self.employee_combox = wx.ComboBox(item, -1, pos=(20, 10), style=wx.CB_DROPDOWN)
        # self._pnl.AddFoldPanelWindow(item, self.employee_combox)
        # self.employee_combox.SetValue('None')



        # search = wx.Button(item, wx.ID_ANY, "搜索")
        # self._pnl.AddFoldPanelWindow(item, search)
        # search.Bind(wx.EVT_BUTTON, self.search_button)
        self._leftWindow1.SizeWindows()
    def EvtText(self,evt):
        if evt.GetString()=='图表':
            self.display_year[0]=1
            # self.ylp_show_finance_inform_panel.Gride_Page(1)
        elif evt.GetString()=='柱状图':
            self.display_year[0] = 2
            # self.ylp_show_finance_inform_panel.Gride_Page(2)
        elif evt.GetString()=='点线图':
            self.display_year[0] = 3
            # self.ylp_show_finance_inform_panel.Gride_Page(3)
        else:
            self.display_year[1] = evt.GetString()
        self.ylp_show_finance_inform_panel.Gride_Page(self.display_year)
        evt.Skip()
    # def EvtText1(self,evt):
    #     print 'wo',evt.GetString()
    #     self.display_year[1] = evt.GetString()
    #     self.ylp_show_finance_inform_panel.Gride_Page(self.display_year)
    #     evt.Skip()

    #----------------------------------------
    def onDateStart(self,event):
        self.date_start=self.calendar_begin.GetValue()
        self.date_end=self.calendar_end.GetValue()
        self.log.WriteText("天外天系统收到操作员控制指令，开始执行日期查询操作，起始日期："+str(self.date_start)+"，终止日期："+str(self.date_end)+"\r\n")
    def OnCreateBottomStyle(self, event):

        # recreate with style collapse to bottom, which means
        # all panels that are collapsed are placed at the bottom,
        # or normal

        if event.IsChecked():
            self.GetMenuBar().Check(self._singlestyle, False)
            self.GetMenuBar().Check(self._exclusivestyle, False)
            self._flags = self._flags & ~fpb.FPB_SINGLE_FOLD
            self._flags = self._flags & ~fpb.FPB_EXCLUSIVE_FOLD
            self._flags = self._flags | fpb.FPB_COLLAPSE_TO_BOTTOM
        else:
            self._flags = self._flags & ~fpb.FPB_COLLAPSE_TO_BOTTOM

        self.ReCreateFoldPanel(self._flags)
        #self.Create_TreeCtrl()
    def OnCreateNormalStyle(self, event):

        # recreate with style where only one panel at the time is
        # allowed to be opened

        if event.IsChecked():
            self.GetMenuBar().Check(self._bottomstyle, False)
            self.GetMenuBar().Check(self._exclusivestyle, False)
            self._flags = self._flags & ~fpb.FPB_EXCLUSIVE_FOLD
            self._flags = self._flags & ~fpb.FPB_COLLAPSE_TO_BOTTOM
            self._flags = self._flags | fpb.FPB_SINGLE_FOLD
        else:
            self._flags = self._flags & ~fpb.FPB_SINGLE_FOLD

        self.ReCreateFoldPanel(self._flags)
        #self.Create_TreeCtrl()
    def OnCreateExclusiveStyle(self, event):
        # recreate with style where only one panel at the time is
        # allowed to be opened and the others are collapsed to bottom
        if event.IsChecked():
            self.GetMenuBar().Check(self._singlestyle, False)
            self.GetMenuBar().Check(self._bottomstyle, False)
            self._flags = self._flags & ~fpb.FPB_SINGLE_FOLD
            self._flags = self._flags & ~fpb.FPB_COLLAPSE_TO_BOTTOM
            self._flags = self._flags | fpb.FPB_EXCLUSIVE_FOLD
        else:
            self._flags = self._flags & ~fpb.FPB_EXCLUSIVE_FOLD
        self.ReCreateFoldPanel(self._flags)
        #self.Create_TreeCtrl()
    def OnCollapseMe(self, event):
        for i in range(0, self._pnl.GetCount()):
            item = self._pnl.GetFoldPanel(i)
            self._pnl.Collapse(item)
    def OnExpandMe(self, event):
        style = fpb.CaptionBarStyle()
        counter = 0
        for items in self.radiocontrols:
            if items.GetValue():
                break
            counter = counter + 1
        if counter == 0:
            mystyle = fpb.CAPTIONBAR_GRADIENT_V
        elif counter == 1:
            mystyle = fpb.CAPTIONBAR_GRADIENT_H
        elif counter == 2:
            mystyle = fpb.CAPTIONBAR_SINGLE
        elif counter == 3:
            mystyle = fpb.CAPTIONBAR_RECTANGLE
        else:
            mystyle = fpb.CAPTIONBAR_FILLED_RECTANGLE

        # style.SetCaptionStyle(mystyle)
        # self._pnl.ApplyCaptionStyleAll(style)
    def OnSlideColour(self, event):

        col1 = wx.Colour(self._rslider1.GetValue(), self._gslider1.GetValue(),
                         self._bslider1.GetValue())
        col2 = wx.Colour(self._rslider2.GetValue(), self._gslider2.GetValue(),
                         self._bslider2.GetValue())

        style = fpb.CaptionBarStyle()

        counter = 0
        for items in self.radiocontrols:
            if items.GetValue():
                break

            counter = counter + 1

        if counter == 0:
            mystyle = fpb.CAPTIONBAR_GRADIENT_V
        elif counter == 1:
            mystyle = fpb.CAPTIONBAR_GRADIENT_H
        elif counter == 2:
            mystyle = fpb.CAPTIONBAR_SINGLE
        elif counter == 3:
            mystyle = fpb.CAPTIONBAR_RECTANGLE
        else:
            mystyle = fpb.CAPTIONBAR_FILLED_RECTANGLE

        style.SetFirstColour(col1)
        style.SetSecondColour(col2)
        style.SetCaptionStyle(mystyle)

        item = self._pnl.GetFoldPanel(0)
        self._pnl.ApplyCaptionStyle(item, style)
    def OnStyleChange(self, event):

        style = fpb.CaptionBarStyle()

        eventid = event.GetId()

        if eventid == self.ID_USE_HGRADIENT:
            style.SetCaptionStyle(fpb.CAPTIONBAR_GRADIENT_H)

        elif eventid == self.ID_USE_VGRADIENT:
            style.SetCaptionStyle(fpb.CAPTIONBAR_GRADIENT_V)

        elif eventid == self.ID_USE_SINGLE:
            style.SetCaptionStyle(fpb.CAPTIONBAR_SINGLE)

        elif eventid == self.ID_USE_RECTANGLE:
            style.SetCaptionStyle(fpb.CAPTIONBAR_RECTANGLE)

        elif eventid == self.ID_USE_FILLED_RECTANGLE:
            style.SetCaptionStyle(fpb.CAPTIONBAR_FILLED_RECTANGLE)

        else:
            raise "ERROR: Undefined Style Selected For CaptionBar: " + repr(eventid)

        col1 = wx.Colour(self._rslider1.GetValue(), self._gslider1.GetValue(),
                         self._bslider1.GetValue())
        col2 = wx.Colour(self._rslider2.GetValue(), self._gslider2.GetValue(),
                         self._bslider2.GetValue())

        style.SetFirstColour(col1)
        style.SetSecondColour(col2)

        if self._single.GetValue():
            item = self._pnl.GetFoldPanel(1)
            self._pnl.ApplyCaptionStyle(item, style)
        else:
            self._pnl.ApplyCaptionStyleAll(style)
    def CreateMenuBar(self, with_window=False):

        # Make a menubar
        file_menu = wx.Menu()

        FPBTEST_QUIT = wx.NewId()
        FPBTEST_REFRESH = wx.NewId()
        FPB_BOTTOM_FOLD = wx.NewId()
        FPB_SINGLE_FOLD = wx.NewId()
        FPB_EXCLUSIVE_FOLD = wx.NewId()
        FPBTEST_TOGGLE_WINDOW = wx.NewId()
        FPBTEST_ABOUT = wx.NewId()

        file_menu.Append(FPBTEST_QUIT, "&Exit")

        option_menu = None

        if with_window:
            # Dummy option
            option_menu = wx.Menu()
            option_menu.Append(FPBTEST_REFRESH, "&Refresh picture")

        # make fold panel menu

        fpb_menu = wx.Menu()
        fpb_menu.AppendCheckItem(FPB_BOTTOM_FOLD, "Create with &fpb.FPB_COLLAPSE_TO_BOTTOM")

        # Now Implemented!
        fpb_menu.AppendCheckItem(FPB_SINGLE_FOLD, "Create with &fpb.FPB_SINGLE_FOLD")

        # Now Implemented!
        fpb_menu.AppendCheckItem(FPB_EXCLUSIVE_FOLD, "Create with &fpb.FPB_EXCLUSIVE_FOLD")

        fpb_menu.AppendSeparator()
        fpb_menu.Append(FPBTEST_TOGGLE_WINDOW, "&Toggle FoldPanelBar")

        help_menu = wx.Menu()
        help_menu.Append(FPBTEST_ABOUT, "&About")

        menu_bar = wx.MenuBar()

        menu_bar.Append(file_menu, "&File")
        menu_bar.Append(fpb_menu, "&FoldPanel")

        if option_menu:
            menu_bar.Append(option_menu, "&Options")

        menu_bar.Append(help_menu, "&Help")

        self.Bind(wx.EVT_MENU, self.OnAbout, id=FPBTEST_ABOUT)
        self.Bind(wx.EVT_MENU, self.OnQuit, id=FPBTEST_QUIT)
        self.Bind(wx.EVT_MENU, self.OnToggleWindow, id=FPBTEST_TOGGLE_WINDOW)
        self.Bind(wx.EVT_MENU, self.OnCreateBottomStyle, id=FPB_BOTTOM_FOLD)
        self.Bind(wx.EVT_MENU, self.OnCreateNormalStyle, id=FPB_SINGLE_FOLD)
        self.Bind(wx.EVT_MENU, self.OnCreateExclusiveStyle, id=FPB_EXCLUSIVE_FOLD)

        self._bottomstyle = FPB_BOTTOM_FOLD
        self._singlestyle = FPB_SINGLE_FOLD
        self._exclusivestyle = FPB_EXCLUSIVE_FOLD

        return menu_bar

#******************物流管理******************************************************888
global transport_company_name
transport_company_name=''
class TestDialog(wx.Dialog):
    def __init__(
            self, parent, id, title, size=wx.DefaultSize, pos=wx.DefaultPosition,
            style=wx.DEFAULT_DIALOG_STYLE, name='dialog'
            ):
        wx.Dialog.__init__(self)
        self.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        self.Create(parent, id, title, pos, size, style, name)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # label = wx.StaticText(self, -1, "")
        # label.SetHelpText("This is the help text for the label")
        # sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, -1, "货运公司")
        label.SetHelpText("This is the help text for the label")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        text = wx.TextCtrl(self, -1, "", size=(80,-1))
        text.SetHelpText("Here's some help text for field #1")
        box.Add(text, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.Bind(wx.EVT_TEXT, self.EvtText, text)

        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)

        # label = wx.StaticText(self, -1, "Field #2:")
        # label.SetHelpText("This is the help text for the label")
        # box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        #
        # text = wx.TextCtrl(self, -1, "", size=(80,-1))
        # text.SetHelpText("Here's some help text for field #2")
        # box.Add(text, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        #
        # sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)

        btnsizer = wx.StdDialogButtonSizer()

        if wx.Platform != "__WXMSW__":
            btn = wx.ContextHelpButton(self)
            btnsizer.AddButton(btn)

        btn = wx.Button(self, wx.ID_OK)
        btn.SetHelpText("The OK button completes the dialog")
        btn.SetDefault()
        btnsizer.AddButton(btn)

        btn = wx.Button(self, wx.ID_CANCEL)
        btn.SetHelpText("The Cancel button cancels the dialog. (Cool, huh?)")
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)
    def EvtText(self, event):
        global transport_company_name
        transport_company_name=event.GetString()
class DelectDialog(wx.Dialog):
    def __init__(
            self, parent, id, title,text, size=wx.DefaultSize, pos=wx.DefaultPosition,
            style=wx.DEFAULT_DIALOG_STYLE, name='dialog'
    ):
        wx.Dialog.__init__(self)
        self.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        self.Create(parent, id, title, pos, size, style, name)
        sizer = wx.BoxSizer(wx.VERTICAL)
        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, -1, "确认删除 %s 货运公司?"% text )
        box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)


        sizer.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)

        # label = wx.StaticText(self, -1, "Field #2:")
        # label.SetHelpText("This is the help text for the label")
        # box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        #
        # text = wx.TextCtrl(self, -1, "", size=(80,-1))
        # text.SetHelpText("Here's some help text for field #2")
        # box.Add(text, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        #
        # sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        line = wx.StaticLine(self, -1, size=(20, -1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT | wx.TOP, 5)

        btnsizer = wx.StdDialogButtonSizer()

        if wx.Platform != "__WXMSW__":
            btn = wx.ContextHelpButton(self)
            btnsizer.AddButton(btn)

        btn = wx.Button(self, wx.ID_OK)
        btn.SetHelpText("The OK button completes the dialog")
        btn.SetDefault()
        btnsizer.AddButton(btn)

        btn = wx.Button(self, wx.ID_CANCEL)
        btn.SetHelpText("The Cancel button cancels the dialog. (Cool, huh?)")
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)

    def EvtText(self, event):
        global transport_company_name
        transport_company_name = event.GetString()
class Transport_Company_Management_Grid(gridlib.Grid):
    def __init__(self, parent):
        gridlib.Grid.__init__(self, parent, -1)
        self.CreateGrid(1, 1)
        self.field_name = ['货运公司']

        for i in range(len(self.field_name)):
            self.SetColLabelValue(i, self.field_name[i])
        self.Show_Transport_Company_Refresh()
        self.AutoSize()
        self.EnableEditing(False)
        #self.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK, self.Change_Data)
        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK, self.Change_Data)
        self.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.Delect_Data)
    def Change_Data(self,evt):
        try:
            row = evt.GetRow()
            text = self.GetCellValue(row, 0)
            dlg = TestDialog(self, -1, "修改货运公司", size=(350, 200),
                             style=wx.DEFAULT_DIALOG_STYLE,
                             )
            dlg.CenterOnScreen()
            # this does not return until the dialog is closed.
            val = dlg.ShowModal()
            if val == wx.ID_OK:
                if transport_company_name != '':
                    if Is_Database_Connect():
                        cursor = DB2.cursor()
                        cursor.execute(
                            "update `info_transport_company__information` set `transport_company_name`= '%s' where `transport_company_name`='%s' " % (transport_company_name,text))
                        DB2.commit()
                        self.Show_Transport_Company_Refresh()
                else:
                    pass
            else:
                pass
            dlg.Destroy()
        except:
            pass
    def Delect_Data(self,evt):
        try:
            row = evt.GetRow()
            text = self.GetCellValue(row, 0)
            dlg = DelectDialog(self, -1, "删除货运公司",text, size=(350, 200),
                             style=wx.DEFAULT_DIALOG_STYLE)
            dlg.CenterOnScreen()
            val = dlg.ShowModal()
            if val == wx.ID_OK:
                if Is_Database_Connect():
                    cursor = DB2.cursor()
                    cursor.execute("UPDATE `info_transport_company__information` SET `State`=-1 WHERE `transport_company_name`='%s' " % (text))
                    DB2.commit()
                    self.Show_Transport_Company_Refresh()
            else:
                pass
            dlg.Destroy()
        except:
            pass
    def Show_Transport_Company_Refresh(self):
        try:
            self.data = []
            new_staff_inform=[]
            if Is_Database_Connect():
                cursor = DB2.cursor()
                cursor.execute("select `transport_company_name` from `info_transport_company__information` where 1 and `State`!=-1" )
                transport_company_name_record = cursor.fetchall()
                if transport_company_name_record is not None or transport_company_name_record!=():
                    self.data=transport_company_name_record

                    now_rows = self.GetNumberRows()
                    if len(self.data) > now_rows:
                        for i in range(len(self.data) - now_rows):
                            self.AppendRows(numRows=1)
                    if len(self.data) < now_rows:
                        for i in range(now_rows - len(self.data)):
                            self.DeleteRows(numRows=1)
                if (len(self.data) != 0):
                    for i in range(len(self.field_name)):  # 用来填写所有表头信息
                        self.SetColLabelValue(i, self.field_name[i])
                    self.SetColLabelAlignment(wx.ALIGN_LEFT, wx.ALIGN_BOTTOM)
                    for i in range(len(self.data)):  # 填数据
                        for j in range(len(self.data[i])):
                            self.SetCellValue(i, j, str(self.data[i][j]))
                else:
                    self.CreateGrid(1, 1)
                    self.field_name = ['货运公司']
                    for i in range(len(self.field_name)):  # 用来填写所有表头信息
                        self.SetColLabelValue(i, self.field_name[i])
                self.AutoSize()
                #wx.adv.LayoutAlgorithm().LayoutWindow(self, self.ylp_Transport_Company_Management_Grid)
        except:
            pass
    def Search_Transport_Company_Refresh(self,transport_company_name):
        try:
            self.data1 = []
            new_staff_inform=[]
            if Is_Database_Connect():
                cursor = DB2.cursor()
                cursor.execute("select `transport_company_name` from `info_transport_company__information` where `transport_company_name`='%s' and `State`!=-1 " % transport_company_name)
                transport_company_name_record = cursor.fetchall()
                if transport_company_name_record is not None or transport_company_name_record!=():
                    self.data1=transport_company_name_record

                    now_rows = self.GetNumberRows()
                    if len(self.data1) > now_rows:
                        for i in range(len(self.data1) - now_rows):
                            self.AppendRows(numRows=1)
                    if len(self.data1) < now_rows:
                        for i in range(now_rows - len(self.data1)):
                            self.DeleteRows(numRows=1)
                if (len(self.data1) != 0):
                    for i in range(len(self.field_name)):  # 用来填写所有表头信息
                        self.SetColLabelValue(i, self.field_name[i])
                    self.SetColLabelAlignment(wx.ALIGN_LEFT, wx.ALIGN_BOTTOM)
                    for i in range(len(self.data1)):  # 填数据
                        for j in range(len(self.data1[i])):
                            self.SetCellValue(i, j, str(self.data1[i][j]))
                else:
                    self.CreateGrid(1, 2)
                    self.field_name = ['经销商','货运公司']
                    for i in range(len(self.field_name)):  # 用来填写所有表头信息
                        self.SetColLabelValue(i, self.field_name[i])
                self.AutoSize()
                #wx.adv.LayoutAlgorithm().LayoutWindow(self, self.ylp_Transport_Company_Management_Grid)
        except:
            pass
class YLP_Transport_Company_Management_Panel(wx.Panel):
    def __init__(self, parent,log, id=wx.ID_ANY, title="", pos=wx.DefaultPosition,
                 size=(700,650), style=wx.DEFAULT_FRAME_STYLE):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.select_code = 0
        self._flags = 0
        self.log = log
        self.label_list=[]
        self._leftWindow1 = wx.adv.SashLayoutWindow(self, 101, wx.DefaultPosition,
                                                wx.Size(200, 1000), wx.NO_BORDER |
                                                wx.adv.SW_3D | wx.CLIP_CHILDREN)
        self._leftWindow1.SetDefaultSize(wx.Size(220, 1000))
        self._leftWindow1.SetOrientation(wx.adv.LAYOUT_VERTICAL)
        self._leftWindow1.SetAlignment(wx.adv.LAYOUT_LEFT)
        self._leftWindow1.SetSashVisible(wx.adv.SASH_RIGHT, True)
        self._leftWindow1.SetExtraBorderSize(10)
        self._pnl = 0
        self.ylp_Transport_Company_Management_Grid=Transport_Company_Management_Grid(self)

        self.ID_WINDOW_LEFT1 = 101
        self.ID_WINDOW_RIGHT1 = 102
        self._leftWindow1.Bind(wx.adv.EVT_SASH_DRAGGED_RANGE, self.OnFoldPanelBarDrag,
                               id=101, id2=102)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        self.Bind(wx.EVT_SCROLL, self.OnSlideColour)
        self.ReCreateFoldPanel(0)

    #-----------------------------------------
    def store_id_click(self,event):
        self.getstring=event.GetString()

    def search_button(self,event):
        pass
    #-----------------------------------------
    def Terminal_id_click(self,event):
        self.store_combox.SetValue('ALL')
        self.member_combox.SetValue('ALL')
        self.time_deal()
        self.TreeCtrl_Refresh(self.start_time, self.end_time)
    def OnSize(self, event):
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.ylp_Transport_Company_Management_Grid)
        event.Skip()
    def OnQuit(self, event):
        self.Destroy()
    def OnToggleWindow(self, event):

        self._leftWindow1.Show(not self._leftWindow1.IsShown())
        # Leaves bits of itself behind sometimes
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.ylp_Show_Inform_Panel)
        self.ylp_Show_Inform_Panel.Refresh()

        event.Skip()
    def OnFoldPanelBarDrag(self, event):

        # if event.GetDragStatus() == wx.SASH_STATUS_OUT_OF_RANGE:
        #     return

        if event.GetId() == self.ID_WINDOW_LEFT1:
            self._leftWindow1.SetDefaultSize(wx.Size(event.GetDragRect().width, 1000))
        # if event.GetId() == self.ID_WINDOW_RIGHT1:
        #     self._leftWindow2.SetDefaultSize(wx.Size(event.GetDragRect().width, 1000))
        # Leaves bits of itself behind sometimes
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.ylp_Transport_Company_Management_Grid)
        # wx.adv.LayoutAlgorithm().LayoutWindow(self, self.ylp_Show_Inform_Panel)
        self.ylp_Transport_Company_Management_Grid.Refresh()
        event.Skip()
    #-------------------------------------------
    def EvtCheckListBox(self,event):
        index = event.GetSelection()
        label = self.lb.GetString(index)
        status = 'False'
        if self.lb.IsChecked(index):
            status = 'True'
            self.label_list.append(label)
        else:
            self.label_list.remove(label)
        self.ylp_Transport_Company_Management_Grid.Show_Transport_Company_Refresh()
        #self.lb.SetSelection(index)

    def ReCreateFoldPanel(self, fpb_flags):

        self._leftWindow1.DestroyChildren()

        self._pnl = fpb.FoldPanelBar(self._leftWindow1, -1, wx.DefaultPosition,
                                     wx.Size(-1,-1), agwStyle=fpb_flags)

        Images = wx.ImageList(16,16)
        Images.Add(GetExpandedIconBitmap())
        Images.Add(GetCollapsedIconBitmap())
        item = self._pnl.AddFoldPanel("搜索", False, foldIcons=Images)
        self.statictext6 = wx.StaticText(item, -1, label="搜索货运公司")
        self._pnl.AddFoldPanelWindow(item, self.statictext6)

        self.lb = wx.TextCtrl(item, -1, "", size=(125, -1))
        self.Bind(wx.EVT_TEXT, self.EvtText)
        #
        # # self.lb = wx.CheckListBox(item, -1, (80, 50), wx.DefaultSize, sampleList)
        # # self.Bind(wx.EVT_CHECKLISTBOX, self.EvtCheckListBox, self.lb)
        # # self.lb.SetSelection(0)
        pos = self.lb.GetPosition().x + self.lb.GetSize().width + 25
        self._pnl.AddFoldPanelWindow(item, self.lb)

        search = wx.Button(item, wx.ID_ANY, "增加货运公司")
        self._pnl.AddFoldPanelWindow(item, search)
        search.Bind(wx.EVT_BUTTON, self.OnButton)
        self._leftWindow1.SizeWindows()

    #----------------------------------------
    def EvtText(self,event):
        if event.GetString() == '':
            self.ylp_Transport_Company_Management_Grid.Show_Transport_Company_Refresh()
        else:
            self.ylp_Transport_Company_Management_Grid.Search_Transport_Company_Refresh(event.GetString())
    def OnButton(self, evt):
        dlg = TestDialog(self, -1, "增加货运公司", size=(350, 200),
                         style=wx.DEFAULT_DIALOG_STYLE,
                         )
        dlg.CenterOnScreen()

        # this does not return until the dialog is closed.
        val = dlg.ShowModal()

        if val == wx.ID_OK:
            if transport_company_name!='':
                if Is_Database_Connect():
                    cursor = DB2.cursor()
                    cursor.execute(
                        "select `transport_company_name` from `info_transport_company__information` where `transport_company_name`='%s'  " % transport_company_name)
                    transport_company_name_record = cursor.fetchone()
                    if transport_company_name_record is None :
                        cursor.execute(
                            "insert into `info_transport_company__information`(`transport_company_name` ) values ('%s')  " % transport_company_name)
                        DB2.commit()
                        self.ylp_Transport_Company_Management_Grid.Show_Transport_Company_Refresh()

                    else:
                        pass
            else:
                pass
            #self.log.WriteText("You pressed OK\n")
        else:
            self.log.WriteText("You pressed Cancel\n")

        dlg.Destroy()
    def onDateStart(self,event):
        self.date_start=self.calendar_begin.GetValue()
        self.date_end=self.calendar_end.GetValue()
        self.log.WriteText("天外天系统收到操作员控制指令，开始执行日期查询操作，起始日期："+str(self.date_start)+"，终止日期："+str(self.date_end)+"\r\n")
    def OnCreateBottomStyle(self, event):

        # recreate with style collapse to bottom, which means
        # all panels that are collapsed are placed at the bottom,
        # or normal

        if event.IsChecked():
            self.GetMenuBar().Check(self._singlestyle, False)
            self.GetMenuBar().Check(self._exclusivestyle, False)
            self._flags = self._flags & ~fpb.FPB_SINGLE_FOLD
            self._flags = self._flags & ~fpb.FPB_EXCLUSIVE_FOLD
            self._flags = self._flags | fpb.FPB_COLLAPSE_TO_BOTTOM
        else:
            self._flags = self._flags & ~fpb.FPB_COLLAPSE_TO_BOTTOM

        self.ReCreateFoldPanel(self._flags)
        #self.Create_TreeCtrl()
    def OnCreateNormalStyle(self, event):

        # recreate with style where only one panel at the time is
        # allowed to be opened

        if event.IsChecked():
            self.GetMenuBar().Check(self._bottomstyle, False)
            self.GetMenuBar().Check(self._exclusivestyle, False)
            self._flags = self._flags & ~fpb.FPB_EXCLUSIVE_FOLD
            self._flags = self._flags & ~fpb.FPB_COLLAPSE_TO_BOTTOM
            self._flags = self._flags | fpb.FPB_SINGLE_FOLD
        else:
            self._flags = self._flags & ~fpb.FPB_SINGLE_FOLD

        self.ReCreateFoldPanel(self._flags)
        #self.Create_TreeCtrl()
    def OnCreateExclusiveStyle(self, event):
        # recreate with style where only one panel at the time is
        # allowed to be opened and the others are collapsed to bottom
        if event.IsChecked():
            self.GetMenuBar().Check(self._singlestyle, False)
            self.GetMenuBar().Check(self._bottomstyle, False)
            self._flags = self._flags & ~fpb.FPB_SINGLE_FOLD
            self._flags = self._flags & ~fpb.FPB_COLLAPSE_TO_BOTTOM
            self._flags = self._flags | fpb.FPB_EXCLUSIVE_FOLD
        else:
            self._flags = self._flags & ~fpb.FPB_EXCLUSIVE_FOLD
        self.ReCreateFoldPanel(self._flags)
        #self.Create_TreeCtrl()
    def OnCollapseMe(self, event):
        for i in range(0, self._pnl.GetCount()):
            item = self._pnl.GetFoldPanel(i)
            self._pnl.Collapse(item)
    def OnExpandMe(self, event):
        style = fpb.CaptionBarStyle()
        counter = 0
        for items in self.radiocontrols:
            if items.GetValue():
                break
            counter = counter + 1
        if counter == 0:
            mystyle = fpb.CAPTIONBAR_GRADIENT_V
        elif counter == 1:
            mystyle = fpb.CAPTIONBAR_GRADIENT_H
        elif counter == 2:
            mystyle = fpb.CAPTIONBAR_SINGLE
        elif counter == 3:
            mystyle = fpb.CAPTIONBAR_RECTANGLE
        else:
            mystyle = fpb.CAPTIONBAR_FILLED_RECTANGLE

        # style.SetCaptionStyle(mystyle)
        # self._pnl.ApplyCaptionStyleAll(style)
    def OnSlideColour(self, event):

        col1 = wx.Colour(self._rslider1.GetValue(), self._gslider1.GetValue(),
                         self._bslider1.GetValue())
        col2 = wx.Colour(self._rslider2.GetValue(), self._gslider2.GetValue(),
                         self._bslider2.GetValue())

        style = fpb.CaptionBarStyle()

        counter = 0
        for items in self.radiocontrols:
            if items.GetValue():
                break

            counter = counter + 1

        if counter == 0:
            mystyle = fpb.CAPTIONBAR_GRADIENT_V
        elif counter == 1:
            mystyle = fpb.CAPTIONBAR_GRADIENT_H
        elif counter == 2:
            mystyle = fpb.CAPTIONBAR_SINGLE
        elif counter == 3:
            mystyle = fpb.CAPTIONBAR_RECTANGLE
        else:
            mystyle = fpb.CAPTIONBAR_FILLED_RECTANGLE

        style.SetFirstColour(col1)
        style.SetSecondColour(col2)
        style.SetCaptionStyle(mystyle)

        item = self._pnl.GetFoldPanel(0)
        self._pnl.ApplyCaptionStyle(item, style)
    def OnStyleChange(self, event):

        style = fpb.CaptionBarStyle()

        eventid = event.GetId()

        if eventid == self.ID_USE_HGRADIENT:
            style.SetCaptionStyle(fpb.CAPTIONBAR_GRADIENT_H)

        elif eventid == self.ID_USE_VGRADIENT:
            style.SetCaptionStyle(fpb.CAPTIONBAR_GRADIENT_V)

        elif eventid == self.ID_USE_SINGLE:
            style.SetCaptionStyle(fpb.CAPTIONBAR_SINGLE)

        elif eventid == self.ID_USE_RECTANGLE:
            style.SetCaptionStyle(fpb.CAPTIONBAR_RECTANGLE)

        elif eventid == self.ID_USE_FILLED_RECTANGLE:
            style.SetCaptionStyle(fpb.CAPTIONBAR_FILLED_RECTANGLE)

        else:
            raise "ERROR: Undefined Style Selected For CaptionBar: " + repr(eventid)

        col1 = wx.Colour(self._rslider1.GetValue(), self._gslider1.GetValue(),
                         self._bslider1.GetValue())
        col2 = wx.Colour(self._rslider2.GetValue(), self._gslider2.GetValue(),
                         self._bslider2.GetValue())

        style.SetFirstColour(col1)
        style.SetSecondColour(col2)

        if self._single.GetValue():
            item = self._pnl.GetFoldPanel(1)
            self._pnl.ApplyCaptionStyle(item, style)
        else:
            self._pnl.ApplyCaptionStyleAll(style)
    def CreateMenuBar(self, with_window=False):

        # Make a menubar
        file_menu = wx.Menu()

        FPBTEST_QUIT = wx.NewId()
        FPBTEST_REFRESH = wx.NewId()
        FPB_BOTTOM_FOLD = wx.NewId()
        FPB_SINGLE_FOLD = wx.NewId()
        FPB_EXCLUSIVE_FOLD = wx.NewId()
        FPBTEST_TOGGLE_WINDOW = wx.NewId()
        FPBTEST_ABOUT = wx.NewId()

        file_menu.Append(FPBTEST_QUIT, "&Exit")

        option_menu = None

        if with_window:
            # Dummy option
            option_menu = wx.Menu()
            option_menu.Append(FPBTEST_REFRESH, "&Refresh picture")

        # make fold panel menu

        fpb_menu = wx.Menu()
        fpb_menu.AppendCheckItem(FPB_BOTTOM_FOLD, "Create with &fpb.FPB_COLLAPSE_TO_BOTTOM")

        # Now Implemented!
        fpb_menu.AppendCheckItem(FPB_SINGLE_FOLD, "Create with &fpb.FPB_SINGLE_FOLD")

        # Now Implemented!
        fpb_menu.AppendCheckItem(FPB_EXCLUSIVE_FOLD, "Create with &fpb.FPB_EXCLUSIVE_FOLD")

        fpb_menu.AppendSeparator()
        fpb_menu.Append(FPBTEST_TOGGLE_WINDOW, "&Toggle FoldPanelBar")

        help_menu = wx.Menu()
        help_menu.Append(FPBTEST_ABOUT, "&About")

        menu_bar = wx.MenuBar()

        menu_bar.Append(file_menu, "&File")
        menu_bar.Append(fpb_menu, "&FoldPanel")

        if option_menu:
            menu_bar.Append(option_menu, "&Options")

        menu_bar.Append(help_menu, "&Help")

        self.Bind(wx.EVT_MENU, self.OnAbout, id=FPBTEST_ABOUT)
        self.Bind(wx.EVT_MENU, self.OnQuit, id=FPBTEST_QUIT)
        self.Bind(wx.EVT_MENU, self.OnToggleWindow, id=FPBTEST_TOGGLE_WINDOW)
        self.Bind(wx.EVT_MENU, self.OnCreateBottomStyle, id=FPB_BOTTOM_FOLD)
        self.Bind(wx.EVT_MENU, self.OnCreateNormalStyle, id=FPB_SINGLE_FOLD)
        self.Bind(wx.EVT_MENU, self.OnCreateExclusiveStyle, id=FPB_EXCLUSIVE_FOLD)

        self._bottomstyle = FPB_BOTTOM_FOLD
        self._singlestyle = FPB_SINGLE_FOLD
        self._exclusivestyle = FPB_EXCLUSIVE_FOLD

        return menu_bar
#----------------------------------------------------------------
class Dealer_Transport_Dialog(wx.Dialog):
    def __init__(
            self, parent, id, title, size=wx.DefaultSize, pos=wx.DefaultPosition,
            style=wx.DEFAULT_DIALOG_STYLE, name='dialog'
            ):
        wx.Dialog.__init__(self)
        self.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        self.Create(parent, id, title, pos, size, style, name)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # label = wx.StaticText(self, -1, "")
        # label.SetHelpText("This is the help text for the label")
        # sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, -1, "货运公司")
        label.SetHelpText("This is the help text for the label")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        text = wx.TextCtrl(self, -1, "", size=(80,-1))
        text.SetHelpText("Here's some help text for field #1")
        box.Add(text, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.Bind(wx.EVT_TEXT, self.EvtText, text)

        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)

        # label = wx.StaticText(self, -1, "Field #2:")
        # label.SetHelpText("This is the help text for the label")
        # box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        #
        # text = wx.TextCtrl(self, -1, "", size=(80,-1))
        # text.SetHelpText("Here's some help text for field #2")
        # box.Add(text, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        #
        # sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)

        btnsizer = wx.StdDialogButtonSizer()

        if wx.Platform != "__WXMSW__":
            btn = wx.ContextHelpButton(self)
            btnsizer.AddButton(btn)

        btn = wx.Button(self, wx.ID_OK)
        btn.SetHelpText("The OK button completes the dialog")
        btn.SetDefault()
        btnsizer.AddButton(btn)

        btn = wx.Button(self, wx.ID_CANCEL)
        btn.SetHelpText("The Cancel button cancels the dialog. (Cool, huh?)")
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)
    def EvtText(self, event):
        global transport_company_name
        transport_company_name=event.GetString()
class Dealer_Transport_Company_Management_Grid(gridlib.Grid):
    def __init__(self, parent):
        gridlib.Grid.__init__(self, parent, -1)
        self.CreateGrid(1, 2)
        self.field_name = ['经销商','货运公司']

        for i in range(len(self.field_name)):
            self.SetColLabelValue(i, self.field_name[i])
        self.Show_Dealer_Transport_Company_Refresh()
        self.AutoSize()
        self.EnableEditing(False)
        #self.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK, self.Change_Data)
        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK, self.Change_Data)
    def Change_Data(self,evt):
        try:
            row = evt.GetRow()
            text = self.GetCellValue(row, 0)
            dlg = Dealer_Transport_Dialog(self, -1, "修改货运公司", size=(350, 200),
                             style=wx.DEFAULT_DIALOG_STYLE,
                             )
            dlg.CenterOnScreen()
            # this does not return until the dialog is closed.
            val = dlg.ShowModal()
            if val == wx.ID_OK:
                if transport_company_name != '':
                    if Is_Database_Connect():
                        cursor = DB2.cursor()
                        cursor.execute(
                            "update `order_company_info` set `transport_company_name`= '%s' where `company_name`='%s' " % (transport_company_name,text))
                        DB2.commit()
                        self.Show_Dealer_Transport_Company_Refresh()
                else:
                    pass
            else:
                pass
            dlg.Destroy()
        except:
            pass
    def Show_Dealer_Transport_Company_Refresh(self):
        try:
            self.data = []
            new_staff_inform=[]
            if Is_Database_Connect():
                cursor = DB2.cursor()
                cursor.execute("select `company_name`,`transport_company_name` from `order_company_info` where 1 " )
                transport_company_name_record = cursor.fetchall()
                if transport_company_name_record is not None or transport_company_name_record!=():
                    self.data=transport_company_name_record

                    now_rows = self.GetNumberRows()
                    if len(self.data) > now_rows:
                        for i in range(len(self.data) - now_rows):
                            self.AppendRows(numRows=1)
                    if len(self.data) < now_rows:
                        for i in range(now_rows - len(self.data)):
                            self.DeleteRows(numRows=1)
                if (len(self.data) != 0):
                    for i in range(len(self.field_name)):  # 用来填写所有表头信息
                        self.SetColLabelValue(i, self.field_name[i])
                    self.SetColLabelAlignment(wx.ALIGN_LEFT, wx.ALIGN_BOTTOM)
                    for i in range(len(self.data)):  # 填数据
                        for j in range(len(self.data[i])):
                            self.SetCellValue(i, j, str(self.data[i][j]))
                else:
                    self.CreateGrid(1, 2)
                    self.field_name = ['经销商','货运公司']
                    for i in range(len(self.field_name)):  # 用来填写所有表头信息
                        self.SetColLabelValue(i, self.field_name[i])
                self.AutoSize()
                #wx.adv.LayoutAlgorithm().LayoutWindow(self, self.ylp_Transport_Company_Management_Grid)
        except:
            pass
    def Search_Dealer_Transport_Company_Refresh(self,company_name):
        try:
            self.data1 = []
            new_staff_inform=[]
            if Is_Database_Connect():
                cursor = DB2.cursor()
                cursor.execute("select `company_name`,`transport_company_name` from `order_company_info` where `company_name`='%s' " % company_name )
                transport_company_name_record = cursor.fetchall()
                if transport_company_name_record is not None or transport_company_name_record!=():
                    self.data1=transport_company_name_record

                    now_rows = self.GetNumberRows()
                    if len(self.data1) > now_rows:
                        for i in range(len(self.data1) - now_rows):
                            self.AppendRows(numRows=1)
                    if len(self.data1) < now_rows:
                        for i in range(now_rows - len(self.data1)):
                            self.DeleteRows(numRows=1)
                if (len(self.data1) != 0):
                    for i in range(len(self.field_name)):  # 用来填写所有表头信息
                        self.SetColLabelValue(i, self.field_name[i])
                    self.SetColLabelAlignment(wx.ALIGN_LEFT, wx.ALIGN_BOTTOM)
                    for i in range(len(self.data1)):  # 填数据
                        for j in range(len(self.data1[i])):
                            self.SetCellValue(i, j, str(self.data1[i][j]))
                else:
                    self.CreateGrid(1, 2)
                    self.field_name = ['经销商','货运公司']
                    for i in range(len(self.field_name)):  # 用来填写所有表头信息
                        self.SetColLabelValue(i, self.field_name[i])
                self.AutoSize()
                #wx.adv.LayoutAlgorithm().LayoutWindow(self, self.ylp_Transport_Company_Management_Grid)
        except:
            pass
class YLP_Dealer_Transport_Company_Management_Panel(wx.Panel):
    def __init__(self, parent,log, id=wx.ID_ANY, title="", pos=wx.DefaultPosition,
                 size=(700,650), style=wx.DEFAULT_FRAME_STYLE):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.select_code = 0
        self._flags = 0
        self.log = log
        self.label_list=[]
        self._leftWindow1 = wx.adv.SashLayoutWindow(self, 101, wx.DefaultPosition,
                                                wx.Size(200, 1000), wx.NO_BORDER |
                                                wx.adv.SW_3D | wx.CLIP_CHILDREN)
        self._leftWindow1.SetDefaultSize(wx.Size(220, 1000))
        self._leftWindow1.SetOrientation(wx.adv.LAYOUT_VERTICAL)
        self._leftWindow1.SetAlignment(wx.adv.LAYOUT_LEFT)
        self._leftWindow1.SetSashVisible(wx.adv.SASH_RIGHT, True)
        self._leftWindow1.SetExtraBorderSize(10)
        self._pnl = 0
        self.ylp_Dealer_Transport_Company_Management_Grid=Dealer_Transport_Company_Management_Grid(self)

        self.ID_WINDOW_LEFT1 = 101
        self.ID_WINDOW_RIGHT1 = 102
        self._leftWindow1.Bind(wx.adv.EVT_SASH_DRAGGED_RANGE, self.OnFoldPanelBarDrag,
                               id=101, id2=102)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        self.Bind(wx.EVT_SCROLL, self.OnSlideColour)
        self.ReCreateFoldPanel(0)

    #-----------------------------------------
    def store_id_click(self,event):
        self.getstring=event.GetString()

    def search_button(self,event):
        pass
    #-----------------------------------------
    def Terminal_id_click(self,event):
        self.store_combox.SetValue('ALL')
        self.member_combox.SetValue('ALL')
        self.time_deal()
        self.TreeCtrl_Refresh(self.start_time, self.end_time)
    def OnSize(self, event):
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.ylp_Dealer_Transport_Company_Management_Grid)
        event.Skip()
    def OnQuit(self, event):
        self.Destroy()
    def OnToggleWindow(self, event):

        self._leftWindow1.Show(not self._leftWindow1.IsShown())
        # Leaves bits of itself behind sometimes
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.ylp_Show_Inform_Panel)
        self.ylp_Show_Inform_Panel.Refresh()

        event.Skip()
    def OnFoldPanelBarDrag(self, event):

        # if event.GetDragStatus() == wx.SASH_STATUS_OUT_OF_RANGE:
        #     return

        if event.GetId() == self.ID_WINDOW_LEFT1:
            self._leftWindow1.SetDefaultSize(wx.Size(event.GetDragRect().width, 1000))
        # if event.GetId() == self.ID_WINDOW_RIGHT1:
        #     self._leftWindow2.SetDefaultSize(wx.Size(event.GetDragRect().width, 1000))
        # Leaves bits of itself behind sometimes
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.ylp_Dealer_Transport_Company_Management_Grid)
        # wx.adv.LayoutAlgorithm().LayoutWindow(self, self.ylp_Show_Inform_Panel)
        self.ylp_Dealer_Transport_Company_Management_Grid.Refresh()
        event.Skip()
    #-------------------------------------------
    def EvtCheckListBox(self,event):
        index = event.GetSelection()
        label = self.lb.GetString(index)
        status = 'False'
        if self.lb.IsChecked(index):
            status = 'True'
            self.label_list.append(label)
        else:
            self.label_list.remove(label)
        self.ylp_Dealer_Transport_Company_Management_Grid.Show_Dealer_Transport_Company_Refresh()
        #self.lb.SetSelection(index)

    def ReCreateFoldPanel(self, fpb_flags):

        self._leftWindow1.DestroyChildren()

        self._pnl = fpb.FoldPanelBar(self._leftWindow1, -1, wx.DefaultPosition,
                                     wx.Size(-1,-1), agwStyle=fpb_flags)

        Images = wx.ImageList(16,16)
        Images.Add(GetExpandedIconBitmap())
        Images.Add(GetCollapsedIconBitmap())
        item = self._pnl.AddFoldPanel("搜索", False, foldIcons=Images)
        self.statictext6 = wx.StaticText(item, -1, label="搜索经销商")
        self._pnl.AddFoldPanelWindow(item, self.statictext6)

        self.lb = wx.TextCtrl(item, -1, "", size=(125, -1))
        self.Bind(wx.EVT_TEXT, self.EvtText)
        #
        # # self.lb = wx.CheckListBox(item, -1, (80, 50), wx.DefaultSize, sampleList)
        # # self.Bind(wx.EVT_CHECKLISTBOX, self.EvtCheckListBox, self.lb)
        # self.lb.SetSelection(0)
        pos = self.lb.GetPosition().x + self.lb.GetSize().width + 25
        self._pnl.AddFoldPanelWindow(item, self.lb)

        # search = wx.Button(item, wx.ID_ANY, "增加货运公司")
        # self._pnl.AddFoldPanelWindow(item, search)
        # search.Bind(wx.EVT_BUTTON, self.OnButton)
        self._leftWindow1.SizeWindows()

    #----------------------------------------
    def EvtText(self, event):
        if event.GetString()=='':
            self.ylp_Dealer_Transport_Company_Management_Grid.Show_Dealer_Transport_Company_Refresh()
        else:
            self.ylp_Dealer_Transport_Company_Management_Grid.Search_Dealer_Transport_Company_Refresh(event.GetString())
    # def OnButton(self, evt):
    #     dlg = TestDialog(self, -1, "增加货运公司", size=(350, 200),
    #                      style=wx.DEFAULT_DIALOG_STYLE,
    #                      )
    #     dlg.CenterOnScreen()
    #
    #     # this does not return until the dialog is closed.
    #     val = dlg.ShowModal()
    #
    #     if val == wx.ID_OK:
    #         if transport_company_name!='':
    #             if Is_Database_Connect():
    #                 cursor = DB2.cursor()
    #                 cursor.execute(
    #                     "select `transport_company_name` from `info_transport_company__information` where `transport_company_name`='%s'  " % transport_company_name)
    #                 transport_company_name_record = cursor.fetchone()
    #                 if transport_company_name_record is None :
    #                     cursor.execute(
    #                         "insert into `info_transport_company__information`(`transport_company_name` ) values ('%s')  " % transport_company_name)
    #                     DB2.commit()
    #                     self.ylp_Dealer_Transport_Company_Management_Grid.Show_Transport_Company_Refresh()
    #
    #                 else:
    #                     pass
    #         else:
    #             pass
    #         #self.log.WriteText("You pressed OK\n")
    #     else:
    #         self.log.WriteText("You pressed Cancel\n")
    #
    #     dlg.Destroy()
    def onDateStart(self,event):
        self.date_start=self.calendar_begin.GetValue()
        self.date_end=self.calendar_end.GetValue()
        self.log.WriteText("天外天系统收到操作员控制指令，开始执行日期查询操作，起始日期："+str(self.date_start)+"，终止日期："+str(self.date_end)+"\r\n")
    def OnCreateBottomStyle(self, event):

        # recreate with style collapse to bottom, which means
        # all panels that are collapsed are placed at the bottom,
        # or normal

        if event.IsChecked():
            self.GetMenuBar().Check(self._singlestyle, False)
            self.GetMenuBar().Check(self._exclusivestyle, False)
            self._flags = self._flags & ~fpb.FPB_SINGLE_FOLD
            self._flags = self._flags & ~fpb.FPB_EXCLUSIVE_FOLD
            self._flags = self._flags | fpb.FPB_COLLAPSE_TO_BOTTOM
        else:
            self._flags = self._flags & ~fpb.FPB_COLLAPSE_TO_BOTTOM

        self.ReCreateFoldPanel(self._flags)
        #self.Create_TreeCtrl()
    def OnCreateNormalStyle(self, event):

        # recreate with style where only one panel at the time is
        # allowed to be opened

        if event.IsChecked():
            self.GetMenuBar().Check(self._bottomstyle, False)
            self.GetMenuBar().Check(self._exclusivestyle, False)
            self._flags = self._flags & ~fpb.FPB_EXCLUSIVE_FOLD
            self._flags = self._flags & ~fpb.FPB_COLLAPSE_TO_BOTTOM
            self._flags = self._flags | fpb.FPB_SINGLE_FOLD
        else:
            self._flags = self._flags & ~fpb.FPB_SINGLE_FOLD

        self.ReCreateFoldPanel(self._flags)
        #self.Create_TreeCtrl()
    def OnCreateExclusiveStyle(self, event):
        # recreate with style where only one panel at the time is
        # allowed to be opened and the others are collapsed to bottom
        if event.IsChecked():
            self.GetMenuBar().Check(self._singlestyle, False)
            self.GetMenuBar().Check(self._bottomstyle, False)
            self._flags = self._flags & ~fpb.FPB_SINGLE_FOLD
            self._flags = self._flags & ~fpb.FPB_COLLAPSE_TO_BOTTOM
            self._flags = self._flags | fpb.FPB_EXCLUSIVE_FOLD
        else:
            self._flags = self._flags & ~fpb.FPB_EXCLUSIVE_FOLD
        self.ReCreateFoldPanel(self._flags)
        #self.Create_TreeCtrl()
    def OnCollapseMe(self, event):
        for i in range(0, self._pnl.GetCount()):
            item = self._pnl.GetFoldPanel(i)
            self._pnl.Collapse(item)
    def OnExpandMe(self, event):
        style = fpb.CaptionBarStyle()
        counter = 0
        for items in self.radiocontrols:
            if items.GetValue():
                break
            counter = counter + 1
        if counter == 0:
            mystyle = fpb.CAPTIONBAR_GRADIENT_V
        elif counter == 1:
            mystyle = fpb.CAPTIONBAR_GRADIENT_H
        elif counter == 2:
            mystyle = fpb.CAPTIONBAR_SINGLE
        elif counter == 3:
            mystyle = fpb.CAPTIONBAR_RECTANGLE
        else:
            mystyle = fpb.CAPTIONBAR_FILLED_RECTANGLE

        # style.SetCaptionStyle(mystyle)
        # self._pnl.ApplyCaptionStyleAll(style)
    def OnSlideColour(self, event):

        col1 = wx.Colour(self._rslider1.GetValue(), self._gslider1.GetValue(),
                         self._bslider1.GetValue())
        col2 = wx.Colour(self._rslider2.GetValue(), self._gslider2.GetValue(),
                         self._bslider2.GetValue())

        style = fpb.CaptionBarStyle()

        counter = 0
        for items in self.radiocontrols:
            if items.GetValue():
                break

            counter = counter + 1

        if counter == 0:
            mystyle = fpb.CAPTIONBAR_GRADIENT_V
        elif counter == 1:
            mystyle = fpb.CAPTIONBAR_GRADIENT_H
        elif counter == 2:
            mystyle = fpb.CAPTIONBAR_SINGLE
        elif counter == 3:
            mystyle = fpb.CAPTIONBAR_RECTANGLE
        else:
            mystyle = fpb.CAPTIONBAR_FILLED_RECTANGLE

        style.SetFirstColour(col1)
        style.SetSecondColour(col2)
        style.SetCaptionStyle(mystyle)

        item = self._pnl.GetFoldPanel(0)
        self._pnl.ApplyCaptionStyle(item, style)
    def OnStyleChange(self, event):

        style = fpb.CaptionBarStyle()

        eventid = event.GetId()

        if eventid == self.ID_USE_HGRADIENT:
            style.SetCaptionStyle(fpb.CAPTIONBAR_GRADIENT_H)

        elif eventid == self.ID_USE_VGRADIENT:
            style.SetCaptionStyle(fpb.CAPTIONBAR_GRADIENT_V)

        elif eventid == self.ID_USE_SINGLE:
            style.SetCaptionStyle(fpb.CAPTIONBAR_SINGLE)

        elif eventid == self.ID_USE_RECTANGLE:
            style.SetCaptionStyle(fpb.CAPTIONBAR_RECTANGLE)

        elif eventid == self.ID_USE_FILLED_RECTANGLE:
            style.SetCaptionStyle(fpb.CAPTIONBAR_FILLED_RECTANGLE)

        else:
            raise "ERROR: Undefined Style Selected For CaptionBar: " + repr(eventid)

        col1 = wx.Colour(self._rslider1.GetValue(), self._gslider1.GetValue(),
                         self._bslider1.GetValue())
        col2 = wx.Colour(self._rslider2.GetValue(), self._gslider2.GetValue(),
                         self._bslider2.GetValue())

        style.SetFirstColour(col1)
        style.SetSecondColour(col2)

        if self._single.GetValue():
            item = self._pnl.GetFoldPanel(1)
            self._pnl.ApplyCaptionStyle(item, style)
        else:
            self._pnl.ApplyCaptionStyleAll(style)
    def CreateMenuBar(self, with_window=False):

        # Make a menubar
        file_menu = wx.Menu()

        FPBTEST_QUIT = wx.NewId()
        FPBTEST_REFRESH = wx.NewId()
        FPB_BOTTOM_FOLD = wx.NewId()
        FPB_SINGLE_FOLD = wx.NewId()
        FPB_EXCLUSIVE_FOLD = wx.NewId()
        FPBTEST_TOGGLE_WINDOW = wx.NewId()
        FPBTEST_ABOUT = wx.NewId()

        file_menu.Append(FPBTEST_QUIT, "&Exit")

        option_menu = None

        if with_window:
            # Dummy option
            option_menu = wx.Menu()
            option_menu.Append(FPBTEST_REFRESH, "&Refresh picture")

        # make fold panel menu

        fpb_menu = wx.Menu()
        fpb_menu.AppendCheckItem(FPB_BOTTOM_FOLD, "Create with &fpb.FPB_COLLAPSE_TO_BOTTOM")

        # Now Implemented!
        fpb_menu.AppendCheckItem(FPB_SINGLE_FOLD, "Create with &fpb.FPB_SINGLE_FOLD")

        # Now Implemented!
        fpb_menu.AppendCheckItem(FPB_EXCLUSIVE_FOLD, "Create with &fpb.FPB_EXCLUSIVE_FOLD")

        fpb_menu.AppendSeparator()
        fpb_menu.Append(FPBTEST_TOGGLE_WINDOW, "&Toggle FoldPanelBar")

        help_menu = wx.Menu()
        help_menu.Append(FPBTEST_ABOUT, "&About")

        menu_bar = wx.MenuBar()

        menu_bar.Append(file_menu, "&File")
        menu_bar.Append(fpb_menu, "&FoldPanel")

        if option_menu:
            menu_bar.Append(option_menu, "&Options")

        menu_bar.Append(help_menu, "&Help")

        self.Bind(wx.EVT_MENU, self.OnAbout, id=FPBTEST_ABOUT)
        self.Bind(wx.EVT_MENU, self.OnQuit, id=FPBTEST_QUIT)
        self.Bind(wx.EVT_MENU, self.OnToggleWindow, id=FPBTEST_TOGGLE_WINDOW)
        self.Bind(wx.EVT_MENU, self.OnCreateBottomStyle, id=FPB_BOTTOM_FOLD)
        self.Bind(wx.EVT_MENU, self.OnCreateNormalStyle, id=FPB_SINGLE_FOLD)
        self.Bind(wx.EVT_MENU, self.OnCreateExclusiveStyle, id=FPB_EXCLUSIVE_FOLD)

        self._bottomstyle = FPB_BOTTOM_FOLD
        self._singlestyle = FPB_SINGLE_FOLD
        self._exclusivestyle = FPB_EXCLUSIVE_FOLD

        return menu_bar