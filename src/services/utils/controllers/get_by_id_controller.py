# -*- coding: utf-8 -*-
"""Module containing the Generic Controller for Reading Models via their ID

Returns:
    function: Read Function for the Specific Model & Schema
"""
from flask import Blueprint
from flask_marshmallow.schema import Schema
from flask_sqlalchemy.model import Model


def get_by_id_controller_factory(model: Model, schema: Schema, blueprint: Blueprint):
    """Creates a Controller Function to Update an Element based  on its ID

    Args:
        model (Model): Model instance.
        schema (Schema): Schema to Return on success.
        blueprint (Blueprint): Blueprint to contain the new route.

    Returns:
        function: Read Function for the Specific Model & Schema.
    """

    @blueprint.route("/<string:uuid>", methods=["GET"])
    def get_by_id_controller(uuid: str):
        """Read Function for Model based on its ID.

        Args:
            uuid (str): Unique ID for the Model Instance.

        Returns:
            dict: Response dictionary containing the updated model instance.
        """
        data = model().query.get(uuid)
        if not data:
            return {
                "success": False,
                "message": "Model Data Not Found",
                "data": schema().dump(obj=data, many=False),
            }, 200
        return {
            "success": True,
            "message": "Model Data Found Successfully",
            "data": schema().dump(obj=data, many=False),
        }, 200

    return get_by_id_controller
