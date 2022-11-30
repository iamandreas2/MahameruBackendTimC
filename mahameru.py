#!/usr/bin/python
import sys
import logging

activate_this = '/var/www/hello_world/hello_world/venv/bin/activate_this.py'
exec(open(activate_this).read())


logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/hello_world/")
