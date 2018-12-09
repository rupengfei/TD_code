# -*- coding:utf-8 -*-  
# ==========================================
#       author: Pengfei.Ru
#         mail: a773849069@gmail.com
#         time: 2018/12/7
# ==========================================
from PySide2 import QtCore, QtGui
# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*


class DnDListWidget(QListWidget):
    """QListWidget多重继承，其中一个父类是QAbstractItemView,支持setDragEnabled()，
    所以可以直接设置为True，但是还要要有startDrag()方法以创建Drag对象"""
    def __init__(self, parent=None):
        super(DnDListWidget, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setToolTip("DnDListWidget")

    def dragEnterEvent(self, event):
        print "dragEnterEvent"
        # if event.mimeData().hasFormat("application/x-icon-and-text"):
        #     event.accept()
        # else:
        #     event.ignore()

    def dragMoveEvent(self, event):
        print "dragMoveEvent"
        # if event.mimeData().hasFormat("application/x-icon-and-text"):
        #     event.setDropAction(Qt.MoveAction)
        #     event.accept()
        # else:
        #     event.ignore()

    def dropEvent(self, event):
        print "dropEvent"
        # if event.mimeData().hasFormat("application/x-icon-and-text"):
        #     data = event.mimeData().data("application/x-icon-and-text")
        #     stream = QDataStream(data, QIODevice.ReadOnly)
        #     text = stream.readQString()
        #     # text=""
        #     # stream>>text
        #     icon = QIcon()
        #     stream >> icon
        #     item = QListWidgetItem(text, self)
        #     item.setIcon(icon)
        #     event.setDropAction(Qt.MoveAction)
        #     event.accept()
        # else:
        #     event.ignore()

    def startDrag(self, dropActions):
        print "111"
        # item = self.currentItem()
        # icon = item.icon()
        # data = QByteArray()
        # stream = QDataStream(data, QIODevice.WriteOnly)
        # stream.writeQString(item.text())
        # stream<<item.text()
        # stream << icon
        # mimeData = QMimeData()
        # mimeData.setData("application/x-icon-and-text", data)
        # drag = QDrag(self)
        # drag.setMimeData(mimeData)
        # pixmap = icon.pixmap(24, 24)
        # drag.setHotSpot(QPoint(12, 12))
        # drag.setPixmap(pixmap)
        # if drag.exec(QtCore.Qt.MoveAction) == QtCore.Qt.MoveAction:
        #     self.takeItem(self.row(item))


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
        返回列表的长度  是个整数
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
        return current_flags | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled

    # def insertRow(self, value, row=-1, index=QtCore.QModelIndex()):
    #     """
    #     """
    #     if row == -1:
    #         row = self.rowCount()
    #
    #     self.beginInsertRows(index, row, row)
    #     self.__data.insert(row, value)
    #     self.endInsertRows()
    #     return True

    def removeRow(self, row=-1, index=QtCore.QModelIndex(), sel_items=None):
        self.beginRemoveRows(index, row, row)
        for item in sel_items:
            self.__data.pop(item.row())
        self.endRemoveRows()
        return True

    def my_sel(self):
        return True

    def append(self, value, index=QtCore.QModelIndex()):
        self.__data.append(value)
        self.dataChanged.emit(index, index)
        return True

    def fanhui_index(self, index=QtCore.QModelIndex()):
        print "1111111"
        print self.__data[index.flags()]
        return True

    def sel_item(self, index=QtCore.QModelIndex()):
        return self.__data[index.row()]
