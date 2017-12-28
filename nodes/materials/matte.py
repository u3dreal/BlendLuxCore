import bpy
from bpy.props import FloatProperty
from .. import LuxCoreNodeMaterial
from ..sockets import LuxCoreSocketFloat

SIGMA_DESCRIPTION = "Surface roughness, 0 for pure Lambertian reflection"

class LuxCoreSocketSigma(LuxCoreSocketFloat):
    default_value = FloatProperty(min=0, max=45, description=SIGMA_DESCRIPTION)
    slider = True


class LuxCoreNodeMatMatte(LuxCoreNodeMaterial):
    """(Rough) matte material node"""
    bl_label = "Matte Material"
    bl_width_min = 160

    def init(self, context):
        self.add_input("LuxCoreSocketColor", "Diffuse Color", (0.7, 0.7, 0.7))
        self.add_input("LuxCoreSocketSigma", "Sigma", 0)
        self.add_common_inputs()

        self.outputs.new("LuxCoreSocketMaterial", "Material")

    def export(self, props, luxcore_name=None):
        definitions = {
            "type": "roughmatte",
            "kd": self.inputs["Diffuse Color"].export(props),
            "sigma": self.inputs["Sigma"].export(props),
        }
        self.export_common_inputs(props, definitions)
        return self.base_export(props, definitions, luxcore_name)
