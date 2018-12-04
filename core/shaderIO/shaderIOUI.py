# -*- coding:utf-8 -*-  
# ==========================================
#       author: Pengfei.Ru
#         mail: a773849069@gmail.com
#         time: 2018/12/3
# ==========================================
from PySide2 import QtWidgets, QtGui, QtCore
# import shaderCore
import shaderIOQt
from Utils import uiTool
# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*


class ShaderIO(QtWidgets.QMainWindow, shaderIOQt.Ui_MainWindow):
    def __init__(self, parent=uiTool.get_maya_window()):
        super(ShaderIO, self).__init__(parent)
        self.setupUi(self)

        self.__current_dir = ''

        self.show()

