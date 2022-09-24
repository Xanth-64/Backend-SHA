# -*- coding: utf-8 -*-
"""Module containing the Generic Controller for Updating a Measurable Interaction via their ID.

Returns:
    function: Update Function for the Specific Model & Schema.
"""
from typing import Dict
from firebase_admin import App
from flask import Blueprint, request
from flask_marshmallow.schema import Schema
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model
from sqlalchemy.exc import IntegrityError
from src.services.utils.middleware.auth_middleware import auth_middleware


def update_measurable_interaction_controller_factory(
    db: SQLAlchemy,
    models: Dict[str, Model],
    schemas: Dict[str, Schema],
    blueprint: Blueprint,
    expected_role: str = None,
    firebase_app: App = None,
    user_model: Model = None,
):
    """Creates a Controller Function to Update a Measurable Interaction based on its ID.

    Args:
        db (SQLAlchemy): Database Object containing the Model.
        models (Dict[str,Model]): Dictionary of Model Instances.
        schemas (Dict[str,Schema]): Dictionary of Schemas to Return on success.
        blueprint (Blueprint): Blueprint to contain the new route.
        expected_role (str): Expected Role String. Either teacher or student.
        firebase_app (App): Firebase App Instance.
        user_model (Model): User Model Instance.

    Returns:
        function: Update Function for the M<.
    """

    @blueprint.route("/<string:uuid>", methods=["PUT", "PATCH"])
    @auth_middleware(
        expected_role=expected_role, firebase_app=firebase_app, user_model=user_model
    )
    def update_measurable_interaction_controller(uuid: str, current_user=None):
        """Update Function for Measurable Interactions based on its ID.

        Args:
            uuid (string): Unique ID for the Measurable Interaction Instance.

        Returns:
            dict: Response dictionary containing the updated model instance.
        """
        data = models["MeasurableInteraction"]().query.get(uuid)
        if not data:
            return {
                "success": False,
                "message": "Model Data Not Found",
                "data": schemas["MeasurableInteraction_DefaultSchema"]().dump(
                    obj=data, many=False
                ),
            }, 400
        if data.interactions_fired.all():
            return {
                "success": False,
                "message": "Cannot Update Measurable Interaction with Interactions Fired",
                "data": {
                    "error": "MEASURABLE_INTERACTION_WITH_INTERACTIONS_FIRED",
                    "message": "Cannot Update Measurable Interaction with Interactions Fired",
                },
            }, 400
        new_data = request.json
        for key in new_data:
            setattr(data, key, new_data[key])
        try:
            db.session.commit()
        except IntegrityError:
            return {
                "success": False,
                "data": {
                    "error": "UNIQUE_VIOLATION",
                    "message": "Database Constraint Violation",
                },
                "message": "Database Integrity Error",
            }, 400

        return {
            "success": True,
            "message": "Model Data Updated Successfully",
            "data": schemas["MeasurableInteraction_DefaultSchema"]().dump(
                obj=data, many=False
            ),
        }, 200

    return update_measurable_interaction_controller
