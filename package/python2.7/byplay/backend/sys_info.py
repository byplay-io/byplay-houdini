from __future__ import absolute_import
import logging
import platform

from byplay.config import Config
from byplay import get_hou


def sys_info():
    sysname, nodename, release, version, machine, _processor = platform.uname()

    hou_platform = u"unk"
    hou_version = u"unk"
    try:
        hou = get_hou()
        hou_platform = hou.applicationPlatformInfo()
        hou_version = hou.applicationVersionString()
    except Exception, e:
        logging.error(e)

    return {
        u"houdini.platform": hou_platform,
        u"houdini.version": hou_version,
        u"os.name": sysname,
        u"node.name": nodename,
        u"os.release": release,
        u"os.version": version
    }