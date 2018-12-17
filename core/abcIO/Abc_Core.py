# -*- coding:utf-8 -*-  
# ==========================================
#       author: Pengfei.Ru
#         mail: a773849069@gmail.com
#         time: 2018/12/14
# ==========================================
import maya.cmds as mc
import pymel.core as pm

# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*
def export_mod():
    pass

def abc_export(path, start, end, step, geos):
    # abc_members = dict()
    for geo in geos:
        pm.select(geo)
        if "Face_RenderMesh" in geo:
            print "color_set"
            continue
        pynode_geo = pm.PyNode(geo)
        if pynode_geo.getShapes():
            if pynode_geo.getShapes()[0].nodeType() == "camera":
                print "cam"
                continue
            if pynode_geo.getShapes()[0].nodeType() == "mesh":
                print "mesh"
                continue
        else:
            print "Geo"
    return True


def export_geo(start, end, step, geo, path):
    mel_str = "AbcExport - j \""
    mel_str += "-frameRange {0} {1} ".format(start, end)
    mel_str += "-step {0} ".format(step)
    mel_str += "-uvWrite "
    mel_str += "-worldSpace "
    mel_str += "-writeVisibility "
    mel_str += "-dataFormat ogawa "
    mel_str += "-root {0} ".format(geo)
    mel_str += "-file {0}.abc\";".format(path)

    print mel_str
    # pm.mel.eval()
    # AbcExport - j "-frameRange 101 110 -uvWrite -worldSpace -writeVisibility -dataFormat ogawa -root |Seer7_char_RIG_ATieDa_GangGuanChaRu1:Atieda_Mod_Rig|Seer7_char_RIG_ATieDa_GangGuanChaRu1:atieda_Geo -file Z:/SEER7/Work/Shot_work/cacheIO/Animation/sc003/sc003_shot007/atieda.abc";

def export_color_set():
    pass
    # AbcExport - j "-frameRange 101 110 -writeColorSets -worldSpace -dataFormat ogawa -root |Seer7_char_RIG_ATieDa_GangGuanChaRu1:Atieda_Mod_Rig|Seer7_char_RIG_ATieDa_GangGuanChaRu1:Face_RenderMesh -file Z:/SEER7/Work/Shot_work/cacheIO/Animation/sc003/sc003_shot007/face_atieda1.abc";


def export_cam():
    print "cam"


def get_members(geo=(u'pSphere1_Geo', u'Seer7_Props_RIG_ATieDa_BeiBao1:MD_ATieDaBeiBao_Geo')):
    """返回嵌套字典   {"geo":{"namespace":"Seer7_char_RIG_ATieDa_ShengJi2"}, "geo2":{"name":"aa"}}"""
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

