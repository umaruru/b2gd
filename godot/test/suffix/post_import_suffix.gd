@tool
extends EditorScenePostImport

func _post_import(scene: Node) -> Object:
	_iterate(scene)
	return scene

func _iterate(node: Node) -> void:
	print(node.get_class())

	if node is MeshInstance3D:
		node.name += "-col"
	
	for child in node.get_children():
		_iterate(child)
