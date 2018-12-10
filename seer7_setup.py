# -*- coding:utf-8 -*-  
# ==========================================
#       author: Pengfei.Ru
#         mail: a773849069@gmail.com
#         time: 2018/12/9
# ==========================================
import maya.cmds as mc
from Utils import uiTool, scriptTool
from Utils.config import config_seer7
from PySide2 import QtWidgets, QtCore
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
        self.lin_import.setAcceptDrops(True)  # 拖拽接收开启
        self.lin_import.setDragEnabled(True)  # 拖拽反馈开启
        self.lin_import.dragEnterEvent = self.lin_import_dragEnterEvent  # 拖拽启动事件
        # self.lin_import.dragMoveEvent = self.lin_import_dragMoveEvent  # 拖拽移动事件
        self.lin_import.dropEvent = self.lin_import_dropEvent  # 拖拽松开事件

    @QtCore.Slot(bool)
    def on_btn_export_sel_shader_clicked(self, args=None):
        config_seer7.export_sel_shader(self.lin_export.text())

    @QtCore.Slot(bool)
    def on_btn_export_shader_clicked(self, args=None):
        config_seer7.export_all_shader(self.lin_export.text())

    def lin_import_dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    # def lin_import_dragMoveEvent(self, event):
    #     print "11122"

    def lin_import_dropEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                self.lin_import.setText(url.toString()[8:])
            event.acceptProposedAction()

    # @QtCore.Slot(bool)
    # def on_btn_import_sel_shader_clicked(self, args=None):
    #     config_seer7.import_sel_shader(self.lin_import.text(), self.lin_namespace.text())

    @QtCore.Slot(bool)
    def on_btn_import_shader_clicked(self, args=None):
        if self.lin_namespace.text():
            config_seer7.import_all_shader(self.lin_import.text(), self.lin_namespace.text())
        else:
            config_seer7.import_all_shader(self.lin_import.text())


    @QtCore.Slot(bool)
    def on_btn_aoto_export_clicked(self, args=None):
        config_seer7.aoto_export_shader()

    # @QtCore.Slot(bool)
    # def on_btn1_clicked(self, args=None):
    #     print "on_btn_export_clicked"

    def show_win(self, args=None):
        uiTool.windowExists(uiTool.get_maya_window(), win_name)
        return True

