from __future__ import absolute_import
from byplay.backend.amplitude_logger import log_amplitude
from byplay.config import Config
from byplay.recording import Recording
from byplay.wrappers.houdini_object import HoudiniObject
from byplay.wrappers.houdini_params_builder import HoudiniParamsBuilder


class ByplaySettingsContainer(HoudiniObject):
    PATH = u"/obj/byplayloader"

    def __init__(self, recreate=True):
        template_name = u"null"
        if not recreate:
            template_name = None
        super(ByplaySettingsContainer, self).__init__(self.PATH, template_name=template_name)

    def setup(self):
        log_amplitude(u"Byplay loader node created")
        HoudiniParamsBuilder.add_byplay_tab(self.node)
        self.apply_config()

    def apply_config(self):
        self.node.setParms({u"byplay_recordings_dir": Config.recordings_dir()})

    def apply_recording(self, recording):
        path_params = {
            u"video_frames_path": recording.camera_frames_path,
        }
        HoudiniParamsBuilder.set_exr_paths(self.node, recording.environment_exr_names)

        for k, v in path_params.items():
            path_params[k] = v.replace(recording.base_path, u'`chs("recording_path")`')

        path_params[u'recording_path'] = recording.base_path.replace(
            Config.recordings_dir(),
            u'`chs("byplay_recordings_dir")`'
        )
        self.node.setParms(path_params)
