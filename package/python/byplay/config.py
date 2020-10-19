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
    _recordings_dir = None

    @staticmethod
    def is_dev():
        return True

    @staticmethod
    def build():
        return 1002

    @staticmethod
    def user_id():
        return Config._user_id

    @staticmethod
    def recordings_dir():
        return Config._recordings_dir

    @staticmethod
    def ffmpeg_path():
        return os.environ.get(u"BYPLAY_FFMPEG_PATH") or u"ffmpeg"

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
    def user_config_path():
        return os.environ[u"BYPLAY_SYSTEM_DATA_PATH"]

    @staticmethod
    def log_file_path():
        return os.environ[u"BYPLAY_PLUGIN_LOG_PATH"]

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
        logging.debug(u"Successfully read config file, {}".format(data))
        Config._user_id = data.get(u"userId")
        Config._recordings_dir = data.get(u"recordingsDir")

    @staticmethod
    def setup_logger():
        path = Config.log_file_path()
        mkpath(os.path.dirname(path))
        logging.basicConfig(filename=path, format=u'%(asctime)s - [%(levelname)s]: %(message)s', level=logging.DEBUG)
