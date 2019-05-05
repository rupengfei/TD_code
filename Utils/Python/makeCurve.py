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
这个命令用于创建curve到指定的物体
	方法类型：
	1.指定两个空间坐标位置在其中间创建一条曲线
	可设定曲线点的数量

#===============================================================================


### Thursday, December 20, 2012
### 2:58:54 PM

功能 :

1 . fk时各控制器有移动、旋转、缩放功能 ，缩放状态下有可控的挤压拉伸效果，fk状态下有ik控制功能 
	
	--------------

	1.1 . 控制的层级 

		|_ offsetName
			|_ UpExtraName
				|_ controlName --
					|_ DownExtraName
						|_ JointsName
	
	1.2 . 缩放的控制 , 子物体是否继承父物体缩放
		(每个控制器都有可控的缩放范围)

	1.3 . ikHandle 极向量翻转控制 == joint orient  * -1 (极向量翻转骨骼不翻转)

	1.4 . 


可参考的功能 ：

	TSM功能参考 :
		1 . fk带动ik
		2 . 旋转控制极向量 
			_1.可加入位移的控制
			_2.可加轴向锁定（ 例：锁定胳膊肘的运动 ）

	ADV 功能参考 :
		1 . fk控制 状态下 移动、旋转、缩放 

		* 考虑 结合 TSM|ADV 此功能

方法 ：

1 . 骨骼生成方式 ，根据定位骨骼重新生成新骨骼
	生成独立的骨骼点（非骨骼链状态）
	
	1.1 创建 deformation 骨骼（ 用于蒙皮 ）

	1.2 创建 rigging 系统
		1.2.1 FK系统
			****
		1.2.2 IK系统
			****
		1.2.3 各模块的结合（整个身体的整理，结合）
			
			1.2.3.1  腰部、胸部、肩部结合 （spine、chest、shoulder ）
			1.2.3.2  肩部、胳膊的结合 
				肩部带动胳膊的方式 ： 
						_1. 位移 
						_2. 旋转
			
	1.3 rigging connection deformation




2 . 具体分类 ： 脊柱，脖子（spine，neck）； 胸部，肩部（chest，shoulder） ; 胳膊，腿（arm，leg） ； 头（head） ；手（hand） ；脚（foot）

	2.1  脊柱\脖子\四肢次级控制 — > spineIK  、 pointOnCurve 


问题 ：

1. fk状态下的关节是否有反方向的旋转 （例如 ：胳膊肘的部位）
2. 极限旋转时的骨骼翻转 (例如 ：手臂、肩部旋转到极限时的骨骼翻转问题 )


'''