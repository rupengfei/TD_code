# -*- coding:utf-8 -*-  
# ==========================================
#       author: Pengfei.Ru
#         mail: a773849069@gmail.com
#         time: 2018/12/4
# ==========================================
# import sys
from PySide2 import QtCore, QtGui, QtWidgets
# import pyside2uic as uic
import Utils.uiTool as uiTool
# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*


def main():
    #  定义一个电脑界面程序会用到 sys.argv 作为存储参数
    # app = QtWidgets.QApplication(sys.argv)

    # 对于maya，只需定义界面的父层， 赋予maya主窗口名称
    window = QtWidgets.QMainWindow(parent=uiTool.get_maya_window())



    window.show()

    # app.exec_() 电脑桌面界面会用到这个作为启动
