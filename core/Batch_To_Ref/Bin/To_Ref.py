# -*- coding: utf-8 -*-
__author__ = '財'
__time__ = '2018/11/1 0:39'

import os
import maya.cmds as mc
from Qt import QtWidgets, QtCompat, QtCore
import Tools
import re

reload(Tools)


class ToRef(QtWidgets.QWidget):
    def __init__(self):
        super(ToRef, self).__init__()
        QtCompat.loadUi(Tools.get_ui_path(), self)
        self.file = None
        self.iter = None
        self.namespaces = None
        self.thread = MyThread()
        self.thread.signal.connect(self.update_process)
        self.toolButton.clicked.connect(self.get_file)
        self.refButton.clicked.connect(self.check_params)

    # 更新进度条
    def update_process(self, value):
        """

        Args:
            value:

        Returns:

        """
        self.ref_Bar.setValue(value)
        # 如果100，完成
        if self.ref_Bar.value() == 100:
            return

    # 获取文件路径
    def get_file(self):
        """

        Returns:

        """
        # 获取文件路径
        self.file = QtWidgets.QFileDialog.getOpenFileName(self, u'选择参考文件1', Tools.get_project_path())[0]
        self.pathEdit.setText(self.file)

    # 检查所有参数是否匹配
    def check_params(self):
        """

        Returns:method

        """
        # 进度条归零
        if self.ref_Bar.value() != 0:
            self.ref_Bar.setValue(0)
        # 判断路径是不是空的
        if not self.pathEdit.text():
            mc.warning(u'请设置文件路径')
            return
            # 判断是否是文件
        elif not os.path.isfile(self.file):
            mc.warning(u'请选择一个正确的参考文件')
            return
        # 判断空间名是否为空
        elif not self.namespace_edit.text():
            # 警告用户，不能为空，不能用默认空间名
            mc.warning(u'请务必输入一个空间名')
            return
        # 判断是否有特殊字符
        elif not re.match('^[0-9a-zA-Z_]+$', self.namespace_edit.text()):
            mc.warning(u'不要有特殊字符')
            # 把背景色设置为红色提醒
            self.namespace_edit.setStyleSheet('background-color:red')
            return
        else:
            # 恢复默认颜色设置
            self.namespace_edit.setStyleSheet('')
            # 获取空间名信息
            self.namespaces = self.namespace_edit.text()
        # 获取次数，默认为1
        self.iter = self.spinBox.value()
        return self.ref()

    # 调用子线程执行参考动作
    def ref(self):
        self.thread.action(self.iter, self.file, self.namespaces)


class MyThread(QtCore.QThread):
    signal = QtCore.Signal(int)

    def __init__(self):
        super(MyThread, self).__init__()
        self.count = 0

    def action(self, iter_, filename, namespaces):
        """

        :param iter_:
        :param filename:
        :param namespaces:
        :return:
        """
        index = iter_
        while iter_:
            mc.file(filename, r=True, ignoreVersion=True, gl=True, mergeNamespacesOnClash=False,
                    namespace=namespaces, options="mo=1")
            self.count += 1.0
            self.signal.emit(int((self.count / index) * 100))
            iter_ -= 1

        self.count = 0
