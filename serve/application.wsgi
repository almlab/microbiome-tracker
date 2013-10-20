import sys
sys.path.append('/var/www/microbiome-tracker/src/')

from serve import app as application

import monitor
monitor.start(interval=1.0)
