# -*- coding: utf-8 -*-
"""Module containing the functions for instantiating the blueprint
for Test Question Models

Returns:
    function: Function for instantiating the Test Question Blueprint.
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
from src.services.utils.controllers.test_question.get_triggered_adaptative_events_for_test_question import (
    get_triggered_adaptative_events_by_test_question_controller_factory,
)


def create_test_question_blueprint(
    db: SQLAlchemy, models: dict, schemas: dict, firebase_app: App
) -> Blueprint:
    """Function to Create the Test Question Blueprint

    Args:
        db (SQLAlchemy): Database Singleton Object Containing all of the Connection Params.
        models (dict): Model Dictionary.
        schemas (dict): Schema Dictionary.
        firebase_app (App) : Firebase App Instance.

    Returns:
        Blueprint: Blueprint for the Test Question Class.
    """
    blueprint = Blueprint(
        name="/test_questions", import_name=__name__, url_prefix="/test_questions"
    )
    sub_blueprint = Blueprint(
        name="/adaptative_events", import_name=__name__, url_prefix="/adaptative_events"
    )
    create_one_controller_factory(
        db,
        models["TestQuestion"],
        schemas["TestQuestion_DefaultSchema"],
        blueprint,
        expected_role="teacher",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    get_all_controller_factory(
        models["TestQuestion"],
        schemas["TestQuestion_DefaultSchema"],
        blueprint,
        expected_role="student",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    get_by_id_controller_factory(
        models["TestQuestion"],
        schemas["TestQuestion_DefaultSchema"],
        blueprint,
        expected_role="student",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    update_by_id_controller_factory(
        db,
        models["TestQuestion"],
        schemas["TestQuestion_DefaultSchema"],
        blueprint,
        expected_role="teacher",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    get_triggered_adaptative_events_by_test_question_controller_factory(
        models,
        schemas,
        sub_blueprint,
        expected_role="student",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    blueprint.register_blueprint(sub_blueprint)
    return blueprint
