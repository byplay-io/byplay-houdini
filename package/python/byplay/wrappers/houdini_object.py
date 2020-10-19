from __future__ import absolute_import
import logging


from byplay.helpers.util import identity, expand_vector_props
from byplay.houdini_interface import get_hou


class HoudiniObject(object):
    def __init__(self, hou_scene_path, recording=None, template_name = None):
        self.hou_scene_path = hou_scene_path
        if template_name is None:
            self.node = get_hou().node(hou_scene_path)
        else:
            self.node = self.recreate_node(template_name)
        self.recording = recording

    def recreate_node(self, template_name):
        hou = get_hou()
        if hou.node(self.hou_scene_path) is not None:
            hou.node(self.hou_scene_path).destroy()

        parent_path, name = self.split_path_to_parent()
        node = hou.node(parent_path).createNode(template_name, name)
        return node

    def split_path_to_parent(self):
        path = self.hou_scene_path
        spl = path.split(u"/")
        parent = u"/".join(spl[0:-1])
        return parent, spl[-1]

    def make_float_keyframe(self, value, frame):
        kf = get_hou().Keyframe()
        kf.setValue(value)
        kf.setFrame(frame)
        return kf

    def set_dense_vector_values(self, param_prefix, vectors, node=None):
        xs = [v.x for v in vectors]
        ys = [v.y for v in vectors]
        zs = [v.z for v in vectors]
        node = node or self.node
        x_parm = node.parm(param_prefix + u"x")
        y_parm = node.parm(param_prefix + u"y")
        z_parm = node.parm(param_prefix + u"z")
        self.set_dense_params(x_parm, xs)
        self.set_dense_params(y_parm, ys)
        self.set_dense_params(z_parm, zs)

    def set_constant_vector_value(self, param_prefix, vector, node=None):
        node = node or self.node
        node.parm(param_prefix + u"x").set(vector.x)
        node.parm(param_prefix + u"y").set(vector.y)
        node.parm(param_prefix + u"z").set(vector.z)

    def set_dense_params(self, parm, values):
        kfs = [self.make_float_keyframe(v, i+1) for i, v in enumerate(values)]
        parm.deleteAllKeyframes()
        parm.setKeyframes(kfs)

    def set_params(self, props, at_frame=None, create_non_existing=False):
        props = expand_vector_props(props)
        for prop, val in props.items():
            parm = self.node.parm(prop)
            if parm is None:
                print u"Could not find parm {} on {}".format(prop, self.node.path())
                continue
            if type(val) == unicode or at_frame is None:
                parm.set(val)
                continue
            kf = get_hou().Keyframe()
            kf.setValue(float(val))
            if at_frame is not None:
                kf.setFrame(at_frame)
            parm.setKeyframe(kf)
