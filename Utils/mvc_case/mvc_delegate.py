#========================================
#    author: Changlong.Zang
#      mail: zclongpop123@163.com
#      time: Tue Nov 06 11:55:05 2018
#========================================
from PySide2 import QtCore, QtWidgets
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
class ComboDelegate(QtWidgets.QStyledItemDelegate):
    '''
    '''
    def createEditor(self, parent, option, index):
        '''
        '''
        combox = QtWidgets.QLineEdit(parent)
        return combox

    
    def setEditorData(self, editor, index):
        '''
        '''
        editor.setText(str(index.data(QtCore.Qt.DisplayRole)))
    

    def setModelData(self, editor, model, index):
        '''
        '''
        value = editor.text()
        model.setData(index, value)