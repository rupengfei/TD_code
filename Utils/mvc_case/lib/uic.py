#========================================
#    author: Changlong.Zang
#      mail: zclongpop123@163.com
#      time: Wed Nov 07 14:51:24 2018
#========================================
from xml.etree import ElementTree
from cStringIO import StringIO
from PySide2 import QtWidgets
import pyside2uic
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
def loadUiType(ui_file_path):
    """
    Load ui file to python objects...
    """
    xml_doc = ElementTree.parse(ui_file_path)
    form_class   = xml_doc.find('class').text
    widget_class = xml_doc.find('widget').get('class')

    with open(ui_file_path, 'r') as f:
        o = StringIO()
        frame = dict()

        pyside2uic.compileUi(f, o, indent=0)
        pyc = compile(o.getvalue(), '<string>', 'exec')
        exec pyc in frame

        form_class = frame['Ui_{0}'.format(form_class)]
        base_class = eval('QtWidgets.{0}'.format(widget_class))

    return form_class, base_class
