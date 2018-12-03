How To Use
==
```python
import sys

path = 'D:/___________TD____________/TD_Code'
path in sys.path or sys.path.append(path)

import scripts.shaderIO1 as shaderIO
reload(shaderIO)
```
import sys

path = 'D:/___________TD____________/TD_Code'
path in sys.path or sys.path.append(path)

import scripts.shaderIO1.shaderCore as shaderCore

dir(shaderCore)



reload(shaderCore)
shaderCore.export_sel_sg_members("D:/Repo/test_export_sg_nodes.json")






shaderCore.get_sel_sg_nodes()

members = mc.sets("atieda_shenti_allSG", q=True) or list() 











