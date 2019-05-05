import maya.cmds as cmds

def renameList( objects,bName ) :
    for i in range( len(objects) ) :
        rename( objects[i],(bName + str(i+1)) )

def renameTuple( objects,bName ) :
    objLen = len(objects)
    lenShape = 0
    for i in range( objLen ) :
        listLen = len( objects[i] )
        renameList( objects[i],(bName + str(i+1)) )

def renameDict( objects,bName ) :
    for key in objects.keys() :
        for i in range( len(objects[key]) ) :
            rename( objects[key][i],(bName + key + str(i+1)) )

def renameDict1( objects,bName ) :
    for key in objects.keys() :
        rename( objects[key],(bName + key) )

def rename( object,bName ) :
    suffix = ''
    if cmds.nodeType(object) == 'transform' :
        shapes = cmds.listRelatives( object ,s=True,path=True )
        shape = ''
        try :
            lenShape = len(shapes)
            shape = shapes[0]
        except :
            lenShape = 0
        if lenShape > 0 :
            cnodeType = cmds.nodeType( shape )
            if cnodeType == 'nurbsCurve' :
                suffix = 'crv'
            if cnodeType == 'locator' :
                suffix = 'loc'
            if cnodeType == 'mesh' :
                suffix = 'mesh'
            if cnodeType == 'nurbsSurface' :
                suffix = 'nurbs'
            if cnodeType == 'hairSystem' :
                suffix = 'hsys'
            if cnodeType == 'follicle' :
                suffix = 'foll'
        else :
            suffix = 'grp'
            
    elif cmds.nodeType(object) == 'joint' :
        suffix = 'jnt' 
    elif cmds.nodeType(object) == 'ikHandle' :
        suffix = 'ikh' 
    elif cmds.nodeType(object) == 'ikEffector' :
        suffix = 'ikEff'
    elif cmds.nodeType(object) == 'condition' :
        suffix = 'cnd'
    # condition
    else :
        suffix = findUpper( cmds.nodeType(object) )
        
    cmds.rename( (object),( bName + '_' + suffix) )

'''
zhe ge ming ling yong yu ti qu string zhong de upper
examples :
    >>>findUpper("aBCdEfghI")
        'ABCEI'
'''
def findUpper( a ) :
    result = ''
    c = [ list(a)[i] for i in range( len(list(a)) ) if list(a)[i].isupper()]
    result = list(a)[0].upper()
    for i in range( len(c) ):
        result += c[i]
        result = result.lower()
    return(result)

# ZHE GE MING LING YONG YU KUAI SU RENAME CAO ZUO
# 1. KE YONG YU RENAME YI GE WU TI
# 2. USER RENAME A LIST
# 3. USER RENAME A DICT
