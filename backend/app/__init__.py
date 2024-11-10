from flask import Flask
from .auth import auth_blueprint
from .chat import chat_blueprint

def create_app():
    app = Flask(__name__)

    # Register Blueprints
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(chat_blueprint, url_prefix='/chat')

    return app
