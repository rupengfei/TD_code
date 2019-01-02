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
import subprocess
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

def open_mayabatch(version="2017", file=None, command=None, py_command=None, mel_script=None, py_script=None):
    """
    Args:
        version: 2017
        file: r"D:/aaa.ma"
        command: r"file -save"
        py_command: r"print 'happy-----------'"
        mel_script:
        py_script: r"C:\mel.py"

    Returns:subprocess.Popen()
    """
    batch = "C:/Program Files/Autodesk/Maya" + version + "/bin/mayabatch.exe "
    if not file:
        return False
    batch += "-file " + file + " "
    if command:
        batch += "-command \"" + command + "\" "
    if py_command:
        batch += '-command \"python(\\"' + py_command + '\\")\" '
    if mel_script:
        batch += "-script " + mel_script + " "
    if py_script:
        if "\\" in py_script:
            py_script = py_script.replace("\\", "/")
        batch += "-command \"python(\\\"execfile('" + py_script + "')\\\"\") "
    print batch
    subprocess.check_call(batch)


if __name__ == '__main__':
    pass

