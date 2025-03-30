import bpy

prop_name = "b2gd_data__"


class B2GDOperatorAddDataReplaceByScene(bpy.types.Operator):
    bl_idname = "object.b2gd_replace_by_scene"
    bl_label = "Replace by scene"
    bl_description = "Replaces this object by an instance a scene."
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.object is not None
    
    def execute(self, context):
        context.object[prop_name] = { "mode": 0 }
        return {'FINISHED'}


class B2GDOperatorAddDataGeometry(bpy.types.Operator):
    bl_idname = "object.b2gd_geometry"
    bl_label = "Geometry Options"
    bl_description = "Edit MeshInstance3D properties, create collision objects, navigation region and occluder."
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.object
        return obj is not None and obj.type == "MESH"
    
    def execute(self, context):
        context.object[prop_name] = { "mode": 1 }
        return {'FINISHED'}


class B2GDOperatorAddDataCurve(bpy.types.Operator):
    bl_idname = "object.b2gd_curve"
    bl_label = "Path3D from Curve"
    bl_description = "Creates a Path3D from a Bezier Curve."
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
    bl_description = "Remove B2GD data from the object."
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
    bl_label = "Enable \"Include Custom Properties\" in glTF Export Settings"
    bl_description = "Enable \"Include > Custom Properties\" in the glTF export settings. Needed to export B2GD data."
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        gltf_export_settings = context.scene.get("glTF2ExportSettings", {})
        return not gltf_export_settings.get("export_extras", False)
    
    def execute(self, context):
        data = context.scene.get("glTF2ExportSettings", {})
        data["export_extras"] = True
        context.scene["glTF2ExportSettings"] = data
        
        return {'FINISHED'}


class B2GDOperatorCopyData(bpy.types.Operator):
    bl_idname = "object.b2gd_copy"
    bl_label = "Copy B2GD data"
    bl_description = "Copy B2GD data from an object to the selected objects or a collection."
    bl_options = {'REGISTER', 'UNDO'}

    source_mode: bpy.props.EnumProperty(
        name = "Source Object",
        description = "Object to copy B2GD data from.",
        items = [
            ("active", "Active Object", "Copy data from the active object.", 0),
            ("object", "Chosen Object", "Copy data from an object.", 1),
        ],
        default = 0,
    ) # type: ignore

    target_mode: bpy.props.EnumProperty(
        name = "Target",
        description = "Objects to copy B2GD data to.",
        items = [
            ("selected", "Selected Objects", "Copy data to selected objects", 0),
            ("collection", "Collection", "Copy data to objects in a collection", 1),
        ],
        default = 0,
    ) # type: ignore

    def execute(self, context):
        src = context.active_object
        
        if self.source_mode == "object":
            src = context.scene.b2gd_data__.copy_source_object
        
        if src == None:
            self.report({'ERROR_INVALID_INPUT'}, message='No source object to copy B2GD data.')
            return {'FINISHED'}

        data = src.get("b2gd_data__", None)

        if data == None:
            self.report({'WARNING'}, message="Source object doesn't have B2GD data. No data has been changed")
            return {'FINISHED'}
        
        targets = context.selected_objects

        if self.target_mode == "collection":
            collection = context.scene.b2gd_data__.copy_target_collection
            if collection == None:
                self.report({'ERROR_INVALID_INPUT'}, message='No target collection selected.')
                return {'FINISHED'}
            targets = collection.objects
        
        count = len(targets)

        for obj in targets:
            if obj == src:
                count -= 1
                continue
            
            obj["b2gd_data__"] = data
        
        self.report({'INFO'}, message=f"B2GD data copied to {count} objects.")
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
    def draw(self, context):
        layout = self.layout
        col = layout.column()

        row = col.row()
        row.prop(self, "source_mode")

        if self.source_mode == "object":
            row.prop_search(context.scene.b2gd_data__, "copy_source_object", context.scene, "objects")
        
        row = col.row()

        row.prop(self, "target_mode")
        if self.target_mode == "collection":
            row.prop_search(context.scene.b2gd_data__, "copy_target_collection", bpy.data, "collections")



classes = [
    B2GDOperatorAddDataReplaceByScene,
    B2GDOperatorAddDataGeometry,
    B2GDOperatorAddDataCurve,
    B2GDOperatorRemoveData,

    B2GDOperatorAddGLTFExportSettings,

    B2GDOperatorCopyData,
]
