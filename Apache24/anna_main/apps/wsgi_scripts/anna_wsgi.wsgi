# This is a wsgi script to host ANNA Main Server on Apache Server.

import sys

sys.path.insert(0, 'C:\\Apache24\\anna_main\\app\\scripts')

from anna_mainFlask import app as application