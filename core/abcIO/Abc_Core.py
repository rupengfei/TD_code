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
    abc_members = dict()
    for geo in geos:
        abc_members[geo] = get_members(geo)

def get_members(geo=(u'pSphere1_Geo', u'Seer7_Props_RIG_ATieDa_BeiBao1:MD_ATieDaBeiBao_Geo')):
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

