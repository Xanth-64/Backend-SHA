# -*- coding: utf-8 -*-
from os import environ
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger


def create_app():
    app = Flask(__name__)

    app.config["SWAGGER"] = {
        "title": "Backend de Sistema de Hipermedia Adaptativo Educativo",
    }
    app.config["SQLALCHEMY_ECHO"] = (
        environ["ENV_NAME"] == "DEV" or environ["ENV_NAME"] == "STAGING"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = (
        environ["ENV_NAME"] == "DEV" or environ["ENV_NAME"] == "STAGING"
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        environ["DATABASE_URL"].replace("postgres", "postgresql")
        if environ.get("DATABASE_URL")
        else "postgresql://postgres:peer@localhost:5433"
    )
    db = SQLAlchemy(app)
    db.create_all()

    swagger = Swagger(app)
    ## Initialize Config
    app.config.from_pyfile("config.py")

    @app.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"

    db.init_app(app)
    return app
