import maya.cmds as cmds

def cAddAttr( object,longName,attributeType,napS,makeAttribute ):
    ''' zge ming ling yong yu kuai su  tian jia shu xing  '''
    if not cmds.attributeQuery( longName,ex=True,node=object ) :
        nap = {}
        napList = napS.split(',')
        napLen = len( napList )
        keysx = ['min','max','dv']
        evalString = "cmds.addAttr(" + "'" + object + "'" + ",ln=" + "'" + longName + "'"
        evalString += ",at=" + "'" + attributeType + "'"
        if attributeType == 'enum' :
            if napLen > 1 :
                enumStr =''
                for i in range( len(napList) ) :
                    enumStr += napList[i] + ':'
                evalString += "," + "en=" + "'" + enumStr + "'"
        else :
            if napLen > 1 :
                for c in range( min(napLen,len(keysx)) ) :
                    if napList[c] != '' :
                        nap[keysx[c]] = napList[c]
                for i in range( len(nap) ) :
                    evalString += "," + nap.keys()[i] + "=" + str( nap.values()[i] )
        evalString += ")"
        exec( evalString )
        if makeAttribute == 'd' :
            pass
        else :
            cmds.setAttr( (object+'.'+longName),e=True,keyable=True)