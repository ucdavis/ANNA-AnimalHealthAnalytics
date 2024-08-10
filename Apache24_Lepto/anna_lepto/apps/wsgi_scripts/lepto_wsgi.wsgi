# This is a wsgi script to host Lepto Server on Apache Server.

import sys

sys.path.insert(0, 'C:\\Apache24_Lepto\\anna_lepto\\app\\scripts')

from anna_leptoFlask import app as application