# -*- coding:utf-8 -*-  
# ==========================================
#       author: Pengfei.Ru
#         mail: a773849069@gmail.com
#         time: 2018/12/3
# ==========================================
# import sys
import os
import maya.cmds as mc
from PySide2 import QtCore, QtGui, QtWidgets
from Utils import uiTool, scriptTool, mayaTool

# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*
script_path = scriptTool.getScriptPath()
form_class, base_class = uiTool.loadUiType(script_path + "/shaderIOQt.ui")
win_name = "rpf_shaderIO"


class ShaderIO(base_class, form_class):
    def __init__(self, parent=uiTool.get_maya_window()):
        self.window_name = win_name
        if mc.window(self.window_name, exists=True):
            mc.deleteUI(self.window_name)
        super(ShaderIO, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("ShaderIO Tool")
        self.setObjectName(win_name)
        desktop = QtWidgets.QApplication.desktop().availableGeometry()
        size = self.geometry()
        self.move((desktop.width() - size.width()) / 2, (desktop.height() - size.height()) / 2)
        # self.__current_dir = ''

        self.list_widget.setDragEnabled(True)
        self.list_widget.setAcceptDrops(True)
        self.list_widget.setDropIndicatorShown(True)
        # self.list_widget.selectionChanged = self.list_widget_selectionChanged
        self.list_widget.mouseMoveEvent = self.drag_move_event
        self.list_widget.dragEnterEvent = self.list_widget_dragEnterEvent
        self.list_widget.dragMoveEvent = self.drag_move_event
        self.list_widget.dropEvent = self.list_widget_dropEvent



    def list_widget_dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            print("dragEnter")
            event.acceptProposedAction()

    def drag_move_event(self, event):
        pass

    def list_widget_dropEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                # print self.list_widget.
                print url.toString()
                self.list_widget.addItem(url.toString()[8:])
            event.acceptProposedAction()

    @QtCore.Slot(bool)
    def on_list_widget_pressed(self):
        print "111"

    def list_widget_selectionChanged(self, ):
        print "111"

    def show_win(self, args=None):
        uiTool.windowExists(uiTool.get_maya_window(), win_name)
        return True

