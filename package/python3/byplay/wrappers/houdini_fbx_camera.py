from byplay import get_hou
from byplay.helpers.fbx_unpack import FBXUnpack
from byplay.recording import Recording
from byplay.wrappers.houdini_object import HoudiniObject


class HoudiniFBXCamera(HoudiniObject):
    def __init__(self, recording: Recording, node_name: str):
        super(
            HoudiniFBXCamera,
            self
        ).__init__(
            node_name=node_name,
            recording=recording
        )

    def _apply_camera_view(self):
        self.set_params({
            "vm_background": '`chs("{}/video_frames_path")`'.format(self.parent_node.path()),
        })

    def apply_camera(self, add_chopnet):
        self._apply_camera_view()
        if add_chopnet:
            self._create_chopnet()

    def _create_chopnet(self):
        if self.parent_node.node("motionfx") is not None:
            self.parent_node.node("motionfx").destroy()
        chopnet = self.node.findOrCreateMotionEffectsNetwork()

        transform = self.node.parmTuple("t")
        channel = transform.createClip(
            chopnet,
            self.node_name,
            False,
            True,
            False,
            False,
            False
        )

        rotation = self.node.parmTuple("r")
        rotation.appendClip(channel, True, False, False, False)
        focal = self.node.parm("focal")
        focal.appendClip(channel, True, False, False, False)

        channel.setExportFlag(False)

        shift = chopnet.createNode("shift")
        shift.setInput(0, channel)
        shift.setExportFlag(True)
        shift.parm("start").setExpression('ch("../../byplay_start_frame")-1')
        shift.parm("units").set(0)
        chopnet.layoutChildren()

    def legacy_unpack(self, fps: int):
        self.node, = FBXUnpack(
            self.recording.camera_fbx_path,
            fps=fps
        ).unpack_legacy({'Camera': self.node_name}, self.parent_node, only_in_map=True)