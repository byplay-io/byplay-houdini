from __future__ import absolute_import
import logging
import os

from byplay.recording import Recording
from byplay.wrappers.houdini_object import HoudiniObject


class HoudiniPointCloud(HoudiniObject):
    def __init__(self, recording, refined):
        node_name = u"AR_point_cloud"
        self.path = recording.scene_pc_ar_path
        if refined:
            node_name = u"Refined_point_cloud"
            self.path = recording.scene_pc_refined_path
        super(
            HoudiniPointCloud,
            self
        ).__init__(
            node_name,
            recording,
            template_name=u"geo"
        )

    def create_point_cloud(self):
        if not os.path.exists(self.path):
            logging.info(u"Point cloud not found")
            return None
        file = self.node.createNode(u"file")
        file.setParms({
            u'file': self.recording.make_path_relative(self.path)
        })

        return file