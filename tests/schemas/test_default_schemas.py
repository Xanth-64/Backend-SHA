# -*- coding: utf-8 -*-
"""Test case suite for the Default Schemas."""

from typing import Dict

from flask_marshmallow.schema import Schema
from flask_sqlalchemy.model import Model
from marshmallow_sqlalchemy.schema import SQLAlchemyAutoSchema


class TestDefaultSchemas:
    """Test suite for the Default Schemas"""

    def test_schemas_exist(
        self, models: Dict[str, Model], schemas: Dict[str, SQLAlchemyAutoSchema]
    ):
        """Test that all of the Schemas are created"""
        for model_name in models.keys():
            assert f"{model_name}_DefaultSchema" in schemas

    def test_schemas_are_correct_type(self, schemas: Dict[str, SQLAlchemyAutoSchema]):
        """Test that all of the Schemas are of the correct type"""
        for schema_name, schema in schemas.items():
            assert isinstance(schema(), Schema)

    def test_schemas_have_correct_fields(
        self, models: Dict[str, Model], schemas: Dict[str, SQLAlchemyAutoSchema]
    ):
        """Test that all of the Schemas have the correct fields"""
        for model_name, model in models.items():
            schema = schemas[f"{model_name}_DefaultSchema"]
            schema_fields = schema().fields
            assert set(schema_fields.keys()) == set(model.__table__.columns.keys())
