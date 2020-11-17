from __future__ import absolute_import
import logging
import os

from byplay.wrappers.houdini_object import HoudiniObject


class HoudiniPointCloud(HoudiniObject):
    def __init__(self, recording):
        super(
            HoudiniPointCloud,
            self
        ).__init__(
            u"/obj/AR_point_cloud",
            recording,
            template_name=u"geo"
        )

    def create_point_cloud(self):
        path = self.recording.point_cloud_path
        if not os.path.exists(path):
            logging.info(u"Point cloud not found")
            return None
        file = self.node.createNode(u"file")
        file.setParms({
            u'file': self.recording.make_path_relative(path)
        })

        return file