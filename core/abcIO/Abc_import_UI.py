# -*- coding:utf-8 -*-  
# ==========================================
#       author: Pengfei.Ru
#         mail: a773849069@gmail.com
#         time: 2018/12/18
# ==========================================
import os.path
import maya.cmds as mc
from Utils import uiTool, scriptTool
from Utils.config import config_seer7
from PySide2 import QtWidgets, QtCore, QtGui
from core.abcIO import Abc_mvc_mode, Abc_Core

# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*

script_path = scriptTool.getScriptPath()
form_class, base_class = uiTool.loadUiType(script_path + "/Abc_import.ui")


class Setup(base_class, form_class):
    def __init__(self, parent=uiTool.get_maya_window()):
        self.win_name = "ABC IO"
        self.object_name = "abc_io"
        if mc.window(self.object_name, q=True, exists=True):
            mc.deleteUI(self.object_name)
        super(Setup, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(self.win_name)
        self.setObjectName(self.object_name)
        self.__list_model = Abc_mvc_mode.MVC_List_Model(self.list_view)
        self.list_view.setModel(self.__list_model)
        self.list_view.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode(3))
        self.btn_sel_path.setIcon(QtGui.QIcon(script_path + "/icon/file.png"))

    def show_win(self, args=None):
        uiTool.windowExists(uiTool.get_maya_window(), self.object_name)
        return True

    @QtCore.Slot()
    def on_lin_path_returnPressed(self):
        dir_path = self.lin_path.text()
        # reload(config_seer7)
        if os.path.exists(dir_path):
            self.__list_model.replace_row(config_seer7.seer7_find_files(dir_path, take_fix=False))

    @QtCore.Slot(bool)
    def on_btn_sel_path_clicked(self, event):
        dir_path = QtWidgets.QFileDialog.getExistingDirectory(self, "选择镜头文件夹",
                                                              self.lin_path.text())
        if dir_path:
            self.lin_path.setText(dir_path)
            # reload(config_seer7)
            self.__list_model.replace_row(config_seer7.seer7_find_files(dir_path, take_fix=False))

    @QtCore.Slot(bool)
    def on_btn_import_sel_clicked(self, args=None):
        sels = list()
        for sel in self.list_view.selectedIndexes():
            sels.append(sel.data())
        if sels:
            # reload(Abc_Core)
            Abc_Core.abc_import(self.lin_path.text(), sels)

    @QtCore.Slot(bool)
    def on_btn_import_all_clicked(self, args=None):
        Abc_Core.abc_import(self.lin_path.text(), self.__list_model.data(list1=True))

    @QtCore.Slot(bool)
    def on_btn_test_clicked(self, args=None):
        # reload(config_seer7)
        print "------------------------------------"
        print self.lin_path.text()
        print config_seer7.seer7_find_files(self.lin_path.text())
        print
        print "------------------------------------"
