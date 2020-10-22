import logging
import time

from byplay import get_hou
from byplay.backend.sentry import capture_exception
from byplay.config import Config
from byplay.helpers.recording_local_storage import RecordingLocalStorage
from byplay.recording import Recording
import byplay.wrappers.byplay_settings_container as byplay_settings_container
from byplay.wrappers.houdini_scene import HoudiniScene


def setup_byplay_helper_nodes():
    try:
        Config.setup_logger()
        if not Config.read():
            hou = get_hou()
            hou.ui.displayMessage(
                "Could not read config file. Please open Byplay Desktop and set it up",
                severity=hou.severityType.Error
            )
            return
        logging.info("Creating byplay loader node")
        byplay_settings_container.ByplaySettingsContainer().setup()
    except Exception as e:
        capture_exception()
        raise e

def load_recording(recording_id: str) -> Recording:
    logging.info("loading {}".format(recording_id))
    recording = RecordingLocalStorage().load(recording_id)
    return recording


def load_recording_for_ui(recording_id: str):
    recording = load_recording(recording_id)
    HoudiniScene(recording).apply()
    return recording

