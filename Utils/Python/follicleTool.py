#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 根据选择的地膜的毛囊创建 新毛囊到 高摸
#import CRT.Python.General.FollicleTool as ft
#ft.main()
#from CRT.Python.General.FollicleTool import *
#main()
import maya.cmds as cmds

'''
def closestPointOnMeshResult( object,meshHight ) :
    meshHightShapes = cmds.listRelatives( meshHight,s=True )
    meshHightShape = meshHightShapes[0]
    result = {}
    result = closestPointOnMeshResults(object,meshHight )
    return(result)
'''

def closestPointOnMeshResult( object,meshHight ) :
    result = {}
    meshHightShape = ''
    meshHightShapes = cmds.listRelatives( meshHight,s=True,path=True )
    for shape in meshHightShapes :
        if not cmds.getAttr("%s.intermediateObject" % shape) :
            meshHightShape = shape
            print(meshHightShape)
    node = cmds.createNode("closestPointOnMesh")
    cmds.connectAttr( (meshHightShape + ".outMesh"),(node+".inMesh") )
    grp1= cmds.group(em=True)
    cmds.delete( cmds.pointConstraint(object,grp1) )
    cmds.delete( cmds.geometryConstraint( meshHight,grp1) )

    pos = cmds.xform( grp1,q=True,ws=True,t=True)
    cmds.setAttr( node+".inPosition",pos[0],pos[1],pos[2] )
    result['faceIndex'] = cmds.getAttr(node + ".result.closestFaceIndex")
    result['vertexIndex'] = cmds.getAttr(node + ".result.closestVertexIndex")
    result['parameterU'] = cmds.getAttr(node + ".result.parameterU")
    result['parameterV'] = cmds.getAttr(node + ".result.parameterV")
    # ....
    cmds.select( object )
    cmds.delete(node,grp1)
    return( result )

def createFollByPosition() :
    listOldFoll = cmds.ls(sl=True)
    meshHight = cmds.textField("meshObjTF",q=True,text=True)
    pointList = []
    result={}
    createFollByPositionOBJ(listOldFoll,meshHight)
    return( pointList )
    print("OKKKKKKKKKKKK")

def createFollByPositionOBJ(listOldFoll,meshHight) :
    # listOldFoll = cmds.ls(sl=True)
    # meshHight = cmds.textField("meshObjTF",q=True,text=True)
    pointList = []
    result={}
    for foll in listOldFoll :
        result = closestPointOnMeshResult( foll,meshHight )
        vertexIndex = result['vertexIndex']
        point = (meshHight + ".vtx[" + str(vertexIndex) + "]")
        #cmds.select( point )
        #foll = createFoll( vertexIndex )
        folls = createFollicle( meshHight,result['parameterU'],result['parameterV' ]  )
        # cmds.rename( folls ,foll+'_foll')
        pointList.append( folls )
        cmds.select( cl=True )
    return( pointList )


#
# 根据选择的毛囊创建骨骼

def createJointBySelect() :
    listFolls = cmds.ls(sl=True)
    for i in range( len(listFolls) ) :
        cmds.select(cl=True)
        joints = cmds.joint(p=(0,0,0),name=listFolls[i] + '_jnt')
        groups = cmds.group(em=True,name =listFolls[i] + "Offset" )
        groups1 = cmds.group(em=True,name =listFolls[i] + "C1_ctl")
        groups2 = cmds.group(em=True,name =listFolls[i] + "C2_ctl")
        cmds.parent( joints,groups2 )
        cmds.parent( groups2,groups1 )
        cmds.parent( groups1,groups )
        cmds.parentConstraint( listFolls[i],groups,weight=True)
#
# foll
def createFoll( index ) :
    listJnts = cmds.ls(sl=True,fl=True)
    # follList = []
    return( createFoll_obj(listJnts) )


def createFoll_obj(listJnts) :
    # listJnts = cmds.ls(sl=True,fl=True)
    follList = []
    for i in range( len(listJnts) ) :
        foll = createFoll_sigle
        follList.append( foll )
        # cmds.select( cl=True )
    return( follList )

def createFoll_sigle(obj) :
    objects = ''
    meshHightShape = ''
    follicles = cmds.createNode('follicle')
    follicle = cmds.listRelatives(follicles,parent=True)
    if type(obj) is list :
        objects = obj[0].split('.')
    else:
        objects = obj.split('.')
    shapes = cmds.listRelatives( objects[0] )
    for shape in shapes :
        if not cmds.getAttr("%s.intermediateObject" % shape) :
            meshHightShape = shape
    cmds.connectAttr( (meshHightShape + '.outMesh'),(follicles + '.inputMesh') )
    cmds.connectAttr( (meshHightShape + '.worldMatrix[0]'),(follicles + '.inputWorldMatrix') )
    cmds.connectAttr( (follicles + '.outTranslate'),(follicle[0] + '.translate') )
    cmds.connectAttr( (follicles + '.outRotate'),(follicle[0] + '.rotate') )
    # cmds.select(obj)

    parU,parV = 0.0,0.0
    uvs = []

    uvs = getTranformUV(obj)
    parU = uvs[0]
    parV = uvs[1]
    cmds.setAttr( follicles + '.parameterU',parU)
    cmds.setAttr( follicles + '.parameterV',parV)
    cmds.select( cl=True )
    return(follicle[0])

def getTranformUV(obj) :
    # uv = ()
    uv = cmds.polyEditUV( obj,q=True,u=True )
    # UVbc = cmds.polyEvaluate(bc2=True)
    # parU = ( UVbc[0][0] + UVbc[0][1] ) / 2
    # parV = ( UVbc[1][0] + UVbc[1][1] ) / 2
    # parU = UVbc[0]
    # parV = UVbc[1]
    # uv = (parU,parV)
    return(uv)

def shortFloat( ts ) :
    tsStr = str(ts)
    tsStrSplit = tsStr.split('.')
    ts1_list = list(tsStrSplit[1])
    ts0=tsStrSplit[0]
    ts1=''
    for i in range(4) : ts1 += ts1_list[i]
    tsOk = ts0+'.'+ts1
    return(tsOk)

def printTranformUV():
    listObjs = cmds.ls(sl=True)
    if len(listObjs) == 1:
        resU,resV='',''
        meshHight = cmds.textField("meshObjTF",q=True,text=True)
        if cmds.nodeType(listObjs[0]) == "transform" or cmds.nodeType(listObjs[0]) == "joint" :
            result = closestPointOnMeshResult( listObjs[0],meshHight )
            resU = shortFloat( result['parameterU'] )
            resV = shortFloat( result['parameterV'] )
            print(result),
        else:
            result = getTranformUV()
            resU = shortFloat( result[0] )
            resV = shortFloat( result[1] )
            print(result),
        cmds.text('printTranformUVTX',e=True,label=("U: %s  V: %s" %(resU,resV)))

def addSelectMeshToTextField ():
    listObject = cmds.ls(sl=True)
    if len(listObject) == 1:
        cmds.textField("meshObjTF",e=True,text=listObject[0])

def follWindows() :
    text = "load mesh ... "
    listObjs = cmds.ls(sl=True)
    if len(listObjs):
        text = listObjs[0]

    if cmds.window("follToolWindow",q=True,ex=True) :
        cmds.deleteUI("follToolWindow")
    else:
        cmds.window("follToolWindow",title = "Follicle Tool",tlb=True)
        cmds.columnLayout(adj=True,rowSpacing=5)
        cmds.textField("meshObjTF",text=text,editable=False)
        cmds.button(label="Create Foll By Mesh",h=40,command="createFoll('')" )
        cmds.button(label="Create Foll By Select",h=40,command = "createFollByPosition()")
        # cmds.button(label="Create Foll By Select",bgc =(.5,.5,1),h=40,command = "createFollByPosition()")

        cmds.button(label="Create Joint By Select",h=40,command = "createJointBySelect()")
        cmds.button(label="Get UV Bound",h=25,command = "printTranformUV()")
        cmds.text('printTranformUVTX',label="-none-")
        cmds.popupMenu(p="meshObjTF")
        cmds.menuItem(label="Add Select Mesh",command="addSelectMeshToTextField()")
        cmds.showWindow("follToolWindow")


def createFollicle( meshShape,parU,parV ) :
    follicles = cmds.createNode('follicle')
    follicle = cmds.listRelatives(follicles,parent=True)
    cmds.setAttr( follicles + '.parameterU',parU)
    cmds.setAttr( follicles + '.parameterV',parV)
    cmds.connectAttr( ( meshShape + '.outMesh'),(follicles + '.inputMesh') )
    cmds.connectAttr( ( meshShape + '.worldMatrix[0]'),(follicles + '.inputWorldMatrix') )
    cmds.connectAttr( (follicles + '.outTranslate'),(follicle[0] + '.translate') )
    cmds.connectAttr( (follicles + '.outRotate'),(follicle[0] + '.rotate') )

    return( follicle[0] )


# main()
if __name__ == '__main__':
    main()