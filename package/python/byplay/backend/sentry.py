from __future__ import absolute_import
import logging
import sys
import time
import traceback
from datetime import datetime

import random

from byplay.backend.async_post import async_post
from byplay.backend.sys_info import sys_info
from byplay.config import Config
from itertools import imap


def generate_random_key(length):
    return u''.join(random.choice(u'0123456789abcdef') for _ in xrange(length))


STORE_URL = u"https://o244219.ingest.sentry.io/api/5394343/store/"
AUTH = u"""Sentry sentry_version=7,
sentry_timestamp={timestamp},
sentry_key=e6f05e834cb94683bff4831201c2b719,
sentry_client=byplay-houdini-python/1.0""".replace(u"\n", u"")


def capture_exception():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    logging.error(exc_value)
    try:
        payload = {
            u'event_id': generate_random_key(32),
            u'platform': u'python',
            u'culpit': u'-',
            u'timestamp': unicode(datetime.utcnow()),
            u'dist': Config.build(),
            u'tags': sys_info(),
            u'user': {
                u'id': Config.user_id(),
            },
            u"exception": {
                u"values": [{
                    u"type": exc_type.__name__,
                    u"value": exc_value.message,
                    u"stacktrace": {
                        u"frames": list(
                            imap(
                                lambda f: {
                                    u'filename': f[0],
                                    u'lineno': f[1] + 1,
                                    u'function': f[2]
                                },
                                traceback.extract_tb(exc_traceback)
                            )
                        )
                    }
                }]
            }
        }
        async_post(
            STORE_URL,
            headers={u"X-Sentry-Auth": AUTH.format(timestamp=int(time.time()))},
            json=payload
        )
    except Exception, sending_exception:
        # raise sending_exception
        logging.error(sending_exception)
