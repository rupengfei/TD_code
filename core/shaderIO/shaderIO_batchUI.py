# -*- coding:utf-8 -*-  
# ==========================================
#       author: Pengfei.Ru
#         mail: a773849069@gmail.com
#         time: 2018/12/3
# ==========================================
import os
import maya.cmds as mc
from PySide2 import QtCore, QtGui, QtWidgets
from Utils import uiTool, scriptTool  # , mayaTool
# from core.shaderIO import shader_mvc_model  # , shaderIO_batch
from core.shaderIO import shader_mvc_model

# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*
script_path = scriptTool.getScriptPath()
form_class, base_class = uiTool.loadUiType(script_path + "/shaderIO_batch.ui")
win_name = "shaderIO"


class ShaderIO(base_class, form_class):
    # class ShaderIO(shaderIO_batch.Ui_list_window, QtWidgets.QMainWindow):
    def __init__(self, parent=uiTool.get_maya_window()):
        self.__drag_pos = (0, 0)
        self.window_name = win_name
        if mc.window(self.window_name, exists=True):
            mc.deleteUI(self.window_name)
        super(ShaderIO, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("......")
        self.setObjectName(win_name)
        desktop = QtWidgets.QApplication.desktop().availableGeometry()
        size = self.geometry()
        self.move((desktop.width() - size.width()) / 2, (desktop.height() - size.height()) / 2)

        self.__list_model = shader_mvc_model.MVC_List_Model(self.list_view)
        self.list_view.setModel(self.__list_model)
        self.list_view.setAcceptDrops(True)  # 拖拽接收开启
        self.list_view.setDragEnabled(True)  # 拖拽反馈开启
        self.list_view.dragEnterEvent = self.list_view_dragEnterEvent  # 拖拽启动事件
        self.list_view.dragMoveEvent = self.list_view_dragMoveEvent  # 拖拽移动事件
        self.list_view.dropEvent = self.list_view_dropEvent  # 拖拽松开事件

        # self.list_view.mouseMoveEvent = self.mouse_double_clicked_event  # 鼠标移动事件
        self.list_view.mouseDoubleClickEvent = self.get_sel_item  # 鼠标双击事件
        self.list_view.mouseReleaseEvent = self.mouse_release_event
        self.list_view.releaseMouse()
        # self.list_view.mouseGrabber = self.mouse_grabber_event
        # self.list_view.mousePressEvent = self.mouse_press_event
        # self.__current_dir = ''
        # self.__list_model = shader_mvc_model.DnDListWidget(self.list_view)
        # self.list_view.setModel(self.__list_model)

    def list_view_dragEnterEvent(self, event):
        print "dragEnterEvent"
        # self.__drag_pos = (event.pos().x(), event.pos().y())
        if event.mimeData().hasUrls():
            print event.pos().x(), event.pos().y()
            event.acceptProposedAction()

    def list_view_dragMoveEvent(self, event):
        event.ignore()
        # print dir(event)
        # print event.pos().x(), event.pos().y()
        # if event.mimeData().hasUrls():
        #     print event.pos().x(), event.pos().y()
        #     event.acceptProposedAction()

    def list_view_dropEvent(self, event):
        print "11111"
        # if event.mimeData().hasUrls():
        #     for url in event.mimeData().urls():
        #         self.__list_model.append(url.toString()[8:])
        #     event.acceptProposedAction()

    def mouse_double_clicked_event(self, event):
        print "double_clicked"
        print event

    def mouse_release_event(self, event):
        print "release_event"
        print event

    # def mouse_grabber_event(self):
    #     print "mouse_grabber_event"

    # def mouse_press_event(self, event):
    #     print "mouse_Press_event"
    #     print event

    def get_sel_item(self, event):
        print self.__list_model.sel_item(self.list_view.selectedIndexes()[0])
        # print self.list_view.selectedIndexes()[0].text()

    @QtCore.Slot(bool)
    def on_list_view_selectedIndexes(self, qModelIndex):
        print "aaa"
        # QMessageBox.information(self, 'ListWidget', '你选择了：' + self.qList[qModelIndex.row()])

    @QtCore.Slot(bool)
    def on_btn_delete_select_clicked(self, event):
        self.__list_model.removeRow(sel_items=self.list_view.selectedIndexes())

    @QtCore.Slot(bool)
    def on_btn_clear_all_clicked(self, event):
        self.__list_model.fanhui_index()

    @QtCore.Slot(bool)
    def on_export_all_clicked(self, event):
        print "export_all"
        print self.__list_model.data(list1=True)
        print self.__list_model.my_sel()
        print self.__list_model.currentText()

    def show_win(self, args=None):
        uiTool.windowExists(uiTool.get_maya_window(), win_name)
        return True


if __name__ == "__main__":
    pass

