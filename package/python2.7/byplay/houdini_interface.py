from __future__ import absolute_import
import logging
import sys
import os.path
from os.path import join

def joinw(*args):
    return os.path.join(*args).replace(u"\\", u"/")

cached_hou = None

def get_hou():
    global cached_hou

    if cached_hou is not None:
        return cached_hou[1]

    logging.debug(u"Getting hou ref")

    if u'hou' in sys.modules:
        cached_hou = (None, sys.modules[u'hou'])
        logging.debug(u"Got hou from env")
        return cached_hou[1]

    if os.name == u'nt':
        hfs = u"C:/Program Files/Side Effects Software/Houdini 17.5.360"
        sys.path.append(joinw(hfs, u"python27/lib/site-packages"))
        sys.path.append(joinw(hfs, u"python27/libs"))
        sys.path.append(joinw(hfs, u"python27/lib"))
        sys.path.append(joinw(hfs, u"houdini", u"python2.7libs"))
    else:
        hfs = u'/Applications/Houdini/Current/Frameworks/Houdini.framework/Versions/Current/Resources'
        hou_path = join(hfs, u"houdini", u"python%d.%dlibs" % (sys.version_info[:2]))

        if hou_path not in sys.path:
            sys.path.append(hou_path)
        sys.path.append(join(hfs, u'Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages'))

    import hrpyc
    cached_hou = hrpyc.import_remote_module()
    logging.debug(u"Got hou from remote module")
    return cached_hou[1]
