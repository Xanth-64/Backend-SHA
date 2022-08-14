# -*- coding: utf-8 -*-
from firebase_admin import App
from flask import Blueprint
from flask_marshmallow.schema import Schema
from flask_sqlalchemy import Model, SQLAlchemy
from sqlalchemy import Table
from src.services.utils.middleware.auth_middleware import auth_middleware


def get_all_topic_prelations_controller_factory(
    db: SQLAlchemy,
    model: Table,
    topic_precedence_schema: Schema,
    blueprint: Blueprint,
    expected_role: str = None,
    firebase_app: App = None,
    user_model: Model = None,
):
    @blueprint.route("/prelations", methods=["GET"])
    @auth_middleware(
        expected_role=expected_role, firebase_app=firebase_app, user_model=user_model
    )
    def get_all_topic_prelations(current_user=None):
        """Controller to Get All Topic Prelations.

        Returns:
            dict: Dictionary Containing the Required Topic Prelations.
        """
        data = db.engine.execute(model.select()).all()
        return {
            "success": True,
            "message": "Model Bulk Data Found Successfully",
            "data": topic_precedence_schema().dump(obj=data, many=True),
        }, 200
