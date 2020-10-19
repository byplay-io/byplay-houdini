import json
import os
import logging
from distutils.dir_util import mkpath

from byplay.helpers.util import join
import sys


class Config:
    _recordings_dir = None

    @staticmethod
    def is_dev() -> bool:
        return True

    @staticmethod
    def build() -> str:
        return 1002

    @staticmethod
    def user_id() -> str:
        return Config._user_id

    @staticmethod
    def recordings_dir() -> str:
        return Config._recordings_dir

    @staticmethod
    def ffmpeg_path() -> str:
        return os.environ.get("BYPLAY_FFMPEG_PATH") or "ffmpeg"

    @staticmethod
    def utility_geo_path() -> str:
        return ""

    @staticmethod
    def current_package_version() -> str:
        return "Houdini:0.1.0-{}".format(sys.platform)

    @staticmethod
    def video_frames_ext() -> str:
        return "png"

    @staticmethod
    def user_config_path():
        return os.environ["BYPLAY_SYSTEM_DATA_PATH"]

    @staticmethod
    def log_file_path():
        return os.environ["BYPLAY_PLUGIN_LOG_PATH"]

    @staticmethod
    def _read_config_file():
        try:
           config_path = Config.user_config_path()
           if os.path.exists(config_path):
               with open(config_path) as f:
                   logging.debug("Successfully read config file")
                   return json.loads(f.read())
        except Exception as e:
            logging.error("exception while reading config {}".format(config_path))
            logging.exception(e)
            return {}
        return {}

    @staticmethod
    def read():
        data = Config._read_config_file()
        logging.debug("Successfully read config file, {}".format(data))
        Config._user_id = data.get("userId")
        Config._recordings_dir = data.get("recordingsDir")

    @staticmethod
    def setup_logger():
        path = Config.log_file_path()
        mkpath(os.path.dirname(path))
        logging.basicConfig(filename=path, format='%(asctime)s - [%(levelname)s]: %(message)s', level=logging.DEBUG)