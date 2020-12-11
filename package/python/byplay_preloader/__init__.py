import sys
import os

package_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))

if sys.version_info[0] == 2:
    sys.path.append(os.path.join(package_dir, "python2.7"))
else:
    sys.path.append(os.path.join(package_dir, "python3"))
