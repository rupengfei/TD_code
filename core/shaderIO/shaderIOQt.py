# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'shaderIOQt.ui'
#
# Created: Fri Dec 07 15:07:45 2018
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
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setMinimumSize(QtCore.QSize(100, 35))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setMinimumSize(QtCore.QSize(0, 35))
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
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
        list_window.setWindowTitle(QtWidgets.QApplication.translate("list_window", "批量材质导出", None, -1))
        self.pushButton.setText(QtWidgets.QApplication.translate("list_window", "Delete Select", None, -1))
        self.pushButton_2.setText(QtWidgets.QApplication.translate("list_window", "Clear All", None, -1))
        self.export_all.setText(QtWidgets.QApplication.translate("list_window", "Export All", None, -1))

