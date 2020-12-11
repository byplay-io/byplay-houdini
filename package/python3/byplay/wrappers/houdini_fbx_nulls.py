import os

from byplay import get_hou
from byplay.helpers.fbx_unpack import FBXUnpack
from byplay.wrappers.houdini_object import HoudiniObject


class HoudiniFBXNulls(HoudiniObject):
    def __init__(self, recording):
        super(
            HoudiniFBXNulls,
            self
        ).__init__(
            "nulls",
            recording
        )

    def create_nulls(self, fps):
        if not os.path.exists(self.recording.nulls_fbx_path):
            return

        FBXUnpack(self.recording.nulls_fbx_path, fps=fps).unpack(
            parent_node=self.parent_node
        )
        planes = self.parent_node.node("Planes")
        if planes is not None:
            planes_subn = self.parent_node.collapseIntoSubnet((planes,) + planes.outputs())
            planes_subn.setName("Planes")