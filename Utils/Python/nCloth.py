import maya.cmds as cmds
import maya.mel as mm
import os
from functools import partial

class NCloth() :

    def __init__(self) :
        self.localTime = 'localSimulationTime'
        self.time = 'time1'
        self.nucleus = 'nucleus1'
        self.conNode  =  'timeSwitchCondition'
        self.globalDir = "//192.168.10.230/workvol_mov/shelvers/Animation Technology/"

    def createNcloth(self,transforms,*args) :
        melFile_cache = "%s\xb6\xaf\xbb\xad\xb9\xa4\xbe\xdf\xbc\xdc/mel/cloth/cacheFile.mel" % self.globalDir

        mm.eval( "source \"" + melFile_cache + "\"")

        cloth_sim = 'nCloth_sim'
        cloth_out = 'cloth_output'
        # string $animationBS1[] = `blendShape -n "animation#" $animationMesh $outputMesh `;

        nClothMesh = cmds.duplicate( transforms,name = '%s_nMesh#' % transforms )[0]
        cmds.hide( transforms )
        shapeList = cmds.listRelatives( nClothMesh,f=True,s=True )
        for shape in shapeList :
            if cmds.getAttr( '%s.intermediateObject' % shape ) :
                cmds.delete( shape )

        outputMesh = cmds.duplicate( nClothMesh,name = '%s_output#' % transforms )[0]
        cmds.select( nClothMesh )
        bs_input = cmds.blendShape( transforms,nClothMesh,name="%s_bs#" % transforms )[0]
        cmds.blendShape( bs_input,e=True,w=[0,1] )
        cmds.setAttr( "%s.ihi" % bs_input,0 )
        clothNodes = mm.eval( "createNCloth 0")
        clothTransfrom = cmds.listRelatives( clothNodes,p=True )[0]
        clothTransfrom = cmds.rename( clothTransfrom,'%s_nCloth#' % transforms )
        mm.eval( "connectToOutputMesh " + transforms + " " + outputMesh + " " + nClothMesh )
        mm.eval( "addGroupAndLayer " + outputMesh + " " + cloth_out + " " + "0" )
        mm.eval( "assignShadings " + outputMesh + " " + cloth_out + " " + "{0.75,0.75,0}" )
        mm.eval( "addGroupAndLayer " + nClothMesh + " " + cloth_sim + " " + "1" )
        mm.eval( "assignShadings " + nClothMesh + " " + cloth_sim + " " + "{0.5,0.5,1}" )
        mm.eval( "addGroupAndLayer " + clothTransfrom + " " + cloth_sim + " "  + "1" )
        return nClothMesh

    def getClothMesh(self,transforms):
        childs = cmds.listRelatives( transforms,f=True )
        if type( childs ) is list :
            for c in childs :
                if not cmds.getAttr( '%s.intermediateObject' % c ):
                    return c

    def resetPNTS( self,transforms,*args ) :
        shape = self.getClothMesh( transforms )
        vtxNums = cmds.polyEvaluate( transforms,v=True )
        for i in range( cmds.polyEvaluate( transforms,v=True ) ):
            for x in ['x','y','z'] :
                cmds.setAttr( '%s.pnts[%d].pnt%s' % ( shape,i,x),0  )

    def connectNClothAttr(self,clothNode,nucleusNode,*args) :
        if not cmds.objExists( self.localTime ) :
            cmds.createNode( 'time',name=self.localTime )
            cmds.createNode( 'condition',name=self.conNode )
            cmds.connectAttr( '%s.outTime' % self.time,'%s.colorIfTrueR' % self.conNode )
            cmds.connectAttr( '%s.outTime' % self.localTime,'%s.colorIfFalseR' % self.conNode )

        sourceNucleu = cmds.connectionInfo( '%s.currentTime' % nucleusNode,sourceFromDestination=True )
        sourceNcloth = cmds.connectionInfo( '%s.currentTime' % clothNode,sourceFromDestination=True )

        if sourceNucleu.split( '.' )[0] == self.time :
            cmds.disconnectAttr(  '%s.outTime' % self.time,'%s.currentTime' % nucleusNode )
            cmds.connectAttr( '%s.outColorR' % self.conNode,'%s.currentTime' % nucleusNode )

        if sourceNcloth.split( '.' )[0] == self.time :

            cmds.disconnectAttr(  '%s.outTime' % self.time,'%s.currentTime' % clothNode )
            cmds.connectAttr( '%s.outColorR' % self.conNode,'%s.currentTime' % clothNode )
            # print '-' * 100

    def getClothNode(self,clothMeshShape) :
        if cmds.connectionInfo( '%s.inMesh' % clothMeshShape,isDestination=True ) :
            destinations = cmds.connectionInfo( '%s.inMesh' % clothMeshShape,sourceFromDestination =True )
            node = destinations.split('.')[0]
            if cmds.nodeType( node ) == 'nCloth' :
                return node

    def cacheAble( self,node,value,*args ) :
        cmds.setAttr( '%s.caat' % node,value )

    def createNclothCache( self,start,end,*args ) :
        return mm.eval( "doCreateNclothCache 4 { \"3\", \"%s\", \"%s\", \"OneFile\", \"1\"\
            , \"\",\"0\",\"\",\"0\", \"add\", \"0\", \"1\", \"1\",\"0\",\"1\" }" % (str(start),str(end)))

    def createCacheBySelect( self,transforms,*args ) :
        cacheNodes = self.getCacheNode( transforms )
        if cacheNodes is None :
            currentTime = cmds.playbackOptions( q=True,min=True )
            self.createNclothCache( currentTime-1,currentTime )

    def deleteCache(self,*args) :
        return mm.eval( "deleteCacheFile 3 { \"keep\", \"\", \"nCloth\" }" )

    def solver( self,*args ) :
        return mm.eval( "doAppendNclothCache 4 0 10 1 1")

    def solverSingleFrame(self,*args) :
        return mm.eval( "doAppendNclothCache 1 0 10 1 1;playButtonStepForward" )

    def saveLocalSimulation(self,*args) :
        return mm.eval( "doReplaceNclothCacheFrames 1 1 10 0 1 0 0 \"linear\" \"linear\" \"\" 1 1 1" )

    def truncateCache( self,start,end,*args ) :
        return mm.eval( "doDeleteNclothCacheFrames 2 %s %s \"\" 1" % ( str(start),str(end) ) )
        #( str( cmds.currentTime(q=True)+1 ),str( cmds.playbackOptions( q=True,max=True ) ) ) )

    def newSolver( self,transforms,*args ) :
        clothMesh = self.getClothMesh(transforms)
        clothNode = self.getClothNode(clothMesh)
        self.connectNClothAttr( clothNode,self.nucleus )
        endTime_cache = self.cacheSourceEndTime( transforms )
        cmds.currentTime( endTime_cache )
        maxTime = cmds.playbackOptions( q=True,max=True )
        cmds.progressWindow( t='Simulation',pr=0,st='Simulation : 0%',ii=True )
        for i in range( maxTime - endTime_cache ) :
            if not cmds.progressWindow( q=True,ii=True ) :
                break
            if cmds.progressWindow( query=True, ic=True ) :
                break
            mm.eval( "playButtonStepForward" )
            self.saveLocalSimulation()
            cmds.progressWindow( edit=True, pr=i, status=('Simulation : ' + `i` + '%' ) )
            cmds.refresh()
        self.stopLocalSimulation()

    def goSolver( self,transforms,*args ) :
        clothMesh = self.getClothMesh(transforms)
        clothNode = self.getClothNode(clothMesh)
        self.connectNClothAttr( clothNode,self.nucleus )
        cmds.select( transforms )
        self.solver()

    def stopLocalSimulation(self,*args):
        cmds.progressWindow( ep=True )

    def getCacheNode( self, transforms,*args ) :
        nodes = cmds.listHistory( transforms )
        for node in nodes :
            if cmds.nodeType( node ) == 'cacheFile':
                return node
    def cacheSourceEndTime( self,transforms,*args ) :
        nodes = self.getCacheNode( transforms )
        return cmds.getAttr( '%s.sourceEnd' % nodes )

    def toCacheSourceEndTime( self,transforms,*args ) :
        endTime = self.cacheSourceEndTime( transforms )
        cmds.currentTime( endTime )

    def localSimulation(self,transforms,*args):
        amount,localTime = 0,0
        self.truncateCache( cmds.currentTime(q=True),cmds.playbackOptions( q=True,max=True ) )
        current_time1 = cmds.getAttr( '%s.outTime' % self.time )
        cmds.setAttr( '%s.outTime' % self.localTime,current_time1 )
        cmds.setAttr( '%s.firstTerm' % self.conNode,1 )
        # progress windows |||||||||||||||||||
        cmds.progressWindow( t='Local Simulation',pr=0,st='Local Simulation : 0%',ii=True )
        while True :
        # for i in range( 10 ) :
            if not cmds.progressWindow( q=True,ii=True ) :
                break
            if cmds.progressWindow( q=True, ic=True ) :
                break
            localTime += 0.1
            amount += 1
            cmds.setAttr( '%s.outTime' % self.localTime,current_time1 + localTime );cmds.refresh()
            cmds.progressWindow( edit=True, pr=amount, status=('Local Simulation : ' + `amount` + '%' ) )
            if amount > 100 :
                amount = 0
        cmds.refresh()
        self.stopLocalSimulation()
        self.saveLocalSimulation()
        cmds.setAttr( '%s.firstTerm' % self.conNode,0 )

class Control( NCloth ) :

    def __init__(self):
        self.winname = 'nCloth_controlWin'
        self.layname_main = 'nCloth_controlMainLayout'
        self.layname_shelf = 'nCloth_controlShelfLayout'
        # self.layName_tmpMain = 'nCloth_controlMainLayout_tmp'
        self.title = 'nCloth Tools'
        self.nCloth = NCloth()

    def evalCmds(self,witch,*args) :
        selected = cmds.ls(sl=True)
        if not len( selected ) :
            print "\nYou need select a cloth mesh.",
            return
        transforms = selected[0]

        cacheNodes = self.getCacheNode( transforms )

        if witch == 'goSolver' :
            self.nCloth.createCacheBySelect( transforms );cmds.refresh()
            self.nCloth.goSolver( transforms )
        elif witch == 'crateNcloth' :
            nclothMesh = self.nCloth.createNcloth( transforms )
            cmds.setAttr( "%s.startFrame" % self.nCloth.nucleus,cmds.playbackOptions( q=True,min=True ) )
            cmds.select( nclothMesh )
            self.nCloth.createCacheBySelect( nclothMesh );cmds.refresh()

            self.nCloth.connectNClothAttr( self.nCloth.getClothNode( self.nCloth.getClothMesh(nclothMesh) ),self.nCloth.nucleus )

            return
        else:
            pass

        if cacheNodes is None :
            print "\n Not find cache on mesh.",
            return

        if witch == 'newSolver' :
            self.nCloth.createCacheBySelect( transforms );cmds.refresh()
            cacheEndTime = cmds.getAttr( "%s.sourceEnd" % cacheNodes )
            if float(cacheEndTime) < float(cmds.playbackOptions( q=True,max=True ) ):
                self.bls_newSimulation( transforms )
            else:
                self.bls_playButtonForward( transforms )
            # ---------------
            print cacheEndTime,cmds.playbackOptions( q=True,max=True )

        elif witch == 'saveLocalSimulation' :
            self.nCloth.saveLocalSimulation()
        elif witch == 'resetPNTS' :
            self.nCloth.resetPNTS( transforms )
        # resetPNTS
        elif witch == 'truncateCache' :
            self.nCloth.truncateCache(cmds.currentTime(q=True)+1 ,cmds.playbackOptions( q=True,max=True ) )
        elif witch == 'bls_localSimulation' :
            self.bls_localSimulation( transforms )
        elif witch == 'toCacheSourceEndTime' :
            self.nCloth.toCacheSourceEndTime( transforms )
        elif witch == 'openFoldersByCache' :
            fullDir = cmds.getAttr( "%s.cachePath" % cacheNodes )
            eval( "os.system(\"explorer %s\")" % fullDir.replace('/','\\\\') )
        else:
            pass

        print '\nSuccess .',

    def win(self):
        if cmds.window(self.winname,q=True,ex=True) :
            cmds.deleteUI(self.winname)
        if cmds.layout( self.layname_main,q=True,ex=True ) :
            cmds.deleteUI( self.layname_main )

        cmds.window(self.winname,title=self.title)
        # cmds.columnLayout( self.layname_main, adj=True )
        cmds.shelfLayout( self.layname_shelf )
        self.buttonGrps( self.layname_shelf )
        self.buttonGrpSet( self.layname_shelf )
        cmds.showWindow(self.winname)

    def buttonGrps(self,parents,*args) :
        # crateNcloth

        cmds.button( label='Create nCloth',w=100,parent = parents # ,style='textOnly'
            ,ebg=True,bgc=(.35,.35,.35)
            , c=partial( self.evalCmds,'crateNcloth' ) )

        cmds.button( label='Simulation',w=100,parent = parents # ,style='textOnly'
            ,ebg=True,bgc=(.35,.35,.35)
            , c=partial( self.evalCmds,'goSolver' ) )


        self.localSim_but = cmds.button(label='Local Simulation',w=100,parent = parents # ,style='textOnly'
                ,ebg=True,bgc=(.35,.35,.35)
                ,c=partial( self.evalCmds,'bls_localSimulation' ) )

        # solverSingleFrame
        cmds.button(label='Truncate Cache',w=100,parent = parents # ,style='textOnly'
            ,ebg=True,bgc=(.35,.35,.35)
            ,c=partial( self.evalCmds,'truncateCache' ) )

        cmds.button(label='UpData Tweaks',w=100,parent = parents #,style='textOnly'
            ,ebg=True,bgc=(.35,.35,.35)
            ,c=partial( self.evalCmds,'saveLocalSimulation' ))

        cmds.button(label='Reset Mesh',w=100,parent = parents #,style='textOnly'
            ,ebg=True,bgc=(.35,.35,.35)
            ,c=partial( self.evalCmds,'resetPNTS' ))

        cmds.button(label='Open Folder',w=100,parent = parents #,style='textOnly'
            ,ebg=True,bgc=(.35,.35,.35)
            ,c=partial( self.evalCmds,'openFoldersByCache' ))

        # ---------------------------
        cmds.button(label=' |<< ',w=50,parent = parents # ,style='textOnly'
            ,ebg=True,bgc=(.35,.5,.35)
            ,c= partial( self.playControl,'|<<' ) )

        cmds.button(label=' |< ',w=50,parent = parents # ,style='textOnly'
            ,ebg=True,bgc=(.35,.5,.35)
            ,c= partial( self.playControl,'|<' ) )

        #self.playButStep_but = cmds.button(label=' > ',w=100,parent = parents # ,style='textOnly'
        #    ,ebg=True,bgc=(.35,.5,.35)
        #    ,c=partial( self.bls_playButtonForward ) )

        self.newSim_but = cmds.button( label='>',w=100,parent = parents # ,style='textOnly'
            ,ebg=True,bgc=(.35,.5,.35)
            , c=partial( self.evalCmds,'newSolver' ) )

        cmds.button(label=' >| ',w=50,parent = parents # ,style='textOnly'
            ,ebg=True,bgc=(.35,.5,.35)
            ,c= partial( self.playControl,'>|' ) )

        cmds.button(label=' >>| ',w=50,parent = parents # ,style='textOnly'
            ,ebg=True,bgc=(.35,.5,.35)
            ,c= partial( self.playControl,'>>|' ) )

        cmds.button(label=' >||| ',w=50,parent = parents # ,style='textOnly'
            ,ebg=True,bgc=(.35,.5,.35)
            ,c=partial(self.evalCmds,'toCacheSourceEndTime' ))

    def playControl(self,witch,*args) :
        if witch == '|<<' :
            mm.eval( 'playButtonStart' )
        elif witch == '|<' :
            mm.eval( 'playButtonStepBackward' )
        elif witch == '>|' :
            mm.eval( 'playButtonStepForward' )
            self.nCloth.saveLocalSimulation()
        elif witch == '>>|' :
            mm.eval( 'playButtonEnd' )
        else:
            pass

    def buttonGrpSet(self,parents,*args) :
        cmds.button(label='\xa1\xe2',w=22,parent = parents ,ebg=True,bgc=(.75,.5,.5)
            ,c=partial(self.buttonGrpSet_cmds ))

    def tmpLayout(self,getModelParent,*args) :
        return cmds.columnLayout( w=300,h=34,adj=True,parent=getModelParent )

    def deleteLayout(self,layoutName,*args) :
        cmds.deleteUI( layoutName );self.win()

    def buttonGrpSet_cmds(self,*args) :
        getModel = cmds.getPanel( withFocus=True )
        getModelParent = cmds.layout( getModel,q=True,parent=True )
        # create tmp layout attach on main windows
        cmds.columnLayout( self.layname_main,h=40,adj=True,parent=getModelParent )
        cmds.shelfLayout( self.layname_shelf,h=38,parent= self.layname_main )
        self.buttonGrps( self.layname_shelf )
        if cmds.window( self.winname,q=True,ex=True ) :
            cmds.deleteUI( self.winname )
        print getModel,self.layname_main

        self.buttonGrp_options()

    def buttonGrp_options(self,*args) :
        cmds.rowLayout( w = 40,numberOfColumns=2,columnWidth2=(15,15),columnAlign=[1,'right']
                ,columnAttach=[1,'both',0],parent= self.layname_shelf  )
        cmds.button(label='\xa1\xe1',h=30,ebg=True,bgc=(.75,.5,.5)
            ,c=partial(self.deleteLayout,self.layname_main ) )
        cmds.columnLayout( )
        cmds.button( label = '\xa1\xf8',h=15,w=15,command=partial( self.butOptionCmds,5 ) )
        cmds.button( label = '\xa8\x8b',h=15,w=15,command=partial( self.butOptionCmds,-5 ) )

    def butOptionCmds(self,values=5,*args):
        hight = cmds.columnLayout( self.layname_main,q=True,h=True)
        cmds.columnLayout( self.layname_main,e=True,h=hight+values)
        cmds.shelfLayout( self.layname_shelf,e=True,h=hight+values )

    '''
    def bls_playButtonForward(self,*args) :
        if cmds.button( self.playButStep_but,q=True,label=True ) == ' > ' :
            cmds.button( self.playButStep_but,e=True,label = '||',bgc=(0,1,0) )
            mm.eval("playButtonForward")
        else:
            cmds.button( self.playButStep_but,e=True,label = ' > ',bgc=(.35,.5,.35) )
            mm.eval("playButtonForward")
    '''

    def bls_localSimulation(self,transforms,*args) :
        if cmds.button( self.localSim_but,q=True,label=True ) == 'Local Simulation' :
            cmds.button( self.localSim_but,e=True,label='Stop Local Simulation',bgc=(0,1,0) )
            self.nCloth.localSimulation( transforms )
            cmds.button( self.localSim_but,e=True,bgc=(.35,.35,.35) )
        else:
            cmds.button( self.localSim_but,e=True,label='Local Simulation' )
            self.nCloth.stopLocalSimulation()

    def bls_newSimulation(self,transforms,*args) :
        if cmds.button( self.newSim_but,q=True,label=True ) == '>' :
            cmds.button( self.newSim_but,e=True,label='Stop Simulation',bgc=(0,1,0) )
            self.nCloth.newSolver( transforms )
            cmds.button( self.newSim_but,e=True,bgc=(.35,.5,.35),label='>' )
        else:
            cmds.button( self.newSim_but,e=True,label='>',ebg=True,bgc=(.35,.5,.35) )
            self.nCloth.stopLocalSimulation()

    def bls_playButtonForward(self,transforms,*args) :
        if cmds.button( self.newSim_but,q=True,label=True ) == '>' :
            cmds.button( self.newSim_but,e=True,label = '||',bgc=(0,1,0) )
            mm.eval("playButtonForward")
        else:
            cmds.button( self.newSim_but,e=True,label = '>',bgc=(.35,.5,.35) )
            mm.eval("playButtonForward")

    def dockWindow(self) :
        cmds.dockControl( area='bottom', content=self.winname,label = 'nCloth Tools' )

if __name__ == '__main__' :
    ctl = Control()
    ctl.win()
