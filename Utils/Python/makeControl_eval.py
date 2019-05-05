import maya.cmds as cmds
# import makeSpine as cc
import CRT.Python.makeSpine as cc


def makeControl_eval() :
    '''
    this command use make dynamics spine by seleced curves
    create time : 2012.10
    modify time :2012.11
    '''
    bJntNum1 = cmds.intSliderGrp('csj_jointNum_isg',q=True,v=True) -1
    bCtrlNum1 = cmds.intSliderGrp('csj_controlNum_isg',q=True,v=True) -1
    controlSize1 = cmds.floatSliderGrp('csj_controlSize_isg',q=True,v=True)
    if bJntNum1 < bCtrlNum1 :
        bCtrlNum1 = bJntNum1
        
    BaseCurve1 = cmds.ls(sl=True,allPaths=True)
    try :
        for i in range( len(BaseCurve1) ) :
            parents = cmds.ls( BaseCurve1[i],dag=True,type="transform" )
            bName = parents[0]
            upLocs = cmds.duplicate(parents[1])
            upLoc = upLocs[0]
            cmds.parent( upLocs[0],w=True )
            cmds.delete( parents[1],parents[3] )
            groups = cc.makeSpine( parents[0],upLoc,bJntNum1,bCtrlNum1,parents[0],controlSize1 )
            cmds.delete( upLoc )
    except:
        return('you need select some curve .')

def connectToGlobalScale():
    BaseCurve1 = cmds.ls(sl=True,allPaths=True)
    clen = len( BaseCurve1 )
    
    if clen > 1:
        for i in range( 1,clen ) :
            sourcts = BaseCurve1[0]
            tangent = BaseCurve1[i]
            getPrefix = tangent.split('FK1')
            attrName = getPrefix[0] + 'GlobalScale1_md'
            try :
                cmds.connectAttr( (sourcts + '.s'),(attrName + '.input2') )
            except :
                pass

# makeControl_eval()