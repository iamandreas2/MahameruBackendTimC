import os
from flask import Flask
from .model import db_channel
from . import channel
# file ini udah bener

def create_app(test_config=None):
    app = Flask(__name__)
    
    app.config.from_pyfile('settings.cfg', silent=True)
    app.register_blueprint(channel.bp)

    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db_channel.init_app(app)

    @app.route('/')
    def index():
        print("test")
        return "Mahameru Chat"

    return app
