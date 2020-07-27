import sys

from byplay import get_hou, scene
from byplay.config import Config
from byplay.helpers.recording_downloader import RecordingDownloader
from byplay.wrappers.houdini_params_builder import HoudiniParamsBuilder
import byplay.backend.api as byplay_api


def reload_all_modules():
    hou = get_hou()

    hou.ui.displayMessage("reloading")
    for name, module in sys.modules.items():
        if name.split(".")[0] == "byplay" and module is not None:
            print("reloading {}".format(name))
            reload(module)
    Config.read()


def reload_recordings_list(node_path):
    hou = get_hou()
    node = hou.node(node_path)
    byplay_access_token = node.parm("byplay_access_token").evalAsString()
    if not _validate_access_token(byplay_access_token):
        return

    Config.store_access_token(byplay_access_token)
    new_ids = RecordingDownloader().list_recording_ids()
    new_ids = list(reversed(new_ids))
    HoudiniParamsBuilder.set_byplay_recording_ids(node, new_ids)


def load_recording_for_ui(node_path):
    hou = get_hou()
    node = hou.node(node_path)
    byplay_access_token = node.parm("byplay_access_token").evalAsString()
    if not _validate_access_token(byplay_access_token):
        return
    byplay_recordings_dir = node.parm("byplay_recordings_dir").evalAsString()
    recording_id = node.parm("byplay_recording_id").evalAsString()

    if len(byplay_recordings_dir) < 3 or len(recording_id) < 18:
        hou.ui.displayMessage("Please fill in access token, recordings dir and select a recording", severity=hou.severityType.Error)
        return

    Config.store_access_token(byplay_access_token)
    Config.store_byplay_recordings_dir(byplay_recordings_dir)

    scene.load_recording_for_ui(recording_id)


def _validate_access_token(token) -> bool:
    hou = get_hou()
    if len(token) < 5:
        hou.ui.displayMessage("Please fill in Byplay access token", severity=hou.severityType.Error)
        return False

    Config.store_access_token(token)
    error = byplay_api.check_error()
    if error is not None:
        hou.ui.displayMessage(error, severity=hou.severityType.Error)
        return False
    return True
