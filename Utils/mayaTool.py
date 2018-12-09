# -*- coding:utf-8 -*-
# ==========================================
#       author: Pengfei.Ru
#         mail: a773849069@gmail.com
#         time: 2018/12/02
# ==========================================
import maya.cmds as mc
import re
import os
import maya.mel as mel
# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*


def get_scene_name():
    return mc.file(q=True, ns=True)

def get_scene_path():
    return mc.file(q=True, sn=True)

def sel_Geo():
    return mc.ls("*_Geo")

# noinspection PyPep8Naming
def getBlendShapeInfo(blendShape):
    """Return blendShape's ID and attributes dict.."""
    attribute_dict = {}
    if mc.nodeType(blendShape) != 'blendShape':
        return attribute_dict

    infomations = mc.aliasAttr(blendShape, q=True)
    for i in range(len(infomations)):
        if i % 2 == 1:
            continue
        bs_id = infomations[i + 1]
        bs_attr = infomations[i + 0]
        bs_id = int(re.search('\d+', bs_id).group())
        attribute_dict[bs_id] = bs_attr

    return attribute_dict


# noinspection PyPep8Naming
def getBlendShapeAttributes(blendShape):
    """
    Return blendShape attributes..
    """
    attribute_dict = getBlendShapeInfo(blendShape)
    bs_idList = attribute_dict.keys()
    bs_idList.sort()

    attributes = [attribute_dict.get(i, '') for i in bs_idList]
    return attributes


def get_start_dir(start_dir):
    if os.path.isfile(start_dir):
        start_dir = os.path.dirname(start_dir)

    elif os.path.isdir(start_dir):
        pass

    else:
        start_dir = mc.workspace(q=True, lfw=True)[0]

    return start_dir


def get_output_path(filter_format='Maya ASCII (*.ma)', start_dir=None):
    start_dir = get_start_dir(start_dir)
    filePath = mc.fileDialog2(ff=filter_format, startingDirectory=start_dir)
    return filePath


def get_input_path(filter_format='Maya ASCII (*.ma)', start_dir=None):
    start_dir = get_start_dir(start_dir)
    filePath = mc.fileDialog2(ff=filter_format, fm=4, okc='Select', startingDirectory=start_dir)
    return filePath


PROGRESSBAR = mel.eval('string $temp = $gMainProgressBar;')


def startProgress(count):
    mc.progressBar(PROGRESSBAR, e=True, bp=True, maxValue=max(count, 1))


def moveProgress(message):
    mc.progressBar(PROGRESSBAR, e=True, step=1, st=message)


def endProgress():
    mc.progressBar(PROGRESSBAR, e=True, ep=True)
