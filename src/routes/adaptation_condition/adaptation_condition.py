# -*- coding: utf-8 -*-
"""Module containing the functions for instantiating the blueprint
for Adaptation Condition Models

Returns:
    function: Function for instantiating the Adaptation Condition Blueprint.
"""
from firebase_admin import App
from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy

from src.services.utils.controllers.generics.create_one_controller import (
    create_one_controller_factory,
)
from src.services.utils.controllers.adaptation_condition.delete_adaption_condition_by_id import (
    delete_adaptation_condition_by_id_controller_factory,
)
from src.services.utils.controllers.generics.update_by_id_controller import (
    update_by_id_controller_factory,
)


def create_adaptation_condition_blueprint(
    db: SQLAlchemy, models: dict, schemas: dict, firebase_app: App
) -> Blueprint:
    """Function to Create the Adaptation Condition Blueprint

    Args:
        db (SQLAlchemy): Database Singleton Object Containing all of the Connection Params.
        models (dict): Model Dictionary.
        schemas (dict): Schema Dictionary.
        firebase_app (App) : Firebase App Instance.

    Returns:
        Blueprint: Blueprint for the Topic Class.
    """
    blueprint = Blueprint(
        name="/adaptation_condition",
        import_name=__name__,
        url_prefix="/adaptation_condition",
    )

    create_one_controller_factory(
        db,
        models["AdaptationCondition"],
        schemas["AdaptationCondition_DefaultSchema"],
        blueprint,
        expected_role="teacher",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    update_by_id_controller_factory(
        db,
        models["AdaptationCondition"],
        schemas["AdaptationCondition_DefaultSchema"],
        blueprint,
        expected_role="teacher",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    delete_adaptation_condition_by_id_controller_factory(
        db,
        models,
        schemas,
        blueprint,
        expected_role="teacher",
        firebase_app=firebase_app,
        user_model=models["User"],
    )

    return blueprint
