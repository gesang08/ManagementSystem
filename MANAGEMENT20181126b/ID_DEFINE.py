import wx
# from wx.lib.embeddedimage import PyEmbeddedImage
import os
import sys
# try:
#     dirName = os.path.dirname(os.path.abspath(__file__))
# except:
#     dirName = os.path.dirname(os.path.abspath(sys.argv[0]))
#
# sys.path.append(os.path.split(dirName)[0])

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
# close = PyEmbeddedImage(
#     b"iVBORw0KGgoAAAANSUhEUgAAAA0AAAANCAYAAABy6+R8AAAABHNCSVQICAgIfAhkiAAAAh9J"
#     b"REFUKJFl0s1LFGEAx/HvMzO7M9vmrrSuThJIhslmaSZqFgZLdSqKjr147VB/Qn9Af0GXTiIU"
#     b"vVAQdRAKqkuColaiiyiKr7FKL7u6OzM78zxPh6igfvcvv8tHCMMEoHAxr/35AlpK/p0wTZz2"
#     b"HLlXbwWABTBzrk83DnSRvjWE4Tj/Rcr3KU1/Zsav6GNvxoU1cSGvmwZ7SZ3Oo5MpIiuGrvl/"
#     b"X+IOIgpJndmPNONM2Elt7KyuU9/djySCbBNGo4ssriA3FlHfNjAaXchkiSKf+u5+ykvLGHLP"
#     b"XlQiSS0SqLoMosHF6DwJdfWIXC+iwUWls4TaQtkJQtPC8gIPo1pldvQlanGNnqs3iLktyOwB"
#     b"TNMk9AMmnzzEmHjHiVOD7AQBVjUI0JUdDqaTzLwfZS6VovPSFUytQUrmXjynfO8uR9MWyrEJ"
#     b"/QCrFkrU9leM5QVysoa044jSD9AAmoxjk6GKtbqNaukglAojCHyi8Q8Ec7PsO3sZt/UQ3uYG"
#     b"3+cLeF82cdsOk719hyjlIis+Na0wlJRExSJe23EitwW5VWRqZJjHQ9eYGhlGbhWJmlvxOvqp"
#     b"lXeRSmM57TnWSx4/ltZZsR5hOAlKz57St1tmbWSYscou0vNIfJwlyGRIHOlACMPkwUCPzsmQ"
#     b"aswi8Hza/ICYgFDDgmMTd2ySkaRgxrg+NinEb3v3z+f15qdpQt/DQvwREaGJOQmau7q5+fqX"
#     b"vZ+3DPNuDe9/tAAAAABJRU5ErkJggg==")
#
# #----------------------------------------------------------------------
# close_inactive = PyEmbeddedImage(
#     b"iVBORw0KGgoAAAANSUhEUgAAAA0AAAANCAYAAABy6+R8AAAABHNCSVQICAgIfAhkiAAAAh5J"
#     b"REFUKJFl0stLVFEAgPHv3Htn7lzNGW1GZzSNtJI0fFZjQkQPqV0U0SJmnZugP6B9/0O4cZNE"
#     b"ZFAQUdBrlZBYoJmGOYSPSUvRRp25r3NOi8iN3/7b/YQwTAAuDn7VM3kXqdiTaUBbS4w3Q+0C"
#     b"QAjDpD83qfuPNdDZEicWMfZMbqCYzBcZmy0wNtIprIFb4/pUa4bzfXHiVRAxFWVP7w6OLQgk"
#     b"NDTFsWOKyopxbSyubpPtShB6mroaQTolWFiQzM9LCsuadEpQWw1uSZHtSpBfKmLscySVFRpM"
#     b"j+R+SaZWcLrXoDoBJ7shUydIJRVW1MeJaSwzxHLLJUqu4PnLaZYKity1Hg42RjhQb2CaAs/z"
#     b"efjsM+/GDM6e6cErF7Hc8g5bO5rKqmZevJ8iXjXL1csdaC2QoeDpq1nu3S8SiXZgJxWe72NJ"
#     b"6bO+rZhbNvDDdqKOZHMHtBYARJ0UrkyysGRyfEuhVIDhej4fpkO+5H2uXKqm5VCawi+fbz82"
#     b"+fnb4+jhNHdvp8jUh7ihRMkAQ0rF6oaku73EwfqQlbWQ4dEJbt55xPDoBCtrIc2NIX3dZbbd"
#     b"AK0k4lzugS5HT7C+vkG2tYxjmzx++4eiaiJuLHLjQoKSKxmfc0gma3D8iX8istdHtG+3YVHC"
#     b"dX28yBEQEdABdvAd244iRQVRb4aPT3JC/Lc3kBvSn6YKlL0AYVi7IrQKcewIvR0NvB4ZFAB/"
#     b"Aa4X7YpTOtu/AAAAAElFTkSuQmCC")
#
# #----------------------------------------------------------------------
# maximize = PyEmbeddedImage(
#     b"iVBORw0KGgoAAAANSUhEUgAAAA0AAAANCAYAAABy6+R8AAAABHNCSVQICAgIfAhkiAAAAJZJ"
#     b"REFUKJG9kj0OwjAMRp8D6hDUExDmrr0dEkOHXgXuAMfIBl1yCwaMMAyoIJQWqUu/yZa/5x/J"
#     b"Im7BVLnJBLDsg2vbPC3G8e51zapp5QeyGLHzBYbWtcfwJFlv8Nsdrqpypuu4HfY5hHPgPVKW"
#     b"+STv3/XeOnrEH80HfW9SxVIaNFlKoJpDEgL30xGKIqdUkRA+qcz2Ri8+yyNzplbFQwAAAABJ"
#     b"RU5ErkJggg==")
#
# #----------------------------------------------------------------------
# maximize_inactive = PyEmbeddedImage(
#     b"iVBORw0KGgoAAAANSUhEUgAAAA0AAAANCAYAAABy6+R8AAAABHNCSVQICAgIfAhkiAAAAJhJ"
#     b"REFUKJFjZGRiZiAVMJGsg4GBgQXGaGz7+v/CxX84FRroMzHUV3Ezomi6cPEfw/Vb/xiYsbj2"
#     b"718cNsnKMDJUlnAwqKthuvjmrX8MS1b8xtTEyMTAwMXFyMDLw4ihiYuLkYERySyyAoJ+muB+"
#     b"+v2bgeHeA+xBfu/BP4bfiHBAaJKWYmTYsfsPAysrpqbfvyHyMMBIt2QEAFPtI359ud6yAAAA"
#     b"AElFTkSuQmCC")
#
# #----------------------------------------------------------------------
# minimize = PyEmbeddedImage(
#     b"iVBORw0KGgoAAAANSUhEUgAAAA0AAAANCAYAAABy6+R8AAAABHNCSVQICAgIfAhkiAAAAMlJ"
#     b"REFUKJGdkrsNwkAQRN/eWohPByYkQaIKSqAJhBAF0AdExGRUQwoioAREAth3S2BjWzLIwER7"
#     b"oxntzOpEnPIrotcQ1lvjeIbbHXjkpAczkAf0OjAc4GZTQZwiTrHNzhoxX5g4xRU7U9+c654A"
#     b"VEzY150qpuQLedY1qvFJCqrgX3ENQp5C7IMp9eAEQsjEIWQXVC3UpckSWK5gfwCRnKv0nIwL"
#     b"vrLJQDzomytGEXRb5bOYLhfotyEeASk1xfUEcT+r9s83cs2SOp6D2FytkDyOCgAAAABJRU5E"
#     b"rkJggg==")
#
# #----------------------------------------------------------------------
# minimize_inactive = PyEmbeddedImage(
#     b"iVBORw0KGgoAAAANSUhEUgAAAA0AAAANCAYAAABy6+R8AAAABHNCSVQICAgIfAhkiAAAANRJ"
#     b"REFUKJGdkj1OgkEQhp/ZJSCF0VBYmUBPixfwAtzRS2DvCShMvAGRUJCQkMjOjwV8CwT1C77V"
#     b"zGaevO9MViRlrlWnKd7el7HaKGpgpQDg7ng4rkY3Bw/3PZ4nI6lQzpnp0+BPh5fXDwBS8+DR"
#     b"HquonUNEOxWHmaOTWSvk6sDJIRqZO0kEO8nrAUmEiN8gC8iCHyBvYqdU01RIizKbr1msy4/R"
#     b"xo/9uvbRKYIIJewSSgIderWv0PZrRzcrw9tAVeulwvd7fC62DO5uAJD/fKPUPnKpbzVEY0DN"
#     b"U2N1AAAAAElFTkSuQmCC")
#
# #----------------------------------------------------------------------
# restore = PyEmbeddedImage(
#     b"iVBORw0KGgoAAAANSUhEUgAAAA0AAAANCAYAAABy6+R8AAAABHNCSVQICAgIfAhkiAAAAUlJ"
#     b"REFUKJGd0j9LW1EYBvDfvUkM1iaGkohaKJRQv0XJ5FCKg1PnoogUHCwOjnVTx67d2n6Cgq2O"
#     b"7oXupdKhUIOQqMRSE733djiXNkoXPcvhvO/z530fThTFBTc9RUjfvM2020zeC5VS3i3kiBg/"
#     b"ulQa4oXnUREcd9nZ5fAnvQ5nHaKEYkY14w4eNHm6+M9JfTwQHs5w2WdjHSkRBj2W5uge8Ghi"
#     b"iBQl/O6RXDA9gUvWXnJ8xIdPYdQIpXiIVMJpm433tB4H0OcvLMwHxyzoSIeCUEB5QJywvUm/"
#     b"T6vFk2dUavxC5Vp6RlDLya+3ODnBK4p3ebfC4D+RK2AM/TP29slSqjVerPJxJ/RG/6LzK00p"
#     b"Y2UuqF7gHD2Mo5ELX3H62uZ+k85BWDbJF6/nIZUx1eR7d4hUnWR2mZn61eHztEQp344oN8Lz"
#     b"Nn/vD5FAXWAC04u0AAAAAElFTkSuQmCC")
#
# #----------------------------------------------------------------------
# restore_inactive = PyEmbeddedImage(
#     b"iVBORw0KGgoAAAANSUhEUgAAAA0AAAANCAYAAABy6+R8AAAABHNCSVQICAgIfAhkiAAAAYxJ"
#     b"REFUKJGdkr2PTGEUh5/z3ntndmYXIyODiI8oVyGRLTUitpToNCRCJdv7B2gkOrV6Q4hWp6JV"
#     b"jXILhWKHeMfcmXvfj3MUk7jbcqrTPPk9J+cn4gr+dUqAz9OFzWth0CtJCiEaWUHNiMnIahQ0"
#     b"TEYF16+OpARYto6v35SZj/gaZnNj2UIblZlX6lXg8thzf/dYl7RRFfyYK2fHjskI9m6XZIWs"
#     b"4Gtj72VkerAk5SEADiBEWKwEVeHEphASvPoQefq65fRJAdaqmHVQG43vP5XdawX3blZcueh4"
#     b"/qjPqeMQsxEUytKoSu30YjZmXlkFeP8p0URj+0LBrZ2KrYGjpiBlR1bpoDYYhz6Ts7H/MTJv"
#     b"4O4NWIhj/03AZ0hBCNl1UMjCrxr80nj2oI8qbA2FJ28j774oMQnWGqpH/qQ5s2paHr6IbPSg"
#     b"KoTWCYfZcMGhvqHQjGAd5Ehsn/FMD35Ti6NXClnWOiFCkRI7lxKD/pGbzk96PL4zJoUhhvyt"
#     b"S7L1bmpUpXBusgmA/E/3/gASuMtl4Uj5YAAAAABJRU5ErkJggg==")
#
# #----------------------------------------------------------------------
#
# fullscreen = PyEmbeddedImage(
#     b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAActJ"
#     b"REFUOI2dk09I02EYx7/v+/7+DDRRYg4EWWYUKAjDSxBhJKuEUUJslwi8BXoaEaIdhpchddgt"
#     b"CKIgCIbeYmXaTHboEigZ5GENdCCKfyZKTrf5+72Pp7nf9Lcf4gPP5fl+3i9feJ8HcKrghPD4"
#     b"X9c5IdxJvHq4PFKvy3dOjKgltN4f71QU/lGo4kZD250/u5nZtB3H7IY9PRElW6f/ApgPAIiw"
#     b"YZpax+rM8x2nNBeqSoLghMBkyIzFYptSSrcdzDnfCofDzd3db9X5+WdHAKAAQEt/9LKaz3zI"
#     b"Ag+llG7f7UeQks4YLP787AaAnGdn2PsgupD9NvpVaeuLXmeGMkcwm8rg2tYe4tOLVY+D/i5L"
#     b"EtYoQQlvIDqoEKgfoGbGmVEGHt/tQOBWe5WBrut4k05VTAQHA4b4ytTLVyAMSML/smgYBorF"
#     b"YlUbxok/TEkmZ/zHfkHc5ACw/GX4E0B+q4GmaVVtNYBEPOPL39v4/iJ/Zg/O8wvWme0iIRLh"
#     b"3t9osI6u7GI/lRozTqP2t7DUyVjJlWQlV46VXDl+5FpIX4Jmm8rWYDJkEmNPhSoKqqYUJKcn"
#     b"64mxAzu05jHt/UtuN17rJSL6u5IYeV+LOwbQBrHjq9vsKwAAAABJRU5ErkJggg==")
#
# #----------------------------------------------------------------------
# reload = PyEmbeddedImage(
#     b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAApFJ"
#     b"REFUOI11k72LXFUUwH/n3vvmvbzZnZnNl7sWI0mIISaIIKYJ2AmbznQWKezSiOm0NaXpAjZu"
#     b"kQTMHyBC0JBOCwmyWBrXHaMmuopLdt7Ox3vz3r33WMyyCJscOBwOnPPjfAovEFWEr2kBcIla"
#     b"BH1enBxI/Golb7ZGb/kZb6vXkyCI4VeX8G3iFn+Qq1vTFwL0886pcqofNSXvgh41qEGEqBJR"
#     b"tl3Gl2ZBbhy6ujs4ACjXuidiET7zDauuhRFnidky0gwxfkz0gq+JJuEbl9kPDn1YPAYwAHqT"
#     b"VEfhmq9ZdS4aJBIWThNeuUQ4fpEgbbAGk3dMbMxqqMI1vUkK4AAa8vN+ppdj96ypj59DJv+g"
#     b"+TJiFtDuq2iIUO1A1sM8/c7Epr48Nd0voFifAxpzAQ0rdPuEi5/M+6rHaLkDf3yPWzqLOAfT"
#     b"f8G20KZeCT5cANaNKoJKX4RExluIr5B8CXp9aCrsbHvuJ2201SGaNiKaaJS+KmJE0KjRIwZm"
#     b"BZTP5gvXiHRWiJ3+vFObQdqD7AiIQIxeBHUAorqh1lWiIWP3TyiHkPXgpdfg5Dv4jXvY0S9g"
#     b"LGoyRGyFbzb2hxiCfWgdA2M5J5v3sVRodpQg78GRU5B2MX89BT9Bmm1i1MFM7cP9NXZmo83Q"
#     b"hNvEokzKAdZaEuNxjx8gj+6RDB9h8iWME/DDMlbh9jFGm/sAuU7UkbsVxuM1KX+fGgokzUlS"
#     b"S1o9wbUMRgvYHUxDsbsmtbsl14kHTvnZx0td0vqKW2y/b7vLZ6R9LAfQyfY0DLd+nhWTO9a3"
#     b"7h7+dKd43i8I0Hp5kYUrr7vTbyzzZq8tJwB2xvrbj09Yv/uT3/x7zBiYwcEKBEiBfM/aPQUI"
#     b"ewk1MPk/4D/OAyg6YvZkywAAAABJRU5ErkJggg==")
#
# #----------------------------------------------------------------------
# remove = PyEmbeddedImage(
#     b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAApVJ"
#     b"REFUOI2lkUtIVHEUxr//vf9778x4J8d8DDaODjo+mBzLKFJJJbVWFdmiVaEtehBYi2hVENXK"
#     b"XS0iC6JNFkbkInwVQeoiiLAHtlAhW6TjTPnA9DreO/d/WjjOIkiDDnxwFuc7fOd3gP8s+bmD"
#     b"118+UPGmiagsNL88UJqb62gLhTrP1tVdmY5G334zjOiGG574XF00/IjmHt6lO+mujvvb/J1L"
#     b"3d1k9vRQk9fbsWkCX9ya/DIxUdVQ2+gt9Obt3lG1N6ykp+NGe/vnl5OT15aEiGx6x03g4GBl"
#     b"IEGX2ojaLlBXeflKXWbm/n9i8BTILivgV4vkuXC0/x0W3n9C3tYMnsjOXpmyrMEfhmFutIC7"
#     b"s3C9Jpw4vjAO3Ha6zS2Ki11cNZXz+fnnXkUiMbuy8l6OrreYpikxxgVRQmKMyaqa9mJo6PUH"
#     b"PhTc6Q9gDvM1u1BxuFVxKRK+9/UhOjaOiCzL24uLHzcfOlLvcGoAGDRNgSxz9PcPnIrHf9Xy"
#     b"r6FqHm85gXBFCNUeDwMAo7EB77uewdHxIBLI85c3HzsKp9MJxhgYYwCAmZmZwOjoWBp3EbJz"
#     b"SoPQPR5YpglbCLhcaQgEg/Do6XsWF1elkZGPUFUVkiRB0zTouo7p6Rh03bOPBwKBUIbbDQAg"
#     b"AIwxmKYJb1YWTp9pPckkSYrFfoKIUgKAkpIgDMO6xX0+n+R0OSGESJG1LAv5BX4UBQulRCIB"
#     b"y7Jg2zaEsGHbAkQCmqZifn7JwYlk+vM1jDEIIWAYBoQQSbNIiYggxCqEYDZXFDVlWge03v9N"
#     b"azMEzjm4qqp83STLUvJGAmMEYM1AxFLpkgggSYCiaDKPRhenenuHddNM0BokgMhODq+DQyo6"
#     b"QLBtgiwzNju7svwbnlAlxKIQCyQAAAAASUVORK5CYII=")
#
# #----------------------------------------------------------------------
# sort = PyEmbeddedImage(
#     b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAMdJ"
#     b"REFUOI2VklEOgyAMhv+iR1jmdfQWHt1dQXA+dI9K97BpaIFE/4SQAv36UwC5BukAROxaOl7T"
#     b"pPYdbmpZVxUrgMRNyLUkcZMqIIQ64IpCWMqAo6qdrbyfVdymAbmWLDAH+LKDq6oC0uql+FDw"
#     b"uonnFWLcM8vONRkkLBWATSgBAeBt/gH9fp9WjLvY6t3zIZIiCZjnQFkTS8kA0PcDmBn8YTAz"
#     b"hn7IHdSSD0lyLfqfOx3Y5FIPxnFUs3Jw9RUk7kLJerGJd/QF7eJxBTVIT38AAAAASUVORK5C"
#     b"YII=")
#
# #----------------------------------------------------------------------
# superscript = PyEmbeddedImage(
#     b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAYFJ"
#     b"REFUOI3VkTtPAlEQhUfW4INCxMpigcTEVhMbCxO2NDZgg6UUJpSIzZZS+AO201gYaa1MbEy2"
#     b"EAosbCQxxFdUsKLjIffOndl1sTBYiEFjYzzVmWTmy8wZgH+voZ82ru0+RfWpkeOJUV/04lpY"
#     b"J+ZMDgDA91NAwD9s3T9Q4vyqZS3Mjm//Ytl3pfZr5Y2D52qvHu4Z0zQLrusCEQEzAxGllFKH"
#     b"iAiICLZtGzGzkhPoQvUWE725jxMcx7GYeV4pFSOicj6fr0opC1LKKjOnlrYqCZ8G0bvHtsHk"
#     b"BOfWL6MAn0JMp9OGUuqMmaHT6WSVUgnbtg0AgJWdm4I+PRZzX7vwIl9bR5szwT4AAEAymbQc"
#     b"x8kIIYCIJovFYnNQJn1fIKKcEAI8z4N2u537LtQ+gJTyWAiRRUTodruZSCRiDAJoPROPx4O6"
#     b"ru8hYqFUKlmBQGDS7/cvNpvNVU3TTomoPhAQDodPETEopVShUKgupUw1Go0aM9eZeRkAyp7n"
#     b"fQn5W70BAIHMJSEYEtgAAAAASUVORK5CYII=")
try:
    from agw import aui
    from agw.aui import aui_switcherdialog as ASD
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.aui as aui
    from wx.lib.agw.aui import aui_switcherdialog as ASD

# CUSTOM_PANE_BITMAPS = [(close, aui.AUI_BUTTON_CLOSE, True, False),
#                        (close_inactive, aui.AUI_BUTTON_CLOSE, False, False),
#                        (minimize, aui.AUI_BUTTON_MINIMIZE, True, False),
#                        (minimize_inactive, aui.AUI_BUTTON_MINIMIZE, False, False),
#                        (maximize, aui.AUI_BUTTON_MAXIMIZE_RESTORE, True, True),
#                        (maximize_inactive, aui.AUI_BUTTON_MAXIMIZE_RESTORE, False, True),
#                        (restore, aui.AUI_BUTTON_MAXIMIZE_RESTORE, True, False),
#                        (restore_inactive, aui.AUI_BUTTON_MAXIMIZE_RESTORE, False, False)]
#
# CUSTOM_TAB_BUTTONS = {"Left": [(sort, aui.AUI_BUTTON_CUSTOM1),
#                                (superscript, aui.AUI_BUTTON_CUSTOM2)],
#                       "Right": [(fullscreen, aui.AUI_BUTTON_CUSTOM3),
#                                 (remove, aui.AUI_BUTTON_CUSTOM4),
#                                 (reload, aui.AUI_BUTTON_CUSTOM5)]
#                       }
#
# _ = wx.GetTranslation


ID_TOOLBAR_START=wx.ID_HIGHEST + 1
ID_LAYOUT_PARAMETER_SETUP=ID_TOOLBAR_START
ID_CONTRACT_MAKER_PARAMETER_SETUP=ID_TOOLBAR_START+1
ID_TOOLBAR_LAST=ID_CONTRACT_MAKER_PARAMETER_SETUP
ID_CreateTree = ID_TOOLBAR_LAST + 1
ID_CreateGrid = ID_CreateTree + 1
ID_CreateText = ID_CreateTree + 2
ID_CreateHTML = ID_CreateTree + 3
ID_CreateNotebook = ID_CreateTree + 4
ID_CreateSizeReport = ID_CreateTree + 5
ID_GridContent = ID_CreateTree + 6
ID_TextContent = ID_CreateTree + 7
ID_TreeContent = ID_CreateTree + 8
ID_HTMLContent = ID_CreateTree + 9
ID_NotebookContent = ID_CreateTree + 10
ID_SizeReportContent = ID_CreateTree + 11
ID_SwitchPane = ID_CreateTree + 12
ID_CreatePerspective = ID_CreateTree + 13
ID_CopyPerspectiveCode = ID_CreateTree + 14
ID_CreateNBPerspective = ID_CreateTree + 15
ID_CopyNBPerspectiveCode = ID_CreateTree + 16
ID_AllowFloating = ID_CreateTree + 17
ID_AllowActivePane = ID_CreateTree + 18
ID_TransparentHint = ID_CreateTree + 19
ID_VenetianBlindsHint = ID_CreateTree + 20
ID_RectangleHint = ID_CreateTree + 21
ID_NoHint = ID_CreateTree + 22
ID_HintFade = ID_CreateTree + 23
ID_NoVenetianFade = ID_CreateTree + 24
ID_TransparentDrag = ID_CreateTree + 25
ID_NoGradient = ID_CreateTree + 26
ID_VerticalGradient = ID_CreateTree + 27
ID_HorizontalGradient = ID_CreateTree + 28
ID_LiveUpdate = ID_CreateTree + 29
ID_AnimateFrames = ID_CreateTree + 30
ID_PaneIcons = ID_CreateTree + 31
ID_TransparentPane = ID_CreateTree + 32
ID_DefaultDockArt = ID_CreateTree + 33
ID_ModernDockArt = ID_CreateTree + 34
ID_SnapToScreen = ID_CreateTree + 35
ID_SnapPanes = ID_CreateTree + 36
ID_FlyOut = ID_CreateTree + 37
ID_CustomPaneButtons = ID_CreateTree + 38
ID_Settings = ID_CreateTree + 39
ID_SystemParameterSettings = ID_CreateTree+200

ID_CustomizeToolbar = ID_CreateTree + 40
ID_DropDownToolbarItem = ID_CreateTree + 41
ID_MinimizePosSmart = ID_CreateTree + 42
ID_MinimizePosTop = ID_CreateTree + 43
ID_MinimizePosLeft = ID_CreateTree + 44
ID_MinimizePosRight = ID_CreateTree + 45
ID_MinimizePosBottom = ID_CreateTree + 46
ID_MinimizeCaptSmart = ID_CreateTree + 47
ID_MinimizeCaptHorz = ID_CreateTree + 48
ID_MinimizeCaptHide = ID_CreateTree + 49
ID_NotebookNoCloseButton = ID_CreateTree + 50
ID_NotebookCloseButton = ID_CreateTree + 51
ID_NotebookCloseButtonAll = ID_CreateTree + 52
ID_NotebookCloseButtonActive = ID_CreateTree + 53
ID_NotebookCloseOnLeft = ID_CreateTree + 54
ID_NotebookAllowTabMove = ID_CreateTree + 55
ID_NotebookAllowTabExternalMove = ID_CreateTree + 56
ID_NotebookAllowTabSplit = ID_CreateTree + 57
ID_NotebookTabFloat = ID_CreateTree + 58
ID_NotebookTabDrawDnd = ID_CreateTree + 59
ID_NotebookDclickUnsplit = ID_CreateTree + 60
ID_NotebookWindowList = ID_CreateTree + 61
ID_NotebookScrollButtons = ID_CreateTree + 62
ID_NotebookTabFixedWidth = ID_CreateTree + 63
ID_NotebookArtGloss = ID_CreateTree + 64
ID_NotebookArtSimple = ID_CreateTree + 65
ID_NotebookArtVC71 = ID_CreateTree + 66
ID_NotebookArtFF2 = ID_CreateTree + 67
ID_NotebookArtVC8 = ID_CreateTree + 68
ID_NotebookArtChrome = ID_CreateTree + 69
ID_NotebookAlignTop = ID_CreateTree + 70
ID_NotebookAlignBottom = ID_CreateTree + 71
ID_NotebookHideSingle = ID_CreateTree + 72
ID_NotebookSmartTab = ID_CreateTree + 73
ID_NotebookUseImagesDropDown = ID_CreateTree + 74
ID_NotebookCustomButtons = ID_CreateTree + 75
ID_NotebookMinMaxWidth = ID_CreateTree + 76

ID_SampleItem = ID_CreateTree + 77
ID_StandardGuides = ID_CreateTree + 78
ID_AeroGuides = ID_CreateTree + 79
ID_WhidbeyGuides = ID_CreateTree + 80
ID_NotebookPreview = ID_CreateTree + 81
ID_PreviewMinimized = ID_CreateTree + 82

ID_SmoothDocking = ID_CreateTree + 83
ID_NativeMiniframes = ID_CreateTree + 84

ID_LogOut = ID_CreateTree + 100
ID_LogIn = ID_CreateTree + 101
ID_Productive_Moniter = ID_CreateTree+102
ID_WS1_Moniter = ID_Productive_Moniter+1
ID_WS2_Moniter = ID_Productive_Moniter+2
ID_WS3_Moniter = ID_Productive_Moniter+3
ID_WS4_Moniter = ID_Productive_Moniter+4
ID_WS5_Moniter = ID_Productive_Moniter+5
ID_WS6_Moniter = ID_Productive_Moniter+6
ID_WS7_Moniter = ID_Productive_Moniter+7
ID_WS8_Moniter = ID_Productive_Moniter+8
ID_WS9_Moniter = ID_Productive_Moniter+9
ID_WS10_Moniter = ID_Productive_Moniter+10

ID_DB_Browser = ID_Productive_Moniter+11
ID_DB1_Browser = ID_DB_Browser+1
ID_DB2_Browser = ID_DB_Browser+2
ID_DB3_Browser = ID_DB_Browser+3
ID_DB4_Browser = ID_DB_Browser+4
ID_DB5_Browser = ID_DB_Browser+5
ID_DB6_Browser = ID_DB_Browser+6
ID_DB7_Browser = ID_DB_Browser+7
ID_DB8_Browser = ID_DB_Browser+8
ID_DB9_Browser = ID_DB_Browser+9
ID_DB10_Browser = ID_DB_Browser+10

ID_FirstPerspective = ID_CreatePerspective + 1000
ID_FirstNBPerspective = ID_CreateNBPerspective + 10000

ID_PaneBorderSize = ID_SampleItem + 100
ID_SashSize = ID_PaneBorderSize + 2
ID_CaptionSize = ID_PaneBorderSize + 3
ID_BackgroundColour = ID_PaneBorderSize + 4
ID_SashColour = ID_PaneBorderSize + 5
ID_InactiveCaptionColour = ID_PaneBorderSize + 6
ID_InactiveCaptionGradientColour = ID_PaneBorderSize + 7
ID_InactiveCaptionTextColour = ID_PaneBorderSize + 8
ID_ActiveCaptionColour = ID_PaneBorderSize + 9
ID_ActiveCaptionGradientColour = ID_PaneBorderSize + 10
ID_ActiveCaptionTextColour = ID_PaneBorderSize + 11
ID_BorderColour = ID_PaneBorderSize + 12
ID_GripperColour = ID_PaneBorderSize + 13
ID_SashGrip = ID_PaneBorderSize + 14
ID_HintColour = ID_PaneBorderSize + 15

ID_VetoTree = ID_PaneBorderSize + 16
ID_VetoText = ID_PaneBorderSize + 17
ID_NotebookMultiLine = ID_PaneBorderSize + 18


STATE_INITIAL = 0
STATE_TECHNICAL_AUDIT = 5
STATE_PRICE_AUDIT = 10
STATE_FINANCIAL_AUDIT = 15
STATE_CHECK_SPLIT_ORDER = 20
STATE_SPLIT_ORDER = 25
STATE_BEGIN_SCHEDULING=26
STATE_PLAN_PRODUCTION=27
STATE_LAYOUT_FINISH = 30
STATE_BEING_PROCESSED = 35
STATE_MACHINE_FINISH = 40
STATE_SORTTING_BEFORE_EDGE_MILLING = 45
STATE_EDGE_MILLING = 50
STATE_DRILLING = 55
STATE_SPECIAL_SHAPED_SAND_MACHINE = 60
STATE_SORTTING_BEFORE_LAYERING = 65
STATE_LAYERING = 70
STATE_POLISHING = 75
STATE_HALF_QUALITY_TESTING = 80
STATE_SORTTING_BEFORE_MEMBRANE = 85
STATE_MEMBRANE_PRE_LAYOUT = 90
STATE_GLUE_SPRAY_AND_DRY = 95
STATE_MEMBRANE = 100
STATE_SHELF_AFTER_MEMBRANE = 105
STATE_ARCHAIZE = 110
STATE_QUALITY_TESTING = 115
STATE_PACKAGE = 120
STATE_HARD_PACKAGE = 123
STATE_WAREHOUSE = 125
STATE_SHELF_BEFORE_DELIVERY = 130
STATE_DELIVERY = 150
STATE_INSTALLING = 160
STATE_AFTER_SALE_SERVICE = 170
STATE_GUARANTEE_FINISH = 180
STATE_REPORT_ERROR = 1000
STATE_ERROR_ON_DEALING = 1005
STATE_SCRAP = 1010

SORTING_BY_ORDER_POSITION_NUM = 7
DRILLING_POSITION_NUM = 24
EDGE_MILLING_POSITION_NUM = 8
POLISHING_POSITION_NUM = 9
REGULA_POSITION_NUM = 10
ARTIFICAL_POLISHING = 11
ARTIFICAL_POLISHING_AND_CHECK_POSITION_NUM = 11
SORTING_BRFORE_MEMBRANE_POSITION_NUM = 12
GLUE_SPRAR_AND_DRY_POSITION_NUM = 14
SORTING_AFTER_MEMBRANE_POSITION_NUM = 16
ARCHAIZE_POSITION_NUM = 19
QUALITY_TESTING_POSITION_NUM = 18
SORTING_AFTER_PACKAGE_POSITION_NUM = 23
DELIEVERT_ORDER_POSITION_NUM = 17
HALF_TEST = 37


PACKING_TASK_LIST_STATE_INITIAL = 0
PACKING_TASK_LIST_STATE_PACKANG = 5
PACKING_TASK_LIST_STATE_PACKANE_FINISH = 10
PACKING_TASK_LIST_STATE_ELEMENT_PACKAGE_FINISH = 15
PACKING_TASK_LIST_STATE_PRINT_FORM = 20
PACKING_TASK_LIST_STATE_WAREHOUSE = 123
PACKING_TASK_LIST_STATE_WRONG = 1000

SCHEDULE_INITIAL = 0
SCHEDULE_LAYOUT = 5
SCHEDULE_LAYOUT_FINISH = 10
SCHEDULE_ORDER_SORTING = 15
SCHEDULE_ORDER_SORTING_FINISH = 20
SCHEDULE_MEMBRANE_LAYOUT = 25
SCHEDULE_MEMBRANE_LAYOUT_FINISH = 30
SCHEDULE_PACKAGE_LAYOUT = 35
SCHEDULE_PACKAGE_LAYOUT_FINISH = 40
SCHEDULE_SUSPEND = 1000

ELEMENT_TYPE_DOOR=1
ELEMENT_TYPE_ARC_LAYER=2
ELEMENT_TYPE_ROME_COLUMN=3
ELEMENT_TYPE_TOP_LINE=4
ELEMENT_TYPE_WAIST_LINE=5
ELEMENT_TYPE_FOOT_LINE=6
ELEMENT_TYPE_DOORKNOB=7
ELEMENT_TYPE_HINGES=8
ELEMENT_TYPE_LINTEL=9
ELEMENT_TYPE_GLASS=10
ELEMENT_TYPE_KNOB=11
ELEMENT_TYPE_FAKE_BLINDS=13

MEMBRANE_NO_TEXTURE=0
MEMBRANE_VERTICLE_TEXTURE=1
MEMBRANE_HORIZONTAL_TEXTURE=2

WORKORDER_MACHINING_FINISH_STATE=15
ALREADY_UPDATE_MACHINING_FINISH_STATE=20
STATE_MEMBRANE_LAYOUT_OK=10
STATE_BEGIN_MEMBRANE=100
STATE_BUSY_MEMBRANE=105
REWORK_PRIORITY_VALUE=1000
PACKAGE_FINISH_STATE=10
ERROR_COMPONENT_STATE=5
GOT_MEMBRANE_WORKORDER=1
LAYOUT_AREA=3000000
STANDARD_AREA=3862200
RADIUS=17.5
MARGIN=5

RUN_NORMAL = 0
PRE_LAYOUT_ERROR = 1
LAYOUT_ERROR = 2
LAYOUT_OK=3
MEMBRANE_LAYOUT_OK=4
POST_LAYOUT_ERROR = 5
LOAD_ERROR =6
UPDATE_PRIORITY_ERROR =7
UPDATE_STATE_ERROR = 8
MODIFY_NOT_ONLINE_PRIORITY=5
MODIFY_NOT_ONLINE_DAY=14
MODIFY_URGENT_PRIORITY=50
ELEMENT_LATICES_BOARD_INDEX=15
MACHINE_NUM_GLASS='4'
MACHINE_NUM_NORMAL='1&2&3&5&6'
Scheduling_Time=['0:00','1:00','2:00','3:00','4:00','5:00','6:00','7:00','8:00','9:00','10:00','11:00','12:00','13:00','14:00','15:00','16:00','17:00','18:00','19:00','20:00','21:00','22:00','23:00',]

#---------------------------------------zx
ID_WAIT_DELIVERY = wx.NewId()
ID_DELIVERYING = wx.NewId()
ID_COMPLATE_DELIVERY = wx.NewId()
ID_CANCEL_DELIVERY = wx.NewId()

ID_TODAY = wx.NewId()
ID_YESTERDAY = wx.NewId()
ID_BYESTERDAY = wx.NewId()
ID_All_TIME = wx.NewId()

ID_WAIT_DELIVERY = wx.NewId()
ID_DELIVERYING = wx.NewId()
ID_COMPLATE_DELIVERY = wx.NewId()
ID_CANCEL_DELIVERY = wx.NewId()
ID_All_STATE = wx.NewId()

ID_CNC_POSITION = wx.NewId()
ID_SORTING_BEFORE_M = wx.NewId()
ID_QUALITY_TESTING = wx.NewId()
ID_SPARE = wx.NewId()
ID_All_POSITION = wx.NewId()

#----------------------------------------FYF&YLP
ID_today = wx.NewId()
ID_yesterday = wx.NewId()
ID_byesterday = wx.NewId()
ID_bbyesterday = wx.NewId()

ID_part_today = wx.NewId()
ID_part_yesterday = wx.NewId()
ID_part_byesterday = wx.NewId()
ID_part_bbyesterday = wx.NewId()

ID_sec_today = wx.NewId()
ID_sec_yesterday = wx.NewId()
ID_sec_byesterday = wx.NewId()
ID_sec_bbyesterday = wx.NewId()

ID_order_today = wx.NewId()
ID_order_yesterday = wx.NewId()
ID_order_byesterday = wx.NewId()
ID_order_bbyesterday = wx.NewId()

ID_contract_today = wx.NewId()
ID_contract_yesterday = wx.NewId()
ID_contract_byesterday = wx.NewId()
ID_contract_bbyesterday = wx.NewId()

ID_staff_day_today = wx.NewId()
ID_staff_day_yesterday = wx.NewId()
ID_staff_day_byesterday = wx.NewId()
ID_staff_day_bbyesterday = wx.NewId()

ID_staff_month_today = wx.NewId()
ID_staff_month_yesterday = wx.NewId()
ID_staff_month_byesterday = wx.NewId()
ID_staff_January_type = wx.NewId()
ID_staff_February_type = wx.NewId()
ID_staff_March_type = wx.NewId()
ID_staff_April_type = wx.NewId()
ID_staff_May_type = wx.NewId()
ID_staff_June_type = wx.NewId()
ID_staff_July_type = wx.NewId()
ID_staff_August_type = wx.NewId()
ID_staff_September_type = wx.NewId()
ID_staff_October_type = wx.NewId()
ID_staff_November_type = wx.NewId()
ID_staff_December_type = wx.NewId()

ID_library_today = wx.NewId()
ID_library_yesterday = wx.NewId()
ID_library_byesterday = wx.NewId()
ID_library_bbyesterday = wx.NewId()

ID_quality_today = wx.NewId()
ID_quality_yesterday = wx.NewId()
ID_quality_byesterday = wx.NewId()
ID_quality_bbyesterday = wx.NewId()

ID_quality_testing_today = wx.NewId()
ID_quality_testing_yesterday = wx.NewId()
ID_quality_testing_byesterday = wx.NewId()
ID_quality_testing_bbyesterday = wx.NewId()

YLP_popupID1 = wx.NewId()
YLP_popupID2 = wx.NewId()
YLP_complete_popupID1 = wx.NewId()
YLP_waiting_popupID1 = wx.NewId()
YLP_waiting_popupID2 = wx.NewId()


# Sort_server_ip = '192.168.31.53'
# Sort_user_list = ['hcj']
server_ip = '192.168.31.250'
user_list = ['chk']
# server_ip = 'localhost'
# user_list = ['root']
password = '12345678'
database = ['hanhai_manufacture','hanhai_produce','hanhai_management']
charset = 'utf8'

# Cloud_ip='bj-cdb-qwgzr521.sql.tencentcdb.com'
# Cloud_username=['root']
# Cloud_password='tianda123'
# Cloud_manufacturerDB=['hanhai_manufacture','hanhai_produce','hanhai_management']
Cloud_ip='120.77.38.174'
Cloud_username=['root']
Cloud_password='15db6132d967fb52'
Cloud_manufacturerDB=['hanhai_manufacture','hanhai_produce','hanhai_management']

local_server_ip = '127.0.0.1'
local_user_list = ['root']
local_password = '12345678'
local_database = ['hanhai_manufacture','hanhai_produce','hanhai_management']
