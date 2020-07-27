import json
import os
import logging
from distutils.dir_util import mkpath
from byplay.helpers.util import join
import sys


class Config:
    _access_token = None
    _recordings_dir = None

    @staticmethod
    def is_dev() -> bool:
        return False

    @staticmethod
    def api_base() -> str:
        if Config.is_dev():
            return "http://localhost:8080/api/v1"
        return "https://client-recordings-registry-v6o4nieboq-ez.a.run.app/api/v1"

    @staticmethod
    def api_access_token() -> str:
        return Config._access_token

    @staticmethod
    def recordings_dir() -> str:
        return Config._recordings_dir

    @staticmethod
    def ffmpeg_path() -> str:
        return os.environ.get("FFMPEG_PATH") or "ffmpeg"

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
    def store_access_token(access_token: str):
        Config.store_value('access_token', access_token)
        Config._access_token = access_token

    @staticmethod
    def store_byplay_recordings_dir(recordings_dir: str):
        Config.store_value('recordings_dir', recordings_dir)
        Config._recordings_dir = recordings_dir
        pass

    @staticmethod
    def system_data_path():
        return os.environ["BYPLAY_SYSTEM_DATA_PATH"]

    @staticmethod
    def user_config_path():
        return join(Config.system_data_path(), "user_config.json")

    @staticmethod
    def log_file_path():
        return join(Config.system_data_path(), "byplay.log")

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
        logging.debug("Successfully read config file")
        Config._access_token = data.get("access_token")
        Config._recordings_dir = data.get("recordings_dir")

    @staticmethod
    def store_value(key, value):
        data = Config._read_config_file()
        data[key] = value
        config_path = Config.user_config_path()
        mkpath(os.path.dirname(config_path))
        with open(config_path, "wb") as f:
            json.dump(data, f)
        logging.debug("Stored new value for '{}' in config".format(key))

    @staticmethod
    def setup_logger():
        path = Config.log_file_path()
        mkpath(os.path.dirname(path))
        logging.basicConfig(filename=path, format='%(asctime)s - [%(levelname)s]: %(message)s', level=logging.DEBUG)