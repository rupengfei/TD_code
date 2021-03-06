# -*- coding:utf-8 -*-  
# ==========================================
#       author: Pengfei.Ru
#         mail: 773849069@qq.com
#         QQ: 773849069
#         time: 2018/11/30
# ==========================================
import json
import os
import maya.cmds as mc
from Utils import scriptTool, mayaTool
# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*


def get_all_sg_nodes():
    sg_nodes = mc.ls(typ="shadingEngine")
    return sg_nodes


def get_sg_nodes(args=None):
    # print args
    sg_nodes = list()
    for geo in args:
        # print geo
        shapes = mc.listRelatives(geo, children=True, path=True) or list()
        # print shapes
        for shp in shapes:
            sg_node = mc.listConnections(shp, destination=True, t="shadingEngine")
            if not sg_node:
                continue
            sg_nodes.extend(sg_node)

    return scriptTool.arrayRemoveDuplicates(sg_nodes)


def aoto_get_sg_nodes(args=None):
    # print args
    sg_nodes = list()
    for geo in args:
        # print geo
        shapes = mc.listRelatives(geo, children=True, shapes=True, path=True) or list()
        # print shapes
        for shp in shapes:
            sg_node = mc.listConnections(shp, destination=True, t="shadingEngine")
            if not sg_node:
                continue
            sg_nodes.extend(sg_node)

    return scriptTool.arrayRemoveDuplicates(sg_nodes)


def get_sel_sg_nodes(args=None):
    # print args
    if args:
        return aoto_get_sg_nodes(args)
    else:
        args = mc.ls(sl=True)
        return get_sg_nodes(args)


def export_sg_nodes(sg_nodes, file_path, fix_name="ma"):
    # print sg_nodes
    if len(sg_nodes) == 0:
        return False
    if fix_name == "ma":
        fix_name = "mayaAscii"
    if fix_name == "mb":
        fix_name = "mayaBinary"
    mc.select(sg_nodes, r=True, ne=True)
    mc.file(file_path, options="v=0;", typ=fix_name, es=True, force=True)  #  pr=True,

    return True


def export_all_sg_nodes(file_path, fix_name="ma"):
    return export_sg_nodes(get_all_sg_nodes(), file_path, fix_name)


def export_sel_sg_nodes(file_path, fix_name="ma", args=None):
    # print args
    return export_sg_nodes(get_sel_sg_nodes(args), file_path, fix_name)


def get_sg_members(sg_nodes=tuple()):
    data = dict()
    for sg in sg_nodes:
        members = mc.sets(sg, q=True) or list()
        filter_members = list()
        for m in members:
            obj = m.split(".")
            if mc.nodeType(obj[0]) != "transform":
                obj[0] = mc.listRelatives(obj[0], p=True)[0]
            filter_members.append(".".join(obj))
        data[sg] = filter_members
    return data


def get_all_sg_members():
    return get_sg_members(get_all_sg_nodes())


def get_sel_sg_members(args=None):
    # print args
    return get_sg_members(get_sel_sg_nodes(args))


def export_sg_members(data, file_path):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

    return True


def export_all_sg_members(file_path):
    return export_sg_members(get_all_sg_members(), file_path)


def export_sel_sg_members(file_path, args=None):
    return export_sg_members(get_sel_sg_members(args), file_path)


def export_sel_shader(file_path):
    scene_name, json_name, fix_name = mayaTool.format_path(file_path)
    export_sel_sg_members(json_name)
    export_sel_sg_nodes(scene_name, fix_name)

def export_all_shader(file_path):
    scene_name, json_name, fix_name = mayaTool.format_path(file_path)
    export_all_sg_nodes(scene_name, fix_name)
    export_all_sg_members(json_name)


def convert_ma_to_json(file_path):
    return file_path.split(".")[0] + ".json"


def import_sel_shader(file_path, geo_namespace=None, sg_namespace=None):
    sels = mc.ls(sl=True)
    json_path = convert_ma_to_json(file_path)
    sg_namespace = reference_shader_file(file_path, sg_namespace)
    assign_data_to_all(json_path, sg_namespace, geo_namespace, sels)
    return True


def import_all_shader(file_path, geo_namespace=None, sg_namespace=None):
    json_path = convert_ma_to_json(file_path)
    sg_namespace = reference_shader_file(file_path, sg_namespace)
    assign_data_to_all(json_path, sg_namespace, geo_namespace)
    return True


def reference_shader_file(file_path, name_space=None):
    """导入参考文件"""
    file_path = file_path.replace('\\', '/')
    ref_file = mc.file(query=True, reference=True)
    if file_path in ref_file:
        return mc.file(file_path, query=True, namespace=True)
    if not name_space:
        name_space = os.path.splitext(os.path.basename(file_path))[0]
    mc.file(file_path,
            r=True,
            type="mayaAscii",
            ignoreVersion=True,
            gl=True,
            mergeNamespacesOnClash=False,
            namespace=name_space,
            options="v=0;"
            )
    return mc.file(file_path, query=True, namespace=True)


def assign_data_to_all(data_path, sg_namespace=None, geo_namespace=None, selects=None):
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
                geo = "{0}:{1}".format(geo_namespace, geo)
            if selects:
                for sel in selects:
                    sel_colon = sel.split(":")[-1]
                    geo_colon = geo.split(":")[-1]
                    if "." in geo_colon:
                        sel_colon = sel_colon + geo.split(".")[-1]
                        sel = sel + geo.split(".")[-1]
                    if geo_colon in sel_colon:
                        if geo_colon == sel_colon:
                            filter_item.append(sel)
                        else:
                            mc.warning("----场景有重名物体没有附上材质----.\n{0}".format(sel))
                            pass
            else:
                if mc.objExists(geo.split(".")[0]):  # 面材质带点  .f[8]
                    filter_item.append(geo)
        try:
            mc.sets(filter_item, e=True, forceElement=sg)
        except ValueError as e:
            print e
    return True

