# -*- coding: utf-8 -*-
"""Module containing the functions for instantiating the blueprint
for Test Question Models

Returns:
    function: Function for instantiating the Test Question Blueprint.
"""
from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from src.services.utils.controllers.create_one_controller import (
    create_one_controller_factory,
)
from src.services.utils.controllers.get_all_controller import get_all_controller_factory
from src.services.utils.controllers.get_by_id_controller import (
    get_by_id_controller_factory,
)
from src.services.utils.controllers.update_by_id_controller import (
    update_by_id_controller_factory,
)


def create_test_question_blueprint(db: SQLAlchemy, models, schemas) -> Blueprint:
    """Function to Create the Test Question Blueprint

    Args:
        db (SQLAlchemy): Database Singleton Object Containing all of the Connection Params.
        models (dict): Model Dictionary.
        schemas (dict): Schema Dictionary.

    Returns:
        Blueprint: Blueprint for the Test Question Class.
    """
    blueprint = Blueprint(
        name="/test_questions", import_name=__name__, url_prefix="/test_questions"
    )

    create_one_controller_factory(
        db,
        models["TestQuestion"],
        schemas["TestQuestion_DefaultSchema"],
        blueprint,
    )
    get_all_controller_factory(
        models["TestQuestion"],
        schemas["TestQuestion_DefaultSchema"],
        blueprint,
    )
    get_by_id_controller_factory(
        models["TestQuestion"],
        schemas["TestQuestion_DefaultSchema"],
        blueprint,
    )
    update_by_id_controller_factory(
        db,
        models["TestQuestion"],
        schemas["TestQuestion_DefaultSchema"],
        blueprint,
    )
    return blueprint
