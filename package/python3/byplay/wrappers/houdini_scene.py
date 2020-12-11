import logging
import os

from byplay.houdini_interface import get_hou
import byplay.wrappers.byplay_settings_container as byplay_settings_container
from byplay.recording import Recording
from byplay.wrappers.houdini_envlight import HoudiniEnvlight
from byplay.wrappers.houdini_fbx_camera import HoudiniFBXCamera
from byplay.wrappers.houdini_fbx_nulls import HoudiniFBXNulls
from byplay.wrappers.houdini_point_cloud import HoudiniPointCloud
from byplay.wrappers.houdini_recording_container import HoudiniRecordingContainer


class HoudiniScene:
    def __init__(self, recording: Recording):
        self.recording = recording
        self.camera = None
        self.nulls = []
        self.point_cloud = None
        self.envlight = None
        self.container = None
        self.target_fps = 30

    def apply(self, set_30fps=True, add_chopnet=True):
        self.target_fps = get_hou().hscriptExpression("$FPS")
        if set_30fps:
            self.target_fps = 30
        self.apply_animation_settings(set_30fps)

        self.container = HoudiniRecordingContainer(recording=self.recording)
        self.container.apply_recording()

        self.camera = self.load_camera(add_chopnet=add_chopnet)
        parent_subnet = self.container.node
        # byplay_settings_container.ByplaySettingsContainer(recreate=False).apply_recording(self.recording)

        self.nulls = self.load_nulls()
        self.point_cloud = self.load_point_cloud()
        self.envlight = self.load_envlight()

        parent_subnet.layoutChildren()

    def load_camera(self, add_chopnet):
        fbxc = HoudiniFBXCamera(self.recording)
        fbxc.create_camera(fps=self.target_fps, add_chopnet=add_chopnet)
        return fbxc

    def load_nulls(self):
        fbxc = HoudiniFBXNulls(self.recording)
        fbxc.create_nulls(fps=self.target_fps)
        return fbxc

    def load_point_cloud(self):
        hpc = HoudiniPointCloud(self.recording)
        hpc.create_point_cloud()
        return hpc

    def apply_animation_settings(self, set_30fps):
        frame_count = self.recording.frame_count()
        hou = get_hou()
        start_frame = hou.hscriptExpression("$FSTART")
        end_frame = max(hou.hscriptExpression("$FEND"), start_frame + frame_count)
        set_global_frange_expr = "tset `({}-1)/$FPS` `{}/$FPS`".format(start_frame, end_frame)
        hou.hscript(set_global_frange_expr)
        hou.playbar.setPlaybackRange(start_frame, end_frame)

    def load_envlight(self):
        envlight = HoudiniEnvlight(self.recording)
        envlight.create_envlight()
        return envlight