# -*- coding: utf-8 -*-
"""Flask Application for Data Fetching & Filtering.

This is a REST API build using Flask, Marshmallow and SQLAlchemy
for Data Fetching & Filtering, Also includes the logic required
for Bayesian Network representation of data.

"""
from os import environ

from flasgger import Swagger
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from src.models.index import create_models


def create_app():
    """Creates a Flask Application for Data Fetching & Filtering. and Business Logic

    Returns:
        Flask:Flask Application for Data Fetching & Filtering and Business Logic.
    """
    app = Flask(__name__)

    # Swagger Documentation Configuration
    app.config["SWAGGER"] = {
        "title": "Backend de Sistema de Hipermedia Adaptativo Educativo",
    }

    # SQLAlchemy Configuration Params
    app.config["SQLALCHEMY_ECHO"] = (
        environ.get("ENV_NAME") == "DEV" or environ.get("ENV_NAME") == "STAGING"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = (
        environ.get("ENV_NAME") == "DEV" or environ.get("ENV_NAME") == "STAGING"
    )

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        environ["DATABASE_URL"].replace("postgres:", "postgresql:")
        if environ.get("DATABASE_URL")
        else "postgresql://localhost:5432"
    )
    db = SQLAlchemy(app)

    # Database Model Instantiation
    models = create_models(db)
    db.drop_all()
    db.create_all()

    # API Schema Instantiation

    # API Routes Instantiation
    # HACK This way of creating models is not correct. Change to migrations approach.

    # Swagger Docs Initialization
    swagger = Swagger(app)

    ## Initialize Config
    app.config.from_pyfile("config.py")

    # Route Configuration
    @app.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"

    db.init_app(app)
    return app
