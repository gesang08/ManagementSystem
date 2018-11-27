#!/usr/bin/env python
# _*_ coding: UTF-8 _*_
#ZX_MANAGEMENT20180920c:zx修改AUI,将门店管理界面和报错管理界面的权限设置加上。
#20180930b:zx修改权限管理设置，将排产界面只有陈璐的Job_id能登录查看。
#20181005a:zx将门店管理注释掉。
#20181006a:zx将门店管理恢复，将排产管理界面增加到权限设置中。
#20181006c:zx将属性页设置成不可拖拽。
#20181009a:zx将财务管理人员和质检人员的权限和密码设置好。
#20181010b:合入最新版zx和fyf的py
#20181023a:
#1、ZX合入ylp.py,在AUI中增加货运公司属性页，另外增加货运公司属性页的权限设置。
#20181024a:
#1、合入FYF.py，提高程序初始化运行时间的速度
#20181026b:
#1、zx修改aui.py，将发货管理登录密码增加。
#20181029a:
#1、zx合入scheduling.py，修改进散板的套系门型。
#20181031b:
#1、zx合入scheduling.py。
#2、zx合入ZX_Pane.py。
#20181101c:
#1、zx合入scheduling.py。
#2、zx在排产单查询界面详细生产工艺单中增加深度一列。
#20181101c:
#1、zx合入scheduling.py。修改进散板的套系门型，增加排产单状态为2的逻辑
#2、zx在排产单查询界面中增加整套组件信息
#20181116d:
#1.GQ:解决排产的bug:排产完成后，整套组件的长宽高未填写
#2.GQ:单独下五金件把手，排产完成后，需要把部件表单的状态修改为130，而不是25
#3.GQ:圆弧廊桥，双排廊桥,台面廊桥排产时会出现加载0条数据，不应该根据异型字段将其加到散板，应该根据element_type_id字段将其加到散板
#4.铝拐角，合叶，把手，拉直器的状态应为130,双排廊桥的状态与顶线一样，圆弧廊桥与台面廊桥暂时给的是组装工位的状态
import wx
import wx.html
import wx.grid
import os
import sys
import time
import re
from wx.lib.embeddedimage import PyEmbeddedImage
try:
    dirName = os.path.dirname(os.path.abspath(__file__))
except:
    dirName = os.path.dirname(os.path.abspath(sys.argv[0]))
sys.path.append(os.path.split(dirName)[0])
try:
    from agw import aui
    from agw.aui import aui_switcherdialog as ASD
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.aui as aui
    from wx.lib.agw.aui import aui_switcherdialog as ASD

import random
import images
from StatusBar import MyStatusBar
from ID_DEFINE import *
import MySQLdb
from MyLogCtrl import *
from ZX_Pane import *
from FYF_Pane import *
from scheduling import *
from YLP_Pane import *

ArtIDs = [ "wx.ART_ADD_BOOKMARK",
           "wx.ART_DEL_BOOKMARK",
           "wx.ART_HELP_SIDE_PANEL",
           "wx.ART_HELP_SETTINGS",
           "wx.ART_HELP_BOOK",
           "wx.ART_HELP_FOLDER",
           "wx.ART_HELP_PAGE",
           "wx.ART_GO_BACK",
           "wx.ART_GO_FORWARD",
           "wx.ART_GO_UP",
           "wx.ART_GO_DOWN",
           "wx.ART_GO_TO_PARENT",
           "wx.ART_GO_HOME",
           "wx.ART_FILE_OPEN",
           "wx.ART_PRINT",
           "wx.ART_HELP",
           "wx.ART_TIP",
           "wx.ART_REPORT_VIEW",
           "wx.ART_LIST_VIEW",
           "wx.ART_NEW_DIR",
           "wx.ART_HARDDISK",
           "wx.ART_FLOPPY",
           "wx.ART_CDROM",
           "wx.ART_REMOVABLE",
           "wx.ART_FOLDER",
           "wx.ART_FOLDER_OPEN",
           "wx.ART_GO_DIR_UP",
           "wx.ART_EXECUTABLE_FILE",
           "wx.ART_NORMAL_FILE",
           "wx.ART_TICK_MARK",
           "wx.ART_CROSS_MARK",
           "wx.ART_ERROR",
           "wx.ART_QUESTION",
           "wx.ART_WARNING",
           "wx.ART_INFORMATION",
           "wx.ART_MISSING_IMAGE",
           ]
# Custom pane button bitmaps
#----------------------------------------------------------------------
close = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAAA0AAAANCAYAAABy6+R8AAAABHNCSVQICAgIfAhkiAAAAh9J"
    b"REFUKJFl0s1LFGEAx/HvMzO7M9vmrrSuThJIhslmaSZqFgZLdSqKjr147VB/Qn9Af0GXTiIU"
    b"vVAQdRAKqkuColaiiyiKr7FKL7u6OzM78zxPh6igfvcvv8tHCMMEoHAxr/35AlpK/p0wTZz2"
    b"HLlXbwWABTBzrk83DnSRvjWE4Tj/Rcr3KU1/Zsav6GNvxoU1cSGvmwZ7SZ3Oo5MpIiuGrvl/"
    b"X+IOIgpJndmPNONM2Elt7KyuU9/djySCbBNGo4ssriA3FlHfNjAaXchkiSKf+u5+ykvLGHLP"
    b"XlQiSS0SqLoMosHF6DwJdfWIXC+iwUWls4TaQtkJQtPC8gIPo1pldvQlanGNnqs3iLktyOwB"
    b"TNMk9AMmnzzEmHjHiVOD7AQBVjUI0JUdDqaTzLwfZS6VovPSFUytQUrmXjynfO8uR9MWyrEJ"
    b"/QCrFkrU9leM5QVysoa044jSD9AAmoxjk6GKtbqNaukglAojCHyi8Q8Ec7PsO3sZt/UQ3uYG"
    b"3+cLeF82cdsOk719hyjlIis+Na0wlJRExSJe23EitwW5VWRqZJjHQ9eYGhlGbhWJmlvxOvqp"
    b"lXeRSmM57TnWSx4/ltZZsR5hOAlKz57St1tmbWSYscou0vNIfJwlyGRIHOlACMPkwUCPzsmQ"
    b"aswi8Hza/ICYgFDDgmMTd2ySkaRgxrg+NinEb3v3z+f15qdpQt/DQvwREaGJOQmau7q5+fqX"
    b"vZ+3DPNuDe9/tAAAAABJRU5ErkJggg==")
#----------------------------------------------------------------------
close_inactive = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAAA0AAAANCAYAAABy6+R8AAAABHNCSVQICAgIfAhkiAAAAh5J"
    b"REFUKJFl0stLVFEAgPHv3Htn7lzNGW1GZzSNtJI0fFZjQkQPqV0U0SJmnZugP6B9/0O4cZNE"
    b"ZFAQUdBrlZBYoJmGOYSPSUvRRp25r3NOi8iN3/7b/YQwTAAuDn7VM3kXqdiTaUBbS4w3Q+0C"
    b"QAjDpD83qfuPNdDZEicWMfZMbqCYzBcZmy0wNtIprIFb4/pUa4bzfXHiVRAxFWVP7w6OLQgk"
    b"NDTFsWOKyopxbSyubpPtShB6mroaQTolWFiQzM9LCsuadEpQWw1uSZHtSpBfKmLscySVFRpM"
    b"j+R+SaZWcLrXoDoBJ7shUydIJRVW1MeJaSwzxHLLJUqu4PnLaZYKity1Hg42RjhQb2CaAs/z"
    b"efjsM+/GDM6e6cErF7Hc8g5bO5rKqmZevJ8iXjXL1csdaC2QoeDpq1nu3S8SiXZgJxWe72NJ"
    b"6bO+rZhbNvDDdqKOZHMHtBYARJ0UrkyysGRyfEuhVIDhej4fpkO+5H2uXKqm5VCawi+fbz82"
    b"+fnb4+jhNHdvp8jUh7ihRMkAQ0rF6oaku73EwfqQlbWQ4dEJbt55xPDoBCtrIc2NIX3dZbbd"
    b"AK0k4lzugS5HT7C+vkG2tYxjmzx++4eiaiJuLHLjQoKSKxmfc0gma3D8iX8istdHtG+3YVHC"
    b"dX28yBEQEdABdvAd244iRQVRb4aPT3JC/Lc3kBvSn6YKlL0AYVi7IrQKcewIvR0NvB4ZFAB/"
    b"Aa4X7YpTOtu/AAAAAElFTkSuQmCC")
#----------------------------------------------------------------------
maximize = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAAA0AAAANCAYAAABy6+R8AAAABHNCSVQICAgIfAhkiAAAAJZJ"
    b"REFUKJG9kj0OwjAMRp8D6hDUExDmrr0dEkOHXgXuAMfIBl1yCwaMMAyoIJQWqUu/yZa/5x/J"
    b"Im7BVLnJBLDsg2vbPC3G8e51zapp5QeyGLHzBYbWtcfwJFlv8Nsdrqpypuu4HfY5hHPgPVKW"
    b"+STv3/XeOnrEH80HfW9SxVIaNFlKoJpDEgL30xGKIqdUkRA+qcz2Ri8+yyNzplbFQwAAAABJ"
    b"RU5ErkJggg==")
#----------------------------------------------------------------------
maximize_inactive = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAAA0AAAANCAYAAABy6+R8AAAABHNCSVQICAgIfAhkiAAAAJhJ"
    b"REFUKJFjZGRiZiAVMJGsg4GBgQXGaGz7+v/CxX84FRroMzHUV3Ezomi6cPEfw/Vb/xiYsbj2"
    b"718cNsnKMDJUlnAwqKthuvjmrX8MS1b8xtTEyMTAwMXFyMDLw4ihiYuLkYERySyyAoJ+muB+"
    b"+v2bgeHeA+xBfu/BP4bfiHBAaJKWYmTYsfsPAysrpqbfvyHyMMBIt2QEAFPtI359ud6yAAAA"
    b"AElFTkSuQmCC")
#----------------------------------------------------------------------
minimize = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAAA0AAAANCAYAAABy6+R8AAAABHNCSVQICAgIfAhkiAAAAMlJ"
    b"REFUKJGdkrsNwkAQRN/eWohPByYkQaIKSqAJhBAF0AdExGRUQwoioAREAth3S2BjWzLIwER7"
    b"oxntzOpEnPIrotcQ1lvjeIbbHXjkpAczkAf0OjAc4GZTQZwiTrHNzhoxX5g4xRU7U9+c654A"
    b"VEzY150qpuQLedY1qvFJCqrgX3ENQp5C7IMp9eAEQsjEIWQXVC3UpckSWK5gfwCRnKv0nIwL"
    b"vrLJQDzomytGEXRb5bOYLhfotyEeASk1xfUEcT+r9s83cs2SOp6D2FytkDyOCgAAAABJRU5E"
    b"rkJggg==")
#----------------------------------------------------------------------
minimize_inactive = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAAA0AAAANCAYAAABy6+R8AAAABHNCSVQICAgIfAhkiAAAANRJ"
    b"REFUKJGdkj1OgkEQhp/ZJSCF0VBYmUBPixfwAtzRS2DvCShMvAGRUJCQkMjOjwV8CwT1C77V"
    b"zGaevO9MViRlrlWnKd7el7HaKGpgpQDg7ng4rkY3Bw/3PZ4nI6lQzpnp0+BPh5fXDwBS8+DR"
    b"HquonUNEOxWHmaOTWSvk6sDJIRqZO0kEO8nrAUmEiN8gC8iCHyBvYqdU01RIizKbr1msy4/R"
    b"xo/9uvbRKYIIJewSSgIderWv0PZrRzcrw9tAVeulwvd7fC62DO5uAJD/fKPUPnKpbzVEY0DN"
    b"U2N1AAAAAElFTkSuQmCC")
#----------------------------------------------------------------------
restore = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAAA0AAAANCAYAAABy6+R8AAAABHNCSVQICAgIfAhkiAAAAUlJ"
    b"REFUKJGd0j9LW1EYBvDfvUkM1iaGkohaKJRQv0XJ5FCKg1PnoogUHCwOjnVTx67d2n6Cgq2O"
    b"7oXupdKhUIOQqMRSE733djiXNkoXPcvhvO/z530fThTFBTc9RUjfvM2020zeC5VS3i3kiBg/"
    b"ulQa4oXnUREcd9nZ5fAnvQ5nHaKEYkY14w4eNHm6+M9JfTwQHs5w2WdjHSkRBj2W5uge8Ghi"
    b"iBQl/O6RXDA9gUvWXnJ8xIdPYdQIpXiIVMJpm433tB4H0OcvLMwHxyzoSIeCUEB5QJywvUm/"
    b"T6vFk2dUavxC5Vp6RlDLya+3ODnBK4p3ebfC4D+RK2AM/TP29slSqjVerPJxJ/RG/6LzK00p"
    b"Y2UuqF7gHD2Mo5ELX3H62uZ+k85BWDbJF6/nIZUx1eR7d4hUnWR2mZn61eHztEQp344oN8Lz"
    b"Nn/vD5FAXWAC04u0AAAAAElFTkSuQmCC")
#----------------------------------------------------------------------
restore_inactive = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAAA0AAAANCAYAAABy6+R8AAAABHNCSVQICAgIfAhkiAAAAYxJ"
    b"REFUKJGdkr2PTGEUh5/z3ntndmYXIyODiI8oVyGRLTUitpToNCRCJdv7B2gkOrV6Q4hWp6JV"
    b"jXILhWKHeMfcmXvfj3MUk7jbcqrTPPk9J+cn4gr+dUqAz9OFzWth0CtJCiEaWUHNiMnIahQ0"
    b"TEYF16+OpARYto6v35SZj/gaZnNj2UIblZlX6lXg8thzf/dYl7RRFfyYK2fHjskI9m6XZIWs"
    b"4Gtj72VkerAk5SEADiBEWKwEVeHEphASvPoQefq65fRJAdaqmHVQG43vP5XdawX3blZcueh4"
    b"/qjPqeMQsxEUytKoSu30YjZmXlkFeP8p0URj+0LBrZ2KrYGjpiBlR1bpoDYYhz6Ts7H/MTJv"
    b"4O4NWIhj/03AZ0hBCNl1UMjCrxr80nj2oI8qbA2FJ28j774oMQnWGqpH/qQ5s2paHr6IbPSg"
    b"KoTWCYfZcMGhvqHQjGAd5Ehsn/FMD35Ti6NXClnWOiFCkRI7lxKD/pGbzk96PL4zJoUhhvyt"
    b"S7L1bmpUpXBusgmA/E/3/gASuMtl4Uj5YAAAAABJRU5ErkJggg==")
#----------------------------------------------------------------------
fullscreen = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAActJ"
    b"REFUOI2dk09I02EYx7/v+/7+DDRRYg4EWWYUKAjDSxBhJKuEUUJslwi8BXoaEaIdhpchddgt"
    b"CKIgCIbeYmXaTHboEigZ5GENdCCKfyZKTrf5+72Pp7nf9Lcf4gPP5fl+3i9feJ8HcKrghPD4"
    b"X9c5IdxJvHq4PFKvy3dOjKgltN4f71QU/lGo4kZD250/u5nZtB3H7IY9PRElW6f/ApgPAIiw"
    b"YZpax+rM8x2nNBeqSoLghMBkyIzFYptSSrcdzDnfCofDzd3db9X5+WdHAKAAQEt/9LKaz3zI"
    b"Ag+llG7f7UeQks4YLP787AaAnGdn2PsgupD9NvpVaeuLXmeGMkcwm8rg2tYe4tOLVY+D/i5L"
    b"EtYoQQlvIDqoEKgfoGbGmVEGHt/tQOBWe5WBrut4k05VTAQHA4b4ytTLVyAMSML/smgYBorF"
    b"YlUbxok/TEkmZ/zHfkHc5ACw/GX4E0B+q4GmaVVtNYBEPOPL39v4/iJ/Zg/O8wvWme0iIRLh"
    b"3t9osI6u7GI/lRozTqP2t7DUyVjJlWQlV46VXDl+5FpIX4Jmm8rWYDJkEmNPhSoKqqYUJKcn"
    b"64mxAzu05jHt/UtuN17rJSL6u5IYeV+LOwbQBrHjq9vsKwAAAABJRU5ErkJggg==")
#----------------------------------------------------------------------
reload = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAApFJ"
    b"REFUOI11k72LXFUUwH/n3vvmvbzZnZnNl7sWI0mIISaIIKYJ2AmbznQWKezSiOm0NaXpAjZu"
    b"kQTMHyBC0JBOCwmyWBrXHaMmuopLdt7Ox3vz3r33WMyyCJscOBwOnPPjfAovEFWEr2kBcIla"
    b"BH1enBxI/Golb7ZGb/kZb6vXkyCI4VeX8G3iFn+Qq1vTFwL0886pcqofNSXvgh41qEGEqBJR"
    b"tl3Gl2ZBbhy6ujs4ACjXuidiET7zDauuhRFnidky0gwxfkz0gq+JJuEbl9kPDn1YPAYwAHqT"
    b"VEfhmq9ZdS4aJBIWThNeuUQ4fpEgbbAGk3dMbMxqqMI1vUkK4AAa8vN+ppdj96ypj59DJv+g"
    b"+TJiFtDuq2iIUO1A1sM8/c7Epr48Nd0voFifAxpzAQ0rdPuEi5/M+6rHaLkDf3yPWzqLOAfT"
    b"f8G20KZeCT5cANaNKoJKX4RExluIr5B8CXp9aCrsbHvuJ2201SGaNiKaaJS+KmJE0KjRIwZm"
    b"BZTP5gvXiHRWiJ3+vFObQdqD7AiIQIxeBHUAorqh1lWiIWP3TyiHkPXgpdfg5Dv4jXvY0S9g"
    b"LGoyRGyFbzb2hxiCfWgdA2M5J5v3sVRodpQg78GRU5B2MX89BT9Bmm1i1MFM7cP9NXZmo83Q"
    b"hNvEokzKAdZaEuNxjx8gj+6RDB9h8iWME/DDMlbh9jFGm/sAuU7UkbsVxuM1KX+fGgokzUlS"
    b"S1o9wbUMRgvYHUxDsbsmtbsl14kHTvnZx0td0vqKW2y/b7vLZ6R9LAfQyfY0DLd+nhWTO9a3"
    b"7h7+dKd43i8I0Hp5kYUrr7vTbyzzZq8tJwB2xvrbj09Yv/uT3/x7zBiYwcEKBEiBfM/aPQUI"
    b"ewk1MPk/4D/OAyg6YvZkywAAAABJRU5ErkJggg==")
#----------------------------------------------------------------------
remove = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAApVJ"
    b"REFUOI2lkUtIVHEUxr//vf9778x4J8d8DDaODjo+mBzLKFJJJbVWFdmiVaEtehBYi2hVENXK"
    b"XS0iC6JNFkbkInwVQeoiiLAHtlAhW6TjTPnA9DreO/d/WjjOIkiDDnxwFuc7fOd3gP8s+bmD"
    b"118+UPGmiagsNL88UJqb62gLhTrP1tVdmY5G334zjOiGG574XF00/IjmHt6lO+mujvvb/J1L"
    b"3d1k9vRQk9fbsWkCX9ya/DIxUdVQ2+gt9Obt3lG1N6ykp+NGe/vnl5OT15aEiGx6x03g4GBl"
    b"IEGX2ojaLlBXeflKXWbm/n9i8BTILivgV4vkuXC0/x0W3n9C3tYMnsjOXpmyrMEfhmFutIC7"
    b"s3C9Jpw4vjAO3Ha6zS2Ki11cNZXz+fnnXkUiMbuy8l6OrreYpikxxgVRQmKMyaqa9mJo6PUH"
    b"PhTc6Q9gDvM1u1BxuFVxKRK+9/UhOjaOiCzL24uLHzcfOlLvcGoAGDRNgSxz9PcPnIrHf9Xy"
    b"r6FqHm85gXBFCNUeDwMAo7EB77uewdHxIBLI85c3HzsKp9MJxhgYYwCAmZmZwOjoWBp3EbJz"
    b"SoPQPR5YpglbCLhcaQgEg/Do6XsWF1elkZGPUFUVkiRB0zTouo7p6Rh03bOPBwKBUIbbDQAg"
    b"AIwxmKYJb1YWTp9pPckkSYrFfoKIUgKAkpIgDMO6xX0+n+R0OSGESJG1LAv5BX4UBQulRCIB"
    b"y7Jg2zaEsGHbAkQCmqZifn7JwYlk+vM1jDEIIWAYBoQQSbNIiYggxCqEYDZXFDVlWge03v9N"
    b"azMEzjm4qqp83STLUvJGAmMEYM1AxFLpkgggSYCiaDKPRhenenuHddNM0BokgMhODq+DQyo6"
    b"QLBtgiwzNju7svwbnlAlxKIQCyQAAAAASUVORK5CYII=")
#----------------------------------------------------------------------
sort = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAMdJ"
    b"REFUOI2VklEOgyAMhv+iR1jmdfQWHt1dQXA+dI9K97BpaIFE/4SQAv36UwC5BukAROxaOl7T"
    b"pPYdbmpZVxUrgMRNyLUkcZMqIIQ64IpCWMqAo6qdrbyfVdymAbmWLDAH+LKDq6oC0uql+FDw"
    b"uonnFWLcM8vONRkkLBWATSgBAeBt/gH9fp9WjLvY6t3zIZIiCZjnQFkTS8kA0PcDmBn8YTAz"
    b"hn7IHdSSD0lyLfqfOx3Y5FIPxnFUs3Jw9RUk7kLJerGJd/QF7eJxBTVIT38AAAAASUVORK5C"
    b"YII=")
#----------------------------------------------------------------------
superscript = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAYFJ"
    b"REFUOI3VkTtPAlEQhUfW4INCxMpigcTEVhMbCxO2NDZgg6UUJpSIzZZS+AO201gYaa1MbEy2"
    b"EAosbCQxxFdUsKLjIffOndl1sTBYiEFjYzzVmWTmy8wZgH+voZ82ru0+RfWpkeOJUV/04lpY"
    b"J+ZMDgDA91NAwD9s3T9Q4vyqZS3Mjm//Ytl3pfZr5Y2D52qvHu4Z0zQLrusCEQEzAxGllFKH"
    b"iAiICLZtGzGzkhPoQvUWE725jxMcx7GYeV4pFSOicj6fr0opC1LKKjOnlrYqCZ8G0bvHtsHk"
    b"BOfWL6MAn0JMp9OGUuqMmaHT6WSVUgnbtg0AgJWdm4I+PRZzX7vwIl9bR5szwT4AAEAymbQc"
    b"x8kIIYCIJovFYnNQJn1fIKKcEAI8z4N2u537LtQ+gJTyWAiRRUTodruZSCRiDAJoPROPx4O6"
    b"ru8hYqFUKlmBQGDS7/cvNpvNVU3TTomoPhAQDodPETEopVShUKgupUw1Go0aM9eZeRkAyp7n"
    b"fQn5W70BAIHMJSEYEtgAAAAASUVORK5CYII=")
#----------------------------------------------------------------------

# Custom pane bitmaps reference
#                      bitmap  button id       active  maximize
CUSTOM_PANE_BITMAPS = [(close, aui.AUI_BUTTON_CLOSE, True, False),
                       (close_inactive, aui.AUI_BUTTON_CLOSE, False, False),
                       (minimize, aui.AUI_BUTTON_MINIMIZE, True, False),
                       (minimize_inactive, aui.AUI_BUTTON_MINIMIZE, False, False),
                       (maximize, aui.AUI_BUTTON_MAXIMIZE_RESTORE, True, True),
                       (maximize_inactive, aui.AUI_BUTTON_MAXIMIZE_RESTORE, False, True),
                       (restore, aui.AUI_BUTTON_MAXIMIZE_RESTORE, True, False),
                       (restore_inactive, aui.AUI_BUTTON_MAXIMIZE_RESTORE, False, False)]
#----------------------------------------------------------------------
# Custom buttons in tab area
#
CUSTOM_TAB_BUTTONS = {"Left": [(sort, aui.AUI_BUTTON_CUSTOM1),
                               (superscript, aui.AUI_BUTTON_CUSTOM2)],
                      "Right": [(fullscreen, aui.AUI_BUTTON_CUSTOM3),
                                (remove, aui.AUI_BUTTON_CUSTOM4),
                                (reload, aui.AUI_BUTTON_CUSTOM5)]
                      }
#----------------------------------------------------------------------

# Define a translation function
_ = wx.GetTranslation
ID_Base = wx.ID_HIGHEST + 1
ID_CreateNotebook = ID_Base + 1
ID_ManagerAuthoritySetting = ID_Base + 2
ID_Settings = ID_Base + 3
ID_LogOut = ID_Base + 4
ID_LogIn = ID_Base + 5
ID_Productive_Moniter = ID_Base+6
ID_WechatLogin=ID_Base+7
ID_PasswordSetting = ID_Base + 8
ID_PageChange = ID_Base + 9
ID_Send_Wechat_Msg = ID_Base + 10
ID_Print_Bar_Code_Information = ID_Base + 11

def Is_Database_Connect():
    try:
        global DB
        DB = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[2], charset=charset)
        global DB1
        DB1 = MySQLdb.connect(host=server_ip, user=user_list[0], passwd=password, db=database[0], charset=charset)
        return True
    except:
        return False
class MyAuiFrame(wx.Frame):
    def __init__(self, parent, id=wx.ID_ANY, title="", pos= wx.DefaultPosition,
                 size=wx.DefaultSize, style = wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE, log=None):
        wx.Frame.__init__(self, parent, id, title, pos, size, style)
        self.login_state=0
        self.password=''
        self._mgr = aui.AuiManager()
        # tell AuiManager to manage this frame
        self._mgr.SetManagedWindow(self)
        # set frame icon
        self.SetIcon(images.Pencil.GetIcon())
        # set up default notebook style
        self._notebook_style = aui.AUI_NB_DEFAULT_STYLE | wx.NO_BORDER
        self._notebook_style &= ~(aui.AUI_NB_CLOSE_BUTTON |
                                  aui.AUI_NB_CLOSE_ON_ACTIVE_TAB |
                                  aui.AUI_NB_CLOSE_ON_ALL_TABS|
                                  aui.AUI_NB_TAB_MOVE|
                                  aui.AUI_NB_TAB_EXTERNAL_MOVE)

        self._notebook_theme = 5
        # Attributes
        self._textCount = 1
        self._transparency = 255
        self._snapped = False
        self._custom_pane_buttons = False
        self._custom_tab_buttons = False
        self._pane_icons = False
        self._veto_tree = self._veto_text = False
        self.staff_inform = {}
        self.staff_inform_name = {}
        # self.second=0
        if Is_Database_Connect():
            cursor = DB.cursor()
            cursor.execute("select `Job_id` ,`Password`,`Name` from `info_staff_new` where `Position`=25 ")
            record = cursor.fetchall()
            for i in range(len(record)):
                self.staff_inform[record[i][1]] = record[i][0]
                self.staff_inform_name[record[i][0]] = record[i][2]
        else:
            return
        self.log = log
        self.mb_login = wx.MenuBar()
        self.mb_logout = wx.MenuBar()

        self.statusbar = MyStatusBar(self)

        self.SetStatusBar(self.statusbar)
        # self.CreateStatusBar()
        # self.GetStatusBar().SetStatusText("Ready")
        self.BuildPanes()
        self.CreateMenuBar()
        self.BindEvents()
        # self.timer = wx.PyTimer(self.CloseTabTimer)
        # self.timer.Start(1000)
    def CreateMenuBar(self):
        # create menu
        file_menu = wx.Menu()
        file_menu.Append(ID_LogOut, "注销用户")
        file_menu.AppendSeparator()
        file_menu.Append(wx.ID_EXIT, "退出系统")
        file_menu_logout = wx.Menu()
        file_menu_logout.Append(ID_LogIn, "登录...")
        file_menu_logout.AppendSeparator()
        file_menu_logout.Append(wx.ID_EXIT, "退出系统")
        options_menu = wx.Menu()
        options_menu.Append(ID_ManagerAuthoritySetting, "管理员权限设置")
        options_menu.Append(ID_PasswordSetting, "密码设置")
        run_menu = wx.Menu()
        run_menu.Append(ID_Send_Wechat_Msg, "微信发布")
        run_menu.Append(ID_Print_Bar_Code_Information, "打印条形码")
        # run_menu.Append(ID_PasswordSetting, "密码设置")
        help_menu = wx.Menu()
        help_menu.Append(wx.ID_ABOUT, "关于天外天系统...")
        self.mb_login.Append(file_menu, "&F. 文件")
        self.mb_login.Append(options_menu, "&S. 参数设定")
        self.mb_login.Append(run_menu, "&R. 运行")
        self.mb_login.Append(help_menu, "&H. 帮助")
        self.mb_logout.Append(file_menu_logout, "&F. 文件")
        self.SetMenuBar(self.mb_logout)
    def BuildPanes(self):
        self.SetMinSize(wx.Size(400, 300))
        prepend_items, append_items = [], []
        item = aui.AuiToolBarItem()
        item.SetKind(wx.ITEM_SEPARATOR)
        append_items.append(item)
        item = aui.AuiToolBarItem()
        item.SetKind(wx.ITEM_NORMAL)
        item.SetId(ID_CustomizeToolbar)
        item.SetLabel("Customize...")
        append_items.append(item)
        tb_system = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                         wx.TB_FLAT | wx.TB_NODIVIDER)
        tb_system.SetToolBitmapSize(wx.Size(16,16))
        tb_system.AddTool(ID_LogIn, "Test", wx.ArtProvider.GetBitmap(wx.ART_FLOPPY, wx.ART_OTHER, wx.Size(16, 16)))
        tb_system.AddSeparator()
        tb_system.AddTool(wx.ID_EXIT, "Test", wx.ArtProvider.GetBitmap(wx.ART_QUIT, wx.ART_OTHER, wx.Size(16, 16)))
        tb_system.Realize()

        tb_fuctioin = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                         wx.TB_FLAT | wx.TB_NODIVIDER)
        tb_fuctioin.SetToolBitmapSize(wx.Size(16,16))
        tb_fuctioin.AddTool(ID_LogOut, "Test", wx.ArtProvider.GetBitmap(wx.ART_REDO, wx.ART_OTHER, wx.Size(16, 16)))
        tb_fuctioin.AddSeparator()
        tb_fuctioin.AddTool(wx.ID_EXIT, "Test", wx.ArtProvider.GetBitmap(wx.ART_QUIT, wx.ART_OTHER, wx.Size(16, 16)))
        tb_fuctioin.AddTool(wx.ID_ABOUT, "Test", wx.ArtProvider.GetBitmap(wx.ART_QUESTION, wx.ART_OTHER, wx.Size(16, 16)))
        tb_fuctioin.AddTool(ID_ManagerAuthoritySetting, "Test", wx.ArtProvider.GetBitmap(wx.ART_PASTE, wx.ART_OTHER, wx.Size(16, 16)))
        tb_fuctioin.AddTool(101, "Test", wx.ArtProvider.GetBitmap(wx.ART_PRINT, wx.ART_OTHER, wx.Size(16, 16)))
        tb_fuctioin.AddTool(101, "Test", wx.ArtProvider.GetBitmap(wx.ART_PLUS, wx.ART_OTHER, wx.Size(16, 16)))
        tb_fuctioin.AddSeparator()
        tb_fuctioin.AddTool(ID_WechatLogin, "Test", wx.ArtProvider.GetBitmap(wx.ART_REDO, wx.ART_OTHER, wx.Size(16, 16)))
        tb_fuctioin.AddTool(101, "Test", wx.ArtProvider.GetBitmap(wx.ART_QUIT, wx.ART_OTHER, wx.Size(16, 16)))
        tb_fuctioin.AddSeparator()
        tb_fuctioin.AddTool(101, "Test", wx.ArtProvider.GetBitmap(wx.ART_REMOVABLE, wx.ART_OTHER, wx.Size(16, 16)))
        tb_fuctioin.AddTool(101, "Test", wx.ArtProvider.GetBitmap(wx.ART_REPORT_VIEW, wx.ART_OTHER, wx.Size(16, 16)))
        tb_fuctioin.AddTool(101, "Test", wx.ArtProvider.GetBitmap(wx.ART_TICK_MARK, wx.ART_OTHER, wx.Size(16, 16)))
        tb_fuctioin.AddTool(101, "Test", wx.ArtProvider.GetBitmap(wx.ART_TIP, wx.ART_OTHER, wx.Size(16, 16)))
        tb_fuctioin.Realize()
        self.log=self.CreateTextCtrl()

        self._mgr.AddPane(self.log, aui.AuiPaneInfo().
                          Name("Ststem_log").Caption(u"系统日志").
                          Bottom().Layer(1).Position(1).MinimizeButton(False))

        wx.Log.SetActiveTarget(wx.Log())

        self._mgr.AddPane(self.CreateHTMLCtrl(), aui.AuiPaneInfo().Name("html_content").
                          CenterPane().Hide().MinimizeButton(True))
        self._mgr.AddPane(self.CreateNotebook(), aui.AuiPaneInfo().Name("notebook_content").
                          CenterPane().PaneBorder(False))
        # add the toolbars to the manager
        self._mgr.AddPane(tb_system, aui.AuiPaneInfo().Name("tb_system").Caption("Toolbar 2").
                          ToolbarPane().Top().Row(1))
        self._mgr.AddPane(tb_fuctioin, aui.AuiPaneInfo().Name("tb_fuctioin").Caption("Sample Bookmark Toolbar").
                          ToolbarPane().Top().Row(1))
        notebook = self._mgr.GetPane("notebook_content").window
        # self.gauge = wx.Gauge(notebook, size=(55, 15))
        # notebook.AddControlToPage(0, self.gauge)
        self._main_notebook = notebook
        perspective_all = self._mgr.SavePerspective()
        all_panes = self._mgr.GetAllPanes()
        for pane in all_panes:
            if not pane.IsToolbar():
                pane.Hide()
        self._mgr.GetPane("Ststem_log").Show()
        self._mgr.GetPane("notebook_content").Show()
        self.perspective_default = self._mgr.SavePerspective()
        self._mgr.GetPane("tb_system").Hide()
        self._mgr.GetPane("tb_fuctioin").Show()
        self.perspective_login=self._mgr.SavePerspective()
        self._mgr.GetPane("tb_fuctioin").Hide()
        self._mgr.GetPane("notebook_content").Hide()
        self._mgr.GetPane("tb_system").Show()
        self._mgr.GetPane("html_content").Show()
        self.perspective_logout=self._mgr.SavePerspective()
        self._perspectives = []
        self._perspectives.append(self.perspective_default)
        self._perspectives.append(perspective_all)
        self._perspectives.append(self.perspective_login)
        self._perspectives.append(self.perspective_logout)
        self._nb_perspectives = []
        auibook = self._mgr.GetPane("notebook_content").window
        nb_perspective_default = auibook.SavePerspective()
        self._nb_perspectives.append(nb_perspective_default)
        self._mgr.LoadPerspective(self.perspective_logout)
        toolbarPane = self._mgr.GetPane("tb_fuctioin")
        self._mgr.Update()
    def BindEvents(self):
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_MENU, self.OnManagerAuthoritySetting, id=ID_ManagerAuthoritySetting)
        self.Bind(wx.EVT_MENU, self.OnPasswordSetting, id=ID_PasswordSetting)
        # self.Bind(wx.EVT_MENU, self.OnSendWechatMsg, id=ID_Send_Wechat_Msg)
        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=wx.ID_ABOUT)
        self.Bind(wx.EVT_MENU, self.OnLogIn, id=ID_LogIn)
        self.Bind(wx.EVT_MENU, self.OnLogOut, id=ID_LogOut)
        self.Bind(wx.EVT_MENU, self.Print_Bar_Code, id=ID_Print_Bar_Code_Information)
        # self.Bind(wx.EVT_MENU, self.OnWechatLogin, id=ID_WechatLogin)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_TIMER, self.TimerHandlerMilliSecond)
        self.timer_MilliSecond = wx.Timer(self)
        self.timer_MilliSecond.Start(100)
        # self.timer_Second = wx.PyTimer(self.TimerHandlerSecond)
        # self.timer_Second.Start(1000)
    def __del__(self):

        self.timer.Stop()
    def TimerHandlerMilliSecond(self, event):
        try:
            self.gauge.Pulse()
        except:
            self.timer_MilliSecond.Stop()
    def OnClose(self, event):
        self.timer_MilliSecond.Stop()
        self._mgr.UnInit()
        event.Skip()
    def OnLogOut(self, event):
        # itchat.logout()
        self.statusbar.Name("未登录")
        t = time.localtime(time.time())
        st = time.strftime("%Y年%m月%d日 %H:%M:%S", t)
        try:
            self.log.WriteText(st+' 管理员退出登录\r\n')
        except:
            pass
        self.AllTimerStop()
        self.SetMenuBar(self.mb_logout)
        self._mgr.LoadPerspective(self.perspective_logout)
        self._mgr.Update()
        event.Skip()
    def OnLogIn(self, event):
        t = time.localtime(time.time())
        st = time.strftime("%Y年%m月%d日 %H:%M:%S", t)
        try:
            self.log.WriteText(st+' 有操作员尝试登录系统\r\n')
        except:
            pass
        dlg= wx.PasswordEntryDialog(self, '请输入系统管理员密码：','系统登录')
        dlg.SetValue("")
        if dlg.ShowModal() == wx.ID_OK:
            t = time.localtime(time.time())
            st = time.strftime("%Y年%m月%d日 %H:%M:%S", t)
            self.password=dlg.GetValue()
            if self.staff_inform.has_key(self.password)or self.password=="hello8031" or self.password=="zhijian123" or self.password=="caiwu123" or self.password=="12345678" or self.password=="fahuo123":
                # self.WeChatLogIn()
                try:
                    self.log.WriteText(st + ' 登录成功\r\n')
                except:
                    pass
                if self.password=="hello8031":
                    self.statusbar.Name("管理员" )
                    self.Operator_ID = '0'
                elif self.password == "zhijian123":  # 质检工位管理员
                    self.statusbar.Name("质检工位")
                    self.Operator_ID = '0'
                elif self.password == "caiwu123":
                    self.statusbar.Name("财务管理")
                    self.Operator_ID = '0'
                elif self.password == "12345678":
                    self.statusbar.Name("下单员")
                    self.Operator_ID = '0'
                elif self.password == "fahuo123":
                    self.statusbar.Name("下单员")
                    self.Operator_ID = '1817088'
                else:
                    staff_name = self.staff_inform_name[self.staff_inform[self.password]]
                    self.statusbar.Name(u"操作员："+staff_name)
                    self.Operator_ID = self.staff_inform[self.password]
                self.bord_storage_ctrl_panel.operator = self.statusbar.GetStatusText(3)
                self.board_hardware_storage_ctrl_panel.operator = self.statusbar.GetStatusText(3)
                self.board_attachment_storage_ctrl_panel.operator = self.statusbar.GetStatusText(3)
                self.fyf_progress_contract.timer.Start(30000)
                self.fyf_progress_id.timer.Start(10)
                self.zx_delivery_panel.GetOperatorId(self.Operator_ID)
                self.delivery_search_panel.GetOperatorId(self.Operator_ID)
                self.scheduling_panel.Get_Operator_Id(self.Operator_ID)
                self.store_pay_way_panel.Get_Manage_Password(self.staff_inform, self.staff_inform_name)
                self.scheduling_query_management_panel.zx_scheduling_query_middle_panel.scheduling_query_grid.GetOperatorId(self.Operator_ID)
                self.SetMenuBar(self.mb_login)
                self._mgr.LoadPerspective(self.perspective_login)
                self._mgr.Update()
                # if self.Operator_ID == '1825073':#陈璐的Job_id
                #     # self.SetAuthority()
                #     self.ctrl.EnableTab(1, True)
                # else:
                #     # self.SetAuthority()
                #     self.ctrl.EnableTab(1, False)
                self.SetAuthority()
            else:
                try:
                    self.log.WriteText(st + '  因密码错误，登录失败\r\n')
                    self.statusbar.Name("未登录")
                except:
                    pass
                ls=wx.MessageDialog(self, "密码错误！您无权登录系统，请联系管理员", "警告",
                                       wx.OK | wx.ICON_INFORMATION)
                ls.ShowModal()
                ls.Destroy()
                # self.log.WriteText('You entered: %s\n' % dlg.GetValue())
        dlg.Destroy()
        # self.ctrl.EnableTab(1,False)
        # self.ctrl.DeletePage(1)
        event.Skip()
    def Print_Bar_Code(self,event):
        dlg = Print_Dialog(self, -1, "提示：", size=(350, 200),
                           style=wx.DEFAULT_DIALOG_STYLE,
                           )
        dlg.CenterOnScreen()
        # this does not return until the dialog is closed.
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            # print 1
            self.paint_bar_code_panel = Print_Bar_Code_Panel(self, -1, "", self.log, '')
            self.paint_bar_code_panel.Show()
            self.paint_bar_code_panel.CenterOnScreen()
            # print 2
        else:
            self.log.WriteText("You pressed Cancel\n")
        dlg.Destroy()
    def OnManagerAuthoritySetting(self, event):
        Password_dlg =  wx.PasswordEntryDialog(self, '请输入系统管理员密码：','管理员权限设置登录')
        Password_dlg.SetValue("")
        if Password_dlg.ShowModal() == wx.ID_OK:
            self.password = Password_dlg.GetValue()
            if self.password == "hello8031":
                dlg = Authority__Dialog(self, -1, "操作员操作权限设定窗口", size=(800, 600), pos=wx.DefaultPosition,
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
                        refresh_inform = []
                        a = len(dlg.authority_ctrl_grid.data)
                        for i in range(a):
                            job_id = dlg.authority_ctrl_grid.table.GetValue(i, 0)
                            inform = [job_id, int(dlg.authority_ctrl_grid.table.GetValue(i, 3)),
                                      int(dlg.authority_ctrl_grid.table.GetValue(i, 4)),
                                      int(dlg.authority_ctrl_grid.table.GetValue(i, 5)),
                                      int(dlg.authority_ctrl_grid.table.GetValue(i, 6)),
                                      int(dlg.authority_ctrl_grid.table.GetValue(i, 7)),
                                      int(dlg.authority_ctrl_grid.table.GetValue(i, 8)),
                                      int(dlg.authority_ctrl_grid.table.GetValue(i, 9)),
                                      int(dlg.authority_ctrl_grid.table.GetValue(i, 10)),
                                      int(dlg.authority_ctrl_grid.table.GetValue(i, 11)),
                                      int(dlg.authority_ctrl_grid.table.GetValue(i, 12)),
                                      int(dlg.authority_ctrl_grid.table.GetValue(i, 13)),
                                      int(dlg.authority_ctrl_grid.table.GetValue(i, 14)),
                                      int(dlg.authority_ctrl_grid.table.GetValue(i, 15))]
                            refresh_inform.append(inform)
                            cursor = DB.cursor()
                            cursor.execute(
                                "UPDATE `info_staff_new` set `scheduling_management`='%s',`delivery_management`='%s',`workstation_management`='%s',`contract_order_management`='%s',`human_resource_management`='%s',`library_management`='%s',`workload_statistics_management`='%s',`sorting_car_display`='%s',`quality_testing`='%s',`store_management`='%s',`error_management`='%s',`finance_management`='%s',`transport_management`='%s' WHERE `Job_id`='%s' " % (
                                    refresh_inform[i][1], refresh_inform[i][2], refresh_inform[i][3],refresh_inform[i][4], refresh_inform[i][5],
                                     refresh_inform[i][6], refresh_inform[i][7], refresh_inform[i][8], refresh_inform[i][9], refresh_inform[i][10], refresh_inform[i][11], refresh_inform[i][12], refresh_inform[i][13],refresh_inform[i][0]))
                        DB.commit()
                    else:
                        pass
                    dlg1.Destroy()
                # elif val == 1000:
                dlg.Destroy()
            else:
                tip_dlg = wx.MessageDialog(self, '密码错误！您没有权限修改参数设置', '提示',
                                        wx.OK | wx.ICON_INFORMATION
                                        # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                                        )
                tip_dlg.ShowModal()
        Password_dlg.Destroy()
    def SetAuthority(self):
        page_count=self.ctrl.GetPageCount()
        if self.password=="hello8031":
            for i in range(page_count):
                self.ctrl.EnableTab(i,True)
        elif self.password=="caiwu123":
            for i in range(1,page_count):
                self.ctrl.EnableTab(i,False)
            self.ctrl.EnableTab(4, True)
            self.ctrl.EnableTab(6, True)
            self.ctrl.EnableTab(10, True)
            # self.ctrl.EnableTab(12, True)#由于没财务管理界面功能不完善
        elif self.password=="zhijian123":
            for i in range(1,page_count):
                self.ctrl.EnableTab(i,False)
            self.ctrl.EnableTab(4, True)
            self.ctrl.EnableTab(9, True)
        elif self.password == "12345678":
            for i in range(1,page_count):
                self.ctrl.EnableTab(i,False)
            self.ctrl.EnableTab(4, True)
            self.ctrl.EnableTab(10, True)
        elif self.password == "fahuo123":
            for i in range(1,page_count):
                self.ctrl.EnableTab(i,True)
            self.ctrl.EnableTab(1, False)
            self.ctrl.EnableTab(3, False)
            self.ctrl.EnableTab(5, False)
            self.ctrl.EnableTab(8, False)
            self.ctrl.EnableTab(12, False)
        else:
            try:
                if Is_Database_Connect():
                    cursor=DB.cursor()
                    cursor.execute("select `scheduling_management`,`delivery_management`,`workstation_management` ,`contract_order_management`,`human_resource_management`,`library_management` ,`workload_statistics_management`,`sorting_car_display`,`quality_testing`,`store_management`,`error_management`,`finance_management`,`transport_management` from `info_staff_new` where `Job_id`='%s' "%self.staff_inform[self.password])
                    record = cursor.fetchone()
                    for i in range(len(record)):
                        self.ctrl.EnableTab(i+1, bool(record[i]))
            except:
                self.log.WriteText("天外天系统正在运行MyFrame类中SetAuthority方法，读取数据库时出现错误，请进行检查管理员密码和Job_id是否为空或重复或者属性页是否全部启用\r\n")
    def OnPasswordSetting(self,event):
        Password_dlg = wx.PasswordEntryDialog(self, '请输入登录密码：', '密码修改设置')
        Password_dlg.SetValue("")
        if Password_dlg.ShowModal() == wx.ID_OK:
            self.password = Password_dlg.GetValue()
            if self.password == "hello8031":
                pass
            elif self.staff_inform.has_key(self.password):
                dlg=Change_Password_Dialog(self, -1, "设置密码窗口", self.staff_inform[self.password],size=(800, 600), pos=wx.DefaultPosition,style=wx.DEFAULT_DIALOG_STYLE)
                dlg.CenterOnScreen()
                dlg.ShowModal()
            else:
                tip_dlg = wx.MessageDialog(self, '密码错误！您没有权限修改参数设置', '提示',
                                           wx.OK | wx.ICON_INFORMATION
                                           # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                                           )
                tip_dlg.ShowModal()
        Password_dlg.Destroy()
    def TimerHandler(self, event):

        try:
            self.gauge.Pulse()
        except:
            self.timer.Stop()
    def OnEraseBackground(self, event):

        event.Skip()
    def OnSize(self, event):

        event.Skip()
    def OnCreateHTML(self, event):

        self._mgr.AddPane(self.CreateHTMLCtrl(), aui.AuiPaneInfo().
                          Caption("HTML Control").
                          Float().FloatingPosition(self.GetStartPosition()).
                          FloatingSize(wx.Size(300, 200)).MinimizeButton(True))
        self._mgr.Update()
    def OnCreateNotebook(self, event):

        self._mgr.AddPane(self.CreateNotebook(), aui.AuiPaneInfo().
                          Caption("Notebook").
                          Float().FloatingPosition(self.GetStartPosition()).
                          CloseButton(True).MaximizeButton(True).MinimizeButton(True))
        self._mgr.Update()
    def OnCreateText(self, event):

        self._mgr.AddPane(self.CreateTextCtrl(), aui.AuiPaneInfo().
                          Caption("Text Control").
                          Float().FloatingPosition(self.GetStartPosition()).
                          MinimizeButton(True))
        self._mgr.Update()
    def OnExit(self, event):
        self.Close(True)
    def OnAbout(self, event):
        msg = "    Copyright 2017-2020, 天津定智科技有限公司\n" + \
              "                                             \n"+\
              "              天外天定制家居智能生产管理系统\n" + \
              "                                             \n"+\
              "                        Version 0.181126B"
        dlg = wx.MessageDialog(self, msg, "天津定智科技有限公司",
                               wx.OK | wx.ICON_INFORMATION)
        if wx.Platform != '__WXMAC__':
            dlg.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL,
                                False, '', wx.FONTENCODING_DEFAULT))
        dlg.ShowModal()
        dlg.Destroy()
    def CreateTextCtrl(self, ctrl_text=""):
        if ctrl_text.strip():
            text = ctrl_text
        else:
            text = ""
        return MyTextCtrl(self,-1, text, wx.Point(0, 0), wx.Size(150, 100),
                           wx.NO_BORDER | wx.TE_MULTILINE)
    def CreateHTMLCtrl(self, parent=None):
        if not parent:
            parent = self
        ctrl = wx.html.HtmlWindow(parent, -1, wx.DefaultPosition, wx.Size(400, 300))
        ctrl.SetPage(GetIntroText())
        return ctrl
    def CreateNotebook(self):
        # create the notebook off-window to avoid flicker
        client_size = self.GetClientSize()
        self.ctrl = aui.AuiNotebook(self, -1, wx.Point(client_size.x, client_size.y),
                              wx.Size(430, 200), agwStyle=self._notebook_style)
        self.ctrl.Bind(aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        arts = [aui.AuiDefaultTabArt, aui.AuiSimpleTabArt, aui.VC71TabArt, aui.FF2TabArt,
                aui.VC8TabArt, aui.ChromeTabArt]

        art = arts[self._notebook_theme]()
        self.ctrl.SetArtProvider(art)

        page_bmp = wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, wx.Size(16, 16))
        page_bmp1 = wx.ArtProvider.GetBitmap(wx.ART_ADD_BOOKMARK, wx.ART_OTHER, wx.Size(16, 16))
        page_bmp2 = wx.ArtProvider.GetBitmap(wx.ART_CDROM, wx.ART_OTHER, wx.Size(16, 16))
        page_bmp3 = wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_OTHER, wx.Size(16, 16))
        page_bmp4 = wx.ArtProvider.GetBitmap(wx.ART_CLOSE, wx.ART_OTHER, wx.Size(16, 16))

        self.schedule_monitor=aui.AuiNotebook(self, -1, wx.Point(client_size.x, client_size.y),
                              wx.Size(430, 200), agwStyle=self._notebook_style|aui.AUI_NB_BOTTOM)

        self.fyf_progress_id = Progress_Manage_Panel_ID(self.ctrl, self.log)
        self.FYF_Progress_Manage_Panel = Progress_Manage_Panel_Part(self.ctrl, self.log)
        self.fyf_progress_sec = Progress_Manage_Panel_Sec(self.ctrl, self.log)
        self.fyf_progress_order = Progress_Manage_Panel_Order(self.ctrl, self.log)
        self.fyf_progress_contract=Progress_Manage_Panel_Contract(self.ctrl,self.log)
        self.schedule_monitor.AddPage(self.fyf_progress_contract, "合同生产进度管理", False, page_bmp2)
        self.schedule_monitor.AddPage(self.fyf_progress_order, "订单生产进度管理", False, page_bmp2)
        self.schedule_monitor.AddPage(self.fyf_progress_sec, "组件生产进度管理", False, page_bmp2)
        self.schedule_monitor.AddPage(self.FYF_Progress_Manage_Panel, "部件生产进度管理", False, page_bmp2)
        self.schedule_monitor.AddPage(self.fyf_progress_id, "零件生产进度管理", False, page_bmp2)
        self.ctrl.AddPage(self.schedule_monitor, "生产进度管理", True, page_bmp)

        self.scheduling = aui.AuiNotebook(self, -1, wx.Point(client_size.x, client_size.y),
                                          wx.Size(430, 200), agwStyle=self._notebook_style | aui.AUI_NB_BOTTOM)
        self.scheduling_panel = Scheduling_Panel(self, self.log)
        self.scheduling.AddPage(self.scheduling_panel, "排产管理", False, page_bmp2)
        self.scheduling_query_management_panel = Scheduling_Query_Management_Panel(self, self.log)
        self.scheduling.AddPage(self.scheduling_query_management_panel, "排产计划查询", False, page_bmp2)
        self.ctrl.AddPage(self.scheduling, "排产管理", False, page_bmp)

        self.delivery=aui.AuiNotebook(self, -1, wx.Point(client_size.x, client_size.y),
                              wx.Size(430, 200), agwStyle=self._notebook_style|aui.AUI_NB_BOTTOM)
        # self.delivery
        self.zx_delivery_panel=ZX_Delivery_Panel(self.ctrl, self.log)
        self.delivery.AddPage(self.zx_delivery_panel, "发货控制",False, page_bmp2)
        self.delivery_search_panel=Delivery_Search_Panel(self.ctrl,self.log)
        self.delivery.AddPage(self.delivery_search_panel, "发货单查询及管理",False, page_bmp2)
        # self.transport_company_management=Transport_Company_Management_Panel(self.ctrl,self.log)
        # self.delivery.AddPage(self.transport_company_management,"货运公司管理",False,page_bmp2)
        self.ctrl.AddPage(self.delivery, "发货管理",False, page_bmp1)

        self.workposition=aui.AuiNotebook(self, -1, wx.Point(client_size.x, client_size.y),
                              wx.Size(430, 200), agwStyle=self._notebook_style|aui.AUI_NB_BOTTOM)
        self.cnc_workposition_management=Cnc_Workposition_Management_Panel(self.ctrl,self.log)
        self.pvc_workposition_management=Pvc_Workposition_Managemnet_Panel(self.ctrl,self.log)
        self.workposition.AddPage(self.cnc_workposition_management, "加工中心工位",False, page_bmp2)
        self.workposition.AddPage(self.pvc_workposition_management, "模压吸塑工位",False, page_bmp2)
        self.ctrl.AddPage(self.workposition, "工位管理",False, page_bmp2)


        self.contract_order_management_panel=aui.AuiNotebook(self, -1, wx.Point(client_size.x, client_size.y),
                              wx.Size(430, 200), agwStyle=self._notebook_style|aui.AUI_NB_BOTTOM)
        self.ylp_fold_panel_bar = YLP_Contract_Order_Management_Panel(self.ctrl, self.log, self.fyf_progress_order,
                                                                      self.fyf_progress_sec, self.FYF_Progress_Manage_Panel,
                                                                      self.fyf_progress_id, self.schedule_monitor)
        self.ylp_fold_panel = YLP_Contract_Order_Complete_Management_Panel(self.ctrl, self.log)

        # self.offline_contract_order_management_panel=YLP_Contract_Order_Management_Panel(self.ctrl,self.log,FYF_Progress_Manage_Panel)
        # self.waiting_contract_order_management_panel=Waiting_Contract_Management_Panel(self.ctrl,self.log,FYF_Progress_Manage_Panel)
        self.contract_order_management_panel.AddPage(self.ylp_fold_panel_bar,"在产合同订单管理")
        self.contract_order_management_panel.AddPage(self.ylp_fold_panel,"已完工合同订单管理")
        # self.contract_order_management_panel.AddPage(self.waiting_contract_order_management_panel,"待产合同订单管理")
        self.ctrl.AddPage(self.contract_order_management_panel, "合同订单管理",False, page_bmp3,tooltip="查询及管理公司的合同订单")


        self.HR_panel = aui.AuiNotebook(self, -1, wx.Point(client_size.x, client_size.y),
                                                               wx.Size(430, 200),
                                                               agwStyle=self._notebook_style | aui.AUI_NB_BOTTOM)
        self.ylp_staff_inform = YLP_Staff_Inform_Management_Panel(self.ctrl, self.log)
        self.HR_panel.AddPage(self.ylp_staff_inform, "员工信息查询")
        self.ctrl.AddPage(self.HR_panel, "人力资源管理", False, page_bmp2)

        self.storage_panel=aui.AuiNotebook(self, -1, wx.Point(client_size.x, client_size.y),
                              wx.Size(430, 200), agwStyle=self._notebook_style|aui.AUI_NB_BOTTOM)
        self.product_storage_ctrl_panel=Product_Storage_Ctrl_Panel(self.ctrl,self.log)
        self.storage_panel.AddPage(self.product_storage_ctrl_panel, "成品库管理",False, page_bmp1)
        self.bord_storage_ctrl_panel=Board_Storage_Manage_Ctrl_Panel(self.ctrl,self.log)
        self.storage_panel.AddPage(self.bord_storage_ctrl_panel, "板材库管理",False, page_bmp2)
        self.board_hardware_storage_ctrl_panel = Board_Hardware_Store_Ctrl_Panel(self.ctrl, self.log)
        self.storage_panel.AddPage(self.board_hardware_storage_ctrl_panel, "五金件库管理", False, page_bmp2)
        self.board_attachment_storage_ctrl_panel = Board_Attachment_library_Ctrl_Panel(self.ctrl, self.log)
        self.storage_panel.AddPage(self.board_attachment_storage_ctrl_panel, "附件库管理", False, page_bmp2)
        # self.pvc_storage_ctrl_panel=PVC_Storage_Ctrl_Panel(self.ctrl,self.log)
        # self.storage_panel.AddPage(self.pvc_storage_ctrl_panel, "PVC库管理",False, page_bmp3)
        # self.attachment_storage_ctrl_panel=UltimateListCtrlPanel(self.ctrl,self.log)
        # self.storage_panel.AddPage(self.attachment_storage_ctrl_panel, "附件库管理",False, page_bmp4)

        self.ctrl.AddPage(self.storage_panel, "库管理",False, page_bmp4,tooltip="查询/管理公司的成品及原材料库房")
        # self.workload_count_panel = aui.AuiNotebook(self, -1, wx.Point(client_size.x, client_size.y),
        #                                             wx.Size(430, 200),
        #                                             agwStyle=self._notebook_style | aui.AUI_NB_BOTTOM)
        # # self.product_storage_ctrl_panel=Product_Storage_Ctrl_Panel(self.ctrl,self.log)
        # # self.workload_count_panel.AddPage(self.product_storage_ctrl_panel, "按日统计",False, page_bmp1)
        # # self.bord_storage_ctrl_panel=Board_Storage_Ctrl_Panel(self.ctrl,self.log)
        # # self.workload_count_panel.AddPage(self.bord_storage_ctrl_panel, "按月统计",False, page_bmp2)
        # # self.attachment_storage_ctrl_panel=UltimateListCtrlPanel(self.ctrl,self.log)
        # # self.storage_panel.AddPage(self.attachment_storage_ctrl_panel, "附件库管理",False, page_bmp4)
        # staff_workload_statistics_day = Staff_Workload_Statistics_Day(self.ctrl, self.log)
        # self.workload_count_panel.AddPage(staff_workload_statistics_day, "员工日工作量统计", False, page_bmp2)
        # self.ctrl.AddPage(self.workload_count_panel, "员工工作量统计", False, page_bmp4, tooltip="统计/查询公司员工实际工作量")
        self.workload_count_panel = aui.AuiNotebook(self, -1, wx.Point(client_size.x, client_size.y),
                                                    wx.Size(430, 200),
                                                    agwStyle=self._notebook_style | aui.AUI_NB_BOTTOM)
        self.staff_workload_statistics_day = Staff_Workload_Statistics_Day(self.ctrl, self.log)
        self.staff_workload_statistics_month = Staff_Workload_Statistics_Month(self.ctrl, self.log)
        self.workload_count_panel.AddPage(self.staff_workload_statistics_day, "员工日工作量统计", False, page_bmp2)
        self.workload_count_panel.AddPage(self.staff_workload_statistics_month, "员工月工作量统计", False, page_bmp2)
        self.ctrl.AddPage(self.workload_count_panel, "员工工作量统计", False, page_bmp4, tooltip="统计/查询公司员工实际工作量")

        self.led_vehicle_ctrl_panel = aui.AuiNotebook(self, -1, wx.Point(client_size.x, client_size.y),
                                                    wx.Size(430, 200),
                                                    agwStyle=self._notebook_style | aui.AUI_NB_BOTTOM)
        # self.product_storage_ctrl_panel=Product_Storage_Ctrl_Panel(self.ctrl,self.log)
        # self.workload_count_panel.AddPage(self.product_storage_ctrl_panel, "按日统计",False, page_bmp1)
        # self.bord_storage_ctrl_panel=Board_Storage_Ctrl_Panel(self.ctrl,self.log)
        # self.workload_count_panel.AddPage(self.bord_storage_ctrl_panel, "按月统计",False, page_bmp2)
        # self.attachment_storage_ctrl_panel=UltimateListCtrlPanel(self.ctrl,self.log)
        # self.storage_panel.AddPage(self.attachment_storage_ctrl_panel, "附件库管理",False, page_bmp4)
        # staff_workload_statistics_day = Staff_Workload_Statistics_Day(self.ctrl, self.log)
        # self.workload_count_panel.AddPage(staff_workload_statistics_day, "员工日工作量统计", False, page_bmp2)
        self.Sorting_Vehicle_Panel=Sorting_Vehicle_Management_Panel(self.ctrl, self.log)
        self.led_vehicle_ctrl_panel.AddPage(self.Sorting_Vehicle_Panel,"循环读小车测试",False,page_bmp2)
        self.ctrl.AddPage(self.led_vehicle_ctrl_panel, "分拣小车管理", False, page_bmp4, tooltip="管理分拣小车并监控分拣小车运行状态")

        self.Quality_inspection_station = aui.AuiNotebook(self, -1, wx.Point(client_size.x, client_size.y),
                                                          wx.Size(430, 200),
                                                          agwStyle=self._notebook_style | aui.AUI_NB_BOTTOM)
        self.Part_inquiry = Progress_Manage_Panel_Part_query(self.ctrl, self.log)
        self.Part_Quality_inspection = Progress_Manage_Panel_Part_Quality_inspection(self.ctrl, self.log)
        self.Quality_inspection_station.AddPage(self.Part_inquiry, "部件查询", False, page_bmp2)
        self.Quality_inspection_station.AddPage(self.Part_Quality_inspection, "部件质检", False, page_bmp2)
        self.ctrl.AddPage(self.Quality_inspection_station, "质检工位", False, page_bmp4, tooltip="查询/管理部件质检")

        gq_store_management = aui.AuiNotebook(self, -1, wx.Point(client_size.x, client_size.y),
                                              wx.Size(430, 200), agwStyle=self._notebook_style | aui.AUI_NB_BOTTOM)
        self.gq_store_brand_panel = Store_Brand_Management(self, self.log)
        gq_store_management.AddPage(self.gq_store_brand_panel, "门店品牌管理", False, page_bmp2)
        self.store_door_panel = Store_Door_Management(self, self.log)
        gq_store_management.AddPage(self.store_door_panel, "门店门型管理", False, page_bmp2)
        self.brand_door_panel = Brand_Door_Management(self, self.log)
        gq_store_management.AddPage(self.brand_door_panel, "品牌门型管理", False, page_bmp2)
        self.store_pay_way_panel = Store_Pay_Way_Management(self, self.log)
        gq_store_management.AddPage(self.store_pay_way_panel, "门店支付管理", False, page_bmp2)
        self.ctrl.AddPage(gq_store_management, "门店管理", False, page_bmp)

        self.ERROR_panel = aui.AuiNotebook(self, -1, wx.Point(client_size.x, client_size.y),
                                                               wx.Size(430, 200),
                                                               agwStyle=self._notebook_style | aui.AUI_NB_BOTTOM)
        self.ylp_now_element_scrap = YLP_Now_Element_Scrap_Panel(self.ctrl, self.log)
        self.ylp_history_element_scrap = YLP_History_Element_Scrap_Panel(self.ctrl, self.log)
        self.ERROR_panel.AddPage(self.ylp_now_element_scrap, "当前报错信息")
        self.ERROR_panel.AddPage(self.ylp_history_element_scrap, "历史报错信息")
        self.ctrl.AddPage(self.ERROR_panel, "报错显示", False, page_bmp2)

        self.finance_panel = aui.AuiNotebook(self, -1, wx.Point(client_size.x, client_size.y),
                                             wx.Size(430, 200),
                                             agwStyle=self._notebook_style | aui.AUI_NB_BOTTOM)
        self.ylp_finance_management = YLP_Finance_Management_Panel(self.ctrl, self.log)
        self.finance_panel.AddPage(self.ylp_finance_management, "收入查询")
        self.ctrl.AddPage(self.finance_panel, "财务管理", False, page_bmp2)
        #---------------------------新增ylp物流管理panel
        self.transport_panel = aui.AuiNotebook(self, -1, wx.Point(client_size.x, client_size.y),
                                               wx.Size(430, 200),
                                               agwStyle=self._notebook_style | aui.AUI_NB_BOTTOM)
        self.ylp_transport_company_management_panel = YLP_Transport_Company_Management_Panel(self.ctrl, self.log)
        self.ylp_dealer_transport_company_management_panel = YLP_Dealer_Transport_Company_Management_Panel(self.ctrl,
                                                                                                           self.log)
        self.transport_panel.AddPage(self.ylp_transport_company_management_panel, "货运公司管理")
        self.transport_panel.AddPage(self.ylp_dealer_transport_company_management_panel, "经销商与货运公司管理")
        self.ctrl.AddPage(self.transport_panel, "物流管理", False, page_bmp2)
        self.AllTimerStop()
        # self.ctrl.GetTabContainer()
        # self.ctrl.SetSelection(3)
        # self.ctrl.GetSelection()
        # Demonstrate how to disable a tab
        # self.ctrl.EnableTab(1, False)
        # self.ctrl.SetCloseButton(0,False)
        # self.ctrl.SetPageTextColour(2, wx.RED)
        # self.ctrl.SetPageTextColour(3, wx.BLUE)
        # self.ctrl.SetRenamable(2, True)
        self.schedule_monitor.Bind(aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.Progress_Manage_Page_changed)
        self.Quality_inspection_station.Bind(aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.Quality_inspection_changed)
        self.delivery.Bind(aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.Delivery_Page_Changed)
        self.scheduling.Bind(aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.Scheduling_Page_Changed)
        # self.fyf_progress_contract.timer.Start()
        self.workload_count_panel.Bind(aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.workload_count_changed)
        self.storage_panel.Bind(aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.storage_panel_changed)
        return self.ctrl
    def Progress_Manage_Page_changed(self, event):
        self.fyf_progress_contract.timer.Stop()
        self.fyf_progress_order.timer.Stop()
        self.fyf_progress_sec.timer.Stop()
        self.FYF_Progress_Manage_Panel.timer.Stop()
        if self.schedule_monitor.GetSelection() == 0:
            self.fyf_progress_contract.timer.Start(30000)
            self.fyf_progress_contract.Contract_refresh()
        elif self.schedule_monitor.GetSelection() == 1:
            self.fyf_progress_order.timer.Start(30000)
            self.fyf_progress_order.Order_refresh()
        elif self.schedule_monitor.GetSelection() == 2:
            self.fyf_progress_sec.timer.Start(30000)
            self.fyf_progress_sec.Sec_refresh()
        elif self.schedule_monitor.GetSelection() == 3:
            self.FYF_Progress_Manage_Panel.timer.Start(30000)
            self.FYF_Progress_Manage_Panel.Part_refresh()
        elif self.schedule_monitor.GetSelection() == 4:
            self.fyf_progress_id.Id_refresh()
    def Quality_inspection_changed(self, event):
        self.Part_Quality_inspection.timer.Stop()
        if self.Quality_inspection_station.GetSelection() == 0:
            self.Part_inquiry.Part_refresh()
        elif self.Quality_inspection_station.GetSelection() == 1:
            self.Part_Quality_inspection.timer.Start(100)
            self.Part_Quality_inspection.Quality_inspection_refresh()
    def workload_count_changed(self, event):
        self.staff_workload_statistics_day.timer.Stop()
        self.staff_workload_statistics_month.timer.Stop()
        if self.workload_count_panel.GetSelection() == 0:
            self.staff_workload_statistics_day.timer.Start(30000)
            self.staff_workload_statistics_day.Day_refresh()
        elif self.workload_count_panel.GetSelection() == 1:
            self.staff_workload_statistics_month.timer.Start(30000)
            self.staff_workload_statistics_month.Day_refresh()
    def Delivery_Page_Changed(self,event):
        self.zx_delivery_panel.timer.Stop()
        self.delivery_search_panel.remainingSpace.query_managment_grid.timer.Stop()
        sel = self.delivery.GetSelection()
        if sel == 0:
            self.zx_delivery_panel.timer.Start()
            self.zx_delivery_panel.TimeRefresh()
        elif sel == 1:
            self.delivery_search_panel.remainingSpace.query_managment_grid.timer.Start(30000)
            self.delivery_search_panel.remainingSpace.query_managment_grid.MyRefresh()
    def Scheduling_Page_Changed(self,event):
        self.scheduling_panel.timer.Stop()
        # self.scheduling_query_management_panel.timer.Stop()
        if self.scheduling.GetSelection() == 0:
            self.scheduling_panel.timer.Start(1000)
        # elif self.scheduling.GetSelection() == 1:
            # self.scheduling_query_management_panel.timer.Start(5000)
    def storage_panel_changed(self,event):
        self.product_storage_ctrl_panel.timer.Stop()
        self.bord_storage_ctrl_panel.timer.Stop()
        if self.storage_panel.GetSelection() == 0:
            self.product_storage_ctrl_panel.timer.Start(5000)
            self.product_storage_ctrl_panel.MyRefresh()
        if self.storage_panel.GetSelection() == 1:
            self.bord_storage_ctrl_panel.timer.Start(30000)
            self.bord_storage_ctrl_panel.board_storage_refresh()
        if self.storage_panel.GetSelection() == 2:
            self.board_hardware_storage_ctrl_panel.Part_refresh()
        if self.storage_panel.GetSelection() == 3:
            self.board_attachment_storage_ctrl_panel.Part_refresh()
    def AllTimerStop(self):
        self.fyf_progress_contract.timer.Stop()
        self.fyf_progress_order.timer.Stop()
        self.fyf_progress_sec.timer.Stop()
        self.FYF_Progress_Manage_Panel.timer.Stop()
        self.fyf_progress_id.timer.Stop()
        self.staff_workload_statistics_day.timer.Stop()
        self.staff_workload_statistics_month.timer.Stop()
        self.Part_Quality_inspection.timer.Stop()
        self.scheduling_panel.timer.Stop()
        self.zx_delivery_panel.timer.Stop()
        self.delivery_search_panel.remainingSpace.query_managment_grid.timer.Stop()
        self.cnc_workposition_management.remainingSpace.pvc_workposition_right_show1.timer.Stop()
        # self.scheduling_query_management_panel.timer.Stop()
        self.delivery_search_panel.remainingSpace.query_managment_grid.timer.Stop()
        self.product_storage_ctrl_panel.timer.Stop()
        self.bord_storage_ctrl_panel.timer.Stop()
        self.ylp_now_element_scrap.Element_Scrap_Grid.timer.Stop()
        self.Sorting_Vehicle_Panel.remainingSpace.timer.Stop()
    def WeChatLogIn(self):
        if Is_Database_Connect():
            if self.password=="hello8031":
                itchat.auto_login(hotReload=True)
                message = "您的微信登录成功，可以在排产单查询界面给各工位发布排产任务消息，祝工作愉快！"
                dlg = wx.MessageDialog(self, message, "微信登录窗口", wx.OK | wx.ICON_INFORMATION
                                       # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                                       )
                dlg.ShowModal()
                dlg.Destroy()
            else:
                cursor = DB.cursor()
                cursor.execute(
                    "SELECT `scheduling_management` from `info_staff_new` WHERE `Job_id`='%s'" % (self.staff_inform[self.password] ))
                record = cursor.fetchone()
                if record[0]==1:
                    itchat.auto_login(hotReload=True)
                    message = "您的微信登录成功，可以在排产单查询界面给各工位发布排产任务消息，祝工作愉快！"
                    dlg = wx.MessageDialog(self, message, "微信登录窗口", wx.OK | wx.ICON_INFORMATION
                                           # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                                           )
                    dlg.ShowModal()
                    dlg.Destroy()
        else:
            pass
    def OnSendWechatMsg(self,event):
        Password_dlg = wx.PasswordEntryDialog(self, '请输入登录密码：', '微信群消息发布窗口')
        Password_dlg.SetValue("")
        if Password_dlg.ShowModal() == wx.ID_OK:
            self.password = Password_dlg.GetValue()
            if self.password == "hello8031":
                dlg = Send_Wechat_Msg_Dialog(self, -1, "微信群消息发布窗口", size=(800, 600), pos=wx.DefaultPosition, style=wx.DEFAULT_DIALOG_STYLE)
                dlg.CenterOnScreen()
                dlg.ShowModal()
            else:
                tip_dlg = wx.MessageDialog(self, '密码错误！您没有发布微信群消息的权限，请联系管理员', '提示',
                                           wx.OK | wx.ICON_INFORMATION
                                           # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                                           )
                tip_dlg.ShowModal()
    def OnPageChanged(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        sel = self.ctrl.GetSelection()
        # print '23',old,new,sel
        if old ==0:
            self.fyf_progress_contract.timer.Stop()
            self.fyf_progress_order.timer.Stop()
            self.fyf_progress_sec.timer.Stop()
            self.FYF_Progress_Manage_Panel.timer.Stop()
            self.fyf_progress_id.timer.Stop()
        elif old ==1:
            self.scheduling_panel.timer.Stop()
        elif old ==2:
            self.zx_delivery_panel.timer.Stop()
            self.delivery_search_panel.remainingSpace.query_managment_grid.timer.Stop()
        elif old ==3:
            self.cnc_workposition_management.remainingSpace.pvc_workposition_right_show1.timer.Stop()
        elif old ==6:
            self.product_storage_ctrl_panel.timer.Stop()
        elif old ==7:
            self.staff_workload_statistics_day.timer.Stop()
            self.staff_workload_statistics_month.timer.Stop()
        elif old == 8:
            self.Sorting_Vehicle_Panel.remainingSpace.timer.Stop()
        elif old ==9:
            self.Part_Quality_inspection.timer.Stop()
        elif old ==11:
            self.ylp_now_element_scrap.Element_Scrap_Grid.timer.Stop()
        else:
            pass
        if sel ==0:
            self.schedule_monitor.SetSelection(0)
            self.fyf_progress_contract.timer.Start(30000)
            self.fyf_progress_id.timer.Start(10)
            self.fyf_progress_contract.Contract_refresh()
        elif sel ==1:
            self.scheduling.SetSelection(0)
            self.scheduling_panel.timer.Start(1000)
        elif sel ==2:
            self.delivery.SetSelection(0)
            self.zx_delivery_panel.timer.Start(10000)
            self.zx_delivery_panel.TimeRefresh()
        elif sel ==3:
            self.cnc_workposition_management.remainingSpace.SetSelection(0)
            self.cnc_workposition_management.remainingSpace.pvc_workposition_right_show1.timer.Start(10000)
            self.cnc_workposition_management.remainingSpace.pvc_workposition_right_show1.Refresh_left()
        elif sel ==6:
            self.storage_panel.SetSelection(0)
            self.product_storage_ctrl_panel.timer.Start(5000)
            self.product_storage_ctrl_panel.MyRefresh()
        elif sel ==7:
            self.workload_count_panel.SetSelection(0)
            self.staff_workload_statistics_day.timer.Start(30000)
            self.staff_workload_statistics_day.Day_refresh()
        elif sel ==8:
            self.Sorting_Vehicle_Panel.remainingSpace.timer.Start(1000)
        elif sel ==9:
            self.Quality_inspection_station.SetSelection(0)
            self.Part_inquiry.Part_refresh()
        elif sel ==11:
            # self.ERROR_panel.SetSelection(0)
            self.ylp_now_element_scrap.Element_Scrap_Grid.timer.Start(3000)
        else:
            pass
        event.Skip()
def GetIntroText():
    text = \
    "<html><body>" \
    "<h2>欢迎使用天外天智能生产管理系统</h2>" \
    "<h3><br/><b><p>系统概览：</b><br/></h3>" \
    "<h4>天外天智能生产管理系统由天津（天津大学）定智科技有限公司出品。<p>" \
    "它是一套专门针对定制家居家具行业打造的智能化、自动化" \
    "生产综合管理软、硬件系统。</p></h4>" \
    "</ul>" \
    "</ul><p>" \
    "<p>" \
    "</body></html>"

    return text

