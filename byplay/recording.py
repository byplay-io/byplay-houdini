import json
import logging
import os

from byplay.config import Config
from byplay.helpers.util import join


class Recording:
    def __init__(self, base_path: str, id: str):
        self.id = id
        self.base_path = base_path
        self.video_path = join(self.base_path, "src_video.mp4")
        self.manifest_path = join(self.base_path, "recording_manifest.json")
        self.postprocessing_data_path = join(self.base_path, "postprocessing_data.json")
        self.manifest = self.read_manifest()
        logging.info("Got manifest: {}".format(self.manifest))

        self.frames_dir = join(self.base_path, "frames")
        self.camera_frames_path = self.frames_dir + "/$F5." + Config.video_frames_ext()
        self.camera_frames_path_ffmpeg = self.camera_frames_path.replace("$F5", "%05d")

        self.assets_dir = join(self.base_path, "assets")
        self.point_cloud_path = join(self.base_path, "houdini_pointcloud.obj")
        self.camera_fbx_path = join(self.base_path, "houdini_camera.fbx")
        self.nulls_fbx_path = join(self.base_path, "houdini_nulls.fbx")

        self.environment_exr_names = self.find_environment_exr_names()

        self.postprocessing_y_offset = 0
        self.recording_session_id = "unk_1"
        self.read_postprocessing_data()

    def frame_count(self):
        return self.manifest['framesCount']

    def make_path_relative(self, path):
        return path.replace(self.base_path, '`chs("/obj/Byplay_{}/recording_path")`'.format(self.id))

    def __repr__(self):
        return "<Recording at {}>".format(self.base_path)

    def find_environment_exr_names(self):
        if not os.path.exists(self.assets_dir):
            return []
        return [path for path in os.listdir(self.assets_dir) if path.endswith(".exr")]

    def read_manifest(self):
        with open(self.manifest_path, encoding="utf-8") as f:
            return json.load(f)

    def read_postprocessing_data(self):
        if not os.path.exists(self.postprocessing_data_path):
            return
        with open(self.postprocessing_data_path, encoding="utf-8") as f:
            postprocessing = json.load(f)
            if 'y_offset' in postprocessing:
                self.postprocessing_y_offset = postprocessing['y_offset']
            if 'session_id' in postprocessing:
                self.recording_session_id = postprocessing['session_id']
