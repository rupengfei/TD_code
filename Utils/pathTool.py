# -*- coding:utf-8 -*-  
# ==========================================
#       author: Pengfei.Ru
#         mail: a773849069@gmail.com
#         time: 2018/12/6
# ==========================================
import os
import maya.cmds as mc
# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*



def recombine_path(path="", find_str=None, append_str=None):
    """

    Args:
        path: r"D:\Repo\seer7\cacheIO\Chars\atieda\Rig"
        find_str: atieda
        append_str: shader

    Returns: r"D:/Repo/seer7/cacheIO/Chars/shader

    """
    if path:
        path = path.replace("\\", "/")
        if find_str:
            path = path[:path.rfind(find_str)]
            if append_str:
                return path + append_str
            else:
                return path
        else:
            return path
    return False


def get_start_dir(start_dir):
    if os.path.isfile(start_dir):
        start_dir = os.path.dirname(start_dir)

    elif os.path.isdir(start_dir):
        pass

    else:
        start_dir = mc.workspace(q=True, lfw=True)[0]

    return start_dir


def get_output_path(filter_format='Maya ASCII (*.ma)', start_dir=None):
    """
    """
    start_dir = get_start_dir(start_dir)
    filePath = mc.fileDialog2(ff=filter_format, startingDirectory=start_dir)
    return filePath


def get_input_path(filter_format='Maya ASCII (*.ma)', start_dir=None):
    """
    """
    start_dir = get_start_dir(start_dir)
    filePath = mc.fileDialog2(ff=filter_format, fm=4, okc='Select', startingDirectory=start_dir)
    return filePath


if __name__ == '__main__':
    print recombine_path()
