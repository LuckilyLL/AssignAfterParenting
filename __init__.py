bl_info = {
    "name": "Assign After Parenting",
    "author": "Luckily",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "3D View > Pose > Parent",
    "description": "Auto assign the vertex group after parenting objects",
    "category": "Rigging"}


import bpy

class AssignAfterParenting(bpy.types.Operator):
    """Set selected objects's parent to the active bone and assign the vertex group with weight"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.assign_after_parenting"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Set Parent and Assign Vertex Group"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    def execute(self, context):        # execute() is called when running the operator.
        targetBone = bpy.context.active_bone
        boneName = targetBone.name
        selectedObjs = bpy.context.selected_objects
        selectedMeshs = []

        for obj in selectedObjs:
            if obj.type == 'MESH':
                selectedMeshs.append(obj)        
        bpy.types.VIEW3D_MT_edit_armature_parent
        bpy.ops.object.parent_set(type='ARMATURE_NAME', xmirror=False, keep_transform=True)
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        for obj in selectedMeshs:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.object.vertex_group_set_active(group=boneName)
            # TODO: check and set weightbl_icon = "GROUP_VERTEX"
            bpy.ops.object.vertex_group_assign()
            bpy.ops.object.mode_set(mode='OBJECT')
        return {'FINISHED'}            # Lets Blender know the operator finished successfully.

def menu_func(self, context): 
    layout = self.layout
    layout.operator(AssignAfterParenting.bl_idname, text="Assign After Parenting", icon="GROUP_VERTEX")

def register():
    bpy.utils.register_class(AssignAfterParenting)
    bpy.types.VIEW3D_MT_pose_context_menu.append(menu_func)


def unregister():
    bpy.utils.unregister_class(AssignAfterParenting)
    bpy.types.VIEW3D_MT_pose_context_menu.remove(menu_func)

# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()