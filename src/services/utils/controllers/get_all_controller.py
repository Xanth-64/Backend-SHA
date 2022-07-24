# -*- coding: utf-8 -*-
"""Module containing the Generic Controller for Reading All Instances of Model

Returns:
    function: Read Function for the Specific Model & Schema
"""
from flask import Blueprint
from flask_marshmallow.schema import Schema
from flask_sqlalchemy.model import Model


def get_all_controller_factory(model: Model, schema: Schema, blueprint: Blueprint):
    """_summary_

    Args:
        model (Model): _description_
        schema (Schema): _description_
        blueprint (Blueprint): _description_

    Returns:
        _type_: _description_
    """

    @blueprint.route("/", methods=["GET"])
    def get_all_controller():
        data = model().query.all()
        return {
            "message": "Model Bulk Data Found Successfully",
            "data": schema().dump(obj=data, many=True),
        }, 200

    return get_all_controller
