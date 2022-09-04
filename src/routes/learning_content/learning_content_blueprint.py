# -*- coding: utf-8 -*-
"""Module containing the functions for instantiating the blueprint
for Learning Content Models

Returns:
    function: Function for instantiating the Learning Content Blueprint.
"""
from firebase_admin import App
from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from src.services.utils.controllers.generics.create_one_controller import (
    create_one_controller_factory,
)
from src.services.utils.controllers.generics.get_all_controller import (
    get_all_controller_factory,
)
from src.services.utils.controllers.generics.get_by_id_controller import (
    get_by_id_controller_factory,
)
from src.services.utils.controllers.generics.update_by_id_controller import (
    update_by_id_controller_factory,
)


def create_learning_content_blueprint(
    db: SQLAlchemy, models: dict, schemas: dict, firebase_app: App
) -> Blueprint:
    """Function to Create the Learning Content Blueprint

    Args:
        db (SQLAlchemy): Database Singleton Object Containing all of the Connection Params.
        models (dict): Model Dictionary.
        schemas (dict): Schema Dictionary.
        firebase_app (App) : Firebase App Instance.
    Returns:
        Blueprint: Blueprint for the Learning Content Class.
    """
    blueprint = Blueprint(
        name="/learning_content", import_name=__name__, url_prefix="/learning_content"
    )

    create_one_controller_factory(
        db,
        models["LearningContent"],
        schemas["LearningContent_DefaultSchema"],
        blueprint,
        expected_role="teacher",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    get_all_controller_factory(
        models["LearningContent"],
        schemas["LearningContent_DefaultSchema"],
        blueprint,
        expected_role="student",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    get_by_id_controller_factory(
        models["LearningContent"],
        schemas["LearningContent_DefaultSchema"],
        blueprint,
        expected_role="student",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    update_by_id_controller_factory(
        db,
        models["LearningContent"],
        schemas["LearningContent_DefaultSchema"],
        blueprint,
        expected_role="teacher",
        firebase_app=firebase_app,
        user_model=models["User"],
    )

    return blueprint
