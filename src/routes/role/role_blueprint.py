# -*- coding: utf-8 -*-
"""Module containing the functions for instantiating the blueprint
for Roles Models

Returns:
    function: Function for instantiating the Roles Blueprint.
"""
from firebase_admin import App
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


def create_role_blueprint(
    db: SQLAlchemy, models: dict, schemas: dict, firebase_app: App
) -> Blueprint:
    """Function to Create the Role Blueprint

    Args:
        db (SQLAlchemy): Database Singleton Object Containing all of the Connection Params.
        models (dict): Model Dictionary.
        schemas (dict): Schema Dictionary.
        firebase_app (App) : Firebase App Instance.

    Returns:
        Blueprint: Blueprint for the Role Class.
    """
    blueprint = Blueprint(name="/roles", import_name=__name__, url_prefix="/roles")

    create_one_controller_factory(
        db,
        models["Role"],
        schemas["Role_DefaultSchema"],
        blueprint,
        expected_role="teacher",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    get_all_controller_factory(
        models["Role"],
        schemas["Role_DefaultSchema"],
        blueprint,
        expected_role="teacher",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    get_by_id_controller_factory(
        models["Role"],
        schemas["Role_DefaultSchema"],
        blueprint,
        expected_role="teacher",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    update_by_id_controller_factory(
        db,
        models["Role"],
        schemas["Role_DefaultSchema"],
        blueprint,
        expected_role="teacher",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    return blueprint
