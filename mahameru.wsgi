#! /opt/rh/rh-python38/root/usr/bin/python
# ini kg usah dipikirin
import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/html/mahameru')
#sys.stdout = open('output.logs', 'w')
from mahameru import create_app
application = create_app()
