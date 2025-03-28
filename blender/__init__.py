if "bpy" in locals():
    if "ui" in locals():
        import importlib
        importlib.reload(operators)
        importlib.reload(props)
        importlib.reload(ui)

import bpy

from . import operators
from . import props
from . import ui

classes = operators.classes + props.classes + ui.classes


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.b2gd_data__ = bpy.props.PointerProperty(type = props.B2GDPropData)
  

def unregister():
    del bpy.types.Scene.b2gd_data__
    
    for cls in classes:
        bpy.utils.unregister_class(cls)
    

# this helped to reload all scripts instead of just the __init.py__ file
# https://blender.stackexchange.com/questions/28504/blender-ignores-changes-to-python-scripts/28505#28505
