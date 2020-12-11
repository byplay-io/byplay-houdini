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
            node_name=u"AR_camera",
            recording=recording
        )

    def _apply_camera_view(self):
        self.set_params({
            u"vm_background": u'`chs("{}/video_frames_path")`'.format(self.parent_node.path()),
        })

    def create_camera(self, fps, add_chopnet):
        self.node, = FBXUnpack(
            self.recording.camera_fbx_path,
            fps=fps
        ).unpack({u'Camera': self.node_name}, self.parent_node, only_in_map=True)
        self._apply_camera_view()
        if add_chopnet:
            self._create_chopnet()

    def _create_chopnet(self):
        if self.parent_node.node(u"motionfx") is not None:
            self.parent_node.node(u"motionfx").destroy()
        chopnet = self.node.findOrCreateMotionEffectsNetwork()

        transform = self.node.parmTuple(u"t")
        channel = transform.createClip(
            chopnet,
            self.node_name,
            False,
            True,
            False,
            False,
            False
        )

        rotation = self.node.parmTuple(u"r")
        rotation.appendClip(channel, True, False, False, False)
        focal = self.node.parm(u"focal")
        focal.appendClip(channel, True, False, False, False)

        channel.setExportFlag(False)

        shift = chopnet.createNode(u"shift")
        shift.setInput(0, channel)
        shift.setExportFlag(True)
        shift.parm(u"start").setExpression(u'ch("../../byplay_start_frame")-1')
        shift.parm(u"units").set(0)
        chopnet.layoutChildren()