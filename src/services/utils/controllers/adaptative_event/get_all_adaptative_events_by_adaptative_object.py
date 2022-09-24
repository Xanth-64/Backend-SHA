# -*- coding: utf-8 -*-
"""Module containing the Controller for Reading All Instances of Adaptative Events (With Pagination) for an Adaptative Object

Returns:
    function: Read Function for the Specific Adaptative Events & Schema
"""
from typing import Dict
from firebase_admin import App
from flask import Blueprint, request
from flask_marshmallow.schema import Schema
from flask_sqlalchemy.model import Model
from src.services.utils.middleware.auth_middleware import auth_middleware


def get_all_adaptative_events_by_adaptative_object_controller_factory(
    models: Dict[str, Model],
    schemas: Dict[str, Schema],
    blueprint: Blueprint,
    expected_role: str = None,
    firebase_app: App = None,
    user_model: Model = None,
):
    """Creates a Controller for Reading All Instances of Adaptative Events by Adaptative Object (With Pagination)

    Args:
        models Dict(str,Model): Dictionary of Models instance.
        schemas Dict(str,Schema): Dictionary of Schemas to Return on success.
        blueprint (Blueprint): Blueprint to contain the new route.
        expected_role (str): Expected Role String. Either teacher or student.
        firebase_app (App): Firebase App Instance.
        user_model (Model): User Model Instance.


    Returns:
        function: Read All Function for Adaptative Event Model & Schema.
    """

    @blueprint.route("/by_adaptative_object/with_pagination", methods=["GET"])
    @auth_middleware(
        expected_role=expected_role, firebase_app=firebase_app, user_model=user_model
    )
    def get_all_adaptative_events_by_adaptative_object_controller(
        current_user=None,
    ):
        args = request.args
        if args.get("sort_key"):
            data = (
                models["AdaptativeEvent"]()
                .query.filter_by(adaptative_object_id=args.get("adaptative_object_id"))
                .order_by(args.get("sort_key"))
            )
        else:
            data = models["AdaptativeEvent"]().query.filter_by(
                adaptative_object_id=args.get("adaptative_object_id")
            )
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
                "items": schemas["AdaptativeEvent_CompleteSchema"]().dump(
                    obj=data.items if args.get("page") else data, many=True
                ),
            },
            "success": True,
        }, 200

    return get_all_adaptative_events_by_adaptative_object_controller
