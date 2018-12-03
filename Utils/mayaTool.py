# -*- coding:utf-8 -*-
# ==========================================
#       author: Pengfei.Ru
#         mail: a773849069@gmail.com
#         time: 2018/12/02
# ==========================================
import maya.cmds as mc
import re
# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*


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
    """"
    Return blendShape attributes..
    """
    attribute_dict = getBlendShapeInfo(blendShape)
    bs_idList = attribute_dict.keys()
    bs_idList.sort()

    attributes = [attribute_dict.get(i, '') for i in bs_idList]
    return attributes