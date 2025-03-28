import bpy

prop_name = "b2gd_data__"


def get_func(path, default):
    obj = bpy.context.object
    if obj is None: return default
    return obj[prop_name].get(path, default)


def set_func(path, value):
    obj = bpy.context.object
    if obj is None: return
    obj[prop_name][path] = value


def set_and_erase_on_false(path, value, prefix):
    obj = bpy.context.object
    if obj is None: return
    obj[prop_name][path] = value

    if value == False:
        matched_keys = []

        for key in obj[prop_name].keys():
            if key.startswith(prefix):
                matched_keys.append(key)

        for key in matched_keys:
            obj[prop_name].pop(key, None)


def set_and_erase_prefix(path, value, prefix):
    obj = bpy.context.object
    if obj is None: return

    matched_keys = []

    for key in obj[prop_name].keys():
        if key.startswith(prefix):
            matched_keys.append(key)
    
    for key in matched_keys:
        obj[prop_name].pop(key, None)
    
    obj[prop_name][path] = value


def get_layer_bitmask(path, size, default_bitmask, default_vector):
    obj = bpy.context.object
    if obj is None: return default_vector

    bitmask = obj[prop_name].get(path, default_bitmask)
    
    if bitmask == default_bitmask:
        return default_vector

    vector = [False] * size

    for i in range(size):
        vector[i] = (bitmask & (1 << i)) != 0
    
    return vector


def set_layer_bitmask(path, value):
    obj = bpy.context.object
    if obj is None: return
    
    bitmask = 0

    for i in range(len(value)):
        if value[i] == True:
            bitmask |= 1 << i
    
    obj[prop_name][path] = bitmask



########## ---------- Replace by scene ---------- ##########


class B2GDPropReplaceByScene(bpy.types.PropertyGroup):
    path: bpy.props.StringProperty(
        name = "Path or UID",
        description = "Scene path or UID of the scene. Tip: use Copy Path or UID on the FileSystem tab.",
        get = lambda self : get_func("replace_by_scene/path", ""),
        set = lambda self, value : set_func("replace_by_scene/path", value),
    ) # type: ignore

    position: bpy.props.BoolProperty(
        name = "Discard position",
        description = "Discard the object position. The instanced scene will be placed at Vector3(0, 0, 0).",
        get = lambda self : get_func("replace_by_scene/position", False),
        set = lambda self, value : set_func("replace_by_scene/position", value),
    ) # type: ignore

    rotation: bpy.props.BoolProperty(
        name = "Discard rotation",
        description = "Discard the object rotation. The instanced scene won't be rotated.",
        get = lambda self : get_func("replace_by_scene/rotation", False),
        set = lambda self, value : set_func("replace_by_scene/rotation", value),
    ) # type: ignore

    scale: bpy.props.BoolProperty(
        name = "Discard scale",
        description = "Discard the object scale. The instanced scene will have a scale of 1.",
        get = lambda self : get_func("replace_by_scene/scale", False),
        set = lambda self, value : set_func("replace_by_scene/scale", value),
    ) # type: ignore



########## ---------- Curve props ---------- ##########


class B2GDPropCurve(bpy.types.PropertyGroup):
    position: bpy.props.FloatVectorProperty(
        name = "Position",
        subtype = "TRANSLATION",
        get = lambda self : get_func("curve/position", [0, 0, 0]),
        set = lambda self, value : set_func("curve/position", value),
    ) # type: ignore



########## ---------- Mesh Instance ---------- ##########

class B2GDPropMesh(bpy.types.PropertyGroup):
    # VisualInstance3D

    layers_1_10: bpy.props.BoolVectorProperty(
        name = "Layers 1 - 10",
        description = "The render layers this VisualInstance3D is drawn on.",
        size = 10,
        subtype = "LAYER",
        get = lambda self : get_layer_bitmask("geometry/mesh/layers_1_10", 10, 1, [True] + [False] * 9),
        set = lambda self, value : set_layer_bitmask("geometry/mesh/layers_1_10", value),
    ) # type: ignore

    layers_11_20: bpy.props.BoolVectorProperty(
        name = "Layers 11 - 20",
        description = "The render layers this VisualInstance3D is drawn on.",
        size = 10,
        subtype = "LAYER",
        get = lambda self : get_layer_bitmask("geometry/mesh/layers_11_20", 10, 0, [False] * 10),
        set = lambda self, value : set_layer_bitmask("geometry/mesh/layers_11_20", value),
    ) # type: ignore

    # GeometryInstance3D

    transparency: bpy.props.FloatProperty(
        name = "Transparency",
        description = "The transparency applied to the whole geometry. 0.0 is fully opaque. 1.0 is fully transparent.",
        min = 0,
        max = 1,
        get = lambda self : get_func("geometry/mesh/transparency", 0),
        set = lambda self, value : set_func("geometry/mesh/transparency", value),
    ) # type: ignore

    cast_shadow: bpy.props.EnumProperty(
        name = "Cast Shadow",
        description = "The selected shadow casting flag.",
        items = [
            ("off", "Off", "Will not cast any shadows.", 0),
            ("on", "On", "Will cast shadows from all visible faces in the GeometryInstance3D. Takes culling into account.", 1),
            ("double_sided", "Double-Sided", "Will cast shadows from all visible faces in the GeometryInstance3D. Doesn't take culling into account.", 2),
            ("shadows_only", "Shadows Only", "Will only show the shadows casted from this object.", 3),
        ],
        get = lambda self : get_func("geometry/mesh/cast_shadow", 1),
        set = lambda self, value : set_func("geometry/mesh/cast_shadow", value),
    ) # type: ignore

    ignore_occlusion_culling: bpy.props.BoolProperty(
        name = "Ignore Occlusion Culling",
        description = "If true, disables occlusion culling for this instance.",
        get = lambda self : get_func("geometry/mesh/ignore_occlusion_culling", False),
        set = lambda self, value : set_func("geometry/mesh/ignore_occlusion_culling", value),
    ) # type: ignore

    gi_mode: bpy.props.EnumProperty(
        name = "GI Mode",
        description = "The global illumination mode to use for the whole geometry.",
        items = [
            ("disabled", "Disabled", "Disabled global illumination mode.", 0),
            ("static", "Static", "Baked global illumination mode.", 1),
            ("dynamic", "Dynamic", "Dynamic global illumination mode.", 2),
        ],
        get = lambda self : get_func("geometry/mesh/gi_mode", 1),
        set = lambda self, value : set_func("geometry/mesh/gi_mode", value),
    ) # type: ignore

    gi_lightmap_textel_scale: bpy.props.FloatProperty(
        name = "Lightmap Textel Scale",
        description = "The texel density to use for lightmapping in LightmapGI.",
        min = 0.01,
        get = lambda self : get_func("geometry/mesh/gi_lightmap_textel_scale", 1.0),
        set = lambda self, value : set_func("geometry/mesh/gi_lightmap_textel_scale", value),
    ) # type: ignore



########## ---------- Collision ---------- ##########


## ----- Bodies ----- ##


class B2GDPropBodyStatic(bpy.types.PropertyGroup):
    constant_linear_velocity: bpy.props.FloatVectorProperty(
        name = "Constant Linear Velocity",
        description = "The body's constant linear velocity. This does not move the body, but affects touching bodies, as if it were moving.",
        subtype = "VELOCITY",
        get = lambda self : get_func("geometry/gen/collision/body/static/constant_linear_velocity", [0, 0, 0]),
        set = lambda self, value : set_func("geometry/gen/collision/body/static/constant_linear_velocity", value),
    ) # type: ignore
    
    constant_angular_velocity: bpy.props.FloatVectorProperty(
        name = "Constant Angular Velocity",
        description = "The body's constant angular velocity. This does not rotate the body, but affects touching bodies, as if it were rotating.",
        subtype = "VELOCITY",
        get = lambda self : get_func("geometry/gen/collision/body/static/constant_angular_velocity", [0, 0, 0]),
        set = lambda self, value : set_func("geometry/gen/collision/body/static/constant_angular_velocity", value),
    ) # type: ignore


class B2GDPropBodyAnimatable(bpy.types.PropertyGroup):
    sync_to_physics: bpy.props.BoolProperty(
        name = "Sync To Physics",
        description = "If true, the body's movement will be synchronized to the physics frame.",
        get = lambda self : get_func("geometry/gen/collision/body/animatable/sync_to_physics", True),
        set = lambda self, value : set_func("geometry/gen/collision/body/animatable/sync_to_physics", value),
    ) # type: ignore


class B2GDPropBodyRigid(bpy.types.PropertyGroup):
    mass: bpy.props.FloatProperty(
        name = "Mass",
        description = "The body's mass.",
        min = 0.001,
        get = lambda self : get_func("geometry/gen/collision/body/rigid/mass", 1.0),
        set = lambda self, value : set_func("geometry/gen/collision/body/rigid/mass", value),
    ) # type: ignore
    
    gravity_scale: bpy.props.FloatProperty(
        name = "Gravity Scale",
        description = "This is multiplied by \"Physics > 3D > Default Gravity\" to produce this body's gravity.",
        get = lambda self : get_func("geometry/gen/collision/body/rigid/gravity_scale", 1.0),
        set = lambda self, value : set_func("geometry/gen/collision/body/rigid/gravity_scale", value),
    ) # type: ignore

    # deactivation

    sleeping: bpy.props.BoolProperty(
        name = "Sleeping",
        description = "If true, the body will not move and will not calculate forces until woken up by another body through a collision or by using the apply_impulse() or apply_force() methods.",
        get = lambda self : get_func("geometry/gen/collision/body/rigid/sleeping", False),
        set = lambda self, value : set_func("geometry/gen/collision/body/rigid/sleeping", value),
    ) # type: ignore

    can_sleep: bpy.props.BoolProperty(
        name = "Can Sleep",
        description = "If true, the body can enter sleep mode when there is no movement.",
        get = lambda self : get_func("geometry/gen/collision/body/rigid/can_sleep", True),
        set = lambda self, value : set_func("geometry/gen/collision/body/rigid/can_sleep", value),
    ) # type: ignore

    lock_rotation: bpy.props.BoolProperty(
        name = "Lock Rotation",
        description = "If true, the body cannot rotate. Gravity and forces only apply linear movement.",
        get = lambda self : get_func("geometry/gen/collision/body/rigid/lock_rotation", False),
        set = lambda self, value : set_func("geometry/gen/collision/body/rigid/lock_rotation", value),
    ) # type: ignore

    freeze: bpy.props.BoolProperty(
        name = "Freeze",
        description = "If true, the body is frozen. Gravity and forces are not applied anymore.",
        get = lambda self : get_func("geometry/gen/collision/body/rigid/freeze", False),
        set = lambda self, value : set_func("geometry/gen/collision/body/rigid/freeze", value),
    ) # type: ignore
    
    freeze_mode: bpy.props.EnumProperty(
        name = "Freeze Mode",
        description = "The body's freeze mode. Can be used to set the body's behavior when freeze is enabled.",
        items = [
            ("static", "Static", "The body is not affected by gravity and forces. It can be only moved by user code and doesn't collide with other bodies along its path.", 0),
            ("kinematic", "Kinematic", "Similar to Static, but collides with other bodies along its path when moved. Useful for a frozen body that needs to be animated.", 1),
        ],
        get = lambda self : get_func("geometry/gen/collision/body/rigid/freeze_mode", 0),
        set = lambda self, value : set_func("geometry/gen/collision/body/rigid/freeze_mode", value),
    ) # type: ignore


class B2GDPropBodyCharacter(bpy.types.PropertyGroup):
    # better to set up on the engine
    # maybe use replace by scene?
    pass


class B2GDPropBodyArea(bpy.types.PropertyGroup):
    monitoring: bpy.props.BoolProperty(
        name = "Monitoring",
        description = "If true, the area detects bodies or areas entering and exiting it.",
        get = lambda self : get_func("geometry/gen/collision/body/area/monitoring", True),
        set = lambda self, value : set_func("geometry/gen/collision/body/area/monitoring", value),
    ) # type: ignore

    monitorable: bpy.props.BoolProperty(
        name = "Monitorable",
        description = "If true, other monitoring areas can detect this area.",
        get = lambda self : get_func("geometry/gen/collision/body/area/monitorable", True),
        set = lambda self, value : set_func("geometry/gen/collision/body/area/monitorable", value),
    ) # type: ignore

    priority: bpy.props.IntProperty(
        name = "Priority",
        description = "The area's priority. Higher priority areas are processed first.",
        get = lambda self : get_func("geometry/gen/collision/body/area/priority", 0),
        set = lambda self, value : set_func("geometry/gen/collision/body/area/priority", value),
    ) # type: ignore


## ----- Shape ----- ##


class B2GDPropShapeTrimesh(bpy.types.PropertyGroup):
    backface_collision: bpy.props.BoolProperty(
        name = "Backface Collision",
        description = "If set to true, collisions occur on both sides of the concave shape faces. Otherwise they occur only along the face normals.",
        get = lambda self : get_func("geometry/gen/collision/shape/trimesh/backface_collision", False),
        set = lambda self, value : set_func("geometry/gen/collision/shape/trimesh/backface_collision", value),
    ) # type: ignore


class B2GDPropShapeConvex(bpy.types.PropertyGroup):
    mode: bpy.props.EnumProperty(
        name = "Mode",
        description = "The mode the collision shape will be generated.",
        items = [
            ("single", "Single", "Fastest, but least accurate option for collision detection.", 0),
            ("simplified", "Simplified", "Similar to single. Can result in a simpler geometry in some cases, at the cost of accuracy.", 1),
            ("multiple", "Multiple", "This is a performance middle-ground between a single convex collision and a polygon based collision (trimesh).", 2),
        ],
        get = lambda self : get_func("geometry/gen/collision/shape/convex/mode", 0),
        set = lambda self, value : set_func("geometry/gen/collision/shape/convex/mode", value),
    ) # type: ignore


class B2GDPropShapeSphere(bpy.types.PropertyGroup):
    radius = None


class B2GDPropShapeBox(bpy.types.PropertyGroup):
    size = None


class B2GDPropShapeCapsule(bpy.types.PropertyGroup):
    radius = None
    height = None


class B2GDPropShapeCylinder(bpy.types.PropertyGroup):
    height = None
    radius = None


## ----- Collision ----- ##


class B2GDPropCollision(bpy.types.PropertyGroup):
    add_as: bpy.props.EnumProperty(
        name = "Add as",
        description = "Defines if the Collision Object will be added as child or sibling of the Geometry.",
        items = [
            ("child", "Child", "The CollisionObject will be added as child of the MeshInstance3D.", 0),
            ("sibling", "Sibling", "The CollisionObject will be added as sibling of the MeshInstance3D.", 1),
        ],
        get = lambda self : get_func("geometry/gen/collision/add_as", 0),
        set = lambda self, value : set_func("geometry/gen/collision/add_as", value),
    ) # type: ignore

    # CollisionObject3D
    
    disable_mode: bpy.props.EnumProperty(
        name = "Disable Mode",
        description = "Defines the behavior in physics when Node.process_mode is set to Node.PROCESS_MODE_DISABLED.",
        items = [
            ("remove", "Remove", "Remove from the physics simulation to stop all physics interactions with this CollisionObject3D.", 0),
            ("make_static", "Make Static", "Make the body static. Doesn't affect Area3D. PhysicsBody3D can't be affected by forces or other bodies while static.", 1),
            ("keep_active", "Keep Active", "When Node.process_mode is set to Node.PROCESS_MODE_DISABLED, do not affect the physics simulation.", 2),
        ],
        get = lambda self : get_func("geometry/gen/collision/disable_mode", 0),
        set = lambda self, value : set_func("geometry/gen/collision/disable_mode", value),
    ) # type: ignore

    collision_layer_1_16: bpy.props.BoolVectorProperty(
        name = "Collision Layers 1 - 16",
        description = "The physics layers this CollisionObject3D is in.",
        size = 16,
        subtype = "LAYER",
        get = lambda self : get_layer_bitmask("geometry/gen/collision/collision_layer_1_16", 16, 1, [True] + [False] * 15),
        set = lambda self, value : set_layer_bitmask("geometry/gen/collision/collision_layer_1_16", value),
    ) # type: ignore

    collision_layer_17_32: bpy.props.BoolVectorProperty(
        name = "Collision Layers 17 - 32",
        description = "The physics layers this CollisionObject3D is in.",
        size = 16,
        subtype = "LAYER",
        get = lambda self : get_layer_bitmask("geometry/gen/collision/collision_layer_17_32", 16, 0, [False] * 16),
        set = lambda self, value : set_layer_bitmask("geometry/gen/collision/collision_layer_17_32", value),
    ) # type: ignore

    collision_mask_1_16: bpy.props.BoolVectorProperty(
        name = "Collision Mask 1 - 16",
        description = "The physics layers this CollisionObject3D scans.",
        size = 16,
        subtype = "LAYER",
        get = lambda self : get_layer_bitmask("geometry/gen/collision/collision_mask_1_16", 16, 1, [True] + [False] * 15),
        set = lambda self, value : set_layer_bitmask("geometry/gen/collision/collision_mask_1_16", value),
    ) # type: ignore

    collision_mask_17_32: bpy.props.BoolVectorProperty(
        name = "Collision Mask 17 - 32",
        description = "The physics layers this CollisionObject3D scans.",
        size = 16,
        subtype = "LAYER",
        get = lambda self : get_layer_bitmask("geometry/gen/collision/collision_mask_17_32", 16, 0, [False] * 16),
        set = lambda self, value : set_layer_bitmask("geometry/gen/collision/collision_mask_17_32", value),
    ) # type: ignore

    collision_priority: bpy.props.FloatProperty(
        name = "Priority",
        description = "The priority used to solve colliding when occurring penetration. The higher the priority is, the lower the penetration into the object will be.",
        min = 0.001,
        get = lambda self : get_func("geometry/gen/collision/collision_priority", 1.0),
        set = lambda self, value : set_func("geometry/gen/collision/collision_priority", value),
    ) # type: ignore

    input_ray_pickable: bpy.props.BoolProperty(
        name = "Ray Pickable",
        description = "If true, this object is pickable. A pickable object can detect the mouse pointer entering/leaving, and if the mouse is inside it, report input events.",
        get = lambda self : get_func("geometry/gen/collision/input_ray_pickable", True),
        set = lambda self, value : set_func("geometry/gen/collision/input_ray_pickable", value),
    ) # type: ignore

    input_capture_on_drag: bpy.props.BoolProperty(
        name = "Capture on Drag",
        description = "If true, the CollisionObject3D will continue to receive input events as the mouse is dragged across its shapes.",
        get = lambda self : get_func("geometry/gen/collision/input_capture_on_drag", False),
        set = lambda self, value : set_func("geometry/gen/collision/input_capture_on_drag", value),
    ) # type: ignore

    body_type: bpy.props.EnumProperty(
        name = "Body",
        description = "Defines what type of CollisionObject3D will be created.",
        items = [
            ("static", "Static Body", "Creates a StaticBody3D.", 0),
            ("animatable", "Animatable Body", "Creates an AnimatableBody3D.", 1),
            ("rigid", "Rigid Body", "Creates a RigidBody3D", 2),
            ("character", "Character Body", "Creates a CharacterBody3D", 3),
            ("area", "Area", "Creates an Area3D", 4),
            ("none", "Shape Only", "Don't create a Collision Body, only collision shapes.", 5),
        ],
        get = lambda self : get_func("geometry/gen/collision/body_type", 0),
        set = lambda self, value : set_and_erase_prefix("geometry/gen/collision/body_type", value, "geometry/gen/collision/body/"),
    ) # type: ignore

    physics_material_path: bpy.props.StringProperty(
        name = "Physics Material Override Path",
        description = "The path to a PhysicsMaterial resource.",
        get = lambda self : get_func("geometry/gen/collision/physics_material_path", ""),
        set = lambda self, value : set_func("geometry/gen/collision/physics_material_path", value),
    ) # type: ignore
    
    shape_type: bpy.props.EnumProperty(
        name = "Shape",
        description = "Defines what type of CollisionShape3D will be created.",
        items = [
            ("trimesh", "Trimesh", "Creates a polygon based collision shape (ConcavePolygonShape3D).", 0),
            ("convex", "Convex", "Creates a convex collision shape (ConvexPolygonShape3D).", 1),
            ("none", "No shape", "No CollisionShape3D will be created.", 2),
        ],
        get = lambda self : get_func("geometry/gen/collision/shape_type", 0),
        set = lambda self, value : set_and_erase_prefix("geometry/gen/collision/shape_type", value, "geometry/gen/collision/shape/"),
    ) # type: ignore

    shape_disabled: bpy.props.BoolProperty(
        name = "Shape Disabled",
        description = "A disabled collision shape has no effect in the world.",
        get = lambda self : get_func("geometry/gen/collision/shape_disabled", False),
        set = lambda self, value : set_func("geometry/gen/collision/shape_disabled", value),
    ) # type: ignore

    body_type_static: bpy.props.PointerProperty(type = B2GDPropBodyStatic) # type: ignore
    body_type_animatable: bpy.props.PointerProperty(type = B2GDPropBodyAnimatable) # type: ignore
    body_type_rigid: bpy.props.PointerProperty(type = B2GDPropBodyRigid) # type: ignore
    body_type_character: bpy.props.PointerProperty(type = B2GDPropBodyCharacter) # type: ignore
    body_type_area: bpy.props.PointerProperty(type = B2GDPropBodyArea) # type: ignore

    shape_type_trimesh: bpy.props.PointerProperty(type = B2GDPropShapeTrimesh) # type: ignore
    shape_type_convex: bpy.props.PointerProperty(type = B2GDPropShapeConvex) # type: ignore



########## ---------- Navigation ---------- ##########


class B2GDPropNavigationRegion(bpy.types.PropertyGroup):
    add_as: bpy.props.EnumProperty(
        name = "Add as",
        description = "Defines if the Navigation Region will be added as child or sibling of the Geometry.",
        items = [
            ("child", "Child", "The NavigationRegion3D will be added as child of the MeshInstance3D.", 0),
            ("sibling", "Sibling", "The NavigationRegion3D will be added as sibling of the MeshInstance3D.", 1),
        ],
        get = lambda self : get_func("geometry/gen/navigation/add_as", 0),
        set = lambda self, value : set_func("geometry/gen/navigation/add_as", value),
    ) # type: ignore

    enabled: bpy.props.BoolProperty(
        name = "Enabled",
        description = "Determines if the NavigationRegion3D is enabled or disabled.",
        get = lambda self : get_func("geometry/gen/navigation/enabled", True),
        set = lambda self, value : set_func("geometry/gen/navigation/enabled", value),
    ) # type: ignore

    use_edge_connections: bpy.props.BoolProperty(
        name = "Use Edge Connections",
        description = "If enabled the navigation region will use edge connections to connect with other navigation regions within proximity of the navigation map edge connection margin.",
        get = lambda self : get_func("geometry/gen/navigation/use_edge_connections", True),
        set = lambda self, value : set_func("geometry/gen/navigation/use_edge_connections", value),
    ) # type: ignore

    navigation_layers_1_16: bpy.props.BoolVectorProperty(
        name = "Navigation Layers 1 - 16",
        description = "A bitfield determining all navigation layers the region belongs to.",
        size = 16,
        subtype = "LAYER",
        get = lambda self : get_layer_bitmask("geometry/gen/navigation/navigation_layers_1_16", 16, 1, [True] + [False] * 15),
        set = lambda self, value : set_layer_bitmask("geometry/gen/navigation/navigation_layers_1_16", value),
    ) # type: ignore

    navigation_layers_17_32: bpy.props.BoolVectorProperty(
        name = "Navigation Layers 17 - 32",
        description = "A bitfield determining all navigation layers the region belongs to.",
        size = 16,
        subtype = "LAYER",
        get = lambda self : get_layer_bitmask("geometry/gen/navigation/navigation_layers_17_32", 16, 0, [False] * 16),
        set = lambda self, value : set_layer_bitmask("geometry/gen/navigation/navigation_layers_17_32", value),
    ) # type: ignore

    enter_cost: bpy.props.FloatProperty(
        name = "Enter Cost",
        description = "When pathfinding enters this region's navigation mesh from another regions navigation mesh, the enter_cost value is added to the path distance for determining the shortest path.",
        min = 0,
        get = lambda self : get_func("geometry/gen/navigation/enter_cost", 0.0),
        set = lambda self, value : set_func("geometry/gen/navigation/enter_cost", value),
    ) # type: ignore
    
    travel_cost: bpy.props.FloatProperty(
        name = "Travel Cost",
        description = "When pathfinding moves inside this region's navigation mesh, the traveled distances are multiplied with travel_cost for determining the shortest path.",
        min = 0,
        get = lambda self : get_func("geometry/gen/navigation/travel_cost", 1.0),
        set = lambda self, value : set_func("geometry/gen/navigation/travel_cost", value),
    ) # type: ignore


class B2GDPropNavigationObstacle(bpy.types.PropertyGroup):
    radius: None
    height: None
    affect_navigation_mesh: None
    carve_navigation_mesh: None
    avoidance_enabled: None
    avoidance_layers: None
    use_3d_avoidance: None


class B2GDPropNavigationLink(bpy.types.PropertyGroup):
    enabled: None
    bidirectional: None
    navigation_layers: None
    start_position: None
    end_position: None
    enter_cost: None
    travel_cost: None



########## ---------- Geometry ---------- ##########


class B2GDPropGeometry(bpy.types.PropertyGroup):
    mesh: bpy.props.BoolProperty(
        name = "Mesh Instance",
        description = "Determines if Mesh Instance will be kept for this object. Disabling is useful when only collision, navigation or occluder is needed.",
        get = lambda self : get_func("geometry/mesh", True),
        set = lambda self, value : set_and_erase_on_false("geometry/mesh", value, "geometry/mesh/"),
    ) # type: ignore

    mesh_remove_mode: bpy.props.EnumProperty(
        name = "Remove mode",
        description = "What to do with the object when MeshInstance3d is removed.",
        items = [
            ("replace_by_node", "Replace by Node3D", "The MeshInstance3D is replaced by a Node3D. Children will be kept.", 0),
            ("free", "Free Node", "The MeshInstance3D will be deleted from the scene, along with its children", 1),
        ],
        get = lambda self : get_func("geometry/mesh_remove_mode", 0),
        set = lambda self, value : set_func("geometry/mesh_remove_mode", value),
    ) # type: ignore

    collision: bpy.props.BoolProperty(
        name = "Generate Collision",
        description = "Generate collision body and shapes from mesh.",
        get = lambda self : get_func("geometry/gen/collision", False),
        set = lambda self, value : set_and_erase_on_false("geometry/gen/collision", value, "geometry/gen/collision"),
    ) # type: ignore

    navigation: bpy.props.BoolProperty(
        name = "Generate Navigation",
        description = "Generate navigation region from mesh.",
        get = lambda self : get_func("geometry/gen/navigation", False),
        set = lambda self, value : set_and_erase_on_false("geometry/gen/navigation", value, "geometry/gen/navigation"),
    ) # type: ignore

    occluder: bpy.props.BoolProperty(
        name = "Generate Occluder",
        description = "Generate occluder from mesh.",
        get = lambda self : get_func("geometry/gen/occluder", False),
        set = lambda self, value : set_and_erase_on_false("geometry/gen/occluder", value, "geometry/gen/occluder"),
    ) # type: ignore

    mesh_data: bpy.props.PointerProperty(type=B2GDPropMesh) # type: ignore
    collision_data: bpy.props.PointerProperty(type=B2GDPropCollision) # type: ignore
    navigation_data: bpy.props.PointerProperty(type=B2GDPropNavigationRegion) # type: ignore



######## ---------- Main props ---------- ########


class B2GDPropData(bpy.types.PropertyGroup):
    mode: bpy.props.EnumProperty(
        name = "Mode",
        description = "Select mode.",
        items = [
            ("replace_by_scene", "Replace by scene", "Replaces this object with a scene.", 0),
            ("geometry", "Geometry", "Geometry options.", 1),
            ("curve", "Curve", "Create a Path3D node based on this curve.", 2)
        ],
        get = lambda self : get_func("mode", 0),
        set = lambda self, value : set_func("mode", value),
    ) # type: ignore

    replace_by_scene: bpy.props.PointerProperty(type = B2GDPropReplaceByScene) # type: ignore

    curve: bpy.props.PointerProperty(type = B2GDPropCurve) # type: ignore

    geometry: bpy.props.PointerProperty(type = B2GDPropGeometry) # type: ignore



classes = [
    B2GDPropReplaceByScene,

    B2GDPropCurve,

    # ----- mesh instance props ----- #
    B2GDPropMesh,

    # ----- collision props ----- #

    # collision bodies
    B2GDPropBodyStatic,
    B2GDPropBodyAnimatable,
    B2GDPropBodyRigid,
    B2GDPropBodyCharacter,
    B2GDPropBodyArea,

    # collision shapes
    B2GDPropShapeTrimesh,
    B2GDPropShapeConvex,

    B2GDPropCollision,
    
    # ----- navigation props ----- #
    B2GDPropNavigationRegion,

    # ----- geometry props ----- #
    B2GDPropGeometry,

    # B2GDPropProperties,

    B2GDPropData,
]
