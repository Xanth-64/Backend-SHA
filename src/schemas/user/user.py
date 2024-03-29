# -*- coding: utf-8 -*-
from typing import Dict
from flask_marshmallow import Marshmallow
from flask_marshmallow.schema import Schema
from flask_sqlalchemy.model import Model


def create_current_user_schema(
    ma: Marshmallow,
    schemas: Dict[str, Schema],
    db_model: Model,
) -> Schema:
    """Helper Function that Creates a Default Schema for a given Model

    Args:
        ma (Marshmallow): Marshmallow Object for Model Schemas
        db_model (Model) : User Model
    Returns:
        Schema: Current User Schema
    """

    class CurrentUserSchema(ma.SQLAlchemySchema):
        """Current User Schema"""

        class Meta:
            """Metadata for the Class"""

            model = db_model

        id = ma.auto_field()
        created_at = ma.auto_field()
        email = ma.auto_field()
        first_name = ma.auto_field()
        last_name = ma.auto_field()
        image_url = ma.auto_field()
        vark_completed = ma.auto_field()
        learning_style = ma.Nested(schemas["LearningStyle_DefaultSchema"])

    return CurrentUserSchema


def create_user_and_role_schema(
    ma: Marshmallow, schemas: Dict[str, Schema], models: Dict[str, Model]
) -> Schema:
    class UserAndRoleSchema(ma.SQLAlchemySchema):
        class Meta:
            model = models["User"]

        id = ma.auto_field()
        created_at = ma.auto_field()
        email = ma.auto_field()
        first_name = ma.auto_field()
        last_name = ma.auto_field()
        image_url = ma.auto_field()
        vark_completed = ma.auto_field()
        role = ma.Nested(schemas["Role_DefaultSchema"], many=True)

    return UserAndRoleSchema
