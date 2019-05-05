#!/usr/bin/env python
# -*- coding: utf-8 -*-
# name : tsmModify
# Thursday, December 27, 2012
# 
# 功能 ：
# 生成新的身体： 脊柱，脖子，头
# 链接tsm原始属性，到新的身体上
# 控制器层级，上下各添加一个空组
# 上下只保留rotate属性，其他属性是隐藏状态
# 
# 现在的问题:
# Monday, December 31, 2012 12:35:52 PM
# 1 .肩部控制器的上下层无效，原因 tsm是直接属性链接不能继承上下层的transform信息
# 2 ........... 
#

import maya.cmds as cmds
from CRT.Python.cRebuildTool import *

def reFKJoint( name ='',startPos='',endPos='',upPos='') :
	#
	# 用于生产胸部和头部的骨骼等 ，主要fk效果
	jntList = []
	cmds.select(cl=True)
	startJnt = cmds.joint(n=name+'Start')
	cmds.delete( cmds.pointConstraint( startPos,startJnt ) )
	cmds.delete( cmds.aimConstraint( endPos,startJnt,worldUpObject = upPos,worldUpType='object',aimVector=(1,0,0),upVector=(0,1,0) ) )
	cmds.select( startJnt )
	cmds.makeIdentity(apply=True,t=1,r=1,s=1,n=0)
	endJnt = cmds.joint(n=name+'End')
	cmds.delete( cmds.pointConstraint( endPos,endJnt ) )
	jntList = [startJnt,endJnt]
	return( jntList )

def reSpine( name = ['spine','neck'],nameToe = ['chest','head'],bJntNum = [6,4],bCtrlNum = [3,2],controlSize = [4.0,2.5] ):
	import CRT.Python.makeCurve as mc
	if cmds.objExists('Spine_JOINTS') :
		bUpLoc = cmds.createNode('transform')
		cmds.delete( cmds.parentConstraint('Spine_JOINTS',bUpLoc) )
		cmds.parent( bUpLoc,'Spine_JOINTS')
		cmds.setAttr( "%s.tz" % (bUpLoc),10)
		cmds.parent( bUpLoc,w=True )
	# 定义定位骨骼 
	# 根据原始脊柱位置创建
	#

	objs = [['Spine_joint2', 'Spine_joint4', 'Spine_joint6',  'Spine_joint7']
			,['Head_joint1','Head_joint2','Head_joint3']
			] # 'Spine_joint8',
	objToe = [['Spine_joint7','Spine_joint8']
			,['Head_joint3','Head_joint4']
			]

	for i in range( 2 ) :
		curves = mc.MCurve ( objs[i],1)
		BaseCurve =  str(curves)
		#
		import CRT.Python.makeSpine as ms
		groups = ms.makeSpine( BaseCurve,bUpLoc,bJntNum[i],bCtrlNum[i],name[i],controlSize[i] )
		# print(groups)
		
		# if cmds.objExists("%sgrp" % (name[i])):
			#cmds.setAttr( '%sFK1_crv.fkCtrlVis' % (name[i]), 1 )
			#cmds.setAttr( '%sFK1_crv.ikCtrlVis' % (name[i]), 1 )
			#cmds.setAttr( '%sFK1_crv.stretch' % (name[i]), 1 )
			#cmds.setAttr( '%sDynamicControl.pointLock' % (name[i]), 1 )
			#cmds.setAttr( '%sDynamicControl.simulationMethod' % (name[i]), 1 )
			#print("xx")
		fkJnt = reFKJoint( nameToe[i],objToe[i][0],objToe[i][1],bUpLoc )
		# 链接缩放
		#
		# 隐藏End ik controls
		# spineIKUp3_grp
		endIKCtlName = name[i] + "IKUp" + str( bCtrlNum[i] + 1 ) + "_grp"
		endJntName = name[i] + "RollIK" + str( bJntNum[i] + 1 ) + "_jnt"
		try:
			cmds.setAttr( (endIKCtlName + ".v"),0,lock=True )
			# fkJnt[0]
			cmds.connectAttr( (endJntName+'.sy'),(fkJnt[0]+'.sy') )
			cmds.connectAttr( (endJntName+'.sz'),(fkJnt[0]+'.sz') )
			cmds.connectAttr( (fkJnt[0]+'.sz'),(fkJnt[0]+'.sx') )

		except :
			pass

	cmds.delete( bUpLoc )

def headGlobalOrientConstraint( controls = 'neckFK3_crv',headStart = 'neckOffset3_grp',bodyGlobal = 'spineFK1_crv' ) :
	# 创建头部旋转控制 ：是否跟随身体旋转的控制
	# 
	if cmds.objExists( controls ) and cmds.objExists( headStart ) and cmds.objExists( bodyGlobal ) :
		getParents = cmds.listRelatives( headStart,parent=True )
		parents = getParents[0]
		grp1 = cmds.group(em=True,n=(bodyGlobal+'Rot') )
		grp2 = cmds.group(em=True,n=(headStart+'Rot') )
		cmds.delete( cmds.parentConstraint(bodyGlobal,grp1) )
		cmds.delete( cmds.orientConstraint(headStart,grp1) )
		cmds.delete( cmds.parentConstraint(headStart,grp2) )
		cmds.parent( grp1,bodyGlobal )
		cmds.parent( grp2,parents )
		orienConstraint = cmds.orientConstraint( grp1,grp2,headStart )
		cmds.addAttr( controls,ln='global',at='double',min=0,max=1,dv=0)
		cmds.setAttr( (controls+'.global'),e=True,keyable=True )
		cmds.connectAttr( (controls+'.global'),(orienConstraint[0]+'.'+grp1+'W0') )
		rev = cmds.createNode( 'reverse' )
		cmds.connectAttr( (orienConstraint[0]+'.'+grp1+'W0'),(rev+'.inputX') )
		cmds.connectAttr( (rev+'.outputX'),(orienConstraint[0]+'.'+grp2+'W1') )
	else :
		pass

def rebuildClass() :
	# 将原来的链接历史（腿部，胳膊） 链接到行的绑定物体
	# 定义新的跟骨骼 
	# 腰部、胯部
	newRoot = 'spineSkin1_jnt'
	oldRoot = 'Spine_joint1'
	ctlRoot = 'spineFKDown1_grp'
	# 
	# 胸部 胳膊
	newToe = 'chestStart'
	oldToe = 'Spine_joint7'
	# 
	# 需要p到新骨骼的物体，腿部
	# cmds.ls(sl=True)
	
	rootChilen = ['Spine_influence1_compensate', 'RightLeg_scalingCompensate', 'RightLeg_constraintCompensate', 'LeftLeg_scalingCompensate', 'LeftLeg_constraintCompensate'] 
	for child in rootChilen :
		cmds.parent( child,newRoot )
	# 
	# 定义 连接腿部缩放的MD node
	lenScaleMD = ['RightLeg__multiplyDivide','LeftLeg__multiplyDivide']
	for md in lenScaleMD :
		cmds.disconnectAttr( (oldRoot+'.scale'),(md+'.input2') )
		cmds.connectAttr( (newRoot+'.scale'),(md+'.input2') )
	# 
	# 定义p到新骨骼的物体， 胳膊 部分
	# 
	toeChilen = ['Spine_influence7_compensate', 'LeftArm_scalingCompensate', 'LeftArm_constraintCompensate', 'RightArm_scalingCompensate', 'RightArm_constraintCompensate']
	for child in toeChilen :
		cmds.parent( child,newToe )
	armScaleMD = ['LeftArm__multiplyDivide','RightArm__multiplyDivide']
	for md in armScaleMD :
		cmds.disconnectAttr( (oldToe+'.scale'),(md+'.input2') )
		cmds.connectAttr( (newToe+'.scale'),(md+'.input2') )
	#
	# 用于控制四肢旋转的空组
	# 
	rotateIsolate = ['LeftArm_rotationisolate', 'RightArm_rotationisolate', 'Head_rotationisolate', 'RightLeg_rotationisolate', 'LeftLeg_rotationisolate']
	for r in rotateIsolate :
		cmds.parent(r,ctlRoot)

def lockAndHideAttr1( listSs,start=0,stop=10) :
	listAttrs = ['tx','ty','tz','rx','ry','rz','sx','sy','sz','v']
	for c  in range( len(listSs) ) :
		for i in range( start,stop,1 ) :
			cmds.setAttr( (listSs[c]+'.'+listAttrs[i]),lock=True,keyable=False )

def madeLocalScale( pmaNodes = cmds.ls('spineScale*_pma'),ctlNodes = cmds.ls('spineIK*_crv') ) :
	#
	# 链接局部控制器对骨骼的缩放的缩放控制
	pmaLen = len( pmaNodes )
	ctlLen = len( ctlNodes )
	valueMax = 1.0
	attrName_ctl = 'fatYZ'
	
	for i in range( ctlLen ) :
		grpNode = cmds.group(em=True,name=ctlNodes[i]+'CON')
		cmds.parent( grpNode,ctlNodes[i] )
		# cmds.addAttr( ctlNodes[i],ln="curves",at='double' )
		cmds.addAttr( grpNode,ln="curves",at='double' )
		# cmds.connectAttr( (grpNode + '.curves'),(ctlNodes[i] + '.curves') )
		ctlAttr = (grpNode + '.curves')
		# print(ctlAttr)
		if i==0 :
			cmds.setKeyframe( ctlAttr,t=0,v=valueMax )
			cmds.setKeyframe( ctlAttr,t=pmaLen-1,v=0 )
		elif i == (ctlLen-1) :
			cmds.setKeyframe( ctlAttr,t=0,v=0 )
			cmds.setKeyframe( ctlAttr,t=pmaLen-1,v=valueMax )
		else :
			cmds.setKeyframe( ctlAttr,t=0,v=0 )
			cmds.setKeyframe( ctlAttr,t=float(pmaLen+1)/float(ctlLen)*i,v=valueMax )
			cmds.setKeyframe( ctlAttr,t=pmaLen-1,v=0 )
	
		cmds.addAttr( ctlNodes[i],ln=attrName_ctl,at='double',min=-.8,max=5 )
		cmds.addAttr( grpNode,ln=attrName_ctl,at='double',min=-.8,max=5 )
		cmds.connectAttr( (ctlNodes[i] + '.'+attrName_ctl),(grpNode + '.'+attrName_ctl) )

		attrNameLong = (grpNode+'.'+attrName_ctl)
		cmds.setAttr( (ctlNodes[i] + '.'+attrName_ctl),e=True,keyable=True )
		
		for c in range( pmaLen ) :
			nodesFC = cmds.createNode( 'frameCache' )
			cmds.setAttr( (nodesFC+'.varyTime'),c )
			cmds.connectAttr( (ctlAttr),(nodesFC+'.stream') )
			nodesMD = cmds.createNode( 'multiplyDivide' )
			cmds.connectAttr( (attrNameLong),(nodesMD+'.input1X') )
			cmds.connectAttr( (nodesFC+'.varying'),(nodesMD+'.input2X') )
			cmds.connectAttr( (nodesMD+'.outputX'),(pmaNodes[c]+'.input3D['+ str(i+1) +'].input3D'+'y') )
			cmds.connectAttr( (nodesMD+'.outputX'),(pmaNodes[c]+'.input3D['+ str(i+1) +'].input3D'+'z') )

def connectNode( obj = 'spineFK3_crv' ) :
	attr = 'fatYZ'
	objs = obj + '.' + attr
	pmaNode = ''
	if cmds.connectionInfo( objs,isSource =True ) :
		destinations = cmds.connectionInfo( objs,destinationFromSource =True )
		for destination in destinations :
			if cmds.getAttr( (obj+'.sx'),lock=True) :
				cmds.setAttr( (obj+'.sx'),lock=False)
			if not cmds.getAttr( (obj+'.sx'), keyable=True ):
				cmds.setAttr( (obj+'.sx'), keyable=True )
			
			pmaNode = cmds.createNode('plusMinusAverage',name=obj+'PMA')
			cmds.connectAttr( objs,(pmaNode+'.'+'input1D[0]') )
			cmds.connectAttr( (obj+'.sx'),(pmaNode+'.'+'input1D[1]') )
			cmds.setAttr( (pmaNode+'.'+'input1D[2]'),-1 )
			cmds.disconnectAttr( objs,(destination) )
			cmds.connectAttr( (pmaNode+'.'+'output1D'),(destination) )

		if cmds.getAttr( (obj+'.sy'),lock=True) :
			cmds.setAttr( (obj+'.sy'),lock=False)
		if cmds.getAttr( (obj+'.sz'),lock=True) :
			cmds.setAttr( (obj+'.sz'),lock=False)
		cmds.connectAttr( (obj+'.sx'),(obj+'.sy'))
		cmds.connectAttr( (obj+'.sx'),(obj+'.sz'))
		cmds.setAttr( (obj+'.sy'),lock=True,keyable=False )
		cmds.setAttr( (obj+'.sz'),lock=True,keyable=False )
	return(pmaNode)


def main ( jNumSpine = 6,jNumNeck=2,cNumSpine=2,cNumNeck=1,cSize=3.0 ):
	# reSpine()
	# bCtrlNum == >控制器的数量 可设定为 2 or 3
	reSpine( name = ['spine','neck'],nameToe = ['chest','head'],bJntNum = [jNumSpine,jNumNeck],bCtrlNum = [cNumSpine,cNumNeck],controlSize = [ cSize,cSize/1.5]  )
	spine = 'spine'
	neck = 'neck'
	chestStart = 'chestStart'
	headStart = 'headStart'

	parentObj = 'Character'

	# plus1 = 1
	if cmds.objExists( spine+'PortEnd' ) :
		# 脊柱控制脖子 
		if cmds.objExists( neck+'PortEnd' ):
			# cmds.parentConstraint( rootGrpCIK_down[-1],portEnd,st=['x','y','z'],w=1)
			if cmds.objExists("chestEnd"):
				cmds.parentConstraint( (spine+'PortEnd'),(neck+'Offset1_grp'),st=['x','y','z'],mo=True,w=1 )
				cmds.parentConstraint( ('chestEnd'),(neck+'Offset1_grp'),sr=['x','y','z'],mo=True,w=1 )
				cmds.scaleConstraint( (spine+'PortEnd'),(neck+'Offset1_grp'),mo=True,w=1 )

			if cmds.objExists( headStart ):
				# 修复轴向 
				# 将头部控制器的轴向对齐到头部骨骼的轴向
				try :
					grpTop = 'neckOffset3_grp'
					aimObj = 'headStart'
					neckLoc25 = 'neck25_loc'
					neckLoc24 = 'neck24_loc'
					oldParent = 'neckIKDown3_grp'
					cmds.parent(neckLoc25,neckLoc24,w=True)
					cmds.delete(cmds.orientConstraint(aimObj,grpTop))
					cmds.parent(neckLoc25,neckLoc24,oldParent)		
				except :
					pass
				# 脖子控制头部骨骼
				cmds.parent( headStart,(neck+'PortEnd') )

		if cmds.objExists( chestStart ):
			cmds.parent( chestStart,(spine+'PortEnd') )
	
	# 链接四肢原来的链接到新的身体上 
	rebuildClass()
	import CRT.Python.shiftAttr as sa
	if cmds.objExists( "spineControlVis" ):
		sa.shiftAttr( newControl = 'spineControlVis',oldControl = 'Upper_Body',connectIt = 1,delAttr = 1) # spineFK1_crv
	sa.tsmClassModify()
	#
	# 删除原控制
	delOldControl = 1
	if delOldControl :
		cmds.setAttr( 'Upper_Body.v',0 )
		cmds.delete('Upper_Body','Head_IK')
		cmds.parent( (spine+'grp'),(neck+'grp'),parentObj)
		
	# sa.tsmClassModify()
	# 
	# 链接脊柱、脖子，和大环的缩放关系
	# 整体缩放控制
	# 
	try:
		spineMD = "spineGlobalScale1_md.input2"
		neck1MD = "neckGlobalScale1_md.input2"
		neck2MD = "neckGlobalScale2_md.input2"
		cmds.connectAttr( (parentObj+".scale"),( spineMD ) )
		cmds.connectAttr( (parentObj+".scale"),( neck1MD ) )
		cmds.connectAttr( ('spinePortEnd'+".scale"),( neck2MD ) )
		# 
		# 
	except :
		pass
		# print("\n\n\nEORROR ...身体。脖子的整体缩放没有链接成功\n\n")
	# spine
	madeLocalScale(pmaNodes = cmds.ls('spineScale*_pma'),ctlNodes = cmds.ls('spineFK*_crv')) ;
	# print('局部缩放添加成功')
	# neck 
	madeLocalScale( pmaNodes = cmds.ls('neckScale*_pma'),ctlNodes = cmds.ls('neckFK*_crv') )
	# lockAndHideAttr1() ;print( '属性锁定隐藏成功' )
	#
	# 只留 translation rotate
	#listSs = cmds.ls("spineIK1_crv",'spineFK*_crv','neckFK1_crv','neckFK2_crv','*FKDown*_grp','chestStart')
	#lockAndHideAttr1( listSs,6,10)
	listSs = cmds.ls('headStart')
	lockAndHideAttr1( listSs,6,9)
	#
	# 只留 translation
	#listSs = cmds.ls("spineIK2_crv","spineIK3_crv","spineIK4_crv",'neckIK2_crv')
	#lockAndHideAttr1( listSs,3,10) 
	# 只留 rotate
	listSs = cmds.ls('*FKDown*_grp')
	lockAndHideAttr1( listSs,0,3)
	# 不需要的控制器  隐藏
	# listSs = cmds.ls("neckIK1_crv")
	# for ss in listSs : cmds.setAttr( (ss+'.v'),0,lock=True  )

	#  显示chest的scale属性
	spineCtls = cmds.ls("spineFK*_crv")
	axes = ['x','y','z']
	for ax in axes:
		cmds.setAttr(spineCtls[-1]+'.s'+ax,keyable=True,lock=False)
		# cmds.setAttr(spineCtls[-1]+'.s'+ax,lock=True)
	#
	# 链接胸腔的整体缩放
	# connectNode()

	maxValue = 10
	objs_spine = ['spineFK5_crv','spineFK4_crv','spineFK3_crv','spineFK2_crv']
	for obj in objs_spine :
		if cmds.objExists( obj ):
			connectNode( obj )
			break

	objs_neck = ['neckFK5_crv','neckFK4_crv','neckFK3_crv','neckFK2_crv']
	for obj in objs_neck :
		if cmds.objExists( obj ):
			connectNode( obj )
			break
	# posName = ["spine","neck"]
	neckFK = "neckFK"
	for i in range( maxValue ) :
		value = str(maxValue  - i)
		if cmds.objExists( neckFK + value + "_crv"  ) and cmds.objExists( "spineFK1_crv"  ) :
			headGlobalOrientConstraint( (neckFK + value + "_crv"),("neckOffset" + value + "_grp"),"spineFK1_crv" )
			if not cmds.objExists( "Head"):
				cmds.rename( (neckFK + value + "_crv"),"Head" )
				'''
				listControl = cmds.ls( neckFK + "*" +value+ "*",type="transform" )
				for ctl in listControl :
					ctlDf = ctl.split( neckFK )
					print(ctlDf[1])
					ctlSp = ctlDf[1].split(value+"_")
					cmds.rename( ctl,("head"+ctlSp[0])+'_'+ctlSp[1] )
				'''
			if value == "2":
				nodeName = "neckControlVis"
				if cmds.objExists( nodeName ):
					bugAttr = ["fkCtrlVis","ikCtrlVis"]
					for attr in bugAttr:
						if cmds.attributeQuery( attr,exists=True,node=nodeName ):
							cmds.deleteAttr( nodeName,attribute = attr )

			break
		#continue
		#if cmds.objExists( "neckG1" + value + "_grp"  ):
		#	cmds.setAttr( ("neckG1" + value + "_grp" + ".v"),0,lock=True )
		#	continue
		#continue
		#if cmds.objExists( "spineG1" + value + "_grp"  ):
		#	cmds.setAttr( ("spineG1" + value + "_grp" + ".v"),0,lock=True )
		#	break

	for i in range( maxValue ) :
		value = str(maxValue  - i)
		if cmds.objExists( "neckG1" + value + "_grp"  ):
			cmds.setAttr( ("neckG1" + value + "_grp" + ".v"),0,lock=True )
			break
	
	for i in range( maxValue ) :
		value = str(maxValue  - i)
		if cmds.objExists( "spineG1" + value + "_grp"  ):
			cmds.setAttr( ("spineG1" + value + "_grp" + ".v"),0,lock=True )
			break

	#if cmds.objExists( "chestEnd" ):
	#	cmds.setAttr( ("chestEnd" + ".v"),0,lock=True )
	listArmMD = cmds.ls('LeftArm__multiplyDivide','RightArm__multiplyDivide')
	for md in listArmMD: cmds.setAttr( (md+'.operation'),0)

	# 控制器显示调整
	# 删除不用的属性
	nodeName = "spineControlVis"
	if cmds.objExists( nodeName ):
		bugAttr = ["Display","Head_FKIK","Head_Isolation","Spine_FKIK"]
		for attr in bugAttr:
			if cmds.attributeQuery( attr,exists=True,node=nodeName ):
				cmds.deleteAttr( nodeName,attribute = attr )
		# 腰 大环改名
		if not cmds.objExists(  "Upper_Body"  ):
			cmds.rename( nodeName,"Upper_Body")
		
	#
	# 调整骨骼半径大小
	other = 1
	if other :
		radius = 30.0
		skinJnts = cmds.ls("spineSkin*_jnt","neckSkin*_jnt","headStart","chestStart")
		for skin in skinJnts :
			cmds.setAttr( skin+".radius",radius )
		#
		#隐藏不要的属性
		otherList = ["neckG21_crv"]
		Shape = []
		for ot in otherList:
			if cmds.objExists( ot ):
				gShape = cmds.listRelatives( ot,s=True)
				for g in gShape:
					cmds.setAttr( (g + ".lodVisibility"),0,lock=True )

		listBug = cmds.ls('spine*_loc','neck*_loc','chestEnd','neckIK1_crv')
		Shape += listBug
		#for g in Shape:
		channelControls( Shape,['v'],['lock=False','0','lock=True'])

		if cmds.objExists("Character"):
			grp = cmds.group(em=True,name="Character"+'Down')
			cmds.delete( cmds.parentConstraint( 'Character',grp ) )
			gChild = cmds.listRelatives("Character",type='transform')
			cmds.parent( grp,"Character" )
			for g in gChild :cmds.parent( g,grp )
			listSs = [grp]
			lockAndHideAttr1( listSs,6,10) 
		
	# 设定动力学控制器的默认值
	DynamicControl = cmds.ls("*DynamicControl")
	for ctl in DynamicControl :
		cmds.setAttr( ctl+ ".pointLock",1)
		cmds.setAttr( ctl+ ".simulationMethod",1)

	cmds.select(cl=True)
	print(" tsm modify finish ! ")

# main()
#
#

