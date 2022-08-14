# -*- coding: utf-8 -*-
from firebase_admin import App
from flask import Blueprint, request
from flask_marshmallow.schema import Schema
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model
from sqlalchemy.exc import IntegrityError
from src.services.utils.middleware.auth_middleware import auth_middleware


def switch_template_controller_factory(
    db: SQLAlchemy,
    template_model: Model,
    template_schema: Schema,
    blueprint: Blueprint,
    expected_role: str = None,
    firebase_app: App = None,
    user_model: Model = None,
):
    @blueprint.route("/switch", methods=["PUT", "PATCH"])
    @auth_middleware(
        expected_role=expected_role, firebase_app=firebase_app, user_model=user_model
    )
    def swith_template_position(current_user=None):
        """Controller function to Change the Position of a Template.

        Returns:
            dict: Dictionary Containing the Template that Changed Position.
        """
        req_data = request.get_json()
        uuid = req_data.get("uuid")
        template = template_model.query.get(uuid)
        if not template:
            return {
                "success": False,
                "data": {
                    "error": "NOT_FOUND",
                    "message": "Template Not Found",
                },
                "message": "Template Not Found",
            }, 400
        move_direction = req_data.get("move_direction")
        if move_direction not in ("up", "down"):
            return {
                "success": False,
                "data": {
                    "error": "INVALID_MOVE_DIRECTION",
                    "message": "Invalid Move Direction",
                },
                "message": "Invalid Move Direction",
            }, 400
        if move_direction == "up":
            template_exchange = template_model.query.filter_by(
                relative_position=template.relative_position - 1,
                topic_id=template.topic_id,
            ).first()
            if not template_exchange:
                return {
                    "success": False,
                    "data": {
                        "error": "NO_SWITCH_POSSIBLE",
                        "message": "Template Not Found",
                    },
                    "message": "Template Not Found",
                }, 400
            template.relative_position = template.relative_position - 1
            template_exchange.relative_position = (
                template_exchange.relative_position + 1
            )

        elif move_direction == "down":
            template_exchange = template_model.query.filter_by(
                relative_position=template.relative_position + 1,
                topic_id=template.topic_id,
            ).first()
            if not template_exchange:
                return {
                    "success": False,
                    "data": {
                        "error": "NO_SWITCH_POSSIBLE",
                        "message": "template Not Found",
                    },
                    "message": "template Not Found",
                }, 400
            template.relative_position = template.relative_position + 1
            template_exchange.relative_position = (
                template_exchange.relative_position - 1
            )
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
            "data": template_schema().dump(obj=template, many=False),
        }, 200
