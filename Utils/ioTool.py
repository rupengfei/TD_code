# -*- coding:utf-8 -*-
# ==========================================
#       author: Pengfei.Ru
#         mail: a773849069@gmail.com
#         time: 2018/12/8
# ==========================================
import json


# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*

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
