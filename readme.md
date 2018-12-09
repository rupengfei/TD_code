How To Use
==
```python
import sys

path = 'D:/___________TD____________/TD_Code'

path in sys.path or sys.path.append(path)
    
import RootUI
reload(RootUI)
```

import pymel.core as pm
import maya.cmds as mc
import sys

path = 'D:/___________TD____________/TD_Code'
path in sys.path or sys.path.append(path)

import seer7_setup
reload(seer7_setup)
seer7 = seer7_setup.Setup()
seer7.show_win()


def zhixing():
    reload(seer7_setup)
    seer7 = seer7_setup.Setup()
    seer7.show_win()




mc.window()
mc.columnLayout()
mc.button(c=lambda a: zhixing(),w=150,h=150,bgc = [0.4,0.4,1])
mc.showWindow()