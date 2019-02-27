# -*- coding=utf-8 -*-
# ==========================================
#       author: Pengfei.Ru
#         mail: a773849069@gmail.com
#         time: 2018/11/3
# ==========================================
import maya.cmds as mc


# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*


class Attr_code():
    def __init__(self):
        self.win_name = "Attr Tool"
        self.obj_name = "batch_attr_tool"

        if mc.window(self.obj_name, exists=1):
            mc.deleteUI(self.obj_name)

        mc.window(self.obj_name, title=self.win_name, w=400, h=100, sizeable=1)
        self.a_layout = mc.columnLayout(adjustableColumn=True)
        self.frame_subdiv = mc.frameLayout(l="Arnold_Subdivision", cl=1, cll=1, p=self.a_layout)
        mc.rowColumnLayout(w=400, nc=3, p=self.frame_subdiv)
        mc.button(label="none", w=133, h=30, c=lambda x: self.aiSetSubd(0))
        mc.button(label="catclark", w=133, h=30, c=lambda x: self.aiSetSubd(1))
        mc.button(label="linear", w=134, h=30, c=lambda x: self.aiSetSubd(2))
        mc.rowColumnLayout(w=100, nc=4, p=self.frame_subdiv)
        mc.button(label="1", w=100, h=30, c=lambda x: self.aiSetIter(1))
        mc.button(label="2", w=100, h=30, c=lambda x: self.aiSetIter(2))
        mc.button(label="3", w=100, h=30, c=lambda x: self.aiSetIter(3))
        mc.button(label="4", w=100, h=30, c=lambda x: self.aiSetIter(4))
        mc.rowColumnLayout(w=400, nc=1, p=self.frame_subdiv)
        mc.button(label="Turn off subdividing objects", w=400, h=30, c=self.aiobjSmoothOff)

        self.frame_other = mc.frameLayout(l="All Attr find and set", cll=1, p=self.a_layout)
        self.findAttrName_layout = mc.rowColumnLayout(w=400, nc=3, parent=self.frame_other)
        mc.columnLayout(w=100, parent=self.findAttrName_layout)
        self.find_obj_name = mc.textScrollList(w=100, ams=0)
        mc.columnLayout(w=100, parent=self.findAttrName_layout)
        mc.button(label="Add Objects", w=100, h=30, c=self.get_obj_name)
        self.findAttrName_name = mc.textField(w=100, h=35, text='Find Attribute', tcc=self.find_list_Attr)
        mc.text(w=100, h=5, l="")
        mc.text(w=100, h=30, l="This attr type is")
        self.set_attr_Types = mc.text(w=100, bgc=[0, 0, 0], h=25, l="NoneType")
        self.findAttrName_set = mc.textField(w=100, h=35, text='value')
        mc.button(label="Set Attr", w=100, h=30, c=self.set_AttrButton)
        mc.columnLayout(w=200, parent=self.findAttrName_layout)
        self.find_attr_name = mc.textScrollList(w=200, ams=0, sc=self.set_attr_type)

        mc.showWindow(self.obj_name)

    def find_list_Attr(self, *args, **kwargs):
        # 查找属性
        mc.textScrollList(self.find_attr_name, w=200, e=1, ra=1)
        find_obj_name1 = mc.textScrollList(self.find_obj_name, q=1, ai=1)
        findAttrName_name1 = mc.textField(self.findAttrName_name, q=1, text=1)
        if str(type(find_obj_name1))[7:-2] == 'NoneType':
            # 如果物体为空，get attr 查询
            # 如果属性是空 or Attribute_Name 则打印"请添加物体或属性"
            try:
                objAttrs = mc.listAttr(findAttrName_name1)
                mc.textScrollList(self.find_attr_name, w=200, e=1, a=objAttrs, )
            except:
                pass

        else:
            objAttrs = mc.listAttr(find_obj_name1[0])
            if findAttrName_name1 == "" or findAttrName_name1 == "Attribute_Name":
                mc.textScrollList(self.find_attr_name, w=200, e=1, a=objAttrs, )
            else:
                attrName = []
                for i in objAttrs:
                    if i.upper().find(findAttrName_name1.upper()) != -1:
                        attrName.append(i)
                mc.textScrollList(self.find_attr_name, w=200, e=1, a=attrName, )

    def set_attr_type(self, *args, **kwargs):
        print mc.textScrollList(self.find_attr_name, q=1, si=1)
        # 设置属性类型
        obj_name = mc.textScrollList(self.find_obj_name, q=1, si=1)
        my_attr_find = mc.textField(self.findAttrName_name, q=1, text=1)
        attr_name = mc.textScrollList(self.find_attr_name, q=1, si=1)

        if str(type(obj_name))[7:-2] == 'NoneType':
            my_type = my_attr_find + "." + attr_name[0]
        else:
            my_type = obj_name[0] + "." + attr_name[0]

        try:
            getattr_names = mc.getAttr(my_type)
            strname = type(getattr_names)
        except:
            strname = "<type 'string'>"

        strname = str(strname)[7:-2]
        if strname == 'list':
            if len(getattr_names[0]) == 0:
                strname = "NoneType"

            if len(getattr_names[0]) == 1:
                strname = "float"

            if len(getattr_names[0]) == 2:
                strname = "float2"

            if len(getattr_names[0]) == 3:
                strname = "float3"

        elif strname == "unicode":
            strname = "string"

        mc.text(self.set_attr_Types, e=1, l=strname)

    def get_obj_name(self, *args, **kwargs):
        # 添加物体
        mc.textScrollList(self.find_obj_name, e=1, ra=1)
        sels = mc.ls(sl=1)
        if sels:
            mc.textScrollList(self.find_obj_name, e=1, sii=1, a=sels)
        else:
            mc.warning("Please select objects")

    def set_AttrButton(self, *args, **kwargs):
        # 设置属性
        my_obj_list = mc.textScrollList(self.find_obj_name, q=1, ai=1)
        my_attr_find = mc.textField(self.findAttrName_name, q=1, text=1)
        my_atrr_type = mc.text(self.set_attr_Types, q=1, l=1)
        my_attr_value = mc.textField(self.findAttrName_set, q=1, text=1)
        my_attr_name = mc.textScrollList(self.find_attr_name, q=1, si=1)

        if my_atrr_type == 'int':
            try:
                my_attr_value = int(my_attr_value)
            except:
                mc.warning("value is not %s type" % (my_atrr_type))
                return

        elif my_atrr_type == 'float':
            try:
                my_attr_value = float(my_attr_value)
            except:
                mc.warning("value is not %s type" % (my_atrr_type))
                return
        elif my_atrr_type == 'float3' or my_atrr_type == 'double3':
            try:
                my_attr_value = my_attr_value.split(",")
                if len(my_attr_value) == 1:
                    my_attr_value = float(my_attr_value[0]), float(my_attr_value[0]), float(my_attr_value[0])

                elif len(my_attr_value) == 2:
                    mc.warning("value is not %s type" % (my_atrr_type))
                    return
                elif len(my_attr_value) == 3:
                    my_attr_value = float(my_attr_value[0]), float(my_attr_value[1]), float(my_attr_value[2])
            except:
                mc.warning("value is not %s type" % (my_atrr_type))
                return
        elif my_atrr_type == 'bool':
            if my_attr_value == "0":
                my_attr_value = 0
            else:
                my_attr_value = 1

        # 没有属性的加到变量
        no_attr = []

        # if 如果有选物体
        if str(type(my_obj_list))[7:-2] != 'NoneType':
            for i in my_obj_list:
                # 循环物体
                attrname = i + "." + my_attr_name[0]
                # 物体名加属性
                try:
                    if my_atrr_type == "string":
                        mc.setAttr(attrname, my_attr_value, type=my_atrr_type)
                    elif my_atrr_type == "double3" or my_atrr_type == "float2" or my_atrr_type == "float3":
                        if len(my_attr_value) == 2:
                            mc.setAttr(attrname, my_attr_value[0], my_attr_value[1], type=my_atrr_type)
                        elif len(my_attr_value) == 3:
                            mc.setAttr(attrname, my_attr_value[0], my_attr_value[1], my_attr_value[2],
                                       type=my_atrr_type)
                    else:
                        mc.setAttr(attrname, my_attr_value)
                        # setAttr  属性   属性类型   属性值
                except:
                    no_attr.append(attrname)
        else:
            # 没有物体
            attrname = my_attr_find + "." + my_attr_name[0]
            # 存在属性   属性 + 属性名
            if my_atrr_type == "string" or my_atrr_type == "double3" or my_atrr_type == "float2" or my_atrr_type == "float3":
                mc.setAttr(attrname, my_attr_value, type=my_atrr_type)
            else:
                mc.setAttr(attrname, my_attr_value)
                # setAttr 属性名 属性类型   属性值
        if no_attr:
            mc.warning("These properties were not found", no_attr)
        else:
            mc.warning("set ok")

    def aiSetSubd(self, *args, **kwargs):
        mc.pickWalk(d="down")
        sel = mc.ls(sl=1, long=1)
        for i in sel:
            mc.setAttr(i + '.aiSubdivType', args[0])

    def aiSetIter(self, *args, **kwargs):
        mc.pickWalk(d="down")
        sel = mc.ls(sl=1, long=1)
        for i in sel:
            mc.setAttr(i + '.aiSubdivIterations', args[0])

    def aiobjSmoothOff(self, *args, **kwargs):
        mc.pickWalk(d="down")
        sel = mc.ls(sl=1, long=1)
        for i in sel:
            mc.setAttr(i + ".displaySmoothMesh", 0)


if __name__ == "__main__":
    tool = Attr_code()

