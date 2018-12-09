# -*- coding:utf-8 -*-  
# ==========================================
#       author: Pengfei.Ru
#         mail: a773849069@gmail.com
#         time: 2018/12/9
# ==========================================
import sys
import os
import maya.cmds as mc
import pymel.core as pm
from Utils import uiTool,scriptTool,mayaTool
from PySide2 import QtWidgets,QtCore
# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*
script_path = scriptTool.getScriptPath()
form_class, base_class = uiTool.loadUiType(script_path + "/seer7_setup.ui")
win_name = "Seer7 Tool"

class Setup(base_class, form_class):
    def __init__(self, parent=uiTool.get_maya_window()):
        self.window_name = win_name
        if mc.window(self.window_name, exists=True):
            mc.deleteUI(self.window_name)
        super(Setup, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(win_name)
        self.setObjectName(win_name)
        desktop = QtWidgets.QApplication.desktop().availableGeometry()
        size = self.geometry()
        self.move((desktop.width() - size.width()) / 2, (desktop.height() - size.height()) / 2)

    @QtCore.Slot(bool)
    def on_btn1_clicked(self, args=None):
        print "1111"

    @QtCore.Slot(bool)
    def on_btn2_clicked(self, args=None):
        print "22222"

    @QtCore.Slot(bool)
    def on_btn3_clicked(self, args=None):
        print "33333"

    @QtCore.Slot(bool)
    def on_btn_export_clicked(self, args=None):
        sels = mayaTool.sel_Geo()
        # from core.shaderIO import shaderCore
        for sel in sels:
            print sel

    @QtCore.Slot(bool)
    def on_btn_import_clicked(self, args=None):
        print "on_btn_export_clicked"

    def show_win(self, args=None):
        uiTool.windowExists(uiTool.get_maya_window(), win_name)
        return True

