from byplay.backend.amplitude_logger import log_amplitude
from byplay.config import Config
from byplay.recording import Recording
from byplay.wrappers.houdini_object import HoudiniObject
from byplay.wrappers.houdini_params_builder import HoudiniParamsBuilder


class ByplaySettingsContainer(HoudiniObject):
    NODE_NAME = "byplayloader"

    def __init__(self, recreate=True):
        template_name = "null"
        if not recreate:
            template_name = None
        super(ByplaySettingsContainer, self).__init__(
            node_name=self.NODE_NAME,
            template_name=template_name
        )

    def setup(self):
        log_amplitude("Byplay loader node created")
        HoudiniParamsBuilder.add_byplay_tab_to_loader(self.node)
        self.apply_config()

    def apply_config(self):
        self.node.setParms({"byplay_recordings_dir": Config.recordings_dir()})

    # def apply_recording(self, recording: Recording):
    #     path_params = {
    #         "video_frames_path": recording.camera_frames_path,
    #     }
    #     HoudiniParamsBuilder.set_exr_paths(self.node, recording.environment_exr_names)
    #
    #     for k, v in path_params.items():
    #         path_params[k] = v.replace(recording.base_path, '`chs("recording_path")`')
    #
    #     path_params['recording_path'] = recording.base_path.replace(
    #         Config.recordings_dir(),
    #         '`chs("byplay_recordings_dir")`'
    #     )
    #     self.node.setParms(path_params)
