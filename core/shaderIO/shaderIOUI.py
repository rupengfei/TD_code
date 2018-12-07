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
from core.shaderIO import shader_mvc_model, shaderIOQt

reload(shader_mvc_model)
reload(shaderIOQt)

# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*
# script_path = scriptTool.getScriptPath()
# form_class, base_class = uiTool.loadUiType(script_path + "/shaderIOQt.ui")
win_name = "shaderIO"


# class ShaderIO(base_class, form_class):
class ShaderIO(shaderIOQt.Ui_list_window, QtWidgets.QMainWindow):
    def __init__(self, parent=uiTool.get_maya_window()):
        self.window_name = win_name
        if mc.window(self.window_name, exists=True):
            mc.deleteUI(self.window_name)
        super(ShaderIO, self).__init__(parent)
        self.setupUi(self)
        self.__list_model = shader_mvc_model.MVC_List_Model(self.list_view)
        self.list_view.setModel(self.__list_model)
        self.list_view.setDragEnabled(True)
        self.list_view.setAcceptDrops(True)
        self.list_view.setDropIndicatorShown(True)
        # self.list_view.visualRegionForSelection(QtCore.QAbstractItemView.selectedIndexes())
        # self.list_view.selectionChanged = self.list_view_selectionChanged
        self.list_view.mouseMoveEvent = self.drag_move_event
        self.list_view.dragEnterEvent = self.list_view_dragEnterEvent
        self.list_view.dragMoveEvent = self.drag_move_event
        self.list_view.dropEvent = self.list_view_dropEvent
        # self.list_view.clicked = self.list_view_clicked
        self.setWindowTitle("ShaderIO Tool")
        self.setObjectName(win_name)
        desktop = QtWidgets.QApplication.desktop().availableGeometry()
        size = self.geometry()
        self.move((desktop.width() - size.width()) / 2, (desktop.height() - size.height()) / 2)
        # self.__current_dir = ''

    def list_view_dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            print("dragEnter")
            event.acceptProposedAction()

    def drag_move_event(self, event):
        pass

    def list_view_dropEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                # print self.list_view.
                print url.toString()
                self.__list_model.insertRow(url.toString()[8:])
                # self.list_view.addItem(url.toString()[8:])
            event.acceptProposedAction()

    # def list_view_clicked(self):
    #     print "111"

    @QtCore.Slot(bool)
    def on_export_all_clicked(self, event):
        print "export_all"
        print self.__list_model.data(list1=True)

    def show_win(self, args=None):
        uiTool.windowExists(uiTool.get_maya_window(), win_name)
        return True
