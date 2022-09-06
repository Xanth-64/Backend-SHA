# -*- coding: utf-8 -*-
"""Module containing the functions for instantiating the blueprint
for Page Models

Returns:
    function: Function for instantiating the Page Blueprint.
"""
from firebase_admin import App
from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from src.services.utils.controllers.generics.delete_by_id_controller import (
    delete_by_id_controller_factory,
)
from src.services.utils.controllers.generics.get_by_id_controller import (
    get_by_id_controller_factory,
)
from src.services.utils.controllers.generics.update_by_id_controller import (
    update_by_id_controller_factory,
)
from src.services.utils.controllers.page.create_one_page import (
    create_one_page_controller_factory,
)
from src.services.utils.controllers.page.delete_one_page import (
    delete_one_page_controller_factory,
)
from src.services.utils.controllers.page.get_pages_for_template import (
    get_pages_for_template_factory,
)
from src.services.utils.controllers.page.get_triggered_adaptative_events_for_page import (
    get_triggered_adaptative_events_by_page_controller_factory,
)
from src.services.utils.controllers.page.switch_pages import (
    switch_page_controller_factory,
)


def create_page_blueprint(
    db: SQLAlchemy, models: dict, schemas: dict, firebase_app: App
) -> Blueprint:
    """Function to Create the Page Blueprint

    Args:
        db (SQLAlchemy): Database Singleton Object Containing all of the Connection Params.
        models (dict): Model Dictionary.
        schemas (dict): Schema Dictionary.
        firebase_app (App) : Firebase App Instance.

    Returns:
        Blueprint: Blueprint for the Page Class.
    """
    blueprint = Blueprint(name="/pages", import_name=__name__, url_prefix="/pages")
    sub_blueprint = Blueprint(
        name="/adaptative_events", import_name=__name__, url_prefix="/adaptative_events"
    )
    create_one_page_controller_factory(
        db,
        models,
        schemas["Page_PageInheritanceSchema"],
        blueprint,
        expected_role="teacher",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    get_pages_for_template_factory(
        models["Page"],
        schemas["Page_PageInheritanceSchema"],
        blueprint,
        expected_role="student",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    get_by_id_controller_factory(
        models["Page"],
        schemas["Page_PageInheritanceSchema"],
        blueprint,
        expected_role="student",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    update_by_id_controller_factory(
        db,
        models["Page"],
        schemas["Page_PageInheritanceSchema"],
        blueprint,
        expected_role="teacher",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    delete_one_page_controller_factory(
        db,
        models["Page"],
        schemas["Page_PageInheritanceSchema"],
        blueprint,
        expected_role="teacher",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    switch_page_controller_factory(
        db,
        models["Page"],
        schemas["Page_PageInheritanceSchema"],
        blueprint,
        expected_role="teacher",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    get_triggered_adaptative_events_by_page_controller_factory(
        models,
        schemas,
        blueprint=sub_blueprint,
        expected_role="student",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    blueprint.register_blueprint(sub_blueprint)
    return blueprint
