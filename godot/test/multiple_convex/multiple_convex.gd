extends Node3D

@onready var mesh: MeshInstance3D = $"Mesh"


func _ready() -> void:
	mesh.create_multiple_convex_collisions()

	# created static body ends with "_col"
