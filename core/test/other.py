# -*- coding:utf-8 -*-
# ==========================================
#       author: Pengfei.Ru
#         mail: a773849069@gmail.com
#         time: 2018/12/8
# ==========================================


# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*
import pymel.core as pm
import maya.cmds as mc
import sys

path = 'C:/Users/rpf/Downloads/RiggingTeamTools'
path in sys.path or sys.path.append(path)
path = "C:/Python27/Lib/site-packages"
path in sys.path or sys.path.append(path)
import RootUI



import pymel.core as pm
import maya.cmds as mc
import sys

path = 'D:/___________TD____________/TD_Code'
path in sys.path or sys.path.append(path)

import core.shaderIO.shaderIO_batchUI as shaderIOUI


reload(shaderIOUI)
sd = shaderIOUI.ShaderIO()
sd.show_win()




