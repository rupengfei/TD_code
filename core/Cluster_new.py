# -*- coding:utf-8 -*-
import maya.cmds as cmds
import maya.mel as mm
import pymel.core as pm


class Win(object):
    wname = 'meshRepairUI'
    title = 'Final Cut'

    def show(self):
        try:
            pm.deleteUI(self.wname)
        except:
            pass

        width = 200
        high = 130
        pm.window(self.wname, title='Final Cut', toolbox=True, maximizeButton=False, sizeable=False)
        pm.columnLayout(adj=True)
        pm.rowColumnLayout(numberOfRows=1)
        pm.button(w=width / 1.5, h=high, label='Create', command=lambda *args: meshRepairCmd())
        pm.columnLayout(adj=True)
        pm.button(w=width / 3, h=high / 1.25, label='Paint', command=lambda *args: paintClusterWightCmd())
        pm.button(w=width / 3, h=high / 4.0, label='Delete', command=lambda *args: deleteControlCmd(), enable=True)
        pm.setParent('..')
        pm.setParent('..')
        pm.rowColumnLayout(numberOfRows=1)
        pm.rowColumnLayout(numberOfColumns=2)
        pm.button(w=width / 3, h=high / 4, label='|<', command=lambda *args: pm.mel.eval('playButtonStepBackward'))
        pm.button(w=width / 3, h=high / 4, label='>|', command=lambda *args: pm.mel.eval('playButtonStepForward'))
        pm.button(w=width / 3, h=high / 4, label='|<', bgc=[0.588, 0.268, 0.341],
                  command=lambda *args: self.keyAndBackward())
        pm.button(w=width / 3, h=high / 4, label='>|', bgc=[0.588, 0.268, 0.341],
                  command=lambda *args: self.keyAndForward())
        pm.setParent('..')
        pm.button(w=width / 3, h=high / 4, label='<Key>', bgc=[0.588, 0.268, 0.341],
                  command=lambda *args: setKeyFrameCmd(1, ''))
        pm.setParent('..')
        pm.rowColumnLayout(numberOfRows=1)
        pm.button(w=width / 3, h=high / 4, label='Update', command=lambda *args: resetPivotCmd_select())
        pm.button(w=width / 1.5, h=high / 4, label='Bake Pivot >>>', command=lambda *args: bakePivotCmd())
        pm.showWindow(self.wname)
        pm.window(self.wname, e=True, wh=[width + 5, high * 2])

    def keyAndBackward(self):
        setKeyFrameCmd(1, '-')
        pm.mel.eval('playButtonStepBackward')

    def keyAndForward(self):
        setKeyFrameCmd(1, '+')
        pm.mel.eval('playButtonStepForward')


# -----------------------------------------------------------------------------
def cAddAttr(object, longName, attributeType, napS, makeAttribute):
    """ zge ming ling yong yu kuai su  tian jia shu xing  """
    if not cmds.attributeQuery(longName, ex=True, node=object):
        nap = {}
        napList = napS.split(',')
        napLen = len(napList)
        keysx = ['min', 'max', 'dv']
        evalString = "cmds.addAttr('" + object + "'" + ',ln=' + "'" + longName + "'"
        evalString += ",at='" + attributeType + "'"
        if attributeType == 'enum':
            if napLen > 1:
                enumStr = ''
                for i in range(len(napList)):
                    enumStr += napList[i] + ':'

                evalString += ",en='" + enumStr + "'"
        elif napLen > 1:
            for c in range(min(napLen, len(keysx))):
                if napList[c] != '':
                    nap[keysx[c]] = napList[c]

            for i in range(len(nap)):
                evalString += ',' + nap.keys()[i] + '=' + str(nap.values()[i])

        evalString += ')'
        exec evalString
        if makeAttribute == 'd':
            pass
        else:
            cmds.setAttr(object + '.' + longName, e=True, keyable=True)


# -----------------------------------------------------------------------------
def renameDict1(objects, bName):
    for key in objects.keys():
        cRename(objects[key], bName + key)


def cRename(object, bName):
    suffix = ''
    if cmds.nodeType(object) == 'transform':
        shapes = cmds.listRelatives(object, s=True, path=True)
        shape = ''
        try:
            lenShape = len(shapes)
            shape = shapes[0]
        except:
            lenShape = 0

        if lenShape > 0:
            cnodeType = cmds.nodeType(shape)
            if cnodeType == 'nurbsCurve':
                suffix = 'crv'
            if cnodeType == 'locator':
                suffix = 'loc'
            if cnodeType == 'mesh':
                suffix = 'mesh'
            if cnodeType == 'nurbsSurface':
                suffix = 'nurbs'
            if cnodeType == 'hairSystem':
                suffix = 'hsys'
            if cnodeType == 'follicle':
                suffix = 'foll'
        else:
            suffix = 'grp'
    elif cmds.nodeType(object) == 'joint':
        suffix = 'jnt'
    elif cmds.nodeType(object) == 'ikHandle':
        suffix = 'ikh'
    elif cmds.nodeType(object) == 'ikEffector':
        suffix = 'ikEff'
    elif cmds.nodeType(object) == 'condition':
        suffix = 'cnd'
    else:
        suffix = findUpper(cmds.nodeType(object))
    cmds.rename(object, bName + '_' + suffix)


def findUpper(a):
    result = ''
    c = [list(a)[i] for i in range(len(list(a))) if list(a)[i].isupper()]
    result = list(a)[0].upper()
    for i in range(len(c)):
        result += c[i]
        result = result.lower()

    return result


# -----------------------------------------------------------------------------

def curvesDynamics(bCurve):
    """ hairGroup = HG , follicleGroup = FG , outputCurveGroup = OG
    """
    DySys = {}
    cmds.select(bCurve)
    mm.eval('makeCurvesDynamicHairs 1 0 1')
    DySys['HG'] = cmds.pickWalk(direction='up')
    DySys['FG'] = cmds.ls(DySys['HG'][0] + 'Follicles', dagObjects=True, type='transform')
    DySys['OG'] = cmds.ls(DySys['HG'][0] + 'OutputCurves', dagObjects=True, type='transform')
    cmds.select(cl=True)
    return DySys


def spineIKH(rootJoint, bCurve):
    lenSpine = len(rootJoint)
    startJoint = rootJoint[0]
    endJoint = rootJoint[lenSpine - 1]
    ikHTemp = cmds.ikHandle(startJoint=startJoint, endEffector=endJoint, curve=bCurve, sol='ikSplineSolver', ccv=False,
                            pcv=False)
    cmds.makeIdentity(startJoint, apply=True, t=True, r=True, s=True, n=False)
    cmds.delete(ikHTemp)
    ikHSystem = cmds.ikHandle(startJoint=startJoint, endEffector=endJoint, curve=bCurve, sol='ikSplineSolver',
                              ccv=False, pcv=False)
    return ikHSystem


def ikhTwistControlEnable(ikh, toeObj, endObj):
    cmds.setAttr(ikh + '.dTwistControlEnable', 1)
    cmds.setAttr(ikh + '.dWorldUpType', 4)
    cmds.connectAttr(toeObj + '.worldMatrix[0]', ikh + '.dWorldUpMatrix')
    cmds.connectAttr(endObj + '.worldMatrix[0]', ikh + '.dWorldUpMatrixEnd')


def spineJoint_str(rootJoint, bCurve):
    """ this script user make spine joint stretch """
    nodes = {}
    lenSpine = len(rootJoint)
    startJoint = rootJoint[0]
    endJoint = rootJoint[lenSpine - 1]
    nodes['CInfoNode'] = cmds.arclen(bCurve, ch=True)
    nodes['Start'] = cmds.createNode('multiplyDivide')
    nodes['onOff'] = cmds.createNode('blendColors')
    curveLength = cmds.getAttr(nodes['CInfoNode'] + '.arcLength')
    cmds.setAttr(nodes['Start'] + '.operation', 2)
    cmds.setAttr(nodes['Start'] + '.input2X', curveLength)
    cmds.setAttr(nodes['onOff'] + '.color2R', 1)
    cmds.connectAttr(nodes['CInfoNode'] + '.arcLength', nodes['Start'] + '.input1X')
    mdnum = 3
    for c in range(mdnum):
        nodes['GlobalScale' + str(c)] = cmds.createNode('multiplyDivide')
        cmds.setAttr(nodes['GlobalScale' + str(c)] + '.operation', 2)
        if c == 0:
            cmds.connectAttr(nodes['Start'] + '.outputX', nodes['GlobalScale' + str(c)] + '.input1X')
        if mdnum > c > 0:
            cmds.connectAttr(nodes['GlobalScale' + str(c - 1)] + '.outputX', nodes['GlobalScale' + str(c)] + '.input1X')
        if c == mdnum - 1:
            cmds.connectAttr(nodes['GlobalScale' + str(c)] + '.outputX', nodes['onOff'] + '.color1R')

    for i in range(1, lenSpine):
        jntTranslateX = cmds.getAttr(rootJoint[i] + '.tx')
        nodes['Stretch' + str(i)] = cmds.createNode('multiplyDivide')
        cmds.setAttr(nodes['Stretch' + str(i)] + '.input2X', jntTranslateX)
        cmds.connectAttr(nodes['onOff'] + '.outputR', nodes['Stretch' + str(i)] + '.input1X')
        cmds.connectAttr(nodes['Stretch' + str(i)] + '.outputX', rootJoint[i] + '.tx')

    return nodes


def spineJoint_squash(listJnts):
    nodes = {}
    clen = len(listJnts)
    cmds.addAttr(listJnts[0], ln='curves', at='double')
    cmds.setKeyframe(listJnts[0] + '.curves', t=1, v=0)
    cmds.setKeyframe(listJnts[0] + '.curves', t=(clen + 1) / 2.0, v=0.5)
    cmds.setKeyframe(listJnts[0] + '.curves', t=clen, v=0)
    squathIntensity = 'squathIntensity'
    for i in range(1, clen):
        cmds.addAttr(listJnts[i - 1], ln=squathIntensity, at='double', min=0, max=1, dv=0)
        cmds.setAttr(listJnts[i - 1] + '.' + squathIntensity, e=True, keyable=True)
        tx = cmds.getAttr(listJnts[i] + '.tx')
        nodes['SquashMD' + str(i)] = cmds.createNode('multiplyDivide')
        nodes['SquashDI' + str(i)] = cmds.createNode('multiplyDivide')
        nodes['SquashPO' + str(i)] = cmds.createNode('multiplyDivide')
        nodes['SquashIn' + str(i)] = cmds.createNode('blendTwoAttr')
        nodes['SquashFR' + str(i)] = cmds.createNode('frameCache')
        cmds.setAttr(nodes['SquashFR' + str(i)] + '.varyTime', i)
        cmds.connectAttr(listJnts[0] + '.curves', nodes['SquashFR' + str(i)] + '.stream')
        cmds.setAttr(nodes['SquashMD' + str(i)] + '.operation', 2)
        cmds.setAttr(nodes['SquashMD' + str(i)] + '.input2X', tx)
        cmds.setAttr(nodes['SquashDI' + str(i)] + '.operation', 2)
        cmds.setAttr(nodes['SquashDI' + str(i)] + '.input1X', 1)
        cmds.setAttr(nodes['SquashPO' + str(i)] + '.operation', 3)
        cmds.connectAttr(listJnts[i] + '.tx', nodes['SquashMD' + str(i)] + '.input1X')
        cmds.connectAttr(nodes['SquashMD' + str(i)] + '.outputX', nodes['SquashDI' + str(i)] + '.input2X')
        cmds.connectAttr(nodes['SquashDI' + str(i)] + '.outputX', nodes['SquashPO' + str(i)] + '.input1X')
        cmds.connectAttr(nodes['SquashFR' + str(i)] + '.varying', nodes['SquashPO' + str(i)] + '.input2X')
        cmds.setAttr(nodes['SquashIn' + str(i)] + '.input[0]', 1)
        cmds.connectAttr(nodes['SquashPO' + str(i)] + '.outputX', nodes['SquashIn' + str(i)] + '.input[1]')
        cmds.connectAttr(listJnts[i - 1] + '.' + squathIntensity, nodes['SquashIn' + str(i)] + '.attributesBlender')
        cmds.connectAttr(nodes['SquashIn' + str(i)] + '.output', listJnts[i - 1] + '.sy')
        cmds.connectAttr(nodes['SquashIn' + str(i)] + '.output', listJnts[i - 1] + '.sz')

    return nodes


def ctrlGroup(object, type, bCurve, bUpLoc, bCtrlNum_s, level):
    """
    ctrlGroup( object,type,curve,upObject ) ->
    ctrlGroup( 'group','cv','curve1','locator1',5,'True') ->
    ctrlGroup( 'locator','cv','curve15754','locator1',1,'' )
    """
    newGrpList = []
    cmds.select(cl=True)
    bCtrlNum = 0
    if type == 'ep':
        bCtrlNum = bCtrlNum_s + 1
    if type == 'cv':
        bCtrlNum = bCtrlNum_s + 3
    for i in range(bCtrlNum):
        cmds.refresh
        pos_t = cmds.xform(bCurve + '.' + type + '[' + str(i) + ']', q=True, ws=True, t=True)
        newGrp = nullObj(object)
        cmds.xform(newGrp, ws=True, t=(pos_t[0], pos_t[1], pos_t[2]))
        newGrpList.append(newGrp)
        if i > 0:
            cmds.delete(cmds.aimConstraint(newGrpList[i], newGrpList[i - 1], worldUpObject=bUpLoc, weight=1,
                                           worldUpType='object'))
            if i == bCtrlNum - 1:
                cmds.delete(cmds.orientConstraint(newGrpList[i - 1], newGrpList[i]))
            if level == 'True':
                cmds.parent(newGrpList[i], newGrpList[i - 1])
                if object == 'joint':
                    cmds.makeIdentity(newGrpList[0], apply=True, t=True, r=True, s=True, n=False)

    return newGrpList


def ctrlGroupMake(object, listJnts, ctrlNum, level):
    """ ctrlGroupMake('locator',listJnts,2,'')
    listJnts = cmds.ls(sl=True)
    len
    2%2
    13%2
    23/3
    9/2
    """
    clen = len(listJnts)
    steps = clen / ctrlNum
    groups = ''
    groupsList = []
    if steps == clen:
        for i in range(2):
            groups = nullObj(object)
            cmds.delete(cmds.parentConstraint(listJnts[i], groups))
            groupsList.append(groups)
            if i == 1:
                cmds.delete(cmds.parentConstraint(listJnts[-1], groupsList[-1]))

    else:
        for i in range(0, clen, steps):
            groups = nullObj(object)
            cmds.delete(cmds.parentConstraint(listJnts[i], groups))
            groupsList.append(groups)
            if i == clen - steps:
                cmds.delete(cmds.parentConstraint(listJnts[-1], groupsList[-1]))

        if level == 'True':
            for i in range(len(groupsList)):
                if i > 0:
                    cmds.parent(groupsList[i], groupsList[i - 1])

    return groupsList


def nullObj(type):
    object = ''
    cmds.select(cl=True)
    if type == 'group':
        object = cmds.group(em=True)
    if type == 'locator':
        objects = cmds.spaceLocator(p=(0, 0, 0))
        object = objects[0]
    if type == 'joint':
        object = cmds.joint(p=(0, 0, 0))
    return object


def replaceShape_xx(object, type, size):
    """controlShape('RLleft_toe1','box',1) """
    controls = ''
    if type == 'circle':
        controls = cmds.circle(nr=[1, 0, 0], d=3, r=size)
    if type == 'box':
        controls = cmds.curve(d=1, p=([size, size, size],
                                      [-size, size, size],
                                      [-size, size, -size],
                                      [size, size, -size],
                                      [size, size, size],
                                      [size, -size, size],
                                      [size, -size, -size],
                                      [size, size, -size],
                                      [-size, size, -size],
                                      [-size, -size, -size],
                                      [size, -size, -size],
                                      [size, -size, size],
                                      [-size, -size, size],
                                      [-size, -size, -size],
                                      [-size, size, -size],
                                      [-size, size, size],
                                      [-size, -size, size],
                                      [size, -size, size],
                                      [size, size, size]))
    bCurveShapeList = cmds.listRelatives(controls, s=True, path=True)
    Shape = bCurveShapeList[0]
    cmds.parent(Shape, object, add=True, shape=True)
    cmds.delete(controls)


def replaceShapes(objGrp, tanObj, col=17):
    cmds.makeIdentity(objGrp, apply=True, t=True, r=True, s=True, n=False)
    objShapeAll = cmds.listRelatives(objGrp, c=True, allDescendents=True)
    for shape in objShapeAll:
        if cmds.nodeType(shape) == 'nurbsCurve':
            if col != 100:
                cmds.setAttr(shape + '.overrideEnabled', 1)
                cmds.setAttr(shape + '.overrideColor', col)
            cmds.parent(shape, tanObj, add=True, shape=True)


def replaceShape(object, type, size=1.0, offset=0.0, col=17):
    """controlShape('RLleft_toe1','box',1) """
    controls = ''
    control = []
    if type == 'c_circle':
        ctl = cmds.circle(nr=[1, 0, 0], d=3, r=size)
        controls = ctl[0]
    elif type == 'c_box':
        ctl = cmds.curve(d=1, p=([size, size, size],
                                 [-size, size, size],
                                 [-size, size, -size],
                                 [size, size, -size],
                                 [size, size, size],
                                 [size, -size, size],
                                 [size, -size, -size],
                                 [size, size, -size],
                                 [-size, size, -size],
                                 [-size, -size, -size],
                                 [size, -size, -size],
                                 [size, -size, size],
                                 [-size, -size, size],
                                 [-size, -size, -size],
                                 [-size, size, -size],
                                 [-size, size, size],
                                 [-size, -size, size],
                                 [size, -size, size],
                                 [size, size, size]))
        controls = ctl
    else:
        ctl = addTestCurves(object, size, type, offset)
        controls = ctl
    replaceShapes(controls, object, col)
    cmds.delete(controls)


def addTestCurves(obj, size=1, names='Dynamics', offset=-6.0):
    textCurve = ''
    if not cmds.objExists(obj + 'Text'):
        ss = size * 0.2
        textCurve = cmds.textCurves(ch=False,
                                    f='\xef\xbf\xbd\xef\xbf\xbd\xef\xbf\xbd\xef\xbf\xbd\xef\xbf\xbd\xef\xbf\xbd\xef\xbf\xbd\xef\xbf\xbd|w400|h-11',
                                    t=names, name=obj + 'Text')
        cmds.setAttr(textCurve[0] + '.s', ss, ss, ss)
        cmds.delete(cmds.pointConstraint(obj, textCurve[0]))
        cmds.parent(textCurve[0], obj)
        cmds.toggle(textCurve[0], state=True, template=True)
    return textCurve[0]


def channelsAttr(objects, attributes, type):
    """ user lock unlock hide show command,example :  """
    for object in objects:
        for attribute in attributes:
            if type == 'hide':
                cmds.setAttr(object + '.' + attribute, keyable=False, channelBox=False)
            if type == 'show':
                cmds.setAttr(object + '.' + attribute, channelBox=True)
                cmds.setAttr(object + '.' + attribute, keyable=True)
            if type == 'hideLock':
                cmds.setAttr(object + '.' + attribute, lock=True, keyable=False, channelBox=False)
            if type == 'showUnlock':
                cmds.setAttr(object + '.' + attribute, lock=False, channelBox=True)
                cmds.setAttr(object + '.' + attribute, keyable=True)
            if type == 'shapeVisHide':
                objectShapes = cmds.listRelatives(object, s=True, path=True)
                for shape in objectShapes:
                    cmds.setAttr(shape + '.' + attribute, 0)

            if type == 'shapeVisShow':
                objectShapes = cmds.listRelatives(object, s=True, path=True)
                for shape in objectShapes:
                    cmds.setAttr(shape + '.' + attribute, 1)


def connectAttr1(objects, tangents, type, start):
    if type == 'shapeVis':
        for i in range(start, len(tangents)):
            objectShapes = cmds.listRelatives(tangents[i], s=True, path=True)
            for shape in objectShapes:
                if cmds.nodeType(shape) == 'nurbsCurve':
                    cmds.connectAttr(objects, shape + '.visibility')


def addAttributeBase1(objects, tangent):
    attr = dynaimicsAttr2()
    for i in range(len(attr)):
        cAddAttr(objects, attr[i][0], attr[i][1], attr[i][2], attr[i][3])

    if tangent != '':
        cmds.connectAttr(objects + '.' + attr[0][0], tangent + '.blender')


def addAttributeBase1_1(objects, tangent):
    attr = dynaimicsAttr2_1()
    for i in range(len(attr)):
        cAddAttr(objects, attr[i][0], attr[i][1], attr[i][2], attr[i][3])

    if tangent != '':
        cmds.connectAttr(objects + '.' + attr[0][0], tangent + '.blender')


def addAttributeAndConnect1(objects, tangent):
    attr = dynaimicsAttr3()
    for i in range(len(attr)):
        cAddAttr(objects, attr[i][0], attr[i][1], attr[i][2], attr[i][3])

    if tangent != '':
        connectAttrCmd(objects, tangent, attr)


def dynaimicsAttr3():
    attr = [['pointLock',
             'enum',
             'NoAttach,Base,Tip,BothEnds',
             '']]
    return attr


def dynaimicsAttr2_1():
    attr = [['stretch',
             'double',
             '0,1,1',
             ''], ['squathIntensity',
                   'double',
                   '0,1,1',
                   '']]
    return attr


def dynaimicsAttr2():
    attr = [['fkCtrlVis',
             'long',
             '0,1,1',
             ''],
            ['ikCtrlVis',
             'long',
             '0,1,1',
             ''],
            ['localCtrlVis',
             'long',
             '0,1,0',
             ''],
            ['dynamicVis',
             'long',
             '0,1,0',
             '']]
    return attr


def dynaimicsAttr1():
    attr = [['simulationMethod',
             'enum',
             'Off,Static,DynamicFolliclesOnly,AllFollicles',
             ''],
            ['collide',
             'double',
             '0,1,1',
             ''],
            ['startFrame',
             'long',
             ',,1',
             ''],
            ['stiffness',
             'double',
             '0,1,.75',
             ''],
            ['drag',
             'double',
             ',,0.1',
             ''],
            ['motionDrag',
             'double',
             ',,0',
             ''],
            ['damp',
             'double',
             '0,1,0',
             ''],
            ['friction',
             'double',
             '0,,1',
             ''],
            ['mass',
             'double',
             '0,,5',
             ''],
            ['gravity',
             'double',
             ',,9.8',
             ''],
            ['dynamicsWeight',
             'double',
             '0,1,1',
             ''],
            ['startCurveAttract',
             'double',
             '0,1,.85',
             ''],
            ['attractionDamp',
             'double',
             '0,1,0',
             ''],
            ['attractionScale_Position',
             'double',
             '0,1,0',
             '']]
    return attr


def addAttributeAndConnect2(objects, tangent):
    attr = dynaimicsAttr1()
    for i in range(len(attr)):
        cAddAttr(objects, attr[i][0], attr[i][1], attr[i][2], attr[i][3])

    if tangent != '':
        connectAttrCmd(objects, tangent, attr)


def connectAttrCmd(objects, tangent, attributes):
    keyables = cmds.listAttr(tangent, k=True)
    for attrs in attributes:
        if len(attrs) > 0:
            attr = attrs[0]
            if attr in keyables:
                cmds.connectAttr(objects + '.' + attr, tangent + '.' + attr, f=True)
            if attr == 'attractionScale_Position':
                cmds.connectAttr(objects + '.' + attr, tangent + '.attractionScale[0].' + attr, f=True)


def createPointOnCurveTmp(bcurve):
    infoNode = cmds.pointOnCurve(bcurve, ch=True, pr=0.55)
    cmds.setAttr(infoNode + '.turnOnPercentage', 1)
    bgroup = nullObj('locator')
    cmds.connectAttr(infoNode + '.position', bgroup + '.translate')
    tangentConstraints = cmds.tangentConstraint(bcurve, bgroup)
    return (infoNode, bgroup, tangentConstraints)


def userAttributes(objects, attributes, value):
    value = int(value)
    for i in range(len(objects)):
        for c in range(len(attributes)):
            if value == 0:
                cmds.setAttr(objects[i] + '.' + attributes[c], lock=0)
                cmds.setAttr(objects[i] + '.' + attributes[c], 0)
                cmds.setAttr(objects[i] + '.' + attributes[c], lock=1)
            if value == 1:
                cmds.setAttr(objects[i] + '.' + attributes[c], lock=0)
                cmds.setAttr(objects[i] + '.' + attributes[c], 1)
                cmds.setAttr(objects[i] + '.' + attributes[c], lock=1)


def linkToRollIKJnt(sourceJnt, tangentJnt):
    clen = len(sourceJnt)
    node = {}
    trsGrp = {'Translate': 't',
              'Rotate': 'r',
              'Scale': 's'}
    xyzGrp = ['x', 'y', 'z']
    for i in range(clen):
        ii = str(i + 1)
        for c in range(len(trsGrp)):
            node[trsGrp.keys()[c] + ii] = cmds.createNode('plusMinusAverage')
            for xyz in xyzGrp:
                cmds.connectAttr(sourceJnt[i] + '.' + trsGrp.values()[c] + xyz,
                                 node[trsGrp.keys()[c] + ii] + '.input3D[0].input3D' + xyz)
                cmds.connectAttr(node[trsGrp.keys()[c] + ii] + '.output3D' + xyz,
                                 tangentJnt[i] + '.' + trsGrp.values()[c] + xyz)

    return node


def createRollIK(listJnts, groups, intensionYAttr, offsetYAttr, intensionZAttr, offsetZAttr):
    """
    listJnts = cmds.ls(sl=True,dag=True,type='joint')
    intensionYAttr = 'intensionY'
    offsetYAttr = 'offsetY'
    intensionZAttr = 'intensionZ'
    offsetZAttr = 'offsetZ'
    groups = []

    """
    jntSize = len(listJnts)
    node = {}
    attr = [[intensionYAttr,
             'double',
             '',
             ''],
            [offsetYAttr,
             'double',
             ',,1',
             ''],
            [intensionZAttr,
             'double',
             '',
             ''],
            [offsetZAttr,
             'double',
             ',,1',
             '']]
    for i in range(len(attr)):
        cAddAttr(listJnts[0], attr[i][0], attr[i][1], attr[i][2], attr[i][3])

    intensionYAttrAll = listJnts[0] + '.' + intensionYAttr
    offsetYAttrAll = listJnts[0] + '.' + offsetYAttr
    intensionZAttrAll = listJnts[0] + '.' + intensionZAttr
    offsetZAttrAll = listJnts[0] + '.' + offsetZAttr
    nodeName = ['nodeY_cd', 'nodeZ_cd']
    rgbGrp = ['R', 'G', 'B']
    for i in range(len(nodeName)):
        node[nodeName[i]] = cmds.createNode('condition')
        cmds.setAttr(node[nodeName[i]] + '.operation', 4)
        for c in range(len(rgbGrp)):
            cmds.setAttr(node[nodeName[i]] + '.colorIfTrue' + rgbGrp[c], -1)

    cmds.connectAttr(intensionYAttrAll, node['nodeY_cd'] + '.firstTerm')
    cmds.connectAttr(intensionZAttrAll, node['nodeZ_cd'] + '.firstTerm')
    for i in range(jntSize):
        ii = str(i + 1)
        node['nodeY_rv' + ii] = cmds.createNode('remapValue')
        node['nodeZ_rv' + ii] = cmds.createNode('remapValue')
        node['node_md_Imin' + ii] = cmds.createNode('multiplyDivide')
        node['node_md_Imax' + ii] = cmds.createNode('multiplyDivide')
        node['node_md_Omin' + ii] = cmds.createNode('multiplyDivide')
        node['node_md_Omax' + ii] = cmds.createNode('multiplyDivide')
        node['node_md_size' + ii] = cmds.createNode('multiplyDivide')
        imin = jntSize - i - 1
        imax = jntSize - i
        cmds.setAttr(node['node_md_Imin' + ii] + '.input1Y', imin)
        cmds.setAttr(node['node_md_Imax' + ii] + '.input1Y', imax)
        cmds.setAttr(node['node_md_Omin' + ii] + '.input1Y', 0)
        cmds.setAttr(node['node_md_Omax' + ii] + '.input1Y', 10 + 3.5 * i)
        cmds.setAttr(node['node_md_Imin' + ii] + '.input1Z', imin)
        cmds.setAttr(node['node_md_Imax' + ii] + '.input1Z', imax)
        cmds.setAttr(node['node_md_Omin' + ii] + '.input1Z', 0)
        cmds.setAttr(node['node_md_Omax' + ii] + '.input1Z', 10 + 3.5 * i)
        cmds.connectAttr(intensionYAttrAll, node['nodeY_rv' + ii] + '.inputValue')
        cmds.connectAttr(intensionZAttrAll, node['nodeZ_rv' + ii] + '.inputValue')
        cmds.connectAttr(node['nodeY_cd'] + '.outColorG', node['node_md_Imin' + ii] + '.input2Y')
        cmds.connectAttr(node['nodeY_cd'] + '.outColorG', node['node_md_Imax' + ii] + '.input2Y')
        cmds.connectAttr(node['nodeY_cd'] + '.outColorG', node['node_md_Omin' + ii] + '.input2Y')
        cmds.connectAttr(node['nodeY_cd'] + '.outColorG', node['node_md_Omax' + ii] + '.input2Y')
        cmds.connectAttr(node['nodeZ_cd'] + '.outColorB', node['node_md_Imin' + ii] + '.input2Z')
        cmds.connectAttr(node['nodeZ_cd'] + '.outColorB', node['node_md_Imax' + ii] + '.input2Z')
        cmds.connectAttr(node['nodeZ_cd'] + '.outColorB', node['node_md_Omin' + ii] + '.input2Z')
        cmds.connectAttr(node['nodeZ_cd'] + '.outColorB', node['node_md_Omax' + ii] + '.input2Z')
        cmds.connectAttr(node['node_md_Imin' + ii] + '.outputY', node['nodeY_rv' + ii] + '.inputMin')
        cmds.connectAttr(node['node_md_Imax' + ii] + '.outputY', node['nodeY_rv' + ii] + '.inputMax')
        cmds.connectAttr(node['node_md_Omin' + ii] + '.outputY', node['nodeY_rv' + ii] + '.outputMin')
        cmds.connectAttr(node['node_md_Omax' + ii] + '.outputY', node['nodeY_rv' + ii] + '.outputMax')
        cmds.connectAttr(node['node_md_Imin' + ii] + '.outputZ', node['nodeZ_rv' + ii] + '.inputMin')
        cmds.connectAttr(node['node_md_Imax' + ii] + '.outputZ', node['nodeZ_rv' + ii] + '.inputMax')
        cmds.connectAttr(node['node_md_Omin' + ii] + '.outputZ', node['nodeZ_rv' + ii] + '.outputMin')
        cmds.connectAttr(node['node_md_Omax' + ii] + '.outputZ', node['nodeZ_rv' + ii] + '.outputMax')
        cmds.connectAttr(node['nodeY_rv' + ii] + '.outColorG', node['node_md_size' + ii] + '.input1Y')
        cmds.connectAttr(node['nodeZ_rv' + ii] + '.outColorG', node['node_md_size' + ii] + '.input1Z')
        cmds.connectAttr(offsetYAttrAll, node['node_md_size' + ii] + '.input2Y')
        cmds.connectAttr(offsetZAttrAll, node['node_md_size' + ii] + '.input2Z')
        try:
            cmds.connectAttr(node['node_md_size' + ii] + '.outputY', groups['Rotate' + ii] + '.input3D[1].input3Dy')
            cmds.connectAttr(node['node_md_size' + ii] + '.outputZ', groups['Rotate' + ii] + '.input3D[1].input3Dz')
        except:
            pass

    return node


def channelControls(objects=[], listAttrs=['v'], controls=[]):
    command = ''
    for obj in objects:
        for attr in listAttrs:
            for ctl in controls:
                command += "cmds.setAttr(('%s.%s'),%s)\n" % (obj, attr, ctl)
                exec command


def getParentsCmd(transform):
    parentsList = [transform]
    parentsAllList = []
    while 1:
        parentsList = cmds.listRelatives(parentsList[0], parent=True)
        if parentsList is None:
            break
        else:
            parentsAllList.append(parentsList[0])

    return parentsAllList


# -----------------------------------------------------------------------------

def closestPointOnMeshResult(object, meshHight):
    result = {}
    meshHightShape = ''
    meshHightShapes = cmds.listRelatives(meshHight, s=True, path=True)
    for shape in meshHightShapes:
        if not cmds.getAttr('%s.intermediateObject' % shape):
            meshHightShape = shape
            print meshHightShape

    node = cmds.createNode('closestPointOnMesh')
    cmds.connectAttr(meshHightShape + '.outMesh', node + '.inMesh')
    grp1 = cmds.group(em=True)
    cmds.delete(cmds.pointConstraint(object, grp1))
    cmds.delete(cmds.geometryConstraint(meshHight, grp1))
    pos = cmds.xform(grp1, q=True, ws=True, t=True)
    cmds.setAttr(node + '.inPosition', pos[0], pos[1], pos[2])
    result['faceIndex'] = cmds.getAttr(node + '.result.closestFaceIndex')
    result['vertexIndex'] = cmds.getAttr(node + '.result.closestVertexIndex')
    result['parameterU'] = cmds.getAttr(node + '.result.parameterU')
    result['parameterV'] = cmds.getAttr(node + '.result.parameterV')
    cmds.select(object)
    cmds.delete(node, grp1)
    return result


def createFollByPosition():
    listOldFoll = cmds.ls(sl=True)
    meshHight = cmds.textField('meshObjTF', q=True, text=True)
    pointList = []
    result = {}
    createFollByPositionOBJ(listOldFoll, meshHight)
    return pointList
    print 'OKKKKKKKKKKKK',
    print


def createFollByPositionOBJ(listOldFoll, meshHight):
    pointList = []
    result = {}
    for foll in listOldFoll:
        result = closestPointOnMeshResult(foll, meshHight)
        vertexIndex = result['vertexIndex']
        point = meshHight + '.vtx[' + str(vertexIndex) + ']'
        folls = createFollicle(meshHight, result['parameterU'], result['parameterV'])
        pointList.append(folls)
        cmds.select(cl=True)

    return pointList


def createJointBySelect():
    listFolls = cmds.ls(sl=True)
    for i in range(len(listFolls)):
        cmds.select(cl=True)
        joints = cmds.joint(p=(0, 0, 0), name=listFolls[i] + '_jnt')
        groups = cmds.group(em=True, name=listFolls[i] + 'Offset')
        groups1 = cmds.group(em=True, name=listFolls[i] + 'C1_ctl')
        groups2 = cmds.group(em=True, name=listFolls[i] + 'C2_ctl')
        cmds.parent(joints, groups2)
        cmds.parent(groups2, groups1)
        cmds.parent(groups1, groups)
        cmds.parentConstraint(listFolls[i], groups, weight=True)


def createFoll(index):
    listJnts = cmds.ls(sl=True, fl=True)
    return createFoll_obj(listJnts)


def createFoll_obj(listJnts):
    follList = []
    for i in range(len(listJnts)):
        foll = createFoll_sigle
        if foll is None:
            continue
        follList.append(foll)

    return follList


def createFoll_sigle(obj):
    uvs = getTranformUV(obj)
    if uvs is None:
        return
    objects = ''
    meshHightShape = ''
    follicles = cmds.createNode('follicle')
    follicle = cmds.listRelatives(follicles, parent=True)
    if type(obj) is list:
        objects = obj[0].split('.')
    else:
        objects = obj.split('.')
    shapes = cmds.listRelatives(objects[0])
    for shape in shapes:
        if not cmds.getAttr('%s.intermediateObject' % shape):
            meshHightShape = shape

    cmds.connectAttr(meshHightShape + '.outMesh', follicles + '.inputMesh')
    cmds.connectAttr(meshHightShape + '.worldMatrix[0]', follicles + '.inputWorldMatrix')
    cmds.connectAttr(follicles + '.outTranslate', follicle[0] + '.translate')
    cmds.connectAttr(follicles + '.outRotate', follicle[0] + '.rotate')
    parU, parV = (0.0, 0.0)
    parU = uvs[0]
    parV = uvs[1]
    cmds.setAttr(follicles + '.parameterU', parU)
    cmds.setAttr(follicles + '.parameterV', parV)
    cmds.select(cl=True)
    return follicle[0]


def getTranformUV(obj):
    uv = cmds.polyEditUV(obj, q=True, u=True)
    return uv


def shortFloat(ts):
    tsStr = str(ts)
    tsStrSplit = tsStr.split('.')
    ts1_list = list(tsStrSplit[1])
    ts0 = tsStrSplit[0]
    ts1 = ''
    for i in range(4):
        ts1 += ts1_list[i]

    tsOk = ts0 + '.' + ts1
    return tsOk


def printTranformUV():
    listObjs = cmds.ls(sl=True)
    if len(listObjs) == 1:
        resU, resV = ('', '')
        meshHight = cmds.textField('meshObjTF', q=True, text=True)
        if cmds.nodeType(listObjs[0]) == 'transform' or cmds.nodeType(listObjs[0]) == 'joint':
            result = closestPointOnMeshResult(listObjs[0], meshHight)
            resU = shortFloat(result['parameterU'])
            resV = shortFloat(result['parameterV'])
            print result,
        else:
            result = getTranformUV()
            resU = shortFloat(result[0])
            resV = shortFloat(result[1])
            print result,
        cmds.text('printTranformUVTX', e=True, label='U: %s  V: %s' % (resU, resV))


def addSelectMeshToTextField():
    listObject = cmds.ls(sl=True)
    if len(listObject) == 1:
        cmds.textField('meshObjTF', e=True, text=listObject[0])


def follWindows():
    text = 'load mesh ... '
    listObjs = cmds.ls(sl=True)
    if len(listObjs):
        text = listObjs[0]
    if cmds.window('follToolWindow', q=True, ex=True):
        cmds.deleteUI('follToolWindow')
    else:
        cmds.window('follToolWindow', title='Follicle Tool', tlb=True)
        cmds.columnLayout(adj=True, rowSpacing=5)
        cmds.textField('meshObjTF', text=text, editable=False)
        cmds.button(label='Create Foll By Mesh', h=40, command="createFoll('')")
        cmds.button(label='Create Foll By Select', h=40, command='createFollByPosition()')
        cmds.button(label='Create Joint By Select', h=40, command='createJointBySelect()')
        cmds.button(label='Get UV Bound', h=25, command='printTranformUV()')
        cmds.text('printTranformUVTX', label='-none-')
        cmds.popupMenu(p='meshObjTF')
        cmds.menuItem(label='Add Select Mesh', command='addSelectMeshToTextField()')
        cmds.showWindow('follToolWindow')


def createFollicle(meshShape, parU, parV):
    follicles = cmds.createNode('follicle')
    follicle = cmds.listRelatives(follicles, parent=True)
    cmds.setAttr(follicles + '.parameterU', parU)
    cmds.setAttr(follicles + '.parameterV', parV)
    cmds.connectAttr(meshShape + '.outMesh', follicles + '.inputMesh')
    cmds.connectAttr(meshShape + '.worldMatrix[0]', follicles + '.inputWorldMatrix')
    cmds.connectAttr(follicles + '.outTranslate', follicle[0] + '.translate')
    cmds.connectAttr(follicles + '.outRotate', follicle[0] + '.rotate')
    return follicle[0]


# -----------------------------------------------------------------------------
def rivet():
    file_path = pm.Path(__file__)
    shelvesPath = file_path.parent.joinpath('/rivet.mel')
    node = None
    try:
        node = pm.mel.eval('source "%s"' % shelvesPath.replace('\\', '/'))
    except:
        pass

    if node is not None:
        node = pm.PyNode(node)
        node.rename('rivet#')
        return node.name()


def meshRepairCmd():
    nodes = {}
    listObj = cmds.ls(sl=True, fl=True)
    size = len(listObj)
    if size > 0 and '.' in listObj[0]:
        lockAttrList, hideObjList, parentsAllList = [], [], []
        dist, distMax = (0.0, 0.0)
        modifyWeight = 0
        transformName = ''
        folliclesList = None
        if size > 1:
            if '.e' in listObj[0] and '.e' in listObj[1]:
                cmds.select(listObj[0], listObj[-1])
                folliclesList = rivet()
        if folliclesList is None:
            mm.eval('ConvertSelectionToUVs()')
            listObj = cmds.ls(sl=True, fl=True)
            folliclesList = createFoll_sigle(listObj[0])
        if folliclesList is None:
            pm.warning('Select two edge, and retry.')
            return
        cmds.select(listObj)
        mm.eval('ConvertSelectionToVertices()')
        listObj = cmds.ls(sl=True, fl=True)
        splitObject = listObj[0].split('.')
        transform = splitObject[0]
        if ':' in transform:
            nameSplit = transform.split(':')
            transformName = nameSplit[1]
        else:
            transformName = transform
        parentsList = cmds.listRelatives(transform, parent=True)
        if parentsList is None:
            pass
        else:
            parentsAllList = getParentsCmd(transform)
        pe_v = cmds.polyEvaluate(transform, v=True)
        nodes['follicles'] = folliclesList
        newCluster = cmds.cluster(transform, before=True)
        clusters = newCluster[0]
        cmds.setAttr('%s.ihi' % clusters, 0)
        nodes['clusterHandle'] = newCluster[1]
        cmds.setAttr('%s.relative' % clusters, 1)
        cmds.percent(clusters, '%s.vtx[0:%d]' % (transform, pe_v), v=0)
        cmds.percent(clusters, listObj, v=1)
        nodes['G1'] = cmds.group(em=True)
        nodes['G2'] = cmds.group(em=True)
        nodes['G3'] = cmds.group(em=True, name='repairCtl#')
        cmds.parent(nodes['G2'], nodes['G1'])
        cmds.parent(nodes['G3'], nodes['G2'])
        cmds.connectAttr('%s.t' % nodes['G3'], '%s.t' % nodes['clusterHandle'])
        cmds.connectAttr('%s.r' % nodes['G3'], '%s.r' % nodes['clusterHandle'])
        cmds.connectAttr('%s.s' % nodes['G3'], '%s.s' % nodes['clusterHandle'])
        print '>>>nodes', nodes
        cmds.pointConstraint(nodes['follicles'], nodes['G1'])
        nodes['mdNode1'] = cmds.createNode('multiplyDivide')
        cmds.setAttr('%s.ihi' % nodes['mdNode1'], 0)
        cmds.setAttr('%s.input2' % nodes['mdNode1'], -1, -1, -1)
        cmds.connectAttr('%s.t' % nodes['G3'], '%s.input1' % nodes['mdNode1'])
        cmds.connectAttr('%s.output' % nodes['mdNode1'], '%s.t' % nodes['G2'])
        dagCon = cmds.createNode('dagContainer', name='repair#')
        cmds.setAttr('%s.blackBox' % dagCon, 1, l=True)
        cmds.setAttr('%s.iconName' % dagCon, 'out_transform.png', type='string', l=True)
        pm.parent(nodes['follicles'], nodes['clusterHandle'], nodes['G1'], dagCon)
        nodes['defGrp'] = dagCon
        if len(parentsAllList):
            pass
        hideObjList = [nodes['follicles'], nodes['clusterHandle']]
        lockAttrList = [nodes['G1'],
                        nodes['G2'],
                        nodes['follicles'],
                        nodes['clusterHandle'],
                        nodes['defGrp'],
                        nodes['mdNode1']]
        for hideObj in hideObjList:
            cmds.setAttr('%s.v' % hideObj, 0)

        for obj in lockAttrList:
            print obj
            attrList = cmds.listAttr(obj, keyable=True)
            for attr in attrList:
                cmds.setAttr('%s.%s' % (obj, attr), lock=True, keyable=False, channelBox=False)

        RS_Pivot = 'RS_Pivot'
        envelope = 'envelope'
        cmds.addAttr(nodes['G3'], ln=envelope, at='double', min=0, max=1, dv=1)
        cmds.setAttr('%s.%s' % (nodes['G3'], envelope), keyable=True)
        cmds.connectAttr('%s.%s' % (nodes['G3'], envelope), '%s.%s' % (clusters, envelope))
        cmds.addAttr(nodes['G2'], ln=RS_Pivot, at='double3')
        cmds.addAttr(nodes['G2'], ln='%sX' % RS_Pivot, at='double', p=RS_Pivot)
        cmds.addAttr(nodes['G2'], ln='%sY' % RS_Pivot, at='double', p=RS_Pivot)
        cmds.addAttr(nodes['G2'], ln='%sZ' % RS_Pivot, at='double', p=RS_Pivot)
        cmds.setAttr('%s.%s' % (nodes['G2'], RS_Pivot), keyable=True)
        cmds.setAttr('%s.%sX' % (nodes['G2'], RS_Pivot), keyable=True)
        cmds.setAttr('%s.%sY' % (nodes['G2'], RS_Pivot), keyable=True)
        cmds.setAttr('%s.%sZ' % (nodes['G2'], RS_Pivot), keyable=True)
        cmds.connectAttr('%s.%s' % (nodes['G2'], RS_Pivot), '%s.rotatePivot' % nodes['clusterHandle'])
        cmds.connectAttr('%s.%s' % (nodes['G2'], RS_Pivot), '%s.scalePivot' % nodes['clusterHandle'])
        cmds.setAttr('%s.displayHandle' % nodes['G3'], 1, k=True)
        cmds.setAttr('%s.v' % nodes['G3'], 1, k=False)
        size = 0.25
        if cmds.currentUnit(q=True, linear=True) == 'm':
            size = 0.025
        replaceShape(nodes['G3'], 'c_box', size, 0, 25)
        cmds.select(nodes['G3'])
        setKeyFrameCmd(1, '+')
        setKeyFrameCmd(1, '-')
        resetPivotCmd_select()
        try:
            vid = listObj[0].split('[')[1].split(']')[0]
            renameDict1(nodes, '%sF%d_' % (transformName, vid))
        except:
            pass

        cmds.containerPublish(dagCon, publishNode=['repairCtl', ''])
        cmds.containerPublish(dagCon, bindNode=['repairCtl', nodes['G3']])
    return nodes


def resetPivotCmd(ctlObj):
    if '|' in ctlObj:
        splitStr = ctlObj.split('|')
        souObj = splitStr[len(splitStr) - 3]
        tanObj = splitStr[len(splitStr) - 2]
        gAttrT = cmds.getAttr('%s.t' % souObj)
        cmds.setAttr('%s.RS_Pivot' % tanObj, gAttrT[0][0], gAttrT[0][1], gAttrT[0][2])
        cmds.setKeyframe(tanObj, at='RS_Pivot')


def resetPivotCmd_List(listObjs):
    for obj in listObjs:
        resetPivotCmd(obj)


def resetPivotCmd_select():
    listObjs = cmds.ls(sl=True, l=True, allPaths=True)
    resetPivotCmd_List(listObjs)


def bakePivotCmd():
    listObjs = cmds.ls(sl=True, l=True, allPaths=True)
    minTime = int(cmds.playbackOptions(q=True, min=True))
    maxTime = int(cmds.playbackOptions(q=True, max=True))
    for i in range(minTime, maxTime + 1):
        resetPivotCmd_List(listObjs)
        mm.eval('playButtonStepForward')


def setKeyFrameCmd(distTime, pos):
    listObjs = cmds.ls(sl=True)
    attrList = ['t', 'r', 's']
    for obj in listObjs:
        gTime = cmds.currentTime(query=True)
        cmds.setKeyframe(obj, time=gTime, at=attrList)
        if pos == '+' or pos == '-':
            for attr in attrList:
                atTime = eval('%d%s%d' % (gTime, pos, distTime))
                if 's' in attr:
                    cmds.setKeyframe(obj, time=atTime, v=1, at=attr)
                else:
                    cmds.setKeyframe(obj, time=atTime, v=0, at=attr)


def paintClusterWightCmd():
    listObjs = cmds.ls(sl=True)
    if len(listObjs):
        clusObj = listObjs[0]
        attrs = 'envelope'
        attrs_out = 'outputGeometry'
        try:
            clusObjList = cmds.connectionInfo('%s.%s' % (clusObj, attrs), destinationFromSource=True)
            clustSplit = clusObjList[0].split('.')
            clusters = clustSplit[0]
            listAttrs = [clusters]
            while 1:
                if cmds.attributeQuery(attrs_out, exists=True, node=listAttrs[0]):
                    listAttrs = cmds.listConnections('%s.%s' % (listAttrs[0], attrs_out), destination=True)
                else:
                    break

            cmds.select(listAttrs[0])
            evalCmd = 'artAttrToolScript 3 "cluster";artSetToolAndSelectAttr( "artAttrCtx", "cluster.%s.weights" )' % clusters
            mm.eval(evalCmd)
        except:
            print 'you need select controls .'


def deleteControlCmd():
    listCtls = cmds.ls(sl=True)
    comstr = 'null'
    comstrA = 'group'
    for ctl in listCtls:
        if comstr in ctl:
            gParents = getParentsCmd(ctl)
            if comstrA in gParents[2]:
                cmds.delete(gParents[2])


if __name__ == '__main__':
    RepairUI = Win()
    RepairUI.show()
