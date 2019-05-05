#!/usr/bin/env python
# -*- coding: utf-8 -*-
# name : cRebuildTool
#
# 这个文件的命令是创建rigging元素类的工具
# 例如：创建一些单独的spineIK、拉伸等 ，主要是细节效果的实现
#


import maya.cmds as cmds
import maya.mel as mm
import CRT.Python.cAddAttr as cAddAttr
import CRT.Python.rename as cRename

def curvesDynamics( bCurve ) :
    ''' hairGroup = HG , follicleGroup = FG , outputCurveGroup = OG  
    '''
    DySys ={}
    cmds.select( bCurve )
    mm.eval("makeCurvesDynamicHairs 1 0 1")
    DySys['HG'] = cmds.pickWalk(direction = 'up')
    DySys['FG'] = cmds.ls( (DySys['HG'][0] + 'Follicles'),dagObjects=True,type='transform')
    DySys['OG'] = cmds.ls( (DySys['HG'][0] + 'OutputCurves'),dagObjects=True,type='transform')
    cmds.select(cl=True)
    return(DySys)
        
def spineIKH( rootJoint,bCurve ) :
    lenSpine = len(rootJoint)
    startJoint = rootJoint[0]
    endJoint = rootJoint[lenSpine -1]
    ikHTemp = cmds.ikHandle(startJoint=startJoint,endEffector=endJoint,curve= bCurve,sol='ikSplineSolver',ccv=False,pcv=False)
    cmds.makeIdentity(startJoint,apply=True,t=True,r=True,s=True,n=False)
    cmds.delete(ikHTemp)
    ikHSystem = cmds.ikHandle(startJoint=startJoint,endEffector=endJoint,curve=bCurve,sol='ikSplineSolver',ccv=False,pcv=False)
    return(ikHSystem)

def ikhTwistControlEnable(ikh,toeObj,endObj) :
	cmds.setAttr( ikh + ".dTwistControlEnable",1 )
	cmds.setAttr( ikh + ".dWorldUpType",4 )
	cmds.connectAttr( (toeObj+".worldMatrix[0]"),(ikh+".dWorldUpMatrix") )
	cmds.connectAttr( (endObj+".worldMatrix[0]"),(ikh+".dWorldUpMatrixEnd") )

def spineJoint_str( rootJoint,bCurve ) :
    ''' this script user make spine joint stretch '''
    # ikHandle1 = ikHSystem[0]
    # cmds.setAttr( (ikHandle1 + '.dTwistControlEnable') , 1)
    # cmds.setAttr( (ikHandle1 + '.dWorldUpType') , 4)
    # cmds.connectAttr( (newFKPosJntList[0] + '.worldMatrix[0]'),( ikHandle1 + '.dWorldUpMatrix') )
    # cmds.connectAttr( (newFKPosJntList[bSpans] + '.worldMatrix[0]'),( ikHandle1 + '.dWorldUpMatrixEnd') )
    nodes ={}
    lenSpine = len(rootJoint)
    startJoint = rootJoint[0]
    endJoint = rootJoint[lenSpine -1]
    nodes['CInfoNode'] = cmds.arclen( bCurve , ch=True)
    nodes['Start'] = cmds.createNode( 'multiplyDivide' )
    nodes['onOff'] = cmds.createNode( 'blendColors' )
    curveLength = cmds.getAttr( nodes['CInfoNode']+ '.arcLength' )
    cmds.setAttr( nodes['Start'] + '.operation' , 2 )
    cmds.setAttr( nodes['Start'] + '.input2X' , curveLength)
    cmds.setAttr( nodes['onOff'] + '.color2R' , 1)
    cmds.connectAttr( (nodes['CInfoNode'] + '.arcLength'),( nodes['Start'] + '.input1X') )
    mdnum = 3
    for c in range( mdnum ) :
        nodes['GlobalScale' + str(c) ] = cmds.createNode( 'multiplyDivide' )
        cmds.setAttr( nodes['GlobalScale' + str(c) ] + '.operation' ,2 )
        if c == 0 :
            cmds.connectAttr( (nodes['Start'] + '.outputX'),( nodes['GlobalScale' + str(c) ] + '.input1X') )
        if mdnum > c > 0 :
            cmds.connectAttr( ( nodes['GlobalScale' + str( c - 1 ) ] + '.outputX'),( nodes['GlobalScale' + str(c) ] + '.input1X') )
        if c == mdnum - 1 :
            cmds.connectAttr( (nodes['GlobalScale' + str(c) ] + '.outputX'),(nodes['onOff'] + '.color1R') )
    for i in range( 1 , ( lenSpine ) ) :
        jntTranslateX = cmds.getAttr( rootJoint[i] + '.tx' )
        nodes['Stretch' + str(i)] = cmds.createNode( 'multiplyDivide')
        cmds.setAttr( nodes['Stretch' + str(i) ] + '.input2X' , jntTranslateX)
        cmds.connectAttr( ( nodes['onOff'] + '.outputR'),( nodes['Stretch' + str(i)] + '.input1X') )
        cmds.connectAttr( ( nodes['Stretch' + str(i) ] + '.outputX'),( rootJoint[i] + '.tx') )
    return(nodes)

def spineJoint_squash( listJnts ):
    nodes ={}
    clen = len( listJnts )
    cmds.addAttr(listJnts[0],ln = 'curves',at='double')
    cmds.setKeyframe( (listJnts[0] + '.curves'),t=1,v=0 )
    cmds.setKeyframe( (listJnts[0] + '.curves'),t=(clen+1)/2.0,v=.5 )
    cmds.setKeyframe( (listJnts[0] + '.curves'),t=clen,v=0 )
    squathIntensity = 'squathIntensity'

    for i in range( 1,clen ) :
    	cmds.addAttr( listJnts[i-1],ln= squathIntensity,at='double',min=0,max=1,dv=0 )
    	cmds.setAttr( (listJnts[i-1]+'.'+squathIntensity),e=True,keyable=True )
        tx = cmds.getAttr( listJnts[i] + ".tx" )
        nodes[ 'SquashMD' + str(i) ] = cmds.createNode( 'multiplyDivide' )
        nodes[ 'SquashDI' + str(i) ] = cmds.createNode( 'multiplyDivide' )
        nodes[ 'SquashPO' + str(i) ] = cmds.createNode( 'multiplyDivide' )
        nodes[ 'SquashIn' + str(i) ] = cmds.createNode( 'blendTwoAttr' )	# squathIntensity
        nodes[ 'SquashFR' + str(i) ] = cmds.createNode( 'frameCache' )
        cmds.setAttr( (nodes[ 'SquashFR' + str(i) ] + ".varyTime") , i)
        cmds.connectAttr( (listJnts[0] + '.curves'),( nodes[ 'SquashFR' + str(i) ] + ".stream") )
        cmds.setAttr( nodes['SquashMD' + str(i) ] + '.operation' ,2 )
        cmds.setAttr( nodes['SquashMD' + str(i)] + '.input2X' ,tx )
        cmds.setAttr( nodes['SquashDI' + str(i) ] + '.operation' ,2 )
        cmds.setAttr( nodes['SquashDI' + str(i)] + '.input1X' ,1 )
        cmds.setAttr( nodes['SquashPO' + str(i) ] + '.operation' ,3 )
        
        cmds.connectAttr( (listJnts[i] + ".tx"),(nodes['SquashMD' + str(i) ] + '.input1X') )
        cmds.connectAttr( (nodes['SquashMD' + str(i) ] + '.outputX'),(nodes['SquashDI' + str(i) ] + '.input2X') )
        
        cmds.connectAttr( (nodes['SquashDI' + str(i) ] + '.outputX'),(nodes['SquashPO' + str(i) ] + '.input1X') )
        cmds.connectAttr( ( nodes[ 'SquashFR' + str(i) ] + ".varying"),(nodes['SquashPO' + str(i) ] + '.input2X') )
        
        cmds.setAttr( (nodes[ 'SquashIn' + str(i) ] + ".input[0]"),1 )
        cmds.connectAttr( (nodes['SquashPO' + str(i) ] + '.outputX'),(nodes[ 'SquashIn' + str(i) ] + ".input[1]") )
		#cmds.setAttr( (nodes[ 'SquashIn' + str(i) ] + ".input[0]"),1 )
        cmds.connectAttr( (listJnts[i-1] + '.' + squathIntensity),(nodes[ 'SquashIn' + str(i) ] + ".attributesBlender") )
        
        cmds.connectAttr( (nodes[ 'SquashIn' + str(i) ] + '.output'),(listJnts[i-1] + ".sy") )
        cmds.connectAttr( (nodes[ 'SquashIn' + str(i) ] + '.output'),(listJnts[i-1] + ".sz") )
    return(nodes)

# print('xxxx')	

def ctrlGroup( object,type,bCurve,bUpLoc,bCtrlNum_s,level ) :
    '''
    ctrlGroup( object,type,curve,upObject ) -> 
    ctrlGroup( 'group','cv','curve1','locator1',5,'True') -> 
    ctrlGroup( 'locator','cv','curve15754','locator1',1,'' )
    '''
    newGrpList = []
    cmds.select(cl=True)
    bCtrlNum = 0
    if type == 'ep' :
        bCtrlNum = bCtrlNum_s + 1
    if type == 'cv' :
        bCtrlNum = bCtrlNum_s + 3
    for i in range( bCtrlNum ) :
        cmds.refresh
        pos_t = cmds.xform( (bCurve + '.' + type + '[' + str(i) + ']' ),q=True,ws=True,t=True)
        newGrp = nullObj( object )
        cmds.xform(newGrp,ws=True,t = (pos_t[0],pos_t[1],pos_t[2]) )
        newGrpList.append(newGrp)
        if i > 0 :
            cmds.delete(cmds.aimConstraint(newGrpList[i],newGrpList[i-1],worldUpObject = bUpLoc ,weight=1,worldUpType = 'object'))
            if i == bCtrlNum -1 :
                cmds.delete(cmds.orientConstraint(newGrpList[i-1],newGrpList[i]))
            if level == 'True' :
                cmds.parent(newGrpList[i],newGrpList[i-1])
                if object == 'joint' :
                    cmds.makeIdentity(newGrpList[0],apply=True,t=True,r=True,s=True,n=False)
    return(newGrpList)

def ctrlGroupMake( object,listJnts,ctrlNum,level ) :
    ''' ctrlGroupMake('locator',listJnts,2,'') 
    listJnts = cmds.ls(sl=True)
    len
    2%2
    13%2
    23/3
    9/2
    '''
    clen = len(listJnts)
    steps = clen/ctrlNum
    groups = ''
    groupsList = []
    
    if steps == clen :
        for i in range(2):
            groups = nullObj( object )
            cmds.delete( cmds.parentConstraint(listJnts[i],groups) )
            groupsList.append( groups )
            if i == 1 :
                cmds.delete( cmds.parentConstraint(listJnts[-1],groupsList[-1]) )        
    else :     
        for i in range( 0,clen,steps ) :       
            groups = nullObj( object )
            cmds.delete( cmds.parentConstraint(listJnts[i],groups) )
            groupsList.append( groups )
            if i == (clen -steps) :
                cmds.delete( cmds.parentConstraint(listJnts[-1],groupsList[-1]) )
                
        if level == 'True' :
            for i in range( len(groupsList) ) :
                if i > 0:
                    cmds.parent( groupsList[i],groupsList[i-1])
    return(groupsList)

def nullObj( type ) :
	object = ''
	cmds.select(cl=True)
	if type == 'group' :
		object = cmds.group(em=True)
	if type == 'locator' :
		objects = cmds.spaceLocator( p = (0,0,0))
		object = objects[0]
	if type == 'joint' :
		object = cmds.joint( p = (0,0,0))
	return(object)

def replaceShape_xx(object,type,size) :
	'''controlShape('RLleft_toe1','box',1) '''
	controls = ''
	if type == 'circle' :
		controls = cmds.circle(nr=[1,0,0],d=3,r=size)
	if type == 'box' :
		controls = cmds.curve(d=1,p=([size,size,size],[-size,size,size],[-size,size,-size],[size,size,-size],[size,size,size],[size,-size,size],[size,-size,-size],[size,size,-size],[-size,size,-size],[-size,-size,-size],[size,-size,-size],[size,-size,size],[-size,-size,size],[-size,-size,-size],[-size,size,-size],[-size,size,size],[-size,-size,size],[size,-size,size],[size,size,size]))
	bCurveShapeList = cmds.listRelatives( controls ,s=True,path=True )
	Shape = bCurveShapeList[0]
	cmds.parent( Shape,object,add=True,shape=True )
	cmds.delete(controls)

def replaceShapes( objGrp,tanObj,col=17 ) :
	cmds.makeIdentity( objGrp,apply=True,t=True,r=True,s=True,n=False )
	objShapeAll = cmds.listRelatives(objGrp,c=True,allDescendents=True)
	for shape in objShapeAll :
		if cmds.nodeType( shape ) == "nurbsCurve" :
			if col != 100:
				cmds.setAttr( shape+".overrideEnabled", 1)
				cmds.setAttr( shape+".overrideColor", col)
			cmds.parent( shape,tanObj,add=True,shape=True)

def replaceShape(object,type,size=1.0,offset=0.0,col=17  ) :
	'''controlShape('RLleft_toe1','box',1) '''
	controls = ""
	control = []
	if type == 'c_circle' :
		ctl = cmds.circle(nr=[1,0,0],d=3,r=size)
		controls = ctl[0]
		
	elif type == 'c_box' :
		ctl = cmds.curve(d=1,p=([size,size,size],[-size,size,size],[-size,size,-size],[size,size,-size],[size,size,size],[size,-size,size],[size,-size,-size],[size,size,-size],[-size,size,-size],[-size,-size,-size],[size,-size,-size],[size,-size,size],[-size,-size,size],[-size,-size,-size],[-size,size,-size],[-size,size,size],[-size,-size,size],[size,-size,size],[size,size,size]))
		controls = ctl
		# print(controls)
	else:
		ctl = addTestCurves(object,size,type,offset)
		controls = ctl
	replaceShapes( controls,object,col )
	cmds.delete(controls)

def addTestCurves(obj,size=1,names="Dynamics",offset=-6.0):
	textCurve=''
	if not cmds.objExists( obj+'Text' ):
		ss = size*0.2
		textCurve = cmds.textCurves(ch=False,f= "华文琥珀|w400|h-11",t =names,name = (obj+'Text') )
		cmds.setAttr( textCurve[0]+'.s',ss,ss,ss)
		cmds.delete( cmds.pointConstraint( obj,textCurve[0] ) )
		cmds.parent( textCurve[0],obj )
		#cmds.setAttr( textCurve[0]+'.tx',offset*ss)
		#cmds.setAttr( textCurve[0]+'.ty',offset*ss/(-3.0))
		cmds.toggle(textCurve[0],state=True,template=True)
	return(textCurve[0])

def channelsAttr(objects,attributes,type) :
    ''' user lock unlock hide show command,example :  '''
    for object in objects :
        for attribute in attributes :
            if type == 'hide' :
                cmds.setAttr( ( object + '.' + attribute),keyable=False,channelBox=False)
            if type == 'show' :
                cmds.setAttr( ( object + '.' + attribute),channelBox=True)
                cmds.setAttr( ( object + '.' + attribute),keyable=True)
            if type == 'hideLock' :
                cmds.setAttr( ( object + '.' + attribute),lock=True,keyable=False,channelBox=False)
            if type == 'showUnlock' :
                cmds.setAttr( ( object + '.' + attribute),lock=False,channelBox=True)
                cmds.setAttr( ( object + '.' + attribute), keyable = True)
            if type == 'shapeVisHide' :
                objectShapes = cmds.listRelatives(object,s=True,path=True)
                for shape in objectShapes :
                    cmds.setAttr( (shape + '.' + attribute),0)
            if type == 'shapeVisShow' :
                objectShapes = cmds.listRelatives(object,s=True,path=True)
                for shape in objectShapes :
                    cmds.setAttr( (shape + '.' + attribute),1)

def connectAttr1(objects,tangents,type,start) :
	if type == 'shapeVis' :
		for i in range( start,len(tangents)) :
			objectShapes = cmds.listRelatives( tangents[i],s=True,path=True)
			for shape in objectShapes :
				if cmds.nodeType(shape) == 'nurbsCurve':
					cmds.connectAttr( (objects),(shape + '.visibility'))

def addAttributeBase1( objects,tangent ) :
    attr = dynaimicsAttr2()
    for i in range( len( attr ) ) :
        cAddAttr.cAddAttr( objects,attr[i][0],attr[i][1],attr[i][2],attr[i][3] )
        # cmds.setAttr( (objects+"."+attr[i][0]),keyable=False,channelBox=True )
		# -keyable false
    if tangent != '' :
        cmds.connectAttr( (objects + '.' + attr[0][0] ),(tangent + '.blender') )

def addAttributeBase1_1( objects,tangent ) :
    attr = dynaimicsAttr2_1()
    for i in range( len( attr ) ) :
        cAddAttr.cAddAttr( objects,attr[i][0],attr[i][1],attr[i][2],attr[i][3] )
    if tangent != '' :
        cmds.connectAttr( (objects + '.' + attr[0][0] ),(tangent + '.blender') )
						
def addAttributeAndConnect1( objects,tangent ) :
    attr = dynaimicsAttr3()
    for i in range( len( attr ) ) :
        cAddAttr.cAddAttr( objects,attr[i][0],attr[i][1],attr[i][2],attr[i][3] )
    if tangent != '' :
        connectAttrCmd( objects,tangent,attr)
        
def dynaimicsAttr3():
    attr = [ ['pointLock','enum','NoAttach,Base,Tip,BothEnds',''] ]
    return( attr )
    
def dynaimicsAttr2_1():
    attr = [ ['stretch','double','0,1,1',''],['squathIntensity','double','0,1,1','']]
    return( attr )

def dynaimicsAttr2():
    attr = [ ['fkCtrlVis','long','0,1,1',''],['ikCtrlVis','long','0,1,1',''] ,['localCtrlVis','long','0,1,0',''],['dynamicVis','long','0,1,0','']]
    return( attr )
    
def dynaimicsAttr1():
    attr = [ ['simulationMethod','enum','Off,Static,DynamicFolliclesOnly,AllFollicles',''],['collide','double','0,1,1',''],['startFrame','long',',,1',''],['stiffness','double','0,1,.75',''],['drag','double',',,0.1',''],['motionDrag','double',',,0',''],['damp','double','0,1,0',''],['friction','double','0,,1',''],['mass','double','0,,5',''],['gravity','double',',,9.8',''],['dynamicsWeight','double','0,1,1',''],['startCurveAttract','double','0,1,.85',''],['attractionDamp','double','0,1,0',''],['attractionScale_Position','double','0,1,0','']]
    return attr
    
def addAttributeAndConnect2( objects,tangent ) :
    attr = dynaimicsAttr1()
    for i in range( len( attr ) ) :
        cAddAttr.cAddAttr( objects,attr[i][0],attr[i][1],attr[i][2],attr[i][3] )
    if tangent != '' :
        connectAttrCmd( objects,tangent,attr )        
    
def connectAttrCmd( objects,tangent,attributes ) :
    keyables = cmds.listAttr( tangent,k=True)
    for attrs in attributes :
        if len(attrs) > 0 :
            attr = attrs[0]
            if attr in keyables :
                cmds.connectAttr( ( objects + '.' + attr),( tangent + '.' + attr) )
            if attr == 'attractionScale_Position' :
                cmds.connectAttr( ( objects + '.' + attr),( tangent + '.attractionScale[0].' + attr) )

def createPointOnCurveTmp( bcurve ) :    
    infoNode = cmds.pointOnCurve( bcurve, ch=True, pr=0.55)
    cmds.setAttr( (infoNode + '.turnOnPercentage') ,1)
    bgroup = nullObj( 'locator' )
    cmds.connectAttr( (infoNode + '.position' ),(bgroup + '.translate') )
    tangentConstraints = cmds.tangentConstraint( bcurve,bgroup )
    return( infoNode,bgroup,tangentConstraints )

def userAttributes(objects,attributes,value):
    value = int(value)
    for i in range( len(objects) ) :
        for c in range( len(attributes) ) :
            if value == 0 :
                cmds.setAttr( (objects[i] + '.' + attributes[c]),lock= 0 )
                cmds.setAttr( (objects[i] + '.' + attributes[c]),0 )
                cmds.setAttr( (objects[i] + '.' + attributes[c]),lock= 1 )
            if value == 1 :
                cmds.setAttr( (objects[i] + '.' + attributes[c]),lock= 0 )
                cmds.setAttr( (objects[i] + '.' + attributes[c]),1 )
                cmds.setAttr( (objects[i] + '.' + attributes[c]),lock= 1 )
    
def linkToRollIKJnt( sourceJnt,tangentJnt ) :
    clen = len(sourceJnt)
    node = {}
    trsGrp = {'Translate':'t','Rotate':'r','Scale':'s'}
    xyzGrp = ['x','y','z']
    for i in range(clen) :
        ii = str( i+1 )
        for c in range( len(trsGrp) ) :
            node[ trsGrp.keys()[c] + ii ] = cmds.createNode( 'plusMinusAverage' )
            for xyz in xyzGrp :
                cmds.connectAttr( ( sourceJnt[i] + '.' + trsGrp.values()[c] + xyz),( node[ trsGrp.keys()[c] + ii ] + '.input3D[0].input3D' + xyz ) )
                cmds.connectAttr( ( node[ trsGrp.keys()[c] + ii ] + '.output3D' + xyz ) ,( tangentJnt[i] + '.' + trsGrp.values()[c] + xyz) )
    return(node)


def createRollIK( listJnts,groups,intensionYAttr,offsetYAttr,intensionZAttr,offsetZAttr ) :
    '''
    listJnts = cmds.ls(sl=True,dag=True,type='joint')
    intensionYAttr = 'intensionY'
    offsetYAttr = 'offsetY'
    intensionZAttr = 'intensionZ'
    offsetZAttr = 'offsetZ'
    groups = []
    
    '''
    jntSize = len(listJnts)
    node = {}
    attr = [ [intensionYAttr,'double','',''],[offsetYAttr,'double',',,1',''],[intensionZAttr,'double','',''],[offsetZAttr,'double',',,1',''] ]
    for i in range( len( attr ) ) :
        cAddAttr.cAddAttr( listJnts[0],attr[i][0],attr[i][1],attr[i][2],attr[i][3] )
    
    intensionYAttrAll = (listJnts[0] + '.' + intensionYAttr )
    offsetYAttrAll = (listJnts[0] + '.' + offsetYAttr )
    intensionZAttrAll = (listJnts[0] + '.' + intensionZAttr ) 
    offsetZAttrAll = (listJnts[0] + '.' + offsetZAttr )
    
    nodeName = ['nodeY_cd','nodeZ_cd']
    rgbGrp = ['R','G','B']
    
    for i in range( len(nodeName) ) :
        node[ nodeName[i] ]  = cmds.createNode('condition')
        cmds.setAttr( node[ nodeName[i] ] + '.operation',4 )
        for c in range( len(rgbGrp) ) :
            cmds.setAttr( (node[ nodeName[i] ] + '.colorIfTrue' + rgbGrp[c]),-1 )
            
    cmds.connectAttr( intensionYAttrAll,( node[ 'nodeY_cd' ] + '.firstTerm') )
    cmds.connectAttr( intensionZAttrAll,( node[ 'nodeZ_cd' ] + '.firstTerm') )
            
    for i in range( jntSize ) :
        ii = str(i + 1)
        node[ 'nodeY_rv' + ii ] = cmds.createNode('remapValue')
        node[ 'nodeZ_rv' + ii ] = cmds.createNode('remapValue')

        node[ 'node_md_Imin' + ii ] = cmds.createNode( 'multiplyDivide' )
        node[ 'node_md_Imax' + ii ] = cmds.createNode( 'multiplyDivide' )
        node[ 'node_md_Omin' + ii ] = cmds.createNode( 'multiplyDivide' )
        node[ 'node_md_Omax' + ii ] = cmds.createNode( 'multiplyDivide' )
        node[ 'node_md_size' + ii ] = cmds.createNode( 'multiplyDivide' )
    
        imin = jntSize - i - 1
        imax = jntSize - i
    
        cmds.setAttr( node[ 'node_md_Imin' + ii ] + '.input1Y',imin)
        cmds.setAttr( node[ 'node_md_Imax' + ii ] + '.input1Y',imax)
        cmds.setAttr( node[ 'node_md_Omin' + ii ] + '.input1Y',0)
        cmds.setAttr( node[ 'node_md_Omax' + ii ] + '.input1Y',(10 + 3.5 * i) )
        
        cmds.setAttr( node[ 'node_md_Imin' + ii ] + '.input1Z',imin)
        cmds.setAttr( node[ 'node_md_Imax' + ii ] + '.input1Z',imax)
        cmds.setAttr( node[ 'node_md_Omin' + ii ] + '.input1Z',0)
        cmds.setAttr( node[ 'node_md_Omax' + ii ] + '.input1Z',(10 + 3.5 * i) )
           
        cmds.connectAttr( intensionYAttrAll,( node[ 'nodeY_rv' + ii ] + '.inputValue') )
        cmds.connectAttr( intensionZAttrAll,( node[ 'nodeZ_rv' + ii ] + '.inputValue') )
        
        cmds.connectAttr( ( node[ 'nodeY_cd' ] + '.outColorG'),( node[ 'node_md_Imin' + ii ] + '.input2Y') )
        cmds.connectAttr( ( node[ 'nodeY_cd' ] + '.outColorG'),( node[ 'node_md_Imax' + ii ] + '.input2Y') )
        cmds.connectAttr( ( node[ 'nodeY_cd' ] + '.outColorG'),( node[ 'node_md_Omin' + ii ] + '.input2Y') )
        cmds.connectAttr( ( node[ 'nodeY_cd' ] + '.outColorG'),( node[ 'node_md_Omax' + ii ] + '.input2Y') )

        cmds.connectAttr( ( node[ 'nodeZ_cd' ] + '.outColorB'),( node[ 'node_md_Imin' + ii ] + '.input2Z') )
        cmds.connectAttr( ( node[ 'nodeZ_cd' ] + '.outColorB'),( node[ 'node_md_Imax' + ii ] + '.input2Z') )
        cmds.connectAttr( ( node[ 'nodeZ_cd' ] + '.outColorB'),( node[ 'node_md_Omin' + ii ] + '.input2Z') )
        cmds.connectAttr( ( node[ 'nodeZ_cd' ] + '.outColorB'),( node[ 'node_md_Omax' + ii ] + '.input2Z') )

        cmds.connectAttr( ( node[ 'node_md_Imin' + ii ] + '.outputY'),(node[ 'nodeY_rv' + ii ] + '.inputMin') )
        cmds.connectAttr( ( node[ 'node_md_Imax' + ii ] + '.outputY'),(node[ 'nodeY_rv' + ii ] + '.inputMax') )
        cmds.connectAttr( ( node[ 'node_md_Omin' + ii ] + '.outputY'),(node[ 'nodeY_rv' + ii ] + '.outputMin') )
        cmds.connectAttr( ( node[ 'node_md_Omax' + ii ] + '.outputY'),(node[ 'nodeY_rv' + ii ] + '.outputMax') )
        
        cmds.connectAttr( ( node[ 'node_md_Imin' + ii ] + '.outputZ'),(node[ 'nodeZ_rv' + ii ] + '.inputMin') )
        cmds.connectAttr( ( node[ 'node_md_Imax' + ii ] + '.outputZ'),(node[ 'nodeZ_rv' + ii ] + '.inputMax') )
        cmds.connectAttr( ( node[ 'node_md_Omin' + ii ] + '.outputZ'),(node[ 'nodeZ_rv' + ii ] + '.outputMin') )
        cmds.connectAttr( ( node[ 'node_md_Omax' + ii ] + '.outputZ'),(node[ 'nodeZ_rv' + ii ] + '.outputMax') )
    
        cmds.connectAttr( (node[ 'nodeY_rv' + ii ] + '.outColorG'),( node[ 'node_md_size' + ii ] + '.input1Y') )
        cmds.connectAttr( (node[ 'nodeZ_rv' + ii ] + '.outColorG'),( node[ 'node_md_size' + ii ] + '.input1Z') )
        
        cmds.connectAttr( offsetYAttrAll,( node[ 'node_md_size' + ii ] + '.input2Y') )
        cmds.connectAttr( offsetZAttrAll,( node[ 'node_md_size' + ii ] + '.input2Z') )
        
        try:
            cmds.connectAttr( ( node[ 'node_md_size' + ii ] + '.outputY'),( groups[ 'Rotate' + ii ] + '.input3D[1].input3Dy') )
            cmds.connectAttr( ( node[ 'node_md_size' + ii ] + '.outputZ'),( groups[ 'Rotate' + ii ] + '.input3D[1].input3Dz') )
        except:
            pass
    return( node )

def channelControls( objects=[],listAttrs = ['v'],controls=[] ) :
	command = ""
	for obj in objects:
		for attr in listAttrs:
			for ctl in controls:
				command +=("cmds.setAttr(('%s.%s'),%s)\n" % (obj,attr,ctl) )
                exec( command )

def getParentsCmd(transform) :
	parentsList = [transform]
	parentsAllList = []
	while 1:
		parentsList = cmds.listRelatives( parentsList[0],parent=True )
		if parentsList is None : break
		else:
			parentsAllList.append(parentsList[0])
	return( parentsAllList )