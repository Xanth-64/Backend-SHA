# -*- coding: utf-8 -*-
"""Module containing the functions for instantiating the blueprint
for Test Attempt Models

Returns:
    function: Function for instantiating the Test Attempt Blueprint.
"""
from firebase_admin import App
from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from src.services.utils.controllers.generics.get_by_id_controller import (
    get_by_id_controller_factory,
)
from src.services.utils.controllers.test_attempt.create_one_test_attempt import (
    create_one_test_attempt_controller_factory,
)
from src.services.utils.controllers.test_attempt.get_by_test_id import (
    get_by_test_id_controller_factory,
)


def create_test_attempt_blueprint(
    db: SQLAlchemy, models: dict, schemas: dict, firebase_app: App
) -> Blueprint:
    """Function to Create the Test Attempt Blueprint

    Args:
        db (SQLAlchemy): Database Singleton Object Containing all of the Connection Params.
        models (dict): Model Dictionary.
        schemas (dict): Schema Dictionary.
        firebase_app (App) : Firebase App Instance.

    Returns:
        Blueprint: Blueprint for the Test Attempt Class.
    """
    blueprint = Blueprint(
        name="/test_attempt", import_name=__name__, url_prefix="/test_attempt"
    )
    sub_blueprints = {
        "ByID": Blueprint(name="/by_id", import_name=__name__, url_prefix="/by_id"),
        "ByTestID": Blueprint(
            name="/by_test_id", import_name=__name__, url_prefix="/by_test_id"
        ),
    }

    create_one_test_attempt_controller_factory(
        db=db,
        models=models,
        schemas=schemas,
        blueprint=blueprint,
        expected_role="student",
        firebase_app=firebase_app,
        user_model=models["User"],
    )

    get_by_id_controller_factory(
        model=models["TestAttempt"],
        schema=schemas["TestAttempt_CompleteSchema"],
        blueprint=sub_blueprints["ByID"],
        expected_role="student",
        firebase_app=firebase_app,
        user_model=models["User"],
    )

    get_by_test_id_controller_factory(
        models=models,
        schemas=schemas,
        blueprint=sub_blueprints["ByTestID"],
        expected_role="student",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    for sub_blueprint in sub_blueprints.values():
        blueprint.register_blueprint(sub_blueprint)

    return blueprint
