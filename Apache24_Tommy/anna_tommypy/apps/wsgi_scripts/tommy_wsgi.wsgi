# This is a wsgi script to host TommyPy Server on Apache Server.

import sys

sys.path.insert(0, 'C:\\Apache24_Tommy\\anna_tommypy\\app\\scripts')

from anna_tommyFlask import app as application