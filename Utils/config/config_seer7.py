# -*- coding:utf-8 -*-
# ==========================================
#       author: Pengfei.Ru
#         mail: a773849069@gmail.com
#         time: 2018/12/9
# ==========================================
from Utils import scriptTool, ioTool, mayaTool, pathTool
import os
import maya.cmds as mc
import pymel.core as pm
from core.shaderIO import shaderCore

# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*

"""
[u'Z:/SEER7/Work/Asset_work/Env/BaiMuXingFeiChuanShiShiDiZhi/Mod/Layout_Env/Seer7_Env_to_layout.ma',
 u'Z:/SEER7/Work/Asset_work/Chars/ATieDa_ShengJi/Rig/approve/Seer7_char_RIG_ATieDa_ShengJi.ma',
 u'Z:/SEER7/Work/Asset_work/Props/ATieDa_BeiBao/Rig/approve/Seer7_Props_RIG_ATieDa_BeiBao.ma',
 u'D:/cloth/scenes/seer7_test/atieda_v03.ma',
 u'D:/cloth/scenes/seer7_test/atieda_v03.ma{1}'] 
 """


def references_replace_render():
    mayaTool.references_loaded(".", "_render.", only_load=True)


def references_replace_anim():
    mayaTool.references_loaded("_render", "", only_load=True)


def references_replace_all():
    mayaTool.references_loaded(".", "_render.", only_load=False, load_all=True)


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


def seer7_setting_render():
    geos = list()
    geos.extend(mc.ls("*:*_LVL"))
    geos.extend(mc.ls("*_LVL"))
    for geo in geos:
        try:
            mc.setAttr(geo + ".LvL", 3)
        except RuntimeError:
            mc.setAttr(geo + ".LvL", 2)
    return True


def seer7_split_cam(cam="cam_sc003_shot007_101_268"):
    """
    相机名称过滤镜头号 时间帧信息
    data = ['sc003', 'shot007', sc003_shot007]
    Returns: data
    """
    data = cam.split("_")
    scene = data[1]
    shot = data[2]
    shot_name = "{0}_{1}".format(scene, shot)
    return scene, shot, shot_name


def seer7_cam_get_path():
    """用相机匹配路径"""
    cam_name = mayaTool.filter_camera("cam_*_*")
    if not cam_name:
        print "not camera"
        return "D:/Cache"
    short_name = seer7_split_cam(cam_name)
    path_animation = seer7_data()["cacheIO_an"]
    export_path = os.path.join(path_animation, short_name[0], short_name[2], "approve/Cache").replace("\\", "/")
    if not os.path.isdir(export_path):
        os.makedirs(export_path)
    return export_path


def sel_rn_Geo(rn="Chars"):
    prop_geo = list()
    geos = mc.ls("*:*_Geo")
    geos.extend(mc.ls("*:*:*_Geo"))
    geos.extend(mc.ls("*:*:*:*_Geo"))
    try:
        for geo in geos:
            g = pm.PyNode(geo)
            if rn in str(g.referenceFile()):
                prop_geo.append(geo)
    except Exception as exp:
        print exp
    return prop_geo

def sel_Face_RenderMesh():
    face = mc.ls("*:*_FaceRenderMesh_Grp")
    face.extend(mc.ls("*:*:*_FaceRenderMesh_Grp"))
    face.extend(mc.ls("*:*:*:*_FaceRenderMesh_Grp"))
    return face


def sel_mod(cam, color_set, body, prop, BG, other):
    geo_grp = list()
    if cam:
        geo_grp.extend([mayaTool.filter_camera("cam_*_*"), ])
    if color_set:
        geo_grp.extend(sel_Face_RenderMesh())
    if body:
        geo_grp.extend(sel_rn_Geo("Chars"))
    if prop:
        geo_grp.extend(sel_rn_Geo("Props"))
    if BG:
        geo_grp.extend(sel_rn_Geo("Env"))
    if other:
        geo_grp.extend(mc.ls("*_Geo"))

    return geo_grp

def refresh_list():
    return list("abcdefjhijklmnopqrstuvwxyz")


def seer7_find_files(path, fix="json", take_fix=True):
    """从 Cache 下找一层文件"""
    r_json = list()
    for cwd in os.listdir(path):
        if cwd == "Cache":
            cache_path = os.path.join(path, cwd)
            for geo in os.listdir(cache_path):
                if os.path.splitext(geo)[-1] == ("." + fix):
                    if take_fix:
                        r_json.append("Cache/" + geo)
                    else:
                        r_json.append(os.path.splitext("Cache/" + geo)[0])
        if os.path.splitext(cwd)[-1] == ("." + fix):
            if take_fix:
                r_json.append(cwd)
            else:
                r_json.append(os.path.splitext(cwd)[0])
    return r_json
    #     if os.path.isdir(names):
    #         r_json.extend(find_file1(names, take_fix))
    #     if os.path.splitext(names)[-1] == ("." + fix):
    #         if take_fix:
    #             r_json.append(cwd)
    #         else:
    #             r_json.append(os.path.splitext(names)[0])
    # return r_json

def seer7_shader_format_path():
    """
    """
    source_file = mayaTool.get_scene_path()
    if source_file == "":
        source_file = mc.internalVar(uwd=True) + "Rig/untitled.ma"
    path = pathTool.recombine_path(source_file, "Rig", "Rig/shader")
    if not os.path.exists(path):
        os.makedirs(path)
    name = os.path.basename(source_file)
    scene_name = path + "/" + name.split(".")[0] + "_SG." + name.split(".")[1]  # atieda_SG.ma
    json_name = path + "/" + name.split(".")[0] + "_SG.json"  # atieda_SG.json
    fix_name = name.split(".")[1]  # ma or mb

    return scene_name, json_name, fix_name


def auto_export_shader():
    scene_name, json_name, fix_name = seer7_shader_format_path()
    geos = mc.ls("*_Geo") or list()
    print scene_name
    for geo in geos:
        sels = mc.ls(geo, dag=True, typ="mesh")
        sels1 = mc.listRelatives(sels, p=True)
        shaderCore.export_sel_sg_nodes(scene_name, fix_name, sels1[:])
        shaderCore.export_sel_sg_members(json_name, sels1[:])
    return True

def auto_export_abc():
    from core.abcIO import Abc_Core
    references_replace_render()
    path = seer7_cam_get_path()  # 输出路径
    if not os.path.exists(path):
        os.makedirs(path)
    playblast_time = mayaTool.get_time_slider()
    start = playblast_time[0] # 起始帧
    end = playblast_time[1]  # 结束帧
    step = playblast_time[-1]  # 子步值
    geo_name = sel_mod(cam=True, color_set=True, body=True, prop=True, BG=False, other=False)
    Abc_Core.abc_export(path, start, end, step, geo_name)
    return True

def auto_import_shader():
    pass

def seer7_set_all_LVL_to_render(opened=True):
    geos = list()
    geos.extend(mc.ls("*:*:*:*:*:*_LVL"))
    geos.extend(mc.ls("*:*:*:*:*_LVL"))
    geos.extend(mc.ls("*:*:*:*_LVL"))
    geos.extend(mc.ls("*:*:*_LVL"))
    geos.extend(mc.ls("*:*_LVL"))
    geos.extend(mc.ls("*_LVL"))
    if opened:
        for geo in geos:
            try:
                try:
                    try:
                        mc.cutKey(geo + ".LvL", clear=True)
                        mc.setAttr(geo + ".LvL", 3)
                    except:
                        mc.cutKey(geo + ".LvL", clear=True)
                        mc.setAttr(geo + ".LvL", 2)
                except:
                    try:
                        mc.cutKey(geo + ".LVL", clear=True)
                        mc.setAttr(geo + ".LVL", 3)
                    except:
                        mc.cutKey(geo + ".LVL", clear=True)
                        mc.setAttr(geo + ".LVL", 2)
            except:
                pass
    else:
        for geo in geos:
            try:
                try:
                    mc.cutKey(geo + ".LvL", clear=True)
                    mc.setAttr(geo + ".LvL", 0)
                except:
                    mc.cutKey(geo + ".LVL", clear=True)
                    mc.setAttr(geo + ".LVL", 0)
            except:
                pass
    return True

if __name__ == '__main__':
    setData()
