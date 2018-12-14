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

"""
[u'Z:/SEER7/Work/Asset_work/Env/BaiMuXingFeiChuanShiShiDiZhi/Mod/Layout_Env/Seer7_Env_to_layout.ma',
 u'Z:/SEER7/Work/Asset_work/Chars/ATieDa_ShengJi/Rig/approve/Seer7_char_RIG_ATieDa_ShengJi.ma',
 u'Z:/SEER7/Work/Asset_work/Props/ATieDa_BeiBao/Rig/approve/Seer7_Props_RIG_ATieDa_BeiBao.ma',
 u'D:/cloth/scenes/seer7_test/atieda_v03.ma',
 u'D:/cloth/scenes/seer7_test/atieda_v03.ma{1}'] 
 """

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
            "cacheIO": r"Z:/SEER7/Work/Shot_work/cacheIO",
            "cacheIO_an": r"Z:/SEER7/Work/Shot_work/cacheIO/Animation",
            "cacheIO_fx": r"Z:/SEER7/Work/Shot_work/cacheIO/Fx",
            "cacheIO_lt": r"Z:/SEER7/Work/Shot_work/cacheIO/Lighting",
            "cacheIO_shader": r"Z:/SEER7/Work/Shot_work/cacheIO/Shader",
            "test_scene": r"Z:/SEER7/Work/Shot_work/Layout/sc003/sc003_shot007/work",
        }
        ioTool.writeData(os.path.join(scriptTool.getScriptPath(), "config_seer7.json"), data)
    return True


def seer7_data():
    """返回 seer 项目的配置"""
    return ioTool.readData(os.path.join(scriptTool.getScriptPath(), "config_seer7.json"))


def seer7_split_cam(cam="cam_sc003_shot007_101_268"):
    """
    相机名称过滤镜头号 时间帧信息
    data = ['cam', 'sc003', 'shot007', sc003_shot007, '001', '035']
    """
    data = cam.split("_")
    scene = data[1]
    shot = data[2]
    shot_name = "{0}_{1}".format(scene, shot)
    start_frame = data[2]
    end_frame = data[3]
    return scene, shot, shot_name, start_frame, end_frame


def seer7_cam_get_path():
    """用相机匹配路径"""
    cam_name = mayaTool.filter_camera("cam_*_*")
    short_name = seer7_split_cam(cam_name)
    path_animation = seer7_data()["cacheIO_an"]
    export_path = os.path.join(path_animation, short_name[0], short_name[2])
    if not os.path.isdir(export_path):
        os.makedirs(export_path)
    return export_path

def file_reference():
    references = mc.file(q=True, reference=True)
    return references


def format_path(source_pathName="", proxy_name="_SG"):
    path = os.path.dirname(source_pathName)
    name = os.path.basename(source_pathName)
    scene_name = path + "/" + name.split(".")[0] + proxy_name + "." + name.split(".")[1]  # atieda_SG.ma
    json_name = path + "/" + name.split(".")[0] + proxy_name + ".json"  # atieda_SG.json
    fix_name = name.split(".")[1]  # ma or mb
    return scene_name, json_name, fix_name




# def



















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


def auto_export_shader():
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


def auto_import_shader():
    pass


if __name__ == '__main__':
    setData()
