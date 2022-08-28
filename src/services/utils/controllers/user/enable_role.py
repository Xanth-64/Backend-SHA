# -*- coding: utf-8 -*-
"""Module containing the Controller for Enabling or Disabling User Roles.

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


def enable_role_controller_factory(
    db: SQLAlchemy,
    models: Dict[str, Model],
    schema: Schema,
    blueprint: Blueprint,
    expected_role: str = None,
    firebase_app: App = None,
    user_model: Model = None,
):
    """Creates a Controller Function to Update Users Role.

    Args:
        db (SQLAlchemy): Database Object containing the Model.
        model (Model): Model instance.
        schema (Schema): Schema to Return on success.
        blueprint (Blueprint): Blueprint to contain the new route.
        expected_role (str): Expected Role String. Either teacher or student.
        firebase_app (App): Firebase App Instance.
        user_model (Model): User Model Instance.

    Returns:
        function: Update Function.
    """

    @blueprint.route("/enable_role", methods=["POST"])
    @auth_middleware(
        expected_role=expected_role, firebase_app=firebase_app, user_model=user_model
    )
    def update_role_controller(current_user=None):
        """Update Function for Model based on its ID.

        Args:
            uuid (string): Unique ID for the Model Instance.

        Returns:
            dict: Response dictionary containing the updated model instance.
        """
        data = models["User"]().query.get(request.json.get("user_id"))
        if not data:
            return {
                "success": False,
                "message": "User Not Found",
                "data": {"message": "User Not Found", "error": "USER_NOT_FOUND"},
            }, 200
        role = (
            models["Role"]()
            .query.filter_by(user_id=data.id, role_name=request.json.get("role_name"))
            .first()
        )
        if not role:
            new_role = models["Role"](
                role_name=request.json.get("role_name"),
                is_enabled=request.json.get("role_value"),
            )
            data.role.append(new_role)
        else:
            role.is_enabled = request.json.get("role_value")
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
            "data": schema().dump(obj=data, many=False),
        }, 200

    return update_role_controller
