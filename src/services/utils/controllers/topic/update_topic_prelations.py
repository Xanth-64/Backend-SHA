# -*- coding: utf-8 -*-
from firebase_admin import App
from flask import Blueprint, request
from flask_marshmallow.schema import Schema
from flask_sqlalchemy import Model, SQLAlchemy
from sqlalchemy import Table
from src.services.utils.middleware.auth_middleware import auth_middleware


def update_topic_prelations_controller_factory(
    db: SQLAlchemy,
    model: Table,
    topic_precedence_schema: Schema,
    blueprint: Blueprint,
    expected_role: str = None,
    firebase_app: App = None,
    user_model: Model = None,
):
    @blueprint.route("/prelations", methods=["PATCH", "PUT"])
    @auth_middleware(
        expected_role=expected_role, firebase_app=firebase_app, user_model=user_model
    )
    def update_topic_prelations(current_user=None):
        """Controller to Update Topic Prelations (Based on successor and predecessor).

        Returns:
            dict: Dictionary Containing the Required Topic Prelations.
        """
        req_data = request.get_json()
        db.engine.execute(
            model.update(
                whereclause=(
                    model.c.successor == req_data.get("successor")
                    and model.c.predecessor == req_data.get("predecessor")
                ),
                values={"knowledge_weight": req_data.get("knowledge_weight")},
            )
        )
        data = db.engine.execute(
            model.select(
                whereclause=(
                    model.c.successor == req_data.get("successor")
                    and model.c.predecessor == req_data.get("predecessor")
                )
            )
        ).first()
        if not data:
            return {
                "success": False,
                "message": "Model Data Not Found",
                "data": {
                    "error": "MISSING_ENTITIES",
                    "message": "Model Data Not Found",
                },
            }, 400
        return {
            "success": True,
            "message": "Model Data Updated Successfully",
            "data": topic_precedence_schema().dump(obj=data, many=False),
        }, 200
