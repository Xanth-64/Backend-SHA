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


def get_pages_for_template_factory(
    model: Model,
    schema: Schema,
    blueprint: Blueprint,
    expected_role: str = None,
    firebase_app: App = None,
    user_model: Model = None,
):
    """Creates a Controller for Reading All Instances of Page Model (With Optional Pagination)

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
    def get_templates_for_topic(current_user=None):
        args = request.args
        data = model().query.filter_by(template_id=args.get("template_id"))
        if args.get("sort_key"):
            data = data.order_by(args.get("sort_key"))
        if args.get("page") and args.get("page_size"):
            data = data.paginate(
                page=int(args.get("page")), per_page=int(args.get("page_size"))
            )
        else:
            data = data.all()
        return {
            "message": "Model Bulk Data Found Successfully",
            "data": {
                "total_pages": data.pages if args.get("page") else 1,
                "total_items": data.total if args.get("page") else len(data),
                "current_page": data.page if args.get("page") else 1,
                "page_size": data.per_page if args.get("page") else len(data),
                "items": schema().dump(
                    obj=data.items if args.get("page") else data, many=True
                ),
            },
            "success": True,
        }, 200

    return get_templates_for_topic
