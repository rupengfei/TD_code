# -*- coding:utf-8 -*-
# ==========================================
#       author: Pengfei.Ru
#         mail: a773849069@gmail.com
#         time: 2018/12/9
# ==========================================
import json
from Utils import scriptTool, ioTool
import os


# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*
seer7_json = os.path.join(scriptTool.getScriptPath(), "config_seer7.json")
def setData(data=None):
    """
    data = {
            "shader_source_path": "D:/Repo/seer7/cacheIO/Chars/Rig",
            "cacheIO_an" : "D:/Repo/seer7/cacheIO/Animation"
        }
    """
    if not data:
        data = {
            "shader_source_path": "D:/Repo/seer7/cacheIO/Chars/Rig",
            "cacheIO_an": "D:/Repo/seer7/cacheIO/Animation"

        }
        ioTool.writeData(seer7_json, data)
    return True

def readData():
    data = ioTool.readData(seer7_json)
    return data

def rig_to_shader(rig_path="D:/Repo/seer7/cacheIO/Chars/Rig"):
    """
    D:/Repo/seer7/cacheIO/Chars/shader
    """
    data = rig_path.split("Rig")
    return os.path.join(data[0], "shader")
    # print data


def split_cam(cam="Sc003_054_001_035_cam"):
    """
    ('Sc003', '054', 'Sc003_054', '001', '035')
    """
    data = cam.split("_")
    scene = data[0]
    shot = data[1]
    shot_name = "{0}_{1}".format(scene, shot)
    start_frame = data[2]
    end_frame = data[3]
    return scene, shot,shot_name, start_frame, end_frame


def an_makedir(an_path="D:/Repo/seer7/cacheIO/Animation", scene="sc003", shot_name="sc003_054"):
    """
    D:/Repo/seer7/cacheIO/Animation\sc003\sc003_054
    """
    an_path = os.path.join(an_path, scene, shot_name)
    return an_path


if __name__ == '__main__':
    print rig_to_shader()
    print split_cam()
    print an_makedir()
