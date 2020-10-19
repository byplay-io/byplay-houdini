from __future__ import absolute_import
import logging

import requests
from Queue import Queue
import threading


def _sync_post(url, params):
    logging.info(u"Doing async request to {}".format(url))
    res = requests.post(url, **params)
    logging.info(u"Async response: {}".format(res))


def async_post(url, **params):
    logging.info(u"Starting async request to {}".format(url))
    thread = threading.Thread(target=_sync_post, args=(url, params))
    thread.setDaemon(True)
    thread.start()
