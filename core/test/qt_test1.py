# -*- coding:utf-8 -*-  
# ==========================================
#       author: Pengfei.Ru
#         mail: a773849069@gmail.com
#         time: 2018/12/5
# ==========================================
import sys
from PySide2 import QtCore, QtGui, QtWidgets
import Utils.uiTool as uiTool

# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*

form_class, base_class = uiTool.loadUiType("D:/___________TD____________/TD_Code/core/test/qt_test1_ui.ui")



class ShaderIO(base_class, form_class):
    '''
    '''
    def __init__(self, parent=uiTool.get_maya_window()):
        super(ShaderIO, self).__init__(parent)
        self.setupUi(self)

        self.__current_dir = ''

        self.show()


# if __name__ == "__main__":
#     ShaderIO()
