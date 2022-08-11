# -*- coding: utf-8 -*-
"""Module containing the Generic Controller for Reading All Instances of Model (With Pagination)

Returns:
    function: Read Function for the Specific Model & Schema
"""
from firebase_admin import App
from flask import Blueprint, request
from flask_marshmallow.schema import Schema
from flask_sqlalchemy.model import Model
from src.services.utils.middleware.auth_middleware import auth_middleware


def get_all_with_pagination_controller_factory(
    model: Model,
    schema: Schema,
    blueprint: Blueprint,
    expected_role: str = None,
    firebase_app: App = None,
    user_model: Model = None,
):
    """Creates a Controller for Reading All Instances of Model (With Pagination)

    Args:
        model (Model): Model instance.
        schema (Schema): Schema to Return on success.
        blueprint (Blueprint): Blueprint to contain the new route.
        expected_role (str): Expected Role String. Either teacher or student.
        firebase_app (App): Firebase App Instance.
        user_model (Model): User Model Instance.


    Returns:
        function: Read All Function for the Specific Model & Schema.
    """

    @blueprint.route("/with_pagination", methods=["GET"])
    @auth_middleware(
        expected_role=expected_role, firebase_app=firebase_app, user_model=user_model
    )
    def get_all_with_pagination_controller(current_user=None):
        args = request.args
        if args.get("sort_key"):
            data = (
                model()
                .query.order_by(args.get("sort_key"))
                .paginate(
                    page=int(args.get("page")), per_page=int(args.get("page_size"))
                )
            )
        else:
            data = model().query.paginate(
                page=int(args.get("page")), per_page=int(args.get("page_size"))
            )
        return {
            "message": "Model Bulk Data Found Successfully",
            "data": {
                "total_pages": data.pages,
                "total_items": data.total,
                "current_page": data.page,
                "page_size": data.per_page,
                "items": schema().dump(obj=data.items, many=True),
            },
            "success": True,
        }, 200

    return get_all_with_pagination_controller
