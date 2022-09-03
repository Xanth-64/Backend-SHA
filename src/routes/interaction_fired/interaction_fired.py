# -*- coding: utf-8 -*-
"""Module containing the functions for instantiating the blueprint
for Interaction Fired Models

Returns:
    function: Function for instantiating the Interaction Fired Blueprint.
"""
from firebase_admin import App
from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy

from src.services.utils.controllers.interaction_fired.create_one_interaction_fired import (
    create_one_interaction_fired_factory,
)


def create_interaction_fired_blueprint(
    db: SQLAlchemy, models: dict, schemas: dict, firebase_app: App
) -> Blueprint:
    """Function to Create the Interaction Fired Blueprint

    Args:
        db (SQLAlchemy): Database Singleton Object Containing all of the Connection Params.
        models (dict): Model Dictionary.
        schemas (dict): Schema Dictionary.
        firebase_app (App) : Firebase App Instance.
    Returns:
        Blueprint: Blueprint for the Measurable Interaction Class.
    """
    blueprint = Blueprint(
        name="/interaction_fired",
        import_name=__name__,
        url_prefix="/interaction_fired",
    )

    create_one_interaction_fired_factory(
        db,
        models,
        schemas,
        blueprint,
        expected_role="user",
        firebase_app=firebase_app,
        user_model=models["User"],
    )

    return blueprint
