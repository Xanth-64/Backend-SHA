# -*- coding: utf-8 -*-
"""Module containing the functions for instantiating the blueprint
for Topic Precedence Models

Returns:
    function: Function for instantiating the Topic Precedence Blueprint.
"""
from firebase_admin import App
from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from src.services.utils.controllers.generics.get_all_controller import (
    get_all_controller_factory,
)
from src.services.utils.controllers.generics.get_all_with_pagination_controller import (
    get_all_with_pagination_controller_factory,
)
from src.services.utils.controllers.topic_prelation.create_topic_prelations import (
    create_topic_prelations_controller_factory,
)
from src.services.utils.controllers.generics.update_by_id_controller import (
    update_by_id_controller_factory,
)


def create_topic_precedence_blueprint(
    db: SQLAlchemy, models: dict, schemas: dict, firebase_app: App
) -> Blueprint:
    """Function to Create the Topic Precedence Blueprint

    Args:
        db (SQLAlchemy): Database Singleton Object Containing all of the Connection Params.
        models (dict): Model Dictionary.
        schemas (dict): Schema Dictionary.
        firebase_app (App) : Firebase App Instance.

    Returns:
        Blueprint: Blueprint for the Topic Precedence Class.
    """
    blueprint = Blueprint(
        name="/topics/prelations", import_name=__name__, url_prefix="/topics/prelations"
    )
    get_all_controller_factory(
        models["TopicPrecedence"],
        schemas["TopicPrecedence_TopicPrecedenceRelationSchema"],
        blueprint,
        expected_role="student",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    get_all_with_pagination_controller_factory(
        models["TopicPrecedence"],
        schemas["TopicPrecedence_TopicPrecedenceRelationSchema"],
        blueprint,
        expected_role="student",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    create_topic_prelations_controller_factory(
        db,
        models,
        schemas,
        blueprint,
        expected_role="teacher",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    update_by_id_controller_factory(
        db,
        models["TopicPrecedence"],
        schemas["TopicPrecedence_DefaultSchema"],
        blueprint,
        expected_role="teacher",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    return blueprint
