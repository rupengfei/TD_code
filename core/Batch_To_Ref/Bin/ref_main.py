# -*- coding: utf-8 -*-
__author__ = '財'
__time__ = '2018/11/1 22:10'

import maya.cmds as mc
import To_Ref



def onMayaDroppedPythonFile(*args):
    """

    :param args:
    :return:
    """
    if mc.window('BTR_WIN', q=True, ex=True):
        mc.deleteUI('BTR_WIN')
    win = To_Ref.ToRef()
    win.show()


def mian():
    """

    :return:
    """
    return onMayaDroppedPythonFile()


