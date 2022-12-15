import os
from flask import Flask
from bson.json_util import dumps
from .model import db
from . import user
from . import chat


def create_app(test_config=None):
    app = Flask(__name__)
    
    app.config.from_pyfile('settings.cfg', silent=True)
    app.register_blueprint(user.bp)
    app.register_blueprint(chat.bp)

    
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
