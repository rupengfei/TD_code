#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
这个命令工具用来创建动力学骨骼链
1. 根据一条curve创建
2. 骨骼、控制器的数量可自定义，最好是骨骼的数量是控制器的数量的倍数关系


修改历史 ：
Monday, December 31, 2012 2:35:09 PM
1. 添加挤压强度控制（squathIntensity） ，用来控制骨骼拉长时的骨骼自动变瘦的强度

'''

import maya.cmds as cmds
import maya.mel as mm
from CRT.Python.cRebuildTool import *

try :
    import cAddAttr as cAddAttr
    import rename as cRename
except :
    try :
        import CRT.Python.cAddAttr as cAddAttr
        import CRT.Python.rename as cRename
    except:
        pass

def makeSpine(bCurve,bUpLoc,bJntNum,bCtrlNum,bName,controlSize,ctlName = "IKFK") :

    ''' chuang jian ik spine system '''
    createJoint            = 1
    createDynamicsCurve    = 1
    createSpineIKHandle    = 1
    createStretch          = 1
    createSquash           = 1
    connectStretch         = 1
    createControls         = 1
    connectControls        = 1
    setParentControls      = 1
    addAttrDynamics        = 1
    setParentOutliner      = 1
    setParentDeform        = 1
    rename_1               = 1
    channelsAttrs          = 1
    port = 1
    
    rootJoints = []
    rootRollIKJnts = []
    rootSkins = []
    rootGrp1 = []
    rootGrp2 = []
    skinGroup = ''
    sizeJnt = 0
    DynSys = {}
    linkPMD = {}
    spineJointStr = {}
    spineJointSqu = {}
    rollIKNode    = {}
    ikHSystem = []
    rootGrpCtrlCVs = []
    rootGrpC1s = []
    rootGrpCFK_down = []
    rootGrpCIK_down = []
    returnOutput =()
    PointOnCurveTmp = []
    clen = 0
    shapeAttrs = ['lodVisibility']    
    spineIKHandleCurve = bCurve
    spineControlCurve = bCurve 
    cmds.makeIdentity( bCurve,apply=True,t=True,r=True,s=True,n=False )
    
    if createJoint :
        cmds.rebuildCurve( bCurve,s = bJntNum )
        rootJoints = ctrlGroup( 'joint','ep',bCurve,bUpLoc,bJntNum,'True' )
        rootRollIKJnts = ctrlGroup( 'joint','ep',bCurve,bUpLoc,bJntNum,'True' )
        rootSkins = ctrlGroup( 'joint','ep',bCurve,bUpLoc,bJntNum,'True' )
        
        rootGrp1 = ctrlGroup( 'group','ep',bCurve,bUpLoc,bJntNum,'' )
        rootGrp2 = ctrlGroup( 'group','ep',bCurve,bUpLoc,bJntNum,'' )
        sizeJnt = len(rootJoints)
        cmds.rebuildCurve( bCurve,s = bCtrlNum)
        
        if setParentDeform :
            
            linkPMD = linkToRollIKJnt( rootJoints,rootRollIKJnts )
            
            intensionYAttr = 'intensionY'
            offsetYAttr = 'offsetY'
            intensionZAttr = 'intensionZ'
            offsetZAttr = 'offsetZ'
            try:
                rollIKNode = createRollIK( rootRollIKJnts,linkPMD,intensionYAttr,offsetYAttr,intensionZAttr,offsetZAttr )
            except:
                pass
            if rename_1 :
                try :
                    cRename.renameDict1( linkPMD,( bName + '') )
                    cRename.renameDict1( rollIKNode,( bName + '') )
                except :
                    pass
                
            skinGroup = cmds.group(em=True,name = bName + 'DeformSys_grp' )
            for i in range( sizeJnt ) :
                cmds.parent( (rootSkins[i]),(rootGrp2[i]) )
                cmds.parent( (rootGrp2[i]),(rootGrp1[i]) )                
                cmds.parentConstraint( rootRollIKJnts[i],rootGrp1[i],mo=True,weight=True )
                # cmds.scaleConstraint( rootRollIKJnts[i],rootGrp1[i] )
                cmds.connectAttr( rootRollIKJnts[i]+'.s',rootGrp1[i]+'.s' )
                replaceShape( rootGrp2[i],'c_box',(controlSize*.25),0,27 )
                cmds.parent((rootGrp1[i]),skinGroup)
            
        if createDynamicsCurve :
            DynSys = curvesDynamics( bCurve )
        if createSpineIKHandle :
            if createDynamicsCurve :
                spineIKHandleCurve = DynSys['OG'][1]
            ikHSystem = spineIKH( rootJoints,spineIKHandleCurve )
            if createStretch :
                spineJointStr = spineJoint_str( rootJoints,spineIKHandleCurve )    
            if createSquash :
                spineJointSqu = spineJoint_squash( rootJoints )
                
        if createControls :
            rootGrpCtrlCVs = ctrlGroup( 'locator','cv',bCurve,bUpLoc,bCtrlNum,'' )
            channelsAttr( rootGrpCtrlCVs,shapeAttrs,'shapeVisHide' )
            rootGrpC1s = ctrlGroupMake('group',rootJoints,bCtrlNum,'True')
            rootGrpCFK_up = ctrlGroupMake('group',rootJoints,bCtrlNum,'')
            rootGrpCFK_m = ctrlGroupMake('group',rootJoints,bCtrlNum,'')
            rootGrpCFK_down = ctrlGroupMake('group',rootJoints,bCtrlNum,'')
            rootGrpCIK_up = ctrlGroupMake('group',rootJoints,bCtrlNum,'')
            rootGrpCIK_m = ctrlGroupMake('group',rootJoints,bCtrlNum,'')
            rootGrpCIK_down = ctrlGroupMake('group',rootJoints,bCtrlNum,'')

            clen = len(rootGrpC1s)
            if connectControls :
                if createDynamicsCurve :
                    spineControlCurve = DynSys['FG'][2]
                spineControlCurveShapes = cmds.listRelatives( spineControlCurve )
                shpaeLen = len( spineControlCurveShapes )
                spineControlCurveShape = spineControlCurveShapes[ shpaeLen-1 ]
                if createDynamicsCurve :
                    spineControlCurveShape = spineControlCurveShapes[ shpaeLen-1 ]
                for i in range( len(rootGrpCtrlCVs) ) :
                    ctrlShapes = cmds.listRelatives(rootGrpCtrlCVs[i])
                    cmds.connectAttr( (ctrlShapes[0] + '.worldPosition[0]'),( spineControlCurveShape + '.controlPoints[' + str(i) + ']') )

            ###
			# 添加轴向旋转功能
			# Friday, January 04, 2013 10:21:35 AM 
            if createSpineIKHandle:
            	ikhTwistControlEnable( ikHSystem[0],rootGrpCtrlCVs[0],rootGrpCtrlCVs[-1] )
            
            if setParentControls :
            	for i in range( clen ) :
                    cmds.parent( (rootGrpCFK_up[i]),(rootGrpC1s[i]) )
                    cmds.parent( (rootGrpCFK_m[i]),(rootGrpCFK_up[i]) )
                    cmds.parent( (rootGrpCFK_down[i]),(rootGrpCFK_m[i]) )
                    cmds.parent( (rootGrpCIK_up[i]),(rootGrpCFK_down[i]) )
                    cmds.parent( (rootGrpCIK_m[i]),(rootGrpCIK_up[i]) )
                    cmds.parent( (rootGrpCIK_down[i]),(rootGrpCIK_m[i]) )

                    replaceShape( rootGrpCFK_m[i],'c_circle',controlSize,0,17 )
                    replaceShape( rootGrpCIK_m[i],'c_circle',controlSize*.75,0,4 )

                    if i > 0 :
                        cmds.parent( (rootGrpC1s[i]),(rootGrpCFK_down[i-1]) )
                        if i < (clen - 1) :
                            cmds.parent( rootGrpCtrlCVs[i+1],rootGrpCIK_down[i] )
                        try :
                            cmds.parent( rootGrpCtrlCVs[-1],rootGrpCtrlCVs[-2],rootGrpCIK_down[-1] )
                        except :
                            pass
                    else :
                        cmds.parent( rootGrpCtrlCVs[0],rootGrpCtrlCVs[1],rootGrpCIK_down[0] )
                       
        if addAttrDynamics and createControls and createDynamicsCurve :
            vis_grp = ""
            dl_grp = ""
            if connectStretch and createStretch :
                vis_grp = cmds.group(em=True)
                cmds.delete(cmds.pointConstraint( rootGrpCFK_m[0],vis_grp ))
                cmds.setAttr( vis_grp + '.tx',controlSize*1.2 )
                replaceShape( vis_grp,ctlName,controlSize*.5,0,15 )# ;addTestCurves( vis_grp,controlSize*.4,'IKFK',-3.0 )
                cmds.parentConstraint( rootGrpCFK_m[0],vis_grp ,mo=True,w=1)

                addAttributeBase1_1( rootGrpCFK_m[0],"")
                addAttributeBase1( vis_grp,"")

                connectStretch1 = 1
                if connectStretch1 :
                    cmds.connectAttr( (rootGrpCFK_m[0] + '.stretch'),(spineJointStr['onOff'] + '.blender') )
					#  spineJointSqu 
					#
					# Monday, December 31, 2012
					# 2:25:59 PM 
                    for i in range( bJntNum ) :
                    	cmds.connectAttr( (rootGrpCFK_m[0] + '.squathIntensity'),(rootJoints[i] + '.squathIntensity') )

                    connectAttr1( (vis_grp + '.fkCtrlVis'),rootGrpCFK_m,'shapeVis',1 )
                    connectAttr1( (vis_grp + '.ikCtrlVis'),rootGrpCIK_m,'shapeVis',0 )

                    try :
                        connectAttr1( (vis_grp + '.localCtrlVis'),rootGrp2,'shapeVis',0 )
                    except:
                        pass
                    try :
                        cmds.connectAttr( (rootGrpCFK_m[0] + '.scale'),(spineJointStr['GlobalScale0'] + '.input2') )
                    except :
                        pass
                
            hairShapes = cmds.listRelatives( DynSys['HG'][0] )
            follicleShapes = cmds.listRelatives( DynSys['FG'][1] )
			#########################
			# 创建动力学控制
            dl_grp = cmds.group(em=True)
            cmds.delete(cmds.pointConstraint( rootGrpCFK_m[1],dl_grp ))
            cmds.setAttr( dl_grp + '.tx',controlSize*1.2 )
            replaceShape( dl_grp,'Dyn',controlSize*.5,0,15 )# ;addTestCurves( dl_grp,controlSize*.4,'Dyn',-3.0 )
            cmds.parentConstraint( rootGrpCFK_m[1],dl_grp ,mo=True,w=1)
            attr = "dynamicVis"
            if cmds.objExists( vis_grp ):
                if cmds.attributeQuery( attr,exists=True,node=vis_grp ):
                    cmds.connectAttr( (vis_grp+'.'+attr),(dl_grp+'.v') )
            
            ################################### 添加动力学属性
            #addAttributeAndConnect1( rootGrpCFK_m[0],follicleShapes[0] )
            #addAttributeAndConnect2( rootGrpCFK_m[0],hairShapes[0] )
            
            addAttributeAndConnect1( dl_grp,follicleShapes[0] )
            addAttributeAndConnect2( dl_grp,hairShapes[0] )
            
            PointOnCurveTmp = createPointOnCurveTmp( DynSys['OG'][1] )
            # cmds.connectAttr( (rootGrpCFK_m[0] + '.attractionScale_Position'),(PointOnCurveTmp[0] + '.parameter') )
            cmds.connectAttr( (dl_grp + '.attractionScale_Position'),(PointOnCurveTmp[0] + '.parameter') )
            userAttributes( [ PointOnCurveTmp[1] ],['inheritsTransform'],0 )
            userAttributes( [ PointOnCurveTmp[1] ],['template'],1 )

		##############
		# 添加接口group，用于连接其他控制器
		# 如：一个胸腔位置的一个空组，用于连接 脖子，肩部等
		# 
        
        if port :
        	portEnd = cmds.group(em=True)
        	RConsEnd = cmds.parentConstraint( rootGrpCIK_down[-1],portEnd,st=['x','y','z'],w=1)
        	PConsEnd = cmds.parentConstraint( rootRollIKJnts[-1],rootGrpCIK_down[-1],portEnd,sr=['x','y','z'],w=1)
        	cmds.connectAttr( (rootGrpCFK_m[-1]+'.s'),(portEnd+'.s') )
			# cmds.connectAttr( (rootGrpCFK_m+'.s'),(portEnd+'.s') )
        	# cmds.scaleConstraint( rootRollIKJnts[-1],portEnd,w=1)
        	portStart = cmds.group(em=True)
        	cmds.parentConstraint( rootGrpCIK_down[0],portStart,st=['x','y','z'],w=1)
        	cmds.parentConstraint( rootRollIKJnts[0],portStart,sr=['x','y','z'],w=1)
        	cmds.scaleConstraint( rootRollIKJnts[0],portStart,w=1)
        	#
        	# << Monday, December 31, 2012 -- Start 
        	PConEndW0 = PConsEnd[0]+'.'+rootRollIKJnts[-1]+"W0"
        	PConEndW1 = PConsEnd[0]+'.'+rootGrpCIK_down[-1]+"W1";print(PConEndW1)
        	controlsAttr = (rootGrpCFK_m[0] + '.stretch')
        	reverserNode = cmds.createNode('reverse')
        	cmds.connectAttr( controlsAttr,PConEndW1 )
        	cmds.connectAttr( PConEndW1,(reverserNode+'.inputX') )
        	cmds.connectAttr( (reverserNode+'.outputX'), PConEndW0 )

			## Monday, December 31, 2012 --End  >>

        if setParentOutliner and setParentControls and createDynamicsCurve :
            globalGroup = cmds.group(em=True,name=(bName + 'grp'))
            cmds.parent( (rootJoints[0]),(rootRollIKJnts[0]),(rootGrpCFK_down[0]) )
            cmds.parent( (rootGrpC1s[0]),(DynSys['HG'][0]),(DynSys['FG'][0]),(DynSys['OG'][0]),ikHSystem[0],PointOnCurveTmp[1]
				,dl_grp,vis_grp,portStart,portEnd
				,globalGroup )
            userAttributes( [ ikHSystem[0], DynSys['HG'][0],DynSys['OG'][1],DynSys['FG'][2],DynSys['FG'][1] ],['inheritsTransform','v'],0 )
            userAttributes( [ rootJoints[0],rootRollIKJnts[0] ],['v'],0 )
            if setParentDeform :
                cmds.parent( skinGroup,(rootGrpCFK_down[0]) )

        if channelsAttrs and createControls :
            transform  = ['tx','ty','tz','rx','ry','rz','sx','sy','sz','v']
            channelsAttr(rootGrpCIK_down,['rx','ry','rz'],'hideLock')			
            channelsAttr( [dl_grp,vis_grp],transform,'hideLock')    

        cmds.setAttr( (dl_grp +".pointLock"),1 )
        cmds.setAttr( (dl_grp +".simulationMethod"),1 )
        # print("xxx")  channelControls(['pCube1','pCube2'],['v','tx','ty'],['lock=True','keyable=False'])
        channelControls( rootGrpCFK_m,['sx','sy','sz','v'],['lock=True','keyable=False'])
        channelControls( rootGrpCFK_down,['tx','ty','tz','sx','sy','sz','v'],['lock=True','keyable=False'])
        channelControls( rootGrpCIK_m,['rx','ry','rz','sx','sy','sz','v'],['lock=True','keyable=False'])

        returnOutput1 = ( rootJoints,rootGrpCtrlCVs,ikHSystem,PointOnCurveTmp )# rootRollIKJnts rootGrpC1s
		#channelControls
        if rename_1 :
            cRename.renameTuple( returnOutput1,(bName) )
            cRename.renameList( rootSkins,(bName + 'Skin') )
            cRename.renameList( rootRollIKJnts,(bName + 'RollIK') )
            cRename.renameList( rootGrp1,(bName + 'G1') )
            cRename.renameList( rootGrp2,(bName + 'G2') )
            cRename.renameList( rootGrpC1s,(bName + 'Offset') )
            cRename.renameList( rootGrpCFK_up,(bName + 'FKUp') )
            cRename.renameList( rootGrpCFK_m,(bName + 'FK') )
            cRename.renameList( rootGrpCFK_down,(bName + 'FKDown') )

            cRename.renameList( rootGrpCIK_up,(bName + 'IKUp') )
            cRename.renameList( rootGrpCIK_m,(bName + 'IK') )
            cRename.renameList( rootGrpCIK_down,(bName + 'IKDown') )
            cRename.renameDict( DynSys,(bName + '') )
            cRename.renameDict1( spineJointStr,(bName + '') )
            cRename.renameDict1( spineJointSqu,(bName + '') )
            cmds.rename( dl_grp ,(bName + 'DynamicControl'))
            cmds.rename( vis_grp ,(bName + 'ControlVis'))
            if port :
            	cmds.rename(portEnd,bName+'PortEnd')
            	cmds.rename(portStart,bName+'PortStart')
        # print("ok")
		# print("xx")
		# cmds.setAttr( (dl_grp +".pointLock"),1 )
		# cmds.setAttr( (dl_grp +".simulationMethod"),3 )
		cmds.select(cl=True);print(" Done! ")
    return( linkPMD )

