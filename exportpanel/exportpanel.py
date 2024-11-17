from mpfb._classmanager import ClassManager
from mpfb.services.logservice import LogService
from mpfb.services.uiservice import UiService
from mpfb.ui.abstractpanel import Abstract_Panel

_LOG = LogService.get_logger("ui.exportpanel")

class MPFB_PT_Export_Panel(Abstract_Panel):
    bl_label = "Export"
    bl_category = UiService.get_value("EXPORTCATEGORY")

    def _rescale_ue5(self, scene, layout):
        box = self._create_box(layout, "Rescale for UE5")
        box.label(text="Rescale mesh and armature to work correctly UE5 mannequin")
        box.operator("mpfb.rescale_ue5")

    def _export_ue5(self, scene, layout):
        box = self._create_box(layout, "Export to UE5")
        box.label(text="Select mesh and UE5 armature.")
        box.operator("mpfb.export_ue5")

    def draw(self, context):
        _LOG.enter()
        layout = self.layout
        scene = context.scene
        self._rescale_ue5(scene, layout)
        self._export_ue5(scene, layout)

ClassManager.add_class(MPFB_PT_Export_Panel)