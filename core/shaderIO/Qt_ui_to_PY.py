# -*- coding:utf-8 -*-
# ==========================================
#       author: Pengfei.Ru
#         mail: 773849069@qq.com
#         QQ: 773849069
#         time: 2018/12/3
# ==========================================
import pyside2uic
# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*


with open("shaderIO_batch.py", "w") as f:
    pyside2uic.compileUi("shaderIO.ui", f)
    print "ok"

