# -*- coding:utf-8 -*-
# ==========================================
#       author: Pengfei.Ru
#         mail: a773849069@gmail.com
#         time: 2018/12/8
# ==========================================
import json
import maya.cmds as mc
import os
# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*


def find_files(path, fix="json", take_fix=True):
    """递归找文件，深度搜索模式"""
    r_json = list()
    for cwd in os.listdir(path):
        names = os.path.join(path, cwd)
        if os.path.isdir(names):
            r_json.extend(find_files(names, take_fix))
        if os.path.splitext(names)[-1] == ("." + fix):
            if take_fix:
                r_json.append(cwd)
            else:
                r_json.append(os.path.splitext(names)[0])
    return r_json

def convert_ma_to_json(file_path):
    return file_path.split(".")[0] + ".json"

def readData(path):
    """
    import a file path, read data to return..
    """
    f = open(path, 'r')
    data = json.load(f)
    f.close()
    return data


def writeData(path, data):
    """
    give a file path and data, write data to file..
    Exp:
       writeData("D:/Temp.json", {"a":0, "b":1})
    """
    f = open(path, 'w')
    json.dump(data, f, indent=4)
    f.close()
