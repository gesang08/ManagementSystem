#!/usr/bin/python
# _*_ coding: UTF-8 _*_
#封装成类
#20171220
#修改完善了错误处理机制
#加入了3秒时间事件timer，用于即便程序出现错误，也不会卡在程序内部，无法开始新的运行。加入时间事件，错误在数据库里排除后，3秒时间一到，开始重新执行
#在Post_Package_Update_Package_State函数中关闭数据库
#20171222
#加入了扫码枪与打包程序的接口部分，修改了组件、部件、零件的正在打包中状态，修改了组件、部件、零件打包完成状态
#20171224
#修改了打包后完成状态
#考虑了扫码枪的各个返回值的意义
#修改了AP_id函数，工位工单编号函数，增加了工单最大条数，换为5位，以后还可再大，修改方便灵活
#20180102
#修改了Layout_2D函数，Plate列表增加到30列。
#20180104
#修改组件、部件、零件库状态时，都改为修改online表单（在线表单）
#20180106
#调扫码枪返回值,0表示正常接单，1表示该件未完成质检，2该件正在打包中，3该件已完成打包，请报管理员，100该件已出打包工位，情报管理员。
#cp001表单里能正确的加入操作员与打包完成时间。
#修改了equipment_scanner表单里Position的值，打包工位Position的值为‘11’。
#20180107
#往在线 零件库 里加入了打包开始时间和操作员id。修改了odeGun_StationComputer和Update_State_NowPackage函数。
#20180109
#往在线 部件库 里加入了打包开始时间和操作员id。修改了Update_State_NowPackage函数。
#加入了更新订单状态（订单正在打包中&打包完成）的程序
#修改了CodeGun_StationComputer函数，添加了打包工位表单里操作员（`operator`）的信息，在开始接单时填入操作员信息。
#20180111
#打包工位工单数据库（work_package_task_list）增加了一个字段，该包的总面积（Total_area）。修改了Post_Package_Select_Workorder函数。
#20180125：
#YLP：修改了打包程序。打包完成后，优化了修改订单及组件的打包完成状态的代码。测试成功。
#---------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------
#20180402:
#瀚海工厂没有打包箱，所以读打包箱表单只是为了获取层数信息，该包的长度，宽度分别是尺寸最大的门板的长宽加50mm的余量，写入数据库的格式也变了，把一个零件的信息放到了一个字段里，中间用“&”符号间隔。
#向零件表单填入了（order_element_online)的两个字段（Package_work_order_ap_id & package_work_order_create_time）。
#20180404：
#把当天的总包数信息填入生产调度work_production_scheduling表单，并修改状态字段为打包排样完成。
#20180704a:
#包装的尺寸是按照长度最长，宽度最宽来排的，有可能导致底层会排好几块板子。
#20180723b:
#附件需要单独打包，不能与门板混包。附件打包方案是：一个组件的打一包。附件目前包含：顶线，腰线，踢脚线。
#20180723c:
#门板打包出现这种现象：最后一包的门板块数只有一两块，或面积很少，但是程序还是打了一包。这种情况应该避免。
#20180724a:
#增加了一些注释，删除了之前与扫码枪对接的地方的函数。
#20180724b:
#打包工位工单编号协议做了修改，删除了“ID_”，变得更加简短。
#20180724c:
#修改了开始运行打包算法的条件，当有组件需要打包时 同时生产调度表单里状态为排样结束，就开始打包算法。
#20180724d:
#打包工单表单 新增了一个 需要填的字段“Package_num_now” ，意思是该包是该组件的第几包。
#20180725a:
#数据库修改了字段类型，部件库里 是否是玻璃门的字段（‘Heart_type’）由原来的int型改为varchar型。
#向部件库里添加了一个字段信息（Package_task_list_ap_id），即该部件所属的工单的工单编号。

import MySQLdb
import time
import wx
from compiler.ast import flatten
from ID_DEFINE import *
##----------------------------------------------------------------
PACKAGE_STATE=1
SECTION_PACKAGE_FINISH=5
##--------------------------------------------------------------
class Package():
    def __init__(self,log):
        self.log=log
        self.enabled=True
        self.isrunning=False
        self.all_package_num=0
        self.last_package_information = []
        self.timer_second = wx.PyTimer(self.Timer)
        self.timer_second.Start(3000)
    def Is_NewPackage(self):      #判断是否需要对组件进行打包算法
        start_newpackage =True
        try:
            db = MySQLdb.connect(server_ip, user_list[0], password, database[0])
            cursor = db.cursor()
            cursor.execute("SELECT `Index`,`Order_id`,`Sec_id` FROM `order_section_online` WHERE `Package_state`=0 ")
            record = cursor.fetchone()
            cursor.execute("SELECT `Index` FROM `work_production_scheduling`  WHERE `State`='%s'" % SCHEDULE_LAYOUT_FINISH)
            record1=cursor.fetchone()
            db.close()
            if record == ()or record == None or record1==() or record1 == None or self.isrunning:
                start_newpackage = False
                return start_newpackage
            else:
                self.order_id=record[1]
                self.sec_id=record[2]
        except:
            start_newpackage = False
            self.log.WriteText('天外天系统正在运行打包程序Is_NewPackage函数, 报错 请检查生产数据库连接及表单名有无错误 \r\n')
            return start_newpackage
        return start_newpackage
    def Is_Database_Connected(self):
        try:
            self.db = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0], charset=charset)
        except:
            self.log.WriteText('天外天系统正在运行打包程序, db_hanju数据库连接不成功 \r\n')
            return False
        return True

    def Package_Main(self):
        self.isrunning = True
        if (self.Is_Database_Connected()):
            ERROR_ID= self.Pre_Package()
            if ERROR_ID == 0:
                ERROR_ID=self.Package_CoreProgram()
                if ERROR_ID==0:
                    ERROR_ID = self.Post_Package_Update_Package_State()
                    if ERROR_ID == 0:
                        self.isrunning = False

    #-----------------------中层函数-----------------------------------------------------------------
    def Pre_Package( self):
        ERROR_ID,sec_id=self.Pre_Package_Get_Sec_id()
        if ERROR_ID==0:
            ERROR_ID=self.Pre_Package_Get_Part_Information(sec_id)
            if ERROR_ID == 0:
                ERROR_ID =self.Pre_Package_Read_Box()
                if ERROR_ID == 0:
                    return ERROR_ID
    def Package_CoreProgram(self):
        ERROR_ID = 0
        BOX_LONG = 1
        BOX_SHORT = 2
        PLIES_18MM = 3
        PLIES_20MM = 4
        PLIES_22MM = 5
        PLIES_25MM = 6
        have_box=False
        onesec_door_inform=[]    #一个组件 每一包的 每一块门板的信息    3维列表
        onesec_package_Numplies=[]   #一个组件 每一包的 每一层的门板块数    2维列表
        onesec_package_totalplies=[]   #一个组件 每一包的总块数        1维列表

        try:
            self.part_information=self.door_part_information
            sec_id = self.part_information[0][6]
            for i in range(len(self.part_information)):  # 该循环作用：一个组件门板打几个包
                if (self.part_information != []):
                    width_range=[]
                    max_door_height = self.part_information[0][0]    #取长度最长的门板
                    #max_door_width = self.part_information[0][1]
                    max_door_width=max([x[1] for x in self.part_information])      #取宽度最宽的门板
                    door_thick = self.part_information[0][2]
                    for j in range(len(self.Box_information)):
                        if 0 < max_door_height <= self.Box_information[j][BOX_LONG] and 0 < max_door_width <= self.Box_information[j][BOX_SHORT]:
                            have_box=True
                            if door_thick == 18:
                                plies = self.Box_information[j][PLIES_18MM]
                            elif door_thick == 20:
                                plies = self.Box_information[j][PLIES_20MM]
                            elif door_thick == 22:
                                plies = self.Box_information[j][PLIES_22MM]
                            elif door_thick == 25:
                                plies = self.Box_information[j][PLIES_25MM]
                            plate1, Num_plies1, Total_plies = self.Package(plies, max_door_height+50, max_door_width+50, i)  # i 表示这是第几箱
                            onesec_door_inform.append(plate1)
                            onesec_package_Numplies.append(Num_plies1)
                            onesec_package_totalplies.append(Total_plies)
                            break
                    if not  have_box:   #特殊尺寸，只打包一层
                        plate1, Num_plies1, Total_plies = self.Package(1, max_door_height, max_door_width, i)
                        onesec_door_inform.append(plate1)
                        onesec_package_Numplies.append(Num_plies1)
                        onesec_package_totalplies.append(Total_plies)
            if onesec_package_totalplies[-1]<=2 or sum(onesec_package_Numplies[-1])<=3 :
                need_combine_doorinform=[]
                for i in range(len(onesec_package_totalplies)):
                    if i==len(onesec_package_totalplies)-1:    #循环到最后一包，如果该组件所有的包都是6层，那就得单独打一包了。这种情况目前没有处理，应该从别的包里拆出来几块与该包合到一起。
                        break
                    if onesec_package_totalplies[len(onesec_package_totalplies)-2-i]<6:      #如果倒数第二包（倒数第i包）的层数小于6层
                        onesec_package_totalplies[len(onesec_package_totalplies)-2-i]+=1     #则倒数第二包（倒数第i包）的层数加1

                        onesec_package_Numplies[len(onesec_package_totalplies)-2-i][onesec_package_totalplies[len(onesec_package_totalplies)-2-i]-1]=sum(onesec_package_Numplies[-1])
                                                        # 倒数第二包的索引，               的最后一层块数
                        #把要合并的这一包（B包）的总块数（每一层块数之和）赋值给接收它的那一包（A包）的下一层的总块数   A=[1,1,1,1,0,0]     B=[1,1,0,0,0,0]   合并后A=[1,1,1,1,2,0]


                        for j in range(len(onesec_door_inform[-1])):
                            if onesec_door_inform[-1][j][2]!=0:
                                need_combine_doorinform.append(onesec_door_inform[-1][j])
                        for j in range(len(need_combine_doorinform)):
                            onesec_door_inform[len(onesec_package_totalplies)-2-i][(onesec_package_totalplies[len(onesec_package_totalplies)-2-i]-1)*10+j]=need_combine_doorinform[j]
                        # 把B包的每一层的门板的信息提出来，然后放入到A包新一层的位置上。

                        del onesec_door_inform[-1]
                        del onesec_package_Numplies[-1]
                        del onesec_package_totalplies[-1]
                        break
            #最后一起把数据写入到数据库
            how_many_bags=0
            for i in range(len(onesec_package_totalplies)):
                plate1=onesec_door_inform[i]
                Num_plies1=onesec_package_Numplies[i]
                Total_plies=onesec_package_totalplies[i]
                ERROR_ID,Ap_id = self.AP_id()  # 下料工位工单编号函数
                how_many_bags=i+1
                if ERROR_ID==0:
                    ERROR_ID= self.Post_Package(sec_id, plate1, Num_plies1,Total_plies, Ap_id,how_many_bags)



            #附件的打包 self.accessory_part_information
            if len(self.accessory_part_information)!=0:   #如果有附件
                ERROR_ID, Ap_id = self.AP_id()  # 下料工位工单编号函数
                if ERROR_ID == 0:
                    accessory_info=[[0 for col in range(11)] for row in range(60)]
                    for i in range(len(self.accessory_part_information)):
                        accessory_info[i][5]=self.accessory_part_information[i][0]   #附件高
                        accessory_info[i][6] = self.accessory_part_information[i][1]  #附件宽
                        accessory_info[i][10] = self.accessory_part_information[i][4]  #附件的部件编号
                    ERROR_ID = self.Post_Package(sec_id, accessory_info, (0,0,0,0,0,0), 0, Ap_id,how_many_bags+1)



        except:
            ERROR_ID = 16000
            self.log.WriteText('天外天系统正在运行打包程序Package_CoreProgram函数, 报错  \r\n')
            return ERROR_ID
        return ERROR_ID
    def Post_Package(self,sec_id, plate1, Num_plies1, Total_plies, Ap_id,how_many_bags):
        if (self.Is_Database_Connected()):
            ERROR_ID=self.Post_Package_Select_Workorder(sec_id, plate1, Num_plies1, Total_plies, Ap_id,how_many_bags)
            if ERROR_ID==0:
                return ERROR_ID

    #------------------------底层函数------------------------------------------------------------------
    def Pre_Package_Get_Sec_id(self):
        ERROR_ID=0
        sec_id=[]
        try:  # 读组件表单
            cursor = self.db.cursor()
            #sql="SELECT  `Sec_id` FROM `order_section_online` WHERE `Package_state`=0 ORDER BY `Priority` DESC "
            sql="SELECT  `Sec_id` FROM `order_section_online` WHERE `Package_state`=0 "
            cursor.execute(sql)
            sec_id = cursor.fetchone()
            if len(sec_id)==0:    #组件库里为空
                ERROR_ID=15000
                self.log.WriteText('天外天系统正在运行打包程序Pre_Package_Get_Sec_id函数, 读组件库发现存在未打包的组件，但其组件号有为空 \r\n')
                return  ERROR_ID,sec_id
        except:
            ERROR_ID = 15001
            self.log.WriteText('天外天系统正在运行打包程序Pre_Package_Get_Sec_id函数, 报错 请检查组件库的表单名及字段有无错误 \r\n')
            return ERROR_ID,sec_id
        return ERROR_ID,sec_id[0]
    def Pre_Package_Get_Part_Information(self,sec_id):
        ERROR_ID = 0
        HEIGHT=0
        WIDTH=1
        self.part_information=[]
        self.door_part_information=[]
        self.accessory_part_information=[]
        try:
            cursor = self.db.cursor()
            #cursor.execute( "SELECT  `Door_height`, `Door_width`, `Door_thick`,`Package_state`,`Part_id`,`Door_type`,`Sec_id` ,`Heart_type` FROM `order_part_online` WHERE `Sec_id`='%s' ORDER BY `Door_height` DESC ,`Door_width` DESC" %sec_id)
            cursor.execute( "SELECT  `Door_height`, `Door_width`, `Door_thick`,`Package_state`,`Part_id`,`Door_type`,`Sec_id` ,`Heart_type`,`Element_type_id` FROM `order_part_online` WHERE `Sec_id`='%s' " %sec_id)
            part_information1 = cursor.fetchall()
            if part_information1==() or part_information1==None:
                ERROR_ID = 15005
                self.log.WriteText('天外天系统正在运行打包程序Pre_Package_Get_Part_Information函数, 报错 给定组件号下的部件信息为空 \r\n')
                return ERROR_ID
            for i in range(len(part_information1)):    #for循环的作用：检查record列表里是否有高度小于宽度的情况，如果有，交换值,把所有的高度宽度都转为长短边，用于选择箱子尺寸
                self.part_information.append(list(part_information1[i]))  # 元组转化成列表
                self.part_information[i][3]=0   #不管此时的打包状态是多少，都把它置为0，为后期排样做准备
                if self.part_information[i][HEIGHT]<self.part_information[i][WIDTH]:
                    self.part_information[i][HEIGHT],self.part_information[i][WIDTH]=self.part_information[i][WIDTH],self.part_information[i][HEIGHT]
            self.part_information.sort(key=lambda  x:(x[HEIGHT],x[WIDTH]), reverse=True)    #然后在进行一次排序
            for i in range(len(self.part_information)):
                if self.part_information[i][8]==4 or self.part_information[i][8]==5 or self.part_information[i][8]==6:
                    self.accessory_part_information.append(self.part_information[i])  # 附件
                else:
                    self.door_part_information.append(self.part_information[i])  # 门板部件


        except:
            ERROR_ID = 15006
            self.log.WriteText('天外天系统正在运行打包程序Pre_Package_Get_Part_Information函数, 报错 请检查组件库的表单名及字段有无错误 \r\n')
            return ERROR_ID
        return ERROR_ID
    def Pre_Package_Read_Box(self):
        ERROR_ID=0
        try:#读箱子表单
            cursor = self.db.cursor()
            cursor.execute("SELECT `Box_type`, `Box_long`, `Box_short`, `Plies_18mm`, `Plies_20mm`, `Plies_22mm`, `Plies_25mm` FROM `equipment_package_box` WHERE 1 ORDER BY `Box_long` ,`Box_short` ")
            self.Box_information = cursor.fetchall()
        except:
            ERROR_ID = 15010
            self.log.WriteText('天外天系统正在运行打包程序Pre_Package_Read_Box函数, 报错 请检查组件库的表单名及字段有无错误 \r\n')
            return ERROR_ID
        return ERROR_ID

    def Package(self, plies, height, width, package_num):
        '''
        错误代码从15030——15060
        :param plies:
        :param height:
        :param width:
        :param package_num:
        :return:
        '''
        #Record=self.part_information
        record = []
        # for i1 in Record:  # 元组转化成列表
        #     record.append(list(i1))
        Num_plies = []
        Num_plies1 = [0] * 6  # 每一层的块数，每层最多10块
        plate1 = [[0 for col in range(11)] for row in range(60)]  # 一包里部件总数，共6层，每层10块，为了输出
        b = 0  # 变量a 与 b的作用主要是为了输出，b 负责层数 ，每排一层，b加10
        Total_plies = 0  # 总共铺了几层
        for j in range(plies):  # 层数，循环一次，调用一次二维排样排一层，至于要排几层由变量plies(层数)控制，这是根据箱子的尺寸及部件的厚度决定的
            edge = 0
            control = 0
            glass_board_num=[x[7] for x in self.part_information].count('1')   # 这个for循环的作用及目的：每排完一层，判断剩余部件里是否都是玻璃板的，如果是，就允许玻璃板的排顶层或底层，这样有效防止了顶层没有排样的现象，防止丢件。
            if len(self.part_information) == glass_board_num:  # 说明剩下的全是玻璃板，此时玻璃板就可以放底层和顶层
                edge = 0
                control = 1
            if (j == 0 or j == 1) and control == 0:  # 如果是底层或顶层，则edge=1，若edge==1则只排实心的，不排玻璃框的
                edge = 1
            if plies == 1:  # 特殊尺寸，只打一层
                edge = 0
            num_plies = 0
            Plate, num =self.Layout_2D(self.part_information, height, width, edge)  # 调用二维排样函数
            a = 0  # a 负责每一层上的块数，每放进1块，a 加 1
            for k in range(len(Plate)):  # 赋值层数（即这一版的排样位于第几层）
                if Plate[k][5] != 0:  # 说明有一个部件放入了
                    Plate[k][8] = j + 1  # 该语句显示该部件处于第几层（从1 开始）
                    Plate[k][9] = package_num + 1  # 该语句显示该部件处于第几包
                    num_plies += 1  # 每一层放入了几块？
                    plate1[a + b] = Plate[k]
                    a += 1
            b += 10
            Num_plies.append(num_plies)  # 把每一层的块数都追加进Num_plies列表里
            num.sort()  # 给num 升序，用于下面的删除
            for i in range(len(num) - 1, -1, -1):  # 把这一层已被排版的部件删除，以便于下一层的排版
                del self.part_information[num[i]]
        for i in range(len(Num_plies)):  # 每一层的块数，（若某层一块都没有就是0）把Num_plies列表里的值赋给Num_plies1（1行6列）列表，主要是为了输出
            Num_plies1[i] = Num_plies[i]
        for i in Num_plies:  # 因为每一包的最高上限是6层，通过这个for循环判断实际放了几层？ 作用：为了输出，前端画界面图要用
            if (i != 0):
                Total_plies += 1
        return plate1, Num_plies1, Total_plies
    def Layout_2D(self,Record, height, width, edge):
        '''
        15060——15090
        :param Record:
        :param height:
        :param width:
        :param edge:
        :return:
        '''
        record = []
        for i1 in Record:  # for循环作用：把Record元组转换成列表，以便于后期改变某个元素的数值（因为元组的值是不能改变的 ）
            record.append(list(i1))  # 注意：只要是用append追加进数据的列表，一定要在for循环前定义该列表
        current_level = 0
        total_level = 1
        position = 0
        spill=False
        num = []
        left_area = height * width
        Result = [0] * 10     #每层最多放10块
        Plate = [[0 for col in range(11)] for row in range(60)]
        Plate[0] = [0, 0, height, width, 0, 0, 0, 0, 0, 0, 0]
        while (current_level < total_level):  # 加入这个条件主要是为了，判断每一块新生成的板能否容下未排样的部件
            long_edge = Plate[current_level][2]
            short_edge = Plate[current_level][3]
            for i in range(0, len(record)):
                if record[i][3] == 0:
                    a=record[i][7]
                    if ((edge == 1 and record[i][7] == '0') or edge == 0):  # 实现了玻璃门不能放底层或顶层，edge==1表示排底层或顶层；edge==0表示非底层、顶层；record[i][7]==0表示部件是实心的
                        if ((long_edge >= record[i][0]) and (short_edge >= record[i][1])):  # 芯板能放进去
                            record[i][3] = 1
                            if position>=10:
                                spill=True
                                break
                            Result[position] = i + 1  # position表示放了几块芯板
                            position += 1
                            left_area = left_area - record[i][0] * record[i][1]
                            Plate[current_level][5:8] = record[i][0:3]  # 将放入芯板的尺寸放入Plate列表中
                            Plate[current_level][10] = record[i][4]  # 把该部件的编号放入Plate列表里，用于输出生成工位工单
                            if ((record[i][0] >= short_edge - record[i][1]) and (Plate[current_level][4] == 0)):
                                Plate[total_level][4] = 0  # 当前待填充芯板的旋转状态为0
                                Plate[total_level][2] = record[i][0]  # 待填充芯板的尺寸
                                Plate[total_level][3] = short_edge - record[i][1]
                                Plate[total_level][0] = Plate[current_level][0]  # 赋值左下角坐标
                                Plate[total_level][1] = Plate[current_level][1] + record[i][1]
                            elif ((record[i][0] < short_edge - record[i][1]) and (Plate[current_level][4] == 0)):  # 新生成第一块待填充芯板是竖直的，且上一块待填充芯板是横的
                                Plate[total_level][4] = 1
                                Plate[total_level][2] = short_edge - record[i][1]  # 赋值当前待填充芯板的尺寸
                                Plate[total_level][3] = record[i][0]
                                Plate[total_level][0] = Plate[current_level][0]
                                Plate[total_level][1] = Plate[current_level][1] + record[i][1]
                            elif ((record[i][1] >= long_edge - record[i][0]) and (Plate[current_level][4] == 1)):
                                Plate[total_level][2] = record[i][1]
                                Plate[total_level][3] = long_edge - record[i][0]
                                Plate[total_level][4] = 0
                                Plate[total_level][0] = Plate[current_level][0]
                                Plate[total_level][1] = Plate[current_level][1] + record[i][0]
                            elif ((record[i][1] < long_edge - record[i][0]) and (Plate[current_level][4] == 1)):  # 新生成的第一块待填充芯板是竖直的，并且上一块待填充芯板是竖直的
                                Plate[total_level][3] = record[i][1]
                                Plate[total_level][2] = long_edge - record[i][0]
                                Plate[total_level][4] = 1
                                Plate[total_level][0] = Plate[current_level][0]
                                Plate[total_level][1] = Plate[current_level][1] + record[i][0]

                            if ((short_edge <= long_edge - record[i][0]) and (Plate[current_level][4] == 0)):  # 新生成的第二块可填充区域是横的，且上一块待填充区域也是横的（四种情况）
                                Plate[total_level + 1][4] = 0  # 旋转状态
                                Plate[total_level + 1][3] = short_edge  # 赋值可填充区域长度
                                Plate[total_level + 1][2] = long_edge - record[i][0]
                                Plate[total_level + 1][0] = Plate[current_level][0] + record[i][0]  # 赋值左下角坐标
                                Plate[total_level + 1][1] = Plate[current_level][1]
                            elif ((short_edge > long_edge - record[i][0]) and (Plate[current_level][4] == 0)):
                                Plate[total_level + 1][4] = 1
                                Plate[total_level + 1][3] = long_edge - record[i][0]
                                Plate[total_level + 1][2] = short_edge
                                Plate[total_level + 1][0] = Plate[current_level][0] + record[i][0]
                                Plate[total_level + 1][1] = Plate[current_level][1]
                            elif ((long_edge >= short_edge - record[i][1]) and (Plate[current_level][4] == 1)):
                                Plate[total_level + 1][4] = 1
                                Plate[total_level + 1][3] = short_edge - record[i][1]
                                Plate[total_level + 1][2] = long_edge
                                Plate[total_level + 1][0] = Plate[current_level][0] + record[i][1]
                                Plate[total_level + 1][1] = Plate[current_level][1]
                            elif ((long_edge < short_edge - record[i][1]) and (Plate[current_level][4] == 1)):
                                Plate[total_level + 1][4] = 0
                                Plate[total_level + 1][2] = short_edge - record[i][1]
                                Plate[total_level + 1][3] = long_edge
                                Plate[total_level + 1][0] = Plate[current_level][0] + record[i][1]
                                Plate[total_level + 1][1] = Plate[current_level][1]
                            total_level = total_level + 2
                            num.append(i)
                            break
            if spill:
                break
            current_level += 1
        return Plate, num
    def AP_id(self):  # 下料工位工单编号函数
        '''
        15090——15120
        :return:
        '''
        ERROR_ID=0
        try:
            record = []
            if (self.Is_Database_Connected()):
                prefix = 'PA'
                localtime = int(time.strftime('%Y%m%d', time.localtime()))  # 读一下本地时间，注意：若要对时间进行比较，则必须转换成int型
                cursor = self.db.cursor()
                cursor.execute("SELECT `Ap_id` FROM `work_package_task_list` WHERE 1  ORDER BY `Index` DESC  LIMIT 1" ) # 在工单编号数据库里，先按照index降序排列，后取第一行，也就是降序前的最后一行的数据
                ap_id = cursor.fetchone()  # record里存放的是工单编号数据库里最后一行的数据
                if ap_id==() or ap_id==None:
                    #first_code = '00001'
                    first_code = '1'
                    Ap_id = '%s%s%s' % (prefix, localtime, first_code)
                else:
                    ap_id_split=ap_id[0].split('A')
                    date_time=ap_id_split[-1][:8]
                    #code='1'+str(ap_id_split[-1][8:])
                    code=1+int(ap_id_split[-1][8:])
                    code=int(code)
                    if int(date_time)==localtime:
                        #Ap_id = '%s%s%s' % (prefix, localtime, str(eval('code+1')).lstrip( '1'))
                        Ap_id = '%s%s%s' % (prefix, localtime, str(code))
                    else:
                        #first_code = '00001'
                        first_code = '1'
                        Ap_id = '%s%s%s' % (prefix, localtime, first_code)
                self.db.close()
        except:
            ERROR_ID = 15090
            self.log.WriteText('天外天系统正在运行打包程序AP_id函数, 遇到错误  \r\n')
            return ERROR_ID,None
        return ERROR_ID,Ap_id

    def Post_Package_Select_Workorder(self,sec_id, plate1, Num_plies1, Total_plies, Ap_id,how_many_bags):
        '''
        错误代码15120——15130
        :param sec_id:
        :param plate1:
        :param Num_plies1:
        :param Total_plies:
        :param Ap_id:
        :param Box_type:
        :return:错误代码
        '''
        LONG=5
        SHORT=6
        ERROR_ID=0
        total_area=0
        package_infor=[]
        Contract_C_Time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        for i in range(len(plate1)):
            if plate1[i][LONG]!=0 and plate1[i][SHORT]!=0:
                total_area+=(plate1[i][LONG]*plate1[i][SHORT])
        for i in range(len(plate1)):
            connect='&'
            seq=(str(plate1[i][0]),str(plate1[i][1]),str(plate1[i][5]),str(plate1[i][6]),str(plate1[i][4]),str(plate1[i][10]))
            package_infor.append(connect.join(seq))
            if plate1[i][10] !='0' and plate1[i][10] !=0 :
                cursor = self.db.cursor()
                cursor.execute("SELECT `Index` FROM `order_element_online`WHERE `Part_id`='%s'" % plate1[i][10])
                index = cursor.fetchone()
                if index!=() and index!=None:
                    cursor.execute("UPDATE `order_element_online` SET `Package_work_order_ap_id`='%s',`Package_work_order_create_time`='%s' WHERE `Part_id`='%s' " % (Ap_id,Contract_C_Time,plate1[i][10]))
                cursor.execute("UPDATE `order_part_online` SET `Package_task_list_ap_id`='%s' WHERE `Part_id`='%s' " % ( Ap_id,  plate1[i][10]))
        self.db.commit()
        try:
            cursor = self.db.cursor()
            sql = "INSERT INTO `work_package_task_list` (`Create_Time`,`Order_id`,`Sec_id`,`State`,`Total_plies`,`Total_area`,`Ap_id`, `Long`, `Short`,`Num_plies1`,`Plies1_element_information1`, `Plies1_element_information2`,`Plies1_element_information3`, `Plies1_element_information4`, `Plies1_element_information5`, `Plies1_element_information6`, `Plies1_element_information7`, `Plies1_element_information8`, `Plies1_element_information9`, `Plies1_element_information10`,\
                    `Num_plies2`,`Plies2_element_information1`, `Plies2_element_information2`,`Plies2_element_information3`, `Plies2_element_information4`,`Plies2_element_information5`, `Plies2_element_information6`,`Plies2_element_information7`, `Plies2_element_information8`,`Plies2_element_information9`, `Plies2_element_information10`,\
                   `Num_plies3`,`Plies3_element_information1`, `Plies3_element_information2`,`Plies3_element_information3`, `Plies3_element_information4`,`Plies3_element_information5`, `Plies3_element_information6`,`Plies3_element_information7`, `Plies3_element_information8`,`Plies3_element_information9`, `Plies3_element_information10`,\
                    `Num_plies4`,`Plies4_element_information1`, `Plies4_element_information2`,`Plies4_element_information3`, `Plies4_element_information4`,`Plies4_element_information5`, `Plies4_element_information6`,`Plies4_element_information7`, `Plies4_element_information8`,`Plies4_element_information9`, `Plies4_element_information10`,\
                    `Num_plies5`,`Plies5_element_information1`, `Plies5_element_information2`,`Plies5_element_information3`, `Plies5_element_information4`,`Plies5_element_information5`, `Plies5_element_information6`,`Plies5_element_information7`, `Plies5_element_information8`,`Plies5_element_information9`, `Plies5_element_information10`,\
                    `Num_plies6`,`Plies6_element_information1`, `Plies6_element_information2`,`Plies6_element_information3`, `Plies6_element_information4`,`Plies6_element_information5`, `Plies6_element_information6`,`Plies6_element_information7`, `Plies6_element_information8`, `Plies6_element_information9`, `Plies6_element_information10`,`Package_num_now`) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % \
                  (Contract_C_Time,self.order_id,sec_id, '0', Total_plies, total_area,Ap_id,  plate1[0][2], plate1[0][3],Num_plies1[0],package_infor[0],package_infor[1],package_infor[2],package_infor[3],package_infor[4],package_infor[5],package_infor[6],package_infor[7],package_infor[8],package_infor[9],Num_plies1[1],package_infor[10],package_infor[11],package_infor[12],package_infor[13],package_infor[14],package_infor[15],package_infor[16],package_infor[17],package_infor[18],package_infor[19],
                   Num_plies1[2],package_infor[20],package_infor[21],package_infor[22],package_infor[23],package_infor[24],package_infor[25],package_infor[26],package_infor[27],package_infor[28],package_infor[29],Num_plies1[3],package_infor[30],package_infor[31],package_infor[32],package_infor[33],package_infor[34],package_infor[35],package_infor[36],package_infor[37],package_infor[38],package_infor[39],Num_plies1[4],package_infor[40],package_infor[41],package_infor[42],package_infor[43],package_infor[44],package_infor[45],package_infor[46],package_infor[47],package_infor[48],package_infor[49],Num_plies1[5],package_infor[50],package_infor[51],package_infor[52],package_infor[53],package_infor[54],package_infor[55],package_infor[56],package_infor[57],package_infor[58],package_infor[59],how_many_bags)

            cursor.execute(sql)
            self.db.commit()
            self.all_package_num+=1     #统计所要打的包数
        except:
            ERROR_ID= 15120
            self.log.WriteText('天外天系统正在运行打包程序Post_Package_Select_Workorder函数, 写打包工位工单数据库出现错误  \r\n')
            return ERROR_ID
        return ERROR_ID
    def Post_Package_Update_Package_State(self):
        '''
        错误代码从15130--15140
        一个组件的打包方案生成后，更新组件库及部件库的打包状态
        :return: 错误代码
        '''
        ERROR_ID=0
        try:
            cursor=self.db.cursor()
            cursor.execute("UPDATE `order_section_online` SET  `Package_state`=5  WHERE `Sec_id`='%s' " % (self.sec_id))  # 组件库打包状态置1，表示已经生成打包方案
            cursor.execute("UPDATE `order_part_online` SET  `Package_state`=5  WHERE `Sec_id`='%s' " % (self.sec_id))  # 在部件库里，把该组件的打包状态置1
            self.db.commit()

        except:
            ERROR_ID=15130
            self.log.WriteText('天外天系统正在运行打包程序Post_Package_Update_Package_State函数, 更新组件库或部件库时出现错误  \r\n')
            return ERROR_ID
        try:
            cursor.execute("SELECT `Package_state` FROM `order_section_online`  WHERE 1")
            package_state=cursor.fetchall()
            package_state= flatten(package_state)
            if len(package_state)==package_state.count(SECTION_PACKAGE_FINISH):
                cursor.execute("UPDATE `work_production_scheduling` SET  `State`='%s' ,`Schedule_of_package`='%s' WHERE `State`='%s' " % (SCHEDULE_PACKAGE_LAYOUT_FINISH,'今日总包数为'+str(self.all_package_num)+'包',SCHEDULE_LAYOUT_FINISH))
                self.db.commit()
                cursor.execute("SELECT `Order_id` FROM `order_order_online`  WHERE 1")
                orderid = cursor.fetchall()
                for i in range(len(orderid)):
                    cursor.execute("SELECT `Index` FROM `work_package_task_list`  WHERE `Order_id`='%s'" % orderid[i][0])
                    index = cursor.fetchall()
                    cursor.execute("UPDATE `order_order_online` SET  `Package_num`='%s'  WHERE `Order_id`='%s' " % (len(index),orderid[i][0]))
                    # cursor.execute("UPDATE `order_order_online` SET  `Package_num`='%s'  WHERE `Order_id`='%s' " % (len(index),orderid[i][0]))
                    self.db.commit()
            self.db.close()
        except:
            ERROR_ID = 15130
            self.log.WriteText('天外天系统正在运行打包程序Post_Package_Update_Package_State函数, 修改生产调度表单出现错误  \r\n')
            return ERROR_ID
        return ERROR_ID

    def Timer(self):
        if (self.isrunning ):
            self.isrunning=False

