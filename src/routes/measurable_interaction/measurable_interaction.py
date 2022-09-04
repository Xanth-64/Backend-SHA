# -*- coding: utf-8 -*-
"""Module containing the functions for instantiating the blueprint
for Measurable Interaction Models

Returns:
    function: Function for instantiating the Measurable Interaction Blueprint.
"""
from firebase_admin import App
from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy

from src.services.utils.controllers.generics.create_one_controller import (
    create_one_controller_factory,
)
from src.services.utils.controllers.generics.delete_by_id_controller import (
    delete_by_id_controller_factory,
)

from src.services.utils.controllers.generics.get_all_with_pagination_controller import (
    get_all_with_pagination_controller_factory,
)
from src.services.utils.controllers.measurable_interaction.get_all_measurable_interactions_by_learning_content import (
    get_all_measurable_interactions_by_learning_content_controller_factory,
)
from src.services.utils.controllers.measurable_interaction.get_learning_content_categorized_interactions import (
    get_learning_content_categorized_interactions_controller_factory,
)
from src.services.utils.controllers.measurable_interaction.update_measurable_interaction import (
    update_measurable_interaction_controller_factory,
)


def create_measurable_interaction_blueprint(
    db: SQLAlchemy, models: dict, schemas: dict, firebase_app: App
) -> Blueprint:
    """Function to Create the Measurable Interaction Blueprint

    Args:
        db (SQLAlchemy): Database Singleton Object Containing all of the Connection Params.
        models (dict): Model Dictionary.
        schemas (dict): Schema Dictionary.
        firebase_app (App) : Firebase App Instance.
    Returns:
        Blueprint: Blueprint for the Measurable Interaction Class.
    """
    blueprint = Blueprint(
        name="/measurable_interaction",
        import_name=__name__,
        url_prefix="/measurable_interaction",
    )

    create_one_controller_factory(
        db,
        models["MeasurableInteraction"],
        schemas["MeasurableInteraction_DefaultSchema"],
        blueprint,
        expected_role="teacher",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    delete_by_id_controller_factory(
        db,
        models["MeasurableInteraction"],
        schemas["MeasurableInteraction_DefaultSchema"],
        blueprint,
        expected_role="teacher",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    get_all_with_pagination_controller_factory(
        models["MeasurableInteraction"],
        schemas["MeasurableInteraction_DefaultSchema"],
        blueprint,
        expected_role="teacher",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    get_all_measurable_interactions_by_learning_content_controller_factory(
        models,
        schemas,
        blueprint,
        expected_role="student",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    get_learning_content_categorized_interactions_controller_factory(
        models,
        schemas,
        blueprint,
        expected_role="student",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    update_measurable_interaction_controller_factory(
        db,
        models,
        schemas,
        blueprint,
        expected_role="teacher",
        firebase_app=firebase_app,
        user_model=models["User"],
    )
    return blueprint
