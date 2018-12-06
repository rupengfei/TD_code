# -*- coding:utf-8 -*-  
# ==========================================
#       author: Pengfei.Ru
#         mail: a773849069@gmail.com
#         time: 2018/12/5
# ==========================================
# import sys
import maya.cmds as mc
from PySide2 import QtCore, QtGui, QtWidgets
import Utils.uiTool as uiTool
import Utils.scriptTool as scriptTool

# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*
script_path = scriptTool.getScriptPath()
form_class, base_class = uiTool.loadUiType(script_path + "/qt_test1_ui.ui")
window_name = "qt_test1"

class ShaderIO(base_class, form_class):
    def __init__(self, parent=uiTool.get_maya_window()):
        self.window_name = window_name
        if mc.window(self.window_name, exists=True):
            mc.deleteUI(self.window_name)
        super(ShaderIO, self).__init__(parent)
        self.setupUi(self)
        self.setObjectName(window_name)

        desktop = QtWidgets.QApplication.desktop().availableGeometry()
        size = self.geometry()
        self.move((desktop.width() - size.width()) / 2, (desktop.height() - size.height()) / 2)
        self.pf_label.setText("bbbbbbbb")

    @QtCore.Slot(bool)
    def on_btn_pushButton_clicked(self, args=None):
        print "11111"
        print str(self.pf_label.text())
        return True

    @QtCore.Slot(bool)
    def on_pf_text_changeEvent(self, args=None):
        print("pf_textEdit")
        print(dir(self.pf_text()))
        return True

    @QtCore.Slot(bool)
    def show_win(self, args=None):
        uiTool.windowExists(uiTool.get_maya_window(), window_name)
        return True
