# -*- coding: utf-8 -*-
from typing import Dict
from firebase_admin import App
from flask import Blueprint, request
from flask_marshmallow.schema import Schema
from flask_sqlalchemy.model import Model
from src.services.utils.middleware.auth_middleware import auth_middleware


def get_by_test_id_controller_factory(
    models: Dict[str, Model],
    schemas: Dict[str, Schema],
    blueprint: Blueprint,
    expected_role: str = None,
    firebase_app: App = None,
    user_model: Model = None,
):
    @blueprint.route("/", methods=["GET"])
    @auth_middleware(
        expected_role=expected_role, firebase_app=firebase_app, user_model=user_model
    )
    def get_by_test_id(current_user=None):
        """Controller function to Create an Instance of a given Model.

        Returns:
            dict: Dictionary Containing the Newly Created Model Instance.
        """
        args = request.args
        if not args.get("practice_test_id"):
            return {
                "message": "Practice Test ID is required.",
                "success": False,
                "data": {
                    "error": "TEST_NOT_FOUND",
                    "message": "Practice Test ID is required.",
                },
            }, 400
        test_attempt = (
            models["TestAttempt"]
            .query.filter_by(
                practice_test_id=args.get("practice_test_id"), user_id=current_user.id
            )
            .first()
        )
        return {
            "success": True,
            "message": "Model Data Queried Successfully",
            "data": schemas["TestAttempt_CompleteSchema"]().dump(
                obj=test_attempt, many=False
            ),
        }, 200
