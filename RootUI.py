# -*- coding:utf-8 -*-  
# ==========================================
#       author: Pengfei.Ru
#         mail: a773849069@gmail.com
#         time: 2018/11/30
# ==========================================
import sys
import os
import maya.cmds as mc
import pymel.core as pm
import Utils.scriptTool as scriptTool
import scripts.shaderIO1 as shaderIO
# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*


reload(shaderIO)
shaderIO.shaderCore.get_all_sg_nodes()

