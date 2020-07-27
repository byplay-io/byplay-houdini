from __future__ import absolute_import
import logging
import os
from distutils.dir_util import mkpath


from byplay.config import Config
from byplay.helpers.util import join
import byplay.backend.api as byplay_api
from byplay.recording import Recording
from byplay.wrappers.ffmpeg import FFMPEG


class RecordingDownloader(object):
    def list_recording_ids(self):
        return byplay_api.recordings_list()

    def load(self, recording_id, on_status_update):
        logging.info(u"Loading recording {}".format(recording_id))
        on_status_update(u"Loading recording {}: fetching metadata".format(recording_id))
        recording_links = byplay_api.recording_links(recording_id)

        full_path = self.full_path(recording_id)

        self.download_to(
            recording_links,
            full_path,
            lambda m: on_status_update(u"Loading recording {}: downloading {}".format(recording_id, m))
        )

        on_status_update(u"Loading recording {}: extracting frames".format(recording_id))

        recording = Recording(full_path)
        self.extract_video_frames(recording)

        on_status_update(u"Loading recording {} done".format(recording_id))
        logging.info(u"Loading recording done")
        return recording

    def full_path(self, recording_id):
        return join(Config.recordings_dir(), recording_id)

    def extract_video_frames(self, recording):
        mkpath(recording.frames_dir)

        if len(os.listdir(recording.frames_dir)) > 5:
            logging.info(u"seem to have already extracted frames")
        else:
            FFMPEG().extract_frames(
                video_path=recording.video_path,
                frames_path=recording.camera_frames_path_ffmpeg
            )
            logging.info(u"Extracted frames")

    def download_to(self, links, dir_path, on_download):
        for filename, url in links.items():
            on_download(filename)
            file_path = join(dir_path, filename)
            if byplay_api.download_to(url=url, full_path=file_path):
                logging.info(u"Downloaded {}".format(filename))
            else:
                logging.info(u"Already downloaded {}".format(filename))
