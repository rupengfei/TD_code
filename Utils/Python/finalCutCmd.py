#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 'cRebuildTool','FollicleTool','rename'
#
import maya.cmds as cmds
import maya.mel as mm
import math
from CRT.Python.cRebuildTool import *
from CRT.Python.follicleTool import *

def meshRepairCmd() :
    nodes={}
    mm.eval("ConvertSelectionToUVs()")
    # ConvertSelectionToUVs
    # ConvertSelectionToVertices
    listObj = cmds.ls(sl=True,fl=True)
    size = len(listObj)
    if size > 0 and '.' in listObj[0] :
        lockAttrList,hideObjList,parentsAllList = [],[],[]
        dist,distMax = 0.0,0.0
        modifyWeight = 0
        transformName = ''

        folliclesList = createFoll_sigle( listObj[0] )
        cmds.select(listObj)
        mm.eval("ConvertSelectionToVertices()")
        listObj = cmds.ls(sl=True,fl=True)
        splitObject = listObj[0].split('.')
        transform = splitObject[0]
        if ':' in transform :
            nameSplit = transform.split(':')
            transformName = nameSplit[1]
        else: transformName = transform

        parentsList = cmds.listRelatives( transform,parent=True )
        if parentsList is None :pass
        else: parentsAllList = getParentsCmd(transform)
        # parentsAllList = getParentsCmd(transform)

        pe_v = cmds.polyEvaluate( transform,v=True )
        # create cluster object
        # tmpCluster = cmds.cluster( before =True)#
        # folliclesList = createFollByPositionOBJ( [tmpCluster[1]],transform )
        # folliclesList = createFoll_sigle( listObj[0] )        #########################################
        # result = closestPointOnMeshResult( [tmpCluster[1]],transform )
        # print(result) faceIndex     result['faceIndex']
        nodes['follicles'] = folliclesList
        # cmds.delete(tmpCluster)
        newCluster = cmds.cluster(transform,before =True)
        clusters = newCluster[0]
        nodes['clusterHandle'] = newCluster[1]
        cmds.setAttr( "%s.relative" % clusters,1 )
        # set cluster weight
        # mm.eval("ConvertSelectionToVertices()")
        cmds.percent( clusters,'%s.vtx[0:%d]' % (transform,pe_v ),v=0 )
        cmds.percent( clusters,listObj,v=1)

        nodes['G1'] = cmds.group(em=True)
        nodes['G2'] = cmds.group(em=True)
        nodes['G3'] = cmds.group(em=True)
        cmds.parent(nodes['G2'],nodes['G1'])
        cmds.parent(nodes['G3'],nodes['G2'])
        cmds.connectAttr( ("%s.t" % nodes['G3']) ,("%s.t" % nodes['clusterHandle']) )
        cmds.connectAttr(('%s.r' % nodes['G3']),('%s.r' % nodes['clusterHandle']))
        cmds.connectAttr(('%s.s' % nodes['G3']),('%s.s' % nodes['clusterHandle']))

        cmds.pointConstraint(nodes['follicles'],nodes['G1'])
        # set
        nodes['mdNode1'] = cmds.createNode('multiplyDivide')
        cmds.setAttr( '%s.input2' % nodes['mdNode1'],-1,-1,-1 )
        cmds.connectAttr(('%s.t' % nodes['G3']),('%s.input1' % nodes['mdNode1']) )
        cmds.connectAttr( ('%s.output' % nodes['mdNode1']),('%s.t' % nodes['G2']) )
        # setParent..
        nodes['defGrp'] = cmds.group( nodes['follicles'],nodes['clusterHandle'],nodes['G1'] )
        if len(parentsAllList):
            cmds.parent( nodes['defGrp'],parentsAllList[-1] )
        # cmds.parent( nodes['defGrp'],parentsAllList[-1] )
        hideObjList = [nodes['follicles'],nodes['clusterHandle']]
        lockAttrList = [nodes['G1'],nodes['G2'],nodes['follicles'],nodes['clusterHandle'],nodes['defGrp'],nodes['mdNode1']]
        # lock and hide attr ....
        for hideObj in hideObjList :
            cmds.setAttr('%s.v' % hideObj,0)
        for obj in lockAttrList :
            attrList = cmds.listAttr( obj,keyable=True)
            for attr in attrList :
                cmds.setAttr( '%s.%s' % (obj,attr),lock=True,keyable=False,channelBox=False )

        # add attr
        RS_Pivot = "RS_Pivot"
        envelope = "envelope"
        cmds.addAttr( nodes['G3'],ln=envelope,at='double',min=0,max=1,dv=1 )
        cmds.setAttr( '%s.%s' % (nodes['G3'],envelope),keyable=True )
        cmds.connectAttr( ('%s.%s' % (nodes['G3'],envelope) ),('%s.%s') % (clusters,envelope) )
        cmds.addAttr( nodes['G2'],ln=RS_Pivot,at='double3')
        cmds.addAttr( nodes['G2'],ln=('%sX' % RS_Pivot),at='double',p=RS_Pivot)
        cmds.addAttr( nodes['G2'],ln=('%sY' % RS_Pivot),at='double',p=RS_Pivot)
        cmds.addAttr( nodes['G2'],ln=('%sZ' % RS_Pivot),at='double',p=RS_Pivot)
        cmds.setAttr( '%s.%s' % (nodes['G2'],RS_Pivot),keyable=True )
        cmds.setAttr( '%s.%sX' % (nodes['G2'],RS_Pivot),keyable=True )
        cmds.setAttr( '%s.%sY' % (nodes['G2'],RS_Pivot),keyable=True )
        cmds.setAttr( '%s.%sZ' % (nodes['G2'],RS_Pivot),keyable=True )

        cmds.connectAttr( ('%s.%s' % (nodes['G2'],RS_Pivot) ),('%s.rotatePivot') % nodes['clusterHandle'] )
        cmds.connectAttr( ('%s.%s' % (nodes['G2'],RS_Pivot) ),('%s.scalePivot') % nodes['clusterHandle'] )

        # add shape on group
        cmds.setAttr( "%s.displayHandle" % nodes['G3'],1,k=True)
        cmds.setAttr( "%s.v" % nodes['G3'],1,k=False)
        size = .25
        if cmds.currentUnit(q=True,linear=True) == 'm' :
            size = .025
        replaceShape( nodes['G3'],'c_box',size,0,25 )

        cmds.select(nodes['G3'])
        setKeyFrameCmd(1,'+')
        setKeyFrameCmd(1,'-')
        resetPivotCmd_select()
        try:
            import CRT.Python.rename as cRename
            vid = listObj[0].split('[')[1].split(']')[0]
            cRename.renameDict1( nodes,("%sF%d_" % (transformName,vid)) )
        except :
            pass

    return(nodes)

def resetPivotCmd( ctlObj ) :
    if "|" in ctlObj :
        splitStr = ctlObj.split('|')
        souObj = splitStr[len(splitStr) - 3]
        tanObj = splitStr[len(splitStr) - 2]

        gAttrT = cmds.getAttr('%s.t' % souObj)
        cmds.setAttr('%s.RS_Pivot' % tanObj,gAttrT[0][0],gAttrT[0][1],gAttrT[0][2] )
        cmds.setKeyframe( tanObj,at="RS_Pivot")

def resetPivotCmd_List(listObjs) :
    for obj in listObjs :
        resetPivotCmd(obj)

def resetPivotCmd_select() :
    listObjs = cmds.ls(sl=True,l=True,allPaths=True)
    resetPivotCmd_List(listObjs)

def bakePivotCmd() :
    listObjs = cmds.ls(sl=True,l=True,allPaths=True)
    minTime = int( cmds.playbackOptions(q=True,min=True) )
    maxTime = int( cmds.playbackOptions(q=True,max=True) )
    for i in range( minTime,maxTime+1 ) :
        resetPivotCmd_List(listObjs)
        mm.eval("playButtonStepForward")

def setKeyFrameCmd( distTime,pos ) :
    listObjs = cmds.ls(sl=True)
    attrList = ['t','r','s']
    for obj in listObjs :
        gTime = cmds.currentTime(query=True)
        cmds.setKeyframe( obj,time=(gTime),at=attrList)
        if pos == '+' or pos == '-' :
            for attr in attrList:
                atTime = eval("%d%s%d" % (gTime,pos,distTime))
                if 's' in attr : cmds.setKeyframe( obj,time=atTime,v=1,at=attr)
                else : cmds.setKeyframe( obj,time=atTime,v=0,at=attr)

def paintClusterWightCmd() :
    listObjs = cmds.ls(sl=True)
    if len(listObjs):
        clusObj = listObjs[0]
        attrs = 'envelope'
        attrs_out = 'outputGeometry'
        try:
            clusObjList = cmds.connectionInfo('%s.%s' % (clusObj,attrs),destinationFromSource=True )
            clustSplit = clusObjList[0].split('.')
            clusters = clustSplit[0]
            listAttrs = [clusters]
            while 1 :
                if cmds.attributeQuery( attrs_out,exists=True,node=listAttrs[0] ) :
                    listAttrs = cmds.listConnections( ('%s.%s' % (listAttrs[0],attrs_out)),destination=True)
                else : break
            cmds.select(listAttrs[0])
            evalCmd = "artAttrToolScript 3 \"cluster\";artSetToolAndSelectAttr( \"artAttrCtx\", \"cluster.%s.weights\" )" % (clusters)
            mm.eval(evalCmd)

        except:
            print("you need select controls .")

def deleteControlCmd() :
    listCtls = cmds.ls(sl=True)
    comstr = "null"
    comstrA = "group"
    for ctl in listCtls :
        if comstr in ctl :
            gParents = getParentsCmd(ctl)
            if comstrA in gParents[2] :
                cmds.delete(gParents[2])