# -*- coding: utf-8 -*-
"""Module containing the Generic Controller for Creating one Instance of a Model.

Returns:
    function: Generic Controller to Create an Instance of a Model.
"""
from firebase_admin import App
from flask import Blueprint, request
from flask_marshmallow.schema import Schema
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model
from sqlalchemy.exc import IntegrityError
from src.services.utils.middleware.auth_middleware import auth_middleware


def create_one_controller_factory(
    db: SQLAlchemy,
    model: Model,
    schema: Schema,
    blueprint: Blueprint,
    expected_role: str = None,
    firebase_app: App = None,
    user_model: Model = None,
):
    """Creates a Controller Function to Create an Instance of a given Model.

    Args:
        db (SQLAlchemy): Database Object containing the Model.
        model (Model): Model instance.
        schema (Schema): Schema to Return on success.
        blueprint (Blueprint): Blueprint to contain the new route.
        expected_role (str): Expected Role String. Either teacher or student.
        firebase_app (App): Firebase App Instance.
        user_model (Model): User Model Instance.

    Returns:
        function: Generic Controller to Create an Instance of a Model.
    """

    @blueprint.route("/", methods=["POST"])
    @auth_middleware(
        expected_role=expected_role, firebase_app=firebase_app, user_model=user_model
    )
    def create_one_controller(current_user=None):
        """Controller function to Create an Instance of a given Model.

        Returns:
            dict: Dictionary Containing the Newly Created Model Instance.
        """
        req_data = request.get_json()
        new_instance = model(**req_data)
        try:
            db.session.add(new_instance)
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
            "message": "Model Data Created Successfully",
            "data": schema().dump(obj=new_instance, many=False),
        }, 200

    return create_one_controller
