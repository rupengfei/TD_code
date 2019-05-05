#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Thursday, December 27, 2012
# shiftAttr

import maya.cmds as cmds

def shiftAttr( newControl = 'spineFK1_crv',oldControl = 'Upper_Body',connectIt = 1,delAttr = 1,hideTR=1 ) :
	# ��ѯԭ������������ ��������Ե��¿�����
	# ��ͬʱ����ԭ�������Ե��¿�����
	# ɾ��ԭ����û�õ�����
	# 
	listUserDefined = cmds.listAttr( oldControl ,userDefined=True )
	listKeyable = cmds.listAttr( oldControl ,k=True )
	evalString = ''
	# if len(listUserDefined):
	for uds in listUserDefined :
		# �������
		if not cmds.attributeQuery( uds,exists=True,node=newControl ) :
			oldAttrLongName = (oldControl+'.'+uds)
			evalString = "cmds.addAttr(" + "'" + newControl + "'" + ",ln="
			evalString += "'" + uds + "'" 
		
			if cmds.attributeQuery( uds,node = oldControl,enum=True ) :
				listEnum = cmds.attributeQuery( uds,node = oldControl,listEnum=True )
				evalString += ",at=" + "'enum'"
				evalString += ",en=" + "'" + listEnum[0] + ":'"
				## print('enum :'+uds,listEnum[0],'\n')
			else:
				# oldAttrLongName = (oldControl+'.'+uds)
				if type( cmds.getAttr(oldAttrLongName) ) is int:
					evalString += ",at=" + "'long'"
				if type( cmds.getAttr(oldAttrLongName) ) is float:
					evalString += ",at=" + "'double'"
				if type( cmds.getAttr(oldAttrLongName) ) is bool:
					evalString += ",at=" + "'bool'"
				if type( cmds.getAttr(oldAttrLongName) ) is list:
					# ʸ�����͵�����
					evalString += ",at=" + "'double3'"
					evalString += ");"
					evalString += "cmds.addAttr(" + "'" + newControl + "'" + ",ln=" + "'" + uds + "X'" 
					evalString += ",at=" + "'double'" + ",p=" + "'" + uds + "'"
					evalString += ");"
					evalString += "cmds.addAttr(" + "'" + newControl + "'" + ",ln=" + "'" + uds + "Y'" 
					evalString += ",at=" + "'double'" + ",p=" + "'" + uds + "'"
					evalString += ");"
					evalString += "cmds.addAttr(" + "'" + newControl + "'" + ",ln=" + "'" + uds + "Z'" 
					evalString += ",at=" + "'double'" + ",p=" + "'" + uds + "'"
					evalString += ");"
					evalString += "cmds.setAttr(" + "'" + newControl + "." + uds + "X'," + "e=True,keyable=True"
					evalString += ");"
					evalString += "cmds.setAttr(" + "'" + newControl + "." + uds + "Y'," + "e=True,keyable=True"
					evalString += ");"
					evalString += "cmds.setAttr(" + "'" + newControl + "." + uds + "Z'," + "e=True,keyable=True"
					#evalString += ");"
				# evalString += ",at=" + "'double'"

				if cmds.attributeQuery( uds,node = oldControl,minExists=True ) : # and type( cmds.getAttr(oldAttrLongName) ) is int and type( cmds.getAttr(oldAttrLongName) ) is float 
					mins = cmds.attributeQuery( uds,node = oldControl,min=True )
					evalString += ",min=" + str(mins[0])
					
				if cmds.attributeQuery( uds,node = oldControl,maxExists=True ) : # and type( cmds.getAttr(oldAttrLongName) ) is int and type( cmds.getAttr(oldAttrLongName) ) is float :
					maxs = cmds.attributeQuery( uds,node = oldControl,max=True )
					evalString += ",max=" + str(maxs[0])
					
				# dvs = cmds.getAttr( (oldControl+'.'+uds) )
				# evalString += ",dv=" + str(dvs)
			evalString += ")"
			# ## print('float :',uds,mins[0],maxs[0],dvs )
			## print(evalString)
			exec(evalString)
			# dvs = cmds.getAttr( (oldControl+'.'+uds) )
			# if type( dvs ) is float:
			# 	cmds.setAttr( (newControl+'.'+uds),dvs )
			#
			# �趨������ʾ ----
			# if type( cmds.getAttr(oldAttrLongName) ) is not list:
			if uds in listKeyable :
				cmds.setAttr( (newControl+'.'+uds),e=True,keyable=True )
			#cmds.setAttr( (newControl+'.'+uds),e=True,keyable=True )
		#
		# ��ԭĬ��ֵ
		if cmds.attributeQuery( uds,exists=True,node=oldControl ) :
			dvs = cmds.getAttr( (oldControl+'.'+uds) )
			if type( dvs ) is float:
				cmds.setAttr( (newControl+'.'+uds),dvs )
		##########################################################

		# �������� 
		if connectIt :
			#
			# ���� �Զ������Ե�
			if cmds.attributeQuery( uds,exists=True,node=oldControl ) :
				##
				# ��ѯold�������ӣ�����������������
				if cmds.connectionInfo( (oldControl+'.'+uds),isSource =True ) :
					destinations = cmds.connectionInfo( (oldControl+'.'+uds),destinationFromSource =True )
					for destination in destinations :
						cmds.disconnectAttr( (oldControl+'.'+uds),(destination) )
						cmds.connectAttr( (newControl+'.'+uds),(destination) )
						## print(destination,'\n')
				#
				# ��ѯold�������ӣ�������
				if cmds.connectionInfo( (oldControl+'.'+uds),isDestination =True ) :
					sources = cmds.connectionInfo( (oldControl+'.'+uds),sourceFromDestination =True )
					cmds.disconnectAttr( sources,(oldControl+'.'+uds) )
					cmds.connectAttr( sources,(newControl+'.'+uds) )
			'''
			# ��ѯ��������scale ������
			sysds = ['scale','rotateOrder']
			for sysd in sysds :
				if cmds.connectionInfo( (oldControl+'.'+sysd),isSource =True ) :
					destinations = cmds.connectionInfo( (oldControl+'.'+sysd),destinationFromSource =True )
					for destination in destinations :
						cmds.disconnectAttr( (oldControl+'.'+sysd),(destination) )
						cmds.connectAttr( (newControl+'.'+sysd),(destination) )
			'''
		# ɾ������
		# delAttr = 1
		# if delAttr :
		#	if cmds.attributeQuery( uds,exists=True,node=oldControl ) :
		#		cmds.deleteAttr( oldControl,attribute = uds )
	#listUserDefined = cmds.listAttr( oldControl ,userDefined=True )
	#listKeyable = cmds.listAttr( oldControl ,k=True )
	#evalString = ''
	#
	# ���� new ��������û��ʹ�õ�ͨ��������
	# ɾ�� old �������Զ������� ���س���roate ���������
	for uds in listUserDefined :
		# newList = cmds.listAttr( newControl,k=True)
		newList = ['visibility', 'translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ', 'scaleX', 'scaleY', 'scaleZ']
		oldList = cmds.listAttr( oldControl,k=True)
		[ newList.remove(x) for x in oldList if x in newList ]
		hidden = newList
		for hi in hidden:
			cmds.setAttr( (newControl+'.'+hi),keyable=False,lock=True,channelBox=False )
			## print(hi + '\n��������_____________OKKKKKKKKKKKKK_____\n')
		#pass
		# ɾ������
		if delAttr :
			if cmds.attributeQuery( uds,exists=True,node=oldControl ) :
				cmds.deleteAttr( oldControl,attribute = uds )
				## print(oldControl + '\nɾ������_____________OKKKKKKKKKKKKK_____\n')

	# �������õ�����
	if hideTR :
		roates = ['rotateX', 'rotateY', 'rotateZ']
		listKeyAbles = cmds.listAttr( oldControl,k=True )
		[listKeyAbles.remove(x) for x in roates if x in  listKeyAbles]
		for lists in listKeyAbles :
			# pass 
			cmds.setAttr( (oldControl+'.'+lists),keyable=False,lock=True,channelBox=False )
			# ## print( (oldControl+'.'+lists) +'\n������������_____________OKKKKKKKKKKKKK_____\n' )

	# ��ѯ��������scale ������
	sysds = ['scale','rotateOrder','rotate']
	for sysd in sysds :
		if cmds.connectionInfo( (oldControl+'.'+sysd),isSource =True ) :
			destinations = cmds.connectionInfo( (oldControl+'.'+sysd),destinationFromSource =True )
			for destination in destinations :
				cmds.disconnectAttr( (oldControl+'.'+sysd),(destination) )
				cmds.connectAttr( (newControl+'.'+sysd),(destination) )


# shiftAttr()
# shiftAttr( newControl = 'pCube3',oldControl = 'RightArm_Upper_Arm',delAttr = 1 )

def setParents( object ) :
	# ���group ############
	# �����������²㼶����һ������
	getParents = ''
	up = 'Up'
	down = 'Down'
	tmp = 'Tmp'
	# object = 'LeftArm_Lower_Arm'
	getParents = cmds.listRelatives( object,p=True)
	parentObj = getParents[0]
	groupsUp = cmds.group( em=True,n=object+up)
	groupsTmp = cmds.group( em =True,n=object+tmp)
	cmds.parent( groupsTmp,groupsUp )
	cmds.delete(cmds.parentConstraint( object,groupsUp))
	
	if type(getParents) is list :
		cmds.parent( groupsUp,parentObj )
		cmds.setAttr( (groupsUp+'.s'),1,1,1 )
		cmds.parent( object,groupsTmp )
	
	return( groupsUp,groupsTmp )

def replaceShape( sour ):
	tang = ''
	getParents = cmds.listRelatives( sour,p=True)
	tang = getParents[0]
	newShapeGrp = cmds.duplicate( sour,renameChildren=True )
	newShape = newShapeGrp[0]
	
	getShapes = cmds.listRelatives( newShape )
	shapes= getShapes[0]
	cmds.parent( shapes,tang,add=True,shape=True )
	oldGetShapes = cmds.listRelatives( sour )
	oldShapes= oldGetShapes[0]
	#
	# ���ӿ���������������
	# �õ�������transform��visibility���� ,������
	if cmds.connectionInfo( (sour+'.v'),isDestination  =True ) :
	# if cmds.connectionInfo( (sour+'.v'),isSource  =True ) :
		sources = cmds.connectionInfo( (sour+'.v'),sourceFromDestination =True )
		#destinations = cmds.connectionInfo( (sour+'.v'),destinationFromSource =True )
		#for destination in destinations :
		cmds.disconnectAttr( (sources),(sour+'.v') )
		if cmds.getAttr((tang+'.v'),lock=True):
			cmds.setAttr( (tang+'.v'),lock=False )
		cmds.connectAttr( (sources),(tang+'.v') )
		cmds.setAttr( (sour+'.v'),1 )
		cmds.setAttr( (tang+'.v'),keyable=False,channelBox=False )
	#
	# �õ�old������shape ��visibility���� ,�����ӵ�new��������shape ��visibility����
	if cmds.connectionInfo( (oldShapes+'.v'),isDestination  =True ) :
		sources = cmds.connectionInfo( (oldShapes+'.v'),sourceFromDestination =True )
		cmds.disconnectAttr( (sources),(oldShapes+'.v') )
		cmds.connectAttr( (sources),(shapes+'.v') )

	# ����ԭshape or delete 
	cmds.setAttr( (oldShapes+'.v'),0  )
	cmds.delete( newShape )
	# cmds.delete( oldShapes )

#############################################

def tsmClassModify ():
	
	try:
		cmds.setAttr("LeftLeg_Heel_Pivot.translateX",l=False)
		cmds.setAttr("LeftLeg_Heel_Pivot.translateY",l=False)
		cmds.setAttr("LeftLeg_Heel_Pivot.translateZ",l=False)
	except :
		pass

	#tsmAlls = ['LeftArm_Shoulder', 'LeftArm_Upper_Arm', 'LeftArm_Lower_Arm', 'LeftArm_HandTranslate', 'LeftArm_Hand', 'LeftArm_Arm_IK', 'LeftArm_Arm_Pole_Vector', 'LeftFinger1_finger_control', 'LeftFinger1_finger_IK', 'LeftFinger2_finger_control', 'LeftFinger2_finger_IK', 'LeftFinger3_finger_control', 'LeftFinger3_finger_IK', 'LeftFinger4_finger_control', 'LeftFinger4_finger_IK', 'LeftLeg_Upper_Leg', 'LeftLeg_Lower_Leg', 'LeftLeg_Foot', 'LeftLeg_Toe', 'LeftLeg_Leg_Pole_Vector', 'LeftLeg_Standard_Pole_Vector', 'LeftLeg_IK_Leg', 'LeftLeg_Toe_Pivot', 'LeftLeg_Heel_Pivot', 'LeftThumb_finger_control', 'LeftThumb_finger_IK', 'RightArm_Shoulder', 'RightArm_Upper_Arm', 'RightArm_Lower_Arm', 'RightArm_HandTranslate', 'RightArm_Hand', 'RightArm_Arm_IK', 'RightArm_Arm_Pole_Vector', 'RightFinger1_finger_control', 'RightFinger1_finger_IK', 'RightFinger2_finger_control', 'RightFinger2_finger_IK', 'RightFinger3_finger_control', 'RightFinger3_finger_IK', 'RightFinger4_finger_control', 'RightFinger4_finger_IK', 'RightLeg_Upper_Leg', 'RightLeg_Lower_Leg', 'RightLeg_FootTranslate', 'RightLeg_Foot', 'RightLeg_Toe', 'RightLeg_Leg_Pole_Vector', 'RightLeg_Standard_Pole_Vector', 'RightLeg_IK_Leg', 'RightLeg_Toe_Pivot', 'RightLeg_Heel_Pivot', 'RightThumb_finger_control', 'RightThumb_finger_IK']
	tsmAlls = [ 'LeftArm_Upper_Arm', 'LeftArm_Lower_Arm', 'LeftArm_HandTranslate', 'LeftArm_Hand', 'LeftArm_Arm_IK', 'LeftArm_Arm_Pole_Vector',   'LeftLeg_Upper_Leg', 'LeftLeg_Lower_Leg', 'LeftLeg_Foot', 'LeftLeg_Toe', 'LeftLeg_Leg_Pole_Vector', 'LeftLeg_Standard_Pole_Vector', 'LeftLeg_IK_Leg', 'LeftLeg_Toe_Pivot', 'LeftLeg_Heel_Pivot',  'RightArm_Upper_Arm', 'RightArm_Lower_Arm', 'RightArm_HandTranslate', 'RightArm_Hand', 'RightArm_Arm_IK', 'RightArm_Arm_Pole_Vector',  'RightLeg_Upper_Leg', 'RightLeg_Lower_Leg', 'RightLeg_FootTranslate', 'RightLeg_Foot', 'RightLeg_Toe', 'RightLeg_Leg_Pole_Vector', 'RightLeg_Standard_Pole_Vector', 'RightLeg_IK_Leg', 'RightLeg_Toe_Pivot', 'RightLeg_Heel_Pivot']

	for tsm in tsmAlls :
		if cmds.nodeType(tsm) == 'transform' :
			lAttrs = cmds.listAttr(tsm,k=True)
			## print(lAttrs,"\n<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
			if 'rotateX' in lAttrs and 'rotateY' in lAttrs and 'rotateZ' in lAttrs :
				grps = setParents( tsm )
				## print(tsm+'\n �趨group_____________OK\n')
				shiftAttr( grps[1],tsm,1 )
				## print(tsm+'\n ת������_____________OK\n')
				replaceShape( tsm )
				## print(tsm+'\n �滻shape___________OK\n')
				#
				cmds.rename( tsm,tsm+'Down' )
				cmds.rename( grps[1],tsm )

# tsmClassModify()