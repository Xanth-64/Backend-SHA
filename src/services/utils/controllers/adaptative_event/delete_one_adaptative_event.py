# -*- coding: utf-8 -*-
"""Module containing the Controller for Deleting Adaptative Events via their ID

Returns:
    function: Delete Function for the Adaptative Events
"""
from firebase_admin import App
from flask import Blueprint
from flask_marshmallow.schema import Schema
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model
from src.services.utils.middleware.auth_middleware import auth_middleware


def delete_one_adaptative_event_controller_factory(
    db: SQLAlchemy,
    model: Model,
    schema: Schema,
    blueprint: Blueprint,
    expected_role: str = None,
    firebase_app: App = None,
    user_model: Model = None,
):
    """Creates a Controller Function to Delete an Adaptative Event based on its ID

    Args:
        db (SQLAlchemy): Database Object containing the Model.
        model (Model): Model instance.
        schema (Schema): Schema to Return on success.
        blueprint (Blueprint): Blueprint to contain the new route.
        expected_role (str): Expected Role String. Either teacher or student.
        firebase_app (App): Firebase App Instance.
        user_model (Model): User Model Instance.

    Returns:
        function: Delete Function for the Adaptative Event.
    """

    @blueprint.route("/<string:uuid>", methods=["DELETE"])
    @auth_middleware(
        expected_role=expected_role, firebase_app=firebase_app, user_model=user_model
    )
    def delete_adaptative_event_by_id(uuid: str, current_user=None):
        """Delete Function for Adaptative Event based on its ID.

        Args:
            uuid (str): Unique ID for the Model Instance.

        Returns:
            dict: Response dictionary containing the removed model instance.
        """
        data = model().query.get(uuid)
        if not data:
            return {
                "success": False,
                "message": "Model Data Not Found",
                "data": schema().dump(obj=data, many=False),
            }, 200
        # Reduce by 1 the relative_position of the following elements
        for element in (
            model()
            .query.filter(
                model.adaptative_object_id == data.adaptative_object_id,
                model.relative_position > data.relative_position,
            )
            .all()
        ):
            element.relative_position -= 1
        db.session.delete(data)
        db.session.commit()
        return {
            "success": True,
            "message": "Model Data Deleted Successfully",
            "data": schema().dump(obj=data, many=False),
        }, 200

    return delete_adaptative_event_by_id
