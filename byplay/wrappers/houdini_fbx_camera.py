from byplay import get_hou
from byplay.wrappers.houdini_object import HoudiniObject


class HoudiniFBXCamera(HoudiniObject):
    def __init__(self, recording):
        super(
            HoudiniFBXCamera,
            self
        ).__init__(
            "/obj/AR_camera",
            recording
        )

    def apply_camera_view(self):
        self.set_params({
            "vm_background": '`chs("/obj/byplayloader/video_frames_path")`',
        })

    def create_camera(self):
        hou = get_hou()
        subn, _ = hou.hipFile.importFBX(
            self.recording.camera_fbx_path,
            convert_into_y_up_coordinate_system=True,
            override_framerate=True,
            framerate=30
        )
        camera_node = subn.node("Camera")
        if hou.node("/obj/AR_Camera") is not None:
            hou.node("/obj/AR_Camera").destroy()
        self.node, = hou.moveNodesTo((camera_node,), hou.node("/obj"))
        subn.destroy()
        self.node.setName("AR_Camera")
        self.apply_camera_view()


