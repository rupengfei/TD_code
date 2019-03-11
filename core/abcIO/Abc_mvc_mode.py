# -*- coding:utf-8 -*-  
# ==========================================
#       author: Pengfei.Ru
#         mail: a773849069@gmail.com
#         time: 2018/12/17
# ==========================================
from PySide2 import QtCore, QtGui, QtWidgets

# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*


class MVC_List_Model(QtCore.QAbstractListModel):
    def __init__(self, parent=None, data=None):
        """
        """
        super(MVC_List_Model, self).__init__(parent)
        self.__data = data or list()

    def rowCount(self, index=QtCore.QModelIndex()):
        """返回列表的长度  是个整数"""
        return len(self.__data)

    def data(self, index=QtCore.QModelIndex(), role=QtCore.Qt.EditRole, list1=None, list_sel=None):
        if list1:
            return self.__data
        if list_sel:
            pass
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return self.__data[index.row()]
        if role == QtCore.Qt.ItemIsSelectable:
            return self.__data

    def flags(self, index=QtCore.QModelIndex()):
        """
        """
        current_flags = super(MVC_List_Model, self).flags(index)
        return current_flags | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled

    def removeRow(self, row=-1, index=QtCore.QModelIndex(), sel_items=None):
        sel_items.sort(reverse=True)
        self.beginRemoveRows(index, row, row)
        for item in sel_items:
            self.__data.pop(item.row())
        self.endRemoveRows()
        return True

    def selectRow(self, sel_items=None):
        sel_items.sort()
        sels_data = list()
        for item in sel_items:
            sels_data.append(self.__data[item.row()])
        return sels_data

    def append(self, value, index=QtCore.QModelIndex()):
        self.__data.extend(value)
        self.dataChanged.emit(index, index)
        return True

    def replace_row(self, values=tuple(), row=-1, index=QtCore.QModelIndex()):
        """
        """
        self.__data = values
        self.dataChanged.emit(index, index)
        return True



