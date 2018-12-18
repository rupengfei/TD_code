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


def get_current_frame():
    """返回场景当前选择的帧"""
    return mc.currentTime(q=True)

def get_time_slider():
    """返回时间滑条的信息"""
    min_time = mc.playbackOptions(q=True, minTime=True)  # 开始时间帧
    max_time = mc.playbackOptions(q=True, maxTime=True)  # 结束时间帧
    ast_time = mc.playbackOptions(q=True, ast=True)  # 动画开始帧
    aet_time = mc.playbackOptions(q=True, aet=True)  # 动画结束帧
    by_time = mc.playbackOptions(q=True, by=True)  # step
    return min_time, max_time, ast_time, aet_time, by_time


def filter_camera(cam_name="cam_*_*"):
    """按名称过滤相机"""
    sels_cam = mc.ls(cam_name) or list()
    cams = mc.listCameras()
    cam = list()
    for sel in sels_cam:
        if sel in cams:
            cam.append(sel)
    if len(cam) == 1:
        return cam[0]
    else:
        return False


def get_scene_name():
    return mc.file(q=True, ns=True)

def get_scene_path():
    return mc.file(q=True, sn=True)


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


def getBlendShapeAttributes(blendShape):
    """返回 BlendShape 属性"""
    attribute_dict = getBlendShapeInfo(blendShape)
    bs_idList = attribute_dict.keys()
    bs_idList.sort()

    attributes = [attribute_dict.get(i, '') for i in bs_idList]
    return attributes


def get_start_dir(start_dir):  # 1111111111dir
    """返回一个默认的路径"""
    if os.path.isfile(start_dir):
        start_dir = os.path.dirname(start_dir)

    elif os.path.isdir(start_dir):
        pass

    else:
        start_dir = mc.workspace(q=True, lfw=True)[0]

    return start_dir


def get_output_path(filter_format='Maya ASCII (*.ma)', start_dir=None):  # 1111111111dir
    start_dir = get_start_dir(start_dir)
    filePath = mc.fileDialog2(ff=filter_format, startingDirectory=start_dir)
    return filePath


def get_input_path(filter_format='Maya ASCII (*.ma)', start_dir=None):  # 1111111111dir
    start_dir = get_start_dir(start_dir)
    filePath = mc.fileDialog2(ff=filter_format, fm=4, okc='Select', startingDirectory=start_dir)
    return filePath


PROGRESSBAR = mel.eval('string $temp = $gMainProgressBar;')  # PROGRESSBAR


def startProgress(count):  # PROGRESSBAR
    mc.progressBar(PROGRESSBAR, e=True, bp=True, maxValue=max(count, 1))


def moveProgress(message):  # PROGRESSBAR
    mc.progressBar(PROGRESSBAR, e=True, step=1, st=message)


def endProgress():  # PROGRESSBAR
    mc.progressBar(PROGRESSBAR, e=True, ep=True)
