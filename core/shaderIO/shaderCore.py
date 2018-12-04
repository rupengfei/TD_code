# -*- coding:utf-8 -*-  
# ==========================================
#       author: Pengfei.Ru
#         mail: a773849069@gmail.com
#         time: 2018/11/30
# ==========================================
import json
import os
import maya.cmds as mc
from Utils import scriptTool
# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*


def get_all_sg_nodes():
    sg_nodes = mc.ls(typ="shadingEngine")
    return sg_nodes


def get_sel_sg_nodes():
    sg_nodes = list()
    selected_geos = mc.ls(sl=True)
    for geo in selected_geos:
        shapes = mc.listRelatives(geo, children=True, path=True) or list()
        for shp in shapes:
            sg_node = mc.listConnections(shp, destination=True, t="shadingEngine")
            if not sg_node:
                continue
            sg_nodes.extend(sg_node)

    return scriptTool.arrayRemoveDuplicates(sg_nodes)


def export_sg_nodes(sg_nodes, file_path):
    if len(sg_nodes) == 0:
        return False
    mc.select(sg_nodes, r=True, ne=True)
    mc.file(file_path, options="v=0;", typ="mayaAscii", pr=True, es=True)
    return True


def export_all_sg_nodes(file_path):
    return export_sg_nodes(get_all_sg_nodes(), file_path)


def export_sel_sg_nodes(file_path):
    return export_sg_nodes(get_sel_sg_nodes(), file_path)


def get_sg_members(sg_nodes=tuple()):
    data = dict()
    for sg in sg_nodes:
        members = mc.sets(sg, q=True) or list()
        filter_members = list()
        for m in members:
            obj = m.split(".")
            if mc.nodeType(obj[0]) != "transfrom":
                obj[0] = mc.listRelatives(obj[0], p=True)[0]
            filter_members.append(".".join(obj))
        data[sg] = filter_members
    return data


def get_all_sg_members():
    return get_sg_members(get_all_sg_nodes())


def get_sel_sg_members():
    return get_sg_members(get_sel_sg_nodes())


def export_sg_members(data, file_path):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

    return True


def export_all_sg_members(file_path):
    return export_sg_members(get_all_sg_members(), file_path)


def export_sel_sg_members(file_path):
    return export_sg_members(get_sel_sg_members(), file_path)


def reference_shader_file(file_path):
    file_path = file_path.replace('\\', '/')
    ref_file = mc.file(query=True, reference=True)
    if file_path in ref_file:
        return mc.file(file_path, query=True, namespace=True)
    name_space = os.path.splitext(os.path.basename(file_path))[0]
    mc.file(file_path, r=True, ns=name_space)
    return name_space


def assign_data_to_all(data_path, sg_namespace=None, geo_namespace=None):
    # data = dict()
    with open(data_path, "r") as f:
        data = json.load(f)

    for sg, geos in data.iteritems():
        if sg_namespace:
            sg = "{0}:{1}".format(sg_namespace, sg)
        if not mc.objExists(sg):
            continue

        filter_item = list()
        for geo in geos:
            if geo_namespace:
                geo = "{0}:{1}".format(geo_namespace, sg)
            if mc.objExists(geo.split(".")[0]):
                filter_item.append(geo)

        mc.sets(filter_item, e=True, forceElement=sg)
    return True

