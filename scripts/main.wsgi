#! /usr/bin/python3.9

import logging
import sys

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/html/scripts")
sys.path.append('/home/pi/.local/lib/python3.9/site-packages/zmq')
sys.path.append('/home/pi/.local/lib/python3.9/site-packages/flask')
from WebCamMain import app as application

application.secret_key = "1"
