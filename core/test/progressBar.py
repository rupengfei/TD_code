# -*- coding:utf-8 -*-
# ==========================================
#       author: Pengfei.Ru
#         mail: a773849069@gmail.com
#         time: 2018/12/8
# ==========================================


# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*
self.progressBar.setMaximum(len(polyGeometry))
for i, geo in enumerate(polyGeometry):
    self.progressBar.setValue(i)
    self.btn_replace.setText('%d%%' % mathTool.setRange(0, len(polyGeometry), 0, 100, i))

    realName = re.search('\w+$', geo).group()
    UVgeo = 'UV:%s' % realName
    if not mc.objExists(UVgeo):
        print '# Warning # There are no model in new file for %s...' % geo
        continue
    # -
    mc.transferAttributes(UVgeo, geo, pos=0, nml=0, uvs=2, col=0, spa=5, sus="map1", tus="map1", sm=0, fuv=0, clb=1)
    # -
    print '# Result # Copyed UV %s -> %s' % (UVgeo, geo)

    # - delete history
    RemoveUVWasteNode.delUVTransferAttributesNode(geo)

self.progressBar.setMaximum(1)
self.progressBar.setValue(0)

