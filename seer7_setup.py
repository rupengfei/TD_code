# -*- coding:utf-8 -*-  
# ==========================================
#       author: Pengfei.Ru
#         mail: a773849069@gmail.com
#         time: 2018/12/9
# ==========================================
import maya.cmds as mc
from Utils import scriptTool
from PySide2 import QtCore
from maya import OpenMayaUI as omui
import maya.mel as mel
from Utils import uiTool
# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*
script_path = scriptTool.getScriptPath()
form_class, base_class = uiTool.loadUiType(script_path + "/seer7_setup.ui")



class Setup(base_class, form_class):
    def __init__(self, parent=uiTool.get_maya_window()):
        self.win_name = "Seer7 Tool"
        self.object_name = "seer7_tool"
        super(Setup, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(self.win_name)
        self.setObjectName(self.object_name)

    @QtCore.Slot(bool)
    def on_btn_export_abc_clicked(self, args=None):
        from core.abcIO import Abc_export_UI
        # reload(Abc_export_UI)
        abc1 = Abc_export_UI.Setup()
        abc1.show_win()

    @QtCore.Slot(bool)
    def on_btn_import_abc_clicked(self, args=None):
        from core.abcIO import Abc_import_UI
        # reload(Abc_import_UI)
        abc1 = Abc_import_UI.Setup()
        abc1.show_win()

    @QtCore.Slot(bool)
    def on_btn_shaderIOTool_clicked(self, args=None):
        from core.shaderIO import shaderIOUI
        # reload(shaderIOUI)
        shaderIO = shaderIOUI.ShaderIO()
        shaderIO.show_win()


def show_win():
    Control_object_name = "seer7_toolControl"
    if not omui.MQtUtil.findControl(Control_object_name):
        seer7 = Setup()
        element = mel.eval('getUIComponentDockControl("Channel Box / Layer Editor", false);')
        mc.workspaceControl(Control_object_name, label="Seer7 Tool",
                            tabToControl=(element, -1),
                            retain=True,
                            r=True, vis=True)
        workspace_ctrl = omui.MQtUtil.findControl(Control_object_name)
        qt_ui = omui.MQtUtil.findControl(seer7.objectName())
        omui.MQtUtil.addWidgetToMayaLayout(long(qt_ui), long(workspace_ctrl))
    else:
        mc.workspaceControl(Control_object_name, e=True, r=True, vis=True)
