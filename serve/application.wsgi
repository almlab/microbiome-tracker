import os
import sys
current_location = os.path.dirname(os.path.realpath(__file__))+'/'
sys.path.append(current_location)
sys.path.append(current_location+'../src/')

import serve
serve.init_db()
from serve import app as application

import monitor
monitor.start(interval=1.0)
