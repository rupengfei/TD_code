# -*- coding:utf-8 -*-  
# ==========================================
#       author: Pengfei.Ru
#         mail: a773849069@gmail.com
#         time: 2018/12/9
# ==========================================
import maya.cmds as mc
from Utils import uiTool, scriptTool
# from Utils.config import config_seer7
from PySide2 import QtWidgets, QtCore
# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*
# reload(scriptTool)
script_path = scriptTool.getScriptPath()
form_class, base_class = uiTool.loadUiType(script_path + "/seer7_setup.ui")


class Setup(base_class, form_class):
    def __init__(self, parent=uiTool.get_maya_window()):
        self.win_name = "Seer7 Tool"
        self.object_name = "seer7_tool"
        self.dockControl_object_name = self.object_name + "dockControl"
        if mc.dockControl(self.dockControl_object_name, q=True, exists=True):
            mc.deleteUI(self.dockControl_object_name)
        super(Setup, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(self.win_name)
        self.setObjectName(self.object_name)
        mc.dockControl(self.dockControl_object_name,
                       area='right',
                       label=self.win_name,
                       content=str(self.objectName()), allowedArea=('left', 'right'),
                       vis=True)

    @QtCore.Slot(bool)
    def on_btn_export_abc_clicked(self, args=None):
        print "on_btn_export_clicked"

    @QtCore.Slot(bool)
    def on_btn_shaderIOTool_clicked(self, args=None):
        from core.shaderIO import shaderIOUI
        reload(shaderIOUI)
        shaderIO = shaderIOUI.ShaderIO()
        shaderIO.show_win()

    def show_win(self, args=None):
        mc.dockControl(self.dockControl_object_name, e=True, vis=True)
        # uiTool.windowExists(uiTool.get_maya_window(), self.object_name)
        return True

