# -*- coding: utf-8 -*-
"""Module containing the Generic Controller for Creating one Instance of a Model.

Returns:
    function: Generic Controller to Create an Instance of a Model.
"""
from flask import Blueprint, request
from flask_marshmallow.schema import Schema
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model


def create_one_controller_factory(
    db: SQLAlchemy, model: Model, schema: Schema, blueprint: Blueprint
):
    """Creates a Controller Function to Create an Instance of a given Model.

    Args:
        db (SQLAlchemy): Database Object containing the Model.
        model (Model): Model instance.
        schema (Schema): Schema to Return on success.
        blueprint (Blueprint): Blueprint to contain the new route.

    Returns:
        function: Generic Controller to Create an Instance of a Model.
    """

    @blueprint.route("/", methods=["POST"])
    def create_one_controller():
        """Controller function to Create an Instance of a given Model.

        Returns:
            dict: Dictionary Containing the Newly Created Model Instance.
        """
        req_data = request.get_json()
        new_instance = model(**req_data)
        db.session.add(new_instance)
        db.session.commit()
        return {
            "success": True,
            "message": "Model Data Created Successfully",
            "data": schema().dump(obj=new_instance, many=False),
        }, 200

    return create_one_controller
