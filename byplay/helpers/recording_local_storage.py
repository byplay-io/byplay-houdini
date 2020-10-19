import logging
import os
from distutils.dir_util import mkpath
from typing import Dict

from byplay.config import Config
from byplay.helpers.util import join
import byplay.backend.api as byplay_api
from byplay.recording import Recording
from byplay.wrappers.ffmpeg import FFMPEG


class RecordingLocalStorage:
    def list_recording_ids(self):
        recs = os.listdir(Config.recordings_dir())
        extracted = [rec_id for rec_id in recs if self.is_extracted(rec_id)]
        return list(sorted(extracted))

    def load(self, recording_id) -> Recording:
        logging.info("Loading recording {}".format(recording_id))
        full_path = self.full_path(recording_id)
        recording = Recording(full_path)
        logging.info("Loading recording {} done".format(recording_id))
        return recording

    def full_path(self, recording_id: str) -> str:
        return join(Config.recordings_dir(), recording_id)

    def is_extracted(self, recording_id: str):
        return os.path.exists(join(self.full_path(recording_id), recording_id, ".extracted"))
