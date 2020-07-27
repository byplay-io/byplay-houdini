from byplay.wrappers.houdini_object import HoudiniObject


class HoudiniEnvlight(HoudiniObject):
    def __init__(self, recording):
        super(
            HoudiniEnvlight,
            self
        ).__init__(
            "/obj/AR_envlight",
            recording,
            template_name="envlight"
        )

    def create_envlight(self):
        self.set_params({
            "env_map": '`strcat(strcat(chs("/obj/byplayloader/recording_path"), "/assets/"), chs("/obj/byplayloader/exr_name"))`'
        })