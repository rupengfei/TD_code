# -*- coding:utf-8 -*-  
# ==========================================
#       author: Pengfei.Ru
#         mail: a773849069@gmail.com
#         time: 2018/12/7
# ==========================================
from PySide2 import QtCore, QtGui


# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*


class MVC_List_Model(QtCore.QAbstractListModel):
    def __init__(self, parent=None, data=None):
        """
        """
        super(MVC_List_Model, self).__init__(parent)
        self.__data = data or list("abcde")
        # self.list_view.selectionChanged = self.list_view_selectionChanged
        # self.list_view.mouseMoveEvent = self.drag_move_event
        # self.list_view.dragEnterEvent = self.list_view_dragEnterEvent
        # self.list_view.dragMoveEvent = self.drag_move_event
        # self.list_view.dropEvent = self.list_view_dropEvent

    #
    # def data(self, index=QtCore.QModelIndex(), role=QtCore.Qt.DisplayRole):
    #     """
    #     """
    #     if role == QtCore.Qt.DisplayRole:
    #         return self.__data[index.row()]

    def rowCount(self, index=QtCore.QModelIndex()):
        """
        """
        return len(self.__data)

    def data(self, index=QtCore.QModelIndex(), role=QtCore.Qt.EditRole, list1=None):
        if list1:
            return self.__data
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return self.__data[index.row()]
        if role == QtCore.Qt.ItemIsSelectable:
            return self.__data

    def flags(self, index=QtCore.QModelIndex()):
        """
        """
        current_flags = super(MVC_List_Model, self).flags(index)
        return current_flags | QtCore.Qt.ItemIsSelectable

    def insertRow(self, value, row=-1, index=QtCore.QModelIndex()):
        """
        """
        if row == -1:
            row = self.rowCount()

        self.beginInsertRows(index, row, row)
        self.__data.insert(row, value)
        self.endInsertRows()
        return True

    def removeRow(self, row=-1, index=QtCore.QModelIndex()):
        self.beginRemoveRows(index, row, row)
        if True:
            self.__data.pop(row)
        self.endRemoveRows()
        return True

