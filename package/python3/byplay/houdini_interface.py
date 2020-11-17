import logging
import sys
import os.path
from os.path import join

def joinw(*args):
    return os.path.join(*args).replace("\\", "/")

cached_hou = None

def get_hou():
    global cached_hou

    if cached_hou is not None:
        return cached_hou[1]

    logging.debug("Getting hou ref")

    if 'hou' in sys.modules:
        cached_hou = (None, sys.modules['hou'])
        logging.debug("Got hou from env")
        return cached_hou[1]

    if os.name == 'nt':
        hfs = "C:/Program Files/Side Effects Software/Houdini 17.5.360"
        sys.path.append(joinw(hfs, "python27/lib/site-packages"))
        sys.path.append(joinw(hfs, "python27/libs"))
        sys.path.append(joinw(hfs, "python27/lib"))
        sys.path.append(joinw(hfs, "houdini", "python2.7libs"))
    else:
        hfs = '/Applications/Houdini/Current/Frameworks/Houdini.framework/Versions/Current/Resources'
        hou_path = join(hfs, "houdini", "python%d.%dlibs" % (sys.version_info[:2]))

        if hou_path not in sys.path:
            sys.path.append(hou_path)
        sys.path.append(join(hfs, 'Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages'))

    import hrpyc
    cached_hou = hrpyc.import_remote_module()
    logging.debug("Got hou from remote module")
    return cached_hou[1]
