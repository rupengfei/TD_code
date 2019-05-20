# -*- coding=utf-8 -*-
# ==========================================
#       author: Ruben
#         mail: 773849069@qq.com
#         time: 2019/5/17
# ==========================================
from PyQt4 import QtGui, QtCore
import sys
import os
import json

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*
config = {
    "deskTop_screenCount": 1,
    "menu": [
        {
            "label": u"@百度",
            "open": r"https://www.baidu.com/"
        },
        {
            "label": u"@CSDN",
            "open": "https://www.csdn.net/"
        },
        {
            "label": "",
            "open": ""
        },
        {
            "label": u"打开配置",
            "open": r"ATconfig.json"
        },
    ]
}
config_file = "ATconfig.json"
if os.path.isfile(config_file):
    try:
        with open(config_file, "r")as f:
            config = json.loads(f.read())
    except ValueError:
        with open(config_file, "w")as f:
            f.write(json.dumps(config, indent=4))
else:
    with open(config_file, "w")as f:
        f.write(json.dumps(config, indent=4))


class AngleTool(QtGui.QWidget):
    def __init__(self):
        super(AngleTool, self).__init__(None)
        self.desktop = QtGui.QApplication.desktop()
        self.deskRect = self.desktop.screenGeometry(self.desktop.screenCount())
        self.topBtn = QtGui.QPushButton('')
        self.topBtn.setMinimumSize(25, 25)
        self.topBtn.setStyleSheet('QWidget {border-image: url("icons/windowIcon.png");}')
        # self.topBtn.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.topBtn.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool | QtCore.Qt.Popup)

        self.topBtn.move(self.deskRect.x() - 1, self.deskRect.y() - 1)
        self.topBtn.show()
        self.topBtn.mousePressEvent = self.menuWin
        self.config_win = None
        self.menu_win = None
        self.config = config

    def menuWin(self, *args):
        if self.menu_win:
            self.menu_win.move(QtGui.QCursor().pos())
            self.menu_win.show()
            return

        self.menu_win = QtGui.QMenu()

        for menu in self.config.get('menu', []):
            tmpAction = QtGui.QAction(menu.get('label'), self.menu_win)
            if menu.get('open'):
                tmpAction.triggered.connect(self.menuWin_start_exe(menu['open']))
            else:
                self.menu_win.addSeparator()
                continue
            self.menu_win.addAction(tmpAction)

        self.menu_win.addSeparator()
        tmpAction = QtGui.QAction(u'配置工具列表', self.menu_win)
        tmpAction.triggered.connect(self.configWin)
        self.menu_win.addAction(tmpAction)
        tmpAction = QtGui.QAction(u'退出', self.menu_win)
        tmpAction.triggered.connect(self.close)
        self.menu_win.addAction(tmpAction)
        self.menu_win.move(QtGui.QCursor().pos())
        self.menu_win.show()
        return

    @staticmethod
    def menuWin_start_exe(apps):
        return lambda x: os.popen('start %s' % apps.encode("gbk"))

    def configWin(self):
        if self.config_win:
            self.config_win.move((self.deskRect.x() + 100, self.deskRect.y() + 100))
            self.config_win.show()
            print 111
            return

        self.config_win = QtGui.QWidget(parent=None)
        with open(config_file, "r") as f:
            self.config = json.loads(f.read())
        self.configWin_steupUI()
        self.configWin_build_comboBox()
        self.config_win.move(self.deskRect.x() + 100, self.deskRect.y() + 100)
        self.config_win.show()
        self.config_win.closeEvent = self.configWin_closeEvent

    def configWin_steupUI(self, *args):
        self.config_win.resize(510, 135)
        gridLayout = QtGui.QGridLayout(self.config_win)
        self.config_win.comboBox1 = QtGui.QComboBox(self.config_win)
        label1 = QtGui.QLabel(self.config_win)
        label2 = QtGui.QLabel(self.config_win)
        label3 = QtGui.QLabel(self.config_win)
        pubshBtn1 = QtGui.QPushButton(self.config_win)
        pubshBtn2 = QtGui.QPushButton(self.config_win)
        pubshBtn3 = QtGui.QPushButton(self.config_win)
        self.config_win.text1 = QtGui.QLineEdit(self.config_win)
        self.config_win.text2 = QtGui.QLineEdit(self.config_win)

        gridLayout.addWidget(label1, 0, 0, 1, 1)
        gridLayout.addWidget(self.config_win.comboBox1, 0, 1, 1, 1)
        gridLayout.addWidget(pubshBtn1, 0, 2, 1, 1)
        gridLayout.addWidget(label2, 1, 0, 1, 1)
        gridLayout.addWidget(self.config_win.text1, 1, 1, 1, 1)
        gridLayout.addWidget(pubshBtn2, 1, 2, 1, 1)
        gridLayout.addWidget(label3, 2, 0, 1, 1)
        gridLayout.addWidget(self.config_win.text2, 2, 1, 1, 1)
        gridLayout.addWidget(pubshBtn3, 2, 2, 1, 1)

        label1.setMinimumSize(QtCore.QSize(50, 35))
        label2.setMinimumSize(QtCore.QSize(50, 35))
        label3.setMinimumSize(QtCore.QSize(50, 35))
        pubshBtn1.setMinimumSize(QtCore.QSize(80, 35))
        pubshBtn2.setMinimumSize(QtCore.QSize(80, 35))
        pubshBtn3.setMinimumSize(QtCore.QSize(80, 35))
        self.config_win.comboBox1.setMinimumSize(QtCore.QSize(350, 35))
        self.config_win.text1.setMinimumSize(QtCore.QSize(350, 35))
        self.config_win.text2.setMinimumSize(QtCore.QSize(350, 35))

        # connect
        QtCore.QObject.connect(pubshBtn1, QtCore.SIGNAL("clicked(bool)"), self.configWin_removeItem)
        QtCore.QObject.connect(pubshBtn2, QtCore.SIGNAL("clicked(bool)"), self.configWin_appendItem)
        QtCore.QObject.connect(pubshBtn3, QtCore.SIGNAL("clicked(bool)"), self.configWin_selectFile)
        QtCore.QObject.connect(self.config_win.comboBox1, QtCore.SIGNAL("currentIndexChanged(QString)"),
                               self.configWin_refreshItem)

        # text
        label1.setText(u"配置")
        label2.setText(u"备注")
        label3.setText(u"打开")
        pubshBtn1.setText(u"减少")
        pubshBtn2.setText(u"增加")
        pubshBtn3.setText(u"选择")

    def configWin_refreshItem(self, *args):
        for menu in self.config["menu"]:
            if args[0] == _fromUtf8(menu["label"]):
                self.config_win.text1.setText(menu["label"])
                self.config_win.text2.setText(menu["open"])

    def configWin_build_comboBox(self, sels=None):
        self.config_win.comboBox1.clear()
        for menu in self.config["menu"]:
            self.config_win.comboBox1.addItem(menu["label"])
        if sels:
            print unicode(sels)
            # print self.comboBox1.itemData(self.comboBox1, role=10)
            # self.comboBox1.setCurrentIndex(sels)
            # QtCore.QObject.connect(self.comboBox1, QtCore.SIGNAL("currentIndexChanged(%s)" % sels), self.refreshItem)

    def configWin_selectFile(self):
        sel_file = QtGui.QFileDialog.getOpenFileName(None,
                                                     "kaiwenjian",
                                                     "D:/",
                                                     "All Files *.*\n"
                                                     "Exe Files *.exe\n"
                                                     "Text Files *.txt")
        if sel_file:
            self.config_win.text2.setText(sel_file)
            if not self.config_win.text1.text():
                self.config_win.text1.setText(sel_file.split("/")[-1].split(".")[0])

    def configWin_appendItem(self):
        text1 = self.config_win.text1.text()
        text2 = self.config_win.text2.text()

        have = 1
        dict1 = {"label": unicode(text1), "open": unicode(text2)}
        for num, menu in enumerate(self.config["menu"]):
            if text1 != _fromUtf8(menu["label"]):
                continue
            self.config["menu"][num] = dict1
            have = 0
            break
        if have:
            self.config["menu"].append(dict1)

        self.configWin_build_comboBox(text1)

    def configWin_removeItem(self):
        # TODO:
        pass

    def configWin_closeEvent(self, event=None):
        with open(config_file, "w")as f:
            f.write(json.dumps(self.config, indent=4))
        os.popen(u'start %s' % unicode(" ".join(sys.argv), "gbk"))
        return


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    AngleTool()
    app.exec_()
