# -*- coding: utf-8 -*-
"""Flask Application for Data Fetching & Filtering.

This is a REST API build using Flask, Marshmallow and SQLAlchemy
for Data Fetching & Filtering, Also includes the logic required
for Bayesian Network representation of data.

"""
import json
import traceback
from os import environ, getpid

import firebase_admin
from flasgger import Swagger
from flask import Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException

from src.models.index import create_models
from src.routes.index import create_blueprints
from src.schemas.index import create_schemas


def create_app():
    """Creates a Flask Application for Data Fetching & Filtering. and Business Logic

    Returns:
        Flask:Flask Application for Data Fetching & Filtering and Business Logic.
    """

    app = Flask(__name__)
    CORS(app)
    ## Initialize Config
    app.config.from_pyfile("config.py")

    # Firebase Admin Configuration
    try:
        firebase_app = firebase_admin.initialize_app(name=f"firebase-admin {getpid()}")
    except ValueError:
        firebase_app = firebase_admin.get_app(name=f"firebase-admin {getpid()}")
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
    app.config["FLASK_ENV"] = (
        "development" if environ.get("ENV_NAME") == "DEV" else "production"
    )

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        environ["DATABASE_URL"].replace("postgres:", "postgresql:")
        if environ.get("DATABASE_URL")
        else "postgresql://localhost:5432"
    )
    db = SQLAlchemy(app)
    ma = Marshmallow(app)
    # Database Model Instantiation
    models = create_models(db)
    # HACK This way of creating models is not correct. Change to migrations approach.
    db.drop_all()
    db.create_all()

    # API Schema Instantiation
    schemas = create_schemas(ma=ma, models=models)

    # API Middleware Instantiation

    # Swagger Docs Initialization
    swagger = Swagger(app)

    # API Routes Instantiation
    create_blueprints(db, models, schemas, app, firebase_app)

    # Route Configuration
    @app.route("/")
    def check_health():
        return {"sucess": True, "message": "SHA-API Online."}, 200

    # @app.errorhandler(500)
    # def handle_runtime_exception(e):
    #     return {
    #         "message": "Unexpected Runtime Exception Found",
    #         "name": str(e),
    #         "code": traceback.format_exc(),
    #     }, 500

    @app.errorhandler(HTTPException)
    def handle_http_exception(ex):
        """Return JSON instead of HTML for HTTP errors."""
        # start with the correct headers and status code from the error
        response = ex.get_response()
        # replace the body with JSON
        response.data = json.dumps(
            {
                "code": ex.code,
                "name": ex.name,
                "description": ex.description,
            }
        )
        response.content_type = "application/json"
        return response

    @app.errorhandler(Exception)
    def handle_exception(ex):
        # pass through HTTP errors
        if isinstance(ex, HTTPException):
            return ex

        # now you're handling non-HTTP exceptions only
        return {
            "success": False,
            "code": {"name": str(ex), "traceback": traceback.format_exc()},
            "message": "Unexpected Runtime exception Found",
        }, 500

    db.init_app(app)
    return app
