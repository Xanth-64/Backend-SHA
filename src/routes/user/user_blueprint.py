# -*- coding: utf-8 -*-
"""Module containing the functions for instantiating the blueprint
for User Models

Returns:
    function: Function for instantiating the User Blueprint.
"""
from firebase_admin import App
from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from src.services.utils.controllers.generics.get_all_controller import (
    get_all_controller_factory,
)
from src.services.utils.controllers.generics.get_by_id_controller import (
    get_by_id_controller_factory,
)
from src.services.utils.controllers.generics.update_by_id_controller import (
    update_by_id_controller_factory,
)
from src.services.utils.controllers.user.enable_role import (
    enable_role_controller_factory,
)
from src.services.utils.controllers.user.get_all_users_with_pagination_controller import (
    get_all_users_with_pagination_controller_factory,
)


def create_user_blueprint(
    db: SQLAlchemy, models: dict, schemas: dict, firebase_app: App
) -> Blueprint:
    """Function to Create the User Blueprint

    Args:
        db (SQLAlchemy): Database Singleton Object Containing all of the Connection Params.
        models (dict): Model Dictionary.
        schemas (dict): Schema Dictionary.
        firebase_app (App) : Firebase App Instance.

    Returns:
        Blueprint: Blueprint for the User Class.
    """
    blueprint = Blueprint(name="/users", import_name=__name__, url_prefix="/users")

    get_all_controller_factory(
        models["User"],
        schemas["User_DefaultSchema"],
        blueprint,
        expected_role="teacher",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    get_by_id_controller_factory(
        models["User"],
        schemas["User_DefaultSchema"],
        blueprint,
        expected_role="teacher",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    update_by_id_controller_factory(
        db,
        models["User"],
        schemas["User_DefaultSchema"],
        blueprint,
        expected_role="teacher",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    get_all_users_with_pagination_controller_factory(
        models,
        schemas["User_UserAndRoleSchema"],
        blueprint,
        expected_role="teacher",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    enable_role_controller_factory(
        db,
        models,
        schemas["User_UserAndRoleSchema"],
        blueprint,
        expected_role="teacher",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    return blueprint
