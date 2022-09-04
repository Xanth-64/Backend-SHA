# -*- coding: utf-8 -*-
"""Module containing the functions for instantiating the blueprint
for Adaptative Object Models

Returns:
    function: Function for instantiating the Adaptative Object Blueprint.
"""
from firebase_admin import App
from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy

from src.services.utils.controllers.generics.get_by_id_controller import (
    get_by_id_controller_factory,
)


def create_adaptative_object_blueprint(
    db: SQLAlchemy, models: dict, schemas: dict, firebase_app: App
) -> Blueprint:
    """Function to Create the Adaptative Object Blueprint

    Args:
        db (SQLAlchemy): Database Singleton Object Containing all of the Connection Params.
        models (dict): Model Dictionary.
        schemas (dict): Schema Dictionary.
        firebase_app (App) : Firebase App Instance.

    Returns:
        Blueprint: Blueprint for the Adaptative Object Class.
    """
    blueprint = Blueprint(
        name="/adaptative_object", import_name=__name__, url_prefix="/adaptative_object"
    )

    return blueprint
