#========================================
#    author: Changlong.Zang
#      mail: zclongpop123@163.com
#      time: Tue Nov 06 10:58:26 2018
#========================================
from PySide2 import QtCore, QtGui
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
class MVC_List_Model(QtCore.QAbstractListModel):
    '''
    '''
    def __init__(self, parent=None, data=None):
        '''
        '''
        super(MVC_List_Model, self).__init__(parent)
        self.__data = data or list()
    
    
    
    def rowCount(self, index=QtCore.QModelIndex()):
        '''
        '''
        return len(self.__data)
    
    
    
    def data(self, index=QtCore.QModelIndex(), role=QtCore.Qt.DisplayRole):
        '''
        '''
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return self.__data[index.row()]
        
        if role == QtCore.Qt.CheckStateRole:
            return False
        
        if role == QtCore.Qt.ForegroundRole:
            return QtGui.QColor(255, 0, 255)

        if role == QtCore.Qt.TextAlignmentRole:
            return QtCore.Qt.AlignCenter
        
        if role == QtCore.Qt.DecorationRole:
            return QtGui.QImage('D:/work/mvc_case/icons/gitlab.png').scaled(24, 24)
    

    
    def flags(self, index=QtCore.QModelIndex()):
        '''
        '''
        current_flags = super(MVC_List_Model, self).flags(index)
        return current_flags | QtCore.Qt.ItemIsEditable



    def setData(self, index=QtCore.QModelIndex(), value='', role=QtCore.Qt.EditRole):
        '''
        '''
        if role == QtCore.Qt.EditRole:
            self.__data[index.row()] = value
            self.dataChanged.emit(index, index)
            return True
    
    
    
    def insertRow(self, value, row=-1, index=QtCore.QModelIndex()):
        '''
        '''
        if row == -1:
            row = self.rowCount()
        
        self.beginInsertRows(index, row, row)
        self.__data.insert(row, value)
        self.endInsertRows()
        return True
    
    
    def removeRow(self, row=-1, index=QtCore.QModelIndex()):
        '''
        '''
        if row == -1:
            row = self.rowCount() - 1
        
        self.beginRemoveRows(index, row, row)
        if row > -1 and row < self.rowCount():
            self.__data.pop(row)
        self.endRemoveRows()
        return True 


    def clear(self):
        '''
        '''
        for i in reversed(range(self.rowCount())):
            self.removeRow(i)
        return True



class MVC_table_model(QtCore.QAbstractTableModel):
    '''
    '''
    HEAD_DATA = ['Low', 'Geometry', 'GPU', 'Proxy']
    
    
    def __init__(self, parent=None, data=None):
        '''
        '''
        super(MVC_table_model, self).__init__(parent)
        self.__data = data or list()
    
    
    
    def rowCount(self, index=QtCore.QModelIndex()):
        '''
        '''
        return len(self.__data)
    
    
    
    def columnCount(self, index=QtCore.QModelIndex()):
        '''
        '''
        return 4



    def data(self, index=QtCore.QModelIndex(), role=QtCore.Qt.DisplayRole):
        '''
        '''
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return self.__data[index.row()][index.column()]
    
    
    
    def headerData(self, sec, oritation, role):
        '''
        '''
        if role == QtCore.Qt.DisplayRole:
            if oritation == QtCore.Qt.Horizontal:
                return self.HEAD_DATA[sec]
            else:
                return sec + 1
    
    
    
    def flags(self, index=QtCore.QModelIndex()):
        '''
        '''
        current_flags = super(MVC_table_model, self).flags(index)
        return current_flags | QtCore.Qt.ItemIsEditable


    
    def setData(self, index=QtCore.QModelIndex(), value='', role=QtCore.Qt.EditRole):
        '''
        '''
        if role == QtCore.Qt.EditRole:
            self.__data[index.row()][index.column()] = value
            self.dataChanged.emit(index, index)
            return True
    