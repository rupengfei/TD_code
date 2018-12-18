# -*- coding:gbk -*-
# =============================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Wed, 25 Jun 2014 14:43:02
# =============================================
import inspect
import os
# --+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+


def getModulesPath(moudle):
    """
    返回模块路径
    return dir for imported moudle..
    """
    moduleFile = inspect.getfile(moudle)
    modulePath = os.path.dirname(moduleFile)
    return modulePath


def getScriptPath():
    """
    返回脚本路径
    return dir path for used script..
    """
    scriptPath = getModulesPath(inspect.currentframe().f_back)
    return scriptPath


def arrayRemoveDuplicates(Array):
    """
    删除重复的数组
    [1,1,2,2,3,3,4,5,5,6,6,6,6] -> [1,2,3,4,5,6]
    """
    if not type(Array) is list:
        return Array
    return [x for i, x in enumerate(Array) if x not in Array[:i]]


def openMultiarray(Array):
    """
    打开多阵列
    [1, [2, [3, 4], 5], 6] -> [1, 2, 3, 4, 5, 6]
    (1, (2, (3, 4), 5), 6) -> (1, 2, 3, 4, 5, 6)
    """
    L = []
    for Item in Array:
        if isinstance(Item, (tuple, list)):
            for i in openMultiarray(Item):
                L.append(i)
        else:
            L.append(Item)
    return L