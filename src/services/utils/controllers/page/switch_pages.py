# -*- coding: utf-8 -*-
from firebase_admin import App
from flask import Blueprint, request
from flask_marshmallow.schema import Schema
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model
from sqlalchemy.exc import IntegrityError
from src.services.utils.middleware.auth_middleware import auth_middleware


def switch_page_controller_factory(
    db: SQLAlchemy,
    page_model: Model,
    page_schema: Schema,
    blueprint: Blueprint,
    expected_role: str = None,
    firebase_app: App = None,
    user_model: Model = None,
):
    @blueprint.route("/switch", methods=["PUT", "PATCH"])
    @auth_middleware(
        expected_role=expected_role, firebase_app=firebase_app, user_model=user_model
    )
    def swith_page_position(current_user=None):
        """Controller function to Change the Position of a Page.

        Returns:
            dict: Dictionary Containing the Page that Changed Position.
        """
        req_data = request.get_json()
        uuid = req_data.get("uuid")
        page = page_model.query.get(uuid)
        if not page:
            return {
                "success": False,
                "data": {
                    "error": "NOT_FOUND",
                    "message": "Page Not Found",
                },
                "message": "Page Not Found",
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
            page_exchange = page_model.query.filter_by(
                relative_position=page.relative_position - 1,
                template_id=page.template_id,
            ).first()
            if not page_exchange:
                return {
                    "success": False,
                    "data": {
                        "error": "NO_SWITCH_POSSIBLE",
                        "message": "Template Not Found",
                    },
                    "message": "Template Not Found",
                }, 400
            page.relative_position = page.relative_position - 1
            page_exchange.relative_position = page_exchange.relative_position + 1

        elif move_direction == "down":
            page_exchange = page_model.query.filter_by(
                relative_position=page.relative_position + 1,
                template_id=page.topic_id,
            ).first()
            if not page_exchange:
                return {
                    "success": False,
                    "data": {
                        "error": "NO_SWITCH_POSSIBLE",
                        "message": "Page Not Found",
                    },
                    "message": "Page Not Found",
                }, 400
            page.relative_position = page.relative_position + 1
            page_exchange.relative_position = page_exchange.relative_position - 1
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
            "data": page_schema().dump(obj=page, many=False),
        }, 200
