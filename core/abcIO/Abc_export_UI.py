# -*- coding:utf-8 -*-
# ==========================================
#       author: Pengfei.Ru
#         mail: a773849069@gmail.com
#         time: 2018/12/10
# ==========================================
import os
import maya.cmds as mc
from Utils import uiTool, scriptTool, mayaTool
from Utils.config import config_seer7
from PySide2 import QtWidgets, QtCore, QtGui
from core.abcIO import Abc_mvc_mode, Abc_Core

# reload(Abc_mvc_mode)
# reload(config_seer7)
# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*
# reload(scriptTool)

script_path = scriptTool.getScriptPath()
form_class, base_class = uiTool.loadUiType(script_path + "/Abc_export.ui")


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
        self.on_btn_refresh_setting_clicked()
        self.on_btn_refresh_list_clicked()

    def show_win(self, args=None):
        uiTool.windowExists(uiTool.get_maya_window(), self.object_name)
        return True

    @QtCore.Slot(bool)
    def on_btn_sel_path_clicked(self, event):
        # print "btn_sel_path"
        dir_path = QtWidgets.QFileDialog.getExistingDirectory(self, u"选择文件夹", self.lin_export_path.text() if self.lin_export_path.text() else "D:/Cache")
        if dir_path:
            self.lin_export_path.setText(dir_path)
            return dir_path
        else:
            return False

    @QtCore.Slot(bool)
    def on_btn_refresh_setting_clicked(self, args=None):
        cam_path = config_seer7.seer7_cam_get_path()
        self.lin_export_path.setText(cam_path)
        playblast_time = mayaTool.get_time_slider()
        self.float_start.setValue(playblast_time[0])
        self.float_end.setValue(playblast_time[1])
        self.float_step.setValue(playblast_time[-1])
        print "重置参数 ok"

    @QtCore.Slot(bool)
    def on_btn_refresh_list_clicked(self, args=None):
        # print
        # reload(config_seer7)
        geo_name = config_seer7.sel_mod(self.check_cam.isChecked(),  # 多选框 相机
                                        self.check_color_set.isChecked(),  # _颜色集
                                        self.check_body.isChecked(),  # ______Geo
                                        self.check_prop.isChecked(),  # ______Prop
                                        self.check_BG.isChecked(),  # ________BG
                                        self.check_other.isChecked(),  # _____其他
                                        )
        self.__list_model.replace_row(geo_name)
        # self.__list_model.append(geo_name)
        print "重置列表 ok"

    @QtCore.Slot(bool)
    def on_btn_del_sel_clicked(self, args=None):
        self.__list_model.removeRow(sel_items=self.list_view.selectedIndexes())

    @QtCore.Slot(bool)
    def on_btn_export_sel_clicked(self, args=None):
        # reload(Abc_Core)
        path = self.lin_export_path.text()  # 输出路径
        if not os.path.exists(path):
            os.makedirs(path)
        start = self.float_start.value()  # 起始帧
        end = self.float_end.value()  # 结束帧
        step = self.float_step.value()  # 子步值
        # TODO:geos
        geos = self.__list_model.selectRow(sel_items=self.list_view.selectedIndexes())  # 列表数据
        print "------------------------------------"
        print path, "\n", start, "\n", end, "\n", step, "\n", geos
        print "------------------------------------"
        Abc_Core.abc_export(path, start, end, step, geos)

    @QtCore.Slot(bool)
    def on_btn_export_clicked(self, args=None):
        path = self.lin_export_path.text()  # 输出路径
        if not os.path.exists(path):
            os.makedirs(path)
        start = self.float_start.value()  # 起始帧
        end = self.float_end.value()  # 结束帧
        step = self.float_step.value()  # 子步值
        geos = self.__list_model.data(list1=True)  # 列表数据
        Abc_Core.abc_export(path, start, end, step, geos)





