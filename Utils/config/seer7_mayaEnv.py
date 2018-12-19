# -*- coding:utf-8 -*-
# ==========================================
#       author: Pengfei.Ru
#         mail: a773849069@gmail.com
#         time: 2018/11/30
# ==========================================
import subprocess
import os
import sys
# path = 'D:/___________TD____________/TD_Code'
# path in sys.path or sys.path.append(path)
path = 'Z:/SEER7/bin/rupengfei/TD_code'
path in sys.path or sys.path.append(path)
from Utils import yaml
# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*
yaml_name = __file__[:__file__.rfind(".")] + ".yaml"
mel_name = __file__[:__file__.rfind(".")] + ".mel"
# print file_name

def load_yaml_file(files=str(), mels=str()):
    with open(files, "r") as f:
        data = yaml.load(f)

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
    to_open = data["Exec"] + ' -script "' + mels + '"'
    # -script "Z:/SEER7/bin/rupengfei/TD_code/seer7_start.mel"
    # print to_open
    subprocess.Popen(to_open, env=_env)


load_yaml_file(yaml_name, mel_name)

