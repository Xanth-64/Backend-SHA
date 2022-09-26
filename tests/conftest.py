# -*- coding: utf-8 -*-
import os

import pytest
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from src.models.index import create_models
from src.schemas.index import create_schemas


def pytest_addoption(parser):
    # ability to test API on different hosts
    parser.addoption("--host", action="store", default="http://localhost:5000")


@pytest.fixture(scope="session")
def host(request):
    return request.config.getoption("--host")


@pytest.fixture(scope="session")
def api_v1_host(host):
    return os.path.join(host, "api")


@pytest.fixture(scope="session")
def app():
    return Flask(__name__)


@pytest.fixture(scope="session")
def db(app):
    return SQLAlchemy(app)


@pytest.fixture(scope="session")
def models(app, db):
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "postgresql://xanth:pasta_2000@localhost:5432/sha-test"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ECHO"] = False
    model = create_models(db)
    db.drop_all()
    db.create_all()
    return model


@pytest.fixture(scope="session")
def schemas(app, models):
    ma = Marshmallow(app)
    return create_schemas(ma, models)


@pytest.fixture(scope="session")
def blueprints(app: Flask):
    return app.blueprints
