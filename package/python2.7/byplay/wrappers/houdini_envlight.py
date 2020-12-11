from __future__ import absolute_import
from byplay.wrappers.houdini_object import HoudiniObject


class HoudiniEnvlight(HoudiniObject):
    def __init__(self, recording):
        super(
            HoudiniEnvlight,
            self
        ).__init__(
            u"AR_envlight",
            recording,
            template_name=u"envlight"
        )

    def create_envlight(self):
        self.node.parm(u"light_enable").setExpression(
            u"strcmp(chs('/obj/byplayloader/byplay_use_exr_from'), chs('../byplay_recording_id')) == 0"
        )
        self.set_params({
            u"env_map": u'`strcat(strcat(chs("../recording_path"), "/assets/"), chs("../exr_name"))`'
        })