# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mvc_qt.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 467)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.tab)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.listView = QtWidgets.QListView(self.tab)
        self.listView.setObjectName("listView")
        self.horizontalLayout.addWidget(self.listView)
        self.listView_2 = QtWidgets.QListView(self.tab)
        self.listView_2.setObjectName("listView_2")
        self.horizontalLayout.addWidget(self.listView_2)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.btn_lsv_insert = QtWidgets.QPushButton(self.tab)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_lsv_insert.setFont(font)
        self.btn_lsv_insert.setObjectName("btn_lsv_insert")
        self.verticalLayout_2.addWidget(self.btn_lsv_insert)
        self.btn_lsv_remove = QtWidgets.QPushButton(self.tab)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_lsv_remove.setFont(font)
        self.btn_lsv_remove.setObjectName("btn_lsv_remove")
        self.verticalLayout_2.addWidget(self.btn_lsv_remove)
        self.btn_lsv_clear = QtWidgets.QPushButton(self.tab)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_lsv_clear.setFont(font)
        self.btn_lsv_clear.setObjectName("btn_lsv_clear")
        self.verticalLayout_2.addWidget(self.btn_lsv_clear)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.tab_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tableView = QtWidgets.QTableView(self.tab_2)
        self.tableView.setObjectName("tableView")
        self.horizontalLayout_2.addWidget(self.tableView)
        self.tableView_2 = QtWidgets.QTableView(self.tab_2)
        self.tableView_2.setObjectName("tableView_2")
        self.horizontalLayout_2.addWidget(self.tableView_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.btn_tbv_insert = QtWidgets.QPushButton(self.tab_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_tbv_insert.setFont(font)
        self.btn_tbv_insert.setObjectName("btn_tbv_insert")
        self.verticalLayout_3.addWidget(self.btn_tbv_insert)
        self.btn_tbv_remove = QtWidgets.QPushButton(self.tab_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_tbv_remove.setFont(font)
        self.btn_tbv_remove.setObjectName("btn_tbv_remove")
        self.verticalLayout_3.addWidget(self.btn_tbv_remove)
        self.btn_tbv_clear = QtWidgets.QPushButton(self.tab_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_tbv_clear.setFont(font)
        self.btn_tbv_clear.setObjectName("btn_tbv_clear")
        self.verticalLayout_3.addWidget(self.btn_tbv_clear)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.tabWidget.addTab(self.tab_2, "")
        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_lsv_insert.setText(_translate("MainWindow", "Insert..."))
        self.btn_lsv_remove.setText(_translate("MainWindow", "Remove"))
        self.btn_lsv_clear.setText(_translate("MainWindow", "Clear"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "List View"))
        self.btn_tbv_insert.setText(_translate("MainWindow", "Insert..."))
        self.btn_tbv_remove.setText(_translate("MainWindow", "Remove"))
        self.btn_tbv_clear.setText(_translate("MainWindow", "Clear"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Table View"))
