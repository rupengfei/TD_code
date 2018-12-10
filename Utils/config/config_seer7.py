# -*- coding:utf-8 -*-
# ==========================================
#       author: Pengfei.Ru
#         mail: a773849069@gmail.com
#         time: 2018/12/9
# ==========================================
import json
from Utils import scriptTool, ioTool, mayaTool, pathTool
import os
import maya.cmds as mc
from core.shaderIO import shaderCore


# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*
seer7_json = os.path.join(scriptTool.getScriptPath(), "config_seer7.json")


def setData(data=None):
    """
    data = {
            "shader_source_path": "D:/Repo/seer7/cacheIO/Chars/Rig",
            "cacheIO_an" : "D:/Repo/seer7/cacheIO/Animation"
        }
    """
    if not data:
        data = {
            "shader_source_path": r"D:/Repo/seer7/cacheIO/Chars/Rig",
            "cacheIO": r"Z:\SEER7\Work\Shot_work\cacheIO",
            "cacheIO_an": r"Z:\SEER7\Work\Shot_work\cacheIO\Animation",
            "cacheIO_fx": r"Z:\SEER7\Work\Shot_work\cacheIO\Fx",
            "cacheIO_lt": r"Z:\SEER7\Work\Shot_work\cacheIO\Lighting",
            "cacheIO_shader": r"Z:\SEER7\Work\Shot_work\cacheIO\Shader",
        }
        ioTool.writeData(seer7_json, data)
    return True


def seer7_data():
    return ioTool.readData(seer7_json)


def split_cam(cam="Sc003_054_001_035_cam"):
    """
    ('Sc003', '054', 'Sc003_054', '001', '035')
    """
    data = cam.split("_")
    scene = data[0]
    shot = data[1]
    shot_name = "{0}_{1}".format(scene, shot)
    start_frame = data[2]
    end_frame = data[3]
    return scene, shot, shot_name, start_frame, end_frame


def an_makedir(an_path="D:/Repo/seer7/cacheIO/Animation", scene="sc003", shot_name="sc003_054"):
    """
    D:/Repo/seer7/cacheIO/Animation\sc003\sc003_054
    """
    an_path = os.path.join(an_path, scene, shot_name)
    return an_path


def format_path(source_pathName=""):
    path = os.path.dirname(source_pathName)
    name = os.path.basename(source_pathName)
    scene_name = path + "/" + name.split(".")[0] + "_SG." + name.split(".")[1]  # atieda_SG.ma
    json_name = path + "/" + name.split(".")[0] + "_SG.json"  # atieda_SG.json
    fix_name = name.split(".")[1]  # ma or mb
    return scene_name, json_name, fix_name


def seer7_shader_format_path():
    """
    """
    source_file = mayaTool.get_scene_path()
    path = pathTool.recombine_path(source_file, "Rig", "shader")
    # path = os.path.dirname(source_file)
    if not os.path.exists(path):
        os.makedirs(path)
    # if path[-3:] == "Rig":
    #     path = path[:-3] + "shader"  # path
    #     if not os.path.exists(path):
    #         os.makedirs(path)
    name = os.path.basename(source_file)
    scene_name = path + "/" + name.split(".")[0] + "_SG." + name.split(".")[1]  # atieda_SG.ma
    json_name = path + "/" + name.split(".")[0] + "_SG.json"  # atieda_SG.json
    fix_name = name.split(".")[1]  # ma or mb

    return scene_name, json_name, fix_name


def aoto_export_shader():
    scene_name, json_name, fix_name = seer7_shader_format_path()
    geos = mc.ls("*_Geo") or list()
    for geo in geos:
        # print geo
        sels = mc.ls(geo, dag=True, typ="mesh")
        sels1 = mc.listRelatives(sels, p=True)
        sels2 = sels1[:]
        shaderCore.export_sel_sg_nodes(scene_name, fix_name, sels1)
        shaderCore.export_sel_sg_members(json_name, sels2)

    return True


def export_sel_shader(file_path):
    sels = mc.ls(sl=True)
    scene_name, json_name, fix_name = format_path(file_path)
    shaderCore.export_sel_sg_nodes(scene_name, fix_name)
    mc.select(sels, r=True)
    shaderCore.export_sel_sg_members(json_name)


def export_all_shader(file_path):
    scene_name, json_name, fix_name = format_path(file_path)
    shaderCore.export_all_sg_nodes(scene_name, fix_name)
    shaderCore.export_all_sg_members(json_name)

def import_sel_shader(file_path, geo_namespace=None):
    json_path = ioTool.convert_ma_to_json(file_path)
    shaderCore.reference_shader_file(file_path)
    shaderCore.assign_data_to_all(json_path)
    return True

def import_all_shader(file_path, geo_namespace=None):
    json_path = ioTool.convert_ma_to_json(file_path)
    shaderCore.reference_shader_file(file_path)
    sg_namespace = os.path.basename(file_path)[:os.path.basename(file_path).rfind(".")]
    shaderCore.assign_data_to_all(json_path, sg_namespace, geo_namespace)
    return True


def aoto_import_shader():
    pass


if __name__ == '__main__':
    setData()
