from __future__ import absolute_import
import logging
import os

from byplay.houdini_interface import get_hou
import byplay.wrappers.byplay_settings_container as byplay_settings_container
from byplay.recording import Recording
from byplay.wrappers.houdini_envlight import HoudiniEnvlight
from byplay.wrappers.houdini_fbx_camera import HoudiniFBXCamera
from byplay.wrappers.houdini_point_cloud import HoudiniPointCloud


class HoudiniScene(object):
    def __init__(self, recording):
        self.recording = recording
        self.camera = None
        self.point_cloud = None
        self.envlight = None

    def apply(self):
        byplay_settings_container.ByplaySettingsContainer(recreate=False).apply_recording(self.recording)
        self.apply_animation_settings()

        self.camera = self.load_camera()
        self.point_cloud = self.load_point_cloud()
        self.envlight = self.load_envlight()

        get_hou().node(u"/obj").layoutChildren()

    def load_camera(self):
        fbxc = HoudiniFBXCamera(self.recording)
        fbxc.create_camera()
        return fbxc

    def load_point_cloud(self):
        hpc = HoudiniPointCloud(self.recording)
        hpc.create_point_cloud()
        return hpc

    def apply_animation_settings(self):
        end_frame = self.recording.frame_count()
        start_frame = 1
        set_global_frange_expr = u"tset `({}-1)/$FPS` `{}/$FPS`".format(start_frame, end_frame)
        hou = get_hou()
        hou.hscript(set_global_frange_expr)
        hou.playbar.setPlaybackRange(start_frame, end_frame)

    def load_envlight(self):
        envlight = HoudiniEnvlight(self.recording)
        envlight.create_envlight()
        return envlight
