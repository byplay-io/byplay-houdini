from __future__ import with_statement
from __future__ import absolute_import
import json
import logging
import os

from byplay.config import Config
from byplay.helpers.util import join
from io import open


class Recording(object):
    def __init__(self, base_path, id, refined = False):
        self.id = id
        self.base_path = base_path
        self.video_path = join(self.base_path, u"src_video.mp4")
        self.manifest_path = join(self.base_path, u"recording_manifest.json")
        self.postprocessing_data_path = join(self.base_path, u"postprocessing_data.json")
        self.manifest = self.read_manifest()
        logging.info(u"Got manifest: {}".format(self.manifest))

        self.frames_dir = join(self.base_path, u"frames")

        self.assets_dir = join(self.base_path, u"assets")
        self.camera_fbx_path = join(self.base_path, u"houdini_camera.fbx")
        self.nulls_fbx_path = join(self.base_path, u"houdini_nulls.fbx")

        self.refined = refined

        self.scene_pc_ar_path = join(self.base_path, u"houdini_pointcloud_ar_v1.obj")
        if not os.path.exists(self.scene_pc_ar_path):
            self.scene_pc_ar_path = join(self.base_path, u"houdini_pointcloud.obj")
        self.scene_pc_refined_path = join(self.base_path, u"houdini_pointcloud_refined_v1.obj")

        self.scene_fbx_refined_path = join(self.base_path, u"houdini_scene_refined_v1.fbx")
        self.scene_fbx_ar_path = join(self.base_path, u"houdini_scene_{}.fbx".format(u"ar_v1"))

        self.environment_exr_names = self.find_environment_exr_names()

        self.postprocessing_y_offset = 0
        self.recording_session_id = u"unk_1"
        self.read_postprocessing_data()
        self.fps = self.get_fps()

    def has_refinement(self):
        return os.path.exists(self.scene_fbx_refined_path) and os.path.exists(self.scene_pc_refined_path)

    def get_fps(self):
        if u'fps' in self.manifest:
            return self.manifest[u'fps']
        return 30

    def frame_count(self):
        return self.manifest[u'framesCount']

    def make_path_relative(self, path):
        return path.replace(self.base_path, u'`chs("/obj/Byplay_{}/recording_path")`'.format(self.id))

    def __repr__(self):
        return u"<Recording at {}>".format(self.base_path)

    def find_environment_exr_names(self):
        if not os.path.exists(self.assets_dir):
            return []
        return [path for path in os.listdir(self.assets_dir) if path.endswith(u".exr")]

    def read_manifest(self):
        with open(self.manifest_path, encoding=u"utf-8") as f:
            return json.load(f)

    def read_postprocessing_data(self):
        if not os.path.exists(self.postprocessing_data_path):
            return
        with open(self.postprocessing_data_path, encoding=u"utf-8") as f:
            postprocessing = json.load(f)
            if u'y_offset' in postprocessing:
                self.postprocessing_y_offset = postprocessing[u'y_offset']
            if u'session_id' in postprocessing:
                self.recording_session_id = postprocessing[u'session_id']

    def frames_prefix(self):
        legacy_exists = os.path.exists(join(self.frames_dir, u"00001.png"))
        new_exits = os.path.exists(join(self.frames_dir, u"ar_00001.png"))
        if legacy_exists and not new_exits:
            return u""
        return u"ar_"