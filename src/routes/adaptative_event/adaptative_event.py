# -*- coding: utf-8 -*-
"""Module containing the functions for instantiating the blueprint
for Adaptative Event Models

Returns:
    function: Function for instantiating the Adaptative Event Blueprint.
"""
from firebase_admin import App
from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from src.services.utils.controllers.adaptative_event.create_one_adaptative_event import (
    create_one_adaptative_event_factory,
)
from src.services.utils.controllers.adaptative_event.delete_one_adaptative_event import (
    delete_one_adaptative_event_controller_factory,
)
from src.services.utils.controllers.adaptative_event.get_all_adaptative_events_by_adaptative_object import (
    get_all_adaptative_events_by_adaptative_object_controller_factory,
)
from src.services.utils.controllers.adaptative_event.switch_adaptative_events import (
    switch_adaptative_event_controller_factory,
)


def create_adaptative_event_blueprint(
    db: SQLAlchemy, models: dict, schemas: dict, firebase_app: App
) -> Blueprint:
    """Function to Create the Adaptative Event Blueprint

    Args:
        db (SQLAlchemy): Database Singleton Object Containing all of the Connection Params.
        models (dict): Model Dictionary.
        schemas (dict): Schema Dictionary.
        firebase_app (App) : Firebase App Instance.

    Returns:
        Blueprint: Blueprint for the Adaptative Event Class.
    """
    blueprint = Blueprint(
        name="/adaptative_event", import_name=__name__, url_prefix="/adaptative_event"
    )
    create_one_adaptative_event_factory(
        db,
        models,
        schemas,
        blueprint,
        expected_role="teacher",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    delete_one_adaptative_event_controller_factory(
        db,
        models["AdaptativeEvent"],
        schemas["AdaptativeEvent_CompleteSchema"],
        blueprint,
        expected_role="teacher",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    get_all_adaptative_events_by_adaptative_object_controller_factory(
        models,
        schemas,
        blueprint,
        expected_role="teacher",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    switch_adaptative_event_controller_factory(
        db,
        models["AdaptativeEvent"],
        schemas["AdaptativeEvent_CompleteSchema"],
        blueprint,
        expected_role="teacher",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    return blueprint
