from __future__ import with_statement
from __future__ import absolute_import
import logging
import os
from distutils.dir_util import mkpath


import shutil

from byplay.config import Config

import requests
from io import open


def recordings_list():
    return _do_api_v1_get_request(u"/recordings")[u"recordings"]


def recording_links(recording_id):
    return _do_api_v1_get_request(u"/recordings/{}/links".format(recording_id))[u"links"]


def download_to(url, full_path):
    if os.path.exists(full_path):
        return False
    mkpath(os.path.dirname(full_path))

    with requests.get(url, stream=True) as r:
        with open(full_path, u'wb') as f:
            shutil.copyfileobj(r.raw, f)

    return True


def check_error():
    return _do_api_v1_get_request(u"/check")[u'error']


def _do_api_v1_get_request(path):
    full_url = u"{}/{}".format(Config.api_base(), path)
    logging.debug(u"Api request to {}".format(full_url))
    response = requests.get(full_url, headers=_api_headers())
    data = response.json()
    logging.debug(data)
    return data

def _api_headers():
    return {
        u'x-access-token': Config.api_access_token(),
        u'x-package': Config.current_package_version()
    }
