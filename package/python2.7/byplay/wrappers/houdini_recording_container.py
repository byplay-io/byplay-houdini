from __future__ import absolute_import
from byplay import get_hou
from byplay.config import Config
from byplay.recording import Recording
from byplay.wrappers.houdini_object import HoudiniObject
from byplay.wrappers.houdini_params_builder import HoudiniParamsBuilder


class HoudiniRecordingContainer(HoudiniObject):
    def __init__(self, recording):
        super(
            HoudiniRecordingContainer,
            self
        ).__init__(
            node_name=u"Byplay_{}".format(format(recording.id)),
            parent_path=u"/obj",
            template_name=u"subnet",
            recording=recording
        )

    def apply_recording(self):
        self.connect_to_loader()

        HoudiniParamsBuilder.add_byplay_tab_to_recording_container(self.node)
        pref = self.recording.frames_prefix()
        path_params = {
            u"video_frames_path": u'`chs("recording_path")`/frames/{}`padzero(5, $F-ch("byplay_start_frame")+1)`.png'.format(pref),
        }
        HoudiniParamsBuilder.set_exr_paths(self.node, self.recording.environment_exr_names)

        for k, v in path_params.items():
            path_params[k] = v.replace(self.recording.base_path, u'`chs("recording_path")`')

        path_params[u'recording_path'] = self.recording.base_path.replace(
            Config.recordings_dir(),
            u'`chs("/obj/byplayloader/byplay_recordings_dir")`'
        )
        self.node.setParms(path_params)

        self.node.setParms({
            u'byplay_recording_id': self.recording.id,
            u'byplay_applied_postprocessing_y_offset': self.recording.postprocessing_y_offset,
            u'byplay_target_postprocessing_y_offset': self.target_y_offset(),
            u'byplay_recording_session_id': self.recording.recording_session_id,
        })
        self.node.parm(u"ty").setExpression(
            u"ch('byplay_applied_postprocessing_y_offset') - ch('byplay_target_postprocessing_y_offset')"
        )

    def target_y_offset(self):
        other_node_from_same_session = self.find_other_node_from_same_session()
        if other_node_from_same_session is not None:
            return other_node_from_same_session.parm(u'byplay_target_postprocessing_y_offset').eval()
        else:
            return self.recording.postprocessing_y_offset

    def find_other_node_from_same_session(self):
        for n in get_hou().node(u"/obj").children():
            session_parm = n.parm(u"byplay_recording_session_id")
            if session_parm is not None and session_parm.eval() == self.recording.recording_session_id:
                return n
        return None

    def connect_to_loader(self):
        loader = get_hou().node(u"/obj/byplayloader")
        if loader is None:
            return
        self.node.setInput(0, loader)
        self.node.moveToGoodPosition()


