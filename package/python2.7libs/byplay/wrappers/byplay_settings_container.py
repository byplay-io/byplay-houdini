from __future__ import absolute_import
from byplay.config import Config
from byplay.helpers.recording_downloader import RecordingDownloader
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
        HoudiniParamsBuilder.add_byplay_settings_tab(self.node)
        HoudiniParamsBuilder.add_byplay_recordings_tab(self.node)
        HoudiniParamsBuilder.set_stored_values(self.node)

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
