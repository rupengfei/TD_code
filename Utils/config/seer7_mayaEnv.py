# -*- coding:utf-8 -*-
# ==========================================
#       author: Pengfei.Ru
#         mail: a773849069@gmail.com
#         time: 2018/11/30
# ==========================================
import Utils.yaml
import subprocess
import os
# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*
file_name = __file__[:__file__.rfind(".")] + ".yaml"
# print file_name

def load_yaml_file(files=str()):
    with open(files, "r") as f:
        data = Utils.yaml.load(f)

    _env = os.environ.copy()
    for e in data["Env"]:
        if e["mode"] == "over":
            _env[e["name"]] = e["value"]

        elif e["mode"] == "pre":
            _env[e["name"]] = e["value"] + ";" + os.environ.get(e["name"], "")

        elif e["mode"] == "post":
            _env[e["name"]] = os.environ.get(e["name"] + ";" + e["value"])

        else:
            pass

    subprocess.Popen(data["Exec"], env=_env)


load_yaml_file(file_name)

