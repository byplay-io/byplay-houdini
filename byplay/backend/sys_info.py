import logging
import platform

from byplay.config import Config
from byplay import get_hou


def sys_info():
    sysname, nodename, release, version, machine = platform.uname()

    hou_platform = "unk"
    hou_version = "unk"
    try:
        hou = get_hou()
        hou_platform = hou.applicationPlatformInfo()
        hou_version = hou.applicationVersionString()
    except Exception as e:
        logging.error(e)

    return {
        "houdini.platform": hou_platform,
        "houdini.version": hou_version,
        "os.name": sysname,
        "node.name": nodename,
        "os.release": release,
        "os.version": version
    }