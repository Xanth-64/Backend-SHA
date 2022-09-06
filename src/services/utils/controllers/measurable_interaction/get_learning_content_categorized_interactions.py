# -*- coding: utf-8 -*-
"""Module containing the Controller for Reading All Measurable Interactions of a Learning Content (Categorized)

Returns:
    function: Read Function for the Specific Model & Schema
"""
from typing import Dict
from firebase_admin import App
from flask import Blueprint, request
from flask_marshmallow.schema import Schema
from flask_sqlalchemy.model import Model
from src.services.utils.middleware.auth_middleware import auth_middleware


def get_learning_content_categorized_interactions_controller_factory(
    models: Dict[str, Model],
    schemas: Dict[str, Schema],
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

    @blueprint.route("/by_learning_content/categorized", methods=["GET"])
    @auth_middleware(
        expected_role=expected_role, firebase_app=firebase_app, user_model=user_model
    )
    def get_learning_content_categorized_interactions_controller(current_user=None):
        args = request.args
        learning_content = (
            models["LearningContent"]()
            .query.filter_by(id=args.get("learning_content_id"))
            .first()
        )
        if not learning_content:
            return {
                "message": "Learning Content not found.",
                "success": False,
                "data": {
                    "error": "LEARNING_CONTENT_NOT_FOUND",
                    "message": "Learning Content not found.",
                },
            }
        # Get all measurable interactions completed by the current user.
        completed_measurable_interactions = (
            learning_content.measurable_interactions.join(
                models["InteractionFired"], aliased=True
            ).filter_by(user_id=current_user.id)
        )

        # Get all measurable interactions not completed by the current user.
        not_completed_measurable_interactions = (
            learning_content.measurable_interactions.except_(
                completed_measurable_interactions
            )
        )
        return {
            "message": "Learning Content Interactions Retrieved Successfully.",
            "success": True,
            "data": {
                "learning_content": schemas["LearningContent_DefaultSchema"]().dump(
                    learning_content
                ),
                "completed_measurable_interactions": schemas[
                    "MeasurableInteraction_DefaultSchema"
                ]().dump(completed_measurable_interactions.all(), many=True),
                "not_completed_measurable_interactions": schemas[
                    "MeasurableInteraction_DefaultSchema"
                ]().dump(not_completed_measurable_interactions.all(), many=True),
            },
        }

    return get_learning_content_categorized_interactions_controller
