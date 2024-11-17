from mpfb.services.logservice import LogService
from mpfb.services.locationservice import LocationService
from mpfb._classmanager import ClassManager
import bpy

_LOG = LogService.get_logger("exportpanel.rescale_ue5")

class MPFB_OT_RescaleUE5_Operator(bpy.types.Operator):
    """Rescale model and armature so it works with UE5 mannequin"""
    bl_idname = "mpfb.rescale_ue5"
    bl_label = "Rescale"
    bl_options = {'REGISTER'}

    def execute(self, context):
        # Find mesh
        mesh_Human = None
        for obj in bpy.data.objects:
            if obj.type == 'MESH' and "Human" in obj.name:
                mesh_Human = obj
                break

        # Find armature
        armature_root = None
        for obj in bpy.data.objects:
            if obj.type == 'ARMATURE' and "root" in obj.name:
                armature_root = obj
                break

        # Check if they exist
        if not mesh_Human:
            self.report({'ERROR'}, "No mesh object with 'Human' in its name found.")
            return {'CANCELLED'}

        if not armature_root:
            self.report({'ERROR'}, "No armature object with 'root' in its name found.")
            return {'CANCELLED'}

        # Scale mesh 100x in Object Mode
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        mesh_Human.select_set(True)
        context.view_layer.objects.active = mesh_Human
        bpy.ops.transform.resize(value=(100, 100, 100))

        # Snap 3D Cursor to World Origin
        bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)

        # Scale armature 100x in Edit Mode relative to 3D Cursor
        bpy.ops.object.select_all(action='DESELECT')
        armature_root.select_set(True)
        context.view_layer.objects.active = armature_root
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.armature.select_all(action='SELECT')
        bpy.ops.transform.resize(value=(100, 100, 100), center_override=(0.0, 0.0, 0.0))
        bpy.ops.object.mode_set(mode='OBJECT')

        # Scale Armature root by 0.01x in Object Mode
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        armature_root.select_set(True)
        context.view_layer.objects.active = armature_root
        bpy.ops.transform.resize(value=(0.01, 0.01, 0.01))

        self.report({'INFO'}, "Object succesfuly rescaled for UE5 export.")
        return {'FINISHED'}

ClassManager.add_class(MPFB_OT_RescaleUE5_Operator)