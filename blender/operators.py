import bpy

prop_name = "b2gd_data__"


class B2GDOperatorAddDataReplaceByScene(bpy.types.Operator):
    bl_idname = "object.b2gd_add_data_replace_by_scene"
    bl_label = "Replace by scene"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.object is not None
    
    def execute(self, context):
        context.object[prop_name] = { "mode": 0 }
        return {'FINISHED'}


class B2GDOperatorAddDataGeometry(bpy.types.Operator):
    bl_idname = "object.b2gd_add_data_geometry"
    bl_label = "Geometry Options"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.object
        return obj is not None and obj.type == "MESH"
    
    def execute(self, context):
        context.object[prop_name] = { "mode": 1 }
        return {'FINISHED'}


class B2GDOperatorAddDataCurve(bpy.types.Operator):
    bl_idname = "object.b2gd_add_data_curve"
    bl_label = "Path3D from Curve"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.object
        return obj is not None and obj.type == "CURVE"
    
    def execute(self, context):
        context.object[prop_name] = { "mode": 2 }
        return {'FINISHED'}


class B2GDOperatorRemoveData(bpy.types.Operator):
    bl_idname = "object.b2gd_remove_data"
    bl_label = "Remove B2GD data"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.object is not None
    
    def execute(self, context):
        obj = context.object
        if obj.get(prop_name, None) != None:
            del obj[prop_name]
        
        return {'FINISHED'}


class B2GDOperatorAddGLTFExportSettings(bpy.types.Operator):
    bl_idname = "object.b2gd_add_gltf_settings"
    bl_label = "Enable \"Include Custom Properties\" in GLTF Export Settings"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        data = context.scene.get("glTF2ExportSettings", {})
        data["export_extras"] = True
        context.scene["glTF2ExportSettings"] = data
        
        return {'FINISHED'}


classes = [
    B2GDOperatorAddDataReplaceByScene,
    B2GDOperatorAddDataGeometry,
    B2GDOperatorAddDataCurve,
    B2GDOperatorRemoveData,

    B2GDOperatorAddGLTFExportSettings,
]
