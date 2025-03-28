@tool
extends EditorPlugin

# var post_plugin: EditorScenePostImportPlugin
var gltf_ext: GLTFDocumentExtension

func _enter_tree() -> void:
	# post_plugin = PostImportPlugin.new()
	# add_scene_post_import_plugin(post_plugin)

	gltf_ext = GltfSuffixExt.new()
	GLTFDocument.register_gltf_document_extension(gltf_ext)


func _exit_tree() -> void:
	# remove_scene_post_import_plugin(post_plugin)
	# post_plugin = null

	GLTFDocument.unregister_gltf_document_extension(gltf_ext)
	gltf_ext = null


# class PostImportPlugin extends EditorScenePostImportPlugin:
#	# Adding suffixes don't work on post import.

# 	func process_node(node: Node) -> void:
# 		for child in node.get_children():
# 			process_node(child)
		
# 		var extras := node.get_meta("extras", {}) as Dictionary

# 		if not node is MeshInstance3D or extras.is_empty():
# 			return

# 		var suffixes_string := extras.get("suffixes", "") as String

# 		var split = suffixes_string.split(",", false)

# 		for suffix in split:
# 			node.name += suffix


# 	func _post_process(node: Node) -> void:
# 		process_node(node)




class GltfSuffixExt extends GLTFDocumentExtension:
	func _import_node(state: GLTFState, gltf_node: GLTFNode, json: Dictionary, node: Node) -> Error:
		var extras := json.get("extras", {}) as Dictionary
		
		prints(node.get_class(), " :: ", node.name)

		if not extras.has("suffixes"):
			return OK
		
		var suffix_string := extras.get("suffixes", "") as String
		var split := suffix_string.split(",", false)

		for suffix in split:
			node.name += suffix
		
		return OK
