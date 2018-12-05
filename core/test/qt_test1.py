# -*- coding:utf-8 -*-  
# ==========================================
#       author: Pengfei.Ru
#         mail: a773849069@gmail.com
#         time: 2018/12/5
# ==========================================
# import sys
# from PySide2 import QtCore, QtGui, QtWidgets
import Utils.uiTool as uiTool
import Utils.scriptTool as scriptTool
# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*
script_path = scriptTool.getScriptPath()
form_class, base_class = uiTool.loadUiType(script_path + "/qt_test1_ui.ui")


class ShaderIO(base_class, form_class):
    def __init__(self, parent=uiTool.get_maya_window()):
        self.window_name = 'qt_test_ui'
        super(ShaderIO, self).__init__(parent)
        self.setupUi(self)
        # self.__current_dir = ''

    def show_win(self):
        uiTool.windowExists(uiTool.get_maya_window(), "qt_test_ui")

