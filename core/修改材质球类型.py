# -*- coding:utf-8 -*-  
# ==========================================
#       author: Pengfei.Ru
#         mail: 773849069@qq.com
#         QQ: 773849069
#         time: 2019/3/8
# ==========================================
import maya.cmds as mc
# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*


shader_node = mc.ls(sl=True)[0]
sels = mc.ls(type="phong")


for sel in sels:
    node = mc.connectionInfo(sel+".color", sfd=True).split(".")[0]
    name_sg = mc.connectionInfo(sel+".outColor", dfs=True)
    if not node and not name_sg:
        continue
    mc.select(shader_node, r=True)
    name_ai = mc.duplicate(un=True)[0]
    if name_sg:
        name_sg = name_sg[0].split(".")[0]
        mc.connectAttr(name_ai+".outColor", name_sg+".surfaceShader", f=True)
    if node:
        mc.connectAttr(node+".outColor", name_ai+".baseColor", f=True)