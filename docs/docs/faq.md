# FAQ

## Why use B2GD instead of [suffixes](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/node_type_customization.html)?

The suffixes are a quick way to create collisions, navigation and other stuff. They
can be applied en masse with batch renamer. But they lack customization.

B2GD was created to give more control of the scene. Changing properties directly
on blender means less back and forth between programs.

Another thing is, with suffixes, it seems only the last one is applied.
B2GD can generate collider, navigation and occlusion from a single mesh.

You can use suffixes with B2GD, but the output scene might be unexpected.

## My properties aren't being imported.

Make sure you enabled Include > Custom Properties in the gltf export settings. You
can use the button at the top of B2GD Panel to enable it. Read
[Blender Export Settings](./install.md#blender-export-settings).

!!! warning
    TODO: Actually I have to test this.

## What is the `b2gd_data__` I'm seeing everywhere?

`b2gd_data__` is the chosen name for the property where B2GD stuff is stored. You can see it
in Blender on the object's custom properties.

Scenes in Blender also gain a `b2gd_data__` property.
This was necessary to avoid creating a `b2gd_data__` property in all objects,
even if it was not being used.
The property on the scene is used as a "bridge" to the object property. Setters and getters are
in place to set the data directly in the object.

## Planned features

There are things to be done and fixed in the current feature set. But there
are some features I'd like to add to the plugin:

- **Path3D from Curve**. Save the bezier curve data and recreate as a Path3D.

- **More navigation**. Add more navigation stuff, like creating obstacles, links
and setting agent properties.

- **Multimesh**. Not exactly how it can be done, but have a way take data (vertices, empties, or
something else) and create a MultiMeshInstance with it.

- **Primitive collision shapes**. Create Godot's primitive collision shapes, like
Box, Sphere, Capsule, etc.


## TODO: add list of properties
