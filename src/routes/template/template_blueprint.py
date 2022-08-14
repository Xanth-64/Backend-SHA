# -*- coding: utf-8 -*-
"""Module containing the functions for instantiating the blueprint
for Template Models

Returns:
    function: Function for instantiating the Template Blueprint.
"""
from firebase_admin import App
from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from src.services.utils.controllers.template.get_templates_for_topic import (
    get_templates_for_topic_factory,
)
from src.services.utils.controllers.get_by_id_controller import (
    get_by_id_controller_factory,
)
from src.services.utils.controllers.update_by_id_controller import (
    update_by_id_controller_factory,
)
from src.services.utils.controllers.template.create_one_template import (
    create_one_template_controller_factory,
)
from src.services.utils.controllers.template.switch_templates import (
    switch_template_controller_factory,
)


def create_template_blueprint(
    db: SQLAlchemy, models: dict, schemas: dict, firebase_app: App
) -> Blueprint:
    """Function to Create the Template Blueprint

    Args:
        db (SQLAlchemy): Database Singleton Object Containing all of the Connection Params.
        models (dict): Model Dictionary.
        schemas (dict): Schema Dictionary.
        firebase_app (App) : Firebase App Instance.

    Returns:
        Blueprint: Blueprint for the Template Class.
    """
    blueprint = Blueprint(
        name="/templates", import_name=__name__, url_prefix="/templates"
    )

    create_one_template_controller_factory(
        db,
        models["Template"],
        schemas["Template_DefaultSchema"],
        blueprint,
        expected_role="teacher",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    get_templates_for_topic_factory(
        models["Template"],
        schemas["Template_DefaultSchema"],
        blueprint,
        expected_role="student",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    get_by_id_controller_factory(
        models["Template"],
        schemas["Template_DefaultSchema"],
        blueprint,
        expected_role="student",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    switch_template_controller_factory(
        db,
        models["Template"],
        schemas["Template_DefaultSchema"],
        blueprint,
        expected_role="teacher",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    update_by_id_controller_factory(
        db,
        models["Template"],
        schemas["Template_DefaultSchema"],
        blueprint,
        expected_role="teacher",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    return blueprint
