# -*- coding:utf-8 -*-  
# ==========================================
#       author: Pengfei.Ru
#         mail: a773849069@gmail.com
#         time: 2018/12/3
# ==========================================
import maya.OpenMayaUI as OpenMayaUI
import shiboken2
from PySide2 import QtWidgets
# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*


def get_maya_window():
    # 获取maya主界面窗口名称
    window = OpenMayaUI.MQtUtil.mainWindow()
    return shiboken2.wrapInstance(long(window), QtWidgets.QWidget)


def windowExists(parent, name):
    """
    get named window, if window exists, return false; if not, return true..
    """
    if not parent:
        return False

    wnd = parent.findChild(QtWidgets.QMainWindow, name)
    if wnd:
        wnd.show()  # 显示窗口
        wnd.showNormal()  # 最小化的窗口显示回来
        wnd.activateWindow()  # 别的窗口激活状态下，把它激活到最前面来
        return True
    else:
        return False


