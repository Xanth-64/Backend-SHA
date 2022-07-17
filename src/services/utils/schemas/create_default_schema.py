# -*- coding: utf-8 -*-
""""""
from flask_marshmallow import Marshmallow
from flask_marshmallow.schema import Schema
from flask_sqlalchemy.model import Model


def create_default_schema(
    ma: Marshmallow,
    db_model: Model,
    config_include_fk: bool = False,
    config_include_relationships: bool = False,
) -> Schema:
    """Helper Function that Creates a Default Schema for a given Model

    Args:
        ma (Marshmallow): Marshmallow Object for Model Schemas
        model (Model): Database Model Objects
        include_fk (bool): Logical Value Representing if the foreign key should be included
        include_relationships (bool): Logical Value representing if the relationships should be included

    Returns:
        Schema: Default Schema for the Given Model
    """

    class DefaultSchema(ma.SQLAlchemyAutoSchema):
        """Default Schema For Class"""

        class Meta:
            model = db_model
            include_fk = config_include_fk
            include_relationships = config_include_relationships

    return DefaultSchema
