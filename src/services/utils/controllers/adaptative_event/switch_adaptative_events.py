# -*- coding: utf-8 -*-
from firebase_admin import App
from flask import Blueprint, request
from flask_marshmallow.schema import Schema
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model
from sqlalchemy.exc import IntegrityError
from src.services.utils.middleware.auth_middleware import auth_middleware


def switch_adaptative_event_controller_factory(
    db: SQLAlchemy,
    adaptative_event_model: Model,
    adaptative_event_schema: Schema,
    blueprint: Blueprint,
    expected_role: str = None,
    firebase_app: App = None,
    user_model: Model = None,
):
    @blueprint.route("/switch", methods=["PUT", "PATCH"])
    @auth_middleware(
        expected_role=expected_role, firebase_app=firebase_app, user_model=user_model
    )
    def swith_adaptative_event_position(current_user=None):
        """Controller function to Change the Position of a Adaptative Event.

        Returns:
            dict: Dictionary Containing the adaptative_event that Changed Position.
        """
        req_data = request.get_json()
        uuid = req_data.get("uuid")
        adaptative_event = adaptative_event_model.query.get(uuid)
        if not adaptative_event:
            return {
                "success": False,
                "data": {
                    "error": "NOT_FOUND",
                    "message": "Adaptative Event Not Found",
                },
                "message": "Adaptative Event Not Found",
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
            adaptative_event_exchange = adaptative_event_model.query.filter_by(
                relative_position=adaptative_event.relative_position - 1,
                adaptative_object_id=adaptative_event.adaptative_object_id,
            ).first()
            if not adaptative_event_exchange:
                return {
                    "success": False,
                    "data": {
                        "error": "NO_SWITCH_POSSIBLE",
                        "message": "Adaptative Event Not Found",
                    },
                    "message": "Adaptative Event Not Found",
                }, 400
            adaptative_event.relative_position = adaptative_event.relative_position - 1
            adaptative_event_exchange.relative_position = (
                adaptative_event_exchange.relative_position + 1
            )

        elif move_direction == "down":
            adaptative_event_exchange = adaptative_event_model.query.filter_by(
                relative_position=adaptative_event.relative_position + 1,
                adaptative_object_id=adaptative_event.adaptative_object_id,
            ).first()
            if not adaptative_event_exchange:
                return {
                    "success": False,
                    "data": {
                        "error": "NO_SWITCH_POSSIBLE",
                        "message": "adaptative_event Not Found",
                    },
                    "message": "adaptative_event Not Found",
                }, 400
            adaptative_event.relative_position = adaptative_event.relative_position + 1
            adaptative_event_exchange.relative_position = (
                adaptative_event_exchange.relative_position - 1
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
            "data": adaptative_event_schema().dump(obj=adaptative_event, many=False),
        }, 200
