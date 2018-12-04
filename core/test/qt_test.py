# -*- coding:utf-8 -*-  
# ==========================================
#       author: Pengfei.Ru
#         mail: a773849069@gmail.com
#         time: 2018/12/4
# ==========================================
import sys
from PySide2 import QtCore, QtGui, QtWidgets
# import pyside2uic as uic
# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*


def main():
    app = QtWidgets.QApplication(sys.argv)

    window = QtWidgets.QMainWindow()

    app.exec_()

    window.show()


if __name__ == "__main__":
    pass

