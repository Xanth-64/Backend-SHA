# -*- coding: utf-8 -*-
"""Module containing the functions for instantiating the blueprint
for Template Models

Returns:
    function: Function for instantiating the Template Blueprint.
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


def create_template_blueprint(db: SQLAlchemy, models, schemas) -> Blueprint:
    """Function to Create the Template Blueprint

    Args:
        db (SQLAlchemy): Database Singleton Object Containing all of the Connection Params.
        models (dict): Model Dictionary.
        schemas (dict): Schema Dictionary.

    Returns:
        Blueprint: Blueprint for the Template Class.
    """
    blueprint = Blueprint(
        name="/templates", import_name=__name__, url_prefix="/templates"
    )

    create_one_controller_factory(
        db,
        models["Template"],
        schemas["Template_DefaultSchema"],
        blueprint,
    )
    get_all_controller_factory(
        models["Template"],
        schemas["Template_DefaultSchema"],
        blueprint,
    )
    get_by_id_controller_factory(
        models["Template"],
        schemas["Template_DefaultSchema"],
        blueprint,
    )
    update_by_id_controller_factory(
        db,
        models["Template"],
        schemas["Template_DefaultSchema"],
        blueprint,
    )
    return blueprint
