# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'shaderIO_batch.ui'
#
# Created: Fri Dec 07 15:12:21 2018
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_list_window(object):
    def setupUi(self, list_window):
        list_window.setObjectName("list_window")
        list_window.resize(400, 350)
        list_window.setMinimumSize(QtCore.QSize(400, 350))
        list_window.setAnimated(True)
        self.centralwidget = QtWidgets.QWidget(list_window)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.list_view = QtWidgets.QListView(self.centralwidget)
        self.list_view.setObjectName("list_view")
        self.verticalLayout.addWidget(self.list_view)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_delete_select = QtWidgets.QPushButton(self.centralwidget)
        self.btn_delete_select.setMinimumSize(QtCore.QSize(100, 35))
        self.btn_delete_select.setObjectName("btn_delete_select")
        self.horizontalLayout.addWidget(self.btn_delete_select)
        self.btn_clear_all = QtWidgets.QPushButton(self.centralwidget)
        self.btn_clear_all.setMinimumSize(QtCore.QSize(0, 35))
        self.btn_clear_all.setObjectName("btn_clear_all")
        self.horizontalLayout.addWidget(self.btn_clear_all)
        self.export_all = QtWidgets.QPushButton(self.centralwidget)
        self.export_all.setMinimumSize(QtCore.QSize(100, 35))
        self.export_all.setCursor(QtCore.Qt.PointingHandCursor)
        self.export_all.setObjectName("export_all")
        self.horizontalLayout.addWidget(self.export_all)
        self.verticalLayout.addLayout(self.horizontalLayout)
        list_window.setCentralWidget(self.centralwidget)

        self.retranslateUi(list_window)
        QtCore.QMetaObject.connectSlotsByName(list_window)

    def retranslateUi(self, list_window):
        list_window.setWindowTitle(QtWidgets.QApplication.translate("list_window", "列表窗口", None, -1))
        self.btn_delete_select.setText(QtWidgets.QApplication.translate("list_window", "Delete Select", None, -1))
        self.btn_clear_all.setText(QtWidgets.QApplication.translate("list_window", "Clear All", None, -1))
        self.export_all.setText(QtWidgets.QApplication.translate("list_window", "Export All", None, -1))

