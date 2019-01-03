# -*- coding:utf-8 -*-  
# ==========================================
#       author: Pengfei.Ru
#         mail: a773849069@gmail.com
#         time: 2018/12/3
# ==========================================
import os
import sys
# os.path.abspath(os.path.dirname(__file__)),
# paths = ["C:\Program Files\Autodesk\Maya2017\Python\Lib\site-packages",
paths = ["C:/cgteamwork/bin/lib/pyside",
         # "C:\Program Files\Autodesk\Maya2017\Python\Lib\site-packages\PySide2",
         "C:/cgteamwork/bin/lib/pyside/PySide2",
         # "D:/___________TD____________/TD_Code",
         # "D:/___________TD____________/TD_Code/core",
         "Z:/SEER7/bin/rupengfei/TD_code",
         "Z:/SEER7/bin/rupengfei/TD_code/core",
         "C:/cgteamwork/bin/lib/pyside/PySide2/plugins"
         ]  # CG Team Work python packages
# paths = ["C:\Python27\Lib\site-packages\PySide2",
#          ]  # PC python packages
for path in paths:
    path in sys.path or sys.path.append(path)

from PySide2 import QtGui, QtWidgets, QtCore
import TW_Code.utilTool as utilTool
import shaderIO_batch_mvc_model

# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*
script_path = utilTool.getScriptPath()
form_class, base_class = utilTool.loadUiType(script_path + "/shaderIO_batch.ui")
QtWidgets.QApplication.addLibraryPath("C:/cgteamwork/bin/lib/pyside/PySide2/plugins")








class ShaderIO(base_class, form_class):
    # class ShaderIO(shaderIO_batch.Ui_list_window, QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        self.window_name = "shaderIO"
        self.obj_name = "shaderIO"
        super(ShaderIO, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(self.window_name)
        self.setObjectName(self.obj_name)
        desktop = QtWidgets.QApplication.desktop().availableGeometry()
        size = self.geometry()
        self.move((desktop.width() - size.width()) / 2, (desktop.height() - size.height()) / 2)

        self.__list_model = shaderIO_batch_mvc_model.MVC_List_Model(self.list_view)
        self.list_view.setModel(self.__list_model)
        self.list_view.setAcceptDrops(True)  # 拖拽接收开启
        self.list_view.setDragEnabled(True)  # 拖拽反馈开启
        self.list_view.dragEnterEvent = self.list_view_dragEnterEvent  # 拖拽启动事件
        self.list_view.dragMoveEvent = self.list_view_dragMoveEvent  # 拖拽移动事件
        self.list_view.dropEvent = self.list_view_dropEvent  # 拖拽松开事件
        self.list_view.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode(3))

        # self.list_view.mouseMoveEvent = self.mouse_double_clicked_event  # 鼠标移动事件
        # self.list_view.mouseDoubleClickEvent = self.get_sel_item  # 鼠标双击事件

    def list_view_dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.ignore()
            event.acceptProposedAction()

    def list_view_dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.ignore()
            event.acceptProposedAction()

    def list_view_dropEvent(self, event):
        # print "11111"
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                self.__list_model.append(url.toString()[8:])
            event.acceptProposedAction()

    def get_sel_item(self, event):
        print self.list_view.selectedIndexes()
        print self.__list_model.sel_item(self.list_view.selectedIndexes()[0])
        # print self.list_view.selectedIndexes()[0].text()

    # @QtCore.Slot(bool)
    # def on_list_view_selectedIndexes(self, event):
    #     print "aaa"
    #     # QMessageBox.information(self, 'ListWidget', '你选择了：' + self.qList[qModelIndex.row()])

    @QtCore.Slot(bool)
    def on_btn_delete_select_clicked(self, event):
        self.__list_model.removeRow(sel_items=self.list_view.selectedIndexes())

    @QtCore.Slot(bool)
    def on_btn_clear_all_clicked(self, event):
        self.__list_model.replace_row()

    @QtCore.Slot(bool)
    def on_export_all_clicked(self, event):
        # self.__list_model.selectRow(sel_items=self.list_view.selectedIndexes())
        list_all = self.__list_model.data(list1=True)
        # utilTool.open_mayabatch(list_all)
        child_process = int(self.comboBox_child.currentText())
        B_child = int(self.comboBox_child.currentText())
        if self.comboBox_project.currentText() == "Seer7":
            for _file in list_all:
                if os.path.isfile(_file):
                    print "opening on python child %s" % B_child
                    if B_child == 1:
                        B_child = child_process
                        utilTool.open_mayabatch(file=_file,
                                                tracking=True,
                                                mel_script=r"Z:/SEER7/bin/rupengfei/TD_code/Utils/config/seer7_shader_batch.mel")
                    else:
                        B_child -= 1
                        utilTool.open_mayabatch(file=_file,
                                                mel_script=r"Z:/SEER7/bin/rupengfei/TD_code/Utils/config/seer7_shader_batch.mel")
                else:
                    print "{0} <<<<<----- is not file".format(_file)
        if self.comboBox_project.currentText() == "None":
            print "nothing"

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ShaderIO()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

