from __future__ import absolute_import
from byplay.wrappers.houdini_object import HoudiniObject


class HoudiniEnvlight(HoudiniObject):
    def __init__(self, recording):
        super(
            HoudiniEnvlight,
            self
        ).__init__(
            u"/obj/AR_envlight",
            recording,
            template_name=u"envlight"
        )

    def create_envlight(self):
        self.set_params({
            u"env_map": u'`strcat(strcat(chs("/obj/byplayloader/recording_path"), "/assets/"), chs("/obj/byplayloader/exr_name"))`'
        })
