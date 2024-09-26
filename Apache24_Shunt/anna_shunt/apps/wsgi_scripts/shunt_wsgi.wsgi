# This is a wsgi script to host Shunt Server on Apache Server.

import sys

sys.path.insert(0, 'C:\\Apache24_Shunt\\anna_shunt\\app\\scripts')

from anna_shuntFlask import app as application