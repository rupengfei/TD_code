#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ========================================
#    author: Dango
#      mail: 1007982374@qq.com
#      time: Thu Nov 11 18:43 2018
# ========================================
from PySide2 import QtWidgets, QtCore
import maya.cmds as mc
import os
import Utils.uiTool as uiTool

file_path = str(os.path.split(os.path.realpath(__file__))[0])
form_class, base_class = uiTool.loadUiType(file_path + '/DH_referenceManager.ui')


class DH_referenceManager(base_class, form_class):

    def __init__(self):
        self.window_name = 'DH_referenceManagerWindow'
        if mc.window(self.window_name, exists=True):
            mc.deleteUI(self.window_name)
        super(DH_referenceManager, self).__init__(parent=uiTool.get_maya_window())
        self.setupUi(self)
        desktop = QtWidgets.QApplication.desktop().availableGeometry()
        size = self.geometry()
        self.move((desktop.width() - size.width()) / 2, (desktop.height() - size.height()) / 2)
        self.tableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)  # allow right click pop menu
        self.tableWidget.customContextMenuRequested.connect(self.reference_menu)  # right clicked pop menu
        self.input_path_btn.clicked.connect(self.add_items)
        self.reference_btn.clicked.connect(self.reference_doit)

    def input_file_path(self):  # set asset path
        initial_file_path = self.asset_path_edit.text()
        multiple_filters = "Maya Files (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb);;All Files (*.*)"
        # if os.path.isdir(initial_file_path) or initial_file_path == ''
        input_path = mc.fileDialog2(fileFilter=multiple_filters,
                                    dialogStyle=1,
                                    startingDirectory=initial_file_path,
                                    fileMode=2)
        if input_path:
            self.asset_path_edit.setText(str(input_path).split('\'')[1])
            return str(input_path).split('\'')[1]
        # else:
        #     logging.error("illegal input!!")
        #     return False
        # return True

    def add_items(self):  # add all assets to table
        self.tableWidget.clearContents()
        folder_path = self.input_file_path()
        print folder_path
        # filter = [".ma", ".mb"]
        all_assets = mc.getFileList(folder=folder_path, fs="*.ma")
        all_assets.extend(mc.getFileList(folder=folder_path, fs="*.mb"))
        i = 0
        if all_assets:
            self.tableWidget.setRowCount(len(all_assets))
        for _ in all_assets:
            label = _
            new_item = QtWidgets.QTableWidgetItem(label)
            new_item1 = QtWidgets.QTableWidgetItem(label.split(".")[0])
            new_item2 = QtWidgets.QTableWidgetItem("1")
            self.tableWidget.setItem(i, 0, new_item)
            self.tableWidget.setItem(i, 1, new_item1)
            self.tableWidget.setItem(i, 2, new_item2)
            i += 1
        return True

    def reference_menu(self, pos):  # add menuItems to right click pop menu
        # print pos
        reference_menu = QtWidgets.QMenu()
        item1 = reference_menu.addAction("reference")
        action = reference_menu.exec_(self.tableWidget.mapToGlobal(pos))
        if action == item1:
            self.reference_doit()
        return True

    def reference_preset(self, selected_items):  # set the namespace and refcount before reference
        if selected_items:
            for _ in selected_items:
                # print _
                selected_row = self.tableWidget.indexFromItem(_).row()
                ref_info = list()
                for i in range(3):
                    ref_info.append(self.tableWidget.item(selected_row,i).text())
                    if i == 2:
                        if not (ref_info[2].isalpha()):  # if input number is not an alpha
                            ref_info[2] = int(ref_info[2])
                        else:
                            mc.confirmDialog(t="warning", message="not correct number!!")
                            yield False
                # print ref_info
                yield ref_info

    def reference_doit(self):  # main
        current_dir = self.asset_path_edit.text()
        selected_items = self.tableWidget.selectedItems()
        all_info = self.reference_preset(selected_items)
        # print all_info
        if all_info:
            for ia in all_info:
                for i in range(ia[2]):
                    asset_fullname = current_dir + "/" + ia[0]
                    mc.file(asset_fullname, reference=True, namespace=ia[1])
            return True
        return False

    def show_pic(self, reference_obj):
        """
        pass
        :param reference_obj:
        :return:
        """
