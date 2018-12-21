# -*- coding:utf-8 -*-  
# ==========================================
#       author: Pengfei.Ru
#         mail: a773849069@gmail.com
#         time: 2018/12/3
# ==========================================

from cStringIO import StringIO
from PySide2 import QtWidgets
import xml.etree.ElementTree as xml
import Utils.Qt as Qt

if Qt.__binding__ == 'PySide':
    from shiboken import wrapInstance
    import pysideuic as uic
elif Qt.__binding__ == 'PySide2':
    from shiboken2 import wrapInstance
    import pyside2uic as uic
# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*


def loadUiType(uiFile):
    # 加载 ui 文件
    parsed = xml.parse(uiFile)
    widget_class = parsed.find('widget').get('class')
    form_class = parsed.find('class').text

    with open(uiFile, 'r') as f:
        o = StringIO()
        frame = {}

        uic.compileUi(f, o, indent=0)
        pyc = compile(o.getvalue(), '<string>', 'exec')
        exec pyc in frame

        # Fetch the base_class and form class based on their type in the xml from designer
        form_class = frame['Ui_%s' % form_class]
        base_class = getattr(QtWidgets, widget_class)
        return form_class, base_class


def get_maya_window():
    # 获取maya主界面窗口名称
    import maya.OpenMayaUI as OpenMayaUI
    window = OpenMayaUI.MQtUtil.mainWindow()
    return wrapInstance(long(window), QtWidgets.QWidget)


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


