# -*- coding: utf-8 -*-
"""
@author: 刘国财
@software: PyCharm 2018.1
@file: Tools.py
@time: 2018/10/30 13:28
"""

import maya.cmds as mc
import os

UI_NAME = 'BTR.ui'
UI_PATH = 'Ui'


# 获取UI路径
def get_ui_path():
    """

    :return: FULL_UI_PATH
    """
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), (UI_PATH + '/' + UI_NAME)).replace('\\', '/')


# 获取项目路径
def get_project_path():
    """

    :return: PROJECT_PATH
    """
    return mc.workspace(q=True, fn=True)


# 获取软件版本
def get_soft_version():
    """

    :return: MAYA VERSION
    """
    return mc.about(v=True)

