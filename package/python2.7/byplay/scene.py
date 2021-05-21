from __future__ import absolute_import
import logging
import time


from byplay import get_hou
from byplay.backend.sentry import capture_exception
from byplay.config import Config
from byplay.helpers.recording_local_storage import RecordingLocalStorage
from byplay.recording import Recording
import byplay.wrappers.byplay_settings_container as byplay_settings_container
from byplay.wrappers.houdini_scene import HoudiniScene


def setup_byplay_helper_nodes(node):
    try:
        Config.setup_logger()
    except Exception, e:
        capture_exception()
        raise e

    try:
        Config.read()
    except Exception, e:
        capture_exception()
        hou = get_hou()
        hou.ui.displayMessage(
            u"Could not read config file. Please open Byplay Desktop and set it up",
            severity=hou.severityType.Error
        )
        raise e

    try:
        logging.info(u"Creating byplay loader node")
        byplay_settings_container.ByplaySettingsContainer(node).setup()
    except Exception, e:
        capture_exception()
        raise e


def load_recording(recording_id, refined):
    logging.info(u"loading {}".format(recording_id))
    recording = RecordingLocalStorage().load(recording_id, refined)
    return recording


def load_recording_for_ui(recording_id, refined, config):
    recording = load_recording(recording_id, refined)
    HoudiniScene(recording).apply(**config)
    return recording

