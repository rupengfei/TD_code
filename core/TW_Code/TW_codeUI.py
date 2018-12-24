# -*- coding:utf-8 -*-
# ==========================================
#       author: Pengfei.Ru
#         mail: a773849069@gmail.com
#         time: 2018/12/24
# ==========================================
import os
import sys
paths = [os.path.abspath(os.path.dirname(__file__)),
         "C:/cgteamwork/bin/lib/pyside",
         "C:/cgteamwork/bin/lib/pyside/PySide2",
         ]  # CG Team Work python packages
# paths = ["C:\Python27\Lib\site-packages\PySide2",
#          ]  # PC python packages
for path in paths:
    path in sys.path or sys.path.append(path)

from PySide2 import QtGui, QtWidgets, QtCore
import uiTool
# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*
script_path = uiTool.getScriptPath()
form_class, base_class = uiTool.loadUiType(script_path + "/TW_code.ui")
QtWidgets.QApplication.addLibraryPath("C:/cgteamwork/bin/lib/pyside/PySide2/plugins")


class Setup(base_class, form_class):
    def __init__(self, parent=None):
        self.win_name = "Seer7 Tool"
        self.object_name = "seer7_tool"
        super(Setup, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(self.win_name)
        self.setObjectName(self.object_name)

def my_win():
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    my_win()
