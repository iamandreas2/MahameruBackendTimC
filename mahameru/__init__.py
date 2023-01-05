import os
from flask import Flask
from bson.json_util import dumps
#from . import user
from . import chat
from . import user
from . import contact
from flask_cors import CORS


def create_app(test_config=None):
    app = Flask(__name__)
    
    app.config.from_pyfile('settings.cfg', silent=True)
    CORS(app)
    #app.register_blueprint(user.bp)
    app.register_blueprint(chat.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(contact.bp)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        print("test")
        return "Mahameru Chat"
    
    return app
