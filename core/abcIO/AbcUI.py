# -*- coding:GBK -*-
# ==========================================
#       author: Pengfei.Ru
#         mail: a773849069@gmail.com
#         time: 2018/12/10
# ==========================================
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
form_class, base_class = uiTool.loadUiType(script_path + "/Abc.ui")


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
        self.__list_model = Abc_mvc_mode.MVC_List_Model(self.list_view, config_seer7.sel_all_Geo())
        self.list_view.setModel(self.__list_model)
        self.list_view.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode(3))

        self.btn_sel_path.setIcon(QtGui.QIcon(script_path + "/icon/file.png"))
        self.on_btn_refresh_setting_clicked()

    def show_win(self, args=None):
        uiTool.windowExists(uiTool.get_maya_window(), self.object_name)
        return True

    @QtCore.Slot(bool)
    def on_btn_sel_path_clicked(self, event):
        # print "btn_sel_path"
        dir_path = QtWidgets.QFileDialog.getExistingDirectory()
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
        print "设置刷新成功"

    @QtCore.Slot(bool)
    def on_btn_refresh_list_clicked(self, args=None):
        geo_name = config_seer7.sel_all_Geo()
        self.__list_model.replace_row(geo_name)
        # self.__list_model.append(geo_name)
        print "列表刷新成功"

    @QtCore.Slot(bool)
    def on_btn_del_sel_clicked(self, args=None):
        self.__list_model.removeRow(sel_items=self.list_view.selectedIndexes())

    @QtCore.Slot(bool)
    def on_btn_export_clicked(self, args=None):
        print "btn_export"

    @QtCore.Slot(bool)
    def on_btn_test_clicked(self, args=None):
        path = self.lin_export_path.text()  # 输出路径
        start = self.float_start.value()  # 起始帧
        end = self.float_end.value()  # 结束帧
        step = self.float_step.value()  # 子步值
        geos = self.__list_model.data(list1=True)  # 列表数据
        print path, "\n", start, "\n", end, "\n", step, "\n", geos
        Abc_Core.abc_export(path, start, end, step, geos)
