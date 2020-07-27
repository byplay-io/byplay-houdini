import logging
import os
from distutils.dir_util import mkpath
from typing import Dict

from byplay.config import Config
from byplay.helpers.util import join
import byplay.backend.api as byplay_api
from byplay.recording import Recording
from byplay.wrappers.ffmpeg import FFMPEG


class RecordingDownloader:
    def list_recording_ids(self):
        return byplay_api.recordings_list()

    def load(self, recording_id, on_status_update) -> Recording:
        logging.info("Loading recording {}".format(recording_id))
        on_status_update("Loading recording {}: fetching metadata".format(recording_id))
        recording_links = byplay_api.recording_links(recording_id)

        full_path = self.full_path(recording_id)

        self.download_to(
            recording_links,
            full_path,
            lambda m: on_status_update("Loading recording {}: downloading {}".format(recording_id, m))
        )

        on_status_update("Loading recording {}: extracting frames".format(recording_id))

        recording = Recording(full_path)
        self.extract_video_frames(recording)

        on_status_update("Loading recording {} done".format(recording_id))
        logging.info("Loading recording done")
        return recording

    def full_path(self, recording_id: str) -> str:
        return join(Config.recordings_dir(), recording_id)

    def extract_video_frames(self, recording: Recording):
        mkpath(recording.frames_dir)

        if len(os.listdir(recording.frames_dir)) > 5:
            logging.info("seem to have already extracted frames")
        else:
            FFMPEG().extract_frames(
                video_path=recording.video_path,
                frames_path=recording.camera_frames_path_ffmpeg
            )
            logging.info("Extracted frames")

    def download_to(self, links: Dict[str, str], dir_path: str, on_download):
        for filename, url in links.items():
            on_download(filename)
            file_path = join(dir_path, filename)
            if byplay_api.download_to(url=url, full_path=file_path):
                logging.info("Downloaded {}".format(filename))
            else:
                logging.info("Already downloaded {}".format(filename))
