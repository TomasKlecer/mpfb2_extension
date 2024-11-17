from mpfb.services.logservice import LogService
from mpfb.services.locationservice import LocationService
from mpfb._classmanager import ClassManager
import bpy

_LOG = LogService.get_logger("exportpanel.export_ue5")

class MPFB_OT_ExportUE5_Operator(bpy.types.Operator):
    """Opens export window with UE5 compatible settings"""
    bl_idname = "mpfb.export_ue5"
    bl_label = "Export"
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
            self.report({'ERROR'}, "No mesh 'Human' found.")
            return {'CANCELLED'}

        if not armature_root:
            self.report({'ERROR'}, "No armature 'root' found. Apply UE5 rig.")
            return {'CANCELLED'}

        # Select mesh and armature
        bpy.ops.object.select_all(action='DESELECT')
        mesh_Human.select_set(True)
        armature_root.select_set(True)
        context.view_layer.objects.active = armature_root

        # Open FBX export window with UE5 settings
        bpy.ops.export_scene.fbx(
            'INVOKE_DEFAULT',
            use_selection=True,
            add_leaf_bones=False,
            primary_bone_axis='X',
            secondary_bone_axis='-Z'
        )

        self.report({'INFO'}, "Exporting character to UE5")
        return {'FINISHED'}

ClassManager.add_class(MPFB_OT_ExportUE5_Operator)