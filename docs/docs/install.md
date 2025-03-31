# Installing B2GD

To install B2GD you need to download the Blender extension and the Godot plugin.
Check the releases page. TODO: add link


## Installing the Godot plugin

- Download the godot plugin zip file from the github releases page.
- Extract the downloaded file.
- Copy the extracted b2gd folder to the add-on folder in your project's files. It
should look like `project_root/addons/b2gd/`
- Enable B2GD in Project Settings > Plugins.

TODO: add image showing folder structure

TODO: add image of Project Settings > Plugins ... in the default theme 😔

You might need to reimport some files if they don't get updated automatically.

TODO: put in asset lib and explain how to install from there

More information: <a href="https://docs.godotengine.org/en/stable/tutorials/plugins/editor/installing_plugins.html" target="_blank">Installing Plugins</a> on Godot Documentation.


## Installing the Blender extension

- Download the blender extension zip file from the github releases page TODO: add link.
- In Blender, go to Edit > Preferences.
- Go to the "Get Extensions" tab.
- Click the arrow on the top right and select "Install from Disk".
- Select the downloaded file in the file explorer.

TODO: add image with preferences panel,arrow clicked, menu and "Install from Disk" hightlighted

B2GD should be visible in the extensions list.

- Click on the arrow on the right side.
- Check the "Add-on enabled" checkbox.

TODO: add image showing the menu above

The panel B2GD should be present on the 3D view sidebar. You can toggle the sidebar
with the default **N** shortcut or going to View > Sidebar.

TODO: add image showing B2GD panel

Hopefully I'll be able to put it on the Blender extensions thing. Installing would
be so much easier.

More information: <a href="https://docs.blender.org/manual/en/latest/editors/preferences/extensions.html" target="_blank">Get Extensions</a> on Blender Manual.


## Blender export settings

The way the addon works is by adding custom properties to the objects. These properties
are read in Godot during the import process and nodes are configured accordingly.

Blender doesn't export custom properties by default. You have to enable it on the
GLTF export settings.

- Go to File > Export > glTF 2.0 (.glb/.gltf).
- On the right panel, expand "Include" and check "Custom Properties".

You may want to check "Remember Export Settings" so you won't need to do the steps above
everytime you open the file. Remembering settings is required when using blend files in your
project instead of gltf.

By the way, export settings are file based. You have to do the steps above in every different file.

!!! tip
    A button was added at the top of the B2GD panel to enable Custom Properties on
    the GLTF Export Settings. The button only shows when custom properties aren't
    enabled.
