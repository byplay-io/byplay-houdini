from __future__ import absolute_import
import logging
import os

from byplay.houdini_interface import get_hou
import byplay.wrappers.byplay_settings_container as byplay_settings_container
from byplay.recording import Recording
from byplay.wrappers.houdini_envlight import HoudiniEnvlight
from byplay.wrappers.houdini_fbx_camera import HoudiniFBXCamera
from byplay.wrappers.houdini_fbx_nulls import HoudiniFBXNulls
from byplay.wrappers.houdini_fbx_scene import HoudiniFBXScene
from byplay.wrappers.houdini_point_cloud import HoudiniPointCloud
from byplay.wrappers.houdini_recording_container import HoudiniRecordingContainer


class HoudiniScene(object):
    def __init__(self, recording):
        self.recording = recording
        self.container = None
        self.target_fps = recording.fps
        self.should_load_refinement = self.recording.has_refinement()

    def apply(self, set_30fps=True, add_chopnet=True):
        self.target_fps = get_hou().hscriptExpression(u"$FPS")
        if set_30fps:
            self.target_fps = 30
        self.apply_animation_settings(set_30fps)

        self.container = HoudiniRecordingContainer(recording=self.recording)
        self.container.apply_recording()

        if self.is_legacy_fbx():
            self.load_legacy_camera(add_chopnet=add_chopnet)
            self.load_legacy_nulls()
        else:
            self.load_fbx_scene(add_chopnet=add_chopnet, parent_node=self.container.node)

        self.load_point_cloud()
        self.load_envlight()

        subnet_input_1 = self.container.node.indirectInputs()[0]
        for child in self.container.node.children():
            name = child.name().lower()
            if name == u"planes" or u'camera' in name or u'point_cloud' in name or name == u'nulls':
                child.setInput(0, subnet_input_1)
        self.container.node.layoutChildren()

    def is_legacy_fbx(self):
        return not os.path.exists(self.recording.scene_fbx_ar_path)

    def load_legacy_camera(self, add_chopnet):
        fbxc = HoudiniFBXCamera(self.recording, node_name=u"AR_camera")
        fbxc.legacy_unpack(fps=self.target_fps)
        fbxc.apply_camera(add_chopnet=add_chopnet)

    def load_legacy_nulls(self):
        fbxc = HoudiniFBXNulls(self.recording)
        fbxc.create_nulls(fps=self.target_fps)

    def load_fbx_scene(self, parent_node, add_chopnet):
        HoudiniFBXScene(self.recording, parent_node=parent_node, refined=False).create(
            fps=self.target_fps, add_chopnet=add_chopnet
        )
        if self.should_load_refinement:
            HoudiniFBXScene(self.recording, parent_node=parent_node, refined=True).create(
                fps=self.target_fps, add_chopnet=add_chopnet
            )

    def load_point_cloud(self):
        HoudiniPointCloud(self.recording, refined=False).create_point_cloud()
        if self.should_load_refinement:
            HoudiniPointCloud(self.recording, refined=True).create_point_cloud()

    def apply_animation_settings(self, set_30fps):
        frame_count = self.recording.frame_count()
        hou = get_hou()
        start_frame = hou.hscriptExpression(u"$FSTART")
        end_frame = max(hou.hscriptExpression(u"$FEND"), start_frame + frame_count)
        set_global_frange_expr = u"tset `({}-1)/$FPS` `{}/$FPS`".format(start_frame, end_frame)
        hou.hscript(set_global_frange_expr)
        hou.playbar.setPlaybackRange(start_frame, end_frame)

    def load_envlight(self):
        envlight = HoudiniEnvlight(self.recording)
        envlight.create_envlight()
        return envlight