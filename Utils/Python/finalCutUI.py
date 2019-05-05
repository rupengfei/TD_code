import maya.cmds as cmds
from CRT.Python.finalCutCmd import *

def meshRepairWin(width,high) :
	countBut = 4
	if cmds.window( 'meshRepairUI',q=True,ex=True ) :
		cmds.deleteUI('meshRepairUI')
	cmds.window('meshRepairUI',title='Final Cut',toolbox=True,maximizeButton=False,sizeable=False) # Mesh Repair
	cmds.columnLayout(adj=True)
	
	cmds.rowColumnLayout(numberOfRows=1)
	cmds.button(w=width/(countBut*2.2),h=high/20,label="",command=("editWindow(-10)") )
	for i in range(countBut) :
		sizeW = 100 + i*50
		sizeH = 100 + i*25
		cmdStr = "meshRepairWin(%d,%d)" % (sizeW,sizeH)
		cmds.button(w=width/(countBut+1),h=high/20,label="",command=cmdStr )
	cmds.button(w=width/(countBut*2.2),h=high/20,label="",command=("editWindow(10)") )
	cmds.setParent('..')
	
	cmds.rowColumnLayout(numberOfRows=1)
	cmds.button(w=width/1.5,h=high,label='Create',command=("meshRepairCmd()"))
	cmds.columnLayout(adj=True)
	cmds.button(w=width/3,h=high/1.25,label='Paint',command=("paintClusterWightCmd()"))
	cmds.button(w=width/3,h=high/4.0,label='Delete',command=("deleteControlCmd()"),enable=True)
	cmds.setParent('..')
	cmds.setParent('..')
	
	cmds.rowColumnLayout(numberOfRows=1)
	cmds.rowColumnLayout(numberOfColumns=2)
	cmds.button(w=width/3,h=high/4,label='|<',command=("mm.eval('playButtonStepBackward')"))
	cmds.button(w=width/3,h=high/4,label='>|',command=("mm.eval('playButtonStepForward')"))
	cmds.button(w=width/3,h=high/4,label='|<',bgc=[.588,.268,.341],command=("setKeyFrameCmd(1,'-');mm.eval('playButtonStepBackward')"))
	cmds.button(w=width/3,h=high/4,label='>|',bgc=[.588,.268,.341],command=("setKeyFrameCmd(1,'+');mm.eval('playButtonStepForward')"))
	cmds.setParent('..')
	cmds.button(w=width/3,h=high/4,label='<Key>',bgc=[.588,.268,.341],command=("setKeyFrameCmd(1,'')"))
	cmds.setParent('..')
	
	cmds.rowColumnLayout(numberOfRows=1)
	cmds.button(w=width/3,h=high/4,label='Update',command=("resetPivotCmd_select()"))
	cmds.button(w=width/1.5,h=high/4,label='Bake Pivot >>>',command=("bakePivotCmd()"))
	cmds.showWindow('meshRepairUI')
	cmds.window('meshRepairUI',e=True,wh=[(width+5),high*2])
	
def editWindow( extent = 5):
	whSizes = cmds.window( 'meshRepairUI',q=True,wh=True )
	meshRepairWin( (whSizes[0]-5 + extent),(whSizes[1]/2) )

if __name__ == '__main__':
	meshRepairWin(200,150)