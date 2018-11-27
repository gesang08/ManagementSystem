#!/usr/bin/env python
# _*_ coding: UTF-8 _*
#20180726B:
#GQ:在schedule面板中增加 加载订单面积文本框及批次订单面积文本框,将订单信息显示出来
#20180726C:
#GQ:建立一个十秒钟时间事件，用来更新订单优先级
#GQ:将排产面积及批次面积显示出来，当修改数据时，将修改的值添加到数据库中
#20180726D:
#GQ:显示订单总数，订单总面积，组件总数
#20180726E:
#GQ:点击添加，移除，全部添加，全部移除，把对应订单的状态修改为26，订单可以移到右边或移回来
#20180726F:
#GQ:点击立即排产，将数据库中状态为26的全部加入到生产表单内，并进行排样
#20180727A:
#GQ:点击排产时，将右侧grid更新，将排样加入到线程中
#20180727B:
#点击自动加载，将加载面积阈值内的订单状态按批次面积放到右边表格中（状态为26），
# 同时将批次更新到订单表单的Production_batch表单内
#20180727C:
#GQ:合入打包程序，若自动加载后的订单还想移除，移除时把状态改回来，同时修改production_batch为0，全部加载也一样
#20180727D:
#GQ：在界面增加一个排产时间
#GQ:点击计划排产，将当前排产面积，排产批次面积，排产时间更新到系统参数表单内
#20180727E:
#GQ:将类内增加日志功能
#20180728A:
#GQ:修改YLP打包程序的调用方法，因修改了数据库字段，所以修改向在线表单加载订单的程序
#20180729A:
#GQ: 点击自动加载时，加入到右边表格中的数据应该是按照同门型刀的原则加载的，而不是仅仅按照优先级加载
#20180729B:
#GQ:修改完成排样的订单的first_day，当前零件完成排样，将当前零件对应的部件，组件，订单均填上first_day
#20180730B:
#GQ:修改点击自动加载按钮触发的事件，自动加载应该按之前商量的优先添加优先级高的同门型订单，并分好批次
#20180731b:
#GQ:批次计算有问题
#20180731c：
#发现右侧的部件数显示的不对
#GQ:将界面上的日历选择以及今天明天后天绑定事件，使其可以点击并存储
#20180801b:
#GQ:将排样与加载分开，但都在线程里进行
#20180801E:
#GQ:将界面上应该更新的东西更新
#点击开始排产，建立线程，加载订单，时间事件监控数据库，若可以排样，则调用线程里的排样函数
#20180806a:
#GQ:全部加载时不管总面积的限制，按批次加载，自动加载按面积限制加载，选择加载，点击立即排产时才算一个批次
#20180806b:
#GQ:每天的产量几百平米包含散板，所以直接加载的时候，不论全部加载还是自动加载，全部都加入到待排样表单中，把不符合条件的摘取到临时待排样表单中
#GQ:在点击自动加载或全部加载时，将制单操作员添加到订单表单中
#若为玻璃门，给一个优先级为20
#20180811a:
#GQ:在更新订单表单中的数据库状态时，就将制单操作员id更新到订单表单中，已完成,向待排样表单中填写的状态值不对，已解决
#GQ:修改了AUI.py文件，去掉了实例化该类时，传入的操作员id，改为登录时，调用该类下的一个方法，传入操作员id
#20180811b:
#GQ:在待排样表单中添加一个批次字段，获取到可以加载的订单时，同时将批次也获取到
#GQ:应将production_batch添加到待排样表单
#20180811c:
#GQ:修改排样部分的程序，从待排样表单中选取同一批次的零件，进行排样
#20180813a:
#GQ:点击立即排产时，排产结束后，将制单编号，排产日期，创建时间，操作员,批次数，工单数，批次包含的订单填到对应的表单中
#20180814a:
#GQ:1709,1711,1758三个门型进散板
#20180818a:
#在work_cnk_query表单内增加一个字段，Schedule_hour排产具体时间（几点）
#GQ:计划排样时，订单不能进入在线库，但是要填写排产查询表单，制单编号，排产日期，创建时间，排产时间点，操作员，订单总数，订单总面积，总批次数，批次包含的订单数
#20180818b:
#GQ:从不在线表单向在线表单加载数据时，部件表单忘记读取是否为异型字段
#20180818c:
#加载时，填写查询表单时，将对应的批次面积，玻璃门数量，含有的素板，单面板，格子板的数量，散板，异型的数量，罗马柱，楣板的数量填到对应的查询表单中
#20180824a:
#GQ:加载订单时，除了考虑门型复杂度，优先级，同刀型订单，还要考虑包含压条的门板面积是否达到设定值，仿古面积是否达到设定值
#1.在界面上增加压条面积，仿古面积,###############在系统参数表单内增加两条数据
#2.首先，读取订单信息时，将对应的压条面积与仿古面积也读出来
#3.找到同刀型的订单后，从同刀型的订单中筛选满足压条面积与仿古面积条件的订单
#20180825a:
#GQ:####################在查询表单内增加两个字段，压条面积，仿古面积
#20180825b:
#GQ:修改排样部分的程序
#20180827a:
#GQ:在加载订单时，将顶线腰线脚线的状态置为72，压条的状态置为65
#20180827b:
#GQ:抓取订单时，读取order_type字段
#20180828a：
#GQ:抓取订单时，应读取压条面积以及仿古面积
#20180901a:
#GQ:设置一个原材料板材库，加载订单时，也要考虑到原材料板材
#自动加载
#1.先获取到所有该加载的订单
#2.判断订单是否是加急的，若是，记录加急的订单编号，订单面积，压条面积，仿古面积，各种厚度的板材面积，将此订单状态改为26
#3.加急的加载完之后，将加急订单按订单面积降序排列，找到面积大的加急订单对应的同刀型门型进行加载，若当前没有加急的订单，则选择原列表中优先级最高的那个订单
#对应的同刀型进行加载
#4.加载时判断 ：若板材面积(优先判断)超了，也不加载此订单,若压条面积超了，则不加载此订单，若仿古面积超了，则不加载此订单
#20180901b:
#GQ:增加压条偏差阈值，仿古偏差阈值
#20180903a:
#GQ:点击立即排产时，首先加载数据，先将要进散板(非18厚度的，门型（查看组件表单）)的整单加入到临时待排样表单（记录该订单编号填到查询表单中），再挑选只有压条的订单，修改该订单及以下的零件的初始状态
#再将剩余订单分批次，加载即可
#20180903b:
#GQ:将订单分为进散板的，只含有顶线腰线脚线的以及其他的，之后对其他的进行分批次(也要找同刀型的)，记录批次订单编号，之后再加载
#看数据库中的single_double字段，若该字段为1，则代表走散板(所有素板进散板)
#20180904a:
#GQ:在界面右侧增加提示信息：当前压条面积，当前仿古面积，当前不同厚度的板材库存（18单面板，素板，格子板）
#20180904b:
#GQ:点击移除时，将右侧对应的信息显示更新
#20180904c:
#GQ:初始化时，右侧界面的显示也该有值就有值，而不应该为0
#GQ:从数据库里找到状态为26的订单，统计压条面积仿古面积以及各种板材数量
#20180904d：
#GQ:板材库存以数量来显示，而不是面积
#20180904e:
#GQ:点击自动加载前，把对应的状态为26的订单先改为25，然后再加载
#GQ:点击选择加载，加载完之后界面更新时，统计右侧的界面信息，全部加载也一样
#20180905a:
#GQ:把手，拉直器，铜条玻璃，普通玻璃，推拉槽，合页
#20180905b:
#GQ:点击立即排产，不排，十秒钟之后右边界面又显示出来刚排产的订单
#20180907a:
#GQ:整套组件应进散板
#GQ:进散板的零件多添加了一个single_double字段
#20180908a:
#GQ:当一个订单只含有线条时，应将此订单编号添加到查询表单中
#20180910a:
#GQ:进散板的门板，楣板，罗马柱给初始状态40，整套组件给最终状态130
#20180915a:
#GQ:解决界面上输入信息校验的问题
#20180915b:
#GQ:开始编写门店管理界面
#GQ:编写门店门型管理界面
#GQ:从order_company_info表单中将经销商读出来，查看info_dealer_door_type表单内有无该经销商，没有的话将该经销商插入到
#info_dealer_door_type表单内，然后再显示
#20180916a:
#ZX:左侧排产界面的toppanel显示问题。
#20180916b:
#GQ:将界面显示出来
#20180917a:
#GQ:界面上不需要显示remarks，向info_dealer_door_type表单中插入数据时，将remark字段也插入，否则会有警告
#20180917b:
#GQ:将界面上显示的一些按钮功能完成
#状态为0：激活门店  10：不常用门店
#20180918a：
#GQ:排样时若出现断电问题，应做对应的处理，设置一个排样的零时表单，生成工单时，零件库，查询表单都要有个零时状态
#监控零件表单中的状态，若状态出现26的零件，且此时不在排样，则从查询表单中找到最后立即排产的记录，将对应订单的状态修改为26，并将其挪到
#不在线表单中
#20180918b:
#GQ:创建零时工位工单表单,开始排产时，向查询表单更新一个状态2：开始排产的状态
#20180918c:
#GQ:加载时更新查询表单的状态为2，表示开始排样，更新组件的package_state的状态为1
# 排完样时，更新查询表单的状态为5，将,package状态改为0,将工单从零时表单挪到工位工单表单中
#20180919c:
#GQ:开始编写品牌门型管理界面
#20180919d:
#GQ:编写门店品牌管理界面(差支付管理与新增品牌，新增门店)
#20180920a:
#GQ:编写门店支付管理界面
#20180924a:
#GQ:在门店支付管理界面中的左边一栏里，加入了门店的一些信息以及可以管理门店支付方式的按钮
#20180925a:
#GQ:点击编辑按钮，弹出输入密码对话框，若密码输入正确，则显示两个按钮，同时支付方式使能
#增加修改定金比例功能
#20180925b:
# 1.多少个订单做压条，多少个订单做仿古，做压条的订单面积,仿古面积（排产时统计）
#2.需要打孔的门板面积，涉及的订单个数，涉及多少个门板（排产时统计）
#20180925c:
#GQ:修改排产部分的统计信息功能，统计的应为18素板多少床，123多少床，456多少床，玻璃门多少床（排样时统计）
#20180926a:
#GQ:更新网格的时候，不应把原来选择了的更新为初始状态
#20180926b:
#GQ:发现支付管理界面出现重复的现象
#20180926c:
#GQ:支付管理界面读取的是Payment字段，这个字段最终会变为5，所以新增加一个字段，来判断支付方式pay_type
#20180927a:
#GQ:解决加载时整套组件信息丢失的问题
#20180927b:
#GQ:解决弧形压条加的不对的问题
#20180927c:
#GQ:在界面上增加总计栏
#20180927d：
#GQ:界面上左边栏里的支付方式以及支付比率等应填写初始值
#20180927e:
#GQ:在表格的末尾增加一行明细，双击明细后，弹出当月的所有合同信息
#20180928a:
#GQ:增加明细功能，同时多显示一个合同号
#20180928b:
#GQ:在总计一栏里增加明细选项，点击该选项时，将所有时间内的合同显示出来
#20180928c:
#GQ:在支付管理界面增加一列：合同数
#20180928d:
#GQ:在明细面板中增加一个Top_Panel,统计一些必要信息
#20180929a:
#GQ:支付管理界面的定金支付不勾选时，支付比率变为1
#20180929b:
#GQ:品牌门型管理，修改门型，数据库没改变
#20180929c:
#GQ:当修改界面上的门型勾选状态时，触发相应事件，修改数据库
#20180929d:
#GQ:去掉确认修改按钮，增加将已设置为不常用的门店设置为常用门店
#20180929e:
#GQ:修改排样部分的程序，检查为什么排样掉不下来的问题
#20180930a:
#最后排产完成，才更零件部件组件订单的状态
#GQ:点击立即排产，向排产单表单中增加一个字段，填写的是计算机CPU名称，当读到本机名与数据库中的一致时，才进行断电处理
#20181001a:
#GQ:立即排产与计划排产时，应先排产后加载，计划排产一个状态，立即排产一个状态
#GQ:门店门型管理界面需要增加修改192.168.31.101内对应表单的数据
#GQ:向订单表单添加数据时，增加一个电脑识别号，排产时注意识别号
#GQ:加载前先看一下状态是否为25，如果是才加载，如果不是，刷新界面
#20181005a:
#GQ:解决板材利用率大于1的情况
#GQ:在门店品牌显示界面的Combobox中，显示的应该是未删除的门店，而不是全部
#20181006a:
#GQ:门店框门型，门店框品牌，品牌框门型不仅需要改云端的数据库，还需要改192.168.31.249的数据库
#20181009a:
#GQ:全部移除时，将对应的cpu_index清为0
#20181009b:
#GQ:数据库中增加一个字段，使门店品牌管理界面中出现了remarks字段，已改正
#20181009c:
#GQ:支付管理界面增加显示一个字段，业务经理
#20181014a:
#GQ:排产管理界面最后一栏增加一个总计栏，统计数量
#20181025a:
#GQ:设为不常用门店与设为常用门店时，原来是只修改了info_company表单中的check_state字段，这样会导致显示出来的门店与实际设置的有偏差，
# 应该把info_dealer_door_type表单中的状态也修改了
#20181025b:
#GQ:在门店支付界面中的明细栏里增加一栏支付方式(Financial_audit_remarks)其他支付具体是用什么方式支付的在此体现
#20181027a:
#GQ:去掉了向Info_dealer_brand表单中插入门店的操作，门店注册时已填了，没必要填了
#20181028a:
#修改了去散板的门型套系
#20181030a:
#GQ:门店管理界面，更新表单时，多填写一个是否同步的状态字段
#20181030b:
#GQ:当一个订单内全是非18的烤漆板时，界面出现问题，显示加载0条数据，且右侧界面上的数据一直不消失
#20181031a:
#GQ:没考虑一个订单全是异型的情况，导致排产单中出现状态为2的记录
#20181001a:
#GQ:如果一个订单里同时含有顶线腰线与其他进散板的门型，导致排产单中出现状态为2的记录（缺逻辑）
#20181116a:
#GQ:解决排产的bug:排产完成后，整套组件的长宽高未填写
#GQ:单独下五金件把手，排产完成后，需要把部件表单的状态修改为130，而不是25
#20181116b:
#GQ:圆弧廊桥，双排廊桥,台面廊桥排产时会出现加载0条数据，不应该根据异型字段将其加到散板，应该根据element_type_id字段将其加到散板
#铝拐角，合叶，把手，拉直器的状态应为130,双排廊桥的状态与顶线一样，圆弧廊桥与台面廊桥暂时给的是组装工位的状态
#8482，6046
import wx
from psutil import net_if_addrs
import wx.adv
from wx.adv import Wizard as wiz
from wx.adv import WizardPage, WizardPageSimple
import images
from ZX_Pane import *
from ID_DEFINE import *
from GQ_Layout_2D import *
import time
import datetime
import os, sys
import wx.lib.delayedresult as delayedresult
from wx.adv import CalendarCtrl, GenericCalendarCtrl, CalendarDateAttr
State_Has_Gene_Workorder=5
STATE_IMMEDIATELY_PAY = 5 #现金支付
STATE_MONTHLY_PAY = 10  #月结
STATE_MONTHLY_PAY_OTHER = 13
STATE_DEPOSIT_PAY = 15 #定金支付
STATE_DEPOSIT_PAY_OTHER = 18
STATE_NOT_COMMON_STORE = -1  #不常用门店的状态
STATE_BEGIN_LAYOUT = 2  #开始排产的状态
ELEMENT_SINGLE_BOARD_INDEX=3  #18单面板
ELEMENT_SINGLE_BOARD_INDEX_20=5  #20单面板
ELEMENT_SINGLE_BOARD_INDEX_22=7  #22单面板
ELEMENT_SINGLE_BOARD_INDEX_25=9  #25单面板
ELEMENT_PLAIN_BOARD_INDEX=4  #18素板
ELEMENT_PLAIN_BOARD_INDEX_20=6  #20素板
ELEMENT_PLAIN_BOARD_INDEX_22=8  #22素板
ELEMENT_PLAIN_BOARD_INDEX_25=10 #25素板
ELEMENT_LATICES_BOARD_INDEX_20=16 #20格子板
ELEMENT_LATICES_BOARD_INDEX_22=17  #22格子板
ELEMENT_LATICES_BOARD_INDEX_25=18  #25格子板
ELEMENT_TYPE_DOORKNOB=7  #推拉槽
ELEMENT_TYPE_HINGES=8 #合页
ELEMENT_TYPE_GLASS=10
ELEMENT_TYPE_KNOB=11 #把手
ELEMENT_TYPE_NORMAL_LAYER=15 #普通压条
ELEMENT_TYPE_COPPER_STRIP_GLASS = 16
ELEMENT_TYPE_STRAIGHT = 17 #拉直器
ELEMENT_TYPE_FAKE_BLINDS=13  #假百叶
ELEMENT_TYPE_lVGUAIJIAO=30  #铝拐角###
ELEMENT_TYPE_ARC_BRIDGE=19  #圆弧廊桥########
ELEMENT_TYPE_DOUBLE_BRIDGE=20  #双排廊桥#######
ELEMENT_TYPE_TAIMIAN_BRIDGE=21  #台面廊桥########
ELEMENT_TYPE_GRID=14     #网格
ELEMENT_TYPE_TRUE_BLINDS=12  #真百叶
ELEMENT_TYPE_DOUBLE_COLOR_BAR = 18  #套色压条
STATE_FAKE_BLINDS_MACHINE = 57
STATE_ASSEMBLE_PARTS_MACHINE = 112  #组装状态（先给圆弧和台面廊桥的状态为112）
STATE_ATTACHE_COMPONENT_MACHINE=72  #顶线腰线脚线状态，双排廊桥的状态
STATE_REGULA_LAYOUT=65   #压条状态
STATE_DELIVERY=130
def Is_Database_Connect():
    try:
        global DB
        DB = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0], charset=charset)
        global DB1
        DB1 = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[1], charset=charset)
        return True
    except:
        return False
class Waiting_Scheduling_Grid(gridlib.Grid):
    def __init__(self, parent,log):
        gridlib.Grid.__init__(self, parent, -1,size=(500,600))
        self.log=log
        self.data = []
        gq_record_count = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.load_order_total_num=0
        self.load_order_total_area=0.00
        self.load_sec_total_num=0
        self.field_name = [' ', '订单编号', '优先级', '交货日期', '订单面积','组件数','部件数','门板数','罗马柱个数','楣板数','顶线个数','腰线个数','脚线个数', '经销商', '品牌']
        try:
            db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0], charset=charset)
            cursor = db.cursor()
            cursor.execute(
                "select `Order_id`,`Order_priority`,`Receive_time`,`Order_area`,`Sec_num`,`Part_num`,`Door_num`,`Rome_column_num`,`Lintel_num`,`Top_line_num`,`Waist_line_num`,`Foot_line_num`,`Dealer`,`Brand` from `order_order` where `State`='%s' ORDER BY `Order_priority` desc,`Receive_time`"
                % STATE_SPLIT_ORDER )
            record = cursor.fetchall()
            if record==() or record==None:
                pass
            else:
                for i in range(len(record)+1):
                    if i == len(record): #最后总计
                        inform = [False, '总计', '', '', gq_record_count[0],gq_record_count[1], gq_record_count[2],
                                  gq_record_count[3], gq_record_count[4], gq_record_count[5], gq_record_count[6], gq_record_count[7],
                                  gq_record_count[8], '', '']
                    else:
                        if record[i][3] == None :
                            self.load_order_total_area=0
                            inform = [False, record[i][0], record[i][1], record[i][2].strftime('%m-%d'), 0,
                                      record[i][4], record[i][5],
                                      record[i][6], record[i][7], record[i][8], record[i][9], record[i][10],
                                      record[i][11], record[i][12], record[i][13]]
                        else:
                            for a in range(9):
                                gq_record_count[a]+=record[i][a+3]
                            self.load_order_total_area+=record[i][3]
                            inform = [False, record[i][0], record[i][1], record[i][2].strftime('%m-%d'), record[i][3],
                                      record[i][4], record[i][5],
                                      record[i][6], record[i][7], record[i][8], record[i][9], record[i][10],
                                      record[i][11], record[i][12], record[i][13]]
                        self.load_sec_total_num+=record[i][4]
                    self.data.append(inform)
            db.close()
            self.load_order_total_num=len(record)
            self.table = Wait_Scheduling_Table(self.data,self.field_name)  # 自定义表网格
            self.SetTable(self.table, True)
            self.SetRowLabelSize(0)
            self.SetMargins(0,0)
            self.AutoSizeColumns(False)
            # self.EnableEditing(False)
            self.DisableDragColSize()
            self.DisableDragRowSize()

            # self.Bind(gridlib.EVT_GRID_CELL_CHANGED, self.OnChanged)
            for j in range(len(self.data)):
                for m in range(1,8):
                    self.SetReadOnly(j,m,isReadOnly = True)
        except:
            pass

    # def Is_DBdatabase_Connected(self):
    #     '''
    #     本方法用来连接数据库，避免多次重复连接
    #     :return:
    #     '''
    #     try:
    #         self.db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0],charset=charset)
    #         self.db_produce = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[1],charset=charset)
    #         return True
    #     except:
    #         self.log.WriteText('数据库连接过程中出错请检查用户名、密码等信息  \r\n')
    #         return False
    def My_Refresh(self,check_state):
        '''
        表格刷新
        :return:
        '''
        data = []
        gq_record_count = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.load_order_total_num = 0
        self.load_order_total_area = 0.00
        self.load_sec_total_num = 0
        try:
            db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0], charset=charset)
            cursor = db.cursor()
            cursor.execute(
                "select `Order_id`,`Order_priority`,`Receive_time`,`Order_area`,`Sec_num`,`Part_num`,`Door_num`,`Rome_column_num`,`Lintel_num`,`Top_line_num`,`Waist_line_num`,`Foot_line_num`,`Dealer`,`Brand` from `order_order` where `State`='%s' ORDER BY `Order_priority` desc,`Receive_time`"
                % STATE_SPLIT_ORDER )
            record = cursor.fetchall()
            if record==() or record==None:
                pass
            else:
                for i in range(len(record)+1):
                    if i == len(record): #最后总计
                        inform = [False, '总计', '', '', gq_record_count[0],gq_record_count[1], gq_record_count[2],
                                  gq_record_count[3], gq_record_count[4], gq_record_count[5], gq_record_count[6], gq_record_count[7],
                                  gq_record_count[8], '', '']
                    else:
                        gq_check_state = False
                        for j in range(len(check_state)):
                            if record[i][0] == check_state[j]:
                                gq_check_state = True
                                break
                            elif j == len(check_state) - 1:
                                gq_check_state = False
                        if record[i][3] == None :
                            self.load_order_total_area=0
                            inform = [gq_check_state, record[i][0], record[i][1], record[i][2].strftime('%m-%d'), 0,
                                      record[i][4], record[i][5],
                                      record[i][6], record[i][7], record[i][8], record[i][9], record[i][10],
                                      record[i][11], record[i][12], record[i][13]]

                        else:
                            for a in range(9):
                                gq_record_count[a]+=record[i][a+3]
                            self.load_order_total_area += record[i][3]
                            inform = [gq_check_state, record[i][0], record[i][1], record[i][2].strftime('%m-%d'), record[i][3],
                                      record[i][4], record[i][5],
                                      record[i][6], record[i][7], record[i][8], record[i][9], record[i][10],
                                      record[i][11], record[i][12], record[i][13]]
                        self.load_sec_total_num += record[i][4]
                    data.append(inform)
            db.close()
            self.load_order_total_num = len(record)
            self.table = Wait_Scheduling_Table(data,self.field_name)  # 自定义表网格
            self.SetTable(self.table, True)
            self.SetRowLabelSize(0)
            self.SetMargins(0,0)
            self.AutoSizeColumns(False)
            # self.EnableEditing(False)
            self.DisableDragColSize()
            self.DisableDragRowSize()
            for j in range(len(data)):
                for m in range(1,8):
                    self.SetReadOnly(j,m,isReadOnly = True)
        except:
            pass
class Wait_Scheduling_Table(gridlib.GridTableBase):
    def __init__(self, data,field_name):
        gridlib.GridTableBase.__init__(self)
        self.data=data
        self.field_name=field_name
        self.dataTypes = [gridlib.GRID_VALUE_BOOL,
                            gridlib.GRID_VALUE_STRING,
                            gridlib.GRID_VALUE_NUMBER,
                            gridlib.GRID_VALUE_DATETIME,
                            gridlib.GRID_VALUE_FLOAT + ':6,2',
                            gridlib.GRID_VALUE_NUMBER,
                            gridlib.GRID_VALUE_NUMBER,
                            gridlib.GRID_VALUE_NUMBER,
                            gridlib.GRID_VALUE_NUMBER,
                            gridlib.GRID_VALUE_NUMBER,
                            gridlib.GRID_VALUE_NUMBER,
                            gridlib.GRID_VALUE_NUMBER,
                            gridlib.GRID_VALUE_NUMBER,
                            gridlib.GRID_VALUE_TEXT,
                            gridlib.GRID_VALUE_TEXT,
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
        return self.dataTypes[col]

    def CanGetValueAs(self, row, col, typeName):
        colType = self.dataTypes[col].split(':')[0]
        if typeName == colType:
            return True
        else:
            return False

    def CanSetValueAs(self, row, col, typeName):
        return self.CanGetValueAs(row, col, typeName)
class Begin_Scheduling_Grid(gridlib.Grid):
    def __init__(self, parent,log):
        gridlib.Grid.__init__(self, parent, -1,size=(600,-1))
        self.log=log
        self.data = []
        gq_record_count = [ 0, 0]
        self.field_name = [' ', '订单编号', '优先级', '交货日期', '部件数', '门板数']
        self.scheduling_order_num = 0
        self.scheduling_order_area = 0.00
        self.cpu_index = ''
        for k, v in net_if_addrs().items():
            # if 'WLAN' in k:
            for item in v:
                address = item[1]
                if '-' in address and len(address) == 17:
                    if self.cpu_index != '':
                        self.cpu_index += ',' + address
                    else:
                        self.cpu_index = address
        try:
            db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0], charset=charset)
            cursor = db.cursor()
            cursor.execute(
                "select `Order_id`,`Order_priority`,`Receive_time`,`Part_num`,`Door_num`,`Order_area` from `order_order` where State='%s'and `CPU_index`in ('%s') ORDER BY `Receive_time`" % (STATE_BEGIN_SCHEDULING,self.cpu_index))
            record = cursor.fetchall()
            if record == () :
                pass
            else:
                for i in range(len(record)+1):
                    if i == len(record): #最后总计
                        inform = [False, '总计', '', '', gq_record_count[0],gq_record_count[1]]
                    else:
                        for a in range(2):
                            gq_record_count[a] += record[i][a + 3]
                        if record[i][5] == None :
                            self.scheduling_order_area=0
                        else:
                            self.scheduling_order_area+=float(record[i][5])
                        inform = [False, record[i][0],record[i][1],  record[i][2].strftime('%m-%d'), record[i][3], record[i][4]]
                    self.data.append(inform)
            db.close()
            self.scheduling_order_num = len(record)
            self.table = Begin_Scheduling_Table(self.data,self.field_name)  # 自定义表网格
            self.SetTable(self.table, True)
            self.SetRowLabelSize(0)
            self.SetMargins(0,0)
            self.AutoSizeColumns(False)
            self.DisableDragColSize()
            self.DisableDragRowSize()
            # self.EnableEditing(False)
            # self.Bind(gridlib.EVT_GRID_CELL_CHANGED, self.OnChanged)
            for j in range(len(self.data)):
                for m in range(1,6):
                    self.SetReadOnly(j,m,isReadOnly = True)
        except:
            pass
    # def Is_DBdatabase_Connected(self):
    #     '''
    #     本方法用来连接数据库，避免多次重复连接
    #     :return:
    #     '''
    #     try:
    #         self.db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0],charset=charset)
    #         self.db_produce = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[1],charset=charset)
    #         return True
    #     except:
    #         self.log.WriteText('数据库连接过程中出错请检查用户名、密码等信息  \r\n')
    #         return False
    def OnChanged(self, evt):
        if self.CanEnableCellControl():
            self.EnableCellEditControl()
    def Scheduling_Refresh(self,check_state):
        self.scheduling_order_num = 0
        self.scheduling_order_area = 0.00
        self.data = []
        gq_record_count = [0, 0]
        try:
            db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0], charset=charset)
            cursor = db.cursor()
            cursor.execute(
                "select `Order_id`,`Order_priority`,`Receive_time`,`Part_num`,`Door_num`,`Order_area` from `order_order` where `State`='%s' and `CPU_index`in ('%s') ORDER BY `Receive_time`" % (STATE_BEGIN_SCHEDULING,self.cpu_index))
            record = cursor.fetchall()
            if record == ():
                pass
            else:
                for i in range(len(record)+1):
                    if i == len(record): #最后总计
                        inform = [False, '总计', '', '', gq_record_count[0],gq_record_count[1]]
                    else:
                        for a in range(2):
                            gq_record_count[a] += record[i][a + 3]
                        if record[i][5] == None :
                            self.scheduling_order_area=0
                        else:
                            self.scheduling_order_area += float(record[i][5])
                        gq_check_state = False
                        for j in range(len(check_state)):
                            if record[i][0] == check_state[j] :
                                gq_check_state = True
                                break
                            elif j == len(check_state)-1 :
                                gq_check_state = False
                        inform = [gq_check_state, record[i][0], record[i][1], record[i][2].strftime('%m-%d'), record[i][3], record[i][4]]
                    self.data.append(inform)
            db.close()
            self.scheduling_order_num = len(record)
            self.table = Begin_Scheduling_Table(self.data,self.field_name)  # 自定义表网格
            self.SetTable(self.table, True)
            self.AutoSizeColumns(False)
            self.DisableDragColSize()
            # self.EnableEditing(False)
            self.DisableDragRowSize()
            for j in range(len(self.data)):
                for m in range(1,6):
                    self.SetReadOnly(j,m,isReadOnly = True)
        except:
            pass
class Begin_Scheduling_Table(gridlib.GridTableBase):
    def __init__(self,data, field_name):
        gridlib.GridTableBase.__init__(self)
        self.data = data
        self.field_name=field_name
        self.dataTypes = [  gridlib.GRID_VALUE_BOOL ,
                            gridlib.GRID_VALUE_STRING,
                            gridlib.GRID_VALUE_NUMBER,
                            gridlib.GRID_VALUE_STRING,
                            gridlib.GRID_VALUE_NUMBER,
                            gridlib.GRID_VALUE_NUMBER,
                            gridlib.GRID_VALUE_NUMBER,

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
        return self.dataTypes[col]

    def CanGetValueAs(self, row, col, typeName):
        colType = self.dataTypes[col].split(':')[0]
        if typeName == colType:
            return True
        else:
            return False

    def CanSetValueAs(self, row, col, typeName):
        return self.CanGetValueAs(row, col, typeName)
class Scheduling_Panel(wx.Panel):
    def __init__(self,parent,log):
        wx.Panel.__init__(self, parent, -1)
        self.log=log
        self.element_single_board_index= 1000  #18mm单面板数量
        self.element_plain_board_index= 1000  #18mm素板数量
        self.element_latics_board_index= 1000 #18mm格子板数量
        self.element_single_board_index_20= 1000 #20mm单面板数量
        self.element_plain_board_index_20= 1000  #20mm素板数量
        self.element_latics_board_index_20= 1000  #20mm格子板数量
        self.element_single_board_index_22= 1000 #22mm单面板
        self.element_plain_board_index_22= 1000 #22素板
        self.element_latics_board_index_22= 1000 #22格子板
        self.element_single_board_index_25 = 1000  # 25mm单面板
        self.element_plain_board_index_25 = 1000  # 25素板
        self.element_latics_board_index_25 = 1000  # 25格子板
        self.utilization_ratio = 0.8  #利用率
        self.layer_threshold = 5  #压条面积阈值
        self.archaize_threshold = 5  #仿古面积阈值
        self.Operator_ID=0
        self.workorder_id_immediately=0
        self.layout_algorithm = GQ_Layout_Algorithm(self.log)
        self.can_not_load_door_type = ['1709','1711','1714','1715','1725','1740','1744','1745','1746','1747','1748','1752','1758','1763','1791','1792','1793']
        self.finally_knife_threshold = 6
        self.knife_shrink_wide = 2
        self.normal_layout_thickness = 18
        self.gq_count_times = 0
        self.timer = wx.PyTimer(self.GQ_Check_If_Can_Layout)
        self.timer.Start(1000)
        self.waiting_scheduling_grid = Waiting_Scheduling_Grid(self,self.log)
        self.begin_scheduling_grid = Begin_Scheduling_Grid(self,self.log)
        btn_auto=wx.Button(self, -1, "自\r\n动\r\n加\r\n载",size=(40,30))
        self.Bind(wx.EVT_BUTTON, self.On_btn_auto_load, btn_auto)
        btn_add= wx.Button(self, -1, "添\r\n>>\r\n加",size=(40,30))#增加\r\n字符可以使得字符换行。
        self.Bind(wx.EVT_BUTTON, self.On_btn_add_Click, btn_add)
        btn_remove = wx.Button(self, -1, "移\r\n<<\r\n除",size=(40,30))
        self.Bind(wx.EVT_BUTTON, self.On_btn_remove_Click, btn_remove)
        btn_add_all= wx.Button(self, -1, "全\r\n部\r\n添\r\n加",size=(40,30))
        self.Bind(wx.EVT_BUTTON, self.On_btn_add_all_Click, btn_add_all)
        btn_remove_all= wx.Button(self, -1, "全\r\n部\r\n移\r\n除",size=(40,30))
        self.Bind(wx.EVT_BUTTON, self.On_btn_remove_all_Click, btn_remove_all)
        self.btn_scheduling_plan=wx.Button(self,-1,"计划排产")
        self.Bind(wx.EVT_BUTTON, self.On_btn_scheduling_plan, self.btn_scheduling_plan)
        self.btn_scheduling_immediately= wx.Button(self, -1, "立即排产")
        self.Bind(wx.EVT_BUTTON, self.On_btn_scheduling_immediately, self.btn_scheduling_immediately)
        self.waiting_scheduling_grid.Bind(gridlib.EVT_GRID_CELL_CHANGED,self.On_left_change)
        self.begin_scheduling_grid.Bind(gridlib.EVT_GRID_CELL_CHANGED,self.On_right_change)
        label1 = wx.StaticText(self, -1, "订单总数      ")
        label3 = wx.StaticText(self, -1, "当前排产面积 ")
        label_layer = wx.StaticText(self, -1, "当前压条面积 ")
        label_archaize = wx.StaticText(self, -1, "当前仿古面积")
        label_18_plain_board = wx.StaticText(self, -1, "18厚素板数   ")
        label_18_single_board = wx.StaticText(self, -1, "18厚单面板数")
        label_18_latics_board = wx.StaticText(self, -1, "18厚格子板数")
        label_20_plain_board = wx.StaticText(self, -1, "20厚素板数   ")
        label_20_single_board = wx.StaticText(self, -1, "20厚单面板数")
        label_20_latics_board = wx.StaticText(self, -1, "20厚格子板数")
        label_22_plain_board = wx.StaticText(self, -1, "22厚素板数   ")
        label_22_single_board = wx.StaticText(self, -1, "22厚单面板数")
        label_22_latics_board = wx.StaticText(self, -1, "22厚格子板数")
        label_25_plain_board = wx.StaticText(self, -1, "25厚素板数   ")
        label_25_single_board = wx.StaticText(self, -1, "25厚单面板数")
        label_25_latics_board = wx.StaticText(self, -1, "25厚格子板数")
        self.order_count = wx.TextCtrl(self, wx.ID_ANY,size=(40,20),style=wx.TE_READONLY)
        self.order_area = wx.TextCtrl(self, wx.ID_ANY,size=(40,20), style=wx.TE_READONLY)
        self.order_layer_area = wx.TextCtrl(self, wx.ID_ANY,size=(40,20), style=wx.TE_READONLY)
        self.order_archaize_area = wx.TextCtrl(self, wx.ID_ANY,size=(40,20), style=wx.TE_READONLY)
        self.order_18_plain_board = wx.TextCtrl(self, wx.ID_ANY,size=(40,20), style=wx.TE_READONLY)
        self.order_18_single_board = wx.TextCtrl(self, wx.ID_ANY,size=(40,20), style=wx.TE_READONLY)
        self.order_18_latics_board = wx.TextCtrl(self, wx.ID_ANY,size=(40,20), style=wx.TE_READONLY)
        self.order_20_plain_board = wx.TextCtrl(self, wx.ID_ANY,size=(40,20), style=wx.TE_READONLY)
        self.order_20_single_board = wx.TextCtrl(self, wx.ID_ANY,size=(40,20), style=wx.TE_READONLY)
        self.order_20_latics_board = wx.TextCtrl(self, wx.ID_ANY,size=(40,20), style=wx.TE_READONLY)
        self.order_22_plain_board = wx.TextCtrl(self, wx.ID_ANY,size=(40,20), style=wx.TE_READONLY)
        self.order_22_single_board = wx.TextCtrl(self, wx.ID_ANY,size=(40,20), style=wx.TE_READONLY)
        self.order_22_latics_board = wx.TextCtrl(self, wx.ID_ANY,size=(40,20), style=wx.TE_READONLY)
        self.order_25_plain_board = wx.TextCtrl(self, wx.ID_ANY,size=(40,20), style=wx.TE_READONLY)
        self.order_25_single_board = wx.TextCtrl(self, wx.ID_ANY,size=(40,20), style=wx.TE_READONLY)
        self.order_25_latics_board = wx.TextCtrl(self, wx.ID_ANY,size=(40,20), style=wx.TE_READONLY)

        vsizer1 = wx.BoxSizer(wx.VERTICAL)
        vsizer1.Add(btn_auto, proportion=1, flag=wx.ALL, border=1)
        vsizer1.Add(btn_add, proportion=1, flag=wx.ALL, border=1)
        vsizer1.Add(btn_remove, proportion=1, flag=wx.ALL, border=1)
        vsizer1.Add(btn_add_all, proportion=1, flag=wx.ALL, border=1)
        vsizer1.Add(btn_remove_all, proportion=1, flag=wx.ALL, border=1)
        #self.SetSizer(vsizer1)# 添加四个垂直按钮
        xsizer1 = wx.BoxSizer()
        xsizer1.Add(label1, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xsizer1.Add(self.order_count, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xsizer3 = wx.BoxSizer()
        xsizer3.Add(label3, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xsizer3.Add(self.order_area, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xsizer_layer = wx.BoxSizer()  #压条面积仿古面积
        xsizer_layer.Add(label_layer, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xsizer_layer.Add(self.order_layer_area, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xsizer_arcahize = wx.BoxSizer()
        xsizer_arcahize.Add(label_archaize, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xsizer_arcahize.Add(self.order_archaize_area, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)

        xsizer_l8_plain_board_num = wx.BoxSizer()  # 18mm素板数量，单面板数量格子板数量
        xsizer_l8_plain_board_num.Add(label_18_plain_board, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xsizer_l8_plain_board_num.Add(self.order_18_plain_board, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xsizer_l8_single_board_num = wx.BoxSizer()  # 18mm素板数量，单面板数量格子板数量
        xsizer_l8_single_board_num.Add(label_18_single_board, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xsizer_l8_single_board_num.Add(self.order_18_single_board, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xsizer_l8_latics_board_num = wx.BoxSizer()  # 18mm素板数量，单面板数量格子板数量
        xsizer_l8_latics_board_num.Add(label_18_latics_board, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xsizer_l8_latics_board_num.Add(self.order_18_latics_board, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xsizer_20_plain_board_num = wx.BoxSizer()  # 18mm素板数量，单面板数量格子板数量
        xsizer_20_plain_board_num.Add(label_20_plain_board, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xsizer_20_plain_board_num.Add(self.order_20_plain_board, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xsizer_20_single_board_num = wx.BoxSizer()  # 18mm素板数量，单面板数量格子板数量
        xsizer_20_single_board_num.Add(label_20_single_board, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xsizer_20_single_board_num.Add(self.order_20_single_board, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xsizer_20_latics_board_num = wx.BoxSizer()  # 18mm素板数量，单面板数量格子板数量
        xsizer_20_latics_board_num.Add(label_20_latics_board, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xsizer_20_latics_board_num.Add(self.order_20_latics_board, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xsizer_22_plain_board_num = wx.BoxSizer()  # 18mm素板数量，单面板数量格子板数量
        xsizer_22_plain_board_num.Add(label_22_plain_board, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xsizer_22_plain_board_num.Add(self.order_22_plain_board, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xsizer_22_single_board_num = wx.BoxSizer()  # 18mm素板数量，单面板数量格子板数量
        xsizer_22_single_board_num.Add(label_22_single_board, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xsizer_22_single_board_num.Add(self.order_22_single_board, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xsizer_22_latics_board_num = wx.BoxSizer()  # 18mm素板数量，单面板数量格子板数量
        xsizer_22_latics_board_num.Add(label_22_latics_board, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xsizer_22_latics_board_num.Add(self.order_22_latics_board, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xsizer_25_plain_board_num = wx.BoxSizer()  # 18mm素板数量，单面板数量格子板数量
        xsizer_25_plain_board_num.Add(label_25_plain_board, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xsizer_25_plain_board_num.Add(self.order_25_plain_board, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xsizer_25_single_board_num = wx.BoxSizer()  # 18mm素板数量，单面板数量格子板数量
        xsizer_25_single_board_num.Add(label_25_single_board, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xsizer_25_single_board_num.Add(self.order_25_single_board, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xsizer_25_latics_board_num = wx.BoxSizer()  # 18mm素板数量，单面板数量格子板数量
        xsizer_25_latics_board_num.Add(label_25_latics_board, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xsizer_25_latics_board_num.Add(self.order_25_latics_board, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)

        #创建三个静态文本和相对应的文本框
        xsizer5 = wx.BoxSizer()
        xsizer5.Add(xsizer1, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        xsizer5.Add(xsizer3, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        xsizer5.Add(xsizer_layer, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        xsizer5.Add(xsizer_arcahize, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)

        xsizer_base_material1 = wx.BoxSizer()  #订单包含的不同厚度的素板，单面板，格子板的数量
        xsizer_base_material1.Add(xsizer_l8_plain_board_num, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        xsizer_base_material1.Add(xsizer_20_plain_board_num, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        xsizer_base_material1.Add(xsizer_22_plain_board_num, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        xsizer_base_material1.Add(xsizer_25_plain_board_num, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)

        xsizer_base_material2 = wx.BoxSizer()  # 订单包含的不同厚度的素板，单面板，格子板的数量
        xsizer_base_material2.Add(xsizer_l8_single_board_num, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        xsizer_base_material2.Add(xsizer_20_single_board_num, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        xsizer_base_material2.Add(xsizer_22_single_board_num, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        xsizer_base_material2.Add(xsizer_25_single_board_num, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)

        xsizer_base_material3 = wx.BoxSizer()  # 订单包含的不同厚度的素板，单面板，格子板的数量
        xsizer_base_material3.Add(xsizer_l8_latics_board_num, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        xsizer_base_material3.Add(xsizer_20_latics_board_num, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        xsizer_base_material3.Add(xsizer_22_latics_board_num, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        xsizer_base_material3.Add(xsizer_25_latics_board_num, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)

        hbox=wx.BoxSizer()
        hbox.Add(self.btn_scheduling_plan, proportion=1, flag=wx.EXPAND | wx.ALL, border=3)
        hbox.Add(self.btn_scheduling_immediately, proportion=1, flag=wx.EXPAND | wx.ALL, border=3)
        vsizer2 = wx.BoxSizer(wx.VERTICAL)
        vsizer2.Add(xsizer5, proportion=1, flag=wx.EXPAND | wx.ALL, border=3)
        vsizer2.Add(xsizer_base_material1, proportion=1, flag=wx.EXPAND | wx.ALL, border=3)
        vsizer2.Add(xsizer_base_material2, proportion=1, flag=wx.EXPAND | wx.ALL, border=3)
        vsizer2.Add(xsizer_base_material3, proportion=1, flag=wx.EXPAND | wx.ALL, border=3)
        vsizer2.Add(hbox, proportion=1, flag=wx.EXPAND | wx.ALL, border=3)
        vsizer4 = wx.BoxSizer(wx.VERTICAL)
        vsizer4.Add(self.begin_scheduling_grid, proportion=1, flag=wx.EXPAND | wx.ALL, border=3)
        vsizer4.Add(vsizer2, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xsizer6 = wx.BoxSizer()
        hbox=wx.BoxSizer()
        self.Get_Load_Total_Area_And_Batch_area()  # 获得排产面积阈值,单次排产面积阈值,压条面积阈值，仿古面积阈值
        layer_label = wx.StaticText(self, -1, " 压条面积： ")
        choose_layer_area = ['40', '60', '80', '100', '120', '140', '160', '180', '200', '220']  #当天可以排产的压条面积
        self.layer_area = wx.ComboBox(self, 500, str(self.load_area_and_batch_area[4]), (40, 40),
                         (10, -1), choose_layer_area,wx.CB_DROPDOWN)
        self.layer_area.Bind(wx.EVT_COMBOBOX, self.EvtComboBox_Layer_Area)
        self.layer_area.Bind(wx.EVT_TEXT, self.EvtText_Layer_Area)
        artificial_label = wx.StaticText(self, -1, " 仿古面积： ")
        choose_artificial_area = ['40', '60', '80', '100', '120', '140', '160', '180', '200', '220']  # 当天可以排产的仿古面积
        self.artificial_area = wx.ComboBox(self, 500, str(self.load_area_and_batch_area[5]), (40, 40),
                                      (10, -1), choose_artificial_area, wx.CB_DROPDOWN)
        self.artificial_area.Bind(wx.EVT_COMBOBOX, self.EvtComboBox_Artificial_Area)
        self.artificial_area.Bind(wx.EVT_TEXT, self.EvtText_Artificial_Area)
        label1 = wx.StaticText(self, -1, " 订单总数： ")
        self.order_total_num = wx.TextCtrl(self, wx.ID_ANY,size=(10,18),style=wx.TE_READONLY)
        label2 = wx.StaticText(self, -1, " 订单总面积： ")
        self.order_total_sqare = wx.TextCtrl(self, wx.ID_ANY,size=(10,18),style=wx.TE_READONLY)
        label3 = wx.StaticText(self, -1, " 组件总数： ")
        self.section_total_num = wx.TextCtrl(self, wx.ID_ANY,size=(10,18), style=wx.TE_READONLY)
        label4 = wx.StaticText(self, -1, " 加载订单总面积： ")
        choose_order_area = ['200', '400', '600', '800']
        self.load_order_area = wx.ComboBox(self, 500, str(self.load_area_and_batch_area[0]), (40, 40),
                         (10, -1), choose_order_area,wx.CB_DROPDOWN)
        self.load_order_area.Bind(wx.EVT_COMBOBOX, self.EvtComboBox_Order_Total_Area)
        self.load_order_area.Bind(wx.EVT_TEXT, self.EvtText_Order_Total_Area)
        label5 = wx.StaticText(self, -1, " 批次订单面积： ")
        batch_choose_order_area = ['40', '50', '60', '70','80','90','100']
        self.batch_order_area = wx.ComboBox(self, 500, str(self.load_area_and_batch_area[1]), (40, 40),
                         (10, -1), batch_choose_order_area,wx.CB_DROPDOWN)
        self.batch_order_area.Bind(wx.EVT_COMBOBOX, self.EvtComboBox_Order_Batch_Area)
        self.batch_order_area.Bind(wx.EVT_TEXT, self.EvtText_Order_Batch_Area)
        hbox.Add(layer_label, flag=wx.EXPAND | wx.ALIGN_BOTTOM, border=2)
        hbox.Add(self.layer_area, proportion=1, flag=wx.EXPAND | wx.ALL, border=0)
        hbox.Add(artificial_label, flag=wx.EXPAND | wx.ALIGN_BOTTOM, border=2)
        hbox.Add(self.artificial_area, proportion=1, flag=wx.EXPAND | wx.ALL, border=0)
        hbox.Add(label1,flag=wx.EXPAND|wx.ALIGN_BOTTOM,border=2)
        hbox.Add(self.order_total_num,proportion=1,flag=wx.EXPAND| wx.ALL,border=0)
        hbox.Add(label2,flag=wx.EXPAND|wx.ALIGN_BOTTOM,border=2)
        hbox.Add(self.order_total_sqare,proportion=1,flag=wx.EXPAND| wx.ALL,border=0)
        hbox.Add(label3,flag=wx.EXPAND|wx.ALIGN_BOTTOM,border=2)
        hbox.Add(self.section_total_num,proportion=1,flag=wx.EXPAND| wx.ALL,border=0)
        hbox1=wx.BoxSizer()

        hbox1.Add(label4, flag=wx.EXPAND | wx.ALIGN_BOTTOM, border=2)
        hbox1.Add(self.load_order_area, proportion=1, flag=wx.EXPAND | wx.ALL, border=0)
        hbox1.Add(label5, flag=wx.EXPAND | wx.ALIGN_BOTTOM, border=2)
        hbox1.Add(self.batch_order_area, proportion=1, flag=wx.EXPAND | wx.ALL, border=0)
        hbox1.Add(wx.StaticText(self, -1, " 计划排产日期："),flag=wx.ALIGN_BOTTOM,border=2)
        self.calendar_scheduling=PopDateControl(self, -1)
        now_time_str = str(self.load_area_and_batch_area[3])  # 当前时间
        self.calendar_scheduling.textCtrl.SetValue(now_time_str)
        hbox1.Add(self.calendar_scheduling,proportion=2,flag=wx.EXPAND|wx.ALIGN_CENTER,border=5)
        hbox1.Add(wx.StaticText(self, -1, " 计划排产时间："), flag=wx.ALIGN_BOTTOM, border=2)
        self.plan_scheduling_time = wx.ComboBox(self, 500, str(self.load_area_and_batch_area[2]), (40,20),
                                            (10, -1), Scheduling_Time, wx.CB_DROPDOWN)
        self.plan_scheduling_time.Bind(wx.EVT_COMBOBOX, self.EvtComboBox_Plan_Scheduling_Time)
        self.plan_scheduling_time.Bind(wx.EVT_TEXT, self.EvtText_Plan_Scheduling_Time)
        hbox1.Add(self.plan_scheduling_time, proportion=1, flag=wx.EXPAND | wx.ALL, border=0)
        self.btn_today=wx.Button(self,label="为今天计划排产",size=(10,25))
        self.btn_today.Bind(wx.EVT_BUTTON, self.Show_Today_Schedule)
        hbox1.Add(self.btn_today,proportion=1,flag=wx.EXPAND|wx.ALIGN_CENTER,border=5)
        self.btn_tomorrow=wx.Button(self,label="为明天计划排产",size=(10,25))
        self.btn_tomorrow.Bind(wx.EVT_BUTTON, self.Show_Tomorrow_Schedule)
        hbox1.Add(self.btn_tomorrow,proportion=1,flag=wx.EXPAND|wx.ALIGN_CENTER,border=5)
        self.btn_after_tomorrow=wx.Button(self,label="为后天计划排产",size=(10,25))
        self.btn_after_tomorrow.Bind(wx.EVT_BUTTON, self.Show_After_Tomorrow_Schedule)
        hbox1.Add(self.btn_after_tomorrow,proportion=1,flag=wx.EXPAND|wx.ALIGN_CENTER,border=5)
        vbox=wx.BoxSizer(wx.VERTICAL)
        vbox.Add(hbox,proportion=0,flag=wx.EXPAND| wx.ALL,border=1)
        vbox.Add(hbox1,proportion=0,flag=wx.EXPAND| wx.ALL,border=1)
        vbox.Add(self.waiting_scheduling_grid,proportion=1,flag=wx.EXPAND| wx.ALL,border=1)
        xsizer6.Add(vbox, proportion=3, flag=wx.EXPAND | wx.ALL, border=3)
        xsizer6.Add(vsizer1, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        xsizer6.Add(vsizer4, proportion=1, flag=wx.EXPAND | wx.ALL, border=3)
        self.SetSizer(xsizer6)
        self.GQ_Find_All_Can_Plan_Production(STATE_BEGIN_SCHEDULING,1)  #右侧界面信息统计，初始化
        self.Interface_Refresh()
        self.begin_scheduling_state=0
        self.gq_right_check_value = []
        self.gq_left_check_value = []
        self.cpu_index = ''
        for k, v in net_if_addrs().items():
            # if 'WLAN' in k:
            for item in v:
                address = item[1]
                if '-' in address and len(address) == 17:
                    if self.cpu_index != '':
                        self.cpu_index += ',' + address
                    else:
                        self.cpu_index = address
    def On_left_change(self,evt):
        if self.waiting_scheduling_grid.table.GetValue(evt.GetRow(),0) == True :
            self.gq_left_check_value.append(self.waiting_scheduling_grid.table.GetValue(evt.GetRow(), 1))
        else:
            for i in range(len(self.gq_left_check_value)-1,-1,-1):
                if self.gq_left_check_value[i] == self.waiting_scheduling_grid.table.GetValue(evt.GetRow(), 1):
                    del self.gq_left_check_value[i]
    def On_right_change(self,evt):
        if self.begin_scheduling_grid.table.GetValue(evt.GetRow(),0) == True :
            self.gq_right_check_value.append(self.begin_scheduling_grid.table.GetValue(evt.GetRow(), 1))
        else:
            for i in range(len(self.gq_right_check_value)-1,-1,-1):
                if self.gq_right_check_value[i] == self.begin_scheduling_grid.table.GetValue(evt.GetRow(), 1):
                    del self.gq_right_check_value[i]
    def Update_Order_Priority(self):
        '''
        时间事件内更新订单，组件，部件，零件优先级
        :return:
        '''
        error_receive_time = 0
        try:
            db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0], charset=charset)
            cursor = db.cursor()  # 根据订单编号找到订单的收货时间
            cursor.execute("SELECT `Receive_time`,`Order_priority`,`Order_id` from `order_order`WHERE 1")
            order_information = cursor.fetchall()
            if order_information == ():  # 对收货时间进行合理化校验
                pass
            else:
                for i in range(len(order_information)):  ###########################计算订单优先级的调整值
                    if (order_information[i][0] == None):
                        pass
                    else:
                        # self.log.WriteText('下单时收获时间填写有问题，请进行检查  \r\n')
                        now_time_str = str(time.strftime('%Y-%m-%d', time.localtime()))  # 当前时间
                        receive_time_str = str(order_information[i][0].strftime('%Y-%m-%d'))  # 订单收货时间
                        localtime = datetime.datetime.strptime(now_time_str, '%Y-%m-%d')
                        Time = datetime.datetime.strptime(receive_time_str, '%Y-%m-%d')
                        N = (Time - localtime).days  # 收货时间与当前时间的差值
                        if N <= 0:
                            error_receive_time = 1
                            order_priority = REWORK_PRIORITY_VALUE
                        elif N >= MODIFY_NOT_ONLINE_DAY:
                            order_priority = 0
                        else:
                            order_priority = (MODIFY_NOT_ONLINE_DAY - N) * MODIFY_NOT_ONLINE_PRIORITY  # 计算出需修改的优先级
                        ############################更新订单的优先级
                        if (order_information[i][1] < order_priority):
                            cursor.execute(
                                "UPDATE `order_order` SET `Order_priority`= '%s' WHERE `Order_id`='%s' " % (
                                    order_priority, order_information[i][2]))
                            cursor.execute("UPDATE `order_section` SET `Priority`= '%s' WHERE `Order_id`='%s' " % (
                                order_priority, order_information[i][2]))
                            cursor.execute("UPDATE `order_part` SET `Priority`= '%s' WHERE `Order_id`='%s' " % (
                                order_priority, order_information[i][2]))
                            cursor.execute("UPDATE `order_element` SET `Priority`= '%s' WHERE `Order_id`='%s' " % (
                                order_priority, order_information[i][2]))
                db.commit()
                if (error_receive_time == 1):
                    pass
                    # self.log.WriteText('天外天系统正在运行调整订单优先级的程序, 出现订单收货时间比当前时间还早的情况，请进行检查  \r\n')
                db.close()
        except:
            pass
        self.GQ_Find_All_Can_Plan_Production(STATE_BEGIN_SCHEDULING, 1)
        self.Interface_Refresh()  #界面更新前要获得右边界面记录信息
    def Get_Operator_Id(self,operator_id):
        '''
        该方法用于获得当前登录的操作员id
        :return:
        '''
        self.Operator_ID=operator_id
    def Get_Load_Total_Area_And_Batch_area(self):
        '''
        从数据库中获得排产面积及批次排产面积以及排产时间,排产日期，压条排产面积，仿古排产面积
        :return:
        '''
        self.load_area_and_batch_area=[0,0,0,0,0,0]
        try:
            db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0], charset=charset)
            cursor = db.cursor()
            cursor.execute(
                "select `Program_variable_name`,`Current_value`,`Scheduling_Date` from `info_system_parameter` where `Program_variable_name`='%s'or `Program_variable_name`='%s'or `Program_variable_name`='%s'or `Program_variable_name`='%s' or `Program_variable_name`='%s'or `Program_variable_name`='%s'"
                % ('CNC_Load_Total_Area','CNC_Load_Batch_Area','CNC_Schduling_Date','CNC_Schduling_Time','CNC_Layer_Area','CNC_Artificial_Area') )
            load_area=cursor.fetchall()
            if load_area == () :
                self.log.WriteText('info_system_parameter表单内无排产面积对应记录，请进行检查  \r\n')
            else:
                for i in range(len(load_area)):
                    if load_area[i][0] == 'CNC_Load_Total_Area':
                        self.load_area_and_batch_area[0]=load_area[i][1]
                    elif load_area[i][0] == 'CNC_Load_Batch_Area' :
                        self.load_area_and_batch_area[1] = load_area[i][1]
                    elif load_area[i][0] == 'CNC_Schduling_Time':
                        scheduling_time=str(int(load_area[i][1]))+':00'
                        self.load_area_and_batch_area[2] =scheduling_time
                    elif load_area[i][0] == 'CNC_Schduling_Date':
                        self.load_area_and_batch_area[3] = load_area[i][2]
                    elif load_area[i][0] == 'CNC_Layer_Area':
                        self.load_area_and_batch_area[4] = load_area[i][1]
                    elif load_area[i][0] == 'CNC_Artificial_Area':
                        self.load_area_and_batch_area[5] = load_area[i][1]
                db.close()
        except:
            pass
    def EvtComboBox_Layer_Area(self,evt):
        '''
        将combobox中填的值更新到数据库中，压条面积
        :param evt:
        :return:
        '''
        check_layer_area=evt.GetString()
        try:
            if float(check_layer_area):  #输入的值有效，将值更新到数据库中
                self.Update_System_Parameter_Sheet('',float(check_layer_area),'CNC_Layer_Area')
        except:
            pass
    def EvtText_Layer_Area(self,evt):
        '''
        将combobox中填的值更新到数据库中，压条面积
        :param evt:
        :return:
        '''
        check_layer_area=evt.GetString()
        try:
            if float(check_layer_area):  #输入的值有效，将值更新到数据库中
                self.Update_System_Parameter_Sheet('',float(check_layer_area),'CNC_Layer_Area')
            else:
                pass
        except:
            pass
    def EvtComboBox_Artificial_Area(self,evt):
        '''
        将combobox中填的值更新到数据库中，仿古面积
        :param evt:
        :return:
        '''
        check_artificial_area=evt.GetString()
        try:
            if float(check_artificial_area):  #输入的值有效，将值更新到数据库中
                self.Update_System_Parameter_Sheet('',float(check_artificial_area),'CNC_Artificial_Area')
        except:
            pass
    def EvtText_Artificial_Area(self,evt):
        '''
        将combobox中填的值更新到数据库中，仿古面积
        :param evt:
        :return:
        '''
        check_artificial_area = evt.GetString()
        try:
            if float(check_artificial_area):  # 输入的值有效，将值更新到数据库中
                self.Update_System_Parameter_Sheet('', float(check_artificial_area), 'CNC_Artificial_Area')
        except:
            pass
    def EvtComboBox_Order_Total_Area(self,evt):
        '''
        将combobox中填的值更新到数据库中，加载总面积
        :param evt:
        :return:
        '''
        check_load_area=evt.GetString()
        try:
            if float(check_load_area):  #输入的值有效，将值更新到数据库中
                self.Update_System_Parameter_Sheet(self.calendar_scheduling.textCtrl.GetValue(),float(check_load_area),'CNC_Load_Total_Area')
        except:
            pass
    def EvtText_Order_Total_Area(self,evt):
        '''
        将combobox中填的值更新到数据库中，加载总面积
        :param evt:
        :return:
        '''
        check_load_area = evt.GetString()
        try:
            if float(check_load_area):  # 输入的值有效，将值更新到数据库中
                self.Update_System_Parameter_Sheet(self.calendar_scheduling.textCtrl.GetValue(),float(check_load_area), 'CNC_Load_Total_Area')
        except:
            pass
    def EvtComboBox_Order_Batch_Area(self,evt):
        '''
        将combobox中填的值更新到数据库中，加载批次面积
        :param evt:
        :return:
        '''
        check_batch_load_area = evt.GetString()
        try:
            if float(check_batch_load_area):  # 输入的值有效，将值更新到数据库中
                self.Update_System_Parameter_Sheet(self.calendar_scheduling.textCtrl.GetValue(),float(check_batch_load_area), 'CNC_Load_Batch_Area')
        except:
            pass
    def EvtText_Order_Batch_Area(self,evt):
        '''
        将combobox中填的值更新到数据库中，加载批次面积
        :param evt:
        :return:
        '''
        check_batch_load_area = evt.GetString()
        try:
            if float(check_batch_load_area):  # 输入的值有效，将值更新到数据库中
                self.Update_System_Parameter_Sheet(self.calendar_scheduling.textCtrl.GetValue(),float(check_batch_load_area), 'CNC_Load_Batch_Area')
        except:
            pass
    def EvtComboBox_Plan_Scheduling_Time(self,evt):
        check_plan_time=evt.GetString()
        self.split_time_list=[0,0]
        try:
            if str(check_plan_time):  # 输入的值有效，将值更新到数据库中
                self.split_time_list=check_plan_time.split(':')
                self.Update_System_Parameter_Sheet(self.calendar_scheduling.textCtrl.GetValue(),int(self.split_time_list[0]), 'CNC_Schduling_Time')
        except:
            pass
    def EvtText_Plan_Scheduling_Time(self,evt):
        check_plan_time = evt.GetString()
        try:
            if str(check_plan_time):  # 输入的值有效，将值更新到数据库中
                split_time_list = check_plan_time.split(':')
                self.Update_System_Parameter_Sheet(self.calendar_scheduling.textCtrl.GetValue(), int(split_time_list[0]), 'CNC_Schduling_Time')
        except:
            pass
    def Update_System_Parameter_Sheet(self,scheduling_date,update_value,parameter_name):
        '''
        更新系统参数表单
        :return:
        '''
        try:
            db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0], charset=charset)
            cursor = db.cursor()
            cursor.execute("UPDATE `info_system_parameter` SET `Scheduling_Date`='%s',`Current_value`= '%s' WHERE `Program_variable_name`='%s' " % (scheduling_date,update_value,parameter_name))
            db.commit()
            db.close()
        except:
            pass
    def Show_Today_Schedule(self,evt):
        '''
        按钮事件，点击今天时，显示今天的排产日期
        :param evt:
        :return:
        '''
        now_time_str = str(time.strftime('%d/%m/%Y', time.localtime()))  # 当前时间
        self.calendar_scheduling.textCtrl.SetValue(now_time_str)
    def Show_Tomorrow_Schedule(self,evt):
        today=datetime.date.today()
        tomorrow_day=(today + datetime.timedelta(days=1)).strftime('%d/%m/%Y')
        self.calendar_scheduling.textCtrl.SetValue(tomorrow_day)
    def Show_After_Tomorrow_Schedule(self,evt):
        today = datetime.date.today()
        after_tomorrow_day = (today + datetime.timedelta(days=2)).strftime('%d/%m/%Y')
        self.calendar_scheduling.textCtrl.SetValue(after_tomorrow_day)
    def On_btn_auto_load(self,evt):
        '''
        先把状态为26的改为25
        点击自动加载，将右边的订单按优先级选定给定的面积按批次加到右边来
        :param evt:
        :return:
        '''
        self.GQ_Find_All_Can_Plan_Production(STATE_SPLIT_ORDER,0)  #找到所有可以计划排产的订单
        self.GQ_Load_Urgent_Order(STATE_BEGIN_SCHEDULING)            #加载紧急订单
        self.Record_Other_Can_Load_Order_Id(STATE_BEGIN_SCHEDULING)  #加载其他需加载的订单
        self.Interface_Refresh()
    def On_btn_add_Click(self,evt):
        '''
        选择加载时，将批次置为1
        :param evt:
        :return:
        '''
        try:
            get_left_order_data = self.waiting_scheduling_grid.table.data
            db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0], charset=charset)
            cursor = db.cursor()
            for i in range(len(get_left_order_data)):
                check_value=self.waiting_scheduling_grid.table.GetValue(i,0)
                if check_value==1:
                    order_id=self.waiting_scheduling_grid.table.GetValue(i,1)
                    cursor.execute("SELECT `State` from `order_order`  WHERE `Order_id`='%s'"% order_id)
                    order_state=cursor.fetchone()
                    if order_state != None :
                        if order_state[0] != STATE_SPLIT_ORDER :  #当前订单的状态不是25，刷新界面
                            self.Interface_Refresh()
                        else:
                            cursor.execute("UPDATE `order_order` set `Scheduling_Operator`='%s',`State`='%s',`Production_batch`='%s',`CPU_index`='%s' WHERE `Order_id`='%s' " % (self.Operator_ID,STATE_BEGIN_SCHEDULING,1,self.cpu_index, order_id))
            db.commit()
            db.close()
            self.gq_right_check_value = []
            self.gq_left_check_value = []
        except:
            pass
        self.GQ_Find_All_Can_Plan_Production(STATE_BEGIN_SCHEDULING, 1)
        self.Interface_Refresh()
    def On_btn_remove_Click(self,evt):
        '''
        选择移除时，还要将右侧信息显示更新，压条面积，仿古面积，板材面积，选择加载时，情况一样
        :param evt:
        :return:
        '''
        self.On_Update_Right_Grid(0)  #更新右侧网格内的订单状态
        self.gq_right_check_value = []
        self.gq_left_check_value = []
        self.Interface_Refresh()
    def On_btn_add_all_Click(self,eve):
        try:
            db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0], charset=charset)
            cursor = db.cursor()
            cursor.execute("UPDATE `order_order` set `State`='%s',`CPU_index`='%s' WHERE `State`='%s' " % (STATE_BEGIN_SCHEDULING,self.cpu_index,STATE_SPLIT_ORDER))
            db.commit()
            db.close()
        except:
            pass
        self.GQ_Find_All_Can_Plan_Production(STATE_BEGIN_SCHEDULING, 1)
        self.Interface_Refresh()
    def Interface_Refresh(self):
        '''
        刷新界面上的东西
        :return:
        '''
        try:
            self.begin_scheduling_grid.Scheduling_Refresh(self.gq_right_check_value)
            self.waiting_scheduling_grid.My_Refresh(self.gq_left_check_value)
            self.order_count.SetValue(str(self.begin_scheduling_grid.scheduling_order_num))
            self.order_area.SetValue(str(self.begin_scheduling_grid.scheduling_order_area))
            self.order_total_num.SetValue(str(self.waiting_scheduling_grid.load_order_total_num))  # 左边订单面积，订单数量，组件数量
            self.order_total_sqare.SetValue(str(self.waiting_scheduling_grid.load_order_total_area))
            self.section_total_num.SetValue(str(self.waiting_scheduling_grid.load_sec_total_num))
            self.order_layer_area.SetValue(str(self.record_urgent_order_information[2]))  #仿古面积，压条面积，不同厚度的板材面积
            self.order_archaize_area.SetValue(str(self.record_urgent_order_information[3]))
            self.order_18_plain_board.SetValue(str(self.record_urgent_order_information[5]))
            self.order_18_single_board.SetValue(str(self.record_urgent_order_information[4]))
            self.order_18_latics_board.SetValue(str(self.record_urgent_order_information[6]))
            self.order_20_plain_board.SetValue(str(self.record_urgent_order_information[8]))
            self.order_20_single_board.SetValue(str(self.record_urgent_order_information[7]))
            self.order_20_latics_board.SetValue(str(self.record_urgent_order_information[9]))
            self.order_22_plain_board.SetValue(str(self.record_urgent_order_information[11]))
            self.order_22_single_board.SetValue(str(self.record_urgent_order_information[10]))
            self.order_22_latics_board.SetValue(str(self.record_urgent_order_information[12]))
            self.order_25_plain_board.SetValue(str(self.record_urgent_order_information[14]))
            self.order_25_single_board.SetValue(str(self.record_urgent_order_information[13]))
            self.order_25_latics_board.SetValue(str(self.record_urgent_order_information[15]))
            if len(self.begin_scheduling_grid.data) == 0:
                self.btn_scheduling_immediately.Enable(False)
                self.btn_scheduling_plan.Enable(False)
            else:
                self.btn_scheduling_immediately.Enable(True)
                self.btn_scheduling_plan.Enable(True)
        except:
            pass
    def On_btn_remove_all_Click(self,eve):
        try:
            db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0], charset=charset)
            cursor = db.cursor()
            cursor.execute(
                "UPDATE `order_order` set `State`='%s',`Production_batch`='%s',`Cpu_Index`='0' WHERE `State`='%s'and `Cpu_Index`in ('%s')" % (
                    STATE_SPLIT_ORDER, 0, STATE_BEGIN_SCHEDULING,self.cpu_index))
            db.commit()
            db.close()
        except:
            pass
        self.record_urgent_order_information = [[], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.Interface_Refresh()
    # def Is_DBdatabase_Connected(self):
    #     '''
    #     本方法用来连接数据库，避免多次重复连接
    #     :return:
    #     '''
    #     try:
    #         self.db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0],charset=charset)
    #         self.db_produce = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[1],charset=charset)
    #         return True
    #     except:
    #         self.log.WriteText('数据库连接过程中出错请检查用户名、密码等信息  \r\n')
    #         return False
    def GQ_Find_All_Can_Immediately(self,load_state):
        '''
      找到所有可以立即排产的订单，记录批次面积,记录压条面积，记录仿古面积
      将进散板的整单，只含有线条的整单与其他整单分开
        :return:
        '''
        record_hole_order = []  #记录打孔零件对应的订单号
        self.gq_record_all_knids_of_num = [ 0, 0, 0, 0,0,0,0,0]  #散板(厚度，门型，带拱压条)，异型的数量，罗马柱，楣板的数量，总订单数,门板面积，订单个数，门板数
        try:
            db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0], charset=charset)
            cursor = db.cursor()
            self.all_order_information=[]  #分批次的时候清空了，所以此处备份一下
            self.other_order_information=[] #分批次的同时，向该列表中添加一列批次号
            self.spare_order_information=[]  #进散板的订单，除了加载进在线表单，还要进临时待排样表单
            self.only_has_bar_order_information=[]  #只含有线条的订单，除了加载，还要改状态
            self.record_order_area=0  #记录加载的订单面积
            self.record_layer_area=[0,0,0,0]  #记录加载的压条面积,订单数,加载的仿古面积,订单数
            cursor.execute("SELECT `Order_area`,`Order_id`,`Bar_area`,`Archaize_area`,`Part_num`,`Lintel_num`,`Rome_column_num`,`Door_num`,`Top_line_num`,`Waist_line_num`,`Foot_line_num`,`Sec_num` from `order_order`  WHERE `State`='%s' and `CPU_index`in ('%s') order by `Order_priority` desc"%(load_state,self.cpu_index))
            gq_order_information = cursor.fetchall()
            if gq_order_information==():
                db.close()
            else:
                self.gq_record_all_knids_of_num[4] = len(gq_order_information)
                for i in range(len(gq_order_information)):
                    if gq_order_information[i][0] != None :
                        self.record_order_area += gq_order_information[i][0]
                    if gq_order_information[i][2] != None and gq_order_information[i][2] != 0.0:
                        self.record_layer_area[0] += gq_order_information[i][2]
                        self.record_layer_area[1] += 1
                    if gq_order_information[i][3] != None and gq_order_information[i][3] != 0.0:
                        self.record_layer_area[2] += gq_order_information[i][3]
                        self.record_layer_area[3] += 1
                    if gq_order_information[i][5] == 0 and gq_order_information[i][6] == 0 and gq_order_information[i][7] == 0 and gq_order_information[i][11] != 0 :
                        self.only_has_bar_order_information.append(list(gq_order_information[i]) + [0])  # （一个订单里全是整套组件与顶线腰线脚线或圆弧廊桥，双排廊桥，台面廊桥）
                        for l in range(8, 11):
                            self.gq_record_all_knids_of_num[0] += gq_order_information[i][l]
                    else:#订单里只有门板和其他附件（根据订单编号从零件表单中读出附件数量）
                        kinds_of_bridge_num = 0
                        cursor.execute("SELECT `Element_type_id` from `order_element`  WHERE `Order_id`='%s'" % gq_order_information[i][1])
                        attached_information = cursor.fetchall()
                        if attached_information == () : #没有零件信息
                            pass
                        else:
                            for k in range(len(attached_information)):  #廊桥数量
                                if attached_information[k][0] == ELEMENT_TYPE_ARC_BRIDGE or attached_information[k][0] == ELEMENT_TYPE_DOUBLE_BRIDGE or attached_information[k][0] == ELEMENT_TYPE_TAIMIAN_BRIDGE or attached_information[k][0] == ELEMENT_TYPE_DOORKNOB or attached_information[k][0] == ELEMENT_TYPE_HINGES or attached_information[k][0] == ELEMENT_TYPE_KNOB :
                                    kinds_of_bridge_num+=1
                        cursor.execute("SELECT `Door_thick`,`Door_type`,`Index_of_base_material_thickness`,`Open_way`,`Door_height`,`Door_width`,`heterotype` from `order_part`  WHERE `Order_id`='%s' and (`Element_type_id`<>'%s' and`Element_type_id`<>'%s' and `Element_type_id`<>'%s' and `Element_type_id`<>'%s'and`Element_type_id`<>'%s' and `Element_type_id`<>'%s' and `Element_type_id`<>'%s'and `Element_type_id`<>'%s' and `Element_type_id`<>'%s')" % (gq_order_information[i][1],ELEMENT_TYPE_TOP_LINE,ELEMENT_TYPE_WAIST_LINE,ELEMENT_TYPE_FOOT_LINE,ELEMENT_TYPE_HINGES,ELEMENT_TYPE_DOORKNOB,ELEMENT_TYPE_KNOB,ELEMENT_TYPE_ARC_BRIDGE,ELEMENT_TYPE_DOUBLE_BRIDGE,ELEMENT_TYPE_TAIMIAN_BRIDGE))
                        sec_information = cursor.fetchall()
                        if sec_information == () :
                            pass
                        else:
                            part_thick_num = 0  #组件厚度为非18的数量
                            part_series_num = 0  #组件套系在散板列表中的数量
                            part_material_thick_num = 0  #组件基材类型为素板的数量
                            part_hereotype_num = 0
                            for j in range(len(sec_information)):
                                if sec_information[j][3] != '不开' and sec_information[j][3] != None :
                                    if gq_order_information[i][1] not in record_hole_order :
                                        record_hole_order.append(gq_order_information[i][1])
                                    self.gq_record_all_knids_of_num[5] += (sec_information[j][4] * sec_information[j][5])/1000000
                                    self.gq_record_all_knids_of_num[7] += 1
                                sec_series_split=sec_information[j][1].split('_')
                                if sec_information[j][0] != self.normal_layout_thickness : #非18厚度的
                                    part_thick_num += 1
                                if sec_series_split[1] in self.can_not_load_door_type :  #门型为进散板的门型
                                    part_series_num += 1
                                if sec_information[j][2] == ELEMENT_PLAIN_BOARD_INDEX :  #18mm素板，进散板
                                    part_material_thick_num += 1
                                if sec_information[j][6] == 1 : #单个订单全是异型
                                    part_hereotype_num += 1
                            foot_waist_top_num = gq_order_information[i][8] + gq_order_information[i][9] + gq_order_information[i][10]+kinds_of_bridge_num
                            if part_hereotype_num == gq_order_information[i][4]-foot_waist_top_num or part_series_num == gq_order_information[i][4]-foot_waist_top_num or part_thick_num == gq_order_information[i][4]-foot_waist_top_num or part_material_thick_num == gq_order_information[i][4]-foot_waist_top_num: #该订单应该加到散板，记录散板数量
                                self.spare_order_information.append(list(gq_order_information[i])+[0])
                            else:
                                self.all_order_information.append(list(gq_order_information[i]))
                db.close()
                self.gq_record_all_knids_of_num[6] = len(record_hole_order)
                self.other_order_information = copy.deepcopy(self.all_order_information)
                self.GQ_Get_All_Need_Num(self.spare_order_information)
                self.GQ_Get_All_Need_Num(self.all_order_information)  # 获得玻璃门个数，散板个数，异型个数，罗马柱个数，楣板个数
        except:
            pass
    def GQ_Distribute_Batch_Order(self,modify_state):
        '''
        将订单分批次，从订单中找到同刀型的订单
        :return:
        '''
        cal_batch=1  #分的批次
        currently_load_batch_area = 0
        self.record_batch_order_id = []  #记录批次，批次面积以及批次包含的订单编号
        self.gq_last_signal = 0
        if float(self.batch_order_area.GetValue()) != 0.0 :
            while self.all_order_information != [] :
                self.urgent_record_knife = ['0',None]
                self.GQ_Record_Order_Knife(self.all_order_information[0][1], self.urgent_record_knife)  # 记录刀
                if self.Get_Same_Knife_Order(self.all_order_information):  # 找出同刀型的订单
                    return LOAD_ERROR
                while self.choose_same_knife_order != []:  #找到的同刀型订单,记录面积，判断批次面积是否够
                    currently_load_batch_area += self.choose_same_knife_order[0][0]
                    self.GQ_Update_Can_Plan_Production(cal_batch, self.choose_same_knife_order[0][1],modify_state)
                    for i in range(len(self.other_order_information)):  # 将内存中已加载的订单删除
                        if self.other_order_information[i][1] == self.choose_same_knife_order[0][1]:
                            self.other_order_information[i].append(cal_batch)
                            break
                    if len(self.record_batch_order_id) != cal_batch :  #记录批次，订单面积及订单编号
                        self.record_batch_order_id.append([cal_batch, self.choose_same_knife_order[0][0], self.choose_same_knife_order[0][1]])
                    else:
                        self.record_batch_order_id[cal_batch-1].append(self.choose_same_knife_order[0][1])  # 记录批次对应的订单号
                        self.record_batch_order_id[cal_batch-1][1] += self.choose_same_knife_order[0][0]
                    if currently_load_batch_area >= float(self.batch_order_area.GetValue()):  #批次面积够了
                        left_can_plan_order_area = 0.0
                        for i in range(len(self.all_order_information)):
                            left_can_plan_order_area += self.all_order_information[i][0]
                        if left_can_plan_order_area < 0.5 * float(self.batch_order_area.GetValue()):
                            self.gq_last_signal = 1
                            for i in range(len(self.all_order_information)):
                                self.GQ_Update_Can_Plan_Production(cal_batch, self.all_order_information[i][1],modify_state)
                                for j in range(len(self.other_order_information)):  # 将内存中已加载的订单删除
                                    if self.other_order_information[j][1] == self.all_order_information[i][1]:
                                        self.other_order_information[j].append(cal_batch)
                                        break
                            self.all_order_information=[]
                            self.choose_same_knife_order=[]
                        else:  # 最后剩的零件大于一批的一半
                            cal_batch += 1
                        currently_load_batch_area = 0
                    if self.gq_last_signal == 0 :
                        for i in range(len(self.all_order_information) - 1, -1, -1):  # 将内存中已加载的订单删除
                            if self.all_order_information[i][1] == self.choose_same_knife_order[0][1]:
                                del self.all_order_information[i]
                                break
                        del self.choose_same_knife_order[0]
    def Load_Orders_Online(self,wait_layout_state):
        '''
        向在线表单添加数据，将待排样表单中非18的都加到临时待排样表单中，把零件表单中所有带拱压条加进来
        :return:
        '''
        self.all_load_num = 0
        self.Load_Order_Into_Online_Sheet(0,'work_cnc_before_layout_temporary',self.spare_order_information,wait_layout_state)  #散板
        self.Load_Order_Into_Online_Sheet(1,'work_cnc_before_layout_temporary',self.only_has_bar_order_information,wait_layout_state)  #只含有顶线腰线脚线的
        self.Load_Order_Into_Online_Sheet(2,'work_cnc_before_layout',self.other_order_information,wait_layout_state)
        self.log.WriteText('天外天系统正在运行向待排样数据库添加数据的程序 ：运行正常 加载' + str(self.all_load_num) + '条数据  \r\n')
        return RUN_NORMAL
    def Load_Order_Into_Online_Sheet(self,gq_number,wait_layout_sheet,the_load_order_id,wait_layout_state):
        '''
        根据订单编号将订单加载到order_order_online,order_section_online,order_part_online,order_element_online表单中
        整套组件的也进散板（整套组件时需填写长宽高字段）
        :return:
        '''
        not_meet_condition_door_type_id = []  # 不满足门型条件要求的门型,异型也加进来
        if the_load_order_id == []:
            return LOAD_ERROR
        try:
            db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0], charset=charset)
            db_produce = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[1],charset=charset)
            cursor = db.cursor()
            cursor_produce = db_produce.cursor()
            if gq_number == 2 :
                cursor.execute("UPDATE `work_cnc_workorder_query` set `State`='%s' WHERE `Workorder_id`='%s' " % (
                    STATE_BEGIN_LAYOUT, self.workorder_id_immediately))
            else:
                cursor.execute("UPDATE `work_cnc_workorder_query` set `State`='%s' WHERE `Workorder_id`='%s' " % (
                    State_Has_Gene_Workorder, self.workorder_id_immediately))
            for i in range(len(the_load_order_id)):
                cursor.execute("INSERT INTO `order_order_online`(`discount`,`Archaize_area`,`Bar_area`,`Order_type`,`Scheduling_Operator`,`Contract_id`, `Order_id`, `Contract_C_Time`, `Record_time`, `Receive_time`, `Delivery_time`,`Transport_company`, `Check_number`, `Check_name`, `Customer_address`, `Customer_tel`, `Spare_cust`, `Spare_tel`, `Customer_name`, `Technology_manager_tel`, `Technology_manager_name`, `Financial_manager_tel`, `Financial_manager_name`, `Order_priority`,`specialshaped_price`, `Order_price`,`Charge_price`, `Order_area`, `Sec_type_num`, `Sec_num`,`Lintel_num`,`Rome_column_num`,`Top_line_num`,`Waist_line_num`,`Foot_line_num`,`Door_num`,`Door_area`, `Part_num`, `Ele_num`, `Package_num`, `Package_num_now`,`Edge_type_num`,`Dealer`,`Technical_audit_remarks`,`Price_audit_remarks`,`Financial_audit_remarks`, `State`, `remarks`,`remarkimage`,`Brand`) SELECT `discount`,`Archaize_area`,`Bar_area`,`Order_type`,`Scheduling_Operator`,`Contract_id`, `Order_id`, `Contract_C_Time`, `Record_time`, `Receive_time`, `Delivery_time`,`Transport_company`, `Check_number`, `Check_name`, `Customer_address`, `Customer_tel`, `Spare_cust`, `Spare_tel`, `Customer_name`, `Technology_manager_tel`, `Technology_manager_name`, `Financial_manager_tel`, `Financial_manager_name`, `Order_priority`,`specialshaped_price`, `Order_price`,`Charge_price`, `Order_area`, `Sec_type_num`, `Sec_num`,`Lintel_num`,`Rome_column_num`,`Top_line_num`,`Waist_line_num`,`Foot_line_num`,`Door_num`,`Door_area`, `Part_num`, `Ele_num`, `Package_num`, `Package_num_now`,`Edge_type_num`,`Dealer`,`Technical_audit_remarks`,`Price_audit_remarks`,`Financial_audit_remarks`, `State`, `remarks`,`remarkimage`,`Brand` FROM `order_order`  WHERE `Order_id`='%s'" %
                    the_load_order_id[i][1])
                cursor.execute("INSERT INTO `order_section_online`(`Sec_length`,`Sec_width`,`Sec_height`,`Record_time`, `Contract_id`, `Order_id`, `Order_time`, `Sec_id`, `Sec_name`, `Sec_type`, `Stick_type`, `Priority`, `Sec_light`,`Sec_series`,`Sec_model`, `Sec_color`, `Sec_thick`,`Sec_edge`, `Archaize`, `Index_of_base_material_thickness`,`Sec_num`,`Lintel_num`,`Rome_column_num`,`Foot_line_num`,`Waist_line_num`,`Top_line_num`,`Door_num`, `Door_area`, `Door_price`, `Acce_price`, `Single_price`, `Door_type_num`, `Rom_type_num`, `Euro_type_num`, `Acce_type_num`, `State`, `remarks`) SELECT `Sec_length`,`Sec_width`,`Sec_height`,`Record_time`, `Contract_id`, `Order_id`, `Order_time`, `Sec_id`, `Sec_name`, `Sec_type`, `Stick_type`, `Priority`, `Sec_light`,`Sec_series`,`Sec_model`, `Sec_color`, `Sec_thick`,`Sec_edge`, `Archaize`, `Index_of_base_material_thickness`,`Sec_num`,`Lintel_num`,`Rome_column_num`,`Foot_line_num`,`Waist_line_num`,`Top_line_num`,`Door_num`, `Door_area`, `Door_price`, `Acce_price`, `Single_price`, `Door_type_num`, `Rom_type_num`, `Euro_type_num`, `Acce_type_num`, `State`, `remarks` FROM `order_section` WHERE `Order_id`='%s'" %
                    the_load_order_id[i][1])
                cursor.execute("INSERT INTO `order_part_online`(`heterotype`,`Straightening_device`,`Contract_C_Time`,`Record_time`, `Priority`, `Contract_id`, `Order_id`, `Sec_id`, `Part_id`,`Part_type`,`Same_part_num`, `Door_type`, `Door_color`, `Door_height`, `Door_width`, `Door_thick`, `Archaize`, `Door_area`, `Door_price`,`Extra_charge`, `Bar_type`, `Single_double`,`Texture_direction`,`Element_type_id`,`Interval_width`,`Bottom_part_down`,`Double_color`,`Hole_dire`, `Hole`, `Open_way`, `Edge_type`, `Glass`, `Rom_price`,  `Heart_type`, `State`, `remarks`,`remarkimage`, `is_first`, `Index_of_base_material_thickness`) SELECT `heterotype`,`Straightening_device`,`Contract_C_Time`,`Record_time`, `Priority`, `Contract_id`, `Order_id`, `Sec_id`, `Part_id`,`Part_type`,`Same_part_num`, `Door_type`, `Door_color`, `Door_height`, `Door_width`, `Door_thick`, `Archaize`, `Door_area`, `Door_price`,`Extra_charge`, `Bar_type`, `Single_double`,`Texture_direction`,`Element_type_id`,`Interval_width`,`Bottom_part_down`,`Double_color`,`Hole_dire`, `Hole`, `Open_way`, `Edge_type`, `Glass`, `Rom_price`,  `Heart_type`, `State`, `remarks`,`remarkimage`, `is_first`, `Index_of_base_material_thickness` FROM `order_part` WHERE `Order_id`='%s'" %
                    the_load_order_id[i][1])
                cursor.execute("INSERT INTO `order_element_online`(`Straightening_device`,`Record_time`, `Contract_C_Time`, `Contract_id`, `Order_id`, `Sec_id`, `Part_id`, `Id`, `Priority`, `Color`, `Crosspiece`, `Crosspiece_size`, `Texture_direction`, `Single_double`, `Interval_width`, `Bottom_part_down`, `Glass`, `Handle`, `Element_type_id`, `Board_height`, `Board_width`, `Board_thick`, `Archaize`,`Double_color`, `Open_way`, `Board_type`, `Hole`, `Edge_type`, `Heart_type`,`heterotype`, `Bar_type`, `Index_of_base_material_thickness`,`State`, `Code`, `remarks`) SELECT `Straightening_device`,`Record_time`, `Contract_C_Time`, `Contract_id`, `Order_id`, `Sec_id`, `Part_id`, `Id`, `Priority`, `Color`, `Crosspiece`, `Crosspiece_size`, `Texture_direction`, `Single_double`, `Interval_width`, `Bottom_part_down`, `Glass`, `Handle`, `Element_type_id`, `Board_height`, `Board_width`, `Board_thick`, `Archaize`,`Double_color`, `Open_way`, `Board_type`, `Hole`, `Edge_type`, `Heart_type`,`heterotype`, `Bar_type`, `Index_of_base_material_thickness`,`State`, `Code`, `remarks` FROM `order_element` WHERE `Order_id`='%s'" %
                    the_load_order_id[i][1])
                cursor.execute("UPDATE `order_section_online` SET `Package_state`= '%s' WHERE `Order_id`='%s' " % (1, the_load_order_id[i][1]))
                cursor.execute("UPDATE `order_element_online` SET `State`= '%s' WHERE `Order_id`='%s' and (`Element_type_id`='%s' or `Element_type_id`='%s' or `Element_type_id`='%s'or `Element_type_id`='%s' or `Element_type_id`='%s')" % (
                        STATE_ASSEMBLE_PARTS_MACHINE, the_load_order_id[i][1], ELEMENT_TYPE_GRID,
                        ELEMENT_TYPE_TRUE_BLINDS, ELEMENT_TYPE_DOUBLE_COLOR_BAR,ELEMENT_TYPE_ARC_BRIDGE,ELEMENT_TYPE_TAIMIAN_BRIDGE))  # 网格，真百叶，套色压条，台面廊桥，圆弧廊桥
                cursor.execute("UPDATE `order_element_online` SET `State`= '%s' WHERE `Order_id`='%s' and (`Element_type_id`='%s' or `Element_type_id`='%s' or `Element_type_id`='%s' or `Element_type_id`='%s' or `Element_type_id`='%s' or `Element_type_id`='%s'or `Element_type_id`='%s')" % (
                    STATE_DELIVERY, the_load_order_id[i][1], ELEMENT_TYPE_DOORKNOB,ELEMENT_TYPE_HINGES, ELEMENT_TYPE_GLASS,ELEMENT_TYPE_KNOB,ELEMENT_TYPE_COPPER_STRIP_GLASS,ELEMENT_TYPE_STRAIGHT,ELEMENT_TYPE_lVGUAIJIAO))  # 把手,合页，推拉槽，铝拐角，拉直器
                cursor.execute("UPDATE `order_part_online` SET `State`= '%s' WHERE `Order_id`='%s' and (`Element_type_id`='%s' or `Element_type_id`='%s' or `Element_type_id`='%s' or `Element_type_id`='%s' or `Element_type_id`='%s' or `Element_type_id`='%s'or `Element_type_id`='%s')" % (
                        STATE_DELIVERY, the_load_order_id[i][1], ELEMENT_TYPE_DOORKNOB, ELEMENT_TYPE_HINGES,ELEMENT_TYPE_GLASS, ELEMENT_TYPE_KNOB, ELEMENT_TYPE_COPPER_STRIP_GLASS,ELEMENT_TYPE_STRAIGHT,ELEMENT_TYPE_lVGUAIJIAO))  # 拉直器等修改状态需要把部件的状态也修改回来
                cursor.execute("UPDATE `order_element_online` SET `State`= '%s' WHERE `Order_id`='%s' and (`Element_type_id`='%s' or `Element_type_id`='%s')" % (
                        STATE_REGULA_LAYOUT, the_load_order_id[i][1], ELEMENT_TYPE_NORMAL_LAYER, ELEMENT_TYPE_ARC_LAYER))  #压条
                cursor.execute("UPDATE `order_element_online` SET `State`= '%s' WHERE `Order_id`='%s' and `Element_type_id`='%s'" % (
                        STATE_FAKE_BLINDS_MACHINE, the_load_order_id[i][1], ELEMENT_TYPE_FAKE_BLINDS))  #假百叶
                cursor.execute("UPDATE `order_element_online` SET `State`= '%s' WHERE `Order_id`='%s' and (`Element_type_id`='%s' or `Element_type_id`='%s' or `Element_type_id`='%s'or `Element_type_id`='%s')" % (
                        STATE_ATTACHE_COMPONENT_MACHINE, the_load_order_id[i][1], ELEMENT_TYPE_TOP_LINE,
                        ELEMENT_TYPE_WAIST_LINE, ELEMENT_TYPE_FOOT_LINE,ELEMENT_TYPE_DOUBLE_BRIDGE))  # 顶线腰线脚线，双排廊桥
                cursor.execute("UPDATE `order_part_online` SET `State`= '%s' WHERE `Order_id`='%s' and (`Element_type_id`='%s' or `Element_type_id`='%s' or `Element_type_id`='%s'or `Element_type_id`='%s')" % (
                        STATE_ATTACHE_COMPONENT_MACHINE, the_load_order_id[i][1], ELEMENT_TYPE_TOP_LINE,
                        ELEMENT_TYPE_WAIST_LINE, ELEMENT_TYPE_FOOT_LINE,ELEMENT_TYPE_DOUBLE_BRIDGE))  # 顶线腰线脚线部件，双排廊桥
                cursor.execute("UPDATE `order_section_online` SET `State`= '%s' WHERE `Order_id`='%s' and `Lintel_num`=0 and `Rome_column_num`=0 and `Door_num`=0 and `Top_line_num`=0 and `Waist_line_num`=0 and `Foot_line_num`=0" % (
                    STATE_DELIVERY, the_load_order_id[i][1]))  # 修改整套组件的组件状态，订单状态
                cursor.execute("UPDATE `order_order_online` SET `State`= '%s' WHERE `Order_id`='%s' and `Lintel_num`=0 and `Rome_column_num`=0 and `Door_num`=0 and `Top_line_num`=0 and `Waist_line_num`=0 and `Foot_line_num`=0" % (
                    STATE_DELIVERY, the_load_order_id[i][1]))
                cursor.execute("UPDATE `order_element_online` SET `State`= '%s' WHERE `Order_id`='%s' and (`Element_type_id`='%s' or `Element_type_id`='%s' or `Element_type_id`='%s') and (`Index_of_base_material_thickness`='%s' or `Board_thick`<>'%s')" % (
                    STATE_MACHINE_FINISH, the_load_order_id[i][1], ELEMENT_TYPE_DOOR, ELEMENT_TYPE_LINTEL,
                    ELEMENT_TYPE_ROME_COLUMN,ELEMENT_PLAIN_BOARD_INDEX,self.normal_layout_thickness))  #厚度为18的双面板以及非18的门板楣板罗马柱，初始状态置为40
                cursor.execute("UPDATE `order_part_online` SET `State`= '%s' WHERE `Order_id`='%s' and (`Element_type_id`='%s' or `Element_type_id`='%s' or `Element_type_id`='%s') and (`Index_of_base_material_thickness`='%s' or `Door_thick`<>'%s')" % (
                    STATE_MACHINE_FINISH, the_load_order_id[i][1], ELEMENT_TYPE_DOOR,
                    ELEMENT_TYPE_LINTEL, ELEMENT_TYPE_ROME_COLUMN,ELEMENT_PLAIN_BOARD_INDEX,self.normal_layout_thickness))
                if gq_number == 0 or gq_number == 1 :
                    cursor.execute("UPDATE `order_order_online` SET `First_day`= '%s' WHERE `Order_id`='%s' " % (datetime.date.today(), the_load_order_id[i][1]))
                    cursor.execute("UPDATE `order_section_online` SET `First_day`= '%s',`Package_state`=0 WHERE `Order_id`='%s' " % (datetime.date.today(), the_load_order_id[i][1]))
                    cursor.execute("UPDATE `order_part_online` SET `First_day`= '%s' WHERE `Order_id`='%s'" % (datetime.date.today(), the_load_order_id[i][1]))
                    cursor.execute("UPDATE `order_element_online` SET `First_day`= '%s' WHERE `Order_id`='%s'" % (datetime.date.today(), the_load_order_id[i][1]))
                if gq_number == 0 :  #加载散板，当一个订单只全部含有特殊门型，修改零件 ，部件的状态
                    cursor.execute("UPDATE `order_element_online` SET `State`= '%s' WHERE `Order_id`='%s' and (`Element_type_id`='%s' or `Element_type_id`='%s' or `Element_type_id`='%s')" % (
                            STATE_MACHINE_FINISH, the_load_order_id[i][1], ELEMENT_TYPE_DOOR, ELEMENT_TYPE_LINTEL,ELEMENT_TYPE_ROME_COLUMN))
                    cursor.execute("UPDATE `order_part_online` SET `State`= '%s' WHERE `Order_id`='%s' and (`Element_type_id`='%s' or `Element_type_id`='%s' or `Element_type_id`='%s')" % (
                            STATE_MACHINE_FINISH, the_load_order_id[i][1], ELEMENT_TYPE_DOOR,ELEMENT_TYPE_LINTEL, ELEMENT_TYPE_ROME_COLUMN))
                    cursor.execute("UPDATE `order_section_online` SET `Package_state`= 0,`State`= '%s' WHERE `Order_id`='%s' " %(STATE_MACHINE_FINISH,the_load_order_id[i][1]))
                if gq_number == 1 :  #整套组件或只含有顶线腰线脚线
                    cursor.execute("UPDATE `order_section_online` SET `Package_state`= 0,`State`= '%s' WHERE `Order_id`='%s' and (`Top_line_num`<>0 or `Waist_line_num`<>0 or `Foot_line_num`<>0)" % (STATE_ATTACHE_COMPONENT_MACHINE, the_load_order_id[i][1]))  #只含有顶线等
                    cursor.execute("UPDATE `order_order_online` SET `State`= '%s' WHERE `Order_id`='%s' and (`Top_line_num`<>0 or `Waist_line_num`<>0 or `Foot_line_num`<>0)" % (STATE_ATTACHE_COMPONENT_MACHINE, the_load_order_id[i][1]))
                cursor.execute("INSERT INTO `%s`(`Single_double`,`Contract_C_Time`,`Id`,`Priority`,`Color`,`Height`,`Width`,`Thickness`,`Open_way`,`Type`,`Hole`,`Heart_type`,`Code`,`Order_Id`,`Element_type_id`,`Index_of_base_material_thickness`) SELECT `Single_double`,`Contract_C_Time`,`Id`,`Priority`,`Color`,`Board_height`,`Board_width`,`Board_thick`,`Open_way`,`Board_type`,`Hole`,`Heart_type`,`Code`,`Order_Id`,`Element_type_id`,`Index_of_base_material_thickness` From `order_element` WHERE `Order_id`='%s' and (`Element_type_id`='%s' or `Element_type_id`='%s' or `Element_type_id`='%s' or `Element_type_id`='%s')" % (
                        wait_layout_sheet,the_load_order_id[i][1], ELEMENT_TYPE_DOOR, ELEMENT_TYPE_LINTEL, ELEMENT_TYPE_ROME_COLUMN,ELEMENT_TYPE_ARC_LAYER)) #门板楣板罗马柱带拱压条都加到待排样表单了
                cursor.execute("INSERT INTO `work_cnc_before_layout_temporary`(`Single_double`,`Contract_C_Time`,`Id`,`Priority`,`Color`,`Height`,`Width`,`Thickness`,`Open_way`,`Type`,`Hole`,`Heart_type`,`Code`,`Order_Id`,`Element_type_id`,`Index_of_base_material_thickness`) SELECT `Single_double`,`Contract_C_Time`,`Id`,`Priority`,`Color`,`Board_height`,`Board_width`,`Board_thick`,`Open_way`,`Board_type`,`Hole`,`Heart_type`,`Code`,`Order_Id`,`Element_type_id`,`Index_of_base_material_thickness` From `order_element` WHERE `Order_id`='%s' and (`Element_type_id`='%s' or `Element_type_id`='%s' or `Element_type_id`='%s'or`Element_type_id`='%s' or `Element_type_id`='%s' or `Element_type_id`='%s')" % (
                        the_load_order_id[i][1],ELEMENT_TYPE_TOP_LINE,ELEMENT_TYPE_WAIST_LINE, ELEMENT_TYPE_FOOT_LINE,ELEMENT_TYPE_DOUBLE_BRIDGE,ELEMENT_TYPE_ARC_BRIDGE,ELEMENT_TYPE_TAIMIAN_BRIDGE))  #顶线腰线脚线，双排廊桥，台面廊桥，圆弧廊桥
                cursor.execute("SELECT `Board_type`,`Id`,`heterotype`,`Index_of_base_material_thickness` FROM `order_element` WHERE `Order_id`='%s'and (`Element_type_id`='%s' or `Element_type_id`='%s' or `Element_type_id`='%s')" % (
                    the_load_order_id[i][1], ELEMENT_TYPE_DOOR, ELEMENT_TYPE_LINTEL, ELEMENT_TYPE_ROME_COLUMN))
                type = cursor.fetchall()
                order_element_list = []
                if (type == ()):
                    pass
                else:
                    for row in type:
                        order_element_list.append(copy.deepcopy(list(row)))
                        if gq_number == 2:  # 正常加载，需剔除散板
                            gq_door_type_split = row[0].split('_')
                            door_type_series = ''.join([x for x in gq_door_type_split[1] if x.isdigit()])
                            if door_type_series in self.can_not_load_door_type or row[2] == 1 or row[3] == ELEMENT_PLAIN_BOARD_INDEX:  # 判断哪些进散板
                                not_meet_condition_door_type_id.append(row[1])
                    for j in range(len(order_element_list)):
                        cursor_produce.execute(
                            "SELECT `Tool_1`, `Tool_2`, `Tool_3`, `Tool_4`, `Tool_5`,`Tool_6` FROM `info_door_type` WHERE `Door_style` ='%s'" % (
                                order_element_list[j][0]))
                        record_tool_Knife = cursor_produce.fetchone()
                        if (record_tool_Knife == None):
                            self.log.WriteText('天外天系统正在运行向待排样表单添加数据的程序, 运行错误,info_door_type中无' + str(
                                    order_element_list[j][0]) + '门型或没有该门型对应的刀具类型  \r\n')
                        else:
                            cursor.execute("UPDATE `%s` SET `CPU_index`='%s',`Production_batch`='%s',`State`='%s',`Knife_1`='%s',`Knife_2`='%s',`Knife_3`='%s',`Knife_4`='%s',`Knife_5`='%s',`Knife_6`='%s' WHERE `Id`='%s' " % (
                                wait_layout_sheet,self.cpu_index, the_load_order_id[i][12], wait_layout_state, record_tool_Knife[0],record_tool_Knife[1], record_tool_Knife[2], record_tool_Knife[3],
                                    record_tool_Knife[4], record_tool_Knife[5], order_element_list[j][1]))
                cursor.execute("DELETE FROM `order_order` WHERE `Order_id`='%s' " % the_load_order_id[i][1])
                cursor.execute("DELETE FROM `order_section` WHERE `Order_id`='%s' " % the_load_order_id[i][1])
                cursor.execute("DELETE FROM `order_part` WHERE `Order_id`='%s' " % the_load_order_id[i][1])
                cursor.execute("DELETE FROM `order_element` WHERE `Order_id`='%s' " % the_load_order_id[i][1])
                self.all_load_num += len(order_element_list)
            db.commit()
            if gq_number == 2:  # 正常加载，需剔除散板
                cursor.execute("INSERT INTO `work_cnc_before_layout_temporary`(`Single_double`,`Contract_C_Time`,`Id`,`Priority`,`Color`,`Height`,`Width`,`Thickness`,`Open_way`,`Type`,`Hole`,`Heart_type`,`Code`,`Order_Id`,`Element_type_id`,`Index_of_base_material_thickness`,`Knife_1`,`Knife_2`,`Knife_3`,`Knife_4`,`Knife_5`,`Knife_6`) SELECT `Single_double`,`Contract_C_Time`,`Id`,`Priority`,`Color`,`Height`,`Width`,`Thickness`,`Open_way`,`Type`,`Hole`,`Heart_type`,`Code`,`Order_Id`,`Element_type_id`,`Index_of_base_material_thickness`,`Knife_1`,`Knife_2`,`Knife_3`,`Knife_4`,`Knife_5`,`Knife_6` From `work_cnc_before_layout` WHERE `Thickness`<>'%s'or `Element_type_id`='%s'" % (
                        self.normal_layout_thickness, ELEMENT_TYPE_ARC_LAYER))
                cursor.execute("DELETE FROM `work_cnc_before_layout` WHERE `Thickness`<>'%s'or`Element_type_id`='%s'" % (
                        self.normal_layout_thickness, ELEMENT_TYPE_ARC_LAYER))
                for i in range(len(not_meet_condition_door_type_id)):
                    cursor.execute("UPDATE `order_element_online` SET `State`= '%s' WHERE `Id`='%s' and (`Element_type_id`='%s' or `Element_type_id`='%s' or `Element_type_id`='%s')" % (
                            STATE_MACHINE_FINISH, not_meet_condition_door_type_id[i], ELEMENT_TYPE_DOOR, ELEMENT_TYPE_LINTEL,
                            ELEMENT_TYPE_ROME_COLUMN))  # 因门型进散板的零件状态修改
                    part_id=not_meet_condition_door_type_id[i].split('ID')
                    cursor.execute("UPDATE `order_part_online` SET `State`= '%s' WHERE `Part_id`='%s' and (`Element_type_id`='%s' or `Element_type_id`='%s' or `Element_type_id`='%s')" % (
                            STATE_MACHINE_FINISH, part_id[0], ELEMENT_TYPE_DOOR,
                            ELEMENT_TYPE_LINTEL, ELEMENT_TYPE_ROME_COLUMN))
                    cursor.execute("INSERT INTO `work_cnc_before_layout_temporary`(`Single_double`,`Contract_C_Time`,`Id`,`Priority`,`Color`,`Height`,`Width`,`Thickness`,`Open_way`,`Type`,`Hole`,`Heart_type`,`Code`,`Order_Id`,`Element_type_id`,`Index_of_base_material_thickness`,`Knife_1`,`Knife_2`,`Knife_3`,`Knife_4`,`Knife_5`,`Knife_6`) SELECT `Single_double`,`Contract_C_Time`,`Id`,`Priority`,`Color`,`Height`,`Width`,`Thickness`,`Open_way`,`Type`,`Hole`,`Heart_type`,`Code`,`Order_Id`,`Element_type_id`,`Index_of_base_material_thickness`,`Knife_1`,`Knife_2`,`Knife_3`,`Knife_4`,`Knife_5`,`Knife_6` From `work_cnc_before_layout` WHERE `Id` ='%s' " % (
                            not_meet_condition_door_type_id[i]))
                    cursor.execute("DELETE FROM `work_cnc_before_layout` WHERE `Id` ='%s' " % (not_meet_condition_door_type_id[i]))
            db.commit()
            db.close()
            db_produce.close()
            return RUN_NORMAL
        except:
            pass
    def GQ_Check_If_Can_Layout(self):
        '''
        查找订单表单中是否还有未加载订单（状态为26），没有则启动排样
        :return:
        '''
        self.gq_count_times += 1
        if self.gq_count_times == 10:  # 10s更新事件
            self.Update_Order_Priority()
            self.gq_count_times = 0
        try:
            db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0], charset=charset)
            cursor = db.cursor()
            cursor.execute("SELECT `Index` from `order_order`  WHERE `State`='%s'and `Cpu_Index`in ('%s')"%(STATE_BEGIN_SCHEDULING,self.cpu_index))
            unload_order_num = cursor.fetchall()
            cursor.execute("SELECT `Index` from `work_cnc_before_layout`  WHERE `Cpu_Index`in ('%s')"%self.cpu_index)
            wait_layout_data = cursor.fetchall()
            cursor.execute("SELECT `Index` from `order_element_online`  WHERE `State`='%s'" % STATE_SPLIT_ORDER)
            state_corresponding_index = cursor.fetchall()  #从在线零件表单中获得状态为26的零件，若有且当前不在排样，则证明上次排样失败
              #排样失败，则从查询表单中获得上次排样的订单，清除零时工单表单，将在线表单中对应的订单挪到不在线中，清除待排样与零时待排样表单
            if state_corresponding_index != () and self.begin_scheduling_state == 0 :
                cursor.execute("SELECT `Spare_order_id`,`Total_batch_num`,`Workorder_id`,`Cpu_Index` from `work_cnc_workorder_query`  WHERE `State`='%s'" % STATE_BEGIN_LAYOUT)
                production_information = cursor.fetchone()
                if production_information != None :  #获取到订单信息
                    if self.cpu_index in production_information[3] :  #是同一台电脑
                        batch_order = []
                        if production_information[0] != '0' :  #有散板工单
                            batch_order = production_information[0].split(',')
                        for i in range(production_information[1]):
                            cursor.execute("SELECT `%s` from `work_cnc_workorder_query`  WHERE `Workorder_id`='%s'" % ('Batch_including_order_'+str(i+1),production_information[2]))
                            other_order = cursor.fetchone()
                            if other_order != None :
                                different_batch_order = other_order[0].split(',')
                                for j in range(len(different_batch_order)):
                                    batch_order.append(different_batch_order[j])
                        for i in range(len(batch_order)):
                            cursor.execute("UPDATE `order_order_online` SET `State`= '%s',`CPU_index`= '%s' WHERE `Order_id`='%s' " % (
                                STATE_BEGIN_SCHEDULING,self.cpu_index, batch_order[i]))
                            cursor.execute("INSERT INTO `order_order`(`CPU_index`,`discount`,`Archaize_area`,`Bar_area`,`Order_type`,`Scheduling_Operator`,`Contract_id`, `Order_id`, `Contract_C_Time`, `Record_time`, `Receive_time`, `Delivery_time`,`Transport_company`, `Check_number`, `Check_name`, `Customer_address`, `Customer_tel`, `Spare_cust`, `Spare_tel`, `Customer_name`, `Technology_manager_tel`, `Technology_manager_name`, `Financial_manager_tel`, `Financial_manager_name`, `Order_priority`,`specialshaped_price`, `Order_price`,`Charge_price`, `Order_area`, `Sec_type_num`, `Sec_num`,`Lintel_num`,`Rome_column_num`,`Top_line_num`,`Waist_line_num`,`Foot_line_num`,`Door_num`,`Door_area`, `Part_num`, `Ele_num`, `Package_num`, `Package_num_now`,`Edge_type_num`,`Dealer`,`Technical_audit_remarks`,`Price_audit_remarks`,`Financial_audit_remarks`, `State`, `remarks`,`remarkimage`,`Brand`) SELECT `CPU_index`,`discount`,`Archaize_area`,`Bar_area`,`Order_type`,`Scheduling_Operator`,`Contract_id`, `Order_id`, `Contract_C_Time`, `Record_time`, `Receive_time`, `Delivery_time`,`Transport_company`, `Check_number`, `Check_name`, `Customer_address`, `Customer_tel`, `Spare_cust`, `Spare_tel`, `Customer_name`, `Technology_manager_tel`, `Technology_manager_name`, `Financial_manager_tel`, `Financial_manager_name`, `Order_priority`,`specialshaped_price`, `Order_price`,`Charge_price`, `Order_area`, `Sec_type_num`, `Sec_num`,`Lintel_num`,`Rome_column_num`,`Top_line_num`,`Waist_line_num`,`Foot_line_num`,`Door_num`,`Door_area`, `Part_num`, `Ele_num`, `Package_num`, `Package_num_now`,`Edge_type_num`,`Dealer`,`Technical_audit_remarks`,`Price_audit_remarks`,`Financial_audit_remarks`, `State`, `remarks`,`remarkimage`,`Brand` FROM `order_order_online`  WHERE `Order_id`='%s'" %
                                           batch_order[i])
                            cursor.execute("INSERT INTO `order_section`(`Sec_length`,`Sec_width`,`Sec_height`,`Record_time`, `Contract_id`, `Order_id`, `Order_time`, `Sec_id`, `Sec_name`, `Sec_type`, `Stick_type`, `Priority`, `Sec_light`,`Sec_series`,`Sec_model`, `Sec_color`, `Sec_thick`,`Sec_edge`, `Archaize`, `Index_of_base_material_thickness`,`Sec_num`,`Lintel_num`,`Rome_column_num`,`Foot_line_num`,`Waist_line_num`,`Top_line_num`,`Door_num`, `Door_area`, `Door_price`, `Acce_price`, `Single_price`, `Door_type_num`, `Rom_type_num`, `Euro_type_num`, `Acce_type_num`, `State`, `remarks`) SELECT `Sec_length`,`Sec_width`,`Sec_height`,`Record_time`, `Contract_id`, `Order_id`, `Order_time`, `Sec_id`, `Sec_name`, `Sec_type`, `Stick_type`, `Priority`, `Sec_light`,`Sec_series`,`Sec_model`, `Sec_color`, `Sec_thick`,`Sec_edge`, `Archaize`, `Index_of_base_material_thickness`,`Sec_num`,`Lintel_num`,`Rome_column_num`,`Foot_line_num`,`Waist_line_num`,`Top_line_num`,`Door_num`, `Door_area`, `Door_price`, `Acce_price`, `Single_price`, `Door_type_num`, `Rom_type_num`, `Euro_type_num`, `Acce_type_num`, `State`, `remarks` FROM `order_section_online` WHERE `Order_id`='%s'" %
                                           batch_order[i])
                            cursor.execute("INSERT INTO `order_part`(`heterotype`,`Straightening_device`,`Contract_C_Time`,`Record_time`, `Priority`, `Contract_id`, `Order_id`, `Sec_id`, `Part_id`,`Part_type`,`Same_part_num`, `Door_type`, `Door_color`, `Door_height`, `Door_width`, `Door_thick`, `Archaize`, `Door_area`, `Door_price`,`Extra_charge`, `Bar_type`, `Single_double`,`Texture_direction`,`Element_type_id`,`Interval_width`,`Bottom_part_down`,`Double_color`,`Hole_dire`, `Hole`, `Open_way`, `Edge_type`, `Glass`, `Rom_price`,  `Heart_type`, `State`, `remarks`,`remarkimage`, `is_first`, `Index_of_base_material_thickness`) SELECT `heterotype`,`Straightening_device`,`Contract_C_Time`,`Record_time`, `Priority`, `Contract_id`, `Order_id`, `Sec_id`, `Part_id`,`Part_type`,`Same_part_num`, `Door_type`, `Door_color`, `Door_height`, `Door_width`, `Door_thick`, `Archaize`, `Door_area`, `Door_price`,`Extra_charge`, `Bar_type`, `Single_double`,`Texture_direction`,`Element_type_id`,`Interval_width`,`Bottom_part_down`,`Double_color`,`Hole_dire`, `Hole`, `Open_way`, `Edge_type`, `Glass`, `Rom_price`,  `Heart_type`, `State`, `remarks`,`remarkimage`, `is_first`, `Index_of_base_material_thickness` FROM `order_part_online` WHERE `Order_id`='%s'" %
                                           batch_order[i])
                            cursor.execute("INSERT INTO `order_element`(`Straightening_device`,`Record_time`, `Contract_C_Time`, `Contract_id`, `Order_id`, `Sec_id`, `Part_id`, `Id`, `Priority`, `Color`, `Crosspiece`, `Crosspiece_size`, `Texture_direction`, `Single_double`, `Interval_width`, `Bottom_part_down`, `Glass`, `Handle`, `Element_type_id`, `Board_height`, `Board_width`, `Board_thick`, `Archaize`,`Double_color`, `Open_way`, `Board_type`, `Hole`, `Edge_type`, `Heart_type`,`heterotype`, `Bar_type`, `Index_of_base_material_thickness`,`State`, `Code`, `remarks`) SELECT `Straightening_device`,`Record_time`, `Contract_C_Time`, `Contract_id`, `Order_id`, `Sec_id`, `Part_id`, `Id`, `Priority`, `Color`, `Crosspiece`, `Crosspiece_size`, `Texture_direction`, `Single_double`, `Interval_width`, `Bottom_part_down`, `Glass`, `Handle`, `Element_type_id`, `Board_height`, `Board_width`, `Board_thick`, `Archaize`,`Double_color`, `Open_way`, `Board_type`, `Hole`, `Edge_type`, `Heart_type`,`heterotype`, `Bar_type`, `Index_of_base_material_thickness`,`State`, `Code`, `remarks` FROM `order_element_online` WHERE `Order_id`='%s'" %
                                           batch_order[i])
                            cursor.execute("DELETE FROM `order_order_online` WHERE `Order_id`='%s' " % batch_order[i])
                            cursor.execute("DELETE FROM `order_section_online` WHERE `Order_id`='%s' " % batch_order[i])
                            cursor.execute("DELETE FROM `order_part_online` WHERE `Order_id`='%s' " % batch_order[i])
                            cursor.execute("DELETE FROM `order_element_online` WHERE `Order_id`='%s' " % batch_order[i])
                            cursor.execute("DELETE FROM `work_cnc_before_layout` WHERE `CPU_index`in ('%s')"%self.cpu_index)  #待排样
                            cursor.execute("DELETE FROM `work_cnc_before_layout_temporary` WHERE `Order_id`='%s'"% batch_order[i])   #零时待排样
                            cursor.execute("DELETE FROM `work_cnc_task_list_temporary` WHERE `CPU_index`in ('%s')"%self.cpu_index)   #零时工位工单表单
                            cursor.execute("DELETE FROM `work_cnc_workorder_query` WHERE `Workorder_id`='%s'"%production_information[2])   #零时工位工单表单
                        db.commit()
            db.close()
            if unload_order_num == () and wait_layout_data != () and self.begin_scheduling_state==1:  #开始排样
                if self.layout_algorithm.Complete_Layout(self.workorder_id_immediately):
                    return False
                if (self.Update_Production_Sheet()):  # 全部零件排样完成时，将排样完成的信息加到对应的生产调度表单内
                    self.begin_scheduling_state=0
                    return True
            else:
                return False
        except:
            return False
    def Update_Production_Sheet(self):
        '''
        此方法用于将排样完成的信息加到生产调度表单内
        完成排样后，将加载面积、不同厚度分别对应的工单数量，剩余未排样的面积数加到生产调度表单内
        :return:
        '''
        thick_num=[]
        try:
            db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0], charset=charset)
            db_produce = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[1],charset=charset)
            cursor = db.cursor()
            cursor_produce=db_produce.cursor()
            cursor.execute("SELECT `Index_of_base_material_thickness` FROM `work_cnc_task_list` WHERE `State`='%s'and `CPU_index`in ('%s')" % (STATE_INITIAL,self.cpu_index))
            thickness = cursor.fetchall()
            if thickness==():
                pass
            else:
                for i in range(len(thickness)):#找出当前工单中所包含的厚度种类
                    if thickness[i][0] not in [x[0] for x in thick_num]:
                        thick_num.append([thickness[i][0],0])
                for i in range(len(thick_num)):                 #找出各厚度对应的工单数量
                    num=0
                    for j in range(len(thickness)):
                        if thick_num[i][0]==thickness[j][0]:
                            num+=1
                    thick_num[i][1]=num
                str1= '产生'
                for i in range(len(thick_num)):
                    cursor_produce.execute(
                        "SELECT `Base_material_name` FROM `info_base_material_charge` WHERE `Index`='%s'" % thick_num[i][0])
                    base_material_name = cursor_produce.fetchone()
                    if base_material_name==None:
                        base_material_name[0]=''
                    if i==len(thick_num)-1:
                        str1+=str(base_material_name[0])+'板材的工位工单*'+str(thick_num[i][1])+'*床'
                    else:
                        str1+=str(base_material_name[0])+'板材的工位工单*'+str(thick_num[i][1])+'*床&'
                cursor.execute(
                    "INSERT INTO `work_production_scheduling`(`Schedule_create_time`,`Schedule_of_workstation`,`State`) VALUES ('%s','%s','%s')" % (datetime.datetime.now(),str1,SCHEDULE_LAYOUT_FINISH))
                db.commit()
                db.close()
                db_produce.close()
                self.log.WriteText("天外天系统正在运行加工中心下料预排样的程序，下料排样已完成\r\n")
                return True
        except:
            self.log.WriteText('天外天系统更新生产调度表单出现错误，请进行检查  \r\n')
            return False
    def GQ_Find_All_Can_Plan_Production(self,state_order,number):
        '''
        找到所有可以加载的订单
        :return:
        '''
        self.record_urgent_order_information = [[], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0]  # 订单编号，订单面积，压条面积，仿古面积，各种厚度的板材面积(18mm.20mm.22mm.25mm单面板，素板，格子板)
        self.all_can_plan_production=[]
        try:
            db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0], charset=charset)
            cursor = db.cursor()
            if number == 0 :
                cursor.execute("UPDATE `order_order` set `State`='%s',`CPU_index`='0' WHERE `State`='%s' and `CPU_index`in ('%s')" % (STATE_SPLIT_ORDER, STATE_BEGIN_SCHEDULING,self.cpu_index))
                db.commit()
                cursor.execute("UPDATE `order_order` set `CPU_index`='%s' WHERE `State`='%s'and (`CPU_index`='0'or`CPU_index` is NULL) " % (self.cpu_index, STATE_SPLIT_ORDER))
                db.commit()
            cursor.execute("SELECT `Order_area`,`Order_id`,`Order_priority`,`Bar_area`,`Archaize_area` from `order_order`  WHERE `State`='%s'and `CPU_index`in ('%s')"%(state_order,self.cpu_index))
            gq_order_information = cursor.fetchall()
            if gq_order_information==():
                pass
            else:
                for i in range(len(gq_order_information)):  #所有可加载的订单
                    if number == 1:  #初始化时使用
                        if gq_order_information[i][3] != None:
                            self.record_urgent_order_information[2] += gq_order_information[i][3]
                        if gq_order_information[i][4] != None:
                            self.record_urgent_order_information[3] += gq_order_information[i][4]
                        self.Get_Different_Thick_Meterial_Area(gq_order_information[i][1], 0, 0)
                    self.all_can_plan_production.append(list(gq_order_information[i]))
            db.close()
            self.all_can_plan_production.sort(key=lambda x: -x[2])   #将零件按优先级降序排序
        except:
            pass
    def GQ_Load_Urgent_Order(self,modify_state):
        '''
        记录加急订单的相应信息，将订单状态改为26，删除此已加载订单
        :return:
        '''
        i=0
        while i < len(self.all_can_plan_production) :  #订单已按优先级降序排列了
            if self.all_can_plan_production[i][2] >= MODIFY_URGENT_PRIORITY : #紧急的订单
                self.record_urgent_order_information[0].append([self.all_can_plan_production[i][1],self.all_can_plan_production[i][0]])
                self.record_urgent_order_information[1] += self.all_can_plan_production[i][0]
                if self.all_can_plan_production[i][3] != None :
                    self.record_urgent_order_information[2] += self.all_can_plan_production[i][3]
                if self.all_can_plan_production[i][4] != None:
                    self.record_urgent_order_information[3] += self.all_can_plan_production[i][4]
                self.Get_Different_Thick_Meterial_Area(self.all_can_plan_production[i][1],0,0)
                self.GQ_Update_Can_Plan_Production(0,self.all_can_plan_production[i][1],modify_state)
                del self.all_can_plan_production[i]
                i -= 1
            else:  #紧急的订单已加载完毕
                break
            i += 1
        self.record_urgent_order_information[0].sort(key=lambda x: -x[1])  #面积降序排列
    def Get_Different_Thick_Meterial_Area(self,order_id,number,add_or_sub):
        '''
        根据传入的订单编号，从组件表单中找到对应的板材厚度，记录板材面积
        number=0:加载加急订单时获得板材厚度
        add_or_sub=0:+  1:-
        :return:
        '''
        self.judge_if_the_order_can_load=0
        try:
            db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0], charset=charset)
            cursor = db.cursor()
            cursor.execute(
                "SELECT `Index_of_base_material_thickness`,`Door_area` from `order_section`  WHERE `Order_id`='%s'" % order_id)
            sec_thick_area = cursor.fetchall()
            db.close()
            if sec_thick_area == () :
                pass
            else:
                for i in range(len(sec_thick_area)):
                    if sec_thick_area[i][0] == ELEMENT_SINGLE_BOARD_INDEX :  #18单面板
                        self.GQ_Judge_If_Can_Load_Common_Part(number,4,self.element_single_board_index,sec_thick_area,i,1,add_or_sub)
                    elif sec_thick_area[i][0] == ELEMENT_PLAIN_BOARD_INDEX :  #18素板
                        self.GQ_Judge_If_Can_Load_Common_Part(number, 5, self.element_plain_board_index,sec_thick_area, i,1,add_or_sub)
                    elif sec_thick_area[i][0] == ELEMENT_LATICES_BOARD_INDEX :  #18格子板
                        self.GQ_Judge_If_Can_Load_Common_Part(number, 6, self.element_latics_board_index,sec_thick_area, i,1,add_or_sub)
                    elif sec_thick_area[i][0] == ELEMENT_SINGLE_BOARD_INDEX_20 :  #20单面板
                        self.GQ_Judge_If_Can_Load_Common_Part(number, 7, self.element_single_board_index_20,sec_thick_area,i, 2,add_or_sub)
                    elif sec_thick_area[i][0] == ELEMENT_PLAIN_BOARD_INDEX_20 :  #20素板
                        self.GQ_Judge_If_Can_Load_Common_Part(number, 8, self.element_plain_board_index_20,sec_thick_area, i,2,add_or_sub)
                    elif sec_thick_area[i][0] == ELEMENT_LATICES_BOARD_INDEX_20 :  #20格子板
                        self.GQ_Judge_If_Can_Load_Common_Part(number, 9, self.element_latics_board_index_20,sec_thick_area, i,2,add_or_sub)
                    elif sec_thick_area[i][0] == ELEMENT_SINGLE_BOARD_INDEX_22 :  #22单面板
                        self.GQ_Judge_If_Can_Load_Common_Part(number, 10, self.element_single_board_index_22,sec_thick_area, i,2,add_or_sub)
                    elif sec_thick_area[i][0] == ELEMENT_PLAIN_BOARD_INDEX_22 :  #22素板
                        self.GQ_Judge_If_Can_Load_Common_Part(number, 11, self.element_plain_board_index_22,sec_thick_area, i,2,add_or_sub)
                    elif sec_thick_area[i][0] == ELEMENT_LATICES_BOARD_INDEX_22 :  #22格子板
                        self.GQ_Judge_If_Can_Load_Common_Part(number, 12, self.element_latics_board_index_22,sec_thick_area, i,2,add_or_sub)
                    elif sec_thick_area[i][0] == ELEMENT_SINGLE_BOARD_INDEX_25 :  #25单面板
                        self.GQ_Judge_If_Can_Load_Common_Part(number, 13, self.element_single_board_index_25,sec_thick_area, i,2,add_or_sub)
                    elif sec_thick_area[i][0] == ELEMENT_PLAIN_BOARD_INDEX_25 :  #25素板
                        self.GQ_Judge_If_Can_Load_Common_Part(number, 14, self.element_plain_board_index_25,sec_thick_area, i,2,add_or_sub)
                    else :  #25格子板
                        self.GQ_Judge_If_Can_Load_Common_Part(number, 15, self.element_latics_board_index_25,sec_thick_area, i,2,add_or_sub)
        except:
            pass
    def GQ_Judge_If_Can_Load_Common_Part(self,number,index,kind_of_board,sec_thick_area,gq_index,signal_value,add_or_sub):
        if add_or_sub == 0:
            self.record_urgent_order_information[index] += (sec_thick_area[gq_index][1]*1000000)/(self.utilization_ratio*Plate_Specification_Height*Plate_Specification_Width)
        else:
            self.record_urgent_order_information[index] -= (sec_thick_area[gq_index][1]*1000000)/(self.utilization_ratio*Plate_Specification_Height*Plate_Specification_Width)
        if number == 1 and self.record_urgent_order_information[index] <= kind_of_board :  # 还可以取18单面板
            self.judge_if_the_order_can_load = signal_value
        elif number == 1:  # 不能加载当前板材
            self.record_urgent_order_information[index] -= sec_thick_area[gq_index][1]/self.utilization_ratio
    def GQ_Update_Can_Plan_Production(self,cal_batch,can_load_order_id,modify_state):
        '''
        更新订单表单内的可加载订单
        :return:
        '''
        try:
            db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0], charset=charset)
            cursor = db.cursor()
            cursor.execute(
                "UPDATE `order_order` set `CPU_index`='%s',`Production_batch`='%s',`State`='%s' WHERE `Order_id`='%s' " % (self.cpu_index,cal_batch,modify_state,can_load_order_id))
            db.commit()
            db.close()
        except:
            pass
    def Record_Other_Can_Load_Order_Id(self,modify_state):
        '''
        先看有没有加急的或有没有订单，有的话挑选出同刀型订单，当前加载订单面积够了，则停止加载
        :return:
        '''
        if float(self.load_order_area.GetValue()) and float(self.layer_area.GetValue()) and float(self.artificial_area.GetValue()):
            while self.all_can_plan_production != [] or self.record_urgent_order_information[0] != []:
                self.urgent_record_knife = ['0',None]
                if self.record_urgent_order_information[0] != [] :  #当前有加急的订单
                    get_knife_order_id=self.record_urgent_order_information[0][0][0]
                    del self.record_urgent_order_information[0][0]
                else:
                    get_knife_order_id=self.all_can_plan_production[0][1]
                self.GQ_Record_Order_Knife(get_knife_order_id,self.urgent_record_knife)  #记录刀
                if self.Get_Same_Knife_Order(self.all_can_plan_production):                  #找出同刀型的订单
                    return LOAD_ERROR
                while self.choose_same_knife_order != [] :      #有同刀型的订单，当压条面积不为空也不为0也不为None且真实取的压条面积未超限，则取该订单
                    self.Get_Different_Thick_Meterial_Area(self.choose_same_knife_order[0][1],1,0)  #判断板材够不够
                    if self.judge_if_the_order_can_load != 0 :  #当前订单所属的厚度的板材够
                        if self.choose_same_knife_order[0][3] != None and self.choose_same_knife_order[0][3] != 0.0 and self.choose_same_knife_order[0][4] != None and self.choose_same_knife_order[0][4] != 0.0 :
                            self.record_urgent_order_information[2] += self.choose_same_knife_order[0][3]  # 记录加载的压条以及仿古面积
                            self.record_urgent_order_information[3] += self.choose_same_knife_order[0][4]
                            if self.record_urgent_order_information[2] <= (float(self.layer_area.GetValue())+ self.layer_threshold) and self.record_urgent_order_information[3] <= (float(self.artificial_area.GetValue()) + self.archaize_threshold):
                                self.GQ_Update_Can_Plan_Production(0,self.choose_same_knife_order[0][1],modify_state)
                                if self.choose_same_knife_order[0][0] != None:
                                    self.record_urgent_order_information[1] += self.choose_same_knife_order[0][0]
                            else:
                                self.record_urgent_order_information[2] -= self.choose_same_knife_order[0][3]  # 记录加载的压条以及仿古面积
                                self.record_urgent_order_information[3] -= self.choose_same_knife_order[0][4]
                        elif self.choose_same_knife_order[0][3] != None and self.choose_same_knife_order[0][3] != 0.0 and (self.choose_same_knife_order[0][4] == 0.0 or self.choose_same_knife_order[0][4] == None):
                            self.record_urgent_order_information[2] += self.choose_same_knife_order[0][3]  # 记录加载的压条面积
                            if self.record_urgent_order_information[2] <= (float(self.layer_area.GetValue())+ self.layer_threshold):
                                self.GQ_Update_Can_Plan_Production(0,self.choose_same_knife_order[0][1],modify_state)
                                if self.choose_same_knife_order[0][0] != None:
                                    self.record_urgent_order_information[1] += self.choose_same_knife_order[0][0]
                            else:
                                self.record_urgent_order_information[2] -= self.choose_same_knife_order[0][3]  # 记录加载的压条面积
                        elif self.choose_same_knife_order[0][4] != None and self.choose_same_knife_order[0][4] != 0.0 and (self.choose_same_knife_order[0][3] == 0.0 or self.choose_same_knife_order[0][3] == None):
                            self.record_urgent_order_information[3] += self.choose_same_knife_order[0][4]  # 记录加载的仿古面积
                            if self.record_urgent_order_information[3] <= (float(self.artificial_area.GetValue()) + self.archaize_threshold):
                                self.GQ_Update_Can_Plan_Production(0,self.choose_same_knife_order[0][1],modify_state)
                                if self.choose_same_knife_order[0][0] != None:
                                    self.record_urgent_order_information[1] += self.choose_same_knife_order[0][0]
                            else:
                                self.record_urgent_order_information[3] -= self.choose_same_knife_order[0][4]
                        elif (self.choose_same_knife_order[0][3] == 0.0 or self.choose_same_knife_order[0][3] == None) and (self.choose_same_knife_order[0][4] == 0.0 or self.choose_same_knife_order[0][4] == None):      #既没有压条也没有仿古，正常加
                            self.GQ_Update_Can_Plan_Production(0,self.choose_same_knife_order[0][1],modify_state)
                            if self.choose_same_knife_order[0][0] != None:
                                self.record_urgent_order_information[1] += self.choose_same_knife_order[0][0]
                    for i in range(len(self.all_can_plan_production) - 1, -1, -1):  # 将内存中已加载的订单删除
                        if self.all_can_plan_production[i][1] == self.choose_same_knife_order[0][1]:
                            del self.all_can_plan_production[i]
                            break
                    del self.choose_same_knife_order[0]
                    if self.record_urgent_order_information[1] >= float(self.load_order_area.GetValue()) :  #订单面积够了
                        return RUN_NORMAL
        else:
            self.log.WriteText('请输入排产面积或批次排产面积  \r\n')
    def GQ_Record_Order_Knife(self,record_knife_order,record_knife):
        '''
        记录所选订单下的所有零件所用刀型，所有订单只要获得刀具就可以调用此函数
        :return:
        '''
        try:
            db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0], charset=charset)
            db_produce = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[1],charset=charset)
            cursor = db.cursor()
            cursor_produce = db_produce.cursor()
            load_door_type = []
            cursor.execute(
                "SELECT `Board_type` from `order_element`  WHERE `Order_id`='%s'and (`Element_type_id`='%s' or `Element_type_id`='%s' or `Element_type_id`='%s')" %(record_knife_order,ELEMENT_TYPE_DOOR, ELEMENT_TYPE_LINTEL, ELEMENT_TYPE_ROME_COLUMN))
            board_type = cursor.fetchall()
            if board_type==():
                pass
            else:
                for i in range(len(board_type)):
                    if board_type[i][0] not in load_door_type:
                        load_door_type.append(board_type[i][0])
                for i in range(len(load_door_type)):
                    cursor_produce.execute(
                        "SELECT `Tool_1`, `Tool_2`, `Tool_3`, `Tool_4`, `Tool_5`,`Tool_6` FROM `info_door_type` WHERE `Door_style` ='%s'" % (
                            load_door_type[i]))
                    record_tool_Knife = cursor_produce.fetchone()
                    if (record_tool_Knife == None):
                        self.log.WriteText(
                            '天外天系统正在运行记录同刀型订单的程序, 运行错误,info_door_type中无' + str(
                                load_door_type[i]) + '门型或没有该门型对应的刀具类型  \r\n')
                    else:
                        for j in range(len(record_tool_Knife)):
                            if record_tool_Knife[j] not in record_knife:
                                record_knife.append(record_tool_Knife[j])
            db_produce.close()
            db.close()
        except:
            pass
    def Get_Same_Knife_Order(self,get_same_knife_order_id):
        '''
        从不加急订单中找出跟所找的刀同刀型的订单
        :return:
        '''
        self.choose_same_knife_order=[]
        for i in range(len(get_same_knife_order_id)):
            self.gq_record_knife=['0',None]
            self.GQ_Record_Order_Knife(get_same_knife_order_id[i][1], self.gq_record_knife)  #传的是订单编号
            knife_num=0
            for j in range(len(self.gq_record_knife)):           #一个订单的所有刀
                if self.gq_record_knife[j] not in self.urgent_record_knife:
                    knife_num+=1
                    self.urgent_record_knife.append(self.gq_record_knife[j])
            if len(self.urgent_record_knife)-2<=self.finally_knife_threshold+2 or knife_num == 0:
                self.choose_same_knife_order.append(get_same_knife_order_id[i])
            else:
                for k in range(len(self.urgent_record_knife)-1,len(self.urgent_record_knife)-knife_num-1,-1):
                    del self.urgent_record_knife[k]    #订单不满足条件，将添加进来的刀删除
        self.choose_same_knife_order.sort(key=lambda x: -x[0])
    def On_btn_scheduling_immediately(self,evt):
        '''
        点击立即排产，将要进散板的整单（厚度，门型）加入到临时待排样表单（同时记录订单编号，以便添加到查询表单内）
        :param eve:
        :return:
        '''
        self.begin_scheduling_state=1
        self.btn_scheduling_immediately.Enable(False)
        self.btn_scheduling_plan.Enable(False)
        self.GQ_Find_All_Can_Immediately(STATE_BEGIN_SCHEDULING)  # 点击立即排产，就加载订单
        self.GQ_Distribute_Batch_Order(STATE_BEGIN_SCHEDULING)  #为订单分配批次
        self.Get_Layout_Query_Information(datetime.date.today(),0)
        self.Load_Orders_Online(STATE_BEGIN_SCHEDULING)  #先加载整个进散板的，再加载只含有顶线腰线的，最后加载其他
        self.Interface_Refresh()
    def On_Update_Right_Grid(self,if_is_check_update_state):
        '''
        将右侧内的数据更新一个状态，调用右侧的更新函数
        根据订单编号从订单表单内找到订单面积，压条面积，仿古面积，板材数
        :return:
        '''
        self.record_urgent_order_information = [[], float(self.order_area.GetValue()), float(self.order_layer_area.GetValue()), float(self.order_archaize_area.GetValue()), float(self.order_18_single_board.GetValue()), float(self.order_18_plain_board.GetValue()), float(self.order_18_latics_board.GetValue()), float(self.order_20_single_board.GetValue()), float(self.order_20_plain_board.GetValue()), float(self.order_20_latics_board.GetValue()), float(self.order_22_single_board.GetValue()), float(self.order_22_plain_board.GetValue()), float(self.order_22_latics_board.GetValue()), float(self.order_25_single_board.GetValue()), float(self.order_25_plain_board.GetValue()), float(self.order_25_latics_board.GetValue())]
        try:
            get_right_data = self.begin_scheduling_grid.table.data
            db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0], charset=charset)
            cursor = db.cursor()
            if if_is_check_update_state == 0:  # 移除时更新右侧网格
                for i in range(len(get_right_data)):
                    check_value = self.begin_scheduling_grid.table.GetValue(i, 0)  # 判断复选框是否可选
                    if check_value == 1:
                        order_id = self.begin_scheduling_grid.table.GetValue(i, 1)  # 得到表格第一列的订单号以此作为凭证来更新数据库中相对应订单的状态。
                        cursor.execute(
                            "SELECT `Bar_area`,`Archaize_area` FROM `order_order` WHERE `Order_id`='%s' and `CPU_index`in ('%s')" % (order_id,self.cpu_index))
                        kind_of_area = cursor.fetchone()
                        if kind_of_area == None:
                            pass
                        else:
                            if kind_of_area[0] != None:
                                self.record_urgent_order_information[2] -= kind_of_area[0]  # 压条面积，仿古面积
                            if kind_of_area[1] != None:
                                self.record_urgent_order_information[3] -= kind_of_area[1]
                        self.Get_Different_Thick_Meterial_Area(order_id, 0, 1)
                        cursor.execute(
                            "UPDATE `order_order` set `State`='%s',`Production_batch`='%s',`CPU_index`='0' WHERE `Order_id`='%s' " % (
                                STATE_SPLIT_ORDER, 0, order_id))
            else:
                for i in range(len(get_right_data)):
                    order_id = self.begin_scheduling_grid.table.GetValue(i, 1)
                    cursor.execute(
                        "UPDATE `order_order` set `State`='%s',`CPU_index`='%s' WHERE `Order_id`='%s' " % (
                            STATE_PLAN_PRODUCTION,self.cpu_index,order_id))
            db.commit()
            db.close()
        except:
            pass
    def On_btn_scheduling_plan(self,evt):
        '''
        点击计划排产，填写排产查询表单，制单编号，排产日期，创建时间，排产时间点，
        操作员，订单总数，订单总面积，总批次数，批次包含的订单数，状态
        将订单状态改为27，刷新右边表格
        :param evt:
        :return:
        '''
        self.btn_scheduling_plan.Enabled=False
        self.btn_scheduling_immediately.Enabled = False
        self.On_Update_Right_Grid(1)  #更新右侧数据的订单状态27
        self.record_urgent_order_information = [[], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.Interface_Refresh()
        plan_scheduling = self.plan_scheduling_time.GetValue()
        time_list = plan_scheduling.split(':')
        scheduling_date = self.calendar_scheduling.textCtrl.GetValue()
        scheduling_list = scheduling_date.split('/')
        self.GQ_Find_All_Can_Immediately(STATE_PLAN_PRODUCTION)
        self.GQ_Distribute_Batch_Order(STATE_PLAN_PRODUCTION)  # 为订单分配批次
        self.Get_Layout_Query_Information(str(scheduling_list[2])+'-'+str(scheduling_list[1])+'-'+str(scheduling_list[0]),int(time_list[0]))
    def Get_Layout_Query_Information(self,schedule_date,schedule_time):
        '''
        获取到制单编号，将散板的制单编号填入到查询表单中
        :return:
        '''
        spare_order=0
        try:
            db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0], charset=charset)
            cursor = db.cursor()  #获得排产记录编号
            cursor.execute(
                "SELECT `Index` FROM `work_cnc_workorder_query` WHERE 1 ORDER BY `Index` DESC  LIMIT 1")
            id_index = cursor.fetchone()
            if id_index == None:
                layout_record_id = time.strftime('%Y%m%d%H%M%S', time.localtime()) + str(1)
            else:
                layout_record_id = time.strftime('%Y%m%d%H%M%S', time.localtime()) + str(id_index[0] + 1)
            if self.spare_order_information != [] :
                spare_order=str(self.spare_order_information[0][1])
                for i in range(1,len(self.spare_order_information)):
                    spare_order += ','+ self.spare_order_information[i][1]
            if self.only_has_bar_order_information != [] :
                if spare_order == 0 :
                    spare_order = str(self.only_has_bar_order_information[0][1])
                    index=1
                else:
                    index = 0
                for i in range(index,len(self.only_has_bar_order_information)):
                    spare_order += ','+ self.only_has_bar_order_information[i][1]
            cursor.execute(
                "INSERT INTO `work_cnc_workorder_query`(`Cpu_Index`,`Need_hole_door_area`,`Need_hole_order_num`,`Need_hole_door_num`,`Bar_order_num`,`Archaize_order_num`,`Spare_order_id`,`Bar_area`,`Archaize_area`,`Scattered_plate_num`,`Abnormity_plate_num`,`Roman_column_num`,`Fascia_board_num`,`Workorder_id`,`Schedule_date`,`Create_time`,`Operator_id`,`Total_order_num`,`Total_order_area`,`Total_batch_num`,`Schedule_hour`,`State`) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                    self.cpu_index,self.gq_record_all_knids_of_num[5],self.gq_record_all_knids_of_num[6],self.gq_record_all_knids_of_num[7],self.record_layer_area[1],self.record_layer_area[3],spare_order,self.record_layer_area[0],self.record_layer_area[3],self.gq_record_all_knids_of_num[0],self.gq_record_all_knids_of_num[1],self.gq_record_all_knids_of_num[2],self.gq_record_all_knids_of_num[3],layout_record_id, schedule_date, datetime.datetime.now(),self.Operator_ID,
                    self.gq_record_all_knids_of_num[4], self.record_order_area,
                    len(self.record_batch_order_id), schedule_time, 0))
            for i in range(len(self.record_batch_order_id)):  #填写批次对应的订单号
                str_insert = str(self.record_batch_order_id[i][2])
                for j in range(3, len(self.record_batch_order_id[i])):
                    str_insert += ',' + self.record_batch_order_id[i][j]
                cursor.execute("UPDATE `work_cnc_workorder_query` SET `%s`='%s',`%s`='%s' WHERE `Workorder_id`='%s' " % (
                'Batch_'+str(i+1)+'_area',self.record_batch_order_id[i][1],'Batch_including_order_' + str(i + 1), str_insert,layout_record_id))
            db.commit()
            db.close()
            self.workorder_id_immediately = layout_record_id  #记录当前制单编号
        except:
            pass
    def GQ_Get_All_Need_Num(self,different_order_list):
        '''
        从零件库中找出订单对应的零件
        玻璃门数量，含有的素板，单面板，格子板的数量，散板(厚度，门型，带拱压条)，异型的数量，罗马柱，楣板的数量
        :return:
        '''
        try:
            db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0], charset=charset)
            cursor = db.cursor()
            for i in range(len(different_order_list)):
                cursor.execute(
                    "SELECT `Heart_type`,`Index_of_base_material_thickness`,`Board_type`,`Board_thick`,`heterotype`,`Element_type_id` FROM `order_element` WHERE `Order_id`='%s'"%different_order_list[i][1])
                component_information = cursor.fetchall()
                for j in range(len(component_information)):
                    gq_door_type_split = component_information[j][2].split('_')  # 筛选进散板的,门型，厚度，带拱压条，异型
                    door_type_series = ''.join([x for x in gq_door_type_split[1] if x.isdigit()])
                    if component_information[j][1] == ELEMENT_PLAIN_BOARD_INDEX :  #双面板进散板
                        self.gq_record_all_knids_of_num[0] += 1
                    elif component_information[j][4] == 1 :  #异型散板数各加1
                        self.gq_record_all_knids_of_num[1] += 1
                        self.gq_record_all_knids_of_num[0] += 1
                    elif door_type_series in self.can_not_load_door_type and (component_information[j][5]== ELEMENT_TYPE_DOOR or component_information[j][5]== ELEMENT_TYPE_ARC_LAYER):  #门型散板
                        self.gq_record_all_knids_of_num[0] += 1
                    elif component_information[j][5] == ELEMENT_TYPE_ROME_COLUMN and component_information[j][3] == self.normal_layout_thickness :  #罗马柱
                        self.gq_record_all_knids_of_num[2] += 1
                    elif component_information[j][5] == ELEMENT_TYPE_LINTEL and component_information[j][3] == self.normal_layout_thickness:  #楣板
                        self.gq_record_all_knids_of_num[3] += 1
                    elif component_information[j][5] == ELEMENT_TYPE_ARC_LAYER or component_information[j][5] == ELEMENT_TYPE_TOP_LINE or component_information[j][5] == ELEMENT_TYPE_WAIST_LINE or component_information[j][5] == ELEMENT_TYPE_FOOT_LINE or (component_information[j][3] != self.normal_layout_thickness and (component_information[j][5]==ELEMENT_TYPE_DOOR or component_information[j][5]==ELEMENT_TYPE_ROME_COLUMN or component_information[j][5]==ELEMENT_TYPE_LINTEL)):
                        self.gq_record_all_knids_of_num[0] += 1
            db.close()
        except:
            pass
#获取到所有门店
def Get_All_Store(number):
    '''
    获得所有门店
    number=0:获得所有门店
    number = 1:获得所有激活门店
    :return:
    '''
    gq_company_name = []
    try:
        db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password,
                             db=database[2], charset=charset)
        cursor = db.cursor()
        if number == 0 :
            cursor.execute("select `company_name` from `order_company_info` where 1")
            company_name = cursor.fetchall()
        else:
            cursor.execute("select `company_name` from `order_company_info` where `check_state`=0 or `check_state`=1")
            company_name = cursor.fetchall()
        db.close()
        if company_name == ():  # 没有经销商
            pass
        else:
            for i in range(len(company_name)):
                gq_company_name.append(company_name[i][0])
    except:
        pass
    return gq_company_name
# 门店品牌管理
class Store_Brand_Management(wx.Panel):
    def __init__(self, parent, log):
        wx.Panel.__init__(self, parent, -1)
        self.log = log
        gq_door_select_label = wx.StaticText(self, -1, "     门店查询", (8, 10))
        self.gq_company_name = Get_All_Store(1)
        self.gq_store_cb = wx.ComboBox(self, 500, "", (50, 50), (110, -1), self.gq_company_name, wx.CB_DROPDOWN)
        # gq_store_add = wx.Button(self, 10, "    新增门店     ", (50, 50))
        gq_store_set_up_not_common = wx.Button(self, 10, "设为不常用门店 ", (50, 50))
        gq_store_set_common = wx.Button(self, 10, "  设为常用门店  ", (50, 50))
        gq_store_show_all = wx.Button(self, 10, "  显示全部门店  ", (50, 50))
        gq_store_show_not_common_use = wx.Button(self, 10, " 显示不常用门店", (50, 50))
        gq_store_show_active = wx.Button(self, 10, " 显示已激活门店", (50, 50))
        self.gq_store_door_grid = GQ_Store_Door_Grid(self, self.log, 3, 'info_dealer_brand','经销商')
        gq_sizer = wx.BoxSizer(wx.VERTICAL)
        gq_sizer.Add(gq_door_select_label, proportion=0, flag=wx.ALL, border=1)  # 调整proportion可使按钮不那么大
        gq_sizer.Add(self.gq_store_cb, proportion=0, flag=wx.ALL, border=15)
        # gq_sizer.Add(gq_store_add, proportion=0, flag=wx.ALL, border=15)
        gq_sizer.Add(gq_store_set_up_not_common, proportion=0, flag=wx.ALL, border=15)
        gq_sizer.Add(gq_store_set_common, proportion=0, flag=wx.ALL, border=15)
        gq_sizer.Add(gq_store_show_all, proportion=0, flag=wx.ALL, border=15)
        gq_sizer.Add(gq_store_show_not_common_use, proportion=0, flag=wx.ALL, border=15)
        gq_sizer.Add(gq_store_show_active, proportion=0, flag=wx.ALL, border=15)
        gq_h_sizer = wx.BoxSizer()
        gq_h_sizer.Add(gq_sizer, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        gq_h_sizer.Add(self.gq_store_door_grid, proportion=1, flag=wx.EXPAND | wx.ALL, border=3)
        self.SetSizer(gq_h_sizer)
        self.Bind(wx.EVT_COMBOBOX_DROPDOWN, self.Evt_Combobox_Dropdown, self.gq_store_cb)  # 下拉事件，点击该事件时，刷新该combobox
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox_Store, self.gq_store_cb)
        # gq_store_add.Bind(wx.EVT_BUTTON, self.OnClick_Gq_Store_Add)
        gq_store_set_up_not_common.Bind(wx.EVT_BUTTON, self.OnClick_Set_Not_Common)
        gq_store_show_all.Bind(wx.EVT_BUTTON, self.OnClick_Show_All_Store)
        gq_store_show_not_common_use.Bind(wx.EVT_BUTTON, self.OnClick_Show_Not_Common_Store)
        gq_store_show_active.Bind(wx.EVT_BUTTON, self.OnClick_Show_Active_Store)
        gq_store_set_common.Bind(wx.EVT_BUTTON, self.OnClick_Set_Common)
    def Interface_Refresh(self):
        self.gq_store_door_grid.My_Refresh(self.gq_company_name,3,'info_dealer_brand','经销商')  # 先获得门店信息，再更新需显示的门店门型
    def Evt_Combobox_Dropdown(self,evt):
        '''
        点击combobox的下拉选项触发的事件
        :param evt:
        :return:
        '''
        self.gq_company_name = Get_All_Store(1)
        self.gq_store_cb.Clear()
        for i in range(len(self.gq_company_name)):
            self.gq_store_cb.Append(self.gq_company_name[i])
    def EvtComboBox_Store(self,evt):
        '''
        查询门店，选择了门店之后，右侧显示对应的信息
        :param evt:
        :return:
        '''
        self.gq_company_name = [evt.GetString()]
        self.Interface_Refresh()
    def OnClick_Gq_Store_Add(self,evt):
        '''
        点击新增门店，弹出wizard
        :param evt:
        :return:
        '''
        pass
    def OnClick_Set_Not_Common(self,evt):
        '''
        设置为不常用门店，除了修改check_state之外，还要修改门店品牌表单中的状态为5
        :param evt:
        :return:
        '''
        self.gq_company_name = []
        try:
            gq_not_common_store = self.gq_store_door_grid.table.data
            db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password,db=database[2], charset=charset)
            cursor = db.cursor()
            for i in range(len(gq_not_common_store)):
                check_value = self.gq_store_door_grid.table.GetValue(i, 0)
                if check_value == 1 :
                    the_dealer = self.gq_store_door_grid.table.GetValue(i, 1)
                    cursor.execute("UPDATE `order_company_info` SET `check_state`= '%s',`synchronization_state`=1 WHERE `company_name`='%s' " % (
                        STATE_NOT_COMMON_STORE, the_dealer))
                    cursor.execute("UPDATE `info_dealer_brand` SET `State`= '%s',`synchronization_state`=1 WHERE `经销商`='%s' " % (
                        STATE_NOT_COMMON_STORE, the_dealer))
                else:
                    self.gq_company_name.append(self.gq_store_door_grid.table.GetValue(i, 1))
            db.commit()
            db.close()
            self.Interface_Refresh()
        except:
            pass
    def OnClick_Show_All_Store(self,evt):
        '''
        显示所有门店
        :param evt:
        :return:
        '''
        self.gq_company_name = Get_All_Store(0)
        self.Interface_Refresh()
    def OnClick_Show_Not_Common_Store(self,evt):
        '''
        显示不常用门店
        :param evt:
        :return:
        '''
        self.gq_company_name = []
        try:
            db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[2],charset=charset)
            cursor = db.cursor()
            cursor.execute("select `company_name` from `order_company_info` where `check_state`='%s'"%STATE_NOT_COMMON_STORE)
            company_name = cursor.fetchall()
            db.close()
            if company_name != () :
                for i in range(len(company_name)):
                    self.gq_company_name.append(company_name[i][0])
            self.Interface_Refresh()
        except:
            pass
    def OnClick_Show_Active_Store(self,evt):
        '''
        显示已激活门店
        :param evt:
        :return:
        '''
        self.gq_company_name = []
        try:
            db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password,
                                 db=database[2], charset=charset)
            cursor = db.cursor()
            cursor.execute("select `company_name` from `order_company_info` where `check_state`=0 or `check_state`=1")
            company_name = cursor.fetchall()
            db.close()
            if company_name != ():
                for i in range(len(company_name)):
                    self.gq_company_name.append(company_name[i][0])
            self.Interface_Refresh()
        except:
            pass
    def OnClick_Set_Common(self,evt):
        '''
        将不常用门店设置为常用门店,同时修改info_dealer_brand表单中对应门店的状态为0
        :param evt:
        :return:
        '''
        self.gq_company_name = []
        try:
            gq_not_common_store = self.gq_store_door_grid.table.data
            db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password,
                                 db=database[2], charset=charset)
            cursor = db.cursor()
            for i in range(len(gq_not_common_store)):
                check_value = self.gq_store_door_grid.table.GetValue(i, 0)
                if check_value == 1:
                    the_dealer = self.gq_store_door_grid.table.GetValue(i, 1)
                    cursor.execute("UPDATE `order_company_info` SET `check_state`= 1,`synchronization_state`=1 WHERE `company_name`='%s' " % the_dealer)
                    cursor.execute("UPDATE `info_dealer_brand` SET `State`= '%s',`synchronization_state`=1 WHERE `经销商`='%s' " % (
                        0, the_dealer))
                else:
                    self.gq_company_name.append(self.gq_store_door_grid.table.GetValue(i, 1))
            db.commit()
            db.close()
            self.Interface_Refresh()
        except:
            pass
#门店门型管理界面
class GQ_Store_Door_Grid(gridlib.Grid):
    def __init__(self, parent,log,number,sheet_name,gq_dealer):
        '''
        从order_company_info表单中将经销商读出来，查看info_dealer_door_type表单内有无该经销商，没有的话将该经销商插入到
        info_dealer_door_type表单内
        number:1:表示经销商与门型的界面显示
        2：品牌与门型的界面显示
        3.经销商与品牌的界面显示
        :param parent:
        :param log:
        '''
        gridlib.Grid.__init__(self, parent, -1,size=(500,600))
        self.log=log
        self.data = []
        self.field_name = ['']
        self.gq_sheet_name = sheet_name
        self.gq_dealer = gq_dealer
        self.gq_modify_col_num = 5     #需修改的字段位置，增加字段时，修改此值即可
        try:
            db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password,
                                 db=database[2], charset=charset)
            cursor = db.cursor()
            # if number == 1 or number == 3:#经销商与门型框,经销商与品牌
            #     cursor.execute("select `company_name` from `order_company_info` where `check_state`=0 or `check_state`=1")
            #     company_name = cursor.fetchall()
            #     if company_name == ():  # 没有经销商
            #         pass
            #     else:
            #         for i in range(len(company_name)):
            #             cursor.execute(
            #                 "select `%s` from `%s` where `%s`='%s'" % (self.gq_dealer,self.gq_sheet_name,self.gq_dealer,company_name[i][0]))
            #             dealer = cursor.fetchall()
            #             if dealer == ():  # 当前经销商在表单中没有,插入到表单中
            #                 cursor.execute(
            #                     "INSERT INTO `%s`(`%s`,`remarks`) VALUES ('%s','%s')" % (self.gq_sheet_name,self.gq_dealer,
            #                         company_name[i][0], ''))
            #         db.commit()
            cursor.execute(
                "select COLUMN_NAME from information_schema.COLUMNS where TABLE_SCHEMA = '%s' AND table_name = '%s'"%(database[2],self.gq_sheet_name))
            column_name = cursor.fetchall()  #去重DISTINCT
            if column_name != ():
                for i in range(1, len(column_name) - self.gq_modify_col_num):
                    if i == 1:
                        if number == 1 or number == 3:  #经销商与门型
                            self.field_name.append('门店名称')
                        else:  #品牌与门型
                            self.field_name.append('品牌名称')
                    else:
                        self.field_name.append(column_name[i][0])
            cursor.execute("select * from `%s` where `State`=0 or `State`=1"%self.gq_sheet_name)
            dealer_door_type = cursor.fetchall()
            if dealer_door_type == ():
                pass
            else:
                for i in range(len(dealer_door_type)):
                    inform = [False,dealer_door_type[i][1]]
                    for j in range(2, len(dealer_door_type[i]) - self.gq_modify_col_num):
                        if dealer_door_type[i][j] == 1:
                            inform.append(True)
                        else:
                            inform.append(False)
                    self.data.append(inform)
            db.close()
            self.table = GQ_Store_Door_Table(self.data,self.field_name)  # 自定义表网格
            self.SetTable(self.table, True)
            self.SetRowLabelSize(0)
            self.SetMargins(0,0)
            self.AutoSizeColumns(False)
            self.DisableDragColSize()
            self.DisableDragRowSize()
            self.Bind(gridlib.EVT_GRID_CELL_CHANGED, self.On_Dealing_Door_Change)
        # self.EnableEditing(False)
        except:
            pass
    def My_Refresh(self,store_information,number,sheet_name,dealer_or_brand):
        '''
        表格刷新
        :return:
        '''
        self.data = []
        try:
            db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password,
                                 db=database[2], charset=charset)
            cursor = db.cursor()
            # if number == 1 or number == 3:
            #     cursor.execute("select `company_name` from `order_company_info` where `check_state`=0 or `check_state`=1")
            #     company_name = cursor.fetchall()
            #     if company_name == ():  # 没有经销商
            #         pass
            #     else:
            #         for i in range(len(company_name)):
            #             cursor.execute(
            #                 "select `%s` from `%s` where `%s`='%s'" % (dealer_or_brand,sheet_name,dealer_or_brand,company_name[i][0]))
            #             dealer = cursor.fetchall()
            #             if dealer == ():  # 当前经销商在表单中没有,插入到表单中
            #                 cursor.execute("INSERT INTO `%s`(`%s`,`remarks`) VALUES ('%s','%s')" % (sheet_name,dealer_or_brand,
            #                 company_name[i][0], ''))
            #         db.commit()
            for i in range(len(store_information)):
                cursor.execute("select * from `%s` where `%s`='%s'"%(sheet_name,dealer_or_brand,store_information[i]))
                dealer_door_type = cursor.fetchone()
                if dealer_door_type == None:
                    pass
                else:
                    inform = [False,dealer_door_type[1]]
                    for j in range(2, len(dealer_door_type)-self.gq_modify_col_num):
                        if dealer_door_type[j] == 1:
                            inform.append(True)
                        else:
                            inform.append(False)
                    self.data.append(inform)
            db.close()
            self.table = GQ_Store_Door_Table(self.data, self.field_name)  # 自定义表网格
            self.SetTable(self.table, True)
            self.SetRowLabelSize(0)
            self.SetMargins(0,0)
            self.AutoSizeColumns(False)
            # self.EnableEditing(False)
            self.DisableDragColSize()
            self.DisableDragRowSize()
        except:
            pass
    def On_Dealing_Door_Change(self,evt):
        try:
            db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password,
                                 db=database[2], charset=charset)
            cursor = db.cursor()
            cursor.execute(
                "select COLUMN_NAME from information_schema.COLUMNS where TABLE_SCHEMA = '%s' AND table_name = '%s'" %(database[2],self.gq_sheet_name))
            column_name = cursor.fetchall()  # 读取列名
            if column_name != ():
                data=self.table.data
                if data[evt.Row][evt.Col] == True:
                    gq_store_door_state = 1
                else:
                    gq_store_door_state = 0
                cursor.execute("UPDATE `%s` SET `%s`= '%s',`synchronization_state`=1 WHERE `%s`='%s' " % (self.gq_sheet_name,column_name[evt.Col][0], gq_store_door_state,self.gq_dealer, data[evt.Row][1]))
                db.commit()
            db.close()
        except:
            pass
class GQ_Store_Door_Table(gridlib.GridTableBase):
    def __init__(self, data,field_name):
        gridlib.GridTableBase.__init__(self)
        self.data=data
        self.field_name=field_name
        self.dataTypes = [gridlib.GRID_VALUE_BOOL,gridlib.GRID_VALUE_STRING]
        i = 1
        while i<len(self.field_name):
            self.dataTypes.append(gridlib.GRID_VALUE_BOOL)
            i+=1

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
        return self.dataTypes[col]

    def CanGetValueAs(self, row, col, typeName):
        colType = self.dataTypes[col].split(':')[0]
        if typeName == colType:
            return True
        else:
            return False

    def CanSetValueAs(self, row, col, typeName):
        return self.CanGetValueAs(row, col, typeName)
class Store_Door_Management(wx.Panel):
    def __init__(self,parent,log):
        wx.Panel.__init__(self, parent, -1)
        self.log=log
        gq_door_select_label=wx.StaticText(self, -1, "     门店查询", (8, 10))
        self.gq_company_name = Get_All_Store(1)
        self.gq_store_cb = wx.ComboBox(self, 500, "", (50, 50),(110, -1), self.gq_company_name,wx.CB_DROPDOWN)
        # gq_store_add = wx.Button(self, 10, "    新增门店     ", (50, 50))
        gq_store_set_up_not_common = wx.Button(self, 10, "设为不常用门店 ", (50, 50))
        gq_store_set_common = wx.Button(self, 10, "  设为常用门店  ", (50, 50))
        gq_store_show_all = wx.Button(self, 10, "  显示全部门店  ", (50, 50))
        gq_store_show_not_common_use = wx.Button(self, 10, " 显示不常用门店", (50, 50))
        gq_store_show_active = wx.Button(self, 10, " 显示已激活门店", (50, 50))
        self.gq_store_door_grid = GQ_Store_Door_Grid(self, self.log,1,'info_dealer_door_type','Dealer')
        gq_sizer=wx.BoxSizer(wx.VERTICAL)
        gq_sizer.Add(gq_door_select_label, proportion=0, flag=wx.ALL, border=1)  #调整proportion可使按钮不那么大
        gq_sizer.Add(self.gq_store_cb, proportion=0, flag=wx.ALL, border=15)
        # gq_sizer.Add(gq_store_add, proportion=0, flag=wx.ALL, border=15)
        gq_sizer.Add(gq_store_set_up_not_common, proportion=0, flag=wx.ALL, border=15)
        gq_sizer.Add(gq_store_set_common, proportion=0, flag=wx.ALL, border=15)
        gq_sizer.Add(gq_store_show_all, proportion=0, flag=wx.ALL, border=15)
        gq_sizer.Add(gq_store_show_not_common_use, proportion=0, flag=wx.ALL, border=15)
        gq_sizer.Add(gq_store_show_active, proportion=0, flag=wx.ALL, border=15)
        gq_h_sizer = wx.BoxSizer()
        gq_h_sizer.Add(gq_sizer, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        gq_h_sizer.Add(self.gq_store_door_grid, proportion=1, flag=wx.EXPAND | wx.ALL, border=3)
        self.SetSizer(gq_h_sizer)
        self.Bind(wx.EVT_COMBOBOX_DROPDOWN, self.Evt_Combobox_Dropdown, self.gq_store_cb)  # 下拉事件，点击该事件时，刷新该combobox
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox_Store, self.gq_store_cb)
        # gq_store_add.Bind(wx.EVT_BUTTON, self.OnClick_Gq_Store_Add)
        gq_store_set_up_not_common.Bind(wx.EVT_BUTTON, self.OnClick_Set_Not_Common)
        gq_store_show_all.Bind(wx.EVT_BUTTON, self.OnClick_Show_All_Store)
        gq_store_show_not_common_use.Bind(wx.EVT_BUTTON, self.OnClick_Show_Not_Common_Store)
        gq_store_show_active.Bind(wx.EVT_BUTTON, self.OnClick_Show_Active_Store)
        gq_store_set_common.Bind(wx.EVT_BUTTON, self.OnClick_Set_Common)
    def Interface_Refresh(self):
        self.gq_store_door_grid.My_Refresh(self.gq_company_name,1,'info_dealer_door_type','Dealer')  # 先获得门店信息，再更新需显示的门店门型
    def Evt_Combobox_Dropdown(self,evt):
        '''
        点击combobox的下拉选项触发的事件
        :param evt:
        :return:
        '''
        self.gq_company_name = Get_All_Store(1)
        self.gq_store_cb.Clear()
        for i in range(len(self.gq_company_name)):
            self.gq_store_cb.Append(self.gq_company_name[i])
    def EvtComboBox_Store(self,evt):
        '''
        查询门店，选择了门店之后，右侧显示对应的信息
        :param evt:
        :return:
        '''
        self.gq_company_name = [evt.GetString()]
        self.Interface_Refresh()
    def OnClick_Gq_Store_Add(self,evt):
        '''
        点击新增门店，弹出wizard
        :param evt:
        :return:
        '''
        wizard = wiz(self, -1, "新增门店")
        page1 = TitledPage(wizard, "门店基础信息")
        page2 = TitledPage(wizard, "门店品牌信息")
        page3 = TitledPage(wizard, "门店门型信息")
        page4 = TitledPage(wizard, "门店结算信息")
        self.page1 = page1

        page1.sizer.Add(wx.StaticText(page1, -1, ''))
        wizard.FitToPage(page1)
        page4.sizer.Add(wx.StaticText(page4, -1, "\nThis is the last page."))

        # Use the convenience Chain function to connect the pages
        WizardPageSimple.Chain(page1, page2)
        WizardPageSimple.Chain(page2, page3)
        WizardPageSimple.Chain(page3, page4)

        wizard.GetPageAreaSizer().Add(page1)
        if wizard.RunWizard(page1):
            wx.MessageBox("Wizard completed successfully", "That's all folks!")
        else:
            wx.MessageBox("Wizard was cancelled", "That's all folks!")
    def OnClick_Set_Not_Common(self,evt):
        '''
        设置为不常用门店，将选中的经销商的记录状态置为10
        :param evt:
        :return:
        '''
        self.gq_company_name = []
        try:
            gq_not_common_store = self.gq_store_door_grid.table.data
            db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password,db=database[2], charset=charset)
            cursor = db.cursor()
            for i in range(len(gq_not_common_store)):
                check_value = self.gq_store_door_grid.table.GetValue(i, 0)
                if check_value == 1 :
                    the_dealer = self.gq_store_door_grid.table.GetValue(i, 1)
                    cursor.execute("UPDATE `order_company_info` SET `check_state`= '%s',`synchronization_state`=1 WHERE `company_name`='%s' " % (
                        STATE_NOT_COMMON_STORE, the_dealer))
                    cursor.execute("UPDATE `info_dealer_door_type` SET `State`= '%s',`synchronization_state`=1 WHERE `Dealer`='%s' " % (
                        STATE_NOT_COMMON_STORE, the_dealer))
                else:
                    self.gq_company_name.append(self.gq_store_door_grid.table.GetValue(i, 1))
            db.commit()
            db.close()
            self.Interface_Refresh()
        except:
            pass
    def OnClick_Show_All_Store(self,evt):
        '''
        显示所有门店
        :param evt:
        :return:
        '''
        self.gq_company_name = Get_All_Store(0)
        self.Interface_Refresh()
    def OnClick_Show_Not_Common_Store(self,evt):
        '''
        显示不常用门店
        :param evt:
        :return:
        '''
        self.gq_company_name = []
        try:
            db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[2],charset=charset)
            cursor = db.cursor()
            cursor.execute("select `company_name` from `order_company_info` where `check_state`='%s'"%STATE_NOT_COMMON_STORE)
            company_name = cursor.fetchall()
            db.close()
            if company_name != () :
                for i in range(len(company_name)):
                    self.gq_company_name.append(company_name[i][0])
            self.Interface_Refresh()
        except:
            pass
    def OnClick_Show_Active_Store(self,evt):
        '''
        显示已激活门店
        :param evt:
        :return:
        '''
        self.gq_company_name = []
        try:
            db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password,
                                 db=database[2], charset=charset)
            cursor = db.cursor()
            cursor.execute("select `company_name` from `order_company_info` where `check_state`=0 or `check_state`=1")
            company_name = cursor.fetchall()
            db.close()
            if company_name != ():
                for i in range(len(company_name)):
                    self.gq_company_name.append(company_name[i][0])
            self.Interface_Refresh()
        except:
            pass
    def OnClick_Set_Common(self,evt):
        '''
        将不常用门店设置为常用门店，将info_dealer_door_type中的门型状态改为0
        :param evt:
        :return:
        '''
        self.gq_company_name = []
        try:
            gq_not_common_store = self.gq_store_door_grid.table.data
            db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password,
                                 db=database[2], charset=charset)
            cursor = db.cursor()
            for i in range(len(gq_not_common_store)):
                check_value = self.gq_store_door_grid.table.GetValue(i, 0)
                if check_value == 1:
                    the_dealer = self.gq_store_door_grid.table.GetValue(i, 1)
                    cursor.execute("UPDATE `order_company_info` SET `check_state`= 1,`synchronization_state`=1 WHERE `company_name`='%s' " % the_dealer)
                    cursor.execute("UPDATE `info_dealer_door_type` SET `State`= 0,`synchronization_state`=1 WHERE `Dealer`='%s' " % the_dealer)
                else:
                    self.gq_company_name.append(self.gq_store_door_grid.table.GetValue(i, 1))
            db.commit()
            db.close()
            self.Interface_Refresh()
        except:
            pass
class TitledPage(wx.adv.WizardPageSimple):
    def __init__(self, parent, title):
        WizardPageSimple.__init__(self, parent)
        self.sizer = makePageTitle(self, title)
def makePageTitle(wizPg, title):
    sizer = wx.BoxSizer(wx.VERTICAL)
    wizPg.SetSizer(sizer)
    title = wx.StaticText(wizPg, -1, title)
    title.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
    sizer.Add(title, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
    sizer.Add(wx.StaticLine(wizPg, -1), 0, wx.EXPAND|wx.ALL, 5)
    return sizer
class SkipNextPage(wx.adv.WizardPage):
    def __init__(self, parent, title):
        WizardPage.__init__(self, parent)
        self.next = self.prev = None
        self.sizer = makePageTitle(self, title)

        self.cb = wx.CheckBox(self, -1, "Skip next page")
        self.sizer.Add(self.cb, 0, wx.ALL, 5)

    def SetNext(self, next):
        self.next = next

    def SetPrev(self, prev):
        self.prev = prev


    # Classes derived from wxPyWizardPanel must override
    # GetNext and GetPrev, and may also override GetBitmap
    # as well as all those methods overridable by
    # wx.PyWindow.

    def GetNext(self):
        """If the checkbox is set then return the next page's next page"""
        if self.cb.GetValue():
            self.next.GetNext().SetPrev(self)
            return self.next.GetNext()
        else:
            self.next.GetNext().SetPrev(self.next)
            return self.next

    def GetPrev(self):
        return self.prev
class UseAltBitmapPage(WizardPage):
        def __init__(self, parent, title):
            WizardPage.__init__(self, parent)
            self.next = self.prev = None
            self.sizer = makePageTitle(self, title)

            self.sizer.Add(wx.StaticText(self, -1, "This page uses a different bitmap"),
                           0, wx.ALL, 5)

        def SetNext(self, next):
            self.next = next

        def SetPrev(self, prev):
            self.prev = prev

        def GetNext(self):
            return self.next

        def GetPrev(self):
            return self.prev

        def GetBitmap(self):
            # You usually wouldn't need to override this method
            # since you can set a non-default bitmap in the
            # wxWizardPageSimple constructor, but if you need to
            # dynamically change the bitmap based on the
            # contents of the wizard, or need to also change the
            # next/prev order then it can be done by overriding
            # GetBitmap.
            return images.WizTest2.GetBitmap()
class GQ_Add_New_Store_Panel(wx.Panel):
    def __init__(self,parent,log):
        wx.Panel.__init__(self, parent, -1)
        self.log=log
        gq_door_name_label = wx.StaticText(self, -1, "  门店名称", (8, 10))
        gq_door_select_label = wx.TextCtrl(self, -1,
                        "Here is a looooooooooooooong line of text set in the control.\n\n"
                        "The quick brown fox jumped over the lazy dog...",
                       size=(200, 100), style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)
class GQ_Prompt_Dialog(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, '', size=(230, 140))
        wx.StaticText(self, -1, "     是否确认进行以上修改?" , (20, 20))
        wx.Button(self, wx.ID_OK, '确认', pos=(20, 60))
        wx.Button(self,wx.ID_CANCEL,'取消',pos=(120,60))
#品牌门型管理
class Brand_Door_Management(wx.Panel):
    def __init__(self,parent,log):
        wx.Panel.__init__(self, parent, -1)
        self.log=log
        gq_door_select_label=wx.StaticText(self, -1, "     品牌查询", (8, 10))
        self.Get_All_Brand(1)
        self.gq_store_cb = wx.ComboBox(self, 500, "", (50, 50),(110, -1), self.gq_company_name,wx.CB_DROPDOWN)
        # gq_store_add = wx.Button(self, 10, "    新增品牌     ", (50, 50))
        gq_store_set_up_not_common = wx.Button(self, 10, "设为不常用品牌 ", (50, 50))
        gq_store_set_common = wx.Button(self, 10, "  设为常用品牌  ", (50, 50))
        gq_store_show_all = wx.Button(self, 10, "  显示全部品牌  ", (50, 50))
        gq_store_show_not_common_use = wx.Button(self, 10, " 显示不常用品牌", (50, 50))
        gq_store_show_active = wx.Button(self, 10, " 显示已激活品牌", (50, 50))
        self.gq_store_door_grid = GQ_Store_Door_Grid(self, self.log,2,'info_brand_door_type','Brand')
        gq_sizer=wx.BoxSizer(wx.VERTICAL)
        gq_sizer.Add(gq_door_select_label, proportion=0, flag=wx.ALL, border=1)  #调整proportion可使按钮不那么大
        gq_sizer.Add(self.gq_store_cb, proportion=0, flag=wx.ALL, border=15)
        # gq_sizer.Add(gq_store_add, proportion=0, flag=wx.ALL, border=15)
        gq_sizer.Add(gq_store_set_up_not_common, proportion=0, flag=wx.ALL, border=15)
        gq_sizer.Add(gq_store_set_common, proportion=0, flag=wx.ALL, border=15)
        gq_sizer.Add(gq_store_show_all, proportion=0, flag=wx.ALL, border=15)
        gq_sizer.Add(gq_store_show_not_common_use, proportion=0, flag=wx.ALL, border=15)
        gq_sizer.Add(gq_store_show_active, proportion=0, flag=wx.ALL, border=15)
        gq_h_sizer = wx.BoxSizer()
        gq_h_sizer.Add(gq_sizer, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        gq_h_sizer.Add(self.gq_store_door_grid, proportion=1, flag=wx.EXPAND | wx.ALL, border=3)
        self.SetSizer(gq_h_sizer)
        self.Bind(wx.EVT_COMBOBOX_DROPDOWN, self.Evt_Combobox_Dropdown, self.gq_store_cb)  # 下拉事件，点击该事件时，刷新该combobox
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox_Store, self.gq_store_cb)
        # gq_store_add.Bind(wx.EVT_BUTTON, self.OnClick_Gq_Store_Add)
        gq_store_set_up_not_common.Bind(wx.EVT_BUTTON, self.OnClick_Set_Not_Common)
        gq_store_show_all.Bind(wx.EVT_BUTTON, self.OnClick_Show_All_Store)
        gq_store_show_not_common_use.Bind(wx.EVT_BUTTON, self.OnClick_Show_Not_Common_Store)
        gq_store_show_active.Bind(wx.EVT_BUTTON, self.OnClick_Show_Active_Store)
        gq_store_set_common.Bind(wx.EVT_BUTTON, self.OnClick_Set_Common)
    def Get_All_Brand(self,number):
        '''
        获得所有门店
        :return:
        '''
        self.gq_company_name = []
        try:
            db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password,
                                 db=database[2], charset=charset)
            cursor = db.cursor()
            if number == 0 :
                cursor.execute("select `Brand` from `info_brand_door_type` where 1")
                company_name = cursor.fetchall()
            else:  #激活门店
                cursor.execute("select `Brand` from `info_brand_door_type` where `State`=1 or `State`=0")
                company_name = cursor.fetchall()
            db.close()
            if company_name == ():  # 没有品牌
                pass
            else:
                for i in range(len(company_name)):
                    self.gq_company_name.append(company_name[i][0])
        except:
            pass
    def Interface_Refresh(self):
        self.gq_store_door_grid.My_Refresh(self.gq_company_name,2,'info_brand_door_type','Brand')  # 先获得门店信息，再更新需显示的门店门型
    def Evt_Combobox_Dropdown(self,evt):
        '''
        点击combobox的下拉选项触发的事件
        :param evt:
        :return:
        '''
        self.Get_All_Brand(1)
        self.gq_store_cb.Clear()
        for i in range(len(self.gq_company_name)):
            self.gq_store_cb.Append(self.gq_company_name[i])
    def EvtComboBox_Store(self,evt):
        '''
        查询门店，选择了门店之后，右侧显示对应的信息
        :param evt:
        :return:
        '''
        self.gq_company_name = [evt.GetString()]
        self.Interface_Refresh()
    def OnClick_Gq_Store_Add(self,evt):
        '''
        点击新增门店，弹出wizard
        :param evt:
        :return:
        '''
        pass
    def OnClick_Set_Not_Common(self,evt):
        '''
        设置为不常用门店，将选中的经销商的记录状态置为10
        :param evt:
        :return:
        '''
        self.gq_company_name = []
        try:
            gq_not_common_store = self.gq_store_door_grid.table.data
            db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password,db=database[2], charset=charset)
            cursor = db.cursor()
            for i in range(len(gq_not_common_store)):
                check_value = self.gq_store_door_grid.table.GetValue(i, 0)
                if check_value == 1 :
                    the_dealer = self.gq_store_door_grid.table.GetValue(i, 1)
                    cursor.execute("UPDATE `info_brand_door_type` SET `State`= '%s',`synchronization_state`=1 WHERE `Brand`='%s' " % (
                        STATE_NOT_COMMON_STORE, the_dealer))
                else:
                    self.gq_company_name.append(self.gq_store_door_grid.table.GetValue(i, 1))
            db.commit()
            db.close()
            self.Interface_Refresh()
        except:
            pass
    def OnClick_Show_All_Store(self,evt):
        '''
        显示所有门店
        :param evt:
        :return:
        '''
        self.Get_All_Brand(0)
        self.Interface_Refresh()
    def OnClick_Show_Not_Common_Store(self,evt):
        '''
        显示不常用门店
        :param evt:
        :return:
        '''
        self.gq_company_name = []
        try:
            db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[2],charset=charset)
            cursor = db.cursor()
            cursor.execute("select `Brand` from `info_brand_door_type` where `State`='%s'"%STATE_NOT_COMMON_STORE)
            company_name = cursor.fetchall()
            db.close()
            if company_name != () :
                for i in range(len(company_name)):
                    self.gq_company_name.append(company_name[i][0])
            self.Interface_Refresh()
        except:
            pass
    def OnClick_Show_Active_Store(self,evt):
        '''
        显示已激活门店
        :param evt:
        :return:
        '''
        self.gq_company_name = []
        try:
            db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password,
                                 db=database[2], charset=charset)
            cursor = db.cursor()
            cursor.execute("select `Brand` from `info_brand_door_type` where `State`=1 or `State`=0")
            company_name = cursor.fetchall()
            db.close()
            if company_name != ():
                for i in range(len(company_name)):
                    self.gq_company_name.append(company_name[i][0])
            self.Interface_Refresh()
        except:
            pass
    def OnClick_Set_Common(self,evt):
        '''
        点击确认修改，弹出一个对话框，确认是否进行门店门型修改，点击确认时，将对应的门型勾选跟新到数据库中
        :param evt:
        :return:
        '''
        self.gq_company_name = []
        try:
            gq_not_common_store = self.gq_store_door_grid.table.data
            db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password,
                                 db=database[2], charset=charset)
            cursor = db.cursor()
            for i in range(len(gq_not_common_store)):
                check_value = self.gq_store_door_grid.table.GetValue(i, 0)
                if check_value == 1:
                    the_dealer = self.gq_store_door_grid.table.GetValue(i, 1)
                    cursor.execute("UPDATE `info_brand_door_type` SET `State`= 1,`synchronization_state`=1 WHERE `Brand`='%s' "% the_dealer)
                else:
                    self.gq_company_name.append(self.gq_store_door_grid.table.GetValue(i, 1))
            db.commit()
            db.close()
            self.Interface_Refresh()
        except:
            pass
#门店付款方式管理
class GQ_Store_Payment_Grid(gridlib.Grid):
    def __init__(self, parent,log,dealer_name):
        '''
        从250数据库中的合同表单中根据经销商名称按时间降序排列读出所有记录，统计每个月的合同平方数，合同数（笔数），总计：(元)，
        月结：（元），定金支付（元），现金支付：（元），已支付（元），剩余月结未支付（元），剩余定金未支付（元），剩余现金未支付（元）
        :param parent:
        :param log:
        '''
        self.gq_company_other_information = ['', '',0,0,0,0]
        gridlib.Grid.__init__(self, parent, -1,size=(500,600))
        self.log=log
        self.data = []  #记录每个月的合同平方数及总计，月结等
        self.field_name = ['创建时间','合同数','合同平方数(平方米)','总计(元)','已支付(元)','未支付(元)','月结方式已支付(元)','定金方式已支付(元)','立即方式已支付(元)','月结方式剩余未支付(元)','定金方式剩余未支付(元)','立即方式剩余未支付(元)','编辑项']
        try:
            db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password,db=database[0], charset=charset)
            cursor = db.cursor()
            cursor.execute(
                "select `Contract_C_Time`,`Contract_area`,`Contract_price`,`Deposit_has_been_paid`,`Deposit_has_not_been_paid`,`pay_type` from `order_contract_internal` where `Dealer`='%s'and`pay_type`<>'%s' and`pay_type`<>'%s'and`pay_type`<>0 order by `Contract_C_Time`desc" %
                (dealer_name[0],STATE_MONTHLY_PAY_OTHER,STATE_DEPOSIT_PAY_OTHER))
            contract_information = cursor.fetchall()
            db.close()
            if contract_information != ():
                for i in range(len(contract_information)+1):
                    if i == len(contract_information):  #最后一列
                        self.data.append(['总计', 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0,'明细'])
                        for j in range(len(self.data)-1):
                            for k in range(1,len(self.data[0])-1):
                                self.data[len(self.data)-1][k] += self.data[j][k]
                    else:
                        now_year_and_month = contract_information[i][0].strftime("%Y-%m")
                        if now_year_and_month not in [x[0] for x in self.data]:
                            self.data.append([now_year_and_month, 0,0, 0, 0, 0, 0, 0, 0, 0, 0,0,'明细'])
                        for j in range(len(self.data)):
                            if now_year_and_month == self.data[j][0]:
                                self.data[j][1] += 1
                                for k in range(1, 5):
                                    if contract_information[i][k] != None:
                                        self.data[j][k+1] += contract_information[i][k]
                                if contract_information[i][5] == STATE_IMMEDIATELY_PAY : #现金支付
                                    self.data[j][8] += contract_information[i][3]
                                    self.data[j][11] += contract_information[i][4]
                                elif contract_information[i][5] == STATE_MONTHLY_PAY : #月结
                                    self.data[j][6] += contract_information[i][3]
                                    self.data[j][9] += contract_information[i][4]
                                elif contract_information[i][5] == STATE_DEPOSIT_PAY : #定金支付
                                    self.data[j][7] += contract_information[i][3]
                                    self.data[j][10] += contract_information[i][4]
                                break
            self.table = GQ_Store_Payment_Table(self.data,self.field_name)  # 自定义表网格
            self.SetTable(self.table, True)
            for i in range(len(self.data)):
                self.SetCellBackgroundColour(i, len(self.field_name)-1, wx.YELLOW)
                self.SetCellAlignment(i, len(self.field_name) - 1, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)  # 设置居中
            self.SetRowLabelSize(0)
            self.SetMargins(0,0)
            self.AutoSizeColumns(False)
            self.SetColSize(len(self.field_name) - 1, 50)  # 设置列宽
            self.DisableDragColSize()
            self.EnableEditing(False)
            self.DisableDragRowSize()
        except:
            pass
    def My_Refresh(self,dealer_name):
        '''
        表格刷新
        :return:
        '''
        self.data = []
        try:
            db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password,
                                 db=database[0], charset=charset)
            db_manage = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password,
                                 db=database[2], charset=charset)
            cursor = db.cursor()
            cursor_manage= db_manage.cursor()
            cursor.execute(
                "select `Contract_C_Time`,`Contract_area`,`Contract_price`,`Deposit_has_been_paid`,`Deposit_has_not_been_paid`,`pay_type` from `order_contract_internal` where `Dealer`='%s'and`pay_type`<>'%s' and`pay_type`<>'%s'and`pay_type`<>0 order by `Contract_C_Time`desc" %
                (dealer_name[0], STATE_MONTHLY_PAY_OTHER, STATE_DEPOSIT_PAY_OTHER))
            contract_information = cursor.fetchall()
            cursor_manage.execute(
                "select `manager_name`,`manager_mobile`,`Monthly_knot`,`Payment_of_deposit`,`Deposit_ratio`,`discount` from `order_company_info` where `company_name`='%s'" %
                dealer_name[0])
            company_information = cursor_manage.fetchone()
            db.close()
            db_manage.close()
            if company_information != None :
                for i in range(len(company_information)):
                    self.gq_company_other_information[i] = company_information[i]
            if contract_information != ():
                for i in range(len(contract_information)+1):
                    if i == len(contract_information):  #最后一列
                        self.data.append(['总计', 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0,'明细'])
                        for j in range(len(self.data)-1):
                            for k in range(1,len(self.data[0])-1):
                                self.data[len(self.data)-1][k] += self.data[j][k]
                    else:
                        now_year_and_month = contract_information[i][0].strftime("%Y-%m")
                        if now_year_and_month not in [x[0] for x in self.data]:
                            self.data.append([now_year_and_month, 0,0, 0, 0, 0, 0, 0, 0, 0, 0,0,'明细'])
                        for j in range(len(self.data)):
                            if now_year_and_month == self.data[j][0]:
                                self.data[j][1] += 1
                                for k in range(1, 5):
                                    if contract_information[i][k] != None:
                                        self.data[j][k+1] += contract_information[i][k]
                                if contract_information[i][5] == STATE_IMMEDIATELY_PAY : #现金支付
                                    self.data[j][8] += contract_information[i][3]
                                    self.data[j][11] += contract_information[i][4]
                                elif contract_information[i][5] == STATE_MONTHLY_PAY : #月结
                                    self.data[j][6] += contract_information[i][3]
                                    self.data[j][9] += contract_information[i][4]
                                elif contract_information[i][5] == STATE_DEPOSIT_PAY : #定金支付
                                    self.data[j][7] += contract_information[i][3]
                                    self.data[j][10] += contract_information[i][4]
                                break
            self.table = GQ_Store_Payment_Table(self.data, self.field_name)  # 自定义表网格
            self.SetTable(self.table, True)
            for i in range(len(self.data)):
                self.SetCellBackgroundColour(i, len(self.field_name)-1, wx.YELLOW)  #设置背景颜色
                self.SetCellAlignment(i,len(self.field_name)-1,wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)  #设置居中
            self.SetRowLabelSize(0)
            self.SetMargins(0,0)
            self.AutoSizeColumns(False)
            self.SetColSize(len(self.field_name) - 1, 50)  # 设置列宽
            self.DisableDragColSize()
            self.DisableDragRowSize()
            self.EnableEditing(False)
        except:
            pass
class GQ_Store_Payment_Table(gridlib.GridTableBase):
    def __init__(self, data,field_name):
        gridlib.GridTableBase.__init__(self)
        self.data=data
        self.field_name=field_name
        self.dataTypes = [gridlib.GRID_VALUE_STRING,gridlib.GRID_VALUE_NUMBER,gridlib.GRID_VALUE_STRING,gridlib.GRID_VALUE_STRING,gridlib.GRID_VALUE_STRING,gridlib.GRID_VALUE_STRING,gridlib.GRID_VALUE_STRING,gridlib.GRID_VALUE_STRING,gridlib.GRID_VALUE_STRING,gridlib.GRID_VALUE_STRING,gridlib.GRID_VALUE_STRING,gridlib.GRID_VALUE_STRING,gridlib.GRID_VALUE_STRING]

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
        return self.dataTypes[col]

    def CanGetValueAs(self, row, col, typeName):
        colType = self.dataTypes[col].split(':')[0]
        if typeName == colType:
            return True
        else:
            return False

    def CanSetValueAs(self, row, col, typeName):
        return self.CanGetValueAs(row, col, typeName)
class Store_Pay_Way_Management(wx.Panel):
    def __init__(self,parent,log):
        wx.Panel.__init__(self, parent, -1)
        self.log=log
        gq_door_select_label = wx.StaticText(self, -1, "门店查询", (8, 10))
        self.Get_All_Store(1)
        self.gq_store_cb = wx.ComboBox(self, 500, self.gq_company_name[0], (50, 50), (110, -1), self.gq_company_name, wx.CB_DROPDOWN)
        gq_door_manager_name_label = wx.StaticText(self, -1, "门店联系人:", (8, 10))
        self.gq_door_manager_name = wx.StaticText(self, -1, '     '+ self.gq_company_other_information[0], (8, 10))
        gq_door_manager_num_label = wx.StaticText(self, -1, "门店联系电话:", (8, 10))
        self.gq_door_manager_num = wx.StaticText(self, -1, '     ' + self.gq_company_other_information[1], (8, 10))
        door_manager_label = wx.StaticText(self, -1, "业务经理:", (8, 10))
        self.door_manager = wx.StaticText(self, -1, '     ' + self.gq_company_other_information[6], (8, 10))
        door_manager_num_label = wx.StaticText(self, -1, "业务经理电话:", (8, 10))
        self.door_manager_num = wx.StaticText(self, -1, '     ' +self.gq_company_other_information[7], (8, 10))
        gq_door_pay_way_label = wx.StaticText(self, -1, "支付方式", (8, 10))
        self.gq_pay_month = wx.CheckBox(self, -1, "   月结支付")
        self.gq_pay_deposit = wx.CheckBox(self, -1, "   定金支付")
        self.gq_pay_deposit_ratio_label = wx.StaticText(self, -1, "支付比率 : ", (8, 10))
        self.gq_pay_deposit_ratio = wx.TextCtrl(self, -1, "", size=(40, -1))
        gq_ratio_sizer = wx.BoxSizer()
        gq_ratio_sizer.Add(self.gq_pay_deposit_ratio_label, proportion=0, flag=wx.ALL, border=2)
        gq_ratio_sizer.Add(self.gq_pay_deposit_ratio, proportion=0, flag=wx.ALL, border=2)
        self.gq_discount_ratio_label = wx.StaticText(self, -1, "折扣比率 : ", (8, 10))
        self.gq_discount_ratio = wx.TextCtrl(self, -1, "", size=(40, -1))
        gq_deposit_ratio_sizer = wx.BoxSizer()
        gq_deposit_ratio_sizer.Add(self.gq_discount_ratio_label, proportion=0, flag=wx.ALL, border=2)
        gq_deposit_ratio_sizer.Add(self.gq_discount_ratio, proportion=0, flag=wx.ALL, border=2)
        self.gq_door_edit =wx.Button(self, 10, "编辑", (8, 20),size=(110,-1))
        self.gq_door_confirm =wx.Button(self, 10, "确认", (8, 20),size=(110,-1))
        gq_sizer = wx.BoxSizer(wx.VERTICAL)
        gq_sizer.Add(gq_door_select_label, proportion=0, flag=wx.ALL, border=1)  # 调整proportion可使按钮不那么大
        gq_sizer.Add(self.gq_store_cb, proportion=0, flag=wx.ALL, border=8)
        gq_sizer.Add(gq_door_manager_name_label, proportion=0, flag=wx.ALL, border=5)
        gq_sizer.Add(self.gq_door_manager_name, proportion=0, flag=wx.ALL, border=5)
        gq_sizer.Add(gq_door_manager_num_label, proportion=0, flag=wx.ALL, border=5)
        gq_sizer.Add(self.gq_door_manager_num, proportion=0, flag=wx.ALL, border=5)
        gq_sizer.Add(door_manager_label, proportion=0, flag=wx.ALL, border=5)
        gq_sizer.Add(self.door_manager, proportion=0, flag=wx.ALL, border=5)
        gq_sizer.Add(door_manager_num_label, proportion=0, flag=wx.ALL, border=5)
        gq_sizer.Add(self.door_manager_num, proportion=0, flag=wx.ALL, border=5)
        gq_sizer.Add(gq_door_pay_way_label, proportion=0, flag=wx.ALL, border=5)
        gq_sizer.Add(self.gq_pay_month, proportion=0, flag=wx.ALL, border=5)
        gq_sizer.Add(self.gq_pay_deposit, proportion=0, flag=wx.ALL, border=5)
        gq_sizer.Add(gq_ratio_sizer, proportion=0, flag=wx.ALL, border=5)
        gq_sizer.Add(gq_deposit_ratio_sizer, proportion=0, flag=wx.ALL, border=5)
        gq_sizer.Add(self.gq_door_edit, proportion=0, flag=wx.ALL, border=5)
        gq_sizer.Add(self.gq_door_confirm, proportion=0, flag=wx.ALL, border=5)
        gq_h_sizer = wx.BoxSizer()
        self.gq_store_pay_grid = GQ_Store_Payment_Grid(self, self.log,self.gq_company_name[0])
        gq_h_sizer.Add(gq_sizer, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        gq_h_sizer.Add(self.gq_store_pay_grid, proportion=1, flag=wx.EXPAND | wx.ALL, border=3)
        self.SetSizer(gq_h_sizer)
        self.gq_door_edit.Bind(wx.EVT_BUTTON, self.OnClick_Door_Edit)
        self.gq_door_confirm.Bind(wx.EVT_BUTTON, self.OnClick_Door_Confirm)
        self.Bind(wx.EVT_COMBOBOX_DROPDOWN, self.Evt_Combobox_Dropdown, self.gq_store_cb)  # 下拉事件，点击该事件时，刷新该combobox
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox_Store, self.gq_store_cb)
        self.Bind(wx.EVT_TEXT, self.EvtText_Ratio, self.gq_pay_deposit_ratio)
        self.Bind(wx.EVT_TEXT, self.EvtText_Discount_Ratio, self.gq_discount_ratio)
        self.gq_pay_month.ThreeStateValue = int(self.gq_company_other_information[2])
        self.gq_pay_deposit.ThreeStateValue = int(self.gq_company_other_information[3])
        self.gq_pay_deposit_ratio.SetValue(str(self.gq_company_other_information[4]))
        self.gq_discount_ratio.SetValue(str(self.gq_company_other_information[5]))
        self.gq_pay_month.Enabled=False
        self.gq_pay_deposit.Enabled=False
        self.gq_door_confirm.Enabled=False
        self.gq_pay_deposit_ratio.Enabled=False
        self.gq_discount_ratio.Enabled=False
        self.gq_store_pay_grid.Bind(gridlib.EVT_GRID_CELL_LEFT_DCLICK, self.On_Check_Detail)
    def Get_All_Store(self,number):
        '''
        获得所有门店,获得当前门店的 支付方式以及支付比率，折扣比率
        :return:
        '''
        self.gq_company_name = []
        self.gq_company_other_information = ['','',0,0,0,0,'','']  #门店联系人，联系地址，支付方式（月结，定金），支付比率，折扣比率
        try:
            db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password,
                                 db=database[2], charset=charset)
            cursor = db.cursor()
            if number == 0 :
                cursor.execute("select `company_name` from `order_company_info` where 1")
                company_name = cursor.fetchall()
            else:
                cursor.execute("select `company_name` from `order_company_info` where `check_state`=0 or `check_state`=1")
                company_name = cursor.fetchall()
            if company_name == ():  # 没有经销商
                pass
            else:
                for i in range(len(company_name)):
                    self.gq_company_name.append(company_name[i][0])
                cursor.execute(
                    "select `manager_name`,`manager_mobile`,`Monthly_knot`,`Payment_of_deposit`,`Deposit_ratio`,`discount`,`Sales_manager_name`,`Sales_manager_phone` from `order_company_info` where `company_name`='%s'" %self.gq_company_name[0])
                company_information = cursor.fetchone()
                if company_information != None:
                    for i in range(len(company_information)):
                        if company_information[i] != None:
                            self.gq_company_other_information[i]=company_information[i]
            db.close()
        except:
            pass
        if self.gq_company_name == [] :
            self.gq_company_name=['']
    def Evt_Combobox_Dropdown(self,evt):
        '''
        点击combobox的下拉选项触发的事件
        :param evt:
        :return:
        '''
        self.Get_All_Store(1)
        self.gq_store_cb.Clear()
        for i in range(len(self.gq_company_name)):
            self.gq_store_cb.Append(self.gq_company_name[i])
    def EvtComboBox_Store(self,evt):
        '''
        查询门店，选择了门店之后，右侧显示对应的信息
        :param evt:
        :return:
        '''
        self.gq_company_name = [evt.GetString()]
        self.gq_store_pay_grid.My_Refresh(self.gq_company_name)
        self.gq_pay_month.ThreeStateValue = int(self.gq_store_pay_grid.gq_company_other_information[2])
        self.gq_pay_deposit.ThreeStateValue = int(self.gq_store_pay_grid.gq_company_other_information[3])
        self.gq_pay_deposit_ratio.SetValue(str(self.gq_store_pay_grid.gq_company_other_information[4]))
        self.gq_discount_ratio.SetValue(str(self.gq_store_pay_grid.gq_company_other_information[5]))
        self.gq_door_manager_name.LabelText='     '+self.gq_store_pay_grid.gq_company_other_information[0]
        self.gq_door_manager_num.LabelText='     '+self.gq_store_pay_grid.gq_company_other_information[1]
    def OnClick_Door_Edit(self,evt):
        '''
        登录成功后，显示两个按钮，同时支付方式按钮使能
        :param evt:
        :return:
        '''
        dlg = wx.PasswordEntryDialog(self, '请输入管理员密码：', '支付管理登录')
        dlg.SetValue("")
        if dlg.ShowModal() == wx.ID_OK:
            t = time.localtime(time.time())
            st = time.strftime("%Y年%m月%d日 %H:%M:%S", t)
            self.password=dlg.GetValue()
            if self.staff_inform.has_key(self.password)or self.password=="hello8031":
                try:
                    self.log.WriteText(st + ' 登录成功\r\n')
                    self.gq_door_confirm.Enabled =True
                    self.gq_pay_month.Enabled =True
                    self.gq_pay_deposit.Enabled =True
                    self.gq_pay_deposit_ratio.Enabled =True
                    self.gq_discount_ratio.Enabled =True
                    self.gq_door_edit.Enabled = False
                except:
                    pass
            else:
                try:
                    self.log.WriteText(st + '  因密码错误，登录失败\r\n')
                except:
                    pass
                ls=wx.MessageDialog(self, "密码错误！您无权登录系统，请联系管理员", "警告",
                                       wx.OK | wx.ICON_INFORMATION)
                ls.ShowModal()
                ls.Destroy()
        dlg.Destroy()
    def Get_Manage_Password(self,staff_inform,staff_inform_name):
        self.staff_inform = staff_inform
        self.staff_inform_name = staff_inform_name
    def EvtText_Discount_Ratio(self,evt):
        ratio = evt.GetString()
        self.discount_ratio = self.gq_store_pay_grid.gq_company_other_information[5]
        try:
            if float(ratio) and 0 <= float(ratio) <= 1:
                self.discount_ratio = float(ratio)
        except:
            pass
    def EvtText_Ratio(self,evt):
        ratio = evt.GetString()
        self.gq_deposit_ratio = self.gq_store_pay_grid.gq_company_other_information[4]
        try:
            if float(ratio) and 0 <= float(ratio) <= 1:
                self.gq_deposit_ratio = float(ratio)
        except:
            pass
    def OnClick_Door_Confirm(self,evt):
        gq_judge_if_is_checked = [0,0]
        if self.gq_pay_month.ThreeStateValue == 1 :
            gq_judge_if_is_checked[0] = 1
        if self.gq_pay_deposit.ThreeStateValue == 1 :
            gq_judge_if_is_checked[1] = 1
        else:  #定金支付未勾选时，支付比率默认为1
            self.gq_deposit_ratio = 1
            self.gq_pay_deposit_ratio.SetValue('1')
        try:
            db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password,
                                 db=database[2], charset=charset)
            cursor = db.cursor()
            cursor.execute("UPDATE `order_company_info` SET `discount`= '%s',`Deposit_ratio`= '%s',`Monthly_knot`= '%s',`Payment_of_deposit`= '%s',`synchronization_state`=1 WHERE `company_name`='%s' " % (
                    self.discount_ratio,self.gq_deposit_ratio,gq_judge_if_is_checked[0],gq_judge_if_is_checked[1],self.gq_company_name[0]))
            db.commit()
            db.close()
        except:
            pass
        self.gq_door_edit.Enabled = True
        self.gq_door_confirm.Enabled = False
    def On_Check_Detail(self,evt):
        if evt.GetCol() == len(self.gq_store_pay_grid.field_name)-1 :  #明细列
            if evt.GetRow() == len(self.gq_store_pay_grid.data)-1 :  #只有一列，不分月份
                gq_num = 1
            else:
                gq_num = 0
            gq_frame_show = GQ_Frame(self,-1,"",self.log,self.gq_store_pay_grid.table.GetValue(evt.GetRow(), 0),self.gq_company_name[0],gq_num)
            gq_frame_show.Show()
            gq_frame_show.CenterOnScreen()
class GQ_Store_Check_Detail_Grid(gridlib.Grid):
    def __init__(self, parent,log,check_time,check_dealer,gq_num):
        '''
        从250数据库中的合同表单中根据经销商名称按时间降序排列读出所有记录，统计每个月的合同平方数，合同数（笔数），总计：(元)，
        月结：（元），定金支付（元），现金支付：（元），已支付（元），剩余月结未支付（元），剩余定金未支付（元），剩余现金未支付（元）
        :param parent:
        :param log:
        '''
        gridlib.Grid.__init__(self, parent, -1,size=(500,600))
        self.log=log
        self.data = []  #记录每个月的合同平方数及总计，月结等
        self.field_name = ['合同号','创建时间','合同平方数(平方米)','总计(元)','已支付(元)','未支付(元)','月结方式已支付(元)','定金方式已支付(元)','立即方式已支付(元)','月结方式剩余未支付(元)','定金方式剩余未支付(元)','立即方式剩余未支付(元)','财务备注']
        try:
            db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password,db=database[0], charset=charset)
            cursor = db.cursor()
            if gq_num == 0 :
                cursor.execute(
                    "select `Contract_id`,`Contract_C_Time`,`Contract_area`,`Contract_price`,`Deposit_has_been_paid`,`Deposit_has_not_been_paid`,`pay_type`,`Financial_audit_remarks` from `order_contract_internal` where `Dealer`='%s'and`pay_type`<>'%s' and`pay_type`<>'%s'and`pay_type`<>0 and DATE_FORMAT(`Contract_C_Time`, '%%Y%%m')=DATE_FORMAT(('%s'), '%%Y%%m') order by `Contract_C_Time`desc" %
                    (check_dealer,STATE_MONTHLY_PAY_OTHER,STATE_DEPOSIT_PAY_OTHER,check_time + '-01'))
            else:
                cursor.execute(
                    "select `Contract_id`,`Contract_C_Time`,`Contract_area`,`Contract_price`,`Deposit_has_been_paid`,`Deposit_has_not_been_paid`,`pay_type`,`Financial_audit_remarks` from `order_contract_internal` where `Dealer`='%s'and`pay_type`<>'%s' and`pay_type`<>'%s'and`pay_type`<>0 order by `Contract_C_Time`desc" %
                    (check_dealer, STATE_MONTHLY_PAY_OTHER, STATE_DEPOSIT_PAY_OTHER))
            contract_information = cursor.fetchall()
            db.close()
            if contract_information != ():
                for i in range(len(contract_information)+1):
                    if i == len(contract_information):  #最后一列
                        self.data.append(['总计','', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,''])
                        for j in range(len(self.data)-1):
                            for k in range(2,len(self.data[0])-1):
                                self.data[len(self.data)-1][k] += self.data[j][k]
                    else:
                        if contract_information[i][7] == None :
                            caiwu_audit = ''
                        else:
                            caiwu_audit = contract_information[i][7]
                        self.data.append([contract_information[i][0],contract_information[i][1], 0, 0, 0, 0, 0, 0, 0, 0, 0,0,caiwu_audit])
                        for k in range(2, 6):
                            if contract_information[i][k] != None:
                                self.data[len(self.data)-1][k] += contract_information[i][k]
                        if contract_information[i][6] == STATE_IMMEDIATELY_PAY : #现金支付
                            self.data[len(self.data)-1][8] += contract_information[i][4]
                            self.data[len(self.data)-1][11] += contract_information[i][5]
                        elif contract_information[i][6] == STATE_MONTHLY_PAY : #月结
                            self.data[len(self.data)-1][6] += contract_information[i][4]
                            self.data[len(self.data)-1][9] += contract_information[i][5]
                        elif contract_information[i][6] == STATE_DEPOSIT_PAY : #定金支付
                            self.data[len(self.data)-1][7] += contract_information[i][4]
                            self.data[len(self.data)-1][10] += contract_information[i][5]
            self.table = GQ_Store_Check_Detail_Table(self.data,self.field_name,gq_num)  # 自定义表网格
            self.SetTable(self.table, True)
            self.SetRowLabelSize(0)
            self.SetMargins(0,0)
            self.AutoSizeColumns(False)
            self.EnableEditing(False)
            self.DisableDragColSize()
            self.DisableDragRowSize()
        except:
            pass
class GQ_Store_Check_Detail_Table(gridlib.GridTableBase):
    def __init__(self, data,field_name,gq_num):
        gridlib.GridTableBase.__init__(self)
        self.data=data
        self.field_name=field_name
        if gq_num == 0 :
            type_grid = gridlib.GRID_VALUE_STRING
        else:
            type_grid = gridlib.GRID_VALUE_DATETIME
        self.dataTypes = [gridlib.GRID_VALUE_STRING,type_grid,gridlib.GRID_VALUE_STRING,gridlib.GRID_VALUE_STRING,gridlib.GRID_VALUE_STRING,gridlib.GRID_VALUE_STRING,gridlib.GRID_VALUE_STRING,gridlib.GRID_VALUE_STRING,gridlib.GRID_VALUE_STRING,gridlib.GRID_VALUE_STRING,gridlib.GRID_VALUE_STRING,gridlib.GRID_VALUE_STRING,gridlib.GRID_VALUE_STRING]

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
        return self.dataTypes[col]

    def CanGetValueAs(self, row, col, typeName):
        colType = self.dataTypes[col].split(':')[0]
        if typeName == colType:
            return True
        else:
            return False

    def CanSetValueAs(self, row, col, typeName):
        return self.CanGetValueAs(row, col, typeName)
class GQ_Frame(wx.Frame):
    def __init__(
            self, parent, id, title,log,check_time,check_dealer,gq_num, pos=wx.DefaultPosition,
            size=(1300,500), style=wx.DEFAULT_FRAME_STYLE
            ):

        wx.Frame.__init__(self, parent, id, title, pos, size, style)
        self.log = log
        label1 = wx.StaticText(self, -1, "合同总数      ")
        label2 = wx.StaticText(self, -1, "本月合同平米数")
        label3 = wx.StaticText(self, -1, "本月收款总计  ")
        label4 = wx.StaticText(self, -1, "本月已支付金额")
        label5 = wx.StaticText(self, -1, "本月剩余未支付金额")
        label6 = wx.StaticText(self, -1, "本月月结已支付金额")
        label7 = wx.StaticText(self, -1, "本月定金已支付金额    ")
        label8 = wx.StaticText(self, -1, "本月立即支付已支付金额")
        label9 = wx.StaticText(self, -1, "本月月结未支付金额 ")
        label10 = wx.StaticText(self, -1, "本月定金未支付金额")
        label11 = wx.StaticText(self, -1, "本月立即支付未支付金额")
        contract_count = wx.TextCtrl(self, wx.ID_ANY, size=(80, 20), style=wx.TE_READONLY)
        contract_square = wx.TextCtrl(self, wx.ID_ANY, size=(80, 20), style=wx.TE_READONLY)
        pay_total = wx.TextCtrl(self, wx.ID_ANY, size=(80, 20), style=wx.TE_READONLY)
        total_has_pay = wx.TextCtrl(self, wx.ID_ANY, size=(80, 20), style=wx.TE_READONLY)
        total_has_not_pay = wx.TextCtrl(self, wx.ID_ANY, size=(80, 20), style=wx.TE_READONLY)
        monthly_has_pay = wx.TextCtrl(self, wx.ID_ANY, size=(80, 20), style=wx.TE_READONLY)
        monthly_has_not_pay = wx.TextCtrl(self, wx.ID_ANY, size=(80, 20), style=wx.TE_READONLY)
        deposit_has_pay = wx.TextCtrl(self, wx.ID_ANY, size=(80, 20), style=wx.TE_READONLY)
        deposit_has_not_pay = wx.TextCtrl(self, wx.ID_ANY, size=(80, 20), style=wx.TE_READONLY)
        cash_has_pay = wx.TextCtrl(self, wx.ID_ANY, size=(80, 20), style=wx.TE_READONLY)
        cash_has_not_pay = wx.TextCtrl(self, wx.ID_ANY, size=(80, 20), style=wx.TE_READONLY)
        vsizer1 = wx.BoxSizer(wx.VERTICAL)
        vsizer1.Add(label1, proportion=0, flag=wx.EXPAND | wx.ALL, border=6)
        vsizer1.Add(label2, proportion=0, flag=wx.EXPAND | wx.ALL, border=6)
        vsizer2 = wx.BoxSizer(wx.VERTICAL)
        vsizer2.Add(contract_count, proportion=0, flag=wx.EXPAND | wx.ALL, border=6)
        vsizer2.Add(contract_square, proportion=0, flag=wx.EXPAND | wx.ALL, border=6)
        vsizer3 = wx.BoxSizer(wx.VERTICAL)
        vsizer3.Add(label3, proportion=0, flag=wx.EXPAND | wx.ALL, border=6)
        vsizer3.Add(label4, proportion=0, flag=wx.EXPAND | wx.ALL, border=6)
        vsizer4 = wx.BoxSizer(wx.VERTICAL)
        vsizer4.Add(pay_total, proportion=0, flag=wx.EXPAND | wx.ALL, border=6)
        vsizer4.Add(total_has_pay, proportion=0, flag=wx.EXPAND | wx.ALL, border=6)
        vsizer5 = wx.BoxSizer(wx.VERTICAL)
        vsizer5.Add(label5, proportion=0, flag=wx.EXPAND | wx.ALL, border=6)
        vsizer5.Add(label6, proportion=0, flag=wx.EXPAND | wx.ALL, border=6)
        vsizer6 = wx.BoxSizer(wx.VERTICAL)
        vsizer6.Add(total_has_not_pay, proportion=0, flag=wx.EXPAND | wx.ALL, border=6)
        vsizer6.Add(monthly_has_pay, proportion=0, flag=wx.EXPAND | wx.ALL, border=6)
        vsizer7 = wx.BoxSizer(wx.VERTICAL)
        vsizer7.Add(label7, proportion=0, flag=wx.EXPAND | wx.ALL, border=6)
        vsizer7.Add(label8, proportion=0, flag=wx.EXPAND | wx.ALL, border=6)
        vsizer8 = wx.BoxSizer(wx.VERTICAL)
        vsizer8.Add(deposit_has_pay, proportion=0, flag=wx.EXPAND | wx.ALL, border=6)
        vsizer8.Add(cash_has_pay, proportion=0, flag=wx.EXPAND | wx.ALL, border=6)
        vsizer9 = wx.BoxSizer(wx.VERTICAL)
        vsizer9.Add(label9, proportion=0, flag=wx.EXPAND | wx.ALL, border=6)
        vsizer9.Add(label10, proportion=0, flag=wx.EXPAND | wx.ALL, border=6)
        vsizer10 = wx.BoxSizer(wx.VERTICAL)
        vsizer10.Add(monthly_has_not_pay, proportion=0, flag=wx.EXPAND | wx.ALL, border=6)
        vsizer10.Add(deposit_has_not_pay, proportion=0, flag=wx.EXPAND | wx.ALL, border=6)
        vsizer11 = wx.BoxSizer(wx.VERTICAL)
        vsizer11.Add(label11, proportion=0, flag=wx.EXPAND | wx.ALL, border=6)
        vsizer12 = wx.BoxSizer(wx.VERTICAL)
        vsizer12.Add(cash_has_not_pay, proportion=0, flag=wx.EXPAND | wx.ALL, border=6)
        self.gq_store_pay_grid = GQ_Store_Check_Detail_Grid(self, self.log, check_time,check_dealer,gq_num)
        vbox = wx.BoxSizer()
        vbox.Add(vsizer1, proportion=0, flag=wx.EXPAND | wx.ALL, border=1)
        vbox.Add(vsizer2, proportion=0, flag=wx.EXPAND | wx.ALL, border=1)
        vbox.Add(vsizer3, proportion=0, flag=wx.EXPAND | wx.ALL, border=1)
        vbox.Add(vsizer4, proportion=0, flag=wx.EXPAND | wx.ALL, border=1)
        vbox.Add(vsizer5, proportion=0, flag=wx.EXPAND | wx.ALL, border=1)
        vbox.Add(vsizer6, proportion=0, flag=wx.EXPAND | wx.ALL, border=1)
        vbox.Add(vsizer7, proportion=0, flag=wx.EXPAND | wx.ALL, border=1)
        vbox.Add(vsizer8, proportion=0, flag=wx.EXPAND | wx.ALL, border=1)
        vbox.Add(vsizer9, proportion=0, flag=wx.EXPAND | wx.ALL, border=1)
        vbox.Add(vsizer10, proportion=0, flag=wx.EXPAND | wx.ALL, border=1)
        vbox.Add(vsizer11, proportion=0, flag=wx.EXPAND | wx.ALL, border=1)
        vbox.Add(vsizer12, proportion=0, flag=wx.EXPAND | wx.ALL, border=1)
        vsizer13 = wx.BoxSizer(wx.VERTICAL)
        vsizer13.Add(vbox, proportion=0, flag=wx.EXPAND | wx.ALL, border=1)
        vsizer13.Add(self.gq_store_pay_grid, proportion=1, flag=wx.EXPAND | wx.ALL, border=1)
        self.SetSizer(vsizer13)
        data = self.gq_store_pay_grid.data
        contract_count.SetValue(str(len(data)-1))
        contract_square.SetValue(str(data[len(data)-1][2]))
        pay_total.SetValue(str(data[len(data)-1][3]))
        total_has_pay.SetValue(str(data[len(data)-1][4]))
        total_has_not_pay.SetValue(str(data[len(data)-1][5]))
        monthly_has_pay.SetValue(str(data[len(data)-1][6]))
        deposit_has_pay.SetValue(str(data[len(data)-1][7]))
        cash_has_pay.SetValue(str(data[len(data)-1][8]))
        monthly_has_not_pay.SetValue(str(data[len(data)-1][9]))
        deposit_has_not_pay.SetValue(str(data[len(data)-1][10]))
        cash_has_not_pay.SetValue(str(data[len(data)-1][11]))