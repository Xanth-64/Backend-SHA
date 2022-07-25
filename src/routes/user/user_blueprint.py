# -*- coding: utf-8 -*-
"""Module containing the functions for instantiating the blueprint
for User Models

Returns:
    function: Function for instantiating the User Blueprint.
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


def create_user_blueprint(db: SQLAlchemy, models, schemas) -> Blueprint:
    """Function to Create the User Blueprint

    Args:
        db (SQLAlchemy): Database Singleton Object Containing all of the Connection Params.
        models (dict): Model Dictionary.
        schemas (dict): Schema Dictionary.

    Returns:
        Blueprint: Blueprint for the User Class.
    """
    blueprint = Blueprint(name="/users", import_name=__name__, url_prefix="/users")

    get_all_controller_factory(models["User"], schemas["User_DefaultSchema"], blueprint)
    get_by_id_controller_factory(
        models["User"], schemas["User_DefaultSchema"], blueprint
    )
    update_by_id_controller_factory(
        db, models["User"], schemas["User_DefaultSchema"], blueprint
    )
    return blueprint
