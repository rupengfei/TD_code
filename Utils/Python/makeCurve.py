# -*- coding: utf-8 -*-

import maya.cmds as cmds
import math

def wsValueByTwoPoint( posStartObj,posEndObj,spans = 3):
	# 
	# if len(objs) > 1 :
	#	pass 
	# posStartObj = objs[0]
	# posEndObj = objs[1]
	# 
	# spans = span - 1
	# 
	grp = {}
	grp['Start'] = cmds.createNode('transform')
	grp['End'] = cmds.createNode('transform')
	cmds.delete( cmds.pointConstraint( posStartObj,grp['Start'] ))
	cmds.delete( cmds.pointConstraint( posEndObj,grp['End'] ))
	cmds.delete( cmds.aimConstraint( posEndObj,grp['Start'] ))
	cmds.delete( cmds.orientConstraint( grp['Start'],grp['End'] )) 
	cmds.parent( grp['End'],grp['Start'] )
	allDist = cmds.getAttr( grp['End'] + ".tx" )
	singleDist = allDist / ( spans -1)
	curveStr = []
	for i in range( spans ):
		temp = cmds.createNode('transform')
		cmds.delete( cmds.parentConstraint( grp['Start'],temp ) )
		cmds.parent( temp,grp['Start'] )
		cmds.setAttr( (temp + ".tx") ,(singleDist * i) )
		tPos = cmds.xform( temp,q=True,ws=True,t=True )
		curveStr.append(tPos)

	cmds.delete( grp['Start'] )
	return( curveStr )

def MCurve ( objs,spans = 3):
	makeIt = ""
	lens = len( objs )
	wsValueByTwoPoint1 = []
	if lens == 2 :
		posStartObj = objs[0]
		posEndObj = objs[1]
		wsValueByTwoPoint1 = wsValueByTwoPoint( posStartObj,posEndObj,spans )
		curveCommand = "cmds.curve(degree = 2,p = (%s))" % wsValueByTwoPoint1
		makeIt = eval( curveCommand )
	if lens > 2:
		#
		for i in range( lens ) :
			tPos = cmds.xform( objs[i],q=True,ws=True,t=True )
			wsValueByTwoPoint1.append( tPos )

		curveCommand = "cmds.curve(degree = 2,p = (%s))" % wsValueByTwoPoint1
		makeIt = eval( curveCommand )
	
	return( makeIt )

# objs = ['locator1', 'locator2', 'locator3', 'locator4', 'locator5', 'locator6'] 
# objs = cmds.ls(sl=True)
# curves = MCurve ( objs,10)
# print(curves)


'''

listObjs = cmds.ls(sl=True,fl=True)

tPos = [0,0,0]
curveCommand = "cmds.curve(degree = 1,p = (%s))" % tPos
curveBase = eval( curveCommand )
for c in range( len(listObjs) - 1 ) :
	
	cmds.select( listObjs[c] )
	mm.eval("PolySelectConvert(3)")
	listObjss = cmds.ls(sl=True,fl=True)
	
	for i in range( len( listObjss )):
		tPos = cmds.xform( listObjss[i],q=True,ws=True,t=True )
		cmds.curve( curveBase,append=True,p= tPos )
		cmds.refresh()
		
		cmds.select(cl=True)

cmds.delete(curveBase + ".cv[0]")

	

	
	# curveTest = cmds.curve(degree = 1,p = )



'''


####################################################################################

'''
����������ڴ���curve��ָ��������
	�������ͣ�
	1.ָ�������ռ�����λ�������м䴴��һ������
	���趨���ߵ������

#===============================================================================


### Thursday, December 20, 2012
### 2:58:54 PM

���� :

1 . fkʱ�����������ƶ�����ת�����Ź��� ������״̬���пɿصļ�ѹ����Ч����fk״̬����ik���ƹ��� 
	
	--------------

	1.1 . ���ƵĲ㼶 

		|_ offsetName
			|_ UpExtraName
				|_ controlName --
					|_ DownExtraName
						|_ JointsName
	
	1.2 . ���ŵĿ��� , �������Ƿ�̳и���������
		(ÿ�����������пɿص����ŷ�Χ)

	1.3 . ikHandle ��������ת���� == joint orient  * -1 (��������ת��������ת)

	1.4 . 


�ɲο��Ĺ��� ��

	TSM���ܲο� :
		1 . fk����ik
		2 . ��ת���Ƽ����� 
			_1.�ɼ���λ�ƵĿ���
			_2.�ɼ����������� ���������첲����˶� ��

	ADV ���ܲο� :
		1 . fk���� ״̬�� �ƶ�����ת������ 

		* ���� ��� TSM|ADV �˹���

���� ��

1 . �������ɷ�ʽ �����ݶ�λ�������������¹���
	���ɶ����Ĺ����㣨�ǹ�����״̬��
	
	1.1 ���� deformation ������ ������Ƥ ��

	1.2 ���� rigging ϵͳ
		1.2.1 FKϵͳ
			****
		1.2.2 IKϵͳ
			****
		1.2.3 ��ģ��Ľ�ϣ����������������ϣ�
			
			1.2.3.1  �������ز����粿��� ��spine��chest��shoulder ��
			1.2.3.2  �粿���첲�Ľ�� 
				�粿�����첲�ķ�ʽ �� 
						_1. λ�� 
						_2. ��ת
			
	1.3 rigging connection deformation




2 . ������� �� ���������ӣ�spine��neck���� �ز����粿��chest��shoulder�� ; �첲���ȣ�arm��leg�� �� ͷ��head�� ���֣�hand�� ���ţ�foot��

	2.1  ����\����\��֫�μ����� �� > spineIK  �� pointOnCurve 


���� ��

1. fk״̬�µĹؽ��Ƿ��з��������ת ������ ���첲��Ĳ�λ��
2. ������תʱ�Ĺ�����ת (���� ���ֱۡ��粿��ת������ʱ�Ĺ�����ת���� )


'''