# -*- coding: utf-8 -*-
"""Module containing the Controller for Deleting Adaptation Conditions via their ID

Returns:
    function: Delete Function for the Adaptation Conditions
"""
from typing import Dict
from firebase_admin import App
from flask import Blueprint
from flask_marshmallow.schema import Schema
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model
from src.services.utils.middleware.auth_middleware import auth_middleware


def delete_adaptation_condition_by_id_controller_factory(
    db: SQLAlchemy,
    models: Dict[str, Model],
    schemas: Dict[str, Schema],
    blueprint: Blueprint,
    expected_role: str = None,
    firebase_app: App = None,
    user_model: Model = None,
):
    """Creates a Controller Function to Delete an Adaptation Condition based on its ID

    Args:
        db (SQLAlchemy): Database Object containing the Model.
        models (Dict[str,Model]): Dictionary of Database Models.
        schemas (Dict[str,Schema]): Dictionary of API Schemas.
        blueprint (Blueprint): Blueprint to contain the new route.
        expected_role (str): Expected Role String. Either teacher or student.
        firebase_app (App): Firebase App Instance.
        user_model (Model): User Model Instance.

    Returns:
        function: Delete Function for Adaptation Conditions.
    """

    @blueprint.route("/<string:uuid>", methods=["DELETE"])
    @auth_middleware(
        expected_role=expected_role, firebase_app=firebase_app, user_model=user_model
    )
    def delete_adaptation_condition_by_id_controller(uuid: str, current_user=None):
        """Delete Function for Adaptation Condition on its ID.

        Args:
            uuid (str): Unique ID for the Adaptation Condition Instance.

        Returns:
            dict: Response dictionary containing the removed Adaptation Condition instance.
        """
        data = models["AdaptationCondition"]().query.get(uuid)
        if not data:
            return {
                "success": False,
                "message": "Model Data Not Found",
                "data": schemas["AdaptationCondition_DefaultSchema"]().dump(
                    obj=data, many=False
                ),
            }, 200
        if len(data.adaptative_event.adaptation_conditions.all()) == 1:
            return {
                "success": False,
                "message": "Cannot Delete the Only Adaptation Condition",
                "data": {
                    "error": "CANNOT_DELETE_ONLY_ADAPTATION_CONDITION",
                    "message": "Cannot Delete the Only Adaptation Condition",
                },
            }, 400
        db.session.delete(data)
        db.session.commit()
        return {
            "success": True,
            "message": "Model Data Deleted Successfully",
            "data": schemas["AdaptationCondition_DefaultSchema"]().dump(
                obj=data, many=False
            ),
        }, 200

    return delete_adaptation_condition_by_id_controller
