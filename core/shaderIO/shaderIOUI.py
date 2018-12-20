# -*- coding:utf-8 -*-  
# ==========================================
#       author: Pengfei.Ru
#         mail: a773849069@gmail.com
#         time: 2018/12/13
# ==========================================
import maya.cmds as mc
from Utils import uiTool, scriptTool
from Utils.config import config_seer7
from PySide2 import QtWidgets, QtCore
from core.shaderIO import shaderCore
# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*
# reload(scriptTool)
script_path = scriptTool.getScriptPath()
form_class, base_class = uiTool.loadUiType(script_path + "/shaderIO.ui")


class ShaderIO(base_class, form_class):
    def __init__(self, parent=uiTool.get_maya_window()):
        print "shaderIOUI start"
        self.win_name = "Shader Tool"
        self.object_name = "shader_tool"
        # self.dockControl_object_name = self.object_name + "dockControl"
        if mc.window(self.object_name, exists=True):
            mc.deleteUI(self.object_name)
        super(ShaderIO, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(self.win_name)
        self.setObjectName(self.object_name)
        desktop = QtWidgets.QApplication.desktop().availableGeometry()
        size = self.geometry()
        self.move((desktop.width() - size.width()) / 2, (desktop.height() - size.height()) / 2)
        self.lin_import.setAcceptDrops(True)  # 拖拽接收开启
        self.lin_import.setDragEnabled(True)  # 拖拽反馈开启
        self.lin_import.dragEnterEvent = self.lin_import_dragEnterEvent  # 拖拽启动事件
        # self.lin_import.dragMoveEvent = self.lin_import_dragMoveEvent  # 拖拽移动事件
        self.lin_import.dropEvent = self.lin_import_dropEvent  # 拖拽松开事件
        self.btn_import_sel_shader.setEnabled(False)
        self.btn_auto_import.setEnabled(False)
        # mc.dockControl(self.dockControl_object_name,
        #                area='right',
        #                label=self.win_name,
        #                content=str(self.objectName()), allowedArea=('left', 'right'),
        #                vis=True)

    @QtCore.Slot(bool)
    def on_btn_export_sel_shader_clicked(self, args=None):
        shaderCore.export_sel_shader(self.lin_export.text())

    @QtCore.Slot(bool)
    def on_btn_export_shader_clicked(self, args=None):
        shaderCore.export_all_shader(self.lin_export.text())

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
            shaderCore.import_all_shader(self.lin_import.text(), self.lin_namespace.text())
        else:
            shaderCore.import_all_shader(self.lin_import.text())


    @QtCore.Slot(bool)
    def on_btn_auto_export_clicked(self, args=None):
        config_seer7.auto_export_shader()

    @QtCore.Slot(bool)
    def on_btn_batch_export_clicked(self, args=None):
        print "aaaaa"
        from core.shaderIO import shaderIO_batchUI
        # reload(shaderIO_batchUI)
        batch_IO = shaderIO_batchUI.ShaderIO()
        batch_IO.show_win()

    def show_win(self, args=None):
        uiTool.windowExists(uiTool.get_maya_window(), self.object_name)
        return True

