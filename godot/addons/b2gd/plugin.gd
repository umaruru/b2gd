@tool
extends EditorPlugin

enum Mode {
	REPLACE_BY_SCENE = 0,
	GEOMETRY = 1,
	CURVE = 2,
}

enum GeometryRemoveMode {
	REPLACE_BY_NODE = 0,
	FREE = 1,
}

enum GenAddAs {
	CHILD = 0,
	SIBLING = 1,
}

enum BodyType {
	STATIC = 0,
	ANIMATABLE = 1,
	RIGID = 2,
	CHARACTER = 3,
	AREA = 4,
	NONE = 5,
}

enum ShapeType {
	TRIMESH = 0,
	CONVEX = 1,
	NONE = 2,
}

enum ConvexMode {
	SINGLE = 0,
	SIMPLIFIED = 1,
	MULTIPLE = 2,
}

const PROP_NAME = &"b2gd_data__"

var gltf_ext: GLTFDocumentExtension
var post_plugin: EditorScenePostImportPlugin

func _enter_tree() -> void:
	gltf_ext = B2GDGLTFExt.new()
	GLTFDocument.register_gltf_document_extension(gltf_ext)

	post_plugin = B2GDPostImportPlugin.new()
	add_scene_post_import_plugin(post_plugin)

	print("B2GD (Blender to Godot) plugin enabled.")


func _exit_tree() -> void:
	GLTFDocument.unregister_gltf_document_extension(gltf_ext)
	gltf_ext = null
	
	remove_scene_post_import_plugin(post_plugin)
	post_plugin = null

	print("B2GD (Blender to Godot) plugin disabled.")


class B2GDGLTFExt extends GLTFDocumentExtension:
	# function order

	# _import_preflight
	# _get_supported_extensions
	# _parse_node_extensions
	# _import_post_parse
	# _import_pre_generate
	# _generate_scene_node
	# _import_node
	# _import_post

	func _import_node(state: GLTFState, gltf_node: GLTFNode, json: Dictionary, node: Node) -> Error:
		var extras := json.get("extras", {}) as Dictionary

		if not extras.has(PROP_NAME):
			return OK
		
		var data := extras.get(PROP_NAME, {}) as Dictionary
		var gen_occluder := data.get("geometry/gen/occluder", false) as bool

		if gen_occluder:
			node.name += " -occ"
		
		return OK

	pass


class B2GDPostImportPlugin extends EditorScenePostImportPlugin:
	func swap_node(node: Node, with: Node) -> void:
		# node.replace_by(scene, true) # doesn't work. I think it's for the editor?

		var parent := node.get_parent()
		var owner := node.owner
		var name := node.name

		node.set_name(name + "###?_removing__?###")
		with.name = name

		if parent != null:
			parent.add_child(with)
		
		if owner == node:
			# does this even happen???
			owner = with
		
		with.owner = owner
		
		for child in node.get_children():
			# child.reparent(scene, true) # doesn't work outside tree
			child.owner = null
			node.remove_child(child)
			with.add_child(child)
			child.owner = owner
		
		for meta in node.get_meta_list():
			with.set_meta(meta, node.get_meta(meta))
		
		for group in node.get_groups():
			with.add_to_group(group)



	func mode_replace_by_scene(data: Dictionary, node: Node) -> void:
		var path := data.get("replace_by_scene/path", "") as String
		var ignore_position := data.get("replace_by_scene/position", false) as bool
		var ignore_rotation := data.get("replace_by_scene/rotation", false) as bool
		var ignore_scale := data.get("replace_by_scene/scale", false) as bool

		if not ResourceLoader.exists(path, "PackedScene"):
			push_error('Failed importing B2GD data. Could not load scene "%s".' % path)
			return

		var scene = (ResourceLoader.load(path) as PackedScene).instantiate()
		
		if scene is Node3D:
			if not ignore_position: scene.position = (node as Node3D).position
			if not ignore_rotation: scene.rotation = (node as Node3D).rotation
			if not ignore_scale: scene.scale = (node as Node3D).scale

		swap_node(node, scene)
		node.free()
		
		# prints(scene.name, scene.get_class(), scene.get_parent().name, path)
	

	func apply_geometry_properties(node: MeshInstance3D, data: Dictionary) -> void:
		pass
	

	func create_mesh_collision(node: MeshInstance3D, data: Dictionary, as_sibling: bool) -> void:
		var body_type := data.get("geometry/gen/collision/body_type", 0) as BodyType
		var shape_type := data.get("geometry/gen/collision/shape_type", 0) as ShapeType

		if body_type == BodyType.NONE and shape_type == ShapeType.NONE:
			push_warning('Node "%s" has Generate Collision enabled but Body Type is Shape Only and Shape Type is No Shape. No collision was created.' % node.name)
			return
		
		# create body

		var body: CollisionObject3D

		match body_type:
			BodyType.STATIC:
				var prop_clv := data.get("geometry/gen/collision/body/static/constant_linear_velocity", [0, 0, 0]) as Array
				var prop_cav := data.get("geometry/gen/collision/body/static/constant_angular_velocity", [0, 0, 0]) as Array
				
				body = StaticBody3D.new()
				var sbody := body as StaticBody3D
				sbody.constant_linear_velocity = Vector3(prop_clv[0], prop_clv[1], prop_clv[2])
				sbody.constant_angular_velocity = Vector3(prop_cav[0], prop_cav[1], prop_cav[2])
			
			BodyType.ANIMATABLE:
				var prop_sync_phys := data.get("geometry/gen/collision/body/animatable/sync_to_physics", true) as bool
				
				body = AnimatableBody3D.new()
				var abody := body as AnimatableBody3D
				abody.sync_to_physics = prop_sync_phys

			BodyType.RIGID:
				var prop_mass := data.get("geometry/gen/collision/body/rigid/mass", 1.0) as float
				var prop_gravity_scale := data.get("geometry/gen/collision/body/rigid/gravity_scale", 1.0) as float
				var prop_sleeping := data.get("geometry/gen/collision/body/rigid/sleeping", false) as bool
				var prop_can_sleep := data.get("geometry/gen/collision/body/rigid/can_sleep", true) as bool
				var prop_lock_rot := data.get("geometry/gen/collision/body/rigid/lock_rotation", false) as bool
				var prop_freeze := data.get("geometry/gen/collision/body/rigid/freeze", false) as bool
				var prop_freeze_mode := data.get("geometry/gen/collision/body/rigid/freeze_mode", 0) as int

				body = RigidBody3D.new()
				var rbody := body as RigidBody3D
				rbody.mass = prop_mass
				rbody.gravity_scale = prop_gravity_scale
				rbody.sleeping = prop_sleeping
				rbody.can_sleep = prop_can_sleep
				rbody.lock_rotation = prop_lock_rot
				rbody.freeze = prop_freeze
				rbody.freeze_mode = prop_freeze_mode as RigidBody3D.FreezeMode

			BodyType.CHARACTER:
				# no props yet
				body = CharacterBody3D.new()
			
			BodyType.AREA:
				var prop_monitoring := data.get("geometry/gen/collision/body/area/monitoring", true) as bool
				var prop_monitorable := data.get("geometry/gen/collision/body/area/monitorable", true) as bool
				var prop_priority := data.get("geometry/gen/collision/body/area/priority", 0) as int

				body = Area3D.new()
				var area := body as Area3D
				area.monitoring = prop_monitoring
				area.monitorable = prop_monitorable
				area.priority = prop_priority
			
			BodyType.NONE:
				body = null

			_:
				push_error("Could not create CollisionObject for node %s. Invalid body type: %d" % [node.name, body_type])

		if body != null:
			body.name = node.name + "_col"

			var prop_disable_mode := data.get("geometry/gen/collision/disable_mode", 0) as int
			var prop_col_layer_1_16 := data.get("geometry/gen/collision/collision_layer_1_16", 1) as int
			var prop_col_layer_17_32 := data.get("geometry/gen/collision/collision_layer_17_32", 0) as int
			var prop_col_mask_1_16 := data.get("geometry/gen/collision/collision_mask_1_16", 1) as int
			var prop_col_mask_17_32 := data.get("geometry/gen/collision/collision_mask_17_32", 0) as int
			var prop_col_priority := data.get("geometry/gen/collision/collision_priority", 1.0) as float
			var prop_input_ray_pickable := data.get("geometry/gen/collision/input_ray_pickable", true) as bool
			var prop_input_capture_on_drag := data.get("geometry/gen/collision/input_capture_on_drag", false) as bool
			
			body.disable_mode = prop_disable_mode
			body.collision_layer = prop_col_layer_1_16 | (prop_col_layer_17_32 << 16)
			body.collision_mask = prop_col_mask_1_16 | (prop_col_mask_17_32 << 16)
			body.collision_priority = prop_col_priority
			body.input_ray_pickable = prop_input_ray_pickable
			body.input_capture_on_drag = prop_input_capture_on_drag
			
			if body is StaticBody3D or body is RigidBody3D:
				var prop_physics_material_path := data.get("geometry/gen/collision/physics_material_path", "") as String
				var phys_path := prop_physics_material_path

				if not phys_path.is_empty() and ResourceLoader.exists(phys_path, "PhysicsMaterial"):
					var phys_mat = ResourceLoader.load(phys_path, "PhysicsMaterial")
					body.physics_material_override = phys_mat

		# create shapes

		var shapes: Array[CollisionShape3D] = []

		var shape_disabled := data.get("geometry/gen/collision/shape_disabled", false) as bool

		var mesh := (node as MeshInstance3D).mesh

		if mesh == null:
			push_error("Node \"%s\" doesn't have a mesh. Can't create collision shapes.")
			
		else:
			match shape_type:
				ShapeType.TRIMESH:
					var prop_backface_col := data.get("geometry/gen/collision/shape/trimesh/backface_collision", false) as bool
					
					var shape := mesh.create_trimesh_shape()
					shape.backface_collision = prop_backface_col
					
					var col_shape := CollisionShape3D.new()
					col_shape.name = "CollisionShape3D_Trimesh"
					col_shape.disabled = shape_disabled
					col_shape.shape = shape
					shapes.append(col_shape)
				
				ShapeType.CONVEX:
					var convex_mode := data.get("geometry/gen/collision/shape/convex/mode", 0) as ConvexMode

					if convex_mode == ConvexMode.SINGLE || convex_mode == ConvexMode.SIMPLIFIED:
						var shape = mesh.create_convex_shape(true, convex_mode == ConvexMode.SIMPLIFIED)

						var col_shape := CollisionShape3D.new()
						col_shape.name = "CollisionShape3D_Convex_" + ("Simplified" if convex_mode == ConvexMode.SIMPLIFIED else "Single")
						col_shape.disabled = shape_disabled
						col_shape.shape = shape
						shapes.append(col_shape)
					
					elif convex_mode == ConvexMode.MULTIPLE:
						# TODO: mesh convex decomposition settings
						(node as MeshInstance3D).create_multiple_convex_collisions()
						var sbody := node.get_child(node.get_child_count() - 1)
						
						# TODO: maybe remove "_col" from the end? who knows if they'll change it
						if sbody is StaticBody3D and sbody.name.ends_with("_col"):
							for child in sbody.get_children():
								if child is CollisionShape3D:
									child.disabled = shape_disabled
									child.name = "CollisionShape3D_Multiple"
									child.owner = null
									sbody.remove_child(child)
									shapes.append(child)
								else:
									push_error("Child is not CollisionShape3D (?)")
							
							sbody.free()
						else:
							push_error("Multiple convex shapes could not be created (??)")
				
				ShapeType.NONE:
					shapes = []

				_:
					push_error("Can't create collision shape for node \"%s\". Invalid shape type: %d" % [node.name, shape_type])
		
		var add_as := data.get("geometry/gen/collision/add_as", 0) as GenAddAs
		as_sibling = as_sibling or add_as == GenAddAs.SIBLING
		
		var parent := node.get_parent() if as_sibling  else node
		var owner := node.owner
		var index := (node.get_index() + 1) if as_sibling else -1
		var xform := node.transform if as_sibling else Transform3D()

		if body != null:
			parent.add_child(body)
			parent.move_child(body, index)
			body.owner = owner
			body.transform = xform
			parent = body
		
		for shape in shapes:
			parent.add_child(shape)
			shape.owner = owner
			if as_sibling and body == null:
				shape.transform = xform


	func create_navigation_region(node: MeshInstance3D, data: Dictionary, as_sibling: bool) -> void:
		var prop_add_as := data.get("geometry/gen/navigation/add_as")
		var prop_enabled := data.get("geometry/gen/navigation/enabled", true) as bool
		var prop_use_edge_conn := data.get("geometry/gen/navigation/use_edge_connections", true) as bool
		var prop_layers_1_16 := int(data.get("geometry/gen/navigation/navigation_layers_1_16", 1))
		var prop_layers_17_32 := int(data.get("geometry/gen/navigation/navigation_layers_17_32", 0))
		var prop_enter_cost := data.get("geometry/gen/navigation/enter_cost", 0.0) as float
		var prop_travel_cost := data.get("geometry/gen/navigation/travel_cost", 1.0) as float

		var nav_mesh := NavigationMesh.new()
		nav_mesh.create_from_mesh(node.mesh)

		var nav_region := NavigationRegion3D.new()
		nav_region.navigation_mesh = nav_mesh
		nav_region.enabled = prop_enabled
		nav_region.use_edge_connections = prop_use_edge_conn
		nav_region.navigation_layers = prop_layers_1_16 | (prop_layers_17_32 << 16)
		nav_region.enter_cost = prop_enter_cost
		nav_region.travel_cost = prop_travel_cost

		as_sibling = as_sibling or prop_add_as == GenAddAs.SIBLING

		var parent := node.get_parent() if as_sibling else node
		var owner := node.owner
		var index := (node.get_index() + 1) if as_sibling else -1
		var xform := node.transform if as_sibling else Transform3D()

		parent.add_child(nav_region)
		parent.move_child(nav_region, index)
		nav_region.owner = owner
		nav_region.transform = xform


	func mode_geometry(data: Dictionary, node: Node) -> void:

		# make sure node is MeshInstance
		if node is not MeshInstance3D:
			push_error("Node \"%s\" is not a Mesh. Can't set properties or create colliders and navigation regions." % node.name)
			return
		
		var mesh := data.get("geometry/mesh", true) as bool
		var mesh_remove_mode := data.get("geometry/mesh_remove_mode", 0) as GeometryRemoveMode
		
		var collision := data.get("geometry/gen/collision", false) as bool
		var navigation := data.get("geometry/gen/navigation", false) as bool

		var gen_as_sibling: bool = not mesh and mesh_remove_mode == GeometryRemoveMode.FREE
	
		if collision:
			create_mesh_collision(node, data, gen_as_sibling)
		
		if navigation:
			create_navigation_region(node, data, gen_as_sibling)

		# set geometry props

		if mesh:
			var prop_layers_1_10 := int(data.get("geometry/mesh/layers_1_10", 1))
			var prop_layers_11_20 := int(data.get("geometry/mesh/layers_11_20", 0))
			var prop_transparency := data.get("geometry/mesh/transparency", 0) as float
			var prop_cast_shadow := int(data.get("geometry/mesh/cast_shadow", 1))
			var prop_ignore_occlusion_culling := data.get("geometry/mesh/ignore_occlusion_culling", false) as bool
			var prop_gi_mode := int(data.get("geometry/mesh/gi_mode", 1))
			var prop_gi_lightmap_texel_scale := data.get("geometry/mesh/gi_lightmap_textel_scale", 1.0) as float

			var meshi := node as MeshInstance3D
			meshi.layers = prop_layers_1_10 | (prop_layers_11_20 << 10)
			meshi.transparency = prop_transparency
			meshi.cast_shadow = prop_cast_shadow
			meshi.ignore_occlusion_culling = prop_ignore_occlusion_culling
			meshi.gi_mode = prop_gi_mode
			meshi.gi_lightmap_texel_scale = prop_gi_lightmap_texel_scale
		
		else:
			if mesh_remove_mode == GeometryRemoveMode.REPLACE_BY_NODE:
				var new_node = Node3D.new()
				new_node.transform = node.transform
				swap_node(node, new_node)
			
			node.free()

		
	func process_node(node: Node) -> void:
		for child in node.get_children():
			process_node(child)

		var extras := node.get_meta(&"extras", {}) as Dictionary

		if extras.is_empty():
			return
		
		var data := extras.get(PROP_NAME, {}) as Dictionary

		if data.is_empty():
			node.remove_meta(PROP_NAME)
			return

		var mode: Mode = data.get("mode", -1) as Mode
		
		match mode:
			Mode.REPLACE_BY_SCENE:
				mode_replace_by_scene(data, node)
			
			Mode.GEOMETRY:
				mode_geometry(data, node)
			
			Mode.CURVE:
				pass
			
			_:
				push_error("Failed importing B2GD data. Invalid mode '%d'" % mode)
		
		extras.erase(PROP_NAME)
		
		if is_instance_valid(node) and extras.is_empty():
			node.remove_meta(&"extras")


	func _post_process(scene: Node) -> void:
		process_node(scene)
