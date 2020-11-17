from __future__ import with_statement
from __future__ import absolute_import
import json
import logging
import os

from byplay.config import Config
from byplay.helpers.util import join
from io import open


class Recording(object):
    def __init__(self, base_path, id):
        self.id = id
        self.base_path = base_path
        self.video_path = join(self.base_path, u"src_video.mp4")
        self.manifest_path = join(self.base_path, u"recording_manifest.json")
        self.manifest = self.read_manifest()
        logging.info(u"Got manifest: {}".format(self.manifest))

        self.frames_dir = join(self.base_path, u"frames")
        self.camera_frames_path = self.frames_dir + u"/$F5." + Config.video_frames_ext()
        self.camera_frames_path_ffmpeg = self.camera_frames_path.replace(u"$F5", u"%05d")

        self.assets_dir = join(self.base_path, u"assets")
        self.point_cloud_path = join(self.base_path, u"houdini_pointcloud.obj")
        self.camera_fbx_path = join(self.base_path, u"houdini_camera.fbx")
        self.nulls_fbx_path = join(self.base_path, u"houdini_nulls.fbx")

        self.environment_exr_names = self.find_environment_exr_names()

    def frame_count(self):
        return self.manifest[u'framesCount']

    def make_path_relative(self, path):
        return path.replace(self.base_path, u'`chs("/obj/byplayloader/recording_path")`')

    def __repr__(self):
        return u"<Recording at {}>".format(self.base_path)

    def find_environment_exr_names(self):
        if not os.path.exists(self.assets_dir):
            return []
        return [path for path in os.listdir(self.assets_dir) if path.endswith(u".exr")]

    def read_manifest(self):
        with open(self.manifest_path, encoding=u"utf-8") as f:
            return json.load(f)
