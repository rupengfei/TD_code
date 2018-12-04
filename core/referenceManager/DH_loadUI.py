#!/usr/bin/env python
# -*- coding: utf-8 -*-
#========================================
#    author: Dango
#      mail: 1007982374@qq.com
#      time: Thu Nov 11 18:43 2018
#========================================
import Qt

if Qt.__binding__ == 'PySide':
    from shiboken import wrapInstance
    import pysideuic as uic
elif Qt.__binding__ == 'PySide2':
    from shiboken2 import wrapInstance
    import pyside2uic as uic

import xml.etree.ElementTree as xml
from cStringIO import StringIO
import maya.OpenMayaUI as mui

def loadUiType(uiFile):
    parsed = xml.parse(uiFile)
    widget_class = parsed.find('widget').get('class')
    form_class = parsed.find('class').text

    with open(uiFile, 'r') as f:
        o = StringIO()
        frame = {}

        uic.compileUi(f, o, indent=0)
        pyc = compile(o.getvalue(), '<string>', 'exec')
        exec pyc in frame

        # Fetch the base_class and form class based on their type in the xml from designer
        form_class = frame['Ui_%s' % form_class]
        base_class = getattr(Qt.QtWidgets, widget_class)
        return form_class, base_class

def getMayaWindow():
    main_window_ptr = mui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), Qt.QtWidgets.QWidget)
