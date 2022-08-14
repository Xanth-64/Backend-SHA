# -*- coding: utf-8 -*-
"""Module containing the functions for User Authentication


Returns:
    function: Function for instantiating the User Auth Blueprint.
"""
from os import environ

import requests
from firebase_admin import App
from firebase_admin._auth_utils import EmailAlreadyExistsError
from firebase_admin.auth import create_user
from flask import Blueprint, request
from flask_sqlalchemy import SQLAlchemy
from marshmallow import EXCLUDE
from sqlalchemy.exc import IntegrityError
from src.services.utils.middleware.auth_middleware import auth_middleware
from src.services.utils.controllers.auth.update_current_user import (
    update_current_user_controller_factory,
)


def create_auth_blueprint(
    db: SQLAlchemy, models: dict, schemas: dict, firebase_app: App
) -> Blueprint:
    """Function to Create the User Auth Blueprint

    Args:
        db (SQLAlchemy): Database Singleton Object Containing all of the Connection Params.
        models (dict): Model Dictionary.
        schemas (dict): Schema Dictionary.
        firebase_app (App) : Firebase App Instance.
    Returns:
        Blueprint: Blueprint for the Authentication.
    """
    blueprint = Blueprint(name="/auth", import_name=__name__, url_prefix="/auth")

    @blueprint.route("/signup", methods=["POST"])
    def create_user_account():
        try:
            req_data = request.get_json()
            schema_data = schemas["User_DefaultSchema"]().load(
                req_data, unknown=EXCLUDE
            )
            new_instance = models["User"](**schema_data)
            new_instance.role.append(
                models["Role"](
                    role_name=req_data.get("role")
                    if req_data.get("role")
                    else "student"
                )
            )
            try:
                db.session.add(new_instance)
                db.session.commit()
            except IntegrityError:
                return {
                    "success": False,
                    "data": {
                        "error": "EMAIL_ALREADY_EXISTS",
                        "message": "User Account Already Exists",
                    },
                    "message": "User Account Already Exists",
                }, 403
            create_user(
                uid=str(new_instance.id),
                email=req_data["email"],
                password=req_data["password"],
                app=firebase_app,
            )
            token = requests.post(
                f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={environ.get('GOOGLE_API_KEY')}",
                data={
                    "email": req_data["email"],
                    "password": req_data["password"],
                    "returnSecureToken": True,
                },
            )
            return {
                "success": True,
                "data": token.json(),
                "message": "User Account Created Successfully",
            }, 200
        except EmailAlreadyExistsError:
            return {
                "success": False,
                "data": {
                    "error": "EMAIL_ALREADY_EXISTS",
                    "message": "User Account Already Exists",
                },
                "message": "User Account Already Exists",
            }, 403

    @blueprint.route("/login", methods=["POST"])
    def login_with_email_password():
        req_data = request.get_json()
        token = requests.post(
            f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={environ.get('GOOGLE_API_KEY')}",
            data={
                "email": req_data.get("email"),
                "password": req_data.get("password"),
                "returnSecureToken": True,
            },
        )
        if token.status_code == 400:
            if (
                token.json().get("error").get("message") == "INVALID_PASSWORD"
                or token.json().get("error").get("message") == "EMAIL_NOT_FOUND"
            ):
                return {
                    "success": False,
                    "data": {
                        "error": "EMAIL_PASSWORD_WRONG",
                        "message": "Wrong Email or Password",
                    },
                    "message": "Wrong Email or Password",
                }, 403
        return {
            "success": True,
            "data": token.json(),
            "message": "User Account Retrieved Successfully",
        }, 200

    @blueprint.route("/change_password", methods=["PATCH", "PUT"])
    @auth_middleware(
        expected_role="student", firebase_app=firebase_app, user_model=models["User"]
    )
    def change_password(current_user=None):
        req_data = request.get_json()
        token = requests.post(
            f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={environ.get('GOOGLE_API_KEY')}",
            data={
                "email": current_user.email,
                "password": req_data.get("old_password"),
                "returnSecureToken": True,
            },
        )
        if token.status_code == 400:
            return {
                "success": False,
                "data": {
                    "error": "INVALID_PASSWORD",
                    "message": "Wrong Password",
                },
                "message": "Wrong Password",
            }
        token = requests.post(
            f"https://identitytoolkit.googleapis.com/v1/accounts:update?key={environ.get('GOOGLE_API_KEY')}",
            data={
                "idToken": token.json().get("idToken"),
                "password": req_data.get("new_password"),
                "returnSecureToken": True,
            },
        )
        return {
            "success": True,
            "data": token.json(),
            "message": "Password Changed Successfully",
        }, 200

    update_current_user_controller_factory(
        db,
        models["User"],
        schemas["User_DefaultSchema"],
        blueprint,
        "student",
        firebase_app,
        models["User"],
    )
    return blueprint
