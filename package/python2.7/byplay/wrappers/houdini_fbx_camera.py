from __future__ import absolute_import
from byplay import get_hou
from byplay.helpers.fbx_unpack import FBXUnpack
from byplay.wrappers.houdini_object import HoudiniObject


class HoudiniFBXCamera(HoudiniObject):
    def __init__(self, recording):
        super(
            HoudiniFBXCamera,
            self
        ).__init__(
            u"/obj/AR_camera",
            recording
        )

    def _apply_camera_view(self):
        self.set_params({
            u"vm_background": u'`chs("/obj/byplayloader/video_frames_path")`',
        })

    def create_camera(self):
        self.node, = FBXUnpack(
            self.recording.camera_fbx_path
        ).unpack({u'Camera': u'AR_Camera'})
        self._apply_camera_view()
