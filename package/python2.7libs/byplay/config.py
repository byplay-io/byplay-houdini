from __future__ import with_statement
from __future__ import absolute_import
import json
import os
import logging
from distutils.dir_util import mkpath
from byplay.helpers.util import join
import sys
from io import open


class Config(object):
    _access_token = None
    _recordings_dir = None

    @staticmethod
    def is_dev():
        return False

    @staticmethod
    def api_base():
        if Config.is_dev():
            return u"http://localhost:8080/api/v1"
        return u"https://client-recordings-registry-v6o4nieboq-ez.a.run.app/api/v1"

    @staticmethod
    def api_access_token():
        return Config._access_token

    @staticmethod
    def recordings_dir():
        return Config._recordings_dir

    @staticmethod
    def ffmpeg_path():
        return os.environ.get(u"FFMPEG_PATH") or u"ffmpeg"

    @staticmethod
    def utility_geo_path():
        return u""

    @staticmethod
    def current_package_version():
        return u"Houdini:0.1.0-{}".format(sys.platform)

    @staticmethod
    def video_frames_ext():
        return u"png"

    @staticmethod
    def store_access_token(access_token):
        Config.store_value(u'access_token', access_token)
        Config._access_token = access_token

    @staticmethod
    def store_byplay_recordings_dir(recordings_dir):
        Config.store_value(u'recordings_dir', recordings_dir)
        Config._recordings_dir = recordings_dir
        pass

    @staticmethod
    def system_data_path():
        return os.environ[u"BYPLAY_SYSTEM_DATA_PATH"]

    @staticmethod
    def user_config_path():
        return join(Config.system_data_path(), u"user_config.json")

    @staticmethod
    def log_file_path():
        return join(Config.system_data_path(), u"byplay.log")

    @staticmethod
    def _read_config_file():
        try:
           config_path = Config.user_config_path()
           if os.path.exists(config_path):
               with open(config_path) as f:
                   logging.debug(u"Successfully read config file")
                   return json.loads(f.read())
        except Exception, e:
            logging.error(u"exception while reading config {}".format(config_path))
            logging.exception(e)
            return {}
        return {}

    @staticmethod
    def read():
        data = Config._read_config_file()
        logging.debug(u"Successfully read config file")
        Config._access_token = data.get(u"access_token")
        Config._recordings_dir = data.get(u"recordings_dir")

    @staticmethod
    def store_value(key, value):
        data = Config._read_config_file()
        data[key] = value
        config_path = Config.user_config_path()
        mkpath(os.path.dirname(config_path))
        with open(config_path, u"wb") as f:
            json.dump(data, f)
        logging.debug(u"Stored new value for '{}' in config".format(key))

    @staticmethod
    def setup_logger():
        path = Config.log_file_path()
        mkpath(os.path.dirname(path))
        logging.basicConfig(filename=path, format=u'%(asctime)s - [%(levelname)s]: %(message)s', level=logging.DEBUG)
