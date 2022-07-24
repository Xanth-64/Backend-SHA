# -*- coding: utf-8 -*-
"""Module containing the functions for instantiating the blueprint
for Page Models

Returns:
    function: Function for instantiating the Page Blueprint.
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


def create_page_blueprint(db: SQLAlchemy, models, schemas) -> Blueprint:
    """Function to Create the Page Blueprint

    Args:
        db (SQLAlchemy): Database Singleton Object Containing all of the Connection Params.
        models (dict): Model Dictionary.
        schemas (dict): Schema Dictionary.

    Returns:
        Blueprint: Blueprint for the Page Class.
    """
    blueprint = Blueprint(name="/pages", import_name=__name__, url_prefix="/pages")

    create_one_controller_factory(
        db,
        models["Page"],
        schemas["Page_DefaultSchema"],
        blueprint,
    )
    get_all_controller_factory(
        models["Page"],
        schemas["Page_DefaultSchema"],
        blueprint,
    )
    get_by_id_controller_factory(
        models["Page"],
        schemas["Page_DefaultSchema"],
        blueprint,
    )
    update_by_id_controller_factory(
        db,
        models["Page"],
        schemas["Page_DefaultSchema"],
        blueprint,
    )
    return blueprint
