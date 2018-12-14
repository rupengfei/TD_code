# -*- coding:utf-8 -*-  
# ==========================================
#       author: Pengfei.Ru
#         mail: a773849069@gmail.com
#         time: 2018/12/10
# ==========================================
import maya.cmds as mc
from Utils import uiTool, scriptTool
# from Utils.config import config_seer7
from PySide2 import QtWidgets, QtCore, QtGui

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
        self.btn_sel_path.setIcon(QtGui.QIcon(script_path + "/icon/file.png"))

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
    def on_check_vis_path_clicked(self, event):
        if event:
            self.lin_export_path.setText("test_cam_sc003_shot007_101_268")

    @QtCore.Slot(bool)
    def on_btn_cjjc_clicked(self, event):
        print self.lin_export_path.text()  # 输出路径
        print self.radio_cf.isChecked()  # 当前帧 bool
        print self.radio_ts.isChecked()  # 时间滑条 bool
        print self.radio_se.isChecked()  # 开始结束 bool
        print self.float_start.value()  # 起始帧
        print self.float_end.value()  # 结束帧
        print self.float_step.value()  # 子步值
        print self.check_cam.isChecked()  # 相机 bool
        print self.check_body.isChecked()  # 人物 bool
        print self.check_color_set.isChecked()  # 颜色集 bool
        print self.check_BG.isChecked()  # BG bool
        print self.check_prop.isChecked()  # 道具 bool
        print self.check_export_sel.isChecked()  # 是否选择导出 bool

    @QtCore.Slot(bool)
    def on_btn_export_clicked():
        print "btn_export"
