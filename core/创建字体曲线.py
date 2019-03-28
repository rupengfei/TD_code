# -*- coding:utf-8 -*-  
# ==========================================
#       author: Pengfei.Ru
#         mail: 773849069@qq.com
#         QQ: 773849069
#         time: 2019/3/4
# ==========================================
import maya.cmds as mc

# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*

curve1_name = "ASDWCSFDFASFCVAaaa"


def set_ChangeOverColor():
    sels = mc.ls(sl=1)
    for sel in sels:
        for shape in mc.listRelatives(sel, s=1, f=1):
            mc.setAttr(shape + '.overrideEnabled', 1)
            mc.setAttr(shape + '.overrideColor', 13)


def create_font_curve(font_name=""):
    font1 = mc.textCurves(ch=0, f="Times New Roman|wt:50|sz:28", t=font_name)
    sels = mc.listRelatives(mc.ls(dag=True, typ="nurbsCurve", sl=True), p=True)
    mc.group(sels, n="text")
    mc.select(sels, r=True)
    mc.makeIdentity(apply=True, t=1, r=1, s=1, n=0, pn=1)

    mc.rename(sels[0], font_name)
    old_curve1 = list()
    for num in range(len(sels))[1:]:
        curve1 = mc.rename(sels[num], font_name)
        mc.select(font_name, r=True)
        mc.parent(mc.listRelatives(curve1, s=True), add=True, shape=True)
        old_curve1.append(curve1)
    mc.select(font_name, r=True)
    mc.parent(w=True)

    mc.delete(font1)


create_font_curve(curve1_name)
curve1_name = mc.rename(curve1_name, curve1_name + "_LVL")
mc.addAttr(curve1_name, ln="LVL", at="enum", en="Body:Face:All:Render:")
mc.setAttr(curve1_name + ".LVL", e=True, keyable=True)
mc.select(curve1_name, r=True)
set_ChangeOverColor()
