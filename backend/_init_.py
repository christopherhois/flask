from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object('backend.config.Config')

    db.init_app(app)
    jwt.init_app(app)

    from .routes import example
    app.register_blueprint(example.bp)

    return app
