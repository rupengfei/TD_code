# -*- coding:utf-8 -*-  
# ==========================================
#       author: Pengfei.Ru
#         mail: 773849069@qq.com
#         QQ: 773849069
#         time: 2019/1/26
# ==========================================
from Utils import mayaTool, config
import json
import maya.cmds as mc
# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*


def import_fur_BS():
    with open(config.seer7_fur, "r") as f:
        data = json.load(f)
    for ia, ib in data.iteritems():  # 循环角色
        list1 = mc.ls(ib["geo_name"])
        list1.extend(mc.ls("*:" + ib["geo_name"]))
        if not list1:
            continue
        for num, geo_name in enumerate(list1):  # 循环重复角色
            fix = ("{%d}" % num) if num else ""
            name_space = mc.file(ib["fur_file_path"] + fix, query=True, namespace=True)
            # if name_space != "unknown":
            #     pass
            bs_a = geo_name
            bs_b = name_space + ":" + ib["fur_name"]
            if name_space == "unknown":
                name_space = mayaTool.reference_file(ib["fur_file_path"], name_space=ia, typ="ma", fix=True)
                bs_b = name_space + ":" + ib["fur_name"]
            elif not len(mc.listRelatives(bs_b, shapes=True)) == 1:
                continue
            # blendShape A 动 B 静
            mc.blendShape([bs_a, bs_b], before=True, w=[0, 1], origin="world")