# -*- coding: utf-8 -*-
"""Module Containing the API Schemas Index

This module groups all of the Schema Definitions  for the Backend.
Aggregating them under the same object.

Typical usage example:"""
from typing import Dict
from flask_marshmallow import Marshmallow
from flask_marshmallow.schema import Schema
from flask_sqlalchemy.model import Model
from .page.page import create_page_inheritance_schema
from src.services.utils.schemas.create_default_schema import create_default_schema
from src.schemas.user.user import create_current_user_schema
from src.schemas.topic.topic import create_topic_precedence_schema


def create_schemas(ma: Marshmallow, models: Dict[str, Model]) -> Dict[str, Schema]:
    """Function to create all of the Schemas in the API"""
    schemas = {}
    # NOTE Creation of the Default Schemas (Containing all of the Properties in the Model)
    for model_name, model in models.items():
        if model_name not in ("TopicPrecedence",):
            schemas[f"{model_name}_DefaultSchema"] = create_default_schema(
                ma=ma,
                db_model=model,
                config_include_fk=False,
                config_include_relationships=False,
            )
    schemas["User_CurrentUserSchema"] = create_current_user_schema(
        ma=ma, db_model=models["User"]
    )
    schemas["Topic_TopicPrecedenceSchema"] = create_topic_precedence_schema()
    schemas["Page_PageInheritanceSchema"] = create_page_inheritance_schema(
        ma, schemas, models
    )
    return schemas
