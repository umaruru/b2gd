import bpy

prop_name = "b2gd_data__"


def draw_replace_by_scene(layout: bpy.types.UILayout, context: bpy.types.Context):
    data = context.scene.b2gd_data__.replace_by_scene
    
    layout.label(text="Replace by Scene")

    layout.prop(data, "path")
    layout.prop(data, "position")
    layout.prop(data, "rotation")
    layout.prop(data, "scale")


def draw_mesh_panel(layout: bpy.types.UILayout, data):
    mesh = data.geometry.mesh_data

    header, panel = layout.panel("panel_b2gd_geometry")
    header.prop(data.geometry, "mesh")

    if data.geometry.mesh and panel:
        panel.label(text = "Layers")
        row = panel.row()
        row.prop(mesh, "layers_1_10", text = "")
        # row = panel.row()
        row.prop(mesh, "layers_11_20", text = "")

        panel.prop(mesh, "transparency")
        panel.prop(mesh, "cast_shadow")
        panel.prop(mesh, "ignore_occlusion_culling")
        panel.prop(mesh, "gi_mode")
        panel.prop(mesh, "gi_lightmap_textel_scale")

        panel.separator()
    
    elif not data.geometry.mesh:
        row = layout.row(align=True, heading="Remove Mode")
        row.prop(data.geometry, "mesh_remove_mode", expand=True)

        if data.geometry.mesh_remove_mode == "free":
            layout.label(text="Child objects will be deleted.", icon="WARNING_LARGE")
            layout.label(text="Generated collision and navigation will be added to the parent.")
        
        layout.separator(type="LINE")


def draw_collision_body_panel(layout: bpy.types.UILayout, data):
    collision = data.geometry.collision_data

    header, panel = layout.panel("panel_b2gd_gen_collision_body")
    # header.label(text="Collision Body")

    match collision.body_type:
        case "static":
            header.label(text="StaticBody3D")
        case "animatable":
            header.label(text="AnimatableBody3D")
        case "rigid":
            header.label(text="RigidBody3D")
        case "character":
            header.label(text="CharacterBody3D")
        case "area":
            header.label(text="Area3D")
        case _:
            header.label(text="🤷")

    if panel:
        match collision.body_type:
            case "static":
                body = collision.body_type_static
                panel.label(text="Physics Material Override Path")
                panel.prop(collision, "physics_material_path", text="")
                panel.prop(body, "constant_linear_velocity")
                panel.prop(body, "constant_angular_velocity")

            case "animatable":
                body = collision.body_type_animatable
                panel.label(text="Physics Material Override Path")
                panel.prop(collision, "physics_material_path", text="")
                panel.prop(body, "sync_to_physics")

            case "rigid":
                body = collision.body_type_rigid
                panel.label(text="Physics Material Override Path")
                panel.prop(collision, "physics_material_path", text="")
                panel.prop(body, "mass")
                panel.prop(body, "gravity_scale")
                panel.prop(body, "sleeping")
                panel.prop(body, "can_sleep")
                panel.prop(body, "lock_rotation")
                panel.prop(body, "freeze")
                panel.prop(body, "freeze_mode")

            case "character":
                body = collision.body_type_character
                panel.label(text = "😔")

            case "area":
                body = collision.body_type_area
                panel.prop(body, "monitoring")
                panel.prop(body, "monitorable")
                panel.prop(body, "priority")
            
            case _:
                panel.label("🤷")

        panel.separator(type = "LINE")

        panel.prop(collision, "disable_mode")
        
        panel.label(text = "Collision Layer")
        row = panel.row()
        row.prop(collision, "collision_layer_1_16", text = "")
        row = panel.row()
        row.prop(collision, "collision_layer_17_32", text = "")

        panel.label(text = "Collision Mask")
        row = panel.row()
        row.prop(collision, "collision_mask_1_16", text = "")
        row = panel.row()
        row.prop(collision, "collision_mask_17_32", text = "")

        panel.separator(factor = 0.2)

        panel.prop(collision, "collision_priority")
        panel.prop(collision, "input_ray_pickable")
        panel.prop(collision, "input_capture_on_drag")


def draw_collision_shape_panel(layout: bpy.types.UILayout, data):
    collision = data.geometry.collision_data

    match collision.shape_type:
        case "trimesh":
            layout.prop(collision.shape_type_trimesh, "backface_collision")
        case "convex":
            layout.prop(collision.shape_type_convex, "mode")



def draw_collision_panel(layout: bpy.types.UILayout, data):
    collision = data.geometry.collision_data

    header, panel = layout.panel("panel_b2gd_gen_collision")
    header.prop(data.geometry, "collision")

    if data.geometry.collision and panel:
        row = panel.row(align=True, heading="Add as")
        row.prop(collision, "add_as", expand=True)

        if collision.add_as == "child" and (not data.geometry.mesh and data.geometry.mesh_remove_mode == "free"):
            box = panel.box()
            box.label(text="Mesh Instance is disabled and Remove Mode is \"Free Node\".", icon="WARNING_LARGE")
            box.label(text="The CollisionObject will be added as sibling.")

        panel.separator(type = "LINE")

        panel.prop(collision, "body_type")

        if collision.body_type != "none":
            draw_collision_body_panel(panel, data)
        else:
            panel.label(text="No CollisionObject3D will be created.", icon="QUESTION")
        
        panel.separator(type = "LINE")

        panel.prop(collision, "shape_type")

        if collision.shape_type != "none":
            draw_collision_shape_panel(panel, data)
        else:
            panel.label(text="No CollisionShape3D will be created.", icon="QUESTION")
        
        if collision.body_type == "none" and collision.shape_type == "none":
            box: bpy.types.UILayout = panel.box()
            box.label(text="Collision Body and Shape are disabled.", icon="ERROR")
            box.label(text="No collision will be created.")
        
        panel.separator()


def draw_navigation_panel(layout: bpy.types.UILayout, data):
    navigation = data.geometry.navigation_data

    panel_header, panel = layout.panel("panel_b2gd_props_navigation")
    panel_header.prop(data.geometry, "navigation")

    if data.geometry.navigation and panel:
        row = panel.row(align=True, heading="Add as")
        row.prop(navigation, "add_as", expand=True)

        if navigation.add_as == "child" and (not data.geometry.mesh and data.geometry.mesh_remove_mode == "free"):
            box = panel.box()
            box.label(text="Mesh Instance is disabled and Remove Mode is \"Free Node\".", icon="WARNING_LARGE")
            box.label(text="The NavigationAgent will be added as sibling.")

        panel.prop(navigation, "enabled")
        panel.prop(navigation, "use_edge_connections")
        
        panel.label(text = "Navigation Layers")
        panel.prop(navigation, "navigation_layers_1_16", text = "")
        panel.prop(navigation, "navigation_layers_17_32", text = "")

        panel.separator(factor = 0.2)
        panel.prop(navigation, "enter_cost")
        panel.prop(navigation, "travel_cost")

        panel.separator()


def draw_geometry(layout: bpy.types.UILayout, context: bpy.types.Context):
    data = context.scene.b2gd_data__
    
    header, panel = layout.panel("panel_b2gd_gometry")
    header.label(text="Geometry")

    if panel:
        draw_mesh_panel(panel, data)
        panel.separator(factor = 0.1)
        draw_collision_panel(panel, data)
        panel.separator(factor = 0.1)
        draw_navigation_panel(panel, data)
        panel.separator(factor = 0.1)
        panel.prop(data.geometry, "occluder")

    


def draw_curve(layout: bpy.types.UILayout, context: bpy.types.Context):
    pass


class B2GDUIMainPanel(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_B2GD_UI_MainPanel"
    bl_label = "Blender to Godot"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "B2GD"


    def draw(self, context):
        layout = self.layout
        
        gltf_export_settings = context.scene.get("glTF2ExportSettings", {})
        export_extras = gltf_export_settings.get("export_extras", False)
        
        if not export_extras:
            layout.operator("object.b2gd_add_gltf_settings")
        
        obj = context.object

        if obj is None:
            layout.label(text = "No object.")
            return
        
        box = layout.box()
        box.label(text = obj.name)
        
        if obj.get(prop_name, None) == None:
            layout.operator("object.b2gd_add_data_replace_by_scene")
            layout.operator("object.b2gd_add_data_geometry")
            layout.operator("object.b2gd_add_data_curve")
        
        else:
            mode = obj[prop_name].get("mode", -1)

            if mode != -1:
                layout.operator("object.b2gd_remove_data")
                # layout.prop(scene.b2gd_data__, "mode")

            match mode:
                case 0: # replace by scene
                    draw_replace_by_scene(layout, context)
                
                case 1: # geometry
                    draw_geometry(layout, context)
                
                case 2: # curve
                    data = context.scene.b2gd_data__.curve
                    # layout.prop(data, "position")
                    if obj.type != 'CURVE':
                        layout.label(text = "Object is not a curve!", icon = "ERROR")
                
                case _:
                    layout.label(text = "Invalid data!", icon = "QUESTION")




classes = [B2GDUIMainPanel]
