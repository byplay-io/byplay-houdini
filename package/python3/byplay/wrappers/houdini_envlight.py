from byplay.wrappers.houdini_object import HoudiniObject


class HoudiniEnvlight(HoudiniObject):
    def __init__(self, recording):
        super(
            HoudiniEnvlight,
            self
        ).__init__(
            "AR_envlight",
            recording,
            template_name="envlight"
        )

    def create_envlight(self):
        self.node.parm("light_enable").setExpression(
            "strcmp(chs('/obj/byplayloader/byplay_use_exr_from'), chs('../byplay_recording_id')) == 0"
        )
        self.set_params({
            "env_map": '`strcat(strcat(chs("../recording_path"), "/assets/"), chs("../exr_name"))`'
        })