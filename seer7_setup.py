# -*- coding:utf-8 -*-  
# ==========================================
#       author: Pengfei.Ru
#         mail: a773849069@gmail.com
#         time: 2018/12/9
# ==========================================
import maya.cmds as mc
from Utils import scriptTool, uiTool
from PySide2 import QtCore
from maya import OpenMayaUI as omui
import maya.mel as mel
# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*
script_path = scriptTool.getScriptPath()
form_class, base_class = uiTool.loadUiType(script_path + "/seer7_setup.ui")



class Setup(base_class, form_class):
    def __init__(self, parent=uiTool.get_maya_window()):
        self.win_name = "Seer7 Tool"
        self.object_name = "seer7_tool"
        if mc.window(self.object_name, q=True, exists=True):
            mc.deleteUI(self.object_name)
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
    def on_btn_load_render_ref_clicked(self, args=None):
        from Utils.config import config_seer7
        config_seer7.references_replace_render()

    @QtCore.Slot(bool)
    def on_btn_load_anim_ref_clicked(self, args=None):
        from Utils.config import config_seer7
        config_seer7.references_replace_anim()

    @QtCore.Slot(bool)
    def on_btn_load_all_ref_clicked(self, args=None):
        from Utils.config import config_seer7
        config_seer7.references_replace_all()

    @QtCore.Slot(bool)
    def on_btn_shaderIOTool_clicked(self, args=None):
        from core.shaderIO import shaderIOUI
        # reload(shaderIOUI)
        shaderIO = shaderIOUI.ShaderIO()
        shaderIO.show_win()

    @QtCore.Slot(bool)
    def on_btn_aoto_fur_bs_clicked(self, args=None):
        from core.fur import hair_core
        reload(hair_core)
        hair_core.import_fur_BS()

    @QtCore.Slot(bool)
    def on_btn_setAttr_tool_clicked(self, args=None):
        from core import Attr_tool
        Attr_tool.AttrTool()

def show_win():
    Control_object_name = "seer7_toolControl"  # 窗口名
    if not omui.MQtUtil.findControl(Control_object_name):  # 如果窗口不存在
        seer7 = Setup()  # 初始化任何一个qt的窗口，里边写啥都行能出窗口就行
        element = mel.eval('getUIComponentDockControl("Channel Box / Layer Editor", false);')  # 找到侧边栏位置
        mc.workspaceControl(Control_object_name, label="Seer7 Tool",  # 创建一个maya窗口布局用于接收Qt窗口
                            tabToControl=(element, -1),  # 窗口位置  侧边栏
                            retain=True,  # 关闭窗口之后是否保留  False就是杀死窗口下次还得创建
                            r=True,  # 显示到前边
                            vis=True)  # 显示
        workspace_ctrl = omui.MQtUtil.findControl(Control_object_name)  # 获取 maya 窗口控件的对象
        qt_ui = omui.MQtUtil.findControl(seer7.objectName())  # 获取 Qt 窗口控件的对象
        omui.MQtUtil.addWidgetToMayaLayout(long(qt_ui), long(workspace_ctrl))  # 把Qt的窗口添加到maya的窗口
    else:  # 窗口存在的话
        mc.workspaceControl(Control_object_name, e=True, r=True, vis=True)  # 显示窗口

def test_win():
    seer7_wins = Setup()
    seer7_wins.show()
    seer7_wins.showNormal()
    seer7_wins.activateWindow()