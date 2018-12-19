# -*- coding:utf-8 -*-  
# ==========================================
#       author: Pengfei.Ru
#         mail: a773849069@gmail.com
#         time: 2018/12/14
# ==========================================
import maya.cmds as mc
import pymel.core as pm
import json
from Utils import mayaTool, ioTool
from core.shaderIO import shaderCore


# reload(mayaTool)
# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*


def abc_export(path, starts, ends, step, geos):
    """export 分配函数"""
    # abc_members = dict()
    start = starts - 2
    end = ends + 2
    mc.playbackOptions(e=True, min=start, max=end)
    for geo in geos:
        # print geo
        if pm.objExists(geo):
            pm.select(geo)
        else:
            continue
        out_file_name = path + "/" + mayaTool.name_rest(geo)
        # Gang:a_Geo To Gang_a_Geo
        out_json_name = out_file_name + ".json"
        try:
            pynode_geo = pm.PyNode(geo)
            if "Face_RenderMesh" in geo:
                print "Face_RenderMesh"
                ioTool.writeData(out_json_name, get_face_members(pynode_geo))
                # export_color_set(start, end, step, geo, out_file_name)
                continue
            if pynode_geo.getShapes():
                if pynode_geo.getShapes()[0].nodeType() == "camera":
                    print "cam"
                    ioTool.writeData(out_json_name,
                                     get_cam_members(pynode_geo, starts, ends, step, out_file_name, path))
                    # export_cam(path, geo)
                    continue
                if pynode_geo.getShapes()[0].nodeType() == "mesh":
                    print "mesh"  # 其他的 Geo
                    ioTool.writeData(out_json_name, get_mesh_members(pynode_geo))
                    # export_geo(start, end, step, geo, out_file_name)
                    continue
            else:
                print "Geo"  # 人物道具场景等 Geo, 有的geo可能不在Rig路径下
                # path  路径 geo名 .json
                ioTool.writeData(out_json_name, get_geo_members(pynode_geo))
                # export_geo(start, end, step, geo, out_file_name)
        except Exception as e:
            print e
    mc.playbackOptions(e=True, min=starts, max=ends)
    return True


def export_geo(start, end, step, geo, path):
    """导出几何物体"""
    mel_str = "AbcExport -j \""
    mel_str += "-frameRange {0} {1} ".format(start, end)
    mel_str += "-step {0} ".format(step)
    mel_str += "-uvWrite "
    mel_str += "-worldSpace "
    mel_str += "-writeVisibility "
    mel_str += "-dataFormat ogawa "
    mel_str += "-root {0} ".format(geo)
    mel_str += "-file {0}.abc\";".format(path)
    # print mel_str
    pm.mel.eval(mel_str)
    # AbcExport - j "-frameRange 101 110 -uvWrite -worldSpace -writeVisibility -dataFormat ogawa -root |Seer7_char_RIG_ATieDa_GangGuanChaRu1:Atieda_Mod_Rig|Seer7_char_RIG_ATieDa_GangGuanChaRu1:atieda_Geo -file Z:/SEER7/Work/Shot_work/cacheIO/Animation/sc003/sc003_shot007/atieda.abc";


def export_color_set(start, end, step, geo, path):
    """导出颜色集"""
    mel_str = "AbcExport -j \""
    mel_str += "-frameRange {0} {1} ".format(start, end)
    mel_str += "-step {0} ".format(step)
    mel_str += "-writeColorSets "
    mel_str += "-worldSpace "
    mel_str += "-dataFormat ogawa "
    mel_str += "-root {0} ".format(geo)
    mel_str += "-file {0}.abc\";".format(path)
    # print mel_str
    pm.mel.eval(mel_str)
    # AbcExport - j "-frameRange 101 110 -writeColorSets -worldSpace -dataFormat ogawa -root |Seer7_char_RIG_ATieDa_GangGuanChaRu1:Atieda_Mod_Rig|Seer7_char_RIG_ATieDa_GangGuanChaRu1:Face_RenderMesh -file Z:/SEER7/Work/Shot_work/cacheIO/Animation/sc003/sc003_shot007/face_atieda1.abc";


def export_cam(path, geo):
    """导出相机"""
    path = (path + "/" + geo + ".fbx")
    mc.file(path, force=True, options="v=0", typ="FBX export", pr=True, es=True)
    return True


def get_cam_members(cam, starts, ends, step, out_file_name, *args):
    """
    获取场景信息
        起始帧 100
        结束帧 101
        步值 1
        相机名称 cam_sc003_shot007_101_268
        原镜头名称 seer_sc003_shot007_ly_v02.ma
        原镜头地址 D:\Repo\seer7\cacheIO\Animation\sc003\sc003_shot007

        所有参考文件路径
            参考文件对应信息
    Returns:

    """
    data = dict()
    data["output_path"] = args[0]
    data["type"] = "cam_fbx"
    data["name"] = str(cam.name())
    data["link_name"] = mayaTool.name_rest(str(cam.name())) + ".fbx"
    data["start_frame"] = starts
    data["end_frame"] = ends
    data["step"] = step
    data["an_scene_name"] = mayaTool.get_scene_name()
    data["an_scene_path"] = mayaTool.get_scene_path()
    data["RN"] = mc.file(q=True, r=True)
    return data


def get_mesh_members(geo=None, *args):
    """获取不是参考文件的信息"""
    data = dict()
    data["namespace"] = str(geo.name())
    data["type"] = "mesh_abc"
    data["name"] = str(geo.name())
    data["link_name"] = mayaTool.name_rest(str(geo.name())) + ".abc"
    return data


def get_geo_members(geo="PyNode", typ="geo_abc", *args):
    """
    获取参考文件的相关信息
    文件名：通过镜头号得到abc路径  输出命名为: namespace:geo.abc
    json名：输出命名为  namespace:geo.json
    json内容：
        1 abc_Path    加载文件的时候附上 原场景的命名空间
        2 namespace
        3 shader_Path    场景加载好之后把材质导进来 模型的 namespace 进行着色
        4 模型和材质 ok
    导入需要：
        1 路径
        2
    """
    if geo.isReferenced():
        file_path = str(
            geo.referenceFile())  # 'Z:/SEER7/Work/Asset_work/Chars/ATieDa_ShengJi/Rig/approve/Seer7_char_RIG_ATieDa_ShengJi.ma'
        shader_name = file_path.split("/")[-1].split(".")  # ["Seer7_char_RIG_ATieDa_ShengJi", "ma"]
        shader_name = shader_name[0] + "_SG." + shader_name[1]  # file_name is Seer7_char_RIG_ATieDa_ShengJi_SG.ma
        shader_path = file_path.split("Rig")
        shader_path = shader_path[0] + "Rig/Shader/" + shader_name
        # shader_path is 'Z:/SEER7/Work/Asset_work/Chars/ATieDa_ShengJi/Rig/Shader/Seer7_char_RIG_ATieDa_ShengJi_SG.ma'
    else:
        shader_path = "None"

    data = dict()
    data["namespace"] = str(geo.namespace())[:-1]
    data["reference_file"] = str(geo.referenceFile())
    data["shader_file"] = shader_path
    data["type"] = typ
    data["link_name"] = mayaTool.name_rest(str(geo.name())) + ".abc"
    data["name"] = str(geo.stripNamespace())
    return data


def get_face_members(geo):
    """获取面部颜色集信息"""
    # return get_geo_members(geo, typ="face_abc")
    if geo.isReferenced():
        file_path = str(
            geo.referenceFile())  # 'Z:/SEER7/Work/Asset_work/Chars/ATieDa_ShengJi/Rig/approve/Seer7_char_RIG_ATieDa_ShengJi.ma'
        shader_name = file_path.split("/")[-1].split(".")  # ["Seer7_char_RIG_ATieDa_ShengJi", "ma"]
        shader_name = shader_name[0] + "_Face_RenderMesh_SG." + shader_name[
            1]  # file_name is Seer7_char_RIG_ATieDa_ShengJi_SG.ma
        shader_path = file_path.split("Rig")
        shader_path = shader_path[0] + "Rig/Shader/" + shader_name
        # shader_path is 'Z:/SEER7/Work/Asset_work/Chars/ATieDa_ShengJi/Rig/Shader/Seer7_char_RIG_ATieDa_ShengJi_SG.ma'
    else:
        shader_path = "None"

    data = dict()
    data["namespace"] = str(geo.namespace())[:-1]
    data["reference_file"] = str(geo.referenceFile())
    data["shader_file"] = shader_path
    data["type"] = "face_abc"
    data["link_name"] = mayaTool.name_rest(str(geo.name())) + ".abc"
    data["name"] = str(geo.stripNamespace())
    return data


def read_json(file_name):
    """读取配置"""
    with open(file_name, "r") as f:
        data = json.load(f)
    return data


def abc_import(path="D:/Repo", geos=tuple()):
    """import 分配函数"""
    if not geos:
        return False
    for geo in geos:
        geo_path = path + "/" + geo
        data = read_json(geo_path + ".json")
        if data["type"] == "cam_fbx":
            print "cam"
            import_cam(geo_path, data)
        if data["type"] == "face_abc":
            print "face_abc"
            import_face(geo_path, data)
        if data["type"] == "geo_abc":
            print "geo_abc"
            import_geo(geo_path, data)
        if data["type"] == "mesh_abc":
            print "mesh_abc"
            import_mesh(geo_path, data)
    return True


def import_cam(path, data):
    """导入 fbx 的相机"""
    reload(mayaTool)
    path = path + ".fbx"
    mayaTool.reference_file(path, name_space="camera", typ="fbx")
    mc.playbackOptions(e=True, min=data["start_frame"],
                       max=data["end_frame"],
                       ast=data["start_frame"],
                       aet=data["end_frame"])
    # print data


def import_face(path, data):
    """导入 面部颜色集"""
    path = path + ".abc"
    name_space = mayaTool.reference_file(path, name_space=data["namespace"], typ="abc")
    mc.setAttr(name_space + ":Face_RenderMeshShape.aiExportColors", 1)
    shaderCore.import_all_shader(data["shader_file"], name_space, data["namespace"])
    return True


def import_geo(path, data):
    """导入 参考文件 并附上材质"""
    path = path + ".abc"
    reload(shaderCore)
    name_space = mayaTool.reference_file(path, name_space=data["namespace"], typ="abc")
    shaderCore.import_all_shader(data["shader_file"], name_space, data["namespace"])
    return name_space

def import_mesh(path, data):
    """导入道具等几何体缓存"""
    path = path + ".abc"
    name_space = mayaTool.reference_file(path, name_space=data["namespace"], typ="abc")
    return name_space
