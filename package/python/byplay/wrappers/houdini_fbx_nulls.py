from __future__ import absolute_import
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
            u"/obj/nulls",
            recording
        )

    def create_nulls(self):
        if not os.path.exists(self.recording.nulls_fbx_path):
            return

        FBXUnpack(self.recording.nulls_fbx_path).unpack()
