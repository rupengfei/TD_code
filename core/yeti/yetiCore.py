# -*- coding:utf-8 -*-  
# ==========================================
#       author: Pengfei.Ru
#         mail: a773849069@gmail.com
#         time: 2019/1/14
# ==========================================
import maya.cmds as mc
# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*
def get_graph_node_attribute(yetiNode, node, param):
    return mc.pgYetiGraph(yetiNode, n=node, p=param, getParamValue=True)

def get_graph_TypeNode(yetiNode, type1):
    return mc.pgYetiGraph(yetiNode, ls=1, typ=type1)

def get_sel_graph():
    return mc.ls(sl=1, dag=1, type='pgYetiMaya')

def get_all_graph():
    return mc.ls(type='pgYetiMaya')

def list_graph_node_param(yetiNode, node):
    return mc.pgYetiGraph(yetiNode, n=node, lsp=True)

def list_graph_node(yeti_graph):
    return mc.pgYetiGraph(yeti_graph, listNodes=True)

def replace_all_texture_node_path(rep1, rep2):
    for graph_node in get_sel_graph():
        for node in get_graph_TypeNode(graph_node, "texture"):
            file_names = get_graph_node_attribute(graph_node, node, "file_name")
            file_names = file_names.replace(rep1, rep2)
            set_string_pram(graph_node, node, "file_name", file_names)

def set_string_pram(yetiNode, node, param, value):
    mc.pgYetiGraph(yetiNode, n=node, p=param, setParamValueString=value)

