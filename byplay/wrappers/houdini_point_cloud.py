import logging
import os

from byplay.wrappers.houdini_object import HoudiniObject


class HoudiniPointCloud(HoudiniObject):
    def __init__(self, recording):
        super(
            HoudiniPointCloud,
            self
        ).__init__(
            "AR_point_cloud",
            recording,
            template_name="geo"
        )

    def create_point_cloud(self):
        path = self.recording.point_cloud_path
        if not os.path.exists(path):
            logging.info("Point cloud not found")
            return None
        file = self.node.createNode("file")
        file.setParms({
            'file': self.recording.make_path_relative(path)
        })

        return file