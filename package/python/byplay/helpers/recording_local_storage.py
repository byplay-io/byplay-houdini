from __future__ import absolute_import
import logging
import os

from byplay.config import Config
from byplay.helpers.util import join
from byplay.recording import Recording


class RecordingLocalStorage(object):
    def list_recording_ids(self):
        recs = os.listdir(Config.recordings_dir())
        logging.info(u"List of files: {} -> {}".format(Config.recordings_dir(), recs))
        extracted = [rec_id for rec_id in recs if self.is_extracted(rec_id)]
        return list(sorted(extracted))

    def load(self, recording_id):
        logging.info(u"Loading recording {}".format(recording_id))
        full_path = self.full_path(recording_id)
        recording = Recording(full_path, recording_id)
        logging.info(u"Loading recording {} done".format(recording_id))
        return recording

    def full_path(self, recording_id):
        return join(Config.recordings_dir(), recording_id)

    def is_extracted(self, recording_id):
        path = join(self.full_path(recording_id), u".extracted")
        exists = os.path.exists(path)
        logging.info(u"rec: {} / {}".format(path, exists))
        return exists

