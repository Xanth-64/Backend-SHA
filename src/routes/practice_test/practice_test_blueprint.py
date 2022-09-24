# -*- coding: utf-8 -*-
"""Module containing the functions for instantiating the blueprint
for Practice Test Models

Returns:
    function: Function for instantiating the Practice Test Blueprint.
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
from src.services.utils.controllers.practice_test.update_one_practice_test import (
    update_one_practice_test_controller_factory,
)
from src.services.utils.controllers.generics.update_by_id_controller import (
    update_by_id_controller_factory,
)
from src.services.utils.controllers.generics.get_all_with_pagination_controller import (
    get_all_with_pagination_controller_factory,
)


def create_practice_test_blueprint(
    db: SQLAlchemy, models: dict, schemas: dict, firebase_app: App
) -> Blueprint:
    """Function to Create the Practice Test Blueprint

    Args:
        db (SQLAlchemy): Database Singleton Object Containing all of the Connection Params.
        models (dict): Model Dictionary.
        schemas (dict): Schema Dictionary.
        firebase_app (App) : Firebase App Instance.

    Returns:
        Blueprint: Blueprint for the Practice Test Class.
    """
    blueprint = Blueprint(
        name="/practice_tests", import_name=__name__, url_prefix="/practice_tests"
    )
    sub_blueprints = {
        "teacher": Blueprint(
            name="/teacher", import_name=__name__, url_prefix="/teacher"
        ),
        "student": Blueprint(
            name="/student", import_name=__name__, url_prefix="/student"
        ),
    }
    create_one_controller_factory(
        db,
        models["PracticeTest"],
        schemas["PracticeTest_DefaultSchema"],
        blueprint,
        expected_role="teacher",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    get_all_controller_factory(
        models["PracticeTest"],
        schemas["PracticeTest_DefaultSchema"],
        blueprint,
        expected_role="student",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    # Controller for Getting By Id Subdivides Between Student and Teacher
    get_by_id_controller_factory(
        models["PracticeTest"],
        schemas["PracticeTest_WithAnswers"],
        sub_blueprints["teacher"],
        expected_role="teacher",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    get_by_id_controller_factory(
        models["PracticeTest"],
        schemas["PracticeTest_WithAnswers"],
        sub_blueprints["student"],
        expected_role="student",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    update_one_practice_test_controller_factory(
        db,
        models,
        schemas["PracticeTest_WithAnswers"],
        blueprint,
        expected_role="teacher",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    get_all_with_pagination_controller_factory(
        models["PracticeTest"],
        schemas["PracticeTest_DefaultSchema"],
        blueprint,
        expected_role="student",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    for sub_blueprint in sub_blueprints.values():
        blueprint.register_blueprint(sub_blueprint)
    return blueprint
