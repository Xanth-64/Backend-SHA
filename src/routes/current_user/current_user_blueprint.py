# -*- coding: utf-8 -*-
"""Module containing the functions for instantiating the blueprint
for Current User Operations

Returns:
    function: Function for instantiating the User Blueprint.
"""
from firebase_admin import App
from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from src.services.utils.middleware.auth_middleware import auth_middleware


def create_current_user_blueprint(
    db: SQLAlchemy, models: dict, schemas: dict, firebase_app: App
) -> Blueprint:
    """Function to Create the User Blueprint

    Args:
        db (SQLAlchemy): Database Singleton Object Containing all of the Connection Params.
        models (dict): Model Dictionary.
        schemas (dict): Schema Dictionary.
        firebase_app (App) : Firebase App Instance.

    Returns:
        Blueprint: Blueprint for the User Class.
    """
    blueprint = Blueprint(
        name="/current_user", import_name=__name__, url_prefix="/current_user"
    )

    @blueprint.route("/", methods=["GET"])
    @auth_middleware(
        firebase_app=firebase_app, expected_role="student", user_model=models["User"]
    )
    def get_current_user(current_user=None):
        """Function to Get the Current User.

        Args:
            current_user (User): Current User Instance.

        Returns:
            dict: Dictionary Containing the Current User.
        """
        print("Current User", current_user)
        return {
            "success": True,
            "message": "Current User Data Retrieved Successfully",
            "data": {
                "user": schemas["User_DefaultSchema"]().dump(current_user, many=False),
                "role": schemas["Role_DefaultSchema"]().dump(
                    current_user.role, many=True
                ),
            },
        }, 200

    return blueprint
