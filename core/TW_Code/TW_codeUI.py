# -*- coding:utf-8 -*-
# ==========================================
#       author: Pengfei.Ru
#         mail: 773849069@qq.com
#         QQ: 773849069
#         time: 2018/12/24
# ==========================================
import os
import sys
paths = [os.path.abspath(os.path.dirname(__file__)),
         "C:/cgteamwork/bin/lib/pyside",
         "C:/cgteamwork/bin/lib/pyside/PySide2",
         "D:/___________TD____________/TD_Code",
         "D:/___________TD____________/TD_Code/core",
         ]  # CG Team Work python packages
# paths = ["C:\Python27\Lib\site-packages\PySide2",
#          ]  # PC python packages
print paths
for path in paths:
    path in sys.path or sys.path.append(path)
from PySide2 import QtGui, QtWidgets, QtCore
import utilTool
import subprocess
# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*
script_path = utilTool.getScriptPath()
form_class, base_class = utilTool.loadUiType(script_path + "/TW_code.ui")
QtWidgets.QApplication.addLibraryPath("C:/cgteamwork/bin/lib/pyside/PySide2/plugins")
tw_python = "C:/cgteamwork/python/pythonw.exe"



class Setup(base_class, form_class):
    def __init__(self, parent=None):
        self.win_name = "Seer7 Tool"
        self.object_name = "seer7_tool"
        super(Setup, self).__init__(parent)
        self.setupUi(self)
        self.center()
        self.setWindowTitle(self.win_name)
        self.setObjectName(self.object_name)
        self.setWindowIcon(QtGui.QIcon(script_path + "/icons/R.png"))
        print script_path
        # print dir(self)

    def center(self):
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 5,
                  (screen.height() - size.height()) / 5)

    @QtCore.Slot(bool)
    def on_btn_abc_export_clicked(self, args=None):
        subprocess.Popen(tw_python + " D:/___________TD____________/TD_Code/core/shaderIO/shaderIO_batchUI.py")
        # import shaderIO.shaderIO_batchUI
        # shaderIO.shaderIO_batchUI.main()

    @QtCore.Slot(bool)
    def on_btn_shader_export_clicked(self, args=None):
        print "222222"
        print paths[-1]

def my_win():
    app = QtWidgets.QApplication(sys.argv)
    window = Setup()
    window.show()
    app.exec_()


if __name__ == '__main__':
    my_win()
