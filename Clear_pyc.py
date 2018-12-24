# -*- coding:utf-8 -*-  
# ==========================================
#       author: Pengfei.Ru
#         mail: a773849069@gmail.com
#         time: 2018/12/24
# ==========================================
import os
# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*
on_path = __file__[:__file__.rfind("/")]

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

def main():
    files = find_files(on_path, "pyc", False) or list()
    for f in files:
        os.remove(f)

main()