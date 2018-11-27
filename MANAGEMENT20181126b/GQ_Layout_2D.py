#!/usr/bin/env python
# _*_ coding: UTF-8 _*_
#20171213b:
#GQ:修改类结构，将数据库连接部分单独编写为方法，避免重复连接，去掉了gq_error_id部分，发现修改组件表单的门板状态时出现错误，未解决
#20171214a:
#GQ:解决昨天遇到的修改组件状态出现错误的问题,已解决
#20171214b:
#GQ:修改完成排样的订单的状态
#20171214c:
#GQ:修改对应数据库的state为State
#20171214d:
#GQ:修改对应数据库的状态为State，保留原来的state版本
#20171214f:
#1.GQ:修改状态为State之后，发现在线面积统计又不对了，原来是State的初始状态不对，经过讨论确定了，已解决
#2.GQ：更新各表单的状态时，将State=5改成state=PART_LAYOUT_STATE时，发现更新出错，原来是索引部分出了问题，当需格式化的字符串为多个时，对应的字符串必须为元素，而不能是单个元组
#20171215a:
#1.GQ:编写修改完成排样的零件对应组件下的所有零件的优先级，已完成，调试过程中发现出现待排样数据库中的完成排样的零件对应组件下的所有零件的优先级提高了两次，但零件库
#以及部件库组件库只把对应零件、组件的优先级修改了一次，原来是更新部件的地方有个变量索引写错了，已解决
#20171215b:
#1.GQ:将修改完成排样的零件对应组件下所有零件的优先级封装成Update_Priority_And_State，暂时实现了修改组件，部件，零件的，待排样数据库的优先级，后续会将修改完成排样的
# 组件，部件，零件的状态的函数也放入此类
#20171215c:
#GQ:编写修改未进入排产的订单、组件、部件、零件的优先级的函数，将其放入时间事件里调用
#20171217a:
#1.GQ：对于完成排样的组件、部件、零件的状态的修改，将其放入Update_Priority_And_State类内，使其功能可以公用
#2.GQ:将计算实时在线面积的方法单独放入Information_Counter类中，该类中Get_Realtime_Online_Square方法返回的是实时在线面积，在
#本类中计算实时面积部分调用Get_Realtime_Online_Square方法
#20171217c:
#GQ:发现一个问题，当订单面积足够时，日志不再显示，预计是将计算在线面积的函数单独放到另一个统计类里时出现了问题，已解决
#20171218b:
#GQ:将完成排样的时间添加到零件表单中,将门板进入待排样表单的时间添加到零件表单中
#20171218c:
#GQ：发现一个写日志重复多次写同一个错误的问题，对排样前处理的Get_Right_Layout_Thickness_Component方法进行了修改
#20171221e:
#GQ:对于满足排样规则的门板，排出的一床只能放一块门板，利用率低，针对这种情况，设置利用率门限，当利用率低于此值时，放宽刀具类型的门限
#GQ:发现程序运行过程中有些警告：C:\AUI_test\TWT_171222a\GQ_Layout_2D.py:449: Warning: Row size too large (> 8126). Changing some columns to TEXT or BLOB or using ROW_FORMAT=DYNAMIC or ROW_FORMAT=COMPRESSED may help. In current row format, BLOB prefix of 768 bytes is stored inline.
  # cursor.execute(sql1)
# C:\AUI_test\TWT_171222a\MyContractMaker.py:124: Warning: Table '.\db_hanju\info_door_type' is marked as crashed and should be repaired
#   cursor.execute("SELECT `Door_style` FROM `info_door_type` WHERE 1")
# C:\AUI_test\TWT_171222a\MyContractMaker.py:124: Warning: Table 'info_door_type' is marked as crashed and should be repaired
#   cursor.execute("SELECT `Door_style` FROM `info_door_type` WHERE 1")
# C:\AUI_test\TWT_171222a\MyContractMaker.py:124: Warning: 1 client is using or hasn't closed the table properly
#   cursor.execute("SELECT `Door_style` FROM `info_door_type` WHERE 1")
#20171222b:
#GQ:排样中发现零件数据库中有很多零件，但是排不出来，原因是根据排样规则选取的门板零件太少导致排不出来
#GQ:修改排样后处理中向工位工单表单插数据部分，避免冗余
#20171225c:
#GQ:修改了Load函数，它应该放在一个时间事件里单独运行
#20180101a:
#GQ：当待排样表单为空时，不应该建立线程调用排样函数
#GQ：将每部分函数运行所用时间做个记录，显示在日志上
#20180105a:
#GQ:在部件库增加了一个压条类型字段，修改了Load_Online_Data函数
#20180108f:
#GQ:当在线零件库中出现报废的零件时，先将其加入到报废零件表单中，将原来在在线表单中的数据删除，新添加一条状态为返工，并且优先级为1000，条形码编号与之前不一样的零件，并将此零件信息添加到待排样表单中
#20180109c:
#GQ:优化向待排样表单添加数据的函数
#20180117d_performance:
#GQ:修改排样算法中的更换厚度部分，原来是选取待排样表单中的优先级高的门板对应的厚度作为排样厚度，此算法是不合理的，随着生产的进行，此厚度的零件优先级一直在改变，而另一厚度的零件的优先级一直不变，
# 这是不合理的，所以改为一开始给一个厚度默认值，然后当此厚度较长时间内排不出工单时，更换厚度进行排样
#20170127A:
#gq:返工时，零件的状态仍为0，只是优先级与条形码编号变了，调试各个工位对于返工零件的处理
#20180328b:
#GQ:当到向在线表单中加载订单的时间后，调用该程序（1.向在线表单加载数据，加载面积够时，调用排样函数，排样函数结束后，调用膜压函数，膜压结束后，调用打包程序）
#（去掉了原来在排样中加的线程，去掉了计算剩余工单的程序，将计算在线面积的函数从原来的information_counter类中移到此类中）
#订单加载开始时间（主程序开始调用此类的时间），加载的订单总面积，排样开始时间，排样结束时间，18/20mm的工单数量，需特殊下料的零件面积
#20180328d:
# GQ:解决了利用率为1的情况
#20180329a：
#GQ：将所有程序放到一个文件里
#20180330a:
#GQ：修改膜压部分的程序，将其改为静态排样，适应瀚海版本的数据库
#1.向在线表单添加数据时，同时向膜压待排样表单添加数据
#2.修改膜压排样程序，使其适应瀚海版本的数据库结构
#20180331b:
#GQ:研究订单不完全打散且尽量不降低利用率的情况下，该选择多少个订单进行排样合适
############（完成排样时，未修改零件库中的完成排样的时间）
#1.在下料待排样表单中加入一个字段（订单编号），相应的修改向待排样表单添加数据的函数
#2.排样前处理部分获取待排样表单中厚度为当前排样厚度的零件时，加上订单编号字段
#3.根据找出的待排样数据筛选出k个订单，再从这k个订单中筛选出满足刀具类型的零件（取面积和》=标准型材面积进行排样，剩下的零件在排样后看是否能继续放进去）
#20180402a:
#GQ:当当前零件面积不够一床时，原来是直接将这些零件加到临时待排样表单，现改为将certain_order_num_component（筛选出的订单列表）中的第一个加入到临时待排样表单，同时将待排样表单中对应零件删除
#20180402i:
#GQ:在工位工单表单中加入一字段Machine_nums，用来记录该工单分配给哪个机床，修改排样后处理部分的程序
#因排样耗时会很长，而原来排样中加的线程已去掉，故使用HH_System_V1.0_20180328d调试订单不打那么散的情况下，利用率的情况
#20180403a:
#GQ：加工的零件厚度不只有18与20mm的，对此部分进行调整
#20180403b:
#GQ:修改了零件表单，部件表单中的打孔字段hole以及openway（开门方式），相应的修改了Get_Load_Part_Information函数、Get_Load_Component_Inforamtion函数、
#Get_Load_Wait_Layout_Component_Information函数、Insert_Online_Data函数、Get_Right_Layout_Thickness_Component函数、Get_Certain_Num_Order函数、
#Select_Match_Tool_Component函数、Get_All_Layout_Component函数、Get_Every_Hole函数、Get_Component_Hole_Information函数、Get_Component_Other_Information函数、
#Minimum_Horizontal_Line_Algorithm函数、Can_Layout函数、Monitor_Finish_State函数
#20180404k:
#GQ:Realtime_Online_Square_Threshold（在线平米门限值）应为ylp编写的界面中传入，针对此问题进行修改
#GQ:判断此工单应该哪台机器接单时，应该将所有能接单的机器都填入machine_nums字段中，以&符号连接
#GQ:判断该条工单应该分配给哪个机床，应该先看机器号，然后根据机器号找出对应刀库，判断该工单所用刀具是否在刀库中均存在
#20180405f:
#GQ:排样完成后，向生产调度表单添加一串字符串，为了加工中心界面可以读出来显示，在数据之间用分隔符隔开
#############TWT_HH_180326a:read_excel,向待排样表单添加数据
#GQ:对于已经找到最佳排序方案的零件，找到plate中最后连续未填充的第一块区域的纵坐标，当最低水平线大于此纵坐标时，摆放后面补放的零件
#GQ:编写另外一种遗传算法，单点交叉
#20180413f:
#GQ:改变了排样对于裁断刀厚度的处理，在前处理时将零件进行尺寸调整，后处理再改过来
#20180414a:
#GQ:向生产调度添加膜压颜色面积的字段时，统计有误，原来是统计的在线零件表单内所有零件，应该统计的是未进行膜压前分拣的所有零件
#20180416afendan:
#GQ:修改排样前处理部分的程序，将订单按几个单进行排样，分配给固定机床（若还有剩余零件，则在下一次获取给此机床分配工单的订单时，加上此零件），
# 若生成的工单含有玻璃门，则将此工单分配给3号机床。
#暂时还没加玻璃门的排样判断
#20180417afendan:
#GQ:测试排样程序（未加玻璃门的排版）
#20180417b:
#GQ:选择订单时，要考虑到分别为每台机床产生的工单数量相近，即动态的调整为每台机床分配工单而选择的订单数量
#1.统计当前所选面积的订单可以分别为1,2号与4,5，6号产生多少面积的工单
#2.比较1,2号机床与4,5,6号机床的工单面积来决定下一次为哪台机器抓取订单并生成工单
#3.如何确定抓取多少订单(同时考虑订单面积与订单的完整性)，以上次抓取的订单面积作为面积容限，若订单面积达到该容限值或订单数量够设定值，则停止抓取
#20180417cfendan:
#GQ:对于玻璃门的加工，将所有玻璃门挑出来，当该玻璃门对应的订单中已有零件排样完成，则优先对该玻璃门进行排样
#将每次筛选的订单编号进行标记，若某玻璃门的订单编号在所筛选的订单列表中，则提升对应玻璃门的优先级
#将含有玻璃门的零件按优先级进行排序,之后一起排玻璃门
#自测完成
#20180421a:
#GQ:修改了数据库中Element_type字段(改为Element_type_id int)与Interval_width(float)与Bottom_part_down（float）
#20180423afendan:
#GQ:将零件从待排样表单添加到临时待排样表单时，经过了尺寸处理，忘记将其转换回来，导致待排样表单中的数据出现错误，已解决
#20180423bfendan:
#GQ:增加了压条排样之后，需在待排样表单与临时待排样表单中均添加一个字段（Element_type_id int零件类型），相应的向两个表单插入数据
# 的时候，将对应的零件类型信息也添加到对应表单
#GQ:将待排样表单中所有的压条找出来，放到一个列表中，按压条所属订单的排样顺序依次提高压条的优先级,之后将压条零件加到临时待排样表单中
#20180430a:
#GQ:统计的面积应为当天该加的面积
#20180430b:
#GQ:为了将当天所需加载的订单加到在线表单内，先将需加载的订单优先级提高，再将其加载到在线表单，发现的问题是：当一批订单加载之后，主程序不停止运行，
# 若不在线表单内有数据的话，也会将其加入到在线表单，这是不正确的，应当在加载过之后，将realtime_online_square_threshold设置为0，
# 等下次生产调度时再调用，重置realtime_online_square_threshold的值
#20180502b:
#GQ:加入对罗马柱，美板的排样
#GQ:当零件进入待排样表单时，要先判断该罗马柱是需要加工,然后将需要加工的罗马柱与其他需加工的零件一起加到待排样表单
#20180505b:
#GQ:缺少对打孔信息的合理化校对，已解决
#20180605a:
#增强程序的错误处理机制
#20180606a:
#将主程序中调用修改不在线订单优先级的程序去掉了，改为每天排生成任务单的时候，先修改优先级，再加载(将排样程序及修改不在线表单优先级的程序放到线程里)
#修改向在线表单提订单的程序，订单优先级按天来计算，要向在线表单提订单时，先提取优先级高的订单，当优先级一致时，将
# 优先级一致的零件按颜色数量进行排序，取颜色最多的订单，按下单时间进行排序，依次一个个提取

#1.修改不在线订单的优先级
#2.按优先级排序统计优先级不一样的订单数量及订单面积，若订单数量与订单面积够了，则直接将其加到生产表单内，
# 否则，若优先级一致，则选取颜色最多的订单
#20180609a:
#GQ:将进入生产表单的零件中厚度非18的都加到临时待排样表单，供散板加工处加工，修改GQ_Layout_Algorithm类中的前处理部分函数
#20180609b:
#GQ:往在线表单加载数据时，同时向膜压待排样表单加载数据
#20180609c:
#GQ:去掉了向生产调度表单中的Schedule_of_membrane字段填写信息，改为膜压完成后，向该表单填写信息
#20180612a:
#GQ:修改排样部分的程序，之前只为12 456号机床分配工单，3号机床分配玻璃门，现在还要为3号机床分配非玻璃门工单
#20180618a:
#GQ:修改排样部分的程序，1.向在线表单抓取订单的时候，先抓取18厚度的加急的意尔橱品牌的订单（找到加急订单中对应面积最多的订单，记录该订单下的零件所用的刀，
# 然后抓取剩余面积的订单（产能减去其他加急订单的面积为剩余面积），记录面积，若面积不够剩余面积，抓取第二急的订单对应刀下的订单，
# 抓够剩余面积（更新后的剩余面积），直到订单面积大于等于剩余面积），然后将其他加急的订单抓到生产表单中
#2.排样：统计抓进来的订单中单面板，素板，格子板的面积，按面积降序记录
# 3.选取面积最大的板材厚度对应的门板零件按优先级，门型复杂度，面积，id进行排序（意尔橱），之后调用排样算法
#4.抓取正常订单同上
#5.在正常订单中挑选出玻璃门，步骤2，步骤3
#其他正常订单，步骤2，步骤3
#20180619a:
#向在线表单加载数据时，应分为为5号机床加载订单及向正常机床加载订单两部分
#1.修改不在线订单优先级的程序，当发货时间大于20天的话，其优先级为0，小于10天，每天优先级加5，当优先级为150的话，即为加急
#2.获得所有不在线的订单，找到对应订单下的零件，将零件分为两类，意尔橱品牌与瀚海品牌
#3.在意尔橱品牌中或瀚海品牌中，将订单分类为加急与不加急订单
#5.在加急的订单堆中，找出面积最大的订单,记录加急的订单编号
#6.记录该订单下的所有零件所用刀型
#7.计算需加载的同刀型订单面积
#8.统计实际存在的同刀型的订单面积（先从不加急堆中找出同刀型的订单，然后再从订单表单中读出面积并统计）
#20180620a:
#GQ:编写加载订单的主循环部分
#20180620b:
#GQ:开始编写为5号机床生成工单的排样函数
#1.从info_base_material_charge表单中读出所有板材厚度为18的板材类型
#压条未加入到待排样表单中
#20180621a:
#获得零件对应门型的复杂度，同时计算零件的面积，将复杂度及对应的零件面积填到零件列表的末端
#对零件按优先级，门型复杂度，面积进行排序
#对零件进行前处理尺寸调整
#20180628a:
#GQ:测试排样函数
#20180629a:
#GQ:对于玻璃门的排样，格子板的玻璃门只加工正面，算作正常的
#20180706a:
#GQ:修改排样部分的程序，去掉专门为五号机床产生工单的程序，除了玻璃门外，所有机床都可以进行同等接单,发现数据库连接不上的问题，是程序中出现一个死循环，已改正
#调整不在线库优先级工式为（14-（交货日期-当前日期））*5
#当交货日期距离现在只有3天时，即为加急的订单，当前优先级为55
##############################################
#20180712c：
#修改调整不在线订单的程序，改为在线与不在线都需要修改优先级，在开始排样前修改优先级
#20180712d:
#调整排样部分的程序，从订单表单中找到所有订单，将订单按照优先级降序排序，找到优先级最高的订单，记录刀具
#20180712e:订单表单内没有厚度，寻找厚度则在部件表单查找，同时修改订单，部件，组件表单中的字段，相应的修改程序
#20180714c:
#重新编写排样函数,排样时，把当前排样时间填入到零件表单中的first_day中,已修改完毕
#20180714d:
#GQ:开始编写膜压排样部分的程序
#20180715d:
#GQ:编写散板排样前处理部分向在线表单添加数据的程序
#1.先设定一个散板在线面积100
#2.查看临时待排样表单内的零件面积，计算需从不在线表单抓取多少面积的订单
#20180716b:
#修改散板排样部分向临时待排样表单加载订单的程序
#3.从不在线表单中抓取非18厚的订单加载到在线表单中，按优先级同刀型加载
#4.从order_element_online表单中先把所有状态为25的弧形压条加入到临时待排样表单中，再把状态为25的且厚度不为18的门板加到临时待排样表单中
#20180716c:
#把门板，罗马柱，楣板，带拱压条都加到待排样表单中或临时待排样表单中，然后把待排样表单中不符合条件的放到临时待排样表单中
#GQ:若组件中含有1711与1707门型
#20180724c：
#GQ：排样完成时，计算一下当前工单的排产日期，schedule_date
#20180724j:
#GQ:向临时待排样表单添加散板零件时，把假百叶也添加进去，修改状态的函数要改，只修改加工的零件及加工的零件对应的部件，组件，订单
#排样完成时，修改零件，部件，组件，订单的first_day字段
#20180726a:
#修改排样算法，预留10mm的边,在膜压的部件表单增加一个字段，工单编号
#20180806a:
#GQ:获取到同一批次的零件，进行排样
#20180813a:
#制单操作员从订单表单中获得，将批次按大小排序
#GQ:点击立即排产时，排产结束后，将制单编号#，排产日期，创建时间，操作员#,批次数#，工单数#，批次包含的订单#
# 总订单数，总订单面积填到对应的表单中
#20180825b:
#GQ:1.根据批次以及状态找到对应的订单编号，根据订单编号找到对应的面积，按面积降序排列
#2.将获得的订单按面积分为两堆（弓字形分堆法）

#3.将一个批次里所有的玻璃门挑出来，排样，然后再分堆
#20180918b:
#排样时，把工单生成到临时工位工单中
# GQ:排完样时，更新查询表单的状态为5，将,package状态改为0,将工单从零时表单挪到工位工单表单中
#20180925c:
#GQ:修改排产部分的统计信息功能，统计的应为18素板多少床，123多少床,面积多少，涉及多少订单，456多少床，玻璃门多少床（排样时统计）
#20180928b:
#GQ:查找排样的一个bug:掉不下来的情况
#20180930a:
#GQ:每排完一床之后，将对应坐标向右向上提升7毫米
#GQ:最后排产完成，才更零件部件组件订单的状态
#GQ:最后排产完成后，修改对应合同的状态
#20181014a:
#GQ:排产时多统计一些信息，一个批次下123号机床涉及的订单编号，4号机床涉及的订单编号，456号机床涉及的订单编号
#GQ:排样完成后，向零件表单中添加工位工单编号字段
#20181109a:
#GQ:修改排样程序的一个bug:当一床全为玻璃门时，统计为123号机床分配的订单列表初始值设置有问题，已改正
#20181115a:
#GQ:当宽度上限也放到2420的话，相应的修改排样程序

MACHINE_NUM_1_2_3 = '1&2&3'
MACHINE_NUM_4_5_6 = '4&5&6'
import time
import MySQLdb
import datetime
from ID_DEFINE import *
import wx
import random
import copy
import os, sys
from psutil import net_if_addrs
Plate_Specification_Height = 2440
Plate_Specification_Width = 1220
GQ_Reserve_Boundary = 0
Cut_Knife_Diameter=6
State_Has_Gene_Workorder=5
######################排样部分
class GQ_Layout_Algorithm():
    def __init__(self,log):
        self.log = log
        self.gq_bottom_algorithm = GQ_Minimum_Horizontal_Line_Algorithm()  # 将底层摆放算法（最低水平线）实例化
        self.gq_sequence_algorithm=GQ_Particle_Swarm_Algorithm()         #排样的上层算法（排序算法）实例化
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
    def Is_DBdatabase_Connected(self):
        '''
        本方法用来连接数据库，避免多次重复连接
        :return:
        '''
        try:
            self.db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0], charset=charset)
            self.db_produce = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[1], charset=charset)
            return True
        except:
            self.log.WriteText('数据库连接过程中出错请检查用户名、密码等信息  \r\n')
            return False
    def Complete_Layout(self,workorder_id_immediately):
        '''
        1.从info_base_material_charge表单中读出所有板材厚度为18的板材类型
        2.从待排样表单中找到所有板材为a的零件，进行排样
        '''
        self.Init_Parameter()
        self.Get_Now_Can_Layout_Batch() #记录当前可排样的零件批次
        self.GQ_Get_Base_Material_Type()  #记录数据库中存储的所有板材厚度
        while self.get_batch_plan_production != []:  #一个批次
            self.gq_record_glass_order_id.append(['0'])
            self.gq_record_123_order_id.append('')
            self.gq_record_456_order_id.append('')
            self.GQ_Get_All_Glass_And_Layout()
            self.gq_base_material_name = copy.deepcopy(self.gq_base_material_name_restore)
            self.GQ_Get_Batch_Responding_Order_Id()  #获取到批次对应的订单编号及降序排列的面积
            if self.batch_responding_order_id != [] :
                self.GQ_Bow_Shape_Stacking()   #分出第一堆（1.2.3号）与第二堆（4.5.6号）
                for gq_index in range(2):
                    self.GQ_Find_All_Corresponding_Component_And_Layout(gq_index)
                    self.gq_base_material_name = copy.deepcopy(self.gq_base_material_name_restore)  #避免多次重复连接数据库获得板材厚度信息
            del self.get_batch_plan_production[0]  # 将排完样的批次信息删除
            self.record_batch_num += 1  #批次数加1
        self.Get_Layout_Query_Information(workorder_id_immediately)  #排完了
        self.gq_dlg.Update(100, "排样完成...")
        self.gq_dlg.Destroy()
    def Init_Parameter(self):
        '''
        本方法是将类内的参数初始化
        :return:
        '''
        self.standard_area = Plate_Specification_Height*Plate_Specification_Width
        self.normal_layout_thickness=18    #123456号机床的排样厚度
        self.finally_knife_threshold = 6
        self.gq_record_workorder_num=0  #记录工单数
        self.gq_record_layout_result = [0,0,0,0,0,0,0,0,0] #18mm单面板，凌格板数量，123号机床的数量，订单面积，订单数，456号机床的数量，订单面积，订单数，玻璃门数
        self.gq_record_order_id = []  #记录订单编号，以便更新组件表单中的package状态
        self.gq_record_glass_order_id = [] #记录批次下玻璃门涉及的订单编号
        self.gq_record_123_order_id = []  #记录批次下123涉及的订单编号
        self.gq_record_456_order_id = []  #记录批次下456涉及的订单编号
        self.record_batch_num = 0  #记录批次数
        self.count=0
        self.gq_dlg = wx.ProgressDialog("layout dialog", "正在排样...", maximum=100)
        self.gq_dlg.ShowModal()
        self.gq_dlg.Update(self.count, "开始排样...")
    def Get_Layout_Query_Information(self,workorder_id_immediately):
        '''
        获取到制单操作员以及制单编号，将临时工位工单表单中的工单添加到工位工单表单中，删除零时工位工单中的工单，将组件表单中的package状态改为0
        :return:
        '''
        contract_id = []
        try:
            db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0], charset=charset)
            cursor = db.cursor()
            cursor.execute("UPDATE `work_cnc_workorder_query` SET `Single_18_board_num`='%s',`Rhombic_18_board_num`='%s',`123_machine_workorder_num`='%s',`123_machine_order_area`='%s',`123_machine_order_num`='%s',`456_machine_workorder_num`='%s',`456_machine_order_area`='%s',`456_machine_order_num`='%s',`Glass_door_num`='%s',`Workorder_num`='%s',`State`='%s' WHERE `Workorder_id`='%s' " % (
                self.gq_record_layout_result[0],self.gq_record_layout_result[1],self.gq_record_layout_result[2],self.gq_record_layout_result[3],self.gq_record_layout_result[4],self.gq_record_layout_result[5],self.gq_record_layout_result[6],self.gq_record_layout_result[7],self.gq_record_layout_result[8],self.gq_record_workorder_num, State_Has_Gene_Workorder,workorder_id_immediately))
            for i in range(self.record_batch_num):  #记录的批次数
                cursor.execute("UPDATE `work_cnc_workorder_query` SET `%s`='%s',`%s`='%s',`%s`='%s' WHERE `Workorder_id`='%s' " % (
                        'Batch_including_order_'+str(i+1)+'_1&2&3',self.gq_record_123_order_id[i],'Batch_including_order_'+str(i+1)+'_4',self.gq_record_glass_order_id[i],'Batch_including_order_'+str(i+1)+'_4&5&6',
                        self.gq_record_456_order_id[i],workorder_id_immediately))
            for i in range(len(self.gq_record_order_id)):
                list_contract = self.gq_record_order_id[i].split('O')
                contract_id.append(list_contract[0])
                cursor.execute("UPDATE `order_order_online` SET `First_day`= '%s',`State`= '%s' WHERE `Order_id`='%s' " % (datetime.date.today(),STATE_LAYOUT_FINISH, self.gq_record_order_id[i]))
                cursor.execute("UPDATE `order_section_online` SET `First_day`= '%s',`State`= '%s',`Package_state`=0 WHERE `Order_id`='%s' " %(datetime.date.today(),STATE_LAYOUT_FINISH, self.gq_record_order_id[i]))
                cursor.execute("UPDATE `order_part_online` SET `First_day`= '%s' WHERE `Order_id`='%s'" % (datetime.date.today(), self.gq_record_order_id[i]))
                cursor.execute("UPDATE `order_part_online` SET `State`= '%s' WHERE `Order_id`='%s'and (`Element_type_id`='%s' or `Element_type_id`='%s' or `Element_type_id`='%s' )" % (STATE_LAYOUT_FINISH, self.gq_record_order_id[i],ELEMENT_TYPE_DOOR,ELEMENT_TYPE_ROME_COLUMN,ELEMENT_TYPE_LINTEL))
                cursor.execute("UPDATE `order_element_online` SET `First_day`= '%s' WHERE `Order_id`='%s'" % (datetime.date.today(),self.gq_record_order_id[i]))
                cursor.execute("UPDATE `order_element_online` SET `State`= '%s' WHERE `Order_id`='%s'and (`Element_type_id`='%s' or `Element_type_id`='%s' or `Element_type_id`='%s' )" % (STATE_LAYOUT_FINISH, self.gq_record_order_id[i],ELEMENT_TYPE_DOOR,ELEMENT_TYPE_ROME_COLUMN,ELEMENT_TYPE_LINTEL))
            cursor.execute("SELECT `Priority`,`Ap_id`,`Schedule_date`,`Create_time`,`Machine_nums`,`Material_norm`,`Total_seg`,`Index_of_base_material_thickness`,`Glass_num`,`Board_Utilization_Ratio`,`Element_information_1`,`Element_information_2`,`Element_information_3`,`Element_information_4`,`Element_information_5`,`Element_information_6`,`Element_information_7`,`Element_information_8`,`Element_information_9`,`Element_information_10`,`Element_information_11`,`Element_information_12`,`Element_information_13`,`Element_information_14`,`Element_information_15`,`Element_information_16`,`Element_information_17`,`Element_information_18`,`Element_information_19`,`Element_information_20`,`Element_information_21`,`Element_information_22`,`Element_information_23`,`Element_information_24`,`Element_information_25`,`Element_information_26`,`Element_information_27`,`Element_information_28`,`Element_information_29`,`Element_information_30`,`Element_information_31`,`Element_information_32`,`Element_information_33`,`Element_information_34`,`Element_information_35`,`Element_information_36`,`Element_information_37`,`Element_information_38`,`Element_information_39`,`Element_information_40`,`Element_information_41`,`Element_information_42`,`Element_information_43`,`Element_information_44`,`Element_information_45`,`Element_information_46`,`Element_information_47`,`Element_information_48`,`Element_information_49`,`Element_information_50`,`Element_information_51`,`Element_information_52`,`Element_information_53`,`Element_information_54`,`Element_information_55`,`Element_information_56`,`Element_information_57`,`Element_information_58`,`Element_information_59`,`Element_information_60`,`Element_information_61`,`Element_information_62`,`Element_information_63`,`Element_information_64`,`Element_information_65`,`Element_information_66`,`Element_information_67`,`Element_information_68`,`Element_information_69`,`Element_information_70`,`Element_information_71`,`Element_information_72`,`Element_information_73`,`Element_information_74`,`Element_information_75`,`Element_information_76`,`Element_information_77`,`Element_information_78`,`Element_information_79`,`Element_information_80`,`Element_information_81`,`Element_information_82`,`Element_information_83`,`Element_information_84`,`Element_information_85`,`Element_information_86`,`Element_information_87`,`Element_information_88`,`Element_information_89`,`Element_information_90`,`Element_information_91`,`Element_information_92`,`Element_information_93`,`Element_information_94`,`Element_information_95`,`Element_information_96`,`Element_information_97`,`Element_information_98`,`Element_information_99`,`Element_information_100`,`Knife_1`,`Knife_2`,`Knife_3`,`Knife_4`,`Knife_5`,`Knife_6`,`Thickness`,`State` FROM `work_cnc_task_list_temporary` WHERE `CPU_index`in ('%s')"%self.cpu_index)  # 门板楣板罗马柱带拱压条都加到待排样表单了
            work_cnc_temporary_result = cursor.fetchall()
            if work_cnc_temporary_result != ():
                for i in range(len(work_cnc_temporary_result)):
                    cursor.execute("INSERT INTO `work_cnc_task_list`(`CPU_index`,`Priority`,`Ap_id`,`Schedule_date`,`Create_time`,`Machine_nums`,`Material_norm`,`Total_seg`,`Index_of_base_material_thickness`,`Glass_num`,`Board_Utilization_Ratio`,`Knife_1`,`Knife_2`,`Knife_3`,`Knife_4`,`Knife_5`,`Knife_6`,`Thickness`,`State`)VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(self.cpu_index,work_cnc_temporary_result[i][0],work_cnc_temporary_result[i][1],work_cnc_temporary_result[i][2],work_cnc_temporary_result[i][3],work_cnc_temporary_result[i][4],work_cnc_temporary_result[i][5],work_cnc_temporary_result[i][6],work_cnc_temporary_result[i][7],work_cnc_temporary_result[i][8],work_cnc_temporary_result[i][9],work_cnc_temporary_result[i][110],work_cnc_temporary_result[i][111],work_cnc_temporary_result[i][112],work_cnc_temporary_result[i][113],work_cnc_temporary_result[i][114],work_cnc_temporary_result[i][115],work_cnc_temporary_result[i][116],work_cnc_temporary_result[i][117]))
                    db.commit()
                    cursor.execute("SELECT `Index`,`Ap_id` FROM `work_cnc_task_list` WHERE 1 order by `Index`desc limit 1")  # 门板楣板罗马柱带拱压条都加到待排样表单了
                    ap_id_idnex = cursor.fetchone()
                    if ap_id_idnex != None :
                        ap_id = str(ap_id_idnex[1])+str(ap_id_idnex[0])
                        cursor.execute("UPDATE `work_cnc_task_list` SET `Ap_id`= '%s' WHERE `Index`='%s'" % (
                        ap_id, ap_id_idnex[0]))
                        for j in range(work_cnc_temporary_result[i][6]):
                            now_id = work_cnc_temporary_result[i][10+j].split('&')
                            cursor.execute("UPDATE `work_cnc_task_list` SET `%s`= '%s' WHERE `Index`='%s'" % ('Element_information_'+str(j+1),work_cnc_temporary_result[i][10+j],ap_id_idnex[0]))
                            cursor.execute("UPDATE `order_element_online` SET `Cnc_Task_List_Ap_Id`= '%s' WHERE `Id`='%s'" % (
                                ap_id, now_id[2]))
                        db.commit()
            cursor.execute("DELETE FROM `work_cnc_task_list_temporary` WHERE `CPU_index`in ('%s')"%self.cpu_index)
            db.commit()
            contract_id_list = list(set([x for x in contract_id]))
            for i in range(len(contract_id_list)):
                finish_layout_order_num = 0
                cursor.execute(
                    "SELECT `State` from `order_order_online`  WHERE `Contract_id`='%s' " % (contract_id_list[i]))
                order_state = cursor.fetchall()
                for m in range(len(order_state)):  # 判断该订单下的所有组件是否均已处于完成状态
                    if (order_state[m][0] < STATE_LAYOUT_FINISH):
                        break
                    else:
                        finish_layout_order_num += 1
                if finish_layout_order_num == len(order_state):  # 订单下的所有组件均处于完成状态，修改该订单的状态为已完成
                    cursor.execute("UPDATE `order_contract_internal` SET `State`= '%s' WHERE `Contract_id`='%s' " % (
                        STATE_LAYOUT_FINISH, contract_id_list[i]))
            db.commit()
            db.close()
        except:
            pass
    def Get_Now_Can_Layout_Batch(self):
        '''
        从零件库中获得状态为26的零件对应的批次，并记录批次，记录订单编号
        :return:
        '''
        self.get_batch_plan_production=[]
        try:
            db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0], charset=charset)
            cursor = db.cursor()
            cursor.execute("SELECT `Production_batch`,`Order_Id` from `work_cnc_before_layout`  WHERE `State`='%s'and `CPU_index`in ('%s')"%(STATE_BEGIN_SCHEDULING,self.cpu_index))
            production_batch = cursor.fetchall()
            if production_batch == () :
                pass
            else:    #获取到批次
                for i in range(len(production_batch)):
                    if production_batch[i][1] not in self.gq_record_order_id :
                        self.gq_record_order_id.append(production_batch[i][1])
                    if production_batch[i][0] not in self.get_batch_plan_production :
                        self.get_batch_plan_production.append(production_batch[i][0])
            self.get_batch_plan_production.sort()  #批次按升序排列
            db.close()
        except:
            pass
    def GQ_Get_Base_Material_Type(self):
        '''
        获得厚度为18的零件对应的基材种类
        :return:
        '''
        self.gq_base_material_name_restore=[]
        self.gq_base_material_name = []
        try:
            if (self.Is_DBdatabase_Connected()):
                cursor_produce = self.db_produce.cursor()         #根据订单编号找到订单的收货时间
                cursor_produce.execute("SELECT `Index` from `info_base_material_charge`  WHERE `Base_material_thick`='%s'"%self.normal_layout_thickness)
                base_material_name = cursor_produce.fetchall()
                self.db_produce.close()
                if base_material_name==():
                    pass
                else:
                    for i in range(len(base_material_name)) :
                        self.gq_base_material_name_restore.append(base_material_name[i][0])
                    self.gq_base_material_name=copy.deepcopy(self.gq_base_material_name_restore)
                    return RUN_NORMAL
        except:
            self.log.WriteText('天外天系统正在运行查找基材种类的函数,出现错误，请进行检查  \r\n')
            return LAYOUT_ERROR
    def GQ_Get_All_Glass_And_Layout(self):
        '''
        获取到批次下的对应板材的玻璃门，一个批次下的所有玻璃门涉及到的订单编号
        :return:
        '''
        gq_have_component_times = 0
        gq_base_material_length = len(self.gq_base_material_name)-1
        try:
            while self.gq_base_material_name != []:
                self.gq_component_information = []
                if self.gq_base_material_name[0] == ELEMENT_LATICES_BOARD_INDEX :
                    del self.gq_base_material_name[0]
                else:
                    db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0],charset=charset)
                    cursor = db.cursor()
                    cursor.execute("SELECT `Height`,`Width`,`State`,`Id`,`Type`,`Contract_C_Time`,`Priority`,`Thickness`,`Open_way`,`Hole`,`Code`,`Heart_type`,`Knife_1`,`Knife_2`,`Knife_3`,`Knife_4`,`Knife_5`,`Knife_6`,`Order_Id`,`Element_type_id`,`Color`,`Index_of_base_material_thickness` from `work_cnc_before_layout`  WHERE `Heart_type`='%s'and `Index_of_base_material_thickness`='%s'and `State`='%s'and `CPU_index`in ('%s')" % (
                        '1', self.gq_base_material_name[0], STATE_BEGIN_SCHEDULING,self.cpu_index))
                    base_material_component_information = cursor.fetchall()
                    if base_material_component_information != ():  #找到了玻璃门
                        for k in range(len(base_material_component_information)):
                            if base_material_component_information[k][18] not in self.gq_record_glass_order_id[self.record_batch_num]:
                                self.gq_record_glass_order_id[self.record_batch_num].append(base_material_component_information[k][18])
                            self.gq_component_information.append(list(base_material_component_information[k]))
                            self.gq_component_information[k][2] = 0
                    db.close()
                    if self.gq_component_information != []:
                        if self.GQ_Get_Component_Complexity_And_Area():
                            return LAYOUT_ERROR
                        self.Pre_Adjust_And_Get_Glass_Door()  # 前处理尺寸调整及获得玻璃门
                    else:  # 记录当前厚度下零件个数为0的次数
                        gq_have_component_times += 1
                    del self.gq_base_material_name[0]
                    while self.gq_component_information != []:  # 当前含有玻璃门，调用排样算法(排完序的)
                        self.GQ_Choose_Match_Tool_Component(self.gq_component_information)  # 玻璃门匹配刀，获得排样零件
                        self.Layout(self.gq_component_information)  # 排样
                        self.Post_layout(1, 0)  # 后处理，玻璃门状态
                        if self.count + 5 < 100:
                            self.count += 5
                            self.gq_dlg.Update(self.count, "正在排样...")
            order_str_glass = ''
            for i in range(1,len(self.gq_record_glass_order_id[self.record_batch_num])):
                if i != 1 :
                    order_str_glass += ','+ str(self.gq_record_glass_order_id[self.record_batch_num][i])
                else:
                    order_str_glass = str(self.gq_record_glass_order_id[self.record_batch_num][i])
            self.gq_record_glass_order_id[self.record_batch_num]=order_str_glass
            if gq_base_material_length == gq_have_component_times :
                return LAYOUT_ERROR
            return RUN_NORMAL
        except:
            self.log.WriteText('天外天系统正在运行玻璃门排样程序出现错误，请进行检查  \r\n')
            return LAYOUT_ERROR
    def GQ_Get_Batch_Responding_Order_Id(self):
        '''
        根据批次以及状态，从待排样表单中找到对应的订单编号，再根据订单编号从订单表单内找到对应的面积，将面积按降序排列
        :return:
        '''
        self.batch_responding_order_id = []
        try:
            db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0], charset=charset)
            cursor = db.cursor()
            cursor.execute("SELECT `Order_Id` from `work_cnc_before_layout`  WHERE `Production_batch`='%s' and `State`='%s'and `CPU_index`in ('%s')"%(self.get_batch_plan_production[0],STATE_BEGIN_SCHEDULING,self.cpu_index))
            result_order_id = cursor.fetchall()
            if result_order_id==():
                pass
            else:
                for i in range(len(result_order_id)) :
                    if result_order_id[i][0] not in [x[0] for x in self.batch_responding_order_id]:
                        self.batch_responding_order_id.append([result_order_id[i][0]])
                for i in range(len(self.batch_responding_order_id)):
                    cursor.execute("SELECT `Order_area` from `order_order_online`  WHERE `Order_id`='%s'" % self.batch_responding_order_id[i][0])
                    result_order_area = cursor.fetchone()
                    if result_order_area == None or result_order_area[0] == None:
                        self.batch_responding_order_id[i].append(0)
                    else:
                        self.batch_responding_order_id[i].append(result_order_area[0])
                self.batch_responding_order_id.sort(key=lambda x: -x[1])
            db.close()
            return RUN_NORMAL
        except:
            self.log.WriteText('天外天系统正在运行获取批次对应的订单编号出现错误，请进行检查  \r\n')
            return LAYOUT_ERROR
    def GQ_Bow_Shape_Stacking(self):
        '''
        将获得的订单按弓字形分成两堆，记录两堆的面积,将大的那堆给123号机床，小的那堆给456号机床
        :return:
        '''
        self.heap_order_information = [[],[]]
        first_heap_order_area= 0
        second_heap_order_area=0
        self.heap_order_information[0].append(self.batch_responding_order_id[0][0])
        first_heap_order_area += self.batch_responding_order_id[0][1]
        number = 1
        for i in range(1,len(self.batch_responding_order_id),2) :
            self.heap_order_information[number].append(self.batch_responding_order_id[i][0])
            if i != len(self.batch_responding_order_id)-1 :
                self.heap_order_information[number].append(self.batch_responding_order_id[i + 1][0])
            if number == 0 :
                first_heap_order_area += self.batch_responding_order_id[i][1]
                if i != len(self.batch_responding_order_id) - 1:
                    first_heap_order_area += self.batch_responding_order_id[i+1][1]
                number = 1
            else:
                second_heap_order_area += self.batch_responding_order_id[i][1]
                if i != len(self.batch_responding_order_id) - 1:
                    second_heap_order_area += self.batch_responding_order_id[i + 1][1]
                number = 0
        if first_heap_order_area < second_heap_order_area :  #第二堆面积更大，交换第一堆与第二堆
            first_heap_order_information = self.heap_order_information[0]
            self.heap_order_information[0] = self.heap_order_information[1]
            self.heap_order_information[1]  = first_heap_order_information
            self.gq_record_layout_result[3] += second_heap_order_area  #123号
            self.gq_record_layout_result[6] += first_heap_order_area
        else:
            self.gq_record_layout_result[3] += first_heap_order_area  # 123号
            self.gq_record_layout_result[6] += second_heap_order_area
        self.gq_record_layout_result[4] += len(self.heap_order_information[0])  # 123号，涉及订单数
        self.gq_record_layout_result[7] += len(self.heap_order_information[1])
        for j in range(2):
            order_str=''
            for i in range(len(self.heap_order_information[j])):
                if i != 0 :
                    order_str += ','+str(self.heap_order_information[j][i])
                else:
                    order_str = str(self.heap_order_information[j][i])
            if j == 0 :
                self.gq_record_123_order_id[self.record_batch_num]=  order_str         #123与456涉及的订单编号
            else:
                self.gq_record_456_order_id[self.record_batch_num]=  order_str        #123与456涉及的订单编号
    def GQ_Find_All_Corresponding_Component_And_Layout(self,gq_index):
        '''
        找到对应基材的所有待排样零件，获取到零件复杂度及面积并进行排序
        一种板材排完了，删除对应列表中的信息，继续排另一种板材,检索条件多加个批次
        :return:
        '''
        gq_have_component_times=0
        gq_base_material_length=len(self.gq_base_material_name)
        try:
            while self.gq_base_material_name != [] :
                self.gq_component_information = []
                db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0],charset=charset)
                cursor = db.cursor()
                for A in range(len(self.heap_order_information[gq_index])):
                    cursor.execute(
                        "SELECT `Height`,`Width`,`State`,`Id`,`Type`,`Contract_C_Time`,`Priority`,`Thickness`,`Open_way`,`Hole`,`Code`,`Heart_type`,`Knife_1`,`Knife_2`,`Knife_3`,`Knife_4`,`Knife_5`,`Knife_6`,`Order_Id`,`Element_type_id`,`Color`,`Index_of_base_material_thickness` from `work_cnc_before_layout`  WHERE `Order_id`='%s'and `Index_of_base_material_thickness`='%s'and `State`='%s'and `CPU_index`in ('%s')" % (self.heap_order_information[gq_index][A],self.gq_base_material_name[0],STATE_BEGIN_SCHEDULING,self.cpu_index))
                    base_material_component_information = cursor.fetchall()
                    if base_material_component_information != ():
                        for k in range(len(base_material_component_information)):
                            self.gq_component_information.append(list(base_material_component_information[k]))
                            self.gq_component_information[k][2] = 0
                db.close()
                if self.gq_component_information != []:
                    if self.GQ_Get_Component_Complexity_And_Area():
                        return LAYOUT_ERROR
                    self.Pre_Adjust_And_Get_Glass_Door()  # 前处理尺寸调整及获得玻璃门
                else:  #记录当前厚度下零件个数为0的次数
                    gq_have_component_times+=1
                del self.gq_base_material_name[0]
                while self.gq_component_information != []:
                    self.GQ_Choose_Match_Tool_Component(self.gq_component_information)  # 正常零件匹配刀，获得排样零件
                    self.Layout(self.gq_component_information)  # 排样
                    self.Post_layout(0,gq_index)  # 后处理
                    if self.count + 5 < 100:
                        self.count += 5
                        self.gq_dlg.Update(self.count, "正在排样...")
            if gq_base_material_length == gq_have_component_times :
                return LAYOUT_ERROR
            return RUN_NORMAL
        except:
            self.log.WriteText('天外天系统正在运行获取排样零件的程序,出现错误，请进行检查  \r\n')
            return LAYOUT_ERROR
    def GQ_Get_Component_Complexity_And_Area(self):
        '''
        获取到零件的复杂度以及计算零件的面积，将其添加到存储零件的列表末尾
        同时对有问题的零件进行校验
        :return:
        '''
        try:
            if (self.Is_DBdatabase_Connected()):
                cursor_produce = self.db_produce.cursor()
                for i in range(len(self.gq_component_information)-1,-1,-1):
                    cursor_produce.execute(
                        "SELECT `Degree_of_complexity` from `info_door_type` WHERE `Door_style`='%s'" %
                        self.gq_component_information[i][4])
                    degree_of_complexity = cursor_produce.fetchone()
                    if degree_of_complexity == None:
                        self.gq_component_information[i] += [0, 0]
                    else:
                        if degree_of_complexity[0] == '0':
                            gq_insert_degree_complexity = 0
                        else:
                            gq_insert_degree_complexity_split = degree_of_complexity[0].split('系')
                            gq_insert_degree_complexity = int(gq_insert_degree_complexity_split[0])
                        gq_insert_area = self.gq_component_information[i][0] * self.gq_component_information[i][
                            1]  # 统计每个零件面积
                        self.gq_component_information[i] += [gq_insert_degree_complexity, gq_insert_area]
                self.gq_component_information.sort(key=lambda x: (-x[6], -x[22], -x[23]))  # 优先级，复杂度，面积降序排列
                self.db_produce.close()
                return RUN_NORMAL
        except:
            self.log.WriteText('天外天系统正在运行获取零件对应的门型复杂度的程序,出现错误，请进行检查  \r\n')
            return LAYOUT_ERROR
    def Pre_Adjust_And_Get_Glass_Door(self):
        '''
        此方法用于将满足排样条件的零件进行尺寸调整，
        :return:
        '''
        i=0
        while i < len(self.gq_component_information):
            self.gq_component_information[i][0]+=Cut_Knife_Diameter
            self.gq_component_information[i][1]+=Cut_Knife_Diameter
            i+=1
    def GQ_Choose_Match_Tool_Component(self,all_kind_of_component):
        '''
        找到所有满足刀不超过六把且面积大于等于标准型材面积的零件进行排样
        :param all_kind_of_component:
        :return:
        '''
        i=0
        record_layout_knife=['0',None]
        self.match_tool_components = []
        self.component_area = 0
        self.layout_component = []
        while i<len(all_kind_of_component):
                new_add_knife_num = 0  # 新增加的刀具类型数量
                for j in range(12, 18):
                    if all_kind_of_component[i][j] not in record_layout_knife:
                        new_add_knife_num += 1
                if len(record_layout_knife) - 2 + new_add_knife_num <= self.finally_knife_threshold :
                    self.match_tool_components.append(all_kind_of_component[i])
                    self.component_area += all_kind_of_component[i][0] * all_kind_of_component[i][1]
                    for k in range(12, 18):
                        if all_kind_of_component[i][k] not in record_layout_knife:
                            record_layout_knife.append(all_kind_of_component[i][k])
                if (self.component_area >= self.standard_area and self.layout_component == []) or (self.component_area<self.standard_area and i==len(all_kind_of_component)-1):  # 筛选前满足面积条件的零件作为遗传算法或粒子群算法的输入，将剩余满足条件的零件放入match_tool_component,以便调用完算法后还能摆放
                    self.layout_component = copy.deepcopy(self.match_tool_components)
                    self.match_tool_components = []
                i+=1
    def Layout(self,delete_component):
        '''
        打散订单之后的排样（使用遗传算法或粒子群排样算法）
        :return:
        '''
        layout_list=[]
        for i in range(len(self.layout_component)):           #将零件中的优先级字段位修改为零件旋转位
            self.layout_component[i][6]=0
        best_layout_sequence, rectangle_dict=self.gq_sequence_algorithm.Particle_Swarm_Algorithm(self.layout_component)         #调用粒子群算法
        # best_layout_sequence, rectangle_dict = Genetic_Algorithm(self.layout_component)          #最后一个参数为下料中心排样使能，此时调用的排样函数为下料专用的
        for i in best_layout_sequence[0][1]:           #将算法得出的顺序进行解码
            size_list=rectangle_dict[abs(i)]
            if i<0 :
                long_size=size_list[0]
                size_list[0]=size_list[1]
                size_list[1]=long_size
                size_list[6]=1
            layout_list.append(size_list)
        for i in range(len(self.match_tool_components)):
            self.match_tool_components[i][6]=2
        layout_list+=self.match_tool_components
        self.utilization_ratio, self.plate = self.gq_bottom_algorithm.Minimum_Horizontal_Line_Algorithm(layout_list)
        self.Delete_Layout_Component(delete_component)                      #获取到排样结果后，将对应排完样的零件从the_component_of_order删去
    def Delete_Layout_Component(self,delete_component):
        '''
        将完成排样的零件从the_component_of_order列表中删除
        :return:
        '''
        for i in range(len(self.plate)):
            if delete_component == [] :
                break
            for j in range(len(delete_component) - 1, -1, -1):
                if self.plate[i][7]==delete_component[j][3]:
                    del delete_component[j]
                    break
    def Post_layout(self,if_is_glass,gq_index):
        '''
        排样后处理
        :param if_is_glass: 判断当前是否为玻璃门在排样，1：是
        :return:
        '''
        self.Get_All_Layout_Component()  # 获得已排零件信息以及零件所用的总刀具类型
        if self.Get_Knife_Corresponding_Name():
            return POST_LAYOUT_ERROR
        if self.Get_Every_Hole():  # 获得每个零件的每个孔的位置信息
            return POST_LAYOUT_ERROR
        self.Get_Component_Hole_Information()  # 获得零件的打孔信息，格式为0 0,0 0,0 0,0 0,0 0
        self.Get_Component_Other_Information()  # 将零件的信息以2,8,1200,2400,1&Type&Id&0 0,0 0,0 0,0 0,0 0,1&Code格式连接
        if self.Get_Workorder(if_is_glass,gq_index) : # 向工位工单表单中插入当前工单的基础信息
            return POST_LAYOUT_ERROR
        if self.Modify_Component_State_And_Get_Id_List():
            return POST_LAYOUT_ERROR
        else:
            self.gq_record_workorder_num += 1  #记录生成的工单数
            return RUN_NORMAL
    def Get_All_Layout_Component(self):
        '''
        此方法用于从plate中的信息，放在self.layout_result_list列表中，同时获得零件所用刀具类型
        :return:
        '''
        self.layout_knife_recorded=['0',None]   #获得刀具类型，读取到刀具类型对应的刀名，填到工位工单表单内
        self.layout_result_list = []
        for i in range(len(self.plate)):
            if self.plate[i][5] != 0:  # 获得已排样零件的信息
                if self.plate[i][10] != 0:  # 零件若有旋转,将换了的高和宽换过来，旋转状态置为1
                    height = self.plate[i][4]
                    self.plate[i][4] = self.plate[i][5]
                    self.plate[i][5] = height
                    self.plate[i][10] = 1
                self.plate[i][4] -= Cut_Knife_Diameter  # 将调整了的尺寸以及横纵坐标调整回来
                self.plate[i][5] -= Cut_Knife_Diameter
                self.plate[i][0] += GQ_Reserve_Boundary +(Cut_Knife_Diameter / 2)
                self.plate[i][1] += GQ_Reserve_Boundary +(Cut_Knife_Diameter / 2)
                self.layout_result_list.append(self.plate[i])
                for j in range(16,22):
                    if self.plate[i][j] not in self.layout_knife_recorded:
                        self.layout_knife_recorded.append(self.plate[i][j])
    def Get_Knife_Corresponding_Name(self):
        '''
        获取到排样零件所用刀具对应的刀名
        :return:
        '''
        self.layout_knife_name=[]
        try:
            if (self.Is_DBdatabase_Connected()):
                cursor_produce = self.db_produce.cursor()
                for i in range(2,len(self.layout_knife_recorded)):
                    cursor_produce.execute(
                        "SELECT `Name` FROM `sh_tools` WHERE `ID_number`='%s'"%self.layout_knife_recorded[i])
                    knife_name = cursor_produce.fetchone()
                    if knife_name==None:
                        pass
                    else:
                        self.layout_knife_name.append(knife_name[0])
                self.db_produce.close()
                return RUN_NORMAL
        except:
            self.log.WriteText('获得排样所用刀具对应刀名出现错误，请进行检查  \r\n')
            return POST_LAYOUT_ERROR
    def Get_Every_Hole(self):
        '''
        该函数的功能是从一个字符串中获得每个零件各个孔的位置信息
        :return:
        '''
        self.component_hole_list=[]
        for i in range(len(self.layout_result_list)):
            if self.layout_result_list[i][13] == None :
                self.layout_result_list[i][13] = '0/0/0/0/0'
            hole_list=self.layout_result_list[i][13].split('/')
            for j in range(len(hole_list)):
                if self.func(hole_list[j]):  # 判断该字符串是否可以int
                    hole_list[j]=int(hole_list[j])
                elif self.Is_Float(hole_list[j]):    #该字符串可以float
                    hole_list[j] = float(hole_list[j])
                else:
                    hole_list[j] = 0
                    self.log.WriteText('天外天系统正在运行排样后处理部分的程序，打孔信息出现不合理值，请进行检查  \r\n')
            self.component_hole_list.append(hole_list)
        return RUN_NORMAL
    def Is_Float(self,s):
        s = str(s)
        if s.count('.') == 1:  # 判断小数点个数
            sl = s.split('.')  # 按照小数点进行分割
            left = sl[0]  # 小数点前面的
            right = sl[1]  # 小数点后面的
            if left.startswith('-') and left.count('-') == 1 and right.isdigit():
                lleft = left.split('-')[1]  # 按照-分割，然后取负号后面的数字
                if lleft.isdigit():
                    return True
            elif left.isdigit() and right.isdigit():
                # 判断是否为正小数
                return True
        return False
    def func(self,x):
        try:
            x = int(x)
            return isinstance(x, int)
        except ValueError:             #未处理的意外
            return False
    def Get_Component_Hole_Information(self):
        '''
        该方法用于获得零件的打孔位置信息（所打孔的横纵坐标，最后一个为开门方向，每个零件五个孔，以‘0 0,0 0,0 0 ，0 0 ，0 0,1’形式存储）
        :return:
        '''
        self.record_str_hole_list=[]
        for i in range(len(self.layout_result_list)):  # 为避免工位工单表单内字段过多，将其中某一类信息以字符串的形式存储
            record_str_hole = []
            hole_label_x = 0
            hole_label_y = 0
            for k in range(5):
                if (self.component_hole_list[i][k] == 0):
                    hole_label_x = 0
                    hole_label_y = 0
                elif (self.layout_result_list[i][10] == 1):
                    if (self.layout_result_list[i][12] == '左开'):  # 如果门板为躺着放左开
                        if k == 4:  # 最后一个孔的位置信息要单独考虑
                            hole_label_y = self.layout_result_list[i][0] + self.component_hole_list[i][k]  # 孔直径为35
                            hole_label_x = self.layout_result_list[i][1] + MARGIN + RADIUS
                        else:
                            hole_label_y = self.layout_result_list[i][0] + self.layout_result_list[i][4] - self.component_hole_list[i][k]
                            hole_label_x = self.layout_result_list[i][1] + MARGIN + RADIUS
                    elif (self.layout_result_list[i][12] == '右开'):  # 如果门板为躺着放右开
                        if k == 4:
                            hole_label_y = self.layout_result_list[i][0] + self.component_hole_list[i][k]
                            hole_label_x = self.layout_result_list[i][1] + self.layout_result_list[i][
                                5] - MARGIN - RADIUS
                        else:
                            hole_label_y = self.layout_result_list[i][0] + self.layout_result_list[i][4] - self.component_hole_list[i][k]
                            hole_label_x = self.layout_result_list[i][1] + self.layout_result_list[i][
                                5] - RADIUS - MARGIN
                    elif (self.layout_result_list[i][12] == '上翻'):  # 如果门板为躺着放上开
                        if k == 4:
                            hole_label_y = self.layout_result_list[i][0] + MARGIN + RADIUS
                            hole_label_x = self.layout_result_list[i][1] + self.layout_result_list[i][5] - self.component_hole_list[i][k]
                        else:
                            hole_label_y = self.layout_result_list[i][0] + RADIUS + MARGIN
                            hole_label_x = self.layout_result_list[i][1] + self.component_hole_list[i][k]
                    elif (self.layout_result_list[i][12] == '下翻'):  # 如果门板为躺着放下开
                        if k == 4:
                            hole_label_y = self.layout_result_list[i][0] + self.layout_result_list[i][
                                4] - RADIUS - MARGIN
                            hole_label_x = self.layout_result_list[i][1] + self.layout_result_list[i][5] - self.component_hole_list[i][k]
                        else:
                            hole_label_y = self.layout_result_list[i][0] + self.layout_result_list[i][
                                4] - RADIUS - MARGIN
                            hole_label_x = self.layout_result_list[i][1] + self.component_hole_list[i][k]
                elif (self.layout_result_list[i][10] == 0):
                    if (self.layout_result_list[i][12] == '左开'):  # 如果门板为立着放左开
                        if k == 4:
                            hole_label_y = self.layout_result_list[i][0] + RADIUS + MARGIN
                            hole_label_x = self.layout_result_list[i][1] + self.layout_result_list[i][4] - self.component_hole_list[i][k]
                        else:
                            hole_label_y = self.layout_result_list[i][0] + RADIUS + MARGIN
                            hole_label_x = self.layout_result_list[i][1] + self.component_hole_list[i][k]
                    elif (self.layout_result_list[i][12] == '右开'):  # 如果门板为立着放右开
                        if k == 4:
                            hole_label_y = self.layout_result_list[i][0] + self.layout_result_list[i][
                                5] - RADIUS - MARGIN
                            hole_label_x = self.layout_result_list[i][1] + self.layout_result_list[i][4] - self.component_hole_list[i][k]
                        else:
                            hole_label_y = self.layout_result_list[i][0] + self.layout_result_list[i][
                                5] - RADIUS - MARGIN
                            hole_label_x = self.layout_result_list[i][1] + self.component_hole_list[i][k]
                    elif (self.layout_result_list[i][12] == '上翻'):  # 如果门板为立着放上开
                        if k == 4:
                            hole_label_y = self.layout_result_list[i][0] + self.layout_result_list[i][5] - self.component_hole_list[i][k]
                            hole_label_x = self.layout_result_list[i][1] + self.layout_result_list[i][
                                4] - RADIUS - MARGIN
                        else:
                            hole_label_y = self.layout_result_list[i][0] + self.component_hole_list[i][k]
                            hole_label_x = self.layout_result_list[i][1] + self.layout_result_list[i][
                                4] - RADIUS - MARGIN
                    elif (self.layout_result_list[i][12] == '下翻'):  # 如果门板为立着放下开
                        if k == 4:
                            hole_label_y = self.layout_result_list[i][0] + self.layout_result_list[i][5] - self.component_hole_list[i][k]
                            hole_label_x = self.layout_result_list[i][1] + RADIUS + MARGIN
                        else:
                            hole_label_y = self.layout_result_list[i][0] + self.component_hole_list[i][k]
                            hole_label_x = self.layout_result_list[i][1] + RADIUS + MARGIN
                hole_label = ' '.join('%s' % id for id in (hole_label_x, hole_label_y))
                record_str_hole.append(hole_label)
            self.record_str_hole_list.append(','.join('%s' % id for id in (record_str_hole[0],record_str_hole[1],record_str_hole[2], record_str_hole[3], record_str_hole[4],self.layout_result_list[i][12])))
    def Get_Component_Other_Information(self):
        '''
        该方法用于获得零件的其他信息，比如零件的左下角坐标，零件的尺寸以及零件对应的门型，零件编号，条形码等，并将这些信息添加到一个列表中，以供创建工位工单时使用
        :return:
        '''
        self.component_information = []  # 零件的信息，分别包含2,8,1200,2400,1&Type&Id&0 0,0 0,0 0,0 0,0 0,1&Code
        for i in range(len(self.layout_result_list)):
            record_str_part_list = []
            record_str_part_list.append(','.join('%s' % id for id in (self.layout_result_list[i][0], self.layout_result_list[i][1], self.layout_result_list[i][4],
                self.layout_result_list[i][5], self.layout_result_list[i][10])))
            self.component_information.append('&'.join('%s'%id for id in(record_str_part_list[0],self.layout_result_list[i][8],self.layout_result_list[i][7],self.record_str_hole_list[i],self.layout_result_list[i][14])))
    def Get_Workorder(self,if_is_glass,gq_index):
        '''
        该方法用于获得工位工单，先插入初始工位工单，再更新零件所用刀具信息，载更新零件信息
        :return:
        '''
        ap_id = 'WOID_' + time.strftime('%Y%m%d', time.localtime())
        total_seg = len(self.layout_result_list)  # 一床所放的门板块数
        if if_is_glass == 1:   #排玻璃门
            glass_num=total_seg
            machine_nums=MACHINE_NUM_GLASS
            priority_glass=20  #玻璃门优先级为20
            self.gq_record_layout_result[8] += 1
        else :  #1.2.3号机床
            if gq_index == 0 :
                machine_nums = MACHINE_NUM_1_2_3
                self.gq_record_layout_result[2] += 1
            else :#4.5.6号机床
                machine_nums = MACHINE_NUM_4_5_6
                self.gq_record_layout_result[5] += 1
            glass_num=0
            priority_glass=0
        if self.layout_result_list[0][25] == ELEMENT_LATICES_BOARD_INDEX:  #格子板
            self.gq_record_layout_result[1] += 1
        else:
            self.gq_record_layout_result[0] += 1 #单面板
        try:
            db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0], charset=charset)
            cursor = db.cursor()
            sql_insert = "INSERT INTO `work_cnc_task_list_temporary`(`Priority`,`Schedule_date`,`Board_Utilization_Ratio`,`Ap_id`, `Create_time`,`Material_norm`, `Total_seg`,`Thickness`,`State`,`Glass_num`,`Index_of_base_material_thickness`,`Machine_nums`,`CPU_index`) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                priority_glass,datetime.date.today(),self.utilization_ratio, ap_id, datetime.datetime.now(),str(Plate_Specification_Height+GQ_Reserve_Boundary) + '*' + str(Plate_Specification_Width+GQ_Reserve_Boundary), total_seg,
                self.layout_result_list[0][11], STATE_INITIAL,glass_num,self.layout_result_list[0][25],machine_nums,self.cpu_index)
            cursor.execute(sql_insert)
            db.commit()
            cursor.execute("SELECT `Index` FROM `work_cnc_task_list_temporary` WHERE 1 order by `Index`desc limit 1")  # 门板楣板罗马柱带拱压条都加到待排样表单了
            ap_id_idnex = cursor.fetchone()
            if ap_id_idnex != None:
                for i in range(len(self.component_information)):
                    str2 = 'Element_information_' + str(i + 1)
                    cursor.execute("UPDATE `work_cnc_task_list_temporary` SET `%s`='%s' WHERE `Index`='%s' " % (
                    str2, self.component_information[i], ap_id_idnex[0]))
                for i in range(len(self.layout_knife_name)):
                    str_knife='Knife_'+str(i+1)
                    cursor.execute("UPDATE `work_cnc_task_list_temporary` SET `%s`='%s' WHERE `Index`='%s' " % (
                        str_knife, self.layout_knife_name[i], ap_id_idnex[0]))
                db.commit()
                db.close()
                return RUN_NORMAL
        except:
            self.log.WriteText('创建工位工单出现错误，请进行检查  \r\n')
            return POST_LAYOUT_ERROR
    def Modify_Component_State_And_Get_Id_List(self):
        '''
        该方法为删除待排样表单中已完成排样的零件，修改零件库中门板的状态为已完成排样
        :return:
        '''
        try:
            db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0], charset=charset)
            cursor = db.cursor()
            for i in range(len(self.layout_result_list)):
                cursor.execute("DELETE FROM `work_cnc_before_layout` WHERE `Id`='%s' " % (self.layout_result_list[i][7]))
                cursor.execute("UPDATE `order_element_online` SET `Finish_Layout_Time`='%s' WHERE `Id`='%s' " % (
                    datetime.datetime.now(),self.layout_result_list[i][7]))
            db.commit()
            db.close()
        except:
            self.log.WriteText('修改完成排样的零件状态出现错误，请进行检查  \r\n')
######################更新状态和优先级
class Adjust_Priority_And_State():
    def __init__(self,log):
        self.log = log
    def Is_DBdatabase_Connected(self):
        '''
        本方法用来连接数据库，避免多次重复连接
        :return:
        '''
        try:
            self.db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0],charset=charset)
            self.db_produce = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[1],charset=charset)
            return True
        except:
            self.log.WriteText('数据库连接过程中出错请检查用户名、密码等信息  \r\n')
            return False
    def Adjust_State(self, id_list,finish_state):
        '''
        该方法的功能为：
        1.从零件库中找到完成加工的门板零件对应的部件、组件编号
        2.根据部件编号更新部件库的完成状态
        3.根据找到的组件编号，从部件库中找到该组件下的所有部件的状态，判断其是否需要修改完成状态
        4从组件库中根据组件编号找到订单编号，判断其是否需要修改完成状态
        5从订单库中找到合同编号，判断其是否需要修改完成状态
        :param finish_state:
        :return:
        '''
        sec_id=[]
        order_id = []
        contract_id=[]
        start_time = datetime.datetime.now()
        if (id_list == []):
            return UPDATE_STATE_ERROR
        try:
            if (self.Is_DBdatabase_Connected()):
                cursor = self.db.cursor()
                for i in range(len(id_list)):                #根据传入的零件编号找到对应的部件、组件、订单编号
                    list_split = id_list[i].split('ID')
                    part_id = list_split[0]
                    cursor.execute("UPDATE `order_part_online` SET `State`= '%s' WHERE `Part_id`='%s'" % (
                        finish_state, part_id))
                    list_sec=id_list[i].split('P')
                    sec_id.append(list_sec[0])
                    list_order=id_list[i].split('S')
                    order_id.append(list_order[0])
                    list_contract=id_list[i].split('O')
                    contract_id.append(list_contract[0])
                self.db.commit()
                sec_id_list=list(set([x for x in sec_id]))
                order_id_list=list(set([x for x in order_id]))
                contract_id_list=list(set([x for x in contract_id]))
                for j in range(len(sec_id_list)):
                    finish_layout_component_number = 0        #根据找到的组件编号，从部件库中找到该组件下所有部件的状态
                    cursor.execute("SELECT `State` from `order_part_online`  WHERE `Sec_id`='%s'" % sec_id_list[j])
                    part_state = cursor.fetchall()
                    for k in range(len(part_state)):               #判断该组件下的所有部件是否均已处于完成状态
                        if (part_state[k][0] < finish_state):
                            break
                        else:
                            finish_layout_component_number += 1
                    if finish_layout_component_number == len(part_state):        #若该组件下的所有部件均处于完成状态，则更新组件表单的状态
                        cursor.execute("UPDATE `order_section_online` SET `State`= '%s' WHERE `Sec_id`='%s' " % (
                            finish_state, sec_id_list[j]))
                        self.db.commit()
                for l in range(len(order_id_list)):
                    finish_layout_sec_number = 0        #根据找到的订单编号，从组件库中找到该订单下的所有组件的完成状态
                    cursor.execute("SELECT `State` from `order_section_online`  WHERE `Order_id`='%s' " % (order_id_list[l]))
                    sec_state = cursor.fetchall()
                    for m in range(len(sec_state)):               #判断该订单下的所有组件是否均已处于完成状态
                        if (sec_state[m][0] < finish_state):
                            break
                        else:
                            finish_layout_sec_number += 1
                    if finish_layout_sec_number == len(sec_state):    #订单下的所有组件均处于完成状态，修改该订单的状态为已完成
                        cursor.execute("UPDATE `order_order_online` SET `State`= '%s' WHERE `Order_id`='%s' " % (
                            finish_state, order_id_list[l]))
                        self.db.commit()
                for i in range(len(contract_id_list)):
                    finish_layout_order_num=0
                    cursor.execute(
                        "SELECT `State` from `order_order_online`  WHERE `Contract_id`='%s' " % (contract_id_list[i]))
                    order_state = cursor.fetchall()
                    for m in range(len(order_state)):  # 判断该订单下的所有组件是否均已处于完成状态
                        if (order_state[m][0] < finish_state):
                            break
                        else:
                            finish_layout_order_num += 1
                    if finish_layout_order_num == len(order_state):  # 订单下的所有组件均处于完成状态，修改该订单的状态为已完成
                        cursor.execute("UPDATE `order_contract_internal` SET `State`= '%s' WHERE `Contract_id`='%s' " % (
                            finish_state, contract_id_list[i]))
                        self.db.commit()
                end_time = datetime.datetime.now()
                self.log.WriteText(
                    '天外天系统正在运行修改各个工位完成状态的程序,  ' + '运行正常  运行时间为 ' + str(
                        (end_time - start_time).seconds * 1000 + (end_time - start_time).microseconds / 1000) + '毫秒  \r\n')
                self.db.close()
                return RUN_NORMAL
        except:
            self.log.WriteText('修改零件，部件，组件，订单的状态出现错误，请进行检查 \r\n')
        return UPDATE_STATE_ERROR
class GQ_Particle_Swarm_Algorithm():
    def __init__(self):
        self.gq_layout = GQ_Minimum_Horizontal_Line_Algorithm()
        self.birds = 350  # 初代撒种子的个数
        self.pop_size = 80  # 遗传代数
        self.dict = {}
    def Particle_Swarm_Algorithm(self,rectangle_list):
        '''
        粒子群算法
        :return:
        '''
        results = []
        self.chrom_length = len(rectangle_list)  # 问题规模的个数（每个标准型材上排放的块数）
        for i in range(0, self.chrom_length):  # 给所选矩形块编号
            self.dict[i + 1] = rectangle_list[i]
        self.pos = self.GeneEncoding()  # 给矩形块编码,pos为初始位置
        self.speed = self.GeneEncoding()  # speed为个体迁徙的初始速度
        best_obj_value, best_pop_value = self.CalobjValue()  # 每个个体的最优值以及种群最优值
        for j in range(self.pop_size):
            self.Update_Speed_And_Pos(best_obj_value, best_pop_value)  # 更新速度及位置
            self.Update_Obj_And_Pop_Value( best_obj_value, best_pop_value)  # 更新个体最优值以及种群最优值
            results.append(copy.deepcopy(best_pop_value[0]))
            if results[j][0] == 1.0:
                break
        results.sort(key=lambda x: -x[0])
        return results, self.dict
    def GeneEncoding(self):
        '''
        产生初代种群
        :return:
        '''
        sequence_list = []
        i = 0
        if self.birds > (self.chrom_length + (self.chrom_length * (self.chrom_length - 1)) / 2) * (self.chrom_length * (self.chrom_length - 1)):
            if self.chrom_length==1:
                num=2
            else:
                num = (self.chrom_length + (self.chrom_length * (self.chrom_length - 1)) / 2) * (self.chrom_length * (self.chrom_length - 1))
        else:
            num = self.birds
        while i < num:
            temp = []  # 对于选取的10个待排放的门板，随机产生1种排放顺序（初始种群数量）
            j = 0
            while j < self.chrom_length:
                sequence_num_value = random.randint(-self.chrom_length, self.chrom_length)  # 随机产生1-10中的一个数
                if sequence_num_value not in temp and -sequence_num_value not in temp and sequence_num_value != 0:  # 避免产生重复的数
                    temp.append(sequence_num_value)
                else:
                    j -= 1
                j += 1
            if temp not in sequence_list:
                sequence_list.append(temp)
            else:
                i -= 1
            i += 1
        return sequence_list
    def CalobjValue(self):
        '''
        此函数用于计算每个个体的值（即利用率）
        :return:
        '''
        best_obj_value = []  # 存放的是个体值（利用率）以及个体值对应的排放顺序
        best_pop_value = [[0]]  # 存放的是种群的最优值
        i = 0
        while i < len(self.pos):
            decode_list = []  # 将编完号的矩形块解码为原模样，存放在decode_list
            j = 0
            while j < self.chrom_length:
                if self.pos[i][j] < 0:  # 如果染色体中某一基因值为负值，则将此基因对应的矩形块长和宽互换
                    height = self.dict[-self.pos[i][j]][0]
                    self.dict[-self.pos[i][j]][0] = self.dict[-self.pos[i][j]][1]
                    self.dict[-self.pos[i][j]][1] = height
                    self.dict[-self.pos[i][j]][6] = 1
                decode_list.append(self.dict[abs(self.pos[i][j])])
                j += 1
            utilization_ratio, plate= self.gq_layout.Minimum_Horizontal_Line_Algorithm(decode_list)  # 根据此排序方式排放求出一个利用率（个体值）
            for k in range(len(self.dict)):  # 将排样状态置为0
                self.dict[k + 1][2] = 0
                if self.dict[k + 1][6] == 1:  # 若矩形块有旋转，将其旋转状态置为0，同时将交换了的长和宽换回来
                    width = self.dict[k + 1][0]
                    self.dict[k + 1][0] = self.dict[k + 1][1]
                    self.dict[k + 1][1] = width
                    self.dict[k + 1][6] = 0
            temporary_list = [utilization_ratio, self.pos[i],plate]
            best_obj_value.append(temporary_list)  # 将利用率及对应的排放顺序放到此列表中
            i += 1
        for l in range(len(best_obj_value)):
            if best_obj_value[l][0] > best_pop_value[0][0]:
                best_pop_value[0] = best_obj_value[l]
        return best_obj_value, best_pop_value
    def Update_Speed_And_Pos(self, best_obj_value, best_pop_value):
        '''
        此函数用于获得下一代每个个体对应的迁徙速度以及更新每个个体的位置
        :param best_obj_value:
        :param best_pop_value:
        :return:
        '''
        for i in range(len(self.pos)):
            velocity_coefficient = random.randint(0, 1)  # 每个个体的速度系数
            best_obj_coefficient = random.randint(0, 1)  # 每个个体的个体最优值系数
            best_pop_coefficient = random.randint(0, 1)  # 每个个体的种群最优值系数
            obj_subtract_result, self.pos[i] = self.Make_Subtract_Transform(best_obj_value[i][1], self.pos[i])  # 第一个个体的个体最优值与第i个个体的当前位置进行做变换
            pop_subtract_result, self.pos[i] = self.Make_Subtract_Transform(best_pop_value[0][1], self.pos[i])  # 第一个个体的种群最优值与第i个个体的当前位置进行做差变换
            if velocity_coefficient != 0 and best_obj_coefficient != 0 and best_pop_coefficient != 0:  # 影响速度的三个因素的系数值均不为0，速度相加项有三项两项，将结果赋值给一个变量，然后再加第三项
                first_result, addend = self.Add_Transform(self.speed[i], obj_subtract_result)
                self.speed[i], addend = self.Add_Transform(first_result, pop_subtract_result)  # 计算出个体的速度
            elif velocity_coefficient != 0:
                if best_obj_coefficient != 0:  # 速度系数与个体最优值系数不为0，种群最优值系数为0的情况
                    self.speed[i], addend = self.Add_Transform(self.speed[i], obj_subtract_result)
                elif best_pop_coefficient != 0:  # 速度系数与种群最优值系数不为0，个体最优值系数为0的情况
                    self.speed[i], addend = self.Add_Transform(self.speed[i], pop_subtract_result)
            elif best_obj_coefficient != 0:  # 速度系数为0，个体最优值系数不为0
                if best_pop_coefficient == 0:  # 种群最优值系数为0
                    self.speed[i] = obj_subtract_result
                else:  # 种群最优值系数不为0
                    self.speed[i], addend = self.Add_Transform(obj_subtract_result, pop_subtract_result)
            elif best_pop_coefficient != 0:
                self.speed[i] = pop_subtract_result
            self.pos[i], addend = self.Add_Transform(self.pos[i], self.speed[i])  # 更新每个个体的位置
    def Update_Obj_And_Pop_Value(self, best_obj_value, best_pop_value):
        '''
        此函数用于更新个体最优值以及种群的最优值
        :return:
        '''
        new_best_obj_value, new_best_pop_value = self.CalobjValue()  # 计算更新位置以后的个体最优值以及种群最优值
        for i in range(len(best_obj_value)):
            if new_best_obj_value[i][0] > best_obj_value[i][0]:  # 新计算的个体值大于上一次计算的值，更新个体最优值
                best_obj_value[i][0] = new_best_obj_value[i][0]
                best_obj_value[i][1] = new_best_obj_value[i][1]
        if new_best_pop_value[0][0] > best_pop_value[0][0]:
            best_pop_value[0][0] = new_best_pop_value[0][0]
            best_pop_value[0][1] = new_best_pop_value[0][1]
        return best_obj_value, best_pop_value
    def Make_Subtract_Transform(self,best_sequence, obj_sequence):
        '''
        此函数用于两种排样顺序的做差变换
        :param best_obj_sequence:
        :param obj_sequence:
        :return:
        '''
        subtract_result = [0] * self.chrom_length
        save_obj_sequence = copy.deepcopy(obj_sequence)
        for i in range(len(best_sequence)):
            for j in range(len(obj_sequence)):
                if abs(best_sequence[i]) == abs(obj_sequence[j]):
                    subtract_result[i] = j + 1  # 减法变换为加法变换的逆变换，该列表记录的是交换顺序
                    sequence_value = obj_sequence[i]  # 每产生一种顺序，将obj_sequence按顺序交换一下
                    obj_sequence[i] = obj_sequence[j]
                    obj_sequence[j] = sequence_value
                    break
        obj_sequence = save_obj_sequence
        return subtract_result, obj_sequence
    def Add_Transform(self,addend, Augend):
        '''
        此函数用于两种排样顺序的加法变换
        :param addend: 加数
        :param Augend: 被加数
        :return:
        '''
        save_addend = copy.deepcopy(addend)
        for i in range(len(Augend)):
            sequence_value = addend[i]  # 按交换顺序进行交换，获得结果
            addend[i] = addend[abs(Augend[i]) - 1]
            addend[abs(Augend[i]) - 1] = sequence_value
        add_result = copy.deepcopy(addend)
        addend = save_addend
        return add_result, addend
##################最低水平线算法
class GQ_Minimum_Horizontal_Line_Algorithm():
    def __init__(self):
        self.Init_Layout_Parameter()
    def Init_Layout_Parameter(self):
        self.plate_specification_height = Plate_Specification_Height
        self.plate_specification_width = Plate_Specification_Width
    def Minimum_Horizontal_Line_Algorithm(self,list):
        '''
        该算法为最低水平线排样算法
        :return:
        '''
        self.gq_layout_list=list
        self.left_area=0
        self.minimum_horizontal_line=0                #设定最低水平线的初始值
        self.left_wait_layout_width = self.plate_specification_width        # 待填充区域的宽度
        i=0
        j=1
        self.plate = [[0 for col in range(26)] for row in range(300)]  # 该二维列表存放的是放入矩形块的横纵坐标以及新产生待填充矩形的长和宽，放入矩形的长和宽
        self.plate[0] = [0, 0, self.plate_specification_height, self.plate_specification_width, 0, 0,0, 0,0, 0,0, 0,0, 0,0, 0,0, 0,0, 0,0, 0,0, 0,0, 0]  # 待填充矩形的长为2400，宽为1200
        while i<j:
            can_not_layout_enable = 0  # 该变量为0表示所有矩形块都放不进当前待填充矩形块
            wait_layout_long=self.plate[i][2]
            for k in range(len(self.gq_layout_list)):        #矩形块可以放进待填充区域
                if self.gq_layout_list[k][2]==0 :
                    if wait_layout_long>=self.gq_layout_list[k][1] and self.left_wait_layout_width>=self.gq_layout_list[k][0] :        #门板立着(只有无纹的情况才能立着，否则纹就旋转了)可以放进去
                        if self.gq_layout_list[k][6]==2 and self.plate[i][5] == 0:      #后放的，未旋转,将其旋转状态置为0,plate中未放，才能放
                            self.gq_layout_list[k][6]=0
                            can_not_layout_enable = self.Can_Layout(i, j, k)
                            j += 1
                            break
                        elif self.gq_layout_list[k][6]!=2 :
                            can_not_layout_enable = self.Can_Layout(i, j, k)
                            j += 1
                            break
                    elif wait_layout_long>=self.gq_layout_list[k][0] and self.left_wait_layout_width>=self.gq_layout_list[k][1] and self.gq_layout_list[k][6]==2  :                    #后面补放的零件，如果立着放不进来，将其旋转，或者是膜压有纹的情况
                        component_long=self.gq_layout_list[k][0]
                        self.gq_layout_list[k][0]=self.gq_layout_list[k][1]
                        self.gq_layout_list[k][1]=component_long
                        self.gq_layout_list[k][6]=1
                        can_not_layout_enable=self.Can_Layout(i,j,k)
                        j+=1
                        break
            i += 1
            if can_not_layout_enable==0 and i==j:     #当前水平线下所有待填充区域矩形块都放不进去，则提升最低水平线
                self.Lift_Level_Line()                                           #提升最低水平线
                if self.layout_component_information==[]:
                    break
                self.left_wait_layout_width=self.plate_specification_width-self.minimum_horizontal_line                         #提升水平线之后，计算待填充区域的宽度
                j=self.Get_Wait_Layout_Region(j)
        utilization_ratio = round(float(self.left_area) / (self.plate_specification_height*self.plate_specification_width),3)
        return utilization_ratio,self.plate
    def Can_Layout(self,current_level,total_level,index):
        '''
        该函数的功能是：当举行块可以摆放进去时，记录摆放的信息以及新产生的待填充区域
        :return:
        '''
        self.plate[current_level][4:26] = self.gq_layout_list[index][0:22]  # 记录放入矩形的长和宽
        can_not_layout_enable = 1
        self.gq_layout_list[index][2] = 1
        self.plate[total_level][0] = self.plate[current_level][0] + self.gq_layout_list[index][1]
        self.plate[total_level][1] = self.plate[current_level][1]
        self.plate[total_level][2] = self.plate[current_level][2] - self.gq_layout_list[index][1]
        self.plate[total_level][3] = self.left_wait_layout_width
        self.left_area += self.gq_layout_list[index][0] * self.gq_layout_list[index][1]
        return can_not_layout_enable
    def Get_Wait_Layout_Region(self,total_level):
        '''
        当提升最低水平线之后，该函数用于获得用于存放矩形的待填充区域
        :return:
        '''
        self.layout_component_information.sort(key=lambda x: x[3])                     #将存储信息的列表按矩形块的横坐标升序排列
        i=0
        while i<len(self.layout_component_information):
            if self.layout_component_information[i][0]==self.minimum_horizontal_line:            #矩形块的左上角坐标所处位置有两种情况：在最低水平线上与在最低水平线之上
                if i==len(self.layout_component_information)-1:               #左上角坐标在最低水平线上又分:三种情况：1.从第k块之后可以找到左上角坐标在水平线之上的矩形块2：从第k块之后直到最后一块也没找到左上角坐标在水平线之上的3：第k块本身就处于排放的最后一块
                    self.plate[total_level][2] = self.plate_specification_height- self.layout_component_information[i][3]
                    total_level=self.Get_New_Plate_Information(total_level,self.layout_component_information[i][3])
                for j in range(i+1,len(self.layout_component_information)):
                    if self.layout_component_information[j][0]!=self.minimum_horizontal_line:
                        if i==0 and self.layout_component_information[i][3]!=0:                #第一块在水平线上且横坐标不为0的情况
                            self.plate[total_level][2] = self.layout_component_information[j][3]
                            total_level = self.Get_New_Plate_Information(total_level,0)
                        else:
                            self.plate[total_level][2] = self.layout_component_information[j][3] -self.layout_component_information[i][3]
                            total_level =self.Get_New_Plate_Information(total_level,self.layout_component_information[i][3])
                        i = j - 1
                        break
                    elif j==len(self.layout_component_information)-1 and self.layout_component_information[j][0]==self.minimum_horizontal_line:
                        if i == 0 and self.layout_component_information[i][3] != 0:                   #第一块在水平线上且横坐标不为0的情况
                            self.plate[total_level][2] = self.plate_specification_height
                            total_level = self.Get_New_Plate_Information(total_level,0)
                        else:
                            self.plate[total_level][2] = self.plate_specification_height- self.layout_component_information[i][3]
                            total_level =self.Get_New_Plate_Information(total_level,self.layout_component_information[i][3])
                        i = j
                        break
            else:                                   #第k块矩形块的左上角坐标在最低水平线之上，此种情况
                x_label_list = [x[3] for x in self.layout_component_information]                                  #该列表存放的是矩形块的横坐标
                get_x_label = self.layout_component_information[i][3] + self.layout_component_information[i][2]           #将矩形块的横坐标加上矩形块的宽，将其赋值于get_x_label，self.layout_component_information列表中左上角坐标与get_x_label有两种关系：get_x_label在列表中或不在列表中（或者第k块处于本身就处于排放的最后一块）：
                                                                                                                #在列表中的情况又可分为第k+1块的左上角坐标在最低水平线上（讨论情况如上）、在最低水平线之上（不做任何处理）或第k+1块本身就处于排放的最后一块
                                                                                                           #不在列表中的情况又可分为1：从第k块之后可以找到左上角坐标在最低水平线之上的矩形块2：从第k+1块之后直到最后一块也没找到左上角坐标在水平线之上的
                if i==len(self.layout_component_information)-1:               #第k块处于排放的最后一块
                    self.plate[total_level][2] = self.plate_specification_height- get_x_label
                    total_level=self.Get_New_Plate_Information(total_level,get_x_label)
                elif get_x_label not in x_label_list:                   #不在列表中的情况
                    if i == 0 and self.layout_component_information[i][3] != 0:  # 第一块在水平线之上且横坐标不为0的情况（该列表中有多块门板）
                        self.plate[total_level][2] = self.layout_component_information[i][3]
                        total_level = self.Get_New_Plate_Information(total_level,0)
                    for k in range(i+1,len(self.layout_component_information)):
                        if self.layout_component_information[k][0]!=self.minimum_horizontal_line:
                            self.plate[total_level][2] = self.layout_component_information[k][3] - get_x_label
                            total_level = self.Get_New_Plate_Information(total_level,get_x_label)
                            i =k - 1
                            break
                        elif k==len(self.layout_component_information)-1 and self.layout_component_information[k][0]==self.minimum_horizontal_line:
                            self.plate[total_level][2] = self.plate_specification_height- get_x_label
                            total_level =self.Get_New_Plate_Information(total_level,get_x_label)
                            i = k
                            break
                elif i == 0 and self.layout_component_information[i][3] != 0:  # 第一块在水平线之上且横坐标不为0的情况（该列表中有多块门板）
                    self.plate[total_level][2] = self.layout_component_information[i][3]
                    total_level = self.Get_New_Plate_Information(total_level,0)
                elif self.layout_component_information[i+1][0]!=self.minimum_horizontal_line:  # 在列表中的情况，但第i+1块处于最低水平线之上，此时啥也不做
                    pass
                elif self.layout_component_information[i+1][0]==self.minimum_horizontal_line:       #在列表中的情况（第k+1块矩形的左上角坐标在最低水平线上）
                    if i == len(self.layout_component_information) - 2:  # 在列表中的情况(第k+1块处于排放的最后一块)
                        self.plate[total_level][2] = self.plate_specification_height- get_x_label
                        total_level = self.Get_New_Plate_Information(total_level, get_x_label)
                        i += 1
                    for l in range(i+2,len(self.layout_component_information)):
                        if self.layout_component_information[l][0]!=self.minimum_horizontal_line:                  #从第k块之后可以找到左上角坐标在最低水平线之上的矩形块
                            self.plate[total_level][2] = self.layout_component_information[l][3] - get_x_label
                            total_level = self.Get_New_Plate_Information(total_level, get_x_label)
                            i = l - 1
                            break
                        elif l==len(self.layout_component_information)-1 and self.layout_component_information[l][0]==self.minimum_horizontal_line:           #找到末尾了还是没找到左上角坐标在最低水平线之上的
                            self.plate[total_level][2] = self.plate_specification_height- get_x_label
                            total_level = self.Get_New_Plate_Information(total_level, get_x_label)
                            i = l
                            break
            i+=1
        return total_level
    def Get_New_Plate_Information(self,total_level,x_label):
        self.plate[total_level][0] = x_label
        self.plate[total_level][1] = self.minimum_horizontal_line
        self.plate[total_level][3] = self.left_wait_layout_width
        total_level += 1
        return total_level
    def Lift_Level_Line(self):
        '''
        该函数用于提升最低水平线
        :return:
        '''
        self.layout_component_information=[]          #该列表存放的是矩形块左上角坐标高于最低水平线的矩形信息（左上角坐标，矩形块放入self.plate的序号，矩形的宽度以及矩形的横坐标）
        for i in range(len(self.plate)):
            if self.plate[i][4]!=0 :
                if self.plate[i][1]+self.plate[i][4] >self.minimum_horizontal_line:                   #矩形块的左上角坐标大于最低水平线
                    temporary_list=[self.plate[i][1]+self.plate[i][4],i,self.plate[i][5],self.plate[i][0]]
                    self.layout_component_information.append(temporary_list)
        if self.layout_component_information!=[]:
            self.layout_component_information.sort(key=lambda x: x[0])                       #将self.layout_component_information列表中的左上角坐标一列按升序排序，以便提升最低水平线
            for j in range(len(self.layout_component_information)):
                if self.layout_component_information[j][0]!=self.minimum_horizontal_line:
                    self.minimum_horizontal_line=self.layout_component_information[j][0]
                    break

