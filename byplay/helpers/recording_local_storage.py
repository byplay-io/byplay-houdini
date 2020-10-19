import logging
import os

from byplay.config import Config
from byplay.helpers.util import join
from byplay.recording import Recording


class RecordingLocalStorage:
    def list_recording_ids(self):
        recs = os.listdir(Config.recordings_dir())
        logging.info("List of files: {} -> {}".format(Config.recordings_dir(), recs))
        extracted = [rec_id for rec_id in recs if self.is_extracted(rec_id)]
        return list(sorted(extracted))

    def load(self, recording_id) -> Recording:
        logging.info("Loading recording {}".format(recording_id))
        full_path = self.full_path(recording_id)
        recording = Recording(full_path, recording_id)
        logging.info("Loading recording {} done".format(recording_id))
        return recording

    def full_path(self, recording_id: str) -> str:
        return join(Config.recordings_dir(), recording_id)

    def is_extracted(self, recording_id: str):
        path = join(self.full_path(recording_id), ".extracted")
        exists = os.path.exists(path)
        logging.info("rec: {} / {}".format(path, exists))
        return exists

