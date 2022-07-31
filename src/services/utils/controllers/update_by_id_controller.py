# -*- coding: utf-8 -*-
"""Module containing the Generic Controller for Updating Models via their ID.

Returns:
    function: Update Function for the Specific Model & Schema.
"""
from firebase_admin import App
from flask import Blueprint, request
from flask_marshmallow.schema import Schema
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model
from src.services.utils.middleware.auth_middleware import auth_middleware


def update_by_id_controller_factory(
    db: SQLAlchemy,
    model: Model,
    schema: Schema,
    blueprint: Blueprint,
    expected_role: str = None,
    firebase_app: App = None,
    user_model: Model = None,
):
    """Creates a Controller Function to Update an Element based on its ID.

    Args:
        db (SQLAlchemy): Database Object containing the Model.
        model (Model): Model instance.
        schema (Schema): Schema to Return on success.
        blueprint (Blueprint): Blueprint to contain the new route.
        expected_role (str): Expected Role String. Either teacher or student.
        firebase_app (App): Firebase App Instance.
        user_model (Model): User Model Instance.

    Returns:
        function: Update Function for the Specific Model & Schema.
    """

    @blueprint.route("/<string:uuid>", methods=["PUT", "PATCH"])
    @auth_middleware(
        expected_role=expected_role, firebase_app=firebase_app, user_model=user_model
    )
    def update_by_id_controller(uuid: str, current_user=None):
        """Update Function for Model based on its ID.

        Args:
            uuid (string): Unique ID for the Model Instance.

        Returns:
            dict: Response dictionary containing the updated model instance.
        """
        data = model().query.get(uuid)
        if not data:
            return {
                "success": False,
                "message": "Model Data Not Found",
                "data": schema().dump(obj=data, many=False),
            }, 200
        new_data = request.json
        for key in new_data:
            setattr(data, key, new_data[key])
        db.session.commit()
        return {
            "success": True,
            "message": "Model Data Updated Successfully",
            "data": schema().dump(obj=data, many=False),
        }, 200

    return update_by_id_controller
