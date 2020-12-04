import logging
from typing import Dict

from byplay.helpers.util import identity, expand_vector_props
from byplay.houdini_interface import get_hou
from byplay.recording import Recording


class HoudiniObject:
    recording: Recording

    def __init__(self, node_name, recording=None, parent_path=None, template_name: str = None):
        self.recording = recording
        self.parent_node = self._get_parent_node(parent_path)
        self.node_name = node_name
        if template_name is None:
            self.node = self.parent_node.node(node_name)
        else:
            self.node = self.recreate_node(template_name)

    def node_path(self):
        return "/".join([self.parent_node.path(), self.node_name])

    def recreate_node(self, template_name):
        if self.parent_node.node(self.node_name) is not None:
            self.parent_node.node(self.node_name).destroy()

        node = self.parent_node.createNode(template_name, self.node_name)
        return node

    def split_path_to_parent(self):
        path = self.hou_scene_path
        spl = path.split("/")
        parent = "/".join(spl[0:-1])
        return parent, spl[-1]

    def make_float_keyframe(self, value: float, frame: int) -> object:
        kf = get_hou().Keyframe()
        kf.setValue(value)
        kf.setFrame(frame)
        return kf

    def set_dense_vector_values(self, param_prefix, vectors, node=None):
        xs = [v.x for v in vectors]
        ys = [v.y for v in vectors]
        zs = [v.z for v in vectors]
        node = node or self.node
        x_parm = node.parm(param_prefix + "x")
        y_parm = node.parm(param_prefix + "y")
        z_parm = node.parm(param_prefix + "z")
        self.set_dense_params(x_parm, xs)
        self.set_dense_params(y_parm, ys)
        self.set_dense_params(z_parm, zs)

    def set_constant_vector_value(self, param_prefix, vector, node=None):
        node = node or self.node
        node.parm(param_prefix + "x").set(vector.x)
        node.parm(param_prefix + "y").set(vector.y)
        node.parm(param_prefix + "z").set(vector.z)

    def set_dense_params(self, parm, values):
        kfs = [self.make_float_keyframe(v, i+1) for i, v in enumerate(values)]
        parm.deleteAllKeyframes()
        parm.setKeyframes(kfs)

    def set_params(self, props: Dict[str, any], at_frame=None, create_non_existing=False):
        props = expand_vector_props(props)
        for prop, val in props.items():
            parm = self.node.parm(prop)
            if parm is None:
                print("Could not find parm {} on {}".format(prop, self.node.path()))
                continue
            if type(val) == str or at_frame is None:
                parm.set(val)
                continue
            kf = get_hou().Keyframe()
            kf.setValue(float(val))
            if at_frame is not None:
                kf.setFrame(at_frame)
            parm.setKeyframe(kf)

    def _get_parent_node(self, parent_path):
        hou = get_hou()
        if parent_path is not None:
            return hou.node(parent_path)

        root = hou.node("/obj")
        if self.recording is None:
            return root
        parent_name = "Byplay_{}".format(self.recording.id)
        parent = root.node(parent_name)
        if parent is None:
            raise ValueError("Could not find parent node {}".format(parent_name))
        return parent

