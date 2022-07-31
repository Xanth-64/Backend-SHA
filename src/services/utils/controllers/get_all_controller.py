# -*- coding: utf-8 -*-
"""Module containing the Generic Controller for Reading All Instances of Model

Returns:
    function: Read Function for the Specific Model & Schema
"""
from firebase_admin import App
from flask import Blueprint
from flask_marshmallow.schema import Schema
from flask_sqlalchemy.model import Model
from src.services.utils.middleware.auth_middleware import auth_middleware


def get_all_controller_factory(
    model: Model,
    schema: Schema,
    blueprint: Blueprint,
    expected_role: str = None,
    firebase_app: App = None,
    user_model: Model = None,
):
    """Creates a Controller for Reading All Instances of Model

    Args:
        model (Model): Model instance.
        schema (Schema): Schema to Return on success.
        blueprint (Blueprint): Blueprint to contain the new route.
        expected_role (str): Expected Role String. Either teacher or student.
        firebase_app (App): Firebase App Instance.
        user_model (Model): User Model Instance.


    Returns:
        function: Read All Function for the Specific Model & Schema.
    """

    @blueprint.route("/", methods=["GET"])
    @auth_middleware(
        expected_role=expected_role, firebase_app=firebase_app, user_model=user_model
    )
    def get_all_controller(current_user=None):
        data = model().query.all()
        return {
            "message": "Model Bulk Data Found Successfully",
            "data": schema().dump(obj=data, many=True),
            "success": True,
        }, 200

    return get_all_controller
