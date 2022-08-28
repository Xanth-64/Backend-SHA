# -*- coding: utf-8 -*-
"""Module containing the functions for instantiating the blueprint
for Learning Style Models

Returns:
    function: Function for instantiating the Learning Style Blueprint.
"""
from firebase_admin import App
from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy

from src.services.utils.controllers.learning_style.update_one_learning_style import (
    update_one_learning_style_controller_factory,
)


def create_learning_style_blueprint(
    db: SQLAlchemy, models: dict, schemas: dict, firebase_app: App
) -> Blueprint:
    """Function to Create the Learning Style Blueprint

    Args:
        db (SQLAlchemy): Database Singleton Object Containing all of the Connection Params.
        models (dict): Model Dictionary.
        schemas (dict): Schema Dictionary.
        firebase_app (App) : Firebase App Instance.
    Returns:
        Blueprint: Blueprint for the Learning Style Class.
    """
    blueprint = Blueprint(
        name="/learning_style", import_name=__name__, url_prefix="/learning_style"
    )

    update_one_learning_style_controller_factory(
        db=db,
        models=models,
        learning_style_schema=schemas["LearningStyle_DefaultSchema"],
        blueprint=blueprint,
        expected_role="user",
        firebase_app=firebase_app,
        user_model=models["User"],
    )

    return blueprint
