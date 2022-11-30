import os
from flask import Flask
from . import db
from channel import channel


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_pyfile('settings.cfg', silent=True)
    app.register_blueprint(channel)

    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    @app.route('/')
    def index():
        print("test")
        return "Mahameru Chat"


    return app
