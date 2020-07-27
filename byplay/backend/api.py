import logging
import os
from distutils.dir_util import mkpath
from typing import Dict

import shutil

from byplay.config import Config

import requests


def recordings_list() -> [str]:
    return _do_api_v1_get_request("/recordings")["recordings"]


def recording_links(recording_id: str) -> Dict[str, str]:
    return _do_api_v1_get_request("/recordings/{}/links".format(recording_id))["links"]


def download_to(url: str, full_path: str) -> bool:
    if os.path.exists(full_path):
        return False
    mkpath(os.path.dirname(full_path))

    with requests.get(url, stream=True) as r:
        with open(full_path, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

    return True


def check_error():
    return _do_api_v1_get_request("/check")['error']


def _do_api_v1_get_request(path: str):
    full_url = "{}/{}".format(Config.api_base(), path)
    logging.debug("Api request to {}".format(full_url))
    response = requests.get(full_url, headers=_api_headers())
    data = response.json()
    logging.debug(data)
    return data

def _api_headers():
    return {
        'x-access-token': Config.api_access_token(),
        'x-package': Config.current_package_version()
    }
