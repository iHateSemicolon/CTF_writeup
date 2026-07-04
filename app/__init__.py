from flask import Flask
from flask_wtf import CSRFProtect
from app.config import Config
from app import database

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config.update(
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
    )
    CSRFProtect(app)
    database.init_db()

    from app.routes.auth import auth_bp
    from app.routes.notes import notes_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(notes_bp)

    return app