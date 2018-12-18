# -*- coding:utf-8 -*-  
# ==========================================
#       author: Pengfei.Ru
#         mail: a773849069@gmail.com
#         time: 2018/12/14
# ==========================================
import maya.cmds as mc
import pymel.core as pm
from Utils import mayaTool
# reload(mayaTool)
# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*


def abc_export(path, starts, ends, step, geos):
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
        try:
            if "Face_RenderMesh" in geo:
                export_color_set(start, end, step, geo, path)
                continue
            pynode_geo = pm.PyNode(geo)
            if pynode_geo.getShapes():
                if pynode_geo.getShapes()[0].nodeType() == "camera":
                    export_cam(path, geo)
                    continue
                if pynode_geo.getShapes()[0].nodeType() == "mesh":
                    print "mesh"
                    export_geo(start, end, step, geo, path)
                    continue
            else:
                # print "Geo"
                export_geo(start, end, step, geo, path)
        except Exception as e:
            print e
    mc.playbackOptions(e=True, min=starts, max=ends)
    return True


def export_geo(start, end, step, geo, path):
    mel_str = "AbcExport -j \""
    mel_str += "-frameRange {0} {1} ".format(start, end)
    mel_str += "-step {0} ".format(step)
    mel_str += "-uvWrite "
    mel_str += "-worldSpace "
    mel_str += "-writeVisibility "
    mel_str += "-dataFormat ogawa "
    mel_str += "-root {0} ".format(geo)
    mel_str += "-file {0}.abc\";".format(path + "/" + mayaTool.reference_name_restructuring(geo))
    # print mel_str
    pm.mel.eval(mel_str)
    # AbcExport - j "-frameRange 101 110 -uvWrite -worldSpace -writeVisibility -dataFormat ogawa -root |Seer7_char_RIG_ATieDa_GangGuanChaRu1:Atieda_Mod_Rig|Seer7_char_RIG_ATieDa_GangGuanChaRu1:atieda_Geo -file Z:/SEER7/Work/Shot_work/cacheIO/Animation/sc003/sc003_shot007/atieda.abc";


def export_color_set(start, end, step, geo, path):
    mel_str = "AbcExport -j \""
    mel_str += "-frameRange {0} {1} ".format(start, end)
    mel_str += "-step {0} ".format(step)
    mel_str += "-writeColorSets "
    mel_str += "-worldSpace "
    mel_str += "-dataFormat ogawa "
    mel_str += "-root {0} ".format(geo)
    mel_str += "-file {0}.abc\";".format(path + "/" + mayaTool.reference_name_restructuring(geo))
    # print mel_str
    pm.mel.eval(mel_str)
    # AbcExport - j "-frameRange 101 110 -writeColorSets -worldSpace -dataFormat ogawa -root |Seer7_char_RIG_ATieDa_GangGuanChaRu1:Atieda_Mod_Rig|Seer7_char_RIG_ATieDa_GangGuanChaRu1:Face_RenderMesh -file Z:/SEER7/Work/Shot_work/cacheIO/Animation/sc003/sc003_shot007/face_atieda1.abc";


def export_cam(path, geo):
    path = (path + "/" + geo + ".fbx")
    mc.file(path, force=True, options="v=0", typ="FBX export", pr=True, es=True)
    return True


def get_cam_members():
    pass


def get_geo_members(geo=(u'pSphere1_Geo', u'Seer7_Props_RIG_ATieDa_BeiBao1:MD_ATieDaBeiBao_Geo')):
    """
    文件名：通过 镜头号 得到abc路径  输出命名为  namespace:geo.abc
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
    pynode_geo = pm.PyNode(geo)
    if pynode_geo.isReferenced():
        NameSpace = pynode_geo.namespace()

        return NameSpace
    # print dir(pynode_geo)
    # print pynode_geo.referenceFile()  # Z:/SEER7/Work/Asset_work/Props/ATieDa_BeiBao/Rig/approve/Seer7_Props_RIG_ATieDa_BeiBao.ma
    if pynode_geo.isReferenced():  # True
        print pynode_geo.namespace()  # 名称空间 Seer7_char_RIG_ATieDa_ShengJi2:
        print pynode_geo.stripNamespace()  # 带名称空间 atieda_Geo
        print pynode_geo.nextUniqueName()  # 下一个唯一的名字 Seer7_char_RIG_ATieDa_ShengJi2:atieda_Geo1



def import_abc():
    """
    import
    """
    pass
