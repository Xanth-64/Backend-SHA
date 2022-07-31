"""Auth Middleware to discrimnitate between student and teacher"""

from functools import wraps

from firebase_admin import App
from firebase_admin.auth import (
    ExpiredIdTokenError,
    InvalidIdTokenError,
    RevokedIdTokenError,
    verify_id_token,
)
from flask import request
from flask_sqlalchemy import Model


def auth_middleware(
    expected_role: str = None, firebase_app: App = None, user_model: Model = None
):
    """Auth Middleware to discriminate between student and teacher

    Args:
        expected_role (str, optional): Expected User Role. Either student or teacher. Defaults to None.
        firebase_app (App, optional): Firebase Application Instance. Defaults to None.
        user_model (dict, optional): Database ORM Model Object Representing the User. Defaults to None.

    Returns:
        function: Decorated Function Object representing the Controller.
    """

    def decorate(controller):
        @wraps(controller)
        def wrapper(*args, **kwargs):
            token = None
            if expected_role is not None:
                token = request.headers.get("Authorization")
                if token is None:
                    return {
                        "success": False,
                        "code": {"name": "NO_AUTH_HEADER"},
                        "message": "Unauthorized",
                    }, 401

                try:
                    token = token.split(" ")[1]
                except IndexError:
                    return {
                        "success": False,
                        "code": {"name": "BAD_AUTH_HEADER"},
                        "message": "Unauthorized",
                    }, 401
                try:
                    decoded_token = verify_id_token(
                        id_token=token, check_revoked=True, app=firebase_app
                    )
                except ValueError:
                    return {
                        "success": False,
                        "code": {"name": "BAD_AUTH_HEADER"},
                        "message": "Unauthorized",
                    }, 401
                except (InvalidIdTokenError, ExpiredIdTokenError, RevokedIdTokenError):
                    return {
                        "success": False,
                        "code": {"name": "INVALID_AUTH_HEADER"},
                        "message": "Unauthorized",
                    }, 401
                uuid = decoded_token.get("user_id")
                if uuid is None:
                    return {
                        "success": False,
                        "code": {"name": "INVALID_AUTH_HEADER"},
                        "message": "Unauthorized",
                    }, 401
                current_user = user_model().query.get(uuid)
                if expected_role == "teacher":
                    if not any(
                        role.role_name == expected_role for role in current_user.role
                    ):
                        return {
                            "success": False,
                            "code": {"name": "INVALID_ROLE"},
                            "message": "Unauthorized",
                        }, 401
                elif expected_role == "student":
                    if not any(
                        role.role_name == expected_role or role.role_name == "teacher"
                        for role in current_user.role
                    ):
                        return {
                            "success": False,
                            "code": {"name": "INVALID_ROLE"},
                            "message": "Unauthorized",
                        }, 401
            return controller(current_user=current_user, *args, **kwargs)

        return wrapper

    return decorate
