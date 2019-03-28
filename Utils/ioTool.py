# -*- coding:utf-8 -*-
# ==========================================
#       author: Pengfei.Ru
#         mail: 773849069@qq.com
#         QQ: 773849069
#         time: 2018/12/8
# ==========================================
import json
import os
# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*


def find_files(path, fix=str(), take_fix=True, take_path=True):
    """
    递归找文件，深度搜索模式
    参数
        fix        str
        take_fix   True False
        take_path  True False
    Returns: All
    """
    finds = list()
    for dir_name in os.listdir(path):
        names = os.path.join(path, dir_name)
        if os.path.isdir(names):
            # print names
            finds.extend(find_files(names, fix=fix, take_fix=take_fix, take_path=take_path))
        if os.path.splitext(names)[-1] == ("." + fix):
            if take_path:
                if take_fix:
                    finds.append(names)
                else:
                    finds.append(os.path.splitext(names)[0])
            else:
                if take_fix:
                    finds.append(dir_name)
                else:
                    finds.append(os.path.splitext(dir_name)[0])
    return finds

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

def user_log(data=""):
    user_logs = os.path.expanduser('~') + "/user_log.log"
    if not os.path.exists(user_logs):
        with open(user_logs, "w"):
            pass
    with open(user_logs, "a") as f:
        f.write(data)

def writeData(path, data):
    """
    give a file path and data, write data to file..
    Exp:
       writeData("D:/Temp.json", {"a":0, "b":1})
    """
    f = open(path, 'w')
    json.dump(data, f, indent=4)
    f.close()
