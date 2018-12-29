# -*- coding:utf-8 -*-  
# ==========================================
#       author: Pengfei.Ru
#         mail: a773849069@gmail.com
#         time: 2018/12/24
# ==========================================
from cStringIO import StringIO
from PySide2 import QtWidgets
import xml.etree.ElementTree as xml
import Qt
import os
import inspect
if Qt.__binding__ == 'PySide':
    import pysideuic as uic
elif Qt.__binding__ == 'PySide2':
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


def getScriptPath():
    """
    返回脚本路径
    return dir path for used script..
    """
    scriptPath = getModulesPath(inspect.currentframe().f_back)
    return scriptPath


def getModulesPath(moudle):
    """
    返回模块路径
    return dir for imported moudle..
    """
    moduleFile = inspect.getfile(moudle)
    modulePath = os.path.dirname(moduleFile)
    return modulePath
