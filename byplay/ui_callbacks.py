import sys

from byplay import get_hou, scene
from byplay.backend.amplitude_logger import log_amplitude
from byplay.backend.sentry import capture_exception
from byplay.config import Config
from byplay.helpers.recording_local_storage import RecordingLocalStorage
from byplay.wrappers.houdini_params_builder import HoudiniParamsBuilder


def reload_all_modules():
    hou = get_hou()

    hou.ui.displayMessage("reloading")
    for name, module in sys.modules.items():
        if name.split(".")[0] == "byplay" and module is not None:
            print("reloading {}".format(name))
            reload(module)
    Config.read()


def reload_recordings_list(node_path):
    try:
        hou = get_hou()
        node = hou.node(node_path)
        new_ids = RecordingLocalStorage().list_recording_ids()
        new_ids = list(reversed(new_ids))
        HoudiniParamsBuilder.set_byplay_recording_ids(node, new_ids)
        log_amplitude("Recording list reloaded")
    except Exception as e:
        capture_exception()
        raise e


def load_recording_for_ui(node_path):
    try:
        hou = get_hou()
        node = hou.node(node_path)
        recording_id = node.parm("byplay_recording_id").evalAsString()
        log_amplitude("Recording loaded", recording_id=recording_id)

        if len(recording_id) < 18:
            hou.ui.displayMessage("Please select a recording", severity=hou.severityType.Error)
            return

        scene.load_recording_for_ui(recording_id)
        node.setParms({"byplay_loaded_recording_id": recording_id})
    except Exception as e:
        capture_exception()
        raise e
