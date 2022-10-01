# -*- coding: utf-8 -*-
from typing import Dict

from firebase_admin import App
from flask import Blueprint
from flask_marshmallow.schema import Schema
from flask_sqlalchemy.model import Model

from src.services.utils.middleware.auth_middleware import auth_middleware


def get_all_starting_tests_controller_factory(
    models: Dict[str, Model],
    schemas: Dict[str, Schema],
    blueprint: Blueprint,
    expected_role: str = None,
    firebase_app: App = None,
    user_model: Model = None,
):
    @blueprint.route("/starting_tests", methods=["GET"])
    @auth_middleware(
        expected_role=expected_role, firebase_app=firebase_app, user_model=user_model
    )
    def get_all_starting_tests(current_user=None):
        """Controller function to Get all instances of Starting Practice Tests.

        Returns:
            dict: Dictionary Containing the Listing of all Starting Practice Tests.
        """
        starting_tests = (
            models["Page"]
            .query.join(models["PracticeTest"])
            .filter(models["PracticeTest"].show_on_init == True)
            .join(models["Template"])
            .join(models["Topic"])
            .order_by(models["Topic"].relative_position)
            .all()
        )
        return {
            "success": True,
            "message": "Starting Tests Retrieved Successfully",
            "data": {
                "items": schemas["Page_PageInheritanceSchema"]().dump(
                    starting_tests, many=True
                )
            },
        }, 200
