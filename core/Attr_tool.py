# -*- coding=utf-8 -*-
# ==========================================
#       author: Pengfei.Ru
#         mail: 773849069@qq.com
#         QQ: 773849069
#         time: 2018/11/3
# ==========================================
import maya.cmds as mc


# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*


class AttrTool:
    def __init__(self):
        self.win_name = "Attr Tool"
        self.obj_name = "batch_attr_tool"

        if mc.window(self.obj_name, exists=1):
            mc.deleteUI(self.obj_name)

        mc.window(self.obj_name, title=self.win_name, w=400, h=100, sizeable=1)
        self.column_layout_a = mc.columnLayout(adjustableColumn=True)
        self.frame_subdivision = mc.frameLayout(label="Arnold_Subdivision", cl=1, cll=1, p=self.column_layout_a)
        mc.rowColumnLayout(w=400, nc=3, p=self.frame_subdivision)
        mc.button(label="none", w=133, h=30, c=lambda x: self.ai_set_subdivision(0))
        mc.button(label="catclark", w=133, h=30, c=lambda x: self.ai_set_subdivision(1))
        mc.button(label="linear", w=134, h=30, c=lambda x: self.ai_set_subdivision(2))
        mc.rowColumnLayout(w=100, nc=4, p=self.frame_subdivision)
        mc.button(label="1", w=100, h=30, c=lambda x: self.ai_set_iter(1))
        mc.button(label="2", w=100, h=30, c=lambda x: self.ai_set_iter(2))
        mc.button(label="3", w=100, h=30, c=lambda x: self.ai_set_iter(3))
        mc.button(label="4", w=100, h=30, c=lambda x: self.ai_set_iter(4))
        mc.rowColumnLayout(w=400, nc=1, p=self.frame_subdivision)
        mc.button(label="Turn off subdividing objects", w=400, h=30, c=self.ai_obj_smooth_off)

        self.frame_attr = mc.frameLayout(label="All Attr find and set", cll=1, p=self.column_layout_a)
        self.row_layout_a = mc.rowColumnLayout(w=400, nc=3, parent=self.frame_attr)
        mc.columnLayout(w=100, parent=self.row_layout_a)
        self.find_obj_name = mc.textScrollList(w=100, ams=0)
        mc.columnLayout(w=100, parent=self.row_layout_a)
        mc.button(label="Add Objects", w=100, h=30, c=self.get_obj_name)
        self.find_attr_text = mc.textField(w=100, h=35, text='Find Attribute', tcc=self.find_list_Attr)
        mc.text(w=100, h=5, label="")
        mc.text(w=100, h=30, label="This attr type is")
        self.attr_type = mc.text(w=100, bgc=[0, 0, 0], h=25, label="NoneType")
        self.find_attr_name_set = mc.textField(w=100, h=35, text='value')
        mc.button(label="Set Attr", w=100, h=30, c=self.set_attr_button)
        mc.columnLayout(w=200, parent=self.row_layout_a)
        self.find_attr_name = mc.textScrollList(w=200, ams=0, sc=self.set_attr_type)

        mc.showWindow(self.obj_name)

    def find_list_Attr(self, *args, **kwargs):
        # 查找属性
        mc.textScrollList(self.find_attr_name, w=200, e=1, ra=1)
        find_obj_name1 = mc.textScrollList(self.find_obj_name, q=1, ai=1)
        find_attr_name1 = mc.textField(self.find_attr_text, q=1, text=1)
        if str(type(find_obj_name1))[7:-2] == 'NoneType':
            # 如果物体为空，get attr 查询
            try:
                objAttrs = mc.listAttr(find_attr_name1)
                mc.textScrollList(self.find_attr_name, w=200, e=1, a=objAttrs, )
            except:
                pass

        else:
            objAttrs = mc.listAttr(find_obj_name1[0])
            if find_attr_name1 == "" or find_attr_name1 == "Attribute_Name":
                mc.textScrollList(self.find_attr_name, w=200, e=1, a=objAttrs, )
            else:
                attr_name = []
                for i in objAttrs:
                    if i.upper().find(find_attr_name1.upper()) != -1:
                        attr_name.append(i)
                mc.textScrollList(self.find_attr_name, w=200, e=1, a=attr_name, )

    def set_attr_type(self, *args, **kwargs):
        print mc.textScrollList(self.find_attr_name, q=1, si=1)
        # 设置属性类型
        obj_name = mc.textScrollList(self.find_obj_name, q=1, si=1)
        my_attr_find = mc.textField(self.find_attr_text, q=1, text=1)
        attr_name = mc.textScrollList(self.find_attr_name, q=1, si=1)
        get_attr_names = str()
        if str(type(obj_name))[7:-2] == 'NoneType':
            my_type = my_attr_find + "." + attr_name[0]
        else:
            my_type = obj_name[0] + "." + attr_name[0]

        try:
            get_attr_names = mc.getAttr(my_type)
            str_name = type(get_attr_names)
        except:
            str_name = "<type 'string'>"

        str_name = str(str_name)[7:-2]
        if str_name == 'list':
            if len(get_attr_names[0]) == 0:
                str_name = "NoneType"

            if len(get_attr_names[0]) == 1:
                str_name = "float"

            if len(get_attr_names[0]) == 2:
                str_name = "float2"

            if len(get_attr_names[0]) == 3:
                str_name = "float3"

        elif str_name == "unicode":
            str_name = "string"

        mc.text(self.attr_type, e=1, l=str_name)

    def get_obj_name(self, *args, **kwargs):
        # 添加物体
        mc.textScrollList(self.find_obj_name, e=1, ra=1)
        sels = mc.ls(sl=1)
        if sels:
            mc.textScrollList(self.find_obj_name, e=1, sii=1, a=sels)
        else:
            mc.warning("Please select objects")

    def set_attr_button(self, *args, **kwargs):
        # 设置属性
        my_obj_list = mc.textScrollList(self.find_obj_name, q=1, ai=1)
        my_attr_find = mc.textField(self.find_attr_text, q=1, text=1)
        my_atrr_type = mc.text(self.attr_type, q=1, label=1)
        my_attr_value = mc.textField(self.find_attr_name_set, q=1, text=1)
        my_attr_name = mc.textScrollList(self.find_attr_name, q=1, si=1)

        if my_atrr_type == 'int':
            try:
                my_attr_value = int(my_attr_value)
            except:
                mc.warning("value is not %s type" % my_atrr_type)
                return

        elif my_atrr_type == 'float':
            try:
                my_attr_value = float(my_attr_value)
            except:
                mc.warning("value is not %s type" % my_atrr_type)
                return
        elif my_atrr_type == 'float3' or my_atrr_type == 'double3':
            try:
                my_attr_value = my_attr_value.split(",")
                if len(my_attr_value) == 1:
                    my_attr_value = float(my_attr_value[0]), float(my_attr_value[0]), float(my_attr_value[0])

                elif len(my_attr_value) == 2:
                    mc.warning("value is not %s type" % my_atrr_type)
                    return
                elif len(my_attr_value) == 3:
                    my_attr_value = float(my_attr_value[0]), float(my_attr_value[1]), float(my_attr_value[2])
            except:
                mc.warning("value is not %s type" % my_atrr_type)
                return
        elif my_atrr_type == 'bool':
            if my_attr_value == "0":
                my_attr_value = 0
            else:
                my_attr_value = 1

        no_attr = []
        # 如果有选物体
        if str(type(my_obj_list))[7:-2] != 'NoneType':
            for i in my_obj_list:
                # 循环物体
                attr_name = i + "." + my_attr_name[0]
                # 串联属性字符
                try:
                    if my_atrr_type == "string":
                        # setAttr  属性   属性值   属性类型
                        mc.setAttr(attr_name, my_attr_value, type=my_atrr_type)
                    elif my_atrr_type == "double3" or my_atrr_type == "float2" or my_atrr_type == "float3":
                        if len(my_attr_value) == 2:
                            mc.setAttr(attr_name, my_attr_value[0], my_attr_value[1], type=my_atrr_type)
                        elif len(my_attr_value) == 3:
                            mc.setAttr(attr_name, my_attr_value[0], my_attr_value[1], my_attr_value[2],
                                       type=my_atrr_type)
                    else:
                        mc.setAttr(attr_name, my_attr_value)
                except:
                    no_attr.append(attr_name)
        else:
            # 没有物体
            attr_name = my_attr_find + "." + my_attr_name[0]
            # 存在属性
            if my_atrr_type == "string" or my_atrr_type == "double3" or my_atrr_type == "float2" or my_atrr_type == "float3":
                mc.setAttr(attr_name, my_attr_value, type=my_atrr_type)
            else:
                mc.setAttr(attr_name, my_attr_value)
        if no_attr:
            mc.warning("These properties were not found", no_attr)
        else:
            mc.warning("set ok")

    def ai_set_subdivision(self, *args, **kwargs):
        mc.pickWalk(d="down")
        sel = mc.ls(sl=1, long=1)
        for i in sel:
            mc.setAttr(i + '.aiSubdivType', args[0])

    def ai_set_iter(self, *args, **kwargs):
        mc.pickWalk(d="down")
        sel = mc.ls(sl=1, long=1)
        for i in sel:
            mc.setAttr(i + '.aiSubdivIterations', args[0])

    def ai_obj_smooth_off(self, *args, **kwargs):
        mc.pickWalk(d="down")
        sel = mc.ls(sl=1, long=1)
        for i in sel:
            mc.setAttr(i + ".displaySmoothMesh", 0)


if __name__ == "__main__":
    tool = AttrTool()
