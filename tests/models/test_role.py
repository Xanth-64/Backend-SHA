# -*- coding: utf-8 -*-
"""Test case suite for the Role model."""

import uuid
from datetime import datetime
from typing import Dict

from flask_sqlalchemy.model import Model


class TestRoleModel:
    """Test suite for the Role model's methods"""

    def test_model_exists(self, models: Dict[str, Model]):
        """Test case to assert that the Role model exists

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        assert "Role" in models

    def test_model_has_correct_fields(self, models: Dict[str, Model]):
        """Test case to assert that the Role model has the correct fields

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        model = models["Role"]
        assert hasattr(model, "id")
        assert hasattr(model, "created_at")
        assert hasattr(model, "role_name")
        assert hasattr(model, "is_enabled")
        assert hasattr(model, "user_id")

    def test_model_has_correct_relationships(self, models: Dict[str, Model]):
        """Test case to assert that the Role model has the correct relationships

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        model = models["Role"]

    def test_model_has_correct_attribute_types(self, mock_role: Model):
        """Test case to assert that the Role model has the correct attribute types

        Args:
            mock_role (Model): Mock Role
        """
        assert isinstance(mock_role.id, uuid.UUID)
        assert isinstance(mock_role.created_at, datetime)
        assert isinstance(mock_role.role_name, str)
        assert isinstance(mock_role.is_enabled, bool)
        assert isinstance(mock_role.user_id, uuid.UUID)

    def test_model_has_correct_relationship_types(self, mock_role: Model):
        """Test case to assert that the Role model has the correct
        relationship types

        Args:
            mock_role (Model): Mock Role
        """
        assert isinstance(mock_role.user, object)
