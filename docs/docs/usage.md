# Usage

B2GD is located at the 3D view on the right panel (default shortcut `N`).

TODO: add b2gd panel image

It can be added to an object individually or copied to other objects.

TODO: 

- [Replace by scene](#replace-by-scene)
- [Geometry options](#geometry-options)

-----

## Replace by scene

This mode replaces the object by a scene.

- `Path or UID`: The scene path or UID. You can get this by going in the filesystem
tab in Godot and selecting `Copy Path` or `Copy UID`.

TODO: Add image with these, crossing `copy absolute path`

- `Discard position`: The object position will be ignored and the scene will be placed
at `[0, 0, 0]`.

- `Discard rotation`: The object rotation will be ignored and the scene will have a rotation
of `[0, 0, 0]`.

- `Discard scale`: The object rotation will be ignored and the scene will have a scale of
`[1, 1, 1]`.

!!! note
    All discard options are applied to the scene local coordinates. If the parent has a
    transform, it will be propagated to the scene as well.
    A [`top_level`](https://docs.godotengine.org/en/4.4/classes/class_node3d.html#class-node3d-property-top-level) property may be added in the future.

!!! note
    The plugin tries to copy all the data from the replaced object to the instanced scene: metadata,
    children, groups, etc.
    If there's other user cases where the data should be copied, please open an issue.

-----

## Geometry options

This mode allows to set Node properties to Mesh objects, as well as creating collider, 
navigation region and occluder.

### Mesh Instance

The `Mesh` checkbox allows to set
[`VisualInstance3D`](https://docs.godotengine.org/en/4.4/classes/class_visualinstance3d.html)
and [`GeometryInstance3D`](https://docs.godotengine.org/en/4.4/classes/class_geometryinstance3d.html)
properties.

It is enabled by default. It can be disabled when a MeshInstance3D is not
needed, but collision, navigation or occluder are. When disabled, the property `Remove Mode`
becomes available, where you can choose between:

- **`Remove by Node3D`**: The MeshInstance3D is replaced by a Node3D. Children are kept.
- **`Free Node`**: The MeshInstance3D and its children are removed.

!!! note
    If `Remove Node` option is set to `Free Node`, generated colliders and navigation
    regions will be added as sibling, independent of their `Add as` property.

List of Godot properties:

| property | Godot documentation |
| --- | --- |
| Layers | [VisualInstance3D.layers](https://docs.godotengine.org/en/4.4/classes/class_visualinstance3d.html#class-visualinstance3d-property-layers) |
| Transparency | [GeometryInstance3D.transparency](https://docs.godotengine.org/en/4.4/classes/class_geometryinstance3d.html#class-geometryinstance3d-property-transparency) |
| Cast Shadow | [GeometryInstance3D.cast_shadow](https://docs.godotengine.org/en/4.4/classes/class_geometryinstance3d.html#class-geometryinstance3d-property-cast-shadow) |
| Ignore Occlusion Culling | [GeometryInstance3D.ignore_occlusion_culling](https://docs.godotengine.org/en/4.4/classes/class_geometryinstance3d.html#class-geometryinstance3d-property-ignore-occlusion-culling) |
| GI Mode | [GeometryInstance3D.gi_mode](https://docs.godotengine.org/en/4.4/classes/class_geometryinstance3d.html#class-geometryinstance3d-property-gi-mode) |
| Lightmap Textel Scale | [GeometryInstance3D.gi_lightmap_texel_scale](https://docs.godotengine.org/en/4.4/classes/class_geometryinstance3d.html#class-geometryinstance3d-property-gi-lightmap-texel-scale) |

### Generate Collision

The `Generate Collision` checkbox enables creating collision bodies and shapes. Like `-col` and `-convcol`
[suffixes](https://docs.godotengine.org/en/4.4/tutorials/assets_pipeline/importing_3d_scenes/node_type_customization.html).

You can choose what type of body (CollisionObject3D) to use as collider, if the shape
is trimesh (ConcavePolygonShape3D) or convex (ConvexPolygonShape3D) and several properties.

The `Add as` property determines if the body and shapes will be added as sibling
or child of the MeshInstance3D node.

-----

#### Body

There are several body types available. There's also the `Only Shapes` option, which
creates collision shapes without a body.

List of Godot properties shared by all bodies:

| property | Godot documentation |
| --- | --- |
| Disable Mode | [CollisionObject3D.disable_mode](https://docs.godotengine.org/en/4.4/classes/class_collisionobject3d.html#class-collisionobject3d-property-disable-mode) |
| Collision Layer | [CollisionObject3D.collision_layer](https://docs.godotengine.org/en/4.4/classes/class_collisionobject3d.html#class-collisionobject3d-property-collision-layer) |
| Collision Mask | [CollisionObject3D.collision_mask](https://docs.godotengine.org/en/4.4/classes/class_collisionobject3d.html#class-collisionobject3d-property-collision-mask) |
| Priority | [CollisionObject3D.collision_priority](https://docs.godotengine.org/en/4.4/classes/class_collisionobject3d.html#class-collisionobject3d-property-collision-priority) |
| Ray Pickable | [CollisionObject3D.input_ray_pickable](https://docs.godotengine.org/en/4.4/classes/class_collisionobject3d.html#class-collisionobject3d-property-input-ray-pickable) |
| Capture on Drag | [CollisionObject3D.input_capture_on_drag](https://docs.godotengine.org/en/4.4/classes/class_collisionobject3d.html#class-collisionobject3d-property-input-capture-on-drag) |

Body types:

##### Static Body

Creates a [StaticBody3D](https://docs.godotengine.org/en/4.4/classes/class_staticbody3d.html).

| property | Godot documentation |
| --- | --- |
| Constant Linear Velocity | [StaticBody3D.constant_linear_velocity](https://docs.godotengine.org/en/4.4/classes/class_staticbody3d.html#class-staticbody3d-property-constant-linear-velocity) |
| Constant Angular Velocity | [StaticBody3D.constant_angular_velocity](https://docs.godotengine.org/en/4.4/classes/class_staticbody3d.html#class-staticbody3d-property-constant-angular-velocity) |
| Physics Material Override Path | [StaticBody3D.physics_material_override](https://docs.godotengine.org/en/4.4/classes/class_staticbody3d.html#class-staticbody3d-property-physics-material-override) |

!!! note
    `Physics Material Override Path` should be a path or uid of a PhysicsMaterial
    saved to the disk as a resource.

##### Animatable Body

Creates an [AnimatableBody3D](https://docs.godotengine.org/en/4.4/classes/class_animatablebody3d.html).

| property | Godot documentation |
| --- | --- |
| Sync to Physics | [AnimatableBody3D.sync_to_physics](https://docs.godotengine.org/en/4.4/classes/class_animatablebody3d.html#class-animatablebody3d-property-sync-to-physics) |
| Physics Material Override Path | [StaticBody3D.physics_material_override](https://docs.godotengine.org/en/4.4/classes/class_staticbody3d.html#class-staticbody3d-property-physics-material-override) |

!!! note
    `Physics Material Override Path` should be a path or uid of a PhysicsMaterial
    saved to the disk as a resource.

##### Rigid Body

Creates a [RigidBody3D](https://docs.godotengine.org/en/4.4/classes/class_rigidbody3d.html).

| property | Godot documentation |
| --- | --- |
| Mass | [StaticBody3D.mass](https://docs.godotengine.org/en/4.4/classes/class_rigidbody3d.html#class-rigidbody3d-property-mass) |
| Gravity Scale | [StaticBody3D.gravity_scale](https://docs.godotengine.org/en/4.4/classes/class_rigidbody3d.html#class-rigidbody3d-property-gravity-scale) |
| Sleeping | [StaticBody3D.sleeping](https://docs.godotengine.org/en/4.4/classes/class_rigidbody3d.html#class-rigidbody3d-property-sleeping) |
| Can Sleep | [StaticBody3D.can_sleep](https://docs.godotengine.org/en/4.4/classes/class_rigidbody3d.html#class-rigidbody3d-property-can-sleep) |
| Lock Rotation | [StaticBody3D.lock_rotation](https://docs.godotengine.org/en/4.4/classes/class_rigidbody3d.html#class-rigidbody3d-property-lock-rotation) |
| Freeze | [StaticBody3D.freeze](https://docs.godotengine.org/en/4.4/classes/class_rigidbody3d.html#class-rigidbody3d-property-freeze) |
| Freeze Mode | [StaticBody3D.freeze_mode](https://docs.godotengine.org/en/4.4/classes/class_rigidbody3d.html#class-rigidbody3d-property-freeze-mode) |
| Physics Material Override Path | [StaticBody3D.physics_material_override](https://docs.godotengine.org/en/4.4/classes/class_rigidbody3d.html#class-rigidbody3d-property-physics-material-override) |

!!! note
    `Physics Material Override Path` should be a path or uid of a PhysicsMaterial
    saved to the disk as a resource.

##### Character Body

Creates a [CharacterBody3D](https://docs.godotengine.org/en/4.4/classes/class_characterbody3d.html).

!!! warning
    Currently there are no properties for Character Body

##### Area

Creates an [Area3D](https://docs.godotengine.org/en/4.4/classes/class_area3d.html).

| property | Godot documentation |
| --- | --- |
| Monitoring | [Area3D.monitoring](https://docs.godotengine.org/en/4.4/classes/class_area3d.html#class-area3d-property-monitoring) |
| Monitorable | [Area3D.monitorable](https://docs.godotengine.org/en/4.4/classes/class_area3d.html#class-area3d-property-monitorable) |
| Priority | [Area3D.priority](https://docs.godotengine.org/en/4.4/classes/class_area3d.html#class-area3d-property-priority) |

##### Shape Only

Doesn't create a CollisionObject3D. Shapes are created and added accordingly.

-----

#### Shape

Creates a CollisionShape3D node. The shape can a ConcavePolygonShape3D (trimesh)
or a ConvexPolygonShape3D (convex).

The option `No Shape` will skip the generation of shapes.

##### Trimesh

Creates a [ConcavePolygonShape3D](https://docs.godotengine.org/en/4.4/classes/class_concavepolygonshape3d.html).

| property | Godot documentation |
| --- | --- |
| Backface Collision | [ConcavePolygonShape3D.backface_collision](https://docs.godotengine.org/en/4.4/classes/class_concavepolygonshape3d.html#class-concavepolygonshape3d-property-backface-collision) |
| Shape Disabled | [CollisionShape3D.disabled](https://docs.godotengine.org/en/4.4/classes/class_collisionshape3d.html#class-collisionshape3d-property-disabled) |

##### Convex

Creates a [ConvexPolygonShape3D](https://docs.godotengine.org/en/4.4/classes/class_convexpolygonshape3d.html).

There are three modes for the creation of convex shapes:

- **Single**: Creates a single collision shape. Fast but less accurate.
- **Simplified**: Similar to single. Can result in a simpler geometry, at the cost of accuracy.
- **Multiple**: Creates multiple collision shapes. Middle-ground between Single Convex and Concave polygon collision (trimesh).

| property | Godot documentation |
| --- | --- |
| Mode | see above |
| Shape Disabled | [CollisionShape3D.disabled](https://docs.godotengine.org/en/4.4/classes/class_collisionshape3d.html#class-collisionshape3d-property-disabled) |

##### No Shape

Does not create collision shapes.

!!! note
    If body is set to `Only Shapes` and shape is set to `No Shape`, the collision
    generation will be skipped.

-----


### Generate Navigation

The `Generate Navigation` checkbox enables the creation of a NavigationRegion, similar
to the `-navmesh` [suffix](https://docs.godotengine.org/en/4.4/tutorials/assets_pipeline/importing_3d_scenes/node_type_customization.html).

The `Add as` property determines if the NavigationRegion node will be added as child
of the MeshInstance3D or as its sibling.

The following Godot properties are available:

| property | Godot documentation |
| --- | --- |
| Enabled | [NavigationRegion3D.enabled](https://docs.godotengine.org/en/stable/classes/class_navigationregion3d.html#class-navigationregion3d-property-enabled) |
| Use Edge Connections | [NavigationRegion3D.use_edge_connections](https://docs.godotengine.org/en/stable/classes/class_navigationregion3d.html#class-navigationregion3d-property-use-edge-connections) |
| Navigation Layers | [NavigationRegion3D.navigation_layers](https://docs.godotengine.org/en/stable/classes/class_navigationregion3d.html#class-navigationregion3d-property-navigation-layers) |
| Enter Cost | [NavigationRegion3D.enter_cost](https://docs.godotengine.org/en/stable/classes/class_navigationregion3d.html#class-navigationregion3d-property-enter-cost) |
| Travel Cost | [NavigationRegion3D.travel_cost](https://docs.godotengine.org/en/stable/classes/class_navigationregion3d.html#class-navigationregion3d-property-travel-cost) |

-----


### Generate Occluder

Occluders can be generated from the mesh by selecting this option.

At the moment, the functionality to bake occluders
[is not exposed](https://github.com/godotengine/godot/pull/90590). The occluders
are generated by adding the [suffix](https://docs.godotengine.org/en/4.4/tutorials/assets_pipeline/importing_3d_scenes/node_type_customization.html)
`-occ` to the MeshInstance3D during import.

Please read the page
[Occlusion culling](https://docs.godotengine.org/en/4.4/tutorials/3d/occlusion_culling.html)
on the Godot documentation to learn more.
