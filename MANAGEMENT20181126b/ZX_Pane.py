#!/usr/bin/env python
# _*_ coding: UTF-8 _*
#ZX_MANAGEMENT20180806a:在发货单上加上页脚来显示页数。
#ZX_MANAGEMENT20180806b:将表头画出来，剩下的是从数据库中获取数据。
#ZX_MANAGEMENT20180806c:能够将数据库中字段信息读取并显示出来。在这个版本中使用del a[0]语法，删除列表的特定列。也使用了列表
#的拼接，然后统一将数据填写进PDF表格。
#ZX_MANAGEMENT20180806d:调整表头格式。
#ZX_MANAGEMENT20180812b:将AUI登录重新改为密码输入登录
#ZX_MANAGEMENT20180815a:在排产单查询界面增加逻辑判断，当使用超级管理员密码登录时默认为管理员。其余情况下访问数据库读取相关信息，此处应该改为用字典索引，快速查找。
#ZX_MANAGEMENT20180816a:修改数据库中字段名称，将State变为Group_chat_State
#ZX_MANAGEMENT20180819b:合入GQ版本。
#ZX_MANAGEMENT20180819c:发货界面点击确认发货按钮时能够更新零件、部件、组件合同在线表单的操作员，操作时间以及状态，点击取消按钮能够重新更新操作员操作时间和状态，在发货查询界面
#点击取消发货单时，能够在各个在线表单中重新更新这三个状态。
#ZX_MANAGEMENT20180820a：调整显示排样的命名格式，从那个数据库中具体读取到的详细信息显示，如果没有就说明没有该门型图片。将上个版本发货查询界面SetValue方法恢复成
#原来版本的Settable,后续调整查询界面的结构，将刷新函数放到表格类中。往250数据库中导入workorderquery表单。
#ZX_MANAGEMENT20180820b：FYF最新程序。
#ZX_MANAGEMENT20180820c：调整cnc加工中心板材利用率和加工时间限定在小数点后两位。重新调整发货单查询接口的刷新函数，现在拥挤面板上的显示还有一定的问题。
#ZX_MANAGEMENT20180820d：此版本发现一个订单有两个组件时画出的PDF有重复问题，调整后解决，但是并没有大量测试。在点击优先生产和恢复生产后调用刷新函数
#使得界面能够立即显示结果。
#ZX_MANAGEMENT20180820e：将cnc_task_list监控的表单时未完成状态从原来的10 变成现在的12。在工位工单表单中状态为已完成然而机器截单时间为空时加一个判断。
#ZX_MANAGEMENT20180821a：重新调整数据库中读取到的字段
#ZX_MANAGEMENT20180828a：合进FYF_pane.py和YLP_Pane.py和AUI.py
#ZX_MANAGEMENT20180829a：修改上个版本中，列表不清空导致画相同排产单的不同生产工艺单出现数据重复现象，将列表清空语句放到循环里面。
#ZX_MANAGEMENT20180829b：利用部件表单中same_part_num字段和组件号，显示相同门板的块数，但是开孔方向和特殊工艺还没有加上。
#ZX_MANAGEMENT20180829c：可以正确显示块数和备注信息，加上了开孔信息的备注判断。
#ZX_MANAGEMENT20180830a：修改压条工位、线条工位和cnc的PDF中一些小bug,依旧没有解决合并单元格问题。画PDF之前进行判断文件是否存在，存在的话直接加载，不存在再重新画。
#ZX_MANAGEMENT20180831a：修改线条工位、组装工位类型读取数据库中字段，读取hanhai_produce的info_element_type进行零件类型判断，用于组装工位
#ZX_MANAGEMENT20180831b：在特殊工艺中增加异形判断。
#ZX_MANAGEMENT20180901b:修改工位工单界面中今天的未完成工单在点击昨天，前天时依然存在但是不显示的问题。没有考虑未完成工单的时间和查询时间的比较。修改点击未完成工单时
#加工时间会显示之前点击的完成的工单的时间.
#ZX_MANAGEMENT20180902a:修改压条工位工单和组装工位工单相同类型的零件的合并问题。
#ZX_MANAGEMENT20180902b:在线条工位加上边型和数量和序号。
#ZX_MANAGEMENT20180902c:在CNC生产工艺单中加入对开判断。
#ZX_MANAGEMENT20180902d:解决reList报错问题，错误提示，reList在之前一将被命名了。主要是因为没有让解释器清楚变量是全局变量还是局部变量。变量需要声明，列表无需声明，但必须在同一层次。
#ZX_MANAGEMENT20180903a:在压条工位工单和组装工位工单中加入序号，解决重复填入数据问题。
#ZX_MANAGEMENT20180903b:在生产工艺单上的特殊备注中加上双面板的判断。
#ZX_MANAGEMENT20180903c:加上散板工位生产工艺单，并对完成库中的散板进行挑选，但是没有验证可能会出现错误。在读取排产单的时候增加散板的订单号。修改排产单查询界面详细信息显示表格的行标和列标。
#ZX_MANAGEMENT20180903d:增加鼠标右键双击的取消功能。
#ZX_MANAGEMENT20180904a:更改排产单查询界面布局，读取数据库中详细信息，将排产单的详细信息显示在界面上。
#ZX_MANAGEMENT20180904b:更改排产单界面查询条件筛选，增加按时间段查询。
#ZX_MANAGEMENT20180904c:更改排产单查询界面中PDF生成的条件判断，如果没有散板、压条、线条、组装，则不会重新绘制。
#ZX_MANAGEMENT20180904d:在发货单界面增加取消人和取消时间。增加右边的PDF窗口。如果发货状态为已发货，双击表格会在右边pdf表格中显示该发货单，如果找不到路径会报错。
#ZX_MANAGEMENT20180905a:修改工位工单工位图片显示的代码。
#ZX_MANAGEMENT20180907a:增加双面模压生产单，将散板打印按钮分开，放在不同的PDF界面。删除发货管理查询界面上的执行人和执行时间。增加如果取消人为空的判断。
#ZX_MANAGEMENT20180908a:解决生产工艺单重复问题（已测试），双面模压生产工艺单也有修改，但是没有测试。增加dvc.musicdata控件，但是大小还没有调整好。
#ZX_MANAGEMENT20180908b:在生产工艺单上的特殊工艺中增加玻璃的判断。
#ZX_MANAGEMENT20180908c:修改压条工位工单PDF，能够正确显示有该压条的工单和重复问题。双面模压工位也修改完成。修改压条组装工位的PDF读取条件判断。
#ZX_MANAGEMENT20180910b:修改返工工位PDF程序，经过测试能够正确的画出返工工位生产工艺单。
#ZX_MANAGEMENT20180910d:增加打印返工条码程序，经过验证可以正确打印。修改排产单查询界面中散板数量的显示方式，改为统计散板表单中的数量。
#ZX_MANAGEMENT20180913a:修改压条工位和线条工位出现的重复性错误，将通过部件号查找，直接改成通过组件号查找。
#ZX_MANAGEMENT20180913b:修改散板工位读取数据库的条件，加上限制条件。
#ZX_MANAGEMENT20180913c:能将文件生成在250，只需要配置文件路径，没有数据还没有测试。
#ZX_MANAGEMENT20180914a:修改排产单PDF所显示基材的名称为基材表单的字典，从中获取名称。
#ZX_MANAGEMENT20180915a:修改工位工单表单为待加工工单，修改排产单查询界面排产单批次包含订单表格初始值为两行一列，修改排产单显示表格中获得订单号的循环的逻辑。
#ZX_MANAGEMENT20180915b:在cnc,返工，双面PDF中加上列宽限制，解决组装工位套色工位重复现象。
#ZX_MANAGEMENT20180916a:合并单元格显示异形图片。
#ZX_MANAGEMENT20180916b:修改画表格线的范围，更改备注显示的空格问题。目前为止，纸单结束！！！加上管理员管理权限设置，将其所包含的类放在zx_pane.py中。经过测试没有问题。
#ZX_MANAGEMENT20180916c:修改订单号不在在线库时，log日志提示内容。原因可能因为未在order_order_online表单中找到该订单号。
#ZX_MANAGEMENT20180916d:增加设置密码对话框操作，能够修改密码。修改图片显示的照片
#ZX_MANAGEMENT20180917a:重新设置异形图片大小,加了一个判断。
#ZX_MANAGEMENT20180917c:增加底部状态栏在线订单面积和个数显示。
#ZX_MANAGEMENT20180917d:修改工位工单表单中图片显示的逻辑。路径下有中文时，使用os.path.exits(path)需要加上u,进行中文utf-8转码。
#ZX_MANAGEMENT20180918a:在AUI中加入时间事件检测当前是哪个界面，在ZX_Pane.py中修改时间事件的使用，修改散板打印单打印条码中的字段可以正常打印。
#ZX_MANAGEMENT20180920a:在AUI中设置时间的关闭和开始的方法，一开始的时候只开生产调度管理，当触发页面改变的事件时，当前页面时间打开，原来页面时间关闭。
#ZX_MANAGEMENT20180920b:在发货管理界面增加逻辑判断当合同支付定金未完成时不能发货。
#ZX_MANAGEMENT20180920c:zx修改AUI,将门店管理界面和报错管理界面的权限设置加上。
#ZX_MANAGEMENT20180920d:修改库管理界面，将musicdatactrl加上，数据显示正确，加上sizer之后解决了。删除ListCtrl.py
#ZX_MANAGEMENT20180920e:修改工位工单表单中右边toppanl显示信息，将控件以参数的方式传入表格类中，响应左击事件时显示这些统计信息。能够即时显示。
#ZX_MANAGEMENT20180921a:增加微信登录在排产查询界面的微信发布消息按钮。点击能够给cnc工位和原材料库管理工位的员工发消息。同时在AUI里修改。
#ZX_MANAGEMENT20180922a:在生产工艺单中增加五金件统计啊，经过自测成功。
#ZX_MANAGEMENT20180922b:在库管理界面中，当完成入库时，首先判断是否为月结和交齐尾款，如果没有显示为紫色，如果满足条件则按正常步骤执行。
#ZX_MANAGEMENT20180922c:在cnc界面，将超期两天的颜色有红色替换为紫色。
#ZX_MANAGEMENT20180924a:将微信发布对话框的TextCtrl风格变为多行。
#ZX_MANAGEMENT20180925a:将微信功能注释掉，修改打印Pdf时传入参数的条件，当排产单状态为已完成时传入参数。
#ZX_MANAGEMENT20180927a:将18毫米素板从排产管理查询界面去掉。
#ZX_MANAGEMENT20180927b:修改排产管理界面中大前天按钮的位置。
#ZX_MANAGEMENT20180928a:修改排产管理界面表格中删除一列，使得排产单状态变为第18列。修改之前未完全修改的生成发货单的存储位置。
#ZX_MANAGEMENT20180929a:修改排产单中只有散板时无法取消排产的操作。
#ZX_MANAGEMENT20180930c:修改条形码生成的位置，改成生成在C盘image下 。
#ZX_MANAGEMENT20181001a:在参数权限设置中增加衣利萍的财务管理属性页，能够进行权限设置，在排产单查询界面中的详细订单号表格显示中增加自适应列宽设置。
#ZX_MANAGEMENT20181001b:在发货单查询界面，建立的字典中增加工位为17的发货人，能够进行发货处理。
#ZX_MANAGEMENT20181004c:赵笑修改YLP中财务管理和人力资源管理的win拖动报错问题。
#ZX_MANAGEMENT20181005d:将生成条码改成调用exe,通过传参数生成条形码调用，已经能生成exe,此版本何如GQ最新程序。
#ZX_MANAGEMENT20181006a:在此版本中修改发货管理界面中的逻辑可以发货，但是没有加判断订单定金和是否月结的判断。修改FYF程序中读取零件类型表单中的element_id换为index.。
#ZX_MANAGEMENT20181006b:修改AUI中权限设置程序，将排产管理界面增加到权限管理中。
#ZX_MANAGEMENT20181006d:修改发货单界面中刷新时会清掉选中订单问题，不满足发货条件的不会进入发货单界面。
#ZX_MANAGEMENT20181007a:将库管理界面中的详细信息显示的字段对应起来。
#ZX_MANAGEMENT20181007b:将库管理界面中点击不同订单调用一次增加全部列的操作，致使数据重复，将添加行的程序放到构造函数中。
#ZX_MANAGEMENT20181007c:修改发货单查询界面，使得查询单显示今天的发货单。
#ZX_MANAGEMENT20181010a:在exe_barcode中加上try和except。何入冯永芳最新程序，在FYF_Pane.py中修改全局变量字典dict的命名
#解决由于模块导入命名问题导致一些模块不能调用导致出错的问题。通过修改变量名解决。这个版本为目前功能最新程序。
#ZX_MANAGEMENT20181010a:解决工位工单表无法恢复生产问题。
#ZX_MANAGEMENT20181014c:ZX将发货单生成到250上，在发货单查询界面直接加载250上的发货单，合入gq最新版本。
#ZX_MANAGEMENT20181018a:ZX修改发货查询界面中点击确认发货按钮弹出窗口再取消发货后对发货单表单中状态、取消人和取消日期的修改。
#ZX_MANAGEMENT20181018a:ZX在小车管理界面增加左面板。
#ZX_MANAGEMENT20181019a:zx修改小车管理界面，增加查询功能。
#ZX_MANAGEMENT20181024b:zx修改线条工位显示系信息，增加楣板罗马柱。
#ZX_MANAGEMENT20181025a:zx在工位工单界面增加生产调度分配的按钮，当4号机床出故障时，能够重新设置玻璃门的加工加床号。
#ZX_MANAGEMENT20181025b:zx在工位工单界面增加生产调度分配按钮的使能设置，改为有未接单工单就使能，相反就不使能，只要是4号机床单元格背景色
#设为灰色，但是逻辑依然不对，应该将玻璃门工单的单元格设为灰色。
#ZX_MANAGEMENT20181027a:修改附件生产工艺单，增加双排廊桥F,隔板收口线，在组装工位生产工艺单中增加开孔方向那一列，增加吊架酒杯，台面廊桥和圆弧廊桥，
#ZX_MANAGEMENT20181031b:修改排产单查询界面，将详细表格显示为批次里的订单改为显示批次里的订单和进散板订单。对异性图片的图片标注进行字符串转换
#将异性图片的高的大小变为原来的0.25倍。
#ZX_MANAGEMENT20181101b:修改排产单查询界面，在散板工艺单、线条工艺单、双面和返工工艺单上增加异形图片显示。
#ZX_MANAGEMENT20181101c:修改排产单查询界面，在生产工艺单中增加整套组件的信息。
#MANAGEMENT20181102b:在散板生产工艺单中增加整套组件信息。
#ZX_MANAGEMENT20181113a:修改把手和五金件的个数统计。
#ZX_MANAGEMENT20181113b:在生产工艺单中增加整套组件的特殊工艺(仿古),在散板生产工艺单中也增加整套组件的特殊工艺。增加基材字典中0对应''这个关键字
#ZX_MANAGEMENT20181113b:在生产工艺单中增加整套组件的特殊工艺(仿古),在散板生产工艺单中也增加整套组件的特殊工艺。增加基材字典中0对应''这个关键字
#ZX_MANAGEMENT20181114a:修改组装工位生产工艺单中数量显示位置错误.
#MANAGEMENT20181114a:修改发货控制界面中显示信息
#ZX_MANAGEMENT20181115a:修改生产工艺单中整套组件的数目统计方式,由原来的自己统计个数,变为直接读section_online表单中sec_num字段.
#ZX_MANAGEMENT20181116a:修改生产工艺单中打孔信息计算方式是整形还是浮点型.
#ZX_MANAGEMENT20181119a:重新调整发货查询界面中信息显示顺序.
#ZX_MANAGEMENT20181119b:在散板生产工艺单中增加数量一列,整套组件读取在线组件库中sec_num字段,其余默认为1.
#ZX_MANAGEMENT20181122a:将在散板工单中增加的数量一列去掉,在详细的生产工艺单中修改整套组件的数量的统计方式.
#ZX_MANAGEMENT20181122b:修改调用hcj生成条形码的程序.

import wx
import wx.dataview as dv
from wx.lib.ticker import Ticker
import wx.grid as gridlib
import MySQLdb
import datetime
import time
import os
import numpy as np
import random
import ftplib
import urllib2
import re
import itchat
import wxpy
import win32api
import win32event
import win32process
from ftplib import FTP as FTP
try:
    from agw import foldpanelbar as fpb
except ImportError:                     # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.foldpanelbar as fpb
#-------------------------------------------------------
from barcode.writer import ImageWriter
from barcode.codex import Code39
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('msyh', 'msyh.ttf'))
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer,Image,Table,TableStyle
from reportlab.pdfgen import canvas
from reportlab.platypus.frames import Frame
from reportlab.platypus.flowables import *
from reportlab.platypus.flowables import _ContainerSpace
from reportlab.lib.units import inch
from reportlab.platypus.paragraph import Paragraph
from reportlab.lib.utils import isSeq, encode_label, decode_label, annotateException, strTypes
from reportlab.lib.pagesizes import LETTER
import reportlab.lib.sequencer
try:
    set
except NameError:
    from sets import Set as set
import logging
#----------------------------------PDF表格使用的导入模块。
import shutil
import sys
reload(sys)
sys.setdefaultencoding('utf8')  #用于解决ascii和unicode之间的编码错误问题。
from compiler.ast import flatten
from MyFoldPanelBar import *
from ID_DEFINE import *
from FYF_Pane import *
# from PIL import Image

from SpeedMeter import Board_Storage_Ctrl_Panel
logger = logging.getLogger("reportlab.platypus")
WAIT_DELIVERY=125
WAIT_CONFIRM_DELIVERY=126
CONFIRM_DELIVERY=127
NO_RECEPTION=0
CREATE_CNC=12
DOOR_WORK_FISHED=15
ALL_WORK_FISHED=20
ERROR_TASK_LIST=1000
REPRINT_BARCODE=120
STORAGING=123
COMPLETED_STORAGE=125
BEING_OUT_OF_LIBRARY=127
OUT_OF_LIBRARY=128
FRAGMENTARY_BARCODE=120
BIG_PLACE_NUM=6
FIRST_COL_PLACE_NUM=11
EVERY_COL_SMALL_PLACE_NUM =17
SINGLE_DOUBLE=1
NO_SINGLE_DOUBLE=0
LAYER =15
BOARD=1
LMZ=3
MB=9
TOP_LINE=4
BELT_LINE=5
FOOT_LINE=6
TRUE_SHUTTER=12
CNC_WORKORDER_CANCEL=77
WAIT_SCHEDULE=0
COMPLETED_SCHEDULE=5
# ELEMENT_TYPE_ARC_LAYER=2
# FALSE_SHUTTER=13
GRID_DOOR=14
DOUBLE_COLOR_LAYER=18
REWORK=1005
CNC_POSITION=6
LAYER_POSITION=10
HOLE_POSITION=24
MATERIAL_POSITION=40
WAIT_WECHAT_SEND=0
COMPLETE_SEND=10
LOGIN =1
LOGOUT =-1
MANAGEMENT_POSITION=25
DELIVERY_POSITION=17
#------------------------------------
try:
    from wx.lib.pdfviewer import pdfViewer, pdfButtonPanel
    havePyPdf = True
except ImportError:
    havePyPdf = False
def Is_Database_Connect():
    try:
        global DB
        DB = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0], charset=charset)
        global DB1
        DB1 = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[2], charset=charset)
        global DB2
        DB2 = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[1], charset=charset)
        # global DB3
        # DB3 = MySQLdb.connect(host=Sort_server_ip, user=Sort_user_list[0], passwd=password, db=database[0],charset=charset)
        return True
    except:
        return False
# -----------------------------------------------------排产计划查询界面
class Scheduling_Query_Table(gridlib.GridTableBase):
    def __init__(self, data,field_name):
        gridlib.GridTableBase.__init__(self)
        self.data=data
        self.field_name=field_name
        self.dataTypes = [gridlib.GRID_VALUE_NUMBER,
            gridlib.GRID_VALUE_STRING,
            gridlib.GRID_VALUE_STRING,
            gridlib.GRID_VALUE_STRING,
            gridlib.GRID_VALUE_STRING,
            gridlib.GRID_VALUE_STRING,
            gridlib.GRID_VALUE_STRING,
            gridlib.GRID_VALUE_NUMBER,
            gridlib.GRID_VALUE_STRING,
            gridlib.GRID_VALUE_STRING,
            gridlib.GRID_VALUE_STRING,
            gridlib.GRID_VALUE_STRING,
            gridlib.GRID_VALUE_STRING,
            gridlib.GRID_VALUE_STRING,
            gridlib.GRID_VALUE_STRING,
            gridlib.GRID_VALUE_STRING,
            gridlib.GRID_VALUE_STRING,
            gridlib.GRID_VALUE_STRING,
            gridlib.GRID_VALUE_STRING,
            gridlib.GRID_VALUE_STRING,
            gridlib.GRID_VALUE_STRING,
        ]
    #--------------------------------------------------
    # required methods for the wxPyGridTableBase interface
    def GetNumberRows(self):
        return len(self.data)
    def GetNumberCols(self):
        return len(self.field_name)
    def IsEmptyCell(self, row, col):
        try:
            return not self.data[row][col]
        except IndexError:
            return True
    def GetValue(self, row, col):
        try:
            return self.data[row][col]
        except IndexError:
            return ''
    def SetValue(self, row, col, value):
        def innerSetValue(row, col, value):
            try:
                self.data[row][col] = value
            except IndexError:
                # add a new row
                self.data.append([''] * self.GetNumberCols())
                innerSetValue(row, col, value)
        innerSetValue(row, col, value)
    #--------------------------------------------------
    # Some optional methods
    def GetColLabelValue(self, col):
        return self.field_name[col]
    def GetTypeName(self, row, col):
        # pass
        return self.dataTypes[col]
    def CanGetValueAs(self, row, col, typeName):
        colType = self.dataTypes[col].split(':')[0]
        if typeName == colType:
            return True
        else:
            return False
    def CanSetValueAs(self, row, col, typeName):
        return self.CanGetValueAs(row, col, typeName)
class Scheduling_Query_Grid(gridlib.Grid):
    def __init__(self, parent,log,drawPDF,detailed_query_grid,layer_PDF,line_PDF,assembly_PDF,scattered_PDF,double_sided_PDF,rework_PDF):
        gridlib.Grid.__init__(self, parent, -1)
        self.log=log
        self.drawPDF=drawPDF
        self.detailed_query_grid=detailed_query_grid
        self.layer_PDF=layer_PDF
        self.line_PDF=line_PDF
        self.assembly_PDF=assembly_PDF
        self.scattered_PDF=scattered_PDF
        self.double_sided_PDF=double_sided_PDF
        self.rework_PDF=rework_PDF
        self.data = []
        self.operator_id=''
        # self.date = datetime.datetime.now()
        self.start_date = datetime.date.today().strftime('%Y-%m-%d')
        self.end_date = datetime.date.today().strftime('%Y-%m-%d')
        self.field_name = ['','排产单编号','创建时间', '排产日期', '制单员', '订单数', '排产面积', '批次数', 'CNC工单总数', '玻璃门数量', '散板数量',
                           '异形数量', '罗马柱数量', '楣板数量', '压条面积', '仿古面积', '18mm单面板', '18mm菱格板', '排产单状态', '取消日期', '取消操作员',]
        self.staff_inform = {}
        try:
            if Is_Database_Connect():
                cursor = DB1.cursor()
                cursor.execute("select `Job_id` ,`Name` from `info_staff_new` where `Position`=25 ")
                record = cursor.fetchall()
                for i in range(len(record)):
                    self.staff_inform[record[i][0]] = record[i][1]
            else:
                return
        except:
            self.log.WriteText("天外天系统正在运行ZX_Pane.py,在Scheduling_Query_Grid（）的构造函数中读取info_staff_new表单出现错误，请检查！\r\n")
        self.MyRefresh()
        self.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.OnLeftClick)
        self.Bind(gridlib.EVT_GRID_CELL_RIGHT_DCLICK, self.OnRightDClick)
        self.EnableEditing(False)  # 使得整个表格都不使能
        # self.timer = wx.PyTimer(self.Refresh)
        # self.timer.Start(10000)
    def OnLeftClick(self,event):
        row = event.GetRow()  # 获得鼠标单击的单元格所在的行
        # col = event.GetCol()
        total_batch = self.GetCellValue(row, 7)
        workorder_id = self.GetCellValue(row, 1)
        workorder_state = self.GetCellValue(row, 18)
        if Is_Database_Connect():
            self.order_list = []
            order_list_total = []
            spare_order = []
            cursor = DB.cursor()
            cursor.execute(
                "SELECT `Spare_order_id` FROM `work_cnc_workorder_query` WHERE `Workorder_id`='%s'" % (workorder_id))
            spare_order_information = cursor.fetchone()
            if spare_order_information != None and spare_order_information[0] != '0':
                spare_split_list = spare_order_information[0].split(',')
                spare_order.append(spare_split_list)
            else:
                pass
            for i in range(int(total_batch)):
                str1 = 'Batch_including_order_' + str(i + 1)
                cursor=DB.cursor()
                cursor.execute(
                    "SELECT `%s` FROM `work_cnc_workorder_query` WHERE `Workorder_id`='%s'" % (str1, workorder_id))
                order_information = cursor.fetchone()
                split_list = order_information[0].split(',')
                order_list_total.append(split_list)
            order_list=order_list_total+spare_order
            self.order_list=flatten(order_list)#将二维列表转换成一维列表
            # self.order_list=list(set(order_list))#去重
            self.detailed_query_grid.SetGridValue(order_list_total)
            if workorder_state == '已完成':
                self.drawPDF.DrawTable_PDF(self.order_list,workorder_id)
                self.layer_PDF.DrawTable_PDF(self.order_list, workorder_id)
                self.line_PDF.DrawTable_PDF(self.order_list, workorder_id)
                self.line_PDF.SetValue(self.order_list)
                self.assembly_PDF.DrawTable_PDF(self.order_list, workorder_id)
                self.scattered_PDF.DrawTable_PDF(self.order_list, workorder_id)
                self.scattered_PDF.SetValue(self.order_list)
                self.double_sided_PDF.DrawTable_PDF(self.order_list, workorder_id)
                self.double_sided_PDF.SetValue(self.order_list)
                self.rework_PDF.DrawTable_PDF(self.order_list, workorder_id)
        else:
            return
        event.Skip()
    def OnRightDClick(self,event):
        row = event.GetRow()  # 获得鼠标单击的单元格所在的行
        cnc_schedule_state = self.GetCellValue(row, 18)
        total_batch = self.GetCellValue(row, 7)
        workorder_id = self.GetCellValue(row, 1)
        Cancel_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if cnc_schedule_state== '已完成':
            dlg = wx.MessageDialog(self, '此排产单已经排产完成，无法取消！',
                                   '警告！',
                                   wx.OK | wx.ICON_INFORMATION
                                   # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                                   )
            dlg.ShowModal()
        elif cnc_schedule_state=='等待排产':
            dlg = wx.MessageDialog(self, '此排产单排产类型为计划排产，当前状态为等待排产，请确认是否取消此排产单！',
                                   '警告！',
                                   wx.OK | wx.ICON_INFORMATION | wx.CANCEL
                                   # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                                   )
            val = dlg.ShowModal()
            if val == wx.ID_OK:
                if Is_Database_Connect():
                    order_list_total = []
                    spare_order = []
                    cursor = DB.cursor()
                    cursor.execute(
                        "UPDATE `work_cnc_workorder_query` set `State`='%s',`Cancel_time`='%s',`Cancel_operator_id`='%s' WHERE `Workorder_id`='%s'" % (
                            CNC_WORKORDER_CANCEL, Cancel_time, self.operator_id, workorder_id))
                    cursor.execute(
                        "SELECT `Spare_order_id` FROM `work_cnc_workorder_query` WHERE `Workorder_id`='%s'" % ( workorder_id))
                    spare_order_information = cursor.fetchone()
                    if spare_order_information[0] != None and spare_order_information[0] != '0':
                        spare_split_list = spare_order_information[0].split(',')
                        spare_order.append(spare_split_list)
                    else:
                        pass
                    for i in range(int(total_batch)):
                        str1 = 'Batch_including_order_' + str(i + 1)
                        cursor=DB.cursor()
                        cursor.execute("SELECT `%s` FROM `work_cnc_workorder_query` WHERE `Workorder_id`='%s'" % (str1, workorder_id))
                        order_information = cursor.fetchone()
                        split_list = order_information[0].split(',')
                        order_list_total.append(split_list)
                    order_list = order_list_total + spare_order
                    order_list_one = flatten(order_list)  # 将二维列表转换成一维列表
                    for row in range(len(order_list_one)):
                        cursor = DB.cursor()
                        cursor.execute( "UPDATE `order_order` set `State`='%s' WHERE `Order_id`='%s'" % (STATE_SPLIT_ORDER,order_list_one[row]))
                    DB.commit()
                    self.MyRefresh()
                else:
                    return
            else:
                pass
        elif cnc_schedule_state ==  '已取消':
            dlg = wx.MessageDialog(self, '此排产单已经被取消！',
                                   '警告！',
                                   wx.OK | wx.ICON_INFORMATION
                                   # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                                   )
            dlg.ShowModal()
        else:
            pass
        event.Skip()
    def MyRefresh(self):
        self.data = []
        self.order_list = []
        order_list_total = []
        spare_order = []
        spare_num=0
        try:
            if Is_Database_Connect():
                cursor=DB.cursor()
                cursor.execute("select `Workorder_id`,`Create_time`,`Schedule_date`,`Operator_id`,`Total_order_num`,`Total_order_area`,`Total_batch_num`,`Workorder_num`,`Glass_door_num` ,`Scattered_plate_num`,`Abnormity_plate_num`,`Roman_column_num` ,`Fascia_board_num`,`Bar_area`,`Archaize_area`,`Single_18_board_num`,`Rhombic_18_board_num`,`State` ,`Cancel_time`,`Cancel_operator_id` from `work_cnc_workorder_query` where `Schedule_date`>='%s' and `Schedule_date`<='%s' ORDER BY `Index` DESC " %(self.start_date,self.end_date))
                record=cursor.fetchall()
                cursor.execute(
                    "select `Order_Id` from `work_cnc_before_layout_temporary` where 1 ")
                list_count_record = cursor.fetchall()
                for i in range(len(record)):
                    cursor = DB.cursor()
                    cursor.execute(
                        "SELECT `Spare_order_id` FROM `work_cnc_workorder_query` WHERE `Workorder_id`='%s'" % (record[i][0]))
                    spare_order_information = cursor.fetchone()
                    if spare_order_information != None and spare_order_information[0] != '0':
                        spare_split_list = spare_order_information[0].split(',')
                        spare_order.append(spare_split_list)
                    else:
                        pass
                    for num in range(int(record[i][6])):
                        str1 = 'Batch_including_order_' + str(num + 1)
                        cursor = DB.cursor()
                        cursor.execute(
                            "SELECT `%s` FROM `work_cnc_workorder_query` WHERE `Workorder_id`='%s'" % (str1, record[i][0]))
                        order_information = cursor.fetchone()
                        split_list = order_information[0].split(',')
                        order_list_total.append(split_list)
                    order_list = order_list_total + spare_order
                    self.order_list = flatten(order_list)  # 将二维列表转换成一维列表
                    for num in range (len(list_count_record)):
                        if list_count_record[num][0] in self.order_list:
                            spare_num+=1
                    if record[i][3]=='0':
                        staff_name='管理员'
                    else:
                        staff_name=self.staff_inform[record[i][3]]
                    if record[i][17]==WAIT_SCHEDULE:
                        cnc_workorder_list_state='等待排产'
                    elif record[i][17]==COMPLETED_SCHEDULE:
                        cnc_workorder_list_state = '已完成'
                    elif record[i][17] == CNC_WORKORDER_CANCEL:
                        cnc_workorder_list_state = '已取消'
                    else:
                        cnc_workorder_list_state=''
                    if record[i][19] == None:
                        operator_name=''
                    elif record[i][19] == '0':
                        operator_name='管理员'
                    else:
                        operator_name = self.staff_inform[record[i][20]]
                    inform = [(i+1),record[i][0],record[i][1].strftime('%Y-%m-%d %H:%M:%S'),record[i][2],staff_name,record[i][4],record[i][5],record[i][6],record[i][7],record[i][8],spare_num,
                              record[i][10], record[i][11], record[i][12], record[i][13], record[i][14], record[i][15], record[i][16],cnc_workorder_list_state,record[i][18],operator_name]
                    self.data.append(inform)
            else:
                return
        except:
            self.log.WriteText(
                "天外天系统正在ZX_Pane.py执行读取数据库work_cnc_workorder_query表单操作，连接数据库是出现错误，请检查   \r\n")
        self.table = Scheduling_Query_Table(self.data,self.field_name)  # 自定义表网格
        self.SetTable(self.table, True)
        self.SetRowLabelSize(0)
        self.SetMargins(0,0)
        self.AutoSizeColumns(False)
        self.DisableDragColSize()
        self.DisableDragRowSize()
    def SetValue(self,start_date,end_date):
        self.start_date=start_date
        self.end_date=end_date
    def GetOperatorId(self,operator_id):
        self.operator_id=operator_id
class Scheduling_Detailed_Query_Grid(gridlib.Grid):
    def __init__(self, parent, log):
        gridlib.Grid.__init__(self, parent, -1)
        self.log = log
        self.moveTo = None
        self.CreateGrid(2, 1)  # , gridlib.Grid.SelectRows)
        # self.SetRowLabelSize(25)
        self.SetRowLabelValue(0,'批次1')
        self.SetRowLabelValue(1,'批次2')
        self.SetColLabelValue(0,'订单1')
        self.EnableEditing(False)
        self.SetColLabelAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)
        self.DisableDragColSize()
        self.DisableDragRowSize()
        # self.AutoSizeColumns(True)#表格列自适应
        self.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.OnLeftClick)
    def OnLeftClick(self,evt):
        row = evt.GetRow()  # 获得鼠标单击的单元格所在的行
        col = evt.GetCol()
        text = self.GetCellValue(row, col)
        evt.Skip()
    def SetGridValue(self,order_list_total):
        self.order_list_total=order_list_total
        order_len=[]
        now_rows = self.GetNumberRows()
        now_cols = self.GetNumberCols()
        for i in range(len(self.order_list_total)):
            order_len.append(len(self.order_list_total[i]))
        if len(order_len)!=0:
            Max_col = max(order_len)
        else:
            Max_col=0
        if len(self.order_list_total) > now_rows:
            for j in range(len(self.order_list_total) - now_rows):
                self.AppendRows(numRows=1)
        elif len(self.order_list_total) < now_rows:
            for j in range(now_rows - len(self.order_list_total)):
                self.DeleteRows(numRows=1)
        if Max_col > now_cols:
            for j in range(Max_col - now_cols):
                self.AppendCols(numCols=1)
        elif Max_col < now_cols:
            for j in range(now_cols - Max_col):
                self.DeleteCols(numCols=1)
        # RowLable=a()#数据库中都出来的批次数目通过传值的方式传进来。
        now_row = self.GetNumberRows()
        now_col = self.GetNumberCols()
        for i in range(now_row):  # 用来填写所有表头信息
            RowName='批次'+str(i+1)
            self.SetRowLabelValue(i, RowName)
        for i in range(now_col):  # 用来填写所有表头信息
            ColName='订单'+str(i+1)
            self.SetColLabelValue(i, ColName)
        for i in range(len(self.order_list_total)):  # 填数据
            for j in range(order_len[i]):
                self.SetCellValue(i, j, self.order_list_total[i][j])
        self.AutoSizeColumns(True)
class FooterCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []
        # self.order_inform=order_inform
    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()
    def save(self):
        page_count = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_canvas(page_count)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)
    def SetValue(self,order_inform):
        self.order_inform=order_inform
    def draw_canvas(self, page_count):
        # if Is_Database_Connect():
        #     order_list = []
        #     order_list_total = []
        #     for i in range(int(total_batch)):
        #         self.log.WriteText(str(total_batch))
        #         str1 = 'Batch_including_order_' + str(i + 1)
        #         cursor=DB.cursor()
        #         cursor.execute(
        #             "SELECT `%s` FROM `work_cnc_workorder_query` WHERE `Workorder_id`='%s'" % (str1, workorder_id))
        #         order_information = cursor.fetchone()
        #         split_list = order_information[0].split(',')
        #         order_list_total.append(split_list)
        #         order_list=flatten(order_list_total)#将二维列表转换成一维列表
        page = "第%s页/共%s页" % (self._pageNumber, page_count)
        # x = 128
        self.saveState()
        # self.setStrokeColorRGB(0, 0, 0)
        # self.setLineWidth(0.5)
        # self.line(66, 78, LETTER[0] - 76, 78)
        self.setFont('msyh', 9)
        # self.setFont('Times-Roman', 10)
        self.drawString(4 * inch, 0.75 * inch, page)
        # self.drawString(LETTER[0]-x, 65, page)
        self.restoreState()
class Scheduling_Query_PDF(wx.Panel):
    def __init__(self, parent,log):
        wx.Panel.__init__(self, parent, -1)
        self.log=log
        self.order_list=''
        self.a=1
        # self.Scheduling_Query_Layer_PDF=Scheduling_Query_Layer_PDF(self,self.log)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        self.buttonpanel = pdfButtonPanel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        vsizer.Add(self.buttonpanel, 0,wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT | wx.TOP, 5)
        self.viewer = pdfViewer(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL | wx.VSCROLL | wx.SUNKEN_BORDER)
        vsizer.Add(self.viewer, 1, wx.GROW | wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)
        # self.loadbutton = wx.Button(self, wx.ID_ANY, "打印散板条码", wx.DefaultPosition, wx.DefaultSize, 0)
        # vsizer.Add(self.loadbutton, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.SetSizer(vsizer)
        self.SetAutoLayout(True)
        self.buttonpanel.viewer = self.viewer
        self.viewer.buttonpanel = self.buttonpanel
        #self.DrawTable_PDF()  # 画pdf表
        wx.BeginBusyCursor()
        #self.viewer.LoadFile('order_pdf.pdf')
        wx.EndBusyCursor()
        # self.Bind(wx.EVT_BUTTON, self.OnLoadButton, self.loadbutton)
    def DrawTable_PDF(self,order_inform,workorder_id):
        try:
            f = os.path.exists("C:\Production_Process_PDF\\")  # 用于判断在D盘中是否存在delivery_list_history文件夹，如果不在在这个路径下新建文件夹。
            if not f:
                os.mkdir("C:\Production_Process_PDF\\")  # 新建文件夹
            filename_server_name=u"\\\\192.168.31.250\\Production_Process_PDF\\"+ str(workorder_id) + '_cnc.pdf'
            filename_local_name=u"C:\\Production_Process_PDF\\" + str(workorder_id) +'_cnc.pdf'
            is_exist_file = os.path.exists("\\\\192.168.31.250\\Production_Process_PDF\\"+ str(workorder_id) + '_cnc.pdf')
            if is_exist_file:
                shutil.copyfile(filename_server_name, filename_local_name)
                self.viewer.LoadFile("C:\\Production_Process_PDF\\" + str(workorder_id) + '_cnc.pdf')
            else:
                story = []
                stylesheet = getSampleStyleSheet()
                normalStyle = stylesheet['Normal']
                today = datetime.datetime.now()
                formatted_today = today.strftime('%Y.%m.%d')
                formatted1_today = today.strftime('%H:%M')
                #############################生成条形码
                if Is_Database_Connect():
                    cursor = DB.cursor()
                    cursor.execute("select `Order_id` from `order_order_online` where 1 " )
                    order_online=cursor.fetchall()
                    # list(flatten(order_online))
                    Judgment=set(list(flatten(order_inform))).issubset(set(list(flatten(order_online))))
                    if Judgment == True:
                        total_inform=0
                        total_inform+=(len(order_inform))
                        cursor = DB2.cursor()
                        base_material = {0:'无'}
                        cursor.execute("select `Index`,`Base_material_name` from `info_base_material_charge` where 1 ")
                        base_name_record=cursor.fetchall()
                        for row in range(len(base_name_record)):
                            base_material[base_name_record[row][0]]=base_name_record[row][1]
                        if len(order_inform)!=0:
                            for i in range(len(order_inform)):
                                row = 0
                                part_inform = []
                                part_gropby_inform = []
                                hardware_tem_detail=[]
                                hardware_detail=[]
                                component_tem_detail=[]
                                component_detail=[]
                                cursor = DB.cursor()
                                cursor.execute("select `Brand`,`Dealer` ,`Customer_name`,`remarks`,`remarkimage`,`Order_area`,`Part_num`,`Door_num`,`Top_line_num`,`Waist_line_num`,`Foot_line_num`,`Rome_column_num`,`Lintel_num`,`Contract_id` from `order_order_online` where `Order_id`='%s' " % order_inform[i])
                                header_data=cursor.fetchone()
                                cursor.execute("select `Index_of_base_material_thickness`,`Sec_color` ,`Sec_series`,`Sec_id` from `order_section_online` where `Order_id`='%s' " % order_inform[i])
                                sec_inform = cursor.fetchall()
                                cursor = DB.cursor()
                                cursor.execute("select `Order_account_number` from `order_contract_internal` where `Contract_id`='%s' " % header_data[13])
                                data = cursor.fetchone()
                                cursor = DB1.cursor()
                                cursor.execute("select `realname` from `order_user` where `Id`='%s' " % data[0])
                                order_person=cursor.fetchone()
                                cursor = DB.cursor()
                                cursor.execute(
                                    "select `Board_type`,`Board_height`,`Board_width` from `order_element_online` where `Order_id`='%s' and (`Element_type_id`='%s' or `Element_type_id`='%s' or `Element_type_id`='%s' or `Element_type_id`='%s' or `Element_type_id`='%s' or `Element_type_id`='%s')  " % (
                                    order_inform[i], 7, 8, 10, 11, 16, 17))
                                hardware_inform = cursor.fetchall()
                                cursor.execute(
                                    "select `Index_of_base_material_thickness`,`Sec_color`,`Sec_series`,`Sec_edge`,`Sec_height`,`Sec_length`,`Sec_width`,`Archaize` from `order_section_online` where `Order_id`='%s' and `Sec_type`='%s' " % (
                                    order_inform[i], '1'))
                                component_inform = cursor.fetchall()
                                if header_data[2]==None:
                                    customer='无'
                                else:
                                    customer =header_data[2]
                                code_img=exe_Barcode(order_inform[i])
                                rpt_title = '<para autoLeading="off" fontSize=24 align=center><b><font face="msyh">%s膜压</font></b><br/><br/><br/></para>' % \
                                            header_data[0]
                                story.append(Paragraph(rpt_title, normalStyle))
                                component_data = [['', '', '', '', '', '', '', '', '', '', ''],
                                                  ['', formatted_today, '', formatted1_today ,'', '', '', '', '', '',''],
                                                  ['', '客户名称:', '', str(header_data[1]), '', '', '', '', '', '', order_inform[i]],
                                                  ['', '终端客户:', '', str(customer), '', '', '', '', '', '', code_img],
                                                  ['序号', '基材', '颜色', '套系', '门型', '边型', '高', '宽','深度','数量', '打孔', '特殊工艺']]
                                for m in range(len(sec_inform)):
                                    cursor = DB.cursor()
                                    cursor.execute(
                                        "select `Door_type`,`Edge_type`,`Door_height` ,`Door_width`,`Open_way`,`Door_color`,`Index_of_base_material_thickness`,`Straightening_device`,`Double_color`,`Archaize`,`Hole`,`heterotype`,`Single_double`,`Glass` from `order_part_online` where `Sec_id`='%s' and `Element_type_id`<>'%s'and `Element_type_id`<>'%s'and `Element_type_id`<>'%s'  " %(sec_inform[m][3],11,7,8))
                                    part_detail_inform = cursor.fetchall()
                                    if part_detail_inform != ():
                                        for j in range(len(part_detail_inform)):
                                            if 'MY'in part_detail_inform[j][0]:
                                                Door_type=part_detail_inform[j][0].split('_')
                                                # Door_type_split=Door_type[-1]
                                                number=Door_type[1]
                                                number_style=number[-1]
                                                if number_style=='B':
                                                    style='单拱B型'
                                                elif number_style=='C':
                                                    style = '肩膀拱C型'
                                                elif number_style=='D':
                                                    style = '多拱D型'
                                                elif number_style=='E':
                                                    style = '复杂拱E型'
                                                else:
                                                    style='普通A型'
                                                Door_type_split=style+Door_type[-1]
                                            else:
                                                Door_type_split=part_detail_inform[j][0]
                                            if part_detail_inform[j][7]==1:
                                                remark1 = '拉直器'+'\n'
                                            else:
                                                remark1=''
                                            if part_detail_inform[j][8]!=None:#套色
                                                remark2 = part_detail_inform[j][8]+'\n'
                                            else:
                                                remark2=''
                                            if part_detail_inform[j][9]!=None:#仿古
                                                remark3 = part_detail_inform[j][9]+'\n'
                                            else:
                                                remark3=''
                                            if part_detail_inform[j][11] == 0:
                                                remark5 = ''
                                            else:
                                                remark5 = '异形'+'\n'
                                            if part_detail_inform[j][12] == 0:
                                                remark6 = ''
                                            else:
                                                remark6 = '双面板'+'\n'
                                            if part_detail_inform[j][13] == None or part_detail_inform[j][13] == 0:
                                                remark7 = ''
                                            else:
                                                remark7 = part_detail_inform[j][13]+'\n'
            #----------------------------------------------------------------------开孔具体信息计算规则
                                            # if part_detail_inform[4] != '不开' and part_detail_inform[2]<1000:
                                            if part_detail_inform[j][2]<1000:
                                                hole=str(120)+'/'+str(0)+'/'+str(0)+'/'+str(0)+'/'+str(120)
                                            elif part_detail_inform[j][2]>=1000 and part_detail_inform[j][2]<1530:
                                                if part_detail_inform[j][2]%2==0:
                                                    hole=str(120)+'/'+str(0)+'/'+str(int(part_detail_inform[j][2]*0.5))+'/'+str(0)+'/'+str(120)
                                                else:
                                                    hole = str(120)+ '/'+ str(0)+'/'+ str(float(part_detail_inform[j][2] * 0.5)) + '/'+ str(0)+'/'+ str(120)
                                            elif part_detail_inform[j][2]>=1530 and part_detail_inform[j][2]<1645:
                                                hole=str(120)+'/'+str(550)+'/'+str(0)+'/'+str(int(part_detail_inform[j][2]-550))+'/'+str(120)
                                            elif part_detail_inform[j][2]>=1645 and part_detail_inform[j][2]<1800:
                                                hole=str(120)+'/'+str(600)+'/'+str(0)+'/'+str(int(part_detail_inform[j][2]-600))+'/'+str(120)
                                            elif part_detail_inform[j][2]>=1800 and part_detail_inform[j][2]<1900:
                                                hole=str(120)+'/'+str(650)+'/'+str(0)+'/'+str(int(part_detail_inform[j][2]-650))+'/'+str(120)
                                            elif part_detail_inform[j][2]>=1900 and part_detail_inform[j][2]<2100:
                                                hole=str(120)+'/'+str(700)+'/'+str(0)+'/'+str(int(part_detail_inform[j][2]-700))+'/'+str(120)
                                            elif part_detail_inform[j][2]>=2100 and part_detail_inform[j][2]<2250:
                                                hole=str(120)+'/'+str(750)+'/'+str(0)+'/'+str(int(part_detail_inform[j][2]-750))+'/'+str(120)
                                            elif part_detail_inform[j][2]>=2250 and part_detail_inform[j][2]<2300:
                                                hole=str(120)+'/'+str(800)+'/'+str(0)+'/'+str(int(part_detail_inform[j][2]-800))+'/'+str(120)
                                            elif part_detail_inform[j][2]>=2300:
                                                hole=str(120)+'/'+str(850)+'/'+str(0)+'/'+str(int(part_detail_inform[j][2]-850))+'/'+str(120)
                                            else:
                                                hole='尺寸错误'
                                            if part_detail_inform[j][4] != '不开' and part_detail_inform[j][10] != None and hole != part_detail_inform[j][10]:
                                                remark4=part_detail_inform[j][10]+'\n'
                                            else:
                                                remark4 = ''
                                            remark_total=remark1+remark2+remark3+remark5+remark6+remark7+remark4#增加备注
                                            part_compera_inform=[base_material[part_detail_inform[j][6]], part_detail_inform[j][5], sec_inform[m][2],Door_type_split,part_detail_inform[j][1],part_detail_inform[j][2],part_detail_inform[j][3],part_detail_inform[j][4],remark_total]
                                            part_gropby_inform.append(part_compera_inform)
                                            part_detail=['',base_material[part_detail_inform[j][6]], part_detail_inform[j][5], sec_inform[m][2],Door_type_split,part_detail_inform[j][1],part_detail_inform[j][2],part_detail_inform[j][3],'','',part_detail_inform[j][4],remark_total]
                                            part_inform.append(part_detail)
                                        for j in range(len(part_inform)):
                                            count = 0
                                            for k in range(len(part_inform)):
                                                if part_gropby_inform[k] == part_gropby_inform[j]:
                                                    count = count + 1
                                                    part_inform[j][9] = count
                                    # else:
                                    #     continue
                                if hardware_inform!= ():
                                    for j in range(len(hardware_inform)):
                                        hardware_tem=['','','','',hardware_inform[j][0],'',hardware_inform[j][1],hardware_inform[j][2],'','','','']
                                        hardware=[hardware_inform[j][0],hardware_inform[j][1],hardware_inform[j][2]]
                                        hardware_tem_detail.append(hardware)
                                        hardware_detail.append(hardware_tem)
                                    for j in range(len(hardware_inform)):
                                        count1 = 0
                                        for k in range(len(hardware_inform)):
                                            if hardware_tem_detail[k] == hardware_tem_detail[j]:
                                                count1 = count1 + 1
                                                hardware_detail[j][9] = count1
                                # else:
                                #     continue
                                if component_inform!= ():
                                    for j in range(len(component_inform)):
                                        remark_component=component_inform[j][7]
                                        component_tem=['', base_material[component_inform[j][0]], component_inform[j][1],component_inform[j][2],'',component_inform[j][3],component_inform[j][4],component_inform[j][5],component_inform[j][6],'','',remark_component]
                                        component=[base_material[component_inform[j][0]],component_inform[j][1],component_inform[j][2],component_inform[j][3],component_inform[j][4],component_inform[j][5],component_inform[j][6],remark_component]
                                        component_tem_detail.append(component)
                                        component_detail.append(component_tem)
                                    for j in range(len(component_inform)):
                                        count1 = 0
                                        for k in range(len(component_detail)):
                                            if component_tem_detail[k] == component_tem_detail[j]:
                                                count1 = count1 + 1
                                                component_detail[j][9] = count1
                                # # else:
                                # #     continue
                                part_total_inform=part_inform+hardware_detail+component_detail
                                reList = list( set([tuple(t) for t in part_total_inform]))  # 二维列表的子元素也是列表，将子元素的一维列表转换成元组，然后使用set()去重
                                reList = [list(v) for v in reList]  # 将二维列表转换成元组
                                reList.sort(key=part_total_inform.index)  # 按照二维列表的索引值对去重之后得列表进行排序。
                                for j in range(len(reList)):
                                    reList[j][0] = j + 1
                                component_data += (reList)
                                if header_data[4] != None:
                                    special_shaped = header_data[4].split('&&')
                                    downloadpic(special_shaped, order_inform[i])
                                    row=len(special_shaped)
                                    for p in range(1,len(special_shaped)+1):
                                        special_shaped_image=Image("C:\Special_Shaped\\"+str(order_inform[i])+"_"+str(p)+".png")
                                        if special_shaped_image.imageHeight>685 or special_shaped_image.imageWidth>439:
                                            special_shaped_image.drawHeight=special_shaped_image.imageHeight*0.25
                                            special_shaped_image.drawWidth=special_shaped_image.imageWidth*0.3
                                        else:
                                            special_shaped_image.drawHeight = special_shaped_image.imageHeight
                                            special_shaped_image.drawWidth = special_shaped_image.imageWidth
                                        component_data += [['图'+str(p),'','','','',special_shaped_image,'','','','','','']]
                                component_table = Table(component_data,colWidths=[22,40,56,46,114,88,35,35,27,27,27,75])
                                component_table.setStyle(TableStyle([
                                ('FONTNAME',(0,0),(-1,-1),'msyh'),#字体
                                ('FONTSIZE',(0,0),(-1,-1),10),#字体大小
                                # ('SPAN',(0,-1),(-1,-row)),#合并第一行前三列
                                # ('BACKGROUND',(0,0),(-1,0), colors.lightskyblue),#设置第一行背景颜色
                                # ('SPAN',(1,h),(1,h1)), #合并第一行后两列
                                # ('SPAN', (2, h), (2, h1)),  # 合并第一行后两列
                                # ('SPAN', (3, h), (3, h1)),  # 合并第一行后两列
                                # ('SPAN', (4, h), (4, h1)),  # 合并第一行后两列
                                ('ALIGN',(0,0),(-1,-1),'CENTER'),#对齐
                                # ('ALIGN',(-1,0),(-1,4),'LEFT'),#对齐
                                ('ALIGN',(0,0),(0,3),'RIGHT'),#对齐
                                ('ALIGN',(1,0),(1,3),'LEFT'),#对齐
                                ('ALIGN',(-1,0),(-2,5),'RIGHT'),#对齐
                                ('VALIGN',(0,0),(-1,-1),'MIDDLE'),  #对齐
                                # ('LINEBEFORE',(0,0),(0,-1),0.1,colors.grey),#设置表格左边线颜色为灰色，线宽为0.1
                                #('TEXTCOLOR',(0,1),(-2,-1),colors.royalblue),#设置表格内文字颜色
                                ('TEXTCOLOR',(-1,-1),(-1,-1),colors.black),#设置表格内文字颜色
                                ('GRID',(0,4),(-1,(-row-1)),1,colors.black),#设置表格框线为黑色，线宽为0.5
                                # ('GRID',(0,-1),(-1,-row),1,colors.white),#设置表格框线为红色，线宽为0.5
                                ]))
                                story.append(component_table)
                                story.append(Spacer(0, 0.2 * inch))
                                rpt_total = '<para autoLeading="off" fontSize=10 ><b><font face="msyh">订单面积：%s </font></b>&nbsp;&nbsp;&nbsp</para>' \
                                            '<para autoLeading="off" fontSize=10 ><b><font face="msyh">部件总数：%s </font></b>&nbsp;&nbsp;&nbsp</para>' \
                                            '<para autoLeading="off" fontSize=10 ><b><font face="msyh">门板总数：%s </font></b>&nbsp;&nbsp;&nbsp</para>' \
                                            '<para autoLeading="off" fontSize=10 ><b><font face="msyh">顶线总数：%s </font></b><br/><br/></para>' \
                                            '<para autoLeading="off" fontSize=10 ><b><font face="msyh">腰线总数：%s </font></b>&nbsp;&nbsp;&nbsp</para>' \
                                            '<para autoLeading="off" fontSize=10 ><b><font face="msyh">脚线总数：%s </font></b>&nbsp;&nbsp;&nbsp</para>' \
                                            '<para autoLeading="off" fontSize=10 ><b><font face="msyh">罗马柱数：%s </font></b>&nbsp;&nbsp;&nbsp</para>' \
                                            '<para autoLeading="off" fontSize=10 ><b><font face="msyh">楣板总数：%s </font></b><br/><br/></para>' \
                                            '<para autoLeading="off" fontSize=10 ><b><font face="msyh">下 单 员：%s </font></b>&nbsp;&nbsp;&nbsp</para>' % (
                                                header_data[5], header_data[6], header_data[7], header_data[8],
                                                header_data[9], header_data[10], header_data[11], header_data[12], order_person[0])
                                story.append(Paragraph(rpt_total, normalStyle))
                                story.append(Spacer(0, 0.2 * inch))
                                header_data_list = list(header_data)
                                if header_data[3]==None:
                                    header_data_list[3]='无'
                                else:
                                    header_data_list[3]
                                remarks = '<para autoLeading="off" fontSize=15 align=center><b><font face="msyh">备注：%s</font></b><br/><br/><br/></para>' % \
                                          header_data_list[3]
                                para = Paragraph(remarks, normalStyle)
                                story.append(para)
                                story.append(PageBreak())
                        if total_inform != 0:
                            doc = SimpleDocTemplate("C:\Production_Process_PDF\\" + str(workorder_id) + '_cnc.pdf')
                            doc.build(story,canvasmaker=FooterCanvas)
                            self.viewer.LoadFile("C:\Production_Process_PDF\\" + str(workorder_id) + '_cnc.pdf')
                            shutil.copyfile(filename_local_name, filename_server_name)
                        # else:
                        #     self.viewer.LoadFile('None.pdf')
                    else:
                        self.log.WriteText( "天外天程序正在运行ZX_Pane.py   Scheduling_Query_PDF类 未找到生产工艺单，加载失败  \r\n")
                else:
                    return
        except:
            self.log.WriteText("天外天程序正在运行ZX_Pane.py   Scheduling_Query_PDF类 DrawTable_PDF方法 报错，画pdf表格出错 请检查 \r\n")
class Scheduling_Query_Scattered_PDF(wx.Panel):
    def __init__(self, parent,log):
        wx.Panel.__init__(self, parent, -1)
        self.log=log
        self.order_list=''
        # self.can_not_load_door_type = ['1709','1711','1739','1740','1742','1743','1744','1745','1746','1747','1748','1749','1750','1751','1752','1753','1754','1755','1758']
        # self.Scheduling_Query_Layer_PDF=Scheduling_Query_Layer_PDF(self,self.log)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        self.buttonpanel = pdfButtonPanel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        vsizer.Add(self.buttonpanel, 0,wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT | wx.TOP, 5)
        self.viewer = pdfViewer(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL | wx.VSCROLL | wx.SUNKEN_BORDER)
        vsizer.Add(self.viewer, 1, wx.GROW | wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)
        self.loadbutton = wx.Button(self, wx.ID_ANY, "打印异形和整套散板条码", wx.DefaultPosition, wx.DefaultSize, 0)
        vsizer.Add(self.loadbutton, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.SetSizer(vsizer)
        self.SetAutoLayout(True)
        self.buttonpanel.viewer = self.viewer
        self.viewer.buttonpanel = self.buttonpanel
        #self.DrawTable_PDF()  # 画pdf表
        wx.BeginBusyCursor()
        #self.viewer.LoadFile('order_pdf.pdf')
        wx.EndBusyCursor()
        self.Bind(wx.EVT_BUTTON, self.OnLoadButton, self.loadbutton)
    def DrawTable_PDF(self,order_inform,workorder_id):
        try:
            f = os.path.exists("C:\Production_Process_PDF\\")  # 用于判断在D盘中是否存在delivery_list_history文件夹，如果不在在这个路径下新建文件夹。
            if not f:
                os.mkdir("C:\Production_Process_PDF\\")  # 新建文件夹
            filename_server_name = u"\\\\192.168.31.250\\Production_Process_PDF\\" + str(workorder_id) + '_scattered.pdf'
            filename_local_name = u"C:\\Production_Process_PDF\\" + str(workorder_id) + '_scattered.pdf'
            is_exist_file = os.path.exists("\\\\192.168.31.250\\Production_Process_PDF\\" + str(workorder_id) + '_scattered.pdf')
            if is_exist_file:
                shutil.copyfile(filename_server_name, filename_local_name)
                self.viewer.LoadFile("C:\\Production_Process_PDF\\" + str(workorder_id) + '_scattered.pdf')
            else:
                story = []
                stylesheet = getSampleStyleSheet()
                normalStyle = stylesheet['Normal']
                today = datetime.datetime.now()
                formatted_today = today.strftime('%Y.%m.%d')
                formatted1_today = today.strftime('%H:%M')
                #############################生成条形码
                if Is_Database_Connect():
                    base_type={0:'无'}
                    cursor = DB2.cursor()
                    cursor.execute("select `Base_material_name`,`Index` from `info_base_material_charge` where 1 ")
                    base_type_record = cursor.fetchall()
                    for l in range(len(base_type_record)):
                        base_type[base_type_record[l][1]] = base_type_record[l][0]
                    cursor = DB.cursor()
                    cursor.execute("select `Order_id` from `order_order_online` where 1 " )
                    order_online=cursor.fetchall()
                    list(flatten(order_online))
                    Judgment=set(list(flatten(order_inform))).issubset(set(list(flatten(order_online))))
                    if Judgment == True:
                        total_imform=0
                        for i in range(len(order_inform)):
                            row=0
                            scattered_inform=[]
                            cursor = DB.cursor()
                            cursor.execute("select `Brand`,`Dealer` ,`Customer_name`,`remarks`,`remarkimage` from `order_order_online` where `Order_id`='%s' " % order_inform[i])
                            header_data=cursor.fetchone()
                            if header_data[2]==None:
                                customer='无'
                            else:
                                customer =header_data[2]
                            cursor = DB.cursor()
                            cursor.execute(
                                "select `Index_of_base_material_thickness`,`Color`,`Type`,`Height`,`Width` from `work_cnc_before_layout_temporary` where `Order_id`='%s' AND `State`<>'%s'AND `Single_double`='%s'AND `Element_type_id`<>'%s'AND `Element_type_id`<>'%s'AND `Element_type_id`<>'%s'" %(order_inform[i],REWORK,NO_SINGLE_DOUBLE,TOP_LINE,BELT_LINE,FOOT_LINE))
                            scattered_element_record = cursor.fetchall()
                            cursor.execute(
                                "select `Index_of_base_material_thickness`,`Sec_color`,`Sec_series`,`Sec_height`,`Sec_length`,`Sec_width`,`Archaize` from `order_section_online` where `Order_id`='%s' and `Sec_type`='%s' " % (
                                    order_inform[i], '1'))
                            component_inform = cursor.fetchall()
                            total_len=len(scattered_element_record)+len(component_inform)
                            total_imform+=total_len
                            if scattered_element_record != () or component_inform!= ():
                                code_img=exe_Barcode(order_inform[i])
                                rpt_title = '<para autoLeading="off" fontSize=24 align=center><b><font face="msyh">散板工位工单</font></b><br/><br/><br/></para>'
                                story.append(Paragraph(rpt_title, normalStyle))
                                component_data = [['', '', '', '', '','', '', '',''],
                                                  [formatted_today,'', formatted1_today, '','','', '',''],
                                                  ['客户名称:','',str(header_data[1]),'', '',  '', '',order_inform[i]],
                                                  ['终端客户:','',str(customer),'','','', '',code_img],
                                                ['序号','基材', '颜色', '名称', '高', '宽','深度','特殊工艺']]
                                for j in range(len(scattered_element_record)):
                                    base_type_inform=base_type[scattered_element_record[j][0]]
                                    scattered_element_inform=['',base_type_inform,scattered_element_record[j][1],scattered_element_record[j][2],scattered_element_record[j][3],scattered_element_record[j][4],'','']
                                    scattered_inform.append(scattered_element_inform)
                                for j in range(len(component_inform)):
                                    scattered_component_inform=['',base_type[component_inform[j][0]],component_inform[j][1],component_inform[j][2],component_inform[j][3],component_inform[j][4],component_inform[j][5],component_inform[j][6]]
                                    scattered_inform.append(scattered_component_inform)
                                for j in range(len(scattered_inform)):
                                    scattered_inform[j][0]=j+1
                                component_data += (scattered_inform)
                                if header_data[4] != None:
                                    special_shaped = header_data[4].split('&&')
                                    downloadpic(special_shaped, order_inform[i])
                                    row=len(special_shaped)
                                    for p in range(1,len(special_shaped)+1):
                                        special_shaped_image=Image("C:\Special_Shaped\\"+str(order_inform[i])+"_"+str(p)+".png")
                                        # special_shaped_image.drawWidth = special_shaped_image.imageWidth * 0.625
                                        if special_shaped_image.imageHeight > 685 or special_shaped_image.imageWidth > 439:
                                            special_shaped_image.drawHeight = special_shaped_image.imageHeight * 0.25
                                            special_shaped_image.drawWidth = special_shaped_image.imageWidth * 0.3
                                        else:
                                            special_shaped_image.drawHeight = special_shaped_image.imageHeight
                                            special_shaped_image.drawWidth = special_shaped_image.imageWidth
                                        component_data += [['图'+str(p),'','',special_shaped_image,'','','']]
                                component_table = Table(component_data,colWidths=[25,60,60,140,45,45,50])
                                component_table.setStyle(TableStyle([
                                ('FONTNAME',(0,0),(-1,-1),'msyh'),#字体
                                ('FONTSIZE',(0,0),(-1,-1),10),#字体大小
                                # ('SPAN', (0,-1), (-1,-row)),
                                ('ALIGN',(0,0),(-1,-1),'CENTER'),#对齐
                                ('ALIGN',(1,0),(1,3),'RIGHT'),#对齐
                                ('ALIGN',(2,0),(2,3),'LEFT'),#对齐
                                ('ALIGN',(-1,0),(-2,5),'RIGHT'),#对齐
                                ('VALIGN',(0,0),(-1,-1),'MIDDLE'),  #对齐
                                ('TEXTCOLOR',(-1,-1),(-1,-1),colors.black),#设置表格内文字颜色
                                ('GRID',(0,4),(-1,(-row-1)),1,colors.black),#设置表格框线为红色，线宽为0.5
                                # ('GRID',(0,-1), (-1,-row),1,colors.black),#设置表格框线为红色，线宽为0.5
                                ]))
                                story.append(component_table)
                                story.append(Spacer(0, 0.2 * inch))
                                header_data_list = list(header_data)
                                if header_data[3]==None:
                                    header_data_list[3]='无'
                                else:
                                    header_data_list[3]
                                remarks = '<para autoLeading="off" fontSize=15 align=center><b><font face="msyh">备注：%s</font></b><br/><br/><br/></para>' % header_data_list[3]
                                para = Paragraph(remarks, normalStyle)
                                story.append(para)
                                story.append(PageBreak())
                            else:
                                continue
                        if total_imform != 0:
                            doc = SimpleDocTemplate("C:\Production_Process_PDF\\" + str(workorder_id) + '_scattered.pdf')
                            doc.build(story, canvasmaker=FooterCanvas)
                            self.viewer.LoadFile("C:\Production_Process_PDF\\" + str(workorder_id) + '_scattered.pdf')
                            shutil.copyfile(filename_local_name, filename_server_name)
                        else:
                            self.viewer.LoadFile('None.pdf')
                    else:
                        self.log.WriteText(
                            "天外天程序正在运行ZX_Pane.py   Scheduling_Query_Scattered_PDF类 未找到生产工艺单，加载失败 \r\n")
                else:
                    return
        except:
            self.log.WriteText("天外天程序正在运行ZX_Pane.py   Scheduling_Query_Scattered_PDF类 DrawTable_PDF方法 报错，画pdf表格出错 请检查 \r\n")
    def OnLoadButton(self, event):
        try:
            if Is_Database_Connect():
                cursor = DB.cursor()
                for i in range(len(self.order_list)):
                    cursor.execute(
                        "UPDATE `work_cnc_before_layout_temporary` set `Print_Barcode`='%s' WHERE `Order_Id`='%s' and (`Element_type_id`='%s' or `Element_type_id`='%s' or `Element_type_id`='%s')and `Single_double`='%s'and `State`<>'%s'" % ( FRAGMENTARY_BARCODE, self.order_list[i],BOARD,LMZ,MB,NO_SINGLE_DOUBLE,REWORK))
                DB.commit()
            else:
                return
        except:
            self.log.WriteText('天外天系统正在运行ZX_Pane.py Scheduling_Query_PDF中OnLoadButton方法打印条形码操作出错，请检查临时待排样表单中与排产工单中订单号相对应\r\n')
    def SetValue(self,order_list):
        self.order_list = order_list
class Scheduling_Query_Double_Sided_PDF(wx.Panel):
    def __init__(self, parent,log):
        wx.Panel.__init__(self, parent, -1)
        self.log=log
        self.order_list=''
        # self.Scheduling_Query_Layer_PDF=Scheduling_Query_Layer_PDF(self,self.log)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        self.buttonpanel = pdfButtonPanel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        vsizer.Add(self.buttonpanel, 0,wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT | wx.TOP, 5)
        self.viewer = pdfViewer(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL | wx.VSCROLL | wx.SUNKEN_BORDER)
        vsizer.Add(self.viewer, 1, wx.GROW | wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)
        self.loadbutton = wx.Button(self, wx.ID_ANY, "打印双面模压条码", wx.DefaultPosition, wx.DefaultSize, 0)
        vsizer.Add(self.loadbutton, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.SetSizer(vsizer)
        self.SetAutoLayout(True)
        self.buttonpanel.viewer = self.viewer
        self.viewer.buttonpanel = self.buttonpanel
        #self.DrawTable_PDF()  # 画pdf表
        wx.BeginBusyCursor()
        #self.viewer.LoadFile('order_pdf.pdf')
        wx.EndBusyCursor()
        self.Bind(wx.EVT_BUTTON, self.OnLoadButton, self.loadbutton)
    def DrawTable_PDF(self,order_inform,workorder_id):
        try:
            f = os.path.exists("C:\Production_Process_PDF\\")  # 用于判断在D盘中是否存在delivery_list_history文件夹，如果不在在这个路径下新建文件夹。
            if not f:
                os.mkdir("C:\Production_Process_PDF\\")  # 新建文件夹
            filename_server_name = u"\\\\192.168.31.250\\Production_Process_PDF\\" + str(workorder_id) + '_double_sided.pdf'
            filename_local_name = u"C:\\Production_Process_PDF\\" + str(workorder_id) + '_double_sided.pdf'
            is_exist_file = os.path.exists("\\\\192.168.31.250\\Production_Process_PDF\\" + str(workorder_id) + '_double_sided.pdf')
            if is_exist_file:
                shutil.copyfile(filename_server_name, filename_local_name)
                self.viewer.LoadFile("C:\\Production_Process_PDF\\" + str(workorder_id) + '_double_sided.pdf')
            else:
                story = []
                stylesheet = getSampleStyleSheet()
                normalStyle = stylesheet['Normal']
                today = datetime.datetime.now()
                formatted_today = today.strftime('%Y.%m.%d')
                formatted1_today = today.strftime('%H:%M')
                #############################生成条形码
                if Is_Database_Connect():
                    cursor = DB.cursor()
                    cursor.execute("select `Order_id` from `order_order_online` where 1 " )
                    order_online=cursor.fetchall()
                    Judgment=set(list(flatten(order_inform))).issubset(set(list(flatten(order_online))))
                    if Judgment == True:
                        total_inform=0
                        base_material = {0:'无'}
                        cursor = DB2.cursor()
                        cursor.execute("select `Index`,`Base_material_name` from `info_base_material_charge` where 1 ")
                        base_name_record = cursor.fetchall()
                        for row in range(len(base_name_record)):
                            base_material[base_name_record[row][0]] = base_name_record[row][1]
                        # total_inform+=(len(order_inform))
                        if len(order_inform)!=0:
                            for i in range(len(order_inform)):
                                row=0
                                part_inform = []
                                part_gropby_inform = []
                                cursor = DB.cursor()
                                cursor.execute("select `Brand`,`Dealer` ,`Customer_name`,`remarks`,`remarkimage` from `order_order_online` where `Order_id`='%s' " % order_inform[i])
                                header_data=cursor.fetchone()
                                if header_data[2]==None:
                                    customer='无'
                                else:
                                    customer =header_data[2]
                                cursor = DB.cursor()
                                cursor.execute(
                                    "select `Door_type`,`Edge_type`,`Door_height` ,`Door_width`,`Open_way`,`Door_color`,`Index_of_base_material_thickness`,`Straightening_device`,`Double_color`,`Archaize`,`Hole`,`heterotype`,`Glass` from `order_part_online` where `Order_id`='%s' and `Single_double`='%s'" %(order_inform[i],1))
                                part_detail_inform = cursor.fetchall()
                                if part_detail_inform!=():
                                    total_inform += (len(part_detail_inform))
                                    code_img=exe_Barcode(order_inform[i])
                                    rpt_title = '<para autoLeading="off" fontSize=24 align=center><b><font face="msyh">双面膜压生产工艺单</font></b><br/><br/><br/></para>'
                                    story.append(Paragraph(rpt_title, normalStyle))
                                    component_data = [['', '', '', '', '', '', '', '', '', '', ''],
                                                      ['', formatted_today, '', formatted1_today, '', '', '', '', '', '', ''],
                                                      ['', '客户名称:', '', str(header_data[1]), '', '', '', '', '', '', order_inform[i]],
                                                      ['', '终端客户:', '', str(customer), '', '', '', '', '', '',code_img],
                                                      ['序号', '基材', '颜色', '套系', '门型', '边型', '高', '宽', '数量', '打孔', '特殊工艺']]
                                    for j in range(len(part_detail_inform)):
                                        if 'MY' in part_detail_inform[j][0]:
                                            Door_type = part_detail_inform[j][0].split('_')
                                            Door_type_split = Door_type[-1]
                                            Door_series = Door_type[0] + '_' + Door_type[1]
                                        else:
                                            Door_type_split = part_detail_inform[j][0]
                                        if part_detail_inform[j][7] == 1:
                                            remark1 = '拉直器'+ '\n'
                                        else:
                                            remark1 = ''
                                        if part_detail_inform[j][8] != None:
                                            remark2 = part_detail_inform[j][8]+ '\n'
                                        else:
                                            remark2 = ''
                                        if part_detail_inform[j][9] != None:
                                            remark3 = part_detail_inform[j][9]+ '\n'
                                        else:
                                            remark3 = ''
                                        if part_detail_inform[j][11] == 0:
                                            remark5 = ''
                                        else:
                                            remark5 = '异形'+ '\n'
                                        if part_detail_inform[j][12] == None or part_detail_inform[j][12] == 0:
                                            remark6 = ''
                                        else:
                                            remark6 = part_detail_inform[j][12]+ '\n'
                                            # ----------------------------------------------------------------------开孔具体信息计算规则
                                        # if part_detail_inform[4] != '不开' and part_detail_inform[2]<1000:
                                        if part_detail_inform[j][2] < 1000:
                                            hole = str(120) + '/' + str(0) + '/' + str(0) + '/' + str( 0) + '/' + str(120)
                                        elif part_detail_inform[j][2] >= 1000 and part_detail_inform[j][2] < 1530:
                                            hole = str(120) + '/' + str(0) + '/' + str(int(part_detail_inform[j][2] * 0.5)) + '/' + str(0) + '/' + str(120)
                                        elif part_detail_inform[j][2] >= 1530 and part_detail_inform[j][2] < 1645:
                                            hole = str(120) + '/' + str(550) + '/' + str(0) + '/' + str(int(part_detail_inform[j][2] - 550)) + '/' + str(120)
                                        elif part_detail_inform[j][2] >= 1645 and part_detail_inform[j][2] < 1800:
                                            hole = str(120) + '/' + str(600) + '/' + str(0) + '/' + str(int(part_detail_inform[j][2] - 600)) + '/' + str(120)
                                        elif part_detail_inform[j][2] >= 1800 and part_detail_inform[j][2] < 1900:
                                            hole = str(120) + '/' + str(650) + '/' + str(0) + '/' + str(int(part_detail_inform[j][2] - 650)) + '/' + str(120)
                                        elif part_detail_inform[j][2] >= 1900 and part_detail_inform[j][2] < 2100:
                                            hole = str(120) + '/' + str(700) + '/' + str(0) + '/' + str(int(part_detail_inform[j][2] - 700)) + '/' + str(120)
                                        elif part_detail_inform[j][2] >= 2100 and part_detail_inform[j][2] < 2250:
                                            hole = str(120) + '/' + str(750) + '/' + str(0) + '/' + str(int(part_detail_inform[j][2] - 750)) + '/' + str(120)
                                        elif part_detail_inform[j][2] >= 2250 and part_detail_inform[j][2] < 2300:
                                            hole = str(120) + '/' + str(800) + '/' + str(0) + '/' + str(int(part_detail_inform[j][2] - 800)) + '/' + str(120)
                                        elif part_detail_inform[j][2] >= 2300:
                                            hole = str(120) + '/' + str(850) + '/' + str(0) + '/' + str(int(part_detail_inform[j][2] - 850)) + '/' + str(120)
                                        else:
                                            hole = '尺寸错误'
                                        if part_detail_inform[j][4] != '不开' and part_detail_inform[j][
                                            10] != None and hole != part_detail_inform[j][10]:
                                            remark4 = part_detail_inform[j][10]+ '\n'
                                        else:
                                            remark4 = ''
                                        remark_total = remark1 + remark2 + remark3 + remark5+ remark6+ remark4  # 增加备注
                                        part_compare_inform = [base_material[part_detail_inform[j][6]], part_detail_inform[j][5],Door_series, Door_type_split,
                                                               part_detail_inform[j][1], part_detail_inform[j][2],part_detail_inform[j][3], part_detail_inform[j][4],remark_total]
                                        part_gropby_inform.append(part_compare_inform)
                                        part_detail = ['', base_material[part_detail_inform[j][6]], part_detail_inform[j][5],Door_series, Door_type_split, part_detail_inform[j][1],part_detail_inform[j][2], part_detail_inform[j][3], '',part_detail_inform[j][4], remark_total]
                                        part_inform.append(part_detail)
                                    for j in range(len(part_inform)):
                                        count = 0
                                        for k in range(len(part_inform)):
                                            if part_gropby_inform[k] == part_gropby_inform[j]:
                                                count = count + 1
                                                part_inform[j][8] = count
                                else:
                                    continue
                                if total_inform != 0:
                                    reList = list( set([tuple(t) for t in part_inform]))  # 二维列表的子元素也是列表，将子元素的一维列表转换成元组，然后使用set()去重
                                    reList = [list(v) for v in reList]  # 将二维列表转换成元组
                                    reList.sort(key=part_inform.index)  # 按照二维列表的索引值对去重之后得列表进行排序。
                                    for j in range(len(reList)):
                                        reList[j][0] = j + 1
                                    component_data += (reList)
                                    if header_data[4] != None:
                                        special_shaped = header_data[4].split('&&')
                                        downloadpic(special_shaped, order_inform[i])
                                        row = len(special_shaped)
                                        for p in range(1, len(special_shaped) + 1):
                                            special_shaped_image = Image(
                                                "C:\Special_Shaped\\" + str(order_inform[i]) + "_" + str(p) + ".png")
                                            if special_shaped_image.imageHeight > 685 or special_shaped_image.imageWidth > 439:
                                                special_shaped_image.drawHeight = special_shaped_image.imageHeight * 0.25
                                                special_shaped_image.drawWidth = special_shaped_image.imageWidth * 0.3
                                            else:
                                                special_shaped_image.drawHeight = special_shaped_image.imageHeight
                                                special_shaped_image.drawWidth = special_shaped_image.imageWidth
                                            component_data += [
                                                ['图' + str(p), '', '', '', '', special_shaped_image, '','', '', '', '']]
                                    component_table = Table(component_data,colWidths=[23,43,58,51,85,110,38,38,28,27,80])
                                    component_table.setStyle(TableStyle([
                                    ('FONTNAME',(0,0),(-1,-1),'msyh'),#字体
                                    ('FONTSIZE',(0,0),(-1,-1),10),#字体大小
                                    # ('SPAN',(0,h),(0,h1)),#合并第一行前三列
                                    # ('BACKGROUND',(0,0),(-1,0), colors.lightskyblue),#设置第一行背景颜色
                                    # ('SPAN',(1,h),(1,h1)), #合并第一行后两列
                                    # ('SPAN', (2, h), (2, h1)),  # 合并第一行后两列
                                    # ('SPAN', (3, h), (3, h1)),  # 合并第一行后两列
                                    # ('SPAN', (4, h), (4, h1)),  # 合并第一行后两列
                                    ('ALIGN',(0,0),(-1,-1),'CENTER'),#对齐
                                    # ('ALIGN',(-1,0),(-1,4),'LEFT'),#对齐
                                    ('ALIGN',(0,0),(0,3),'RIGHT'),#对齐
                                    ('ALIGN',(1,0),(1,3),'LEFT'),#对齐
                                    ('ALIGN',(-1,0),(-2,5),'RIGHT'),#对齐
                                    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),  #对齐
                                    # ('LINEBEFORE',(0,0),(0,-1),0.1,colors.grey),#设置表格左边线颜色为灰色，线宽为0.1
                                    #('TEXTCOLOR',(0,1),(-2,-1),colors.royalblue),#设置表格内文字颜色
                                    ('TEXTCOLOR',(-1,-1),(-1,-1),colors.black),#设置表格内文字颜色
                                    ('GRID',(0,4),(-1,(-row-1)),1,colors.black),#设置表格框线为红色，线宽为0.5
                                    ]))
                                    story.append(component_table)
                                    story.append(Spacer(0, 0.2 * inch))
                                    header_data_list = list(header_data)
                                    if header_data[3]==None:
                                        header_data_list[3]='无'
                                    else:
                                        header_data_list[3]
                                    remarks = '<para autoLeading="off" fontSize=15 align=center><b><font face="msyh">备注：%s</font></b><br/><br/><br/></para>' % \
                                              header_data_list[3]
                                    para = Paragraph(remarks, normalStyle)
                                    story.append(para)
                                    story.append(PageBreak())
                                else:
                                    continue
                        if total_inform != 0:
                            doc = SimpleDocTemplate("C:\\Production_Process_PDF\\" + str(workorder_id) + '_double_sided.pdf')
                            doc.build(story,canvasmaker=FooterCanvas)
                            self.viewer.LoadFile("C:\\Production_Process_PDF\\" + str(workorder_id) + '_double_sided.pdf')
                            shutil.copyfile(filename_local_name,filename_server_name)
                        else:
                            self.viewer.LoadFile('None.pdf')
                    else:
                        self.log.WriteText( "天外天程序正在运行ZX_Pane.py   Scheduling_Query_Double_Sided_PDF类 未找到生产工艺单，加载失败 \r\n")
                else:
                    return
        except:
            self.log.WriteText("天外天程序正在运行ZX_Pane.py   Scheduling_Query_Double_Sided_PDF类 DrawTable_PDF方法 报错，画pdf表格出错 请检查 \r\n")
    def OnLoadButton(self, event):
        try:
            if Is_Database_Connect():
                cursor = DB.cursor()
                for i in range(len(self.order_list)):
                    cursor.execute(
                        "UPDATE `work_cnc_before_layout_temporary` set `Print_Barcode`='%s' WHERE `Order_Id`='%s' and `Single_double`='%s'" % ( FRAGMENTARY_BARCODE, self.order_list[i],SINGLE_DOUBLE))
                DB.commit()
            else:
                return
        except:
            self.log.WriteText('天外天系统正在运行ZX_Pane.py Scheduling_Query_PDF中OnLoadButton方法打印条形码操作出错，请检查临时待排样表单中与排产工单中订单号相对应\r\n')
    def SetValue(self,order_list):
        self.order_list = order_list
class Scheduling_Query_Rework_PDF(wx.Panel):
    def __init__(self, parent,log):
        wx.Panel.__init__(self, parent, -1)
        self.log=log
        self.order_list=''
        self.rework_id=[]
        # self.Scheduling_Query_Layer_PDF=Scheduling_Query_Layer_PDF(self,self.log)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        self.buttonpanel = pdfButtonPanel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        vsizer.Add(self.buttonpanel, 0,wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT | wx.TOP, 5)
        self.viewer = pdfViewer(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL | wx.VSCROLL | wx.SUNKEN_BORDER)
        vsizer.Add(self.viewer, 1, wx.GROW | wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)
        self.loadbutton = wx.Button(self, wx.ID_ANY, "打印返工条码", wx.DefaultPosition, wx.DefaultSize, 0)
        vsizer.Add(self.loadbutton, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.SetSizer(vsizer)
        self.SetAutoLayout(True)
        self.buttonpanel.viewer = self.viewer
        self.viewer.buttonpanel = self.buttonpanel
        #self.DrawTable_PDF()  # 画pdf表
        wx.BeginBusyCursor()
        #self.viewer.LoadFile('order_pdf.pdf')
        wx.EndBusyCursor()
        self.Bind(wx.EVT_BUTTON, self.OnLoadButton, self.loadbutton)
    def DrawTable_PDF(self,order_inform,workorder_id):
        try:
            f = os.path.exists("C:\Production_Process_PDF\\")  # 用于判断在D盘中是否存在delivery_list_history文件夹，如果不在在这个路径下新建文件夹。
            if not f:
                os.mkdir("C:\Production_Process_PDF\\")  # 新建文件夹
            filename_server_name = u"\\\\192.168.31.250\\Production_Process_PDF\\" + str( workorder_id) + '_Rework.pdf'
            filename_local_name = u"C:\\Production_Process_PDF\\" + str(workorder_id) + '_Rework.pdf'
            is_exist_file = os.path.exists("\\\\192.168.31.250\\Production_Process_PDF\\" + str(workorder_id) + '_Rework.pdf')
            if is_exist_file:
                shutil.copyfile(filename_server_name, filename_local_name)
                self.viewer.LoadFile("C:\Production_Process_PDF\\" + str(workorder_id) + '_Rework.pdf')
            else:
                story = []
                stylesheet = getSampleStyleSheet()
                normalStyle = stylesheet['Normal']
                today = datetime.datetime.now()
                formatted_today = today.strftime('%Y.%m.%d')
                formatted1_today = today.strftime('%H:%M')
                #############################生成条形码
                if Is_Database_Connect():
                    cursor = DB.cursor()
                    cursor.execute("select `Order_id` from `order_order_online` where 1 " )
                    order_online=cursor.fetchall()
                    Judgment=set(list(flatten(order_inform))).issubset(set(list(flatten(order_online))))
                    if Judgment == True:
                        total_inform = 0
                        base_material = {0:'无'}
                        cursor = DB2.cursor()
                        cursor.execute("select `Index`,`Base_material_name` from `info_base_material_charge` where 1 ")
                        base_name_record = cursor.fetchall()
                        for row in range(len(base_name_record)):
                            base_material[base_name_record[row][0]] = base_name_record[row][1]
                        # total_inform+=(len(order_inform))
                        if len(order_inform)!=0:
                            for i in range(len(order_inform)):
                                row=0
                                part_inform = []
                                part_gropby_inform = []
                                cursor = DB.cursor()
                                cursor.execute("select `Brand`,`Dealer` ,`Customer_name`,`remarks`,`remarkimage` from `order_order_online` where `Order_id`='%s' " % order_inform[i])
                                header_data=cursor.fetchone()
                                if header_data[2]==None:
                                    customer='无'
                                else:
                                    customer =header_data[2]
                                cursor.execute(
                                    "select `Board_type`,`Edge_type`,`Board_height` ,`Board_width`,`Open_way`,`Color`,`Index_of_base_material_thickness`,`Straightening_device`,`Double_color`,`Archaize`,`Hole`,`heterotype`,`Glass`,`Id`  from `order_element_scrap` where `Order_id`='%s' " %(order_inform[i]))
                                part_detail_inform = cursor.fetchall()

                                if part_detail_inform!=():
                                    total_inform += (len(part_detail_inform))
                                    code_img=exe_Barcode(order_inform[i])
                                    rpt_title = '<para autoLeading="off" fontSize=24 align=center><b><font face="msyh">返工生产工艺单</font></b><br/><br/><br/></para>'
                                    story.append(Paragraph(rpt_title, normalStyle))
                                    component_data = [['', '', '', '', '', '', '', '', '', '', ''],
                                                      ['', formatted_today, '', formatted1_today, '', '', '', '', '', '', ''],
                                                      ['', '客户名称:', '', str(header_data[1]), '', '', '', '', '', '', order_inform[i]],
                                                      ['', '终端客户:','', str(customer), '', '', '', '', '', '',code_img],
                                                      ['序号', '基材', '颜色', '套系', '门型', '边型', '高', '宽', '数量', '打孔', '特殊工艺']]
                                    for j in range(len(part_detail_inform)):
                                        self.rework_id.append(part_detail_inform[j][13])
                                        if 'MY' in part_detail_inform[j][0]:
                                            Door_type = part_detail_inform[j][0].split('_')
                                            Door_type_split = Door_type[-1]
                                            Door_series = Door_type[0] + '_' + Door_type[1]
                                        else:
                                            Door_type_split = part_detail_inform[j][0]
                                        if part_detail_inform[j][7] == 1:
                                            remark1 = '拉直器'+ '\n'
                                        else:
                                            remark1 = ''
                                        if part_detail_inform[j][8] != None:
                                            remark2 = part_detail_inform[j][8]+ '\n'
                                        else:
                                            remark2 = ''
                                        if part_detail_inform[j][9] != None:
                                            remark3 = part_detail_inform[j][9]+ '\n'
                                        else:
                                            remark3 = ''
                                        if part_detail_inform[j][11] == 0:
                                            remark5 = ''
                                        else:
                                            remark5 = '异形'+ '\n'
                                        if part_detail_inform[j][12] == None or part_detail_inform[j][12] == 0:
                                            remark6 = ''
                                        else:
                                            remark6 = part_detail_inform[j][12]+ '\n'
                                            # ----------------------------------------------------------------------开孔具体信息计算规则
                                        # if part_detail_inform[4] != '不开' and part_detail_inform[2]<1000:
                                        if part_detail_inform[j][2] < 1000:
                                            hole = str(120) + '/' + str(0) + '/' + str(0) + '/' + str( 0) + '/' + str(120)
                                        elif part_detail_inform[j][2] >= 1000 and part_detail_inform[j][2] < 1530:
                                            hole = str(120) + '/' + str(0) + '/' + str(int(part_detail_inform[j][2] * 0.5)) + '/' + str(0) + '/' + str(120)
                                        elif part_detail_inform[j][2] >= 1530 and part_detail_inform[j][2] < 1645:
                                            hole = str(120) + '/' + str(550) + '/' + str(0) + '/' + str(int(part_detail_inform[j][2] - 550)) + '/' + str(120)
                                        elif part_detail_inform[j][2] >= 1645 and part_detail_inform[j][2] < 1800:
                                            hole = str(120) + '/' + str(600) + '/' + str(0) + '/' + str(int(part_detail_inform[j][2] - 600)) + '/' + str(120)
                                        elif part_detail_inform[j][2] >= 1800 and part_detail_inform[j][2] < 1900:
                                            hole = str(120) + '/' + str(650) + '/' + str(0) + '/' + str(int(part_detail_inform[j][2] - 650)) + '/' + str(120)
                                        elif part_detail_inform[j][2] >= 1900 and part_detail_inform[j][2] < 2100:
                                            hole = str(120) + '/' + str(700) + '/' + str(0) + '/' + str(int(part_detail_inform[j][2] - 700)) + '/' + str(120)
                                        elif part_detail_inform[j][2] >= 2100 and part_detail_inform[j][2] < 2250:
                                            hole = str(120) + '/' + str(750) + '/' + str(0) + '/' + str(int(part_detail_inform[j][2] - 750)) + '/' + str(120)
                                        elif part_detail_inform[j][2] >= 2250 and part_detail_inform[j][2] < 2300:
                                            hole = str(120) + '/' + str(800) + '/' + str(0) + '/' + str(int(part_detail_inform[j][2] - 800)) + '/' + str(120)
                                        elif part_detail_inform[j][2] >= 2300:
                                            hole = str(120) + '/' + str(850) + '/' + str(0) + '/' + str(int(part_detail_inform[j][2] - 850)) + '/' + str(120)
                                        else:
                                            hole = '尺寸错误'+ '\n'
                                        if part_detail_inform[j][4] != '不开' and part_detail_inform[j][
                                            10] != None and hole != part_detail_inform[j][10]:
                                            remark4 = part_detail_inform[j][10]+ '\n'
                                        else:
                                            remark4 = ''
                                        remark_total = remark1+ remark2+ remark3+ remark5+ remark6 + remark4  # 增加备注
                                        part_compare_inform = [base_material[part_detail_inform[j][6]], part_detail_inform[j][5],Door_series, Door_type_split,
                                                               part_detail_inform[j][1], part_detail_inform[j][2],part_detail_inform[j][3], part_detail_inform[j][4],remark_total]
                                        part_gropby_inform.append(part_compare_inform)
                                        part_detail = ['', base_material[part_detail_inform[j][6]], part_detail_inform[j][5],Door_series, Door_type_split, part_detail_inform[j][1],
                                                       part_detail_inform[j][2], part_detail_inform[j][3], '',part_detail_inform[j][4], remark_total]
                                        part_inform.append(part_detail)
                                    for j in range(len(part_inform)):
                                        count = 0
                                        for k in range(len(part_inform)):
                                            if part_gropby_inform[k] == part_gropby_inform[j]:
                                                count = count + 1
                                                part_inform[j][8] = count
                                else:
                                    continue
                                if total_inform != 0:
                                    reList = list( set([tuple(t) for t in part_inform]))  # 二维列表的子元素也是列表，将子元素的一维列表转换成元组，然后使用set()去重
                                    reList = [list(v) for v in reList]  # 将二维列表转换成元组
                                    reList.sort(key=part_inform.index)  # 按照二维列表的索引值对去重之后得列表进行排序。
                                    for j in range(len(reList)):
                                        reList[j][0] = j + 1
                                    component_data += (reList)
                                    if header_data[4] != None:
                                        special_shaped = header_data[4].split('&&')
                                        downloadpic(special_shaped, order_inform[i])
                                        row = len(special_shaped)
                                        for p in range(1, len(special_shaped) + 1):
                                            special_shaped_image = Image(
                                                "C:\Special_Shaped\\" + str(order_inform[i]) + "_" + str(p) + ".png")
                                            if special_shaped_image.imageHeight > 685 or special_shaped_image.imageWidth > 439:
                                                special_shaped_image.drawHeight = special_shaped_image.imageHeight * 0.25
                                                special_shaped_image.drawWidth = special_shaped_image.imageWidth * 0.3
                                            else:
                                                special_shaped_image.drawHeight = special_shaped_image.imageHeight
                                                special_shaped_image.drawWidth = special_shaped_image.imageWidth
                                            component_data += [['图'+str(p), '','','','', special_shaped_image,'','','','','']]
                                    component_table = Table(component_data,colWidths=[23,43,58,51,85,110,38,38,28,27,80])
                                    component_table.setStyle(TableStyle([
                                    ('FONTNAME',(0,0),(-1,-1),'msyh'),#字体
                                    ('FONTSIZE',(0,0),(-1,-1),10),#字体大小
                                    # ('SPAN',(0,h),(0,h1)),#合并第一行前三列
                                    # ('BACKGROUND',(0,0),(-1,0), colors.lightskyblue),#设置第一行背景颜色
                                    # ('SPAN',(1,h),(1,h1)), #合并第一行后两列
                                    # ('SPAN', (2, h), (2, h1)),  # 合并第一行后两列
                                    # ('SPAN', (3, h), (3, h1)),  # 合并第一行后两列
                                    # ('SPAN', (4, h), (4, h1)),  # 合并第一行后两列
                                    ('ALIGN',(0,0),(-1,-1),'CENTER'),#对齐
                                    # ('ALIGN',(-1,0),(-1,4),'LEFT'),#对齐
                                    ('ALIGN',(0,0),(0,3),'RIGHT'),#对齐
                                    ('ALIGN',(1,0),(1,3),'LEFT'),#对齐
                                    ('ALIGN',(-1,0),(-2,5),'RIGHT'),#对齐
                                    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),  #对齐
                                    # ('LINEBEFORE',(0,0),(0,-1),0.1,colors.grey),#设置表格左边线颜色为灰色，线宽为0.1
                                    #('TEXTCOLOR',(0,1),(-2,-1),colors.royalblue),#设置表格内文字颜色
                                    ('TEXTCOLOR',(-1,-1),(-1,-1),colors.black),#设置表格内文字颜色
                                    ('GRID',(0,4),(-1,(-row-1)),1,colors.black),#设置表格框线为红色，线宽为0.5
                                    ]))
                                    story.append(component_table)
                                    story.append(Spacer(0, 0.2 * inch))
                                    header_data_list = list(header_data)
                                    if header_data[3]==None:
                                        header_data_list[3]='无'
                                    else:
                                        header_data_list[3]
                                    remarks = '<para autoLeading="off" fontSize=15 align=center><b><font face="msyh">备注：%s</font></b><br/><br/><br/></para>' % \
                                              header_data_list[3]
                                    para = Paragraph(remarks, normalStyle)
                                    story.append(para)
                                    story.append(PageBreak())
                                else:
                                    continue
                        if total_inform != 0:
                            doc = SimpleDocTemplate("C:\Production_Process_PDF\\" + str(workorder_id) + '_Rework.pdf')
                            doc.build(story,canvasmaker=FooterCanvas)
                            self.viewer.LoadFile("C:\Production_Process_PDF\\" + str(workorder_id) + '_Rework.pdf')
                            shutil.copyfile( filename_local_name,filename_server_name)
                        else:
                            self.viewer.LoadFile('None.pdf')
                    else:
                        self.log.WriteText("天外天程序正在运行ZX_Pane.py   Scheduling_Query__Rework_PDF类 未找到生产工艺单，加载失败 \r\n")
                else:
                    return
        except:
            self.log.WriteText("天外天程序正在运行ZX_Pane.py   Scheduling_Query__Rework_PDF类 DrawTable_PDF方法 报错，画pdf表格出错 请检查 \r\n")
    def OnLoadButton(self, event):
        try:
            if Is_Database_Connect():
                cursor = DB.cursor()
                for i in range(len(self.rework_id)):
                    cursor.execute(
                        "UPDATE `work_cnc_before_layout_temporary` set `Print_Barcode`='%s' WHERE `Id`='%s'" % ( FRAGMENTARY_BARCODE, self.rework_id[i]))
                DB.commit()
            else:
                return
        except:
            self.log.WriteText('天外天系统正在运行ZX_Pane.py Scheduling_Query_PDF中OnLoadButton方法打印条形码操作出错，请检查临时待排样表单中与排产工单中订单号相对应\r\n')
class Scheduling_Query_Line_PDF(wx.Panel):
    def __init__(self, parent,log):
        wx.Panel.__init__(self, parent, -1)
        self.log=log
        self.order_list=''
        # self.Scheduling_Query_Layer_PDF=Scheduling_Query_Layer_PDF(self,self.log)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        self.buttonpanel = pdfButtonPanel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        vsizer.Add(self.buttonpanel, 0,wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT | wx.TOP, 5)
        self.viewer = pdfViewer(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL | wx.VSCROLL | wx.SUNKEN_BORDER)
        vsizer.Add(self.viewer, 1, wx.GROW | wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)
        self.loadbutton = wx.Button(self, wx.ID_ANY, "打印线条条码", wx.DefaultPosition, wx.DefaultSize, 0)
        vsizer.Add(self.loadbutton, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.SetSizer(vsizer)
        self.SetAutoLayout(True)
        self.buttonpanel.viewer = self.viewer
        self.viewer.buttonpanel = self.buttonpanel
        #self.DrawTable_PDF()  # 画pdf表
        wx.BeginBusyCursor()
        #self.viewer.LoadFile('order_pdf.pdf')
        wx.EndBusyCursor()
        self.Bind(wx.EVT_BUTTON, self.OnLoadButton, self.loadbutton)
    def DrawTable_PDF(self,order_inform,workorder_id):
        try:
            f = os.path.exists("C:\Production_Process_PDF\\")  # 用于判断在D盘中是否存在delivery_list_history文件夹，如果不在在这个路径下新建文件夹。
            if not f:
                os.mkdir("C:\Production_Process_PDF\\")  # 新建文件夹
            filename_server_name = u"\\\\192.168.31.250\\Production_Process_PDF\\" + str( workorder_id) + '_line.pdf'
            filename_local_name = u"C:\\Production_Process_PDF\\" + str(workorder_id) + '_line.pdf'
            is_exist_file = os.path.exists( "\\\\192.168.31.250\\Production_Process_PDF\\" + str(workorder_id) + '_line.pdf')
            if is_exist_file:
                shutil.copyfile(filename_server_name, filename_local_name)
                self.viewer.LoadFile("C:\Production_Process_PDF\\" + str(workorder_id) + '_line.pdf')
            else:
                story = []
                stylesheet = getSampleStyleSheet()
                normalStyle = stylesheet['Normal']
                today = datetime.datetime.now()
                formatted_today = today.strftime('%Y.%m.%d')
                formatted1_today = today.strftime('%H:%M')
                #############################生成条形码
                if Is_Database_Connect():
                    cursor = DB.cursor()
                    cursor.execute("select `Order_id` from `order_order_online` where 1 " )
                    order_online=cursor.fetchall()
                    list(flatten(order_online))
                    Judgment=set(list(flatten(order_inform))).issubset(set(list(flatten(order_online))))
                    if Judgment == True:
                        total_inform=0
                        for i in range(len(order_inform)):
                            a = []
                            row=0
                            part_inform = []
                            cursor = DB.cursor()
                            cursor.execute("select `Dealer` ,`Customer_name`,`remarks`,`remarkimage` from `order_order_online` where `Order_id`='%s' " % order_inform[i])
                            header_data=cursor.fetchone()
                            if header_data[1]==None:
                                customer='无'
                            else:
                                customer =header_data[1]
                            cursor.execute(
                                "select `Color`,`Board_type`,`Edge_type`,`Board_height` ,`Board_width`,`remarks` from `order_element_online` where `Order_id`='%s' AND (`Element_type_id`='%s' or `Element_type_id`='%s' or `Element_type_id`='%s'or `Element_type_id`='%s' or `Element_type_id`='%s' or `Element_type_id`='%s' or `Element_type_id`='%s') " %(order_inform[i],TOP_LINE,BELT_LINE,FOOT_LINE,LMZ,MB,20,23))
                            part_detail_inform = cursor.fetchall()
                            total_inform += len(part_detail_inform)
                            if part_detail_inform != ():
                                code_img=exe_Barcode(order_inform[i])#使用exe生成条形码，调用。
                                rpt_title = '<para autoLeading="off" fontSize=24 align=center><b><font face="msyh">附件生产工艺单</font></b><br/><br/><br/></para>'
                                story.append(Paragraph(rpt_title, normalStyle))
                                component_data = [['', '', '', '', '', '', '', ''],
                                                  [formatted_today, formatted1_today,'', '',  '', '','',''],
                                                  ['客户名称：',str(header_data[0]),  '', '', '', '', '',order_inform[i]],
                                                  ['终端客户：',str(customer),  '', '', '', '', '', code_img],
                                                ['序号','颜色', '型号', '边型', '高', '宽','数量', '备注']]
                                for j in range(len(part_detail_inform)):
                                    part_record=[part_detail_inform[j][0],part_detail_inform[j][1],part_detail_inform[j][2],part_detail_inform[j][3],part_detail_inform[j][4],part_detail_inform[j][5]]
                                    a.append(part_record)
                                    part_inform_record=['',part_detail_inform[j][0],part_detail_inform[j][1],part_detail_inform[j][2],part_detail_inform[j][3],part_detail_inform[j][4],'',part_detail_inform[j][5]]
                                    part_inform.append(part_inform_record)
                                for j in range(len(part_detail_inform)):
                                    count=0
                                    for k in range(len(part_detail_inform)):
                                        if a[k]==a[j]:
                                            count=count+1
                                            part_inform[j][6]=count
                            else:
                                continue
                            if total_inform!=0:
                                reList=list(set([tuple(t) for t in part_inform]))# 二维列表的子元素也是列表，将子元素的一维列表转换成元组，然后使用set()去重
                                reList=[list(v) for v in reList]#将二维列表转换成元组
                                reList.sort(key=part_inform.index)  # 按照二维列表的索引值对去重之后得列表进行排序。
                                for j in range(len(reList)):
                                    reList[j][0]=j+1
                                component_data += (reList)
                                if header_data[3] != None:
                                    special_shaped = header_data[3].split('&&')
                                    downloadpic(special_shaped, order_inform[i])
                                    row=len(special_shaped)
                                    for p in range(1,len(special_shaped)+1):
                                        special_shaped_image=Image("C:\Special_Shaped\\"+str(order_inform[i])+"_"+str(p)+".png")
                                        if special_shaped_image.imageHeight>685 or special_shaped_image.imageWidth>439:
                                            special_shaped_image.drawHeight=special_shaped_image.imageHeight*0.25
                                            special_shaped_image.drawWidth=special_shaped_image.imageWidth*0.3
                                        else:
                                            special_shaped_image.drawHeight = special_shaped_image.imageHeight
                                            special_shaped_image.drawWidth = special_shaped_image.imageWidth
                                        component_data += [['图'+str(p),'','',special_shaped_image,'','','','']]
                                # component_table = Table(component_data)  #
                                component_table = Table(component_data, colWidths=[25,90,70, 90, 60, 60, 65, 45])
                                component_table.setStyle(TableStyle([
                                ('FONTNAME',(0,0),(-1,-1),'msyh'),#字体
                                ('FONTSIZE',(0,0),(-1,-1),10),#字体大小
                                ('ALIGN',(0,0),(-1,-1),'CENTER'),#对齐
                                ('ALIGN',(0,0),(0,3),'RIGHT'),#对齐
                                ('ALIGN',(1,0),(1,3),'LEFT'),#对齐
                                ('ALIGN',(-1,0),(-2,5),'RIGHT'),#对齐
                                ('VALIGN',(0,0),(-1,-1),'MIDDLE'),  #对齐
                                ('TEXTCOLOR',(-1,-1),(-1,-1),colors.black),#设置表格内文字颜色
                                ('GRID',(0,4),(-1,(-row-1)),1,colors.black),#设置表格框线为红色，线宽为0.5
                                ]))
                                story.append(component_table)
                                story.append(Spacer(0, 0.2 * inch))
                                header_data_list = list(header_data)
                                if header_data[2]==None:
                                    header_data_list[2]='无'
                                else:
                                    header_data_list[2]
                                remarks = '<para autoLeading="off" fontSize=15 align=center><b><font face="msyh">备注：%s</font></b><br/><br/><br/></para>' %  header_data_list[2]
                                para = Paragraph(remarks, normalStyle)
                                story.append(para)
                                story.append(PageBreak())
                        if total_inform!=0:
                            doc = SimpleDocTemplate("C:\Production_Process_PDF\\" + str(workorder_id) + '_line.pdf')
                            doc.build(story, canvasmaker=FooterCanvas)
                            self.viewer.LoadFile("C:\Production_Process_PDF\\" + str(workorder_id) + '_line.pdf')
                            shutil.copyfile(filename_local_name,filename_server_name)
                        else:
                            self.viewer.LoadFile('None.pdf')
                    else:
                        self.log.WriteText( "天外天程序正在运行ZX_Pane.py   Scheduling_Query_Line_PDF类 DrawTable_PDF方法 未找到生产工艺单，加载失败 \r\n")
                else:
                    return
        except:
            self.log.WriteText("天外天程序正在运行ZX_Pane.py   Scheduling_Query_Line_PDF类 DrawTable_PDF方法 报错，画pdf表格出错 请检查 \r\n")
    def OnLoadButton(self, event):
        try:
            if Is_Database_Connect():
                cursor = DB.cursor()
                for i in range(len(self.order_list)):
                    cursor.execute(
                        "UPDATE `work_cnc_before_layout_temporary` set `Print_Barcode`='%s' WHERE `Order_Id`='%s' and (`Element_type_id`='%s' or `Element_type_id`='%s' or `Element_type_id`='%s')" % ( FRAGMENTARY_BARCODE, self.order_list[i],TOP_LINE,BELT_LINE,FOOT_LINE))
                DB.commit()
            else:
                return
        except:
            self.log.WriteText('天外天系统正在运行ZX_Pane.py Scheduling_Query_PDF中OnLoadButton方法打印条形码操作出错，请检查临时待排样表单中与排产工单中订单号相对应\r\n')
    def SetValue(self,order_list):
        self.order_list = order_list
class Scheduling_Query_Layer_PDF(wx.Panel):
    def __init__(self, parent,log):
        wx.Panel.__init__(self, parent, -1)
        self.log=log
        self.cnc_inform_list=''
        vsizer = wx.BoxSizer(wx.VERTICAL)
        self.buttonpanel = pdfButtonPanel(self, wx.ID_ANY,
                                          wx.DefaultPosition, wx.DefaultSize, 0)
        vsizer.Add(self.buttonpanel, 0,
                   wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT | wx.TOP, 5)
        self.viewer = pdfViewer(self, wx.ID_ANY, wx.DefaultPosition,
                                wx.DefaultSize, wx.HSCROLL | wx.VSCROLL | wx.SUNKEN_BORDER)
        vsizer.Add(self.viewer, 1, wx.GROW | wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)
        self.SetSizer(vsizer)
        self.SetAutoLayout(True)
        self.buttonpanel.viewer = self.viewer
        self.viewer.buttonpanel = self.buttonpanel
        #self.DrawTable_PDF()  # 画pdf表
        wx.BeginBusyCursor()
        wx.EndBusyCursor()
    def DrawTable_PDF(self,order_inform,workorder_id):
        try:
            f = os.path.exists("C:\Production_Process_PDF\\")  # 用于判断在D盘中是否存在delivery_list_history文件夹，如果不在在这个路径下新建文件夹。
            if not f:
                os.mkdir("C:\Production_Process_PDF\\")  # 新建文件夹
            filename_server_name = u"\\\\192.168.31.250\\Production_Process_PDF\\" + str( workorder_id) + '_layer.pdf'
            filename_local_name = u"C:\\Production_Process_PDF\\" + str(workorder_id) + '_layer.pdf'
            is_exist_file = os.path.exists("\\\\192.168.31.250\\Production_Process_PDF\\" + str(workorder_id) + '_layer.pdf')
            if is_exist_file:
                shutil.copyfile(filename_server_name, filename_local_name)
                self.viewer.LoadFile("C:\Production_Process_PDF\\" + str(workorder_id) + '_layer.pdf')
            else:
                story = []
                stylesheet = getSampleStyleSheet()
                normalStyle = stylesheet['Normal']
                today = datetime.datetime.now()
                formatted_today = today.strftime('%Y.%m.%d')
                formatted1_today = today.strftime('%H:%M')
                #############################生成条形码
                if Is_Database_Connect():
                    cursor = DB.cursor()
                    cursor.execute("select `Order_id` from `order_order_online` where 1 " )
                    order_online=cursor.fetchall()
                    list(flatten(order_online))
                    Judgment=set(list(flatten(order_inform))).issubset(set(list(flatten(order_online))))
                    if Judgment == True:
                        total_inform=0
                        for i in range(len(order_inform)):
                            part_inform = []
                            a=[]
                            cursor = DB.cursor()
                            cursor.execute("select `Dealer` ,`Customer_name`,`remarks` from `order_order_online` where `Order_id`='%s' " % order_inform[i])
                            header_data=cursor.fetchone()
                            if header_data[1] == None:
                                customer = '无'
                            else:
                                customer = header_data[1]
                            cursor.execute(
                                "select `Board_type`,`Color`,`Bar_type`,`Board_height`,`Board_width`,`remarks` from `order_element_online` where `Order_id`='%s' AND `Element_type_id`='%s' " %(order_inform[i],LAYER))
                            part_detail_inform = cursor.fetchall()
                            total_inform+=len(part_detail_inform)
                            if part_detail_inform!=():

                                code_img=exe_Barcode(order_inform[i])
                                rpt_title = '<para autoLeading="off" fontSize=24 align=center><b><font face="msyh">压条工位工单</font></b><br/><br/><br/></para>'
                                story.append(Paragraph(rpt_title, normalStyle))
                                component_data = [['', '', '', '', '', '', '', ''],
                                                  ['', formatted_today, formatted1_today, '', '', '', '', ''],
                                                  ['', '客户名称：', str(header_data[0]), '', '', '', '',
                                                   order_inform[i]],
                                                  ['', '终端客户：', str(customer), '', '', '', '', code_img],
                                                  ['序号', '门板类型', '颜色', '压条类型', '高', '宽', '数量', '备注']]
                                for j in range(len(part_detail_inform)):
                                    door_type=part_detail_inform[j][0].split('_')
                                    del door_type[-1]
                                    door_type_split='_'.join(door_type)
                                    part_record=[door_type_split,part_detail_inform[j][1],part_detail_inform[j][2],part_detail_inform[j][3],part_detail_inform[j][4],part_detail_inform[j][5]]
                                    a.append(part_record)
                                    part_inform_record = ['',door_type_split, part_detail_inform[j][1],part_detail_inform[j][2], part_detail_inform[j][3],part_detail_inform[j][4],'1',part_detail_inform[j][5]]
                                    part_inform.append(part_inform_record)
                                for j in range(len(part_detail_inform)):
                                    count=0
                                    for k in range(len(part_detail_inform)):
                                        if a[k]==a[j]:
                                            count=count+1
                                            part_inform[j][6]=count
                                        else:
                                            pass
                            else:
                                continue
                            if total_inform != 0:
                                reList = list(set([tuple(t) for t in part_inform]))#二维列表的子元素也是列表，将子元素的一维列表转换成元组，然后使用set()去重
                                reList = [list(v) for v in reList]
                                reList.sort(key=part_inform.index)#按照二维列表的索引值对去重之后得列表进行排序。
                                for m in range(len(reList)):
                                    reList[m][0]=m+1
                                component_data += (reList)
                                component_table = Table(component_data)  #
                                component_table.setStyle(TableStyle([
                                ('FONTNAME',(0,0),(-1,-1),'msyh'),#字体
                                ('FONTSIZE',(0,0),(-1,-1),10),#字体大小
                                ('ALIGN',(0,0),(-1,-1),'CENTER'),#对齐
                                ('ALIGN',(1,0),(1,3),'RIGHT'),#对齐
                                ('ALIGN',(2,0),(2,3),'LEFT'),#对齐
                                ('ALIGN',(-1,0),(-2,5),'RIGHT'),#对齐
                                ('VALIGN',(0,0),(-1,-1),'MIDDLE'),  #对齐
                                ('TEXTCOLOR',(0,1),(-2,-1),colors.black),#设置表格内文字颜色
                                ('GRID',(0,4),(-1,-1),1,colors.black),#设置表格框线为红色，线宽为0.5
                                ]))
                                story.append(component_table)
                                story.append(Spacer(0, 0.2 * inch))
                                header_data_list = list(header_data)
                                if header_data[2]==None:
                                    header_data_list[2]='无'
                                else:
                                    header_data_list[2]
                                remarks = '<para autoLeading="off" fontSize=15 align=center><b><font face="msyh">备注：%s</font></b><br/><br/><br/></para>' % \
                                          header_data_list[2]
                                para = Paragraph(remarks, normalStyle)
                                story.append(para)
                                story.append(PageBreak())
                            else:
                                continue
                        if total_inform!=0:
                            doc = SimpleDocTemplate("C:\Production_Process_PDF\\" + str(workorder_id) + '_layer.pdf')
                            doc.build(story,canvasmaker=FooterCanvas)
                            self.viewer.LoadFile("C:\Production_Process_PDF\\" + str(workorder_id) + '_layer.pdf')
                            shutil.copyfile(filename_local_name,filename_server_name)
                        else:
                            self.viewer.LoadFile('None.pdf')
                    else:
                        self.log.WriteText("天外天程序正在运行ZX_Pane.py   Scheduling_Query_Layer_PDF类 未找到生产工艺单，加载失败 \r\n")
                else:
                    return
        except:
            self.log.WriteText("天外天程序正在运行ZX_Pane.py   Scheduling_Query_Layer_PDF类 DrawTable_PDF方法 报错，画pdf表格出错 请检查 \r\n")
class Scheduling_Query_Assembly_PDF(wx.Panel):
    def __init__(self, parent,log):
        wx.Panel.__init__(self, parent, -1)
        self.log=log
        self.a=1
        vsizer = wx.BoxSizer(wx.VERTICAL)
        self.buttonpanel = pdfButtonPanel(self, wx.ID_ANY,
                                          wx.DefaultPosition, wx.DefaultSize, 0)
        vsizer.Add(self.buttonpanel, 0,
                   wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT | wx.TOP, 5)
        self.viewer = pdfViewer(self, wx.ID_ANY, wx.DefaultPosition,
                                wx.DefaultSize, wx.HSCROLL | wx.VSCROLL | wx.SUNKEN_BORDER)
        vsizer.Add(self.viewer, 1, wx.GROW | wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)
        self.SetSizer(vsizer)
        self.SetAutoLayout(True)
        self.buttonpanel.viewer = self.viewer
        self.viewer.buttonpanel = self.buttonpanel
        #self.DrawTable_PDF()  # 画pdf表
        wx.BeginBusyCursor()
        wx.EndBusyCursor()
    def DrawTable_PDF(self,order_inform,workorder_id):
        try:
            f = os.path.exists("C:\Production_Process_PDF\\")  # 用于判断在D盘中是否存在delivery_list_history文件夹，如果不在在这个路径下新建文件夹。
            if not f:
                os.mkdir("C:\Production_Process_PDF\\")  # 新建文件夹
            filename_server_name = u"\\\\192.168.31.250\\Production_Process_PDF\\" + str( workorder_id) + '_assembly.pdf'
            filename_local_name = u"C:\\Production_Process_PDF\\" + str(workorder_id) + '_assembly.pdf'
            is_exist_file = os.path.exists( "\\\\192.168.31.250\\Production_Process_PDF\\" + str(workorder_id) + '_assembly.pdf')
            if is_exist_file:
                shutil.copyfile(filename_server_name, filename_local_name)
                self.viewer.LoadFile("C:\Production_Process_PDF\\" + str(workorder_id) + '_assembly' + '.pdf')
            else:
                story = []
                stylesheet = getSampleStyleSheet()
                normalStyle = stylesheet['Normal']
                today = datetime.datetime.now()
                formatted_today = today.strftime('%Y.%m.%d')
                formatted1_today = today.strftime('%H:%M')
                #############################生成条形码
                if Is_Database_Connect():
                    cursor = DB.cursor()
                    cursor.execute("select `Order_id` from `order_order_online` where 1 " )
                    order_online=cursor.fetchall()
                    list(flatten(order_online))
                    Judgment=set(list(flatten(order_inform))).issubset(set(list(flatten(order_online))))
                    if Judgment == True:
                        total_inform=0
                        for i in range(len(order_inform)):
                            a=[]
                            part_inform = []
                            cursor = DB.cursor()
                            cursor.execute("select `Dealer` ,`Customer_name`,`remarks` from `order_order_online` where `Order_id`='%s' " % order_inform[i])
                            header_data=cursor.fetchone()
                            if header_data[1] == None:
                                customer = '无'
                            else:
                                customer = header_data[1]
                            cursor.execute(
                                "select `Board_type`,`Color`,`Board_height` ,`Board_width`,`remarks` ,`Element_type_id` ,`Open_way` from `order_element_online` where `Order_id`='%s' AND (`Element_type_id`='%s' or `Element_type_id`='%s' or `Element_type_id`='%s'or `Element_type_id`='%s' or `Element_type_id`='%s' or `Element_type_id`='%s'or `Element_type_id`='%s') " %(order_inform[i],TRUE_SHUTTER,GRID_DOOR,DOUBLE_COLOR_LAYER,22,21,19,11))
                            part_detail_inform = cursor.fetchall()
                            total_inform+=len(part_detail_inform)
                            if len(part_detail_inform)!=0:
                                code_img=exe_Barcode(order_inform[i])
                                rpt_title = '<para autoLeading="off" fontSize=24 align=center><b><font face="msyh">组装工位工单</font></b><br/><br/><br/></para>'
                                story.append(Paragraph(rpt_title, normalStyle))
                                component_data = [['', '', '', '', '', '', '', ''],
                                                  ['', formatted_today, formatted1_today, '', '', '', '', ''],
                                                  ['', '客户名称：', str(header_data[0]), '', '', '', '',
                                                   order_inform[i]],
                                                  ['', '终端客户：', str(customer), '', '', '', '', code_img],
                                                  ['序号', '门板类型', '颜色', '零件类型','开孔方向', '高', '宽', '数量', '备注']]
                                for j in range(len(part_detail_inform)):
                                    door_type = part_detail_inform[j][0].split('_')
                                    element_name=door_type[-1]
                                    del door_type[-1]
                                    door_type_split = '_'.join(door_type)
                                    part_record=[door_type_split,part_detail_inform[j][1],element_name,part_detail_inform[j][6],part_detail_inform[j][2],part_detail_inform[j][3],part_detail_inform[j][4]]
                                    a.append(part_record)
                                    part_inform_record=['',door_type_split,part_detail_inform[j][1],element_name,part_detail_inform[j][6],part_detail_inform[j][2],part_detail_inform[j][3],'',part_detail_inform[j][4]]
                                    part_inform.append(part_inform_record)
                                for j in range(len(part_detail_inform)):
                                    count=0
                                    for k in range(len(part_detail_inform)):
                                        if a[k]==a[j]:
                                            count=count+1
                                        else:
                                            pass
                                    part_inform[j][7] = count
                            else:
                                continue
                            if total_inform!=0:
                                reList = list(set([tuple(t) for t in part_inform]))#二维列表的子元素也是列表，将子元素的一维列表转换成元组，然后使用set()去重
                                reList = [list(v) for v in reList]
                                reList.sort(key=part_inform.index)#按照二维列表的索引值对去重之后得列表进行排序。
                                for m in range(len(reList)):
                                    reList[m][0]=m+1
                                component_data += (reList)
                                component_table = Table(component_data)  #
                                component_table.setStyle(TableStyle([
                                ('FONTNAME',(0,0),(-1,-1),'msyh'),#字体
                                ('FONTSIZE',(0,0),(-1,-1),10),#字体大小
                                ('ALIGN',(0,0),(-1,-1),'CENTER'),#对齐
                                # ('ALIGN',(-1,0),(-1,4),'LEFT'),#对齐
                                ('ALIGN',(1,0),(1,3),'RIGHT'),#对齐
                                ('ALIGN',(2,0),(2,3),'LEFT'),#对齐
                                ('ALIGN',(-1,0),(-2,5),'RIGHT'),#对齐
                                ('VALIGN',(0,0),(-1,-1),'MIDDLE'),  #对齐
                                ('TEXTCOLOR',(0,1),(-2,-1),colors.black),#设置表格内文字颜色
                                ('GRID',(0,4),(-1,-1),1,colors.black),#设置表格框线为红色，线宽为0.5
                                ]))
                                story.append(component_table)
                                story.append(Spacer(0, 0.2 * inch))
                                header_data_list = list(header_data)
                                if header_data[2]==None:
                                    header_data_list[2]='无'
                                else:
                                    header_data_list[2]
                                remarks = '<para autoLeading="off" fontSize=15 align=center><b><font face="msyh">备注：%s</font></b><br/><br/><br/></para>' %  header_data_list[2]
                                para = Paragraph(remarks, normalStyle)
                                story.append(para)
                                story.append(PageBreak())
                        if total_inform!=0:
                            doc = SimpleDocTemplate("C:\Production_Process_PDF\\" + str(workorder_id) + '_assembly' + '.pdf')
                            doc.build(story,canvasmaker=FooterCanvas)
                            self.viewer.LoadFile("C:\Production_Process_PDF\\" + str(workorder_id) + '_assembly' + '.pdf')
                            shutil.copyfile(filename_local_name,filename_server_name)
                        else:
                            self.viewer.LoadFile('None.pdf')
                    else:
                        self.log.WriteText("天外天程序正在运行ZX_Pane.py   Scheduling_Query_Assembly_PDF类 未找到生产工艺单，加载失败 \r\n")
                else:
                    return
        except:
            self.log.WriteText("天外天程序正在运行ZX_Pane.py   Scheduling_Query_Assembly_PDF类 DrawTable_PDF方法 报错，画pdf表格出错 请检查 \r\n")
class Scheduling_Query_Right_Panel(wx.Notebook):
    def __init__(self, parent, id, log):
        wx.Notebook.__init__(self, parent, id, size=(21,21), style=
                             wx.BK_DEFAULT|wx.SUNKEN_BORDER
                             #wx.BK_TOP
                             #wx.BK_BOTTOM
                             #wx.BK_LEFT
                             #wx.BK_RIGHT
                             # | wx.NB_MULTILINE
                             )
        self.log = log
        # self.pvc_workposition_right_show1 = Pvc_Workposition_Right_Panel_Workorder(self,self.log)
        self.scheduling_query_cnc_PDF = Scheduling_Query_PDF(self,self.log)
        self.scheduling_query_scattered_PDF = Scheduling_Query_Scattered_PDF(self,self.log)
        self.scheduling_query_line_PDF = Scheduling_Query_Line_PDF(self,self.log)
        self.scheduling_query_layer_PDF = Scheduling_Query_Layer_PDF(self,self.log)
        self.scheduling_query_assembly_PDF = Scheduling_Query_Assembly_PDF(self,self.log)
        self.scheduling_query_double_sided_PDF = Scheduling_Query_Double_Sided_PDF(self,self.log)
        self.scheduling_query_rework_PDF = Scheduling_Query_Rework_PDF(self,self.log)
        # self.AddPage(self.pvc_workposition_right_show1, "工位工单管理")
        self.AddPage(self.scheduling_query_cnc_PDF, "CNC生产工艺单")
        self.AddPage(self.scheduling_query_scattered_PDF, "散板工位工艺单")
        self.AddPage(self.scheduling_query_line_PDF, "附件工位工艺单")
        self.AddPage(self.scheduling_query_layer_PDF, "压条工位工艺单")
        self.AddPage(self.scheduling_query_assembly_PDF, "组装工位工艺单")
        self.AddPage(self.scheduling_query_double_sided_PDF, "双面板工艺单")
        self.AddPage(self.scheduling_query_rework_PDF, "返工工艺单")
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnPageChanging)

    def OnPageChanged(self, event):
        if self:
            old = event.GetOldSelection()
            new = event.GetSelection()
            sel = self.GetSelection()
            # self.log.write('OnPageChanged,  old:%d, new:%d, sel:%d\n' % (old, new, sel))
        event.Skip()

    def OnPageChanging(self, event):
        if self:
            old = event.GetOldSelection()
            new = event.GetSelection()
            sel = self.GetSelection()
            # self.log.write('OnPageChanging, old:%d, new:%d, sel:%d\n' % (old, new, sel))
        event.Skip()
class Scheduling_Query_Middle_Panel(wx.Panel):
    def __init__(self,parent,log,drawPDF,layer_PDF,line_PDF,assembly_PDF,scattered_PDF,double_sided_PDF,rework_PDF):
        wx.Panel.__init__(self, parent, -1,style=wx.BK_DEFAULT|wx.SUNKEN_BORDER)
        self.log=log
        # self.drawPdf=drawPDF
        self.scheduling_detailed_query_grid=Scheduling_Detailed_Query_Grid(self,self.log)
        self.scheduling_query_grid=Scheduling_Query_Grid(self,self.log,drawPDF,self.scheduling_detailed_query_grid,layer_PDF,line_PDF,assembly_PDF,scattered_PDF,double_sided_PDF,rework_PDF)
        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox1.Add(self.scheduling_query_grid, proportion=4, flag=wx.EXPAND | wx.ALL, border=3)
        vbox1.Add(self.scheduling_detailed_query_grid, proportion=1, flag=wx.EXPAND | wx.ALL, border=3)
        self.SetSizer(vbox1)
        # self.timer = wx.PyTimer(self.Refresh_right)
        # self.timer.Start(5000)
    def Refresh_left(self):
        pass
class Scheduling_Query_Management_Panel(wx.Panel):
    def __init__(self, parent,log, id=wx.ID_ANY, title="", pos=wx.DefaultPosition,
                 size=(700,650), style=wx.DEFAULT_FRAME_STYLE):
        wx.Panel.__init__(self, parent)
        self._flags = 0
        self.log=log
        self.order_sum = 0
        self.order_area_sum = 0
        self.package_sum = 0
        self._leftWindow1 = wx.adv.SashLayoutWindow(self, 101, wx.DefaultPosition,
                                                wx.Size(250, 1000), wx.NO_BORDER |
                                                wx.adv.SW_3D | wx.CLIP_CHILDREN)
        self._leftWindow1.SetDefaultSize(wx.Size(250, 1000))
        self._leftWindow1.SetOrientation(wx.adv.LAYOUT_VERTICAL)
        self._leftWindow1.SetAlignment(wx.adv.LAYOUT_LEFT)
        self._leftWindow1.SetSashVisible(wx.adv.SASH_RIGHT, True)
        self._leftWindow1.SetExtraBorderSize(10)
        self._pnl = 0
        # self.scheduling_query_PDF=Scheduling_Query_PDF(self,self.log)
        self._leftWindow2= wx.adv.SashLayoutWindow(self, 102, wx.DefaultPosition,
                                                    wx.Size(950, 1000), wx.NO_BORDER |
                                                    wx.adv.SW_3D | wx.CLIP_CHILDREN)
        self._leftWindow2.SetDefaultSize(wx.Size(250, 500))
        # self.scheduling_query_PDF.SetDefaultSize(wx.Size(550, 1000))
        self._leftWindow2.SetOrientation(wx.adv.LAYOUT_HORIZONTAL)
        self._leftWindow2.SetAlignment(wx.adv.LAYOUT_BOTTOM)
        self._leftWindow2.SetSashVisible(wx.adv.SASH_TOP, True)
        self._leftWindow2.SetExtraBorderSize(10)
        self._pnl = 0
        self.ID_WINDOW_TOP = 100
        self.ID_WINDOW_LEFT1 = 101
        self.ID_WINDOW_RIGHT1 = 102
        self.ID_WINDOW_BOTTOM = 103
        self._leftWindow1.Bind(wx.adv.EVT_SASH_DRAGGED_RANGE, self.OnFoldPanelBarDrag,
                               id=100, id2=103)
        self._leftWindow2.Bind(wx.adv.EVT_SASH_DRAGGED_RANGE, self.OnFoldPanelBarDrag,
                               id=100, id2=103)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.ReCreateFoldPanel(0)
        self.OnPDFShow()
        self.zx_scheduling_query_middle_panel= Scheduling_Query_Middle_Panel(self,self.log,self.scheduling_query_PDF.scheduling_query_cnc_PDF,self.scheduling_query_PDF.scheduling_query_layer_PDF,self.scheduling_query_PDF.scheduling_query_line_PDF,
                                                                             self.scheduling_query_PDF.scheduling_query_assembly_PDF,self.scheduling_query_PDF.scheduling_query_scattered_PDF ,self.scheduling_query_PDF.scheduling_query_double_sided_PDF,
                                                                            self.scheduling_query_PDF.scheduling_query_rework_PDF)
        # self.order_list=self.zx_scheduling_query_middle_panel.scheduling_query_grid.order_list
        # self.timer = wx.PyTimer(self.SendWechatMsg)
        # self.timer.Start(5000)
    def OnSize(self, event):
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self._leftWindow1)
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self._leftWindow2)
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.zx_scheduling_query_middle_panel)
        event.Skip()
    def OnQuit(self, event):
        self.Destroy()
    def OnToggleWindow(self, event):
        self._leftWindow1.Show(not self._leftWindow1.IsShown())
        self._leftWindow2.Show(not self._leftWindow2.IsShown())
        # Leaves bits of itself behind sometimes
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.zx_scheduling_query_middle_panel)
        self.zx_scheduling_query_middle_panel.Refresh()
        event.Skip()
    def OnFoldPanelBarDrag(self, event):
        # if event.GetDragStatus() == wx.SASH_STATUS_OUT_OF_RANGE:
        #     return
        if event.GetId() == self.ID_WINDOW_LEFT1:
            self._leftWindow1.SetDefaultSize(wx.Size(event.GetDragRect().width, 1000))
        if event.GetId() == self.ID_WINDOW_RIGHT1:
            # self._leftWindow2.SetDefaultSize(wx.Size(event.GetDragRect().width, 1000))
            self._leftWindow2.SetDefaultSize(wx.Size(1000, event.GetDragRect().height))#可以上下拖动空间窗口
        # Leaves bits of itself behind sometimes
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.zx_scheduling_query_middle_panel)
        self.zx_scheduling_query_middle_panel.Refresh()
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
        self.date_start = wx.DateTimeFromDMY  # canlander日历的起始时间获得
        self.date_end = wx.DateTimeFromDMY  # canlander日历的截至时间获得
        self.calendar_begin = PopDateControl(item, -1)
        self.calendar_begin.textCtrl.SetValue("从:")
        self._pnl.AddFoldPanelWindow(item, self.calendar_begin, fpb.FPB_ALIGN_WIDTH, 2, 20)
        self.calendar_end = PopDateControl(item, -1)
        self.calendar_end.textCtrl.SetValue("至:")
        self._pnl.AddFoldPanelWindow(item, self.calendar_end, fpb.FPB_ALIGN_WIDTH, 2, 20)
        btn_date_start = wx.Button(item, wx.ID_ANY, "开始日期查询")
        self._pnl.AddFoldPanelWindow(item, btn_date_start)
        btn_date_start.Bind(wx.EVT_BUTTON, self.OnDateStart)
        self._pnl.AddFoldPanelSeparator(item)  # 设置分割线
        self.cal = CalendarCtrl(item, -1, wx.DateTime().Today(),
                                style=wx.adv.CAL_SEQUENTIAL_MONTH_SELECTION)
        self.cal.Bind(wx.adv.EVT_CALENDAR_SEL_CHANGED, self.OnCalSelChanged)
        self._pnl.AddFoldPanelWindow(item,self.cal,fpb.FPB_ALIGN_WIDTH,0,0)
        self._pnl.AddFoldPanelSeparator(item)
        btn_today = wx.Button(item, wx.ID_ANY, "今天")
        btn_today.Bind(wx.EVT_BUTTON, self.OnTodayQuery)
        self._pnl.AddFoldPanelWindow(item, btn_today)
        btn_yesterday = wx.Button(item, wx.ID_ANY, "昨天")
        btn_yesterday.Bind(wx.EVT_BUTTON, self.OnYesterdayQuery)
        self._pnl.AddFoldPanelWindow(item, btn_yesterday,spacing=0)
        btn_Byesterday = wx.Button(item, wx.ID_ANY, "前天")
        btn_Byesterday.Bind(wx.EVT_BUTTON, self.OnBYesterdayQuery)
        self._pnl.AddFoldPanelWindow(item, btn_Byesterday,spacing=0)
        btn_BByesterday = wx.Button(item, wx.ID_ANY, "大前天")
        btn_BByesterday.Bind(wx.EVT_BUTTON, self.OnBBYesterdayQuery)
        self._pnl.AddFoldPanelWindow(item, btn_BByesterday, spacing=0)
        self._pnl.AddFoldPanelSeparator(item)
        # self._pnl.AddFoldPanelSeparator(item)
        # btn_SendWeChat = wx.Button(item, wx.ID_ANY, "微信任务发布")
        # btn_SendWeChat.Bind(wx.EVT_BUTTON, self.OnWriteWechatMsg)
        # self._pnl.AddFoldPanelWindow(item, btn_SendWeChat,spacing=3)
        self._pnl.AddFoldPanelSeparator(item)
    def OnDateStart(self,eve):
        try:
            date_start = self.calendar_begin.GetValue()
            date_end = self.calendar_end.GetValue()
            if date_start == "从:" or date_end == "至:":
                pass
                # self.start_time = "从:"
                # self.end_time = "至:"
            else:
                t1 = date_start.split('/')
                t2 = t1[2], t1[1], t1[0]
                st = '-'
                self.start_time = st.join(t2)
                t3 = date_end.split('/')
                t4 = t3[2], t3[1], t3[0]
                et = '-'
                self.end_time = et.join(t4)
                self.zx_scheduling_query_middle_panel.scheduling_query_grid.SetValue(self.start_time, self.end_time)
                self.zx_scheduling_query_middle_panel.scheduling_query_grid.MyRefresh()
            # print '111',self.start_time,self.end_time
        except:
            self.log.WriteText("天外天系统正在运行ZX_Pane.py Scheduling_Query_Management_Panel()中OnDateStart(),出现错误，请进行检查！ \r\n")
    def OnCalSelChanged(self, eve):
        t1 = str(self.cal.GetDate())
        t2 = t1.split(' ')
        t3 = t2[0].split('/')
        # t4 = t3[2], t3[0], t3[1]
        start_time1 = '%s%s-%s-%s' % ('20', t3[2], t3[0], t3[1])
        end_time1 = '%s%s-%s-%s' % ('20', t3[2], t3[0], t3[1])

        self.calendar_begin.textCtrl.SetValue('%s/%s/%s%s' % ( t3[1], t3[0],'20',t3[2]))#使查询界面上
        self.calendar_end.textCtrl.SetValue('%s/%s/%s%s' % ( t3[1], t3[0],'20',t3[2]))
        # dt = ''
        # start_time = dt.join(t4)
        # start_time1 = '20'+start_time
        self.zx_scheduling_query_middle_panel.scheduling_query_grid.SetValue(start_time1,end_time1)
        self.zx_scheduling_query_middle_panel.scheduling_query_grid.MyRefresh()
        self.log.WriteText( "天外天系统收到操作员控制指令，ZX_Pane.py 开始执行工位工单日期查询操作，日期：" + str(start_time1) + "\r\n")
    def OnTodayQuery(self, eve):
        start_today = datetime.date.today().strftime('%Y-%m-%d')
        end_today = datetime.date.today().strftime('%Y-%m-%d')
        today = datetime.date.today().strftime('%d/%m/%Y')#用于日历时间段查询
        self.calendar_begin.textCtrl.SetValue(today)
        self.calendar_end.textCtrl.SetValue(today)
        self.zx_scheduling_query_middle_panel.scheduling_query_grid.SetValue(start_today,end_today)
        self.zx_scheduling_query_middle_panel.scheduling_query_grid.MyRefresh()
        self.log.WriteText(
            "天外天系统收到操作员控制指令，ZX_Pane.py 开始执行工位工单日期查询操作，日期：" + str(start_today) + "\r\n")
    def OnYesterdayQuery(self, eve):
        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        start_yesterday = (today - oneday).strftime('%Y-%m-%d')
        end_yesterday = (today - oneday).strftime('%Y-%m-%d')
        yesterday = (today - oneday).strftime('%d/%m/%Y')  # 用于日历时间段查询
        self.calendar_begin.textCtrl.SetValue(yesterday)
        self.calendar_end.textCtrl.SetValue(yesterday)
        self.zx_scheduling_query_middle_panel.scheduling_query_grid.SetValue(start_yesterday,end_yesterday)
        self.zx_scheduling_query_middle_panel.scheduling_query_grid.MyRefresh()
        self.log.WriteText(
            "天外天系统收到操作员控制指令，ZX_Pane.py开始执行工位工单日期查询操作，日期：" + str(start_yesterday) + "\r\n")
    def OnBYesterdayQuery(self, eve):
        today = datetime.date.today()
        twoday = datetime.timedelta(days=2)
        start_Byesterday = (today - twoday).strftime('%Y-%m-%d')
        end_Byesterday = (today - twoday).strftime('%Y-%m-%d')
        Byesterday = (today - twoday).strftime('%d/%m/%Y')  # 用于日历时间段查询
        self.calendar_begin.textCtrl.SetValue(Byesterday)
        self.calendar_end.textCtrl.SetValue(Byesterday)
        self.zx_scheduling_query_middle_panel.scheduling_query_grid.SetValue(start_Byesterday,end_Byesterday)
        self.zx_scheduling_query_middle_panel.scheduling_query_grid.MyRefresh()
        self.log.WriteText(
            "天外天系统收到操作员控制指令，ZX_Pane.py开始执行工位工单日期查询操作，日期：" + str(start_Byesterday) + "\r\n")
    def OnBBYesterdayQuery(self, eve):
        today = datetime.date.today()
        threeday = datetime.timedelta(days=3)
        start_BByesterday = (today - threeday).strftime('%Y-%m-%d')
        end_BByesterday = (today - threeday).strftime('%Y-%m-%d')
        BByesterday = (today - threeday).strftime('%d/%m/%Y')  # 用于日历时间段查询
        self.calendar_begin.textCtrl.SetValue(BByesterday)
        self.calendar_end.textCtrl.SetValue(BByesterday)
        self.zx_scheduling_query_middle_panel.scheduling_query_grid.SetValue(start_BByesterday,end_BByesterday)
        self.zx_scheduling_query_middle_panel.scheduling_query_grid.MyRefresh()
        self.log.WriteText(
            "天外天系统收到操作员控制指令，ZX_Pane.py开始执行工位工单日期查询操作，日期：" + str(start_BByesterday) + "\r\n")
    def OnWriteWechatMsg(self,eve):
        try:
            t1 = str(self.cal.GetDate())
            t2 = t1.split(' ')
            t3 = t2[0].split('/')
            start_time = '%s%s-%s-%s' % ('20', t3[2], t3[0], t3[1])
            # today = datetime.datetime.now()
            # formatted_today = today.strftime('%Y-%m-%d')
            if Is_Database_Connect():
                cursor = DB.cursor()
                cursor.execute(
                    "SELECT `Total_order_area`,`Total_batch_num`,`Single_18_board_num`,`Rhombic_18_board_num`,`Glass_door_num`,`Spare_order_id` from `work_cnc_workorder_query` WHERE `Schedule_date`='%s' and `State`='%s'" % (start_time,5))
                record = cursor.fetchall()
                if record != ():
                    for i in range(len(record)):
                        if record[i][6]!=None:
                            spare_order=record[i][5].split(',')
                            spare_count=len(spare_order)
                        else:
                            spare_count =0
                        CNC_Msg = start_time + '日连线加工中心排产任务为:订单总面积 ' + str(record[i][0]) + '平方米,共有' + str( record[i][1]) + '个批次，其中18毫米单面板有' + str(
                            record[i][2]) + '床、18毫米菱格板有' + str(record[i][3]) + '床，玻璃门有' + str(record[i][4]) + '床。祝您工作愉快！'
                        Scatter_Mag = start_time+'日散板加工中心排产任务为:订单共 '+str(spare_count) + '个,散板总面积共'+ str( record[i][1])+'平方米。祝您工作愉快！'
                        Material_Msg=start_time +'日排产任务需要18毫米素板 '+ str(record[i][2]) + '张、18毫米单面板'+str(record[i][3])+'张、18毫米菱格板' + str(record[i][4]) +'张，请提前准备。'
                        Hole_Msg=start_time+'日排产任务需要的打孔门板面积有'+ str(record[i][2]) +'平方米。'
                        Layer_Msg=start_time+'日排产任务需要的压条面积'+ str(record[i][2]) +'平方米，具体参照生产工艺单。请提前准备！'
                        cursor = DB1.cursor()
                        cursor.execute( "INSERT INTO `info_wechat`(`Receive_Group`,`Message`,`State`) VALUES ('%s','%s','%s')" % (CNC_POSITION, CNC_Msg, WAIT_WECHAT_SEND))
                        cursor.execute( "INSERT INTO `info_wechat`(`Receive_Group`,`Message`,`State`) VALUES ('%s','%s','%s')" % (CNC_POSITION, Scatter_Mag, WAIT_WECHAT_SEND))
                        cursor.execute( "INSERT INTO `info_wechat`(`Receive_Group`,`Message`,`State`) VALUES ('%s','%s','%s')" % (MATERIAL_POSITION, Material_Msg, WAIT_WECHAT_SEND))
                        cursor.execute( "INSERT INTO `info_wechat`(`Receive_Group`,`Message`,`State`) VALUES ('%s','%s','%s')" % (HOLE_POSITION, Hole_Msg, WAIT_WECHAT_SEND))
                        cursor.execute( "INSERT INTO `info_wechat`(`Receive_Group`,`Message`,`State`) VALUES ('%s','%s','%s')" % (LAYER_POSITION, Layer_Msg, WAIT_WECHAT_SEND))
                    DB1.commit()
                else:
                    pass
            else:
                self.log.WriteText('天外天系统正在运行ZX_Pane.py，数据库连接出现问题，请检查\r\n')
                return
        except:
            self.log.WriteText('天外天系统正在运行ZX_Pane.py，在往数据库更新微信信息时出现错误，请检查\r\n')
    def SendWechatMsg(self):
        try:
            if Is_Database_Connect():
                cursor=DB.cursor()
                cursor.execute("select `Job_id`,`checkin_time` from `info_staff_login_state` where `is_login_state`='%s' " % LOGIN)
                record = cursor.fetchall()
                if record != ():
                    for i in range(len(record)):
                        # today = datetime.datetime.now()
                        # self.today = today.strftime('%y%m%d')
                        start_time=record[i][1].strftime('%Y-%m-%d')
                        cursor = DB1.cursor()
                        cursor.execute("select `Name`,`Remarkname`,`Position_name`,`Position` from `info_staff_new` where `Job_id`='%s' " % record[i][0])
                        staff_record = cursor.fetchall()
                    for j in range(len(staff_record)):
                        if staff_record[j][3]==6:
                            cursor = DB.cursor()
                            cursor.execute(
                                "SELECT `Total_order_area`,`Total_batch_num`,`Single_18_board_num`,`Rhombic_18_board_num`,`Glass_door_num`,`Spare_order_id` from `work_cnc_workorder_query` WHERE `Schedule_date`='%s' and `State`='%s'" % (
                                start_time, 5))
                            record = cursor.fetchall()
                            if record != ():
                                for i in range(len(record)):
                                    Wechat_Msg  = start_time + '日连线加工中心排产任务为:订单总面积 ' + str(record[i][0]) + '平方米,共有' + str(
                                        record[i][1]) + '个批次，其中18毫米单面板有' + str(
                                        record[i][2]) + '床、18毫米菱格板有' + str(record[i][3]) + '床，玻璃门有' + str(
                                        record[i][4]) + '床。祝您工作愉快！'
                                    users = itchat.search_friends(staff_record[j][1])
                                    if users!={}:
                                        userName = users[0]['UserName']
                                        itchat.send(Wechat_Msg, toUserName=userName)
                #             cursor = DB1.cursor()
                #             cursor.execute("UPDATE `info_wechat` set `State`='%s' WHERE `State`='%s'" % (COMPLETE_SEND, WAIT_WECHAT_SEND))
                # DB1.commit()
            else:
                return
        except:
            print("请检查数据库中该工位工作人员的备注名称是否与注册时所给备注相同\r\n")
    def OnPDFShow(self):
        self._leftWindow2.DestroyChildren()
        self.scheduling_query_PDF=Scheduling_Query_Right_Panel(self._leftWindow2,-1,self.log)
#-------------------------------------------------------下载异形图片
def downloadpic(special_shaped,order_id):#在特别指定URL地址去下载图片验证码，并保存为pic.png的图片
    pwd = os.path.exists("C:\Special_Shaped\\")
    if pwd:#判断文件夹是否存在，如果不存在则创建
        pass
        # print "File Exist!!!"
    else:
        os.mkdir("C:\Special_Shaped\\")
    #下载图片验证码文件，并保存
    for i in range(1,len(special_shaped)+1):
        # pic_url = "http://www.hanhai-order.com/user/project/images/"+str(special_shaped[i-1])#请求验证码生成页面的地址
        try:
            pic_url = "http://192.168.31.249/user/project/images/"+str(special_shaped[i-1])#请求验证码生成页面的地址
            pic_data_url = urllib2.urlopen(pic_url)
            pic_data = pic_data_url.read()  # 读取验证码图片
        except:
            pic_url = "http://120.77.38.174/s.fkgeek.com/public/user/project/images/" + str(special_shaped[i-1])  # 请求验证码生成页面的地址
            pic_data_url = urllib2.urlopen(pic_url)
            pic_data = pic_data_url.read()#读取验证码图片
        # localtime = time.strftime("%Y%m%d%H%M%S",time.localtime())
        filename = "C:\Special_Shaped\\"+str(order_id)+"_"+str(i)+".png"#文件名格式
        f = open(filename,"wb")
        f.write(pic_data)
        f.close()
        print "文件"+"  "+str(i)+":"+str(order_id)+"_"+str(i)+".png"
        time.sleep(1)#暂停一秒
    print "文件保存完成！！"
#---------------------------------------------------库管理场地管理界面
class Song(object):
    def __init__(self, sec_id, part_id,type,color,height,width,Double_color,Archaize,Edge_type):
        self.genre = sec_id
        self.id = part_id
        self.artist = type
        self.title = color
        self.text = height
        self.width = width
        self.double_color = Double_color
        self.date = Archaize
        self.like = Edge_type
    # def __repr__(self):
    #     return 'Song: %s-%s' % (self.artist, self.title)
class Genre(object):
    def __init__(self, name):
        self.name = name
        self.songs = []
    def __repr__(self):
        return 'Genre: ' + self.name
#----------------------------------------------------------------------
class MyTreeListModel(dv.PyDataViewModel):
    def __init__(self, data, log):
        dv.PyDataViewModel.__init__(self)
        self.data = data
        self.log = log

        # The PyDataViewModel derives from both DataViewModel and from
        # DataViewItemObjectMapper, which has methods that help associate
        # data view items with Python objects. Normally a dictionary is used
        # so any Python object can be used as data nodes. If the data nodes
        # are weak-referencable then the objmapper can use a
        # WeakValueDictionary instead.
        self.UseWeakRefs(True)
    # Report how many columns this model provides data for.
    def GetColumnCount(self):
        return 6
    # Map the data column numbers to the data type
    def GetColumnType(self, col):
        mapper = { 0 : 'string',
                   1 : 'string',
                   2 : 'string',
                   3 : 'string', # the real value is an int, but the renderer should convert it okay
                   4 : 'string',
                   5 : 'string',
                   6 : 'string',
                   7 : 'string',
                   8 : 'string',
                   }
        return mapper[col]

    def GetChildren(self, parent, children):
        if not parent:
            for genre in self.data:
                children.append(self.ObjectToItem(genre))
            return len(self.data)
        node = self.ItemToObject(parent)
        if isinstance(node, Genre):
            for song in node.songs:
                children.append(self.ObjectToItem(song))
            return len(node.songs)
        return 0
    def IsContainer(self, item):
        # Return True if the item has children, False otherwise.
        ##self.log.write("IsContainer\n")

        # The hidden root is a container
        if not item:
            return True
        # and in this model the genre objects are containers
        node = self.ItemToObject(item)
        if isinstance(node, Genre):
            return True
        # but everything else (the song objects) are not
        return False
    #def HasContainerColumns(self, item):
    #    self.log.write('HasContainerColumns\n')
    #    return True
    def GetParent(self, item):
        # Return the item which is this item's parent.
        ##self.log.write("GetParent\n")

        if not item:
            return dv.NullDataViewItem

        node = self.ItemToObject(item)
        if isinstance(node, Genre):
            return dv.NullDataViewItem
        elif isinstance(node, Song):
            for g in self.data:
                if g.name == node.genre:
                    return self.ObjectToItem(g)
    def GetValue(self, item, col):
        # Fetch the data object for this item.
        node = self.ItemToObject(item)
        if isinstance(node, Genre):
            mapper = { 0 : node.name,
                       1 : "",
                       2 : "",
                       3 : "",
                       4 : "", #wx.DateTime.FromTimeT(0),  # TODO: There should be some way to indicate a null value...
                       5 : "",
                       6 : "",
                       7 : "",
                       8 : "",
                       }
            return mapper[col]

        elif isinstance(node, Song):
            mapper = { 0 : node.genre,
                       1 : node.id,
                       2 : node.artist,
                       3 : node.title,
                       4 : node.text,
                       5 : node.width,
                       6 : node.double_color,
                       7 : node.date,
                       8 : node.like
                       }
            return mapper[col]
        else:
            raise RuntimeError("unknown node type")
    def GetAttr(self, item, col, attr):
        ##self.log.write('GetAttr')
        node = self.ItemToObject(item)
        if isinstance(node, Genre):
            attr.SetColour('blue')
            attr.SetBold(True)
            return True
        return False
    def SetValue(self, value, item, col):
        node = self.ItemToObject(item)
        if isinstance(node, Song):
            # if col == 1:
            #     node.genre = value
            if col == 1:
                node.id = value
            elif col == 2:
                node.artist = value
            elif col == 3:
                node.title = value
            elif col == 4:
                node.text = value
            elif col == 5:
                node.width = value
            elif col == 6:
                node.double_color = value
            elif col == 7:
                node.date = value
            elif col == 8:
                node.like = value
        return True
#----------------------------------------------------------------------
class Order_Details_Panel(wx.Panel):
    def __init__(self, parent, log,data=None, model=None):
        self.log = log
        self.modelshow=model
        wx.Panel.__init__(self, parent, -1)
        self.dvc = dv.DataViewCtrl(self,
                                   style=wx.BORDER_THEME
                                         | dv.DV_ROW_LINES  # nice alternating bg colors
                                         # | dv.DV_HORIZ_RULES
                                         | dv.DV_VERT_RULES
                                         | dv.DV_MULTIPLE
                                   )
        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.Sizer.Add(self.dvc, 1, wx.EXPAND)
        # Define the columns that we want in the view.  Notice the
        # parameter which tells the view which column in the data model to pull
        # values from for each view column.
        if 1:
            # here is an example of adding a column with full control over the renderer, etc.
            tr = dv.DataViewTextRenderer()
            c0 = dv.DataViewColumn("组件号",   # title
                                   tr,        # renderer
                                   0,         # data model column
                                   width=150 )#
            self.dvc.AppendColumn(c0)
        else:
            # otherwise there are convenience methods for the simple cases
            self.dvc.AppendTextColumn("组件号",   0, width=100)#

        c1 = self.dvc.AppendTextColumn("部件号",1, mode=dv.DATAVIEW_CELL_EDITABLE, width=120)#
        c2 = self.dvc.AppendTextColumn("门型",  2, mode=dv.DATAVIEW_CELL_EDITABLE, width=120)#
        c3 = self.dvc.AppendTextColumn("颜色",  3, mode=dv.DATAVIEW_CELL_EDITABLE, width=70)#
        c4 = self.dvc.AppendTextColumn('高度',  4, mode=dv.DATAVIEW_CELL_ACTIVATABLE, width=60)#
        c5 = self.dvc.AppendTextColumn("宽度",  5, mode=dv.DATAVIEW_CELL_EDITABLE, width=60)  #
        c6 = self.dvc.AppendTextColumn('套色',  6, mode=dv.DATAVIEW_CELL_ACTIVATABLE, width=80)#
        c7 = self.dvc.AppendTextColumn('仿古',  7, mode=dv.DATAVIEW_CELL_ACTIVATABLE, width=80)#
        c8 = self.dvc.AppendTextColumn('边形',  8, mode=dv.DATAVIEW_CELL_ACTIVATABLE, width=70)#

        # Notice how we pull the data from col 3, but this is the 6th column
        # added to the DVC. The order of the view columns is not dependent on
        # the order of the model columns at all.

        c1.Alignment = wx.ALIGN_CENTER
        c2.Alignment = wx.ALIGN_CENTER
        c3.Alignment = wx.ALIGN_CENTER
        c4.Alignment = wx.ALIGN_CENTER
        c5.Alignment = wx.ALIGN_CENTER
        c6.Alignment = wx.ALIGN_CENTER
        c7.Alignment = wx.ALIGN_CENTER
        c8.Alignment = wx.ALIGN_CENTER
        # Set some additional attributes for all the columns
        for c in self.dvc.Columns:
            c.Sortable = True
            c.Reorderable = True

    def DrawMusicData(self,order_id):
        music_data={}
        # Create a dataview control
        if Is_Database_Connect():
            cursor=DB.cursor()
            cursor.execute("select `Sec_id` from `order_part_online` where `Order_id`='%s'" %(order_id))
            record=cursor.fetchall()
            sec_id_list = flatten(record)  # 将二维列表转换成一维列表
            sec_id=list(set(sec_id_list))#去重
            changedata = []
            if record !=():
                for row in range(len(sec_id)):
                    cursor = DB.cursor()
                    cursor.execute("select `Sec_id`,`Part_id`,`Door_type`,`Door_color`,`Door_height`,`Door_width`,`Double_color`,`Archaize`,`Edge_type` from `order_part_online` where `Sec_id`='%s'" % (sec_id[row]))
                    part_record = cursor.fetchall()
                    for i in range(len(part_record)):
                        if part_record[i][3]==None:
                            door_color=''
                        else:
                            door_color =part_record[i][3]
                        if part_record[i][6]==None:
                            double_color=''
                        else:
                            double_color =part_record[i][6]
                        if part_record[i][7]==None:
                            archaize=''
                        else:
                            archaize =part_record[i][7]
                        if part_record[i][8]==None:
                            edge_type=''
                        else:
                            edge_type =part_record[i][8]
                        inform=[part_record[i][0],part_record[i][1],part_record[i][2],door_color,part_record[i][4],part_record[i][5],double_color,archaize,edge_type]
                        changedata.append(inform)
                # music_data.clear()# 清空字典
                for row in range(len(changedata)):
                    music_data[row+1] = changedata[row]
        else:
            return
        musicdata = sorted(music_data.items())
        data = dict()
        for key, val in musicdata:
            # for key in musicdata:
            song = Song( val[0], val[1], val[2], val[3], val[4], val[5], val[6], val[7], val[8])
            genre = data.get(song.genre)
            if genre is None:
                genre = Genre(song.genre)
                data[song.genre] = genre
            genre.songs.append(song)
        data = data.values()
        # Create an instance of our model...
        if self.modelshow is None:
            self.model = MyTreeListModel(data, self.log)
        else:
            self.model = self.modelshow

        # Tell the DVC to use the model
        self.dvc.AssociateModel(self.model)
class PVC_Storage_Ctrl_Panel(wx.Panel):
    def __init__(self, parent, log):
        wx.Panel.__init__(self, parent, -1)
        self.log = log
        winids = []
       # A window to the left of the client window
        leftwin1 =  wx.adv.SashLayoutWindow(
                self, -1, wx.DefaultPosition, (200, 30),
                wx.NO_BORDER|wx.adv.SW_3D
                )
        leftwin1.SetDefaultSize((800, 1000))
        leftwin1.SetOrientation(wx.adv.LAYOUT_VERTICAL)
        leftwin1.SetAlignment(wx.adv.LAYOUT_LEFT)
        # leftwin1.SetBackgroundColour(wx.Colour(0, 255, 0))
        leftwin1.SetSashVisible(wx.adv.SASH_RIGHT, True)
        leftwin1.SetExtraBorderSize(10)

        self.leftWindow1 = leftwin1
        winids.append(leftwin1.GetId())
        self.Bind(
            wx.adv.EVT_SASH_DRAGGED_RANGE, self.OnSashDrag,
            id=min(winids), id2=max(winids)
            )
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.textWindow = wx.TextCtrl(
            leftwin1, -1, "", wx.DefaultPosition, wx.DefaultSize,
            style=wx.SUNKEN_BORDER
        )
        self.Bind(wx.EVT_TEXT, self.EvtText, self.textWindow)
        self.remainingSpace = wx.TextCtrl(
            self, -1, "1234", wx.DefaultPosition, wx.DefaultSize,
            style=wx.SUNKEN_BORDER
        )

    def EvtText(self,eve):
        self.text=self.textWindow.GetValue()
        self.remainingSpace.SetValue(self.text)
    def OnSashDrag(self, event):
        if event.GetDragStatus() == wx.adv.SASH_STATUS_OUT_OF_RANGE:
            # self.log.write('drag is out of range')
            return
        eobj = event.GetEventObject()
        # if eobj is self.topWindow:
        #     # self.log.write('topwin received drag event')
        #     self.topWindow.SetDefaultSize((1000, event.GetDragRect().height))
        #
        if eobj is self.leftWindow1:
            # self.log.write('leftwin1 received drag event')
            self.leftWindow1.SetDefaultSize((event.GetDragRect().width, 1000))
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.remainingSpace)
        self.remainingSpace.Refresh()
    def OnSize(self, event):
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.remainingSpace)
class Product_Storage_Ctrl_Left_Panel(wx.Panel):
    def __init__(self,parent,log,details_inform):
        wx.Panel.__init__(self, parent, -1,style=wx.BK_DEFAULT|wx.SUNKEN_BORDER)
        self.log=log
        self.product_storage_profile_grid=Product_Storage_Profile_Grid(self,self.log,details_inform)
        label1 = wx.StaticText(self, -1, "被占用场地总数")
        label2 = wx.StaticText(self, -1, "入库中场地总数")
        label3 = wx.StaticText(self, -1, "已入库场地总数")
        label4 = wx.StaticText(self, -1, "出库中场地总数")
        label5 = wx.StaticText(self, -1, "已出库场地总数")

        self.occupied_place_sum = wx.TextCtrl(self, wx.ID_ANY, size=(60, 20), style=wx.TE_READONLY)
        self.storaging_place_sum = wx.TextCtrl(self, wx.ID_ANY, size=(60, 20), style=wx.TE_READONLY)
        self.storaged_place_sum = wx.TextCtrl(self, wx.ID_ANY, size=(60, 20), style=wx.TE_READONLY)
        self.being_out_of_libaray_sum = wx.TextCtrl(self, wx.ID_ANY, size=(60, 20), style=wx.TE_READONLY)
        self.complate_out_of_libaray_sum = wx.TextCtrl(self, wx.ID_ANY, size=(60, 20), style=wx.TE_READONLY)
        xbox1 = wx.BoxSizer()
        xbox1.Add(label1, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox1.Add(self.occupied_place_sum, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox2 = wx.BoxSizer()
        xbox2.Add(label2, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox2.Add(self.storaging_place_sum, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox3 = wx.BoxSizer()
        xbox3.Add(label3, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox3.Add(self.storaged_place_sum, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox4 = wx.BoxSizer()
        xbox4.Add(label4, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox4.Add(self.being_out_of_libaray_sum, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox5 = wx.BoxSizer()
        xbox5.Add(label5, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox5.Add(self.complate_out_of_libaray_sum, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        staticbox_query = wx.StaticBox(self, -1)
        staticboxsizer_query1 = wx.StaticBoxSizer(staticbox_query, wx.HORIZONTAL)
        staticboxsizer_query1.Add(xbox1, proportion=1, flag=wx.EXPAND, border=3)
        staticboxsizer_query1.Add(xbox2, proportion=1, flag=wx.EXPAND, border=3)
        staticboxsizer_query1.Add(xbox3, proportion=1, flag=wx.EXPAND, border=3)
        staticboxsizer_query1.Add(xbox4, proportion=1, flag=wx.EXPAND, border=3)
        staticboxsizer_query1.Add(xbox5, proportion=1, flag=wx.EXPAND, border=3)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(staticboxsizer_query1, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        vbox.Add(self.product_storage_profile_grid, proportion=1, flag=wx.EXPAND | wx.ALL, border=3)
        self.SetSizer(vbox)
        self.occupied_place_sum.SetValue(str(self.product_storage_profile_grid.occupied_place))
        self.storaging_place_sum.SetValue(str(self.product_storage_profile_grid.storaging_place))
        self.storaged_place_sum.SetValue(str(self.product_storage_profile_grid.storaged_place))
        self.being_out_of_libaray_sum.SetValue(str(self.product_storage_profile_grid.being_out_of_libaray))
        self.complate_out_of_libaray_sum.SetValue(str(self.product_storage_profile_grid.complate_out_of_libaray))
        # self.timer= wx.PyTimer(self.Refresh)
        # self.timer.Start(5000)
    def Refresh(self):
        try:
            self.occupied_place_sum.SetValue(str(self.product_storage_profile_grid.occupied_place))
            self.storaging_place_sum.SetValue(str(self.product_storage_profile_grid.storaging_place))
            self.storaged_place_sum.SetValue(str(self.product_storage_profile_grid.storaged_place))
            self.being_out_of_libaray_sum.SetValue(str(self.product_storage_profile_grid.being_out_of_libaray))
            self.complate_out_of_libaray_sum.SetValue(str(self.product_storage_profile_grid.complate_out_of_libaray))
            self.product_storage_profile_grid.Refresh()
        except:
            self.log.WriteText('天外天系统正在运行ZX_Pane.py,Product_Storage_Ctrl_Left_Panel类Refresh方法出现错误，请检查\r\n')
class Product_Storage_Profile_Grid(gridlib.Grid): ##, mixins.GridAutoEditMixin):
    def __init__(self, parent, log,details_inform):
        gridlib.Grid.__init__(self, parent, -1)
        ##mixins.GridAutoEditMixin.__init__(self)
        self.log = log
        self.moveTo = None
        self.CreateGrid(17, 9)#, gridlib.Grid.SelectRows)
        self.EnableEditing(False)
        self.SetColLabelAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)
        self.SetDefaultColSize(118)
        self.SetDefaultRowSize(28)
        self.SetColSize(1,60)
        self.SetColSize(4,60)
        self.SetColSize(7,60)
        collablevalue=["第六列","", "第五列", "第四列", "", "第三列", "第二列", "", "第一列"]
        rowlablevalue=["第一行","第二行","第三行","第四行","第五行","第六行","第七行","第八行","第九行","第十行","第十一行",
                       "第十二行", "第十三行", "第十四行", "第十五行", "第十六行", "第十七行"]
        # simple cell formatting
        self.SetCellSize(0, 1, 17, 1)
        self.SetCellSize(0, 4, 17, 1)
        self.SetCellSize(0, 7, 17, 1)
        self.SetCellSize(0, 8, 2, 1)
        self.SetCellSize(2, 8, 2, 1)
        self.SetCellSize(4, 8, 2, 1)
        self.SetCellSize(6, 8, 2, 1)
        self.SetCellSize(8, 8, 2, 1)
        self.SetCellSize(10, 8, 2, 1)
        attr = gridlib.GridCellAttr()
        attr.SetTextColour(wx.BLACK)
        # attr.SetBackgroundColour(wx.BLACK)
        attr.SetFont(wx.Font(30, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.SetColAttr(1, attr)
        self.SetCellValue(0, 1, "过\r\n\r\n\r\n道")
        self.SetColAttr(4, attr)
        self.SetCellValue(0, 4, "过\r\n\r\n\r\n道")
        self.SetColAttr(7, attr)
        self.SetCellValue(0, 7, "过\r\n\r\n\r\n道")
        for i in range(17):
            self.SetRowLabelValue(i, rowlablevalue[i])
        for i in range(9):
            self.SetColLabelValue(i, collablevalue[i])
        for i in range(17):
            for j in range(9):
                self.SetCellAlignment(i, j, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)#将单元格文本属性设置为居中
        # self.SetScrollLineY(12)#设置滚条滚动的像素。
        # self.AppendRows(0)#增加0行，目的是为了增加滚动条。
        self.DisableDragColSize()
        self.DisableDragRowSize()
        self.order_id = ''
        self.details_inform = details_inform
        self.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.OnLeftClick)
        self.Refresh()
    def Refresh(self):
        # start_time=datetime.datetime.now()
        self.occupied_place = 0
        self.storaging_place = 0
        self.storaged_place = 0
        self.being_out_of_libaray = 0
        self.complate_out_of_libaray = 0
        try:
            if Is_Database_Connect():
                cursor = DB.cursor()
                cursor.execute(
                    "select `Index`,`Now_package_num`,`Total_package_num`,`Order_id`,`State` from `place_delivery_place` where 1 ORDER BY `Index` ")
                record = cursor.fetchall()
                for i in range(BIG_PLACE_NUM):  # 1-5号大场地
                    if record[i][4] == STORAGING:
                        self.occupied_place += 1
                        self.storaging_place += 1
                        self.SetCellValue((2 * i), 8, str(record[i][3]) + " " + str(record[i][1]) + "/" + str(record[i][2]))
                        self.SetCellBackgroundColour((2 * i), 8, wx.YELLOW)
                    elif record[i][4] == COMPLETED_STORAGE:
                        cursor.execute("select `State`, `Contract_id` from `order_order_online` where `Order_id`='%s'" % record[i][3])
                        state_record = cursor.fetchone()
                        cursor.execute( "select `Payment_method` from `order_contract_internal` where `Contract_id`='%s'" %state_record[1])
                        payment_state = cursor.fetchone()
                        self.storaged_place += 1
                        if payment_state[0] == 10 or payment_state[0] == 5:
                            if state_record[0] == 126:
                                self.occupied_place += 1
                                self.SetCellValue((2 * i), 8,str(record[i][3]) + " " + str(record[i][1]) + "/" + str(record[i][2]))
                                self.SetCellBackgroundColour((2 * i), 8, wx.CYAN)
                            elif state_record[0] == BEING_OUT_OF_LIBRARY:
                                self.occupied_place += 1
                                self.being_out_of_libaray += 1
                                self.SetCellValue((2 * i), 8,str(record[i][3]) + " " + str(record[i][1]) + "/" + str(record[i][2]))
                                self.SetCellBackgroundColour((2 * i), 8, wx.BLUE)
                            elif state_record[0] == OUT_OF_LIBRARY:
                                self.occupied_place += 1
                                self.complate_out_of_libaray += 1
                                self.SetCellValue((2 * i), 8, '')
                                self.SetCellBackgroundColour((2 * i), 8, wx.LIGHT_GREY)
                            else:
                                self.occupied_place += 1
                                # self.storaged_place += 1
                                self.SetCellValue((2 * i), 8,str(record[i][3]) + " " + str(record[i][1]) + "/" + str(record[i][2]))
                                self.SetCellBackgroundColour((2 * i), 8, wx.GREEN)
                        else:
                            self.SetCellValue((2 * i), 8,
                                              str(record[i][3]) + " " + str(record[i][1]) + "/" + str(record[i][2]))
                            self.SetCellBackgroundColour((2 * i), 8,(186,85,211))
                    else:
                        self.SetCellValue((2 * i), 8, '')
                        self.SetCellBackgroundColour((2 * i), 8, wx.WHITE)
                for i in range(BIG_PLACE_NUM, FIRST_COL_PLACE_NUM):  # 6-10号小场地
                    if record[i][4] == STORAGING:
                        self.occupied_place += 1
                        self.storaging_place += 1
                        self.SetCellValue((i + BIG_PLACE_NUM), 8, str(record[i][3]) + " " + str(record[i][1]) + "/" + str(record[i][2]))
                        self.SetCellBackgroundColour((i + BIG_PLACE_NUM), 8, wx.YELLOW)
                    elif record[i][4] == COMPLETED_STORAGE:
                        cursor.execute(
                            "select `State`, `Contract_id` from `order_order_online` where `Order_id`='%s'" % record[i][3])
                        state_record = cursor.fetchone()
                        cursor.execute(
                            "select `Payment_method` from `order_contract_internal` where `Contract_id`='%s'" %
                            state_record[1])
                        payment_state = cursor.fetchone()
                        self.storaged_place += 1
                        if payment_state[0] == 10 or payment_state[0] == 5:
                            if state_record[0] == 126:
                                self.occupied_place += 1
                                # self.storaged_place += 1
                                self.SetCellValue((i + BIG_PLACE_NUM), 8,
                                                  str(record[i][3]) + " " + str(record[i][1]) + "/" + str(record[i][2]))
                                self.SetCellBackgroundColour((i + BIG_PLACE_NUM), 8, wx.CYAN)
                            elif state_record[0] == BEING_OUT_OF_LIBRARY:
                                self.occupied_place += 1
                                self.being_out_of_libaray += 1
                                self.SetCellValue((i + BIG_PLACE_NUM), 8,
                                                  str(record[i][3]) + " " + str(record[i][1]) + "/" + str(record[i][2]))
                                self.SetCellBackgroundColour((i + BIG_PLACE_NUM), 8, wx.BLUE)
                            elif state_record[0] == OUT_OF_LIBRARY:
                                self.occupied_place += 1
                                self.complate_out_of_libaray += 1
                                self.SetCellValue((i + BIG_PLACE_NUM), 8, '')
                                self.SetCellBackgroundColour((i + BIG_PLACE_NUM), 8, wx.LIGHT_GREY)
                            else:
                                self.occupied_place += 1
                                # self.storaged_place += 1
                                self.SetCellValue((i + BIG_PLACE_NUM), 8,
                                                  str(record[i][3]) + " " + str(record[i][1]) + "/" + str(record[i][2]))
                                self.SetCellBackgroundColour((i + BIG_PLACE_NUM), 8, wx.GREEN)
                        else:
                            self.SetCellValue((i + BIG_PLACE_NUM), 8,str(record[i][3]) + " " + str(record[i][1]) + "/" + str(record[i][2]))
                            self.SetCellBackgroundColour((i + BIG_PLACE_NUM), 8, (186,85,211))
                    else:
                        self.SetCellValue((i + BIG_PLACE_NUM), 8, '')
                        self.SetCellBackgroundColour((i + BIG_PLACE_NUM), 8, wx.WHITE)
                for i in range(FIRST_COL_PLACE_NUM, (FIRST_COL_PLACE_NUM + EVERY_COL_SMALL_PLACE_NUM)):  # 11-28号小场地
                    if record[i][4] == STORAGING:
                        self.occupied_place += 1
                        self.storaging_place += 1
                        self.SetCellValue((i - FIRST_COL_PLACE_NUM), 6,str(record[i][3]) + " " + str(record[i][1]) + "/" + str(record[i][2]))
                        self.SetCellBackgroundColour((i - FIRST_COL_PLACE_NUM), 6, wx.YELLOW)
                    elif record[i][4] == COMPLETED_STORAGE:
                        cursor.execute(
                            "select `State` , `Contract_id` from `order_order_online` where `Order_id`='%s'" % record[i][3])
                        state_record = cursor.fetchone()
                        cursor.execute(
                            "select `Payment_method` from `order_contract_internal` where `Contract_id`='%s'" %
                            state_record[1])
                        payment_state = cursor.fetchone()
                        self.storaged_place += 1
                        if payment_state[0] == 10 or payment_state[0] == 5:
                            if state_record[0] == 126:
                                self.occupied_place += 1
                                # self.storaged_place += 1
                                self.SetCellValue((i - FIRST_COL_PLACE_NUM), 6,str(record[i][3]) + " " + str(record[i][1]) + "/" + str(record[i][2]))
                                self.SetCellBackgroundColour((i - FIRST_COL_PLACE_NUM), 6, wx.CYAN)
                            elif state_record[0] == BEING_OUT_OF_LIBRARY:
                                self.occupied_place += 1
                                self.being_out_of_libaray += 1
                                self.SetCellValue((i - FIRST_COL_PLACE_NUM), 6,str(record[i][3]) + " " + str(record[i][1]) + "/" + str(record[i][2]))
                                self.SetCellBackgroundColour((i - FIRST_COL_PLACE_NUM), 6, wx.BLUE)
                            elif state_record[0] == OUT_OF_LIBRARY:
                                self.occupied_place += 1
                                self.complate_out_of_libaray += 1
                                self.SetCellValue((i - FIRST_COL_PLACE_NUM), 6, '')
                                self.SetCellBackgroundColour((i - FIRST_COL_PLACE_NUM), 6, wx.LIGHT_GREY)
                            else:
                                self.occupied_place += 1
                                # self.storaged_place += 1
                                self.SetCellValue((i - FIRST_COL_PLACE_NUM), 6,
                                                  str(record[i][3]) + " " + str(record[i][1]) + "/" + str(record[i][2]))

                                self.SetCellBackgroundColour((i - FIRST_COL_PLACE_NUM), 6, wx.GREEN)
                        else:
                            self.SetCellValue((i - FIRST_COL_PLACE_NUM), 6,
                                              str(record[i][3]) + " " + str(record[i][1]) + "/" + str(record[i][2]))
                            self.SetCellBackgroundColour((i - FIRST_COL_PLACE_NUM), 6, (186,85,211))
                    else:
                        self.SetCellValue((i - FIRST_COL_PLACE_NUM), 6, " ")
                        self.SetCellBackgroundColour((i - FIRST_COL_PLACE_NUM), 6, wx.WHITE)
                for i in range((FIRST_COL_PLACE_NUM + EVERY_COL_SMALL_PLACE_NUM), (FIRST_COL_PLACE_NUM + 2*EVERY_COL_SMALL_PLACE_NUM)):  # 28-44号小场地
                    if record[i][4] == STORAGING:
                        self.occupied_place += 1
                        self.storaging_place += 1
                        self.SetCellValue((i - (FIRST_COL_PLACE_NUM + EVERY_COL_SMALL_PLACE_NUM)), 5,
                                          str(record[i][3]) + " " + str(record[i][1]) + "/" + str(record[i][2]))
                        self.SetCellBackgroundColour((i - (FIRST_COL_PLACE_NUM + EVERY_COL_SMALL_PLACE_NUM)), 5, wx.YELLOW)
                    elif record[i][4] == COMPLETED_STORAGE:
                        cursor.execute(
                            "select `State`, `Contract_id` from `order_order_online` where `Order_id`='%s'" % record[i][3])
                        state_record = cursor.fetchone()
                        cursor.execute(
                            "select `Payment_method` from `order_contract_internal` where `Contract_id`='%s'" %
                            state_record[1])
                        payment_state = cursor.fetchone()
                        self.storaged_place += 1
                        if payment_state[0] == 10 or payment_state[0] == 5:
                            if state_record[0] == 126:
                                self.occupied_place += 1
                                # self.storaged_place += 1
                                self.SetCellValue((i - (FIRST_COL_PLACE_NUM + EVERY_COL_SMALL_PLACE_NUM)), 5,
                                                  str(record[i][3]) + " " + str(record[i][1]) + "/" + str(record[i][2]))
                                self.SetCellBackgroundColour((i - (FIRST_COL_PLACE_NUM + EVERY_COL_SMALL_PLACE_NUM)), 5, wx.CYAN)
                            elif state_record[0] == BEING_OUT_OF_LIBRARY:
                                self.occupied_place += 1
                                self.being_out_of_libaray += 1
                                self.SetCellValue((i - (FIRST_COL_PLACE_NUM + EVERY_COL_SMALL_PLACE_NUM)), 5,
                                                  str(record[i][3]) + " " + str(record[i][1]) + "/" + str(record[i][2]))
                                self.SetCellBackgroundColour((i - (FIRST_COL_PLACE_NUM + EVERY_COL_SMALL_PLACE_NUM)), 5, wx.BLUE)
                            elif state_record[0] == OUT_OF_LIBRARY:
                                self.occupied_place += 1
                                self.complate_out_of_libaray += 1
                                self.SetCellValue((i - (FIRST_COL_PLACE_NUM + EVERY_COL_SMALL_PLACE_NUM)), 5, '')
                                self.SetCellBackgroundColour((i - (FIRST_COL_PLACE_NUM + EVERY_COL_SMALL_PLACE_NUM)), 5, wx.LIGHT_GREY)
                            else:
                                self.occupied_place += 1
                                # self.storaged_place += 1
                                self.SetCellValue((i - (FIRST_COL_PLACE_NUM + EVERY_COL_SMALL_PLACE_NUM)), 5,
                                                  str(record[i][3]) + " " + str(record[i][1]) + "/" + str(record[i][2]))
                                self.SetCellBackgroundColour((i - (FIRST_COL_PLACE_NUM + EVERY_COL_SMALL_PLACE_NUM)), 5, wx.GREEN)
                        else:
                            self.SetCellValue((i - (FIRST_COL_PLACE_NUM + EVERY_COL_SMALL_PLACE_NUM)), 5,
                                              str(record[i][3]) + " " + str(record[i][1]) + "/" + str(record[i][2]))
                            self.SetCellBackgroundColour((i - (FIRST_COL_PLACE_NUM + EVERY_COL_SMALL_PLACE_NUM)), 5, (186,85,211))

                    else:
                        self.SetCellValue((i - (FIRST_COL_PLACE_NUM + EVERY_COL_SMALL_PLACE_NUM)), 5, " ")
                        self.SetCellBackgroundColour((i - (FIRST_COL_PLACE_NUM + EVERY_COL_SMALL_PLACE_NUM)), 5, wx.WHITE)
                for i in range((FIRST_COL_PLACE_NUM + 2*EVERY_COL_SMALL_PLACE_NUM), (FIRST_COL_PLACE_NUM + 3*EVERY_COL_SMALL_PLACE_NUM)):  # 46-62号小场地
                    if record[i][4] == STORAGING:
                        self.occupied_place += 1
                        self.storaging_place += 1
                        self.SetCellValue((i - (FIRST_COL_PLACE_NUM + 2*EVERY_COL_SMALL_PLACE_NUM)), 3,
                                          str(record[i][3]) + " " + str(record[i][1]) + "/" + str(record[i][2]))
                        self.SetCellBackgroundColour((i - (FIRST_COL_PLACE_NUM + 2*EVERY_COL_SMALL_PLACE_NUM)), 3, wx.YELLOW)
                    elif record[i][4] == COMPLETED_STORAGE:
                        cursor.execute(
                            "select `State`,`Contract_id` from `order_order_online` where `Order_id`='%s'" % record[i][3])
                        state_record = cursor.fetchone()
                        cursor.execute(
                            "select `Payment_method` from `order_contract_internal` where `Contract_id`='%s'" % state_record[1])
                        payment_state = cursor.fetchone()
                        self.storaged_place += 1
                        if payment_state[0]==10 or payment_state[0]==5:
                            if state_record[0] == 126:
                                self.occupied_place += 1
                                # self.storaged_place += 1
                                self.SetCellValue((i - (FIRST_COL_PLACE_NUM + 2*EVERY_COL_SMALL_PLACE_NUM)), 3,
                                                  str(record[i][3]) + " " + str(record[i][1]) + "/" + str(record[i][2]))
                                self.SetCellBackgroundColour((i - (FIRST_COL_PLACE_NUM + 2*EVERY_COL_SMALL_PLACE_NUM)), 3, wx.CYAN)
                            elif state_record[0] == BEING_OUT_OF_LIBRARY:
                                self.occupied_place += 1
                                self.being_out_of_libaray += 1
                                self.SetCellValue((i - (FIRST_COL_PLACE_NUM + 2*EVERY_COL_SMALL_PLACE_NUM)), 3,
                                                  str(record[i][3]) + " " + str(record[i][1]) + "/" + str(record[i][2]))
                                self.SetCellBackgroundColour((i - (FIRST_COL_PLACE_NUM + 2*EVERY_COL_SMALL_PLACE_NUM)), 3, wx.BLUE)
                            elif state_record[0] == OUT_OF_LIBRARY:
                                self.occupied_place += 1
                                self.complate_out_of_libaray += 1
                                self.SetCellValue((i - (FIRST_COL_PLACE_NUM + 2*EVERY_COL_SMALL_PLACE_NUM)), 3, '')
                                self.SetCellBackgroundColour((i - (FIRST_COL_PLACE_NUM + 2*EVERY_COL_SMALL_PLACE_NUM)), 3, wx.LIGHT_GREY)
                            else:
                                self.occupied_place += 1
                                # self.storaged_place += 1
                                self.SetCellValue((i - (FIRST_COL_PLACE_NUM + 2*EVERY_COL_SMALL_PLACE_NUM)), 3,
                                                  str(record[i][3]) + " " + str(record[i][1]) + "/" + str(record[i][2]))

                                self.SetCellBackgroundColour((i - (FIRST_COL_PLACE_NUM + 2*EVERY_COL_SMALL_PLACE_NUM)), 3, wx.GREEN)
                        else:
                            self.SetCellValue((i - (FIRST_COL_PLACE_NUM + 2 * EVERY_COL_SMALL_PLACE_NUM)), 3,
                                              str(record[i][3]) + " " + str(record[i][1]) + "/" + str(record[i][2]))
                            self.SetCellBackgroundColour((i - (FIRST_COL_PLACE_NUM + 2 * EVERY_COL_SMALL_PLACE_NUM)), 3,(186,85,211))
                    else:
                        self.SetCellValue((i - (FIRST_COL_PLACE_NUM + 2*EVERY_COL_SMALL_PLACE_NUM)), 3, '')
                        self.SetCellBackgroundColour((i - (FIRST_COL_PLACE_NUM + 2*EVERY_COL_SMALL_PLACE_NUM)), 3, wx.WHITE)
                for i in range((FIRST_COL_PLACE_NUM + 3*EVERY_COL_SMALL_PLACE_NUM), (FIRST_COL_PLACE_NUM + 4*EVERY_COL_SMALL_PLACE_NUM)):  # 63-79号小场地
                    if record[i][4] == STORAGING:
                        self.occupied_place += 1
                        self.storaging_place += 1
                        self.SetCellValue((i - (FIRST_COL_PLACE_NUM + 3*EVERY_COL_SMALL_PLACE_NUM)), 2,
                                          str(record[i][3]) + " " + str(record[i][1]) + "/" + str(record[i][2]))
                        self.SetCellBackgroundColour((i - (FIRST_COL_PLACE_NUM + 3*EVERY_COL_SMALL_PLACE_NUM)), 2, wx.YELLOW)
                    elif record[i][4] == COMPLETED_STORAGE:
                        cursor.execute(
                            "select `State`, `Contract_id` from `order_order_online` where `Order_id`='%s'" % record[i][3])
                        state_record = cursor.fetchone()
                        cursor.execute(
                            "select `Payment_method` from `order_contract_internal` where `Contract_id`='%s'" %
                            state_record[1])
                        payment_state = cursor.fetchone()
                        self.storaged_place += 1
                        if payment_state[0] == 10 or payment_state[0] == 5:
                            if state_record[0] == 126:
                                self.occupied_place += 1
                                # self.storaged_place += 1
                                self.SetCellValue((i - (FIRST_COL_PLACE_NUM + 3*EVERY_COL_SMALL_PLACE_NUM)), 2,
                                                  str(record[i][3]) + " " + str(record[i][1]) + "/" + str(record[i][2]))
                                self.SetCellBackgroundColour((i - (FIRST_COL_PLACE_NUM + 3*EVERY_COL_SMALL_PLACE_NUM)), 2, wx.CYAN)
                            elif state_record[0] == BEING_OUT_OF_LIBRARY:
                                self.occupied_place += 1
                                self.being_out_of_libaray += 1
                                self.SetCellValue((i - (FIRST_COL_PLACE_NUM + 3*EVERY_COL_SMALL_PLACE_NUM)), 2,
                                                  str(record[i][3]) + " " + str(record[i][1]) + "/" + str(record[i][2]))
                                self.SetCellBackgroundColoucr((i - (FIRST_COL_PLACE_NUM + 3*EVERY_COL_SMALL_PLACE_NUM)), 2, wx.BLUE)
                            elif state_record[0] == OUT_OF_LIBRARY:
                                self.occupied_place += 1
                                self.complate_out_of_libaray += 1
                                self.SetCellValue((i - (FIRST_COL_PLACE_NUM + 3*EVERY_COL_SMALL_PLACE_NUM)), 2, '')
                                self.SetCellBackgroundColour((i - (FIRST_COL_PLACE_NUM + 3*EVERY_COL_SMALL_PLACE_NUM)), 2, wx.LIGHT_GREY)
                            else:
                                self.occupied_place += 1
                                # self.storaged_place += 1
                                self.SetCellValue((i - (FIRST_COL_PLACE_NUM + 3*EVERY_COL_SMALL_PLACE_NUM)), 2,
                                                  str(record[i][3]) + " " + str(record[i][1]) + "/" + str(record[i][2]))
                                self.SetCellBackgroundColour((i - (FIRST_COL_PLACE_NUM + 3*EVERY_COL_SMALL_PLACE_NUM)), 2, wx.GREEN)
                        else:
                            self.SetCellValue((i - (FIRST_COL_PLACE_NUM + 3 * EVERY_COL_SMALL_PLACE_NUM)), 2,
                                              str(record[i][3]) + " " + str(record[i][1]) + "/" + str(record[i][2]))
                            self.SetCellBackgroundColour((i - (FIRST_COL_PLACE_NUM + 3 * EVERY_COL_SMALL_PLACE_NUM)), 2, (186,85,211))

                    else:
                        self.SetCellValue((i - (FIRST_COL_PLACE_NUM + 3*EVERY_COL_SMALL_PLACE_NUM)), 2, '')
                        self.SetCellBackgroundColour((i - (FIRST_COL_PLACE_NUM + 3*EVERY_COL_SMALL_PLACE_NUM)), 2, wx.WHITE)
                for i in range((FIRST_COL_PLACE_NUM + 4*EVERY_COL_SMALL_PLACE_NUM), (FIRST_COL_PLACE_NUM + 5*EVERY_COL_SMALL_PLACE_NUM)):  # 79-96号小场地
                    if record[i][4] == STORAGING:
                        self.occupied_place += 1
                        self.storaging_place += 1
                        self.SetCellValue((i - (FIRST_COL_PLACE_NUM + 4*EVERY_COL_SMALL_PLACE_NUM)), 0,
                                          str(record[i][3]) + " " + str(record[i][1]) + "/" + str(record[i][2]))
                        self.SetCellBackgroundColour((i - (FIRST_COL_PLACE_NUM + 4*EVERY_COL_SMALL_PLACE_NUM)), 0, wx.YELLOW)
                    elif record[i][4] == COMPLETED_STORAGE:
                        cursor.execute("select `State` , `Contract_id` from `order_order_online` where `Order_id`='%s'" % record[i][3])
                        state_record = cursor.fetchone()
                        cursor.execute(
                            "select `Payment_method` from `order_contract_internal` where `Contract_id`='%s'" %
                            state_record[1])
                        payment_state = cursor.fetchone()
                        self.storaged_place += 1
                        if payment_state[0] == 10 or payment_state[0] == 5:
                            if state_record[0] == 126:
                                self.occupied_place += 1
                                # self.storaged_place += 1
                                self.SetCellValue((i - (FIRST_COL_PLACE_NUM + 4*EVERY_COL_SMALL_PLACE_NUM)), 0,str(record[i][3]) + " " + str(record[i][1]) + "/" + str(record[i][2]))
                                self.SetCellBackgroundColour((i - (FIRST_COL_PLACE_NUM + 4*EVERY_COL_SMALL_PLACE_NUM)), 0, wx.CYAN)
                            elif state_record[0] == BEING_OUT_OF_LIBRARY:
                                self.occupied_place += 1
                                self.being_out_of_libaray += 1
                                self.SetCellValue((i - (FIRST_COL_PLACE_NUM + 4*EVERY_COL_SMALL_PLACE_NUM)), 0,str(record[i][3]) + " " + str(record[i][1]) + "/" + str(record[i][2]))
                                self.SetCellBackgroundColour((i - (FIRST_COL_PLACE_NUM + 4*EVERY_COL_SMALL_PLACE_NUM)), 0, wx.BLUE)
                            elif state_record[0] == OUT_OF_LIBRARY:
                                self.occupied_place += 1
                                self.complate_out_of_libaray += 1
                                self.SetCellValue((i - (FIRST_COL_PLACE_NUM + 4*EVERY_COL_SMALL_PLACE_NUM)), 0, '')
                                self.SetCellBackgroundColour((i - (FIRST_COL_PLACE_NUM + 4*EVERY_COL_SMALL_PLACE_NUM)), 0, wx.LIGHT_GREY)
                            else:
                                self.occupied_place += 1
                                # self.storaged_place += 1
                                self.SetCellValue((i - (FIRST_COL_PLACE_NUM + 4*EVERY_COL_SMALL_PLACE_NUM)), 0,str(record[i][3]) + " " + str(record[i][1]) + "/" + str(record[i][2]))
                                self.SetCellBackgroundColour((i - (FIRST_COL_PLACE_NUM + 4*EVERY_COL_SMALL_PLACE_NUM)), 0, wx.GREEN)
                        else:
                            self.SetCellValue((i - (FIRST_COL_PLACE_NUM + 4 * EVERY_COL_SMALL_PLACE_NUM)), 0,
                                              str(record[i][3]) + " " + str(record[i][1]) + "/" + str(record[i][2]))
                            self.SetCellBackgroundColour((i - (FIRST_COL_PLACE_NUM + 4 * EVERY_COL_SMALL_PLACE_NUM)), 0, (186,85,211))

                    else:
                        self.SetCellValue((i - (FIRST_COL_PLACE_NUM + 4*EVERY_COL_SMALL_PLACE_NUM)), 0, '')
                        self.SetCellBackgroundColour((i - (FIRST_COL_PLACE_NUM + 4*EVERY_COL_SMALL_PLACE_NUM)), 0, wx.WHITE)
            else:
                self.log.WriteText("天外天系统正在运行ZX_Panel.py  库管理界面刷新函数中无法连接数据库place_delivery_place表单时出现错误\r\n")
                return
        except:
            self.log.WriteText("天外天系统正在运行ZX_Panel.py 库管理界面刷新函数中读取数据库place_delivery_place表单时出错，请检查数据库中场地号是否满足给定条件\r\n")
            return False
        # end_time=datetime.datetime.now()
        # during_time = (end_time - start_time).seconds * 1000 + (end_time - start_time).microseconds / 1000
    def OnLeftClick(self,evt):
        row = evt.GetRow()  # 获得鼠标单击的单元格所在的行
        col = evt.GetCol()
        text = self.GetCellValue(row, col)
        c=text.split(' ')
        self.order_id=c[0]
        self.details_inform.DrawMusicData(self.order_id)
        evt.Skip()
class Product_Storage_Ctrl_Right_Panel(wx.Panel):
    def __init__(self,parent,log):
        wx.Panel.__init__(self, parent, -1,style=wx.BK_DEFAULT|wx.SUNKEN_BORDER)
        self.log=log
        self.Order_Details_Panel=Order_Details_Panel(self,self.log)
        label1 = wx.StaticText(self, -1, "经 销 商 ")
        label2 = wx.StaticText(self, -1, "品     牌 ")
        label3 = wx.StaticText(self, -1, "合 同 号 ")
        label4 = wx.StaticText(self, -1, "快递公司")
        label5 = wx.StaticText(self, -1, "订单面积")
        label6 = wx.StaticText(self, -1, "订单价格")
        label7 = wx.StaticText(self, -1, "下单日期")
        label8 = wx.StaticText(self, -1, "交货日期")
        label9 = wx.StaticText(self, -1, "门板数目")
        label10= wx.StaticText(self, -1, "门板面积")
        self.Dealer = wx.TextCtrl(self, wx.ID_ANY, size=(130, 30), style=wx.TE_READONLY)
        self.brand = wx.TextCtrl(self, wx.ID_ANY, size=(130, 30), style=wx.TE_READONLY)
        self.contract_id = wx.TextCtrl(self, wx.ID_ANY, size=(130, 30), style=wx.TE_READONLY)
        self.transport_company = wx.TextCtrl(self, wx.ID_ANY, size=(130, 30), style=wx.TE_READONLY)
        self.order_area = wx.TextCtrl(self, wx.ID_ANY, size=(130, 30), style=wx.TE_READONLY)
        self.order_price = wx.TextCtrl(self, wx.ID_ANY, size=(130, 30), style=wx.TE_READONLY)
        self.record_date = wx.TextCtrl(self, wx.ID_ANY, size=(130, 30), style=wx.TE_READONLY)
        self.receive_date = wx.TextCtrl(self, wx.ID_ANY, size=(130, 30), style=wx.TE_READONLY)
        self.door_num = wx.TextCtrl(self, wx.ID_ANY, size=(130, 30), style=wx.TE_READONLY)
        self.door_area = wx.TextCtrl(self, wx.ID_ANY, size=(130, 30), style=wx.TE_READONLY)
        xbox1 = wx.BoxSizer()
        xbox1.Add(label1, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox1.Add(self.Dealer, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox2 = wx.BoxSizer()
        xbox2.Add(label2, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox2.Add(self.brand, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox3 = wx.BoxSizer()
        xbox3.Add(label3, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox3.Add(self.contract_id, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox4 = wx.BoxSizer()
        xbox4.Add(label4, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox4.Add(self.transport_company, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox5 = wx.BoxSizer()
        xbox5.Add(label5, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox5.Add(self.order_area, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox6 = wx.BoxSizer()
        xbox6.Add(label6, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox6.Add(self.order_price, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox7 = wx.BoxSizer()
        xbox7.Add(label7, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox7.Add(self.record_date, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox8 = wx.BoxSizer()
        xbox8.Add(label8, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox8.Add(self.receive_date, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox9 = wx.BoxSizer()
        xbox9.Add(label9, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox9.Add(self.door_num, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox10 = wx.BoxSizer()
        xbox10.Add(label10, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox10.Add(self.door_area, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        # staticbox_interface = wx.StaticBox(self, -1)
        # staticboxsizer_interface1 = wx.StaticBoxSizer(staticbox_interface, wx.VERTICAL)
        staticboxsizer_interface1=wx.BoxSizer()#wx.VERTICAL
        staticboxsizer_interface1.Add(xbox1, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        staticboxsizer_interface1.Add(xbox2, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        staticboxsizer_interface1.Add(xbox3, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        staticboxsizer_interface1.Add(xbox4, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        staticboxsizer_interface1.Add(xbox5, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        # staticbox_interface1 = wx.StaticBox(self, -1)
        # staticboxsizer_interface2 = wx.StaticBoxSizer(staticbox_interface1, wx.VERTICAL)
        staticboxsizer_interface2 = wx.BoxSizer()#wx.VERTICAL
        staticboxsizer_interface2.Add(xbox6, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        staticboxsizer_interface2.Add(xbox7, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        staticboxsizer_interface2.Add(xbox8, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        staticboxsizer_interface2.Add(xbox9, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        staticboxsizer_interface2.Add(xbox10, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        staticbox_interface1 = wx.StaticBox(self, -1)
        staticboxsizer_interface3 = wx.StaticBoxSizer(staticbox_interface1, wx.VERTICAL)
        xxbox1 = wx.BoxSizer(wx.VERTICAL)
        staticboxsizer_interface3.Add(staticboxsizer_interface1, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        staticboxsizer_interface3.Add(staticboxsizer_interface2, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xxbox1.Add(staticboxsizer_interface3, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xxbox1.Add(self.Order_Details_Panel, proportion=1, flag=wx.EXPAND | wx.ALL, border=3)
        self.SetSizer(xxbox1)
    def Refresh(self,order_id):
        # self.order_id = str(order_id)
        try:
            if Is_Database_Connect():
                cursor=DB.cursor()
                cursor.execute(
                    "select `Contract_id`,`Receive_time`,`Record_time`,`Transport_company`,`Charge_price`,`Order_area`,`Door_num`,`Door_area`,`Dealer`,`Brand` from `order_order_online` where Order_id='%s' "%order_id)
                record = cursor.fetchone()
                if record is not None:
                    self.Dealer.SetValue(str(record[8]))
                    self.brand.SetValue(str(record[9]))
                    self.contract_id.SetValue(str(record[0]))
                    self.transport_company.SetValue(str(record[3]))
                    self.order_area.SetValue(str(record[5]))
                    self.order_price.SetValue(str(record[4]))
                    self.record_date.SetValue(str(record[2].strftime('%Y-%m-%d')))
                    self.receive_date.SetValue(str(record[1].strftime('%Y-%m-%d')))
                    self.door_num.SetValue(str(record[6]))
                    self.door_area.SetValue(str(record[7]))
                else:
                    self.Dealer.SetValue(' ')
                    self.brand.SetValue(' ')
                    self.contract_id.SetValue(' ')
                    self.transport_company.SetValue(' ')
                    self.order_area.SetValue(' ')
                    self.order_price.SetValue(' ')
                    self.record_date.SetValue(' ')
                    self.receive_date.SetValue(' ')
                    self.door_num.SetValue(' ')
                    self.door_area.SetValue(' ')
            else:
                return
        except:
            self.log.WriteText('天外天系统正在运行ZX_Pane.py  成品库管理Product_Storage_Ctrl_Right_Panel类中刷新方法读取数据库时出现错误，请检查传入参数类型或数据库字段是否完整\r\n')
class Product_Storage_Ctrl_Panel(wx.Panel):
    def __init__(self, parent, log):
        wx.Panel.__init__(self, parent, -1)
        self.log = log
        winids = []
       # A window to the left of the client window
        leftwin1 =  wx.adv.SashLayoutWindow(self, -1, wx.DefaultPosition, (200, 30), wx.NO_BORDER|wx.adv.SW_3D)
        leftwin1.SetDefaultSize((950, 1000))
        leftwin1.SetOrientation(wx.adv.LAYOUT_VERTICAL)
        leftwin1.SetAlignment(wx.adv.LAYOUT_LEFT)
        # leftwin1.SetBackgroundColour(wx.Colour(0, 255, 0))
        leftwin1.SetSashVisible(wx.adv.SASH_RIGHT, True)
        leftwin1.SetExtraBorderSize(2)
        # self.product_storage_profile_panel = Product_Storage_Ctrl_Left_Panel(leftwin1,self.log)
        self.leftWindow1 = leftwin1
        winids.append(leftwin1.GetId())
        self.remainingSpace =Product_Storage_Ctrl_Right_Panel(self, self.log)
        self.Bind(wx.adv.EVT_SASH_DRAGGED_RANGE, self.OnSashDrag,id=min(winids), id2=max(winids))
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.product_storage_profile_panel = Product_Storage_Ctrl_Left_Panel(leftwin1, self.log,self.remainingSpace.Order_Details_Panel)
        wx.adv.LayoutAlgorithm().LayoutWindow(self.leftWindow1,self.product_storage_profile_panel.product_storage_profile_grid)

        #用来重新分配这个控件在父类窗口的显示的位置和大小。wx.adv.LayoutAlgorithm().LayoutWindow（parent,控件）
        self.timer = wx.PyTimer(self.MyRefresh)
        self.timer.Start(5000)
    def MyRefresh(self):
        try:
            self.product_storage_profile_panel.Refresh()
            self.order_id = self.product_storage_profile_panel.product_storage_profile_grid.order_id
            self.remainingSpace.Refresh(self.order_id)
        except:
            self.log.WriteText('天外天系统正在运行Product_Storage_Ctrl_Panel中刷新函数出现错误，请检查\r\n')
    def OnSashDrag(self, event):
        if event.GetDragStatus() == wx.adv.SASH_STATUS_OUT_OF_RANGE:
            return
        eobj = event.GetEventObject()
        if eobj is self.leftWindow1:
            self.leftWindow1.SetDefaultSize((event.GetDragRect().width, 1000))
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.remainingSpace)
    def OnSize(self, event):
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.remainingSpace)
#----------------------------------------------------------pvc工位工单管理界面
class Pvc_Workposition_Managemnet_Panel(wx.Panel):
    def __init__(self, parent,log, id=wx.ID_ANY, title="", pos=wx.DefaultPosition,
                 size=(700,650), style=wx.DEFAULT_FRAME_STYLE):
        wx.Panel.__init__(self, parent)
        self._flags = 0
        self.log=log
        self.order_sum = 0
        self.order_area_sum = 0
        self.package_sum = 0
        # self.SetIcon(GetMondrianIcon())
        # self.SetMenuBar(self.CreateMenuBar())
        self._leftWindow1 = wx.adv.SashLayoutWindow(self, 101, wx.DefaultPosition,
                                                wx.Size(230, 1000), wx.NO_BORDER |
                                                wx.adv.SW_3D | wx.CLIP_CHILDREN)
        self._leftWindow1.SetDefaultSize(wx.Size(250, 1000))
        self._leftWindow1.SetOrientation(wx.adv.LAYOUT_VERTICAL)
        self._leftWindow1.SetAlignment(wx.adv.LAYOUT_LEFT)
        self._leftWindow1.SetSashVisible(wx.adv.SASH_RIGHT, True)
        self._leftWindow1.SetExtraBorderSize(10)
        self._pnl = 0

        self.remainingSpace = Pvc_Workposition_Right_Panel(self,-1,self.log)

        self.ID_WINDOW_TOP = 100
        self.ID_WINDOW_LEFT1 = 101
        self.ID_WINDOW_RIGHT1 = 102
        self.ID_WINDOW_BOTTOM = 103
        self._leftWindow1.Bind(wx.adv.EVT_SASH_DRAGGED_RANGE, self.OnFoldPanelBarDrag,
                               id=100, id2=103)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_SCROLL, self.OnSlideColour)
        self.ReCreateFoldPanel(0)
    def OnSize(self, event):
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.remainingSpace)
        event.Skip()
    def OnQuit(self, event):
        self.Destroy()
    def OnToggleWindow(self, event):

        self._leftWindow1.Show(not self._leftWindow1.IsShown())
        # Leaves bits of itself behind sometimes
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.remainingSpace)
        self.remainingSpace.Refresh()

        event.Skip()
    def OnFoldPanelBarDrag(self, event):

        # if event.GetDragStatus() == wx.SASH_STATUS_OUT_OF_RANGE:
        #     return

        if event.GetId() == self.ID_WINDOW_LEFT1:
            self._leftWindow1.SetDefaultSize(wx.Size(event.GetDragRect().width, 1000))

        # Leaves bits of itself behind sometimes
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.remainingSpace)
        self.remainingSpace.Refresh()

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
        self.cal = CalendarCtrl(item, -1, wx.DateTime().Today(),
                                style=wx.adv.CAL_SEQUENTIAL_MONTH_SELECTION)
        self._pnl.AddFoldPanelWindow(item,self.cal,fpb.FPB_ALIGN_WIDTH,0,0)

        self._pnl.AddFoldPanelSeparator(item)
        btn_today = wx.Button(item, wx.ID_ANY, "今天")
        btn_today.Bind(wx.EVT_BUTTON, self.OnTodayQuery)
        self._pnl.AddFoldPanelWindow(item, btn_today)
        btn_yesterday = wx.Button(item, wx.ID_ANY, "昨天")
        btn_yesterday.Bind(wx.EVT_BUTTON, self.OnYesterdayQuery)
        self._pnl.AddFoldPanelWindow(item, btn_yesterday,spacing=0)
        btn_Byesterday = wx.Button(item, wx.ID_ANY, "前天")
        btn_Byesterday.Bind(wx.EVT_BUTTON, self.OnBYesterdayQuery)
        self._pnl.AddFoldPanelWindow(item, btn_Byesterday,spacing=0)
        btn_All = wx.Button(item, wx.ID_ANY, "大前天")
        btn_All.Bind(wx.EVT_BUTTON, self.OnBBYesterdayQuery)
        self._pnl.AddFoldPanelWindow(item, btn_All,spacing=0)
        self._pnl.AddFoldPanelSeparator(item)
        # btn_date_clear=wx.Button(item, wx.ID_ANY, "清除日期索引")
        # btn_date_clear.Bind(wx.EVT_BUTTON, self.OnExpandMe)
        # self._pnl.AddFoldPanelWindow(item, btn_date_clear)
        item = self._pnl.AddFoldPanel("按发货单状态查询", False, foldIcons=Images)
        # ID_WAIT_DELIVERY = 301
        # ID_DELIVERYING = 302
        # ID_COMPLATE_DELIVERY = 303
        # ID_CANCEL_DELIVERY = 304

        radio1 = wx.RadioButton(item, ID_WAIT_DELIVERY, "&等待发货")
        radio2 = wx.RadioButton(item, ID_DELIVERYING, "&发货中")
        radio3 = wx.RadioButton(item, ID_COMPLATE_DELIVERY, "&已发货")
        radio4 = wx.RadioButton(item, ID_CANCEL_DELIVERY, "&已取消")
        # radio5 = wx.RadioButton(item, self.ID_All_STATE, "&查看全部状态")

        # currStyle.Bind(wx.EVT_RADIOBUTTON, self.OnStateQuery)
        radio1.Bind(wx.EVT_RADIOBUTTON, self.OnStateQuery)
        radio2.Bind(wx.EVT_RADIOBUTTON, self.OnStateQuery)
        radio3.Bind(wx.EVT_RADIOBUTTON, self.OnStateQuery)
        radio4.Bind(wx.EVT_RADIOBUTTON, self.OnStateQuery)
        # radio5.Bind(wx.EVT_RADIOBUTTON, self.OnStateQuery)

        self._pnl.AddFoldPanelWindow(item, radio1, fpb.FPB_ALIGN_WIDTH, fpb.FPB_DEFAULT_SPACING, 10)
        self._pnl.AddFoldPanelWindow(item, radio2, fpb.FPB_ALIGN_WIDTH, fpb.FPB_DEFAULT_SPACING, 10)
        self._pnl.AddFoldPanelWindow(item, radio3, fpb.FPB_ALIGN_WIDTH, fpb.FPB_DEFAULT_SPACING, 10)
        self._pnl.AddFoldPanelWindow(item, radio4, fpb.FPB_ALIGN_WIDTH, fpb.FPB_DEFAULT_SPACING, 10)
        # self._pnl.AddFoldPanelWindow(item, radio5, fpb.FPB_ALIGN_WIDTH, fpb.FPB_DEFAULT_SPACING, 10)
        self._pnl.AddFoldPanelSeparator(item)
        self._single = wx.Button(item,-1, "&查看全部状态")
        self._single.Bind(wx.EVT_BUTTON, self.OnBBYesterdayQuery)
        self._pnl.AddFoldPanelWindow(item, self._single, fpb.FPB_ALIGN_WIDTH,
                                     fpb.FPB_DEFAULT_SPACING, 10)
        self._leftWindow1.SizeWindows()
    def onDateStart(self,evt):
        self.date_start=self.calendar_begin.GetValue()
        self.date_end=self.calendar_end.GetValue()
        if self.date_start=="从:" or self.date_end =="至:":
            self.log.WriteText("请选择查询起始日期！")
        else:
            t1 = self.date_start.split('/')
            t2 = t1[2], t1[1], t1[0]
            st = ''
            start_time = st.join(t2)
            t3 = self.date_end.split('/')
            t4 = t3[2], t3[1], t3[0]
            et = ''
            end_time = et.join(t4)
            self.data = []
            if Is_Database_Connect():
                cursor = DB.cursor()
                cursor.execute(
                    "select `Delivery_ID`,`Order_amount`,`Delivery_total_area`,`Package_amount`,`Creat_date`,`Creator`,`Execute_date`,`Executor`,`Delivery_date`,`Delivery_operator`,`State` from `delivery_form_zx` where 1 ORDER BY `Creat_date` DESC")
                record = cursor.fetchall()
                if record is not None:
                    for i in range(len(record)):
                        datetime1 = record[i][4].strftime('%Y%m%d')
                        if datetime1 >= start_time and datetime1 <= end_time:
                            inform = [record[i][0], record[i][1], record[i][2], record[i][3],record[i][4].strftime('%Y-%m-%d'),
                                      record[i][5], record[i][6], record[i][7], record[i][8],record[i][9],record[i][10]]
                            self.data.append(inform)
                            self.order_sum += int(record[i][1])
                            self.order_area_sum += int(record[i][2])
                            self.package_sum += int(record[i][3])
                        else:
                            pass
                    self.delivery_sum = len(self.data)
                    self.remainingSpace.query_managment_grid.Refresh_Query(self.data)
                else:
                    pass
            else:
                return
            self.remainingSpace.delivery_order_count_sum.SetValue(str(self.delivery_sum))
            self.remainingSpace.order_count_sum.SetValue(str(self.order_sum))
            self.remainingSpace.package_count_sum.SetValue(str(self.package_sum))
            self.remainingSpace.delivery_area_sum.SetValue(str(self.order_area_sum))

        self.log.WriteText("天外天系统收到操作员控制指令，ZX_Pane.py 中开始执行日期查询操作，起始日期："+str(self.date_start)+"，终止日期："+str(self.date_end)+"\r\n")
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
    def OnTodayQuery(self,eve):
        pass
    def OnYesterdayQuery(self,eve):
        pass
    def OnBYesterdayQuery(self,eve):
        pass
    def OnBBYesterdayQuery(self,eve):
        pass
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

        style.SetCaptionStyle(mystyle)
        self._pnl.ApplyCaptionStyleAll(style)
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
    def OnStateQuery(self, event):#按发货单状态查询
        style = fpb.CaptionBarStyle()
        eventid = event.GetId()
        if eventid == self.ID_WAIT_DELIVERY:
            style.SetCaptionStyle(fpb.CAPTIONBAR_GRADIENT_H)
            self.data=[]
            if Is_Database_Connect():
                cursor = DB.cursor()
                cursor.execute(
                    "select `Delivery_ID`,`Order_amount`,`Delivery_total_area`,`Package_amount`,`Creat_date`,`Creator`,`Execute_date`,`Executor`,`Delivery_date`,`Delivery_operator`,`State` from `delivery_form_zx` where `State`='%s' ORDER BY `Creat_date` DESC"%'等待发货')
                record = cursor.fetchall()
                for i in range(len(record)):
                    inform = [record[i][0], record[i][1], record[i][2], record[i][3],
                              record[i][4].strftime('%Y-%m-%d'),
                              record[i][5], record[i][6], record[i][7], record[i][8],
                              record[i][9],
                              record[i][10]]
                    self.data.append(inform)
                    self.order_sum += int(record[i][1])
                    self.order_area_sum += int(record[i][2])
                    self.package_sum += int(record[i][3])
                self.delivery_sum = len(self.data)
                self.remainingSpace.query_managment_grid.Refresh_Query(self.data)
            else:
                return
            self.remainingSpace.delivery_order_count_sum.SetValue(str(self.delivery_sum))
            self.remainingSpace.order_count_sum.SetValue(str(self.order_sum))
            self.remainingSpace.package_count_sum.SetValue(str(self.package_sum))
            self.remainingSpace.delivery_area_sum.SetValue(str(self.order_area_sum))

        # elif eventid == self.ID_USE_VGRADIENT:
        #     style.SetCaptionStyle(fpb.CAPTIONBAR_GRADIENT_V)

        elif eventid == self.ID_DELIVERYING:
            style.SetCaptionStyle(fpb.CAPTIONBAR_SINGLE)
            self.data = []
            if Is_Database_Connect():
                cursor = DB.cursor()
                cursor.execute(
                    "select `Delivery_ID`,`Order_amount`,`Delivery_total_area`,`Package_amount`,`Creat_date`,`Creator`,`Execute_date`,`Executor`,`Delivery_date`,`Delivery_operator`,`State` from `delivery_form_zx` where `State`='%s' ORDER BY `Creat_date` DESC" % '发货中')
                record = cursor.fetchall()
                for i in range(len(record)):
                    inform = [record[i][0], record[i][1], record[i][2], record[i][3],
                              record[i][4].strftime('%Y-%m-%d'),
                              record[i][5], record[i][6], record[i][7],
                              record[i][8],
                              record[i][9],
                              record[i][10]]
                    self.data.append(inform)
                    self.order_sum += int(record[i][1])
                    self.order_area_sum += int(record[i][2])
                    self.package_sum += int(record[i][3])
                self.delivery_sum = len(self.data)
                self.remainingSpace.query_managment_grid.Refresh_Query(self.data)
            else:
                return
            self.remainingSpace.delivery_order_count_sum.SetValue(str(self.delivery_sum))
            self.remainingSpace.order_count_sum.SetValue(str(self.order_sum))
            self.remainingSpace.package_count_sum.SetValue(str(self.package_sum))
            self.remainingSpace.delivery_area_sum.SetValue(str(self.order_area_sum))

        elif eventid == self.ID_COMPLATE_DELIVERY:
            style.SetCaptionStyle(fpb.CAPTIONBAR_RECTANGLE)
            self.data = []
            if Is_Database_Connect():
                cursor = DB.cursor()
                cursor.execute(
                    "select `Delivery_ID`,`Order_amount`,`Delivery_total_area`,`Package_amount`,`Creat_date`,`Creator`,`Execute_date`,`Executor`,`Delivery_date`,`Delivery_operator`,`State` from `delivery_form_zx` where `State`='%s' ORDER BY `Creat_date` DESC" % '已发货')
                record = cursor.fetchall()
                for i in range(len(record)):
                    inform = [record[i][0], record[i][1], record[i][2], record[i][3],
                              record[i][4].strftime('%Y-%m-%d'),
                              record[i][5], record[i][6], record[i][7],
                              record[i][8],
                              record[i][9],
                              record[i][10]]
                    self.data.append(inform)
                    self.order_sum += int(record[i][1])
                    self.order_area_sum += int(record[i][2])
                    self.package_sum += int(record[i][3])
                self.delivery_sum = len(self.data)
                self.remainingSpace.query_managment_grid.Refresh_Query(self.data)
            else:
                return
            self.remainingSpace.delivery_order_count_sum.SetValue(str(self.delivery_sum))
            self.remainingSpace.order_count_sum.SetValue(str(self.order_sum))
            self.remainingSpace.package_count_sum.SetValue(str(self.package_sum))
            self.remainingSpace.delivery_area_sum.SetValue(str(self.order_area_sum))

        elif eventid == self.ID_CANCEL_DELIVERY:
            style.SetCaptionStyle(fpb.CAPTIONBAR_FILLED_RECTANGLE)
            self.data = []
            if Is_Database_Connect():
                cursor = DB.cursor()
                cursor.execute(
                    "select `Delivery_ID`,`Order_amount`,`Delivery_total_area`,`Package_amount`,`Creat_date`,`Creator`,`Execute_date`,`Executor`,`Delivery_date`,`Delivery_operator`,`State` from `delivery_form_zx` where `State`='%s' ORDER BY `Creat_date` DESC" % '已取消')
                record = cursor.fetchall()
                for i in range(len(record)):
                    inform = [record[i][0], record[i][1], record[i][2], record[i][3],record[i][4].strftime('%Y-%m-%d'),
                              record[i][5], record[i][6], record[i][7],record[i][8],record[i][9],record[i][10]]
                    self.data.append(inform)
                    self.order_sum += int(record[i][1])
                    self.order_area_sum += int(record[i][2])
                    self.package_sum += int(record[i][3])
                self.delivery_sum = len(self.data)
                self.remainingSpace.query_managment_grid.Refresh_Query(self.data)
            else:
                return
            self.remainingSpace.delivery_order_count_sum.SetValue(str(self.delivery_sum))
            self.remainingSpace.order_count_sum.SetValue(str(self.order_sum))
            self.remainingSpace.package_count_sum.SetValue(str(self.package_sum))
            self.remainingSpace.delivery_area_sum.SetValue(str(self.order_area_sum))
        else:
            raise "ERROR: Undefined State : " + repr(eventid)
class Pvc_Workposition_Right_Panel_Workorder(wx.Panel):
    def __init__(self, parent,log, id=wx.ID_ANY, title="", pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE):
        wx.Panel.__init__(self, parent)
        self.log=log
        self.ticker = Ticker(self)
        self.ticker.SetBackgroundColour((255,0,255))
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.ticker, flag=wx.EXPAND|wx.ALL, border=5)
        self.SetSizer(vbox)
        self.ticker.SetDirection("ltr")
        # self.ticker.SetFont(self.ticker.GetFont())
        self.ticker.SetText("系统建设中，敬请期待")
        self.Bind(wx.EVT_WINDOW_DESTROY,self.OnClose)
    def OnClose(self,event):
        self.ticker.Stop()
    def ShutdownTicker(self):
        self.ticker.Stop()
class Pvc_Workposition_Right_Panel(wx.Notebook):
    def __init__(self, parent, id, log):
        wx.Notebook.__init__(self, parent, id, size=(21,21), style=
                             wx.BK_DEFAULT|wx.SUNKEN_BORDER
                             #wx.BK_TOP
                             #wx.BK_BOTTOM
                             #wx.BK_LEFT
                             #wx.BK_RIGHT
                             # | wx.NB_MULTILINE
                             )
        self.log = log
        self.pvc_workposition_right_show1 = Pvc_Workposition_Right_Panel_Workorder(self,self.log)
        self.pvc_workposition_right_show2 = wx.TextCtrl(self)
        self.AddPage(self.pvc_workposition_right_show1, "工位工单管理")
        self.AddPage(self.pvc_workposition_right_show2, "工位订单管理")
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnPageChanging)


    def OnPageChanged(self, event):
        if self:
            old = event.GetOldSelection()
            new = event.GetSelection()
            sel = self.GetSelection()
            # self.log.write('OnPageChanged,  old:%d, new:%d, sel:%d\n' % (old, new, sel))
        event.Skip()

    def OnPageChanging(self, event):
        if self:
            old = event.GetOldSelection()
            new = event.GetSelection()
            sel = self.GetSelection()
            # self.log.write('OnPageChanging, old:%d, new:%d, sel:%d\n' % (old, new, sel))
        event.Skip()
#-------------------------------------------------------------cnc工位工单管理界面
class Layout_Picture_Panel(wx.Panel):
    """ class MyPanel creates a panel to draw on, inherits wx.Panel """
    def __init__(self, parent,log,size=(500,300)):
        # create a panel
        self.log=log
        # self.paint_times=0
        wx.Panel.__init__(self, parent,size=size,style=wx.SUNKEN_BORDER)
        self.SetBackgroundColour("white")
        # self.Bind(wx.EVT_PAINT, self.OnPaint)
    def OnPaint(self,Ap_id):
        """set up the device context (DC) for painting"""
        try:
            layout_inform=[]
            if Ap_id == '':
                pass
            else:
                self.Ap_id = Ap_id
                if Is_Database_Connect():
                    cursor=DB.cursor()
                    cursor.execute(
                        "SELECT `Material_norm`,`Total_seg` FROM `work_cnc_task_list` WHERE `Ap_id`='%s'" % self.Ap_id)
                    record = cursor.fetchone()
                    material_size = record[0].split('*')
                    for i in range(record[1]):
                        element_list = []
                        str1 = 'Element_information_' + str(i + 1)
                        cursor.execute(
                            "SELECT `%s` FROM `work_cnc_task_list` WHERE `Ap_id`='%s'" % (str1, self.Ap_id))
                        element_information = cursor.fetchone()
                        for j in (element_information):  # for i in range():是指遍布这个列表或元组的每一个元素；for i in ()是指遍布这个列表和元组的一行。
                            element_list.append(element_information[0])
                        split_list = element_list[0].split('&')  # 获得零件的坐标及高宽信息
                        label_and_size = split_list[0].split(',')
                        layout_inform.append(
                            [float(label_and_size[0]), float(label_and_size[1]), float(label_and_size[2]), float(label_and_size[3]), int(label_and_size[4]),
                             split_list[2], float(material_size[0]), float(material_size[1]),split_list[1],split_list[1]])
                else:
                    return
            self.dc = wx.ClientDC(self)
            rect = self.GetClientRect()
            width=rect.width
            height=rect.height
            self.dc.SetPen(wx.BLACK_PEN)          # for drawing lines / borders
            yellowbrush = wx.Brush(wx.Colour(244, 164, 96))
            self.dc.SetBrush(yellowbrush)  # Yellow fill
            self.dc.SetDeviceOrigin(1, height-10) # 先改变坐标原点,将坐标原点改为左下角。
            # self.dc.SetAxisOrientation(True,False)                      #再改变象限,true代表x方向为正
            self.dc.SetAxisOrientation(True,True)                      #再改变象限,true代表x方向为正
            self.dc.DrawRectangle(1,-8,width-10, height-3)  # 排样标准型材的尺寸(2440*1220)
            # split1=split_list[1].split('_')
            # lmz=split1[0]
            # split_style=lmz[0:2]
            # try:
            for i in range(record[1]):
                if layout_inform[i][4] == 0:  # 门板不旋转了,按当前的画法，高宽不变
                    is_image_exist=os.path.exists(u"C:\\image\\"+str(layout_inform[i][9])+"&0"+str(layout_inform[i][4])+".png")#判断路径下是否存在图片
                    if is_image_exist:
                        bmp = wx.Bitmap(u"C:\\image\\"+str(layout_inform[i][9])+"&0"+str(layout_inform[i][4])+".png")
                    else:
                        bmp = wx.Bitmap(u"C:\\image\\None.png")
                else:
                    is_image_exist = os.path.exists(u"C:\image\\" + str(layout_inform[i][9]) + "&0" + str(layout_inform[i][4]) + ".png")
                    if is_image_exist:
                        bmp = wx.Bitmap(u"C:\\image\\"+str(layout_inform[i][9])+"&0"+str(layout_inform[i][4])+".png")
                    else:
                        bmp = wx.Bitmap(u"C:\\image\\None.png")
                    now_long = layout_inform[i][3]  # 旋转，高和宽互换
                    layout_inform[i][3] = layout_inform[i][2]
                    layout_inform[i][2] = str(now_long)
                w = ((float(layout_inform[i][3]))/float( layout_inform[i][6])) * (width-10)
                h = ((float(layout_inform[i][2]))/float(layout_inform[i][7])) * (height-3)
                img = bmp.ConvertToImage()
                bmp = img.Scale(w, h)
                bmp = bmp.ConvertToBitmap()
                self.dc.DrawBitmap(bmp,layout_inform[i][0]/(float(layout_inform[i][6]))*(width-10)+1,
                                layout_inform[i][1] /float(layout_inform[i][7])*(height-3)-8)
                                    #横纵坐标
                # self.dc.DrawBitmap(bmp,1,-8)
                # num = str(i + 1) + '号 '+' \n零件编号:' + str(layout_inform[i][5])
                #
                # self.dc.DrawText(num,layout_inform[i][0]/(float(layout_inform[i][6]))*(width-10)+1,
                #                  layout_inform[i][1] / float(layout_inform[i][7]) * (height - 3) + 13)
                # self.dc.DrawText(num,1,-8)
                if layout_inform[i][4] == 0:  # 将换过的高和宽换回来，否则重绘的时候就会出现问题
                    now_long = layout_inform[i][2]  # 没旋转，高和宽互换
                    layout_inform[i][2] = layout_inform[i][3]
                    layout_inform[i][3] = now_long
            del self.dc
            # except:
            #     self.log.WriteText('天外天系统正在运行ZX_Pane.py Layout_Picture_Panel类中执行画排样图时出现错误，请检查当前执行文件目录下是否有相应图片\r\n')
        except:
            self.log.WriteText('天外天系统正在运行ZX_Pane.py Layout_Picture_Panel类中执行画排样图时出现错误，请检查当前执行文件目录下是否有相应图片\r\n')
class Cnc_Workposition_Right_Panel_Workorder(wx.Panel):
    def __init__(self,parent,log):
        wx.Panel.__init__(self, parent, -1,style=wx.BK_DEFAULT|wx.SUNKEN_BORDER)
        self.log=log
        self.layout_picture_panel = Layout_Picture_Panel(self, self.log, size=(500, 300))
        btn_Priority = wx.Button(self,1005, "优先生产")
        btn_Reprint_Barcode = wx.Button(self, wx.ID_ANY, "打印条形码")
        btn_Reproduction  = wx.Button(self, 1006, "恢复生产")
        btn_production_allocation  = wx.Button(self, wx.ID_ANY, "生产调度分配")
        cnc_total_count = wx.TextCtrl(self, wx.ID_ANY, size=(87, 20), style=wx.TE_READONLY)
        cnc_finish_count = wx.TextCtrl(self, wx.ID_ANY, size=(75, 20), style=wx.TE_READONLY)
        cnc_unfinish_count = wx.TextCtrl(self, wx.ID_ANY, size=(87, 20), style=wx.TE_READONLY)
        machine1_cnc_count = wx.TextCtrl(self, wx.ID_ANY, size=(60, 20), style=wx.TE_READONLY)
        machine2_cnc_count = wx.TextCtrl(self, wx.ID_ANY, size=(60, 20), style=wx.TE_READONLY)
        machine3_cnc_count = wx.TextCtrl(self, wx.ID_ANY, size=(60, 20), style=wx.TE_READONLY)
        machine4_cnc_count = wx.TextCtrl(self, wx.ID_ANY, size=(60, 20), style=wx.TE_READONLY)
        machine5_cnc_count = wx.TextCtrl(self, wx.ID_ANY, size=(60, 20), style=wx.TE_READONLY)
        machine6_cnc_count = wx.TextCtrl(self, wx.ID_ANY, size=(60, 20), style=wx.TE_READONLY)

        ap_id = wx.TextCtrl(self, wx.ID_ANY, size=(110, 20), style=wx.TE_READONLY)
        schedule_date = wx.TextCtrl(self, wx.ID_ANY, size=(90, 20), style=wx.TE_READONLY)
        board_num = wx.TextCtrl(self, wx.ID_ANY, size=(100, 20), style=wx.TE_READONLY)
        processing_time = wx.TextCtrl(self, wx.ID_ANY, size=(110, 20), style=wx.TE_READONLY)
        operator = wx.TextCtrl(self, wx.ID_ANY, size=(90, 20), style=wx.TE_READONLY)
        utilization_ratio = wx.TextCtrl(self, wx.ID_ANY, size=(90, 20), style=wx.TE_READONLY)

        self.cnc_workposition_right_grid=Cnc_Workposition_Right_Grid(self,self.log,self.layout_picture_panel,btn_Priority,btn_Reprint_Barcode,btn_Reproduction,btn_production_allocation,
                                                                     cnc_total_count,cnc_finish_count,cnc_unfinish_count,machine1_cnc_count,
                                                                     machine2_cnc_count,machine3_cnc_count,machine4_cnc_count,machine5_cnc_count,machine6_cnc_count,
                                                                     ap_id,schedule_date,board_num,processing_time,operator,utilization_ratio)
        label1 = wx.StaticText(self, -1, "当日待完成工单总数")
        label2 = wx.StaticText(self, -1, "实际完成工单数")
        label3 = wx.StaticText(self, -1, "待加工工单数")
        label4 = wx.StaticText(self, -1, "1#机台完成工单数")
        label5 = wx.StaticText(self, -1, "2#机台完成工单数")
        label6 = wx.StaticText(self, -1, "3#机台完成工单数")
        label7 = wx.StaticText(self, -1, "4#机台完成工单数")
        label8 = wx.StaticText(self, -1, "5#机台完成工单数")
        label9 = wx.StaticText(self, -1, "6#机台完成工单数")

        xbox1 = wx.BoxSizer()
        xbox1.Add(label1, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox1.Add(cnc_total_count, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox2 = wx.BoxSizer()
        xbox2.Add(label2, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox2.Add(cnc_finish_count, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox3 = wx.BoxSizer()
        xbox3.Add(label3, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox3.Add(cnc_unfinish_count, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox4 = wx.BoxSizer()
        xbox4.Add(label4, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox4.Add(machine1_cnc_count, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox5 = wx.BoxSizer()
        xbox5.Add(label5, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox5.Add(machine2_cnc_count, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox6 = wx.BoxSizer()
        xbox6.Add(label6, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox6.Add(machine3_cnc_count, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox7 = wx.BoxSizer()
        xbox7.Add(label7, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox7.Add(machine4_cnc_count, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox8 = wx.BoxSizer()
        xbox8.Add(label8, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox8.Add(machine5_cnc_count, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox9 = wx.BoxSizer()
        xbox9.Add(label9, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox9.Add(machine6_cnc_count, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        #----------------------------------------------将统计栏分为三行，使用两个水平sizer和一个垂直staticsizer
        xbox10 = wx.BoxSizer()
        xbox10.Add(xbox1, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox10.Add(xbox2, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox10.Add(xbox3, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox11 = wx.BoxSizer()
        xbox11.Add(xbox4, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox11.Add(xbox5, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox11.Add(xbox6, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox12 = wx.BoxSizer()
        xbox12.Add(xbox7, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox12.Add(xbox8, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox12.Add(xbox9, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)

        statisticbox = wx.StaticBox(self, -1)
        statisticsizer1 = wx.StaticBoxSizer(statisticbox, wx.VERTICAL)
        statisticsizer1.Add(xbox10, proportion=1, flag=wx.EXPAND, border=3)
        statisticsizer1.Add(xbox11, proportion=1, flag=wx.EXPAND, border=3)
        statisticsizer1.Add(xbox12, proportion=1, flag=wx.EXPAND, border=3)
        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox1.Add(statisticsizer1, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        vbox1.Add(self.cnc_workposition_right_grid, proportion=1, flag=wx.EXPAND | wx.ALL, border=3)
#----------------------------------------------------------设置右边查询栏
        label10 = wx.StaticText(self, -1, "工单编号")
        label11 = wx.StaticText(self, -1, "排产日期")
        label12 = wx.StaticText(self, -1, "门板数量")
        label13 = wx.StaticText(self, -1, "加工工时")
        label14 = wx.StaticText(self, -1, "操 作 员 ")
        label15 = wx.StaticText(self, -1, "板材利用率")

        xbox13 = wx.BoxSizer()
        xbox13.Add(label10, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox13.Add(ap_id, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox14 = wx.BoxSizer()
        xbox14.Add(label11, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox14.Add(schedule_date, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox15 = wx.BoxSizer()
        xbox15.Add(label12, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox15.Add(board_num, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox16 = wx.BoxSizer()
        xbox16.Add(label13, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox16.Add(processing_time, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox17 = wx.BoxSizer()
        xbox17.Add(label14, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox17.Add(operator, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox18 = wx.BoxSizer()
        xbox18.Add(label15, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xbox18.Add(utilization_ratio, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
#--------------------------------------------------使用三个水平sizer和一个垂直staticsizer
        xbox19 = wx.BoxSizer()
        xbox19.Add(xbox13, proportion=1, flag=wx.EXPAND | wx.ALL, border=3)
        xbox19.Add(xbox14, proportion=1, flag=wx.EXPAND | wx.ALL, border=3)
        xbox19.Add(xbox15, proportion=1, flag=wx.EXPAND | wx.ALL, border=3)
        xbox20 = wx.BoxSizer()
        xbox20.Add(xbox16, proportion=1, flag=wx.EXPAND | wx.ALL, border=3)
        xbox20.Add(xbox17, proportion=1, flag=wx.EXPAND | wx.ALL, border=3)
        xbox20.Add(xbox18, proportion=1, flag=wx.EXPAND | wx.ALL, border=3)

        staticbox_query = wx.StaticBox(self, -1)
        statisticsizer2 = wx.StaticBoxSizer(staticbox_query, wx.VERTICAL)
        statisticsizer2.Add(xbox19, proportion=1, flag=wx.EXPAND, border=3)
        statisticsizer2.Add(xbox20, proportion=1, flag=wx.EXPAND, border=3)
        # self.btn_Reprint_Barcode = wx.Button(self, wx.ID_ANY,"打印条形码")
        self.Bind(wx.EVT_BUTTON,self.OnReprintBarcode,btn_Reprint_Barcode)
        # btn_send_wechat = wx.Button(self, 1007,"微信发布CNC任务")
        # self.btn_Priority = wx.Button(self, wx.ID_ANY,"优先生产")
        self.Bind(wx.EVT_BUTTON, self.OnPriority, btn_Priority)
        self.Bind(wx.EVT_BUTTON, self.OnPriority, btn_Reproduction)
        self.Bind(wx.EVT_BUTTON, self.OnProductionAllocation, btn_production_allocation)
#----------------------------------
        xbox21 = wx.BoxSizer()
        xbox21.Add(btn_Reprint_Barcode, proportion=1, flag=wx.EXPAND | wx.ALL, border=3)
        xbox21.Add(btn_Priority, proportion=1, flag=wx.EXPAND | wx.ALL, border=3)
        xbox21.Add(btn_Reproduction, proportion=1, flag=wx.EXPAND | wx.ALL, border=3)
        xbox21.Add(btn_production_allocation, proportion=1, flag=wx.EXPAND | wx.ALL, border=3)
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        # self.cnc_workposition_right_show=wx.TextCtrl(self)
        vbox2.Add(statisticsizer2, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        # vbox2.Add(self.cnc_workposition_right_show, proportion=1, flag=wx.EXPAND | wx.ALL, border=3)
        vbox2.Add(self.layout_picture_panel, proportion=1, flag=wx.EXPAND | wx.ALL, border=3)
        vbox2.Add(xbox21, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        hbox=wx.BoxSizer()
        hbox.Add(vbox1,proportion=1,flag=wx.EXPAND|wx.ALL,border=3)
        hbox.Add(vbox2,proportion=2,flag=wx.EXPAND|wx.ALL,border=3)
        self.SetSizer(hbox)
        self.timer = wx.PyTimer(self.Refresh_left)
        self.timer.Start(10000)
        # self.timer= wx.PyTimer(self.Refresh_right)
        # self.timer.Start(5000)
        btn_Reprint_Barcode.Enable(False)
        btn_Priority.Enable(False)
        btn_Reproduction.Enable(False)
        if self.cnc_workposition_right_grid.inform_unreception!=[]:
            btn_production_allocation.Enable(True)
        else:
            btn_production_allocation.Enable(False)
    def Refresh_left(self):
        try:
            self.cnc_workposition_right_grid.MyRefresh()
        except:
            self.log.WriteText('天外天系统正在运行ZX_Pane.py 中 Cnc_Workposition_Right_Panel_Workorder类下的Refresh_left方法时发生错误，请检查   \r\n')
    def OnReprintBarcode(self,eve):
        try:
            if Is_Database_Connect():
                cursor = DB.cursor()
                cursor.execute(
                    "SELECT `State` from `work_cnc_task_list` WHERE `Ap_id`='%s'" % (self.cnc_workposition_right_grid.printbarcode_id))
                record=cursor.fetchone()
                if record[0]==10 or record[0]==DOOR_WORK_FISHED or record[0]==ALL_WORK_FISHED:
                    cursor.execute(
                        "UPDATE `work_cnc_task_list` set `Print_Barcode`='%s' WHERE `Ap_id`='%s'" % (
                            REPRINT_BARCODE,self.cnc_workposition_right_grid.printbarcode_id))
                    DB.commit()
                else:
                    self.log.WriteText('天外天程序正在ZX_Pane.py 中执行操作员重新打印条形码操作，工单状态不在重新打印条形码的操作范围  \r\n')
        except:
            self.log.WriteText('天外天系统正在ZX_Pane.py 中运行ReprintBarcode方法，往数据库中更新Print_Barcode字段时出现错误 \r\n')
    def OnPriority(self,eve):
        if Is_Database_Connect():
            cursor=DB.cursor()
            if eve.GetId()==1005:
                cursor.execute("UPDATE `work_cnc_task_list` set `Priority`='%s' WHERE `Ap_id`='%s' " % (
                    10, self.cnc_workposition_right_grid.Priority_id))
            elif eve.GetId()==1006:
                cursor.execute("UPDATE `work_cnc_task_list` set `State`='%s',`Receive_time`=NULL ,`Machine_Begin_Time`=NULL,`Machine_Finish_Time`=NULL,`Operator_id`=NULL,`Machine_num`=NULL,`CNC`= 0,`NC_PATH`=NULL  WHERE `Ap_id`='%s' " % (
                    0, self.cnc_workposition_right_grid.Reproduction_id))
            else:
                pass
            DB.commit()
            self.cnc_workposition_right_grid.MyRefresh()
        else:
            self.log.WriteText("天外天系统正在运行ZX_Pane.py OnPriority方法，更新数据库数据时出现错误，请检查是否连接数据库\r\n")
            return
    def OnProductionAllocation(self,event):
        Password_dlg = wx.PasswordEntryDialog(self, '请输入系统管理员密码：', '管理员权限设置登录')
        Password_dlg.SetValue("")
        if Password_dlg.ShowModal() == wx.ID_OK:
            self.password = Password_dlg.GetValue()
            if self.password == "hello8031":
                dlg = Production_Scheduling_Allocation_Dialog(self, -1, "生产调度机床号分配窗口", size=(800, 600), pos=wx.DefaultPosition,
                                        style=wx.DEFAULT_DIALOG_STYLE)
                dlg.CenterOnScreen()
                val = dlg.ShowModal()
                if val == wx.ID_OK:  # 类似于绑定事件，将参数传到pdf类
                    dlg1 = wx.MessageDialog(self, '请确认是否保存更改', '警告',
                                            wx.OK | wx.ICON_INFORMATION | wx.CANCEL
                                            # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                                            )
                    val1 = dlg1.ShowModal()
                    if val1 == wx.ID_OK:
                        if Is_Database_Connect():
                            cursor=DB.cursor()
                            cursor.execute(
                                "UPDATE `work_cnc_task_list` SET `Machine_nums`='%s' where `State`='%s' and `Machine_nums`='%s' " % (dlg.alternative_num, NO_RECEPTION,'4'))#'4'代表加工机床为4号机床
                            DB.commit()
                            message='备用机床号保存成功，请提示'+str(dlg.alternative_num)+'号机床操作员：\r\n1、注意单边对齐\r\n2、注意相应板材更换'
                            dlg = wx.MessageDialog(self, message, '提示',
                                                    wx.OK | wx.ICON_INFORMATION | wx.CANCEL
                                                    # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                                                    )
                            dlg.ShowModal()
                        else:
                            return
            else:
                tip_dlg = wx.MessageDialog(self, '密码错误！您没有生产调度分配权限，请联系管理员！', '提示',
                                        wx.OK | wx.ICON_INFORMATION
                                        # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                                        )
                tip_dlg.ShowModal()

        event.Skip()
class Cnc_Workposition_Right_Grid(gridlib.Grid):
    def __init__(self, parent,log,panit,priority_btn,printbarcode_btn,reproduction_btn,production_allocation_btn,cnc_total_count,cnc_finish_count,cnc_unfinish_count,
        machine1_cnc_count,machine2_cnc_count,machine3_cnc_count,machine4_cnc_count,machine5_cnc_count,machine6_cnc_count,ap_id,schedule_date,board_num,processing_time,operator,utilization_ratio):
        gridlib.Grid.__init__(self, parent,-1)
        self.log=log
        self.inform_unreception = []
        self.paint=panit
        self.priority_btn=priority_btn
        self.printbarcode_btn=printbarcode_btn
        self.reproduction_btn=reproduction_btn
        self.production_allocation_btn=production_allocation_btn
        self.cnc_total_count=cnc_total_count
        self.cnc_finish_count=cnc_finish_count
        self.cnc_unfinish_count=cnc_unfinish_count
        self.machine1_cnc_count=machine1_cnc_count
        self.machine2_cnc_count=machine2_cnc_count
        self.machine3_cnc_count=machine3_cnc_count
        self.machine4_cnc_count=machine4_cnc_count
        self.machine5_cnc_count=machine5_cnc_count
        self.machine6_cnc_count=machine6_cnc_count
        self.ap_id=ap_id
        self.schedule_date=schedule_date
        self.element_total = board_num
        self.minutes = processing_time
        self.operator_id = operator
        self.board_utilization_ratio =utilization_ratio
        self.field_name = ['1号机台','2号机台', '3号机台', '4号机台', '5号机台', '6号机台', '未分配工单', '故障工单']
        self.CreateGrid(0, 8)  # , gridlib.Grid.SelectRows)   #利用从数据库里读出来的列表，来建一个对应行数和列数的表格
        for i in range(len(self.field_name)):  # 用来填写所有表头信息
            self.SetColLabelValue(i, self.field_name[i])
        self.date = datetime.date.today().strftime('%Y%m%d')
        self.MyRefresh()
        self.EnableEditing(False)
        self.AutoSizeColumns(False)
        self.SetRowLabelSize(25)
        self.DisableDragColSize()
        self.DisableDragRowSize()
        self.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.OnLeftClick)
        # self.timer= wx.PyTimer(self.MyRefresh)
        # self.timer.Start(5000)
    def MyRefresh(self):
        # start_time = datetime.datetime.now()
        self.inform_unreception = []
        inform1 = []
        inform2 = []
        inform3 = []
        inform4 = []
        inform5 = []
        inform6 = []
        inform_error = []
        workout_realy = 0
        no_workout_realy = 0
        try:
            if Is_Database_Connect():
                    cursor = DB.cursor()
                    cursor.execute(
                        "select `Ap_id`,`Receive_time`,`Machine_num`,`State`,`Schedule_date`,`Priority`,`Glass_num`from `work_cnc_task_list` where ((`State`='%s'or `State`='%s'or `State`='%s') and TO_DAYS(`Receive_time`) = TO_DAYS('%s') )or (`State`='%s'or `State`='%s') ORDER BY `Priority` DESC ,`Index` " % (
                        CREATE_CNC, DOOR_WORK_FISHED, ALL_WORK_FISHED, (self.date), NO_RECEPTION, ERROR_TASK_LIST))
                    record = cursor.fetchall()
                    if record != None:
                        for i in range(len(record)):
                            s1 = record[i][4].split('-')
                            s2 = s1[0], s1[1], s1[2]
                            sd = ''
                            schedule_date = str(sd.join(s2))  # 排产日期
                            if record[i][3] == NO_RECEPTION:
                                if schedule_date<=self.date:
                                    t1 = str(record[i][0]).split('_')
                                    t2 = t1[1][2:]
                                    temporary = [t2, schedule_date, record[i][3], record[i][5], record[i][6]]
                                    self.inform_unreception.append(temporary)
                            elif record[i][3] == ERROR_TASK_LIST:
                                if schedule_date<=self.date:
                                    t1 = str(record[i][0]).split('_')
                                    t2 = t1[1][2:]
                                    temporary = [t2, schedule_date, record[i][3]]
                                    inform_error.append(temporary)
                            else:
                                # recieve_time = record[i][1].strftime('%Y%m%d')  # 接单时间
                                if record[i][2] == '1':
                                    t1 = str(record[i][0]).split('_')
                                    t2 = t1[1][2:]
                                    temporary = [t2, schedule_date, record[i][3]]
                                    inform1.append(temporary)
                                elif record[i][2] == '2':
                                    t1 = str(record[i][0]).split('_')
                                    t2 = t1[1][2:]
                                    temporary = [t2, schedule_date, record[i][3]]
                                    inform2.append(temporary)
                                elif record[i][2] == '3':
                                    t1 = str(record[i][0]).split('_')
                                    t2 = t1[1][2:]
                                    temporary = [t2, schedule_date, record[i][3]]
                                    inform3.append(temporary)
                                elif record[i][2] == '4':
                                    t1 = str(record[i][0]).split('_')
                                    t2 = t1[1][2:]
                                    temporary = [t2, schedule_date, record[i][3]]
                                    inform4.append(temporary)
                                elif record[i][2] == '5':
                                    t1 = str(record[i][0]).split('_')
                                    t2 = t1[1][2:]
                                    temporary = [t2, schedule_date, record[i][3]]
                                    inform5.append(temporary)
                                elif record[i][2] == '6':
                                    t1 = str(record[i][0]).split('_')
                                    t2 = t1[1][2:]
                                    temporary = [t2, schedule_date, record[i][3]]
                                    inform6.append(temporary)
                                else:
                                    self.log.WriteText(
                                        "天外天系统正在运行ZX_Pane.py Cnc_Workposition_Right_Grid()，请检查cnc_work_task_list表单中已接单机床号是否填写\r\n")
                            if record[i][3] == ALL_WORK_FISHED:
                                workout_realy += 1
                            elif record[i][3] == ERROR_TASK_LIST or record[i][3] == NO_RECEPTION and schedule_date<=self.date:
                                no_workout_realy += 1
                            else:
                                pass
                        self.cnc_total_count.SetValue(str(len(self.inform_unreception)))
                        self.cnc_finish_count.SetValue(str(workout_realy))
                        self.cnc_unfinish_count.SetValue(str(no_workout_realy))
                        self.machine1_cnc_count.SetValue(str(flatten(inform1).count(ALL_WORK_FISHED)))
                        self.machine2_cnc_count.SetValue(str(flatten(inform2).count(ALL_WORK_FISHED)))
                        self.machine3_cnc_count.SetValue(str(flatten(inform3).count(ALL_WORK_FISHED)))
                        self.machine4_cnc_count.SetValue(str(flatten(inform4).count(ALL_WORK_FISHED)))
                        self.machine5_cnc_count.SetValue(str(flatten(inform5).count(ALL_WORK_FISHED)))
                        self.machine6_cnc_count.SetValue(str(flatten(inform6).count(ALL_WORK_FISHED)))
                    else:
                        pass
        except:
            self.log.WriteText(
                '天外天系统正在运行 ZX_Pane.py中Cnc_Workposition_Right_Grid类 读取数据库work_cnc_task_list表单操作，可能出现字段填写不完整现象，请检查数据库中数据    \r\n')
            return
        Max_len = max(len(self.inform_unreception), len(inform1), len(inform2), len(inform3), len(inform4), len(inform5),
                      len(inform6), len(inform_error))
        now_rows = self.GetNumberRows()
        try:
            if Max_len > now_rows:
                for i in range(Max_len - now_rows):
                    self.AppendRows(numRows=1)
            elif Max_len < now_rows:
                for i in range(now_rows - Max_len):
                    self.DeleteRows(numRows=1)
            else:
                pass
            self.ClearGrid()#用来清除表格数据
            if Max_len != 0:
                for i in range(Max_len):#用来清除背景色
                    for j in range(len(self.field_name)):
                        self.SetCellBackgroundColour(i,j, wx.WHITE)
                for i in range(len(self.field_name)):  # 用来填写所有表头信息
                    self.SetColLabelValue(i, self.field_name[i])
                self.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

                if len(self.inform_unreception) != 0:
                    self.production_allocation_btn.Enable(True)
                    for i in range(len(self.inform_unreception)):  # 填数据
                        if self.inform_unreception[i][4]==0:
                            self.SetCellBackgroundColour(i,6,wx.WHITE)#设置玻璃门的背景颜色为灰色
                            if self.date == self.inform_unreception[i][1]:
                                self.SetCellValue(i, 6, str(self.inform_unreception[i][0]))
                                self.SetCellTextColour(i, 6, wx.BLACK)
                            elif int(self.date) - int(self.inform_unreception[i][1]) == 1:
                                self.SetCellValue(i, 6, str(self.inform_unreception[i][0]))
                                self.SetCellTextColour(i, 6, wx.BLUE)
                            elif int(self.date) - int(self.inform_unreception[i][1]) == 2:
                                self.SetCellValue(i, 6, str(self.inform_unreception[i][0]))
                                self.SetCellTextColour(i, 6, (160,32,240))
                            elif int(self.date) - int(self.inform_unreception[i][1]) >= 3:
                                self.SetCellValue(i, 6, str(self.inform_unreception[i][0]))
                                self.SetCellTextColour(i, 6, wx.CYAN)
                            else:
                                pass
                        else:
                            self.SetCellBackgroundColour(i, 6, wx.LIGHT_GREY)
                            if self.date == self.inform_unreception[i][1]:
                                # self.SetCellColour(i,6,())
                                self.SetCellValue(i, 6, str(self.inform_unreception[i][0]))
                                self.SetCellTextColour(i, 6, wx.BLACK)
                            elif int(self.date) - int(self.inform_unreception[i][1]) == 1:
                                self.SetCellValue(i, 6, str(self.inform_unreception[i][0]))
                                self.SetCellTextColour(i, 6, wx.BLUE)
                            elif int(self.date) - int(self.inform_unreception[i][1]) == 2:
                                self.SetCellValue(i, 6, str(self.inform_unreception[i][0]))
                                self.SetCellTextColour(i, 6, (160, 32, 240))
                            elif int(self.date) - int(self.inform_unreception[i][1]) >= 3:
                                self.SetCellValue(i, 6, str(self.inform_unreception[i][0]))
                                self.SetCellTextColour(i, 6, wx.CYAN)
                            else:
                                pass
                else:
                    self.production_allocation_btn.Enable(False)
                if len(inform1) != 0:
                    for i in range(len(inform1)):
                        if inform1[i][2] == CREATE_CNC:
                            if self.date == inform1[i][1]:
                                self.SetCellValue(i, 0, inform1[i][0])
                                self.SetCellBackgroundColour(i, 0, wx.YELLOW)
                                self.SetCellTextColour(i, 0, wx.BLACK)
                            elif int(self.date) - int(inform1[i][1]) == 1:
                                self.SetCellValue(i, 0, inform1[i][0])
                                self.SetCellBackgroundColour(i, 0, wx.YELLOW)
                                self.SetCellTextColour(i, 0, wx.BLUE)
                            elif int(self.date) - int(inform1[i][1]) == 2:
                                self.SetCellValue(i, 0, inform1[i][0])
                                self.SetCellBackgroundColour(i, 0, wx.YELLOW)
                                self.SetCellTextColour(i, 0, (160,32,240))
                            elif int(self.date) - int(inform1[i][1]) >= 3:
                                self.SetCellValue(i, 0, inform1[i][0])
                                self.SetCellBackgroundColour(i, 0, wx.YELLOW)
                                self.SetCellTextColour(i, 0, wx.CYAN)
                            else:
                                pass
                        elif inform1[i][2] == ALL_WORK_FISHED or inform1[i][2] == DOOR_WORK_FISHED:
                            if self.date == inform1[i][1]:
                                self.SetCellValue(i, 0, inform1[i][0])
                                self.SetCellBackgroundColour(i, 0, wx.GREEN)
                                self.SetCellTextColour(i, 0, wx.BLACK)
                            elif int(self.date) - int(inform1[i][1]) == 1:
                                self.SetCellValue(i, 0, inform1[i][0])
                                self.SetCellBackgroundColour(i, 0, wx.GREEN)
                                self.SetCellTextColour(i, 0, wx.BLUE)
                            elif int(self.date) - int(inform1[i][1]) == 2:
                                self.SetCellValue(i, 0, inform1[i][0])
                                self.SetCellBackgroundColour(i, 0, wx.GREEN)
                                self.SetCellTextColour(i, 0,(160,32,240))
                            elif int(self.date) - int(inform1[i][1]) >= 3:
                                self.SetCellValue(i, 0, inform1[i][0])
                                self.SetCellBackgroundColour(i, 0, wx.GREEN)
                                self.SetCellTextColour(i, 0, wx.CYAN)
                            else:
                                self.SetCellBackgroundColour(i, 0, wx.WHITE)
                        else:
                            pass
                else:
                    pass
                if len(inform2) != 0:
                    for i in range(len(inform2)):
                        if inform2[i][2] == CREATE_CNC:
                            if self.date == inform2[i][1]:
                                self.SetCellValue(i, 1, inform2[i][0])
                                self.SetCellBackgroundColour(i, 1, wx.YELLOW)
                                self.SetCellTextColour(i, 1, wx.BLACK)
                            elif int(self.date) - int(inform2[i][1]) == 1:
                                self.SetCellValue(i, 1, inform2[i][0])
                                self.SetCellBackgroundColour(i, 1, wx.YELLOW)
                                self.SetCellTextColour(i, 1, wx.BLUE)
                            elif int(self.date) - int(inform2[i][1]) == 2:
                                self.SetCellValue(i, 1, inform2[i][0])
                                self.SetCellBackgroundColour(i, 1, wx.YELLOW)
                                self.SetCellTextColour(i, 1,(160,32,240))
                            elif int(self.date) - int(inform2[i][1]) >= 3:
                                self.SetCellValue(i, 1, inform2[i][0])
                                self.SetCellBackgroundColour(i, 1, wx.YELLOW)
                                self.SetCellTextColour(i, 1, wx.CYAN)
                            else:
                                pass
                        elif inform2[i][2] == ALL_WORK_FISHED or inform2[i][2] == DOOR_WORK_FISHED:
                            if self.date == inform2[i][1]:
                                self.SetCellValue(i, 1, inform2[i][0])
                                self.SetCellBackgroundColour(i, 1, wx.GREEN)
                                self.SetCellTextColour(i, 1, wx.BLACK)
                            elif int(self.date) - int(inform2[i][1]) == 1:
                                self.SetCellValue(i, 1, inform2[i][0])
                                self.SetCellBackgroundColour(i, 1, wx.GREEN)
                                self.SetCellTextColour(i, 1, wx.BLUE)
                            elif int(self.date) - int(inform2[i][1]) == 2:
                                self.SetCellValue(i, 1, inform2[i][0])
                                self.SetCellBackgroundColour(i, 1, wx.GREEN)
                                self.SetCellTextColour(i, 1, (160,32,240))
                            elif int(self.date) - int(inform2[i][1]) >= 3:
                                self.SetCellValue(i, 1, inform2[i][0])
                                self.SetCellBackgroundColour(i, 1, wx.GREEN)
                                self.SetCellTextColour(i, 1, wx.CYAN)
                            else:
                                pass
                        else:
                            pass
                else:
                    pass
                if len(inform3) != 0:
                    for i in range(len(inform3)):
                        if inform3[i][2] == CREATE_CNC:
                            if self.date == inform3[i][1]:
                                self.SetCellValue(i, 2, inform3[i][0])
                                self.SetCellBackgroundColour(i, 2, wx.YELLOW)
                                self.SetCellTextColour(i, 2, wx.BLACK)
                            elif int(self.date) - int(inform3[i][1]) == 1:
                                self.SetCellValue(i, 2, inform3[i][0])
                                self.SetCellBackgroundColour(i, 2, wx.YELLOW)
                                self.SetCellTextColour(i, 2, wx.BLUE)
                            elif int(self.date) - int(inform3[i][1]) == 2:
                                self.SetCellValue(i, 2, inform3[i][0])
                                self.SetCellBackgroundColour(i, 2, wx.YELLOW)
                                self.SetCellTextColour(i, 2, (160,32,240))
                            elif int(self.date) - int(inform3[i][1]) >= 3:
                                self.SetCellValue(i, 2, inform3[i][0])
                                self.SetCellBackgroundColour(i, 2, wx.YELLOW)
                                self.SetCellTextColour(i, 2, wx.CYAN)
                            else:
                                pass
                        elif inform3[i][2] == ALL_WORK_FISHED or inform3[i][2] == DOOR_WORK_FISHED:
                            if self.date == inform3[i][1]:
                                self.SetCellValue(i, 2, inform3[i][0])
                                self.SetCellBackgroundColour(i, 2, wx.GREEN)
                                self.SetCellTextColour(i, 2, wx.BLACK)
                            elif int(self.date) - int(inform3[i][1]) == 1:
                                self.SetCellValue(i, 2, inform3[i][0])
                                self.SetCellBackgroundColour(i, 2, wx.GREEN)
                                self.SetCellTextColour(i, 2, wx.BLUE)
                            elif int(self.date) - int(inform3[i][1]) == 2:
                                self.SetCellValue(i, 2, inform3[i][0])
                                self.SetCellBackgroundColour(i, 2, wx.GREEN)
                                self.SetCellTextColour(i, 2, (160,32,240))
                            elif int(self.date) - int(inform3[i][1]) >= 3:
                                self.SetCellValue(i, 2, inform3[i][0])
                                self.SetCellBackgroundColour(i, 2, wx.GREEN)
                                self.SetCellTextColour(i, 2, wx.CYAN)
                            else:
                                pass
                        else:
                            pass
                else:
                    pass
                if len(inform4) != 0:
                    for i in range(len(inform4)):
                        if inform4[i][2] == CREATE_CNC:
                            if self.date == inform4[i][1]:
                                self.SetCellValue(i, 3, inform4[i][0])
                                self.SetCellBackgroundColour(i, 3, wx.YELLOW)
                                self.SetCellTextColour(i, 3, wx.BLACK)
                            elif int(self.date) - int(inform4[i][1]) == 1:
                                self.SetCellValue(i, 3, inform4[i][0])
                                self.SetCellBackgroundColour(i, 3, wx.YELLOW)
                                self.SetCellTextColour(i, 3, wx.BLUE)
                            elif int(self.date) - int(inform4[i][1]) == 2:
                                self.SetCellValue(i, 3, inform4[i][0])
                                self.SetCellBackgroundColour(i, 3, wx.YELLOW)
                                self.SetCellTextColour(i, 3,(160,32,240))
                            elif int(self.date) - int(inform4[i][1]) >= 3:
                                self.SetCellValue(i, 3, inform4[i][0])
                                self.SetCellBackgroundColour(i, 3, wx.YELLOW)
                                self.SetCellTextColour(i, 3, wx.CYAN)
                            else:
                                pass
                        elif inform4[i][2] == ALL_WORK_FISHED or inform4[i][2] == DOOR_WORK_FISHED:
                            if self.date == inform4[i][1]:
                                self.SetCellValue(i, 3, inform4[i][0])
                                self.SetCellBackgroundColour(i, 3, wx.GREEN)
                                self.SetCellTextColour(i, 3, wx.BLACK)
                            elif int(self.date) - int(inform4[i][1]) == 1:
                                self.SetCellValue(i, 3, inform4[i][0])
                                self.SetCellBackgroundColour(i, 3, wx.GREEN)
                                self.SetCellTextColour(i, 3, wx.BLUE)
                            elif int(self.date) - int(inform4[i][1]) == 2:
                                self.SetCellValue(i, 3, inform4[i][0])
                                self.SetCellBackgroundColour(i, 3, wx.GREEN)
                                self.SetCellTextColour(i, 3,(160,32,240))
                            elif int(self.date) - int(inform4[i][1]) >= 3:
                                self.SetCellValue(i, 3, inform4[i][0])
                                self.SetCellBackgroundColour(i, 3, wx.GREEN)
                                self.SetCellTextColour(i, 3, wx.CYAN)
                            else:
                                pass
                        else:
                            pass
                else:
                    pass
                if len(inform5) != 0:
                    for i in range(len(inform5)):
                        if inform5[i][2] == CREATE_CNC:
                            if self.date == inform5[i][1]:
                                self.SetCellValue(i, 4, inform5[i][0])
                                self.SetCellBackgroundColour(i, 4, wx.YELLOW)
                                self.SetCellTextColour(i, 4, wx.BLACK)
                            elif int(self.date) - int(inform5[i][1]) == 1:
                                self.SetCellValue(i, 4, inform5[i][0])
                                self.SetCellBackgroundColour(i, 4, wx.YELLOW)
                                self.SetCellTextColour(i, 4, wx.BLUE)
                            elif int(self.date) - int(inform5[i][1]) == 2:
                                self.SetCellValue(i, 4, inform5[i][0])
                                self.SetCellBackgroundColour(i, 4, wx.YELLOW)
                                self.SetCellTextColour(i, 4, (160,32,240))
                            elif int(self.date) - int(inform5[i][1]) >= 3:
                                self.SetCellValue(i, 4, inform5[i][0])
                                self.SetCellBackgroundColour(i, 4, wx.YELLOW)
                                self.SetCellTextColour(i, 4, wx.CYAN)
                            else:
                                pass
                        elif inform5[i][2] == ALL_WORK_FISHED or inform5[i][2] == DOOR_WORK_FISHED:
                            if self.date == inform5[i][1]:
                                self.SetCellValue(i, 4, inform5[i][0])
                                self.SetCellBackgroundColour(i, 4, wx.GREEN)
                                self.SetCellTextColour(i, 4, wx.BLACK)
                            elif int(self.date) - int(inform5[i][1]) == 1:
                                self.SetCellValue(i, 4, inform5[i][0])
                                self.SetCellBackgroundColour(i, 4, wx.GREEN)
                                self.SetCellTextColour(i, 4, wx.BLUE)
                            elif int(self.date) - int(inform5[i][1]) == 2:
                                self.SetCellValue(i, 4, inform5[i][0])
                                self.SetCellBackgroundColour(i, 4, wx.GREEN)
                                self.SetCellTextColour(i, 4, (160,32,240))
                            elif int(self.date) - int(inform5[i][1]) >= 3:
                                self.SetCellValue(i, 4, inform5[i][0])
                                self.SetCellBackgroundColour(i, 4, wx.GREEN)
                                self.SetCellTextColour(i, 4, wx.CYAN)
                            else:
                                pass
                        else:
                            pass
                else:
                    pass
                if len(inform6) != 0:
                    for i in range(len(inform6)):
                        if inform6[i][2] == CREATE_CNC:
                            if self.date == inform6[i][1]:
                                self.SetCellValue(i, 5, inform6[i][0])
                                self.SetCellBackgroundColour(i, 5, wx.YELLOW)
                                self.SetCellTextColour(i, 5, wx.BLACK)
                            elif int(self.date) - int(inform6[i][1]) == 1:
                                self.SetCellValue(i, 5, inform6[i][0])
                                self.SetCellBackgroundColour(i, 5, wx.YELLOW)
                                self.SetCellTextColour(i, 5, wx.BLUE)
                            elif int(self.date) - int(inform6[i][1]) == 2:
                                self.SetCellValue(i, 5, inform6[i][0])
                                self.SetCellBackgroundColour(i, 5, wx.YELLOW)
                                self.SetCellTextColour(i, 5,(160,32,240))
                            elif int(self.date) - int(inform6[i][1]) >= 3:
                                self.SetCellValue(i, 5, inform6[i][0])
                                self.SetCellBackgroundColour(i, 5, wx.YELLOW)
                                self.SetCellTextColour(i, 5, wx.CYAN)
                            else:
                                pass
                        elif inform6[i][2] == ALL_WORK_FISHED or inform6[i][2] == DOOR_WORK_FISHED:
                            if self.date == inform6[i][1]:
                                self.SetCellValue(i, 5, inform6[i][0])
                                self.SetCellBackgroundColour(i, 5, wx.GREEN)
                                self.SetCellTextColour(i, 5, wx.BLACK)
                            elif int(self.date) - int(inform6[i][1]) == 1:
                                self.SetCellValue(i, 5, inform6[i][0])
                                self.SetCellBackgroundColour(i, 5, wx.GREEN)
                                self.SetCellTextColour(i, 5, wx.BLUE)
                            elif int(self.date) - int(inform6[i][1]) == 2:
                                self.SetCellValue(i, 5, inform6[i][0])
                                self.SetCellBackgroundColour(i, 5, wx.GREEN)
                                self.SetCellTextColour(i, 5, (160,32,240))
                            elif int(self.date) - int(inform6[i][1]) >= 3:
                                self.SetCellValue(i, 5, inform6[i][0])
                                self.SetCellBackgroundColour(i, 5, wx.GREEN)
                                self.SetCellTextColour(i, 5, wx.CYAN)
                            else:
                                pass
                        else:
                            pass
                else:
                    pass
                if len(inform_error) != 0:
                    for i in range(len(inform_error)):
                        if self.date == inform_error[i][1]:
                            self.SetCellValue(i, 7, inform_error[i][0])
                            self.SetCellBackgroundColour(i, 7, wx.RED)
                            self.SetCellTextColour(i, 7, wx.BLACK)
                        elif int(self.date) - int(inform_error[i][1]) == 1:
                            self.SetCellValue(i, 7, inform_error[i][0])
                            self.SetCellBackgroundColour(i, 7, wx.RED)
                            self.SetCellTextColour(i, 7, wx.BLUE)
                        elif int(self.date) - int(inform_error[i][1]) == 2:
                            self.SetCellValue(i, 7, inform_error[i][0])
                            self.SetCellBackgroundColour(i, 7, wx.RED)
                            self.SetCellTextColour(i, 7, (160,32,240))
                        elif int(self.date) - int(inform_error[i][1]) >= 3:
                            self.SetCellValue(i, 7, inform_error[i][0])
                            self.SetCellBackgroundColour(i, 7, wx.RED)
                            self.SetCellTextColour(i, 7, wx.CYAN)
                        else:
                            pass
                else:
                    pass
            else:
                for i in range(len(self.field_name)):  # 用来填写所有表头信息
                    self.SetColLabelValue(i, self.field_name[i])
        except:
            self.log.WriteText('天外天系统正在运行，在Cnc_Workposition_Right_Grid类MyFresh()方法中出现错误请检查\r\n')
        self.EnableEditing(False)
        self.AutoSizeColumns(False)
        # end_time = datetime.datetime.now()
        # during_time = (end_time - start_time).seconds * 1000 + (end_time - start_time).microseconds / 1000
        # print "时间", during_time
    def SetValue(self,date):#用来接收错传递参数的值
        self.date=date
    def OnLeftClick(self,event):
        row = event.GetRow() # 获得鼠标单击的单元格所在的行
        col = event.GetCol()
        text = self.GetCellValue(row, col)
        if text != '':
            ap_id='WOID_20'+text
            if col==6:
                self.priority_btn.Enable()
                self.Priority_id=ap_id
                # self.production_allocation_btn.Enable()
            elif col==7:
                self.reproduction_btn.Enable()
                self.Reproduction_id=ap_id
            else:
                self.printbarcode_btn.Enable()
                self.printbarcode_id=ap_id
                self.priority_btn.Enable(False)
                self.reproduction_btn.Enable(False)
                # self.production_allocation_btn.Enable(False)
            self.paint.OnPaint(ap_id)
            try:
                if Is_Database_Connect():
                    cursor=DB.cursor()
                    cursor.execute("select `Ap_id`,`Machine_Begin_Time`,`Machine_Finish_Time`,`Operator_id`,`Total_seg`,`Board_Utilization_Ratio`,`State`,`Schedule_date` from `work_cnc_task_list` where Ap_id='%s' "%ap_id)
                    record = cursor.fetchone()
                    # self.Transmitdata(record)
                    ap_id_split=record[0].split('_')
                    self.ap_id.SetValue(str(ap_id_split[1]))
                    self.schedule_date.SetValue(str(record[7]))
                    self.board_utilization_ratio.SetValue(str(record[5]))
                    self.operator_id.SetValue(str(record[3]))
                    self.element_total.SetValue(str(record[4]))
                    if record[6] == ALL_WORK_FISHED:
                        if record[1] != None:
                            startTime = datetime.datetime.strptime(str(record[1].strftime('%Y-%m-%d %H:%M:%S')), "%Y-%m-%d %H:%M:%S")
                            endTime = datetime.datetime.strptime(str(record[2].strftime('%Y-%m-%d %H:%M:%S')), "%Y-%m-%d %H:%M:%S")
                            # 相减得到秒数
                            # seconds = (self.record_data[1] - self.record_data[2]).seconds
                            seconds = (endTime - startTime).seconds
                            minutes = round(seconds / 60.0, 2)  # 保留到小数点后两位
                            self.minutes.SetValue(str(minutes))
                        else:
                            self.log.WriteText("天外天系统正在运行ZX_Pane.py，请检查cnc_task_list表单中接单时间是否为空\r\n")
                    else:
                        minutes = ''
                        self.minutes.SetValue(str(minutes))
            except:
                self.log.WriteText('天外天系统正在运行ZX_Pane.py 获取工位工单表单中信息出现错误，请进行检查  \r\n')
                return
        else:
            self.reproduction_btn.Enable(False)
            self.priority_btn.Enable(False)
            self.printbarcode_btn.Enable(False)
            self.production_allocation_btn.Enable(False)
        event.Skip()
class Cnc_Workposition_Right_Panel(wx.Notebook):
    def __init__(self, parent, id, log):
        wx.Notebook.__init__(self, parent, id, size=(21,21), style=
                             wx.BK_DEFAULT|wx.SUNKEN_BORDER
                             #wx.BK_TOP
                             #wx.BK_BOTTOM
                             #wx.BK_LEFT
                             #wx.BK_RIGHT
                             # | wx.NB_MULTILINE
                             )
        self.log = log
        self.pvc_workposition_right_show1 = Cnc_Workposition_Right_Panel_Workorder(self,self.log)
        # self.pvc_workposition_right_show2 =wx.TextCtrl(self)
        self.pvc_workposition_right_show2 =Cnc_Workposition_Right_Order_TopPanel(self,self.log)
        self.AddPage(self.pvc_workposition_right_show1, "工位工单管理")
        self.AddPage(self.pvc_workposition_right_show2, "工位订单管理")
        # self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        # self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnPageChanging)
    # def OnPageChanged(self, event):
    #     if self:
    #         old = event.GetOldSelection()
    #         new = event.GetSelection()
    #         sel = self.GetSelection()
    #         # self.log.write('OnPageChanged,  old:%d, new:%d, sel:%d\n' % (old, new, sel))
    #     event.Skip()
    # def OnPageChanging(self, event):
    #     if self:
    #         old = event.GetOldSelection()
    #         new = event.GetSelection()
    #         sel = self.GetSelection()
    #     event.Skip()
class Cnc_Workposition_Management_Panel(wx.Panel):
    def __init__(self, parent,log, id=wx.ID_ANY, title="", pos=wx.DefaultPosition,
                 size=(700,650), style=wx.DEFAULT_FRAME_STYLE):
        wx.Panel.__init__(self, parent)
        self._flags = 0
        self.log=log
        self.order_sum = 0
        self.order_area_sum = 0
        self.package_sum = 0
        # self.SetIcon(GetMondrianIcon())
        # self.SetMenuBar(self.CreateMenuBar())
        self._leftWindow1 = wx.adv.SashLayoutWindow(self, 101, wx.DefaultPosition,
                                                wx.Size(230, 1000), wx.NO_BORDER |
                                                wx.adv.SW_3D | wx.CLIP_CHILDREN)
        self._leftWindow1.SetDefaultSize(wx.Size(250, 1000))
        self._leftWindow1.SetOrientation(wx.adv.LAYOUT_VERTICAL)
        self._leftWindow1.SetAlignment(wx.adv.LAYOUT_LEFT)
        self._leftWindow1.SetSashVisible(wx.adv.SASH_RIGHT, True)
        self._leftWindow1.SetExtraBorderSize(10)
        self._pnl = 0
        self.remainingSpace = Cnc_Workposition_Right_Panel(self,-1,self.log)
        self.ID_WINDOW_TOP = 100
        self.ID_WINDOW_LEFT1 = 101
        self.ID_WINDOW_RIGHT1 = 102
        self.ID_WINDOW_BOTTOM = 103
        self._leftWindow1.Bind(wx.adv.EVT_SASH_DRAGGED_RANGE, self.OnFoldPanelBarDrag,
                               id=100, id2=103)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.ReCreateFoldPanel(0)
    def OnSize(self, event):
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.remainingSpace)
        event.Skip()
    def OnQuit(self, event):
        self.Destroy()
    def OnToggleWindow(self, event):
        self._leftWindow1.Show(not self._leftWindow1.IsShown())
        # Leaves bits of itself behind sometimes
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.remainingSpace)
        self.remainingSpace.Refresh()
        event.Skip()
    def OnFoldPanelBarDrag(self, event):

        # if event.GetDragStatus() == wx.SASH_STATUS_OUT_OF_RANGE:
        #     return
        if event.GetId() == self.ID_WINDOW_LEFT1:
            self._leftWindow1.SetDefaultSize(wx.Size(event.GetDragRect().width, 1000))
        # Leaves bits of itself behind sometimes
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.remainingSpace)
        self.remainingSpace.Refresh()
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
        self.cal = CalendarCtrl(item, -1, wx.DateTime().Today(),
                                style=wx.adv.CAL_SEQUENTIAL_MONTH_SELECTION)
        self.cal.Bind(wx.adv.EVT_CALENDAR_SEL_CHANGED, self.OnCalSelChanged)
        self._pnl.AddFoldPanelWindow(item,self.cal,fpb.FPB_ALIGN_WIDTH,0,0)
        self._pnl.AddFoldPanelSeparator(item)
        btn_today = wx.Button(item, wx.ID_ANY, "今天")
        btn_today.Bind(wx.EVT_BUTTON, self.OnTodayQuery)
        self._pnl.AddFoldPanelWindow(item, btn_today)
        btn_yesterday = wx.Button(item, wx.ID_ANY, "昨天")
        btn_yesterday.Bind(wx.EVT_BUTTON, self.OnYesterdayQuery)
        self._pnl.AddFoldPanelWindow(item, btn_yesterday,spacing=0)
        btn_Byesterday = wx.Button(item, wx.ID_ANY, "前天")
        btn_Byesterday.Bind(wx.EVT_BUTTON, self.OnBYesterdayQuery)
        self._pnl.AddFoldPanelWindow(item, btn_Byesterday,spacing=0)
        btn_All = wx.Button(item, wx.ID_ANY, "大前天")
        btn_All.Bind(wx.EVT_BUTTON, self.OnBBYesterdayQuery)
        self._pnl.AddFoldPanelWindow(item, btn_All,spacing=0)
        self._pnl.AddFoldPanelSeparator(item)
    def OnCalSelChanged(self,eve):
        t1 = str(self.cal.GetDate())
        t2 = t1.split(' ')
        t3 = t2[0].split('/')
        t4 = t3[2], t3[0], t3[1]
        dt = ''
        start_time = dt.join(t4)
        start_time1 = '20'+start_time
        if self.remainingSpace.GetSelection() == 0:
            self.remainingSpace.pvc_workposition_right_show1.cnc_workposition_right_grid.SetValue(start_time1)
            self.remainingSpace.pvc_workposition_right_show1.cnc_workposition_right_grid.MyRefresh()
        if self.remainingSpace.GetSelection() == 1:
            self.remainingSpace.pvc_workposition_right_show2.grid.Cnc_Workposition_Order_display(start_time1)
            self.remainingSpace.pvc_workposition_right_show2.tree_panel.TreeCtrl_Refresh(start_time1)
        self.log.WriteText(
            "天外天系统收到操作员控制指令，ZX_Pane.py 开始执行工位工单日期查询操作，日期：" + str(start_time1) +  "\r\n")
    def OnTodayQuery(self,eve):
        today=datetime.date.today().strftime('%Y%m%d')
        if self.remainingSpace.GetSelection() == 0:
            self.remainingSpace.pvc_workposition_right_show1.cnc_workposition_right_grid.SetValue(today)
            self.remainingSpace.pvc_workposition_right_show1.cnc_workposition_right_grid.MyRefresh()
        if self.remainingSpace.GetSelection() == 1:
            self.remainingSpace.pvc_workposition_right_show2.grid.Cnc_Workposition_Order_display(today)
            self.remainingSpace.pvc_workposition_right_show2.tree_panel.TreeCtrl_Refresh(today)
        self.log.WriteText(
            "天外天系统收到操作员控制指令，ZX_Pane.py 开始执行工位工单日期查询操作，日期：" + str(today) + "\r\n")
    def OnYesterdayQuery(self,eve):
        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        yesterday = (today - oneday).strftime('%Y%m%d')
        if self.remainingSpace.GetSelection() == 0:
            self.remainingSpace.pvc_workposition_right_show1.cnc_workposition_right_grid.SetValue(yesterday)
            self.remainingSpace.pvc_workposition_right_show1.cnc_workposition_right_grid.MyRefresh()
        if self.remainingSpace.GetSelection() == 1:
            self.remainingSpace.pvc_workposition_right_show2.grid.Cnc_Workposition_Order_display(yesterday)
            self.remainingSpace.pvc_workposition_right_show2.tree_panel.TreeCtrl_Refresh(yesterday)
        self.log.WriteText(
            "天外天系统收到操作员控制指令，ZX_Pane.py开始执行工位工单日期查询操作，日期：" + str(yesterday) + "\r\n")
    def OnBYesterdayQuery(self,eve):
        today = datetime.date.today()
        twoday = datetime.timedelta(days=2)
        Byesterday = (today - twoday).strftime('%Y%m%d')
        if self.remainingSpace.GetSelection() == 0:
            self.remainingSpace.pvc_workposition_right_show1.cnc_workposition_right_grid.SetValue(Byesterday)
            self.remainingSpace.pvc_workposition_right_show1.cnc_workposition_right_grid.MyRefresh()
        if self.remainingSpace.GetSelection() == 1:
            self.remainingSpace.pvc_workposition_right_show2.grid.Cnc_Workposition_Order_display(Byesterday)
            self.remainingSpace.pvc_workposition_right_show2.tree_panel.TreeCtrl_Refresh(Byesterday)
        self.log.WriteText(
            "天外天系统收到操作员控制指令，ZX_Pane.py开始执行工位工单日期查询操作，日期：" + str(Byesterday) + "\r\n")
    def OnBBYesterdayQuery(self,eve):
        today = datetime.date.today()
        threeday = datetime.timedelta(days=3)
        BByesterday = (today - threeday).strftime('%Y%m%d')
        if self.remainingSpace.GetSelection() == 0:
            self.remainingSpace.pvc_workposition_right_show1.cnc_workposition_right_grid.SetValue(BByesterday)
            self.remainingSpace.pvc_workposition_right_show1.cnc_workposition_right_grid.MyRefresh()
        if self.remainingSpace.GetSelection() == 1:
            self.remainingSpace.pvc_workposition_right_show2.grid.Cnc_Workposition_Order_display(BByesterday)
            self.remainingSpace.pvc_workposition_right_show2.tree_panel.TreeCtrl_Refresh(BByesterday)
        self.log.WriteText(
            "天外天系统收到操作员控制指令，ZX_Pane.py开始执行工位工单日期查询操作，日期：" + str(BByesterday) + "\r\n")
# ---------------------------------------生产调度管理分配机床号对话框
class Production_Scheduling_Allocation_Dialog(wx.Dialog):
    def __init__(self, parent, id, title, size, pos=wx.DefaultPosition,
                 style=wx.DEFAULT_DIALOG_STYLE):
        wx.Dialog.__init__(self)
        self.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        self.Create(parent, id, title, pos, size, style)
        # self.Close(False)
        self.alternative_num = '4'
        sizer = wx.BoxSizer(wx.VERTICAL)
        # self.authority_ctrl_grid = Authority_Ctrl_Grid(self,pos=(5, 5),size=(650, 450))
        if Is_Database_Connect():
            cursor = DB.cursor()
            cursor.execute(
                "select COUNT(*) from `work_cnc_task_list` where `State`='%s' AND `Machine_nums`='%s' " % (0, '4'))
            record = cursor.fetchone()
        else:
            return
        if record[0] == 0:
            message = '当前4号机床待接单工单有0个\r\n无需更换机床！'
            string = wx.StaticText(self, -1, message)
            sizer.Add(string, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        else:
            message = '当前4号机床待接单工单有' + str(record[0]) + '个，请选择备用机床号'
            string = wx.StaticText(self, -1, message)
            label = wx.StaticText(self, -1, "请选择备选机床号：")
            machine_number = ['1号机床', '2号机床', '3号机床', '5号机床', '6号机床']
            Alternative_machine_combox = wx.ComboBox(self, 500, "", (50, 50), (110, -1), machine_number,
                                                     wx.CB_DROPDOWN|wx.CB_READONLY)
            Alternative_machine_combox.Bind(wx.EVT_COMBOBOX, self.SelectMachineNumber)
            hbox = wx.BoxSizer()
            hbox.Add(label, proportion=1, flag=wx.ALL, border=3)
            hbox.Add(Alternative_machine_combox, proportion=1, flag=wx.ALL, border=3)
            btn_ok = wx.Button(self, wx.ID_OK, "确定")
            btn_cancel = wx.Button(self, wx.ID_CANCEL, "取消")
            hbox1 = wx.BoxSizer()
            hbox1.Add(btn_ok, proportion=1, flag=wx.ALL, border=3)
            hbox1.Add(btn_cancel, proportion=1, flag=wx.ALL, border=3)
            # sizer.Add(self.authority_ctrl_grid, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            sizer.Add(string, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            sizer.Add(hbox, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            sizer.Add(hbox1, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.SetSizer(sizer)
        sizer.Fit(self)

    def SelectMachineNumber(self, event):
        machine_name = event.GetString()
        if machine_name == '1号机床':
            self.alternative_num = '1'
        elif machine_name == '2号机床':
            self.alternative_num = '2'
        elif machine_name == '3号机床':
            self.alternative_num = '3'
        elif machine_name == '5号机床':
            self.alternative_num = '5'
        elif machine_name == '6号机床':
            self.alternative_num = '6'
#----------------------------------------------------创建初始界面显示的数据库中等待发货的发货单表格
class Confirm_Delivery_Dialog(wx.Dialog):
    def __init__(
            self, parent, log,id, title,x, delivery_id, operator_id,size,pos=wx.DefaultPosition,
            style=wx.DEFAULT_DIALOG_STYLE, name='确认发货窗口'):
        wx.Dialog.__init__(self)
        self.x=x
        self.delivery_id=delivery_id
        self.log=log
        self.operator_id=operator_id
        self.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        self.Create(parent,id, title, pos, size, style, name)
        # self.Close(False)
        box = wx.BoxSizer(wx.HORIZONTAL)
        self.delivery_tasklist_ID = wx.TextCtrl(self, wx.ID_ANY, size=(100,-1), style=wx.TE_READONLY)
        box.Add(wx.StaticText(self, -1, "发货订单号:"), 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        box.Add(self.delivery_tasklist_ID, 0, wx.ALIGN_RIGHT|wx.ALL, 5)
        if self.x=='1':
            self.confirm_delivery = Confirm_Delivery_Grid(self, self.log, pos=(5, 5), size=(650, 450))
            btnsizer = wx.BoxSizer()
            btn_print = wx.Button(self, wx.ID_OK, "打印发货单")
            btn_cancel = wx.Button(self, wx.ID_CANCEL, "取消发货")
            btnsizer.Add(btn_print, proportion=1, flag=wx.ALL, border=3)
            btnsizer.Add(btn_cancel, proportion=1, flag=wx.ALL, border=3)
            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            sizer.Add(self.confirm_delivery, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        elif self.x=='2':
            self.confirm_delivery = Confirm_Delivery_Query_Grid(self, self.log,self.delivery_id, pos=(5, 5), size=(650, 450))
            btnsizer=wx.BoxSizer()
            btn_print = wx.Button(self, wx.ID_OK, "重新打印发货单")
            btn_check = wx.Button(self,-1, "取消发货")
            btn_cancel = wx.Button(self, wx.ID_CANCEL, "关闭")
            btnsizer.Add(btn_print, proportion=1, flag=wx.ALL, border=3)
            btnsizer.Add(btn_check, proportion=1, flag=wx.ALL, border=3)
            btnsizer.Add(btn_cancel, proportion=1, flag=wx.ALL, border=3)
            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            sizer.Add(self.confirm_delivery, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            # self.SetSizer(sizer)
            # sizer.Fit(self)
            self.Bind(wx.EVT_BUTTON, self.On_btn_check, btn_check)
        self.SetSizer(sizer)
        sizer.Fit(self)
    def On_btn_check(self,eve):
        today = datetime.datetime.now()
        dlg = wx.MessageDialog(self, '此发货单已被打印，取消此单将会影响正常发货，请确认是否取消此单',
                               '警告！',
                               wx.OK | wx.ICON_INFORMATION | wx.CANCEL
                               # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                               )
        val=dlg.ShowModal()
        if val == wx.ID_OK:
            try:
                if Is_Database_Connect():
                    cursor = DB.cursor()
                    cursor.execute(
                        "UPDATE `delivery_form_zx` set `State`='%s',`Cancel_date`='%s',`Cancel_operator`='%s' WHERE (`State`='%s' AND  `Delivery_ID`='%s')" % (
                            '已取消',today,self.operator_id, '等待发货', self.delivery_id))
                    DB.commit()
                    cursor.execute(
                        "SELECT `Order_id`,`Contract_id` FROM `order_order_online` WHERE `Order_delivery_num`='%s'" % self.delivery_id)
                    order_num_record = cursor.fetchall()
                    for i in range(len(order_num_record)):
                        cursor.execute(
                            "UPDATE `order_order_online` set `Order_delivery_num`='%s', `Delievery_schedule_operator_id`='%s',`Delievery_schedule_time`='%s',`State`='%s' WHERE `Order_id`='%s'" % (
                                '', self.operator_id, today, WAIT_DELIVERY, order_num_record[i][0]))
                        cursor = DB.cursor()
                        cursor.execute(
                            "UPDATE `order_element_online` set `Delievery_schedule_operator_id`='%s',`Delievery_schedule_time`='%s',`State`='%s'WHERE `Order_id`='%s'" % (
                                self.operator_id, today, WAIT_DELIVERY, order_num_record[i][0]))
                        cursor = DB.cursor()
                        cursor.execute(
                            "UPDATE `order_part_online` set `Delievery_schedule_operator_id`='%s', `Delievery_schedule_time`='%s', `State`='%s' WHERE `Order_id`='%s'" % (
                                self.operator_id, today, WAIT_DELIVERY, order_num_record[i][0]))
                        cursor = DB.cursor()
                        cursor.execute(
                            "UPDATE `order_section_online` set `Delievery_schedule_operator_id`='%s', `Delievery_schedule_time`='%s', `State`='%s' WHERE `Order_id`='%s'" % (
                                self.operator_id, today, WAIT_DELIVERY, order_num_record[i][0]))
                        cursor = DB.cursor()
                        cursor.execute("UPDATE `order_contract_internal` set `State`='%s' WHERE `Contract_id`='%s'" % ( WAIT_DELIVERY, order_num_record[i][1]))
                    DB.commit()  # DB.commit()将这条语句放在for循环外面一块提会使程序运行变快。
                    dlg.Destroy()
            except:
                self.log.WriteText('天外天系统正在响应 ZX_Pane.py 中 On_btn_check事件，进行数据库的更新操作时出现错误，请检查更新语句是否正确     \r\n')
                return
        else:
            self.log.WriteText('天外天系统正在响应 ZX_Pane.py 中 On_btn_check事件，操作员取消此次操作     \r\n')
        self.Destroy()
class Order_Query_Table(gridlib.GridTableBase):
    def __init__(self, data, field_name):
        gridlib.GridTableBase.__init__(self)
        self.data = data
        self.field_name = field_name
        self.dataTypes = [
            gridlib.GRID_VALUE_STRING,
            gridlib.GRID_VALUE_NUMBER,
            gridlib.GRID_VALUE_FLOAT + ':6,2',
            gridlib.GRID_VALUE_NUMBER,
            gridlib.GRID_VALUE_STRING,
            gridlib.GRID_VALUE_DATETIME,
            gridlib.GRID_VALUE_STRING,
            gridlib.GRID_VALUE_DATETIME,
            gridlib.GRID_VALUE_STRING,
            gridlib.GRID_VALUE_STRING,
            gridlib.GRID_VALUE_STRING,
            gridlib.GRID_VALUE_STRING,
        ]

    # --------------------------------------------------
    # required methods for the wxPyGridTableBase interface
    def GetNumberRows(self):
        return len(self.data)

    def GetNumberCols(self):
        return len(self.field_name)

    def IsEmptyCell(self, row, col):
        try:
            return not self.data[row][col]
        except IndexError:
            return True

    def GetValue(self, row, col):
        try:
            return self.data[row][col]
        except IndexError:
            return ''


    def DeleteRows(self, pos=0, numRows=1):  # real signature unknown; restored from __doc__
        """
        DeleteRows(pos=0, numRows=1) -> bool

        Delete rows from the table.
        """
        if self.data is None or len(self.data) == 0:
            return False
        for rowNum in range(0,numRows):
            self.data.remove(self.data[numRows-1-pos-rowNum])
        gridView=self.GetView()
        gridView.BeginBatch()
        deleteMsg=wx.grid.GridTableMessage(self,wx.grid.GRIDTABLE_NOTIFY_ROWS_DELETED,pos,numRows)
        gridView.ProcessTableMessage(deleteMsg)
        gridView.EndBatch()
        getValueMsg=wx.grid.GridTableMessage(self,wx.grid.GRIDTABLE_REQUEST_VIEW_GET_VALUES)
        gridView.ProcessTableMessage(getValueMsg)
        # if self.onGridValueChanged:
        #     self.onGridValueChanged()
        return True
    # def DeleteRows(*args, **kwargs):
    #     """DeleteRows(self, size_t pos=0, size_t numRows=1) -> bool"""
    #     return _grid.GridTableBase_DeleteRows(*args, **kwargs)
    #


    def SetValue(self, row, col, value):
        def innerSetValue(row, col, value):
            try:
                self.data[row][col] = value
            except IndexError:
                # add a new row
                self.data.append([''] * self.GetNumberCols())
                innerSetValue(row, col, value)

        innerSetValue(row, col, value)

    # --------------------------------------------------
    # Some optional methods
    def GetColLabelValue(self, col):
        return self.field_name[col]

    def GetTypeName(self, row, col):
        return self.dataTypes[col]

    def CanGetValueAs(self, row, col, typeName):
        colType = self.dataTypes[col].split(':')[0]
        if typeName == colType:
            return True
        else:
            return False
    def CanSetValueAs(self, row, col, typeName):
        return self.CanGetValueAs(row, col, typeName)
class Order_Query_Grid(gridlib.Grid):
    def __init__(self, parent, log,operator_id,delivery_order_count_sum,order_count_sum,package_count_sum,delivery_area_sum,completed_delivery_PDF):
        gridlib.Grid.__init__(self, parent, -1)
        self.log = log
        self.operator_id=operator_id
        self.completed_delivery_PDF=completed_delivery_PDF
        self.delivery_order_count_sum=delivery_order_count_sum
        self.order_count_sum=order_count_sum
        self.package_count_sum=package_count_sum
        self.delivery_area_sum=delivery_area_sum
        self.data = []
        self.delivery_sum = 0
        self.order_sum = 0
        self.order_area_sum = 0
        self.package_sum = 0
        self.field_name = ['发货单号', '订单总数', '总面积', '总件数', '制单日期', '制单人', '发货日期', '发货人', '发货单状态', '取消日期', '取消人']
        self.state = '1'
        self.begin_time = '从:'
        self.end_time = '至:'
        #-------------------------------关闭一开始初始界面的显示，当触发属性页改变事件时再调用刷新函数显示表格
        # self.MyRefresh()
        # self.table = Order_Query_Table(self.data, self.field_name)  # 自定义表网格
        # self.SetTable(self.table, True)
        self.SetRowLabelSize(0)
        self.SetMargins(0, 0)
        self.AutoSizeColumns(False)
        self.DisableDragColSize()# 使单元格不可拖拽
        self.DisableDragRowSize()
        self.Bind(gridlib.EVT_GRID_CELL_LEFT_DCLICK, self.OnLeftDClick)# 绑定单元格双击事件
        self.EnableEditing(False)  # 使得整个表格都不使能
        self.timer = wx.PyTimer(self.MyRefresh)
        self.timer.Start(30000)
    def MyRefresh(self):
        data = []
        self.delivery_sum=0
        self.order_sum = 0
        self.order_area_sum = 0
        self.package_sum = 0
        try:
            if Is_Database_Connect():
                cursor = DB1.cursor()
                staff_inform = {}
                cursor.execute("select `Job_id` ,`Name` from `info_staff_new` where `Position`='%s' or `Position`='%s'"%(MANAGEMENT_POSITION,DELIVERY_POSITION))
                record = cursor.fetchall()
                for i in range(len(record)):
                    staff_inform[record[i][0]] = record[i][1]
                if self.state == '1':
                    cursor = DB.cursor()
                    cursor.execute(
                        "select `Delivery_ID`,`Order_amount`,`Delivery_total_area`,`Package_amount`,`Creat_date`,`Creator`,`Delivery_date`,`Delivery_operator`,`State`,`Cancel_date`,`Cancel_operator` from `delivery_form_zx` where 1 ORDER BY `Creat_date` DESC")
                    self.record = cursor.fetchall()
                    if self.record is not None:
                        for i in range(len(self.record)):
                            if self.record[i][5] == '0':
                                creator_name = '管理员'
                            else:
                                creator_name = staff_inform[self.record[i][5]]
                            if self.record[i][7] == '0':
                                delivery_name = '管理员'
                            elif self.record[i][7] != None:
                                delivery_name = staff_inform[self.record[i][7]]
                            else:
                                delivery_name=''
                            if self.record[i][10] == '0':
                                cancel_name = '管理员'
                            elif self.record[i][10] != None:
                                cancel_name = staff_inform[self.record[i][10]]
                            else:
                                cancel_name=''
                            if self.record[i][4].strftime('%Y%m%d') >= self.begin_time and self.record[i][4].strftime(
                                    '%Y%m%d') <= self.end_time:
                                inform = [self.record[i][0], self.record[i][1], self.record[i][2], self.record[i][3],
                                          self.record[i][4].strftime('%Y-%m-%d'),
                                          creator_name, self.record[i][6], delivery_name,
                                          self.record[i][8],self.record[i][9],cancel_name]
                                data.append(inform)
                                self.order_sum += int(self.record[i][1])
                                self.order_area_sum += int(self.record[i][2])
                                self.package_sum += int(self.record[i][3])
                            elif self.begin_time == '从:' or self.end_time == '至:':
                                inform = [self.record[i][0], self.record[i][1], self.record[i][2], self.record[i][3],
                                          self.record[i][4].strftime('%Y-%m-%d'),creator_name, self.record[i][6], delivery_name,
                                          self.record[i][8],self.record[i][9],cancel_name]
                                data.append(inform)
                                self.order_sum += int(self.record[i][1])
                                self.order_area_sum += int(self.record[i][2])
                                self.package_sum += int(self.record[i][3])
                    else:
                        pass
                    self.delivery_sum = len(data)
                    # self.remainingSpace.query_managment_grid.Refresh_Query(data)
                else:
                    cursor = DB.cursor()
                    cursor.execute(
                        "select `Delivery_ID`,`Order_amount`,`Delivery_total_area`,`Package_amount`,`Creat_date`,`Creator`,`Delivery_date`,`Delivery_operator`,`State`,`Cancel_date`,`Cancel_operator` from `delivery_form_zx` where `State`='%s' ORDER BY `Creat_date` DESC" % self.state)
                    self.record = cursor.fetchall()
                    if self.record is not None:
                        for i in range(len(self.record)):
                            if self.record[i][5] == '0':
                                creator_name = '管理员'
                            elif staff_inform.has_key(self.record[i][5]):
                                creator_name = staff_inform[self.record[i][5]]
                            else:
                                creator_name =''
                            if self.record[i][7] == '0':
                                delivery_name = '管理员'
                            elif self.record[i][7] != None:
                                delivery_name = staff_inform[self.record[i][7]]
                            else:
                                delivery_name=''
                            if self.record[i][10] == '0':
                                cancel_name = '管理员'
                            elif staff_inform.has_key(self.record[i][10]):
                                cancel_name = staff_inform[self.record[i][10]]
                            else:
                                cancel_name=''
                            if self.record[i][4].strftime('%Y%m%d') >= self.begin_time and self.record[i][4].strftime(
                                    '%Y%m%d') <= self.end_time:
                                inform = [self.record[i][0], self.record[i][1], self.record[i][2], self.record[i][3],
                                          self.record[i][4].strftime('%Y-%m-%d'),
                                          creator_name, self.record[i][6], delivery_name,
                                          self.record[i][8],self.record[i][9],cancel_name]
                                data.append(inform)
                                self.order_sum += int(self.record[i][1])
                                self.order_area_sum += int(self.record[i][2])
                                self.package_sum += int(self.record[i][3])
                            elif self.begin_time == '从:' or self.end_time == '至:':
                                inform = [self.record[i][0], self.record[i][1], self.record[i][2], self.record[i][3],
                                          self.record[i][4].strftime('%Y-%m-%d'),
                                          creator_name, self.record[i][6], delivery_name,
                                          self.record[i][8],self.record[i][9],cancel_name]
                                data.append(inform)
                                self.order_sum += int(self.record[i][1])
                                self.order_area_sum += int(self.record[i][2])
                                self.package_sum += int(self.record[i][3])
                    else:
                        pass
                    self.delivery_sum = len(data)
                self.table = Order_Query_Table(data, self.field_name)  # 自定义表网格
                self.SetTable(self.table, True)
                # print 'test',self.table.data
                # for i in range(len(data)):
                #     print 'test1',self.table.data[i][8]
                self.AutoSizeColumns(False)
                self.DisableDragColSize()
                self.DisableDragRowSize()
                self.EnableEditing(False)
            else:
                return
            self.delivery_order_count_sum.SetValue(str(self.delivery_sum))
            self.order_count_sum.SetValue(str(self.order_sum))
            self.package_count_sum.SetValue(str(self.package_sum))
            self.delivery_area_sum.SetValue(str(self.order_area_sum))
        except:
            self.log.WriteText('天外天系统正在运行ZX_Pane.py查询发货单表格更新函数，出现错误，请检查  \r\n')
    def OnLeftDClick(self, eve):
        row = eve.GetRow()  # 获得鼠标单击的单元格所在的行
        self.text = self.GetCellValue(row, 0)
        self.text_state = self.GetCellValue(row, 8)
        try:
            if self.text_state == '等待发货':
                dlg = Confirm_Delivery_Dialog(self, self.log, -1, "确认发货窗口", '2', self.text, self.operator_id,size=(800, 600),
                                              pos=wx.DefaultPosition,
                                              style=wx.DEFAULT_DIALOG_STYLE, name='确认发货窗口')  # 将对话框类实例化
                dlg.delivery_tasklist_ID.SetValue(self.text)  # 将发货单号写进对话框中的静态文本框中
                dlg.CenterOnScreen()
                val = dlg.ShowModal()
                if val == wx.ID_OK:  # 类似于绑定事件，将参数传到pdf类
                    print_data = dlg.confirm_delivery.Return_Data()
                    print_delivery_code = dlg.confirm_delivery.Return_delivery_code()
                    self.print_delivery_form = Print_Delivery_Form(self, -1, print_data, print_delivery_code)
                    self.print_delivery_form.Show(True)  # frame有Show属性。
                    self.MyRefresh()
                    self.log.WriteText('天外天系统进行确认重新打印发货单操作   \r\n')
                elif val == wx.ID_CANCEL:
                    self.Refresh()
                    self.log.WriteText('天外天系统进行取消重新打印发货单操作   \r\n')
                dlg.Destroy()
            elif self.text_state == '已发货' or self.text_state == '发货中':
                try:
                    self.completed_delivery_PDF.DrawTable_PDF(self.text)
                except:
                    self.log.WriteText("天外天程序正在运行ZX_Pane.py Order_Query_Grid() OnLeftDClick()未找到已生成发货单路径，请进行检查\r\n")
            elif self.text_state == '已取消':
                dlg = wx.MessageDialog(self, '此发货单已被取消！',
                                       '警告',
                                       wx.OK | wx.ICON_INFORMATION
                                       # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                                       )
                dlg.ShowModal()
                dlg.Destroy()
        except:
            self.log.WriteText('天外天系统正在ZX_Pane.py中响应鼠标左键双击事件，出现错误   请检查往对话框中所传入的参数是否正确  \r\n')
    def SetValue(self, begin_time, end_time, state):
        self.begin_time=begin_time
        self.end_time=end_time
        self.state=state
class Confirm_Delivery_Query_Grid(gridlib.Grid):
    def __init__(self, parent,log,delivery_id,pos,size):
        gridlib.Grid.__init__(self, parent, -1,pos,size)
        self.log=log
        self.data = []
        self.information=[]
        self.delivery_id=delivery_id
        self.field_name = ['货运公司','品牌','订单编号','打包包数','收货人电话','发货编号','收货信息']
        try:
            if Is_Database_Connect():
                cursor = DB.cursor()
                cursor.execute(
                        "select `Transport_company`,`Brand`,`Order_id`,`Package_num_hcj`,`Order_delivery_num` from `order_order_online` where`Order_delivery_num`='%s'" %
                            (str(self.delivery_id)))
                self.record = cursor.fetchall()
                if self.record==() or self.record==None:
                    self.data = []
                else:
                    for i in range(len(self.record)):
                        cursor = DB.cursor()
                        cursor.execute(
                            "select `Contract_id` from `order_order_online` where Order_id='%s' ORDER BY `Receive_time`" % self.record[i][2])
                        contract_record = cursor.fetchone()
                        cursor.execute(
                            "select `Customer_name`,`Customer_tel`,`Payment_method` from `order_contract_internal` where Contract_id='%s'"
                            % contract_record[0])
                        address_record = cursor.fetchone()
                        # if address_record[2]==() or address_record[2]==None:
                        #     self.log.WriteText("天外天系统正在 ZX_Pane.py 进行获取门店地址和电话操作，该条订单对应合同号在order_contract_internal中无记录 \r\n")
                        if address_record[2]==10 or address_record[2]==5:
                            inform = [self.record[i][0], self.record[i][1], self.record[i][2], self.record[i][3], address_record[1], self.record[i][4],
                                      address_record[0]]
                            self.data.append(inform)
                        else:
                            pass
            else:
                return
            self.table = Confirm_Delivery_Table(self.data, self.field_name)  # 自定义表网格
            self.SetTable(self.table, True)
            self.SetRowLabelSize(0)
            self.SetMargins(0, 0)
            self.AutoSizeColumns(False)
            self.DisableDragColSize()
            self.DisableDragRowSize()
            self.EnableEditing(False)
            # self.timer= wx.PyTimer(self.Refresh)
            # self.timer.Start(5000)
        except:
            self.log.WriteText(
                '天外天系统正在ZX_Pane.py进行Confirm_Delivery_Query_Grid获取数据库中相应发货单号的订单操作时，出现错误，请检查order_order_online中订单的发货编号是否存在   \r\n')
    def Return_Data(self):
        delivery_data=[]
        try:
            for i in range(len(self.data)):
                # imagewriter = ImageWriter()
                # cd39_i = Code39(str(self.data[i][2]), writer=imagewriter, add_checksum=False)
                # cd39_i.save(opj('bitmaps/code_image'+str(i)))
                # code_img_i = Image(opj('bitmaps/code_image'+str(i)+'.png'))
                # code_img_i.drawHeight = 60
                # code_img_i.drawWidth = 120
                code_img_i=exe_Barcode(self.data[i][2])
                # address=self.data[i][6].split("·")
                row_delivery_data=[self.data[i][0],self.data[i][1],str(self.data[i][2]),str(self.data[i][3]),str(self.data[i][4]),self.data[i][6],code_img_i]
                delivery_data.append(row_delivery_data)
            return delivery_data
        except:
            self.log.WriteText("天外天系统正在 ZX_Pane.py 执行Return_Data方法，出现错误，请核对编码数据是否为订单的发货编号，或者数据库中数据类型是否为字符串型，或者address[3]是否为空，从而导致不能进行类型转换操作   \r\n")
    def Return_delivery_code(self):
        return self.delivery_id
class Completed_delivery_PDF(wx.Panel):
    def __init__(self, parent, log):
        wx.Panel.__init__(self, parent, -1)
        self.log = log
        vsizer = wx.BoxSizer(wx.VERTICAL)
        self.buttonpanel = pdfButtonPanel(self, wx.ID_ANY,wx.DefaultPosition, wx.DefaultSize, 0)
        vsizer.Add(self.buttonpanel, 0,wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT | wx.TOP, 5)
        self.viewer = pdfViewer(self, wx.ID_ANY, wx.DefaultPosition,
                                wx.DefaultSize, wx.HSCROLL | wx.VSCROLL | wx.SUNKEN_BORDER)
        vsizer.Add(self.viewer, 1, wx.GROW | wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)
        self.SetSizer(vsizer)
        self.SetAutoLayout(True)
        self.buttonpanel.viewer = self.viewer
        self.viewer.buttonpanel = self.buttonpanel
        wx.BeginBusyCursor()
        wx.EndBusyCursor()
        # self.viewer.LoadFile("D:\delivery_list_history\\" + str(print_delivery_code) + '.pdf')
    def DrawTable_PDF(self,print_delivery_code):
        try:
            f = os.path.exists("C:\delivery_list_history\\")  # 用于判断在C盘中是否存在delivery_list_history文件夹，如果不在在这个路径下新建文件夹。
            if not f:
                os.mkdir("C:\delivery_list_history\\")  # 新建文件夹
            filename_server_name = u"\\\\192.168.31.250\\delivery_list_history\\" + str(print_delivery_code) + '.pdf'
            filename_local_name = u"C:\\delivery_list_history\\" + str(print_delivery_code) + '.pdf'
            is_exist_file = os.path.exists("\\\\192.168.31.250\\delivery_list_history\\" + str(print_delivery_code) + '.pdf')
            if is_exist_file:
                shutil.copyfile(filename_server_name, filename_local_name)
                self.viewer.LoadFile("C:\\delivery_list_history\\" + str(print_delivery_code) + '.pdf')
            else:
                self.log.WriteText("天外天程序正在运行ZX_Pane.py   Completed_delivery_PDF 不存在请检查 \r\n")
            # self.viewer.LoadFile("C:\delivery_list_history\\" + str(print_delivery_code) + '.pdf')
        except:
            self.log.WriteText(
                "天外天程序正在运行ZX_Pane.py   Completed_delivery_PDF 加载发货单时 报错，请检查是否存在 \r\n")
#-------------------------------------------------------弹出的对话框
class ZX_Order_Query_Panel(wx.Panel):
    def __init__(self,parent,log,operator_id,completed_delivery_PDF):
        wx.Panel.__init__(self, parent, -1,style=wx.SUNKEN_BORDER)
        self.log=log
        # self.completed_delivery_PDF=completed_delivery_PDF
        delivery_order_count_sum = wx.TextCtrl(self, wx.ID_ANY, size=(60, 20), style=wx.TE_READONLY)
        order_count_sum = wx.TextCtrl(self, wx.ID_ANY, size=(60, 20), style=wx.TE_READONLY)
        package_count_sum = wx.TextCtrl(self, wx.ID_ANY, size=(60, 20), style=wx.TE_READONLY)
        delivery_area_sum = wx.TextCtrl(self, wx.ID_ANY, size=(60, 20), style=wx.TE_READONLY)
        self.query_managment_grid=Order_Query_Grid(self,self.log,operator_id,delivery_order_count_sum,order_count_sum,package_count_sum,delivery_area_sum,completed_delivery_PDF)
        label1 = wx.StaticText(self, -1, "界面中发货单数")
        label2 = wx.StaticText(self, -1, "界面订单总数")
        label3 = wx.StaticText(self, -1, "界面中打包总件数")
        label4 = wx.StaticText(self, -1, "界面中发货面积")

        self.xbox1 = wx.BoxSizer()
        self.xbox1.Add(label1, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        self.xbox1.Add(delivery_order_count_sum, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        self.xbox2 = wx.BoxSizer()
        self.xbox2.Add(label2, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        self.xbox2.Add(order_count_sum, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        self.xbox3 = wx.BoxSizer()
        self.xbox3.Add(label3, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        self.xbox3.Add(package_count_sum, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        self.xbox4 = wx.BoxSizer()
        self.xbox4.Add(label4, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        self.xbox4.Add(delivery_area_sum, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        self.staticbox_query = wx.StaticBox(self, -1)
        self.staticboxsizer_query1 = wx.StaticBoxSizer(self.staticbox_query, wx.HORIZONTAL)
        self.staticboxsizer_query1.Add(self.xbox1, proportion=1, flag=wx.EXPAND, border=3)
        self.staticboxsizer_query1.Add(self.xbox2, proportion=1, flag=wx.EXPAND, border=3)
        self.staticboxsizer_query1.Add(self.xbox3, proportion=1, flag=wx.EXPAND, border=3)
        self.staticboxsizer_query1.Add(self.xbox4, proportion=1, flag=wx.EXPAND, border=3)
        self.vbox1 = wx.BoxSizer(wx.VERTICAL)
        self.vbox1.Add(self.staticboxsizer_query1, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        self.vbox1.Add(self.query_managment_grid, proportion=1, flag=wx.EXPAND | wx.ALL, border=3)
        self.SetSizer(self.vbox1)
        # self.timer = wx.PyTimer(self.Refresh_Static_date)
        # self.timer.Start(45000)
class Delivery_Search_Panel(wx.Panel):
    def __init__(self, parent,log, id=wx.ID_ANY, title="", pos=wx.DefaultPosition,
                 size=(700,650), style=wx.DEFAULT_FRAME_STYLE):
        wx.Panel.__init__(self, parent)
        self._flags = 0
        self.log = log
        self.operator_id = '0'
        self.id_state=''
        self.begin_time = '从:'
        self.end_time = '至:'
        self.state='1'
        self._leftWindow1 = wx.adv.SashLayoutWindow(self, 101, wx.DefaultPosition,
                                                wx.Size(200, 1000), wx.NO_BORDER |
                                                wx.adv.SW_3D | wx.CLIP_CHILDREN)
        self._leftWindow1.SetDefaultSize(wx.Size(220, 1000))
        self._leftWindow1.SetOrientation(wx.adv.LAYOUT_VERTICAL)
        self._leftWindow1.SetAlignment(wx.adv.LAYOUT_LEFT)
        self._leftWindow1.SetSashVisible(wx.adv.SASH_RIGHT, True)
        self._leftWindow1.SetExtraBorderSize(10)
        self._pnl = 0
        self._leftWindow2 = wx.adv.SashLayoutWindow(self, 102, wx.DefaultPosition,
                                                    wx.Size(200, 1000), wx.NO_BORDER |
                                                    wx.adv.SW_3D | wx.CLIP_CHILDREN)
        self._leftWindow2.SetDefaultSize(wx.Size(500, 1000))
        self._leftWindow2.SetOrientation(wx.adv.LAYOUT_VERTICAL)
        self._leftWindow2.SetAlignment(wx.adv.LAYOUT_RIGHT)
        self._leftWindow2.SetSashVisible(wx.adv.SASH_LEFT, True)
        self._leftWindow2.SetExtraBorderSize(10)
        self._pnl = 0
        # self.remainingSpace = ZX_Order_Query_Panel(self,log,self.operator_id)
        self._leftWindow1.Bind(wx.adv.EVT_SASH_DRAGGED_RANGE, self.OnFoldPanelBarDrag,
                               id=100, id2=103)
        self._leftWindow2.Bind(wx.adv.EVT_SASH_DRAGGED_RANGE, self.OnFoldPanelBarDrag,
                               id=100, id2=103)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.ReCreateFoldPanel(0)
        self.OnPDFShow()
        self.remainingSpace = ZX_Order_Query_Panel(self,log, self.operator_id,self.completed_delivery_PDF)
        today = datetime.date.today().strftime('%Y%m%d')
        self.remainingSpace.query_managment_grid.SetValue(today, today, '1')
        self.remainingSpace.query_managment_grid.MyRefresh()
    def OnSize(self, event):
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.remainingSpace)
        event.Skip()
    def OnQuit(self, event):
        self.Destroy()
    def OnToggleWindow(self, event):
        self._leftWindow1.Show(not self._leftWindow1.IsShown())
        self._leftWindow2.Show(not self._leftWindow2.IsShown())
        # Leaves bits of itself behind sometimes
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.remainingSpace)
        self.remainingSpace.Refresh()
        event.Skip()
    def OnFoldPanelBarDrag(self, event):
        if event.GetId() == 101:
            self._leftWindow1.SetDefaultSize((event.GetDragRect().width, 1000))
        if event.GetId() == 102:
            self._leftWindow2.SetDefaultSize((event.GetDragRect().width, 1000))
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.remainingSpace)
        self.remainingSpace.Refresh()
        event.Skip()
    def ReCreateFoldPanel(self, fpb_flags):
        self._leftWindow1.DestroyChildren()
        self._pnl = fpb.FoldPanelBar(self._leftWindow1, -1, wx.DefaultPosition,
                                     wx.Size(-1,-1), agwStyle=fpb_flags)
        Images = wx.ImageList(16,16)
        Images.Add(GetExpandedIconBitmap())
        Images.Add(GetCollapsedIconBitmap())
        item = self._pnl.AddFoldPanel("按日期查询", collapsed=False,
                                      foldIcons=Images)
        self.date_start=wx.DateTimeFromDMY  #canlander日历的起始时间获得
        self.date_end=wx.DateTimeFromDMY   #canlander日历的截至时间获得
        self.calendar_begin=PopDateControl(item, -1)
        self.calendar_begin.textCtrl.SetValue("从:")
        self._pnl.AddFoldPanelWindow(item,self.calendar_begin,fpb.FPB_ALIGN_WIDTH,2,20)
        self.calendar_end=PopDateControl(item, -1)
        self.calendar_end.textCtrl.SetValue("至:")
        self._pnl.AddFoldPanelWindow(item,self.calendar_end,fpb.FPB_ALIGN_WIDTH,2,20)
        btn_date_start=wx.Button(item, wx.ID_ANY, "开始日期查询")
        self._pnl.AddFoldPanelWindow(item, btn_date_start)
        btn_date_start.Bind(wx.EVT_BUTTON,self.onDateStart)
        # self._pnl.AddFoldPanelSeparator(item)#设置分割线
        self.radio5 = wx.RadioButton(item, ID_TODAY, "&今天")
        self.radio5.Bind(wx.EVT_RADIOBUTTON, self.OnToday)
        self._pnl.AddFoldPanelWindow(item, self.radio5, fpb.FPB_ALIGN_WIDTH, fpb.FPB_DEFAULT_SPACING, 10)
        self.radio6 = wx.RadioButton(item, ID_YESTERDAY, "&昨天")
        self.radio6.Bind(wx.EVT_RADIOBUTTON, self.OnYesterday)
        self._pnl.AddFoldPanelWindow(item, self.radio6, fpb.FPB_ALIGN_WIDTH, fpb.FPB_DEFAULT_SPACING, 10)
        self.radio7 = wx.RadioButton(item, ID_BYESTERDAY, "&前天")
        self.radio7.Bind(wx.EVT_RADIOBUTTON, self.OnBYesterday)
        self._pnl.AddFoldPanelWindow(item, self.radio7, fpb.FPB_ALIGN_WIDTH, fpb.FPB_DEFAULT_SPACING, 10)
        # self._pnl.AddFoldPanelSeparator(item)
        self._single = wx.RadioButton(item, ID_All_TIME, "&查看全部时间")
        self._single.Bind(wx.EVT_RADIOBUTTON, self.OnAllTime)
        self._pnl.AddFoldPanelWindow(item, self._single, fpb.FPB_ALIGN_WIDTH,
                                     fpb.FPB_DEFAULT_SPACING, 10)
        item = self._pnl.AddFoldPanel("按发货单状态查询", False, foldIcons=Images)
        self.radio1 = wx.RadioButton(item, ID_WAIT_DELIVERY, "&等待发货")
        self.radio1.Bind(wx.EVT_RADIOBUTTON, self.OnWaitDelivery)
        self._pnl.AddFoldPanelWindow(item, self.radio1, fpb.FPB_ALIGN_WIDTH, fpb.FPB_DEFAULT_SPACING, 10)
        self.radio2 = wx.RadioButton(item, ID_DELIVERYING, "&发货中")
        self.radio2.Bind(wx.EVT_RADIOBUTTON, self.OnDeliverying)
        self._pnl.AddFoldPanelWindow(item, self.radio2, fpb.FPB_ALIGN_WIDTH, fpb.FPB_DEFAULT_SPACING, 10)
        self.radio3 = wx.RadioButton(item, ID_COMPLATE_DELIVERY, "&已发货")
        self.radio3.Bind(wx.EVT_RADIOBUTTON, self.OnComplateDelivery)
        self._pnl.AddFoldPanelWindow(item, self.radio3, fpb.FPB_ALIGN_WIDTH, fpb.FPB_DEFAULT_SPACING, 10)
        self.radio4 = wx.RadioButton(item, ID_CANCEL_DELIVERY, "&已取消")
        self.radio4.Bind(wx.EVT_RADIOBUTTON, self.OnCancelDelivery)
        self._pnl.AddFoldPanelWindow(item, self.radio4, fpb.FPB_ALIGN_WIDTH, fpb.FPB_DEFAULT_SPACING, 10)
        # self._pnl.AddFoldPanelSeparator(item)
        self._single1 = wx.RadioButton(item, ID_All_STATE, "&查看全部状态")
        self._single1.Bind(wx.EVT_RADIOBUTTON, self.OnAllState)
        self._pnl.AddFoldPanelWindow(item, self._single1, fpb.FPB_ALIGN_WIDTH, fpb.FPB_DEFAULT_SPACING, 10)
        self._leftWindow1.SizeWindows()
    def onDateStart(self,event):
        date_start=self.calendar_begin.GetValue()
        date_end=self.calendar_end.GetValue()
        eventid=event.GetId()
        if date_start=="从:" or date_end =="至:":
            self.start_time="从:"
            self.end_time ="至:"
        else:
            t1 = date_start.split('/')
            t2 = t1[2], t1[1], t1[0]
            st = ''
            self.start_time = st.join(t2)
            t3 = date_end.split('/')
            t4 = t3[2], t3[1], t3[0]
            et = ''
            self.end_time = et.join(t4)
        self.QueryTime()
        self.log.WriteText(
            "天外天系统收到操作员控制指令，ZX_Pane.py开始执行发货日期查询操作，起始日期：" + str(self.start_time) + "，终止日期：" + str(self.end_time) + "\r\n")
    def OnToday(self,event):
        today = datetime.date.today().strftime('%d/%m/%Y')
        self.calendar_begin.textCtrl.SetValue(today)
        self.calendar_end.textCtrl.SetValue(today)
        self.start_time1=self.calendar_begin.GetValue()
        self.end_time1=self.calendar_end.GetValue()
        t1 = self.start_time1.split('/')
        t2 = t1[2], t1[1], t1[0]
        st = ''
        self.start_time = st.join(t2)
        t3 = self.end_time1.split('/')
        t4 = t3[2], t3[1], t3[0]
        et = ''
        self.end_time = et.join(t4)
        self.QueryTime()
        self.log.WriteText(
            "天外天系统收到操作员控制指令，ZX_Pane.py开始执行发货日期查询操作，起始日期：" + str(today) + "，终止日期：" + str(today) + "\r\n")
    def OnYesterday(self,event):
        today1 = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        yesterday = (today1 - oneday).strftime('%d/%m/%Y')
        self.calendar_begin.textCtrl.SetValue(yesterday)
        self.calendar_end.textCtrl.SetValue(yesterday)
        self.start_time1 = self.calendar_begin.GetValue()
        self.end_time1 = self.calendar_end.GetValue()
        t1 = self.start_time1.split('/')
        t2 = t1[2], t1[1], t1[0]
        st = ''
        self.start_time = st.join(t2)
        t3 = self.end_time1.split('/')
        t4 = t3[2], t3[1], t3[0]
        et = ''
        self.end_time = et.join(t4)
        self.QueryTime()

        self.log.WriteText(
                "天外天系统收到操作员控制指令，ZX_Pane.py开始执行发货日期查询操作，起始日期：" + str(yesterday) + "，终止日期：" + str(yesterday) + "\r\n")
    def OnBYesterday(self,event):
        today1 = datetime.date.today()
        twoday = datetime.timedelta(days=2)
        Byesterday = (today1 - twoday).strftime('%d/%m/%Y')
        self.calendar_begin.textCtrl.SetValue(Byesterday)
        self.calendar_end.textCtrl.SetValue(Byesterday)
        self.start_time1 = self.calendar_begin.GetValue()
        self.end_time1 = self.calendar_end.GetValue()
        t1 = self.start_time1.split('/')
        t2 = t1[2], t1[1], t1[0]
        st = ''
        self.start_time = st.join(t2)
        t3 = self.end_time1.split('/')
        t4 = t3[2], t3[1], t3[0]
        et = ''
        self.end_time = et.join(t4)
        self.QueryTime()
        self.log.WriteText(
            "天外天系统收到操作员控制指令，ZX_Pane.py开始执行发货日期查询操作，起始日期：" + str(Byesterday) + "，终止日期：" + str(Byesterday) + "\r\n")
    def OnAllTime(self,event):
        self.calendar_begin.textCtrl.SetValue("从:")
        self.calendar_end.textCtrl.SetValue("至:")
        self.start_time = self.calendar_begin.GetValue()
        self.end_time = self.calendar_end.GetValue()
        self.QueryTime()
        self.log.WriteText(
            "天外天系统收到操作员控制指令，ZX_Pane.py开始执行发货日期查询操作，起始日期：" + str(self.start_time) + "，终止日期：" + str(self.end_time) + "\r\n")
    def OnWaitDelivery(self,event):
        eventid = event.GetId()
        self.id_state=eventid
        self.state = '等待发货'
        self.QueryState()
        self.log.WriteText(
            "天外天系统收到操作员控制指令，ZX_Pane.py开始执行发货单状态查询操作，当前进行等待发货状态发货单查询    \r\n")
    def OnDeliverying(self,event):
        eventid = event.GetId()
        self.id_state = eventid
        self.state = '发货中'
        self.QueryState()
        self.log.WriteText(
            "天外天系统收到操作员控制指令，ZX_Pane.py开始执行发货单状态查询操作，当前进行发货中状态发货单查询    \r\n")
    def OnComplateDelivery(self,event):
        eventid = event.GetId()
        self.id_state = eventid
        self.state = '已发货'
        self.QueryState()
        self.log.WriteText(
            "天外天系统收到操作员控制指令，ZX_Pane.py开始执行发货单状态查询操作，当前进行已发货状态发货单查询    \r\n")
    def OnCancelDelivery(self,event):
        eventid = event.GetId()
        self.id_state = eventid
        self.state = '已取消'
        self.QueryState()
        self.log.WriteText(
            "天外天系统收到操作员控制指令，ZX_Pane.py开始执行发货单状态查询操作，当前进行已取消状态发货单查询    \r\n")
    def OnAllState(self,event):
        eventid = event.GetId()
        self.id_state = eventid
        self.state = '1'
        self.QueryState()
        self.log.WriteText(
            "天外天系统收到操作员控制指令，ZX_Pane.py开始执行发货单状态查询操作，当前进行全部状态发货单查询    \r\n")
    def QueryState(self):
        if self.calendar_begin.GetValue() == "从:" and self.calendar_end.GetValue() == "至:":
            start_time = "从:"
            end_time = "至:"
            self.remainingSpace.query_managment_grid.SetValue(start_time, end_time, self.state)
            self.remainingSpace.query_managment_grid.MyRefresh()
        else:
            self.start_time1 = self.calendar_begin.GetValue()
            self.end_time1 = self.calendar_end.GetValue()
            t1 = self.start_time1.split('/')
            t2 = t1[2], t1[1], t1[0]
            st = ''
            start_time = st.join(t2)
            t3 = self.end_time1.split('/')
            t4 = t3[2], t3[1], t3[0]
            et = ''
            end_time = et.join(t4)
            self.remainingSpace.query_managment_grid.SetValue(start_time, end_time, self.state)
            self.remainingSpace.query_managment_grid.MyRefresh()
    def QueryTime(self):
        if self.id_state!=0:
            if self.id_state==self.radio1.GetId():
                state='等待发货'
                self.remainingSpace.query_managment_grid.SetValue(self.start_time,self.end_time,state)
                self.remainingSpace.query_managment_grid.MyRefresh()
            elif self.id_state==self.radio2.GetId():
                state = '发货中'
                self.remainingSpace.query_managment_grid.SetValue(self.start_time, self.end_time, state)
                self.remainingSpace.query_managment_grid.MyRefresh()
            elif self.id_state==self.radio3.GetId():
                state = '已发货'
                self.remainingSpace.query_managment_grid.SetValue(self.start_time, self.end_time, state)
                self.remainingSpace.query_managment_grid.MyRefresh()
                # self.remainingSpace.Refresh()
            elif self.id_state==self.radio4.GetId():
                state = '已取消'
                self.remainingSpace.query_managment_grid.SetValue(self.start_time, self.end_time, state)
                self.remainingSpace.query_managment_grid.MyRefresh()
                # self.remainingSpace.Refresh()
            elif self.id_state==self._single1.GetId():
                state = '1'
                self.remainingSpace.query_managment_grid.SetValue(self.start_time, self.end_time, state)
                self.remainingSpace.query_managment_grid.MyRefresh()
                # self.remainingSpace.Refresh()
            else:
                state ='1'
                self.remainingSpace.query_managment_grid.SetValue(self.start_time, self.end_time, state)
                self.remainingSpace.query_managment_grid.MyRefresh()
                # self.remainingSpace.Refresh()
        else:
            pass
    def GetOperatorId(self, operator_id):
        self.operator_id = operator_id
    def OnPDFShow(self):
        self._leftWindow2.DestroyChildren()
        self.completed_delivery_PDF=Completed_delivery_PDF(self._leftWindow2,self.log)
#-------------------------------------创建确认发货订单表格
class Confirm_Delivery_Table(gridlib.GridTableBase):
    def __init__(self,data, field_name):
        gridlib.GridTableBase.__init__(self)
        self.data = data
        self.field_name=field_name
        # self.transport_company_record=transport_company_record
        if Is_Database_Connect():
            cursor = DB1.cursor()
            cursor.execute("select `transport_company_name` from `info_transport_company__information` where 1 ORDER BY `Index`")
            transport_company_record = cursor.fetchall()
            Str=':'
            for i in range (len(transport_company_record)):
                Str+=transport_company_record[i][0]+','
        else:
            return
        self.dataTypes = [  gridlib.GRID_VALUE_CHOICE + str(Str),
                            gridlib.GRID_VALUE_STRING,
                            gridlib.GRID_VALUE_STRING,
                            gridlib.GRID_VALUE_NUMBER,
                            gridlib.GRID_VALUE_STRING,
                            gridlib.GRID_VALUE_STRING,
                            gridlib.GRID_VALUE_STRING,
        ]
    #--------------------------------------------------
    # required methods for the wxPyGridTableBase interface
    def GetNumberRows(self):
        return len(self.data)
    def GetNumberCols(self):
        return len(self.field_name)
    def IsEmptyCell(self, row, col):
        try:
            return not self.data[row][col]
        except IndexError:
            return True
    def GetValue(self, row, col):
        try:
            return self.data[row][col]
        except IndexError:
            return ''
    def SetValue(self, row, col, value):
        def innerSetValue(row, col, value):
            try:
                self.data[row][col] = value
            except IndexError:
                # add a new row
                self.data.append([''] * self.GetNumberCols())
                innerSetValue(row, col, value)
                # tell the grid we've added a row
                msg = gridlib.GridTableMessage(self,            # The table
                        gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED, # what we did to it
                        1                                       # how many
                        )
                self.GetView().ProcessTableMessage(msg)
        innerSetValue(row, col, value)
    def DeleteRows(self, pos=0, numRows=1):  # real signature unknown; restored from __doc__
        if self.data is None or len(self.data) == 0:
            return False
        for rowNum in range(0,numRows):
            self.data.remove(self.data[numRows-1-pos-rowNum])
        self.GetView().BeginBatch()#进行批量显示
        deleteMsg=wx.grid.GridTableMessage(self,wx.grid.GRIDTABLE_NOTIFY_ROWS_DELETED,pos,numRows)
        self.GetView().ProcessTableMessage(deleteMsg)
        # ... same thing for columns ....
        self.GetView().EndBatch()#要加上个结尾
        getValueMsg=wx.grid.GridTableMessage(self,wx.grid.GRIDTABLE_REQUEST_VIEW_GET_VALUES)
        self.GetView().ProcessTableMessage(getValueMsg)
        return True
    #--------------------------------------------------
    # Some optional methods
    def GetColLabelValue(self, col):
        return self.field_name[col]
    def GetTypeName(self, row, col):
        return self.dataTypes[col]
    def CanGetValueAs(self, row, col, typeName):
        colType = self.dataTypes[col].split(':')[0]
        if typeName == colType:
            return True
        else:
            return False
    def CanSetValueAs(self, row, col, typeName):
        return self.CanGetValueAs(row, col, typeName)
class Confirm_Delivery_Grid(gridlib.Grid):
    def __init__(self, parent,log,pos,size):
        gridlib.Grid.__init__(self, parent,-1,pos,size)
        self.log=log
        self.data = []
        self.information=[]
        self.field_name = ['货运公司','品牌','订单编号','打包包数','收货人电话','发货编号','收货信息']
        try:
            if Is_Database_Connect():
                self.ReadDatabase()
            else:
                self.log.WriteText('天外天系统正在运行ZX_Paint.py中Confirm_Delivery_Grid类OnChanged方法时未连接数据库，请检查数据库名和密码是否正确\r\n')
                return False
        except:
            self.log.WriteText("天外天系统正在执行ZX_Pane.py中Confirm_Delivery_Grid类OnChanged方法数据处理过程中出现错误，请检查数据库中相应字段信息是否为空或者数据类型转换是否正确\r\n")
        self.table = Confirm_Delivery_Table(self.data, self.field_name)  # 自定义表网格
        self.SetTable(self.table, True)
        self.SetRowLabelSize(0)
        self.SetMargins(0, 0)
        self.AutoSizeColumns(False)
        self.DisableDragColSize()
        self.DisableDragRowSize()
        for j in range(len(self.data)):
            for m in range(1, 7):
                self.SetReadOnly(j, m, isReadOnly=True)
        self.Bind(gridlib.EVT_GRID_CELL_CHANGED, self.OnChanged)
        # self.timer = wx.PyTimer(self.Refresh)
        # self.timer.Start(5000)
    def OnChanged(self,eve):
        self.data = []
        self.information = [] #  清空构造函数时建立的列表
        row = eve.GetRow()  # 获得鼠标单击的单元格所在的行
        order_id = self.GetCellValue(row, 2)
        transport_company= self.GetCellValue(row, 0)
        try:
            if Is_Database_Connect():
                cursor = DB.cursor()
                cursor.execute("UPDATE `order_order_online` set `Transport_company`='%s' WHERE `Order_id`='%s' AND `State`='%s'" % (
                    transport_company, order_id,CONFIRM_DELIVERY))#在对话框中修改货运公司时，将修改的货运公司更新到数据库中。
                DB.commit()
                self.ReadDatabase()
            else:
                self.log.WriteText('天外天系统正在运行ZX_Paint.py中Confirm_Delivery_Grid类OnChanged方法时未连接数据库，请检查数据库名和密码是否正确\r\n')
                return False
        except:
            self.log.WriteText(
                "天外天系统在响应ZX_Pane.py 中确认发货表格中OnChanged（）方法，请检查数据库中相关字段是否为空或者数据类型转换是否正确  \r\n")
        for i in range(len(self.data)):
            for j in range(len(self.field_name)):
                self.table.SetValue(i, j,self.data[i][j])
        self.SetRowLabelSize(0)
        self.SetMargins(0, 0)
        self.AutoSizeColumns(False)
        self.DisableDragColSize()
        self.DisableDragRowSize()
    def ReadDatabase(self):
        try:
            cursor = DB1.cursor()
            cursor.execute(
                "select `transport_company_name` from `info_transport_company__information` where 1 ORDER BY `Index`")
            self.transport_company_record = cursor.fetchall()
            cursor = DB.cursor()
            cursor.execute(
                "select `Delivery_ID` from `delivery_form_zx` WHERE 1  ORDER BY `Index` DESC  LIMIT 1 ")
            self.delivery_id = cursor.fetchone()
            for t in range(len(self.transport_company_record)):
                cursor.execute(
                    "select `Transport_company`,`Brand`,`Order_id`,`Package_num_hcj`,`Order_delivery_num` from `order_order_online` where `Transport_company`='%s' AND `State`='%s'AND `Order_delivery_num`='%s'" %
                    (self.transport_company_record[t][0], CONFIRM_DELIVERY, str(self.delivery_id[0])))
                delivery_inform = cursor.fetchall()
                if delivery_inform == ():
                    pass
                else:
                    self.information.append(delivery_inform)
            # --------------------------------------------------使用三维列表将数据库添加到self.data中
            if self.information == ():
                self.data = []
            else:
                for i1 in range(len(self.information)):
                    for i in range(len(self.information[i1])):
                        cursor = DB.cursor()
                        cursor.execute(
                            "select `Contract_id` from `order_order_online` where Order_id='%s'" % self.information[i1][i][2])
                        contract_record = cursor.fetchone()
                        cursor.execute(
                            "select `Customer_name`,`Customer_tel`,`Payment_method` from `order_contract_internal` where Contract_id='%s'"
                            % contract_record[0])
                        address_record = cursor.fetchone()
                        # if address_record == () or address_record == None:
                        #     self.log.WriteText(
                        #         "天外天系统在ZX_Pane.py 中 order_contract_internal查找行对应合同号的门店地址和门店收货人出现错误，请检查订单所属合同号是否存在内部合同表单，或者内部合同表单门店地址和收货人电话是否为空  \r\n")
                        if address_record[2]==10 or address_record[2]==5:
                            inform = [self.information[i1][i][0], self.information[i1][i][1], self.information[i1][i][2],
                                      self.information[i1][i][3], address_record[1], self.information[i1][i][4],
                                      address_record[0]
                                      ]
                            self.data.append(inform)
                        else:
                            self.log.WriteText("天外天系统在ZX_Pane.py 中 定金未结清 \r\n")
        except:
            self.log.WriteText("天外天系统正在运行ZX_Pane.py Confirm_Delivery_Grid()中ReadDatabase()出现错误，请检查\r\n")
    def Return_Data(self):
        delivery_data=[]
        for i in range(len(self.data)):
            code_img_i=exe_Barcode(self.data[i][2])
            # address=self.data[i][6].split("·")
            row_delivery_data=[self.data[i][0],self.data[i][1],str(self.data[i][2]),str(self.data[i][3]),str(self.data[i][4]),self.data[i][6],code_img_i]
            delivery_data.append(row_delivery_data)
        return delivery_data
    def Return_delivery_code(self):
        return self.delivery_id[0]
#--------------------------------创建等待确认发货订单表格
class Wait_Confirm_Delivery_Table(gridlib.GridTableBase):
    def __init__(self,data, field_name):
        gridlib.GridTableBase.__init__(self)
        self.data = data
        self.field_name=field_name
        self.dataTypes = [gridlib.GRID_VALUE_BOOL,
                            gridlib.GRID_VALUE_STRING,
                            gridlib.GRID_VALUE_DATETIME,
                            gridlib.GRID_VALUE_FLOAT + ':6,2',
                            gridlib.GRID_VALUE_NUMBER,
                            gridlib.GRID_VALUE_STRING,
                        ]
    #--------------------------------------------------
    # required methods for the wxPyGridTableBase interface
    def GetNumberRows(self):
        return len(self.data)
    def GetNumberCols(self):
        return len(self.field_name)
    def IsEmptyCell(self, row, col):
        try:
            return not self.data[row][col]
        except IndexError:
            return True
    def GetValue(self, row, col):
        try:
            return self.data[row][col]
        except IndexError:
            return ''
    def SetValue(self, row, col, value):
        def innerSetValue(row, col, value):
            try:
                self.data[row][col] = value
            except IndexError:
                # add a new row
                self.data.append([''] * self.GetNumberCols())
                innerSetValue(row, col, value)
                # tell the grid we've added a row
                msg = gridlib.GridTableMessage(self,            # The table
                        gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED, # what we did to it
                        1                                       # how many
                        )
                self.GetView().ProcessTableMessage(msg)
        innerSetValue(row, col, value)
    def DeleteRows(self, pos=0, numRows=1):  # real signature unknown; restored from __doc__
        if self.data is None or len(self.data) == 0:
            return False
        for rowNum in range(0,numRows):
            self.data.remove(self.data[numRows-1-pos-rowNum])
        self.GetView().BeginBatch()#进行批量显示
        deleteMsg=wx.grid.GridTableMessage(self,wx.grid.GRIDTABLE_NOTIFY_ROWS_DELETED,pos,numRows)
        self.GetView().ProcessTableMessage(deleteMsg)
        # ... same thing for columns ....
        self.GetView().EndBatch()#要加上个结尾
        getValueMsg=wx.grid.GridTableMessage(self,wx.grid.GRIDTABLE_REQUEST_VIEW_GET_VALUES)
        self.GetView().ProcessTableMessage(getValueMsg)
        return True
    #--------------------------------------------------
    # Some optional methods
    def GetColLabelValue(self, col):
        return self.field_name[col]
    def GetTypeName(self, row, col):
        return self.dataTypes[col]
    def CanGetValueAs(self, row, col, typeName):
        colType = self.dataTypes[col].split(':')[0]
        if typeName == colType:
            return True
        else:
            return False
    def CanSetValueAs(self, row, col, typeName):
        return self.CanGetValueAs(row, col, typeName)
class Wait_Confirm_Delivery_Grid(gridlib.Grid):
    def __init__(self, parent,log):
        gridlib.Grid.__init__(self, parent, -1)
        self.data = []
        self.log=log
        self.field_name = [' ', '订单编号', '交货日期', '订单面积', '打包包数', '货运公司']
        self.Database_data([])
        self.table = Wait_Confirm_Delivery_Table(self.data, self.field_name)  # 自定义表网格
        self.SetTable(self.table, True)
        self.SetRowLabelSize(0)
        self.SetMargins(0, 0)
        self.AutoSizeColumns(False)
        self.DisableDragColSize()
        self.DisableDragRowSize()
        for j in range(len(self.data)):
            for m in range(1, 6):
                self.SetReadOnly(j, m, isReadOnly=True)
        # self.timer = wx.PyTimer(self.MyRefresh)
        # self.timer.Start(20000)
    def MyRefresh(self,check_state):
        try:
            self.DeleteRows(0, numRows=self.GetNumberRows())
            self.data = []
            self.Database_data(check_state)
            for i in range(len(self.data)):
                for j in range(len(self.field_name)):
                    self.table.SetValue(i, j,self.data[i][j])
            self.SetRowLabelSize(0)
            self.SetMargins(0, 0)
            self.AutoSizeColumns(False)
            self.DisableDragColSize()
            self.DisableDragRowSize()
        except:
            self.log.WriteText("天外天系统正在运行ZX_Pane.py Wait_Confirm_Delivery_Grid()中MyRefresh()出现错误，请检查\r\n")
    def Database_data(self,check_state):
        self.order_wait_confirm_sum = 0
        self.package_total_sum = 0
        self.order_area_now = 0.00
        try:
            if Is_Database_Connect():
                cursor = DB.cursor()
                cursor.execute(
                    "select `Order_id`,`Receive_time`,`Order_area`,`Package_num_hcj`,`Transport_company`,`Contract_id` from `order_order_online` where State='%s' ORDER BY `Receive_time`" % WAIT_CONFIRM_DELIVERY)
                record = cursor.fetchall()
                for i in range(len(record)):
                    cursor.execute(
                        "select `Payment_method` from `order_contract_internal` where `Contract_id`='%s' " % record[i][5])
                    payment = cursor.fetchone()
                    if payment[0]==10 or payment[0]==5:
                        check_state_history = False
                        for j in range(len(check_state)):
                            if record[i][0] == check_state[j]:
                                check_state_history = True
                                break
                            elif j == len(check_state) - 1:
                                check_state_history = False
                        inform = [check_state_history, record[i][0], record[i][1].strftime('%m-%d'), record[i][2], record[i][3], record[i][4]]
                        self.data.append(inform)
                        self.package_total_sum += int(record[i][3])
                        self.order_area_now += float(record[i][2])
                    else:
                        pass
                self.order_wait_confirm_sum = len(record)
            else:
                return
        except:
            self.log.WriteText(
                "天外天系统正在ZX_Pane.py 中 等待确认发货表格类刷新方法中执行读取数据库操作，出现错误，请检查数据库中相关字段是否为空或者数据类型转换是否正确  \r\n")
#--------------------------------创建等待发货订单表格
class Wait_Delivery_Table(gridlib.GridTableBase):
    def __init__(self, data,field_name):
        gridlib.GridTableBase.__init__(self)
        self.data=data
        self.field_name=field_name
        self.dataTypes = [gridlib.GRID_VALUE_BOOL,
                            gridlib.GRID_VALUE_STRING,
                            gridlib.GRID_VALUE_STRING,
                            gridlib.GRID_VALUE_TEXT,
                            gridlib.GRID_VALUE_FLOAT + ':6,2',
                            gridlib.GRID_VALUE_NUMBER,
                            gridlib.GRID_VALUE_NUMBER,
                            gridlib.GRID_VALUE_STRING,
                            gridlib.GRID_VALUE_STRING,
                            gridlib.GRID_VALUE_DATETIME,
                        ]
    #--------------------------------------------------
    # required methods for the wxPyGridTableBase interface
    def GetNumberRows(self):
        return len(self.data)
    def GetNumberCols(self):
        return len(self.field_name)
    def IsEmptyCell(self, row, col):
        try:
            return not self.data[row][col]
        except IndexError:
            return True
    def GetValue(self, row, col):
        try:
            return self.data[row][col]
        except IndexError:
            return ''
    def SetValue(self, row, col, value):
        def innerSetValue(row, col, value):
            try:
                self.data[row][col] = value
            except IndexError:
                # add a new row
                self.data.append([''] * self.GetNumberCols())
                innerSetValue(row, col, value)
                # tell the grid we've added a row
                msg = gridlib.GridTableMessage(self,            # The table
                        gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED, # what we did to it
                        1                                       # how many
                        )
                self.GetView().ProcessTableMessage(msg)
        innerSetValue(row, col, value)
    def DeleteRows(self, pos=0, numRows=1):  # real signature unknown; restored from __doc__
        if self.data is None or len(self.data) == 0:
            return False
        for rowNum in range(0,numRows):
            self.data.remove(self.data[numRows-1-pos-rowNum])
        self.GetView().BeginBatch()#进行批量显示
        deleteMsg=wx.grid.GridTableMessage(self,wx.grid.GRIDTABLE_NOTIFY_ROWS_DELETED,pos,numRows)
        self.GetView().ProcessTableMessage(deleteMsg)
        # ... same thing for columns ....
        self.GetView().EndBatch()#要加上个结尾
        getValueMsg=wx.grid.GridTableMessage(self,wx.grid.GRIDTABLE_REQUEST_VIEW_GET_VALUES)
        self.GetView().ProcessTableMessage(getValueMsg)
        return True
    def Clear(self):

        self.GetView().BeginBatch()

        msg = wx.grid.GridTableMessage(self, wx.grid.GRIDTABLE_NOTIFY_ROWS_DELETED,
                                   0,self.GetNumberCols() - 1)

        self.GetView().ProcessTableMessage(msg)

        # ... same thing for columns ....

        self.GetView().EndBatch()

        self.data = []

        msg = wx.grid.GridTableMessage(self, wx.grid.GRIDTABLE_REQUEST_VIEW_GET_VALUES)
        self.GetView().ProcessTableMessage(msg)
    # --------------------------------------------------
    # Some optional methods
    def GetColLabelValue(self, col):
        return self.field_name[col]
    def GetTypeName(self, row, col):
        return self.dataTypes[col]
    def CanGetValueAs(self, row, col, typeName):
        colType = self.dataTypes[col].split(':')[0]
        if typeName == colType:
            return True
        else:
            return False
    def CanSetValueAs(self, row, col, typeName):
        return self.CanGetValueAs(row, col, typeName)
class Wait_Delivery_Grid(gridlib.Grid):
    def __init__(self, parent,log):
        gridlib.Grid.__init__(self, parent, -1)
        self.data = []
        self.log=log
        self.field_name = [' ', '订单编号', '客户', '终端客户','订单面积','总块数', '打包包数','品牌','货运公司','交货工期']
        self.Database_data([])
        #self.EnableEditing(False)                         #使得整个表格都不使能
        self.table = Wait_Delivery_Table(self.data, self.field_name)  # 自定义表网格
        self.SetTable(self.table, False)
        self.SetRowLabelSize(0)
        self.SetMargins(0, 0)
        self.AutoSizeColumns(False)
        self.DisableDragColSize()
        self.DisableDragRowSize()

        for j in range(len(self.data)):
            for m in range(1, 8):
                self.SetReadOnly(j, m, isReadOnly=True)
        # self.timer = wx.PyTimer(self.MyRefresh)
        # self.timer.Start(20000)
    def MyRefresh(self,check_state):
        # self.table.Clear()
        try:
            self.DeleteRows(0,numRows=self.GetNumberRows())
            self.data = []
            self.Database_data(check_state)
            for i in range(len(self.data)):
                for j in range(len(self.field_name)):
                    self.table.SetValue(i, j,self.data[i][j])
            self.SetRowLabelSize(0)
            self.SetMargins(0, 0)
            self.AutoSizeColumns(False)
            self.DisableDragColSize()
            self.DisableDragRowSize()
        except:
            self.log.WriteText("天外天系统正在运行ZX_Pane.py Wait_Delivery_Grid()中MyRefresh()出现错误，请检查\r\n")
    def Database_data(self,check_state):
        try:
            if Is_Database_Connect():
                cursor = DB.cursor()
                cursor.execute(
                    "select `Order_id`,`Receive_time`,`Order_area`,`Package_num_hcj`,`Transport_company`,`Brand`,`Customer_name`,`Part_num` from `order_order_online` where State='%s' ORDER BY `Receive_time`"
                    % WAIT_DELIVERY)
                record = cursor.fetchall()
                for i in range(len(record)):
                    cursor = DB.cursor()
                    cursor.execute(
                        "select `Contract_id` from `order_order_online` where Order_id='%s' ORDER BY `Receive_time`"% record[i][0])
                    contract_record = cursor.fetchone()
                    cursor.execute(
                        "select `Customer_name`,`Payment_method` from `order_contract_internal` where Contract_id='%s'"% contract_record[0])
                    address_record = cursor.fetchone()
                    # if address_record==None:
                    #     self.log.WriteText("天外天系统在 ZX_Pane.py 中 order_contract_internal查找行对应合同号的门店地址和门店收货人出现错误，请检查订单所属合同号是否存在内部合同表单，或者内部合同表单门店地址和收货人电话是否为空  \r\n")
                    check_state_history = False
                    for j in range(len(check_state)):
                        if record[i][0] == check_state[j]:
                            check_state_history = True
                            break
                        elif j == len(check_state) - 1:
                            check_state_history = False
                    if address_record[1]==10 or address_record[1]==5:
                        inform = [check_state_history,record[i][0],address_record[0],record[i][6],record[i][2],record[i][7],record[i][3],record[i][5],record[i][4],record[i][1].strftime('%m-%d')]
                        self.data.append(inform)
                        # for j in range(len(inform)):
                        #     self.table.SetValue(i, j,inform[j])
                        # self.Refresh()
                    else:
                        self.log.WriteText("天外天系统在 ZX_Pane.py 中 该订单定金支付未完成或者不存在月结功能 \r\n")
                # print 'inform',self.data,'record',record
            else:
                self.log.WriteText("天外天系统在ZX_Pane.py 中等待发货表格类中执行读取数据库操作，数据库未连接，请检查\r\n")
                return
        except:
            self.log.WriteText(
                "天外天系统在ZX_Pane.py 中等待发货表格类中执行读取数据库操作，出现错误，请检查数据库相关信息是否为空或者进行数据类型转换时出现错误   \r\n")
class ZX_Delivery_Panel(wx.Panel):
    def __init__(self,parent,log):
        wx.Panel.__init__(self, parent, -1)
        self.log=log
        self.operator_id='0'
        self.grid1 = Wait_Delivery_Grid(self,self.log)
        self.grid2 = Wait_Confirm_Delivery_Grid(self,self.log)
        self.grid1.Bind(gridlib.EVT_GRID_CELL_CHANGED, self.On_left_change)
        self.grid2.Bind(gridlib.EVT_GRID_CELL_CHANGED, self.On_right_change)
        self.num=''
        btn_add= wx.Button(self, 1001, "添\r\n>>\r\n加",size=(30,30))#增加\r\n字符可以使得字符换行。
        self.Bind(wx.EVT_BUTTON, self.OnButton, btn_add)
        btn_remove = wx.Button(self, 1002, "移\r\n<<\r\n除",size=(30,30))
        # self.Bind(wx.EVT_BUTTON, self.On_btn_remove_Click, btn_remove)
        self.Bind(wx.EVT_BUTTON, self.OnButton, btn_remove)
        btn_add_all= wx.Button(self, 1003, "全\r\n部\r\n添\r\n加",size=(30,30))
        self.Bind(wx.EVT_BUTTON, self.OnButton, btn_add_all)
        btn_remove_all= wx.Button(self, 1004, "全\r\n部\r\n移\r\n除",size=(30,30))
        self.Bind(wx.EVT_BUTTON, self.OnButton, btn_remove_all)
        self.btn_ok= wx.Button(self, -1, "确认发货")
        self.Bind(wx.EVT_BUTTON, self.On_btn_ok, self.btn_ok)
        label1 = wx.StaticText(self, -1, "订单总数")
        label2 = wx.StaticText(self, -1, "打包总数")
        label3 = wx.StaticText(self, -1, "当前发货面积")
        self.order_count = wx.TextCtrl(self, wx.ID_ANY,size=(60,20),style=wx.TE_READONLY)
        self.package_count = wx.TextCtrl(self, wx.ID_ANY,size=(60,20),style=wx.TE_READONLY)
        self.delivery_area = wx.TextCtrl(self, wx.ID_ANY,size=(60,20), style=wx.TE_READONLY)
        vsizer1 = wx.BoxSizer(wx.VERTICAL)
        vsizer1.Add(btn_add, proportion=2, flag=wx.ALL, border=1)
        vsizer1.Add(btn_remove, proportion=2, flag=wx.ALL, border=1)
        vsizer1.Add(btn_add_all, proportion=1, flag=wx.ALL, border=1)
        vsizer1.Add(btn_remove_all, proportion=1, flag=wx.ALL, border=1)
        #self.SetSizer(vsizer1)# 添加四个垂直按钮
        xsizer1 = wx.BoxSizer()
        xsizer1.Add(label1, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xsizer1.Add(self.order_count, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xsizer2 = wx.BoxSizer()
        xsizer2.Add(label2, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xsizer2.Add(self.package_count, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xsizer3 = wx.BoxSizer()
        xsizer3.Add(label3, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xsizer3.Add(self.delivery_area, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        #创建三个静态文本和相对应的文本框
        xsizer5 = wx.BoxSizer()
        xsizer5.Add(xsizer1, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        xsizer5.Add(xsizer2, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        xsizer5.Add(xsizer3, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        vsizer2 = wx.BoxSizer(wx.VERTICAL)
        vsizer2.Add(xsizer5, proportion=1, flag=wx.EXPAND | wx.ALL, border=3)
        vsizer2.Add(self.btn_ok, proportion=1, flag=wx.EXPAND | wx.ALL, border=3)
        vsizer4 = wx.BoxSizer(wx.VERTICAL)
        vsizer4.Add(self.grid2, proportion=1, flag=wx.EXPAND | wx.ALL, border=3)
        vsizer4.Add(vsizer2, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xsizer6 = wx.BoxSizer()
        xsizer6.Add(self.grid1, proportion=1, flag=wx.EXPAND | wx.ALL, border=3)
        xsizer6.Add(vsizer1, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xsizer6.Add(vsizer4, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        self.SetSizer(xsizer6)
        self.SetTextctrl()
        self.timer = wx.PyTimer(self.TimeRefresh)
        self.timer.Start(10000)
        self.right_check_value = []
        self.left_check_value = []
    def OnButton(self,eve):
        try:
            if Is_Database_Connect():
                if eve.GetId() == 1001:
                    for i in range(len(self.grid1.table.data)):
                        if self.grid1.table.GetValue(i,0)==1:
                            order_id=self.grid1.table.GetValue(i,1)
                            cursor = DB.cursor()
                            cursor.execute("UPDATE `order_order_online` set `State`='%s' WHERE `Order_id`='%s' " % (WAIT_CONFIRM_DELIVERY, order_id))
                        else:
                            pass
                elif eve.GetId() == 1002:
                    for i in range(len(self.grid2.table.data)):
                        if self.grid2.table.GetValue(i,0)==1:
                            order_id=self.grid2.table.GetValue(i,1)
                            cursor = DB.cursor()
                            cursor.execute("UPDATE `order_order_online` set `State`='%s' WHERE `Order_id`='%s' " % (WAIT_DELIVERY, order_id))
                        else:
                            pass
                elif eve.GetId() == 1003:
                    cursor = DB.cursor()
                    cursor.execute("UPDATE `order_order_online` set `State`='%s' WHERE `State`='%s' " % (
                        WAIT_CONFIRM_DELIVERY, WAIT_DELIVERY))
                elif eve.GetId() == 1004:
                    cursor = DB.cursor()
                    cursor.execute("UPDATE `order_order_online` set `State`='%s' WHERE `State`='%s' " % (
                        WAIT_DELIVERY, WAIT_CONFIRM_DELIVERY))
                else:
                    pass
                DB.commit()
                # self.grid1.MyRefresh(self.left_check_value)
                # self.grid2.MyRefresh(self.right_check_value)
                self.TimeRefresh()
                self.SetTextctrl()
            else:
                self.log.WriteText('天外天系统正在运行ZX_Pane.py ZX_Delivery_Panel未连接数据库，请检查用户名和密码\r\n')
                return
        except:
            self.log.WriteText('天外天系统正在运行ZX_Pane.py ZX_Delivery_Panel中按钮OnButton事件时出错，请检查\r\n')
    def On_btn_ok(self,eve):
        today = datetime.datetime.now()
        self.today = today.strftime('%y%m%d')#'%Y%m%d'的结果是20180715，'%y%m%d'的结果是180715
        try:
            if Is_Database_Connect():
                cursor =DB.cursor()
                cursor.execute(
                    "SELECT `Index` FROM `delivery_form_zx` WHERE 1  ORDER BY `Index` DESC  LIMIT 1")  # 在发货编号数据库里，先按照index降序排列，后取第一行，也就是降序前的最后一行的数据
                record = cursor.fetchone()  # record里存放的是发货单数据库里最后一行的数据
                if record == () or record == None:
                    first_code = '1001'
                    D_code = str(first_code).lstrip('1')
                    self.num = 'DE' + self.today + D_code
                else:
                    first_code=eval('1000+(record[0]+1)')#进行字符串之间的运算
                    D_code=str(first_code).lstrip('1')#lstrip（）进行字符串之间的截取
                    self.num ='DE' + self.today + D_code
                cursor.execute(
                    "INSERT INTO `delivery_form_zx`(`Order_amount`,`Delivery_ID`,`Delivery_total_area`,`Package_amount`,`Creator`,`State`)VALUES ('%s','%s','%s','%s','%s','%s')" % (
                    self.order_count.GetValue(),self.num,self.delivery_area.GetValue(), self.package_count.GetValue(),self.operator_id,"等待发货"))
                DB.commit()
                cursor.execute(
                    "SELECT `Index`, `Order_id`,`Contract_id` FROM `order_order_online` WHERE `State`='%s'  ORDER BY `Index` "% WAIT_CONFIRM_DELIVERY)
                self.order_num_record = cursor.fetchall()
                for o in range(len(self.order_num_record)):
                    cursor.execute("UPDATE `order_order_online` set `Order_delivery_num`='%s', `Delievery_schedule_operator_id`='%s',`Delievery_schedule_time`='%s',`State`='%s' WHERE `Order_id`='%s'" % (
                            self.num , self.operator_id,today,CONFIRM_DELIVERY,self.order_num_record[o][1]))
                    cursor = DB.cursor()
                    cursor.execute(
                        "UPDATE `order_element_online` set `Delievery_schedule_operator_id`='%s',`Delievery_schedule_time`='%s',`State`='%s'WHERE `Order_id`='%s'" % (
                            self.operator_id, today,CONFIRM_DELIVERY, self.order_num_record[o][1]))
                    cursor = DB.cursor()
                    cursor.execute(
                        "UPDATE `order_part_online` set `Delievery_schedule_operator_id`='%s', `Delievery_schedule_time`='%s', `State`='%s' WHERE `Order_id`='%s'" % (
                            self.operator_id, today,CONFIRM_DELIVERY, self.order_num_record[o][1]))
                    cursor = DB.cursor()
                    cursor.execute(
                        "UPDATE `order_section_online` set `Delievery_schedule_operator_id`='%s', `Delievery_schedule_time`='%s', `State`='%s' WHERE `Order_id`='%s'" % (
                            self.operator_id, today, CONFIRM_DELIVERY, self.order_num_record[o][1]))
                    cursor = DB.cursor()
                    cursor.execute(
                        "UPDATE `order_contract_internal` set `State`='%s' WHERE `Contract_id`='%s'" % (
                            CONFIRM_DELIVERY, self.order_num_record[o][2]))
                DB.commit()#DB.commit()将这条语句放在for循环外面一块提会使程序运行变快。
                self.grid2.Refresh()
            else:
                self.log.WriteText('天外天系统正在运行ZX_Pane.py，On_btn_ok方法时未连接数据库，请检查用户名、密码等信息\r\n')
                return
            dlg = Confirm_Delivery_Dialog(self,self.log ,-1, "确认发货窗口" , '1' , '' ,self.operator_id, size=(800, 600),
                             style=wx.DEFAULT_DIALOG_STYLE)#将对话框类实例化
            dlg.delivery_tasklist_ID.SetValue(self.num)          #将发货单号写进对话框中的静态文本框中
            dlg.CenterOnScreen()
            val = dlg.ShowModal()
            if val == wx.ID_OK:                                  #类似于绑定事件，将参数传到pdf类
                print_data=dlg.confirm_delivery.Return_Data()
                print_delivery_code=dlg.confirm_delivery.Return_delivery_code()
                self.print_delivery_form=Print_Delivery_Form(self,-1,print_data,print_delivery_code)
                self.print_delivery_form.Show(True)                  #frame有Show属性。
                self.order_count.SetValue('0')
                self.package_count.SetValue('0')
                self.delivery_area.SetValue('0.0')                                   #重新设置静态文本框的显示信息和确认按钮是否使能
                if len(self.grid2.data) == 0:
                    self.btn_ok.Enable(False)
                else:
                    self.btn_ok.Enable(True)
                self.log.WriteText("天外天系统正在执行操作员确认发货操作，进入打印发货单界面   \r\n")
            elif val == wx.ID_CANCEL:
                if Is_Database_Connect():
                    cursor=DB.cursor()
                    cursor.execute("UPDATE `delivery_form_zx` set `Cancel_operator`='%s',`Cancel_date`='%s', `State`='%s' WHERE `State`='%s'AND `Delivery_ID`='%s'" % (self.operator_id,today,'已取消', '等待发货',self.num))
                    for o in range(len(self.order_num_record)):
                        cursor.execute(
                            "UPDATE `order_order_online` set `Order_delivery_num`='%s', `Delievery_schedule_operator_id`='%s',`Delievery_schedule_time`='%s',`State`='%s' WHERE `Order_id`='%s'" % (
                                '',self.operator_id, today, WAIT_CONFIRM_DELIVERY, self.order_num_record[o][1]))
                        cursor = DB.cursor()
                        cursor.execute(
                            "UPDATE `order_element_online` set `Delievery_schedule_operator_id`='%s',`Delievery_schedule_time`='%s',`State`='%s'WHERE `Order_id`='%s'" % (
                                self.operator_id, today, WAIT_CONFIRM_DELIVERY, self.order_num_record[o][1]))
                        cursor = DB.cursor()
                        cursor.execute(
                            "UPDATE `order_part_online` set `Delievery_schedule_operator_id`='%s', `Delievery_schedule_time`='%s', `State`='%s' WHERE `Order_id`='%s'" % (
                                self.operator_id, today, WAIT_CONFIRM_DELIVERY, self.order_num_record[o][1]))
                        cursor = DB.cursor()
                        cursor.execute(
                            "UPDATE `order_section_online` set `Delievery_schedule_operator_id`='%s', `Delievery_schedule_time`='%s', `State`='%s' WHERE `Order_id`='%s'" % (
                                self.operator_id, today, WAIT_CONFIRM_DELIVERY, self.order_num_record[o][1]))
                        cursor = DB.cursor()
                        cursor.execute(
                            "UPDATE `order_contract_internal` set `State`='%s' WHERE `Contract_id`='%s'" % (WAIT_CONFIRM_DELIVERY, self.order_num_record[o][2]))
                    DB.commit()
                    self.grid2.Refresh()
                else:
                    return
                self.log.WriteText( "天外天系统正在执行操作员取消发货操作    \r\n")
            else:
                pass
            dlg.Destroy()
        except:
            self.log.WriteText(
                "天外天系统正在响应操作员点击确认发货按钮操作，ZX_Pane.py 中 On_btn_ok方法出现错误，请检查数据库中对应字段名称是否改变   \r\n")
    def SetTextctrl(self):
        self.order_count.SetValue(str(self.grid2.order_wait_confirm_sum))
        self.package_count.SetValue(str(self.grid2.package_total_sum))
        self.delivery_area.SetValue(str(self.grid2.order_area_now))
        if len(self.grid2.data) == 0:
            self.btn_ok.Enable(False)
        else:
            self.btn_ok.Enable(True)
    def GetOperatorId(self,operator_id):
        self.operator_id=operator_id
    def TimeRefresh(self):
        self.grid1.MyRefresh(self.left_check_value)
        self.grid2.MyRefresh(self.right_check_value)
    def On_left_change(self,evt):
        if self.grid1.table.GetValue(evt.GetRow(),0) == True :
            self.left_check_value.append(self.grid1.table.GetValue(evt.GetRow(), 1))
        else:
            for i in range(len(self.left_check_value)-1,-1,-1):
                if self.left_check_value[i] == self.grid1.table.GetValue(evt.GetRow(), 1):
                    del self.left_check_value[i]
    def On_right_change(self,evt):
        if self.grid2.table.GetValue(evt.GetRow(),0) == True :
            self.right_check_value.append(self.grid2.table.GetValue(evt.GetRow(), 1))
        else:
            for i in range(len(self.right_check_value)-1,-1,-1):
                if self.right_check_value[i] == self.grid2.table.GetValue(evt.GetRow(), 1):
                    del self.right_check_value[i]
#-----------------------------------------创建PDF打印发货清单
def opj(path):
    """Convert paths to the  platform-specific separator,获取相对路径"""
    st = os.path.join(*tuple(path.split('/')))
    if path.startswith('/'):
        st ='/'+st
    return st
def exe_Barcode(code):
    try:
        pwd = os.path.exists("C:\image\\")
        if pwd:  # 判断文件夹是否存在，如果不存在则创建
            pass
            # print "File Exist!!!"
        else:
            os.mkdir("C:\image\\")
        exePath = ".\hcj_code\code_image.exe"
        param = str(code) + " C:\image"
        win32api.ShellExecute(0, "open", exePath, param, '', 0)
        road = os.path.exists('C:\image\\' + str(code) + '.png')
        while not road:
            time.sleep(0.5)
            win32api.ShellExecute(0, "open", exePath, param, '', 0)
            road = os.path.exists('C:\image\\' + str(code) + '.png')
            if road:
                break
        code_img = Image('C:\image\\' + str(code) + '.png')
        code_img.drawHeight = 45
        code_img.drawWidth = 100
        return code_img
    except:
        pass
class Print_Delivery_Form(wx.Frame):   # 创建打印发货清单PDF
    def __init__(self, parent, id,print_data,print_delivery_code):
        wx.Frame.__init__(self, parent, id, '打印发货单界面', size=(1000, 600),style=wx.MAXIMIZE | wx.CAPTION | wx.CLOSE_BOX | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX)
        #panel = wx.Panel(self)

        self.print_data=print_data
        self.print_delivery_code=print_delivery_code
        vsizer = wx.BoxSizer(wx.VERTICAL)
        self.buttonpanel = pdfButtonPanel(self, wx.ID_ANY,wx.DefaultPosition, wx.DefaultSize, 0)
        vsizer.Add(self.buttonpanel, 0,
                   wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT | wx.TOP, 5)
        self.viewer = pdfViewer(self, wx.ID_ANY, wx.DefaultPosition,
                                wx.DefaultSize, wx.HSCROLL | wx.VSCROLL | wx.SUNKEN_BORDER)
        vsizer.Add(self.viewer, 1, wx.GROW | wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)
        self.SetSizer(vsizer)
        self.SetAutoLayout(True)
        self.buttonpanel.viewer = self.viewer
        self.viewer.buttonpanel = self.buttonpanel
        f = os.path.exists("C:\\delivery_list_history")  # 用于判断在D盘中是否存在delivery_list_history文件夹，如果不在在这个路径下新建文件夹。
        if not f:
            os.mkdir("C:\\delivery_list_history")  # 新建文件夹
        self.filename_server_name = u"\\\\192.168.31.250\\delivery_list_history\\" + str(self.print_delivery_code) + '.pdf'
        self.filename_local_name = u"C:\\delivery_list_history\\" + str(self.print_delivery_code) + '.pdf'
        is_exist_file = os.path.exists("\\\\\delivery_list_history\\" + str(self.print_delivery_code) + '.pdf')
        if is_exist_file:
            try:
                shutil.copyfile(self.filename_server_name, self.filename_local_name)
                self.viewer.LoadFile("C:\\delivery_list_history\\" + str(self.print_delivery_code) + '.pdf')
            except:
                self.DrawTable_PDF()  # 画pdf表
        else:
            self.DrawTable_PDF()  # 画pdf表
        wx.BeginBusyCursor()
        # self.viewer.LoadFile('dispatch_bill.pdf')#在当前执行文件目录下加载dispatch_bill.pdf的pdf文件。
        # self.viewer.LoadFile("C:\delivery_list_history\\"+str(self.print_delivery_code)+'.pdf')#在D:\delivery_list_history下加载str(self.print_delivery_code).pdf
        wx.EndBusyCursor()
    def myFirstPage(self,canvas, doc):
        # from reportlab.lib.colors import blue
        # PAGE_HEIGHT = canvas._pagesize[1]
        canvas.saveState()
        # canvas.setStrokeColor(blue)
        # canvas.setLineWidth(5)
        # canvas.line(66,72,66,PAGE_HEIGHT-72)
        # canvas.setFont(_baseFontNameB,24)
        # canvas.drawString(108, PAGE_HEIGHT-108, "TABLE OF CONTENTS DEMO")
        canvas.setFont('msyh',9)
        canvas.drawString(4 * inch, 0.75 * inch, u"第 1 页")
        canvas.restoreState()
    def myLaterPages(self,canvas, doc):
        # from reportlab.lib.colors import blue
        # PAGE_HEIGHT = canvas._pagesize[1]
        canvas.saveState()
        # canvas.setStrokeColor(blue)
        # canvas.setLineWidth(5)
        # canvas.line(66,72,66,PAGE_HEIGHT-72)
        canvas.setFont('msyh', 9)
        canvas.drawString(4 * inch, 0.75 * inch, u"第 %d 页" % doc.page)
        canvas.restoreState()
    def DrawTable_PDF(self):
        story = []
        stylesheet = getSampleStyleSheet()
        normalStyle = stylesheet['Normal']
        self.today = datetime.date.today()
        self.formatted_today = self.today.strftime('%Y-%m-%d')
        #############################生成条形码
        code_img=exe_Barcode(self.print_delivery_code)
        # 标题：段落的用法详见reportlab-userguide.pdf中chapter 6 Paragraph
        rpt_title = '<para autoLeading="off" fontSize=22 align=center><b><font face="msyh">瀚海发货单</font></b><br/><br/><br/></para>'
        story.append(Paragraph(rpt_title, normalStyle))
        # text = '''<para autoLeading="off" fontSize=8 align=left><b><font face="msyh">2018.07.18</font><font face="msyh"></font></b></para>'''
        # story.append(Paragraph(text, normalStyle))
        # text1 = '''<para autoLeading="off" fontSize=8 align=right><b><font face="msyh">发货单号:</font><font face="msyh">DE180716001</font></b></para>'''
        # story.append(Paragraph(text1, normalStyle))
        #表格数据：用法详见reportlab-userguide.pdf中chapter 7 Table
        # component_data = [['货运公司','品牌','订单编号','包数', '收货人电话','收货信息','发货编号']
        #                 ,['顺丰快递', '瀚海一诺','AA1L1O1','12','12345678901','山东省青岛市崂山区青岛路345号','DE180716001_0001']]
        component_data = [['日期：',self.formatted_today,'','','','发货单号:',code_img],['','','','','','',''],['货运公司','品牌','订单编号','件数', '收货人电话','收货信息','发货编号条形码']]
        for i in range(len(self.print_data)):
            component_data.append(self.print_data[i])#调用二维列表的值
        component_table = Table(component_data,colWidths=[60,45,56,25,140,85,100], rowHeights=None, style=None,splitByRow=0, repeatRows=0, repeatCols=0, rowSplitRange=2, spaceBefore=None, spaceAfter=None)
           #创建表格对象#，并设定各列宽度#设置行列宽度自适应
        #添加表格样式(0,0)表示左上角（0，0）表示右下角（-1，0）表示倒数第一列（-2，0）表示倒数第二列
        component_table.setStyle(TableStyle([
        ('FONTNAME',(0,0),(-1,-1),'msyh'),#字体
        ('FONTSIZE',(0,0),(-1,-1),9),#字体大小
        # ('SPAN',(0,0),(3,0)),#合并第一行前三列
        # ('BACKGROUND',(0,0),(-1,0), colors.lightskyblue),#设置第一行背景颜色
        #('BACKGROUND',(-2,0),(-2,1), colors.lightskyblue),#设置倒数第二列第一行单元格景颜色
        # ('SPAN',(-1,0),(-2,0)), #合并第一行后两列
        # ('ALIGN',(-1,0),(-2,0),'RIGHT'),#对齐
        # ('VALIGN',(-1,0),(-2,0),'MIDDLE'),  #对齐
        #('LINEBEFORE',(0,0),(0,-1),0.1,colors.grey),#设置表格左边线颜色为灰色，线宽为0.1
        #('TEXTCOLOR',(0,1),(-2,-1),colors.royalblue),#设置表格内文字颜色
        ('TEXTCOLOR',(0,1),(-2,-1),colors.black),#设置表格内文字颜色
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),#设置表格内文本居中
        ('ALIGN', (-2, 0), (-2, 1), 'RIGHT'),
        ('VALIGN', (-2, 0), (-2, 1), 'MIDDLE'),  # 设置表格内文本居中
        ('GRID',(0,2),(-1,-1),0.5,colors.black),#设置两行以后表格框线为红色，线宽为0.5
        # ('GRID',(0,0),(-1,0),0.5,colors.red),#设置表格框线为红色，线宽为0.5
        ]))
        story.append(component_table)
        # story.append(PageBreak())
        #rootdir = os.getcwd()#获取一下当前执行文件路径
        # doc = SimpleDocTemplate(os.getcwd()+'\\dispatch_bill.pdf')#将生成的PDF放在当前执行文件下
        # doc.build(story)
        SimpleDocTemplate("C:\delivery_list_history\\"+str(self.print_delivery_code)+'.pdf').build(story,
                                                   onFirstPage=self.myFirstPage, onLaterPages=self.myLaterPages)
        self.viewer.LoadFile("C:\delivery_list_history\\" + str(self.print_delivery_code) + '.pdf') # 在D:\delivery_list_history下加载str(self.print_delivery_code).pdf
        try:
            shutil.copyfile(self.filename_local_name, self.filename_server_name)
        except:
            print '往250共享文件夹中复制文件时出错，请检查'
#--------------------------------------管理员权限设置
class Authority__Dialog(wx.Dialog):
    def __init__(self, parent,id, title,size,pos=wx.DefaultPosition,
            style=wx.DEFAULT_DIALOG_STYLE):
        wx.Dialog.__init__(self)
        self.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        self.Create(parent,id, title, pos, size, style)
        # self.Close(False)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.authority_ctrl_grid = Authority_Ctrl_Grid(self,pos=(5, 5),size=(650, 450))
        btn_ok = wx.Button(self, wx.ID_OK, "确定")
        btn_cancel = wx.Button(self, wx.ID_CANCEL, "取消")
        btn_add = wx.Button(self, -1, "添加")
        btn_add.Bind(wx.EVT_BUTTON, self.OnAddButton)
        hbox=wx.BoxSizer()
        hbox.Add(btn_ok, proportion=1, flag=wx.ALL, border=3)
        hbox.Add(btn_cancel, proportion=1, flag=wx.ALL, border=3)
        hbox.Add(btn_add, proportion=1, flag=wx.ALL, border=3)
        sizer.Add(self.authority_ctrl_grid, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        sizer.Add(hbox, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.SetSizer(sizer)
        sizer.Fit(self)
    def OnAddButton(self,event):
        dlg = Add_Administrators_Dialog(self, -1, "添加管理员窗口", size=(450, 650),
                         style=wx.DEFAULT_DIALOG_STYLE)
        dlg.ShowWindowModal()
        self.Destroy()#在添加管理员窗口关闭之后，此对话框也会随之关闭。
class Add_Administrators_Dialog(wx.Dialog):
    def __init__(self, parent, id, title, size=wx.DefaultSize, pos=wx.DefaultPosition,
                 style=wx.DEFAULT_DIALOG_STYLE, name='添加管理员窗口'):
        wx.Dialog.__init__(self)
        self.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        self.Create(parent, id, title, pos, size, style, name)

        sizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, "添加管理员")

        sizer.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "姓     名 :")
        box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.name_text = wx.TextCtrl(self, -1, "", size=(80, -1))
        box.Add(self.name_text, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        sizer.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "性     别 :")
        box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        genderList = ['男', '女']
        self.gender_text = wx.Choice(self, -1, size=(80, -1), choices=genderList)
        # self.gender_text = wx.TextCtrl(self, -1, "", size=(80, -1))
        box.Add(self.gender_text, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        sizer.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "联系电话:")
        box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.tel_text = wx.TextCtrl(self, -1, "", size=(80, -1))
        box.Add(self.tel_text, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        sizer.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "登录密码:")
        box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.password_text = wx.TextCtrl(self, -1, "", size=(80, -1),style=wx.TE_PASSWORD)#
        box.Add(self.password_text, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        sizer.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "确认密码:")
        box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.second_password_text = wx.TextCtrl(self, -1, "", size=(80, -1),style=wx.TE_PASSWORD)#
        box.Add(self.second_password_text, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        sizer.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "微 信 号 :")
        box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.wechat_text = wx.TextCtrl(self, -1, "", size=(80, -1))#,style=wx.TE_READONLY
        box.Add(self.wechat_text, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        QR_btn=wx.Button(self,-1,'添加')
        QR_btn.Bind(wx.EVT_BUTTON,self.OnWechatLogin)
        box.Add(QR_btn, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        sizer.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "微信备注:")
        box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.wechat_remark_text = wx.TextCtrl(self, -1, "", size=(80, -1))
        box.Add(self.wechat_remark_text, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        sizer.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        line = wx.StaticLine(self, -1, size=(20, -1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT | wx.TOP, 5)
        box = wx.BoxSizer(wx.HORIZONTAL)
        registered_btn = wx.Button(self, wx.ID_OK,'注册')
        registered_btn.Bind(wx.EVT_BUTTON,self.Onregistered_btn)
        box.Add(registered_btn, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        cal_btn = wx.Button(self, wx.ID_CANCEL,'取消')
        box.Add(cal_btn, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        sizer.Add(box, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.SetSizer(sizer)
        sizer.Fit(self)
    def OnWechatLogin(self,event):
        # itchat.auto_login()
        # self.myUserName = itchat.get_friends(update=False)[0]["UserName"]
        # # myNickName = itchat.get_friends(update=False)[0]["NickName"]
        # myNickName = itchat.get_friends(update=False)[0]["NickName"]
        # print myNickName
        # self.wechat_text.SetValue(myNickName)
        # itchat.send(msg=u'您的微信号已成功添加，祝您工作愉快', toUserName='filehelper')
        # itchat.logout()
        skip_wechat_login = Skip_Wechat_Login(self, -1, '扫码添加好友', pos=wx.DefaultPosition,#用来添加图灵机器人为好友的二维码。，目前还没想到好的逻辑方法是
                                              size=(300, 330), style=wx.DEFAULT_FRAME_STYLE)
        skip_wechat_login.Show(True)
    def Onregistered_btn(self,event):
        today1 = datetime.date.today()
        today = today1.strftime('%y')
        tel=self.tel_text.GetValue()
        # b=re.match('1',str(tel))#正则表达式来限定第一个数字为1
        phonenumber = re.findall(r"1\d{10}", str(tel))#正则表达式用于限制第一位为1，并且输入号码为11位。
        # pat='[0-9]'
        # c=re.match('[0-9]',str(tel))
        # c=re.match('[11]',str(tel))
        # print '0',b
        if self.wechat_text.GetValue()!=''and self.name_text.GetValue() !=''and self.gender_text.GetStringSelection()!=''\
                and phonenumber!='' and self.password_text.GetValue() !='' and self.wechat_remark_text.GetValue() !=''\
                and self.password_text.GetValue()==self.second_password_text.GetValue():
            # registered_inform=[self.name_text.GetValue(),self.gender_text.GetValue(),self.tel_text.GetValue(),self.password_text.GetValue(),self.myUserName]
            if Is_Database_Connect():
                cursor=DB1.cursor()
                cursor.execute(
                    "INSERT INTO `info_staff_new`(`Name`,`Gender`,`Phone`,`Password`,`wechatAccount`,`Remarkname`,`Position`,`Group_chat_state`)VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')" % (
                        self.name_text.GetValue(), self.gender_text.GetStringSelection(), self.tel_text.GetValue(),
                        self.password_text.GetValue(),self.wechat_text.GetValue(),self.wechat_remark_text.GetValue(),25,0))
                DB1.commit()
                cursor = DB1.cursor()
                cursor.execute(
                    "SELECT `Index` FROM `info_staff_new` WHERE `Position`=25 ORDER BY `Index` DESC  LIMIT 1")  # 在发货编号数据库里，先按照index降序排列，后取第一行，也就是降序前的最后一行的数据
                record = cursor.fetchone()  # record里存放的是staff_new里最后一行的Index
                if record == () or record == None:
                    first_code = '1001'
                    job_id_code = str(first_code).lstrip('1')
                    job_id= today + '25' + job_id_code
                else:
                    first_code = eval('1000+(record[0]+1)')  # 进行字符串之间的运算
                    job_id_code = str(first_code).lstrip('1')  # lstrip（）进行字符串之间的截取
                    job_id = today + '25' + job_id_code
                cursor = DB1.cursor()
                cursor.execute(
                    "UPDATE `info_staff_new` set `Job_id`='%s' WHERE `Index`='%s'" % (job_id, record[0]))
                DB1.commit()
                self.Destroy()
                dlg = wx.MessageDialog(self, '您已成功添加管理员'+self.name_text.GetValue(), '提示',
                                       wx.OK | wx.ICON_INFORMATION
                                       # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                                       )
                dlg.ShowModal()
            else:
                return
        elif self.wechat_text.GetValue() == '' or self.name_text.GetValue() == '' or self.gender_text.GetStringSelection() == '' \
                or self.password_text.GetValue() == '' or self.wechat_remark_text.GetValue() == '':

            dlg = wx.MessageDialog(self, '信息输入不能为空，请检查后重新填入信息！', '警告',
                                   wx.OK | wx.ICON_INFORMATION
                                   # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                                   )
            dlg.ShowModal()
        elif self.password_text.GetValue()!=self.second_password_text.GetValue():
            dlg = wx.MessageDialog(self, '确认密码不正确，请重新输入密码！', '警告',
                                   wx.OK | wx.ICON_INFORMATION
                                   # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                                   )
            dlg.ShowModal()
        elif phonenumber != '':
            dlg = wx.MessageDialog(self, '电话号码输入错误，请检查后重新填入信息！', '警告',
                                    wx.OK | wx.ICON_INFORMATION
                                    # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                                    )
            dlg.ShowModal()
        else:
            dlg = wx.MessageDialog(self, '信息输入不正确，请检查后重新填入信息！', '警告',
                                   wx.OK | wx.ICON_INFORMATION
                                   # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                                   )
            dlg.ShowModal()
class Authority_Ctrl_Table(gridlib.GridTableBase):
        def __init__(self, data, field_name):
            gridlib.GridTableBase.__init__(self)
            self.data = data
            self.field_name = field_name
            self.dataTypes = [gridlib.GRID_VALUE_STRING,
                              gridlib.GRID_VALUE_STRING,
                              gridlib.GRID_VALUE_STRING,
                              gridlib.GRID_VALUE_BOOL,
                              gridlib.GRID_VALUE_BOOL,
                              gridlib.GRID_VALUE_BOOL,
                              gridlib.GRID_VALUE_BOOL,
                              gridlib.GRID_VALUE_BOOL,
                              gridlib.GRID_VALUE_BOOL,
                              gridlib.GRID_VALUE_BOOL,
                              gridlib.GRID_VALUE_BOOL,
                              gridlib.GRID_VALUE_BOOL,
                              gridlib.GRID_VALUE_BOOL,
                              gridlib.GRID_VALUE_BOOL,
                              gridlib.GRID_VALUE_BOOL,
                              gridlib.GRID_VALUE_BOOL,
                              ]

        # --------------------------------------------------
        # required methods for the wxPyGridTableBase interface
        def GetNumberRows(self):
            return len(self.data)

        def GetNumberCols(self):
            return len(self.field_name)
        def IsEmptyCell(self, row, col):
            try:
                return not self.data[row][col]
            except IndexError:
                return True
        def GetValue(self, row, col):
            try:
                return self.data[row][col]
            except IndexError:
                return ''
        def SetValue(self, row, col, value):
            def innerSetValue(row, col, value):
                try:
                    self.data[row][col] = value
                except IndexError:
                    # add a new row
                    self.data.append([''] * self.GetNumberCols())
                    innerSetValue(row, col, value)
                    # tell the grid we've added a row
                    msg = gridlib.GridTableMessage(self,  # The table
                                                   gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED,  # what we did to it
                                                   1  # how many
                                                   )

                    self.GetView().ProcessTableMessage(msg)

            innerSetValue(row, col, value)

        # --------------------------------------------------
        # Some optional methods
        def GetColLabelValue(self, col):
            return self.field_name[col]

        def GetTypeName(self, row, col):
            return self.dataTypes[col]

        def CanGetValueAs(self, row, col, typeName):
            colType = self.dataTypes[col].split(':')[0]
            if typeName == colType:
                return True
            else:
                return False

        def CanSetValueAs(self, row, col, typeName):
            return self.CanGetValueAs(row, col, typeName)
class Authority_Ctrl_Grid(gridlib.Grid):
    def __init__(self, parent,pos,size):
        gridlib.Grid.__init__(self, parent, -1)
        self.data = []
        # self.log = log
        self.field_name = ['工作编号', '姓名', '性别', '排产管理', '发货管理', '工位管理', '合同订单管理', '人力资源管理','库管理','员工工作量统计管理','分拣小车显示','质检工位','门店管理','报错管理','财务管理','货运公司管理']
        # self.EnableEditing(False)                         #使得整个表格都不使能
        if Is_Database_Connect():
            cursor = DB1.cursor()
            cursor.execute(
                "select `Job_id`,`Name`,`Gender`,`scheduling_management`,`delivery_management`,`workstation_management`,`contract_order_management`,`human_resource_management`,`library_management`,`workload_statistics_management`,`sorting_car_display`,`quality_testing`,`store_management`,`error_management`,`finance_management`,`transport_management` from `info_staff_new` where `Position`=25 ORDER BY `Index`")
            record = cursor.fetchall()
            for i in range(len(record)):
                inform = [record[i][0], record[i][1], record[i][2], record[i][3], record[i][4], record[i][5], record[i][6], record[i][7], record[i][8], record[i][9], record[i][10], record[i][11], record[i][12], record[i][13], record[i][14], record[i][15]]
                self.data.append(inform)
        else:
            return
        self.table = Authority_Ctrl_Table(self.data, self.field_name)  # 自定义表网格
        self.SetTable(self.table, True)
        self.SetRowLabelSize(0)
        self.SetMargins(0, 0)
        self.AutoSizeColumns(False)
        self.DisableDragColSize()
        self.DisableDragRowSize()
        for j in range(len(self.data)):
            for m in range(0, 2):
                self.SetReadOnly(j, m, isReadOnly=True)
class Skip_Wechat_Login(wx.Frame):           # 创建弹出微信扫描二维码登录界面
    def __init__(
            self, parent, ID, title, pos=wx.DefaultPosition,
            size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE):
        wx.Frame.__init__(self, parent, ID, '管理员微信名片', pos, size=(300,330), style=wx.DEFAULT_FRAME_STYLE)
        panel = wx.Panel(self, -1)
        self.Center(wx.BOTH)#将Frame窗口显示在屏幕中间
        bmp = wx.Bitmap(opj("bitmaps/Wechat.jpg"))
        img = bmp.ConvertToImage()
        bmp = img.Scale(290, 300)
        temp = bmp.ConvertToBitmap()
        self.bmp = wx.StaticBitmap(parent=self, bitmap=temp)
#------------------------------------修改密码对话框
class Change_Password_Dialog(wx.Dialog):
    def __init__(self, parent, id, title,job_id, size=wx.DefaultSize, pos=wx.DefaultPosition,
                 style=wx.DEFAULT_DIALOG_STYLE, name='密码设置窗口'):
        wx.Dialog.__init__(self)
        self.job_id=job_id
        self.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        self.Create(parent, id, title, pos, size, style, name)
        sizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, "修改密码")
        sizer.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "原始密码:")
        box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.start_password = wx.TextCtrl(self, -1, "", size=(80, -1),style=wx.TE_PASSWORD)
        box.Add(self.start_password, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        sizer.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "新 密 码 :")
        box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.new_password_text = wx.TextCtrl(self, -1, "", size=(80, -1),style=wx.TE_PASSWORD)#
        box.Add(self.new_password_text, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        sizer.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "确认密码:")
        box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.second_password_text = wx.TextCtrl(self, -1, "", size=(80, -1),style=wx.TE_PASSWORD)#
        box.Add(self.second_password_text, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        sizer.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        box = wx.BoxSizer(wx.HORIZONTAL)
        registered_btn = wx.Button(self, wx.ID_OK,'确认')
        registered_btn.Bind(wx.EVT_BUTTON,self.Onregistered_btn)
        box.Add(registered_btn, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        cal_btn = wx.Button(self, wx.ID_CANCEL,'取消')
        box.Add(cal_btn, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        sizer.Add(box, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.SetSizer(sizer)
        sizer.Fit(self)
    def Onregistered_btn(self,event):
        if self.start_password.GetValue()!=''and self.new_password_text.GetValue() !=''and self.new_password_text.GetValue()==self.second_password_text.GetValue():
            if Is_Database_Connect():
                cursor=DB1.cursor()
                cursor.execute("UPDATE `info_staff_new` set `Password`='%s' WHERE `Job_id`='%s' " % ( self.new_password_text.GetValue(),self.job_id))
                DB1.commit()
                dlg = wx.MessageDialog(self, '密码修改成功', '提示',
                                       wx.OK | wx.ICON_INFORMATION
                                       # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                                       )
                dlg.ShowModal()
                self.Destroy()
            else:
                return
        elif self.start_password.GetValue() == '' or self.new_password_text.GetValue() == '' :
            dlg = wx.MessageDialog(self, '初始密码和新密码不能为空，请检查后重新填入信息！', '警告',
                                   wx.OK | wx.ICON_INFORMATION
                                   # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                                   )
            dlg.ShowModal()
        elif self.new_password_text.GetValue()!=self.second_password_text.GetValue():
            dlg = wx.MessageDialog(self, '确认密码不正确，请重新输入密码！', '警告',
                                   wx.OK | wx.ICON_INFORMATION
                                   # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                                   )
            dlg.ShowModal()
#------------------------------------微信发布窗口
class Send_Wechat_Msg_Dialog(wx.Dialog):
    def __init__(self, parent, id, title, size=wx.DefaultSize, pos=wx.DefaultPosition,
                 style=wx.DEFAULT_DIALOG_STYLE, name='微信发布窗口'):
        wx.Dialog.__init__(self)
        self.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        self.Create(parent, id, title, pos, size, style, name)
        sampleList = ['群发布', '按岗位发布']
        sizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, "微信发布")
        sizer.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "发布内容:")
        box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.Wechat_Text = wx.TextCtrl(self, -1, "", size=(80, -1),style=wx.TE_MULTILINE)
        box.Add(self.Wechat_Text, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        sizer.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        label = wx.StaticText(self, -1, "发布对象:")
        box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.sampleList =  wx.RadioBox(
                self, -1, "", wx.DefaultPosition, wx.DefaultSize,
                sampleList, 1, wx.RA_SPECIFY_COLS | wx.NO_BORDER
                )
        box.Add(self.sampleList, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        sizer.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        # cb1 = wx.CheckBox(self, -1, "群     发")
        # cb2 = wx.CheckBox(self, -1, "按工位发送")
        # cb3 = wx.CheckBox(self, -1, "工位发送")
        box = wx.BoxSizer(wx.HORIZONTAL)
        registered_btn = wx.Button(self, wx.ID_OK,'确认')
        # registered_btn.Bind(wx.EVT_BUTTON,self.OnSend_btn)
        box.Add(registered_btn, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        cal_btn = wx.Button(self, wx.ID_CANCEL,'取消')
        box.Add(cal_btn, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        sizer.Add(box, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.SetSizer(sizer)
        sizer.Fit(self)
    def OnSend_btn(self,event):
        if self.Wechat_Text.GetValue()!='':
            if Is_Database_Connect():
                # cursor = DB1.cursor()
                # cursor.execute(
                #     "Insert into `info_wechat` set `Receive_Group`,`State`='%s'，`Message`='%s' WHERE `State`='%s',`Message`" % (222,WAIT_WECHAT_SEND, self.Wechat_Text.GetValue()))
                # cursor.execute(
                #     "select `Receive_Group`,`Message` from `info_wechat` where `State`='%s' ORDER BY `Index` " % WAIT_WECHAT_SEND)
                # record = cursor.fetchall()
                # for i in range(len(record)):
                #     if record[i][0] == 222:
                chat_rooms = itchat.search_chatrooms(name=u'瀚海工作群')
                itchat.send('%s' % self.Wechat_Text.GetValue(), toUserName=chat_rooms[0]['UserName'])
                dlg = wx.MessageDialog(self, '消息发布成功', '提示',
                                       wx.OK | wx.ICON_INFORMATION
                                       # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                                       )
                dlg.ShowModal()
                self.Destroy()
        else:
            dlg = wx.MessageDialog(self, '发布内容不能为空，请重新输入！', '警告',
                                   wx.OK | wx.ICON_INFORMATION
                                   # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                                   )
            dlg.ShowModal()
#------------------------------------分拣小车表格显示
class Sorting_Vehicle_Management_Table(gridlib.GridTableBase):
    def __init__(self,data, field_name):
        gridlib.GridTableBase.__init__(self)
        self.data = data
        self.field_name=field_name
        self.dataTypes = [
                            gridlib.GRID_VALUE_STRING,
                            gridlib.GRID_VALUE_STRING,
                            gridlib.GRID_VALUE_STRING,
                            gridlib.GRID_VALUE_STRING,
                            gridlib.GRID_VALUE_STRING,
                            gridlib.GRID_VALUE_STRING,
                            gridlib.GRID_VALUE_STRING,
                            gridlib.GRID_VALUE_STRING,
                            gridlib.GRID_VALUE_STRING,
                            gridlib.GRID_VALUE_STRING,
                            gridlib.GRID_VALUE_STRING,
                            gridlib.GRID_VALUE_STRING,
                            gridlib.GRID_VALUE_STRING,
                            gridlib.GRID_VALUE_STRING,
                            gridlib.GRID_VALUE_STRING,
                            gridlib.GRID_VALUE_STRING,
                            gridlib.GRID_VALUE_STRING,
                            gridlib.GRID_VALUE_STRING,
                            gridlib.GRID_VALUE_STRING,
                            gridlib.GRID_VALUE_STRING,
                        ]
    #--------------------------------------------------
    # required methods for the wxPyGridTableBase interface
    def GetNumberRows(self):
        return len(self.data)
    def GetNumberCols(self):
        return len(self.field_name)
    def IsEmptyCell(self, row, col):
        try:
            return not self.data[row][col]
        except IndexError:
            return True
    def GetValue(self, row, col):
        try:
            return self.data[row][col]
        except IndexError:
            return ''
    def SetValue(self, row, col, value):
        def innerSetValue(row, col, value):
            try:
                self.data[row][col] = value
            except IndexError:
                # add a new row
                self.data.append([''] * self.GetNumberCols())
                innerSetValue(row, col, value)
                # tell the grid we've added a row
                msg = gridlib.GridTableMessage(self,            # The table
                        gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED, # what we did to it
                        1                                       # how many
                        )
                self.GetView().ProcessTableMessage(msg)
        innerSetValue(row, col, value)
    def DeleteRows(self, pos=0, numRows=1):  # real signature unknown; restored from __doc__
        if self.data is None or len(self.data) == 0:
            return False
        for rowNum in range(0,numRows):
            self.data.remove(self.data[numRows-1-pos-rowNum])
        self.GetView().BeginBatch()#进行批量显示
        deleteMsg=wx.grid.GridTableMessage(self,wx.grid.GRIDTABLE_NOTIFY_ROWS_DELETED,pos,numRows)
        self.GetView().ProcessTableMessage(deleteMsg)
        # ... same thing for columns ....
        self.GetView().EndBatch()#要加上个结尾
        getValueMsg=wx.grid.GridTableMessage(self,wx.grid.GRIDTABLE_REQUEST_VIEW_GET_VALUES)
        self.GetView().ProcessTableMessage(getValueMsg)
        return True
    #--------------------------------------------------
    # Some optional methods
    def GetColLabelValue(self, col):
        return self.field_name[col]
    def GetTypeName(self, row, col):
        return self.dataTypes[col]
    def CanGetValueAs(self, row, col, typeName):
        colType = self.dataTypes[col].split(':')[0]
        if typeName == colType:
            return True
        else:
            return False
    def CanSetValueAs(self, row, col, typeName):
        return self.CanGetValueAs(row, col, typeName)
class Sorting_Vehicle_Management_Grid(gridlib.Grid):
    def __init__(self, parent,log):
        gridlib.Grid.__init__(self, parent, -1)
        self.data = []
        self.log=log
        self.sort_car_position='ALL'
        self.sort_car_state='ALL'
        self.state_inform={}
        self.state_inform_nume={}
        self.position_inform_nume={'加工中心下料':6,'模压前分拣':12,'质量检查':18,'未分配':0}
        self.position_inform={6:'加工中心下料',12:'模压前分拣',18:'质量检查',0:'未分配'}
        self.field_name = ['序号', '控制器序列号', '分拣车类型', '分拣车ip地址', '控制器端口号', '电池电压',  '控制器版本号',  '所属工位', 'LED控制字', '分拣车状态','在线状态', '命令执行状态','在线返回语句', '命令返回语句','电量偏差','分拣车格数', '闪烁控制','远程升级', '控制器复位', 'WIFI复位']
        if Is_Database_Connect():
            cursor = DB.cursor()
            cursor.execute(
                "select `state`,`state_name` from `info_car_state_online` where 1 ")
            State_record = cursor.fetchall()
            for i in range(len(State_record)):
                self.state_inform[State_record[i][0]] = State_record[i][1]
                self.state_inform_nume[State_record[i][1]] = State_record[i][0]#根据中文名字的得到position
            cursor = DB.cursor()
            cursor.execute(
                "select `Index`,`MCU_SN`,`Position_Style`,`MCU_IP`,`MCU_Port`,`MCU_Power`,`MCU_Ver`,`Position`,`Led_control`,`State`,`is_online`,`is_order_done`,`Return`,`Return_get_order`,`MCU_Power_dev`,`Led_total_num`,`MCU_LED_twinkle`,`MCU_OTA_UPDATE`,`MCU_restart`,`MCU_wifi_clear` from `equipment_led_controler` where 1 ")
            Sorting_record = cursor.fetchall()
            for i in range(len(Sorting_record)):
                inform = [Sorting_record[i][0], Sorting_record[i][1], Sorting_record[i][2], Sorting_record[i][3],
                          Sorting_record[i][4], Sorting_record[i][5], Sorting_record[i][6], self.position_inform[Sorting_record[i][7]],
                          Sorting_record[i][8],
                          self.state_inform[Sorting_record[i][9]], Sorting_record[i][10], Sorting_record[i][11], Sorting_record[i][12],
                          Sorting_record[i][13], Sorting_record[i][14], Sorting_record[i][15], Sorting_record[i][16],
                          Sorting_record[i][17],
                          Sorting_record[i][18], Sorting_record[i][19]]
                self.data.append(inform)
        else:
            return
        self.table = Sorting_Vehicle_Management_Table(self.data, self.field_name)  # 自定义表网格
        self.SetTable(self.table, True)
        self.SetRowLabelSize(0)
        self.SetMargins(0, 0)
        self.AutoSizeColumns(False)
        self.DisableDragColSize()
        self.DisableDragRowSize()
        self.EnableEditing(False)
        # for j in range(len(self.data)):
        #     for m in range(1, 6):
        #         self.SetReadOnly(j, m, isReadOnly=True)
        self.timer = wx.PyTimer(self.MyRefresh)
        self.timer.Start(1000)
    def MyRefresh(self):
        try:
            self.DeleteRows(0, numRows=self.GetNumberRows())
            self.data = []
            if self.sort_car_state=='ALL':
                if Is_Database_Connect():
                    cursor = DB.cursor()
                    cursor.execute(
                        "select `Index`,`MCU_SN`,`Position_Style`,`MCU_IP`,`MCU_Port`,`MCU_Power`,`MCU_Ver`,`Position`,`Led_control`,`State`,`is_online`,`is_order_done`,`Return`,`Return_get_order`,`MCU_Power_dev`,`Led_total_num`,`MCU_LED_twinkle`,`MCU_OTA_UPDATE`,`MCU_restart`,`MCU_wifi_clear` from `equipment_led_controler` where 1 ")
                    Sorting_record_refresh = cursor.fetchall()
                    for i in range(len(Sorting_record_refresh)):
                        if self.sort_car_position=='ALL':
                            inform = [Sorting_record_refresh[i][0], Sorting_record_refresh[i][1], Sorting_record_refresh[i][2],Sorting_record_refresh[i][3],Sorting_record_refresh[i][4],Sorting_record_refresh[i][5],Sorting_record_refresh[i][6],self.position_inform[Sorting_record_refresh[i][7]],Sorting_record_refresh[i][8],
                                      self.state_inform[Sorting_record_refresh[i][9]], Sorting_record_refresh[i][10],Sorting_record_refresh[i][11],Sorting_record_refresh[i][12],Sorting_record_refresh[i][13],Sorting_record_refresh[i][14],Sorting_record_refresh[i][15],Sorting_record_refresh[i][16],Sorting_record_refresh[i][17],
                                      Sorting_record_refresh[i][18],Sorting_record_refresh[i][19]]
                            self.data.append(inform)
                        else:
                            if self.position_inform_nume[self.sort_car_position]==Sorting_record_refresh[i][7]:
                                inform = [Sorting_record_refresh[i][0], Sorting_record_refresh[i][1],
                                          Sorting_record_refresh[i][2], Sorting_record_refresh[i][3],
                                          Sorting_record_refresh[i][4], Sorting_record_refresh[i][5],
                                          Sorting_record_refresh[i][6], self.position_inform[Sorting_record_refresh[i][7]],
                                          Sorting_record_refresh[i][8],
                                          self.state_inform[Sorting_record_refresh[i][9]],
                                          Sorting_record_refresh[i][10], Sorting_record_refresh[i][11],
                                          Sorting_record_refresh[i][12], Sorting_record_refresh[i][13],
                                          Sorting_record_refresh[i][14], Sorting_record_refresh[i][15],
                                          Sorting_record_refresh[i][16], Sorting_record_refresh[i][17],
                                          Sorting_record_refresh[i][18], Sorting_record_refresh[i][19]]
                                self.data.append(inform)
                            else:
                                pass
                    for i in range(len(self.data)):
                        for j in range(len(self.field_name)):
                            self.table.SetValue(i, j,self.data[i][j])
                else:
                    return
            else:
                number=self.state_inform_nume[self.sort_car_state]
                if Is_Database_Connect():
                    cursor = DB.cursor()
                    cursor.execute(
                        "select `Index`,`MCU_SN`,`Position_Style`,`MCU_IP`,`MCU_Port`,`MCU_Power`,`MCU_Ver`,`Position`,`Led_control`,`State`,`is_online`,`is_order_done`,`Return`,`Return_get_order`,`MCU_Power_dev`,`Led_total_num`,`MCU_LED_twinkle`,`MCU_OTA_UPDATE`,`MCU_restart`,`MCU_wifi_clear` from `equipment_led_controler` where `State`='%s' "%number)
                    Sorting_record_refresh = cursor.fetchall()
                    for i in range(len(Sorting_record_refresh)):
                        if self.sort_car_position=='ALL':
                            inform = [Sorting_record_refresh[i][0], Sorting_record_refresh[i][1], Sorting_record_refresh[i][2],Sorting_record_refresh[i][3],Sorting_record_refresh[i][4],Sorting_record_refresh[i][5],Sorting_record_refresh[i][6],self.position_inform[Sorting_record_refresh[i][7]],Sorting_record_refresh[i][8],
                                      self.state_inform[Sorting_record_refresh[i][9]], Sorting_record_refresh[i][10],Sorting_record_refresh[i][11],Sorting_record_refresh[i][12],Sorting_record_refresh[i][13],Sorting_record_refresh[i][14],Sorting_record_refresh[i][15],Sorting_record_refresh[i][16],Sorting_record_refresh[i][17],
                                      Sorting_record_refresh[i][18],Sorting_record_refresh[i][19]]
                            self.data.append(inform)
                        else:
                            if self.position_inform_nume[self.sort_car_position]==Sorting_record_refresh[i][7]:
                                inform = [Sorting_record_refresh[i][0], Sorting_record_refresh[i][1],
                                          Sorting_record_refresh[i][2], Sorting_record_refresh[i][3],
                                          Sorting_record_refresh[i][4], Sorting_record_refresh[i][5],
                                          Sorting_record_refresh[i][6], self.position_inform[Sorting_record_refresh[i][7]],
                                          Sorting_record_refresh[i][8],
                                          self.state_inform[Sorting_record_refresh[i][9]],
                                          Sorting_record_refresh[i][10], Sorting_record_refresh[i][11],
                                          Sorting_record_refresh[i][12], Sorting_record_refresh[i][13],
                                          Sorting_record_refresh[i][14], Sorting_record_refresh[i][15],
                                          Sorting_record_refresh[i][16], Sorting_record_refresh[i][17],
                                          Sorting_record_refresh[i][18], Sorting_record_refresh[i][19]]
                                self.data.append(inform)
                            else:
                                pass
                    for i in range(len(self.data)):
                        for j in range(len(self.field_name)):
                            self.table.SetValue(i, j,self.data[i][j])
                else:
                    return

            self.SetRowLabelSize(0)
            self.SetMargins(0, 0)
            self.AutoSizeColumns(False)
            self.DisableDragColSize()
            self.DisableDragRowSize()
        except:
            self.log.WriteText("天外天系统正在运行ZX_Pane.py Wait_Confirm_Delivery_Grid()中MyRefresh()出现错误，请检查\r\n")
    def SetValue(self,sort_car_position,sort_car_state):
        self.sort_car_position=sort_car_position
        self.sort_car_state=sort_car_state
class Sorting_Vehicle_Management_Panel(wx.Panel):
    def __init__(self, parent,log, id=wx.ID_ANY, title="", pos=wx.DefaultPosition,
                 size=(700,650), style=wx.DEFAULT_FRAME_STYLE):
        wx.Panel.__init__(self, parent)
        self._flags = 0
        self.log=log
        self.sorting_car_state_name='ALL'
        self.sorting_car_position_name='ALL'
        # self.SetIcon(GetMondrianIcon())
        # self.SetMenuBar(self.CreateMenuBar())
        self._leftWindow1 = wx.adv.SashLayoutWindow(self, 101, wx.DefaultPosition,
                                                wx.Size(230, 1000), wx.NO_BORDER |
                                                wx.adv.SW_3D | wx.CLIP_CHILDREN)
        self._leftWindow1.SetDefaultSize(wx.Size(250, 1000))
        self._leftWindow1.SetOrientation(wx.adv.LAYOUT_VERTICAL)
        self._leftWindow1.SetAlignment(wx.adv.LAYOUT_LEFT)
        self._leftWindow1.SetSashVisible(wx.adv.SASH_RIGHT, True)
        self._leftWindow1.SetExtraBorderSize(10)
        self._pnl = 0
        self.remainingSpace = Sorting_Vehicle_Management_Grid(self,self.log)
        self.ID_WINDOW_TOP = 100
        self.ID_WINDOW_LEFT1 = 101
        self.ID_WINDOW_RIGHT1 = 102
        self.ID_WINDOW_BOTTOM = 103
        self._leftWindow1.Bind(wx.adv.EVT_SASH_DRAGGED_RANGE, self.OnFoldPanelBarDrag,
                               id=100, id2=103)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.ReCreateFoldPanel(0)
    def OnSize(self, event):
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.remainingSpace)
        event.Skip()
    def OnQuit(self, event):
        self.Destroy()
    def OnToggleWindow(self, event):
        self._leftWindow1.Show(not self._leftWindow1.IsShown())
        # Leaves bits of itself behind sometimes
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.remainingSpace)
        self.remainingSpace.Refresh()
        event.Skip()
    def OnFoldPanelBarDrag(self, event):
        # if event.GetDragStatus() == wx.SASH_STATUS_OUT_OF_RANGE:
        #     return
        if event.GetId() == self.ID_WINDOW_LEFT1:
            self._leftWindow1.SetDefaultSize(wx.Size(event.GetDragRect().width, 1000))
        # Leaves bits of itself behind sometimes
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.remainingSpace)
        self.remainingSpace.Refresh()
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

        # item = self._pnl.AddFoldPanel("按分检车工位查询", False, foldIcons=Images)
        # self.select_position = wx.StaticText(item, -1, label="选择查询工位：")
        # self._pnl.AddFoldPanelWindow(item, self.select_position)
        # position=self.GetSortingCarPosition()
        # self.position_combox = wx.ComboBox(item, 500, "", (50, 50), (110, -1), position, wx.CB_DROPDOWN)
        # # self.Bind(wx.EVT_COMBOBOX_DROPDOWN, self.GetSortingCarPosition, self.position_combox)  # 下拉事件，点击该事件时，刷新该combobox
        # self.Bind(wx.EVT_COMBOBOX, self.SelectSortCarPosition, self.position_combox)
        # self._pnl.AddFoldPanelWindow(item, self.position_combox,spacing=1)
        # # self._pnl.AddFoldPanelSeparator(item)

        item = self._pnl.AddFoldPanel("按分检车工位查询", False, foldIcons=Images)
        self.radio1 = wx.RadioButton(item, ID_CNC_POSITION, "&加工中心下料")
        self.radio1.Bind(wx.EVT_RADIOBUTTON, self.SelectCNCPosition)
        self._pnl.AddFoldPanelWindow(item, self.radio1, fpb.FPB_ALIGN_WIDTH, fpb.FPB_DEFAULT_SPACING, 10)
        self.radio2 = wx.RadioButton(item, ID_SORTING_BEFORE_M, "&模压前分拣")
        self.radio2.Bind(wx.EVT_RADIOBUTTON, self.SelectSortPosition)
        self._pnl.AddFoldPanelWindow(item, self.radio2, fpb.FPB_ALIGN_WIDTH, fpb.FPB_DEFAULT_SPACING, 10)
        self.radio3 = wx.RadioButton(item, ID_QUALITY_TESTING, "&质量检查")
        self.radio3.Bind(wx.EVT_RADIOBUTTON, self.SelectQualityPosition)
        self._pnl.AddFoldPanelWindow(item, self.radio3, fpb.FPB_ALIGN_WIDTH, fpb.FPB_DEFAULT_SPACING, 10)
        self.radio4 = wx.RadioButton(item, ID_SPARE, "&未分配")
        self.radio4.Bind(wx.EVT_RADIOBUTTON, self.SelectSparePosition)
        self._pnl.AddFoldPanelWindow(item, self.radio4, fpb.FPB_ALIGN_WIDTH, fpb.FPB_DEFAULT_SPACING, 10)
        # self._pnl.AddFoldPanelSeparator(item)
        self._single1 = wx.RadioButton(item, ID_All_POSITION, "&查看全部工位")
        self._single1.Bind(wx.EVT_RADIOBUTTON, self.SelectAllPosition)
        self._pnl.AddFoldPanelWindow(item, self._single1, fpb.FPB_ALIGN_WIDTH, fpb.FPB_DEFAULT_SPACING, 10)
        self._pnl.AddFoldPanelSeparator(item)

        item = self._pnl.AddFoldPanel("按分检车状态查询", False, foldIcons=Images)
        self.sorting_car_state = wx.StaticText(item, -1, label="选择查询状态：")
        self._pnl.AddFoldPanelWindow(item, self.sorting_car_state)
        state=self.GetSortingCarState()
        self.sorting_car_combox = wx.ComboBox(item, 500, "", (50, 50), (110, -1), state, wx.CB_DROPDOWN)
        # self.Bind(wx.EVT_COMBOBOX_DROPDOWN, self.RefreshComboboxDropdown, self.sorting_car_combox)  # 下拉事件，点击该事件时，刷新该combobox
        self.Bind(wx.EVT_COMBOBOX, self.SelectSortCarState, self.sorting_car_combox)
        self._pnl.AddFoldPanelWindow(item, self.sorting_car_combox)
        self._pnl.AddFoldPanelSeparator(item)
        self._leftWindow1.SizeWindows()
        self.sorting_car_combox.SetValue('ALL')
    def GetSortingCarState(self):
        state_list=['ALL']
        if Is_Database_Connect():
            cursor = DB.cursor()
            cursor.execute(
                "select `state_name` from `info_car_state_online` where 1")
            record = cursor.fetchall()
            for i in range(len(record)):
                state_list.append(record[i][0])
        return state_list
    # def RefreshComboboxDropdown(self,eve):
    #     state=self.GetSortingCarState()
    #     self.sorting_car_combox.Clear()
    #     for i in range(len(state)):
    #         self.sorting_car_combox.Append(state[i])
    def SelectSortCarPosition(self,eve):
        self.sorting_car_position_name = eve.GetString()
        self.Refresh_Grid()
    def SelectSortCarState(self,eve):
        self.sorting_car_state_name = eve.GetString()
        self.Refresh_Grid()
    def SelectCNCPosition(self,event):
        self.sorting_car_position_name='加工中心下料'
        self.Refresh_Grid()
    def SelectSortPosition(self,event):
        self.sorting_car_position_name = '模压前分拣'
        self.Refresh_Grid()
    def SelectQualityPosition(self,event):
        self.sorting_car_position_name='质量检查'
        self.Refresh_Grid()
    def SelectSparePosition(self,event):
        self.sorting_car_position_name='未分配'
        self.Refresh_Grid()
    def SelectAllPosition(self,event):
        self.sorting_car_position_name = 'ALL'
        self.Refresh_Grid()
    def Refresh_Grid(self):
        self.remainingSpace.SetValue(self.sorting_car_position_name,self.sorting_car_state_name)
        self.remainingSpace.MyRefresh()
    def OnCalSelChanged(self,eve):
        pass
        # t1 = str(self.cal.GetDate())
        # t2 = t1.split(' ')
        # t3 = t2[0].split('/')
        # t4 = t3[2], t3[0], t3[1]
        # dt = ''
        # start_time = dt.join(t4)
        # start_time1 = '20'+start_time
        # if self.remainingSpace.GetSelection() == 0:
        #     self.remainingSpace.pvc_workposition_right_show1.cnc_workposition_right_grid.SetValue(start_time1)
        #     self.remainingSpace.pvc_workposition_right_show1.cnc_workposition_right_grid.MyRefresh()
        # if self.remainingSpace.GetSelection() == 1:
        #     self.remainingSpace.pvc_workposition_right_show2.grid.Cnc_Workposition_Order_display(start_time1)
        #     self.remainingSpace.pvc_workposition_right_show2.tree_panel.TreeCtrl_Refresh(start_time1)
        # self.log.WriteText(
        #     "天外天系统收到操作员控制指令，ZX_Pane.py 开始执行工位工单日期查询操作，日期：" + str(start_time1) +  "\r\n")
    def OnTodayQuery(self,eve):
        pass
        # today=datetime.date.today().strftime('%Y%m%d')
        # if self.remainingSpace.GetSelection() == 0:
        #     self.remainingSpace.pvc_workposition_right_show1.cnc_workposition_right_grid.SetValue(today)
        #     self.remainingSpace.pvc_workposition_right_show1.cnc_workposition_right_grid.MyRefresh()
        # if self.remainingSpace.GetSelection() == 1:
        #     self.remainingSpace.pvc_workposition_right_show2.grid.Cnc_Workposition_Order_display(today)
        #     self.remainingSpace.pvc_workposition_right_show2.tree_panel.TreeCtrl_Refresh(today)
        # self.log.WriteText(
        #     "天外天系统收到操作员控制指令，ZX_Pane.py 开始执行工位工单日期查询操作，日期：" + str(today) + "\r\n")
    def OnYesterdayQuery(self,eve):
        pass
        # today = datetime.date.today()
        # oneday = datetime.timedelta(days=1)
        # yesterday = (today - oneday).strftime('%Y%m%d')
        # if self.remainingSpace.GetSelection() == 0:
        #     self.remainingSpace.pvc_workposition_right_show1.cnc_workposition_right_grid.SetValue(yesterday)
        #     self.remainingSpace.pvc_workposition_right_show1.cnc_workposition_right_grid.MyRefresh()
        # if self.remainingSpace.GetSelection() == 1:
        #     self.remainingSpace.pvc_workposition_right_show2.grid.Cnc_Workposition_Order_display(yesterday)
        #     self.remainingSpace.pvc_workposition_right_show2.tree_panel.TreeCtrl_Refresh(yesterday)
        # self.log.WriteText(
        #     "天外天系统收到操作员控制指令，ZX_Pane.py开始执行工位工单日期查询操作，日期：" + str(yesterday) + "\r\n")
    def OnBYesterdayQuery(self,eve):
        pass
        # today = datetime.date.today()
        # twoday = datetime.timedelta(days=2)
        # Byesterday = (today - twoday).strftime('%Y%m%d')
        # if self.remainingSpace.GetSelection() == 0:
        #     self.remainingSpace.pvc_workposition_right_show1.cnc_workposition_right_grid.SetValue(Byesterday)
        #     self.remainingSpace.pvc_workposition_right_show1.cnc_workposition_right_grid.MyRefresh()
        # if self.remainingSpace.GetSelection() == 1:
        #     self.remainingSpace.pvc_workposition_right_show2.grid.Cnc_Workposition_Order_display(Byesterday)
        #     self.remainingSpace.pvc_workposition_right_show2.tree_panel.TreeCtrl_Refresh(Byesterday)
        # self.log.WriteText(
        #     "天外天系统收到操作员控制指令，ZX_Pane.py开始执行工位工单日期查询操作，日期：" + str(Byesterday) + "\r\n")
    def OnBBYesterdayQuery(self,eve):
        pass
        # today = datetime.date.today()
        # threeday = datetime.timedelta(days=3)
        # BByesterday = (today - threeday).strftime('%Y%m%d')
        # if self.remainingSpace.GetSelection() == 0:
        #     self.remainingSpace.pvc_workposition_right_show1.cnc_workposition_right_grid.SetValue(BByesterday)
        #     self.remainingSpace.pvc_workposition_right_show1.cnc_workposition_right_grid.MyRefresh()
        # if self.remainingSpace.GetSelection() == 1:
        #     self.remainingSpace.pvc_workposition_right_show2.grid.Cnc_Workposition_Order_display(BByesterday)
        #     self.remainingSpace.pvc_workposition_right_show2.tree_panel.TreeCtrl_Refresh(BByesterday)
        # self.log.WriteText(
        #     "天外天系统收到操作员控制指令，ZX_Pane.py开始执行工位工单日期查询操作，日期：" + str(BByesterday) + "\r\n")
