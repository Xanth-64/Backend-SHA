# -*- coding: utf-8 -*-
"""Module containing the Controller for Creating one Instance of an Adaptative Event.

Returns:
    function: Controller to Create an Instance of an Adaptative Event.
"""
from typing import Dict
from firebase_admin import App
from flask import Blueprint, request
from flask_marshmallow.schema import Schema
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from src.services.utils.middleware.auth_middleware import auth_middleware


def create_one_adaptative_event_factory(
    db: SQLAlchemy,
    models: Dict[str, Model],
    schemas: Dict[str, Schema],
    blueprint: Blueprint,
    expected_role: str = None,
    firebase_app: App = None,
    user_model: Model = None,
):
    """Creates a Controller Function to Create an Instance of an Adaptative Event.

    Args:
        db (SQLAlchemy): Database Object containing the Model.
        model (Dict[str,Model]): Dictionary of Model instances.
        schema (Dict[str,Schema]): Dictionary of API Schemas.
        blueprint (Blueprint): Blueprint to contain the new route.
        expected_role (str): Expected Role String. Either teacher or student.
        firebase_app (App): Firebase App Instance.
        user_model (Model): User Model Instance.

    Returns:
        function: Generic Controller to Create an Instance of an Adaptative Event
    """

    @blueprint.route("/", methods=["POST"])
    @auth_middleware(
        expected_role=expected_role, firebase_app=firebase_app, user_model=user_model
    )
    def create_one_adaptative_event(current_user=None):
        """Controller function to Create an Instance of an Adaptative Event.

        Returns:
            dict: Dictionary Containing the Newly Created Adaptative Event Instance.
        """
        req_data = request.get_json()
        relative_position = (
            db.session.query(func.max(models["AdaptativeEvent"].relative_position))
            .filter(
                models["AdaptativeEvent"].adaptative_object_id
                == req_data.get("adaptative_object_id")
            )
            .scalar()
        )
        relative_position = relative_position + 1 if relative_position else 1
        new_instance = models["AdaptativeEvent"](
            triggered_change=req_data.get("triggered_change"),
            condition_aggregator=req_data.get("condition_aggregator"),
            adaptative_object_id=req_data.get("adaptative_object_id"),
            relative_position=relative_position,
        )
        for condition in req_data.get("adaptation_conditions"):
            new_instance.adaptation_conditions.append(
                models["AdaptationCondition"](
                    value_to_compare=condition.get("value_to_compare"),
                    comparation_condition=condition.get("comparation_condition"),
                    variable_to_compare=condition.get("variable_to_compare"),
                )
            )
        try:
            db.session.add(new_instance)
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
            "message": "Model Data Created Successfully",
            "data": schemas["AdaptativeEvent_CompleteSchema"]().dump(
                obj=new_instance, many=False
            ),
        }, 200

    return create_one_adaptative_event
