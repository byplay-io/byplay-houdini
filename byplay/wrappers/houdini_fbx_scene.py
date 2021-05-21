from byplay import get_hou
from byplay.helpers.fbx_unpack import FBXUnpack
from byplay.recording import Recording
from byplay.wrappers.houdini_fbx_camera import HoudiniFBXCamera
from byplay.wrappers.houdini_object import HoudiniObject


class HoudiniFBXScene:
    def __init__(self, recording: Recording, refined: bool, parent_node):
        self.recording = recording
        self.parent_node = parent_node
        self.refined = refined

    def create(self, fps, add_chopnet):
        path = self.recording.scene_fbx_ar_path
        node_name = "AR_camera"
        if self.refined:
            path = self.recording.scene_fbx_refined_path
            node_name = "Refined_camera"
        _new_nodes = FBXUnpack(
            path,
            fps=fps
        ).unpack({
            'Camera': node_name,
            'AR_camera': 'AR_camera'
        }, self.parent_node, only_in_map=False)#(not self.refined))

        fbx_camera = HoudiniFBXCamera(recording=self.recording, node_name=node_name)
        fbx_camera.apply_camera(add_chopnet)

        self.arrange_planes()
        self.arrange_nulls()

    def arrange_nulls(self):
        nulls = [n for n in self.parent_node.children() if "byplay_null" in n.name()]
        if len(nulls) > 0:
            null_parent = self.parent_node.createNode("null", "NULLs")
            for n in nulls:
                n.setInput(0, null_parent)
                n.parmTuple("r").set([0, 0, 0])

    def arrange_planes(self):
        planes = [n for n in self.parent_node.children() if "ARPlane_" in n.name()]
        if len(planes) > 0:
            planes_subn = self.parent_node.collapseIntoSubnet(planes)
            planes_subn.setName("Planes")
            subnet_input_1 = planes_subn.indirectInputs()[0]
            for plane in planes_subn.children():
                plane.setInput(0, subnet_input_1)
            planes_subn.layoutChildren()
