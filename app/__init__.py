import os
import json

from flask import Flask, render_template
from .db import ponds, ponds_activation, material,

def create_app(test_config=None):
    #create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('settings.cfg', silent=True)
    
    #ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
        db.init_app(app)

    @app.route('/index')
    @app.route('/')
    def index():
        return "Here's the page"
        
    @app.get('/')
    def pond():
      data = get_ponds({})
      data = dumps(data)
      return json.loads(data)


    return app