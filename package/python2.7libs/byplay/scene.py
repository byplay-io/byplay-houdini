from __future__ import absolute_import
import logging
import time

from byplay import get_hou
from byplay.config import Config
from byplay.helpers.recording_downloader import RecordingDownloader
from byplay.recording import Recording
import byplay.wrappers.byplay_settings_container as byplay_settings_container
from byplay.wrappers.houdini_scene import HoudiniScene


def setup_byplay_helper_nodes():
    Config.setup_logger()
    Config.read()
    logging.info(u"Creating byplay loader node")
    byplay_settings_container.ByplaySettingsContainer().setup()


def load_recording(recording_id):
    logging.info(u"loading {}".format(recording_id))
    hou = get_hou()
    recording = RecordingDownloader().load(
        recording_id,
        hou.ui.setStatusMessage
    )
    return recording


def load_recording_for_ui(recording_id):
    recording = load_recording(recording_id)
    HoudiniScene(recording).apply()
    return recording

